import asyncio
import sys
import requests
import discord
from discord import member

try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except Exception:
    pass


class MyClient(discord.Client):

    async def on_ready(self):
        print("Ich habe mich eingeloggt")

    async def on_member_join(self):
        await member.create_dm()
        await member.dm_channel.send(
            "Herzlich Wikommen " + str(member.name) + " auf den Community Discord Server von gammagames")

    async def on_message(self, message):
        if message.content.startswith("start bot"):
            try:
                with open('oauth.txt', 'r') as f:
                    oauth = f.read()
            # Store OAuth in oauth.txt
            except FileNotFoundError:
                print("Paste your OAuth (like 'yaxb50....')")
                with open('oauth.txt', 'w') as f:
                    f.write(input())
                with open('oauth.txt', 'r') as f:
                    oauth = f.read()

            headers = {
                'Accept': 'application/vnd.twitchtv.v5+json',
                'Client-ID': 'dsv0rf69bvzgi9ch6ys16vwncjax1z',
                'Authorization': 'OAuth ' + oauth,
            }
            while True:
                try:
                    response = requests.get('https://api.twitch.tv/kraken/streams/followed', headers=headers)
                    data = response.json()
                except (KeyError, ValueError):
                    print("Error - make sure your OAuth is formatted correctly in oauth.txt")
                    sys.exit(1)
                print(data)
                numStreams = len(data['streams'])
                for i in range(0, numStreams):
                    name = data["streams"][i]["channel"]["name"]
                    game = data["streams"][i]["channel"]["game"]
                    viewers = str(data["streams"][i]["viewers"])
                    stream = data["streams"][i]["stream_type"]

                if stream == "live":
                    messages = (
                            name + " ist nun live und spielt " + game + " aktuell hat er " + viewers + " Zuschauer" + "\nhttps://www.twitch.tv/daannyy")
                    message = await message.channel.send(messages)
                    await asyncio.sleep(30)
                    await message.delete()


if __name__ == '__main__':
    bot = MyClient()
    bot.run("Your bot token")
