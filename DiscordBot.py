import discord
from discord.ext import commands
import GetAnimeList
import Game
import asyncio
import yt_dlp
import PlayYoutubeMusic
import os

secret = "MTM0NjkwODEzNjM0MjE2MzYxMQ.G-42vk.BssqmstlLTbekIFykr6wddDSrwz8fkp1g7jJBU"
client_id = "1346908136342163611"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def play_audio(ctx, url):
    if not ctx.author.voice:
        await ctx.send('Você não está em um canal de voz.')
        return

    channel = ctx.author.voice.channel
    
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()

    voice_channel = await channel.connect()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [],
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        audio_file = f'downloads/{info["id"]}.mp3'
    raw = f'downloads/{info["id"]}.webm'
    converted = audio_file
    PlayYoutubeMusic.convert_webm_to_mp3(raw, converted)

    ffmpeg_audio = discord.FFmpegPCMAudio(audio_file, before_options="-ss 00:00:00 -t 00:00:20")

    voice_channel.play(ffmpeg_audio, after=lambda e: print('done', e))

    while voice_channel.is_playing():
        await asyncio.sleep(1)

    await voice_channel.disconnect()

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command(name='mylist')
async def mylist(ctx, arg):
    user_id = ctx.author.id 
    user = GetAnimeList.REQUEST(arg, user_id)
    user.print_user_info()
    await ctx.send(f'Lista atualizada')

@bot.command(name='play')
async def play(ctx):
    if ctx.author.voice:
        user_id = str(ctx.author.id)
        search = Game.start(user_id)
        url = PlayYoutubeMusic.search_opening(search)
        await play_audio(ctx, url)
    else:
        await ctx.send('Você não está em um canal de voz.')

bot.run(secret)
