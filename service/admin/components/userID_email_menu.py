import discord

class KeySelectionView(discord.ui.View):
    def __init__(self, bot : discord.Client):
        super().__init__(timeout=60)
        self.bot = bot
        self.chosen_method = None 

    @discord.ui.select(
        placeholder="Choose update method...",
        options=[
            discord.SelectOption(label="User ID", value="user", description="Update by discord user ID"),
            discord.SelectOption(label="Email", value="email", description="Update by email address")
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.defer()
        self.chosen_method = select.values[0] 
        self.stop()