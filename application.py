import json 
from flask import Flask, jsonify, request, url_for, abort, g, render_template, redirect
from models import Base, Category, Item, User 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2

''' TODO successful update: Add message indicating sucess
    TODO non existant data: Add message and redirect back one page
    TODO temporary backend check for category when creating new item'''

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

@app.route('/glogin/'):
def login(provider):


@app.route('/<category>/')
def showcategory(category): 
    db_category = session.query(Category).filter_by(name=category.replace('_', ' ')).first()
    if db_category is not None:
        items = session.query(Item).filter_by(category_id=db_category.id).all() 
        return render_template('showcategory.html', category_name=db_category.name, items=items) 
    else:
        return redirect('/')  # TODO non existent

@app.route('/category/new/', methods=['POST', 'GET'])
def newCategory(): 
    if request.method == 'POST':
        if request.form['category_name'] is not None: 
            newCat = Category(name=request.form['category_name'])
            session.add(newCat)
            session.commit() 
            return redirect('/') 
        else:
            return redirect('/') 
    else:
        return render_template('newcategory.html')

@app.route('/<category>/delete/', methods=['POST', 'GET'])
def deleteCategory(category):
    if request.method == 'POST': 
        deletedCategory = session.query(Category).filter_by(name=category.replace('_', ' ')).first() 
        items = session.query(Item).filter_by(category_id=deletedCategory.id).delete()
        session.delete(deletedCategory)
        session.commit() 
        return redirect('/') 
    else:
        return render_template('deletecategory.html', category=category) 

@app.route('/<category>/edit/', methods=['POST', 'GET']) 
def editCategory(category):
    if request.method == 'POST': 
        if request.form['category_name'] is not None:
            editedCategory = session.query(Category).filter_by(name=category.replace('_', ' ')).first()
            editedCategory.name = request.form['category_name']
            session.add(editedCategory)
            session.commit() 
            return redirect('/')
        else:
            return redirect('/') 
    else:
        return render_template('editcategory.html', category=category) 
        

@app.route('/<category>/<item>/') 
def showitem(category, item): 
    db_category = session.query(Category).filter_by(name=category.replace('_', ' ')).first() 
    item = session.query(Item).filter_by(name=item.replace('_',' '), category_id=db_category.id).first() 
     # if both category and item are in the database render template
    if db_category is not None and item is not None: 
        return render_template('item.html', item=item)
    else:
        return redirect('/')  # TODO non existent

@app.route('/new/', methods=['POST', 'GET'])
def newItem():
    categories = session.query(Category).all() 
    if request.method == 'POST': 
        if request.form['category'] == "none":
            return redirect('/')
        name = request.form['item_name'] 
        description = request.form['item_desc'] 
        category_id = session.query(Category).filter_by(name=request.form['category']).first()
        # TODO: Get user_id from logged in user 
        newItem = Item(name=name, description=description, category_id=category_id.id, user_id=1) 
        session.add(newItem)
        session.commit() 
        return redirect('/') # TODO successful update
    else:
         return render_template('newitem.html', categories=categories)

@app.route('/<category>/<item>/edit/', methods=['POST', 'GET']) 
def editItem(category, item): 
    db_category = session.query(Category).filter_by(name=category).first() 
    currentItem = session.query(Item).filter_by(name=item.replace('_', ' '), category_id=db_category.id).first() 
    if db_category is None or item is None: 
        return redirect('/') # TODO non existent
    if request.method == 'POST': 
        print(request.form)
        updateItem = session.query(Item).filter_by(name=item.replace('_', ' '), category_id=db_category.id).first()
        if request.form['item_name']: 
            updateItem.name = request.form['item_name'] 
        if request.form['item_desc']: 
            updateItem.description = request.form['item_desc']
        newCategory = session.query(Category).filter_by(name=request.form['category']).first() 
        updateItem.category_id = newCategory.id 
        session.add(updateItem)
        session.commit() 
        return redirect('/') # TODO successful update
    else:
        categories = session.query(Category).all() 
        return render_template('edititem.html', categories=categories, item=currentItem)

@app.route('/<category>/<item>/delete/', methods=['POST', 'GET'])
def deleteItem(category, item):
    db_category = session.query(Category).filter_by(name=category).first() 
    item = session.query(Item).filter_by(name=item.replace('_', ' '), category_id=db_category.id).first() 
    if db_category is None or item is None: 
        return redirect('/') # TODO non existent
    if request.method == 'POST': 
        session.delete(item) 
        session.commit() 
        return redirect('/') 
    else: 
        return render_template('deleteitem.html', item=item) 



if __name__ == '__main__':
    app.debug = True
    #app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    app.run(host='0.0.0.0', port=8000)