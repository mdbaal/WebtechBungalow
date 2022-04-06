from flask import Blueprint, render_template

bp_bungalows = Blueprint('bungalows', __name__, template_folder="templates")

@bp_bungalows.route("/offers")
def offers():
    #temp 
   
    return render_template("offers.html", bungalow_data = {})