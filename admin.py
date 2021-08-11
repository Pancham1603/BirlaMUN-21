from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://admin:admin@pancham.vxuje.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
)
db = client.bmun
user_collection = db['users']


def admin_check(email):
    try:
        if user_collection.find_one({'_id': email.lower()})['role'] == 'organizer':
            return True
        else:
            return False
    except:
        return False


def user_list():
    results = user_collection.find()
    participants = []
    for result in results:
        participants.append(
            {
                '_id': result['_id'],
                'name': result['name'],
                'school': result['school'],
                'role': result['role'].title(),
                'committee': result['committee'],
                'allotment': result['allotment']
            }
        )
    return participants


def update_user(email, data):
    user_collection.update_one(
        {'_id':email.lower()},
        {'$set':{
            'name': data['name'],
            'school': data['school'],
            'role': data['role'],
            'committee': data['committee'],
            'allotment': data['allotment']
        }}
    )
    return 'User updated successfully'


def delete_user(email):
    name = user_collection.find_one({'_id':email.lower()})['name']
    user_collection.delete_one({'_id':email.lower()})
    return f'Deleted user {name} successfully'