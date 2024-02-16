'''
Installations required -
pip install cloud-sql-python-connector["pymysql"] SQLAlchemy
pip install google-cloud-secret-manager
'''
#Import required dependencies

import random
import json
import pymysql
from mysql.database_connector import connection





## CHECKING VALUES FUNCTIONS
#--------------##-------------##-------------##

def user_id_check(_user_id):
    
    query = 'SELECT 1 FROM users WHERE user_id = %s;'
    print("Attempting to connect to the database...")
    
    try:

        cursor =  connection.cursor() 
        cursor.execute(query,(_user_id,))
        result = cursor.fetchone() 

        if result:
            print('User is registered.')
            return True
        else:
            print('User is not registered.')
            return False
    
    except Exception as e:
        print(f'Error checking user ID: {e}')
        return None

    



def check_user_survey_id(user_id):
    try:
        select_survey_id_query = """
            SELECT survey_id FROM users 
            WHERE user_id = %s AND survey_id IS NOT NULL;
        """
        
        cursor = connection.cursor()
        cursor.execute(select_survey_id_query, (user_id,))
        result = cursor.fetchone()
        print("debug result value from check_user_survey_id", result)

        if result:
            return result['survey_id']
        else:
            return False

    except Exception as e:
        print(f'Error checking user survey: {e}')



def check_chosen_ing_in_answers(survey_id):
    try:
        select_survey_id_query = """
            SELECT survey_answers FROM answers 
            WHERE survey_id = %s;
        """

        cursor = connection.cursor()
        cursor.execute(select_survey_id_query, (survey_id,))
        result = cursor.fetchone()
        print("debug result value from check_ing_chosen function:", result)
        
        if result:
    
            #chosen_ingredients = json.loads(result[0])  
            answers_compilation_json = result['survey_answers']
            answers_compilation = json.loads(answers_compilation_json)

            return answers_compilation
        else:
            return None

    except Exception as e:
        print(f'Error checking user survey: {e}')



def check_survey_id_uniqueness(survey_id):
   
    query = 'SELECT 1 FROM answers WHERE survey_id = %s;'
   
    try:
        cursor = connection.cursor()
        cursor.execute(query, (survey_id,))
        result = cursor.fetchone()
        
        if result:
            print('El bot te ha asignado un ID que ya existe!.')
            return False
        else:
            print('Survey ID is unique.')
            return True

    except Exception as e:
        print(f'Error checking survey status')
        return False





## REGISTER FUNCTIONS
#--------------##-------------##-------------##


def register_new_user(user_info):
    
    add_query = "INSERT INTO users (user_id, name, age, genre, location) VALUES (%s,%s,%s,%s,%s);"
    
    user_id, name, age, genre, location = user_info

    try:
        cursor = connection.cursor()
        cursor.execute(add_query, (user_id, name, age, genre, location))
        connection.commit()

        print("Insertion successful.")

        return f"Bienvenido '{name}'. El registro del usuario '{user_id}' ha sido exitoso. Presiona /cuestionario para comenzar tu diagnóstico nutricional"
    
    except Exception as e:
        print(f'Error registering new user: {e}')
    
    return False





def insert_chosen_ingredients(survey_id, chosen_ing):
    try:            
        chosen_ing_json = json.dumps(chosen_ing)
        print("debug survey_id value:", survey_id)
        print("debug chosen_ing_json value and type:", chosen_ing_json, type(chosen_ing_json) )
        add_survey_id = "UPDATE answers SET chosen_ingredients = %s WHERE survey_id = %s;"
        
        with connection.cursor() as cursor:
            cursor.execute(add_survey_id, (chosen_ing_json, survey_id))
            connection.commit()
            print("Chosen ingredients column updated")
        
        return True
       
    except Exception as e:
        print(f'Error inserting chosen ingredients: {e}')




def insert_survey_data(survey_data, plan_name_list):
    try:
        survey_name = plan_name_list[0]
        survey_id_value = generate_random_survey_id()
        
        user_id = list(survey_data.keys())[0]
        print("debug1 user_id and survey_name values:\n",user_id,survey_name)
        
        answers = survey_data.values()
        temp_dict = {}

        for key in answers:
            temp_dict.update(key)

        # Convert the dictionary to JSON format
        answer_compilation_value = json.dumps(temp_dict)

        
        print('debug2 answer_compilation:', answer_compilation_value, type(answer_compilation_value) )
        print('debug3 survey_id value:', survey_id_value, type(survey_id_value) )
        
        if survey_id_value:
            
            # Insert survey ID into users table
            add_survey_id = "UPDATE users SET survey_id = %s WHERE user_id = %s;"
            
            with connection.cursor() as cursor:
                cursor.execute(add_survey_id, (survey_id_value, user_id))
                connection.commit()
                print(f"User {user_id}, new survey_id: {survey_id_value}, updated in table users ")
            
            # Insert survey data into answers table
            add_answers = "INSERT INTO answers (survey_id, survey_name, survey_answers) VALUES (%s,%s,%s);"
        
            with connection.cursor() as cursor:
                cursor.execute(add_answers, (survey_id_value, survey_name, answer_compilation_value))
                connection.commit()
                print(f"Survey with survey_id {survey_id_value} inserted into 'answers' table")
            
            return survey_id_value, survey_name 

    except Exception as e:
        # Log the error for debugging
        print(f'Error registering new survey: {e}')
        return f'Failed to register survey: {e}'
    





## UTILITY FUNCTIONS
#--------------##-------------##-------------##

def generate_random_survey_id():
    min_val = 100000  # Minimum value for the random ID
    max_val = 999999  # Maximum value for the random ID
    while True:
        survey_id = random.randint(min_val, max_val)
        # Check if the random ID is already used
        if check_survey_id_uniqueness(survey_id):
            return survey_id
        