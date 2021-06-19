import json
import discord
from discord.message import Message
import config as conf
import logging
import commands.pihole as pi

# create logger
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

command = conf.get_setting("bani-command", "bani")

cmds = {
    "pihole": pi.get_pihole_status_json
}

class MyClient(discord.Client):
    async def on_ready(self):
        logging.info(f"Successfully logged in as {self.user}")

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
        if "die" in message.content:
            client.close()

client = MyClient()
logging.info("Running bot...")
client.run(conf.get_setting("token", ""))