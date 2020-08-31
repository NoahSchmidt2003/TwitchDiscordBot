import asyncio
import json
import sys
import requests
import discord
from discord import *


def Twitch():
    global live, viewercount, username, game_id, title, startedat, thumbnail, livebool

    apitoken = "https://id.twitch.tv/oauth2/token?client_id=Your ID&client_secret" \
               "=Your clientsecret&grant_type=client_credentials&scope="
    API = 'https://api.twitch.tv/helix/streams?user_login=your streamer of choice'
    Client_ID = "Your Client ID"
    rq_token = requests.post(url=apitoken)
    tokendic = json.loads(rq_token.text)
    token = tokendic['access_token']
    head = {
        'client-id': Client_ID,
        "Authorization": "Bearer " + token
    }
    rq = requests.get(url=API, headers=head)
    rqdic = json.loads(rq.text)
    print(rqdic)
    try:
        live = rqdic['data'][0]['type']
    except:
        livebool = False
        return livebool
    viewercount = str(rqdic['data'][0]['viewer_count'])
    username = str(rqdic['data'][0]['user_name'])
    game_id = str(rqdic['data'][0]['game_id'])

    title = str(rqdic['data'][0]['title'])
    startedat = str(rqdic['data'][0]['started_at'])
    thumbnail = str(rqdic['data'][0]['thumbnail_url'])
    thumbnail = thumbnail[:thumbnail.find('{')]
    thumbnail = str(thumbnail + "1920x1080.jpg")
    livebool = True

    return live, viewercount, username, game_id, title, startedat, thumbnail


class BotClient(discord.Client):

    async def on_ready(self):
        print("Bot is ready")

    async def on_message(self, message):
        firstmsg = "@everyone "
        if message.content.startswith("start bot"):
            while True:
                Twitch()
                if livebool:
                    messages = (
                            "" + firstmsg + "Streamer :red_circle: is live :red_circle: " + title + "with "
                                                                                                              ":ok_hand: " + viewercount + " vieweres :ok_hand: \nSometext \nLink from the streamer ")
                    firstmsg = ""
                else:
                    messages = "streamer is acutally  :black_circle:  offline :black_circle: !"
                message = await message.channel.send(messages)
                await asyncio.sleep(300)
                await message.delete()


if __name__ == '__main__':
    bot = BotClient()
    bot.run("Your discord bot token")
