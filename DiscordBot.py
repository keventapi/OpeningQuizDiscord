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
import time

class Game_configs:
    def __init__(self, ctx=None, user_id='', voice_channel=None, host='', match={}, alternative_names=[], played=[], url='', file=''):
        self.ctx = ctx
        self.user_id = user_id
        self.voice_channel = voice_channel
        self.host = host
        self.match = match
        self.alternative_names = alternative_names
        self.played = played
        self.url = url
        self.file = file

global configs

secret = ''
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
configs = Game_configs()

last_autocomplete_time = 0
cooldown = 1/30

async def autocomplete(interaction: discord.Interaction, current: str):
    global last_autocomplete_time
    
    current_time = time.time()

    if current_time - last_autocomplete_time < cooldown:
        return []
    
    last_autocomplete_time = current_time
    
    try:
        options_list = await Game.get_name_list()
        if not options_list:
            print("No options found in Data.json.")
            return []
    except Exception as e:
        print(f"Error in get_name_list: {e}")
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
    global configs
    configs.user_id = str(interaction.user.id)
    configs = pontuation_system(opcao)
    print(f'<@{str(interaction.user.id)}> has {configs.match[str(interaction.user.id)]["points"]} points')
    await interaction.response.send_message(f'<@{str(interaction.user.id)}> has {configs.match[str(interaction.user.id)]["points"]} points', ephemeral=True)

def check_player_in_match(user_id):
    global configs
    if user_id not in configs.match:
        configs.match[user_id] = {'points': 0, 'guessed': False}
    return configs

async def download():
    global configs
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [],
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
        'nocheckcertificate': True
    }
    attempts = 2
    for i in range(attempts):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(configs.url, download=True)
            configs.file = f'downloads/{info["id"]}.{info["ext"]}'
            return configs
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            await asyncio.sleep(3)
    return await search_opening()
    

def pontuation_system(answer):
    global configs
    configs = check_player_in_match(str(configs.user_id))
    if answer in configs.alternative_names and configs.match[configs.user_id]['guessed'] is not True:
        configs.match[configs.user_id]['points'] += 1
        configs.match[configs.user_id]['guessed'] = True
    elif answer not in configs.alternative_names and configs.match[configs.user_id]['guessed'] is not True:
        configs.match[configs.user_id]['guessed'] = True
    return configs


def make_it_guesseble():
    global configs
    if configs.match != {}:
        for i in configs.match.keys():
            configs.match[i]['guessed'] = False
    return configs

def create_end_message(match):
    global configs
    message = ""
    for i in match.keys():
        message += f'<@{i}> has {match[i]["points"]} points\n'
    return message


async def reset_game(ctx, counter):
    global configs
    if counter == 20:
        for i in configs.match.keys():
            configs.match[i]['points'] = 0
            configs.match[i]['guessed'] = False
        await ctx.voice_client.disconnect()
        message = create_end_message(configs.match)        
        print(configs.played)
        configs.played = []
        await ctx.send(message)
        return configs
    return configs
        

async def show_round_answer(ctx):
    global configs
    await ctx.send(f'{configs.url}')
    names = ", ".join(str(i) for i in configs.alternative_names)
    await ctx.send(f'anime name: {configs.alternative_names[-1]}')
    await ctx.send(f'alternative names: {names}')

async def check_on_call(ctx, voice_channel):
    global configs
    return ctx.voice_client.is_playing()
    
async def delete_unused_itens(archives):
    return Game.unused_itens(archives)


async def search_opening():
    global configs
    search = await Game.start(configs.host)
    while search[0] in configs.played:
        search = await Game.start(configs.host)
    configs.played.append(search[0])
    configs.alternative_names = search[1]
    configs.url = await PlayYoutubeMusic.search_opening(search[0])
    configs = await download()
    return configs

async def round_end(ctx, counter):
    global configs
    configs = make_it_guesseble()
    await show_round_answer(ctx)
    await delete_unused_itens([configs.file])
    configs = await reset_game(ctx, counter)
    return configs

async def play_audio(ctx):
    global configs
    counter = 0
    while counter < 20:
        try:
            configs = await search_opening()
            ffmpeg_audio = discord.FFmpegPCMAudio(configs.file, executable="ffmpeg", before_options="-ss 00:00:00 -t 00:00:30")
            ctx.voice_client.play(ffmpeg_audio, after=lambda e: print(''))
            while await check_on_call(ctx, configs.voice_channel):
                await asyncio.sleep(1)   
            counter += 1
            configs = await round_end(ctx, counter)
        except Exception as e:
            print(f"An error occurred: {e}")
            configs = await ctx.send(f"An error occurred: {e}")
            if ctx.voice_client.is_connected():
                await ctx.voice_client.disconnect()
            break

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
    global configs

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
        host = str(ctx.author.id)
        configs = Game_configs(ctx, user_id, ctx.voice_client.channel, host, match={}, alternative_names=[], played=[])
        await play_audio(ctx)
    else:
        await ctx.send('Você não está em um canal de voz.')

@bot.command(name='stop')
async def stop(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send('não to jogando otario')


bot.run(secret)