import settings
import discord 
from discord.ext import commands


logger = settings.logging.getLogger("bot")
class Main:

    def __init__(self):

        self.intents = discord.Intents.all()
        self.bot = commands.Bot(command_prefix='!',intents=self.intents,application_id= settings.APPLICATION_ID)
        self.bot.remove_command('help')

        @self.bot.event
        async def on_ready():

            print("Connected")

            try:
                for cog_file in settings.COGS_DIR.glob("*.py"):
                    if cog_file != "__init__.py":
                        await self.bot.load_extension(f"cogs.{cog_file.name[:-3]}")
            except Exception as e:
                print(f"Error loading cog: {e}")
        
        @self.bot.command()
        @commands.has_permissions(administrator=True)
        async def reload(ctx, cog: str):
            try:
                await self.bot.reload_extension(f"cogs.{cog.lower()}")
                await ctx.send(f"Reloaded {cog} successfully")
            except Exception as e:
                print(f"Error loading cog: {e}")
        
        
        self.bot.run(settings.DISCORD_API_SECRET,root_logger=True)

if __name__ == "__main__":
    Main()
