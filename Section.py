import pymongo
from orm_base import Base
from sqlalchemy import Table
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from sqlalchemy import String, Integer, Identity
from sqlalchemy.types import Time
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint, CheckConstraint
from IntrospectionFactory import IntrospectionFactory
from Enrollment import Enrollment
from Course import Course
from typing import List
from datetime import time
class Section(db):

    section_validator = {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'A Section in a Course.',
                'required': ['departmentAbbreviation', 'sectionId', 'name', 'courseNumber', 'sectionNumber', 'semester',
                             'sectionYear', 'schedule', 'room', 'building', 'startTime', 'instructor'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'departmentAbbreviation': {
                        'bsonType': 'string',
                        'minLength': 1,
                        'maxLength': 6,
                        'description': 'Short phrase that describes a department name.'
                        # add foreign key
                    },
                    'sectionId': {
                        'bsonType': 'integer',
                        'minLength': 1,
                        'maxLength': 50,
                        'description': 'The Id that is given to a Section of a Course'
                        # add primary key
                    },
                    'name': {
                        'bsonType': 'string',
                        'minLength': 1,
                        'maxLength': 50,
                        'description': 'A word that refers to a course.'
                    },
                    'courseNumber': {
                        'bsonType': 'string',
                        'minLength': 1,
                        'maxLength': 80,
                        'description': 'The number associated to the course.'
                    },
                    'sectionNumber': {
                        'bsonType': 'integer',
                        'description': 'The number of the section.'
                    },
                    'semester': {
                        'bsonType': 'string',
                        'enum': ['Fall', 'Spring', 'Winter', 'Summer I', 'Summer II'],
                        'minLength': 1,
                        'maxLength': 50,
                        'description': 'The given semester a course is in.'
                    },
                    'sectionYear': {
                        'bsonType': 'integer',
                        'description': 'The year the given section is offered in.'
                    },
                    'schedule': {
                        'bsonType': 'string',
                        'minLength': 1,
                        'maxLength': 6,
                        'enum': ['MW', 'TuTh', 'MWF', 'F', 'S'],
                        'description': 'the schedule of the given class'
                    },
                    'room': {
                        'bsonType': 'integer',
                        'description': 'the room for the class.'
                    },
                    'building': {
                        'bsonType': 'string',
                        'minLength': 1,
                        'maxLength': 6,
                        'enum': ['VEC','ECS','EN2','EN3','EN4','ET','SSPA'],
                        'description': 'the building that the section is being taught in'
                    },
                    'startTime': {
                        'bsonType': 'time',
                        'description': 'the time the class starts at'
                    },
                    'instructor': {
                        'bsonType': 'string',
                        'minLength': 1,
                        'maxLength': 80,
                        'description': 'the teacher for the class'
                    }
                }

            }
        }
    }



    def __init__(self, course: Course, sectionNumber: int,
                 semester: str, sectionYear: int, building: str, room: int, schedule: str,
                 startTime: Time, instructor: str):
        self.set_course(course)
        self.sectionNumber = sectionNumber
        self.semester = semester
        self.sectionYear = sectionYear
        self.building = building
        self.room = room
        self.schedule = schedule
        self.startTime = startTime
        self.instructor = instructor

    # initialize migrated values from course into section
    def set_course(self, course: Course):
        self.course = course
        self.departmentAbbreviation = course.departmentAbbreviation
        self.courseNumber = course.courseNumber

    # basing off add_major/add_student from student.py
    def add_student(self, student):
        for next_student in self.students:
            if next_student.student == student:
                return
        enrollment = Enrollment(student, self)


    def remove_enrollment(self, student):
        for next_student in self.students:
            if next_student.student == student:
                self.students.remove(next_student)
                return

    def __str__(self):
        return f"Department Abbreviation: {self.departmentAbbreviation}\nCourse Number: {self.courseNumber}\n" \
               f"Section Number: {self.sectionNumber}\nSemester: {self.semester}\nSection Year: {self.sectionYear}\n" \
               f"Building: {self.building}\nRoom: {self.room}\nSchedule: {self.schedule}\nStart Time: {self.startTime}\n" \
               f"Instructor: {self.instructor}"