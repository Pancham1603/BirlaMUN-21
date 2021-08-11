import pymongo.errors
from flask import session
from pymongo import MongoClient

client = MongoClient(
    ""
)
db = client.bmun
user_collection = db['users']
meeting_collection = db['meetings']


def add_meeting(data):
    try:
        meeting_collection.insert_one({
            '_id':int(data['meeting_id']),
            'topic':data['topic'],
            'meeting_url':data['meeting_url'],
            'time':data['time']
        })
        return f"Scheduled {data['topic']} successfully"
    except pymongo.errors.DuplicateKeyError:
        return 'Meeting already exists'


def fetch_meetings():
    meetings = []
    results = meeting_collection.find()
    for result in results:
        meetings.append(
            {
                'topic':result['topic'],
                'time':result['time'],
                'meeting_id':result['_id'],
                'meeting_url':result['meeting_url']
            }
        )
    return meetings


def fetch_meeting(id):
    meeting = meeting_collection.find_one({'_id':int(id)})
    return meeting


def update_meeting(id, data):
    meeting_collection.delete_one({'_id':int(id)})
    meeting_collection.insert_one({
            '_id':int(data['meeting_id']),
            'topic': data['topic'],
            'time': data['time'],
            'meeting_url':data['meeting_url'],
        }
    )
    return 'Meeting updated successfully'


def delete_meeting(id):
    meeting_collection.delete_one({'_id': int(id)})
    return 'Deleted meeting successfully'
