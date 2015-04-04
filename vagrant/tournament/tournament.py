#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from bleach import clean

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname='tournament'")

def getData(sql):
    try:
        conn = connect()
    except:
        print "Unable to connect to database"
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    conn.close()
    return result
    
def getDataItem(sql):
    try:
        conn = connect()
    except:
        print "Unable to connect to database"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()[0]
    conn.close()
    return result

def putData(sql, data = None):
    try:
        conn = connect()
    except:
        print "Unable to connect to database"
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    conn.close()

#-----------------------------------------------

def deleteMatches():
    """Remove all the match records from the database."""
    
    SQL = "delete from matches;"
    putData(SQL)

def deletePlayers():
    """Remove all the player records from the database."""
    
    SQL = "delete from players;"
    putData(SQL)

def countPlayers():
    """Returns the number of players currently registered."""
    
    SQL = "select count(*) from players;"
    return getDataItem(SQL)

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    
    SQL = "insert into players (name) values (%s);" # unquoted token
    data = (clean(name),)      # always as a tuple
    putData(SQL, data)

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    SQL = "select * from standings;"
    result = getData(SQL)

     # replace None with zero
    standings =[(row[0], row[1], row[2] or 0, row[3] or 0) for row in result]
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    
    SQL = "insert into matches (winner, loser) values (%s, %s);" # unquoted token
    data = (clean(winner), clean(loser)) # tuple always 
    putData(SQL, data)
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    
    standings = playerStandings()
    pairings =[]
    c = countPlayers()
    
    def pairPlayers(s1, s2 ):
        return ( s1[0], s1[1], s2[0], s2[1])
    
    for index in range(0, c, 2):
        pairings.append(pairPlayers(standings[index], standings[index + 1]))

    return pairings

