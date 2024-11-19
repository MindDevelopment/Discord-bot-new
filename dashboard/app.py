# app.py (dashboard)
from flask import Flask, render_template, request, redirect, url_for, session
import subprocess
import threading
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Gebruikersinformatie
users = {'Daan': 'Daan123'}

# PM2 pad configuratie
PM2_PATH = "C:\\Users\\Administrator\\AppData\\Roaming\\npm\\pm2.cmd"  # Pas dit pad aan als nodig

# PM2 commando's
def pm2_start():
    subprocess.run([PM2_PATH, 'start', 'bot.py'], check=True)

def pm2_stop():
    subprocess.run([PM2_PATH, 'stop', 'bot.py'], check=True)

def pm2_restart():
    subprocess.run([PM2_PATH, 'restart', 'bot.py'], check=True)

def get_console_output():
    """Lees de laatste 10 regels van het logbestand."""
    try:
        with open("bot.log", "r") as log_file:
            lines = log_file.readlines()[-10:]  # Laatste 10 regels
        return "".join(lines)
    except Exception as e:
        return f"Error reading logs: {str(e)}"

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

    console_output = get_console_output()
    return render_template('dashboard.html', user=session['username'], console_output=console_output)

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
    app.run(debug=True, host='0.0.0.0', port=5000)
