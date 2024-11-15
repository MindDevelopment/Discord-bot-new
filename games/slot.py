import random
from discord.ext import commands

class SlotGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="slot")
    async def slot(self, ctx):
        symbols = ["🍒", "🍋", "🍊", "🍉", "⭐", "💎"]
        slot_result = [random.choice(symbols) for _ in range(3)]
        result_str = " | ".join(slot_result)
        await ctx.send(f"🎰 | {result_str} | 🎰")
        
        if len(set(slot_result)) == 1:
            await ctx.send(f"🎉 Gefeliciteerd, {ctx.author.mention}! Je hebt gewonnen! 🎉")
        else:
            await ctx.send(f"Helaas, {ctx.author.mention}. Probeer het opnieuw!")

# De setup functie asynchroon maken
async def setup(bot):
    await bot.add_cog(SlotGame(bot))
