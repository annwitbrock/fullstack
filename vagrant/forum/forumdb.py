#
# Database access functions for the web forum.
# 

import time, psycopg2
import bleach

## Database connection
DB = []
    
## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    try:
        conn = psycopg2.connect("dbname='forum'")
    except:
        print "GetAllPosts - unable to connect to database"
    cur = conn.cursor()
    SQL = "select content, time from posts order by time desc;"
    cur.execute(SQL)
    result = cur.fetchall()
    conn.close()
    
    posts = [{'content': str(bleach.clean(row[0],strip=True)), 'time': str(row[1])} for row in result]
#    posts.sort(key=lambda row: row['time'], reverse=True)
    
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
#    t = time.strftime('%c', time.localtime())
#    DB.append((t, content))
    cleaned = bleach.clean(content,strip=True)
    try:
        conn = psycopg2.connect("dbname='forum'")
    except:
        print "AddPost - unable to connect to database"
    cur = conn.cursor()
    SQL = "insert into posts (content) values (%s);" # no quotes around token
    data = (cleaned,)       # always as a tuple
    cur.execute( SQL, data) # using the second parameter is the safe way to pass data
    conn.commit()
    conn.close()
