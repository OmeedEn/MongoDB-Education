# collection 
majors = db['majors']
    major_count = majors.count_documents({})
    print(f'Majors in collection so far: {major_count}')

# unique index 
majors_indexes = majors.index_information()
    
    if 'name' in majors_indexes.keys():
        print('major name index present')
        
    else:
        # create a single UNIQUE index on major name
        majors.create_index([('name', pymongo.ASCENDING)],
                            unique=True,
                            name='name')

# schema 


