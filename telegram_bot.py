from logger import logger
from env_vars import bot

from user_answer_handler import get_user_local_info, update_user_info, reset_user_info, get_ingredient_category, reset_chosen_ingredients, remove_ingredient, update_user_ingredients, get_user_chosen_ing, get_user_answers, update_user_answers, reset_answers_data
from user_manager import send_location_question, get_user_name_age, handle_user_id, validate_name_age_input, welcome_message
from survey_manager import  ingredients_data, send_ingredients, create_category_menu, diseases_dict, send_next_question, create_diseases_menu
from database_manager import register_new_user, check_user_survey_id, insert_chosen_ingredients
from diet_manager import evaluate_survey_answers

from mysql.mysql_commands import select_from_table, delete_user_id_row, update_and_delete_survey_id

# Create a set to store the selected options
selected_options = set()
plan_name_list = []
commands = ["/inicio","/start","/cuestionario","/dieta"]



# Handle '/start' and '/help'
@bot.message_handler(commands=['inicio','start'])
def send_welcome(message):
    ## Reset local variables
    plan_name_list.clear()
    reset_answers_data()

    bot.send_message(message.chat.id, welcome_message())
    user_id = handle_user_id(message.chat.id)
    survey_id = check_user_survey_id(message.chat.id)

    print("debug user_id and survey_id:", user_id, survey_id)

    if user_id == True and survey_id == False:
        return bot.send_message(message.chat.id, 'El usuario principal está registrado! Presiona /cuestionario para crear tu primer plan alimenticio')
    elif user_id == True and survey_id:
        return bot.send_message(message.chat.id, 'El usuario esta ya registrado! Y tienes un Plan-Nutricional creado, presiona /dieta para verlas')
    elif user_id == False:
        return bot.send_message(message.chat.id, f"Tu ID de telegram {message.chat.id}, no está registrado, para registrarte, presiona /planes")
        





@bot.message_handler(commands=['planes'])
def start_survey(message):
    reset_user_info()
    try:
        user_id = handle_user_id(message.chat.id)
        survey_id = check_user_survey_id(message.chat.id)

        if user_id == True and survey_id == False:
            return bot.send_message(message.chat.id, 'El usuario principal está registrado! Presiona /cuestionario para crear tu primer plan alimenticio')
        
        elif user_id == True and survey_id:
            return bot.send_message(message.chat.id, 'El usuario esta ya registrado! Y tienes un Plan-Nutricional creado, presiona /dieta para verlas')
        
        else: 
            bot.send_message(message.chat.id, f"Comencemos con tu informacion básica. Ingresa tu nombre y edad (Por ejemplo: Jose 43, Maria 19): ")
            bot.register_next_step_handler(message, get_user_name_age)

    except Exception as e:
        logger.error(f"Error starting survey: {e}")
        bot.send_message(message.chat.id, "Error starting the survey. Please try again later.")





@bot.message_handler(commands=['cuestionario'])
def start_ingredients_selection(message):
    reset_chosen_ingredients()

    user_id = handle_user_id(message.chat.id)
    survey_id = check_user_survey_id(message.chat.id)
    print("debug user_id and survey_id in cuestionario function:", user_id, survey_id)

    if user_id == False:
        bot.send_message(message.chat.id,"Tu usuario no está aun registrado. Presiona /planes para ingresar tu información básica")
    
    elif user_id == True and survey_id == True:
        bot.send_message(message.chat.id,"Tu usuario ya está aun registrado. Y tienes un Plan creado, presiona /dieta para generar una y ver las recomendaciones")
    
    elif user_id == True and survey_id == False:

        bot.send_message(message.chat.id, 'Crear Plan-Nutricional, que contendrá tus respuestas e ingredientes preferidos.\nIngresa un nombre como Dieta Jose, Dieta personal, etc:' )
        bot.register_next_step_handler(message, get_survey_name)




