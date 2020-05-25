import pymongo
import os


class DataLayer:

    def get_year_of_birth_by_id(self, user_id):
        user_dict = self.__db.users.find_one({"user_id": user_id})
        return user_dict['year_of_birth']

    def populate_db(self):
        for i in range(10000):
            dob_info = {'id': i, 'year_of_birth': 1950}
            self.__db.users.insert_one(dob_info)

    def __init__(self):
        mongo_uri = os.environ.get('MONGODB_URI')

        if mongo_uri:
            self.__client = pymongo.MongoClient(mongo_uri)
        else:
            # running locally, not on Heroku (or MongoDB was not added as AddOn)
            self.__client = pymongo.MongoClient(mongo_uri, 27017)

        self.__db = self.__client["years_of_birth"]
