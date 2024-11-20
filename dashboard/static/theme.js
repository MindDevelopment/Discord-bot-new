document.addEventListener('DOMContentLoaded', function() {
    // Laad de opgeslagen modus bij het laden van de pagina
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
        document.body.classList.remove('light-mode');
        document.getElementById('theme-switch').checked = true;
    } else {
        document.body.classList.add('light-mode');
        document.body.classList.remove('dark-mode');
    }

    // Luister naar veranderingen van de schakelaar
    document.getElementById('theme-switch').addEventListener('change', function() {
        if (this.checked) {
            document.body.classList.add('dark-mode');
            document.body.classList.remove('light-mode');
            localStorage.setItem('theme', 'dark');  // Bewaar de keuze
        } else {
            document.body.classList.add('light-mode');
            document.body.classList.remove('dark-mode');
            localStorage.setItem('theme', 'light');  // Bewaar de keuze
        }
    });
});