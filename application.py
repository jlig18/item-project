import json 
from flask import Flask, jsonify, request, url_for, abort, g, render_template, redirect
from models import Base, Category, Item, User 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

''' TODO successful update: Add message indicating sucess
    TODO non existant data: Add message and redirect back one page'''

engine = create_engine('sqlite:///itemcatalog.db', connect_args={'check_same_thread': False}) 

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/')
def index(): 
    categories = session.query(Category).all() 
    last_items = session.query(Item).order_by('Item.id desc').limit(10).all() 
    return render_template('index.html', categories=categories, items=last_items)  

@app.route('/<category>/')
def showcategory(category): 
    db_category = session.query(Category).filter_by(name=category).first()
    if db_category is not None:
        items = session.query(Item).filter_by(category_id=db_category.id).all() 
        return render_template('showcategory.html', category_name=db_category.name, items=items) 
    else:
        return redirect('/')  # TODO non existent

# @app.route('/<category>/new/', methods=['POST', 'GET'])
# def newCategory(): 
#     if request.method == 'GET': 
#         return render_template('newcategory.html')

@app.route('/<category>/<item>/') 
def showitem(category, item): 
    db_category = session.query(Category).filter_by(name=category).first() 
    item = session.query(Item).filter_by(name=item.replace('_',' '), category_id=db_category.id).first() 
     # if both category and item are in the database render template
    if db_category is not None and item is not None: 
        return render_template('item.html', item=item)
    else:
        return redirect('/')  # TODO non existent

@app.route('/new/', methods=['POST', 'GET'])
def newItem():
    categories = session.query(Category).all() 
    if request.method == 'GET': 
        return render_template('newitem.html', categories=categories)
    elif request.method == 'POST': 
        name = request.form['item_name'] 
        description = request.form['item_desc'] 
        category_id = session.query(Category).filter_by(name=request.form['category']).first()
        # TODO: Get user_id from logged in user 
        newItem = Item(name=name, description=description, category_id=category_id.id, user_id=1) 
        session.add(newItem)
        session.commit() 
        return redirect('/') # TODO successful update

@app.route('/<category>/<item>/delete/', methods=['POST', 'GET'])
def deleteItem(category, item):
    db_category = session.query(Category).filter_by(name=category).first() 
    item = session.query(Item).filter_by(name=item.replace('_', ' '), category_id=db_category.id).first() 
    if request.method == 'GET': 
        return render_template('deleteitem.html', item=item) 
    elif request.method =='POST': 
        if request.form['button'] == 'Confirm': 
            session.delete(item) 
            session.commit() 
            return redirect('/') 
            # TODO successful update
        else: 
            return redirect('/') 
        return redirect('/') # TODO non existent

if __name__ == '__main__':
    app.debug = True
    #app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    app.run(host='0.0.0.0', port=8000)