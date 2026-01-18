import discord
from .email_modal import EmailModal

class EmailTypeView(discord.ui.View):
    def __init__(self, bot, timeout = 60):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.prem_kind = None 
        self.current_data = None 


    @discord.ui.button(label="Old Premium", style=discord.ButtonStyle.blurple)
    async def old_prem(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = EmailModal(self.bot,self.current_data,prem_kind="old")
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.current_data = modal.current_data
        self.stop()

    @discord.ui.button(label="New Premium", style=discord.ButtonStyle.blurple)
    async def new_prem(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = EmailModal(self.bot,self.current_data,prem_kind="new")
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.current_data = modal.current_data
        self.stop()