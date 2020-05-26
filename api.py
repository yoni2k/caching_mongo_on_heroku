from flask import Flask
from flask import request
from db.data_layer import DataLayer
# from db.data_layer_with_cache import DataLayerWithCache
import os

app = Flask(__name__)

use_cache = False

# if use_cache:
#     dataLayer = DataLayerWithCache()
# else:
dataLayer = DataLayer()


@app.route("/dob_vars/<string:user_id>", methods=['GET', 'PUT', 'DELETE'])
def dob_vars(user_id):
    """
    Handle Date of birth info (year of birth).
    :param user_id:  Id of the user whose Date of birth we want to get / set / delete
    :return:
        In case of GET, return the year of birth. Otherwise return 'OK' on success
    """
    if request.method == 'GET':
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
    dataLayer.populate_db(request.args.get('num_dobs'))
    return 'OK'


if __name__ == "__main__":
    # Heroku provides environment variable 'PORT' that should be listened on by Flask
    port = os.environ.get('PORT')

    if port:
        app.run(host='0.0.0.0', port=int(port))
    else:
        app.run()
