
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import random, string 

Base = declarative_base()

class Category(Base): 
    __tablename__ = 'category' 

    id = Column(Integer, primary_key=True) 
    name = Column(String(255), nullable=False) 

    @property 
    def serialize(self): 
        return {
            'id': self.id, 
            'name': self.name 
        }

class User(Base): 
    __tablename__ = 'user' 

    id = Column(Integer, primary_key=True) 
    name = Column(String(255), nullable=False) 
    email = Column(String(255), nullable=False) 

    def generate_auth_token(self, expiration=600): 
        s = Serializer

class Item(Base): 
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True) 
    name = Column(String(255), nullable=False)  
    description = Column(String(1024)) 
    category_id = Column(Integer, ForeignKey('category.id')) 
    user_id = Column(Integer, ForeignKey('user.id')) 
    category = relationship(Category)

    @property
    def serialize(self): 
        return { 
            'id' : self.id, 
            'name': self.name, 
            'description' : self.description, 

        }

engine = create_engine('sqlite:///itemcatalog.db') 
Base.metadata.create_all(engine)