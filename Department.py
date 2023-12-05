# collections 
departments = db['departments']
    department_count = departments.count_documents({})
    print(f'Departments in the collection so far: {department_count}')

# unique indexes 
departments_indexes = departments.index_information()

    if 'abbreviation' in departments_indexes.keys():
        print('abbreviation index present.')
    else:
        # Create a single UNIQUE index on abbreviation
        departments.create_index([('abbreviation', pymongo.ASCENDING)],
                                 unique=True,
                                 name='abbreviations')

    if 'chair_name' in departments_indexes.keys():
        print('chair name index present.')
    else:
        # Create a single UNIQUE index on chair name
        departments.create_index([('chair_name', pymongo.ASCENDING)],
                                 unique=True,
                                 name='chair_names')

    if 'buildings_and_offices' in departments_indexes.keys():
        print('building and office index present.')
    else:
        # Create a single UNIQUE index on BOTH the building and office
        departments.create_index([('building', pymongo.ASCENDING), ('office', pymongo.ASCENDING)],
                                 unique=True,
                                 name='buildings_and_offices')

    if 'name' in departments_indexes.keys():
        print('name index present.')
    else:
        # Create a single UNIQUE index on name
        departments.create_index([('name', pymongo.ASCENDING)],
                                 unique=True,
                                 name='names')
    pprint(departments.index_information())

# schema 
    department_validator = {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'A department in a university.',
                'required': ['abbreviation', 'name', 'chair_name', 'building', 'office', 'description'],
                'additionalProperties': False,
                'properties': {
                    '_id': {'abbreviation'}, # primary key
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
