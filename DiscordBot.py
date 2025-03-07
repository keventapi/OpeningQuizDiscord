import discord
from discord.ext import commands
from discord import app_commands
import GetAnimeList
import Game
import asyncio
import yt_dlp
import PlayYoutubeMusic
import os

secret = ""
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
global match
global alternative_names
alternative_names = []
match = {}

async def autocomplete(interaction: discord.Interaction, current: str):
    options_list = Game.get_name_list()
    filtered_options = []
    seen = set()
    for option in options_list:
        if current.lower() in option.lower() and option not in seen:
            filtered_options.append(app_commands.Choice(name=option, value=option))
            seen.add(option)
    return filtered_options[:20]

@bot.tree.command(name='guess', description="it's your openning guess")
@app_commands.describe(opcao='guess the anime')
@app_commands.autocomplete(opcao=autocomplete)
async def guess(interaction: discord.Interaction, opcao: str):
    global alternative_names
    global match
    if str(interaction.user.id) not in match:
        match[str(interaction.user.id)] = {'points': 0, 'guessed': False}
    
    if opcao in alternative_names and match[str(interaction.user.id)]['guessed'] is not True:
        match[str(interaction.user.id)]['points'] += 1
        match[str(interaction.user.id)]['guessed'] = True
        user_points = match[str(interaction.user.id)]['points']    
    elif opcao not in alternative_names and match[str(interaction.user.id)]['guessed'] is not True:
        match[str(interaction.user.id)]['guessed'] = True
        user_points = match[str(interaction.user.id)]['points']

    user_points = match[str(interaction.user.id)]['points']
    print(f'<@{str(interaction.user.id)}> has {user_points} points')
    await interaction.response.send_message(f'<@{str(interaction.user.id)}> has {match[str(interaction.user.id)]["points"]} points', ephemeral=True)

async def play_audio(ctx, user_id, voice_channel, counter=0):
    search = Game.start(user_id)
    global match
    global alternative_names
    alternative_names = search[1]

    url = PlayYoutubeMusic.search_opening(search[0])
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
    ffmpeg_audio = discord.FFmpegPCMAudio(audio_file, before_options="-ss 00:00:00 -t 00:00:30")
    voice_channel.play(ffmpeg_audio, after=lambda e: print('done', e))
    
    while voice_channel.is_playing():
        await asyncio.sleep(1)
    
    await ctx.send(f'{url}')
    names = ", ".join(str(i) for i in alternative_names)
    await ctx.send(f'anime name: {alternative_names[-1]}')
    await ctx.send(f'alternative names: {names}')
    if user_id in match:
        match[user_id]['guessed'] = False

    if voice_channel.is_playing() != True:
        Game.unused_itens([raw, converted])
    if counter < 20:
        print(names)
        counter += 1
        await play_audio(ctx, user_id, voice_channel, counter)
    else:
        match = {}
        await ctx.voice_client.disconnect()

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    await bot.tree.sync()
    print('sincronizado')

@bot.command(name='mylist')
async def mylist(ctx, arg):
    user_id = ctx.author.id 
    user = GetAnimeList.REQUEST(arg, user_id)
    user.print_user_info()
    await ctx.send(f'Lista atualizada')

@bot.command(name='play')
async def play(ctx):
    if not ctx.author.voice:
        await ctx.send('Você não está em um canal de voz.')
        return

    channel = ctx.author.voice.channel
    
    if ctx.voice_client is not None:
        await ctx.send('To no meio de um jogo panaca')
        return

    voice_channel = await channel.connect()

    if ctx.author.voice:
        user_id = str(ctx.author.id)
        await play_audio(ctx, user_id, voice_channel)
    else:
        await ctx.send('Você não está em um canal de voz.')

bot.run(secret)
