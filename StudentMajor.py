# collection 
 studentMajors = db['studentMajors']
    studentMajor_count = studentMajors.count_documents({})
    print(f'Student Majors in collection so far: {studentMajor_count}')


# unique index 


# schema 
student_major_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': 'object',
            'description': 'A major dedicated to a student',
            'required': ['declarationDate'],
            'additionalProperties': False,
            'properties': {
                '_id': {},
                'declarationDate': {
                    'bsonType': 'date',
                    'description': 'The date the Student declared his/her major. '
                }
            }
        }
    }
}
