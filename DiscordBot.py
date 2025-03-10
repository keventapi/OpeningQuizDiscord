import discord
from discord.ext import commands
from discord import app_commands
import GetAnimeList
import Game
import asyncio
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
    voice_clients = interaction.client.voice_clients
    if any(vc.guild.id == interaction.guild.id for vc in voice_clients):
        configs.user_id = str(interaction.user.id)
        configs = pontuation_system(opcao)
        print(f'<@{str(interaction.user.id)}> has {configs.match[str(interaction.user.id)]["points"]} points')
        await interaction.response.send_message(f'<@{str(interaction.user.id)}> has {configs.match[str(interaction.user.id)]["points"]} points', ephemeral=True)
    else:
        await interaction.response.send_message(f'<@{str(interaction.user.id)}> im not in game', ephemeral=True)

def check_player_in_match(user_id):
    global configs
    if user_id not in configs.match:
        configs.match[user_id] = {'points': 0, 'guessed': False}
    return configs

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
        message = create_end_message(configs.match)    
        for i in configs.match.keys():
            configs.match[i]['points'] = 0
            configs.match[i]['guessed'] = False
        await ctx.voice_client.disconnect()
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
    playing = ctx.voice_client.is_playing()
    if playing is None:
        return False
    return playing

async def search_opening():
    global configs
    search = await Game.start(configs.host)
    while search[0] in configs.played:
        search = await Game.start(configs.host)
    configs.played.append(search[0])
    configs.alternative_names = search[1]
    configs.url = search[0]
    return configs

async def round_end(ctx, counter):
    global configs
    configs = make_it_guesseble()
    await show_round_answer(ctx)
    configs = await reset_game(ctx, counter)
    return configs

async def play_audio(ctx):
    global configs
    counter = 0
    while counter < 20:
        try:
            configs = await search_opening()

            if ctx.voice_client:
                ffmpeg_audio = discord.FFmpegPCMAudio(configs.url, executable="ffmpeg", before_options="-ss 00:00:00 -t 00:00:30")
                ctx.voice_client.play(ffmpeg_audio, after=lambda e: print(''))
            else:
                break

            while await check_on_call(ctx, configs.voice_channel):
                await asyncio.sleep(1)   
            counter += 1
            configs = await round_end(ctx, counter)
        except Exception as e:
            print(f"An error occurred: {e}")

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
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send('não to jogando otario')


bot.run(secret)