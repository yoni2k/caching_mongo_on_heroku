import pymongo
from flask_caching import Cache
from db.data_layer import DataLayer


class DataLayerSetGet(DataLayer):

    def get_dob(self, user_id):
        dob = self.__cache.get(user_id)
        if dob:
            print(f'In data_layer_set_get.py: Getting Date of birth for user id FROM CACHE: {user_id}')
            return dob
        else:
            print(f'In data_layer_set_get.py: Getting Date of birth for user id FROM DB: {user_id}')
            return self.__get_dob_generic(self.__dob, user_id)

    def set_dob(self, user_id, dob):
        self.__cache.set(user_id, dob)
        self.__dob.insert_one({"id": user_id, 'dob': dob})

    def delete_dob(self, user_id):
        self.__cache.delete(user_id)
        self.__dob.delete_one({"id": user_id})

    def __init__(self, cache):
        self.__cache = cache
