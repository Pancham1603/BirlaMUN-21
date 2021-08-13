from flask import session
from pymongo import MongoClient
import bcrypt

client = MongoClient(r"***REMOVED***")
db = client.bmun
user_collection = db['users']


def add_new_user(form_data):
    name = form_data['name']
    email = form_data['email']
    school = form_data['school']
    committee = form_data['committee']
    password = form_data['password']

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    result = user_collection.find_one({
        '_id': email.lower()
    })

    if not result:
        user_collection.insert_one({
            '_id': email.lower(),
            'name': name.title(),
            'school': school,
            'committee': committee,
            'allotment': 'TBD',
            'role': 'delegate',
            'password': hashed_password
        })
        return 'Registered user successfully'
    return 'User already exists'


def login_user(form_data):
    email = form_data['email']
    password = form_data['password']

    user = user_collection.find_one({
        '_id': email.lower(),
    })
    if user:
        if bcrypt.checkpw(password.encode(), user['password']):
            session['login'] = True
            session['user'] = email.lower()
            return 'Logged in successfully'
        else:
            return 'In-valid credentials'
    else:
        return 'In-valid credentials'


def fetch_user(email):
    user = user_collection.find_one({'_id': email.lower()})
    return {
        '_id': user['_id'],
        'name': user['name'],
        'school': user['school'],
        'role': user['role'],
        'committee': user['committee'],
        'allotment': user['allotment']
    }
