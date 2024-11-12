const express = require('express');
const session = require('express-session');
const passport = require('passport');
const path = require('path');
const { Client } = require('discord.js');
const app = express();

// Gebruik ejs als view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Bodyparser middleware
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Sessies voor gebruikersauthenticatie
app.use(session({
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false
}));

// Initialiseer Passport
app.use(passport.initialize());
app.use(passport.session());

// Root route
app.get('/', (req, res) => {
    if (req.isAuthenticated()) {
        res.render('dashboard', { user: req.user });
    } else {
        res.render('index');
    }
});

// Login route
app.get('/login', (req, res) => {
    res.render('login');
});

// Logout route
app.get('/logout', (req, res) => {
    req.logout(err => {
        if (err) {
            return next(err);
        }
        res.redirect('/');
    });
});

// Start de server
const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`Server draait op http://localhost:${port}`);
});
