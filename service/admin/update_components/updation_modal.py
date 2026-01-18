import discord
from utility.database import update_premium
from utility import constants

class UpdationModal(discord.ui.Modal):

    def __init__(self, bot : discord.Client, current_data,status,message,timeout = 300):
        super().__init__(title=f"Update {current_data['user_id']}",timeout=timeout)
        self.bot = bot
        self.status = status 
        self.message = message
        self.update_payload = None
        self.data = current_data

        self.user_id_field = discord.ui.TextInput(
            label="User ID",
            default=str(current_data["user_id"]),
            placeholder="Enter 18-digit Discord ID",
            min_length=15,
            required=False
        )

        self.new_premium_flag_field = discord.ui.TextInput(
            label="Has New Premium",
            default=str(self.data["has_premium_new"]),
            placeholder="True or False",
            required=False
        )

        self.old_premium_flag_field = discord.ui.TextInput(
            label="Has Old Premium",
            default=str(self.data["has_premium_old"]),
            placeholder="True or False",
            required=False
        )

        self.add_item(self.user_id_field)

        if self.data["new_email"]:

            self.new_prem_email_field = discord.ui.TextInput(
            label="New Premium Email",
            default=self.data["new_email"],
            placeholder="example@gmail.com",
            required=False
        )
            self.add_item(self.new_prem_email_field)
            
        if self.data["old_email"]:

            self.old_prem_email_field = discord.ui.TextInput(
            label="Old Premium Email",
            default=self.data["old_email"],
            placeholder="example@gmail.com",
            required=False
        )
            self.add_item(self.old_prem_email_field)
    
        self.add_item(self.new_premium_flag_field)
        self.add_item(self.old_premium_flag_field)


    async def on_submit(self, interaction: discord.Interaction):

        try:
            await interaction.response.defer(ephemeral=True)

            def to_bool(s:str) -> bool:
                return s.lower() == "true"

            self.update_payload = {
                "user_id" : int(self.user_id_field.value),
                "has_premium_old" : to_bool(self.old_premium_flag_field.value),
                "has_premium_new" : to_bool(self.new_premium_flag_field.value)
            }

            if hasattr(self,'old_prem_email_field'):
                self.update_payload["old_email"] = self.old_prem_email_field.value
            else:
                self.update_payload["old_email"] = None
            
            if hasattr(self,'new_prem_email_field'):
                self.update_payload["new_email"] = self.new_prem_email_field.value
            else:
                self.update_payload["new_email"] = None

            response = await update_premium(self.data,self.update_payload)

            if response['success'] == False:
                self.status = False 
                self.message = response["error"]
            else:
                self.status = True
                self.message = "Updated Successfully"

            self.stop()

        except Exception as e:
            print(e)
            self.status = False
            self.message = "Unexpected Error occured"
        


class UpdationTriggerView(discord.ui.View):
    def __init__(self,bot,current_data):
        super().__init__(timeout=60)
        self.bot = bot
        self.current_data = current_data
        self.status = None 
        self.message = None 
        self.update_payload = None 

    @discord.ui.button(label="Open Updation Form", style=discord.ButtonStyle.blurple)
    async def open_update_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = UpdationModal(self.bot,self.current_data,self.status,self.message)
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.status = modal.status
        self.message = modal.message
        self.update_payload = modal.update_payload
        self.stop()