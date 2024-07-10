from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash




import os

current_dir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = 'static/'



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "database.sqlite3")
db = SQLAlchemy()
db.init_app(app)
#ensures that application context sets correctly for the database
app.app_context().push()
app.secret_key='dfgdxferg'
from controller import *
from model import *

if __name__ == "__main__":

    with app.app_context():
        db.create_all()
        user=Register.query.filter_by(role='admin').first()
        if not user:
            user=Register(role='admin',username='admin',email='admin@admin',password=generate_password_hash("admin"))
            db.session.add(user)
            db.session.commit()
    app.run(debug=True)


