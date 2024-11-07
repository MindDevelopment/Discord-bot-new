module.exports = {
    name: 'spam',
    description: 'Spamt 50 berichten in één keer, alleen voor geautoriseerde gebruikers.',
    
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

        // Spam 50 berichten
        try {
            for (let i = 0; i < 10; i++) {
                await message.channel.send(`Dit is spambericht #${i + 1}`);
            }
            return message.reply({
                content: '50 berichten zijn succesvol gespamd!',
            });
        } catch (error) {
            console.error(error);
            return message.reply({
                content: 'Er is een fout opgetreden bij het spammen van berichten.',
            });
        }
    },
};
