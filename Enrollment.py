import pymongo
from pymongo import MongoClient
from pprint import pprint

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

# schema 
#im not sure if we need schemas or relations to the other passfail/lettergrade files


enrollment_validator2 = {
    'oneOf': [
        {
            'bsonType': 'object',
            'required': ['application_date'],
            'additionalProperties': False,
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
            'additionalProperties': False,
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
student_validator = {
    'bsonType': 'object',
    'required': ['student_id'],
    'additionalProperties': False,
    'properties': {
        'student_id': {
            'bsonType': 'objectId', #not too sure if its different from the object
            'description': 'unique identifier of students'
        }
    }
}
enrollment_valid = {
    'bsonType': "object",
    'description': 'the enrollment of the students',
    'required': ['students', 'enrollment_data'],
    'additionalProperties': False,
    'properties': {
        'students': student_validator,
        'enrollment': enrollment_validator2
    }
}

# enrollment_validator = {
#     'validator': {
#         '$jsonSchema': {
#             'bsonType': 'object',
#             'description': 'An enrollment for each student',
#             'required': ['enrollment'],
#             'additionalProperties': False,
#             'properties': {
#                 '_id': {},
#                 'enrollment': {
#                     'bsonType': 'object',
#                     'description': 'The enrollment for the students',
#                     'additionalProperties': False,
#                     'properties': {
#                         'passFail': {
#                             'bsonType': 'array',
#                             'items': {
#                                 'bsonType': 'object',
#                                 'description': 'Determines whether a student can pass or fail',
#                                 'required': ['applicationDate'],  # Add other required fields if any
#                                 'properties': {
#                                     'applicationDate': {
#                                         'bsonType': 'date',
#                                         'description': 'The date the student filed for pass or fail'
#                                     },
#                                 }
#                             }
#                         },
#                         'letterGrade': {
#                             'bsonType': 'array',
#                             'items': {
#                                 'bsonType': 'object',
#                                 'description': 'The letter grade for each student that is enrolling',
#                                 'required': ['minSatisfactory'],
#                                 'properties': {
#                                     'minSatisfactory': {
#                                         'bsonType': 'string',
#                                         'enum': ['A', 'B', 'C'],
#                                         'description': 'The minimum grade that would be satisfactory'
#                                     }
#                                 }
#                             }
#                         }
#                     }
#                 }
#             }
#         }
#     }
# }
