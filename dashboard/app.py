import logging
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import subprocess
import threading
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configureren van SocketIO
socketio = SocketIO(app)

# Gebruikersinformatie
users = {'Daan': 'Daan123'}

# PM2 pad configuratie
PM2_PATH = "C:\\Users\\Administrator\\AppData\\Roaming\\npm\\pm2.cmd"  # Pas dit pad aan als nodig

# PM2 commando's
def pm2_start():
    subprocess.run([PM2_PATH, 'start', 'bot.py', '--name', 'discord-bot'], check=True)

def pm2_stop():
    subprocess.run([PM2_PATH, 'stop', 'discord-bot'], check=True)

def pm2_restart():
    subprocess.run([PM2_PATH, 'restart', 'discord-bot'], check=True)

import time

def stream_console():
    """Stream de console output naar de webclient."""
    while True:
        time.sleep(1)  # Pauze om CPU te sparen
        socketio.emit('console_update', 'Bot draait...')  # Dummy log data, kan worden aangepast om echte logs door te geven

# Custom log handler die logs naar SocketIO stuurt
class SocketIOHandler(logging.Handler):
    def emit(self, record):
        log_message = self.format(record)
        socketio.emit('console_update', log_message)  # Zend log naar de frontend

@app.route('/start_bot', methods=['POST'])
def start_bot():
    try:
        pm2_start()
        logging.info("Bot gestart")
        return redirect(url_for('dashboard'))
    except Exception as e:
        logging.error(f"Error starting bot: {e}")
        return f"Error starting bot: {e}"

@app.route('/stop_bot', methods=['POST'])
def stop_bot():
    try:
        pm2_stop()
        logging.info("Bot gestopt")
        return redirect(url_for('dashboard'))
    except Exception as e:
        logging.error(f"Error stopping bot: {e}")
        return f"Error stopping bot: {e}"

@app.route('/restart_bot', methods=['POST'])
def restart_bot():
    try:
        pm2_restart()
        logging.info("Bot herstart")
        return redirect(url_for('dashboard'))
    except Exception as e:
        logging.error(f"Error restarting bot: {e}")
        return f"Error restarting bot: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Zorg ervoor dat de SocketIO verbinding correct werkt
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    socketio.emit('console_update', 'Connected to server')  # Verzend een bericht naar de frontend bij connectie

if __name__ == '__main__':
    # Logging configureren om naar SocketIO te sturen
    socketio_handler = SocketIOHandler()
    socketio_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    socketio_handler.setFormatter(formatter)
    logging.getLogger().addHandler(socketio_handler)
    
    # Start de console streaming in een aparte thread
    threading.Thread(target=stream_console, daemon=True).start()
    
    # Start de server met SocketIO
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
