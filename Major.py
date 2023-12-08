import pymongo
from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import CollectionInvalid, OperationFailure
import Department

#imported functions
def add_major(db):
    collection = db["majors"]
    print("Which department offers this major?")
    department = Department.select_department(db)  # Assuming select_department is adapted for MongoDB
    unique_name = False
    name = ''

    while not unique_name:
        name = input("Major name--> ")
        name_count = db.majors.count_documents({'name': name, 'departmentAbbreviation': department['abbreviation']})
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a major by that name in that department. Try again.")

    description = input('Please give this major a description -->')
    major = {
        'departmentAbbreviation': department['abbreviation'],
        'name': name,
        'description': description
    }
    collection.insert_one(major)

def select_major(db):

    collection = db["major"]
    found: bool = False
    name = ''

    while not found:
        name = input("Major's name--> ")
        major = collection.find_one({'name': name})
        found = major is not None
        if not found:
            print("No major found by that name. Try again.")

    major = collection.find_one(
        {'name': name})

    return major
def list_majors(db):

    majors = db["majors"].find({}).sort([("", pymongo.ASCENDING),
                                        ("", pymongo.ASCENDING)])

    for major in majors:
        pprint(major)

# schema function
def create_major(db):
    # collection
    majors = db['majors']
    major_count = majors.count_documents({})
    print(f'Majors in collection so far: {major_count}')

    # unique index
    majors_indexes = majors.index_information()

    if 'name' in majors_indexes.keys():
        print('major name index present')

    else:
        # create a single UNIQUE index on major name
        majors.create_index([('name', pymongo.ASCENDING)],
                            unique=True,
                            name='name')
    pprint(majors.index_information())

    major_validator = {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'A major in a department.',
                'required': ['name', 'description'],
                'additionalProperties': True,
                'properties': {
                    '_id': {}, #change to relationship
                    'name': {
                        'bsonType': 'string',
                        'minLength': 1,
                        'maxLength': 50,
                        'description': 'A word that refers to a major.'
                    },
                    'description': {
                        'bsonType': 'string',
                        'minLength': 10,
                        'maxLength': 80,
                        'description': 'Statement that describes the major.'
                    }
                }
            }
        }
    }
    db.command('collMod', 'majors', **major_validator)

