# collections
courses = db['courses']
    course_count = courses.count_documents({})
    print(f'Courses in the collection so far: {course_count}')


# unique index 


# schema 
course_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': 'object',
            'description': 'A course in a department.',
            'required': ['courseNumber', 'courseName','description', 'units'],
            'additionalProperties': False,
            'properties': {
                '_id': {},
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


