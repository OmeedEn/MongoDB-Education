import pymongo
from pprint import pprint
from pymongo.errors import CollectionInvalid, OperationFailure
import Department

# imported function

def add_course(db):
    collection = db["courses"]

    print("Which department offers this course?")
    department = Department.select_department(db)
    unique_number = False
    unique_name = False

    while not unique_number or not unique_name:
        name = input("Course full name--> ")
        number = int(input("Course number--> "))
        name_count = collection.count_documents({'departmentAbbreviation': department['abbreviation'], 'name': name})
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a course by that name in that department. Try again.")
        if unique_name:
            number_count = collection.count_documents({'departmentAbbreviation': department['abbreviation'],
                                                       'number': number})
            unique_number = number_count == 0
            if not unique_number:
                print("We already have a course in this department with that number. Try again.")
        description = input('Please enter the course description-->')
        units = int(input('How many units for this course-->'))
        course = {
            'departmentAbbreviation': department['abbreviation'],
            'courseNumber': number,
            'courseName': name,
            'description': description,
            'units': units
        }
        collection.insert_one(course)

def select_course(db):
    collection = db["courses"]
    found: bool = False
    department_abbreviation = ''
    course_number = -1

    while not found:
        department_abbreviation = input("Department abbreviation--> ")
        course_number = int(input("Course Number--> "))

        course_count: int = collection.count_documents({'departmentAbbreviation': department_abbreviation,
                                                        'courseNumber': course_number})
        found = course_count == 1
        if not found:
            print("No course by that number in that department. Try again.")

    course = collection.find_one(
        {'departmentAbbreviation': department_abbreviation, 'courseNumber': course_number})

    return course

def delete_course(db):
    course = select_course(db)
    courses = db["courses"]
    sections = db['sections']
    n_sections = sections.count_documents({'courseNumber': course['courseNumber'],
                                           'departmentAbbreviation': course['departmentAbbreviation']})
    if n_sections > 0:
        print(f'Sorry, there are {n_sections} sections in that course. Delete them first, then come back here to '
              f'delete the course.')
    else:
        deleted = courses.delete_one({"_id": course["_id"]})
        print(f"We just deleted: {deleted.deleted_count} courses.")

def list_course(db):
    courses = db["courses"].find({}).sort([("courseName", pymongo.ASCENDING)])
    for course in courses:
        pprint(course)


# schema function
def create_course(db):
    # collections
    courses = db['courses']
    course_count = courses.count_documents({})
    print(f'Courses in the collection so far: {course_count}')

    # unique index
    courses_index = courses.index_information()

    if 'departmentAbbreviation_and_courseName' in courses_index.keys():
        print('department abbreviation and course name index present')
    else:
        # create a single UNIQUE index on departmentAbbreviation and courseName
        courses.create_index([('departmentAbbreviation', pymongo.ASCENDING), ('courseName', pymongo.ASCENDING)],
                             unique=True,
                             name='departmentAbbreviation_and_courseNames')

    if 'departmentAbbreviation_and_courseNumber' in courses_index.keys():
        print('department abbreviation and course number index present')
    else:
        # create a single UNIQUE index on departmentAbbreviation and courseNumber
        courses.create_index([('departmentAbbreviation', pymongo.ASCENDING), ('courseNumber', pymongo.ASCENDING)],
                             unique=True,
                             name='departmentAbbreviation_and_courseNumbers')
    pprint(courses.index_information())

    course_validator = {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'A course in a department.',
                'required': ['departmentAbbreviation','courseNumber', 'courseName', 'description', 'units'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},  # primary key
                    'departmentAbbreviation': {
                        'bsonType': 'string',
                        'description': 'The department that the course is in.'
                    },
                    'courseNumber': {
                        'bsonType': 'number',
                        'minLength': 1,
                        'maxLength': 6,
                        'minimum': 100,
                        'maximum': 699,
                        'description': 'The course ID that is unique to that course.'
                    },
                    'courseName': {
                        'bsonType': 'string',
                        'minLength': 1,
                        'maxLength': 50,
                        'description': 'The word that determines the course.'
                    },
                    'description': {
                        'bsonType': 'string',
                        'minLength': 10,
                        'maxLength': 80,
                        'description': 'Statement that describes the course.'
                    },
                    'units': {
                        'bsonType': 'number',
                        'minimum': 1,
                        'maximum': 5,
                        'description': 'Amount of units a specific course has.'
                    },
                }

            }
        }
    }
    db.command('collMod', 'courses', **course_validator)

