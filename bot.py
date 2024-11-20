import discord
from discord.ext import commands
import os
import json
import logging

# Configuratie laden
with open("config/config.json", "r") as config_file:
    config = json.load(config_file)

TOKEN = config["token"]
PREFIX = config["prefix"]
ACTIVITY = config["activity"]

# Logging instellen
logging.basicConfig(
    filename="bot.log", 
    filemode="a", 
    format="%(asctime)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)

# Bot-intentie instellingen voor server- en berichtbeheer
intents = discord.Intents.default()
intents.message_content = True  # Nodig voor berichtinhoud

# Bot prefix instellen en initialiseren
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Log elke gebeurtenis (gebruikerscommando's)
@bot.event
async def on_command(ctx):
    logging.info(f"Commando uitgevoerd: {ctx.command} door {ctx.author} in {ctx.guild.name}")
    print(f"Commando uitgevoerd: {ctx.command} door {ctx.author} in {ctx.guild.name}")

# Log elke fout die optreedt tijdens de uitvoering van een commando
@bot.event
async def on_command_error(ctx, error):
    logging.error(f"Fout bij het uitvoeren van commando {ctx.command}: {error}")
    print(f"Fout bij het uitvoeren van commando {ctx.command}: {error}")

# Log wanneer de bot succesvol inlogt
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

# Commando's laden vanuit mappen zoals moderation, games, etc.
@bot.command(name="bothelp")
async def bothelp(ctx):
    help_text = """
    **Beschikbare commando's:**
    - !slot: Speel het slotspel
    - !bothelp: Toon dit help-bericht
    """
    await ctx.send(help_text)
    logging.info("Help commando uitgevoerd door %s in %s", ctx.author, ctx.guild.name)

# Voeg de economy extensie toe
from economy.economy import Economy
bot.load_extension("economy.economy")

# Bot starten
bot.run(TOKEN)
