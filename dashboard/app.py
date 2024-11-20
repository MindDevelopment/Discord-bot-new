from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import subprocess
import threading
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

# Gebruikersinformatie
users = {'Daan': 'Daan123'}

# PM2 pad configuratie
PM2_PATH = "C:\\Users\\Administrator\\AppData\\Roaming\\npm\\pm2.cmd"  # Pas dit pad aan als nodig
FULL_BOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../bot.py"))

# Functie om bot-log continu te lezen
def stream_logs():
    log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../bot.log"))
    try:
        with open(log_path, "r") as log_file:
            # Ga naar het einde van het logbestand
            log_file.seek(0, os.SEEK_END)

            while True:
                line = log_file.readline()
                if line:
                    socketio.emit('console_output', {'data': line})  # Stuur data naar de client
    except FileNotFoundError:
        socketio.emit('console_output', {'data': "Logbestand niet gevonden."})

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
        subprocess.run([PM2_PATH, 'start', FULL_BOT_PATH, '--name', 'discord-bot'], check=True)
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Error starting bot: {e}"

@app.route('/stop_bot', methods=['POST'])
def stop_bot():
    try:
        subprocess.run([PM2_PATH, 'stop', 'discord-bot'], check=True)
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Error stopping bot: {e}"

@app.route('/restart_bot', methods=['POST'])
def restart_bot():
    try:
        subprocess.run([PM2_PATH, 'restart', 'discord-bot'], check=True)
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Error restarting bot: {e}"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    log_thread = threading.Thread(target=stream_logs)
    log_thread.daemon = True
    log_thread.start()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
