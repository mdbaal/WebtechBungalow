from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from sqlalchemy import Column, Integer, String, ForeignKey

class Bungalow_Type(db.Model):
    __tablename__ = 'bungalow_type'
    id = Column(Integer, primary_key=True)
    size = Column(Integer)
    week_price = Column(Integer)

    def __init__(self, size, week_price):
        self.size = size
        self.week_price = week_price

    def _repr__(self):
        return f"Id: {self.id} Size: {self.size} Week-Price: {self.week_price}"

class Bungalow(db.Model):
    __tablename__ = 'bungalow'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    gallery = Column(String)
    type = Column(Integer, ForeignKey('bungalow_type.id'))

    def __init__(self, name, type, gallery):
        self.name = name
        self.type = type
        self.gallery = gallery

    def _repr__(self):
        return f"Bungalow: {self.naam} Type: {self.type} Gallery: {self.gallery}"


class Guest(db.Model, UserMixin):
    __tablename__ = "guest"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    password = Column(String, unique=True)

    def __init__(self, name, password):
        self.name = name
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @login_manager.user_loader
    def load_user(user_id):
        return Guest.query.get(user_id)

    def _repr__(self):
        return f"Guest: {self.id} Name: {self.name}"


class Reservation(db.Model):
    __tablename__ = "reservation"
    id = Column(Integer, primary_key=True)
    guest = Column(Integer, ForeignKey('guest.id'))
    bungalow = Column(Integer, ForeignKey('bungalow.id'))
    week = Column(Integer)

    def __init__(self, guest, bungalow, week):
        self.guest = guest
        self.bungalow = bungalow
        self.week = week

    def _repr__(self):
        return f"Reservation: {self.id} Guest: {self.guest} Bungalow: {self.bungalow} Week: {self.week}"