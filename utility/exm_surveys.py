import settings
import aiohttp
import settings

   
async def survey_repsonse(email):
    try:
        headers = {
            "X-API_KEY": settings.X_API_KEY, 
            "Accept": "application/json"
        }
        async with aiohttp.ClientSession() as session:     
            url = f"{settings.API_BASE}/services/lookup?email={email}"
            
            async with session.get(url, headers=headers) as data:
                
                if data.status == 200:
                    response = await data.json() 
                    if response and response.get("success"):
                        return response
                else:
                    print(f"API Failed with status {data.status}. Response text: {await data.text()}")
                
                return None 

    except Exception as e:
        print(f"Error Hitting the old premium API: {e}")        
