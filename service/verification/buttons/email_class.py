import discord
from ..verify_service import validation 

class EmailModal(discord.ui.Modal, title="EXM 1.3 Login"):
    def __init__(self, bot, interaction):
        super().__init__(timeout=None)
        self.bot = bot
        self.interaction = interaction

        self.email = discord.ui.TextInput(
            label="Enter your email",
            placeholder="you@example.com",
            required=True,
            style=discord.TextStyle.short,
            max_length=255,
        )
        self.add_item(self.email)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        await validation(self.bot, interaction, interaction.user.id, self.email.value)