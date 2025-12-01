from utility.payment import new_endpoint
from models import Customer
from utility.server_roles import role_updates
from utility.embed import email_not_found, new_prem_embed, old_prem_embed
import discord 


async def new_ver_validation(bot, user_id, email = None):

    email_check = await Customer.filter(email=email).first()

    #If email exists and is linked to someone else other than the user who used it 
    if email_check and email_check.user_id != user_id: 
        return discord.Embed(
            title="EMAIL ADDRESS ALREADY REGISTERED",
            color = 0x0000ff)
        
    #If email is already linked to the user
    if await Customer.get_or_none(user_id=user_id): 
        return await old_prem_embed()

    #If email doesnt exists in the db we hit the endpoint
    data = await new_endpoint(email)

    if data:

        if len(data["subscriptions"]) > 0  :

            await Customer.update_or_create(
            user_id=user_id,
            defaults={
                "has_premium_new": True,
                "email": email
            }) 
            
            await role_updates(bot, user_id)
            return await new_prem_embed()
        
        else:

            await Customer.update_or_create(
            user_id=user_id,
            defaults={
                "email": email
            }) 
            
            await role_updates(bot, user_id)
            return await email_not_found()
    
    else:
        return await email_not_found()
        
