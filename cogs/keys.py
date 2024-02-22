import discord 
from discord.ext import commands
from discord import app_commands
import asyncio
import aiohttp
import settings


class Keys(commands.Cog):

    def __init__(self,bot:commands.Bot):

        self.bot = bot
        self.log_channel = self.bot.get_channel(1198137815121272944)

    @commands.Cog.listener()
    async def on_ready(self):
         print("Keys cog loaded")


    @app_commands.command(name = 'standard_key',description='Sends the key for standard utility to user in DMS')
    async def standard_key(self, interaction :discord.Interaction, member : discord.Member):

        try:
            await interaction.response.defer(ephemeral=True)

            async with aiohttp.ClientSession() as session:      
                async with session.get(settings.STANDARD_KEYS) as s_url:
                    if s_url.status == 200:

                        if interaction.permissions.administrator == False:
                            await interaction.followup.send("You Do Not Have the Adequate Permissions For This Command",ephemeral=True)
                        
                        else:
                                    self.s_key = await s_url.text()
                                    
                                    if len(self.s_key) == 43 and self.s_key.startswith('STANDARD'):
                                        self.channel = await member.create_dm()
                                        await self.channel.send(f'''***Key for standard tweaks :-***
                                                                        
{self.s_key}''')
                                        if interaction.response.is_done():
                                            await interaction.followup.send("The key has been successfully sent to the user", ephemeral=True)
                                            await asyncio.sleep(5)
                                            await self.log_channel.send(f"{member.mention} received the Standard key")
                        
                    else:
                        await interaction.followup.send("Authy Key Generator is probably down, please be patient")
                                                   
        except discord.errors.NotFound as e:
            print(f"Interaction not found: {e}")
        
        except discord.errors.Forbidden as e:
            print(f"Error: {e}")
            await interaction.followup.send("Cannot send messages to this user. DMs are closedS.", ephemeral=True)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await interaction.followup.send("An unexpected error occurred. Try again ", ephemeral=True)



    @app_commands.command(name = 'tester_key',description='Sends the key to testers in DMS')
    async def tester_key(self, interaction :discord.Interaction, member : discord.Member):

        self.tester_role = 1198162651520438272
        self.flag = 0

        try:

            await interaction.response.defer(ephemeral=True)

            if interaction.permissions.administrator == False:
                await interaction.followup.send("You Do Not Have the Adequate Permissions For This Command",ephemeral=True)
            
            else:
                 if type(self.tester_role) is not discord.role:
                    self.tester_role = interaction.guild.get_role(self.tester_role)
                
                    for i in member.roles:
                        if self.tester_role == i:
                            self.flag+=1
                        
                    if self.flag == 1:
                        async with aiohttp.ClientSession() as session:      
                            async with session.get(settings.TESTER_KEYS) as t_url:
                                if t_url.status == 200:

                                    self.t_key = await t_url.text()

                                    if len(self.t_key) == 41 and self.t_key.startswith('TESTER'):

                                        self.channel = await member.create_dm()
                                        await self.channel.send(f'''***Key for Tester :-***
                                                                        
{self.t_key}''')
                                        if interaction.response.is_done():
                                            await interaction.followup.send("The key has been successfully sent to the user", ephemeral=True)
                                            await asyncio.sleep(4)
                                            await self.log_channel.send(f"{member.mention} received the Tester key")
                                    
                                else:
                                    await interaction.followup.send("Authy Key Generator is probably down, please wait")
                                                    
                    elif self.flag == 0:
                        await interaction.followup.send("The user doesn't have the Tester discord role",ephemeral=True)
                        
                    else:
                        await interaction.followup.send("Error occured",ephemeral=True)

        except discord.errors.NotFound as e:
            print(f"Interaction not found: {e}")

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await interaction.followup.send("An unexpected error occurred. Try again ", ephemeral=True)

async def setup(bot):
        await bot.add_cog(Keys(bot),guilds = [discord.Object(id=1198137813800079480)])
                                                  