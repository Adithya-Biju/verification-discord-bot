from discord.ext import commands
import discord 
from discord import app_commands
from utility import embed
class AutoMessages(commands.Cog):

    def __init__(self,bot:commands.Bot):

        self.bot = bot
        self.allowed_roles = [1281699344613117962,
                              1302632538774175797,
                              1198183845036568637,
                              1342104962913533992,
                              1190630311185371267,
                              1299740293892935720,
                              1195788286740922378,
                              1228620751935111240,
                              1417214175670960355]
        
        self.bot.remove_command("help")
    

    @app_commands.command(name="refund",description="Automated response for refund prompt")
    async def refund(self,interaction : discord.Interaction):
        
        await interaction.response.defer(ephemeral=True)  
        
        if not (interaction.permissions.administrator == True or any(role.id in self.allowed_roles for role in interaction.user.roles)):
            await interaction.followup.send("🚫 You don't have permission to use this command.", ephemeral=True)
            return
        self.refund_embed = await embed.refund_embed()
        
        try:
            await interaction.channel.send(embed = self.refund_embed)
            await interaction.followup.send("Successfully sent refund automated message", ephemeral=True)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await interaction.followup.send("An unexpected error occurred. Try again ", ephemeral=True)

    @app_commands.command(name="reinstallnousb",description="Automated response for reinstallnousb prompt")
    async def reinstallnousb(self,interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)  

        if not (interaction.permissions.administrator == True or any(role.id in self.allowed_roles for role in interaction.user.roles)):
            await interaction.followup.send("🚫 You don't have permission to use this command.", ephemeral=True)
            return
        self.reinstallnousb_embed = await embed.reinstallnousb_embed()
        
        try:
            
            await interaction.channel.send(embed = self.reinstallnousb_embed)
            await interaction.followup.send("Successfully sent reinstallnousb automated message", ephemeral=True)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await interaction.followup.send("An unexpected error occurred. Try again ", ephemeral=True)

    @app_commands.command(name="reinstallusb",description="Automated response for reinstallusb prompt")
    async def reinstallusb(self,interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)  

        if not (interaction.permissions.administrator == True or any(role.id in self.allowed_roles for role in interaction.user.roles)):
            await interaction.followup.send("🚫 You don't have permission to use this command.", ephemeral=True)
            return   
        self.reinstallusb_embed = await embed.reinstallusb_embed()
        
        try:
            
            await interaction.channel.send(embed = self.reinstallusb_embed)
            await interaction.followup.send("Successfully sent reinstallusb automated message", ephemeral=True)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await interaction.followup.send("An unexpected error occurred. Try again ", ephemeral=True)
    
    @app_commands.command(name="checktemp",description="Automated response for checktemp prompt")
    async def checktemp(self,interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)  

        if not (interaction.permissions.administrator == True or any(role.id in self.allowed_roles for role in interaction.user.roles)):
            await interaction.followup.send("🚫 You don't have permission to use this command.", ephemeral=True)
            return
        self.checktemp_embed = await embed.checktemp_embed()
        
        try:
            
            await interaction.channel.send(embed = self.checktemp_embed)
            await interaction.followup.send("Successfully sent checktemp automated message", ephemeral=True)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await interaction.followup.send("An unexpected error occurred. Try again ", ephemeral=True)

    @app_commands.command(name="keynotworking",description="Automated response for keynotworking prompt")
    async def keynotworking(self,interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)  

        if not (interaction.permissions.administrator == True or any(role.id in self.allowed_roles for role in interaction.user.roles)):
            await interaction.followup.send("🚫 You don't have permission to use this command.", ephemeral=True)
            return
        self.keynotworking_embed = await embed.keynotworking_embed()
        
        try:
            
            await interaction.channel.send(embed = self.keynotworking_embed)
            await interaction.followup.send("Successfully sent keynotworking automated message", ephemeral=True)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await interaction.followup.send("An unexpected error occurred. Try again ", ephemeral=True)
    
    @app_commands.command(name="rp",description="Automated response for rp prompt")
    async def rp(self,interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)  

        if not (interaction.permissions.administrator == True or any(role.id in self.allowed_roles for role in interaction.user.roles)):
            await interaction.followup.send("🚫 You don't have permission to use this command.", ephemeral=True)
            return
        self.rp_embed = await embed.rp_embed()
        
        try:
            
            await interaction.channel.send(embed = self.rp_embed)
            await interaction.followup.send("Successfully sent rp automated message", ephemeral=True)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await interaction.followup.send("An unexpected error occurred. Try again ", ephemeral=True)
    
    @app_commands.command(name="laptop",description="Automated response for laptop prompt")
    async def laptop(self,interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)  

        if not (interaction.permissions.administrator == True or any(role.id in self.allowed_roles for role in interaction.user.roles)):
            await interaction.followup.send("🚫 You don't have permission to use this command.", ephemeral=True)
            return   
        self.laptop_embed = await embed.laptop_embed()
        
        try:
            
            await interaction.channel.send(embed = self.laptop_embed)
            await interaction.followup.send("Successfully sent laptop automated message", ephemeral=True)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await interaction.followup.send("An unexpected error occurred. Try again ", ephemeral=True)
    
    @app_commands.command(name="hwid",description="Automated response for hwid prompt")
    async def hwid(self,interaction: discord.Interaction,option : int):

        await interaction.response.defer(ephemeral=True)  

        if not (interaction.permissions.administrator == True or any(role.id in self.allowed_roles for role in interaction.user.roles)):
            await interaction.followup.send("🚫 You don't have permission to use this command.", ephemeral=True)
            return
        try:

            if option == 1: 
                self.hwid_embed = await embed.hwid_embed(1)

                
                await interaction.channel.send(embed = self.hwid_embed)
                await interaction.followup.send("Successfully sent hwid 1 automated message", ephemeral=True)
            
            elif option == 2: 
                self.hwid_embed = await embed.hwid_embed(2)
            
                
                await interaction.channel.send(embed = self.hwid_embed)
                await interaction.followup.send("Successfully sent hwid 2 automated message", ephemeral=True)
            
            else:

                await interaction.followup.send("Type 1 or 2",ephemeral=True)


        except Exception as e:
            print(f"Unexpected Error: {e}")

async def setup(bot):
    await bot.add_cog(AutoMessages(bot))