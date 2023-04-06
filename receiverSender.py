import websockets
import json
import sys
from twitchio.ext import commands


CHANNEL = "Replace with the name of the twitch channel"
KICK_CHATROOM_ID = "Replace this with the ID of the kick chatroom"

TOKEN = ""
# get token from token.txt file
with open("token.txt", "r") as f:
    TOKEN = f.readline()


class Bot(commands.Bot):
    def __init__(self):
        """initial connection with specified token"""
        super().__init__(
            token=TOKEN,
            prefix="?",
            initial_channels=[CHANNEL],
        )

    async def event_ready(self):
        """Start the chat bot"""
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")

        while True:
            try:
                await self.connectToChat()
            except KeyboardInterrupt:
                await sys.exit()
            except:
                pass

    async def send_to_chat(self, message: str):
        # get the channel from the bots init cache
        channel = self.get_channel(CHANNEL)
        # send the message
        await channel.send(message)

    async def connectToChat(self):
        # get kick chat
        async with websockets.connect(
            "ws://ws-us2.pusher.com/app/eb1d5f283081a78b932c?protocol=7"
        ) as websocket:
            # get specified channel chat chatroom
            await websocket.send(
                '{"event":"pusher:subscribe","data":{"auth":"","channel":"chatrooms.'
                + KICK_CHATROOM_ID
                + '"}}'
            )
            while True:
                await self.processmsg(await websocket.recv())

    async def processmsg(self, msg: str):
        msg = json.loads(msg)
        if "ChatMessageSentEvent" in msg["event"]:
            data = json.loads(msg["data"])

            # seperate the message from data
            message = data["message"]["message"]

            # if command in defined lumia commands
            if message[0] == "!":
                commands = [
                    "red",
                    "green",
                    "blue",
                    "pink",
                    "purple",
                    "aqua",
                    "orange",
                    "yellow",
                    "flash",
                    "police",
                    "rgb",
                    "hex",
                    "color",
                    "random",
                    "usa",
                    "rip",
                    "dub",
                    "flashbang",
                    "shots",
                    "goavsgo",
                    "nam",
                    "wild",
                    "wompwomp",
                    "nuke",
                    "blitz",
                    "pbf",
                    "hector",
                ]
                if message[1:] in commands:
                    await self.send_to_chat(message)


bot = Bot()
bot.run()
