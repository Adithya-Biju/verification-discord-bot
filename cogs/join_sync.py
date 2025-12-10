import discord
from discord.ext import commands
from models import Customer
from utility.update_queue import enqueue


class JoinSync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")
        
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Triggered when a user joins one of the monitored servers."""
   
        customer = await Customer.get_or_none(user_id=member.id)

        if not customer:
            return
        
        await enqueue(member.id)



async def setup(bot):
    await bot.add_cog(JoinSync(bot))
