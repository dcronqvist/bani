import json
from typing import Text
import discord
from discord.abc import GuildChannel
from discord.channel import TextChannel
from discord.message import Message
import config as conf
import logging
import commands.pihole as pi
import discord.ext.commands as commands
import random as rand

# create logger
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

command = conf.get_setting("bani-command", "bani")

cmds = {
    "pihole": pi.get_pihole_status_json
}

def get_random_emoji():
    return rand.choice([
        ":duck:",
        ":dodo:",
        ":bird:",
        ":baby_chick:"
    ])

version = "v0.1-alpha"
class MyClient(discord.Client):

    async def on_ready(self):
        logging.info(f"Successfully logged in as {self.user}")

        for guild in self.guilds:
            for channel in guild.channels:
                if type(channel) is TextChannel:
                    if channel.permissions_for(channel.guild.me).send_messages == True:
                        await channel.send(f"🤖 `{command}` is ready to go! running version `{version}` {get_random_emoji()}")
                        logging.info(f"Announced in {channel} in {guild}")
            

    async def on_message(self, message : Message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if not message.content.startswith(command):
            return

        cmd = message.content[len(command) + 1:]

        logging.info(f"{message.author.display_name} sent message: {message.content}")
        #---------------------------

        run = cmds.get(cmd, None)

        if run:
            await run(message)

        #----------------------------

client = MyClient()
logging.info("Running bot...")
client.run(conf.get_setting("token", ""))