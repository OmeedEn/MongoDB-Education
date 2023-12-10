import datetime

import pymongo
from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import CollectionInvalid, OperationFailure
import Student
import Major

#imported functions

def add_student_major(db):

    collection = db["studentMajors"]
    student = Student.select_student(db)  # Assuming select_student is adapted for MongoDB
    major = Major.select_major(db)  # Assuming select_major is adapted for MongoDB

    # Check if the student already has this major
    student_major_count = collection.count_documents({
        'studentId': student['_id'],  # Assuming student ID is stored in '_id'
        'majorName': major['name']  # Assuming major name is stored in 'name'
    })

    unique_student_major = student_major_count == 0

    while not unique_student_major:
        print("That student already has that major. Try again.")
        student = Student.select_student(db)
        major = Major.select_major(db)
        student_major_count = db.students.count_documents({
            '_id': student['_id'],
            'majors': major['name']
        })
        unique_student_major = student_major_count == 0

    name = f'{student['first_name']} {student['last_name']}'
    student_major = {
            'studentId': student['_id'],
            'studentName': name,
            'major': major['_id'],
            'majorName': major['name'],
            'declarationDate': datetime.datetime.now()
        }
    collection.insert_one(student_major)

def select_student_major(db):
    collection = db['studentMajors']
    found = False
    student = Student.select_student(db)
    major = Major.select_major(db)
    while not found:
        found_count = collection.count_documents({
            'studentId': student['_id'],
            'major': major['_id']
        })
        found = found_count == 1
        if not found:
            print('No student found with that major. Try again.')
            student = Student.select_student(db)
            major = Major.select_major(db)
    found_student_major = collection.find_one({'studentId': student['_id'],
                                               'major': major['_id']})
    return found_student_major


def delete_student_major(db):
    collection = db['studentMajors']
    student_major = select_student_major(db)

    deleted = collection.delete_one({'studentId': student_major['studentId'],
                                     'major': student_major['major']})
    print("We just deleted the student_major. ")
def list_student_major(db):
    student_majors = db['studentMajors'].find({}).sort([('decalrationDate', pymongo.ASCENDING)])
    for student in student_majors:
        pprint(student)

# schema
def create_student_major(db):

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
        studentMajors.create_index([('studentId', pymongo.ASCENDING), ('majorName', pymongo.ASCENDING)],
                                   unique=True,
                                   name='student_and_majorNames')
    pprint(studentMajors.index_information())

    student_major_validator = {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'A major dedicated to a student',
                'required': ['declarationDate'],
                'additionalProperties': True,
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
    db.command('collMod', 'studentMajors', **student_major_validator)
