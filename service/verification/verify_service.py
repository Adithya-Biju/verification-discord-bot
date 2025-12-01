from .customer_validation.old_customer_verify import old_ver_validation
from .customer_validation.new_customer_verify import new_ver_validation

async def validation(bot,interaction, user_id, email = None):
    new_pren_res =  await new_ver_validation(bot,user_id,email)
    old_pren_res =  await old_ver_validation(bot,user_id,email)
    # await interaction.followup.send(embed = new_pren_res,ephemeral=True)
    await interaction.followup.send(embed = old_pren_res,ephemeral=True)
        
