from flask import Flask, render_template, request, redirect, url_for, session
import subprocess
import json
import os
import threading

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
PM2_PATH = "C:\\Users\\Administrator\\AppData\\Roaming\\npm\\pm2.cmd"  # Pas dit pad aan naar jouw situatie


def pm2_start():
    return subprocess.Popen([PM2_PATH, 'start', 'bot.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def pm2_stop():
    subprocess.run([PM2_PATH, 'stop', 'bot.py'], check=True)


def pm2_restart():
    subprocess.run([PM2_PATH, 'restart', 'bot.py'], check=True)


def async_get_console_output(callback):
    """Asynchroon logs ophalen zonder vast te lopen."""
    def fetch_logs():
        try:
            process = subprocess.Popen(
                [PM2_PATH, 'logs', 'discord-bot', '--lines', '10'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            output, _ = process.communicate(timeout=5)  # Timeout na 5 seconden
            callback(output or "No logs available.")
        except Exception as e:
            callback(f"Error fetching logs: {e}")

    thread = threading.Thread(target=fetch_logs)
    thread.start()


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
    console_output = []

    # Logs worden later opgehaald om de laadtijd te verkorten
    def handle_output(result):
        console_output.append(result)

    async_get_console_output(handle_output)

    return render_template('dashboard.html', user=user, console_output="Loading logs...")


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
