import pymongo
import pprint
# collection
majors = db['majors']
    major_count = majors.count_documents({})
    print(f'Majors in collection so far: {major_count}')

# unique index 
majors_indexes = majors.index_information()
    
    if 'name' in majors_indexes.keys():
        print('major name index present')
        
    else:
        # create a single UNIQUE index on major name
        majors.create_index([('name', pymongo.ASCENDING)],
                            unique=True,
                            name='name')
    pprint(majors.index_information())

# schema

major_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': 'object',
            'description': 'A major in a department.',
            'required': ['_id', 'description'], #i dont think we need the name attribute in here anymore
            'additionalProperties': False,
            'properties': {
                '_id': {
                    'bsonType': 'string',
                    'minLength': 1,
                    'maxLength': 50,
                    'description': 'A word that refers to a major.'
                }, #change to relationship
                # 'name': {
                #     'bsonType': 'string',
                #     'minLength': 1,
                #     'maxLength': 50,
                #     'description': 'A word that refers to a major.'
                # },
                'description': {
                    'bsonType': 'string',
                    'minLength': 10,
                    'maxLength': 80,
                    'description': 'Statement that describes the major.'
                }
            }
        }
    }
}


