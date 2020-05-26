from flask import Flask
from flask import request
import pymongo
import os
import random

OFFSET_OF_IDs = 5


class DataLayer:

    def get_dob(self, user_id):
        print(f'DB: Getting Date of birth for user id: {user_id}')
        user_dict = self.__dob.find_one({"id": user_id})
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

    def __init__(self):
        client = pymongo.MongoClient(os.environ.get('MONGODB_URI'), retryWrites=False)

        db = client.get_default_database()
        self.__dob = db["dates_of_birth"]


app = Flask(__name__)
data_layer = DataLayer()


@app.route("/dob/<string:user_id>", methods=['GET', 'PUT', 'DELETE'])
def dob(user_id):
    if request.method == 'GET':
        print(f'API: Getting Date of birth for user id: {user_id}')
        dob = data_layer.get_dob(user_id)
        return str(dob)
    elif request.method == 'PUT':
        dob = request.args.get('dob')
        data_layer.set_dob(user_id, dob)
        return 'OK'
    else:
        #  DELETE DOB
        data_layer.delete_dob(user_id)
        return 'OK'


@app.route("/populate_db", methods=['POST'])
def populate_db():
    data_layer.populate_db(int(request.args.get('num_dobs')))
    return 'OK'


if __name__ == "__main__":
    # Heroku provides environment variable 'PORT' that should be listened on by Flask
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))
