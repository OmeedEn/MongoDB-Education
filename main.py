import pymongo
from pymongo import MongoClient
from pprint import pprint
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu

def add(db):
    """
    Present the add menu and execute the user's selection.
    :param db: The connection to the current database.
    :return: None
    """
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
    exec(add_action)

def delete(db):
    """
    Present the delete menu and execute the user's selection.
    :param db: The connection to the current database.
    :return: None
    """
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
    exec(delete_action)

def list_objects(db):
    """
    Present the list menu and execute the user's selection.
    :param db: The connection to the current database.
    :return: None
    """
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
    exec(list_action)

def add_student(db):
    """
    Add a new student, making sure that we don't put in any duplicates,
    based on all the candidate keys (AKA unique indexes) on the
    students collection. Theoretically, we could query MongoDB to find
    the uniqueness constraints in place, and use that information to
    dynamically decide what searches we need to do to make sure that
    we don't violate any of the uniqueness constraints. Extra credit anyone?
    :param collection: The pointer to the students collection.
    :return: None
    """
    # Create a "pointer" to the students collection within the db database.
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
        name_count: int = collection.count_documents({"last_name": lastName,
        "first_name": firstName})
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
    "last_name": lastName,
    "first_name": firstName,
    "e_mail": email
    }
    results = collection.insert_one(student)
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
    found_student = collection.find_one({"last_name": lastName, "first_name":firstName})
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
    students = db["students"].find({}).sort([("last_name", pymongo.ASCENDING),
    ("first_name", pymongo.ASCENDING)])
    # pretty print is good enough for this work. It doesn't have to win a beauty contest.
    for student in students:
        pprint(student)


def select_department(db):
    collection = db["department"]
    found: bool = False
    name: str = ''
    while not found:
        name = input("Department's name--> ")
        name_count: int = collection.count_documents({"name": name})
        found = name_count == 1
        if not found:
            print("No department found by that name. Try again.")
    found_department = collection.find_one({"name": name})
    return found_department

def add_department(db):
    # collection pointer to department collections in db
    collection = db["department"]
    unique_name: bool = False
    unique_abbreviation: bool = False
    unique_chair_name: bool = False
    unique_building_and_office: bool = False
    unique_description: bool = False
    name: str = ''
    abbreviation: str = ''
    chair_name: str = ''
    building: str = ''
    office: int = 0
    description: str = ''
    while not unique_abbreviation or not unique_name or not unique_chair_name or not unique_building_and_office or not unique_description:
        name = input("Department full name--> ")
        abbreviation = input("Department abbreviation--> ")
        chair_name = input("Department chair name--> ")
        building = input("Department building--> ")
        office = int(input("Department office--> "))
        description = input("Department description--> ")
        name_count: int = collection.count_documents({"name": name})
        unique_name = name_count == 0
        if not unique_name:
            print("There is already a department with that name. Try again")
        if unique_name:
            abbreviation_count = collection.count_documents({"abbreviation": abbreviation})
            unique_abbreviation = abbreviation_count == 0
        if not unique_abbreviation:
            print("We already have a department with that abbreviation. Try again.")
        if unique_abbreviation:
            chair_count = collection.count_documents({"chair_name": chair_name})
            unique_chair_name = chair_count == 0
            if not unique_chair_name:
                print("We already have a department with that chair name. Try again.")
                if unique_chair_name:
                    build_office_count = collection.count_documents({"building": building, "office": office})
                    unique_building_and_office = build_office_count == 0
                    if not unique_building_and_office:
                        print("We already have a department with that building and office. Try again.")
                        if unique_building_and_office:
                            description_count = collection.count_documents({"description": description})
                            unique_description = description_count == 0
                            if not unique_description:
                                print("We already have a department with that description. Try again.")

    department = {
    "name": name,
    "abbreviation": abbreviation,
    "chair_name": chair_name,
    "building": building,
    "office": office,
    "description": description
    }
    result = collection.insert_one(department)

def list_department(db):
    departments = db["department"].find({}).sort([("name", pymongo.ASCENDING)])
    # pretty print is good enough for this work. It doesn't have to win a beauty contest.
    for department in departments:
        pprint(department)

