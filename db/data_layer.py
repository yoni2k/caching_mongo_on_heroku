import pymongo
import os
import random

OFFSET_OF_IDs = 5


class DataLayer:

    def populate_db(self, num_entries):
        # delete everything existing
        self.__dob.drop()

        dob_infos = [
            {'id': str(i),
             'dob': random.randint(1920, 2020)}
            for i in range(OFFSET_OF_IDs, num_entries + OFFSET_OF_IDs)]
        self.__dob.insert_many(dob_infos)

    def __init__(self):
        client = pymongo.MongoClient(os.environ.get('MONGODB_URI'), retryWrites=False)

        db = client.get_default_database()
        self.__dob = db["dates_of_birth"]
