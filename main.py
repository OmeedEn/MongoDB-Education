import pymongo
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
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
        # "_id": student.studentID # not sure if we need this
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
    students = db["students"].find({}).sort([("last_name", pymongo.ASCENDING), ("first_name", pymongo.ASCENDING)])
    # pretty print is good enough for this work. It doesn't have to win a beauty contest.
    for student in students:
        pprint(student)

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

def add_course(db):
    collection = db["courses"]

    print("Which department offers this course?")
    department = select_department(db)  # This function should be implemented to select a department.
    unique_number = False
    unique_name = False
    number = -1
    name = ''

    while not unique_number or not unique_name:
        name = input("Course full name--> ")
        number = int(input("Course number--> "))

        name_count = collection.count_documents({'department': department, 'name': name})
        unique_name = name_count == 0

        if not unique_name:
            print("We already have a course by that name in that department. Try again.")

        if unique_name:
            number_count = collection.count_documents({'department': department, 'number': number})
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

    collection.insert_one(course)

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

def add_section(db):
    collection = db["sections"]
    # Assuming you have a function to select a course
    course = select_course(db)

    unique_section_number = False
    unique_room = False
    unique_instructor = False

    while not (unique_section_number and unique_room and unique_instructor):
        section_number = int(input("Section number--> "))
        section_year = int(input("Section Year--> "))
        semester = input("Section semester--> ")
        schedule = input("Schedule--> ")
        start_time_hour = int(input("Section start time hour--> "))
        start_time_minute = int(input("Section start time minute--> "))
        building = input("Section building--> ")
        room = int(input("Section room--> "))
        instructor = input("Section instructor--> ")

        # Validate semester, schedule, building, etc. as needed

        # Construct startTime as a string or a datetime object
        start_time = datetime(section_year, 1, 1, start_time_hour, start_time_minute)

        # Check for unique section number
        section_count = collection.count_documents({
            "course_id": course["_id"],
            "section_number": section_number,
            "semester": semester,
            "section_year": section_year
        })
        unique_section_number = section_count == 0

        # Check for unique room set
        room_set_count = collection.count_documents({
            "section_year": section_year,
            "semester": semester,
            "schedule": schedule,
            "start_time": start_time,
            "building": building,
            "room": room
        })
        unique_room_set = room_set_count == 0

        # Check for unique instructor set
        instructor_set_count = collection.count_documents({
            "section_year": section_year,
            "semester": semester,
            "schedule": schedule,
            "start_time": start_time,
            "instructor": instructor
        })
        unique_instructor_set = instructor_set_count == 0

        if not unique_section_number:
            print("Section number already exists for this course. Try again.")
        elif not unique_room_set:
            print("Room is already booked for this time. Try again.")
        elif not unique_instructor_set:
            print("Instructor is already teaching at this time. Try again.")

        new_section = {
            "course_id": course["_id"],
            "section_number": section_number,
            "semester": semester,
            "section_year": section_year,
            "building": building,
            "room": room,
            "schedule": schedule,
            "start_time": start_time,
            "instructor": instructor
        }

        collection.insert_one(new_section)
def select_section(db):
    collection = db["section"]
    found: bool = False
    section_year: int
    semester: str
    schedule: str
    instructor: str

    while not found:
        section_year = int(input("Enter section year: "))
        semester = input("Enter semester: ")
        schedule = input("Enter schedule: ")
        instructor = input("Enter instructor: ")

        section_s = {
            "sectionYear": section_year,
            "semester": semester,
            "schedule": schedule,
            "instructor": instructor
        }

        section = collection.find_one(section_s)

        if section:
            print("Selected section:\n", section)
            return section
        else:
            print("No section with those values for that course. Try again.")

def delete_section(db):

    section_collection = db["sections"]
    enrollment_collection = db["enrollments"]

    print("Deleting a section")

    # Assuming you have a function to select a section
    section = select_section(db)

    if section is None:
        print("No section selected or section not found.")
        return

    # Assuming 'sectionID' in the 'enrollments' collection references 'sectionID' in the 'sections' collection
    n_enrollments = enrollment_collection.count_documents({"sectionID": section["_id"]})

    if n_enrollments > 0:
        print(f"Sorry, there are {n_enrollments} enrollments in that section. Delete them first, "
              f"then come back here to delete the section.")
    else:
        section_collection.delete_one({"_id": section["_id"]})
        print("Section deleted successfully.")

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

def list_majors(db):

    majors = db["majors"].find({}).sort([("", pymongo.ASCENDING),
                                        ("", pymongo.ASCENDING)])

    for major in majors:
        pprint(major)

def add_student_major(db):

    collection = db["student_major"]
    student = select_student(db)  # Assuming select_student is adapted for MongoDB
    major = select_major(db)  # Assuming select_major is adapted for MongoDB

    # Check if the student already has this major
    student_major_count = collection.count_documents({
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
def add_letter_grade(db):
    collection = db["enrollments"]

    unique_student_section = False
    while not unique_student_section:
        grade = input("What is the Satisfactory grade?---> ")

        # Assuming select_student and select_section return the ObjectId of the selected document
        student_id = select_student(db)  # Modify this function as needed
        section_id = select_section(db)  # Modify this function as needed

        # Check if the student is already enrolled in the section
        enrollment = collection.find_one({"studentId": student_id, "sectionId": section_id})

        if not enrollment:
            print("No enrollment record found for that student and section. Try again.")
        else:
            # Update the enrollment record with the letter grade
            letter_grade = {
                "minSatisfactory": grade  # Assuming you want to record the date of grade assignment
            }

            collection.update_one(
                {"_id": enrollment["_id"]},
                {"$set": {"letterGrade": letter_grade}}
            )
            print("Letter grade added to the student's enrollment.")
            unique_student_section = True
def add_student_pass_fail(db):

    collection = db["enrollments"]

    student_id = select_student(db)
    section_id = select_section(db)
    # Check if the student is already enrolled in the section
    if collection.find_one({'studentId': student_id, 'sectionId': section_id}):
        print("That section already has that student enrolled in it. Try again.")
        return

    # Create a pass/fail record as a subschema
    pass_fail = {
        'applicationDate': datetime.now(),
        # Add other passFail fields here if necessary
    }

    # Create the enrollment record with the passFail subschema
    enrollment = {
        'studentId': student_id,
        'sectionId': section_id,
        'passFail': pass_fail,
        # Include other fields or subschemas (like letterGrade) if necessary
    }

    # Add the enrollment record to the enrollments collection
    collection.insert_one(enrollment)
    print("Student added to section as pass/fail.")

if __name__ == '__main__':
    cluster = "mongodb+srv://AngelaAndJustin:SpkZVc@cecs323.mxqdekf.mongodb.net/?retryWrites=true&w=majority"
    print('Cluster: mongodb+srv://AngelaAndJustin:****@cecs323.mxqdekf.mongodb.net/?retryWrites=true&w=majority')
    client = MongoClient(cluster)
    # As a test that the connection worked, print out the database names.
    print(client.list_database_names())
    # db will be the way that we refer to the database from here on out.
    db = client["CECS323MongoDB"]
    # Print off the collections that we have available to us, again more of a test than anything.
    print(db.list_collection_names())

    # insert our student, department, major, course collections here when ready...

    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
