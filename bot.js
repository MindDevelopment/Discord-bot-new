require('dotenv').config(); // Load environment variables from .env
const { Client, GatewayIntentBits, EmbedBuilder, ActionRowBuilder, StringSelectMenuBuilder } = require('discord.js');  // Voeg EmbedBuilder hier toe
const fs = require('fs');
const path = require('path');
const config = require('./config.json'); // Zorg ervoor dat dit bestand bestaat

// Maak een nieuwe Discord Client aan met de benodigde intents
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
        GatewayIntentBits.GuildMembers,
        GatewayIntentBits.GuildMessageReactions
    ]
});

// Laad alle command bestanden uit alle submappen in de 'commands' map
client.commands = new Map();
const commandFolders = fs.readdirSync(path.join(__dirname, 'commands'));  // Lees alle submappen (fun, info, etc.)

commandFolders.forEach(folder => {
    const commandFiles = fs.readdirSync(path.join(__dirname, 'commands', folder)).filter(file => file.endsWith('.js'));

    commandFiles.forEach(file => {
        const command = require(path.join(__dirname, 'commands', folder, file));
        client.commands.set(command.name, command);
    });
});

// Event: Wanneer de bot online gaat
client.once('ready', () => {
    console.log('Bot is online!');
});

// Event: Wanneer een bericht wordt ontvangen
client.on('messageCreate', message => {
    // Zorg ervoor dat de bot niet reageert op zijn eigen berichten
    if (message.author.bot) return;

    // Zorg ervoor dat je prefix correct instelt
    const prefix = '!';

    // Controleer of het bericht een commando is
    if (message.content.startsWith(prefix)) {
        const args = message.content.slice(prefix.length).trim().split(/ +/);
        const commandName = args.shift().toLowerCase();

        // Controleer of het commando bestaat
        if (client.commands.has(commandName)) {
            const command = client.commands.get(commandName);
            command.execute(message, args);  // Voer het commando uit
        }
    }
});

// Event: Wanneer een gebruiker interactie heeft met de dropdown (Hoofd Categorieën)
client.on('interactionCreate', async (interaction) => {
    if (!interaction.isStringSelectMenu()) return;

    const category = interaction.values[0];

    // Maak een embed voor de lijst van commando's in de gekozen categorie
    const commandEmbed = new EmbedBuilder()
        .setColor('#0099ff')
        .setTitle(`**Beschikbare commando's in de categorie ${category}:**`)
        .setTimestamp()
        .setFooter({ text: 'Help Command' });

    const commandFolderPath = path.join(__dirname, 'commands', category);
    let commandList = '';

    if (fs.existsSync(commandFolderPath)) {
        const commandFiles = fs.readdirSync(commandFolderPath).filter(file => file.endsWith('.js'));

        commandFiles.forEach(file => {
            const command = require(path.join(commandFolderPath, file));
            commandList += `\`!${command.name}\` - ${command.description}\n`;
        });

        commandEmbed.setDescription(commandList);
    } else {
        commandEmbed.setDescription(`Er zijn geen commando's gevonden in de categorie **${category}**.`);
    }

    // Maak een nieuwe ActionRow met de hoofd-categorieën voor het dropdownmenu
    const mainCategoryRow = new ActionRowBuilder()
        .addComponents(
            new StringSelectMenuBuilder()
                .setCustomId('help_select')
                .setPlaceholder('Kies een andere categorie...')
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
                    {
                        label: 'owner',
                        value: 'owner',
                        description: 'Bekijk owner commando\'s.',
                    },
                ]),
        );

    // Werk de interactie bij met de embed en de nieuwe dropdown met de hoofd-categorieën
    await interaction.update({
        embeds: [commandEmbed],
        components: [mainCategoryRow], // Voeg de nieuwe dropdown met hoofd-categorieën toe
    });
});

// Event: Wanneer een gebruiker interactie heeft met de subcategorie dropdown
client.on('interactionCreate', async (interaction) => {
    if (!interaction.isStringSelectMenu()) return;

    // Als de subcategorie is geselecteerd
    if (interaction.customId === 'sub_category_select') {
        const subCategory = interaction.values[0];

        // Maak een embed voor de subcategorie lijst
        const subCategoryEmbed = new EmbedBuilder()
            .setColor('#0099ff')
            .setTitle(`**Beschikbare commando's in de subcategorie ${subCategory}:**`)
            .setTimestamp()
            .setFooter({ text: 'Help Command' });

        // Hier zou je de commando's van de subcategorie kunnen laden, afhankelijk van je mapstructuur
        const subCategoryPath = path.join(__dirname, 'commands', 'fun', subCategory);
        let subCategoryList = '';

        if (fs.existsSync(subCategoryPath)) {
            const commandFiles = fs.readdirSync(subCategoryPath).filter(file => file.endsWith('.js'));

            commandFiles.forEach(file => {
                const command = require(path.join(subCategoryPath, file));
                subCategoryList += `\`!${command.name}\` - ${command.description}\n`;
            });

            subCategoryEmbed.setDescription(subCategoryList);
        } else {
            subCategoryEmbed.setDescription(`Er zijn geen commando's gevonden in de subcategorie **${subCategory}**.`);
        }

        // Stuur de subcategorie embed
        await interaction.update({
            embeds: [subCategoryEmbed],
            components: [], // Verwijder de subcategorie dropdown na selectie
        });
    }
});

const { sendLogToChannel } = require('./scripts/logging');

// listeners voor logs
const { logJoinLeave, logMessage, logModAction } = require('./scripts/logging');

client.on('guildMemberAdd', member => {
    const channel = member.guild.channels.cache.find(c => c.name === 'join-leave');
    if (channel) logJoinLeave(channel, member, 'joined');
});

client.on('guildMemberRemove', member => {
    const channel = member.guild.channels.cache.find(c => c.name === 'join-leave');
    if (channel) logJoinLeave(channel, member, 'left');
});

client.on('messageDelete', message => {
    const channel = message.guild.channels.cache.find(c => c.name === 'messages');
    if (channel && message.partial === false) {
        logMessage(channel, message, message);
    }
});

client.on('messageUpdate', (oldMessage, newMessage) => {
    const channel = oldMessage.guild.channels.cache.find(c => c.name === 'messages');
    if (channel) logMessage(channel, oldMessage, newMessage);
});

client.on('voiceStateUpdate', (oldState, newState) => {
    const channel = newState.guild.channels.cache.find(c => c.name === 'voicecall');
    if (channel) {
        if (oldState.channelId !== newState.channelId) {
            logModAction(channel, `${newState.member.user.tag} verliet de voice call: ${oldState.channel?.name ?? 'N/A'} en is nu in: ${newState.channel?.name ?? 'N/A'}`);
        }
    }
});

// Login de bot met de token uit config.json
client.login(process.env.DISCORD_TOKEN);
