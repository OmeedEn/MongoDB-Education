import pymongo
from pprint import pprint
from pymongo.errors import CollectionInvalid, OperationFailure
import Department

#imported functions
def add_major(db):
    collection = db["majors"]
    print("Which department offers this major?")
    department = Department.select_department(db)
    unique_name = False

    while not unique_name:
        name = input("Major name--> ")
        name_count = collection.count_documents({'name': name, 'departmentAbbreviation': department['abbreviation']})
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
    collection = db["majors"]
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
    majors = db["majors"].find({}).sort([("name", pymongo.ASCENDING)])
    for major in majors:
        pprint(major)
def delete_major(db):
    major = select_major(db)
    majors = db['majors']
    student_majors = db['studentMajors']
    n_stuMaj = student_majors.count_documents({'majorId': major['_id']})
    if n_stuMaj > 0:
        print(f"Sorry, there are {n_stuMaj} students in that major. Delete them first, "
              f"then come back here to delete the major.")
    else:
        deleted = majors.delete_one({"_id": major["_id"]})
        print(f"We just deleted: {deleted.deleted_count} majors.")
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
                'required': ['departmentAbbreviation', 'name', 'description'],
                'additionalProperties': False,
                'properties': {
                    '_id': {}, #change to relationship
                    'departmentAbbreviation': {
                        'bsonType': 'string',
                        'description': 'A short phrase that describes the department.'
                    },
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
