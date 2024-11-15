import json
from discord.ext import commands

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Laad de gegevens van gebruikerspunten uit een JSON bestand
    def load_data(self):
        try:
            with open("data/points.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    # Sla de gegevens van gebruikerspunten op in een JSON bestand
    def save_data(self, data):
        with open("data/points.json", "w") as f:
            json.dump(data, f, indent=4)

    # Toon het aantal punten van een gebruiker
    @commands.command(name="balans")
    async def balance(self, ctx):
        data = self.load_data()
        user_id = str(ctx.author.id)
        points = data.get(user_id, 0)
        await ctx.send(f"{ctx.author.mention}, je hebt {points} punten.")

    # Geef punten aan een gebruiker
    @commands.command(name="givepoints")
    async def give_points(self, ctx, member: commands.MemberConverter, points: int):
        if points <= 0:
            await ctx.send("Je kunt geen negatieve of nulpunten geven!")
            return
        
        data = self.load_data()
        user_id = str(member.id)

        if user_id not in data:
            data[user_id] = 0
        
        data[user_id] += points
        self.save_data(data)
        await ctx.send(f"Je hebt {points} punten gegeven aan {member.mention}.")

    # Verdien punten door het spelen van een game
    @commands.command(name="earnpoints")
    async def earn_points(self, ctx):
        points_earned = 10  # Stel het aantal verdiende punten in
        data = self.load_data()
        user_id = str(ctx.author.id)

        if user_id not in data:
            data[user_id] = 0
        
        data[user_id] += points_earned
        self.save_data(data)

        await ctx.send(f"{ctx.author.mention}, je hebt {points_earned} punten verdiend!")

# De setup functie voor deze cog
async def setup(bot):
    await bot.add_cog(Economy(bot))
