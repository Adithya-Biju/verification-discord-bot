import discord
from utility.database import update_premium
from utility import constants

class UpdationModal(discord.ui.Modal):

    def __init__(self, bot : discord.Client, current_data,timeout = 300):
        super().__init__(title=f"Update {current_data["user_id"]}",timeout=timeout)
        self.data = current_data
        log_guild = bot.get_guild(constants.LOG_SERVER)

        if not log_guild:
            try:
                log_guild = bot.fetch_guild(constants.LOG_SERVER)
            except discord.NotFound:
                print(f"[ERROR] Guild {constants.LOG_SERVER} not found.")
                return
            except discord.Forbidden:
                print(f"[ERROR] Bot doesn't have permission to access the guild {constants.LOG_SERVER}.")
                return
        self.log_channel = log_guild.get_channel(constants.TRANSFER_LOG)
        self.bot = bot

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
        await interaction.response.defer(ephemeral=True)

        def to_bool(s:str) -> bool:
            return s.lower() == "true"

        update_payload = {
            "user_id" : int(self.user_id_field.value),
            "has_premium_old" : to_bool(self.old_premium_flag_field.value),
            "has_premium_new" : to_bool(self.new_premium_flag_field.value)
        }

        if hasattr(self,'old_prem_email_field'):
            update_payload["old_email"] = self.old_prem_email_field.value
        else:
            update_payload["old_email"] = None
        
        if hasattr(self,'new_prem_email_field'):
            update_payload["new_email"] = self.new_prem_email_field.value
        else:
            update_payload["new_email"] = None


        response = await update_premium(self.data,update_payload)

        if response['success'] == False:
            await self.log_channel.send(
                f"🔴 **PREMIUM UPDATION FAILED**\n"
                f"Attempted on : {self.data}\n"
                f"Updation attempt: {update_payload}\n"
                f"Failing reason : {response['error']}\n"
                f"Attempted by: {interaction.user.mention}"
            )
            await interaction.followup.send(response['error'],ephemeral=True)
        else:
            await self.log_channel.send(
                f"🟢 **PREMIUM UPDATION SUCCESS**\n"
                f"Old data : {self.data}\n"
                f"Updated data: {update_payload}\n"
                f"Attempted by: {interaction.user.mention}"
            )
            await interaction.followup.send("Updated successfully", ephemeral=True)
        