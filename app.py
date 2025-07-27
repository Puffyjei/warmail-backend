from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Esto añade la cabecera Access-Control-Allow-Origin: *

@app.route('/')
def index():
    return 'Warmail backend funcionando'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = f"{username}@warmail.com"
    
    # Aquí deberías guardar el usuario (esto es solo una simulación)
    print(f"Registrado: {email} con contraseña {password}")

    return jsonify({"message": "Usuario registrado correctamente", "email": email})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Aquí deberías verificar la contraseña (esto es solo una simulación)
    inbox = [
        {"from": "otro@warmail.com", "message": "¡Hola!"},
        {"from": "admin@warmail.com", "message": "Bienvenido a Warmail."}
    ]
    return jsonify({"inbox": inbox})

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    from_email = data.get('from')
    to_email = data.get('to')
    message = data.get('message')
    
    # Aquí deberías guardar el mensaje (esto es solo una simulación)
    print(f"{from_email} envió a {to_email}: {message}")

    return jsonify({"message": "Correo enviado correctamente"})
