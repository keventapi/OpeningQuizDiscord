import json
import time
import requests
import asyncio
import random
from time import sleep
import aiohttp

class REQUEST():
    def __init__(self, user, discord_id):
        self.CLIENT_ID = 'e29fe4120a686914b88e4b23a1e41bf9'
        self.ATapi = 'https://api.animethemes.moe'
        self.played = []
        self.user = user
        self.discord_id = discord_id
        self.anime_list = {}


    def print_user_info(self):
        url = f"https://api.myanimelist.net/v2/users/{self.user}/animelist?status=completed&limit=1000"
        response = requests.get(url, headers = {'X-MAL-CLIENT-ID': self.CLIENT_ID})
        response.raise_for_status()
        user = response.json()
        response.close()
        self.clear_data(user)
    
    def get_only_openings(self, data):
        data = data['anime'][0]['animethemes']
        openings = []
        for theme in data:
            if theme['type'] == 'OP':
                openings.append(theme['animethemeentries'][0]['videos'][0]['link'])
        return openings

    async def get_data(self):
        file = 'Data.json'
        with open(file, 'r', encoding='utf-8') as f:
            file_content = f.read().strip()
            if not file_content:
                return "voce precisa registrar sua lista com !mylist (SEU PERFIL DO MAL)"
            else:
                f.seek(0)
                dados = json.load(f)
            return dados

    def get_alias(self, user):
        other_animes_name = user['alternative_titles']['synonyms']
        other_animes_name.append(user['alternative_titles']['en'])
        other_animes_name.append(user['title'])
        return other_animes_name

    async def get_anime_type(self, id):
        url = f'https://api.myanimelist.net/v2/anime/{id}?fields=id,alternative_titles,media_type'
        response = requests.get(url, headers = {'X-MAL-CLIENT-ID': self.CLIENT_ID})
        response.raise_for_status()
        user = response.json()
        response.close()
        alias = self.get_alias(user)
        anime_type = user['media_type']
        return anime_type, alias
    
    async def get_random_anime(self):
        dados = await self.get_data()        
        random_key = random.choice(list(dados[self.discord_id]["anime_list"][0].keys()))
        anime_type, anime_alias = await self.get_anime_type(random_key)
        anime_name = dados[self.discord_id]["anime_list"][0][random_key][-1]
        if dados[self.discord_id]["anime_list"][0][random_key][-1] not in self.played and anime_type == 'tv':
            self.played.append(dados[self.discord_id]["anime_list"][0][random_key][-1])
            return random_key, anime_name, anime_alias
        await asyncio.sleep(5)
        return await self.get_random_anime()

    async def get_anime_info_with_MAL(self):
        try:
            anime_id, anime_name, anime_alias = await self.get_random_anime()
            url = f'{self.ATapi}/anime/?filter[has]=resources&filter[site]=MyAnimeList&filter[external_id]={anime_id}&include=animethemes.animethemeentries.videos'
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()
            
            data = self.get_only_openings(data)
            return {'anime_id': anime_id, 'anime_name': anime_name, 'anime_alias': anime_alias, 'openings': data}
        
        except Exception as e:
            print(e)
            return await self.get_anime_info_with_MAL()

        
    def clear_data(self, data):
        length = len(data['data'])
        for i in range(length):
            self.anime_list[(str(data['data'][i]['node']['id']))] = [data['data'][i]['node']['title']]
        self.create_data()
    
    def create_data(self):
        file = 'Data.json'
        with open(file, 'r', encoding='utf-8') as f:
            file_content = f.read().strip()
            if not file_content:
                dados = {}
            else:
                f.seek(0)
                dados = json.load(f)
        self.data_update(dados)

    def data_update(self, old_data):
        if self.discord_id not in old_data:
            old_data[self.discord_id] = {'anime_list': []}
        
        old_data[self.discord_id]['anime_list'] = [self.anime_list]
        file = 'Data.json'
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(old_data, f, ensure_ascii=False, indent=4)

    def reset_played(self):
        self.played = []