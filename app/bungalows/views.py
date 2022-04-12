from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from app import db, app
from app.models import Bungalow, Bungalow_Type, Reservation
from app.bungalows.forms import ReserveForm
from datetime import date
import os

bp_bungalows = Blueprint(
    'bungalows',
    __name__,
    template_folder="templates",
    url_prefix="/bungalows")

@bp_bungalows.route("/offers")
def offers():
    data = db.session.query(Bungalow.id.label('id'), Bungalow.name.label('name'), Bungalow_Type.size.label('capacity'), Bungalow_Type.week_price.label('price')).\
        join(Bungalow_Type, Bungalow_Type.id == Bungalow.type).\
        all()
    return render_template("offers.html", bungalow_data = data)

@bp_bungalows.route("/reserve", methods=['GET', 'POST'])
def reserve():
    bungalow_id = request.args.get('bungalow_id')
    if not bungalow_id or bungalow_id == -1:
        flash('Selecteer alstublieft een bungalow')
        return redirect(url_for('.offers'))

    #if no signed-in user is found. Make the user register first.
    if not current_user.is_authenticated:
       return redirect(url_for('visitor.register', next=request.url))

    data = db.session.query(Bungalow.name.label('name'), Bungalow_Type.size.label('capacity'), Bungalow_Type.week_price.label('price'), Bungalow.gallery.label('gallery')).\
        join(Bungalow_Type, Bungalow_Type.id == Bungalow.type).\
        filter(Bungalow.id == bungalow_id).\
        first()

    images = os.listdir(os.path.join(app.root_path, 'static', 'images', 'bungalows', data["gallery"]))
    images = [f'images/bungalows/{data["gallery"]}/' + file for file in images]

    form = ReserveForm()

    current_week = date.today().isocalendar().week
    available_weeks = [current_week + i + 1 for i in range(5)] #Get all week numbers of 5 weeks ahead after this week.
    for reservation in Reservation.query.filter_by(bungalow=bungalow_id).all():
        try:
            available_weeks.remove(reservation.week) #Remove weeks that already have a reservation for this bungalow.
        except ValueError:
            pass
    
    form.week_nr.choices = available_weeks

    if form.validate_on_submit():
        form.check_valid(bungalow_id, form.week_nr.data)

        reservation = Reservation(current_user.id, bungalow_id, form.week_nr.data)

        db.session.add(reservation)
        db.session.commit()

        flash('Succesvol gereserveerd!')
        return redirect(url_for('visitor.reservations'))
    return render_template('offerInfo.html', form=form, bungalow_data=data, images=images)