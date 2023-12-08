import pymongo
from pymongo import MongoClient
from pprint import pprint

# collection
studentMajors = db['studentMajors']
studentMajor_count = studentMajors.count_documents({})
print(f'Student Majors in collection so far: {studentMajor_count}')


# unique index 
studentMajors_index = studentMajors.index_information()
if 'student_and_majorName' in studentMajors_index.keys():
    print('student and major name index present')
else:
    # create a single UNIQUE index on student and majorName
    studentMajors.create_index([('student', pymongo.ASCENDING), ('majorName', pymongo.ASCENDING)],
                               unique=True,
                               name='student_and_majorNames')
pprint(studentMajors.index_information())


# schema 
student_major_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': 'object',
            'description': 'A major dedicated to a student',
            'required': ['declarationDate'],
            'additionalProperties': False,
            'properties': {
                '_id': {},
                'declarationDate': {
                    'bsonType': 'date',
                    'description': 'The date the Student declared his/her major. '
                }
            }
        }
    }
}
db.command('collMod', 'students', **student_major_validator)
