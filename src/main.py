# File: src/main.py
import os
import discord
from dotenv import load_dotenv
import datetime as td
import methods as mtd

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
    activity = discord.Game(name=mtd.eptShort())
    await client.change_presence(activity=activity)

    # Ensure the bot is fully ready before scheduling the reminder
    ept_time = td.datetime(2025, 11, 8, 9)
    ept_reminder_time = td.datetime(2025, 11, 7, 9)
    channel_id = 1414953421982924810  # Replace with your channel's ID

    # Pass the client instance to the method
    await mtd.schedule_ctf_reminder(client, channel_id, ept_time)
    await mtd.schedule_ctf_reminder(client, channel_id, ept_reminder_time)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    raw = message.content
    content = raw.lower().strip()

    # Trigger: messages starting with "key"
    if content.startswith("exec "):
        command = content[len("exec "):].strip()

        if "help" in command:
            await message.channel.send(mtd.help())
            mtd.log_command("help", message.author)

        elif "join" in command or "join" in content:
            if message.author.voice:
                channel = message.author.voice.channel
                await channel.connect()
                await message.channel.send(f"🔊 Joined {channel.name}!")
                mtd.log_command("join", message.author)
            else:
                await message.channel.send("❌ You need to be in a voice channel first!")
                mtd.log_command("join_failed", message.author)

        elif "leave" in command:
            if message.guild and message.guild.voice_client:
                await message.guild.voice_client.disconnect()
                await message.channel.send("👋 Left the voice channel.")
                mtd.log_command("leave", message.author)
            else:
                await message.channel.send("❌ I'm not in a voice channel.")
                mtd.log_command("leave_failed", message.author)

        elif "update bot" in command:
            await message.channel.send("Updating bot...")
            mtd.log_command("update bot", message.author)
            mtd.updateBot() #Må kalles her fordi return må være sist i en metode og scriptet dreper prosessen så den kjører aldri message send....

        elif "test bot" in command:
            await message.channel.send("Updating bot to test suite...")
            mtd.log_command("test bot", message.author)
            mtd.testBot() #Må kalles her fordi return må være sist i en metode og scriptet dreper prosessen så den kjører aldri message send....

        elif command.startswith("base64"):
            await message.channel.send(mtd.b64(message.content[10:].strip()))
            mtd.log_command("base64", message.author)

        elif "ept" in message.content.lower():
            await message.channel.send(mtd.ept())
            mtd.log_command("ept", message.author)

        elif "sem_goon" in message.content.lower():
            await message.channel.send("sem_init()")
            await message.channel.send("sem_wait()")
            await message.channel.send("sem_post()")
            await message.channel.send("💦💦💦")
            mtd.log_command("sem_goon", message.author)

        elif "huzz" in message.content.lower():
            await message.channel.send("https://cdn.discordapp.com/attachments/1276515217517318178/1428704557571244092/tenor.gif")
            mtd.log_command("huzz", message.author)


        elif command.startswith("+rep "):
            user = message.content[9:].strip()
            await message.channel.send(mtd.pRep(message, user))
            mtd.log_command("+rep", message.author)

        elif command.startswith("-rep "):
            user = message.content[9:].strip()
            await message.channel.send(mtd.mRep(message, user))
            mtd.log_command("-rep", message.author)

        elif "repboard" in command:
            await message.channel.send(mtd.getLeaderboard())
            mtd.log_command("repboard", message.author)
        else:
            emoji = discord.utils.get(message.guild.emojis, name="minusrep")
            await message.add_reaction(emoji)
            mtd.log_command("unknown_command", message.author)

    # Standalone keyword checks
    if "keystrokers" in message.content.lower():
        await message.add_reaction("🔑")
        await message.add_reaction("👋")
        await message.add_reaction("💦")

print(f"TOKEN loaded: {token!r}")
client.run(token)