import os
import re
import json
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

FILE_PATH = "data/rep.json"


def help():
    helpText = ("Use key as keyword to get started!   eks: key ept\n\n\nept: Shows time until the EPT CTF\n\nbase64: Use base64 xxxx== to decode base64 directly\n \nsem_goon: Shows the sem goon pipeline\n\nhuzz: Shows the huzz\n\n\nupdate/test bot pulls most recent version in either main or testing branch")

    return helpText
def _fetch_html_str(link):
    data = urllib.request.urlopen(link).read()
    return data.decode("utf-8", errors="ignore")

def check_for_tickets_when_sold_out(link):
    html = _fetch_html_str(link)
    parts = re.split(r'(?=<div id="item_type_\d+")', html)
    if "data-available-amount='0'" not in parts[1] or "data-available-amount='0'" not in parts[3]:
        return True
    else:
        return False

def biletter(link):
    if b"Tilgjengelige varer" in urllib.request.urlopen(link).read():
        return(f"Tickets available at {link}")
    else:
        return ("No tickets yet!")

def updateBot():
    subprocess.run(["./roll-out.sh"])

def testBot():
    subprocess.run(["./testing.sh"])

def b64(content):
    message_bytes = base64.b64decode(content)
    return (f"Decoded base64: {message_bytes.decode('utf-8', errors='ignore')}")

def ept():
    event_date = td.datetime(2025, 11, 8, 9)
    now = td.datetime.now()
    delta = event_date - now
    days, seconds = delta.days, delta.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return (f"Time until EPT CTF: {days} days, {hours} hours, and {minutes} minutes.")

def eptShort():
    event_date = td.datetime(2025, 11, 8, 9)
    now = td.datetime.now()
    delta = event_date - now
    days, seconds = delta.days, delta.seconds
    return (f"EPT in: {days} days")


# -------------------------------
# JSON Handling
# -------------------------------

def load_reps():
    """Load reputation data from JSON file."""
    if not os.path.exists(FILE_PATH):
        # Make sure the folder exists
        os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
        return {}

    with open(FILE_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}  # In case the file is empty or corrupted


def save_reps(data):
    """Save reputation data to JSON file."""
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)


# -------------------------------
# Reputation Commands
# -------------------------------

def pRep(message, user):
    if user == message.author:
        return "❌ You cannot give reputation to yourself!"
    elif user in ["Simen", "Frikk", "Mathias", "Odin", "Joakim", "Nick", "Arpit"]:
        """Give +1 reputation to a user."""
        emoji = discord.utils.get(message.guild.emojis, name="plusrep")
        if emoji is None:
            emoji = "👍"

        reps = load_reps()

        # Update user’s score (case-insensitive)
        user_key = user.capitalize()
        reps[user_key] = reps.get(user_key, 0) + 1

        save_reps(reps)

        return f"✅ Gave +1 rep to **{user_key}**! Total: **{reps[user_key]}** {emoji}"
    else:
        return "❌ You can only give reputation to Simen, Frikk, Mathias, Odin, Joakim, Arpit, or Nick!"


def mRep(message, user):
    if user == message.author:
        return "❌ You cannot give reputation to yourself!"
    elif user in ["Simen", "Frikk", "Mathias", "Odin", "Joakim", "Nick"]:

        emoji = discord.utils.get(message.guild.emojis, name="plusrep")
        if emoji is None:
            emoji = "👍"

        reps = load_reps()

        # Update user’s score (case-insensitive)
        user_key = user.capitalize()
        reps[user_key] = reps.get(user_key, 0) - 1

        save_reps(reps)

        return f"⚠️ Gave -1 rep to **{user_key}**! Total: **{reps[user_key]}** {emoji}"
    else:
        return "❌ You can only give reputation to Simen, Frikk, Mathias, Odin, Joakim, or Nick!"



# -------------------------------
# Utility Command (optional)
# -------------------------------

def getLeaderboard(limit=10):
    """Return a formatted string of the top rep users."""
    reps = load_reps()

    if not reps:
        return "No reputation data yet!"

    # Sort by score (highest first)
    sorted_users = sorted(reps.items(), key=lambda x: x[1], reverse=True)

    leaderboard = "**🏆 Reputation Leaderboard 🏆**\n"
    for i, (user, score) in enumerate(sorted_users[:limit], start=1):
        leaderboard += f"{i}. **{user}** — {score} points\n"

    return leaderboard