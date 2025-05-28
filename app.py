from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Configura tu clave API de Wolfram|Alpha.
# Opción Recomendada: Usar una variable de entorno en PythonAnywhere
# Lee la clave de la variable de entorno llamada WOLFRAM_ALPHA_API_KEY
WOLFRAM_ALPHA_API_KEY = os.environ.get('WOLFRAM_ALPHA_API_KEY')

# URL base de la API de Short Answers de Wolfram|Alpha
WOLFRAM_ALPHA_API_URL = "http://api.wolframalpha.com/v1/result"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data.get('message', '').lower()
    
    response = ""
    
    # Procesar el mensaje y generar una respuesta
    if 'hola' in user_message or 'saludos' in user_message:
        response = "¡Hola! ¿En qué puedo ayudarte hoy?"
    elif 'ayuda' in user_message or 'socorro' in user_message:
        response = "Estoy aquí para ayudarte. ¿Qué necesitas?"
    elif 'gracias' in user_message:
        response = "¡De nada! ¿Hay algo más en lo que pueda ayudarte?"
    elif 'adios' in user_message or 'chao' in user_message or 'hasta luego' in user_message:
        response = "¡Hasta luego! Que tengas un buen día."
    elif 'precio' in user_message or 'costo' in user_message or 'valor' in user_message:
        response = "¿Sobre qué producto te gustaría saber el precio?"
    elif 'horario' in user_message or 'horas' in user_message or 'abierto' in user_message:
        response = "Estamos abiertos de lunes a viernes de 9:00 a 18:00, y los sábados de 10:00 a 14:00."
    else:
        # Si no entiende, listar los temas disponibles
        response = "Lo siento, no entiendo tu pregunta. Puedo hablar sobre los siguientes temas: Hola, Ayuda, Gracias, Adiós, Precios (de productos), Horario (de la tienda). ¿Sobre cuál te gustaría conversar?"
    
    # --- Integración con Wolfram|Alpha API ---
    # Si no encontramos una respuesta predefinida Y tenemos una clave API configurada
    if not response and WOLFRAM_ALPHA_API_KEY:
        try:
            # Preparamos los parámetros para la API de Short Answers
            params = {
                'i': user_message, # La pregunta del usuario
                'appid': WOLFRAM_ALPHA_API_KEY, # Tu clave API
                'units': 'metric', # Opcional: para unidades métricas si aplica
                'output': 'text' # Pedimos la respuesta en texto plano
            }
            # Hacemos la solicitud GET a la API
            # timeout=10 es para que la llamada no espere infinitamente
            api_response = requests.get(WOLFRAM_ALPHA_API_URL, params=params, timeout=10)

            # Verificamos que la solicitud fue exitosa (código 200)
            if api_response.status_code == 200:
                api_result = api_response.text.strip()

                # La API devuelve "No short answer available" si no sabe la respuesta
                if api_result and "No short answer available" not in api_result:
                    response = api_result # Usamos la respuesta de la API
                else:
                    # Mensaje si la API no tiene una respuesta específica
                    response = "Interesante pregunta. No tengo una respuesta específica para eso en este momento."

            else:
                # Mensaje si la API devuelve un código de error HTTP
                print(f"Error calling Wolfram|Alpha API: Status Code {api_response.status_code}")
                response = "Lo siento, tuve un problema al buscar información sobre eso."

        except requests.exceptions.RequestException as e:
            # Mensaje si hay un error de conexión o timeout al llamar a la API
            print(f"Request to Wolfram|Alpha API failed: {e}")
            response = "Lo siento, no pude contactar la fuente de información en este momento."
        except Exception as e:
             # Capturamos cualquier otro error inesperado durante la llamada a la API
             print(f"An unexpected error occurred during API call: {e}")
             response = "Ocurrió un error interno al procesar tu solicitud."

    # --- Fin Integración con Wolfram|Alpha API ---

    return jsonify({'response': response})

if __name__ == '__main__':
    # Para probar localmente usando la variable de entorno,
    # necesitarías configurar la variable WOLFRAM_ALPHA_API_KEY
    # en tu sistema antes de ejecutar 'python app.py'.
    # Si quieres probar localmente sin configurar la variable de entorno,
    # puedes descomentar la línea 'WOLFRAM_ALPHA_API_KEY = "TU_CLAVE_AQUI"'
    # y poner tu clave ahí temporalmente (menos seguro para producción).
    app.run(debug=True) 