import os
import discord
from discord.ext import commands
import yt_dlp

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ytdlp_opts = {'format': 'bestaudio/best', 'quiet': True}
ffmpeg_opts = {'options': '-vn'}

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        await ctx.send("🎧 Joined voice channel")
    else:
        await ctx.send("❌ Join a voice channel first")

@bot.command(aliases=["p"])
async def play(ctx, *, url):
    if not ctx.author.voice:
        await ctx.send("❌ Join a voice channel first")
        return

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
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

# ✅ SAFE
bot.run(os.getenv("MTQ1Mzk1MjU1MjQ5NTIxODgwMA.G3611k.iqfUqq21UgGE2rJOfOvOv_9TpcIdLgUY_Cpt_U"))

