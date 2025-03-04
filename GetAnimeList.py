import json
import requests
from time import sleep

class REQUEST():
    def __init__(self, user, discord_id):
        self.CLIENT_ID = 'e29fe4120a686914b88e4b23a1e41bf9'
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

    def get_anime_alias(self):
        for i in self.anime_list:
            url = f'https://api.myanimelist.net/v2/anime/{i}?fields=id,alternative_titles,media_type'
            response = requests.get(url, headers = {'X-MAL-CLIENT-ID': self.CLIENT_ID})
            response.raise_for_status()
            user = response.json()
            print(i, user)
            response.close()
            sleep(3)

        pass

    def get_anime_type(self):
        pass

    def clear_data(self, data):
        length = len(data['data'])
        for i in range(length):
            self.anime_list[(str(data['data'][i]['node']['id']))] = data['data'][i]['node']['title']
        self.get_anime_alias()
        self.create_data()
    
    def create_data(self):
        file = 'Data.json'
        with open(file, 'r', encoding='utf-8') as f:
            file_content = f.read().strip()
            if not file_content:
                dados = {}
            else:
                dados = json.load(f)
        self.data_update(dados)

    def data_update(self, old_data):
        if self.discord_id not in old_data:
            old_data[self.discord_id] = {'anime_list': []}
        
        old_data[self.discord_id]['anime_list'] = self.anime_list
        file = 'Data.json'
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(old_data, f, ensure_ascii=False, indent=4)

keven = REQUEST('Keven_Lohan', '418456190704549908').print_user_info()