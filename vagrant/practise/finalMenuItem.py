#!/usr/bin/env python
#
# restaurant.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
    
# def db_session():
    # engine = create_engine('sqlite:///restaurantmenu.db')
    # Base.metadata.bind=engine
    # DBSession = sessionmaker(bind = engine)
    # return DBSession()

def menuItems():
    #session = db_session()
    menuItems = session.query(MenuItem).all()
    return menuItems
    
def menuItemNames():
    return [i.name for i in menuItems()]

def restaurantMenu(restaurant_id):
    #session = db_session()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return menuItems
    
def restaurantMenuNames(restaurant_id):
    return [i.name for i in RestaurantMenu(restaurant_id)]
    
def menuItemById(id):
    #session = db_session()
    menuItem = session.query(MenuItem).filter_by(id=id).one()
    return menuItem

# def MenuItemByName(name):
    # pass #return 0
    
def addNewMenuItem(restaurant_id, menuItem_name):
    #session = db_session()
    menuItem = MenuItem(name = menuItem_name, restaurant_id = restaurant_id)
    session.add(menuItem)
    session.commit()

def editMenuItemById(id, newItem):
    #session = db_session()
    menuItem = menuItemById(id)

    for i in newItem:
        print "Item", menuItem
        print "New Item", newItem
        print "editing item %s" % (i,)
    if newItem['name']:
            menuItem.name = newItem['name']
    session.add(menuItem)
    session.commit()
    
def deleteMenuItemById(id):
    #session = db_session()
    menuItem = menuItemById(id)
    session.delete(menuItem)
    session.commit()
    
# def deleteMenuItemByName(restaurant_id, name):
    # session = db_session()
    # menuItem = session.query(MenuItem).filter_by(name=name).first()
    # session.delete(menuItem)
    # session.commit()