import discord

def check_permissions(func):

    async def check_role(*args):

        print(*args)  
        return await func(*args)

    return check_role   