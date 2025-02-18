from discord.ext import commands
import discord 
import settings
from utility import embed

class AutoMessages(commands.Cog):

    def __init__(self,bot:commands.Bot):

        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
         print("Auto messages cog loaded")
    

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def refund(self,ctx):

        self.refund_embed = await embed.refund_embed()
         
        try:
            await ctx.message.delete()
            await ctx.send(embed = self.refund_embed)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await ctx.send("An unexpected error occurred. Try again ", ephemeral=True)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reinstallnousb(self,ctx):

        self.reinstallnousb_embed = await embed.reinstallnousb_embed()
         
        try:
            await ctx.message.delete()
            await ctx.send(embed = self.reinstallnousb_embed)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await ctx.send("An unexpected error occurred. Try again ", ephemeral=True)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reinstallusb(self,ctx):

        self.reinstallusb_embed = await embed.reinstallusb_embed()
         
        try:
            await ctx.message.delete()
            await ctx.send(embed = self.reinstallusb_embed)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await ctx.send("An unexpected error occurred. Try again ", ephemeral=True)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def checktemp(self,ctx):

        self.checktemp_embed = await embed.checktemp_embed()
         
        try:
            await ctx.message.delete()
            await ctx.send(embed = self.checktemp_embed)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await ctx.send("An unexpected error occurred. Try again ", ephemeral=True)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def keynotworking(self,ctx):

        self.keynotworking_embed = await embed.keynotworking_embed()
         
        try:
            await ctx.message.delete()
            await ctx.send(embed = self.keynotworking_embed)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await ctx.send("An unexpected error occurred. Try again ", ephemeral=True)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rp(self,ctx):

        self.rp_embed = await embed.rp_embed()
         
        try:
            await ctx.message.delete()
            await ctx.send(embed = self.rp_embed)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await ctx.send("An unexpected error occurred. Try again ", ephemeral=True)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def laptop(self,ctx):

        self.laptop_embed = await embed.laptop_embed()
         
        try:
            await ctx.message.delete()
            await ctx.send(embed = self.laptop_embed)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await ctx.send("An unexpected error occurred. Try again ", ephemeral=True)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def hwid(self,ctx,option : int):

        try:

            if option == 1: 
                self.hwid_embed = await embed.hwid_embed(1)

                await ctx.message.delete()
                await ctx.send(embed = self.hwid_embed)
            
            elif option == 2: 
                self.hwid_embed = await embed.hwid_embed(2)
            
                await ctx.message.delete()
                await ctx.send(embed = self.hwid_embed)
            
            else:

                await ctx.send("Invalid")

        except Exception as e:
            print(f"Unexpected Error: {e}")
            await ctx.send("An unexpected error occurred. Try again ", ephemeral=True)

async def setup(bot):
        await bot.add_cog(AutoMessages(bot),guilds = [discord.Object(id=settings.GUILD_ID)])
            