## GENERATE DIET 
@bot.message_handler(commands=['dieta'])
def start_ingredients_selection(message):

    user_id = handle_user_id(message.chat.id)
    survey_id = check_user_survey_id(message.chat.id)
    

    if user_id == False:
        return bot.send_message(message.chat.id,"Tu usuario no está aun registrado. Presiona /planes para ingresar tu información básica")
    
    elif user_id == True and survey_id == False:
        return bot.send_message(message.chat.id,"Tu usuario ya está registrado. Presiona /cuestionario para terminar de armar tu Plan Nutricional")
    
    elif user_id and survey_id:

        result = evaluate_survey_answers(survey_id)

        bot.send_message(message.chat.id, f"Según el cuestionario tus probabilidades de tener la condicion médica es: {result[0]} con un score de {result[1]}, su lista de ingredientes es:")

    


@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    global selected_options

    user_id = call.from_user.id
    chat_id = call.message.chat.id

    data = call.data.split('-')
    print(data)

    user_answers = get_user_answers()
    chosen_ing = get_user_chosen_ing()


    ## BOTÓN: 'CUESTIONARIO'
    if len(data) == 3:
        print(data)
        disease_key, question_key, answer_key = data
        update_user_answers(user_id, disease_key, question_key, answer_key)
        print('debug user_answers:', user_answers)

        bot.answer_callback_query(call.id, text=f"Tu respuesta para ha sido guardada!", cache_time=5)
        bot.delete_message(chat_id, call.message.message_id)
        
        status = send_next_question(chat_id, selected_options,plan_name_list)

        ## CONECTA EL FIN DEL CUESTIONARIO CON EL INICIO DE LA ELECCION DE INGREDIENTES

        if status:
            reset_chosen_ingredients()
            menu_markup = create_category_menu(chat_id)
    
            bot.send_message(chat_id, "Ahora elige tus alimentos favoritos! Una vez seleccionados todos, presiona 'Guardar selección'.",reply_markup=menu_markup)
 


    ## BOTÓN:  'GUARDAR SELECCIÓN'
    elif call.data == 'save_ingredients':

        ### Crear funcion insert ingredients in survey_id
        ### Crear funcion get_user_survey_id
        user_survey_id = check_user_survey_id(user_id)

        status = insert_chosen_ingredients(user_survey_id, chosen_ing)
        print("Save all ingredients command", chosen_ing)
        if status:
            bot.send_message(chat_id, "Tu lista de ingredientes ha sido guardada! Presiona '/dieta' para generar tu primera dieta")
            return
        else:
            bot.send_message(chat_id, "Hubo algún error, Intenta de nuevo.")
        

    ## BOTÓN:  'INGREDIENTE'
    elif call.data.startswith('chosen-'):
        ingredient = call.data.split('-')[1]

        if ingredient in chosen_ing:
            remove_ingredient(ingredient)
        else:
            update_user_ingredients(ingredient)

        
        update_ingredients_menu(chat_id,call.message.message_id,ingredient)

        
        print("ingredient selected:", ingredient)
        return
    
    ## BOTÓN:  'SELECCION DE CATEGORIA'
    elif call.data.startswith('category_'):
        category = call.data.split('_')[1]
        check_ingredient = None
        keyboard = send_ingredients(chat_id,category,check_ingredient)
        bot.send_message(chat_id,f"Los alimentos dentro de la categoría: {category}", reply_markup=keyboard )
        return


    ## BOTÓN:  'GUARDAR Y SEGUIR ELIGIENDO -- CATEGORIAS DE INGREDIENTES'
    elif call.data == 'back_to_categories':
        update_category_menu(chat_id,call.message.message_id)


    ## BOTÓN: SELECCION DE GÉNERO
    elif call.data.startswith('genre-'):

        genre = call.data.split('-')[1]
        update_user_info(genre)
        
        send_location_question(call.message, chat_id)

    ## BOTÓN GUARDAR ALL USER INFO 
    elif call.data == "save_user_info":
        user_info = get_user_local_info()
        
        status = register_new_user(user_info)

        if status:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(chat_id,f"{status}")
            return 

    elif call.data == "cancelar-pregunta":

        bot.send_message(call.message.chat.id, "/inicio")

    else:

        #Handle diseases menu callback data
        if call.data == "send":
            if selected_options:
                print('selected options after send:', selected_options)
                bot.delete_message(chat_id, call.message.message_id)
                # If at least one disease is selected, proceed to send questions            
                send_next_question(chat_id, selected_options, plan_name_list)
                
            else:
                # If no disease is selected, prompt the user to select at least one
                bot.send_message(chat_id, "Por favor, selecciona al menos una opción antes de presionar 'Enviar'")
            return
        
        option = call.data
        if option in diseases_dict:
            if option in selected_options:
                selected_options.remove(option)
            else:
                selected_options.add(option)
            update_diseases_menu(chat_id,call.message.message_id)

        


