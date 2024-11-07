// index.js - Het dashboard en de server voor de bot beheren
const cors = require('cors');
const express = require('express');
const { exec } = require('child_process');
const WebSocket = require('ws');

// Maak een express app voor het dashboard
const app = express();
app.use(cors());

// Stel EJS in als template engine
app.set('view engine', 'ejs');

// Serve de statische bestanden van het dashboard (bijv. HTML, CSS, JS)
app.use(express.static('public')); // Zorg ervoor dat de 'public' map bestaat

// Stop route voor de bot
app.post('/dashboard/stop', (req, res) => {
    exec('pm2 stop bot.js --name "bot"', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return res.status(500).send("Er is iets mis gegaan met het stoppen van de bot.");
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return res.status(500).send("Er is iets mis gegaan met het stoppen van de bot.");
        }
        console.log(`stdout: ${stdout}`);
        res.send("Bot is stopped.");
    });
});

// Start route voor de bot
app.post('/dashboard/start', (req, res) => {
    exec('pm2 start bot.js --name "bot"', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return res.status(500).send("Er is iets mis gegaan met het starten van de bot.");
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return res.status(500).send("Er is iets mis gegaan met het starten van de bot.");
        }
        console.log(`stdout: ${stdout}`);
        res.send("Bot is starting...");
    });
});

// Restart route voor de bot
app.post('/dashboard/restart', (req, res) => {
    exec('pm2 restart bot.js', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return res.status(500).send("Er is iets mis gegaan met het herstarten van de bot.");
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return res.status(500).send("Er is iets mis gegaan met het herstarten van de bot.");
        }
        console.log(`stdout: ${stdout}`);
        res.send("Bot is restarting...");
    });
});

// Nieuwe route voor de consolepagina
app.get('/dashboard/console', (req, res) => {
    res.sendFile(__dirname + '/public/console.html');  // Verwijs naar de nieuwe consolepagina
});

// Nieuwe route voor de commando lijst
app.get('/dashboard/commands', (req, res) => {
    const commandList = [];

    // Voeg alle commando's toe aan een lijst
    client.commands.forEach((command, name) => {
        commandList.push({
            name: command.name,
            description: command.description || 'Geen beschrijving'
        });
    });

    // Render de pagina met de commandolijst
    res.render('commands', { commands: commandList });
});

// Setup WebSocket server voor console logs en commando's
const wss = new WebSocket.Server({ noServer: true });

// Wanneer een nieuwe WebSocket-client verbinding maakt
wss.on('connection', ws => {
    console.log("A new client connected to the console.");

    // Gebruik 'pm2' om de logs van de bot te lezen en deze naar de WebSocket-client te sturen
    const logStream = exec('pm2 logs bot --lines 100 --watch');  // Volg de laatste 100 regels van de botlog

    logStream.stdout.on('data', data => {
        ws.send(data.toString());  // Stuur de data naar de WebSocket client
    });

    ws.on('close', () => {
        console.log("Client disconnected from the console.");
        logStream.kill();  // Stop de log stream als de client de verbinding verbreekt
    });
});

// Zorg ervoor dat de WebSocket-server werkt via de express-server
app.server = app.listen(3000, () => {
    console.log('Dashboard is running op http://localhost:3000');
});

// Verbind de WebSocket-server met de HTTP-server
app.server.on('upgrade', (request, socket, head) => {
    wss.handleUpgrade(request, socket, head, (ws) => {
        wss.emit('connection', ws, request);
    });
});
