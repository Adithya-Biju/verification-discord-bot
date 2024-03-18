from typing import Any
import discord 
from discord.ext import commands
from discord import app_commands
import settings
from discord.ui import Select,Button,View
from utility import embed


class SelectMenu(discord.ui.Select):
    def __init__(self):
        options = [
                discord.SelectOption(label = "Spoof", 
                                     value = "0",
                                     emoji="🔵"),
                discord.SelectOption(label = "Lag Gpu Wise",
                                     value = "1",
                                     emoji="🔵"),
                discord.SelectOption(label="Other", 
                                     value = "2",
                                     emoji="🔵")

            ]
        super().__init__(placeholder="Select a question",options=options,custom_id="SelectMenu")
    
    async def callback(self, interaction: discord.Interaction):

        if self.values[0] == "0":
            await interaction.response.send_message("If you **spoof**, you **WON'T** get a key reset since we do **NOT** condone spoofing.",ephemeral = True)

        elif self.values[0] == "1":
            await interaction.response.send_message("If you are experiencing lagging **GPU-wise** after doing tweaks, just play some matches; your cache has to build up it will eventually get good",ephemeral = True)

        elif self.values[0] == "2":
            await interaction.response.send_message(view = ButtonView(),ephemeral = True)

        else:
            pass 


class ButtonMenu(discord.ui.Button):
    def __init__(self):
        super().__init__(label= "Open a ticket",
                            style = discord.ButtonStyle.green,
                            emoji = '📝',
                            custom_id="ButtonMenu")
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Under construction",ephemeral=True)


class ButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ButtonMenu())


class SelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SelectMenu())


class Admin(commands.Cog):

    def __init__(self,bot:commands.Bot):

        self.bot = bot
        self.bot.remove_command("help")
        self.select_persistent_view = SelectView()
        self.button_persistent_view = ButtonView()
    
    async def cog_load(self):
        self.bot.add_view(self.select_persistent_view)
        self.bot.add_view(self.button_persistent_view)
    
    async def cog_unload(self):
        self.bot.add_view(self.select_persistent_view)
        self.bot.add_view(self.button_persistent_view)


    @commands.Cog.listener()
    async def on_ready(self):
         print("Admin cog loaded")
    

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def faq(self,ctx):

        self.faq_embed = await embed.faq()
         
        try:
            await ctx.send(embed = self.faq_embed, view = SelectView())

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await ctx.send("An unexpected error occurred. Try again ", ephemeral=True)
        

async def setup(bot):
        await bot.add_cog(Admin(bot),guilds = [discord.Object(id=settings.GUILD_ID)])