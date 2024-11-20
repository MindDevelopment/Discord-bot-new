# app.py (dashboard)
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import subprocess
import threading
import json
import os
import time

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
    """Start de bot met PM2."""
    subprocess.run([PM2_PATH, 'start', 'bot.py'], check=True)

def pm2_stop():
    """Stop de bot met PM2."""
    subprocess.run([PM2_PATH, 'stop', 'bot.py'], check=True)

def pm2_restart():
    """Herstart de bot met PM2."""
    subprocess.run([PM2_PATH, 'restart', 'bot.py'], check=True)

def stream_console():
    """Stream de console output naar de webclient via SocketIO."""
    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bot.log")
    try:
        with open(log_path, "r") as log_file:
            while True:
                # Lees nieuwe regels toe aan het bestand
                new_line = log_file.readline()
                if new_line:
                    socketio.emit('console_update', new_line)  # Stuur elke nieuwe regel naar de client
                time.sleep(1)  # 1 seconde pauze tussen updates
    except Exception as e:
        print(f"Error reading log: {e}")

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

if __name__ == '__main__':
    # Start de console streaming in een aparte thread
    threading.Thread(target=stream_console, daemon=True).start()
    
    # Start de server met SocketIO
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
