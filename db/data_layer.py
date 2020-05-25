import pymongo
from bson import ObjectId

import os


class DataLayer:

    def get_year_of_birth_by_id(self, user_id):
        user_dict = self.__db.users.find_one({"_id": ObjectId(user_id)})
        return user_dict['year_of_birth']

    def __init__(self):
        mongo_uri = os.environ.get('MONGODB_URI')

        if mongo_uri:
            self.__client = pymongo.MongoClient(mongo_uri)
        else:
            # running locally, not on Heroku (or MongoDB was not added as AddOn)
            self.__client = pymongo.MongoClient(mongo_uri, 27017)

        self.__db = self.__client["music"]
