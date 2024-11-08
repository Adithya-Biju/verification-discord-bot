from typing import Any
import discord 
from discord.ext import commands
from discord import app_commands
import settings
from discord.ui import Select,Button,View
from utility import embed
from tortoise.exceptions import IntegrityError
from models.ticket_model import Ticket
from service import TicketView, TicketMenu



# class ButtonMenu(discord.ui.Button):
#     def __init__(self):
#         super().__init__(label= "Open a ticket",
#                             style = discord.ButtonStyle.green,
#                             emoji = '📝',
#                             custom_id="ButtonMenu")

#     async def callback(self, interaction: discord.Interaction):
#         await interaction.response.defer(ephemeral=True)
#         try:
   
#             user_data = await Ticket.create(user_id = interaction.user.id)
#             thread = await interaction.channel.create_thread(
#                 name=user_data.ticket_id,
#                 type=discord.ChannelType.private_thread,  # or private_thread
#         )
#             await thread.send(f"{interaction.user.mention}, your ticket has been created! 🎟️")
   
#             await interaction.followup.send(f"Ticket created with ID: {user_data.ticket_id}", ephemeral=True)

#         except IntegrityError as e:
#         # Handle integrity errors (e.g., if you have constraints in your table)
#             await interaction.followup.send("Failed to create ticket due to integrity error.")
#             print(f"Integrity error: {str(e)}")

#         except Exception as e:
#             # Catch all other exceptions
#             await interaction.followup.send("An error occurred while creating the ticket.")
#         print(f"Error: {str(e)}")



class Admin(commands.Cog):

    def __init__(self,bot:commands.Bot):

        self.bot = bot
        self.bot.remove_command("help")
    
    async def cog_load(self):
        self.ticket_menu = await TicketMenu.generate_menu_options()
        self.ticket_view = discord.ui.View(timeout=None)
        self.ticket_view.add_item(self.ticket_menu)
        self.bot.add_view(self.ticket_view)


    @commands.Cog.listener()
    async def on_ready(self):
         print("Admin cog loaded")
    

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ticket(self,ctx):

        self.faq_embed = await embed.ticket()
         
        try:
            await ctx.send(embed = self.faq_embed, view = TicketView())

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await ctx.send("An unexpected error occurred. Try again ", ephemeral=True)
        

async def setup(bot):
        await bot.add_cog(Admin(bot),guilds = [discord.Object(id=settings.GUILD_ID)])