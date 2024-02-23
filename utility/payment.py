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
                       
                        payment = []

                        for i in response:
                            payment.append(i['order_value']) 
                            p=0
                            s=0

                            for i in payment:
                            
                                if i == 25 or i == 27.5:
                                    p+=1
                            
                                else:
                                    s+=1
                                    
                        if p == 1 and s==0:
                            return {"util":"premium"}

                        elif p>=1 and s == 0:
                            return{"util":"premium"}

                        elif p==0 and s >= 1:
                            return{"util":"standard"}

                        elif s == 1 and p == 0:
                            return{"util":"standard"}

                        elif p >= 1 and s >= 1:
                            return{"util":"both"}
                            
                        else:
                            return"False"
                    

except Exception as e:
    print(f"Unexpected Error: {e}")        
