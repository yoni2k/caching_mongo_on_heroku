from flask import Flask
from flask import request
import os

from api_no_cache import DataLayer

# For caching
from flask_caching import Cache

app = Flask(__name__)
data_layer = DataLayer()

# For caching
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)


@app.route("/dob/<string:user_id>", methods=['GET', 'PUT', 'DELETE'])
@cache.cached(timeout=30)
def dob_cache_api(user_id):
    if request.method == 'GET':
        print(f'In apy.py: Getting Date of birth for user id: {user_id}')
        dob = data_layer.get_dob(user_id)
        return str(dob)
    elif request.method == 'PUT':
        dob = request.args.get('dob')
        data_layer.set_dob(user_id, dob)
        return 'OK'
    else:
        #  DELETE date
        data_layer.delete_dob(user_id)
        return 'OK'


@app.route("/populate_db", methods=['POST'])
def populate_db():
    data_layer.populate_db(int(request.args.get('num_dobs')))
    return 'OK'


if __name__ == "__main__":
    # Heroku provides environment variable 'PORT' that should be listened on by Flask
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))

