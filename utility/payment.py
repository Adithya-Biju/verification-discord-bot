import settings
import aiohttp

try:
   
    async def endpoint(email):
        async with aiohttp.ClientSession() as session:     
                async with session.get(settings.API_BASE+email,auth = aiohttp.BasicAuth(login=settings.API_USSERNAME,password=settings.API_PASSWORD)) as data:
                    response = await data.json() 
                    if response is False:
                        return False
                    else:
                        for i in response:
                            payment = i['order_value'] 
                            
                            if payment == 25 or payment == 27.5:
                                  return {"util":"premium"} 
                            
                            else:
                                  return{"util":"standard"}
                    

except Exception as e:
    print(f"Unexpected Error: {e}")        
