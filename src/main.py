# This example requires the 'message_content' intent.

import os
from dotenv import load_dotenv
import discord
import subprocess
import base64

load_dotenv()
token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "keystrokers" in message.content.lower():
        await message.add_reaction("🔑")
        await message.add_reaction("👋")

    if "stroke" in message.content.lower():
        await message.channel.send('Currently stroking...')

    if "join" in message.content.lower():
        if message.author.voice:  # user is in a voice channel
            channel = message.author.voice.channel
            await channel.connect()
            await message.channel.send(f"🔊 Joined {channel.name}!")
        else:
            await message.channel.send("❌ You need to be in a voice channel first!")

        # Leave voice channel
    elif "leave" in message.content.lower():
        if message.guild.voice_client:
            await message.guild.voice_client.disconnect()
            await message.channel.send("👋 Left the voice channel.")
        else:
            await message.channel.send("❌ I'm not in a voice channel.")

    if "update bot" in message.content.lower():
        await message.channel.send("Updating bot...")
        subprocess.run("./roll-out.sh")

    if "test bot" in message.content.lower():
        await message.channel.send("Updating to test suite...")
        subprocess.run("./testing.sh")


    if message.content.startswith("base64"):
        message_bytes = base64.b64decode(message.content[6:].strip())
        message_string = message_bytes[2:-1]
        message_string = message_string[2:-1]

        await message.channel.send(message_string)

print(f"TOKEN loaded: {token!r}")
client.run(token)