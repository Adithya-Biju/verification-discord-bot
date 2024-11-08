import discord 
from tortoise.exceptions import IntegrityError
from models.captions_model import Caption
from tortoise.transactions import in_transaction

class TicketMenu(discord.ui.Select):
    def __init__(self, options):
        super().__init__(placeholder="Open a ticket", options=options, custom_id="SelectMenu")

    @classmethod
    async def generate_menu_options(cls):
        options = []
        designs = await Caption.filter(main_design='Ticket_Select')
        for design in designs:
            options.append(discord.SelectOption(label=design.label, value=design.value, emoji=design.emoji))
        return cls(options)

    # async def callback(self, interaction: discord.Interaction):
    #     try:
    #         # Defer the response to indicate processing
    #         await interaction.response.defer(ephemeral=True)

    #         # Fetch the response message from the database based on the selected value
    #         selected_design = await Ticket.get(value=self.values[0], main_design__main_design='ticket_select')

    #         # Create the ticket and thread
    #         user_data = await Ticket.create(user_id=interaction.user.id)
    #         thread = await interaction.channel.create_thread(
    #             name=f"Ticket {user_data.ticket_id}",  # Thread name based on ticket ID
    #             type=discord.ChannelType.private_thread  # Choose the type of thread
    #         )

    #         # Send a message in the thread
    #         await thread.send(f"{interaction.user.mention}, your ticket has been created! 🎟️\n{selected_design.response_message}")
        
    #     except IntegrityError as e:
    #         # Handle integrity errors
    #         await interaction.followup.send("Failed to create the ticket due to an integrity error.", ephemeral=True)
    #         print(f"Integrity error: {str(e)}")

    #     except Exception as e:
    #         # Handle any other errors
    #         await interaction.followup.send("An error occurred while creating the ticket.", ephemeral=True)
    #         print(f"Error: {str(e)}")