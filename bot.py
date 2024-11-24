import discord
from discord.ext import commands
import logging
import os
import json

# Configuratie laden
with open("config/config.json", "r") as config_file:
    config = json.load(config_file)

TOKEN = config["token"]
PREFIX = config["prefix"]
ACTIVITY = config["activity"]

# Bot-intentie instellingen voor server- en berichtbeheer
intents = discord.Intents.default()
intents.message_content = True

# Bot prefix instellen en initialiseren
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Logging instellen (logt naar een bestand)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

@bot.event
async def on_ready():
    logging.info("Bot is ingelogd als %s", bot.user)
    await bot.change_presence(activity=discord.Game(name=ACTIVITY))

    for folder in ["commands", "moderation", "games", "information", "music", "utils", "economy"]:
        for filename in os.listdir(folder):
            if filename.endswith(".py"):
                try:
                    await bot.load_extension(f"{folder}.{filename[:-3]}")
                    logging.info("Succesvol geladen: %s.%s", folder, filename[:-3])
                except Exception as e:
                    logging.error("Fout bij het laden van %s.%s: %s", folder, filename[:-3], e)

bot.run(TOKEN)