def delete_department(db):
    department = select_department(db)
    # Create a "pointer" to the students collection within the db database.
    departments = db["department"]
    # student["_id"] returns the _id value from the selected student document.
    deleted = departments.delete_one({"_id": department["_id"]})
    # The deleted variable is a document that tells us, among other things, how
    # many documents we deleted.
    print(f"We just deleted: {deleted.deleted_count} departments.")

#add add, delete, select, and list for course, section, major...

def select_department(db):
    collection = db["department"]
    found: bool = False
    name: str = ''
    while not found:
        name = input("Department's name--> ")
        name_count: int = collection.count_documents({"name": name})
        found = name_count == 1
        if not found:
            print("No department found by that name. Try again.")
    found_department = collection.find_one({"name": name})
    return found_department

def add_department(db):
    # collection pointer to department collections in db
    collection = db["department"]
    unique_name: bool = False
    unique_abbreviation: bool = False
    unique_chair_name: bool = False
    unique_building_and_office: bool = False
    unique_description: bool = False
    name: str = ''
    abbreviation: str = ''
    chair_name: str = ''
    building: str = ''
    office: int = 0
    description: str = ''
    while not unique_abbreviation or not unique_name or not unique_chair_name or not unique_building_and_office or not unique_description:
        name = input("Department full name--> ")
        abbreviation = input("Department abbreviation--> ")
        chair_name = input("Department chair name--> ")
        building = input("Department building--> ")
        office = int(input("Department office--> "))
        description = input("Department description--> ")
        name_count: int = collection.count_documents({"name": name})
        unique_name = name_count == 0
        if not unique_name:
            print("There is already a department with that name. Try again")
        if unique_name:
            abbreviation_count = collection.count_documents({"abbreviation": abbreviation})
            unique_abbreviation = abbreviation_count == 0
        if not unique_abbreviation:
            print("We already have a department with that abbreviation. Try again.")
        if unique_abbreviation:
            chair_count = collection.count_documents({"chair_name": chair_name})
            unique_chair_name = chair_count == 0
            if not unique_chair_name:
                print("We already have a department with that chair name. Try again.")
                if unique_chair_name:
                    build_office_count = collection.count_documents({"building": building, "office": office})
                    unique_building_and_office = build_office_count == 0
                    if not unique_building_and_office:
                        print("We already have a department with that building and office. Try again.")
                        if unique_building_and_office:
                            description_count = collection.count_documents({"description": description})
                            unique_description = description_count == 0
                            if not unique_description:
                                print("We already have a department with that description. Try again.")

    department = {
    "name": name,
    "abbreviation": abbreviation,
    "chair_name": chair_name,
    "building": building,
    "office": office,
    "description": description
    }

    collection.insert_one(department)

def list_department(db):
    departments = db["department"].find({}).sort([("name", pymongo.ASCENDING)])
    # pretty print is good enough for this work. It doesn't have to win a beauty contest.
    for department in departments:
        pprint(department)

def delete_department(db):
    department = select_department(db)
    # Create a "pointer" to the students collection within the db database.
    departments = db["department"]
    # student["_id"] returns the _id value from the selected student document.
    deleted = departments.delete_one({"_id": department["_id"]})
    # The deleted variable is a document that tells us, among other things, how
    # many documents we deleted.
    print(f"We just deleted: {deleted.deleted_count} departments.")

#add add, delete, and list for course, section, major...

def add_course(db):
    """
    Prompt the user for the information for a new course and validate
    the input to make sure that we do not create any duplicates.
    :param db: The database connection.
    :return:    None
    """
    print("Which department offers this course?")
    department = select_department(db)  # This function should be implemented to select a department.
    unique_number = False
    unique_name = False
    number = -1
    name = ''

    while not unique_number or not unique_name:
        name = input("Course full name--> ")
        number = int(input("Course number--> "))

        name_count = db.courses.count_documents({'department': department, 'name': name})
        unique_name = name_count == 0

        if not unique_name:
            print("We already have a course by that name in that department. Try again.")

        if unique_name:
            number_count = db.courses.count_documents({'department': department, 'number': number})
            unique_number = number_count == 0

            if not unique_number:
                print("We already have a course in this department with that number. Try again.")

    description = input('Please enter the course description-->')
    units = int(input('How many units for this course-->'))

    course = {
        'department': department,
        'number': number,
        'name': name,
        'description': description,
        'units': units
    }

    db.courses.insert_one(course)

