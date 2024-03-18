import settings
import aiohttp
import stripe
import settings

try:
   
    async def endpoint(email):
        async with aiohttp.ClientSession() as session:     
                async with session.get(settings.API_BASE+email,auth = aiohttp.BasicAuth(login=settings.API_USSERNAME,password=settings.API_PASSWORD)) as data:

                    if data.status == 200:

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
                                        
                            if p>=1 and s == 0:
                                return{"util":"premium"}

                            elif p==0 and s >= 1:
                                return{"util":"standard"}

                            elif p >= 1 and s >= 1:
                                return{"util":"both"}
                                
                            else:
                                return False
                        
                    else:
                        
                        stripe.api_key = settings.STRIPE_KEY
                        customers = stripe.Customer.search(query=f"email : '{email}'")
                        a = []
                        p = []
                        prem = 0
                        stan = 0
                        if customers['data'] == '':
                            print("empty")

                        for i in customers:
                            a.append(i['id'])

                        for i in a:
                            pi = stripe.PaymentIntent.search(query=f"customer:'{i}'")
                            
                            for i in pi['data']:
                                p.append(i['amount_received'])

                        if p == []:
                            print("Empty")

                        else:
                            for i in p:
                                if i == 2500 or i == 2750:
                                    prem+=1
                                elif i == 1500 or i == 1750:
                                    stan+=1
                                else:
                                    pass
                            

                        if prem >= 1 and stan == 0:
                            return {"util":"premium"}
                        
                        elif stan >= 1 and stan == 0:
                            return{"util":"standard"}

                        elif prem>=1 and stan>=1:
                            return{"util":"both"}
                        
                        else:
                            return False
        

                    

except Exception as e:
    print(f"Unexpected Error: {e}")        
