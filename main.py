import pymongo
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu
import Department
import Student
import Major
import Section
import Course
import StudentMajor
import Enrollment
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

def dep_add(db):
    Department.add_department(db)
def dep_sel(db):
    Department.select_department(db)
def dep_lis(db):
    Department.list_department(db)
def dep_del(db):
    Department.delete_department(db)
def stud_add(db):
    Student.add_student(db)
def stud_sel(db):
    Student.select_student(db)
def stud_lis(db):
    Student.list_student(db)
def stud_del(db):
    Student.delete_student(db)
def maj_add(db):
    Major.add_major(db)
def maj_sel(db):
    Major.select_major(db)
def maj_lis(db):
    Major.list_majors(db)
def cour_add(db):
    Course.add_course(db)
def cour_sel(db):
    Course.select_course(db)
def cour_lis(db):
    Course.list_course(db)
def sec_add(db):
    Section.add_section(db)
def sec_sel(db):
    Section.select_section(db)
def sec_del(db):
    Section.delete_section(db)
def studmaj_add(db):
    StudentMajor.add_student_major(db)
def studmaj_lis(db):
    StudentMajor.list_student_major(db)
def studmaj_del(db):
    StudentMajor.delete_student_major(db)
def enroll_add_let(db):
    Enrollment.add_letter_grade(db)
def enroll_add_pas(db):
    Enrollment.add_student_pass_fail(db)

if __name__ == '__main__':
    cluster = 'mongodb+srv://omeedenshaie01:QXK8h6E3JeYWa8mX@cluster0.u4fphnt.mongodb.net/?retryWrites=true&w=majority'
    print(f"Cluster: {cluster}")
    client = MongoClient(cluster)
    # As a test that the connection worked, print out the database names.
    print(client.list_database_names())
    # db will be the way that we refer to the database from here on out.
    db = client["MongoEducation"]
    # Print off the collections that we have available to us, again more of a test than anything.
    print(db.list_collection_names())

    Department.create_department(db)
    Course.create_course(db)
    Student.create_student(db)
    Major.create_major(db)
    Section.create_section(db)
    #Enrollment.create_enrollment(db)
    StudentMajor.create_student_major(db)

    # insert our student, department, major, course collections here when ready...
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
