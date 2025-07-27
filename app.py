from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Permitir cualquier origen


import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    return conn

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = f"{username}@warmail"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    if cur.fetchone():
        return jsonify({'error': 'Email ya existe'}), 400
    cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Usuario creado', 'email': email})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cur.fetchone()
    if not user:
        return jsonify({'error': 'Credenciales inválidas'}), 401
    cur.execute("SELECT sender, content FROM messages WHERE receiver = %s", (email,))
    messages = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({'inbox': [{'from': m[0], 'message': m[1]} for m in messages]})

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    sender = data['from']
    receiver = data['to']
    content = data['message']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (sender, receiver, content) VALUES (%s, %s, %s)", (sender, receiver, content))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Mensaje enviado'})

@app.route('/')
def home():
    return 'API de Warmail funcionando'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
