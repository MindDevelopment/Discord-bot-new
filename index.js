const express = require('express');
const session = require('express-session');
const path = require('path');
const app = express();

// Stel de sessie in
app.use(session({
    secret: 'jouw_geheime_willekeurige_string',  // Vervang dit door een veilige, willekeurige string
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false }  // Zet secure op true in een HTTPS-omgeving
}));

// Stel de view engine in voor ejs
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Stel de public folder in
app.use(express.static(path.join(__dirname, 'public')));

// Stel de body parser in voor JSON en URL-encoded formuliervelden
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Homepage route
app.get('/', (req, res) => {
    res.render('index', { user: req.session.user });
});

// Login route
app.get('/login', (req, res) => {
    res.render('login');
});

app.listen(3000, () => {
    console.log('Server draait op http://localhost:3000');
});
