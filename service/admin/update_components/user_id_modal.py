import discord
from models import CustomerOld, Customer
from .updation_modal import UpdationModal


class UserIDModal(discord.ui.Modal, title='Update via User ID'):

    user_input = discord.ui.TextInput(
        label='Enter User ID or Mention',
        placeholder='e.g., 123456789012345678'
    )

    def __init__(self,bot):
        super().__init__()
        self.bot = bot 

    async def on_submit(self, interaction: discord.Interaction):
        
        raw_id = self.user_input.value.strip('<@!>')
        
        try:
            user_id = int(raw_id)
            customer = await Customer.get_or_none(user_id=user_id)
            customer_old = await CustomerOld.get_or_none(user_id=user_id)

            if customer: 

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

            else:
                await interaction.response.send_message("User ID does not exist in the database",ephemeral=True)
        except ValueError:
            await interaction.followup.send("Invalid ID format. Please enter numbers only.", ephemeral=True)


class UserTriggerView(discord.ui.View):
        def __init__(self,bot):
            super().__init__(timeout=60)
            self.bot = bot 

        @discord.ui.button(label="Enter User ID", style=discord.ButtonStyle.blurple)
        async def open_user_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_modal(UserIDModal(self.bot))