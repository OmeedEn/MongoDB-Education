
from Menu import Menu
from Option import Option
"""
This little file just has the menus declared. Each variable (e.g. menu_main) has
its own set of options and actions. Although, you'll see that the "action" could
be something other than an operation to perform.
Doing the menu declarations here seemed like a cleaner way to define them. When
this is imported in main.py, these assignment statements are executed and the
variables are constructed. To be honest, I'm not sure whether these are global
variables or not in Python.
"""
# The main options for operating on Departments and Courses.
menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add", "add(db)"),
    Option("List", "list_objects(db)"),
    Option("Delete", "delete(db)"),
    # Option("Boilerplate Data", "boilerplate(db)"),
    Option("Exit this application", "pass")
])
add_menu = Menu('add', 'Please indicate what you want to add:', [
    Option("Department", "dep_add(db)"),
    Option("Course", "cour_add(db)"),
    Option("Major", "maj_add(db)"),
    Option("Student", "stud_add(db)"),
    Option("Section", "sec_add(db)"),
    Option("Student Major", "studmaj_add(db)"),
    # Option("Student to Major", "add_student_major(db)"),
    # Option("Major to Student", "add_major_student(db)"),
    Option("Exit", "pass")
])
delete_menu = Menu('delete', 'Please indicate what you want to delete from:', [
    Option("Department", "dep_del(db)"),
    Option("Course", "cour_del(db)"),
    Option("Major", "maj_del(db)"),
    Option("Student", "stud_del(db)"),
    Option("Section", "sec_del(db)"),
    Option("Student Major", "studmaj_del(db)"),
    # Option("Student to Major", "delete_student_major(db)"),
    # Option("Major to Student", "delete_major_student(db)"),
    Option("Exit", "pass")
])
list_menu = Menu('list', 'Please indicate what you want to list:', [
    Option("Department", "dep_lis(db)"),
    Option("Course", "cour_lis(db)"),
    Option("Major", "maj_lis(db)"),
    Option("Student", "stud_lis(db)"),
    Option("Student Major", "studmaj_lis(db)"),
    # Option("Student to Major", "list_student_major(db)"),
    # Option("Major to Student", "list_major_student(db)"),
    Option("Exit", "pass")
])
