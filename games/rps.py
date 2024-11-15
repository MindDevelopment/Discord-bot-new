import discord
from discord.ext import commands
import random
from economy.economy import Economy  # Zorg ervoor dat je de juiste import hebt voor de economy module

class RPSGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rps(self, ctx, choice: str, bet: int):
        """Speel een steen-papier-schaar spel met een inzet."""
        choices = ['steen', 'papier', 'schaar']
        
        if choice not in choices:
            await ctx.send("Kies tussen 'steen', 'papier' of 'schaar'.")
            return
        
        # Haal de gebruiker zijn huidige saldo op (bijvoorbeeld uit de economy module)
        economy = Economy(ctx.guild)
        balance = await economy.get_balance(ctx.author.id)

        if balance < bet:
            await ctx.send("Je hebt niet genoeg punten om te wedden.")
            return

        # Genereer een willekeurige keuze voor de bot
        bot_choice = random.choice(choices)
        
        # Bepaal de winnaar
        if choice == bot_choice:
            result = "Het is gelijk!"
        elif (choice == "steen" and bot_choice == "schaar") or \
             (choice == "papier" and bot_choice == "steen") or \
             (choice == "schaar" and bot_choice == "papier"):
            result = "Jij wint!"
            # Verhoog de punten
            await economy.update_balance(ctx.author.id, bet)
        else:
            result = "Je verliest!"
            # Verlies de punten
            await economy.update_balance(ctx.author.id, -bet)
        
        await ctx.send(f"Jij koos {choice}, ik koos {bot_choice}. {result}")

# Voeg de cog toe aan de bot (let op: zonder await)
def setup(bot):
    bot.add_cog(RPSGame(bot))
