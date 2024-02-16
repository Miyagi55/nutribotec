from logger import logger
from iniciador_bot import bot
from telebot import TeleBot, types
from user_answer_handler import get_user_local_info, update_user_info, reset_user_info
from database_manager import user_id_check, register_new_user



commands = ["/inicio","/start","/cuestionario","/dieta"]


def welcome_message():
    return 'Éste es el mensaje de bienvenida' 
    

def handle_user_id(user_id):
    checked_id = user_id_check(user_id)   #consulta a base datos si el telgram ID esta registrado o no.
    return checked_id  


## USER INITIAL DATA
def get_user_name_age(message):
    
    answer = message.text 
    name_age_status = validate_name_age_input(message.chat.id, answer)

    if name_age_status:
        markup = get_genre()
        bot.send_message(message.chat.id, "Selecciona tu género biológico de nacimiento:", reply_markup=markup)
        
        return name_age_status
    
    




def get_ibm(weight_lbs, height_in):

    bmi = (weight_lbs / (height_in ** 2)) * 703

    return bmi


    

## IBM QUESTION ## SIN IMPLEMENTEAR AUN
def ibm_question():
    keyboard = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton(text="Sí, sé al menos un aproximado.", callback_data=f"ibm-true")
    button2 = types.InlineKeyboardButton(text="No tengo idea cuánto mido o peso", callback_data=f"ibm-false")

    keyboard.add(button1)
    keyboard.add(button2)

    return keyboard 



## GET LOCATION FUNCTIONS
def send_location_question(message,chat_id):

    bot.send_message(chat_id, f"Ingresa tu provincia, localidad, ciudad o país:\nPor ejemplo: Manta, Manabí")
    bot.register_next_step_handler(message, get_location)
    

def get_location(message):

    answer = message.text

    if answer in commands:
        bot.send_message(message.chat.id, "Has tratado de ingresar un comando como ubicación, vuelve a intentarlo presionando /planes")
        return

    user_info = update_user_info(answer)
    
    for typo in user_info:
        print(type(typo)) 

    markup = save_info_question()
    bot.send_message(message.chat.id, f"Bien! Has guardado toda la información básica!\nTu info hasta ahora: {user_info}\n\nDa click en Guardar para continuar con el cuestionario", reply_markup=markup)

    return 





## CREATE GENRE MENU 
def get_genre():
    keyboard = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton(text="Mujer", callback_data=f"genre-mujer")
    button2 = types.InlineKeyboardButton(text="Hombre", callback_data=f"genre-hombre")

    keyboard.add(button1,button2)

    return keyboard




## CREATE SAVE INFO QUESTION
def save_info_question():
    keyboard = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton(text="Guardar", callback_data=f"save_user_info")
    button2 = types.InlineKeyboardButton(text="Cancelar", callback_data=f"cancelar-pregunta")

    keyboard.add(button1,button2)

    return keyboard




def validate_name_age_input(user_id, name_age):
    name_age_ = name_age.strip()
    name_age_parts = name_age_.split()



    if len(name_age_parts) != 2:
        bot.send_message(user_id, "ERROR: Formato inválido. Por favor, ingresa bien tu nombre y tu edad. Da clic a '/planes' para intentar de nuevo")
        return False

    name, age_str = name_age_parts

    if not name.isalpha():
        bot.send_message(user_id, "ERROR: Formato de nombre inválido. El nombre solo debe contener letras. Da clic a '/planes' para intentar de nuevo")
        return False
    elif not age_str.isdigit():
        bot.send_message(user_id, "ERROR: Formato de edad inválido. La edad tiene que ser un número entero positivo. Da clic a '/planes' para intentar de nuevo")
        return False
    else:
        age = int(age_str)
        
        temp_list = [str(user_id), name, age]
        
        for data in temp_list:
            update_user_info(data)
        

        user_actual_info = get_user_local_info()
        print(user_actual_info)

        return f"VALID INPUT (ready to insert on table) {user_id}, {name}, {age}"






