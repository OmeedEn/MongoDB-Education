import pymongo
import pprint

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
                    'enum': ['A', 'B', 'C'],
                    'description': 'the minimum grade that would be satisfactory'
                }
            }
        }
    }
}
