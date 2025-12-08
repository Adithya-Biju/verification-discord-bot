import aiohttp
import settings


async def premium_key():
    
    try:

        async with aiohttp.ClientSession() as session:      
            async with session.get(settings.PREMIUM_KEY) as t_url:
                if t_url.status == 200:

                    t_key = await t_url.text()

                    if len(t_key) == 42 and t_key.startswith('PREMIUM'):                           
                        return t_key              
                    else:                           
                        return False
                
                else:
                    return False
                
    except Exception as e:
        print(e)
                    
                    



