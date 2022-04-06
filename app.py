import os
from flask import Flask, Blueprint
from app import db
from app.models import Bungalow
# Createe app
app = Flask(__name__,root_path="app/")

# Setup database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_db()



# Index
from app import view
app.register_blueprint(view.bp)

from app.bungalows import views
app.register_blueprint(views.bp_bungalows, url_prefix="/bungalows")

if __name__ == "__main__":
    app.run(debug=True)