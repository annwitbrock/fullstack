#!/usr/bin/env python
#
# Test cases for restaurant.py

from restaurant import *

def testGetRestaurants():
    r = restaurants()
    if len(r) == 0:
        raise ValueError("No Restaurants found")
    print "%d Restaurants were found." % (len(r),)
    
def testGetRestaurantNames():
    name = u'Pizza Palace'
    r = restaurantNames()
    if name not in r:
        print "Restaurants found:\n", r
        raise ValueError("Restaurant name not found")
    print "Restaurant %s was found." % (name,)
    
# def testRestaurantByName():
    # name = u'Pizza Palace'
    # id = restaurantByName(name)
    # if id != 0:
        # raise ValueError("Restaurant not found by name")
    # print "Restaurant %s had ID %d." % (name, id)

def testRestaurantById():
    name = u'Pizza Palace'
    found = restaurantById("1")
    if found.name != name:
        raise ValueError("Restaurant ID not found")
    print "Restaurant %s had ID %d." % (found.name, found.id)
    
def testAddNewRestaurant():
    name = u'Fab New Restaurant'
    addNewRestaurant(name)

    r = restaurantNames()
    if name not in r:
        print "Restaurants found:\n", r
        raise ValueError("Added restaurant name not found")
    print "Restaurant %s was added." % (name,)

def testDeleteRestaurantById():
    name = u'Fab New Restaurant'
    deleteRestaurantById("20")

    r = restaurantNames()
    if name in r:
        print "Restaurant found:\n", r
        raise ValueError("Restaurant not deleted")
    print "Restaurant %s was deleted." % (name,)

def testDeleteRestaurantByName():
    name = u'Fab New Restaurant'
    deleteRestaurantByName(name)

    r = restaurantNames()
    if name in r:
        print "Restaurant found:\n", r
        raise ValueError("Restaurant not deleted")
    print "Restaurant %s was deleted." % (name,)
    
def testEditRestaurant():
    name = u'Pizza Palace'
    newname = u'Edited Restaurant'
    id = "1"
    editRestaurantById(id, newname)

    r = restaurantNames()
    if name in r:
        print "Restaurant found:\n", r
        raise ValueError("Original restaurant name found")
    if newname not in r:
        print "Restaurant found:\n", r
        raise ValueError("Edited restaurant name not found")
    print "Restaurant %s was edited to %s." % (name, newname)

if __name__ == '__main__':
    print "Starting tests"
    #testGetRestaurants()
    #testGetRestaurantNames()
    #testAddNewRestaurant()
    #testRestaurantById()
    #testEditRestaurant()
    #testDeleteRestaurantById()
    testDeleteRestaurantByName()
    print "Success! All tests pass!"