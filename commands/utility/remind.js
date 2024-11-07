// In commands/utility/remind.js

module.exports = {
    name: 'remind',
    description: 'Zet een herinnering voor jezelf na een bepaalde tijd.',
    async execute(message, args) {
        if (args.length < 2) {
            return message.reply('Gebruik: `!remind [tijd in seconden] [boodschap]`');
        }

        const time = parseInt(args[0]);
        const reminderMessage = args.slice(1).join(' ');

        if (isNaN(time) || time <= 0) {
            return message.reply('Geef een geldig aantal seconden op.');
        }

        message.reply(`Ik zal je over ${time} seconden herinneren aan: "${reminderMessage}"`);

        setTimeout(() => {
            message.reply(`Herinnering: ${reminderMessage}`);
        }, time * 1000);
    }
};
