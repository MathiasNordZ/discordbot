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
    channel = client.get_channel(1427570847241207910)  # replace with your
    await channel.send('Bot is now online!')
    activity = discord.Game(name="Stroking...")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Checks if a message starts with stroke
    # Stroke is a keyword that triggers the bot to respond
    # The bot will then process the rest of the message
    if "key" in message.content.startswith.lower():
        command = message.content[len("key"):].strip()

        if "join" in command or "keystrokers" in message.content.lower():
            if message.author.voice:  # user is in a voice channel
                channel = message.author.voice.channel
                await channel.connect()
                await message.channel.send(f"🔊 Joined {channel.name}!")
            else:
                await message.channel.send("❌ You need to be in a voice channel first!")

        elif "leave" in command.lower():
            if message.guild.voice_client:
                await message.guild.voice_client.disconnect()
                await message.channel.send("👋 Left the voice channel.")
            else:
                await message.channel.send("❌ I'm not in a voice channel.")

        elif "update bot" in command.lower():
            await message.channel.send("Updating bot...")
            subprocess.run("./roll-out.sh")

        elif "test bot" in command.lower():
            await message.channel.send("Updating to test suite...")
            subprocess.run("./testing.sh")

        elif command.startswith("base64"):
            message_bytes = base64.b64decode(message.content[6:].strip())

            await message.channel.send(message_bytes)


    elif "keystrokers" in message.content.lower():
        await message.add_reaction("🔑")
        await message.add_reaction("👋")
        await message.add_reaction("💦")

print(f"TOKEN loaded: {token!r}")
client.run(token)