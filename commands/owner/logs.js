const { EmbedBuilder, PermissionsBitField, ActionRowBuilder, StringSelectMenuBuilder } = require('discord.js');

module.exports = {
    name: 'logs',
    description: 'Helpt je Discord server beter te loggen',

    async execute(interaction) {
        // Maak een embed voor de selectie
        const embed = new EmbedBuilder()
            .setColor(0x0000FF) // Of gebruik een hex-code
            .setTitle('Kies het logtype')
            .setDescription('Selecteer het logtype dat je wilt instellen:');

        // Maak een drop-down menu
        const row = new ActionRowBuilder().addComponents(
            new StringSelectMenuBuilder()
                .setCustomId('log_type_select')
                .setPlaceholder('Selecteer het logtype')
                .addOptions([
                    {
                        label: 'Join/Leave Log',
                        value: 'join_leave',
                        description: 'Log de join/leave activiteiten',
                    },
                    {
                        label: 'Bericht Log',
                        value: 'message_log',
                        description: 'Log bericht wijzigingen',
                    },
                    {
                        label: 'Voicecall Log',
                        value: 'voicecall_log',
                        description: 'Log voicecall activiteiten',
                    },
                    {
                        label: 'Moderatie Log',
                        value: 'mod_log',
                        description: 'Log moderatie acties',
                    },
                ])
        );

        // Stuur de embed met het menu
        await interaction.reply({ embeds: [embed], components: [row] });

        // Wacht op selectie door de gebruiker
        const filter = i => i.user.id === interaction.user.id;
        const collector = interaction.channel.createMessageComponentCollector({ filter, time: 15000 });

        collector.on('collect', async i => {
            if (i.customId === 'log_type_select') {
                const logType = i.values[0];

                // Vraag de gebruiker om een kanaal ID in te voeren
                await i.update({ content: `Je hebt gekozen voor ${logType}. Voer nu de kanaal ID in waar je de logs wilt opslaan.`, components: [] });

                const responseFilter = m => m.author.id === interaction.user.id;
                const responseCollector = interaction.channel.createMessageCollector({ filter: responseFilter, time: 60000 });

                responseCollector.on('collect', async message => {
                    const channelId = message.content.trim();
                    const logChannel = await interaction.guild.channels.fetch(channelId);

                    if (!logChannel || logChannel.type !== 'GUILD_TEXT') {
                        return message.reply('Het opgegeven kanaal bestaat niet of is geen geldig tekstkanaal.');
                    }

                    // Maak het logkanaal aan op basis van het type en zorg ervoor dat het binnen de juiste categorie wordt geplaatst
                    const category = logChannel.parentId; // Haal de categorie van het opgegeven kanaal
                    await interaction.guild.channels.create({
                        name: `${logType}-${logChannel.name}`,
                        type: 0, // GUILD_TEXT
                        parent: category, // Plaats het nieuwe kanaal in dezelfde categorie
                    });

                    message.reply(`${logType} logkanaal succesvol ingesteld in ${logChannel.name}.`);
                    responseCollector.stop();
                });
            }
        });

        collector.on('end', collected => {
            if (collected.size === 0) {
                interaction.editReply({ content: 'Tijd om een logtype te kiezen is verstreken.', components: [] });
            }
        });
    },
};
