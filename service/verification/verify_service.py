from .customer_validation.old_customer_verify import old_ver_validation
from .customer_validation.new_customer_verify import new_ver_validation
import discord

async def validation(bot, interaction, user_id, username, email=None):

    new_res = await new_ver_validation(bot, user_id, username, email)
    old_res = await old_ver_validation(bot, user_id, username, email)

    # If BOTH return email taken → send email taken
    if new_res["status"] == "email_taken" and old_res["status"] == "email_taken":
        return await interaction.followup.send(embed=new_res["embed"], ephemeral=True)

    # If verified in BOTH → send existing verified embed
    if new_res["is_new"] and old_res["is_old"]:
        combined_embed = discord.Embed(
            description="Hello, you have been verified as a premium customer and granted access to priority support & other benefits.\n\nHave an amazing rest of your day! ❤️",
            color=0x00FF00
        )
        return await interaction.followup.send(embed=combined_embed, ephemeral=True)

    # If only NEW validated → send NEW
    if new_res["status"] == "new_premium":
        return await interaction.followup.send(embed=new_res["embed"], ephemeral=True)

    # If only OLD validated → send OLD
    if old_res["status"] == "old_premium":
        return await interaction.followup.send(embed=old_res["embed"], ephemeral=True)

    # If NOTHING validated → email not found
    if new_res["status"] == "none" and old_res["status"] == "none":
        return await interaction.followup.send(embed=new_res["embed"], ephemeral=True)
