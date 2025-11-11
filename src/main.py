# File: src/main.py
import os
import asyncio
import discord
from dotenv import load_dotenv
import datetime as td
import methods as mtd
from pathlib import Path

from src.methods import debug_ctftime

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
    activity = discord.Game(name=mtd.activity())
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
        mtd.increment_cmd_count(message.author)

        if "help" in command:
            await message.channel.send(mtd.help())
            mtd.log_command("help", message.author)

        elif "join" in command or "join" in content:
            if message.author.voice:
                channel = message.author.voice.channel
                voice_client = None
                try:
                    voice_client = await channel.connect()
                except Exception as e:
                    # If already connected elsewhere, try to move the bot
                    if message.guild and message.guild.voice_client:
                        voice_client = message.guild.voice_client
                        await voice_client.move_to(channel)
                    else:
                        await message.channel.send(f"❌ Could not connect to voice channel: {e}")
                        mtd.log_command("join_failed", message.author)
                        return

                await message.channel.send(f"🔊 Joined {channel.name}!")
                mtd.log_command("join", message.author)

                # Try to play a local wav file after joining
                wav_path = Path(__file__).resolve().parent / "sounds" / "iku2.mp3"
                print(f"Looking for audio at: {wav_path}")  # console debug

                if wav_path.exists():
                    try:
                        # ensure string path if mtd.play_wav expects it
                        await mtd.play_wav(voice_client, str(wav_path), disconnect_after=False)
                    except Exception as e:
                        await message.channel.send(f"⚠️ Failed to play audio: {e}")
                else:
                    await message.channel.send(f"Couldn't find the audio file at `{wav_path}`")
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

        elif "ping" in command:
            await message.channel.send(mtd.ping())
            mtd.log_command("ping", message.author)

        elif command.startswith("top10"):
            response = await asyncio.to_thread(mtd.top10_gap)
            await message.channel.send(response)
            mtd.log_command("top10", message.author)

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

        elif "cmdboard" in command:
            await message.channel.send(mtd.cmd_board())

        elif "debugctftime" in command:
            await message.channel.send("Debug: Running CTFtime fetch...")
            debug_ctftime()

        else:
            emoji = discord.utils.get(message.guild.emojis, name="minusrep")
            await message.add_reaction(emoji)
            mtd.decrement_cmd_count(message.author) #Possible race cond?
            mtd.log_command("unknown_command", message.author)



    # Standalone keyword checks
    if "keystrokers" in message.content.lower():
        await message.add_reaction("🔑")
        await message.add_reaction("👋")
        await message.add_reaction("💦")

    if "lolexec" in message.content.lower():
        await message.channel.send("https://cdn.discordapp.com/attachments/1414944813031231611/1437047515894775929/3dgifmaker78214.gif")

print(f"TOKEN loaded: {token!r}")
client.run(token)
