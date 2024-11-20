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
intents.message_content = True  # Nodig voor berichtinhoud

# Bot prefix instellen en initialiseren
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Logging instellen (logt naar de console en naar SocketIO)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Maak een SocketIOHandler aan voor logging
from app import socketio
class SocketIOHandler(logging.Handler):
    def emit(self, record):
        log_message = self.format(record)
        socketio.emit('console_update', log_message)  # Zend log naar de frontend

# Voeg de SocketIOHandler toe aan de rootlogger
socketio_handler = SocketIOHandler()
socketio_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
socketio_handler.setFormatter(formatter)
logging.getLogger().addHandler(socketio_handler)

# Bot is gereed en online
@bot.event
async def on_ready():
    logging.info("Bot is ingelogd als %s", bot.user)
    print(f"Bot is ingelogd als {bot.user}")
    await bot.change_presence(activity=discord.Game(name=ACTIVITY))

    # Laad de cogs na het opstarten
    for folder in ["commands", "moderation", "games", "information", "music", "utils", "economy"]:
        for filename in os.listdir(folder):
            if filename.endswith(".py"):
                try:
                    await bot.load_extension(f"{folder}.{filename[:-3]}")
                    logging.info("Succesvol geladen: %s.%s", folder, filename[:-3])
                except Exception as e:
                    logging.error("Fout bij het laden van %s.%s: %s", folder, filename[:-3], e)

@bot.command(name="bothelp")
async def bothelp(ctx):
    help_text = """
    **Beschikbare commando's:**
    - !slot: Speel het slotspel
    - !bothelp: Toon dit help-bericht
    """
    await ctx.send(help_text)

# Voeg de economy extensie toe
from economy.economy import Economy
bot.load_extension("economy.economy")

# Bot starten
bot.run(TOKEN)
