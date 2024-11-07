const { ActionRowBuilder, StringSelectMenuBuilder, EmbedBuilder } = require('discord.js');  // Zorg ervoor dat je de juiste imports hebt
const fs = require('fs');
const path = require('path');

module.exports = {
    name: 'help',
    description: 'Toont de lijst met beschikbare commando\'s en categorieën',

    async execute(message, args) {
        // Informatie over de bot
        const helpMessage = `**Bot Help Menu**\nGebruik de dropdown hieronder om een categorie van commando's te bekijken.`;

        // Maak de eerste dropdown met hoofd categorieën
        const row = new ActionRowBuilder()
            .addComponents(
                new StringSelectMenuBuilder()
                    .setCustomId('help_select')
                    .setPlaceholder('Kies een categorie...')
                    .addOptions([
                        {
                            label: 'Fun',
                            value: 'fun',
                            description: 'Bekijk leuke commando\'s.',
                        },
                        {
                            label: 'Info',
                            value: 'info',
                            description: 'Bekijk informatie commando\'s.',
                        },
                        {
                            label: 'Moderation',
                            value: 'moderation',
                            description: 'Bekijk moderatie commando\'s.',
                        },
                        {
                            label: 'Utility',
                            value: 'utility',
                            description: 'Bekijk utility commando\'s.',
                        },
                    ]),
            );

        // Stuur het bericht met de dropdown
        await message.reply({ content: helpMessage, components: [row] });
    },
};
