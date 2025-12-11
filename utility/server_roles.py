from models import Server, Customer
import discord
import asyncio
from utility import constants


async def role_updates(bot: discord.Client, user_id: int):
    
    log_guild = bot.get_guild(constants.LOG_SERVER)

    if not log_guild:
        try:
            log_guild = await bot.fetch_guild(constants.LOG_SERVER)
        except discord.NotFound:
            print(f"[ERROR] Guild {constants.LOG_SERVER} not found.")
            return
        except discord.Forbidden:
            print(f"[ERROR] Bot doesn't have permission to access the guild {constants.LOG_SERVER}.")
            return
    log_channel = log_guild.get_channel(constants.ROLE_LOG)

    server_details = await Server.all().values("server_id","old_role_id", "new_role_id","main_premium_role")
    user_details = await Customer.get(user_id=user_id).values("has_premium_old","has_premium_new")

    try:
        for server in server_details:

            guild = bot.get_guild(server["server_id"])
            if not guild:
                continue

            member = guild.get_member(user_id)
            if not member:
                try:
                    member = await guild.fetch_member(user_id)
                except discord.NotFound:
                    continue
                except discord.Forbidden:
                    continue

            old_role = guild.get_role(server["old_role_id"])
            new_role = guild.get_role(server["new_role_id"])
            main_role = guild.get_role(server["main_premium_role"])

            try:
                # OLD PREMIUM ROLE
                if user_details["has_premium_old"]:
                    if old_role and old_role not in member.roles:
                        await member.add_roles(old_role, reason="EXM 1.3 verification completed")
                        await log_channel.send(f"🟢 Added **OLD Premium** to **{member.name}** : {user_id} in **{guild.name}**")
                else:
                    if old_role and old_role in member.roles:
                        await member.remove_roles(old_role, reason="EXM 1.3 premium removed")
                        await log_channel.send(f"🔴 Removed **OLD Premium** from **{member.name}** : {user_id} in **{guild.name}**")

                # NEW PREMIUM ROLE
                if user_details["has_premium_new"]:
                    if new_role and new_role not in member.roles:
                        await member.add_roles(new_role, reason="EXM 2.0 subscription active")
                        await log_channel.send(f"🟢 Added **NEW Premium** to **{member.name}** : {user_id} in **{guild.name}**")
                else:
                    if new_role and new_role in member.roles:
                        await member.remove_roles(new_role, reason="EXM 2.0 premium removed")
                        await log_channel.send(f"🔴 Removed **NEW Premium** from **{member.name}** : {user_id} in **{guild.name}**")

                # MAIN PREMIUM ROLE
                if user_details["has_premium_old"] or user_details["has_premium_new"]:
                    if main_role and main_role not in member.roles:
                        await member.add_roles(main_role, reason="EXM premium active")
                        await log_channel.send(f"🟢 Added **MAIN Premium** to **{member.name}** : {user_id} in **{guild.name}**")
                else:
                    if main_role and main_role in member.roles:
                        await member.remove_roles(main_role, reason="No EXM premium active")
                        await log_channel.send(f"🔴 Removed **MAIN Premium** from **{member.name}** : {user_id} in **{guild.name}**")

            except discord.HTTPException as e:
                print(f"HTTP error updating roles for {member} in {guild.name}: {e}")

            await asyncio.sleep(0.5)

    except Exception as e:
        print(f"Unhandled error updating roles for user {user_id}: {e}")
