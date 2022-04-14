from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from app.models import Guest

class RegistrationForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    pass_confirm = PasswordField('Bevestig wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Verzenden!')

    def check_username(self):
        return not Guest.query.filter_by(name=self.username.data).first()
        
    def check_password(self):
        return self.password.data == self.pass_confirm.data

class LoginForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Inloggen')