import json
import discord
from discord.message import Message
import config as conf
import logging
import commands.pihole as pi

# create logger
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

command = conf.get_setting("bani-command", "bani")

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

        if cmd == "pihole":
            status = pi.get_pihole_status_json()
            status = status['status']

            mess = f"""
```json
{status['dns_queries_today']} DNS queries today, where {status['ads_blocked_today']} were towards ads. 
{round(status['ads_percentage_today'] * 10.0) / 10.0}% of all requests were towards ads.
```
"""
            message.channel
            await message.channel.send(mess)
        

        #----------------------------
        if "die" in message.content:
            client.close()

client = MyClient()
logging.info("Running bot...")
client.run(conf.get_setting("token", ""))