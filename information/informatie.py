import discord
from discord.ext import commands
import psutil
import datetime
import logging
import platform

# Informatie command
class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info")
    async def info(self, ctx):
        # Systeem informatie ophalen
        uptime = self.get_uptime()
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        bot_version = "1.0.0"  # Dit kan een versiebestand zijn

        # Bot-informatie in een bericht weergeven
        embed = discord.Embed(title="Bot Informatie", color=0x00ff00)
        embed.add_field(name="Bot versie", value=bot_version, inline=True)
        embed.add_field(name="CPU gebruik", value=f"{cpu_usage}%", inline=True)
        embed.add_field(name="Geheugen gebruik", value=f"{memory_usage}%", inline=True)
        embed.add_field(name="Uptime", value=uptime, inline=True)
        embed.add_field(name="Platform", value=platform.system(), inline=True)
        embed.add_field(name="Bot draait op", value=platform.machine(), inline=True)
        await ctx.send(embed=embed)

    def get_uptime(self):
        # Uptime berekenen van de bot
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.datetime.now() - boot_time
        return str(uptime).split('.')[0]  # Uptime als "X dagen, X uren, etc."


def setup(bot):
    bot.add_cog(Info(bot))
