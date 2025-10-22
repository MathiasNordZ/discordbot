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


def check_for_tickets_when_sold_out(link, ticket_id_type_1, ticket_id_type_2, ticket_type_id_3):
    html = urllib.request.urlopen(link).read()
    tickets = html.split(ticket_id_type_1, ticket_id_type_2, ticket_type_id_3)
    if b"data-available-amount='{0}'" not in tickets[1] or tickets[3]:
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