const express = require('express');
const session = require('express-session');
const passport = require('passport');
const DiscordStrategy = require('passport-discord').Strategy;

const app = express();
const PORT = 3000;

// Sessies en Passport instellen voor login
passport.use(new DiscordStrategy({
    clientID: 'YOUR_DISCORD_CLIENT_ID',
    clientSecret: 'YOUR_DISCORD_CLIENT_SECRET',
    callbackURL: 'http://localhost:3000/login/callback',
    scope: ['identify', 'guilds']
}, (accessToken, refreshToken, profile, done) => {
    return done(null, profile);
}));

passport.serializeUser((user, done) => {
    done(null, user);
});

passport.deserializeUser((user, done) => {
    done(null, user);
});

// Middleware voor sessie
app.use(session({
    secret: 'SESSION_SECRET',
    resave: false,
    saveUninitialized: false
}));

app.use(passport.initialize());
app.use(passport.session());

// Basisroute voor homepage
app.get('/', (req, res) => {
    res.render('index');  // Dit verwijst naar 'views/index.ejs'
});

// Login route
app.get('/login', (req, res) => {
    res.redirect('/auth/discord');
});

// Login callback
app.get('/login/callback', passport.authenticate('discord', {
    failureRedirect: '/login'
}), (req, res) => {
    res.redirect('/dashboard');
});

// Dashboard route na inloggen
app.get('/dashboard', (req, res) => {
    if (!req.isAuthenticated()) {
        return res.redirect('/login');
    }
    res.render('dashboard', { user: req.user });  // Toon dashboard na login
});

// Start de server
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
