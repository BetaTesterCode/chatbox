from flask import Flask, render_template, request, jsonify
import requests
import os
from fuzzywuzzy import process # Importar fuzzywuzzy

app = Flask(__name__)

# Diccionario de productos y precios
products = {
    'epson l3250': 'S/ 699.00 (efectivo/transferencia) o S/ 730.00 (tarjeta)',
    'epson l4260': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'epson l5590': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'epson l6270': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'impresora epson l3250': 'S/ 699.00 (efectivo/transferencia) o S/ 730.00 (tarjeta)',
    'impresora epson l4260': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'impresora epson l5590': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'impresora epson l6270': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'mochila': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'mochilas': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'suministros': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'tinta': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'tintas': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'cartucho': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'cartuchos': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'repuesto laptop': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'repuestos laptop': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'soporte laptop': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'soportes laptop': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'enfriador laptop': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'enfriadores laptop': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'cooler laptop': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    'coolers laptop': 'Precio no especificado en este momento, por favor contacta para más detalles.',
    # Puedes añadir más productos aquí
}

# Servicios ofrecidos
services = [
    'venta de equipos tecnológicos',
    'servicios de soporte técnico para empresas',
    'servicios de soporte técnico para personas naturales',
    'reparación de laptops',
    'mantenimiento de equipos tecnológicos'
    # Puedes añadir más servicios aquí
]

# Umbral de similitud para fuzzy matching (ajústalo si es necesario)
SIMILARITY_THRESHOLD = 70 # Porcentaje de similitud (0-100)

# Configura tu clave API de Wolfram|Alpha.
# Opción Recomendada: Usar una variable de entorno en PythonAnywhere
# Lee la clave de la variable de entorno llamada WOLFRAM_ALPHA_API_KEY
WOLFRAM_ALPHA_API_KEY = os.environ.get('WOLFRAM_ALPHA_API_KEY')

# URL base de la API de Short Answers de Wolfram|Alpha
WOLFRAM_ALPHA_API_URL = "http://api.wolframalpha.com/v1/result"


