import discord 
from discord.ext import commands
from discord import app_commands
import settings
from utility import key


class Keys(commands.Cog):

    def __init__(self,bot:commands.Bot):

        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
         print("Keys cog loaded")


    @app_commands.command(name = 'standard_key',description='Sends the key to standard in DMS')
    async def standard_key(self, interaction :discord.Interaction, member : discord.Member):

        self.stan_role = 1196567231786664017
        self.stan_role = interaction.guild.get_role(self.stan_role)

        try:

            await interaction.response.defer(ephemeral=True)

            if interaction.permissions.administrator == False:
                await interaction.followup.send("You Do Not Have the Adequate Permissions For This Command",ephemeral=True)
            
            else:
                 
                if self.stan_role in member.roles:

                    self.response = await key.standard_key()

                    if self.response == False:
                        
                        await interaction.followup.send("Key authy is probably down",ephemeral=True)
                    
                    elif self.response != False:

                        try:
                        
                            self.channel = await member.create_dm()
                            await self.channel.send(f'''***Key for standard tweaks :-***
                                                                            
{self.response}''')
                            await interaction.followup.send("Key sent successfull",ephemeral=True)

                        except discord.errors.Forbidden as e:
                            await interaction.followup.send("You're DMS are closed",ephemeral=True)

                    else:
                        
                        await interaction.followup.send("Error",ephemeral=True)
                
                else:

                    await interaction.followup.send("User doesn't have the standard role",ephemeral=True)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await interaction.followup.send("An unexpected error occurred. Try again ", ephemeral=True)



    @app_commands.command(name = 'premium_key',description='Sends the key to premium in DMS')
    async def premium_key(self, interaction :discord.Interaction, member : discord.Member):

        self.prem_role = 1196567144847118346
        self.prem_role = interaction.guild.get_role(self.prem_role)

        try:

            await interaction.response.defer(ephemeral=True)

            if interaction.permissions.administrator == False:
                await interaction.followup.send("You Do Not Have the Adequate Permissions For This Command",ephemeral=True)
            
            else:
                 
                if self.prem_role in member.roles:

                    self.response = await key.premium_key()

                    if self.response == False:
                        
                        await interaction.followup.send("Key authy is probably down",ephemeral=True)
                    
                    elif self.response != False:

                        try:
                            
                            self.channel = await member.create_dm()
                            await self.channel.send(f'''***Key for premium tweaks :-***
                                                                            
{self.response}''')
                            await interaction.followup.send("Key sent successfull",ephemeral=True)

                        except discord.errors.Forbidden as e:
                            await interaction.followup.send("You're DMS are closed",ephemeral=True)

                    else:
                        
                        await interaction.followup.send("Error",ephemeral=True)
                
                else:

                    await interaction.followup.send("User doesn't have the premium role",ephemeral=True)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await interaction.followup.send("An unexpected error occurred. Try again ", ephemeral=True)

async def setup(bot):
        await bot.add_cog(Keys(bot),guilds = [discord.Object(id=settings.GUILD_ID)])
                                                  