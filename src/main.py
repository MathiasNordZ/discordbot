import os

from discord.ext import tasks
from dotenv import load_dotenv
import discord
import subprocess
import base64
import datetime as td
import urllib.request

load_dotenv()
token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
link = "https://huset.ticketco.events/no/nb/e/halloweenfest__huset"

@tasks.loop(seconds=20)
async def check_for_tickets():
    if b"Tilgjengelige varer" in urllib.request.urlopen(link).read():
        await client.get_channel(1414953421982924810).send(f"@everyone Billetter for HALLOWEENFEST fest er nå ute {link}")
        check_for_tickets.stop()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    if not check_for_tickets.is_running():
        check_for_tickets.start()
    channel = client.get_channel(1427570847241207910)  # replace with your channel id
    if channel:
        await channel.send('Bot is now online!')
    activity = discord.Game(name="Stroking...")
    await client.change_presence(activity=activity)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    raw = message.content
    content = raw.lower().strip()

    # Trigger: messages starting with "key"
    if content.startswith("key "):
        command = content[len("key "):].strip()

        if "halloween" in command:
            if b"Tilgjengelige varer" in urllib.request.urlopen(link).read():
                await message.channel.send(f"Tickets available at {link}")
            else:
                await message.channel.send("No tickets yet!")

        if "join" in command or "join" in content:
            if message.author.voice:
                channel = message.author.voice.channel
                await channel.connect()
                await message.channel.send(f"🔊 Joined {channel.name}!")
            else:
                await message.channel.send("❌ You need to be in a voice channel first!")

        elif "leave" in command:
            if message.guild and message.guild.voice_client:
                await message.guild.voice_client.disconnect()
                await message.channel.send("👋 Left the voice channel.")
            else:
                await message.channel.send("❌ I'm not in a voice channel.")

        elif "update bot" in command:
            await message.channel.send("Updating bot...")
            subprocess.run(["./roll-out.sh"])

        elif "test bot" in command:
            await message.channel.send("Updating to test suite...")
            subprocess.run(["./testing.sh"])


        elif command.startswith("base64"):
            message_bytes = base64.b64decode(message.content[6:].strip())
            await message.channel.send(f"Decoded base64: {message_bytes.decode('utf-8', errors='ignore')}")

        elif "ept" in message.content.lower():
            event_date = td.datetime(2025, 11, 8)
            now = td.datetime.now()
            delta = event_date - now
            days, seconds = delta.days, delta.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            await message.channel.send(f"Time until EPT CTF: {days} days, {hours} hours, and {minutes} minutes.")

    # Standalone keyword checks
    if "keystrokers" in message.content.lower():
        await message.add_reaction("🔑")
        await message.add_reaction("👋")
        await message.add_reaction("💦")

print(f"TOKEN loaded: {token!r}")
client.run(token)