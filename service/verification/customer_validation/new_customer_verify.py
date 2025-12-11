from utility.payment import new_endpoint
from models import Customer
from utility.update_queue import enqueue
from utility.embed import email_not_found, new_prem_embed, existing_embed
import discord 
from utility import constants

async def new_ver_validation(bot, user_id, interaction, email=None):
    email_check = await Customer.filter(email=email).first()
    log_guild = bot.get_guild(constants.LOG_SERVER)
    log_channel = log_guild.get_channel(constants.VERIFY_LOG)

    # EMAIL TAKEN
    if email_check and email_check.user_id != user_id:
        return {
            "status": "email_taken",
            "embed": discord.Embed(title="EMAIL ADDRESS ALREADY REGISTERED", color=0x0000ff),
            "is_old": False,
            "is_new": False
        }

    # ALREADY VERIFIED (new or old)
    existing = await Customer.get_or_none(user_id=user_id)
    if existing:
        return {
            "status": "already_verified",
            "embed": await existing_embed(),
            "is_old": existing.has_premium_old,
            "is_new": existing.has_premium_new
        }

    # HIT API
    data = await new_endpoint(email)

    if not data:
        return {
            "status": "none",
            "embed": await email_not_found(),
            "is_old": False,
            "is_new": False
        }

    # NEW PREMIUM ACTIVE
    if len(data["subscriptions"]) > 0:
        await Customer.update_or_create(
            user_id=user_id,
            defaults={"has_premium_new": True, "email": email}
        )
        await enqueue(user_id)

        # Log
        await log_channel.send(
            f"✅ **New Premium Verified!**\nUser: {interaction.user.mention}\nEmail: `{email}`"
        )

        return {
            "status": "new_premium",
            "embed": await new_prem_embed(),
            "is_new": True,
            "is_old": False
        }

    # EMAIL EXISTS BUT NO SUBSCRIPTION
    await Customer.update_or_create(
        user_id=user_id,
        defaults={"email": email}
    )
    await enqueue(user_id)

    return {
        "status": "none",
        "embed": await email_not_found(),
        "is_old": False,
        "is_new": False
    }
