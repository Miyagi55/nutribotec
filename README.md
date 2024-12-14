# NutriBotEC

## Descripción
NutribotEC es un bot de Telegram que está alimentado con información en materia de nutrición. Su función es, en base a las elecciones de los usuarios, dar recomendaciones para cada uno de los padecimientos más comunes relacionados, generalmente, a los hábitos alimenticios. 

Dentro de su información también hay una extensa lista de ingredientes donde cada uno tiene su respectiva porción, entonces al ser seleccionados y guardados, el bot genera una dieta diaria que es una combinación aleatoria de todos los ingredientes elegidos. 

## Arquitectura del Proyecto
### Diagrama de infraestructura tecnológica para el desarrollo y despligue del Bot (BackEnd)
Principalmente alojado en la nube de Google, el proyecto fué desarrollado usando la Cloud Shell y su editor de texto. El bot está desplegado para producción, en una Instancia de una Máquina Virtual Ubuntu y se conecta también a una Base de datos MySQL proveída por [Aiven](https://aiven.io/).  


![text](https://github.com/Miyagi55/nutribotec/blob/main/photo_2024-02-23_22-08-55.jpg)



### Descripción de Componentes
- **Telegram Bot API:** Servicio de Telegram, su [API pública](https://core.telegram.org/api) de Bot te permite crear fácilmente programas que utilizan mensajes de Telegram como interfaz de usuario (FrontEnd).
- **pyTelegramBotAPI:** [Librería usada](https://pypi.org/project/pyTelegramBotAPI/) en el proyecto, es una implementación de Python simple pero extensible que conecta muestro código con la API de Telegram Bot.
- **Google Cloud Shell:** [Cloud Shell](https://cloud.google.com/shell?hl=es) es un entorno de desarrollo y operaciones online. Puedes desarrollar, compilar, depurar y desplegar tus aplicaciones nativas de la nube mediante el editor de Cloud Shell.
- **Máquina virtual Ubuntu:** Máquina virtual creada como instancia de [Compute Engine](https://cloud.google.com/compute/docs/faq?hl=es-419) en la [consola de la nube de google.](https://cloud.google.com/cloud-console?hl=es-419). Aquí permanece alojado el codigo fuente y su ejecución permanente.
- **Aiven.io - Servicio de base de datos:** Usando su API, el bot se conecta programáticamente a la base de datos MySQL alojada y administrada por [Aiven](https://aiven.io/mysql).  



## Modelado de datos
En este modelado sencillo, se reconocieron dos *entidades*, que son las dos tablas: *users*(usuarios) y *answers*(respuestas). El id_usuario es relacionado con el ID de telegram, y el id_cuestionario es asignado una vez terminado el paso ejecutado por el comando /cuestionario. Con ésta lógica, solo puede haber un usuario por sesion de Telegram y un cuestionario (que puede ser sobre-escrito) por usuario. 

![text](https://github.com/Miyagi55/nutribotec/blob/main/photo_2024-02-23_22-09-05.jpg)


Fuente de consulta: [¿Qué es un diagrama de entidad-relación?](https://www.lucidchart.com/pages/es/que-es-un-diagrama-entidad-relacion)


## Funcionamiento del Proyecto
### Diagrama de Flujo
Diagrama de flujo que muestra la lógica del programa, define los comandos del bot(/inicio,/registrarse, etc) en cada paso y cómo lleva al usuario hasta los resultados que ofrece el programa.


![text](https://github.com/Miyagi55/nutribotec/blob/main/diagrama_de_flujo.jpg)



### Comandos iniciales
1. **/inicio:** Inicia el bot, desplegando el mensaje de bienvenida y chequeando si el usuario está registrado o no.
2. **/registrarse:** Inicia registro de usuario, pidiendo nombre, edad y género al usuario. Por defecto, el id_usuario es igual al ID de Telegram y relacionado a la información ingresada.
3. **/cuestionario:** Empieza cuestionario para asignar condición de salud y guardar la eleccion de ingredientes preferidos. 

### Comandos finales
1. **/menu:** Muestra las recomendaciones generales, alimentos permitidos y no permitidos por condición de salud asignada.
2. **/dieta:** Genera una dieta para el día en base a los ingredientes elegidos.
3. **/ingredientes:** Agrega una nueva lista de ingredientes.


## Link de telegram que dirige al NutriBot-EC

- https://t.me/AsistenteNutricionalEC_bot


## Consideraciones de Seguridad y Privacidad
Toda la información manejada es confidencial, anónima y está respaldada por los servicios de Google y Aiven. La información no es compartida con terceros y su fin es acádemico, investigativo y de divulgación informativa en materia de nutrición. 

## Links de importancia

- https://aiven.io/mysql
- https://cloud.google.com/cloud-console?hl=es-419
- https://cloud.google.com/compute/docs/faq?hl=es-419
- https://cloud.google.com/shell?hl=es
- https://pypi.org/project/pyTelegramBotAPI
- https://core.telegram.org/ap
  

## Licencia
Libre.


# NutriBotEC (English version) 

## Description
NutriBotEC is a Telegram bot powered by nutrition-related information. Its function is to provide recommendations based on users' choices for the most common conditions generally related to dietary habits.

The bot also features an extensive list of ingredients, each with its respective portion. When users select and save ingredients, the bot generates a daily diet by randomly combining the chosen ingredients.

## Project Architecture
### Technological Infrastructure Diagram for Bot Development and Deployment (BackEnd)
The project is primarily hosted on Google Cloud, developed using Cloud Shell and its text editor. The bot is deployed in production on an Ubuntu Virtual Machine Instance and connects to a MySQL database provided by [Aiven](https://aiven.io/).

![text](https://github.com/Miyagi55/nutribotec/blob/main/photo_2024-02-23_22-08-55.jpg)

### Component Description
- **Telegram Bot API:** A service from Telegram. Its [public API](https://core.telegram.org/api) allows developers to easily create programs that use Telegram messages as a user interface (FrontEnd).
- **pyTelegramBotAPI:** [Library used](https://pypi.org/project/pyTelegramBotAPI/) in the project. It is a simple yet extensible Python implementation that connects the code with the Telegram Bot API.
- **Google Cloud Shell:** [Cloud Shell](https://cloud.google.com/shell?hl=en) is an online development and operations environment. It allows for developing, building, debugging, and deploying cloud-native applications.
- **Ubuntu Virtual Machine:** A virtual machine created as an instance of [Compute Engine](https://cloud.google.com/compute/docs/faq) in the [Google Cloud Console](https://cloud.google.com/cloud-console). This instance hosts the source code and ensures its continuous execution.
- **Aiven.io - Database Service:** Using its API, the bot programmatically connects to the MySQL database hosted and managed by [Aiven](https://aiven.io/mysql).

## Data Modeling
In this simple model, two *entities* were identified, represented by two tables: *users* and *answers*. The `id_usuario` is linked to the Telegram ID, and the `id_cuestionario` is assigned once the step executed by the `/cuestionario` command is completed. This logic ensures one user per Telegram session and one questionnaire (which can be overwritten) per user.

![text](https://github.com/Miyagi55/nutribotec/blob/main/photo_2024-02-23_22-09-05.jpg)

Source: [What is an Entity-Relationship Diagram?](https://www.lucidchart.com/pages/what-is-an-entity-relationship-diagram)

## Project Functionality
### Flow Diagram
The flow diagram illustrates the program logic, defining the bot commands (/start, /register, etc.) at each step and guiding users to the results offered by the program.

![text](https://github.com/Miyagi55/nutribotec/blob/main/diagrama_de_flujo.jpg)

### Initial Commands
1. **/start:** Launches the bot, displaying the welcome message and checking if the user is registered.
2. **/register:** Begins user registration, requesting the user's name, age, and gender. By default, the `id_usuario` equals the Telegram ID and is linked to the entered information.
3. **/questionnaire:** Starts the questionnaire to assign a health condition and save preferred ingredient choices.

### Final Commands
1. **/menu:** Displays general recommendations, permitted foods, and prohibited foods based on the assigned health condition.
2. **/diet:** Generates a daily diet based on the chosen ingredients.
3. **/ingredients:** Adds a new list of ingredients.

## Telegram Link to Access NutriBot-EC
- [NutriBotEC](https://t.me/AsistenteNutricionalEC_bot)

## Security and Privacy Considerations
All information handled is confidential, anonymous, and backed by Google and Aiven services. The information is not shared with third parties and is intended for academic, research, and informational purposes in the field of nutrition.

## Important Links
- [Aiven MySQL](https://aiven.io/mysql)
- [Google Cloud Console](https://cloud.google.com/cloud-console)
- [Google Compute Engine](https://cloud.google.com/compute/docs/faq)
- [Google Cloud Shell](https://cloud.google.com/shell)
- [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI)
- [Telegram Bot API](https://core.telegram.org/api)

## License
Open Source.

