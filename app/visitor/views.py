import app
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, logout_user, login_user
from app import login_manager

from app import db
from app.visitor.forms import RegistrationForm, LoginForm
from app.models import Guest, Reservation, Bungalow, Bungalow_Type

from datetime import date

bp_visitor = Blueprint(
    'visitor',
    __name__,
    template_folder='templates',
    url_prefix='/visitor'
)

@bp_visitor.route("/reservations")
@login_required
def reservations():
    data = db.session.query(Reservation.week.label('week'), Bungalow.name.label('name'), Bungalow_Type.size.label('capacity')).\
        join(Bungalow, Bungalow.id == Reservation.bungalow).\
        join(Bungalow_Type, Bungalow_Type.id == Bungalow.type).\
        filter(Reservation.guest == current_user.id).\
        order_by(Reservation.week.asc(), Reservation.bungalow.asc()).\
        all()
    return render_template("reservations.html", reservation_data = data)

@bp_visitor.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Je bent nu uitgelogd!', 'info')
    return redirect(url_for('root.index'))

@bp_visitor.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if not form.check_username():
            flash('Deze gebruikersnaam is al vergeven, probeer een ander naam!', 'danger')
            return render_template('register.html', form=form)
        if not form.check_password():
            flash('Uw bevestigingswachtwoord komt niet overeen met uw opgegeven wachtwoord!', 'danger')
            return render_template('register.html', form=form)

        visitor = Guest(name=form.username.data, password=form.password.data)

        db.session.add(visitor)
        db.session.commit()
        flash('Dank voor de registratie. Er kan nu ingelogd worden!', 'success')

        next = request.args.get('next')

        return redirect(url_for('.login', next=next))
    return render_template('register.html', form=form)

@bp_visitor.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Guest.query.filter_by(name=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Succesvol ingelogd.', 'success')

            next = request.args.get('next')

            return redirect(next or url_for('root.index'))
        else:
            flash('Inlog ongeldig.', 'danger')
    return render_template('login.html', form=form)