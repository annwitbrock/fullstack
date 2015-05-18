from flask import (Flask, render_template, url_for, request, redirect, flash, jsonify)
import finalRestaurant as rdb
import finalMenuItem as mdb

app = Flask(__name__)

###
##Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

# restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


##Fake Menu Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]

# item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}
###

restaurant = {'id': '0'}
restaurants = []
item = {'id': '0'}
items = []


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    #return "show all restaurants"
    return render_template('restaurants.html', restaurants=rdb.restaurants())

@app.route('/restaurant/new/', methods=['GET','POST'])
def newRestaurant():
    #return "add restaurant"
    if request.method == 'POST':
        name = request.form['name']
        rdb.addNewRestaurant(name)
        flash('New restaurant %s created' % name)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html' )
    
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET','POST'])
def editRestaurant(restaurant_id=1):
    #return "edit restaurant %s" %(restaurant_id)
    if request.method == 'POST':
        name = request.form['name']
        rdb.editRestaurantById(restaurant_id, name)
        flash('Restaurant %s edited' % name)
        return redirect(url_for('showRestaurants'))
    else:
        restaurant = rdb.restaurantById(restaurant_id)
        return render_template('editRestaurant.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id=1):
    #return "delete restaurant %s" %(restaurant_id)
    restaurant = rdb.restaurantById(restaurant_id)
    if request.method == 'POST':
        rdb.deleteRestaurantById(restaurant_id)
        flash('Restaurant %s deleted' % restaurant.name)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant=restaurant)
    
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id=1):
    #return "restaurant %s show menu"  %(restaurant_id,)
    restaurant = rdb.restaurantById(restaurant_id)
    items = mdb.restaurantMenu(restaurant_id)
    return render_template('menu.html', restaurant=restaurant, items=items)

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id=1):
    #return "restaurant %s add menuitem " %(restaurant_id,)
    if request.method == 'POST':
        name = request.form['name']
        mdb.addNewMenuItem(restaurant_id, name)
        flash('New menu item %s created' % name)
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        restaurant = rdb.restaurantById(restaurant_id)
        return render_template('newMenuItem.html', restaurant=restaurant)
    
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id=1, menu_id=1):
    #return "restaurant %s edit menu item %s" %(restaurant_id, menu_id)
    item = mdb.menuItemById(menu_id)
    if request.method == 'POST':
        mdb.editMenuItemById(menu_id, request.form)
        flash('Menu item %s edited' % (item.name))
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        restaurant = rdb.restaurantById(restaurant_id)
        return render_template('editMenuItem.html', restaurant=restaurant, menu_id=menu_id, item=item)
    
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id=1, menu_id=1):
    #return "restaurant %s delete menu item %s" %(restaurant_id, menu_id)
    if request.method == 'POST':
        itemname = mdb.menuItemById(menu_id).name
        mdb.deleteMenuItemById(menu_id)
        flash('Menu item %s deleted' % itemname)
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        restaurant = rdb.restaurantById(restaurant_id)
        item = mdb.menuItemById(menu_id)
        return render_template('deleteMenuItem.html', restaurant=restaurant, menu_id=menu_id, item=item)



if __name__ == '__main__':
    app.secret_key = 'notsosecretkey'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)