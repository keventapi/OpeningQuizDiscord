import json
import requests
import asyncio
import random
from time import sleep

class REQUEST():
    def __init__(self, user, discord_id):
        self.CLIENT_ID = ''
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

    async def get_anime_type(self, id):
        url = f'https://api.myanimelist.net/v2/anime/{id}?fields=id,alternative_titles,media_type'
        response = requests.get(url, headers = {'X-MAL-CLIENT-ID': self.CLIENT_ID})
        response.raise_for_status()
        user = response.json()
        response.close()
        anime_type = user['media_type']
        return anime_type
    
    async def get_random_anime(self):
        dados = await self.get_data()        
        random_key = random.choice(list(dados[self.discord_id]["anime_list"][0].keys()))
        anime_type = await self.get_anime_type(random_key)
        anime_name = dados[self.discord_id]["anime_list"][0][random_key][-1]
        anime_alias = dados[self.discord_id]["anime_list"][0][random_key]
        if dados[self.discord_id]["anime_list"][0][random_key][-1] not in self.played and anime_type == 'tv':
            self.played.append(dados[self.discord_id]["anime_list"][0][random_key][-1])
            return random_key, anime_name, anime_alias
        await asyncio.sleep(5)
        return await self.get_random_anime()
    
    async def get_anime_info_with_MAL(self):
        try:
            anime_id, anime_name, anime_alias = await self.get_random_anime()
            url = f'{self.ATapi}/anime/?filter[has]=resources&filter[site]=MyAnimeList&filter[external_id]={anime_id}&include=animethemes.animethemeentries.videos'
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            data = self.get_only_openings(data)
            response.close()
            data = {'anime_id': anime_id, 'anime_name': anime_name, 'anime_alias': anime_alias, 'openings': data}
            return data
        except Exception as e:
            print(e)
            return await self.get_anime_info_with_MAL()

    def reset_played(self):
        self.played = []
