import json
import random
import GetAnimeList

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
        return False
    else:
        return f'{informations[0][-1]} opening'