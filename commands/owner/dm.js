module.exports = {
    name: 'dm',
    description: 'Stuurt een DM naar een specifieke gebruiker met een bericht.',
    
    async execute(message, args) {
        // Zorg ervoor dat de gebruiker een ID opgeeft en een bericht
        const userId = args[0];  // De eerste argument moet de gebruikers-ID zijn
        const messageContent = args.slice(1).join(' '); // Het bericht dat gestuurd wordt naar de gebruiker

        if (!userId || !messageContent) {
            return message.reply('Geef zowel een gebruikers-ID als een bericht op.');
        }

        try {
            // Haal de gebruiker op via hun ID
            const user = await message.client.users.fetch(userId);
            
            // Stuur het bericht naar de gebruiker via een DM
            await user.send(messageContent);
            
            return message.reply('Bericht is succesvol verstuurd naar de gebruiker!');
        } catch (error) {
            console.error(error);
            return message.reply('Er is een fout opgetreden bij het versturen van de DM.');
        }
    },
};
