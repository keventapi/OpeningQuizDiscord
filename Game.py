import json
import random
import GetAnimeList
import os

def start(discord_id):
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
        return start(discord_id)
    else:
        update_anime_alias(discord_id, random_key, informations[0])
        return [f'{informations[0][-1]} opening', informations[0]]
    
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


def get_name_list():
    with open('Data.json', 'r', encoding='utf-8') as f:
        file_content = f.read().strip()
        if not file_content:
            return False
        else:
            f.seek(0)
            data = json.load(f)
            result = get_all_names(data)
            return result
        
def get_all_names(data):
    empty_array = []
    for users in data.keys():
        print(users)
        for anime_list in data[users].keys():
            print(anime_list)
            for id in data[users][anime_list][0].keys():
                empty_array.append(data[users][anime_list][0][id][0])
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
