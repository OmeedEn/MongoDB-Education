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


# schema 
course_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': 'object',
            'description': 'A course in a department.',
            'required': ['courseNumber', 'courseName','description', 'units'],
            'additionalProperties': False,
            'properties': {
                '_id': {'courseNumber'}, #primary key
                'courseNumber': {
                    'bsonType': 'number',
                    'minLength': 1,
                    'maxLength': 6,
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
                    'description': 'Amount of units a specific course has.'
                },
            }

        }
    }
}


