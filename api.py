from flask import Flask
from flask import request
import os

from db.data_layer import DataLayer

# For caching
from flask_caching import Cache
from db.data_layer_with_cache import DataLayerWithCache

app = Flask(__name__)

use_cache = True

if use_cache:
    cache = Cache(config={'CACHE_TYPE': 'simple'})
    cache.init_app(app)
    dataLayer = DataLayerWithCache(cache)
else:
    dataLayer = DataLayer()


@app.route("/dob_vars/<string:user_id>", methods=['GET', 'PUT', 'DELETE'])
# @cache.cached(timeout=30)
def dob_vars(user_id):
    """
    Handle Date of birth info (year of birth).
    :param user_id:  Id of the user whose Date of birth we want to get / set / delete
    :return:
        In case of GET, return the year of birth. Otherwise return 'OK' on success
    """
    if request.method == 'GET':
        print(f'In apy.py: Getting Date of birth for user id: {user_id}')
        dob = dataLayer.get_dob(user_id)
        return str(dob)
    elif request.method == 'PUT':
        dob = request.args.get('dob')
        dataLayer.set_dob(user_id, dob)
        return 'OK'
    else:
        #  DELETE date
        dataLayer.delete_dob(user_id)
        return 'OK'

#
# @app.route("/dob_params", methods=['GET', 'PUT', 'DELETE'])
# def dob_params():
#     if request.method == 'GET':
#         dob = dataLayer.get_dob(request.args.get('user_id'))
#         return str(dob)
#     else:
#         # POST request
#         user_id = request.args.get('user_id')
#         dob = request.args.get('dob')
#         dataLayer.set_dob(user_id, dob)
#         return str(dob)
#     dob = dataLayer.get_year_of_birth_by_id(user_id)
#     return str(dob)


# @app.route("/dob/<string:user_id>")
# def get_add_dob(user_id):
#     user_year_of_birth = dataLayer.get_year_of_birth_by_id(user_id)
#     return str(user_year_of_birth)


@app.route("/populate_db", methods=['POST'])
def populate_db():
    dataLayer.populate_db(int(request.args.get('num_dobs')))
    return 'OK'


if __name__ == "__main__":
    # Heroku provides environment variable 'PORT' that should be listened on by Flask
    port = os.environ.get('PORT')

    if port:
        app.run(host='0.0.0.0', port=int(port))
    else:
        app.run()
