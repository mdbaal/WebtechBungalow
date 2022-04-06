from ast import In
from enum import unique
import app.db as db

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Bungalow_Type(db.base):
    __tablename__ = 'bungalow_types'
    id = Column(Integer,primary_key=True)
    size = Column(Integer)
    week_price = Column(Integer)

class Bungalow(db.base):
    __tablename__ = 'bungalows'
    id = Column(Integer,primary_key=True)
    naam = Column(String)
    type = Column(Integer, ForeignKey('bungalow_types.id'))
    user = relationship("Bungalow_Type", back_populates="bungalows")

    def __init__(self, naam,type):
        self.naam = naam
        self.type = type


    def _repr__(self):
        return f"Bungalow: {self.naam} Type: {self.type}"


class Guest(db.base):
    __tablename__ = "guests"
    id = Column(Integer,primary_key=True)
    gebruikersnaam = Column(String, unique=True)
    wachtwoord = Column(String, unique=True)


class Boeking(db.base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    guest_id = Column(Integer, ForeignKey('guests.id'))
    start_week = Column(Integer)


# ! todo add innit and repr to other models