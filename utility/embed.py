import discord
from discord.ext import commands

async def old_prem_embed():
        embed = discord.Embed(
            title="Hello, you have been verified as a premium customer (legacy) and granted access to priority support & other benefits",
            color = 0x0000ff,
            description=f'''Have an amazing rest of your day! ❤️'''
)
        return embed

async def new_prem_embed():
        embed = discord.Embed(
            title="Hello, you have been verified as a premium customer and granted access to priority support & other benefits. After your subscribtion ends you will lose access",
            color = 0x0000ff,
            description=f'''Have an amazing rest of your day! ❤️'''
)
        return embed


async def existing_embed():
        embed = discord.Embed(
            title="Hello, you already are verified in the discord server",
            color = 0x0000ff,
            description=f'''If you think there is an error, please open a ticket in https://discord.com/channels/1196563515926909008/1303435489302286397'''
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
            title="Your email address was not found",
            color = 0x0000ff,
            description=f'''
If you bought premium,  Open a verification ticket https://discord.com/channels/1196563515926909008/1303435489302286397 and give us proof of purchase '''
)
        return embed 


async def ticket():
        embed = discord.Embed(
                title = "EXM TICKET DESK",
                color = 0x0000ff,
                description= '''Welcome to EXM's ticket Desk!
It is a channel to create ticket;

By selecting a question using the below dropdown, you will open ticket.'''
        )
        return embed


async def refund_embed():
        embed = discord.Embed(
                title = "Refund",
                color = 0x0000ff,
                description= '''In order to get a refund, you will have to send a minute-long screen recording of the game of your choice with your FPS displayed and ``alt + tab`` to show your Task Manager right now with the tweaks applied. Additionally, you will have to do a `CapFrameX` benchmark and provide us with the results. Then, use the system restore point you created before applying the tweaks to revert to the state your PC was at before the tweaks were applied. Do the same minute-long screen recording with your FPS displayed and ``alt + tab`` to show your Task Manager as well. Again, do a `CapFrameX` benchmark and provide us with the results. Due to the nature of the product, we require proof of any issues occuring since the refund policy can be very easily abused.

How to benchmark with `CapFrameX`: https://youtu.be/W7yINXWty90
'''
        )
        return embed


async def reinstallnousb_embed():
        embed = discord.Embed(
                title = "Reinstall No USB",
                color = 0x0000ff,
                description= '''https://www.youtube.com/watch?v=A3Ig7utyaPo'''
        )
        return embed


async def reinstallusb_embed():
        embed = discord.Embed(
                title = "Reinstall USB",
                color = 0x0000ff,
                description= '''https://www.youtube.com/watch?v=6K_Fw16vVqc'''
        )
        return embed
        

async def reinstallusb_embed():
        embed = discord.Embed(
                title = "Reinstall USB",
                color = 0x0000ff,
                description= '''https://www.youtube.com/watch?v=6K_Fw16vVqc'''
        )
        return embed


async def hwid_embed(option : int):
        if option == 1:
                embed = discord.Embed(
                        color = 0x0000ff,
                        description= '''please do this:

1. Open the Start menu, type in 'cmd', and hit Enter.
2. In the command prompt window, paste the following command: 'wmic baseboard get serialnumber' and press Enter.
3. Copy the number that popped up and send it here plus take screenshot of it.
''')
        
        else:
               embed = discord.Embed(
                        color = 0x0000ff,
                        description= '''please do this:

1. Open the Start menu by pressing the windows key on your keyboard, type in 'powershell' and find "Powershell" and click "Run as administrator".
2. Paste the following command into the powershell window that popped up: Get-WmiObject Win32_BaseBoard | Select-Object -ExpandProperty SerialNumber
3. Copy the number that popped up and send it here plus take screenshot of it.
4. If the previous command doesn't work, please use: Get-CimInstance Win32_BaseBoard | Select-Object -ExpandProperty SerialNumber
''')
                
        return embed


async def checktemp_embed():
        embed = discord.Embed(
                color = 0x0000ff,
                description= '''Download hwinfo64, install it, open the app and tick the "sensors-only" option here and click start. Then scroll down till you see CPU and GPU temperature and make screenshot of the app as shown on the picture.'''
        )
        embed.set_image(url=f"https://cdn.discordapp.com/attachments/1341271867310477343/1343159891384209459/hwinfo.png?ex=67bc42a0&is=67baf120&hm=a3461375c48f777492c422a65ecb977c311315ff31c539ed7d9d2baa971e33dc&")
        return embed


async def keynotworking_embed():
        embed = discord.Embed(
                color = 0x0000ff,
                description= '''Keys don’t randomly stop working. They typically stop working if you've switched or spoofed a PC component (such as the motherboard) or if you've switched to a different PC than the one where the key was initially activated. Or, if you haven’t used your key in a long time; you might have bought before the key reset. Please provide proof of your receipt and your receipt on the site.'''
        )
        return embed


async def rp_embed():
        embed = discord.Embed(
                color = 0x0000ff,
                description= '''To use an restore point follow the guide below:

1. Press win + r 
2. Type "rstrui.exe" and hit enter
3. Select the restore point you want to use and click next
'''
        )
        return embed


async def laptop_embed():
        embed = discord.Embed(
                color = 0x0000ff,
                description= '''Just hover over each button to get a little description of what each tweak does. I'd recommend only applying the ones that appeal to YOU. If your system has poor cooling, I'd suggest NOT applying the CPU, GPU, and power tweaks. Also, be aware that the BIOS tweaks can cause issues for some people. Additionally, you should stay away from the red buttons unless you are ABSOLUTELY sure you want to apply those tweaks. If you don't trust yourself with applying the tweaks, you can open a ticket and an available staff member can connect to your PC via AnyDesk and apply them for you. Some do it for ~$5, while others do it for free.'''
        )
        return embed