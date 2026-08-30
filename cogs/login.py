import discord
from discord import app_commands
from discord.ext import commands
from service import LoginView
from utility.constants import OWNER_ID 

class Login(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @app_commands.command(
        name="create_login_panel",
        description="Create the Premium customer verification panel"
    )
    async def create_login_panel(self, interaction: discord.Interaction ):

        if interaction.user.id != OWNER_ID:
            return

        embed = discord.Embed(
            title="🔐 Verify as a Premium Customer",
            description='''Click below and enter the email you used to purchase EXM to instantly receive your Premium role, unlocking priority support and all premium-exclusive benefits''',
            color=discord.Color.blurple()
        )

        view = LoginView(self.bot)

        await interaction.response.send_message(
            embed=embed,
            view=view
        )

async def setup(bot):
    await bot.add_cog(Login(bot))
