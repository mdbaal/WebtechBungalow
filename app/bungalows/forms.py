from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms import ValidationError

from app.models import Reservation

class ReserveForm(FlaskForm):
    week_nr = SelectField('Kies een beschikbare week', coerce=int)
    submit = SubmitField('Reserveer!')

    def check_valid(self, bungalow_id, week_nr):
        if Reservation.query.filter_by(bungalow=bungalow_id, week=week_nr).first():
            raise ValidationError('Deze bungalow is al voor deze week gereserveerd, probeer een andere bungalow of week!')