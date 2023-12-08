import pymongo
from pymongo import MongoClient
from pprint import pprint

# collections
students = db["students"]
student_count = students.count_documents({})
print(f"Students in the collection so far: {student_count}")


# uniqe index 

students_indexes = students.index_information()
if 'students_last_and_first_names' in students_indexes.keys():
    print("first and last name index present.")
else:
    # Create a single UNIQUE index on BOTH the last name and the first name.
    students.create_index([('last_name', pymongo.ASCENDING), ('first_name', pymongo.ASCENDING)],
                          unique=True,
                          name="students_last_and_first_names")
if 'students_e_mail' in students_indexes.keys():
    print("e-mail address index present.")
else:
    # Create a UNIQUE index on just the e-mail address
    students.create_index([('e_mail', pymongo.ASCENDING)],
                          unique=True,
                          name='students_e_mail')
pprint(students.index_information())


# schema
student_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': 'object',
            'description': 'A student in a university.',
            'required': ['studentId', 'lastname', 'firstname', 'email'],
            'additionalProperties': False,
            'properties': {
                '_id': {},
                'studentId': {
                    'bsonType': 'integer',
                    'description': 'Student identification number'
                },
                'lastname': {
                    'bsonType': 'string',
                    'minLength': 1,
                    'maxLength': 50,
                    'description': 'Last name of the student'
                },
                'firstname': {
                    'bsonType': 'string',
                    'minLength': 1,
                    'maxLength': 50,
                    'description': 'First name of the student'
                },
                'email': {
                    'bsonType': 'string',
                    'minLength': 1,
                    'maxLength': 255,
                    'description': 'email of the student'
            }
        }
    }
}
}
db.command('collMod', 'students', **student_validator)
