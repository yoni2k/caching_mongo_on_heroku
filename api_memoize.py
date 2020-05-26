from flask import Flask
from flask import request
import os

from api_no_cache import DataLayer

# For caching
from flask_caching import Cache


class DataLayer:

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
        return get_dob_internal(user_id)

    def set_dob(self, user_id, dob):
        self.__dob.insert_one({"id": user_id, 'dob': dob})

    def delete_dob(self, user_id):
        self.__cache.delete_memoized(self.get_dob.get_dob_internals, user_id)
        self.__dob.delete_one({"id": user_id})

    def __init__(self, cache):
        super().__init__()
        self.__cache = cache


app = Flask(__name__)

# For caching
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

data_layer = DataLayer(cache)


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
        # DELETE DOB
        data_layer.delete_dob(user_id)
        return 'OK'


if __name__ == "__main__":
    # Heroku provides environment variable 'PORT' that should be listened on by Flask
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))
