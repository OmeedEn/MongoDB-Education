import pymongo
from pprint import pprint
from pymongo.errors import CollectionInvalid, OperationFailure


# imported add/delete/list functions
def add_student(db):

    collection = db["students"]

    unique_name: bool = False
    unique_email: bool = False
    lastName: str = ''
    firstName: str = ''
    email: str = ''
    while not unique_name or not unique_email:
        lastName = input("Student last name--> ")
        firstName = input("Student first name--> ")
        email = input("Student e-mail address--> ")
        name_count: int = collection.count_documents({"last_name": lastName, "first_name": firstName})
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a student by that name. Try again.")
        if unique_name:
            email_count = collection.count_documents({"e_mail": email})
            unique_email = email_count == 0
            if not unique_email:
                print("We already have a student with that e-mail address. Try again.")
    student = {
        "last_name": lastName,
        "first_name": firstName,
        "e_mail": email
    }
    collection.insert_one(student)
def select_student(db):
    """
    Select a student by the combination of the last and first.
    :param db: The connection to the database.
    :return: The selected student as a dict. This is not the same as it was
    in SQLAlchemy, it is just a copy of the Student document from
    the database.
    """
    # Create a connection to the students collection from this database
    collection = db["students"]
    found: bool = False
    lastName: str = ''
    firstName: str = ''
    while not found:
        lastName = input("Student's last name--> ")
        firstName = input("Student's first name--> ")
        name_count: int = collection.count_documents({"last_name": lastName,
        "first_name": firstName})
        found = name_count == 1
    if not found:
        print("No student found by that name. Try again.")
    found_student = collection.find_one({"last_name": lastName, "first_name": firstName})
    return found_student

def delete_student(db):
    student = select_student(db)
    students = db["students"]
    student_majors = db['studentMajors']
    enrollments = db['enrollments']
    n_stuMaj = student_majors.count_documents({'studentId': student['_id']})
    n_enrollments = enrollments.count_documents({'studentId': student['_id']})
    if n_stuMaj > 0:
        print(f'Sorry, there are {n_stuMaj} majors for that student. Delete them first, then come back here to '
              f'delete the student.')
    elif n_enrollments > 0:
        print(f'Sorry, there are {n_enrollments} enrollments for that student. Delete them first, then come back here '
              f'to delete the student.')
    else:
        deleted = students.delete_one({"_id": student["_id"]})
        print(f"We just deleted: {deleted.deleted_count} students.")

def list_student(db):
    """
    List all of the students, sorted by last name first, then the first name.
    :param db: The current connection to the MongoDB database.
    :return: None
    """
    # No real point in creating a pointer to the collection, I'm only using it
    # once in here. The {} inside the find simply tells the find that I have
    # no criteria. Essentially this is analogous to a SQL find * from students.
    # Each tuple in the sort specification has the name of the field, followed
    # by the specification of ascending versus descending.
    students = db["students"].find({}).sort([("last_name", pymongo.ASCENDING), ("first_name", pymongo.ASCENDING)])
    # pretty print is good enough for this work. It doesn't have to win a beauty contest.
    for student in students:
        pprint(student)

# schema function
def create_student(db):

    # collections
    students = db["students"]
    student_count = students.count_documents({})
    print(f"Students in the collection so far: {student_count}")

    # unique index
    students_indexes = students.index_information()
    if 'students_last_and_first_names' in students_indexes.keys():
        print("first and last name index present.")
    else:
        # Create a single UNIQUE index on BOTH the last name and the first name.
        students.create_index([('last_name', pymongo.ASCENDING), ('first_name', pymongo.ASCENDING)],
                              unique=True,
                              name="students_last_and_first_names")
    if 'students_e_mail' in students_indexes.keys():
        print("e_mail address index present.")
    else:
        # Create a UNIQUE index on just the e-mail address
        students.create_index([('e_mail', pymongo.ASCENDING)],
                              unique=True,
                              name='students_e_mail')
    pprint(students.index_information())

    student_validator = {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'A student in a university.',
                'required': ['last_name', 'first_name', 'e_mail'],
                'additionalProperties': True,
                'properties': {
                    '_id': {},# create unique index
                    'last_name': {
                        'bsonType': 'string',
                        'minLength': 1,
                        'maxLength': 50,
                        'description': 'Last name of the student'
                    },
                    'first_name': {
                        'bsonType': 'string',
                        'minLength': 1,
                        'maxLength': 50,
                        'description': 'First name of the student'
                    },
                    'e_mail': {
                        'bsonType': 'string',
                        'minLength': 1,
                        'maxLength': 255,
                        'description': 'email of the student'
                    }
                }
            }
        }
    }
    db.command('collMod', 'students', **student_validator)
