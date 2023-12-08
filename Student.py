import pymongo
from pymongo import MongoClient
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
    # Build a new students document preparatory to storing it
    student = {
        # "_id": student.studentID # not sure if we need this
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
    """
    Delete a student from the database.
    :param db: The current database connection.
    :return: None
    """
    # student isn't a Student object (we have no such thing in this application)
    # rather it's a dict with all the content of the selected student, including
    # the MongoDB-supplied _id column which is a built-in surrogate.
    student = select_student(db)
    # Create a "pointer" to the students collection within the db database.
    students = db["students"]
    # student["_id"] returns the _id value from the selected student document.
    deleted = students.delete_one({"_id": student["_id"]})
    # The deleted variable is a document that tells us, among other things, how
    # many documents we deleted.
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
    # if '_id' in students_indexes.keys():
    #     print('id index present.')
    # else:
    #     # create a UNIQUE index on the _id
    #     students.create_index(['_id', pymongo.ASCENDING],
    #                           unique=True,
    #                           name='_ids')
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

