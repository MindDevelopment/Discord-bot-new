// index.js

// Importeer de benodigde pakketten
const { Client, GatewayIntentBits } = require('discord.js');
const express = require('express');
const path = require('path');
const http = require('http');
const socketIo = require('socket.io');

// Importeer je bot code
const bot = require('./bot.js'); // Zorg ervoor dat dit bestand je botlogica bevat

// Maak een nieuwe Discord client aan
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

// Voeg de bot token toe
const DISCORD_TOKEN = process.env.DISCORD_TOKEN;

// Bot inloggen
client.login(DISCORD_TOKEN);

// Maak een express server voor het dashboard
const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// Stel statische bestanden in voor het dashboard (je dashboard-bestanden)
app.use(express.static(path.join(__dirname, 'dashboard/public')));

// Stel een route in om toegang te krijgen tot de dashboardpagina
// Pas het pad naar je index.html bestand aan
app.get('/', (req, res) => {
  res.sendFile(path.join('D:', 'Github', 'Discord-bot-new', 'dashboard', 'src', 'pages', 'api', 'auth', 'index.html'));
});

// Stel een route in voor socket.io communicatie (als dat nodig is)
io.on('connection', (socket) => {
  console.log('Een gebruiker is verbonden');
  
  socket.on('disconnect', () => {
    console.log('Een gebruiker is verbroken');
  });
});

// Start de webserver (bijvoorbeeld op poort 3000)
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Dashboard draait op http://localhost:${PORT}`);
});

// Bot event: bot is online
client.once('ready', () => {
  console.log(`Bot is ingelogd als ${client.user.tag}`);
});
