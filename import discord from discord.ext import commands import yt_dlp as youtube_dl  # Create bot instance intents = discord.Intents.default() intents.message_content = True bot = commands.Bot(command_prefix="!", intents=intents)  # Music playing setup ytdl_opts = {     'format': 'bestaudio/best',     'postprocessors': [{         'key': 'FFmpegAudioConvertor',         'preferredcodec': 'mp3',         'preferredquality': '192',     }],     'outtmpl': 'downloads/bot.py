import discord
from discord.ext import commands
import yt_dlp as youtube_dl

# Create bot instance
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Music playing setup
ytdl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegAudioConvertor',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'downloads/%(id)s.%(ext)s',
}

ffmpeg_opts = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

# Music commands
@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send("You must join a voice channel first!")
        return
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def play(ctx, url: str):
    ydl_opts['outtmpl'] = f'{ctx.guild.id}.%(ext)s'

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice = ctx.voice_client

        if not voice.is_playing():
            voice.play(discord.FFmpegPCMAudio(url2, **ffmpeg_opts))
            await ctx.send(f"Now playing: {info['title']}")
        else:
            await ctx.send("A song is already playing.")

@bot.command()
async def pause(ctx):
    ctx.voice_client.pause()
    await ctx.send("Paused the music.")

@bot.command()
async def resume(ctx):
    ctx.voice_client.resume()
    await ctx.send("Resumed the music.")

@bot.command()
async def stop(ctx):
    ctx.voice_client.stop()
    await ctx.send("Stopped the music.")

# Run the bot
bot.run('YOUR_BOT_TOKEN')
