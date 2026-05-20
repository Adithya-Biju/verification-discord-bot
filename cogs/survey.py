import discord
from discord.ext import commands
from discord import app_commands
from utility.exm_surveys import survey_repsonse

class Survey(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @app_commands.command(name="survey",description="data filled out in the survey + the service name")
    @app_commands.describe(email="Please enter email address")
    @app_commands.guilds(discord.Object(id=1417214175670960349))
    async def survey(self, interaction: discord.Interaction, email: str):
         
        await interaction.response.defer(ephemeral=True)

        if interaction.permissions.administrator == False:
                await interaction.followup.send("You don't have the permissions to user this command",ephemeral=True)
                return
        
        try:

            api_data = await survey_repsonse(email)
            
            if not api_data or not api_data.get("orders"):
                await interaction.followup.send(f"❌ No active survey or order data found for `{email}`.", ephemeral=True)
                return
            
            first_order = api_data["orders"][0]
            product_name = first_order["product"]["name"]
            order_number = first_order.get("order_number", "N/A")
            status = first_order["service_status_label"]
            survey_questions = first_order.get("survey", [])
                 
            embed = discord.Embed(
                title=f"📋 Survey Results: {product_name}",
                description=f"Showing the layout configuration for customer lookup.",
                color=0x0000ff
            )

            embed.add_field(name="Order #", value=f"{order_number}", inline=True)
            embed.add_field(name="Status", value=f"🟢 {status}" if status == "Pending" else f"🔵 {status}", inline=True)
            embed.add_field(name="User ID", value=f"`{api_data.get('user_id')}`", inline=True)
            
            embed.add_field(name="Customer Email", value=email, inline=False)
            
            # Visual divider line
            embed.add_field(name="─" * 35, value="**Survey Responses**", inline=False)

            # 5. Populate questions and answers using clean programming code blocks
            if survey_questions:
                for item in survey_questions:
                    question = item["question"]
                    answer = item["answer"]
                
                    # Presenting the data inside a clean gray background box
                    embed.add_field(
                        name=f"❓ {question}", 
                        value=f"```yaml\n{answer}\n```", 
                        inline=False
                    )
            else:
                embed.add_field(name="Survey Data", value="⚠️ This order item didn't require any custom fields.", inline=False)

            await interaction.followup.send(embed=embed, ephemeral=True)

        
        except Exception as e:
            print(e)
            await interaction.followup.send("Unexpected error occured",ephemeral=True) 


async def setup(bot):
    await bot.add_cog(Survey(bot))