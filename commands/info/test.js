// test.js - Een test commando om te controleren of de bot werkt
module.exports = {
    name: 'test',  // Het commando wat de gebruiker moet invoeren
    description: 'Dit is een test commando om te checken of de bot werkt.',

    execute(message, args) {
        message.channel.send('De bot is succesvol online en werkt!');
    }
};
