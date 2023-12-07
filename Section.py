import pymongo
from pymongo import MongoClient
from pprint import pprint

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


# schema 

section_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': 'object',
            'description': 'A Section in a Course.',
            'required': ['departmentAbbreviation', 'sectionId', 'name', 'courseNumber', 'sectionNumber', 'semester',
                         'sectionYear', 'schedule', 'room', 'building', 'startTime', 'instructor'],
            'additionalProperties': False,
            'properties': {
                '_id': {}, #three primary keys?
                'departmentAbbreviation': {
                    'bsonType': 'string',
                    'minLength': 1,
                    'maxLength': 6,
                    'description': 'Short phrase that describes a department name.'
                    # add foreign key
                },
                'sectionId': {
                    'bsonType': 'integer',
                    'minLength': 1,
                    'maxLength': 50,
                    'description': 'The Id that is given to a Section of a Course'
                    # add primary key
                },
                'name': {
                    'bsonType': 'string',
                    'minLength': 1,
                    'maxLength': 50,
                    'description': 'A word that refers to a course.'
                },
                'courseNumber': {
                    'bsonType': 'string',
                    'minLength': 1,
                    'maxLength': 80,
                    'description': 'The number associated to the course.'
                },
                'sectionNumber': {
                    'bsonType': 'integer',
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
                    'bsonType': 'integer',
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
                    'bsonType': 'integer',
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
                    'bsonType': 'time',
                    'description': 'the time the class starts at'
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
