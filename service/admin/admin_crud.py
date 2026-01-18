import discord
from utility import database, update_queue, constants, embed
from .components.email_option_modal import EmailTypeView
from .components.userID_email_menu import KeySelectionView
from .components.userid_modal import UserTriggerView
from .update_components.updation_modal import UpdationTriggerView 

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

        userid_email = KeySelectionView(self.bot)
        await interaction.followup.send("How would you like to proceed?", view=userid_email, ephemeral=True)

        await userid_email.wait()

        if userid_email.chosen_method == "email":

            await interaction.edit_original_response(content="Opening Email Update options...", view=None)
            email_type_view = EmailTypeView(self.bot) 

            await interaction.edit_original_response(content="Legacy user's Email address or New user's Email address", view=email_type_view)
            await email_type_view.wait()

            if email_type_view.current_data:
                data = email_type_view.current_data
                
                updation_modal = UpdationTriggerView(self.bot,data)
                await interaction.edit_original_response(content=f"Found data for User `{data['user_id']}`. Click below to edit", view=updation_modal)
                await updation_modal.wait()
                    
                await interaction.edit_original_response(content=updation_modal.message, view=None)

                if updation_modal.status :
                        await self.log_channel.send(
                    f"🟢 **PREMIUM UPDATION SUCCESS**\n"
                    f"Old data : {data}\n"
                    f"Updated data: {updation_modal.update_payload}\n"
                    f"Attempted by: {interaction.user.mention}"
                )
                        await update_queue.enqueue(data['user_id'])

                else:
                    await self.log_channel.send(
                    f"🔴 **PREMIUM UPDATION FAILED**\n"
                    f"Attempted on : {data}\n"
                    f"Updation attempt: {updation_modal.update_payload}\n"
                    f"Failing reason : {updation_modal.message}\n"
                    f"Attempted by: {interaction.user.mention}"
                ) 
                
                
            else:
                await interaction.edit_original_response(content="Data not found", view=None)
                
        
        elif userid_email.chosen_method == "user":

            await interaction.edit_original_response(content="Opening User ID View options...", view=None)
            userid_type_view = UserTriggerView(self.bot) 

            await interaction.edit_original_response(content="Opening User ID View ...", view=userid_type_view)
            await userid_type_view.wait()
            if userid_type_view.current_data:
                data = userid_type_view.current_data
                
                updation_modal = UpdationTriggerView(self.bot,data)
                await interaction.edit_original_response(content=f"Found data for User `{data['user_id']}`. Click below to edit", view=updation_modal)
                await updation_modal.wait()
                    
                await interaction.edit_original_response(content=updation_modal.message, view=None)

                if updation_modal.status :
                        await self.log_channel.send(
                    f"🟢 **PREMIUM UPDATION SUCCESS**\n"
                    f"Old data : {data}\n"
                    f"Updated data: {updation_modal.update_payload}\n"
                    f"Attempted by: {interaction.user.mention}"
                )
                        await update_queue.enqueue(data['user_id'])

                else:
                    await self.log_channel.send(
                    f"🔴 **PREMIUM UPDATION FAILED**\n"
                    f"Attempted on : {data}\n"
                    f"Updation attempt: {updation_modal.update_payload}\n"
                    f"Failing reason : {updation_modal.message}\n"
                    f"Attempted by: {interaction.user.mention}"
                ) 
                
                
            else:
                await interaction.edit_original_response(content="Data not found", view=None)

    
    async def view_data_customer(self,interaction: discord.Interaction):

        userid_email = KeySelectionView(self.bot)
        await interaction.followup.send("How would you like to proceed?", view=userid_email, ephemeral=True)

        await userid_email.wait()

        if userid_email.chosen_method == "email":

            await interaction.edit_original_response(content="Opening Email View options...", view=None)
            email_type_view = EmailTypeView(self.bot) 

            await interaction.edit_original_response(content="Opening Old Email View ...", view=email_type_view)
            await email_type_view.wait()

            if email_type_view.current_data:
                data = email_type_view.current_data
                customer_embed = await embed.customer_data(data)
                await interaction.edit_original_response(content=None, embed=customer_embed, view=None)
            
            else:
                await interaction.edit_original_response(content="Data not found", view=None)
                
        
        elif userid_email.chosen_method == "user":

            await interaction.edit_original_response(content="Opening User ID View options...", view=None)
            userid_type_view = UserTriggerView(self.bot) 

            await interaction.edit_original_response(content="Opening User ID View ...", view=userid_type_view)
            await userid_type_view.wait()
            if userid_type_view.current_data:
                data = userid_type_view.current_data
                customer_embed = await embed.customer_data(data)
                await interaction.edit_original_response(content=None, embed=customer_embed, view=None)
            
            else:
                await interaction.edit_original_response(content="Data not found", view=None)
        

        else: 
            await interaction.edit_original_response(content="Message timed out, please run the update comamand again",view=None)