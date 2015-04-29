#!/usr/bin/env python
#
# restaurant.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

def db_session():
    engine = create_engine('sqlite:///restaurantMenu.db')
    Base.metadata.bind=engine
    DBSession = sessionmaker(bind = engine)
    return DBSession()

def restaurants():
    session = db_session()
    restaurants = session.query(Restaurant).all()
    return restaurants
    
def restaurantNames():
    return [r.name for r in restaurants()]
    
def restaurantById(id):
    session = db_session()
    restaurant = session.query(Restaurant).filter_by(id=id).one()
    return restaurant

def restaurantByName(name):
    pass #return 0
    
def addNewRestaurant(restaurant_name):
    session = db_session()
    restaurant = Restaurant(name = restaurant_name)
    session.add(restaurant)
    session.commit()

def editRestaurantById(id, newname):
    session = db_session()
    restaurant = session.query(Restaurant).filter_by(id=id).one()
    restaurant.name = newname
    session.add(restaurant)
    session.commit()
    
def deleteRestaurantById(id):
    session = db_session()
    restaurant = session.query(Restaurant).filter_by(id=id).one()
    session.delete(restaurant)
    session.commit()
    
def deleteRestaurantByName(name):
    session = db_session()
    restaurant = session.query(Restaurant).filter_by(name=name).first()
    session.delete(restaurant)
    session.commit()