import pymongo
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from pymongo.errors import CollectionInvalid, OperationFailure
import Course

#imported functions
def add_section(db):
    collection = db["sections"]
    # Assuming you have a function to select a course
    course = Course.select_course(db)

    unique_section_number = False
    unique_room = False
    unique_instructor = False

    while not (unique_section_number and unique_room and unique_instructor):
        section_number = int(input("Section number--> "))
        section_year = int(input("Section Year--> "))
        semester = input("Section semester--> ")
        schedule = input("Schedule--> ")
        start_time_hour = int(input("Section start time hour--> "))
        start_time_minute = int(input("Section start time minute--> "))
        building = input("Section building--> ")
        room = int(input("Section room--> "))
        instructor = input("Section instructor--> ")

        # Validate semester, schedule, building, etc. as needed

        # Construct startTime as a string or a datetime object
        start_time = datetime(section_year, 1, 1, start_time_hour, start_time_minute)

        # Check for unique section number
        section_count = collection.count_documents({
            "courseNumber": course["courseNumber"],
            "sectionNumber": section_number,
            "semester": semester,
            "sectionYear": section_year
        })
        unique_section_number = section_count == 0

        # Check for unique room set
        room_set_count = collection.count_documents({
            "sectionYear": section_year,
            "semester": semester,
            "schedule": schedule,
            "startTime": start_time,
            "building": building,
            "room": room
        })
        unique_room_set = room_set_count == 0

        # Check for unique instructor set
        instructor_set_count = collection.count_documents({
            "sectionYear": section_year,
            "semester": semester,
            "schedule": schedule,
            "startTime": start_time,
            "instructor": instructor
        })
        unique_instructor_set = instructor_set_count == 0

        if not unique_section_number:
            print("Section number already exists for this course. Try again.")
        elif not unique_room_set:
            print("Room is already booked for this time. Try again.")
        elif not unique_instructor_set:
            print("Instructor is already teaching at this time. Try again.")

        new_section = {
            "departmentAbbreviation": course["departmentAbbreviation"],
            "courseNumber": course["courseNumber"],
            "sectionNumber": section_number,
            "semester": semester,
            "sectionYear": section_year,
            "building": building,
            "room": room,
            "schedule": schedule,
            "startTime": start_time,
            "instructor": instructor
        }
        collection.insert_one(new_section)
def select_section(db):
    collection = db["sections"]
    found: bool = False
    section_year: int
    semester: str
    schedule: str
    instructor: str

    while not found:
        section_year = int(input("Enter section year: "))
        semester = input("Enter semester: ")
        schedule = input("Enter schedule: ")
        instructor = input("Enter instructor: ")

        section_s = {
            "sectionYear": section_year,
            "semester": semester,
            "schedule": schedule,
            "instructor": instructor
        }

        section = collection.find_one(section_s)

        if section:
            print("Selected section:\n", section)
            return section
        else:
            print("No section with those values for that course. Try again.")

def delete_section(db):

    section_collection = db["sections"]
    enrollment_collection = db["enrollments"]

    print("Deleting a section")

    # Assuming you have a function to select a section
    section = select_section(db)

    if section is None:
        print("No section selected or section not found.")
        return

    # Assuming 'sectionID' in the 'enrollments' collection references 'sectionID' in the 'sections' collection
    n_enrollments = enrollment_collection.count_documents({"sectionID": section["_id"]})

    if n_enrollments > 0:
        print(f"Sorry, there are {n_enrollments} enrollments in that section. Delete them first, "
              f"then come back here to delete the section.")
    else:
        section_collection.delete_one({"_id": section["_id"]})
        print("Section deleted successfully.")

