import asyncio
import discord
from discord.ext import commands
from tortoise import Tortoise
from models.server_model import Server
import settings
import uvicorn
from service import LoginView
from api.main import app



class Main(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(
            command_prefix="!",
            intents=intents,
            application_id=settings.APPLICATION_ID,
        )
        self.remove_command("help")

    # ------------------------------------------------------------
    async def setup_hook(self):
        # Load database models dynamically
        models = [
            f"models.{m.name[:-3]}"
            for m in settings.MODELS_DIR.glob("*.py")
            if m.name != "__init__.py"
        ]

        await Tortoise.init(db_url=settings.POSTGRES, modules={"models": models})
        await Tortoise.generate_schemas()
        print("Database connected and schemas ready.")

        # Load all cogs
        for cog_file in settings.COGS_DIR.glob("*.py"):
            if cog_file.name != "__init__.py":
                try:
                    await self.load_extension(f"cogs.{cog_file.name[:-3]}")
                    print(f"Loaded cog: {cog_file.name[:-3]}")
                except Exception as e:
                    print(f"Error loading cog {cog_file.name}: {e}")
        

    # ------------------------------------------------------------
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        self.add_view(LoginView(self))
        await self.sync_commands_per_guild()

    # ------------------------------------------------------------
    async def sync_commands_per_guild(self):
        """Sync slash commands for all servers in DB."""
        try:
            servers = await Server.all().values_list("server_id", flat=True)
            print(f"Found {len(servers)} servers in DB")

            for sid in servers:
                try:
                    guild = discord.Object(id=sid)
                    self.tree.copy_global_to(guild=guild)
                    await self.tree.sync(guild=guild)
                    print(f"Synced commands for guild: {sid}")
                    await asyncio.sleep(1)
                except Exception as e:
                    print(f"Error syncing guild {sid}: {e}")
        except Exception as e:
            print(f"Database sync error: {e}")


# ------------------------------------------------------------
async def start_discord_bot():
    bot = Main()
    async with bot:
        await bot.start(settings.DISCORD_API_SECRET)

async def start_webhook():   
    config = uvicorn.Config(app, host="localhost", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    await asyncio.gather(start_discord_bot(), start_webhook())


if __name__ == "__main__":
    asyncio.run(main())
