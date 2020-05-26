from flask import Flask
from flask import request
import os

from api_no_cache import DataLayer

# For caching
from flask_caching import Cache


app = Flask(__name__)

# For caching
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

data_layer = DataLayer()


@cache.memoize(30)
def get_dob(user_id):
    return str(data_layer.get_dob(user_id))


@app.route("/dob/<string:user_id>", methods=['GET', 'PUT', 'DELETE'])
def dob(user_id):
    if request.method == 'GET':
        print(f'API: Getting Date of birth for user id: {user_id}')
        return get_dob(user_id)
    elif request.method == 'PUT':
        cache.delete_memoized(get_dob, user_id)

        dob = request.args.get('dob')
        data_layer.set_dob(user_id, dob)
        return 'OK'
    else:
        # DELETE DOB
        cache.delete_memoized(get_dob, user_id)

        data_layer.delete_dob(user_id)
        return 'OK'


if __name__ == "__main__":
    # Heroku provides environment variable 'PORT' that should be listened on by Flask
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))
