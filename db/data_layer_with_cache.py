import pymongo
import os
import random
from flask_caching import Cache

cache_config = {
    "DEBUG": True,           # some Flask specific configs
    "CACHE_TYPE": "simple",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

OFFSET_OF_IDs = 5


class DataLayerWithCache:

    def get_dob(self, user_id):
        user_dict = self.__dob.find_one({"id": user_id})
        print(f'Getting user info: {user_id}')
        if user_dict:
            return user_dict['dob']
        else:
            return 'No such user'

    def set_dob(self, user_id, dob):
        self.__dob.insert_one({"id": user_id, 'dob': dob})

    def delete_dob(self, user_id):
        self.__dob.delete_one({"id": user_id})

    def populate_db(self, num_entries):
        # delete everything existing
        self.__dob.drop()

        dob_infos = [
            {'id': str(i),
             'dob': random.randint(1920, 2020)}
            for i in range(OFFSET_OF_IDs, num_entries + OFFSET_OF_IDs)]
        self.__dob.insert_many(dob_infos)

    def __init__(self, cache):
        mongo_uri = os.environ.get('MONGODB_URI')

        if mongo_uri:
            client = pymongo.MongoClient(mongo_uri, retryWrites=False)
        else:
            # running locally, not on Heroku (or MongoDB was not added as AddOn)
            client = pymongo.MongoClient(mongo_uri, 27017)

        db = client.get_default_database()
        self.__dob = db["dates_of_birth"]
        self.__cache = cache