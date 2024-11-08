import discord 
from discord.ext import commands
from discord import app_commands
import settings
from utility import key,constants
from models.ticket_model import Ticket
from tortoise.exceptions import IntegrityError


class TicketTest(commands.Cog):

    def __init__(self,bot:commands.Bot):

        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
         print("Ticket cog loaded")

    @app_commands.command(name = 'ticket_test')
    async def ticket_test(self, interaction :discord.Interaction):

        await interaction.response.defer(ephemeral=True)
        try:
            
            user_data = await Ticket.create(user_id = interaction.user.id)
            thread = await interaction.channel.create_thread(
                name=user_data.ticket_id,
                type=discord.ChannelType.private_thread,  # or private_thread
                message=interaction.message  # Pin the command message to the thread
        )
            await thread.send(f"{interaction.user.mention}, your ticket has been created! 🎟️")
            
            await interaction.followup.send(f"Ticket created with ID: {user_data.ticket_id}")

        except IntegrityError as e:
        # Handle integrity errors (e.g., if you have constraints in your table)
            await interaction.followup.send("Failed to create ticket due to integrity error.")
            print(f"Integrity error: {str(e)}")
    
        except Exception as e:
            # Catch all other exceptions
            await interaction.followup.send("An error occurred while creating the ticket.")
        print(f"Error: {str(e)}")

        # except:
        #     await interaction.followup.send("An unexpected error occurred. Try again ", ephemeral=True)
        
        

async def setup(bot):
        await bot.add_cog(TicketTest(bot),guilds = [discord.Object(id=settings.GUILD_ID)])