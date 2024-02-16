import os
import json
from database_manager import check_chosen_ing_in_answers


ingredients_file_path = "local-data/ingredients.json"


def read_ingredients(ingredients_file_path):
    with open(ingredients_file_path, 'r') as file:
        data = json.load(file)
    return data




def get_standard_portion(ingredients_data, ingredient):

    standard_portion = ingredients_data[f'{ingredient}']
    return standard_portion ## dentro de ingredients.values()



def get_user_ingredients_and_answers_from_db(survey_id):
    user_answers = check_chosen_ing_in_answers(survey_id)
    return user_answers


def evaluate_survey_answers(survey_id):

    answers_from_survey = check_chosen_ing_in_answers(survey_id)

    
    lst = list(answers_from_survey.items())

    print("debug answers from survey: ", lst[0][1])
    
    score = 0
    for answer in lst[0][1].values():
            print("debug question and answer:", answer)
            if answer == 'answer1':
                score += 1
            elif answer == 'answer3':
                score -= 1

    result = score_logic(score)   
    
    
    return result, score


def score_logic(score):

    if score > 2:
        return 'alta'
    elif -2 <= score < 2:
        return 'media'
    elif -5 <= score < -2:
        return 'baja'





def read_diet_json_files(directory):
    """Reads all JSON files ending with '_diet.json' in the specified directory."""
    json_data = []
    for filename in os.listdir(directory):
        if filename.endswith('_diet.json'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                json_data.append(data)
    return json_data



##-------------------EN CONSTRUCCION----------------------------##
def extract_ideas_de_preparaciones(json_data):
    """Extracts 'ideas_de_preparaciones' from JSON data."""
    all_ideas = []
    for data in json_data:
        if 'ideas_de_preparaciones' in data:
            all_ideas.extend(data['ideas_de_preparaciones'])
    return all_ideas


def print_ideas_de_preparaciones(ideas):
    """Prints 'ideas_de_preparaciones'."""
    for idea in ideas:
        tiempo_de_comida = idea['tiempo_de_comida']
        combinaciones = idea['combinaciones']
        ejemplo = idea['ejemplo']
        print(f"Tiempo de comida: {tiempo_de_comida}")
        print(f"Combinaciones: {combinaciones}")
        print(f"Ejemplo: {ejemplo}")
        print()




