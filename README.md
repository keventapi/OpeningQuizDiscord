OpeningQuizDiscord

OpeningQuizDiscord is a Discord bot designed for anime fans to test their knowledge by guessing anime openings. The bot plays a random anime opening, and users have one chance to guess the anime. Points are awarded for correct guesses, and a leaderboard is displayed at the end of the match.

Features

Fetches anime lists from MyAnimeList and stores them.

Retrieves anime openings from AnimeThemes.moe.

Interactive Discord bot using discord.py.

Slash command /guess with autocomplete support.

Score tracking and leaderboard display.

Installation

Requirements

Python 3.8+

discord.py library

requests library

asyncio library

Setup

Clone the repository:

git clone https://github.com/keventapi/OpeningQuizDiscord.git
cd OpeningQuizDiscord

Install dependencies:

pip install -r requirements.txt

Create a .env file and add your bot token:

DISCORD_BOT_TOKEN=your_token_here

Run the bot:

python Discord.py

File Structure

OpeningQuizDiscord/
├── Data.json          # Stores user anime list (ID, name, alias)
├── Discord.py         # Handles Discord bot interactions
├── Game.py            # Core game logic
├── GetAnimeList.py    # Fetches anime info (openings, names, IDs, aliases)
├── requirements.txt   # Required dependencies
└── README.md          # Documentation

Commands

!mylist

Fetch or update the user's completed anime list from MyAnimeList.

!play

Start a match. (User must be in a voice channel)

!stop

Stop the match. (Bot must be in a voice channel)

/guess

Slash command with autocomplete support, fetching anime names from Data.json.
(Must be in a match for this command to work)

APIs Used

discord.py: Handles interactions within the Discord server.

MyAnimeList API: Retrieves user anime lists.

AnimeThemes.moe API: Fetches anime openings.

How It Works

The bot retrieves and stores a user's completed anime list from MyAnimeList.

During a match, the bot selects a random anime and plays its opening.

Users have one guess per opening.

If guessed correctly, the player earns a point.

At the end of the match, the bot displays the leaderboard.

License

This project is for fun and is open-source. Feel free to contribute!

Contact

For issues or suggestions, open an issue on GitHub.