def get_survey_name(message):
    survey_name = message.text

    if survey_name in commands:
        bot.send_message(message.chat.id, "Has tratado de ingresar un comando como nombre, vuelve a intentarlo presionando /cuestionario")
    else:
        plan_name_list.append(survey_name)

        keyboard = create_diseases_menu()
        bot.send_message(message.chat.id, f"El Plan-Nutricional '{plan_name_list[0]}' ha sido creado, ahora selecciona una o varias de las siguientes opciones:", reply_markup=keyboard)
        


#UPDATE MENUS
##-----------------#------------------------------------------------------#

def update_diseases_menu(chat_id, message_id):
    keyboard = create_diseases_menu()
    selected_options_text = f"Has seleccionado los siguientes: {', '.join(selected_options)}"
    # Update the menu with the current selection
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=selected_options_text, reply_markup=keyboard)


def update_ingredients_menu(chat_id, message_id, ingredient):
    chosen_ing = get_user_chosen_ing()
    format_chosen_ing = ', '.join(chosen_ing)

    print('debug ingredient value:', ingredient)

    
    category = get_ingredient_category(ingredient)

    print('debug category value from update_ingredients_menu function:',category)


    keyboard = send_ingredients(chat_id,category,ingredient)
    selected_options_text = f"Los alimentos dentro de la categoría: {category}.\nHas elegido hasta ahora:{format_chosen_ing}"
    
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=selected_options_text, reply_markup=keyboard)


def update_category_menu(chat_id, message_id):

    chosen_ing = get_user_chosen_ing()
    format_chosen_ing = ', '.join(chosen_ing)

    keyboard = create_category_menu(chat_id)

    selected_options_text = f"Elige tus alimentos favoritos! Una vez seleccionados todos, presiona 'Guardar selección'.\nTu lista de ingredientes hasta ahora: \n{format_chosen_ing}"
    
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=selected_options_text, reply_markup=keyboard)





#MYSQL COMMANDS
##-----------------#------------------------------------------------------------------##

## BORRA TODA LA FILA DE UN USER ID
@bot.message_handler(commands=['borrarUsuario'])
def display_test1(message):
    args = message.text.split()[1:]
    delete_user_id_row(int(args[0]))
    bot.send_message(message.chat.id,"'DELETE FROM users WHERE user_id = %s;' ha sido ejecutado")


## BORRAR SURVEY ID EN USERS Y BORRAR TODA LA FILA DE ANSWERS 
@bot.message_handler(commands=['borrarSurveyid'])
def display_test2(message):
    args = message.text.split()[1:]
    update_and_delete_survey_id(args[0])
    bot.send_message(message.chat.id, "El query:'UPDATE users SET survey_id = NULL WHERE survey_id = %s;' ha sido ejecutado")

## SELECT users and answers table
@bot.message_handler(commands=['consultaTabla'])
def display_test2(message):
    args = message.text.split()[1:]
    print( "debug args in select table function", args[0])
    result = select_from_table(args[0])
    bot.send_message(message.chat.id, f"El comando SELECT * FROM table {args} ha sido ejecutado.\n\n Resultados: {result} ")


   






if __name__ == "__main__":
    try:
        bot.infinity_polling()
        print("Polling stopped...")
    except Exception as e:
        print("Error initializing bot:", e)
        exit()
