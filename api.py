from flask import Flask
from db.data_layer import DataLayer
import os

app = Flask(__name__)

dataLayer = DataLayer()


@app.route("/get_year_of_birth/<string:user_id>")
def get_year_by_id(user_id):
    user_year_of_birth = dataLayer.get_year_of_birth_by_id(user_id)
    return user_year_of_birth


@app.route("/populate_db")
def populate_db(user_id):
    dataLayer.populate_db()
    return 'DB populated'


if __name__ == "__main__":
    # Heroku provides environment variable 'PORT' that should be listened on by Flask
    port = os.environ.get('PORT')

    if port:
        app.run(host='0.0.0.0', port=int(port))
    else:
        app.run()
