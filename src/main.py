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

async def keystrokersReact(message):
    await message.add_reaction("🔑")
    await message.add_reaction("👋")

async def sendStrokingMessage(message):
    await message.channel.send('Currently stroking...')

async def joinVoice(message):
    if message.author.voice:  # user is in a voice channel
        channel = message.author.voice.channel
        await channel.connect()
        await message.channel.send(f"🔊 Joined {channel.name}!")
    else:
        await message.channel.send("❌ You need to be in a voice channel first!")

async def leaveVoice(message):
    if message.guild.voice_client:
        await message.guild.voice_client.disconnect()
        await message.channel.send("👋 Left the voice channel.")
    else:
        await message.channel.send("❌ I'm not in a voice channel.")

async def updateBot(message):
    await message.channel.send("Updating bot...")
    subprocess.run("./roll-out.sh")

async def testBot(message):
    await message.channel.send("Updating to test suite...")
    subprocess.run("./testing.sh")

async def decryptBase64(b64_payload, message):
    try:
        message_bytes = base64.b64decode(b64_payload)
        try:
            decoded = message_bytes.decode("utf-8")
            await message.channel.send(decoded)
        except Exception:
            await message.channel.send(f"Decoded bytes: {message_bytes!r}")
    except Exception as e:
        await message.channel.send(f"Base64 decode error: {e}")


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

    raw = message.content
    content = raw.lower().strip()
    command = content[len("key "):].strip()

    if content.startswith("key "):
        command.cotent.lower = {
            "stroke": sendStrokingMessage(message),
            "join": joinVoice(message),
            "leave": leaveVoice(message),
            "update bot": updateBot(message),
            "test bot": testBot(message)
    }
    elif "keystrokers" in message:
        await keystrokersReact(message)
    elif content.satswith("base64 "):
        b64_payload = raw[len("base64"):].strip()
        await decryptBase64(b64_payload, message)


    message.content.lower = {
        "keystrokers": keystrokersReact(message),
    }


    if message.content.startswith("base64"):
        message_bytes = base64.b64decode(message.content[6:].strip())

        await message.channel.send(message_bytes)

print(f"TOKEN loaded: {token!r}")
client.run(token)