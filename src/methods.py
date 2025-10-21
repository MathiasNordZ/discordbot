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

def help():
    helpText = ("Use key as keyword to get started!   eks: key ept\n    ept: Shows time until the EPT CTF\n    base64: Use base64 xxxx== to decode base64 directly\n   sem_goon: Shows the sem goon pipeline\n  huzz: Shows the huzz\n \n   update/test bot pulls most recent version in either main or testing branch")

    return helpText


def biletter():
    if b"Tilgjengelige varer" in urllib.request.urlopen(link).read():
        return(f"Tickets available at {link}")
    else:
        return ("No tickets yet!")

def updateBot():
    subprocess.run(["./roll-out.sh"])

def testBot():
    subprocess.run(["./testing.sh"])

def base64(content):
    message_bytes = base64.b64decode(content)
    return (f"Decoded base64: {message_bytes.decode('utf-8', errors='ignore')}")

def ept():
    event_date = td.datetime(2025, 11, 8, 10)
    now = td.datetime.now()
    delta = event_date - now
    days, seconds = delta.days, delta.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return (f"Time until EPT CTF: {days} days, {hours} hours, and {minutes} minutes.")

def eptShort():
    event_date = td.datetime(2025, 11, 8, 10)
    now = td.datetime.now()
    delta = event_date - now
    days, seconds = delta.days, delta.seconds