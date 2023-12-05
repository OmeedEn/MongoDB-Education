import pymongo
import pprint

#not sure if we need a primary key 
letter_grade_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': 'object',
            'description': 'A letter grade given to a specific course. ',
            'required': ['_id', 'minSatisfactory'],
            'additionalProperties': False,
            'properties': {
                '_id': {},
                'minSatisfactory': {
                    'bsonType': 'string',
                    'description': 'the minimum grade that would be satisfactory'
                }
            }
        }
    }
}
