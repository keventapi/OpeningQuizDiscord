files:
  Data.Json
    it will store the MAL user list information such as id, anime name and alias
  Discord.py
    it is where the functions that works with the discord api will work
  Game.py
    the game logic that dont need to be requested will work here 
  GetAnimeList.py  
    the animes info will be requested here, such as opening link, name, id and alias

commands:
  !mylist
    get or update the MyAnimeList completed anime
  !play
    start a match ~user needs to be in a voice-channel to make the bot start a match~
  !stop
    stop the match ~bot nees to be in a call to use this commands~
  /guess
    slash command to use the feature autocomplete and it will get all te Data.json animes and alias to help the players guess the anime ~you need to be in a match to make the command work, otherwise it will just say that its not playing at the moment~

APIS:
discord.py
  to do the interactions in the server and make it playable
MyAnimeList
  to get the user list and save it in the Data.json
AnimeThemes.moe
  it will get the openings

what is it for:
its just a for fun bot, it will create a match in the call and play openings, you will guess once per opening, if you guess it right you will score a point, at the end of the match the bot will show the leaderboard

