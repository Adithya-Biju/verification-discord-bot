from models import Customer 
from utility.server_roles import role_updates
import discord

async def sync_roles(bot: discord.Client , user_id : int):

    if await Customer.get_or_none(user_id=user_id):
        await role_updates(bot, user_id)
        return "Roles synced"

    return "Do not have premium"