def select_course(db):
    collection = db["course"]
    found: bool = False
    department_abbreviation = ''
    course_number = -1

    while not found:
        department_abbreviation = input("Department abbreviation--> ")
        course_number = int(input("Course Number--> "))

        found = course_number == 1
        if not found:
            print("No course by that number in that department. Try again.")

    course = collection.find_one(
        {'departmentAbbreviation': department_abbreviation, 'courseNumber': course_number})

    return course

def list_course(db):
    courses = db["courses"].find({}).sort([("", pymongo.ASCENDING),
                                           ("", pymongo.ASCENDING)])
    for course in courses:
        pprint(course)

def add_major(db):
    collection = db["majors"]
    print("Which department offers this major?")
    department = select_department(db)  # Assuming select_department is adapted for MongoDB
    unique_name = False
    name = ''

    while not unique_name:
        name = input("Major name--> ")
        name_count = db.majors.count_documents({'name': name, 'departmentAbbreviation': department['abbreviation']})
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a major by that name in that department. Try again.")

    description = input('Please give this major a description -->')
    major = {
        'name': name,
        'description': description
    }
    collection.insert_one(major)

def select_major(db):

    collection = db["major"]
    found: bool = False
    name = ''

    while not found:
        name = input("Major's name--> ")
        major = collection.find_one({'name': name})
        found = major is not None
        if not found:
            print("No major found by that name. Try again.")

    major = collection.find_one(
        {'name': name})

    return major
    
def add_student_major(db):

    collection = db["student_major"]
    student = select_student(db)  # Assuming select_student is adapted for MongoDB
    major = select_major(db)  # Assuming select_major is adapted for MongoDB

    # Check if the student already has this major
    student_major_count = db.student_majors.count_documents({
        'studentId': student['_id'],  # Assuming student ID is stored in '_id'
        'majorName': major['name']  # Assuming major name is stored in 'name'
    })

    unique_student_major = student_major_count == 0

    while not unique_student_major:
        print("That student already has that major. Try again.")
        student = select_student(db)
        major = select_major(db)
        student_major_count = db.students.count_documents({
            '_id': student['_id'],
            'majors': major['name']
        })
        unique_student_major = student_major_count == 0

    collection.add(student, major)

def delete_student_major(db):
    collection = db["student_major"]
    print("Prompting you for the student and the major that they no longer have.")
    student = select_student(db)  # Assuming select_student is adapted for MongoDB
    major = select_major(db)  # Assuming select_major is adapted for MongoDB

    collection.delete_one({"_id": student["_id"]})
    collection.delete_one({"_id": major["_id"]})
    print("We just deleted the student_major. ")

def list_student_major(db):
    student = select_student(db)  # Assuming select_student is adapted for MongoDB
    # Assuming each student document has a 'majors' field that is a list of major names
    student_data = db.students.find_one({'_id': student['_id']}, {'majors': 1, 'lastName': 1, 'firstName': 1})

    if student_data and 'majors' in student_data:
        for major_name in student_data['majors']:
            major_data = db.majors.find_one({'name': major_name}, {'description': 1})
            if major_data:
                print(
                    f"Student name: {student_data['lastName']}, {student_data['firstName']}, Major: {major_name}, Description: {major_data.get('description', 'No description')}")
    else:
        print("No majors found for this student.")

if __name__ == '__main__':
    cluster = ""
    client = MongoClient(cluster)
    # As a test that the connection worked, print out the database names.
    print(client.list_database_names())
    # db will be the way that we refer to the database from here on out.
    db = client["Demonstration"]
    # Print off the collections that we have available to us, again more of a test than anything.
    print(db.list_collection_names())

    # insert our student, department, major, course collections here when ready...

    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
