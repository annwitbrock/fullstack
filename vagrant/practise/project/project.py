from flask import (Flask, render_template, url_for, request, redirect, flash, jsonify)
app = Flask(__name__)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

#API endpoint (GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
    #ignores the restaurant id
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    #doesn't handle unknown menu_id
    return jsonify(MenuItem=item.serialize)
    
    
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)

#Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        itemname = newItem.name
        session.add(newItem)
        session.commit()
        flash('New menu item %s created' % itemname)
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)

#Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, MenuID):
    editedItem = session.query(MenuItem).filter_by(id = MenuID).one()
    itemname = editedItem.name
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash('Menu item %s edited to %s' % (itemname, editedItem.name))
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        #USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLE NAMES YOU SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, MenuID = MenuID, item = editedItem)

#Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deleteItem = session.query(MenuItem).filter_by(id = menu_id).one()
    itemname = deleteItem.name
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        flash('Menu item %s deleted' % itemname)
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant_id = restaurant_id, item = deleteItem)


if __name__ == '__main__':
    app.secret_key = 'notsosecretkey'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)