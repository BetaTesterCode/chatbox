from flask import Flask, render_template, request, jsonify
import requests
import os
from fuzzywuzzy import process # Importar fuzzywuzzy

app = Flask(__name__)

# Catálogo de productos con precios y descripciones
productos = {
    'laptops': {
        'gaming': {
            'laptop_gaming_1': {
                'nombre': 'Laptop Gaming MSI Katana',
                'precio': 'S/ 4,999.00',
                'especificaciones': {
                    'procesador': 'Intel Core i7 12th Gen',
                    'ram': '16GB DDR4',
                    'almacenamiento': 'SSD 512GB',
                    'tarjeta_grafica': 'NVIDIA RTX 3060 6GB',
                    'pantalla': '15.6" FHD 144Hz'
                },
                'descripcion': 'Ideal para gaming y trabajo profesional'
            },
            'laptop_gaming_2': {
                'nombre': 'Laptop Gaming ASUS TUF',
                'precio': 'S/ 3,999.00',
                'especificaciones': {
                    'procesador': 'AMD Ryzen 7',
                    'ram': '16GB DDR4',
                    'almacenamiento': 'SSD 512GB',
                    'tarjeta_grafica': 'NVIDIA RTX 3050 4GB',
                    'pantalla': '15.6" FHD 144Hz'
                },
                'descripcion': 'Excelente relación precio-rendimiento'
            }
        },
        'profesional': {
            'laptop_pro_1': {
                'nombre': 'Laptop HP Envy',
                'precio': 'S/ 3,499.00',
                'especificaciones': {
                    'procesador': 'Intel Core i7 12th Gen',
                    'ram': '16GB DDR4',
                    'almacenamiento': 'SSD 512GB',
                    'tarjeta_grafica': 'Intel Iris Xe',
                    'pantalla': '15.6" FHD'
                },
                'descripcion': 'Perfecta para trabajo profesional'
            },
            'laptop_pro_2': {
                'nombre': 'Laptop Dell XPS',
                'precio': 'S/ 4,499.00',
                'especificaciones': {
                    'procesador': 'Intel Core i7 12th Gen',
                    'ram': '16GB DDR4',
                    'almacenamiento': 'SSD 1TB',
                    'tarjeta_grafica': 'NVIDIA RTX 3050 4GB',
                    'pantalla': '15.6" 4K'
                },
                'descripcion': 'Alta gama para profesionales exigentes'
            }
        },
        'estudio': {
            'laptop_estudio_1': {
                'nombre': 'Laptop Lenovo IdeaPad',
                'precio': 'S/ 2,499.00',
                'especificaciones': {
                    'procesador': 'Intel Core i5 12th Gen',
                    'ram': '8GB DDR4',
                    'almacenamiento': 'SSD 256GB',
                    'tarjeta_grafica': 'Intel Iris Xe',
                    'pantalla': '15.6" FHD'
                },
                'descripcion': 'Ideal para estudiantes'
            },
            'laptop_estudio_2': {
                'nombre': 'Laptop Acer Aspire',
                'precio': 'S/ 1,999.00',
                'especificaciones': {
                    'procesador': 'AMD Ryzen 5',
                    'ram': '8GB DDR4',
                    'almacenamiento': 'SSD 256GB',
                    'tarjeta_grafica': 'AMD Radeon Graphics',
                    'pantalla': '15.6" FHD'
                },
                'descripcion': 'Económica y eficiente para estudios'
            }
        }
    },
    'desktops': {
        'gaming': {
            'pc_gaming_1': {
                'nombre': 'PC Gaming Ultra',
                'precio': 'S/ 5,999.00',
                'especificaciones': {
                    'procesador': 'Intel Core i9 12th Gen',
                    'ram': '32GB DDR4',
                    'almacenamiento': 'SSD 1TB + HDD 2TB',
                    'tarjeta_grafica': 'NVIDIA RTX 3070 8GB',
                    'refrigeracion': 'Líquida'
                },
                'descripcion': 'Alto rendimiento para gaming y streaming'
            },
            'pc_gaming_2': {
                'nombre': 'PC Gaming Pro',
                'precio': 'S/ 4,499.00',
                'especificaciones': {
                    'procesador': 'AMD Ryzen 7',
                    'ram': '16GB DDR4',
                    'almacenamiento': 'SSD 512GB + HDD 1TB',
                    'tarjeta_grafica': 'NVIDIA RTX 3060 6GB',
                    'refrigeracion': 'Aire'
                },
                'descripcion': 'Excelente para gaming y trabajo'
            }
        },
        'profesional': {
            'pc_pro_1': {
                'nombre': 'PC Workstation',
                'precio': 'S/ 3,999.00',
                'especificaciones': {
                    'procesador': 'Intel Core i7 12th Gen',
                    'ram': '32GB DDR4',
                    'almacenamiento': 'SSD 1TB',
                    'tarjeta_grafica': 'NVIDIA RTX 3050 4GB',
                    'refrigeracion': 'Aire'
                },
                'descripcion': 'Potente para trabajo profesional'
            }
        },
        'estudio': {
            'pc_estudio_1': {
                'nombre': 'PC Estudio',
                'precio': 'S/ 2,499.00',
                'especificaciones': {
                    'procesador': 'Intel Core i5 12th Gen',
                    'ram': '16GB DDR4',
                    'almacenamiento': 'SSD 512GB',
                    'tarjeta_grafica': 'Intel UHD Graphics',
                    'refrigeracion': 'Aire'
                },
                'descripcion': 'Ideal para estudiantes y trabajo básico'
            }
        }
    },
    'impresoras': {
        'epson l3250': {
            'precio': 'S/ 699.00 (efectivo) o S/ 730.00 (tarjeta)',
            'descripcion': 'Impresora multifuncional con sistema de tanque de tinta'
        },
        'epson l4260': {
            'precio': 'S/ 899.00 (efectivo) o S/ 930.00 (tarjeta)',
            'descripcion': 'Impresora multifuncional con WiFi y panel táctil'
        }
    },
    'tintas': {
        'kit tintas epson': {
            'precio': 'S/ 120.00',
            'descripcion': 'Kit completo (negro, cian, magenta, amarillo)'
        },
        'tinta negra epson': {
            'precio': 'S/ 35.00',
            'descripcion': 'Botella de tinta negra original'
        }
    },
    'mochilas': {
        'mochila 15.6': {
            'precio': 'S/ 89.90',
            'descripcion': 'Mochila para laptop hasta 15.6"'
        },
        'mochila 17.3': {
            'precio': 'S/ 99.90',
            'descripcion': 'Mochila para laptop hasta 17.3"'
        }
    }
}

