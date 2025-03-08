import json
import requests
import Game
from time import sleep

class REQUEST():
    def __init__(self, user, discord_id):
        self.CLIENT_ID = ''
        self.user = user
        self.discord_id = discord_id
        self.anime_list = {}

    def print_user_info(self):
        url = f"https://api.myanimelist.net/v2/users/{self.user}/animelist?status=completed&limit=1000"
        response = requests.get(url, headers = {'X-MAL-CLIENT-ID': self.CLIENT_ID})
        print(response.status_code)
        response.raise_for_status()
        user = response.json()
        response.close()
        self.clear_data(user)

    def get_anime_info(self, id):
        url = f'https://api.myanimelist.net/v2/anime/{id}?fields=id,alternative_titles,media_type'
        response = requests.get(url, headers = {'X-MAL-CLIENT-ID': self.CLIENT_ID})
        response.raise_for_status()
        user = response.json()
        response.close()
        other_animes_name = user['alternative_titles']['synonyms']
        other_animes_name.append(user['alternative_titles']['en'])
        other_animes_name.append(user['title'])
        anime_type = user['media_type']
        return [other_animes_name, anime_type]

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

    def json_log(self, json_data):
        json_log = json.dumps(json_data['data']['music_videos'][0], indent=4, ensure_ascii=False)
        title = json_data['data']['music_videos'][0]['meta']['title']
        author = json_data['data']['music_videos'][0]['meta']['author']
        print(json_log)
        return json_log
                            

    async def get_opening(self, anime_id, anime, discord_id):
        try:
            url = f'https://api.jikan.moe/v4/anime/{anime_id}/videos'
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            response.close()
            title = data['data']['music_videos'][0]['meta']['title']
            author = data['data']['music_videos'][0]['meta']['author']
            print(f'{anime} anime opening {title} - {author} tv size')
            return data['data']['music_videos'][0]['video']['url']
        except:
            return await Game.start(discord_id)