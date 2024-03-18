import discord
from discord.ext import commands

async def new_prem_embed(download,review):
        embed = discord.Embed(
            title="Hello, Thank you for purchasing our product",
            color = 0x0000ff,
            description=f'''You can download it in this channel: <#{download}>

**make sure to write a review after using**. Have an amazing rest of your day! ❤️ <#{review}>'''
)
        return embed

async def old_prem_embed(download,review):
        embed = discord.Embed(
            title="Hello, Thanks for being an amazing customer",
            color = 0x0000ff,
            description=f'''• You can download it in this channel: <#{download}>
• You can find your license key in dms

**make sure to write a review after using**. Have an amazing rest of your day! ❤️ <#{review}>'''
)
        return embed


async def stan_embed(download,review):
        embed = discord.Embed(
            title="Hello, Thank you for purchasing our product",
            color = 0x0000ff,
            description=f'''You can download it in this channel: <#{download}>

**make sure to write a review after using**. Have an amazing rest of your day! ❤️ <#{review}>'''
)
        return embed


async def dms_failed():
        embed = discord.Embed(
            title="Your DMS are turned off so you are unable to receive the license, do the following steps to recieve a license key",
            color = 0x0000ff,
            description=f'''1. Go to your **settings** by tapping on the logo in the bottom right-hand corner. 

2. Tap **Privacy and Safety** 

3. Copy these settings (you can turn it back off after receiving the license)

**After that, verify again and you will recieve the license in your messages**'''
)
        embed.set_image(url=f"https://cdn.discordapp.com/attachments/1198954954480680980/1211297643721003049/image.png?ex=65edafd7&is=65db3ad7&hm=d976c2faf5640a61d68a2c18b4d2e83c912ad525595e7e892f486852489161df&")
        return embed 


async def email_not_found():
        embed = discord.Embed(
            title="EMAIL ADDRESS NOT FOUND",
            color = 0x0000ff,
            description=f'''If you bought the tweaks, do this:

1. Open a ticket by typing /open

2. Put in proof of purchase (IE: receipt)

**Me or my admins will take care of it (note: it may take up to 24 hours)**'''
)
        return embed 


async def faq():
        embed = discord.Embed(
                title = "EXM FAQ DESK",
                color = 0x0000ff,
                description= '''Welcome to EXM's FAQ Desk!
It is a channel for frequently asked questions; you will easily find an answer to common questions regarding Tweaking Utiltiy!

By selecting a question using the below dropdown, you will receive an answer to that question.'''
        )
        return embed

