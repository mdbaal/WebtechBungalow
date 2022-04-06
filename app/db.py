import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

base = declarative_base()
db = create_engine('sqlite:///database.sqlite')
session = sessionmaker(db)()
    
def init_db():
    base.metadata.create_all(db)
    



