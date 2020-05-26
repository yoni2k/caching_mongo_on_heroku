from flask import Flask
from flask import request
import os
import time

from db.data_layer_set_get import DataLayerSetGet

app = Flask(__name__)

data_layer = DataLayerSetGet(app)


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


@app.route("/benchmark", methods=['POST'])
def benchmark():
    threshold = data_layer.__cache_threshold

    data_layer.clear_cache()

    offset = data_layer.OFFSET_OF_IDs

    data_layer.populate_db(threshold)

    start_time = time.time()
    for i in range(offset, offset + threshold):
        data_layer.get_dob(i)
    no_cache_time = time.time() - start_time

    start_time = time.time()
    for i in range(offset, offset + threshold):
        data_layer.get_dob(i)
    with_cache_time = time.time() - start_time

    return f'Time no cache {round(no_cache_time, 2)} secs, with cache {round(with_cache_time, 2)} secs, ' + \
           f'{round(no_cache_time / with_cache_time)} times faster'


if __name__ == "__main__":
    # Heroku provides environment variable 'PORT' that should be listened on by Flask
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))
