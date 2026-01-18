import discord
from models import CustomerOld, Customer


class UserIDModal(discord.ui.Modal, title='Update via User ID'):

    user_input = discord.ui.TextInput(
        label='Enter User ID or Mention',
        placeholder='e.g., 123456789012345678'
    )

    def __init__(self,bot,current_data):
        super().__init__()
        self.bot = bot 
        self.current_data = current_data

    async def on_submit(self, interaction: discord.Interaction):

        await interaction.response.defer()
        
        raw_id = self.user_input.value.strip('<@!>')
        
        try:
            user_id = int(raw_id)
            customer = await Customer.get_or_none(user_id=user_id)
            customer_old = await CustomerOld.get_or_none(user_id=user_id)

            if customer: 

                self.current_data = {
                    "user_id": user_id,
                    "new_email": (customer.email if customer and customer.email else None),
                    "has_premium_new": getattr(customer, 'has_premium_new', False),
                    "has_premium_old": getattr(customer, 'has_premium_old', False),
                    "old_email": customer_old.email if (customer_old and customer_old.email) else None
                }

                self.stop()

        except ValueError:
            await interaction.followup.send("Invalid ID format. Please enter numbers only.", ephemeral=True)


class UserTriggerView(discord.ui.View):
    def __init__(self,bot):
        super().__init__(timeout=60)
        self.bot = bot
        self.current_data = None  

    @discord.ui.button(label="Enter User ID", style=discord.ButtonStyle.blurple)
    async def open_user_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = UserIDModal(self.bot,self.current_data)
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.current_data = modal.current_data
        self.stop()