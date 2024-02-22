import discord 
from discord.ext import commands
from discord import app_commands
from utility import db,payment
import settings

class database(commands.Cog):

    def __init__(self,bot:commands.Bot):

        self.bot = bot
        self.bot.remove_command("help")

    @commands.Cog.listener()
    async def on_ready(self):
         print("Database cog loaded")


    @app_commands.command(name="insert",description="Register a user and sends a key")
    @app_commands.describe(util = "Choose the utility:-")
    @app_commands.choices(util = [
        discord.app_commands.Choice(name="premium",value=1),
        discord.app_commands.Choice(name="standard",value=2)
    ])
    async def insert(self, interaction :discord.Interaction,email : str,member:discord.Member, util: discord.app_commands.Choice[int]):

        try:

            await interaction.response.defer(ephemeral=True)

            self.endpoint = await payment.endpoint(email)
            self.info = await db.find_dm(email)

            if interaction.permissions.administrator == False:
                await interaction.followup.send("You don't have the permissions to user this command",ephemeral=True)
            
            else:

                if self.info != None or self.endpoint != False:
                    await interaction.followup.send("Customer exists, use the /check command",ephemeral=True)
                
                elif self.info == None and self.endpoint == False :

                    if util.value == 1:
                        
                        await db.struct_premium(email,member.id)
                        await db.struct_keys(email,member.id)
                        self.response = await db.find_email_main(email)
                        await interaction.followup.send(f'''Successfully registered, RUN /CHECK COMMAND TO GIVE THEM ROLES AND SEND A KEY ''',ephemeral=True)
                    

                    elif util.value == 2:

                        await db.struct_standard(email,member.id)
                        self.response = await db.find_email_main(email)
                        await interaction.followup.send(f'''Successfully registered, RUN /CHECK COMMAND TO GIVE THEM ROLE ACCORDINGLY''',ephemeral=True)
                    
                    else:
                        await interaction.followup.send("Error",ephemeral=True)

        except Exception as e:
            print(e)
            await interaction.response.send_message("Error",ephemeral=True)

    
    @app_commands.command(name = "find_email", description= " Find the email using the user id")
    async def find_email(self,interaction:discord.Interaction,member:discord.Member):

        try:
            await interaction.response.defer(ephemeral=True)

            if interaction.permissions.administrator == False:
                await interaction.followup.send("You don't have the adequate permissions to use this command",ephemeral=True)
            
            else:
                self.info = await db.find_user(member.id)

                if self.info == None:
                    
                    await interaction.followup.send("User not found",ephemeral=True)
                
                elif self.info != None:

                    await interaction.followup.send(f'''User found: -

{self.info['email']}
<@{self.info['user_id']}>
{self.info['util']}''',ephemeral=True)
                
                else:

                    await interaction.followup.send("Error",ephemeral=True)
            
        except Exception as e:
            print(e)
            await interaction.response.send_message("Unexpected error occured")

    
    @app_commands.command(name = "find_user", description= " Find the user using the email id")
    async def find_user(self,interaction:discord.Interaction,email:str):

        try:
            await interaction.response.defer(ephemeral=True)

            if interaction.permissions.administrator == False:
                await interaction.followup.send("You don't have the adequate permissions to use this command",ephemeral=True)
            
            else:
                self.info = await db.find_email_main(email)

                if self.info == None:
                    
                    await interaction.followup.send("User not found",ephemeral=True)
                
                elif self.info != None:

                    await interaction.followup.send(f'''User found <@{self.info['user_id']}>: -

{self.info['email']}
<@{self.info['user_id']}>
{self.info['util']}''',ephemeral=True)
                
                else:

                    await interaction.followup.send("Error",ephemeral=True)
            
        except Exception as e:
            print(e)
            await interaction.response.send_message("Unexpected error occured")
        
    
    @app_commands.command(name = "update_email", description= " Update a registered email ID")
    async def update_email(self,interaction:discord.Interaction,old_email:str,new_email:str):

        try:
            await interaction.response.defer(ephemeral=True)

            if interaction.permissions.administrator == False:
                await interaction.followup.send("You don't have the adequate permissions to use this command",ephemeral=True)
            
            else:
                self.info = await db.find_email_main(old_email)

                if self.info == None:
                    
                    await interaction.followup.send("User not found",ephemeral=True)
                
                elif self.info != None:
                    
                    await db.UpdateEmail(old_email,new_email)
                    self.info = await db.find_email_main(new_email)
                    if self.info != None:
                        await interaction.followup.send(f'''Successfully updated: -

{self.info['email']}
<@{self.info['user_id']}>
{self.info['util']}''',ephemeral=True)
                    else:
                        await interaction.followup.send("Error")
                
                else:

                    await interaction.response.send_message("Error",ephemeral=True)
            
        except Exception as e:
            print(e)
            await interaction.followup.send("Unexpected error occured")
        
    @app_commands.command(name = "update_user", description= " Update a registered user ID")
    async def update_user(self,interaction:discord.Interaction,old_user:discord.Member,new_user:discord.Member):

        try:
            await interaction.response.defer(ephemeral=True)

            if interaction.permissions.administrator == False:
                await interaction.followup.send("You don't have the adequate permissions to use this command",ephemeral=True)
            
            else:
                self.info = await db.find_user(old_user.id)

                if self.info == None:
                    
                    await interaction.followup.send("User not found",ephemeral=True)
                
                elif self.info != None:
                    
                    await db.UpdateUser(old_user.id,new_user.id)
                    self.info = await db.find_user(new_user.id)
                    if self.info != None:
                        await interaction.followup.send(f'''Successfully updated : -

{self.info['email']}
<@{self.info['user_id']}>
{self.info['util']}''',ephemeral=True)
                    else:
                        await interaction.followup.send("Error")
                
                else:

                    await interaction.followup.send("Error",ephemeral=True)
            
        except Exception as e:
            print(e)
            await interaction.response.send_message("Unexpected error occured")
        
    
    @app_commands.command(name = "delete_user", description= "Delete user info using their User ID")
    async def delete_user(self,interaction:discord.Interaction,member:str):

        try:
            await interaction.response.defer(ephemeral=True)

            if interaction.permissions.administrator == False:
                await interaction.followup.send("You don't have the adequate permissions to use this command",ephemeral=True)
            
            else:
                self.info = await db.find_user(member)

                if self.info == None:
                    
                    await interaction.followup.send("User not found",ephemeral=True)
                
                elif self.info != None:
                    
                    await db.delete_user(member)
                    await interaction.followup.send(f'''Successfully deleted''',ephemeral=True)
                
                else:

                    await interaction.followup.send("Error",ephemeral=True)
            
        except Exception as e:
            print(e)
            await interaction.response.send_message("Unexpected error occured")

    @app_commands.command(name = "delete_email", description= "Delete email info using their email ID")
    async def delete_email(self,interaction:discord.Interaction,email:str):

        try:
            await interaction.response.defer(ephemeral=True)

            if interaction.permissions.administrator == False:
                await interaction.followup.send("You don't have the adequate permissions to use this command",ephemeral=True)
            
            else:
                self.info = await db.find_email_main(email)

                if self.info == None:
                    
                    await interaction.followup.send("User not found",ephemeral=True)
                
                elif self.info != None:
                    
                    await db.delete_email(email)
                    await interaction.followup.send(f'''Successfully deleted''',ephemeral=True)
                
                else:

                    await interaction.response.send_message("Error",ephemeral=True)
            
        except Exception as e:
            print(e)
            await interaction.followup.send("Unexpected error occured")


    
async def setup(bot):
    await bot.add_cog(database(bot),guilds = [discord.Object(id=settings.GUILD_ID)])
    
    