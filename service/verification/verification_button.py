import discord
from .buttons import EmailModal

class LoginView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        label="Enter Email",
        style=discord.ButtonStyle.blurple,
        custom_id="login_email_button"
    )
    async def enter_email(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EmailModal(self.bot))
    