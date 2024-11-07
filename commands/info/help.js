const { ActionRowBuilder, StringSelectMenuBuilder, EmbedBuilder } = require('discord.js');
const fs = require('fs');
const path = require('path');

module.exports = {
    name: 'help',
    description: 'Toont de lijst met beschikbare commando\'s en categorieën',

    async execute(message, args) {
        // Laad de submappen in de hoofdmap 'commands'
        const commandFolders = fs.readdirSync(path.join(__dirname, '..', '..', 'commands')); 

        // Maak een lijst van opties voor de dropdown, gebaseerd op de mappen in 'commands'
        const categories = commandFolders.map(folder => ({
            label: folder.charAt(0).toUpperCase() + folder.slice(1),
            value: folder,
            description: `Bekijk de commando's in de ${folder} categorie.`,
        }));

        // Embed bericht
        const helpMessage = new EmbedBuilder()
            .setColor('#0099ff')
            .setTitle('Bot Help Menu')
            .setDescription('Gebruik de dropdown hieronder om een categorie van commando\'s te bekijken.');

        // Maak de eerste dropdown met de beschikbare categorieën
        const row = new ActionRowBuilder()
            .addComponents(
                new StringSelectMenuBuilder()
                    .setCustomId('help_select')
                    .setPlaceholder('Kies een categorie...')
                    .addOptions(categories)
            );

        // Stuur het bericht met de embed en de dropdown
        await message.reply({ embeds: [helpMessage], components: [row] });
    },
};
