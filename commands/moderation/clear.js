module.exports = {
    name: 'clear',
    description: 'Verwijdert een opgegeven aantal berichten.',
    
    async execute(message, args) {
        // De rol ID die de permissie heeft
        const requiredRoleId = '1298706029781192755';

        // Haal de rol van de gebruiker op
        const memberRole = message.member.roles.cache;

        // Controleer of de gebruiker een rol heeft die gelijk of hoger is dan de vereiste rol
        const userHasPermission = memberRole.some(role => role.id === requiredRoleId || message.guild.roles.cache.get(role.id).position > message.guild.roles.cache.get(requiredRoleId).position);

        if (!userHasPermission) {
            return message.reply({
                content: 'Je hebt niet de juiste rol om dit commando te gebruiken!',
            });
        }

        // Controleer of er een aantal berichten is opgegeven
        const aantal = parseInt(args[0], 10);
        if (isNaN(aantal) || aantal < 1 || aantal > 100) {
            return message.reply({
                content: 'Geef een geldig aantal berichten op (tussen de 1 en 100).',
            });
        }

        // Haal de berichten op die verwijderd moeten worden
        try {
            const messages = await message.channel.messages.fetch({ limit: aantal + 1 }); // Haal het aantal berichten op (plus 1 om het commando-bericht ook mee te nemen)
            await message.channel.bulkDelete(messages);

            return message.reply({
                content: `${aantal} berichten zijn verwijderd!`,
            });
        } catch (error) {
            console.error(error);
            return message.reply({
                content: 'Er is een fout opgetreden bij het verwijderen van berichten.',
            });
        }
    },
};
