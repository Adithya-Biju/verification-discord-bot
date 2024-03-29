import aiohttp
import settings

try:

    async def premium_key():

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
    
    async def standard_key():
         
         async with aiohttp.ClientSession() as session:      
                async with session.get(settings.STANDARD_KEYS) as s_url:
                    if s_url.status == 200:

                        s_key = await s_url.text()

                        if len(s_key) == 43 and s_key.startswith('STANDARD'):
                             return s_key
                        
                        else:
                             return False
                    
                    else:
                         return False
            

except Exception as e:
     print(e)
                    



