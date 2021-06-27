import json
from typing import Text
import discord
from discord.abc import GuildChannel
from discord.channel import TextChannel
from discord.message import Message
import config as conf
import logging
import discord.ext.commands as commands
import random as rand
from commands.pihole import get_pihole_status_json
import commands.api_requests as ar

# create logger
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
version = "v0.2-alpha"
command = conf.get_setting("bani-command", "bani")
def get_random_emoji():
    return rand.choice([
        ":duck:",
        ":dodo:",
        ":bird:",
        ":baby_chick:",
        ":dog:"
    ])

@ar.use_token
async def get_version(message):
    mess = f"""
`{command} is running version {version}!` {get_random_emoji()}
"""
    await message.channel.send(mess)

cmds = {
    "pihole": get_pihole_status_json,
    "version": get_version
}


class MyClient(discord.Client):

    async def on_ready(self):
        logging.info(f"Successfully logged in as {self.user}")

        for guild in self.guilds:
            for channel in guild.channels:
                if type(channel) is TextChannel:
                    if channel.permissions_for(channel.guild.me).send_messages == True and command == "bani":
                        await channel.send(f"🤖 `{command}` is ready to go! running version `{version}` {get_random_emoji()}")
                        logging.info(f"Announced in {channel} in {guild}")
            

    async def on_message(self, message : Message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if not message.content.startswith(command):
            return

        if not message.author.display_name == "dnl":
            await message.channel.send("you are not dani!! shat ap!! >:(")
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