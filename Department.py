
    department_validator = {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'A department in a university.',
                'required': ['abbreviation', 'name', 'chair_name', 'building', 'office', 'description'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'abbreviation': {
                        'bsonType': 'string',
                        'minLength': 1,
                        'maxLength': 6,
                        'description': 'Short phrase that describes a department name.'
                    },
                    'name': {
                        'bsonType': 'string',
                        'minLength': 10,
                        'maxLength': 50,
                        'description': 'A word that refers to a department.'
                    },
                    'chair_name': {
                        'bsonType': 'string',
                        'minLength': 1,
                        'maxLength': 80,
                        'description': 'Faculty member who manages a department.'
                    },
                    'building': {
                        'bsonType': 'string',
                        'enum': ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC'],
                        'description': 'Name used to identify an educational facility.'
                    },
                    'office': {
                        'bsonType': 'number',
                        'description': 'Room number that the chair uses.'
                    },
                    'description': {
                        'bsonType': 'string',
                        'minLength': 10,
                        'maxLength': 80,
                        'description': 'Statement that describes the department.'
                    }
                }
                
            }
        }
    }
    db.command('collMod', 'departments', **department_validator)
