# author: tiankai
# copywrite 2019

# author: tiank
# copywrite 2019

import click
import pymongo
from flask import current_app, g

def get_db():
    if 'db' not in g:
        # mongo client
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        g.db = client['myServices']

    return g.db

def close_db(e=None):

    '''
    db = g.pop('db', None)
    if db is not None:
        db.close()
    '''
    # nothing to do for mongodb
    pass

# add user
def add_user(username, password="service"):
    ''' add an user account
    username: -
    password: -
    return: whether successfully added.
    '''

    db = get_db()
    flag = False

    ans = db.user.find_one({'username': username})
    if ans is None:
        db.user.insert_one({'username': username, 'password': password})
        flag = True

    return flag

# find user
def find_user_by_name(username):
    ''' find an user account
    username: -
    return: finded user or None
    '''

    db = get_db()
    ans = db.user.find_one({'username': username})
    return ans

def find_user_by_id(id):
    ''' find an user account
    username: -
    return: finded user or None
    '''

    db = get_db()
    ans = db.user.find_one({'_id': id})
    return ans
