import discord 
from discord.ext import commands
from discord import app_commands
import settings
from service import sync_roles


class Sync(commands.Cog):

    def __init__(self,bot:commands.Bot):

        self.bot = bot
        self.bot.remove_command("help")

    @commands.Cog.listener()
    async def on_ready(self):
         print("Sync cog loaded")
        
    @app_commands.command(name="sync",description="Syncing the roles in all the 3 servers")
    async def sync(self, interaction :discord.Interaction):

        try:

            await interaction.response.defer(ephemeral=True)
            validation_response = await sync_roles( self.bot, interaction.user.id)
            await interaction.followup.send(validation_response, ephemeral=True)

        except:
            return
        
async def setup(bot):
    await bot.add_cog(Sync(bot))