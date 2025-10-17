import os
from dotenv import load_dotenv
import discord
import subprocess
import base64
import datetime as td

load_dotenv()
token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
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
            b64_payload = raw[len("base64"):].strip()
            try:
                message_bytes = base64.b64decode(b64_payload)
                try:
                    decoded = message_bytes.decode("utf-8")
                    await message.channel.send(decoded)
                except Exception:
                    await message.channel.send(f"Decoded bytes: {message_bytes!r}")
            except Exception as e:
                await message.channel.send(f"Base64 decode error: {e}")

        #shows time until EPT CTF 8.nov 2025
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
