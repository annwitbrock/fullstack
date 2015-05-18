from flask import Flask
#from flask import (Flask, render_template, url_for, request, redirect, flash, jsonify)

app = Flask(__name__)

### to do:  replace these with database as required
###         see sqlalchemy for that
#Fake Categories
category = {'name': 'Category 1', 'id': '1'}
categories = [  {'name': 'Category 1', 'id': '1'},
                {'name': 'Category 2', 'id': '2'},
                {'name': 'Category 3', 'id': '3'}]

#Fake Products
product = {'name': 'Product A', 'id': '1'}
products = [{'name': 'Product A', 'id': '1'},
            {'name': 'Product B', 'id': '2'},
            {'name': 'Product C', 'id': '3'}]

###



@app.route('/')
@app.route('/categories/')
def showCategories():
    return "show all categories"

@app.route('/category/new/', methods=['GET','POST'])
def newCategory():
    return "add category"
    
@app.route('/category/<int:category_id>/edit/', methods=['GET','POST'])
def editCategory(category_id=1):
    return "edit category %s" %(category_id)

@app.route('/category/<int:category_id>/delete/', methods=['GET','POST'])
def deleteCategory(category_id=1):
    return "delete category %s" %(category_id)
    
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/product/')
def showproduct(category_id=1):
    return "category %s show products"  %(category_id,)

@app.route('/category/<int:category_id>/product/new/', methods=['GET','POST'])
def addproductItem(category_id=1):
    return "category %s add product " %(category_id,)
    
@app.route('/category/<int:category_id>/product/<int:product_id>/edit/', methods=['GET','POST'])
def editproductItem(category_id=1, product_id=1):
    return "category %s edit product %s" %(category_id, product_id)
    
@app.route('/category/<int:category_id>/product/<int:product_id>/delete/', methods=['GET','POST'])
def deleteproductItem(category_id=1, product_id=1):
    return "category %s delete product item %s" %(category_id, product_id)



if __name__ == '__main__':
#    app.secret_key = 'notsosecretkey'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)