module.exports = {
    name: 'ping',  // De naam van het commando
    description: 'Reageer met Pong! om de botstatus te controleren',  // Omschrijving van het commando
    execute(message, args) {
        message.channel.send('Pong!');  // Het antwoord dat de bot terugstuurt
    },
};
