import discord 
from models import CustomerOld, Customer


class EmailModal(discord.ui.Modal, title='Enter Email address'):
    email = discord.ui.TextInput(label='Email Address', placeholder='example@gmail.com')
    
    def __init__(self,bot,current_data, prem_kind:str):
        super().__init__()
        self.bot = bot
        self.prem_kind = prem_kind
        self.current_data = current_data 
        

    async def on_submit(self, interaction: discord.Interaction):

        await interaction.response.defer()

        user_id = 0

        if self.prem_kind == "old":
            customer_old = await CustomerOld.get_or_none(email=self.email.value)
            user_id = customer_old.user_id if customer_old else 0

        
        else:
            customer = await Customer.get_or_none(email = self.email.value)     
            user_id = customer.user_id if customer else 0
        

        if user_id != 0: 
            customer = await Customer.get_or_none(user_id=user_id)
            customer_old = await CustomerOld.get_or_none(user_id=user_id)

            self.current_data = {
                "user_id": user_id,
                "new_email": (customer.email if customer and customer.email else None),
                "has_premium_new": getattr(customer, 'has_premium_new', False),
                "has_premium_old": getattr(customer, 'has_premium_old', False),
                "old_email": customer_old.email if (customer_old and customer_old.email) else None
            }

            self.stop()

