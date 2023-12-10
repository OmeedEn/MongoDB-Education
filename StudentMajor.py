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

    student_major = {
            'studentId': student['_id'],
            'major': major['_id'],
            'declarationDate': datetime.date
        }
    collection.insert_one(student_major)

def delete_student_major(db):
    collection = db["studentMajors"]
    print("Prompting you for the student and the major that they no longer have.")
    student = Student.select_student(db)  # Assuming select_student is adapted for MongoDB
    major = Major.select_major(db)  # Assuming select_major is adapted for MongoDB

    collection.delete_one({"_id": student["_id"]})
    collection.delete_one({"_id": major["_id"]})
    print("We just deleted the student_major. ")
def list_student_major(db):
    student = Student.select_student(db)  # Assuming select_student is adapted for MongoDB
    # Assuming each student document has a 'majors' field that is a list of major names
    student_data = db.students.find_one({'_id': student['_id']}, {'majors': 1, 'lastName': 1, 'firstName': 1})

    if student_data and 'majors' in student_data:
        for major_name in student_data['majors']:
            major_data = db.majors.find_one({'name': major_name}, {'description': 1})
            if major_data:
                print(
                    f"Student name: {student_data['lastName']}, {student_data['firstName']}, Major: {major_name}, "
                    f"Description: {major_data.get('description', 'No description')}")
    else:
        print("No majors found for this student.")

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
        studentMajors.create_index([('student', pymongo.ASCENDING), ('majorName', pymongo.ASCENDING)],
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

def delete_student_major(db):
    collection = db["studentMajors"]
    print("Prompting you for the student and the major that they no longer have.")
    student = Student.select_student(db)  # Assuming select_student is adapted for MongoDB
    major = Major.select_major(db)  # Assuming select_major is adapted for MongoDB

    deleted = collection.delete_one({'studentId': student['_id']},
                                    {'major': major['_id']})
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

