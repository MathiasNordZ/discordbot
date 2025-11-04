import methods as mtd
from discord.ext import tasks
import urllib.request

"""
If tickets are listed but sold out

In bot startup put this
    if not message_if_tickets.is_running():
        message_if_tickets.start()
"""
@tasks.loop(seconds=30)
async def message_if_tickets(client, link):
    if mtd.check_for_tickets_when_sold_out(link) is True:
        await client.get_channel(1414953421982924810).send(
            f"@everyone Billetter for HALLOWEENFEST fest er nå ute {link}")
        message_if_tickets.stop()

"""
If the tickets are not listed on the website

In bot startup put this:
    if not check_for_tickets.is_running():
        check_for_tickets.start()
"""
@tasks.loop(seconds=30)
async def check_for_tickets(client, link):
    if b"Tilgjengelige varer" in urllib.request.urlopen(link).read():
        await client.get_channel(1414953421982924810).send(f"@everyone Billetter for HALLOWEENFEST fest er nå ute {link}")
        check_for_tickets.stop()