# schema function
def create_section(db):

    # creating collection
    sections = db['sections']
    section_count = sections.count_documents({})
    print(f'Sections in collection so far: {section_count}')

    # unique indexes
    sections_index = sections.index_information()
    if 'course_sectionNumber_semester_sectionYear' in sections_index.keys():
        print('course, section year, section number, and semester index present')
    else:
        # create a single UNIQUE index on course, section year, section number, and semester
        sections.create_index([('course', pymongo.ASCENDING), ('sectionYear', pymongo.ASCENDING),
                               ('sectionNumber', pymongo.ASCENDING), ('semester', pymongo.ASCENDING)],
                              unique=True,
                              name='course_sectionNumber_semester_sectionYears')
    if 'semester_sectionYear_building_room_schedule_startTime' in sections_index.keys():
        print('semester, section year, building, room, schedule, and start time index present')
    else:
        # create a UNIQUE index on semester, section year, building, room, schedule, start time
        sections.create_index([('semester', pymongo.ASCENDING), ('sectionYear', pymongo.ASCENDING),
                               ('building', pymongo.ASCENDING), ('room', pymongo.ASCENDING),
                               ('schedule', pymongo.ASCENDING), ('startTime', pymongo.ASCENDING)],
                              unique=True,
                              name='semester_sectionYear_building_room_schedule_startTimes')
    if 'semester_sectionYear_schedule_startTime_instructor' in sections_index.keys():
        print('semester, section year, schedule, start time, instructor index present')
    else:
        # create a UNQIUE index on semester, section year, schedule, start time, instructor
        sections.create_index([('semester', pymongo.ASCENDING), ('sectionYear', pymongo.ASCENDING),
                               ('schedule', pymongo.ASCENDING), ('startTime', pymongo.ASCENDING),
                               ('instructor', pymongo.ASCENDING)],
                              unique=True,
                              name='semester_sectionYear_schedule_startTime_instructors')
    if 'departmentAbbreviation_courseNumber_studentID_semester_sectionYear' in sections_index.keys():
        print('department abbreviation, course number, student ID, semester, section year index present')
    else:
        # create a UNQIUE index on department abbreviation, course number, student ID, semester, section year
        sections.create_index([('departmentAbbreviation', pymongo.ASCENDING), ('courseNumber', pymongo.ASCENDING),
                               ('studentID', pymongo.ASCENDING), ('semester', pymongo.ASCENDING),
                               ('sectionYear', pymongo.ASCENDING)],
                              unique=True,
                              name='departmentAbbreviation_courseNumber_studentID_semester_sectionYears')
    pprint(sections.index_information())

    section_validator = {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'A Section in a Course.',
                'required': ['departmentAbbreviation', 'courseNumber', 'sectionNumber', 'semester',
                             'sectionYear', 'schedule', 'room', 'building', 'startTime', 'instructor'],
                'additionalProperties': True,
                'properties': {
                    '_id': {},  # three primary keys?
                    'departmentAbbreviation': {
                        'bsonType': 'string',
                        'minLength': 1,
                        'maxLength': 6,
                        'description': 'Short phrase that describes a department name.'
                        # add foreign key
                    },
                    'courseNumber': {
                        'bsonType': 'number',
                        'minLength': 1,
                        'maxLength': 80,
                        'description': 'The number associated to the course.'
                    },
                    'sectionNumber': {
                        'bsonType': 'number',
                        'description': 'The number of the section.'
                    },
                    'semester': {
                        'bsonType': 'string',
                        'enum': ['Fall', 'Spring', 'Summer I', 'Summer II', 'Summer III', 'Winter'],
                        'minLength': 1,
                        'maxLength': 50,
                        'description': 'The given semester a course is in.'
                    },
                    'sectionYear': {
                        'bsonType': 'number',
                        'description': 'The year the given section is offered in.'
                    },
                    'schedule': {
                        'bsonType': 'string',
                        'minLength': 1,
                        'maxLength': 6,
                        'enum': ['MW', 'TuTh', 'MWF', 'F', 'S'],
                        'description': 'the schedule of the given class'
                    },
                    'room': {
                        'bsonType': 'number',
                        'minimum': 1,
                        'maximum': 999,
                        'description': 'the room for the class.'
                    },
                    'building': {
                        'bsonType': 'string',
                        'minLength': 1,
                        'maxLength': 6,
                        'enum': ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4',
                                 'EN5', 'ET', 'HSCI', 'NUR', 'VEC'],
                        'description': 'the building that the section is being taught in'
                    },
                    'startTime': {
                        'bsonType': 'date',
                        'description': 'the time the class starts at',
                        'pattern': '^((0[8-9]|1[0-2]):[0-5][0-9]|1[2-8]:[0-5][0-9]|19:[0-2][0-9]|19:30)$',
                        # this is saying from ((8-9 OR 10-12) : 00-59) OR (12-18 : 00-59) OR (19: 00-29) OR (19:30)
                        'minLength': 5,
                        'maxLength': 5
                    },
                    'instructor': {
                        'bsonType': 'string',
                        'minLength': 1,
                        'maxLength': 80,
                        'description': 'the teacher for the class'
                    }
                }

            }
        }
    }
    db.command('collMod', 'sections', **section_validator)

