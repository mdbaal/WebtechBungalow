import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Create app
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mijngeheimesleutel'

# Setup database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from app.models import Bungalow_Type, Bungalow

@app.before_first_request
def before_first_request_func():

    # Maak de tabel(len) aan in de database
    db.create_all()

    # Create bungalow types
    if not Bungalow_Type.query.filter_by(size=4).first():
        db.session.add(Bungalow_Type(4, 485))
    if not Bungalow_Type.query.filter_by(size=6).first():
        db.session.add(Bungalow_Type(6, 567))
    if not Bungalow_Type.query.filter_by(size=8).first():
        db.session.add(Bungalow_Type(8, 726))

    # Save to the database
    db.session.commit()

    # Create bungalows
    type_x = Bungalow_Type.query.filter_by(size=4).first().id
    if not Bungalow.query.filter_by(type=type_x).first():
        db.session.add(Bungalow("Homeless", type_x, "4p_scandinavische_bungalow"))
    type_x = Bungalow_Type.query.filter_by(size=6).first().id
    if not Bungalow.query.filter_by(type=type_x).first():
        db.session.add(Bungalow("Broke", type_x, "6p_veluwse_bungalow"))
    type_x = Bungalow_Type.query.filter_by(size=8).first().id
    if not Bungalow.query.filter_by(type=type_x).first():
        db.session.add(Bungalow("Rich", type_x, "8p_luxe_bungalow"))

    # Save to the database
    db.session.commit()

    # Checken of de ID's zijn toegevoegd.
    print(Bungalow_Type.query.all())
    print(Bungalow.query.all())