// routes/auth.js
const express = require('express');
const router = express.Router();

router.get('/login', (req, res) => {
    const redirectUri = `https://discord.com/api/oauth2/authorize?client_id=${process.env.CLIENT_ID}&redirect_uri=${process.env.REDIRECT_URI}&response_type=code&scope=identify%20guilds`;
    res.redirect(redirectUri);
});

module.exports = router;

router.get('/callback', async (req, res) => {
    const code = req.query.code;
    if (!code) return res.send("Geen code ontvangen");

    try {
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

        req.session.access_token = tokenData.data.access_token;
        res.redirect('/dashboard'); // Doorsturen naar het dashboard
    } catch (err) {
        console.error('Error bij OAuth2-token:', err);
        res.send("OAuth2 mislukt.");
    }
});

const axios = require('axios');

router.get('/dashboard', async (req, res) => {
    if (!req.session.access_token) return res.redirect('/login');

    try {
        const userData = await axios.get('https://discord.com/api/users/@me', {
            headers: {
                Authorization: `Bearer ${req.session.access_token}`
            }
        });

        res.render('dashboard', { user: userData.data });
    } catch (err) {
        console.error("Error bij ophalen gebruiker:", err);
        res.redirect('/login');
    }
});

