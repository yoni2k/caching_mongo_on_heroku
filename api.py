from flask import Flask
from db.data_layer import DataLayer
import os

app = Flask(__name__)

dataLayer = DataLayer()


@app.route("/user_year_of_birth/<string:user_id>")
def get_user_by_id(user_id):
    user_year_of_birth = dataLayer.get_year_of_birth_by_id(user_id)
    return user_year_of_birth


if __name__ == "__main__":
    # Heroku provides environment variable 'PORT' that should be listened on by Flask
    port = os.environ.get('PORT')

    if port:
        app.run(host='0.0.0.0', port=int(port))
    else:
        app.run()
