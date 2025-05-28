from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True) 