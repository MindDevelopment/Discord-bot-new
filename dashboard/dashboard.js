// Importeer de benodigde modules
const express = require('express');
const { exec } = require('child_process');
const router = express.Router();
const client = require('../index'); // Zorg ervoor dat je toegang hebt tot je bot client

// Route om de bot te stoppen
router.post('/stop', (req, res) => {
    client.destroy() // Stop de bot
        .then(() => {
            console.log("Bot is stopped");
            res.send("Bot is stopped.");
        })
        .catch(error => {
            console.error("Error stopping the bot:", error);
            res.status(500).send("Er is iets mis gegaan met het stoppen van de bot.");
        });
});

// Route om de bot te herstarten
router.post('/restart', (req, res) => {
    exec('pm2 restart bot', (error, stdout, stderr) => {
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

// Route om de bot te starten
router.post('/start', (req, res) => {
    exec('pm2 start bot', (error, stdout, stderr) => {
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

module.exports = router;
