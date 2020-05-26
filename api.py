from flask import Flask
from flask import request
import os

from db.data_layer_no_cache import DataLayerNoCache

# For caching
from flask_caching import Cache
from db.data_layer_with_memoize import DataLayerWithMemoize
from db.data_layer_set_get import DataLayerSetGet

app = Flask(__name__)

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

data_layers = {
    'no_cache': DataLayerNoCache(),
    'memoize': DataLayerWithMemoize(cache),
    'set_get': DataLayerSetGet(cache)
}


def dob_generic(user_id, req, data_layer):
    if req.method == 'GET':
        print(f'In apy.py: Getting Date of birth for user id: {user_id}')
        dob = data_layer.get_dob(user_id)
        return str(dob)
    elif req.method == 'PUT':
        dob = req.args.get('dob')
        data_layer.set_dob(user_id, dob)
        return 'OK'
    else:
        #  DELETE date
        data_layer.delete_dob(user_id)
        return 'OK'


@app.route("/dob_cache_api/<string:user_id>", methods=['GET', 'PUT', 'DELETE'])
@cache.cached(timeout=30)
def dob_cache_api(user_id):
    """
    Handle Date of birth info (year of birth).  Use caching on the API level.
    :param user_id:  Id of the user whose Date of birth we want to get / set / delete
    :return:
        In case of GET, return the year of birth. Otherwise return 'OK' on success
    """
    return dob_generic(user_id, request, data_layers['no_cache'])


@app.route("/dob/<string:user_id>", methods=['GET', 'PUT', 'DELETE'])
def dob(user_id):
    cache_type = request.args.get('cache_type')
    if cache_type == 'memoize':
        data_layer = data_layers['memoize']
    elif cache_type == 'set_get':
        data_layer = data_layers['set_get']
    else:
        data_layer = data_layers['no_cache']

    return dob_generic(user_id, request, data_layer)


@app.route("/populate_db", methods=['POST'])
def populate_db():
    data_layers['no_cache'].populate_db(int(request.args.get('num_dobs')))
    return 'OK'


if __name__ == "__main__":
    # Heroku provides environment variable 'PORT' that should be listened on by Flask
    app.run(host='0.0.0.0', port=int(port = os.environ.get('PORT')))
