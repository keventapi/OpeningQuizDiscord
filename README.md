# Anime Guessing Bot

This is a fun Discord bot focused on anime guessing. During a match, the bot will play anime openings, and players will have to guess the anime name to score points. At the end of the match, the bot will show the leaderboard.

## Features

- **!mylist**: Fetches or updates the user's completed anime list from MyAnimeList.
- **!play**: Starts a match. The user must be in a voice channel for the bot to start the match.
- **!stop**: Stops the match. The bot must be in a voice channel for this command to work.
- **/guess**: Autocomplete slash command to guess the anime. It fetches data from the `Data.json` file to help players guess the anime. This command works only when a match is active.

## Files

- **Data.json**: Stores the user's MyAnimeList information, including anime ID, name, and alias.
- **Discord.py**: Contains functions that interact with the Discord API to manage matches on the server.
- **Game.py**: Contains the game logic, such as score management, match control, and ending the match.
- **GetAnimeList.py**: Responsible for fetching anime information, including opening links, names, IDs, and aliases, and saving it to the data file.

## APIs

- **discord.py**: Used for interacting with the Discord API to control server aspects, such as starting matches, handling commands, and updating the leaderboard.
- **MyAnimeList**: Used to fetch the user's anime list and save the data to `Data.json`.
- **AnimeThemes.moe**: Used to fetch anime openings that will be played during the match.

## How to Use

1. **Add the bot to your server**:
   - Ensure the bot has the necessary permissions to join voice channels and send messages.

2. **Commands**:
   - **!mylist**: The bot will fetch and update your completed anime list.
   - **!play**: Start a match in the voice channel. You must be in a voice channel to start the match.
   - **!stop**: End the match if the bot is in a voice channel.
   - **/guess**: Try to guess the anime based on the openings played during the match.

3. **Requirements**:
   - The bot needs access to the voice channel to start the match and play the openings.
   - The `/guess` command only works when a match is active.

## How to Contribute

1. Fork this repository.
2. Create a branch for your changes (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to your repository (`git push origin feature/new-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
