import settings
import aiohttp
import settings

   
async def old_endpoint(email):
    try:
        async with aiohttp.ClientSession() as session:     
            async with session.get(settings.API_BASE+"/orders/"+email,auth = aiohttp.BasicAuth(login=settings.API_USSERNAME,password=settings.API_PASSWORD)) as data:
                if data.status == 200:
                    response = await data.json() 
                    if response:
                        return True
                    else:
                        return False  
                return False    

    except Exception as e:
        print(f"Error Hitting the old premium API: {e}")        


async def new_endpoint(email):

    url = f"{settings.API_BASE}/subscription/status?email={email}"

    headers = {
            "X-API-Key": settings.X_API_KEY
    }
    try:
         
        async with aiohttp.ClientSession() as session:     
                async with session.get(url, headers=headers) as data:

                    if data.status == 200:
                        response = await data.json()
                        if response:
                            return response
                        else:
                            return False  
                        
                    return False
                        
    except Exception as e:
        print(f"Error Hitting the New premium API: {e}")            
    