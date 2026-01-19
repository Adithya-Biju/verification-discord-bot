import discord 
from discord.ext import commands
from discord import app_commands
from service import CustomerUpdates
from typing import Optional

class Admin(commands.Cog):

    def __init__(self,bot:commands.Bot):

        self.bot = bot
        self.bot.remove_command("help")

    @app_commands.command(name='insert', description='Insert Old premium member')
    async def insert_customer_old(self, interaction: discord.Interaction, member: discord.Member, email: str):

        await interaction.response.defer(ephemeral=True)

        if interaction.permissions.administrator == False:
                await interaction.followup.send("You don't have the permissions to user this command",ephemeral=True)
                return
        
        try:
        
            insert = CustomerUpdates(self.bot)
            await insert.insert_data_old_customer(interaction,member,email)

        except Exception as e:
            print(e)
            await interaction.followup.send("Unexpected error occured",ephemeral=True) 

    @app_commands.command(name='update', description='Update premium member')
    async def update_customer(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)

        if interaction.permissions.administrator == False:
                await interaction.followup.send("You don't have the permissions to user this command",ephemeral=True)
                return
        
        try:
        
            update = CustomerUpdates(self.bot)
            await update.update_data_customer(interaction)

        except Exception as e:
            print(e)
            await interaction.followup.send("Unexpected error occured",ephemeral=True) 
        
    @app_commands.command(name='view', description='View premium member data')
    async def view_customer(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)

        if interaction.permissions.administrator == False:
                await interaction.followup.send("You don't have the permissions to user this command",ephemeral=True)
                return
        
        try:
        
            view = CustomerUpdates(self.bot)
            await view.view_data_customer(interaction)

        except Exception as e:
            print(e)
            await interaction.followup.send("Unexpected error occured",ephemeral=True) 
        
    
    @app_commands.command(name='delete', description='Insert Old premium member')
    async def delete_customer_old(self, interaction: discord.Interaction, member: discord.Member):

        await interaction.response.defer(ephemeral=True)

        if interaction.permissions.administrator == False:
                await interaction.followup.send("You don't have the permissions to user this command",ephemeral=True)
                return
        
        try:
        
            delete = CustomerUpdates(self.bot)
            await delete.delete_data_customer(interaction,member)

        except Exception as e:
            print(e)
            await interaction.followup.send("Unexpected error occured",ephemeral=True) 


async def setup(bot):
        await bot.add_cog(Admin(bot))
                                                  