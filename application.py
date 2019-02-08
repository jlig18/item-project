import json 
from Flask import Flask, jsonify, request, url_for, abort, g, render_template
from models import Base, Category, Item, User 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///itemcatalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/')
def index(): 
    categories = session.query(Category).all() 
    items = session.query(Item).order_by('Item.id desc').limit(10).all() 
    render_template('index.html', categories=categories, items=items)  

@app.route('/<category')
def showcategory(category): 
    db_category = session.query(Category).filter_by(name=category).first()
    items = session.query(Item).filter_by(category_id=db_category.id).all() 
    render_template('showcategory.html', category_name=category, items=items) 


if __name__ == '__main__':
    app.debug = True
    #app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    app.run(host='0.0.0.0', port=8000)