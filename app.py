from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Diccionario de productos y precios (ejemplos basados en la imagen)
products = {
    'epson l3250': 'S/ 699.00 (efectivo/transferencia) o S/ 730.00 (tarjeta)',
    'epson l4260': 'Precio no especificado en este momento, por favor contacta para más detalles.', # Precio no visible en la imagen
    'epson l5590': 'Precio no especificado en este momento, por favor contacta para más detalles.', # Precio no visible en la imagen
    'epson l6270': 'Precio no especificado en este momento, por favor contacta para más detalles.', # Precio no visible en la imagen
    'impresora epson l3250': 'S/ 699.00 (efectivo/transferencia) o S/ 730.00 (tarjeta)',
    'impresora epson l4260': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'impresora epson l5590': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'impresora epson l6270': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    # Puedes añadir más productos aquí
}

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
    user_message = data.get('message', '')
    user_message_lower = user_message.lower()

    response = ""

    # Respuestas básicas y contextualizadas
    if 'hola' in user_message_lower or 'saludos' in user_message_lower or 'buenos dias' in user_message_lower or 'buenas tardes' in user_message_lower or 'buenas noches' in user_message_lower:
        response = "¡Hola! Soy tu asistente virtual de ULTRATEC. ¿En qué puedo ayudarte hoy con nuestros productos o servicios?"
    elif 'ayuda' in user_message_lower or 'socorro' in user_message_lower or 'necesito saber' in user_message_lower or 'consulta' in user_message_lower:
        response = "Claro, estoy aquí para ayudarte con información sobre ULTRATEC y nuestros equipos de cómputo y tecnología. ¿Sobre qué tema necesitas información?"
    elif 'gracias' in user_message_lower:
        response = "¡De nada! Si tienes más preguntas sobre ULTRATEC o nuestros productos, no dudes en consultarme."
    elif 'adios' in user_message_lower or 'chao' in user_message_lower or 'hasta luego' in user_message_lower or 'bye' in user_message_lower:
        response = "¡Hasta luego! Que tengas un excelente día. Estoy a tu disposición si necesitas algo más de ULTRATEC."
    
    # Respuestas sobre ULTRATEC (información relevante para atención al cliente)
    elif 'servicios' in user_message_lower or 'productos' in user_message_lower or 'ofrecen' in user_message_lower or 'venden' in user_message_lower or 'equipos' in user_message_lower or 'tecnologia' in user_message_lower or 'que tienen' in user_message_lower:
        product_list = "\n".join([f"- {p.title()}" for p in products.keys() if not p.startswith('impresora')]) # Listar productos principales sin el prefijo 'impresora'
        response = (
            "En ULTRATEC nos especializamos en la venta de equipos tecnológicos y ofrecemos servicios de soporte técnico tanto para empresas como para personas naturales.\n\n" +
            "Algunos de nuestros productos (pregúntame por su precio):\n" +
            f"{product_list}\n\n" +
            "¿Hay algo más en lo que pueda ayudarte?"
        )
    elif 'ubicacion' in user_message_lower or 'donde estan' in user_message_lower or 'direccion' in user_message_lower or 'tienda' in user_message_lower or 'donde ubicar' in user_message_lower:
        response = "Nuestra dirección principal es Jr. Emilio Fernández N° 171, Urb. Santa Beatriz, Lima. También tenemos operaciones en Piura y realizamos envíos a cualquier distrito de la provincia de Piura."
    elif 'envios' in user_message_lower or 'entrega' in user_message_lower or 'delivery' in user_message_lower or 'mandan a piura' in user_message_lower:
         response = "Sí, realizamos envíos a cualquier distrito de la provincia de Piura."
    elif 'contacto' in user_message_lower or 'llamar' in user_message_lower or 'telefono' in user_message_lower or 'correo' in user_message_lower or 'facebook' in user_message_lower or 'whatsapp' in user_message_lower or 'redes sociales' in user_message_lower:
        response = "Puedes contactar a ULTRATEC REPRESENTACIONES S.A.C. llamando al (01) 330-1111 o visitando nuestra página de Facebook: facebook.com/ultratecperu."
    elif 'horario' in user_message_lower or 'horas' in user_message_lower or 'abierto' in user_message_lower or 'atienden' in user_message_lower:
        response = "Nuestro horario de atención es de lunes a viernes de 9:00 a 18:00, y los sábados de 10:00 a 14:00."
    
    # Lógica para precios
    elif 'precio' in user_message_lower or 'costo' in user_message_lower or 'valor' in user_message_lower or 'cuanto cuesta' in user_message_lower:
        found_product = None
        for product_key in products:
            if product_key in user_message_lower:
                found_product = product_key
                break
                
        if found_product:
            price = products[found_product]
            response = f"El precio de {found_product.title()} es: {price}"
        else:
            # Si preguntan por precio pero no especifican producto
            product_list_prices = "\n".join([f"- {p.title()}" for p in products.keys() if not p.startswith('impresora')])
            response = (
                "Puedo darte información de precios para los siguientes productos:\n" +
                f"{product_list_prices}\n\n" +
                "¿De cuál te gustaría saber el precio?"
            )

    # --- Respuesta por defecto si no se encuentra una coincidencia ---
    # Si no encontramos una respuesta predefinida, indicamos los temas que sí manejamos.
    if not response:
        response = (
            "Lo siento, no entendí tu pregunta. Soy un chatbot diseñado para ayudarte con información sobre ULTRATEC REPRESENTACIONES S.A.C. enfocada en productos y servicios.\n\n" +
            "Puedo responder sobre:\n"
            "- **Productos y Servicios:** Qué ofrecemos y qué productos tenemos (puedes preguntar por precios).\n"
            "- **Ubicación y Envíos:** Dirección en Lima y envíos a Piura.\n"
            "- **Contacto:** Teléfono fijo y Facebook.\n"
            "- **Horario de Atención.\n\n"
            "¿Sobre cuál de estos temas te gustaría conversar?"
        )

    # --- Integración con Wolfram|Alpha API ---
    # Si no encontramos una respuesta predefinida Y tenemos una clave API configurada
    # (Esta parte está aquí por si decides reactivar la API en el futuro)
    # if not response and WOLFRAM_ALPHA_API_KEY:
    #     try:
    #         params = {
    #             'i': user_message, # La pregunta del usuario
    #             'appid': WOLFRAM_ALPHA_API_KEY, # Tu clave API
    #             'units': 'metric', # Opcional
    #             'output': 'text'
    #         }
    #         api_response = requests.get(WOLFRAM_ALPHA_API_URL, params=params, timeout=10)

    #         if api_response.status_code == 200:
    #             api_result = api_response.text.strip()
    #             if api_result and "No short answer available" not in api_result:
    #                 response = api_result
    #             else:
    #                 response = "Interesante pregunta. No tengo una respuesta específica para eso en este momento."

    #         else:
    #             print(f"Error calling Wolfram|Alpha API: Status Code {api_response.status_code}")
    #             response = "Lo siento, tuve un problema al buscar información sobre eso."

    #     except requests.exceptions.RequestException as e:
    #         print(f"Request to Wolfram|Alpha API failed: {e}")
    #         response = "Lo siento, no pude contactar la fuente de información en este momento."
    #     except Exception as e:
    #          print(f"An unexpected error occurred during API call: {e}")
    #          response = "Ocurrió un error interno al procesar tu solicitud."

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