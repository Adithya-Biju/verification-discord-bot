from models import Server, Customer
import discord
from settings import logging
import asyncio

logger = logging.getLogger("bot")

async def role_updates(bot: discord.client ,user_id: int):

    server_details = await Server.all().values("server_id","old_role_id", "new_role_id")
    user_details = await Customer.all().values("has_premium_old","has_premium_new")

    try: 

    
        for server in server_details:

            guild = bot.get_guild(server["server_id"])
            if not guild:
                logger.warning(f"Bot not in guild {server['server_id']}")
                continue

            guild = bot.get_guild(server["server_id"])
            member = guild.get_member(user_id)
            
            if not member:
                try:
                    member = await guild.fetch_member(user_id)
                except discord.NotFound:
                    logger.warning(f"User {user_id} not found in guild {guild.name}")
                    continue
                except discord.Forbidden:
                    logger.error(f"Missing permissions to fetch members in {guild.name}")
                    continue

            old_role = guild.get_role(server["old_role_id"])
            new_role = guild.get_role(server["new_role_id"])

            try:
                if user_details[0]['has_premium_old'] and old_role and old_role not in member.roles:
                    await member.add_roles(old_role, reason="EXM 1.3 verification completed")
                    logger.info(f"Added old premium to {member} in {guild.name}")

                if user_details[0]["has_premium_new"] and new_role and new_role not in member.roles:
                    await member.add_roles(new_role, reason="EXM 2.0 subscription active")
                    logger.info(f"Added new premium to {member} in {guild.name}")

            except discord.HTTPException as e:
                logger.error(f"HTTP error updating roles for {member} in {guild.name}: {e}")

            await asyncio.sleep(0.5) 
        
    except Exception as e:
        logger.exception(f"Unhandled error in subcription_status role_updates for user {user_id}: {e}")