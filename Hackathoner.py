import discord
import asyncio
from flask import Flask, request
from threading import Thread
import os
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

# discord.py wants the channel id as int, not string
DISCORD_CHANNEL = int(os.getenv("CHANNEL"))
# This is the Token of the bot
TOKEN = os.getenv("TOKEN")
# Category of the Hackathon in the Discord Channel. ex. WEB3-WORLD
hackathon_category = os.getenv('CATEGORY')
# Every category has max. 50 channels allowed, once a category reaches > 40 channels,
# this counter is increased and creates another category
counter_cat = 1

# Makes bot run 24/7
app = Flask('')


@app.route('/new/channel', methods=['POST'])
def createchan():
    # Work Plan of the user
    issue_message = request.form.get('issue_message')
    # The discord username of the worker applied
    discord_username = request.form.get('discord_username')
    # Name of the sponsor ex. AAVE or STATUS
    sponsor_name = request.form.get('sponsor_name')
    # This is the id of the "general" channel, it's the easiest way to get the guild
    channel = client.get_channel(DISCORD_CHANNEL)
    # Create an async task
    client.loop.create_task(create_channel(discord_username, channel.guild, sponsor_name, issue_message))
    return "Who are you? "


async def create_channel(discord_username, guild, sponsor_name, issue_message):
    global hackathon_category, counter_cat

    # Get the category object
    category = discord.utils.get(guild.categories, name=hackathon_category)
    # Name of the channel is set as sponsor_name + Discord_username ex. aave-explorer
    name_channel = (sponsor_name + '-' + discord_username.split('#')[0]).lower()
    # Check the category where I am creating channels doesn't have more than 40 channels
    if len(category.channels) < 40:
        await guild.create_text_channel(name_channel, category=category)
    else:
        if hackathon_category == 'GLOBAL-COMMUNITIES-PROJECTS':
            hackathon_category = hackathon_category + '-2'
        else:
            hackathon_category = hackathon_category.replace(hackathon_category[-2:],
                                                            "-" + str(int(hackathon_category[-1:]) + 1))
        await guild.create_category(hackathon_category)
        category = discord.utils.get(guild.categories, name=hackathon_category)
        await guild.create_text_channel(name_channel, category=category)
    created_channel = discord.utils.get(guild.text_channels, name=name_channel)
    user = discord.utils.get(guild.members, name=discord_username)
    # If username is not found, it cannot be pinged
    username = '@' + discord_username if user is None else user.mention
    # Insert text of the channel
    text_channel = username + ' Work Plan: ' + issue_message + '\nUse this channel to discuss the project with the sponsors or other hackers'
    # Send the message
    await created_channel.send(text_channel)


def start_server():
    app.run(host='0.0.0.0', port=8080)


t = Thread(target=start_server)
t.start()


# Discord bot code

@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)


# return await client.change_presence(game=discord.Game(name='games')) #Would display as "playing games" in Discord

@client.event
async def on_message(message):
    # TODO: Add cmd set private channel
    pass


client.run(TOKEN)

