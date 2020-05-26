import pymongo
from db.data_layer import DataLayer


class DataLayerNoCache(DataLayer):

    def get_dob(self, user_id):
        print(f'In data_layer_no_cache.py: Getting Date of birth for user id: {user_id}')
        user_dict = self.__dob.find_one({"id": user_id})
        if user_dict:
            return user_dict['dob']
        else:
            return 'No such user'

    def set_dob(self, user_id, dob):
        self.__dob.insert_one({"id": user_id, 'dob': dob})

    def delete_dob(self, user_id):
        self.__dob.delete_one({"id": user_id})
