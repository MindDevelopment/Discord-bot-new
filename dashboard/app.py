from flask import Flask, render_template, request, redirect, url_for, session
import subprocess
import json
import os
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Zorg ervoor dat je een geheime sleutel hebt voor sessies

# Gebruikersnaam en wachtwoord (voor de demo, beter in een database voor productie)
users = {
    'Daan': 'Daan123'
}

# Config laden
with open('./config/config.json', 'r') as config_file:
    config = json.load(config_file)

CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']
REDIRECT_URI = config['redirect_uri']

# PM2 commando's
def pm2_start():
    return subprocess.Popen(['pm2', 'start', 'bot.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def pm2_stop():
    subprocess.run(['pm2', 'stop', 'bot.py'], check=True)

def pm2_restart():
    subprocess.run(['pm2', 'restart', 'bot.py'], check=True)

def get_console_output():
    """ Haal de laatste uitvoer op van de bot via PM2 logs """
    process = subprocess.Popen(['pm2', 'logs', 'discord-bot'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, errors = process.communicate()
    return output

# Inlog route
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))  # Als de gebruiker al ingelogd is, doorverwijzen naar het dashboard

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['username'] = username  # Gebruiker inloggen
            return redirect(url_for('dashboard'))  # Doorverwijzen naar het dashboard
        else:
            return "Invalid credentials, please try again."

    return render_template('login.html')

# Dashboard route (alleen toegankelijk na inloggen)
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))  # Als de gebruiker niet is ingelogd, doorverwijzen naar inlogpagina
    
    user = session['username']
    console_output = get_console_output()  # Haal de console-output op van de bot
    return render_template('dashboard.html', user=user, console_output=console_output)

# Start route voor de bot
@app.route('/start_bot', methods=['POST'])
def start_bot():
    try:
        pm2_start()
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Error starting bot: {e}"

# Stop route voor de bot
@app.route('/stop_bot', methods=['POST'])
def stop_bot():
    try:
        pm2_stop()
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Error stopping bot: {e}"

# Restart route voor de bot
@app.route('/restart_bot', methods=['POST'])
def restart_bot():
    try:
        pm2_restart()
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Error restarting bot: {e}"

# Logout route
@app.route('/logout')
def logout():
    session.clear()  # Verwijder alle sessie-informatie
    return redirect(url_for('index'))  # Redirect naar de inlogpagina

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
