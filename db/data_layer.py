import pymongo
import os
import random


class DataLayer:

    def get_year_of_birth_by_id(self, user_id):
        user_dict = self.__dob.find_one({"id": user_id})
        return user_dict['year_of_birth']

    def populate_db(self):
        # delete everything existing
        self.__dob.drop()

        dob_info = [{'id': str(i), 'year_of_birth': random.randint(1920, 2020)} for i in range(10000)]
        self.__dob.insert_many(dob_info)

        # for i in range(10000):
        #     dob_info = {'id': str(i), 'year_of_birth': 1950}
        #     self.__dob.insert_many(dob_info)

    def __init__(self):
        mongo_uri = os.environ.get('MONGODB_URI')

        if mongo_uri:
            client = pymongo.MongoClient(mongo_uri, retryWrites=False)
        else:
            # running locally, not on Heroku (or MongoDB was not added as AddOn)
            client = pymongo.MongoClient(mongo_uri, 27017)

        db = client.get_default_database()
        self.__dob = db["years_of_birth"]
