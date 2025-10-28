import os
import re

from discord import message
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


def pRep(message, user):
    emoji = discord.utils.get(message.guild.emojis, name="plussrep")
    if emoji is None:
        emoji = "👍"
    if user in ["Mathias", "Simen", "Odin", "Frikk", "Nick", "Joakim"]:
        return f"Plus rep to {user}! {emoji}"
    else:
        return f"User '{user}' not found! {emoji}"

def mRep(message, user):
    emoji = discord.utils.get(message.guild.emojis, name="minusrep")
    if emoji is None:
        emoji = "👎"
    if user in ["Mathias", "Simen", "Odin", "Frikk", "Nick", "Joakim"]:
        return f"Minus rep to {user}! {emoji}"
    else:
        return f"User '{user}' not found! {emoji}"