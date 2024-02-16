import json
from telebot import TeleBot, types
from env_vars import bot
from user_answer_handler import get_user_local_info, get_user_chosen_ing, get_user_answers, update_user_answers, reset_answers_data
from database_manager import insert_survey_data




questions_file_path = "local-data/questions_options.json"
ingredients_file_path = "local-data/ingredients.json"
diseases_dict = {
    'anemia': 'Anemia',
    'calculos_infecciones_renales': 'Infección o Cálculos Renales (vías urinarias y riñones)',
    'calculos_biliares': 'Cálculos Biliares (problemas con la vesícula)',
    'desnutricion_bajopeso': 'Desnutrición (Bajo peso, carencia de nutrientes variados)',
    'diabetes': 'Diabetes (condición médica o principios de la enfermedad)',
    'estrenimiento': 'Estreñimiento (problemas de evacuación)',
    'higado_graso': 'Hígado Graso',
    'hipertension_arterial': 'Presión Alta (problemas con el sistema sanguíneo y cardiaco)',
    'obesidad_sobrepeso': 'Obesidad (problemas con el control de peso, incluye sobrepeso)'
}


def read_file(questions_file_path):
    with open(questions_file_path, 'r') as file:
        data = json.load(file)
    return data
    
ingredients_data = read_file(ingredients_file_path)
questions_data = read_file(questions_file_path)



## CREATE DISEASES MENU
def create_diseases_menu():
    
    keyboard = types.InlineKeyboardMarkup()

    for disease_key, disease_name in diseases_dict.items():
        button = types.InlineKeyboardButton(text=disease_name, callback_data=disease_key)
        keyboard.add(button)

    send_button = types.InlineKeyboardButton(text="Empezar cuestionario", callback_data="send")
    keyboard.add(send_button)
    return keyboard


## CREATE MENU FOR EACH QUESTION AND BUILD CALLBACK DATA FORMAT
def create_inline_keyboard(disease, question_key, answer_options, answer_keys):

    markup = types.InlineKeyboardMarkup(row_width=2)
    
    buttons = [types.InlineKeyboardButton(answer_text, callback_data=f'{disease}-{question_key}-{answer_key}') for answer_key, answer_text in zip(answer_keys, answer_options)]
    markup.add(*buttons)
    
    return markup




##---SEND SURVEY QUESTION
def send_next_question(chat_id, selected_options,plan_name_list):
                
    user_answers = get_user_answers()
    
    for disease in selected_options:
        
        for question_key, question_data in questions_data.get(disease, {}).items():
            # Check if the user has answered the current question for the current disease
            if user_answers.get(chat_id, {}).get(disease, {}).get(question_key) is None:
            
                question_text = question_data.get('question')

                answer_options = question_data['answers'].values()
                answer_keys = question_data['answers'].keys()

                keyboard = create_inline_keyboard(disease, question_key, answer_options, answer_keys)
                bot.send_message(chat_id, text=question_text, reply_markup=keyboard)
                
                return  # Stop after sending the first unanswered question
            

    # Clear the selected options after sending all questions
    selected_options.clear()

    ##ELECCION DE INGREDIENTES

    survey_data = insert_survey_data(user_answers,plan_name_list)
    print("debug survey_data value after insert_survey_data function:", survey_data)
    
    survey_id_value, survey_name = survey_data

    bot.send_message(chat_id, f"Tu cuestionario '{survey_id_value}-{survey_name}' ha sido registrado exitosamente.")
    plan_name_list.clear()
    reset_answers_data()
    return True





## INGREDIENTS CATEGORY MENU 
def create_category_menu(chat_id):

    markup = types.InlineKeyboardMarkup()

    for category in ingredients_data["CLASIFICACION"]:
        markup.add(types.InlineKeyboardButton(category, callback_data=f'category_{category}'))

    save_button = types.InlineKeyboardButton(text='Guardar selección', callback_data='save_ingredients')
    markup.add(save_button)
    
    return markup




def send_ingredients(chat_id, category, check_ingredient):
    
    chosen_ing = get_user_chosen_ing()

    markup = types.InlineKeyboardMarkup()
    ingredients_and_portions = ingredients_data["CLASIFICACION"][category]
    print("debug category value:",category)

    ingredients = list(ingredients_and_portions.keys())
    print("debug send_ingredients - ingredients type and value:",type(ingredients),ingredients)
    num_columns = 4

    
    

    # Iterate over ingredients in the current row and add buttons to the markup
    for i in range(0, len(ingredients), num_columns):
        row_ingredients = ingredients[i:i+num_columns]
        row_buttons = []

        for ingredient in row_ingredients:
                # Check if the ingredient is chosen, if so, add a check emoji
            if check_ingredient is not None and ingredient in chosen_ing:
                ingredient_text = f"{ingredient} ✅"
            else:
                ingredient_text = ingredient
            row_buttons.append(types.InlineKeyboardButton(ingredient_text, callback_data=f'chosen-{ingredient}'))
        
        markup.row(*row_buttons)

    # Add "Back to Categories" button
    markup.add(types.InlineKeyboardButton("Guardar ingredientes y seguir eligiendo", callback_data='back_to_categories'))

    return markup    










        

       









