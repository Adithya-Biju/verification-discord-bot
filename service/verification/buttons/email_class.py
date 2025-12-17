import discord
from ..verify_service import validation 
from utility import constants
from utility import embed as emb

class EmailModal(discord.ui.Modal, title="EXM Premium Verification"):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

        self.email = discord.ui.TextInput(
            label="Enter your EXM account email",
            placeholder="you@example.com",
            required=True,
            style=discord.TextStyle.short,
            max_length=255,
        )
        self.add_item(self.email)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            response = await validation(
                interaction.user.id,
                self.email.value
            )
            status = response["status"]

            if status == "email_taken":
                embed = await emb.email_taken_embed()

            if status == "already_verified":
                embed = await emb.existing_embed()

            elif status == "both_verified":
                embed = await emb.both_prem_embed()

            elif status == "new_only":
                embed = await emb.new_prem_embed()

            elif status == "old_only":
                embed = await emb.old_prem_embed()

            else:
                embed = await emb.email_not_found()

            await interaction.followup.send(embed=embed, ephemeral=True)

            log = response.get("log")
            if log:
                log_guild = self.bot.get_guild(constants.LOG_SERVER)
                if log_guild:
                    log_channel = log_guild.get_channel(constants.VERIFY_LOG)
                    if log_channel:
                        await log_channel.send(
                            f"📝 **Verification Event**\n"
                            f"Type: `{log['type']}`\n"
                            f"User: <@{log['user_id']}>\n"
                            f"Email: `{log['email']}`"
                        )
            
        except Exception as e:
            
            try:
                await interaction.followup.send(
                    "Something went wrong while verifying your email.\n"
                    "Please try again in a minute or open a support ticket.",
                    ephemeral=True
                )
            except:
                pass
            raise
