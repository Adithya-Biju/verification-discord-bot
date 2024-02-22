import discord 
from discord.ext import commands
from discord import app_commands
from utility import db,key,payment
import settings


class Verify(commands.Cog):

    def __init__(self,bot:commands.Bot):

        self.bot = bot
        self.bot.remove_command("help")

    @commands.Cog.listener()
    async def on_ready(self):
         print("Verify cog loaded")
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sync(self, ctx) -> None:
            try:
                fmt = await self.bot.tree.sync(guild=ctx.guild)
                await ctx.send(f"Synced {len(fmt)} commands.")
            except Exception as e:
                print(e)

    ## VERIFY COMMAND USING A MAIL ID INPUT ##

    @app_commands.command(name="verify",description="Verify to get the premium role")
    async def verified(self, interaction :discord.Interaction,email : str):

        self.premium_role = 1198162651520438272
        self.standard_role = 1208844730486493265
        self.premium_role = interaction.guild.get_role(self.premium_role)
        self.standard_role = interaction.guild.get_role(self.standard_role)
        
        try:

            await interaction.response.defer(ephemeral=True)  

            ## CHECKING THE ID IN THE DATABASE ##

            self.info = await db.find_email_main(email) 
            self.dm = await db.find_dm(email)
            self.endpoint = await payment.endpoint(email)
            self.user = await db.find_user(interaction.user.id)

            ## CHECKING IF THE USER HAS THE PREMIUM ROLE ##

            if self.premium_role in interaction.user.roles:

                ## IF EMAIL DOESNT EXIST IN THE DATABASE, ITS USING THE ENDPOINTS TO CHECK ##

                if self.info == None:

                    ## IF USER NOT FOUND IN THE ENDPOINT ##
                    
                    if self.endpoint == False:
                        
                        if self.user != None:
                            await interaction.followup.send(f"Registered to: {self.user['email']}")
                        else:
                            await interaction.followup.send("User not found, please / open to open a ticket",ephemeral=True)
                            await interaction.user.remove_roles(self.premium_role)
                    
                    ## USER FOUND, NEW ENTRY IN THE DATABASE ##
                    
                    else:
                        
                        if self.endpoint["util"] == "premium":
                            
                            await db.struct_premium(email,interaction.user.id)
                            await interaction.followup.send("Successfully registerd",ephemeral=True)

                        elif self.endpoint["util"] == "standard":
                                
                                await db.struct_standard(email,interaction.user.id)
                                await interaction.user.remove_roles(self.premium_role)
                                await interaction.user.add_roles(self.standard_role)
                                await interaction.followup.send("Updated",ephemeral=True)
                        
                        else:

                            await interaction.followup.send("Error")

                        
                ## IF EMAIL ID EXISTS IN THE DB BUT THE USER FILED IS EMPTY, WE UPDATE THE USER ID AND SEND A KEY ##
                    
                elif self.info != None and self.info['user_id']=="":

                    if self.info["util"] == "premium":

                        await db.update_verification(email,interaction.user.id)
                        await db.update_keys(email,interaction.user.id)
                        await interaction.followup.send("Successfully registered",ephemeral=True)

                        self.prem_key =  await key.premium_key()
                        
                        if self.prem_key == False:

                            await interaction.followup.send("Authy is down, please try again later",ephemeral=True)
                        
                        elif self.prem_key != False:

                            try:
                                self.channel = await interaction.user.create_dm()
                                await self.channel.send(f'''Premium key : -
{self.prem_key}''')
                                await db.dm_key_successfull(email)
                                await interaction.followup.send("Key sent in DMS",ephemeral=True)
                            except discord.errors.Forbidden:
                                await interaction.followup.send("You're DMS are turned off, bot can't send you the keys",ephemeral=True)
                    
                        else:

                            await interaction.followup.send("Error",ephemeral=True)
                    
                    elif self.info['util'] == "standard":
                        
                        await db.update_verification(email,interaction.user.id)
                        await interaction.user.remove_roles(self.premium_role)
                        await interaction.user.add_roles(self.standard_role)
                        await interaction.followup.send("Updated",ephemeral=True)
                        

                ## CHECKING IF THE USER RECIEVED A DM OR NOT ##
                
                elif self.dm != None and self.dm["user_id"] == interaction.user.id and self.dm['dm']==0 and self.info["util"]=="premium":

                    self.prem_key = await key.premium_key()

                    if self.prem_key == False:

                        await interaction.followup.send("Authy is down, please try again later",ephemeral=True)
                    
                    elif self.prem_key != False:

                        try:
                            self.channel = await interaction.user.create_dm()
                            await self.channel.send(f'''Premium key : -
{self.prem_key}''')
                            await db.dm_key_successfull(email)
                            await interaction.followup.send("Key sent in DMS",ephemeral=True)

                        except discord.errors.Forbidden:
                            await interaction.followup.send("You're DMS are turned off, bot can't send you the keys",ephemeral=True)
                
                ## IF EVERYTHING IS SUFFICED FOR OLD MEMBER ##

                elif (self.dm != None and self.dm["user_id"] == interaction.user.id and self.dm['dm']==1) and (self.info != None and  self.info['user_id']==interaction.user.id and self.info["util"] == "premium"):
                    
                    await interaction.followup.send("Already registered",ephemeral=True) 

                ## IF EVERYTHING IS SUFFICED FOR NEW MEMBERS ##
            
                elif (self.dm == None) and (self.info != None and  self.info['user_id']==interaction.user.id and self.info["util"] == "premium"):
                    
                    await interaction.followup.send("Already registered",ephemeral=True) 
                
                elif  self.info != None and  self.info['user_id']== interaction.user.id and self.info["util"] == "standard":
                    await interaction.user.remove_roles(self.premium_role)
                    await interaction.user.add_roles(self.standard_role)
                    await interaction.followup.send("Updated",ephemeral=True)
                
                else:
                    
                    await interaction.followup.send("Error",ephemeral=True)

            ## CHECKING IF USER HAS STANDARD ##        
            
            if self.standard_role in interaction.user.roles:

                ## IF EMAIL DOESNT EXIST IN THE DATABASE, ITS USING THE ENDPOINTS TO CHECK ##

                if self.info == None:

                    ## IF USER NOT FOUND IN THE ENDPOINT ##
                    
                    if self.endpoint == False:
                        
                        if self.user != None:
                            await interaction.followup.send(f"Registered to: {self.user['email']}")
                        else:
                            await interaction.followup.send("User not found, please / open to open a ticket",ephemeral=True)
                            await interaction.user.remove_roles(self.standard_role)
                    
                    
                    ## USER FOUND, NEW ENTRY IN THE DATABASE ##
                    
                    else:
                        
                        if self.endpoint["util"] == "standard":
                            
                            await db.struct_standard(email,interaction.user.id)
                            await interaction.followup.send("Successfully registerd",ephemeral=True)
                        
                        elif self.endpoint["util"] == "premium":
                            
                            await db.struct_premium(email,interaction.user.id)
                            await interaction.user.remove_roles(self.standard_role)
                            await interaction.user.add_roles(self.premium_role)
                            await interaction.followup.send("Updated",ephemeral=True)
                        
                        else:
                            await interaction.followup.send("Error")
                    
                ## IF EMAIL ID EXISTS IN THE DB BUT THE USER FILED IS EMPTY, WE UPDATE THE USER ID AND SEND A KEY ##
                    
                elif self.info != None and self.info['user_id']=="" and self.info["util"]=="standard":

                    await db.update_verification(email,interaction.user.id)
                    await db.update_keys(email,interaction.user.id)
                    await interaction.followup.send("Successfully registered",ephemeral=True)
                
                ## IF EVERYTHING IS SUFFICED ##

                elif  self.info != None and  self.info['user_id']== interaction.user.id and self.info["util"] == "standard":
                    
                    await interaction.followup.send("Already registered",ephemeral=True) 
                
                
                elif  self.info != None and  self.info['user_id']== interaction.user.id and self.info["util"] == "premium":
                    await interaction.user.remove_roles(self.standard_role)
                    await interaction.user.add_roles(self.premium_role)
                    await interaction.followup.send("Updated",ephemeral=True)
                
                else:
                    await interaction.followup.send("Error")

            ## IF THE USER HAS NO ROLES ##
            
            if (self.standard_role not in interaction.user.roles) and (self.premium_role not in interaction.user.roles):

                ## CHECKING IF THE USER IS IN THE DATABASE ##
                
                if self.info == None:

                    ## IF USER NOT FOUND IN THE ENDPOINT ##
                    
                    if self.endpoint == False:
                        
                        await interaction.followup.send("User not found, please / open to open a ticket",ephemeral=True)

                    ## USER FOUND, NEW ENTRY IN THE DATABASE ##
                    
                    else:
                        
                        if self.endpoint["util"] == "standard":
                            
                            await db.struct_standard(email,interaction.user.id)
                            await interaction.user.add_roles(self.standard_role)
                            await interaction.followup.send("Standard role given",ephemeral=True)

                        elif self.endpoint["util"] == "premium":

                            await db.struct_premium(email,interaction.user.id)
                            await interaction.user.add_roles(self.premium_role)
                            await interaction.followup.send("Premium role given",ephemeral=True)
                        
                        else:

                            await interaction.followup.send("Error")
                    
                ## IF EMAIL ID EXISTS IN THE DB BUT THE USER FILED IS EMPTY, WE UPDATE THE USER ID AND SEND A KEY ##
                    
                elif self.info != None and self.info['user_id']=="":

                    if self.info["util"] == "premium":

                        await interaction.user.add_roles(self.premium_role)
                        await db.update_verification(email,interaction.user.id)
                        await db.update_keys(email,interaction.user.id)
                        await interaction.followup.send("Successfully registered",ephemeral=True)

                        self.prem_key =  await key.premium_key()
                        
                        if self.prem_key == False:

                            await interaction.followup.send("Authy is down, please try again later",ephemeral=True)
                        
                        elif self.prem_key != False:

                            try:
                                self.channel = await interaction.user.create_dm()
                                await self.channel.send(f'''Premium key : -
{self.prem_key}''')
                                await db.dm_key_successfull(email)
                                await interaction.followup.send("Key sent in DMS",ephemeral=True)
                            except discord.errors.Forbidden:
                                await interaction.followup.send("You're DMS are turned off, bot can't send you the keys",ephemeral=True)
                        
                        else:

                            await interaction.followup.send("Error",ephemeral=True)

                    else:
                        
                        await interaction.user.add_roles(self.standard_role)
                        await db.update_verification(email,interaction.user.id)
                        await interaction.followup.send("Successfully registered",ephemeral=True)
                
                ## IF EVERYTHING IS SUFFICED FOR OLD CUSTOMER ##

                elif (self.dm != None and self.dm["user_id"] == interaction.user.id and self.dm['dm']==1) and (self.info != None and  self.info['user_id'] == interaction.user.id):

                    if self.info["util"] == "premium":
                        await interaction.user.add_roles(self.premium_role)
                        await interaction.followup.send("Registered, Role given successfully",ephemeral=True)


                    elif self.info["util"] == "standard":
                        await interaction.user.add_roles(self.standard_role)
                        await interaction.followup.send("Registered, Role given successfully",ephemeral=True)

                    else:
                        await interaction.followup.send("Error",ephemeral=True)
                
                ## CHECKING IF THE KEYS WERE SENT TO THE USER ##

                elif (self.dm != None and self.dm["user_id"] == interaction.user.id and self.dm['dm']==0) and (self.info != None and  self.info['user_id'] == interaction.user.id):

                        await interaction.user.add_roles(self.premium_role)
                        await interaction.followup.send("Added premium role successfully")
                        self.prem_key =  await key.premium_key()
                        
                        if self.prem_key == False:

                            await interaction.followup.send("Authy is down, please try again later",ephemeral=True)
                        
                        elif self.prem_key != False:

                            try:
                                self.channel = await interaction.user.create_dm()
                                await self.channel.send(f'''Premium key : -
{self.prem_key}''')
                                await db.dm_key_successfull(email)
                                await interaction.followup.send("Key sent in DMS",ephemeral=True)
                            except discord.errors.Forbidden:
                                await interaction.followup.send("You're DMS are turned off, bot can't send you the keys",ephemeral=True)
                        
                        else:

                            await interaction.followup.send("Error",ephemeral=True)
                ## IF EVERYTHING IS SUFFICED FOR NEW CUSTOMER ##
                
                elif (self.dm == None) and (self.info != None and  self.info['user_id'] == interaction.user.id ):
                    
                    if self.info["util"] == "premium":
                        await interaction.user.add_roles(self.premium_role)
                        await interaction.followup.send("Registered, Role given successfully",ephemeral=True)

                    elif self.info["util"] == "standard":
                        await interaction.user.add_roles(self.standard_role)
                        await interaction.followup.send("Registered, Role given successfully",ephemeral=True)

                    else:
                        await interaction.followup.send("Error",ephemeral=True)
                
                else:
                    
                    await interaction.followup.send("Error")

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await interaction.followup.send("An unexpected error occurred. Try again ", ephemeral=True)

async def setup(bot):
        await bot.add_cog(Verify(bot),guilds = [discord.Object(id=settings.GUILD_ID)])
            
