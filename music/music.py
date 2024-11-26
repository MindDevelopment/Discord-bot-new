import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None

    @commands.command(name='play')
    async def play(self, ctx, *, url: str):
        """Speelt muziek af vanuit een opgegeven YouTube URL."""
        voice_channel = ctx.author.voice.channel
        if not voice_channel:
            await ctx.send("Je moet in een voice channel zitten om muziek af te spelen.")
            return

        try:
            # Verbinden met het voice kanaal
            self.voice_client = await voice_channel.connect()

            # Haal de audio op van YouTube
            with YoutubeDL({'format': 'bestaudio/best', 'postprocessors': [{
                'key': 'FFmpegAudioConvertor',
                'preferredcodec': 'mp3',
                'preferredquality': '192'}]}) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(url2)

            # Speel de audio af
            self.voice_client.play(source)
            await ctx.send(f"Speel nu: {info['title']}")
            print(f"Spelen: {info['title']}")

        except Exception as e:
            await ctx.send(f"Er is een fout opgetreden: {e}")
            print(f"Fout bij het afspelen: {e}")

    @commands.command(name='stop')
    async def stop(self, ctx):
        """Stop met muziek afspelen en verlaat het kanaal."""
        if self.voice_client.is_playing():
            self.voice_client.stop()
            await ctx.send("De muziek is gestopt.")
        if self.voice_client.is_connected():
            await self.voice_client.disconnect()

    @commands.command(name='pause')
    async def pause(self, ctx):
        """Pauzeer de muziek."""
        if self.voice_client.is_playing():
            self.voice_client.pause()
            await ctx.send("De muziek is gepauzeerd.")
        else:
            await ctx.send("Er wordt momenteel geen muziek afgespeeld.")

    @commands.command(name='resume')
    async def resume(self, ctx):
        """Hervat de muziek."""
        if self.voice_client.is_paused():
            self.voice_client.resume()
            await ctx.send("De muziek is hervat.")
        else:
            await ctx.send("De muziek is niet gepauzeerd.")

    @commands.command(name='skip')
    async def skip(self, ctx):
        """Sla het huidige nummer over."""
        if self.voice_client.is_playing():
            self.voice_client.stop()
            await ctx.send("Het nummer is overgeslagen.")
        else:
            await ctx.send("Er wordt momenteel geen muziek afgespeeld.")

def setup(bot):
    bot.add_cog(Music(bot))
