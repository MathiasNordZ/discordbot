# This example requires the 'message_content' intent.

import os
from dotenv import load_dotenv
import discord

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


print(f"TOKEN loaded: {token!r}")
client.run(token)