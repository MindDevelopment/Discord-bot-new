const { EmbedBuilder, PermissionsBitField } = require('discord.js');

module.exports = {
    async createLogChannels(guild, categoryId) {
        try {
            // Haal de categorie op
            const category = await guild.channels.fetch(categoryId);
            if (!category || category.type !== 'GUILD_CATEGORY') {
                throw new Error('De opgegeven categorie bestaat niet of is geen categorie.');
            }

            console.log('Categorie gevonden:', category);
            console.log('Categorie type:', category.type);  // Verwacht 'GUILD_CATEGORY'

            // Maak de logkanalen aan
            const channels = await Promise.all([
                guild.channels.create({
                    name: 'join-leave',
                    type: 0,  // GUILD_TEXT als numerieke waarde
                    parent: category,
                }),
                guild.channels.create({
                    name: 'messages',
                    type: 0,  // GUILD_TEXT als numerieke waarde
                    parent: category,
                }),
                guild.channels.create({
                    name: 'voicecall',
                    type: 0,  // GUILD_TEXT als numerieke waarde
                    parent: category,
                }),
                guild.channels.create({
                    name: 'mod-acties',
                    type: 0,  // GUILD_TEXT als numerieke waarde
                    parent: category,
                }),
            ]);

            // Set permissies voor de bot om berichten te sturen
            channels.forEach(channel => {
                channel.permissionOverwrites.create(guild.roles.everyone, {
                    SendMessages: false,
                });
                channel.permissionOverwrites.create(guild.me, {
                    SendMessages: true,
                });
            });

            return channels;
        } catch (err) {
            console.error('Fout bij het maken van logkanalen:', err);
            throw err;  // Gooi de fout opnieuw om het in logs.js op te vangen
        }
    },

    async logJoinLeave(channel, member, action) {
        const embed = new EmbedBuilder()
            .setColor(action === 'joined' ? 'GREEN' : 'RED')
            .setTitle(`${member.user.tag} heeft de server ${action === 'joined' ? 'gejoined' : 'verlaten'}`)
            .setThumbnail(member.user.displayAvatarURL())
            .setTimestamp();

        await channel.send({ embeds: [embed] });
    },

    async logMessage(channel, oldMessage, newMessage) {
        const embed = new EmbedBuilder()
            .setColor('YELLOW')
            .setTitle('Bericht Gewijzigd')
            .setDescription(`**Origineel bericht**:\n${oldMessage.content}\n\n**Aangepast bericht**:\n${newMessage.content}`)
            .setTimestamp();

        await channel.send({ embeds: [embed] });
    },

    async logModAction(channel, actionDetails) {
        const embed = new EmbedBuilder()
            .setColor('ORANGE')
            .setTitle('Moderatie Actie')
            .setDescription(actionDetails)
            .setTimestamp();

        await channel.send({ embeds: [embed] });
    },
};
