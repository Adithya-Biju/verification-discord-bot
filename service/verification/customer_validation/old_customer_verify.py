from utility.payment import old_endpoint
from models import CustomerOld, Customer
from utility.server_roles import role_updates
from utility.embed import email_not_found, new_prem_embed, old_prem_embed
import discord 


async def old_ver_validation(bot, user_id, email = None):

    email_check = await CustomerOld.filter(email=email).first()

    #If email exists and is linked to someone else other than the user who used it 
    if email_check and email_check.user_id != user_id: 
        return discord.Embed(
            title="EMAIL ADDRESS ALREADY REGISTERED",
            color = 0x0000ff)
        
    #If user_id already exists in the db so that they dont get another gmail linked
    if await CustomerOld.get_or_none(user_id=user_id): 
        return await old_prem_embed()

    #If email doesnt exists in the db we hit the endpoint
    if await old_endpoint(email):

        await Customer.update_or_create(
        user_id=user_id,
        defaults={
            "has_premium_old": True
        }) 

        await CustomerOld.update_or_create(
        user_id=user_id,
        defaults={
            "email": email
        }) 
        
        await role_updates(bot, user_id)
        return await new_prem_embed()
    
    else:
        return await email_not_found()
        
