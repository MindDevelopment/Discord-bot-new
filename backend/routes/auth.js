// routes/auth.js
const express = require('express');
const axios = require('axios');
const router = express.Router();

router.get('/login', (req, res) => {
    const redirectUri = `https://discord.com/api/oauth2/authorize?client_id=${process.env.CLIENT_ID}&redirect_uri=${process.env.REDIRECT_URI}&response_type=code&scope=identify%20guilds`;
    res.redirect(redirectUri);
});

router.get('/callback', async (req, res) => {
    const code = req.query.code;
    if (!code) return res.send("Geen code ontvangen");

    try {
        // Verkrijg de toegangstoken van Discord
        const tokenData = await axios.post('https://discord.com/api/oauth2/token', new URLSearchParams({
            client_id: process.env.CLIENT_ID,
            client_secret: process.env.CLIENT_SECRET,
            grant_type: 'authorization_code',
            code,
            redirect_uri: process.env.REDIRECT_URI
        }), {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });

        // Sla de toegangstoken op in de sessie
        req.session.access_token = tokenData.data.access_token;
        res.redirect('/dashboard'); // Doorsturen naar het dashboard
    } catch (err) {
        console.error('Error bij OAuth2-token:', err);
        res.send("OAuth2 mislukt.");
    }
});

module.exports = router;
