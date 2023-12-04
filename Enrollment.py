# collections
enrollments = db['enrollments']
    enrollment_count = enrollments.count_documents({})
    print(f'Enrollments in collection so far: {enrollment_count}')

# unique index 
enrollments_index = enrollments.index_information()

    if 'student_and_section' in enrollments_index.keys():
        print('student and section index present')
    else:
        # create a UNIQUE index on student and section
        enrollments.create_index([('student', pymongo.ASCENDING), ('section', pymongo.ASCENDING)],
                                 unique=True,
                                 name='student_and_sections')
    if 'semester_sectionYear_departmentAbbreviation_courseNumber_studentID' in enrollments_index.keys():
        print('semester, section year, department abbreviation, course number, student ID index present')
    else:
        # create a UNIQUE index on semester, section year, department abbreviation, course number, student ID
        enrollments.create_index([('semester', pymongo.ASCENDING), ('sectionYear', pymongo.ASCENDING),
                                  ('departmentAbbreviation', pymongo.ASCENDING), ('courseNumber', pymongo.ASCENDING),
                                  ('studentID', pymongo.ASCENDING)],
                                 unique=True,
                                 name='semester_sectionYear_departmentAbbreviation_courseNumber_studentIDs')
    pprint(enrollments.index_information())


# schema 
#im not sure if we need schemas or relations to the other passfail/lettergrade files

