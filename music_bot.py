import discord
from discord.ext import commands
import yt_dlp
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ytdlp_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
}

ffmpeg_opts = {
    'options': '-vn'
}

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        await ctx.send("🎧 Joined voice channel")
    else:
        await ctx.send("❌ You must join a voice channel first")

@bot.command()
async def play(ctx, *, url):
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()

    vc = ctx.voice_client

    with yt_dlp.YoutubeDL(ytdlp_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']
        title = info.get('title', 'Unknown')

    vc.stop()
    vc.play(discord.FFmpegPCMAudio(audio_url, **ffmpeg_opts))
    await ctx.send(f"▶️ Now playing: **{title}**")

@bot.command()
async def pause(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸ Paused")

@bot.command()
async def resume(ctx):
    if ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("▶️ Resumed")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("⏹ Stopped")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Left voice channel")

bot.run("MTQ1Mzk1MjU1MjQ5NTIxODgwMA.G3611k.iqfUqq21UgGE2rJOfOvOv_9TpcIdLgUY_Cpt_U")
