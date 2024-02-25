import discord 
from discord.ext import commands
from discord import app_commands
from utility import db,key,payment,constants,embed
import settings
import asyncio


class Verification(commands.Cog):

    def __init__(self,bot:commands.Bot):

        self.bot = bot
        self.bot.remove_command("help")

    @commands.Cog.listener()
    async def on_ready(self):
         print("Verification cog loaded")
        
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
    async def verify(self, interaction :discord.Interaction,email : str):

            self.logging = interaction.guild.get_channel(1202584731896651876)
            self.premium_role = 1196567144847118346
            self.standard_role = 1196567231786664017
            self.standard_download = interaction.guild.get_channel(1196576005758926978)
            self.standard_rev = interaction.guild.get_channel(1196575312650174594)
            self.premium_download = interaction.guild.get_channel(1196576005758926978)
            self.premium_rev = interaction.guild.get_channel(1196574152367284264)
            self.embed_old =  embed.old_prem_embed(self.premium_download,self.premium_rev)
            self.embed_new =  embed.new_prem_embed(self.premium_download,self.premium_rev)
            self.embed_stan =  embed.stan_embed(self.standard_download,self.standard_rev)
            self.dms_failed =   embed.dms_failed()
            self.email_not_found = embed.email_not_found()
        
        # try:

            await interaction.response.defer(ephemeral=True)  

            ## CHECKING THE ID IN THE DATABASE ##

            self.info = await db.find_email_main(email) 
            self.dm = await db.find_dm(email)
            self.endpoint = await payment.endpoint(email)
            self.user = await db.find_user(interaction.user.id)
            ## CHECKING IF USER HAS BOTH STANDARD AND PREMIUM ROLE ##

            if (self.premium_role in interaction.user.roles) and (self.standard_role in interaction.user.roles):

                ## IF EMAIL DOESNT EXIST IN THE DATABASE, ITS USING THE ENDPOINTS TO CHECK ##

                if self.info == None:

                    ## IF USER NOT FOUND IN THE ENDPOINT ##
                    
                    if self.endpoint == False:
                        
                        if self.user != None:
                            await interaction.followup.send(f"Registered to: {self.user['email']}")
                        else:
                            await interaction.user.remove_roles(self.premium_role)
                            await interaction.user.remove_roles(self.standard_role)
                            await interaction.followup.send(embed = await self.email_not_found,ephemeral=True)
                    
                    ## USER FOUND, NEW ENTRY IN THE DATABASE ##
                    
                    else:
                        
                        if self.endpoint["util"] == "premium":
                            
                            await db.struct_premium(email,interaction.user.id)
                            await interaction.user.remove_roles(self.standard_role)
                            await interaction.followup.send(embed = self.embed_new,ephemeral=True)
                            await asyncio.sleep(3)
                            await self.logging.send(f"{interaction.user.mention} is registered to {email} as Premium customer")


                        elif self.endpoint["util"] == "standard":
                                
                                await db.struct_standard(email,interaction.user.id)
                                await interaction.user.remove_roles(self.premium_role)
                                await interaction.followup.send(embed = self.embed_stan,ephemeral=True)
                                await asyncio.sleep(3)
                                await self.logging.send(f"{interaction.user.mention} is registered to {email} as Standard customer")
                        
                        elif self.endpoint["util"] == "both":
                            
                            await db.struct_both(email,interaction.user.id)                          
                            await interaction.followup.send(embed=self.embed_new,ephemeral=True)
                            await asyncio.sleep(3)
                            await self.logging.send(f"{interaction.user.mention} is registered to {email} as Premium and Standard customer")

                        else:

                            await interaction.followup.send("Error registering from the endpoint",ephemeral=True)
                
                elif self.info != None and self.info['user_id']=="":

                    if self.info["util"] == "premium":

                        await db.update_verification(email,interaction.user.id)
                        await db.update_keys(email,interaction.user.id)
                        await interaction.user.remove_roles(self.standard_role)
                        await interaction.followup.send(embed = self.embed_old,ephemeral=True)
                        await asyncio.sleep(3)
                        await self.logging.send(f"{interaction.user.mention} is registered to {email} as Old premium customer")

                        self.prem_key =  await key.premium_key()
                        
                        if self.prem_key == False:

                            await interaction.followup.send("Authy is down, please try again later",ephemeral=True)
                        
                        elif self.prem_key != False:

                            try:
                                self.channel = await interaction.user.create_dm()
                                await self.channel.send(self.prem_key)
                                await db.dm_key_successfull(email)
                                await interaction.followup.send(embed = self.embed_old,ephemeral=True)
                                await asyncio.sleep(3)
                                await self.logging.send(f"{interaction.user.mention} recieved the premium key")
                            except discord.errors.Forbidden:
                                await interaction.followup.send(embed = await self.dms_failed,ephemeral=True)
                    
                        else:

                            await interaction.followup.send("Error",ephemeral=True)
                    
                    elif self.info['util'] == "standard":
                        
                        await db.update_verification(email,interaction.user.id)
                        await interaction.user.remove_roles(self.premium_role)
                        await interaction.followup.send(embed = self.embed_stan,ephemeral=True)
                        await asyncio.sleep(3)
                        await self.logging.send(f"{interaction.user.mention} is registered to {email} as Old standard customer")                      

                ## CHECKING IF THE USER RECIEVED A DM OR NOT ##
                
                elif self.dm != None and self.dm["user_id"] == interaction.user.id and self.dm['dm']==0 and self.info["util"]=="premium":
                    
                    await interaction.user.remove_roles(self.standard_role)
                    self.prem_key = await key.premium_key()

                    if self.prem_key == False:

                        await interaction.followup.send("Authy is down, please try again later",ephemeral=True)
                    
                    elif self.prem_key != False:

                        try:
                            self.channel = await interaction.user.create_dm()
                            await self.channel.send(self.prem_key)
                            await db.dm_key_successfull(email)
                            await interaction.followup.send(embed = self.embed_old,ephemeral=True)
                            await asyncio.sleep(3)
                            await self.logging.send(f"{interaction.user.mention} recieved the Premium key")

                        except discord.errors.Forbidden:
                            await interaction.followup.send(embed = await self.dms_failed,ephemeral=True)
                
                ## IF EVERYTHING IS SUFFICED FOR OLD MEMBER ##

                elif (self.dm != None and self.dm["user_id"] == interaction.user.id and self.dm['dm']==1) and (self.info != None and  self.info['user_id']==interaction.user.id and self.info["util"] == "premium" ):
                    
                    await interaction.user.remove_roles(self.standard_role)
                    await interaction.followup.send("Already registered as premium user, removed the standard role",ephemeral=True) 

                ## IF EVERYTHING IS SUFFICED FOR NEW MEMBERS ##
            
                elif (self.dm == None) and (self.info != None and  self.info['user_id']==interaction.user.id and self.info["util"] == "premium" and self.endpoint['util'] == "premium"):
                    await interaction.user.remove_roles(self.standard_role)
                    await interaction.followup.send("Already registered as premium, removing the standard role",ephemeral=True) 
                
                elif  self.info != None and  self.info['user_id']== interaction.user.id and self.info["util"] == "standard" and self.endpoint['util'] == "standard":
                    await interaction.user.remove_roles(self.premium_role)
                    await interaction.followup.send("Already registered as standard role, removed premium role and given standard role",ephemeral=True)
                
                elif (self.dm == None) and (self.info != None and  self.info['user_id']==interaction.user.id and self.info["util"] == "both" and self.endpoint['util'] == 'both'):

                    await interaction.followup.send("Already registered ",ephemeral=True)
                
                elif (self.dm == None) and (self.info != None and  self.info['user_id']==interaction.user.id and self.info["util"] == "premium" and self.endpoint['util'] == "both"):
                    await db.delete_email(email)
                    await db.struct_both(email,interaction.user.id)
                    await interaction.followup.send("Registered to both",ephemeral=True)
                
                elif (self.dm == None) and (self.info != None and  self.info['user_id']==interaction.user.id and self.info["util"] == "standard" and self.endpoint['util'] == "both"):
                    await db.delete_email(email)
                    await db.struct_both(email,interaction.user.id)
                    await interaction.followup.send("Registered to both",ephemeral=True)
                
                elif self.info['user_id'] != interaction.user.id:
                    await interaction.followup.send(f"Mail account is already registered by <@{self.info['user_id']}>",ephemeral=True)

                else:
                    
                    await interaction.followup.send("Error",ephemeral=True)
                    

            ## CHECKING IF THE USER HAS THE PREMIUM ROLE ##

            elif (self.premium_role in interaction.user.roles) and (self.standard_role not in interaction.user.roles):
                print("here")
                ## IF EMAIL DOESNT EXIST IN THE DATABASE, ITS USING THE ENDPOINTS TO CHECK ##

                if self.info == None:

                    ## IF USER NOT FOUND IN THE ENDPOINT ##
                    
                    if self.endpoint == False:
                        
                        if self.user != None:
                            await interaction.followup.send(f"Registered to: {self.user['email']}")
                        else:
                            await interaction.user.remove_roles(self.premium_role)
                            await interaction.followup.send(embed = await self.email_not_found,ephemeral=True)
                    
                    ## USER FOUND, NEW ENTRY IN THE DATABASE ##
                    
                    else:
                        
                        if self.endpoint["util"] == "premium":
                            
                            await db.struct_premium(email,interaction.user.id)
                            await interaction.followup.send(embed = self.embed_new,ephemeral=True)
                            await asyncio.sleep(3)
                            await self.logging.send(f"{interaction.user.mention} is registered to {email} as Premium customer")

                        elif self.endpoint["util"] == "standard":
                                
                                await db.struct_standard(email,interaction.user.id)
                                await interaction.user.remove_roles(self.premium_role)
                                await interaction.user.add_roles(self.standard_role)
                                await interaction.followup.send(embed = self.embed_stan,ephemeral=True)
                                await asyncio.sleep(3)
                                await self.logging.send(f"{interaction.user.mention} is registered to {email} as Premium customer")
                        
                        elif self.endpoint["util"] == "both":
                            
                            await db.struct_both(email,interaction.user.id)
                            await asyncio.sleep(3)
                            await interaction.user.add_roles(self.standard_role)
                            await interaction.followup.send("Successfully registered to both premium and standaed role, added the standard role",ephemeral=True)
                            await self.logging.send(f"{interaction.user.mention} is registered to {email} as Premium and Standard customer")
                        
                        else:

                            await interaction.followup.send("Error registering from the endpoint",ephemeral=True)

                        
                ## IF EMAIL ID EXISTS IN THE DB BUT THE USER FILED IS EMPTY, WE UPDATE THE USER ID AND SEND A KEY ##
                    
                elif self.info != None and self.info['user_id']=="":

                    if self.info["util"] == "premium":

                        await db.update_verification(email,interaction.user.id)
                        await db.update_keys(email,interaction.user.id)
                        await asyncio.sleep(3)
                        await self.logging.send(f"{interaction.user.mention} is registered to {email} as Old Premium customer")
                        print(1)
                        self.prem_key =  await key.premium_key()
                        print(2)
                        if self.prem_key == False:

                            await interaction.followup.send("Authy is down, please try again later",ephemeral=True)
                        
                        elif self.prem_key != False:

                            try:
                                print(3)
                                self.channel = await interaction.user.create_dm()
                                await self.channel.send(self.prem_key)
                                await db.dm_key_successfull(email)
                                await interaction.followup.send(embed = self.embed_old,ephemeral=True)
                                await asyncio.sleep(3)
                                await self.logging.send(f"{interaction.user.mention} recieved the premium key")
                            except discord.errors.Forbidden:
                                await interaction.followup.send(embed = await self.dms_failed,ephemeral=True)
                    
                        else:

                            await interaction.followup.send("Error",ephemeral=True)
                    
                    elif self.info['util'] == "standard":
                        
                        await db.update_verification(email,interaction.user.id)
                        await interaction.user.remove_roles(self.premium_role)
                        await interaction.user.add_roles(self.standard_role)
                        await interaction.followup.send("Successfully registered to standard role",ephemeral=True)
                        await asyncio.sleep(3)
                        await self.logging.send(f"{interaction.user.mention} is registered to {email} as Standard customer")
                        

                ## CHECKING IF THE USER RECIEVED A DM OR NOT ##
                
                elif self.dm != None and self.dm["user_id"] == interaction.user.id and self.dm['dm']==0 and self.info["util"]=="premium":

                    self.prem_key = await key.premium_key()

                    if self.prem_key == False:

                        await interaction.followup.send("Authy is down, please try again later",ephemeral=True)
                    
                    elif self.prem_key != False:

                        try:
                            self.channel = await interaction.user.create_dm()
                            await self.channel.send(self.prem_key)
                            await db.dm_key_successfull(email)
                            await interaction.followup.send("Key sent in DMS",ephemeral=True)
                            await asyncio.sleep(3)
                            await self.logging.send(f"{interaction.user.mention} recieved the premium key")

                        except discord.errors.Forbidden:
                            await interaction.followup.send("You're DMS are turned off, bot can't send you the keys",ephemeral=True)
                
                ## IF EVERYTHING IS SUFFICED FOR OLD MEMBER ##

                elif (self.dm != None and self.dm["user_id"] == interaction.user.id and self.dm['dm']==1) and (self.info != None and  self.info['user_id']==interaction.user.id and self.info["util"] == "premium"):
                    
                    await interaction.followup.send("Already registered",ephemeral=True) 

                ## IF EVERYTHING IS SUFFICED FOR NEW MEMBERS ##
            
                elif (self.dm == None) and (self.info != None and  self.info['user_id']==interaction.user.id and self.info["util"] == "premium" and self.endpoint['util'] == "premium"):
                    
                    await interaction.followup.send("Already registered",ephemeral=True) 
                
                elif  self.info != None and  self.info['user_id']== interaction.user.id and self.info["util"] == "standard" and self.endpoint['util'] == "standard":
                    await interaction.user.remove_roles(self.premium_role)
                    await interaction.user.add_roles(self.standard_role)
                    await interaction.followup.send("Updated, removed premium role and given standard role",ephemeral=True)
                
                elif (self.dm == None) and (self.info != None and  self.info['user_id']==interaction.user.id and self.info["util"] == "both" and self.endpoint['util'] == "both"):
                    await interaction.user.add_roles(self.standard_role)
                    await interaction.followup.send("Updated, added the standard role ",ephemeral=True)
                
                elif (self.dm == None) and (self.info != None and  self.info['user_id']==interaction.user.id and self.info["util"] == "premium" and self.endpoint['util'] == "both"):
                    await db.delete_email(email)
                    await db.struct_both(email,interaction.user.id)
                    await interaction.user.add_roles(self.standard_role)
                    await interaction.followup.send("Updated, registered to both and given the standard role",ephemeral=True)
                
                elif (self.dm == None) and (self.info != None and  self.info['user_id']==interaction.user.id and self.info["util"] == "standard" and self.endpoint['util'] == "both"):
                    await db.delete_email(email)
                    await db.struct_both(email,interaction.user.id)
                    await interaction.user.add_roles(self.standard_role)
                    await interaction.followup.send("Updated, registered to both given the standard role",ephemeral=True)
                
                elif self.info['user_id'] != interaction.user.id:
                    await interaction.followup.send(f"Mail account is already registered by <@{self.info['user_id']}>",ephemeral=True)

                else:
                    
                    await interaction.followup.send("Error",ephemeral=True)

            ## CHECKING IF USER HAS STANDARD ##        
            
            elif (self.standard_role in interaction.user.roles) and (self.premium_role not in interaction.user.roles):

                ## IF EMAIL DOESNT EXIST IN THE DATABASE, ITS USING THE ENDPOINTS TO CHECK ##

                if self.info == None:

                    ## IF USER NOT FOUND IN THE ENDPOINT ##
                    
                    if self.endpoint == False:
                        
                        if self.user != None:
                            await interaction.followup.send(f"Registered to: {self.user['email']}",ephemeral=True)
                        else:
                            await interaction.followup.send(embed = await self.email_not_found,ephemeral=True)
                            await interaction.user.remove_roles(self.standard_role)
                    
                    
                    ## USER FOUND, NEW ENTRY IN THE DATABASE ##
                    
                    else:
                        
                        if self.endpoint["util"] == "standard":
                            
                            await db.struct_standard(email,interaction.user.id)
                            await interaction.followup.send(embed = self.embed_stan,ephemeral=True)
                            await asyncio.sleep(3)
                            await self.logging.send(f"{interaction.user.mention} is registered to {email} as Standard customer")
                        
                        elif self.endpoint["util"] == "premium":
                            
                            await db.struct_premium(email,interaction.user.id)
                            await interaction.user.remove_roles(self.standard_role)
                            await interaction.user.add_roles(self.premium_role)
                            await interaction.followup.send(embed = self.embed_new,ephemeral=True)
                            await asyncio.sleep(3)
                            await self.logging.send(f"{interaction.user.mention} is registered to {email} as Premium customer")
                        
                        elif self.endpoint["util"] == "both":
                            
                            await db.struct_both(email,interaction.user.id)
                            await asyncio.sleep(3)
                            await self.logging.send(f"{interaction.user.mention} is registered to {email} as Premium and Standard customer")
                            await interaction.user.add_roles(self.premium_role)
                            await interaction.followup.send(embed = self.embed_new,ephemeral=True)      
                        
                        else:
                            await interaction.followup.send("Error",ephemeral=True)
                
                ## IF EVERYTHING IS SUFFICED ##

                elif  self.info != None and  self.info['user_id']== interaction.user.id and self.info["util"] == "standard" and self.endpoint['util'] == "standard":
                    
                    await interaction.followup.send("Already registered",ephemeral=True) 
                
                elif self.info != None and self.info['user_id']=="":

                    if self.info["util"] == "premium":
                        await interaction.user.remove_roles(self.standard_role)
                        await interaction.user.add_roles(self.premium_role)
                        await db.update_verification(email,interaction.user.id)
                        await db.update_keys(email,interaction.user.id)
                        await asyncio.sleep(3)
                        await self.logging.send(f"{interaction.user.mention} is registered to {email} as Old Premium customer")

                        self.prem_key =  await key.premium_key()
                        
                        if self.prem_key == False:

                            await interaction.followup.send("Authy is down, please try again later",ephemeral=True)
                        
                        elif self.prem_key != False:

                            try:
                                self.channel = await interaction.user.create_dm()
                                await self.channel.send(self.prem_key)
                                await db.dm_key_successfull(email)
                                await interaction.followup.send(embed = self.embed_old,ephemeral=True)
                                await asyncio.sleep(3)
                                await self.logging.send(f"{interaction.user.mention} recieved the premium key")
                            except discord.errors.Forbidden:
                                await interaction.followup.send(embed = await self.dms_failed,ephemeral=True)
                    
                        else:

                            await interaction.followup.send("Error",ephemeral=True)
                    
                    elif self.info['util'] == "standard":
                        
                        await db.update_verification(email,interaction.user.id)
                        await interaction.followup.send(embed = self.embed_stan,ephemeral=True)
                        await asyncio.sleep(3)
                        await self.logging.send(f"{interaction.user.mention} is registered to {email} as Standard customer")
                        

                ## CHECKING IF THE USER RECIEVED A DM OR NOT ##
                
                elif self.dm != None and self.dm["user_id"] == interaction.user.id and self.dm['dm']==0 and self.info["util"]=="premium":
                    await interaction.user.remove_roles(self.standard_role)
                    await interaction.user.add_roles(self.premium_role)
                    self.prem_key = await key.premium_key()

                    if self.prem_key == False:

                        await interaction.followup.send("Authy is down, please try again later",ephemeral=True)
                    
                    elif self.prem_key != False:

                        try:
                            self.channel = await interaction.user.create_dm()
                            await self.channel.send(self.prem_key)
                            await db.dm_key_successfull(email)
                            await interaction.followup.send(embed = self.embed_old,ephemeral=True)
                            await asyncio.sleep(3)
                            await self.logging.send(f"{interaction.user.mention} recieved the premium key")

                        except discord.errors.Forbidden:
                            await interaction.followup.send(embed = await self.dms_failed,ephemeral=True)
                
                elif self.dm != None and self.dm["user_id"] == interaction.user.id and self.dm['dm']==1 and self.info["util"]=="premium":
                     await interaction.user.remove_roles(self.standard_role)
                     await interaction.user.add_roles(self.premium_role)
                     await interaction.followup.send("Registered as a premium member",ephemeral=True)

                elif  self.info != None and  self.info['user_id']== interaction.user.id and self.info["util"] == "premium" and self.endpoint['util'] == "premium":
                    await interaction.user.remove_roles(self.standard_role)
                    await interaction.user.add_roles(self.premium_role)
                    await interaction.followup.send("Registered to premium role",ephemeral=True)
                
                elif (self.dm == None) and (self.info != None and  self.info['user_id']==interaction.user.id and self.info["util"] == "both" and self.endpoint['util'] == "both"):
                    await interaction.user.add_roles(self.premium_role)
                    await interaction.followup.send("Registered to both, added premium role",ephemeral=True)
                
                elif (self.dm == None) and (self.info != None and  self.info['user_id']==interaction.user.id and self.info["util"] == "premium" and self.endpoint['util'] == "both"):
                    await db.delete_email(email)
                    await db.struct_both(email,interaction.user.id)
                    await interaction.user.add_roles(self.premium_role)
                    await interaction.followup.send("Registered to both and given the premium role",ephemeral=True)
                
                elif (self.dm == None) and (self.info != None and  self.info['user_id']==interaction.user.id and self.info["util"] == "standard" and self.endpoint['util'] == "both"):
                    await db.delete_email(email)
                    await db.struct_both(email,interaction.user.id)
                    await interaction.user.add_roles(self.premium_role)
                    await interaction.followup.send("Registered to both and given the premium role",ephemeral=True)
                
                elif self.info["user_id"] == interaction.user.id:
                    await interaction.followup.send(f"Email is already assigned to <@{self.info['user_id']}>")
                
                else:
                    await interaction.followup.send("Error",ephemeral=True)

            ## IF THE USER HAS NO ROLES ##
            
            elif (self.standard_role not in interaction.user.roles) and (self.premium_role not in interaction.user.roles):

                ## CHECKING IF THE USER IS IN THE DATABASE ##
                
                if self.info == None:

                    ## IF USER NOT FOUND IN THE ENDPOINT ##
                    
                    if self.endpoint == False:
                        
                        await interaction.followup.send(embed=await self.email_not_found,ephemeral=True)

                    ## USER FOUND, NEW ENTRY IN THE DATABASE ##
                    
                    else:
                        
                        if self.endpoint["util"] == "standard":
                            
                            await db.struct_standard(email,interaction.user.id)
                            await interaction.user.add_roles(self.standard_role)
                            await interaction.followup.send(embed= self.embed_stan,ephemeral=True)
                            await asyncio.sleep(3)
                            await self.logging.send(f"{interaction.user.mention} is registered to {email} as Standard customer")

                        elif self.endpoint["util"] == "premium":
                            await db.struct_premium(email,interaction.user.id)
                            await interaction.user.add_roles(self.premium_role)
                            await interaction.followup.send(embed = self.embed_new(self.down,self.rev),ephemeral=True)
                            await asyncio.sleep(3)
                            await self.logging.send(f"{interaction.user.mention} is registered to {email} as Premium customer")
                        
                        elif self.endpoint["util"] == "both":
                            
                            await db.struct_both(email,interaction.user.id)
                            await interaction.user.add_roles(self.premium_role)
                            await interaction.user.add_roles(self.standard_role)
                            await interaction.followup.send(embed=self.embed_new,ephemeral=True)
                            await asyncio.sleep(3)
                            await self.logging.send(f"{interaction.user.mention} is registered to {email} as Premium and Standard customer")
                        
                        else:

                            await interaction.followup.send("Error",ephemeral=True)
                    
                ## IF EMAIL ID EXISTS IN THE DB BUT THE USER FILED IS EMPTY, WE UPDATE THE USER ID AND SEND A KEY ##
                    
                elif self.info != None and self.info['user_id']=="":

                    if self.info["util"] == "premium":

                        await interaction.user.add_roles(self.premium_role)
                        await db.update_verification(email,interaction.user.id)
                        await db.update_keys(email,interaction.user.id)
                        await interaction.followup.send(embed=self.embed_old,ephemeral=True)
                        await asyncio.sleep(3)
                        await self.logging.send(f"{interaction.user.mention} is registered to {email} as Old Premium customer")

                        self.prem_key =  await key.premium_key()
                        
                        if self.prem_key == False:

                            await interaction.followup.send("Authy is down, please try again later",ephemeral=True)
                        
                        elif self.prem_key != False:

                            try:
                                self.channel = await interaction.user.create_dm()
                                await self.channel.send(self.prem_key)
                                await db.dm_key_successfull(email)
                                await interaction.followup.send(embed=self.embed_old,ephemeral=True)
                                await asyncio.sleep(3)
                                await self.logging.send(f"{interaction.user.mention} recieved the Premium key")
                            except discord.errors.Forbidden:
                                await interaction.followup.send(embed=await self.dms_failed(),ephemeral=True)
                        
                        else:

                            await interaction.followup.send("Error",ephemeral=True)

                    else:
                        
                        await interaction.user.add_roles(self.standard_role)
                        await db.update_verification(email,interaction.user.id)
                        await interaction.followup.send("Successfully registered to standard role",ephemeral=True)
                
                ## IF EVERYTHING IS SUFFICED FOR OLD CUSTOMER ##

                elif (self.dm != None and self.dm["user_id"] == interaction.user.id and self.dm['dm']==1) and (self.info != None and  self.info['user_id'] == interaction.user.id):

                    if self.info["util"] == "premium":
                        await interaction.user.add_roles(self.premium_role)
                        await interaction.followup.send("Registered as premium, Role given successfully",ephemeral=True)

                    else:
                        await interaction.followup.send("Error",ephemeral=True)
                
                ## CHECKING IF THE KEYS WERE SENT TO THE USER ##

                elif (self.dm != None and self.dm["user_id"] == interaction.user.id and self.dm['dm']==0) and (self.info != None and  self.info['user_id'] == interaction.user.id):

                        await interaction.user.add_roles(self.premium_role)
                        await interaction.followup.send("Successfully registered, added premium role successfully",ephemeral=True)
                        self.prem_key =  await key.premium_key()
                        
                        if self.prem_key == False:

                            await interaction.followup.send("Authy is down, please try again later",ephemeral=True)
                        
                        elif self.prem_key != False:

                            try:
                                self.channel = await interaction.user.create_dm()
                                await self.channel.send(self.prem_key)
                                await db.dm_key_successfull(email)
                                await interaction.followup.send(embed=self.embed_old,ephemeral=True)
                            except discord.errors.Forbidden:
                                await interaction.followup.send(embed=await self.dms_failed,ephemeral=True)
                        
                        else:

                            await interaction.followup.send("Error",ephemeral=True)
                ## IF EVERYTHING IS SUFFICED FOR NEW CUSTOMER ##
                elif (self.dm != None and self.dm["user_id"] == interaction.user.id and self.dm['dm']==1) and (self.info != None and  self.info['user_id'] == interaction.user.id):
                    await interaction.user.add_roles(self.premium_role)
                    await interaction.followup.send("Registered and given the premium role",ephemeral=True)

                elif (self.dm == None) and (self.info != None and  self.info['user_id'] == interaction.user.id ):
                    
                    if self.info["util"] == "premium" and self.endpoint['util'] == "premium":
                        await interaction.user.add_roles(self.premium_role)
                        await interaction.followup.send("Successfully registered as premium, Role given successfully",ephemeral=True)

                    elif self.info["util"] == "standard" and self.endpoint['util'] == "standard":
                        await interaction.user.add_roles(self.standard_role)
                        await interaction.followup.send("Successfully registered as standard, Role given successfully",ephemeral=True)
                    
                    elif self.info["util"] == "both" and self.endpoint['util'] == "both":
                        await interaction.user.add_roles(self.standard_role)
                        await interaction.user.add_roles(self.premium_role)
                        await interaction.followup.send("Successfully registered to both, Roles given successfully",ephemeral=True)               

                    elif self.info["util"] == "standard" and self.endpoint['util'] == "both":
                        await db.delete_email(email)
                        await db.struct_both(email,interaction.user.id)
                        await interaction.user.add_roles(self.standard_role)
                        await interaction.user.add_roles(self.premium_role)
                        await interaction.followup.send("Registered, added both premium and standard role",ephemeral=True)
                    
                    elif self.info["util"] == "premium" and self.endpoint['util'] == "both":
                        await db.delete_email(email)
                        await db.struct_both(email,interaction.user.id)
                        await interaction.user.add_roles(self.standard_role)
                        await interaction.user.add_roles(self.premium_role)
                        await interaction.followup.send("Registered, added both premium and standard role",ephemeral=True)
                    
                    elif self.info["user_id"] != interaction.user.id:
                        await interaction.followup.send(f"Email ID is already registered to <@{self.info['user_id']}>")

                    else:
                        await interaction.followup.send("Error",ephemeral=True)
            else:
                await interaction.followup.send("Error",ephemeral=True)

        # except Exception as e:
        #     print(f"Unexpected Error: {e}")
        #     await interaction.followup.send("An unexpected error occurred. Try again ", ephemeral=True)

async def setup(bot):
        await bot.add_cog(Verification(bot),guilds = [discord.Object(id=settings.GUILD_ID)])
            
