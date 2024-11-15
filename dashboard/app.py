from flask import Flask, redirect, url_for, session, render_template, request
import subprocess
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Zorg ervoor dat je een geheime sleutel hebt voor sessies

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

# Login route
@app.route('/login')
def login():
    auth_url = f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&scope=bot+identify&response_type=code&redirect_uri={REDIRECT_URI}"
    return redirect(auth_url)

# Callback route
@app.route('/callback')
def callback():
    code = request.args.get('code')  # Haal de code op uit de URL
    guild_id = request.args.get('guild_id')
    permissions = request.args.get('permissions')

    # Verkrijg token van Discord
    token_url = 'https://discord.com/api/oauth2/token'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'scope': 'bot+identify'
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get('access_token')

    # Verkrijg gebruikersinformatie
    user_url = 'https://discord.com/api/v9/users/@me'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    user_info = requests.get(user_url, headers=headers).json()

    # Sla gebruikersinformatie op in de sessie
    session['user'] = user_info
    session['access_token'] = access_token

    return redirect(url_for('index', user=user_info))

# Index route
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = session['user']
    console_output = get_console_output()  # Haal de console-output op
    return render_template('index.html', user=user, console_output=console_output)

# Start route voor de bot
@app.route('/start_bot', methods=['POST'])
def start_bot():
    try:
        pm2_start()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error starting bot: {e}"

# Stop route voor de bot
@app.route('/stop_bot', methods=['POST'])
def stop_bot():
    try:
        pm2_stop()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error stopping bot: {e}"

# Restart route voor de bot
@app.route('/restart_bot', methods=['POST'])
def restart_bot():
    try:
        pm2_restart()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error restarting bot: {e}"

# Logout route
@app.route('/logout')
def logout():
    session.clear()  # Verwijder alle sessie-informatie
    return redirect(url_for('login'))  # Redirect naar de loginpagina

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
