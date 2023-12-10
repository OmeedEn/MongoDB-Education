import pymongo
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from pymongo.errors import CollectionInvalid, OperationFailure
import Student
import Section


#import function
def add_letter_grade(db):
    collection = db["enrollments"]

    unique_student_section = False
    while not unique_student_section:
        grade = input("What is the Satisfactory grade?---> ")

        # Assuming select_student and select_section return the ObjectId of the selected document
        student_id = Student.select_student(db)  # Modify this function as needed
        section_id = Section.select_section(db)  # Modify this function as needed

        # Check if the student is already enrolled in the section
        enrollment = collection.find_one({"studentId": student_id, "sectionId": section_id})

        if not enrollment:
            print("No enrollment record found for that student and section. Try again.")
        else:
            # Update the enrollment record with the letter grade
            letter_grade = {
                "minSatisfactory": grade  # Assuming you want to record the date of grade assignment
            }

            enrollment = {
                'studentId': student_id,
                'sectionId': section_id,
                'letterGrade': letter_grade,
                # Include other fields or subschemas (like letterGrade) if necessary
            }
            collection.insert_one(enrollment)
            print("Letter grade added to the student's enrollment.")
            unique_student_section = True
def add_student_pass_fail(db):

    collection = db["enrollments"]

    student_id = Student.select_student(db)
    section_id = Section.select_section(db)
    # Check if the student is already enrolled in the section
    if collection.find_one({'studentId': student_id, 'sectionId': section_id}):
        print("That section already has that student enrolled in it. Try again.")
        return

    # Create a pass/fail record as a subschema
    pass_fail = {
        'applicationDate': datetime.now(),
        # Add other passFail fields here if necessary
    }

    # Create the enrollment record with the passFail subschema
    enrollment = {
        'studentId': student_id,
        'sectionId': section_id,
        'passFail': pass_fail,
        # Include other fields or subschemas (like letterGrade) if necessary
    }

    # Add the enrollment record to the enrollments collection
    collection.insert_one(enrollment)
    print("Student added to section as pass/fail.")

def select_enrollment(db):

    collection = db["enrollments"]
    found: bool = False
    student = Student.select_student(db)
    section = Section.select_section(db)

    while not found:
        found_count: int = collection.count_documents({"studentId": student['_id'],
                                                       "sectionId": section["_id"]})
        found = found_count == 1
    if not found:
        print("No Student found with that section. Try again. ")
    found_enrollment = collection.find_one({"studentId": student['_id'],
                                            "sectionId": section["_id"]})
    return found_enrollment
def delete_enrollment(db):

    enrollment = select_enrollment(db)
    enrollments = db["enrollments"]

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

    if 'student_and_section' in enrollments_index.keys():
        print('student and section index present')
    else:
        # create a UNIQUE index on student and section
        enrollments.create_index([('student', pymongo.ASCENDING), ('section', pymongo.ASCENDING)],
                                 unique=True,
                                 name='student_and_sections')
    if 'semester_sectionYear_departmentAbbreviation_courseNumber_studentID' in enrollments_index.keys():
        print('semester, section year, department abbreviation, course number, student ID index present')
    else:
        # create a UNIQUE index on semester, section year, department abbreviation, course number, student ID
        enrollments.create_index([('semester', pymongo.ASCENDING), ('sectionYear', pymongo.ASCENDING),
                                  ('departmentAbbreviation', pymongo.ASCENDING), ('courseNumber', pymongo.ASCENDING),
                                  ('studentID', pymongo.ASCENDING)],
                                 unique=True,
                                 name='semester_sectionYear_departmentAbbreviation_courseNumber_studentIDs')
    pprint(enrollments.index_information())

    enrollment_validator = {
        'bsonType': "object",
        'description': 'the enrollment of the students',
        'required': ['enrollmentType'],  # Corrected 'enrollment_data' to 'enrollment'
        'additionalProperties': True,
        'properties': {
            'enrollmentType': {
                'oneOf': [
                    {
                        'bsonType': 'object',
                        'required': ['application_date'],
                        'additionalProperties': True,
                        'properties': {
                            'application_date': {
                                'bsonType': 'date',
                                'description': 'The date the student filed for pass or fail'
                            }
                        }
                    },
                    {
                        'bsonType': 'object',
                        'required': ['min_satisfactory'],
                        'additionalProperties': True,
                        'properties': {
                            'min_satisfactory': {
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
    db.command('collMod', 'enrollments', validator=enrollment_validator)
