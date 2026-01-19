import discord

class ConfirmationButtonView(discord.ui.View):
    def __init__(self, bot, timeout = 60):
        super().__init__(timeout=timeout)
        self.bot = bot

    @discord.ui.button(label="CONFIRM", style=discord.ButtonStyle.blurple)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()