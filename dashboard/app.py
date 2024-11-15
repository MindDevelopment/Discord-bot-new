from flask import Flask, redirect, url_for, session, render_template, request
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Zorg ervoor dat je een geheime sleutel hebt voor sessies

# Tijdelijke lijst met gebruikers (in plaats van Discord login)
users = {
    "Daan": "Daan123"  # Voeg je tijdelijke gebruikersnaam en wachtwoord toe
}

# Config laden (je huidige config blijft hetzelfde)
with open('./config/config.json', 'r') as config_file:
    config = json.load(config_file)

CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']
REDIRECT_URI = config['redirect_uri']

<<<<<<< Updated upstream
=======
<<<<<<< HEAD
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

=======
>>>>>>> 7ae39fdac9dde89f18ca24226200b68f9ef4c7f3
>>>>>>> Stashed changes
# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Controleer of de gebruikersnaam en wachtwoord correct zijn
        if users.get(username) == password:
            # Als de inloggegevens juist zijn, sla deze op in de sessie
            session['user'] = username
            return redirect(url_for('index'))
        else:
            # Als de inloggegevens verkeerd zijn, geef een foutmelding weer
            return "Foutieve gebruikersnaam of wachtwoord!"
    return render_template('login.html')  # Toon het loginformulier

# Index route
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = session['user']
<<<<<<< Updated upstream
    return render_template('index.html', user=user)
=======
    console_output = get_console_output()  # Haal de console-output op
    return render_template('index.html', user=user, console_output=console_output)
>>>>>>> Stashed changes

# Logout route
@app.route('/logout')
def logout():
    session.clear()  # Verwijder alle sessie-informatie
    return redirect(url_for('login'))  # Redirect naar de loginpagina

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
