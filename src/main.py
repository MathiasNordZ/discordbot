import os

from discord.ext import tasks
from dotenv import load_dotenv
import discord
import subprocess
import base64
import datetime as td
import urllib.request
import methods as mtd

load_dotenv()
token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

link = "https://huset.ticketco.events/no/nb/e/halloweenfest__huset"

"""
If tickets are listed but sold out
"""
@tasks.loop(seconds=30)
async def message_if_tickets():
    if mtd.check_for_tickets_when_sold_out(link) is True:
        await client.get_channel(1414953421982924810).send(
            f"@everyone Billetter for HALLOWEENFEST fest er nå ute {link}")
        message_if_tickets.stop()

"""
If the tickets are not listed on the website
"""
@tasks.loop(seconds=30)
async def check_for_tickets():
    if b"Tilgjengelige varer" in urllib.request.urlopen(link).read():
        await client.get_channel(1414953421982924810).send(f"@everyone Billetter for HALLOWEENFEST fest er nå ute {link}")
        check_for_tickets.stop()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    if not message_if_tickets.is_running():
        message_if_tickets.start()
    channel = client.get_channel(1427570847241207910)  # replace with your channel id
    if channel:
        await channel.send('Bot is now online!')
    activity = discord.Game(name=mtd.eptShort())
    await client.change_presence(activity=activity)

    event_time = td.datetime(2025, 10, 31, 13, 0)
    channel_id = 1414953421982924810  # Replace with your channel's ID

    # Schedule the reminder
    client.loop.create_task(mtd.schedule_ctf_reminder(channel_id, event_time))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    raw = message.content
    content = raw.lower().strip()

    # Trigger: messages starting with "key"
    if content.startswith("key "):
        command = content[len("key "):].strip()

        if "help" in command:
            await message.channel.send(mtd.help())

        elif "halloween" in command:
            if mtd.check_for_tickets_when_sold_out(link) is True:
                await message.channel.send(f"Tickets available at {link}")
            else:
                await message.channel.send("No tickets yet!")

        elif "join" in command or "join" in content:
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
            mtd.updateBot() #Må kalles her fordi return må være sist i en metode og scriptet dreper prosessen så den kjører aldri message send....

        elif "test bot" in command:
            await message.channel.send("Updating bot to test suite...")
            mtd.testBot() #Må kalles her fordi return må være sist i en metode og scriptet dreper prosessen så den kjører aldri message send....

        elif command.startswith("base64"):
            await message.channel.send(mtd.b64(message.content[10:].strip()))

        elif "ept" in message.content.lower():
            await message.channel.send(mtd.ept())

        elif "sem_goon" in message.content.lower():
            await message.channel.send("sem_init()")
            await message.channel.send("sem_wait()")
            await message.channel.send("sem_post()")
            await message.channel.send("💦💦💦")

        elif "huzz" in message.content.lower():
            await message.channel.send("https://cdn.discordapp.com/attachments/1276515217517318178/1428704557571244092/tenor.gif")


        elif command.startswith("+rep "):
            user = message.content[9:].strip()
            await message.channel.send(mtd.pRep(message, user))

        elif command.startswith("-rep "):
            user = message.content[9:].strip()
            await message.channel.send(mtd.mRep(message, user))

        elif "repboard" in command:
            await message.channel.send(mtd.getLeaderboard())
        else:
            emoji = discord.utils.get(message.guild.emojis, name="minusrep")
            await message.add_reaction(emoji)

    # Standalone keyword checks
    if "keystrokers" in message.content.lower():
        await message.add_reaction("🔑")
        await message.add_reaction("👋")
        await message.add_reaction("💦")

print(f"TOKEN loaded: {token!r}")
client.run(token)