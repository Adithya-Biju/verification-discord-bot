import discord 
from discord.ext import commands
from discord import app_commands
import settings
import asyncio
from utility import key,constants
from service import find_the_key
from models import StoreKey

class Keys(commands.Cog):

    def __init__(self,bot:commands.Bot):

        self.bot = bot
        self.bot.remove_command("help")

    @app_commands.command(name='premium_key', description='Sends the premium key in DMs')
    async def premium_key(self, interaction: discord.Interaction, member: discord.Member):

        await interaction.response.defer(ephemeral=True)

        log_guild = self.bot.get_guild(constants.LOG_SERVER)
        log_channel = log_guild.get_channel(constants.KEY_LOG)

        # Permission check
        if not interaction.user.guild_permissions.administrator:
            return await interaction.followup.send("You do not have permission.", ephemeral=True)

        # Get a new key
        generated_key = await key.premium_key()
        if not generated_key:
            return await interaction.followup.send("Key service is down.", ephemeral=True)

        # Attempt to DM user
        try:
            dm = await member.create_dm()
            await dm.send(f"""**Your EXM PREMIUM Key:**

`{generated_key}`

This key is locked to one HWID.
""")

            # Log success
            await interaction.followup.send("Key sent successfully.", ephemeral=True)

            # Log in staff-log channel
            await asyncio.sleep(1)
            await log_channel.send(
                f"{member.mention} received a Premium key.\n"
                f"**Key:** `{generated_key}`\n\n"
                f"Issued by: {interaction.user.mention}"
            )

            # STORE INTO DATABASE
            await StoreKey.create(
                user_id=member.id,
                key=generated_key,
                mod_id=interaction.user.id,
                mod_name=str(interaction.user),
            )

        except discord.Forbidden:
            await interaction.followup.send("User's DMs are closed.", ephemeral=True)

        except Exception as e:
            print("Error:", e)
            await interaction.followup.send("Unexpected error occurred.", ephemeral=True)


   
    @app_commands.command(name='missing_key', description='Check stored keys')
    async def missing_key(self, interaction: discord.Interaction, member: discord.Member = None):

        await interaction.response.defer(ephemeral=True)

        target = member or interaction.user

        if member and member != interaction.user and not interaction.user.guild_permissions.administrator:
            return await interaction.followup.send("You cannot check another user's keys.", ephemeral=True)

        key_record = await find_the_key(target.id)
        await interaction.followup.send(key_record, ephemeral=True)



async def setup(bot):
        await bot.add_cog(Keys(bot))
                                                  