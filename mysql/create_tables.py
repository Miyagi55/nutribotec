from test_mysql import connection



def create_tables():
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE users (
            user_id VARCHAR(25) PRIMARY KEY,
            survey_id INT,
            name TEXT,
            age INT,
            genre TEXT,
            location TEXT,
            ibm INT
        );
        ''')
        cursor.execute('''
            CREATE TABLE answers (
            survey_id INT PRIMARY KEY,
            survey_name TEXT,
            survey_answers JSON,
            chosen_ingredients JSON,
            feedback JSON
        );

        ''')
        print("tables users and answers created")
    finally:
        connection.close()
    return

create_tables()