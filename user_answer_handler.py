import json


user_answers = {}         #answers from questions
chosen_ingredients = []   #food choices
user_info = []            #name, age, genre, location



ingredients_file_path = "local-data/ingredients.json"

def read_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


## GET FUNCTIONS
#--------------##-------------##-------------##
def get_user_local_info():
    return user_info

def get_user_answers():
    return user_answers

def get_user_chosen_ing():
    return chosen_ingredients

def get_ingredient_category(ingredient):

    data = read_file(ingredients_file_path)
    
    for category, items in data['CLASIFICACION'].items():
        if ingredient in items:
            return category
    return "Unknown"





## UPDATE FUNCTIONS
#--------------##-------------##-------------##
def update_user_ingredients(ingredient):
    chosen_ingredients.append(ingredient)
    return chosen_ingredients

def update_user_answers(user_id, disease_key, question_key, answer_key):
    user_answers.setdefault(user_id, {})
    user_answers[user_id].setdefault(disease_key, {})
    user_answers[user_id][disease_key][question_key] = answer_key

def update_user_info(data):
    user_info.append(data)
    return user_info





## REMOVE, RESET FUNCTIONS
#--------------##-------------##-------------##
def remove_ingredient(ingredient):
    chosen_ingredients.remove(ingredient)

def reset_answers_data():
    user_answers.clear()

def reset_user_info():
    user_info.clear()

def reset_chosen_ingredients():
    chosen_ingredients.clear()
    return print("user_answer variable reseted to None")

   

