import pymongo
from flask_caching import Cache
from db.data_layer import DataLayer


class DataLayerWithMemoize(DataLayer):

    def get_dob(self, user_id):
        @self.__cache.memoize(30)
        def get_dob_internal(user_id):
            print(f'In data_layer_with_memoize.py INTERNAL: Getting Date of birth for user id: {user_id}')
            user_dict = self.__dob.find_one({"id": user_id})
            if user_dict:
                return user_dict['dob']
            else:
                return 'No such user'

        print(f'In data_layer_with_memoize.py EXTERNAL: Getting Date of birth for user id: {user_id}')
        get_dob_internal(user_id)

    def set_dob(self, user_id, dob):
        self.__dob.insert_one({"id": user_id, 'dob': dob})

    def delete_dob(self, user_id):
        self.__cache.delete_memoized(self.get_dob.get_dob_internals, user_id)
        self.__dob.delete_one({"id": user_id})

    def __init__(self, cache):
        super().__init__()
        self.__cache = cache
