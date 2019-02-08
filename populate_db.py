from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from models import Base, User, Category, Item 

engine = create_engine('sqlite:///itemcatalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

print "Adding users..."
session.add(User(name="Joseph Liguid", email="liguidjoseph@gmail.com")) 
session.flush() 
session.commit() 
session.add(User(name="Keith Lindam", email="saajawea3@gmail.com")) 
session.flush() 
session.commit() 

print "Adding categories..."
# Add categories
category1 = Category(name='Snowboarding') 
session.add(category1) 
session.commit() 

category2 = Category(name='Baseball') 
session.add(category2) 
session.commit() 

category3 = Category(name='Tennis') 
session.add(category3) 
session.commit() 

print "Adding items..."
# Add items 
item1 = Item(name='Snowboard', description='Board used for snowboarding', 
             category=category1, user_id=1)
session.add(item1) 
session.commit() 

item2 = Item(name='Snowboard Bindings', description='Attach the feet of the snowboarder to the snowboard',
             category=category1, user_id=1) 
session.add(item2) 
session.commit() 

item3 = Item(name='Snowboard Goggles', description='Help protect snowboarders eyes from snow blindness and snow',
             category=category1, user_id=2) 
session.add(item3) 
session.commit() 

item4 = Item(name='Baseball Bat', description='Bat used to hit the baseball. Can be wooden or typically aluminum',
             category=category2, user_id=2) 
session.add(item4) 
session.commit() 

item5 = Item(name='Baseball Gloves', description='Oversized leather glove used to catch baseballs.',
             category=category2, user_id=1) 
session.add(item5) 
session.commit() 

item6 = Item(name='Tennis Raquet', description='Raquet for hitting tennis balls',
             category=category3, user_id=1) 
session.add(item6) 
session.commit() 

print "Finished populating database" 