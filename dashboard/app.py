from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit
import subprocess
import threading
import os
import psutil
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

socketio = SocketIO(app, cors_allowed_origins="*")

# Gebruikersinformatie
users = {'Daan': 'Daan123'}

# PM2 pad configuratie
PM2_PATH = "C:\\Users\\daans\\AppData\\Roaming\\npm\\pm2.cmd"
LOG_FILE_PATH = "bot.log"

bot_status = False

# PM2 commando's
def pm2_start():
    global bot_status
    subprocess.run([PM2_PATH, 'start', 'bot.py', '--name', 'discord-bot'], check=True)
    bot_status = True

def pm2_stop():
    global bot_status
    subprocess.run([PM2_PATH, 'stop', 'discord-bot'], check=True)
    bot_status = False

def pm2_restart():
    global bot_status
    subprocess.run([PM2_PATH, 'restart', 'discord-bot'], check=True)
    bot_status = True

def stream_console():
    """Stream de console output naar de webclient."""
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
        bot_status = False
    return jsonify({'bot_status': bot_status})

@app.route('/start_bot', methods=['POST'])
def start_bot():
    try:
        pm2_start()
        return jsonify({'success': True, 'message': 'Bot gestart.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Fout bij starten: {e}'})

@app.route('/stop_bot', methods=['POST'])
def stop_bot():
    try:
        pm2_stop()
        return jsonify({'success': True, 'message': 'Bot gestopt.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Fout bij stoppen: {e}'})

@app.route('/restart_bot', methods=['POST'])
def restart_bot():
    try:
        pm2_restart()
        return jsonify({'success': True, 'message': 'Bot opnieuw gestart.'})
    except Exception as e:
        return f"Error restarting bot: {e}"

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    system_info = get_system_info()  # Haal de systeeminformatie op
    return render_template('dashboard.html', user=session['username'], **system_info)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Ongeldige gebruikersnaam of wachtwoord.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    threading.Thread(target=stream_console, daemon=True).start()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
