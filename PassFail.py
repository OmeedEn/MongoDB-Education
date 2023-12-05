import pymongo
import pprint

passFail_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': 'object',
            'description': 'Determines whether the student is pass/fail for a specific enrollment.',
            'required': ['_id', 'applicationDate'],
            'additionalProperties': False,
            'properties': {
                '_id': {},
                'applicationDate': {
                    'bsonType': 'date',
                    'description': 'the date the application was put in'
                }
            }
        }
    }
}

