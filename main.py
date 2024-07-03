from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy


import os

current_dir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = 'static/'



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "database.sqlite3")
db = SQLAlchemy()
db.init_app(app)
#ensures that application context sets correctly for the database
app.app_context().push()

from controller import *


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)

    
