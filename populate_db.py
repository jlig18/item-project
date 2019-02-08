from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from models import Base 


engine = create_engine('sqlite:///itemcatelog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()