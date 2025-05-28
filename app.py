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
        response = "¡Hola! ¿En qué puedo ayudarte hoy con respecto a ULTRATEC?"
    elif 'ayuda' in user_message or 'socorro' in user_message:
        response = "Estoy aquí para ayudarte con información sobre ULTRATEC. ¿Qué necesitas?"
    elif 'gracias' in user_message:
        response = "¡De nada! ¿Hay algo más en lo que pueda ayudarte sobre ULTRATEC?"
    elif 'adios' in user_message or 'chao' in user_message or 'hasta luego' in user_message:
        response = "¡Hasta luego! Que tengas un buen día."
    
    # --- Respuestas sobre ULTRATEC --- (Nuevas respuestas añadidas aquí)
    elif 'servicios' in user_message or 'que ofrece' in user_message or 'productos' in user_message:
        response = "ULTRATEC ofrece venta de equipos tecnológicos y servicios de soporte técnico para empresas y personas naturales."
    elif 'donde se encuentra' in user_message or 'ubicacion' in user_message or 'piura' in user_message:
        response = "Nuestra sede principal está en Lima, pero también operamos en Piura y realizamos envíos a toda la provincia."
    elif 'contacto' in user_message or 'llamar' in user_message or 'telefono' in user_message or 'facebook' in user_message or 'correo' in user_message:
        response = "Puedes contactar a ULTRATEC llamando al (01) 330-1111, visitando su página de Facebook: facebook.com/ultratecperu, o enviando un correo a [correo parcial por privacidad]."
    elif 'proveedor del estado' in user_message or 'RNP' in user_message or 'empadronada' in user_message:
        response = "Sí, ULTRATEC está empadronada en el Registro Nacional de Proveedores (RNP) como proveedor de bienes y servicios."
    elif 'ruc' in user_message or 'razon social' in user_message:
        response = "La razón social de la empresa es ULTRATEC REPRESENTACIONES S.A.C. y su RUC es 20523303351."
    elif 'horario' in user_message or 'horas' in user_message or 'abierto' in user_message:
        response = "Estamos abiertos de lunes a viernes de 9:00 a 18:00, y los sábados de 10:00 a 14:00."

    # --- Fin Respuestas sobre ULTRATEC ---

    # Si no entiende, listar los temas disponibles (Actualizado)
    if not response:
        # La API de Wolfram|Alpha queda desactivada en este punto ya que response no está vacío inicialmente si una respuesta predefinida coincide
        # Pero si ninguna coincide, antes de usar la API, revisamos si tenemos clave API configurada.
        # Como estamos enfocados en las respuestas de ULTRATEC, desactivamos la llamada a la API por ahora.
        # if WOLFRAM_ALPHA_API_KEY:
        #    try:
        #        params = {
        #            'i': user_message,
        #            'appid': WOLFRAM_ALPHA_API_KEY,
        #            'units': 'metric',
        #            'output': 'text'
        #        }
        #        api_response = requests.get(WOLFRAM_ALPHA_API_URL, params=params, timeout=10)
        #        if api_response.status_code == 200:
        #            api_result = api_response.text.strip()
        #            if api_result and "No short answer available" not in api_result:
        #                response = api_result
        #            else:
        #                response = "Interesante pregunta. No tengo una respuesta específica para eso en este momento."
        #        else:
        #            print(f"Error calling Wolfram|Alpha API: Status Code {api_response.status_code}")
        #            response = "Lo siento, tuve un problema al buscar información sobre eso."
        #    except requests.exceptions.RequestException as e:
        #        print(f"Request to Wolfram|Alpha API failed: {e}")
        #        response = "Lo siento, no pude contactar la fuente de información en este momento."
        #    except Exception as e:
        #         print(f"An unexpected error occurred during API call: {e}")
        #         response = "Ocurrió un error interno al procesar tu solicitud."
        #
        # if not response: # Si la API tampoco respondió
        response = "Lo siento, no entiendo tu pregunta. Puedo hablar sobre los siguientes temas relacionados con ULTRATEC: Servicios/Productos, Ubicación/Piura, Contacto (Teléfono, Facebook, Correo), Proveedor del Estado (RNP), RUC/Razón Social, Horario."
    
    return jsonify({'response': response})

if __name__ == '__main__':
    # Para probar localmente usando la variable de entorno,
    # necesitarías configurar la variable WOLFRAM_ALPHA_API_KEY
    # en tu sistema antes de ejecutar 'python app.py'.
    # Si quieres probar localmente sin configurar la variable de entorno,
    # puedes descomentar la línea 'WOLFRAM_ALPHA_API_KEY = "TU_CLAVE_AQUI"'
    # y poner tu clave ahí temporalmente (menos seguro para producción).
    app.run(debug=True) 