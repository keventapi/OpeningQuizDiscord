import json
import random
import GetAnimeList
import os
import aiofiles

async def start(discord_id):
    file = 'Data.json'
    with open(file, 'r', encoding='utf-8') as f:
        file_content = f.read().strip()
        if not file_content:
            return "voce precisa registrar sua lista com !mylist (SEU PERFIL DO MAL)"
        else:
            f.seek(0)
            dados = json.load(f)
    random_key = random.choice(list(dados[discord_id]["anime_list"][0].keys()))
    info = GetAnimeList.REQUEST('','')
    informations = info.get_anime_info(random_key)
    if informations[1] != 'tv':
        return await start(discord_id)
    else:
        update_anime_alias(discord_id, random_key, informations[0])
        print(informations)
        search = await GetAnimeList.REQUEST('','').get_opening(random_key, informations[0][-1], discord_id)
        return [search, informations[0]]
    
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

def unused_itens(archives):
    for i in archives:
        print(i)
        try:
            os.remove(i)
            print(f"File {i} has been deleted successfully.")
        except FileNotFoundError:
            print(f"The file {i} was not found.")
        except PermissionError:
            print(f"Permission denied to delete the file {i}.")
        except Exception as e:
            print(f"Error: {e}")

