import discord
from service.admin.update_components.email_modal import EmailTypeView

class UpdateSelectionView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=60)
        self.bot = bot
        self.chosen_method = None 

    @discord.ui.select(
        placeholder="Choose update method...",
        options=[
            discord.SelectOption(label="User ID", value="user", description="Update by tagging a user"),
            discord.SelectOption(label="Email", value="email", description="Update by email address")
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.chosen_method = select.values[0] 
        self.stop()
            