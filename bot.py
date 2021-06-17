import discord
from discord.message import Message
import config as conf
import requests
import logging

# create logger
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

class MyClient(discord.Client):
    async def on_ready(self):
        logging.info(f"Successfully logged in as {self.user}")

    async def on_message(self, message : Message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if not message.content.startswith("bani"):
            return

        logging.info(f"{message.author.display_name} sent message: {message.content}")

        if message.author.display_name == "danc":
            await message.channel.send('pong')

        if "die" in message.content:
            client.close()

client = MyClient()
logging.info("Running bot...")
client.run(conf.get_setting("token", ""))