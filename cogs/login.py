import discord
from discord.ext import commands
from service import LoginView
from utility.constants import OWNER_ID 

class Login(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create_login_panel")
    async def create_login_panel(self, ctx):
        # Restrict to only YOU
        if ctx.author.id != OWNER_ID:
            return 

        embed = discord.Embed(
            title="🔐 Link Your EXM Account",
            description="Click below and enter your EXM email to link your subscription.",
            color=discord.Color.blurple()
        )

        view = LoginView(self.bot)

        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Login(bot))
