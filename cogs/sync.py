import discord
from discord.ext import commands
from discord import app_commands
from utility.server_roles import role_updates
from service.sync.sync_service import sync_roles

class SyncRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @app_commands.checks.cooldown(1, 10.0)
    @app_commands.command(name="sync", description="Sync your EXM Premium roles")
    async def sync(self, interaction: discord.Interaction, member: discord.Member = None):
        await interaction.response.defer(ephemeral=True)

        target = member or interaction.user

        if member and member != interaction.user and not interaction.user.guild_permissions.administrator:
            return await interaction.followup.send("You do not have permission to sync other users.", ephemeral=True)
        
        await sync_roles(self.bot, target.id)

        msg = "Your roles have been synced." if target == interaction.user else f"Roles for {target.display_name} have been synced."
        
        await interaction.followup.send(f"✅ {msg}", ephemeral=True)
    
    @sync.error
    async def sync_error(self, interaction: discord.Interaction, error):

        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                f"⏳ Slow down! You can use this command again in **{error.retry_after:.1f} seconds**.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "⚠️ An unexpected error occurred while running this command.",
                ephemeral=True
            )
            raise error  

async def setup(bot):
    await bot.add_cog(SyncRoles(bot))
