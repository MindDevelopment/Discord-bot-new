# app.py (dashboard met live console-updates)
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import subprocess
import threading
import os
import json
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Gebruikersinformatie
users = {'Daan': 'Daan123'}

# Socket.IO instellen
socketio = SocketIO(app)

# PM2 pad configuratie
PM2_PATH = "C:\\Users\\Administrator\\AppData\\Roaming\\npm\\pm2.cmd"  # Pas dit pad aan als nodig

# Console-output streamen naar clients
def stream_console_logs():
    log_path = os.path.join(os.path.dirname(__file__), "..", "bot.log")
    if not os.path.exists(log_path):
        return

    with open(log_path, "r") as log_file:
        # Lees de log vanaf het einde
        log_file.seek(0, os.SEEK_END)
        while True:
            line = log_file.readline()
            if line:
                socketio.emit('console_output', {'data': line})
            time.sleep(1)  # Beperk CPU-gebruik

# Start de console-logstream in een aparte thread
@socketio.on('connect')
def handle_connect():
    threading.Thread(target=stream_console_logs, daemon=True).start()

# PM2 commando's
def pm2_start():
    subprocess.run([PM2_PATH, 'start', 'bot.py'], check=True)

def pm2_stop():
    subprocess.run([PM2_PATH, 'stop', 'bot.py'], check=True)

def pm2_restart():
    subprocess.run([PM2_PATH, 'restart', 'bot.py'], check=True)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['username'])

@app.route('/start_bot', methods=['POST'])
def start_bot():
    try:
        pm2_start()
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Error starting bot: {e}"

@app.route('/stop_bot', methods=['POST'])
def stop_bot():
    try:
        pm2_stop()
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Error stopping bot: {e}"

@app.route('/restart_bot', methods=['POST'])
def restart_bot():
    try:
        pm2_restart()
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Error restarting bot: {e}"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
