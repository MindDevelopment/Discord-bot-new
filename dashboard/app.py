from flask import Flask, redirect, url_for, session, render_template, request
import requests
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Zorg ervoor dat je een geheime sleutel hebt voor sessies

# Config laden
with open('./config/config.json', 'r') as config_file:
    config = json.load(config_file)

CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']
REDIRECT_URI = config['redirect_uri']

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
    return render_template('index.html', user=user)

# Logout route
@app.route('/logout')
def logout():
    session.clear()  # Verwijder alle sessie-informatie
    return redirect(url_for('login'))  # Redirect naar de loginpagina

if __name__ == '__main__':
    app.run(debug=True)
