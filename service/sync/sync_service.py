from models import Customer 
from utility.update_queue import enqueue
import discord

async def sync_roles(bot: discord.Client , user_id : int):

    if await Customer.get_or_none(user_id=user_id):
        await enqueue(user_id)
        return "Roles synced"

    return "Do not have premium"