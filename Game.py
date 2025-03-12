import json
import random
import GetAnimeList
import aiofiles

async def open_json():
    file = 'Data.json'
    with open(file, 'r', encoding='utf-8') as f:
        file_content = f.read().strip()
        if not file_content:
            return "voce precisa registrar sua lista com !mylist (SEU PERFIL DO MAL)"
        else:
            f.seek(0)
            dados = json.load(f)
            return dados

async def start(discord_id):
    dados = GetAnimeList.REQUEST('', discord_id)
    anime_info = await dados.get_anime_info_with_MAL()
    update_anime_alias(discord_id, anime_info['anime_id'], anime_info['anime_alias'])
    search = get_opening(anime_info['openings'])
    print(anime_info['anime_alias'])
    return [search, anime_info['anime_alias']]
    
def get_opening(openings):
    return random.choice(openings)

def update_anime_alias(discord_id, anime_id, alias):
    with open('Data.json', 'r', encoding='utf-8') as f:
            file_content = f.read().strip()
            if not file_content:
                data = {}
            else:
                f.seek(0)
                data = json.load(f)
    data[discord_id]['anime_list'][0][anime_id] = alias
    file = 'Data.json'
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

async def get_name_list():
    async with aiofiles.open('Data.json', 'r', encoding='utf-8') as f:
        file_content = await f.read()
        if not file_content.strip():
            print("Data.json is empty or not found.")
            return []
        data = json.loads(file_content)
    
    return await get_all_names(data)
        
async def get_all_names(data):
    empty_array = []
    for user, user_data in data.items():
        for anime_data in user_data.get('anime_list', []):
            for anime_id, aliases in anime_data.items():
                empty_array.extend(aliases)
    return empty_array

