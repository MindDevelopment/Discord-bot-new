// commands/moderation/kick.js
module.exports = {
    name: 'kick',
    description: 'Kickt een lid van de server',
    async execute(message, args) {
        if (!message.member.permissions.has('KICK_MEMBERS')) {
            return message.reply("Je hebt geen toestemming om leden te kicken!");
        }

        const member = message.mentions.members.first();
        if (!member) return message.reply("Je moet een lid taggen om te kunnen kicken.");
        
        await member.kick().catch(error => message.reply('Er is iets mis gegaan.'));
        message.reply(`${member.user.tag} is gekickt!`);
    }
};
