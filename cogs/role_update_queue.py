from discord.ext import tasks
from models import RoleUpdateQueue, Customer
from utility.server_roles import role_updates 
from discord.ext import commands


class RoleUpdates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")
        self.process_role_updates.start()
    
    async def cog_unload(self):
        self.process_role_updates.cancel()

    @tasks.loop(seconds=5) 
    async def process_role_updates(self):
        
        pending_update = await RoleUpdateQueue.all().order_by('id').first()

        if pending_update:
            user_id = pending_update.user_id

            
            customer = await Customer.get_or_none(user_id=user_id)

            if customer:
                
                await role_updates(self.bot, user_id)

                await pending_update.delete()

            else:
                await pending_update.delete()

        else:
            return 

async def setup(bot):
    await bot.add_cog(RoleUpdates(bot))