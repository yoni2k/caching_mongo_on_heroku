import pymongo
import os
from flask_caching import Cache


class DataLayerSetGet:

    def get_dob(self, user_id):
        dob = self.__cache.get(user_id)
        if dob:
            print(f'In DB: Getting Date of birth for user id FROM CACHE: {user_id}')
            return dob
        else:
            print(f'In DB: Getting Date of birth for user id FROM DB: {user_id}')
            user_dict = self.__dob.find_one({"id": user_id})
            if user_dict:
                ans = user_dict['dob']
            else:
                ans = 'No such user'
            self.__cache.set(user_id, ans)

    def set_dob(self, user_id, dob):
        self.__cache.set(user_id, dob)
        self.__dob.insert_one({"id": user_id, 'dob': dob})

    def delete_dob(self, user_id):
        self.__cache.delete(user_id)
        self.__dob.delete_one({"id": user_id})

    def __init__(self, cache):
        client = pymongo.MongoClient(os.environ.get('MONGODB_URI'), retryWrites=False)

        db = client.get_default_database()
        self.__dob = db["dates_of_birth"]
        self.__cache = cache
