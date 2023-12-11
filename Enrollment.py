import pymongo
from pprint import pprint
from datetime import datetime
from error_trap import print_exception
import Student
import Section


#import function
def add_letter_grade(db):
    collection = db["enrollments"]
    unique_enrollment = False
    while not unique_enrollment:
        student = Student.select_student(db)
        section = Section.select_section(db)
        grade = input("What is the Satisfactory grade?---> ")

        enrollment_count = collection.count_documents({"studentId": student['_id'], "sectionId": section['_id']})
        unique_enrollment = enrollment_count == 0
        if not unique_enrollment:
            print("No enrollment record found for that student and section. Try again.")
        if unique_enrollment:
            name = f'{student['first_name']} {student['last_name']}'
            enrollment = {
                'studentId': student['_id'],
                'studentName': name,
                'sectionId': section['_id'],
                'departmentAbbreviation': section['departmentAbbreviation'],
                'courseNumber': section['courseNumber'],
                'sectionNumber': section['sectionNumber'],
                'sectionYear': section['sectionYear'],
                'semester': section['semester'],
                'enrollmentType': {
                    'type': 'letter grade',
                    'minSatisfactory': grade
                }
            }
            try:
                collection.insert_one(enrollment)
            except Exception as e:
                print(print_exception(e))

def add_student_pass_fail(db):
    collection = db["enrollments"]
    unique_enrollment = False

    while not unique_enrollment:
        student = Student.select_student(db)
        section = Section.select_section(db)
        # app_date_year = int(input('Application year--> '))
        # app_date_month = int(input('Application month--> '))
        # app_date_day = int(input('Application day--> '))
        # app_date = datetime(app_date_year, app_date_month, app_date_day, 0, 0)

        enrollment_count = collection.count_documents({"studentId": student['_id'], "sectionId": section['_id']})
        unique_enrollment = enrollment_count == 0
        if not unique_enrollment:
            print('No enrollment record found for that student and section. Try again.')
        if unique_enrollment:
            name = f'{student['first_name']} {student['last_name']}'
            enrollment = {
                'studentId': student['_id'],
                'studentName': name,
                'sectionId': section['_id'],
                'departmentAbbreviation': section['departmentAbbreviation'],
                'courseNumber': section['courseNumber'],
                'sectionNumber': section['sectionNumber'],
                'sectionYear': section['sectionYear'],
                'semester': section['semester'],
                'enrollmentType': {
                    'type': 'pass fail',
                    'applicationDate': datetime.now()
                }
            }
            try:
                collection.insert_one(enrollment)
            except Exception as e:
                print(print_exception(e))

def select_enrollment(db):
    collection = db["enrollments"]
    found: bool = False
    student = Student.select_student(db)
    section = Section.select_section(db)

    while not found:
        found_count: int = collection.count_documents({
            "studentId": student['_id'],
            "sectionId": section["_id"]
        })
        found = found_count == 1
        if not found:
            print("No Student found with that section. Try again. ")
            student = Student.select_student(db)
            section = Section.select_section(db)
    found_enrollment = collection.find_one({"studentId": student['_id'],
                                            "sectionId": section["_id"]})
    return found_enrollment


def delete_enrollment(db):
    enrollments = db["enrollments"]
    enrollment = select_enrollment(db)
    deleted = enrollments.delete_one({"_id": enrollment["_id"]})
    print(f"We just deleted: {deleted.deleted_count} enrollments.")
def list_enrollment(db):
    enrollments = db["enrollments"].find({}).sort([("_id", pymongo.ASCENDING)])

    for enrollment in enrollments:
        pprint(enrollment)
# schema function
def create_enrollment(db):
    # collections
    enrollments = db['enrollments']
    enrollment_count = enrollments.count_documents({})
    print(f'Enrollments in collection so far: {enrollment_count}')

    # unique index
    enrollments_index = enrollments.index_information()

    if 'studentId_and_sectionId' in enrollments_index.keys():
        print('student and section ID\'s index present')
    else:
        # create a UNIQUE index on student and section
        enrollments.create_index([('studentId', pymongo.ASCENDING), ('sectionId', pymongo.ASCENDING)],
                                 unique=True,
                                 name='student_and_sections')
    if 'semester_sectionYear_departmentAbbreviation_courseNumber_studentID' in enrollments_index.keys():
        print('semester, section year, department abbreviation, course number, student ID index present')
    else:
        # create a UNIQUE index on semester, section year, department abbreviation, course number, student ID
        enrollments.create_index([('semester', pymongo.ASCENDING), ('sectionYear', pymongo.ASCENDING),
                                  ('departmentAbbreviation', pymongo.ASCENDING), ('courseNumber', pymongo.ASCENDING),
                                  ('studentId', pymongo.ASCENDING)],
                                 unique=True,
                                 name='semester_sectionYear_departmentAbbreviation_courseNumber_studentIDs')
    pprint(enrollments.index_information())
    # schema
    enrollment_validator = {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'The enrollment of student into a section.',
                'required': ['studentId', 'studentName', 'sectionId', 'departmentAbbreviation', 'courseNumber', 'sectionYear',
                             'semester', 'enrollmentType'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'studentId': {
                        'bsonType': 'objectId',
                        'description': 'The students\' Id.'
                    },
                    'studentName': {
                        'bsonType': 'string',
                        'description': 'The name of the student.'
                    },
                    'sectionId': {
                        'bsonType': 'objectId',
                        'description': 'The sections\' Id.'
                    },
                    'departmentAbbreviation': {
                        'bsonType': 'string',
                        'description': 'The department of the section the student is enrolling in.'
                    },
                    'courseNumber': {
                        'bsonType': 'number',
                        'description': 'The course number of the section that student is enrolling in.'
                    },
                    'sectionNumber': {
                        'bsonType': 'number',
                        'description': 'The section number of the section that student is enrolling in.'
                    },
                    'sectionYear': {
                        'bsonType': 'number',
                        'description': 'The section year of the section the student is enrolling in.'
                    },
                    'semester': {
                        'bsonType': 'string',
                        'description': 'The semester of the section the student is enrolling in.'
                    },
                    'enrollmentType': {
                        'oneOf': [
                            {
                                'bsonType': 'object',
                                'required': ['type', 'applicationDate'],
                                'additionalProperties': False,
                                'properties': {
                                    'type': {
                                        'bsonType': 'string',
                                        'description': 'The type of enrollment.'
                                    },
                                    'applicationDate': {
                                        'bsonType': 'date',
                                        'description': 'The date the student filed for pass or fail'
                                    }
                                }
                            }, {
                                'bsonType': 'object',
                                'required': ['type', 'minSatisfactory'],
                                'additionalProperties': False,
                                'properties': {
                                    'type': {
                                        'bsonType': 'string',
                                        'description': 'The type of enrollment.'
                                    },
                                    'minSatisfactory': {
                                        'bsonType': 'string',
                                        'enum': ['A', 'B', 'C'],
                                        'description': 'The minimum grade that would be satisfactory'
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }
    }
    db.command('collMod', 'enrollments', **enrollment_validator)
