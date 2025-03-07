import discord
from discord.ext import commands
from discord import app_commands
import GetAnimeList
import Game
import asyncio
import yt_dlp
import PlayYoutubeMusic
import os
import aiofiles

secret = ''
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
global match
global alternative_names
alternative_names = []
match = {}

async def autocomplete(interaction: discord.Interaction, current: str):
    options_list = await Game.get_name_list()
    if not options_list:
        return []
    
    filtered_options = []
    seen = set()
    for option in options_list:
        if current.lower() in option.lower() and option not in seen and option != '' and 1 <= len(option) <= 100:
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

async def download(url):
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [],
                'outtmpl': 'downloads/%(id)s.%(ext)s',
                'quiet': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
            file = f'downloads/{info["id"]}.{info["ext"]}'
            return file
            
            


async def play_audio(ctx, user_id, voice_channel):
    counter = 0
    played = []
    while counter < 20:
        try:
            search = Game.start(user_id)
            while search[0] in played:
                search = Game.start(user_id)
            played.append(search[0])
            global match
            global alternative_names
            alternative_names = search[1]

            url = await PlayYoutubeMusic.search_opening(search[0])
            
            try:
                file = await download(url)
            except:
                search = Game.start(user_id)
                alternative_names = search[1]
                url = await PlayYoutubeMusic.search_opening(search[0])
                file = await download(url)
            
            ffmpeg_audio = discord.FFmpegPCMAudio(file, executable="ffmpeg", before_options="-ss 00:00:00 -t 00:00:30")
            voice_channel.play(ffmpeg_audio, after=lambda e: print('done', e))
            print(f"Playing URL: {url}")
            if user_id in match:
                match[user_id]['guessed'] = False
            
            while voice_channel.is_playing():
                await asyncio.sleep(1)
            
            await ctx.send(f'{url}')
            names = ", ".join(str(i) for i in alternative_names)
            await ctx.send(f'anime name: {alternative_names[-1]}')
            await ctx.send(f'alternative names: {names}')

            if not voice_channel.is_playing():
                Game.unused_itens([file])
                counter += 1
            else:
                match = {}
                await ctx.voice_client.disconnect()
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            await ctx.send(f"An error occurred: {e}")
            if voice_channel.is_connected():
                await ctx.voice_client.disconnect()
            break

    if counter >= 20 and voice_channel.is_connected():
        await ctx.voice_client.disconnect()
        message = f''
        for i in match.keys():
            message += f'<@{i}> has {match[i]["points"]} points\n'
        print(played)
        played = []
        await ctx.send(message)

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

@bot.command(name='stop')
async def stop(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send('não to jogando otario')


bot.run(secret)
