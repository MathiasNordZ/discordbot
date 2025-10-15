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

print(f"TOKEN loaded: {token!r}")
client.run(token)