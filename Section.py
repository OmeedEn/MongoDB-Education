# creating collection


# unique indexes 



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
                    '_id': {},
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