# Catálogo de servicios con precios
servicios = {
    'reparacion': {
        'diagnostico': {
            'precio': 'S/ 30.00',
            'descripcion': 'Diagnóstico completo del equipo'
        },
        'limpieza': {
            'precio': 'S/ 50.00',
            'descripcion': 'Limpieza interna y cambio de pasta térmica'
        },
        'pantalla': {
            'precio': 'Desde S/ 200.00',
            'descripcion': 'Reemplazo de pantalla (precio varía según modelo)'
        }
    },
    'mantenimiento': {
        'preventivo': {
            'precio': 'S/ 80.00',
            'descripcion': 'Mantenimiento preventivo completo'
        },
        'correctivo': {
            'precio': 'Desde S/ 50.00',
            'descripcion': 'Mantenimiento según el problema específico'
        }
    }
}

# Servicios ofrecidos (lista más descriptiva)
services_list = [
    'Venta de equipos tecnológicos nuevos y con garantía (laptops, impresoras, accesorios y más).',
    'Servicios de soporte técnico especializado para empresas.',
    'Servicios de soporte técnico para usuarios domésticos (personas naturales).',
    'Reparación profesional de laptops y computadoras.',
    'Mantenimiento preventivo y correctivo de equipos tecnológicos.',
    'Asesoría personalizada para elegir el equipo o solución adecuada.'
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

    # Saludos
    if any(greeting in user_message_lower for greeting in ['hola', 'buenas', 'buenos dias', 'buenas tardes']):
        return jsonify({
            'response': "¡Hola! Soy el asistente virtual de ULTRATEC. ¿En qué puedo ayudarte hoy? Puedo informarte sobre:\n\n" +
                      "📱 Productos y precios\n" +
                      "🔧 Servicios de reparación\n" +
                      "📞 Información de contacto\n" +
                      "📍 Ubicación\n\n" +
                      "¿Qué te gustaría saber?"
        })

    # Manejo de selección de equipos (Laptops y PCs)
    elif 'laptop' in user_message_lower or 'computadora' in user_message_lower or 'pc' in user_message_lower or 'juegos' in user_message_lower or 'gaming' in user_message_lower:
        # Si solo dice 'juegos' o 'gaming' sin especificar laptop/pc, preguntar primero
        if ('juegos' in user_message_lower or 'gaming' in user_message_lower) and not any(term in user_message_lower for term in ['laptop', 'computadora', 'pc']):
             response = "¡Excelente elección! Para juegos te recomiendo equipos con buen rendimiento. ¿Tienes preferencia por laptop o PC, o te gustaría ver ambas opciones?\n\n"
             response += "Tenemos opciones para:\n"
             response += "🎮 Gaming/Juegos (Laptops y PCs)\n"
             response += "💼 Trabajo Profesional (Laptops y PCs)\n"
             response += "📚 Estudio (Laptops y PCs)\n\n"
             response += "¿Qué tipo de equipo te interesa para juegos?"
             return jsonify({'response': response})

        # Si especifica 'gaming' o 'juegos' Y 'laptop'/'pc'
        elif 'gaming' in user_message_lower or 'juegos' in user_message_lower:
            response = "¡Excelente elección! Para gaming te recomiendo equipos con buen rendimiento. ¿Tienes un presupuesto en mente?\n\n"
            response += "Tenemos estas opciones:\n\n"

            if any(term in user_message_lower for term in ['laptop']):
                response += "**Laptops Gaming:**\n"
                for laptop in productos['laptops']['gaming'].values():
                    response += f"📱 {laptop['nombre']}\n"
                    response += f"💰 {laptop['precio']}\n"
                    response += "Especificaciones:\n"
                    for key, value in laptop['especificaciones'].items():
                        response += f"- {key.replace('_', ' ').title()}: {value}\n"
                    response += f"📝 {laptop['descripcion']}\n\n"

            if any(term in user_message_lower for term in ['computadora', 'pc']):
                response += "**PCs Gaming:**\n"
                for pc in productos['desktops']['gaming'].values():
                    response += f"🖥️ {pc['nombre']}\n"
                    response += f"💰 {pc['precio']}\n"
                    response += "Especificaciones:\n"
                    for key, value in pc['especificaciones'].items():
                        response += f"- {key.replace('_', ' ').title()}: {value}\n"
                    response += f"📝 {pc['descripcion']}\n\n"

            if not any(term in user_message_lower for term in ['laptop', 'computadora', 'pc']):
                 # Si se preguntó solo por gaming/juegos, pero no se especificó laptop/pc, mostrar ambas
                 response = "¡Excelente elección! Para gaming te recomiendo equipos con buen rendimiento. ¿Tienes un presupuesto en mente?\n\n"
                 response += "Tenemos estas opciones:\n\n"

                 response += "**Laptops Gaming:**\n"
                 for laptop in productos['laptops']['gaming'].values():
                     response += f"📱 {laptop['nombre']}\n"
                     response += f"💰 {laptop['precio']}\n"
                     response += "Especificaciones:\n"
                     for key, value in laptop['especificaciones'].items():
                         response += f"- {key.replace('_', ' ').title()}: {value}\n"
                     response += f"📝 {laptop['descripcion']}\n\n"

                 response += "**PCs Gaming:**\n"
                 for pc in productos['desktops']['gaming'].values():
                     response += f"🖥️ {pc['nombre']}\n"
                     response += f"💰 {pc['precio']}\n"
                     response += "Especificaciones:\n"
                     for key, value in pc['especificaciones'].items():
                         response += f"- {key.replace('_', ' ').title()}: {value}\n"
                     response += f"📝 {pc['descripcion']}\n\n"


            response += "¿Cuál de estas opciones te interesa más? ¿O prefieres ver otras alternativas?"
            return jsonify({'response': response})

        elif 'profesional' in user_message_lower or 'trabajo' in user_message_lower:
            response = "¡Perfecto! Para trabajo profesional necesitarás un equipo potente. ¿Cuál es tu presupuesto?\n\n"
            response += "Te muestro nuestras opciones:\n\n"
            response += "**Laptops Profesionales:**\n"
            for laptop in productos['laptops']['profesional'].values():
                response += f"📱 {laptop['nombre']}\n"
                response += f"💰 {laptop['precio']}\n"
                response += "Especificaciones:\n"
                for key, value in laptop['especificaciones'].items():
                    response += f"- {key.replace('_', ' ').title()}: {value}\n"
                response += f"📝 {laptop['descripcion']}\n\n"
            
            response += "**PCs Profesionales:**\n"
            for pc in productos['desktops']['profesional'].values():
                response += f"🖥️ {pc['nombre']}\n"
                response += f"💰 {pc['precio']}\n"
                response += "Especificaciones:\n"
                for key, value in pc['especificaciones'].items():
                    response += f"- {key.replace('_', ' ').title()}: {value}\n"
                response += f"📝 {pc['descripcion']}\n\n"
            
            response += "¿Cuál de estas opciones se ajusta mejor a tus necesidades?"
            return jsonify({'response': response})

        elif 'estudio' in user_message_lower or 'estudiante' in user_message_lower:
            response = "¡Entendido! Para estudios necesitarás un equipo confiable pero económico. ¿Cuál es tu presupuesto?\n\n"
            response += "Te muestro nuestras opciones:\n\n"
            response += "**Laptops para Estudio:**\n"
            for laptop in productos['laptops']['estudio'].values():
                response += f"📱 {laptop['nombre']}\n"
                response += f"💰 {laptop['precio']}\n"
                response += "Especificaciones:\n"
                for key, value in laptop['especificaciones'].items():
                    response += f"- {key.replace('_', ' ').title()}: {value}\n"
                response += f"📝 {laptop['descripcion']}\n\n"
            
            response += "**PCs para Estudio:**\n"
            for pc in productos['desktops']['estudio'].values():
                response += f"🖥️ {pc['nombre']}\n"
                response += f"💰 {pc['precio']}\n"
                for key, value in pc['especificaciones'].items():
                    response += f"- {key.replace('_', ' ').title()}: {value}\n"
                response += f"📝 {pc['descripcion']}\n\n"
            
            response += "¿Cuál de estas opciones te parece más adecuada?"
            return jsonify({'response': response})

        else:
            response = "¡Claro! Para ayudarte mejor, ¿podrías decirme para qué vas a usar el equipo?\n\n"
            response += "Tenemos opciones para:\n"
            response += "🎮 Gaming/Juegos\n"
            response += "💼 Trabajo Profesional\n"
            response += "📚 Estudio\n\n"
            response += "¿Cuál de estas categorías se ajusta mejor a tus necesidades?"
            return jsonify({'response': response})

    # Consulta de precios de otros productos (Impresoras, Tintas, Mochilas)
    elif 'precio' in user_message_lower or 'costo' in user_message_lower:
        if 'tinta' in user_message_lower:
            response = "¡Claro! ¿Sobre qué tipo de tinta te gustaría saber precios o tienes un presupuesto en mente?"
            # Podemos listar opciones si el usuario especifica o pregunta por general
            if 'epson' in user_message_lower or 'kit' in user_message_lower:
                 response += "\n\nNuestro catálogo de tintas incluye:\n\n"
                 for producto, detalles in productos['tintas'].items():
                     response += f"**{producto.title()}**\n"
                     response += f"Precio: {detalles['precio']}\n"
                     response += f"Descripción: {detalles['descripcion']}\n\n"
                 response += "¿Hay alguna que te interese en particular?"

            return jsonify({'response': response})

        elif 'impresora' in user_message_lower:
            response = "¡Por supuesto! ¿Estás buscando una impresora para hogar, oficina, o alguna característica específica? ¿Tienes un presupuesto?\n\n"
            # Podemos listar opciones si el usuario especifica o pregunta por general
            # if '(algún tipo específico)' in user_message_lower:
            # (Lógica para filtrar por tipo/presupuesto - más compleja sin estado)
            # else:
            response += "Nuestro catálogo de impresoras incluye modelos como:\n\n"
            for producto, detalles in productos['impresoras'].items():
                 response += f"**{producto.title()}**\n"
                 response += f"Precio: {detalles['precio']}\n"
                 response += f"Descripción: {detalles['descripcion']}\n\n"
            response += "¿Necesitas más información sobre algún modelo?"
            return jsonify({'response': response})

        elif 'mochila' in user_message_lower:
            response = "¡Con gusto! ¿Qué tamaño de laptop tienes o cuál es tu presupuesto para una mochila?\n\n"
            # Podemos listar opciones si el usuario especifica o pregunta por general
            # if '(tamaño o presupuesto)' in user_message_lower:
            # (Lógica para filtrar por tamaño/presupuesto - más compleja sin estado)
            # else:
            response += "Aquí está nuestro catálogo de mochilas:\n\n"
            for producto, detalles in productos['mochilas'].items():
                 response += f"**{producto.title()}**\n"
                 response += f"Precio: {detalles['precio']}\n"
                 response += f"Descripción: {detalles['descripcion']}\n\n"
            response += "¿Te gustaría conocer más detalles sobre alguna mochila?"
            return jsonify({'response': response})
        
        # Default price query response if no specific product category is matched
        else:
             response = "Claro, ¿sobre qué producto o categoría de productos te gustaría saber precios? Por ejemplo: impresoras, tintas, mochilas."
             return jsonify({'response': response})


    # Consulta general de productos (sin especificar precios)
    elif 'productos' in user_message_lower or 'catalogo' in user_message_lower:
        response = "¡Claro! Tenemos una variedad de productos tecnológicos, incluyendo:\n\n"
        response += "- 📱 **Laptops y PCs** (para gaming, trabajo profesional y estudio)\n"
        response += "- 🖨️ **Impresoras**\n"
        response += "- 🧴 **Tintas** y suministros\n"
        response += "- 🎒 **Mochilas** y accesorios\n\n"
        response += "¿Te interesa algún tipo de producto en particular o quieres ver los precios?"
        return jsonify({'response': response})


    # Consulta de servicios
    elif 'reparacion' in user_message_lower or 'reparar' in user_message_lower:
        response = "¡Claro! ¿Qué tipo de reparación necesitas o cuál es el problema principal del equipo? ¿Tienes un presupuesto?\n\n"
        # Podemos listar opciones si el usuario especifica o pregunta por general
        # if '(tipo de reparación)' in user_message_lower:
        # (Lógica para filtrar por tipo/presupuesto - más compleja sin estado)
        # else:
        response += "Ofrecemos servicios de reparación como:\n\n"
        for servicio, detalles in servicios['reparacion'].items():
            response += f"**{servicio.title()}**\n"
            response += f"Precio: {detalles['precio']}\n"
            response += f"Descripción: {detalles['descripcion']}\n\n"
        response += "¿Qué tipo de reparación necesitas? Puedo darte más detalles."
        return jsonify({'response': response})

    elif 'mantenimiento' in user_message_lower:
        response = "¡Por supuesto! ¿Te interesa el mantenimiento preventivo o correctivo? ¿Tienes algún detalle del problema o un presupuesto?\n\n"
        # Podemos listar opciones si el usuario especifica o pregunta por general
        # if '(tipo de mantenimiento)' in user_message_lower:
        # (Lógica para filtrar por tipo/presupuesto - más compleja sin estado)
        # else:
        response += "Aquí están nuestros servicios de mantenimiento:\n\n"
        for servicio, detalles in servicios['mantenimiento'].items():
            response += f"**{servicio.title()}**\n"
            response += f"Precio: {detalles['precio']}\n"
            response += f"Descripción: {detalles['descripcion']}\n\n"
        response += "¿Qué tipo de mantenimiento te interesa?"
        return jsonify({'response': response})
    
    # Consulta general de servicios
    elif 'servicios' in user_message_lower:
        response = "¡Claro! Ofrecemos una variedad de servicios técnicos, incluyendo:\n\n"
        for service_desc in services_list:
            response += f"- {service_desc}\n"
        response += "\n¿Te interesa algún servicio en particular, como reparación o mantenimiento?"
        return jsonify({'response': response})


    # Información de contacto
    elif 'contacto' in user_message_lower or 'telefono' in user_message_lower or 'email' in user_message_lower or 'whatsapp' in user_message_lower:
        response = "¡Por supuesto! Puedes contactarnos de las siguientes formas:\n\n"
        response += "📞 Teléfono: 969 922 771\n"
        response += "📧 Email: ventas@ultratec.pe\n"
        response += "🌐 Web: ultratec.pe\n\n"
        response += "Nuestro horario de atención es de lunes a viernes de 8:00 AM a 6:00 PM y sábados de 9:00 AM a 1:00 PM."
        return jsonify({'response': response})

    # Ubicación
    elif 'ubicacion' in user_message_lower or 'direccion' in user_message_lower or 'donde estan' in user_message_lower:
        response = "¡Claro! Nuestra tienda está ubicada en:\n\n"
        response += "📍 Jirón Ica 500-598 centro de Piura\n"
        response += "Ref. esquina Arequipa con Ica, Piura, Perú\n\n"
        response += "Estamos en el centro de Piura."
        return jsonify({'response': response})

    # Respuesta por defecto (Fallback mejorado)
    else:
        response = """Lo siento, no estoy seguro de haberte entendido. Puedo ayudarte con:

📱 Información sobre **Productos** y **precios** (laptops, PCs, impresoras, tintas, mochilas)
🔧 **Servicios** de reparación y mantenimiento
📞 Información de **contacto**
📍 **Ubicación**

¿Sobre qué te gustaría saber?"""
        return jsonify({'response': response})

if __name__ == '__main__':
    # Para probar localmente usando la variable de entorno,
    # necesitarías configurar la variable WOLFRAM_ALPHA_API_KEY
    # en tu sistema antes de ejecutar 'python app.py'.
    # Si quieres probar localmente sin configurar la variable de entorno,
    # puedes descomentar la línea 'WOLFRAM_ALPHA_API_KEY = "TU_CLAVE_AQUI"'
    # y poner tu clave ahí temporalmente (menos seguro para producción).
    app.run(debug=True) 