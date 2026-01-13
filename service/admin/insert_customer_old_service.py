import discord
from utility import database, update_queue, constants
from .update_components.email_modal import EmailTypeView
from .update_components.userID_email_menu import UpdateSelectionView 
from .update_components.user_id_modal import UserTriggerView


class CustomerUpdates:

    def __init__(self,bot: discord.Client):

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

    async def insert_data_old_customer(self,interaction: discord.Interaction, member: discord.Member, email: str):

        response = await database.insert_old_premium(member.id, email)

        if response["status"] == "email_linked_to_other":

            await interaction.followup.send(f'''Email ID is already linked to {response["linked_user_id"]}
If you want to make those changes then update or delete the exisiting one''', ephemeral=True)
            await self.log_channel.send(
                f"🔴 **OLD PREMIUM FAILED**\n"
                f"Email `{email}` already linked to `{response['linked_user_id']}`\n"
                f"Attempted on: {member.mention}\n"
                f"Attempted by: {interaction.user.mention}"
            )
            return 
        
        if response["status"] == "already_in_old":

            await interaction.followup.send(f"Already present in the legacy DB", ephemeral=True)
            await self.log_channel.send(
                f"🟡 **OLD PREMIUM EXISTS**\n"
                f"User: {member.mention}\n"
                f"Email: `{email}`\n"
                f"Attempted by: {interaction.user.mention}"
            )
            await update_queue.enqueue(member.id)
            return 
        
        if response["status"] == "old_created_existing_customer":

            await interaction.followup.send("Inserted successfully", ephemeral=True)
            await self.log_channel.send(
                 f"🟢 **INSERTED OLD PREMIUM**\n"
                f"User: {member.mention}\n"
                f"Email: `{email}`"
                f"Attempted by: {interaction.user.mention}"
            )
            await update_queue.enqueue(member.id)
            return 
        
        if response["status"] == "created_customer_and_old":

            await interaction.followup.send("Inserted successfully", ephemeral=True)
            await self.log_channel.send(
                 f"🟢 **INSERTED OLD PREMIUM**\n"
                f"User: {member.mention}\n"
                f"Email: `{email}`\n"
                f"Attempted by: {interaction.user.mention}"
            )
            await update_queue.enqueue(member.id)
            return
    
    async def update_data_customer(self,interaction: discord.Interaction):

        userid_email = UpdateSelectionView(self.bot)
        await interaction.followup.send("How would you like to proceed?", view=userid_email, ephemeral=True)

        await userid_email.wait()

        if userid_email.chosen_method == "email":

            await interaction.edit_original_response(content="Opening Email Update options...", view=None)
            email_modal = EmailTypeView(self.bot) 
            await interaction.followup.send("Please select the premium type to open the email form:", view=email_modal, ephemeral=True)
        
        elif userid_email.chosen_method == "user":

            await interaction.edit_original_response(content="Opening User ID Update options...", view=None)
            user_modal = UserTriggerView(self.bot) 
            await interaction.followup.send(content="Please provide the User ID for the account you wish to update", view=user_modal, ephemeral=True)
        
        else: 

            await interaction.edit_original_response(content="Message timed out, please run the update comamand again",view=None)