from flask import Blueprint, render_template, flash
from app import app

bp_root = Blueprint(
    'root',
    __name__,
    template_folder="templates",
    url_prefix='/')

@bp_root.route("/")
def index():
    return render_template("index.html")