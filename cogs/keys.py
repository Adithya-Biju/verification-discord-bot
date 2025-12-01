import discord 
from discord.ext import commands
from discord import app_commands
import settings
import asyncio
from utility import key,constants
from service import find_the_key

class Keys(commands.Cog):

    def __init__(self,bot:commands.Bot):

        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
         print("Keys cog loaded")


    @app_commands.command(name = 'premium_key',description='Sends the key to premium in DMS')
    async def premium_key(self, interaction :discord.Interaction, member : discord.Member):
        
        try:

            await interaction.response.defer(ephemeral=True)

            self.prem_role = interaction.guild.get_role(constants.PREMIUM_ID)
            self.log = interaction.guild.get_channel(constants.LOGGING_ID)

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
                            await self.channel.send(f'''**Hello, here is your LICENSE KEY for EXM PREMIUM TWEAKS:**

{self.response}

note: you can only use this on one pc (HWID) 
''')
                            await interaction.followup.send("Key sent successfull",ephemeral=True)
                            await asyncio.sleep(3)
                            await self.log.send(f'''{member.mention} recieved a Premium key
                                                
{self.response}

Operation performed by {interaction.user.mention}''')

                        except discord.errors.Forbidden as e:
                            await interaction.followup.send("DMS are closed",ephemeral=True)

                    else:
                        
                        await interaction.followup.send("Error",ephemeral=True)
                
                else:

                    await interaction.followup.send("User doesn't have the premium role",ephemeral=True)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await interaction.followup.send("An unexpected error occurred. Try again ", ephemeral=True)

    @app_commands.command(name = 'missing_key',description='Check the users keys')
    async def missing_key(self, interaction :discord.Interaction, member : discord.Member = None):

        try:
            await interaction.response.defer(ephemeral=True)

            if member is None:

                key_record = await find_the_key(interaction.user.id)
                
                await interaction.followup.send(key_record)
            
            elif member.id == interaction.user.id:

                key_record = await find_the_key(member.id)
                
                await interaction.followup.send(key_record)

            elif member.id != interaction.user.id:

                if interaction.permissions.administrator == False:
                    await interaction.followup.send("You Do Not Have the Adequate Permissions For This Command",ephemeral=True)
                
                else:
                    key_record = await find_the_key(member.id)
                    
                    await interaction.followup.send(key_record)
            
            else:

                await interaction.followup.send("Missing key command missing condition")

        except:
            await interaction.followup.send("Missing key command crashed ", ephemeral=True)


async def setup(bot):
        await bot.add_cog(Keys(bot),guilds = [discord.Object(id=settings.GUILD_ID)])
                                                  