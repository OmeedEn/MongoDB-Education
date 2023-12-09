import pymongo
from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import CollectionInvalid, OperationFailure


# imported add/delete/list

def add_department(db):
    # collection pointer to department collections in db
    collection = db["departments"]
    unique_name: bool = False
    unique_abbreviation: bool = False
    unique_chair_name: bool = False
    unique_building_and_office: bool = False
    unique_description: bool = False
    while not unique_abbreviation or not unique_name or not unique_chair_name or not unique_building_and_office or not unique_description:
        name = input("Department full name--> ")
        abbreviation = input("Department abbreviation--> ")
        chair_name = input("Department chair name--> ")
        building = input("Department building--> ")
        office = int(input("Department office--> "))
        description = input("Department description--> ")

        name_count: int = collection.count_documents({"name": name})
        unique_name = name_count == 0
        if not unique_name:
            print("There is already a department with that name. Try again")
        if unique_name:
            abbreviation_count = collection.count_documents({"abbreviation": abbreviation})
            unique_abbreviation = abbreviation_count == 0
            if not unique_abbreviation:
                print("We already have a department with that abbreviation. Try again.")
            if unique_abbreviation:
                chair_count = collection.count_documents({"chair_name": chair_name})
                unique_chair_name = chair_count == 0
                if not unique_chair_name:
                    print("We already have a department with that chair name. Try again.")
                if unique_chair_name:
                    build_office_count = collection.count_documents({"building": building, "office": office})
                    unique_building_and_office = build_office_count == 0
                    if not unique_building_and_office:
                        print("We already have a department with that building and office. Try again.")
                    if unique_building_and_office:
                        description_count = collection.count_documents({"description": description})
                        unique_description = description_count == 0
                        if not unique_description:
                            print("We already have a department with that description. Try again.")
        department = {
            "name": name,
            "abbreviation": abbreviation,
            "chair_name": chair_name,
            "building": building,
            "office": office,
            "description": description
        }
        collection.insert_one(department)

def list_department(db):
    departments = db["departments"].find({}).sort([("name", pymongo.ASCENDING)])
    # pretty print is good enough for this work. It doesn't have to win a beauty contest.
    for department in departments:
        pprint(department)

def delete_department(db):
    department = select_department(db)
    # Create a "pointer" to the students collection within the db database.
    departments = db["departments"]
    # student["_id"] returns the _id value from the selected student document.
    deleted = departments.delete_one({"_id": department["_id"]})
    # The deleted variable is a document that tells us, among other things, how
    # many documents we deleted.
    print(f"We just deleted: {deleted.deleted_count} departments.")

def select_department(db):
    collection = db["departments"]
    found: bool = False
    name: str = ''
    while not found:
        name = input("Department's name--> ")
        name_count: int = collection.count_documents({"name": name})
        found = name_count == 1
        if not found:
            print("No department found by that name. Try again.")
    found_department = collection.find_one({"name": name})
    return found_department

# schema function
def create_department(db):
    # collections
    departments = db['departments']
    department_count = departments.count_documents({})
    print(f'Departments in the collection so far: {department_count}')

    # unique indexes
    departments_indexes = departments.index_information()

    if 'abbreviation' in departments_indexes.keys():
        print('abbreviation index present.')
    else:
        # Create a single UNIQUE index on abbreviation
        departments.create_index([('abbreviation', pymongo.ASCENDING)],
                                 unique=True,
                                 name='abbreviations')

    if 'chair_name' in departments_indexes.keys():
        print('chair name index present.')
    else:
        # Create a single UNIQUE index on chair name
        departments.create_index([('chair_name', pymongo.ASCENDING)],
                                 unique=True,
                                 name='chair_names')

    if 'buildings_and_offices' in departments_indexes.keys():
        print('building and office index present.')
    else:
        # Create a single UNIQUE index on BOTH the building and office
        departments.create_index([('building', pymongo.ASCENDING), ('office', pymongo.ASCENDING)],
                                 unique=True,
                                 name='buildings_and_offices')

    if 'name' in departments_indexes.keys():
        print('name index present.')
    else:
        # Create a single UNIQUE index on name
        departments.create_index([('name', pymongo.ASCENDING)],
                                 unique=True,
                                 name='names')
    pprint(departments.index_information())

    # schema
    department_validator = {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'A department in a university.',
                'required': ['abbreviation', 'name', 'chair_name', 'building', 'office', 'description'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},  # primary key
                    'abbreviation': {
                        'bsonType': 'string',
                        'minLength': 1,
                        'maxLength': 6,
                        'description': 'Short phrase that describes a department name.'
                    },
                    'name': {
                        'bsonType': 'string',
                        'minLength': 10,
                        'maxLength': 50,
                        'description': 'A word that refers to a department.'
                    },
                    'chair_name': {
                        'bsonType': 'string',
                        'minLength': 1,
                        'maxLength': 80,
                        'description': 'Faculty member who manages a department.'
                    },
                    'building': {
                        'bsonType': 'string',
                        'enum': ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC'],
                        'description': 'Name used to identify an educational facility.'
                    },
                    'office': {
                        'bsonType': 'number',
                        'description': 'Room number that the chair uses.'
                    },
                    'description': {
                        'bsonType': 'string',
                        'minLength': 1,
                        'maxLength': 80,
                        'description': 'Statement that describes the department.'
                    }
                }

            }
        }
    }
    db.command('collMod', 'departments', **department_validator)
