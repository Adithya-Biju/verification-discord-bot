from utility.payment import old_endpoint
from models import CustomerOld, Customer
from utility.update_queue import enqueue
from utility.embed import email_not_found, existing_embed, old_prem_embed
import discord 
from utility import constants


async def old_ver_validation(bot, user_id, interaction, email=None):
    email_check = await CustomerOld.filter(email=email).first()
    log_guild = bot.get_guild(constants.LOG_SERVER)
    log_channel = log_guild.get_channel(constants.VERIFY_LOG)

    # EMAIL TAKEN BY OTHER USER
    if email_check and email_check.user_id != user_id:
        return {
            "status": "email_taken",
            "embed": discord.Embed(title="EMAIL ADDRESS ALREADY REGISTERED", color=0x0000ff),
            "is_old": False,
            "is_new": False
        }

    # ALREADY VERIFIED (old exists)
    if await CustomerOld.get_or_none(user_id=user_id):
        return {
            "status": "already_verified",
            "embed": await existing_embed(),
            "is_old": True,
            "is_new": False
        }

    # HIT API
    if await old_endpoint(email):

        await Customer.update_or_create(
            user_id=user_id,
            defaults={"has_premium_old": True}
        )

        await CustomerOld.update_or_create(
            user_id=user_id,
            defaults={"email": email}
        )

        await enqueue(user_id)


        await log_channel.send(
            f"✅ **Old Premium Verified!**\nUser: {interaction.user.mention} : {user_id}\nEmail: `{email}`"
        )

        return {
            "status": "old_premium",
            "embed": await old_prem_embed(),
            "is_old": True,
            "is_new": False
        }

    return {
        "status": "none",
        "embed": await email_not_found(),
        "is_old": False,
        "is_new": False
    }
