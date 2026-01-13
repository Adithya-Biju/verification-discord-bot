import discord
from .updation_modal import UpdationModal
from models import Customer,CustomerOld

class EmailTypeView(discord.ui.View):
    def __init__(self, bot, timeout = 60):
        super().__init__(timeout=timeout)
        self.bot = bot


    @discord.ui.button(label="Old Premium", style=discord.ButtonStyle.blurple)
    async def old_prem(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = EmailModal(self.bot,prem_kind="old")
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="New Premium", style=discord.ButtonStyle.blurple)
    async def new_prem(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = EmailModal(self.bot,prem_kind="new")
        await interaction.response.send_modal(modal)
        

class EmailModal(discord.ui.Modal, title='Update via Email'):
    email = discord.ui.TextInput(label='Email Address', placeholder='example@gmail.com')
    
    def __init__(self,bot, prem_kind):
        super().__init__()
        self.bot = bot
        self.prem_kind = prem_kind 
        

    async def on_submit(self, interaction: discord.Interaction):

        user_id = 0

        if self.prem_kind == "old":

            customer_old = await CustomerOld.get_or_none(email=self.email.value)

            if customer_old:

                user_id = customer_old.user_id
        
            else:

                await interaction.response.send_message("Gmail acc not found in the legacy database", ephemeral=True)

        
        else:

            customer = await Customer.get_or_none(email = self.email.value)     

            if customer:

                user_id = customer.user_id
        
            else:

                await interaction.response.send_message("Gmail acc not found in the database", ephemeral=True)
        
        if user_id != 0: 
            customer = await Customer.get_or_none(user_id=user_id)
            customer_old = await CustomerOld.get_or_none(user_id=user_id)

            current_data = {
                "user_id": user_id,
                "new_email": (customer.email if customer and customer.email else None),
                "has_premium_new": getattr(customer, 'has_premium_new', False),
                "has_premium_old": getattr(customer, 'has_premium_old', False),
                "old_email": customer_old.email if (customer_old and customer_old.email) else None
            }


            class BridgeView(discord.ui.View):
                def __init__(self, bot, data):
                    super().__init__(timeout=60)
                    self.bot = bot
                    self.data = data

                @discord.ui.button(label="Open Updation Form", style=discord.ButtonStyle.blurple)
                async def open_modal(self, btn_interaction: discord.Interaction, button: discord.ui.Button):
                    await btn_interaction.response.send_modal(UpdationModal(self.bot, self.data))


            view = BridgeView(self.bot, current_data)
            await interaction.response.send_message(
                content=f"Found data for User `{user_id}`. Click below to edit:",
                view=view,
                ephemeral=True
            )