def find_best_match(query, choices):
    """Encuentra la mejor coincidencia difusa para la consulta en una lista de opciones."""
    # process.extractOne devuelve (mejor coincidencia, puntuación)
    best_match = process.extractOne(query, choices)
    if best_match and best_match[1] >= SIMILARITY_THRESHOLD:
        return best_match[0] # Devuelve la opción que mejor coincide
    return None # No se encontró una coincidencia por encima del umbral

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data.get('message', '')
    user_message_lower = user_message.lower()

    response = ""

    # Intentar encontrar una coincidencia difusa con las palabras clave generales
    general_keywords = {
        'hola': ['hola', 'saludos', 'buenos dias', 'buenas tardes', 'buenas noches'],
        'ayuda': ['ayuda', 'socorro', 'necesito saber', 'consulta', 'pregunta'],
        'gracias': ['gracias', 'muchas gracias', 'agradecido'],
        'adios': ['adios', 'chao', 'hasta luego', 'bye', 'nos vemos'],
        'servicios_productos': ['servicios', 'productos', 'ofrecen', 'venden', 'equipos', 'tecnologia', 'que tienen', 'catalogo', 'lista', 'impresoras', 'mochilas', 'suministros', 'tintas', 'cartuchos', 'repuestos laptop', 'soportes laptop', 'enfriadores laptop', 'coolers laptop', 'reparacion', 'mantenimiento'],
        'ubicacion_envios': ['ubicacion', 'donde estan', 'direccion', 'tienda', 'donde ubicar', 'sede', 'local', 'envios', 'entrega', 'delivery', 'mandan a piura', 'enviar'],
        'contacto': ['contacto', 'llamar', 'telefono', 'correo', 'facebook', 'whatsapp', 'redes sociales', 'comunicar'],
        'horario': ['horario', 'horas', 'abierto', 'atienden', 'a que hora'],
        'precio': ['precio', 'costo', 'valor', 'cuanto cuesta', 'presupuesto']
    }

    # Buscar coincidencia con palabras clave generales
    matched_general_keyword = None
    for key, choices in general_keywords.items():
        if find_best_match(user_message_lower, choices):
             matched_general_keyword = key
             break # Encontramos una coincidencia general, procesamos eso

    # Procesar la respuesta basada en la palabra clave general encontrada
    if matched_general_keyword == 'hola':
        response = "¡Hola! Soy tu asistente virtual de ULTRATEC. ¿En qué puedo ayudarte hoy con nuestros productos o servicios?"
    elif matched_general_keyword == 'ayuda':
        response = "Claro, estoy aquí para ayudarte con información sobre ULTRATEC y nuestros equipos de cómputo y tecnología. ¿Sobre qué tema necesitas información?"
    elif matched_general_keyword == 'gracias':
        response = "¡De nada! Si tienes más preguntas sobre ULTRATEC o nuestros productos, no dudes en consultarme."
    elif matched_general_keyword == 'adios':
        response = "¡Hasta luego! Que tengas un excelente día. Estoy a tu disposición si necesitas algo más de ULTRATEC."
    
    elif matched_general_keyword == 'servicios_productos':
        service_list = "\n".join([f"- {s.capitalize()}" for s in services])
        # Excluir nombres de productos específicos que podrían ser subcadenas de otros
        product_keys_to_list = [p.title() for p in products.keys() if 'impresora' not in p] # Ajusta según cómo quieras listar
        product_list_str = ", ".join(sorted(list(set(product_keys_to_list))))

        response = (
            "En ULTRATEC nos especializamos en la venta de equipos tecnológicos y ofrecemos:\n\n" +
            "**Servicios:**\n" +
            f"{service_list}\n\n" +
            "**Productos:**\n" +
            f"Tenemos productos como: {product_list_str}. Puedes preguntar por precios específicos (ej. 'Precio Epson L3250').\n\n" +
            "¿Hay algo más en lo que pueda ayudarte?"
        )
    elif matched_general_keyword == 'ubicacion_envios':
        response = "Nuestra dirección principal es Jr. Emilio Fernández N° 171, Urb. Santa Beatriz, Lima. También tenemos operaciones en Piura y realizamos envíos a cualquier distrito de la provincia de Piura."
    elif matched_general_keyword == 'contacto':
        response = "Puedes contactar a ULTRATEC REPRESENTACIONES S.A.C. llamando al (01) 330-1111 o visitando nuestra página de Facebook: facebook.com/ultratecperu."
    elif matched_general_keyword == 'horario':
        response = "Nuestro horario de atención es de lunes a viernes de 9:00 a 18:00, y los sábados de 10:00 a 14:00."
    
    # Lógica para precios usando fuzzy matching para productos
    elif matched_general_keyword == 'precio':
        found_product_key = None
        best_product_match = find_best_match(user_message_lower, list(products.keys()))
        
        if best_product_match:
             found_product_key = best_product_match

        if found_product_key:
            price = products[found_product_key]
            response = f"El precio de {found_product_key.title()} es: {price}"
        else:
            # Si preguntan por precio pero no se encuentra un producto con buena similitud
            priced_products_info = [p.title() for p, price_info in products.items() if 'Precio no especificado' not in price_info and not p.startswith('impresora')] # Productos con precio directo
            priceless_products_info = [p.title() for p, price_info in products.items() if 'Precio no especificado' in price_info and not p.startswith('impresora')] # Productos sin precio directo

            response_lines = ["Puedo darte información de precios para los siguientes productos:"]
            
            if priced_products_info:
                response_lines.append("\n**Productos con precio disponible:**")
                response_lines.extend([f"- {p}" for p in priced_products_info])
                
            if priceless_products_info:
                 response_lines.append("\n**Otros productos (por favor, contacta para precio):**")
                 response_lines.extend([f"- {p}" for p in priceless_products_info])
                 
            if not priced_products_info and not priceless_products_info:
                 response_lines = ["En este momento no tengo información de precios detallada para mostrar. Por favor, contáctanos directamente para consultar precios de productos específicos."]

            response_lines.append("\n¿De cuál te gustaría saber el precio, o necesitas consultar sobre otro producto?")
            
            response = "\n".join(response_lines)

    # --- Respuesta por defecto si no se encuentra una coincidencia general o de precio ---
    if not response:
         # Si la API de Wolfram Alpha estuviera activada y no encontró respuesta, usaríamos eso aquí.
         # ... (lógica de Wolfram Alpha si se reactiva) ...
         
         # Respuesta si no se encuentra ninguna coincidencia y la API no está activa/no responde
         response = (
            "Lo siento, no entendí tu pregunta. Soy un chatbot diseñado para ayudarte con información sobre ULTRATEC REPRESENTACIONES S.A.C.\n\n" +
            "Puedo responder sobre:\n"
            "- **Productos y Servicios:** (Impresoras, Mochilas, Suministros, Tintas, Cartuchos, Repuestos Laptop, Soportes Laptop, Enfriadores/Coolers, Reparación y Mantenimiento).\n"
            "- **Precios** (puedes preguntar por productos específicos).\n"
            "- **Ubicación y Envíos:** (Dirección en Lima, envíos a Piura).\n"
            "- **Contacto:** (Teléfono fijo, Facebook).\n"
            "- **Horario de Atención.\n\n"
            "¿Sobre cuál de estos temas te gustaría conversar?"
        )

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