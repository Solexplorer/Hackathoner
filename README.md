# Hackathoner

This bot is a POC that I worked on a little time ago but it works.

To start using it, I suggest to create a server and add the bot to that [server](https://github.com/jagrosh/MusicBot/wiki/Adding-Your-Bot-To-Your-Server)

## Steps to install 

- Clone this repo

- Install the python modules using the `requirements.txt`

- Rename `.env.example`: `mv .env.example .env`

- Fill the env variable in the file. `CHANNEL` is the ID of the channel, `TOKEN` is the token of the bot, `CATEGORY` is the Hackathon category

- Remember to create the CATEGORY in the discord server that you defined in the `.env`

- Run the flask app and send post requests with `issue_message`, `discord_username`, `sponsor_name`

 It should be working!
