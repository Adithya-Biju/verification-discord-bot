import motor.motor_asyncio 
import asyncio
import settings

try:
    cluseter = motor.motor_asyncio.AsyncIOMotorClient([settings.MONGO_DB])
    dbs = cluseter["exm"]
    verification = dbs["verification"]
    keys = dbs['keys']

    async def struct_premium(email,user):
        await verification.insert_one({
            "email":email,
            "user_id":user,
            "util":"premium"
            })
        
    async def struct_standard(email,user):
        await verification.insert_one({
            "email":email,
            "user_id":user,
            "util":"standard"
            })
    
    async def struct_keys(email,user):
        await verification.insert_one({
            "email":email,
            "user_id":user,
            "dm":0
        })

    async def find_email_main(email):
        return await verification.find_one({'email':email})
    
    async def find_user(user):
        return await verification.find_one({"user_id":user})
    
    async def find_dm(email):
        return await keys.find_one({"email":email})
    
    async def update_verification(email,user):
        await verification.update_one({
            "email":email
        },{
            "$set":{
                "user_id":user
            }
        })
        
    async def update_keys(email,user):

        await keys.update_one({
            "email":email
        },{
            "$set":{
                "user_id":user
            }
        })

    async def dm_key_successfull(email):    
        await keys.update_one({
            "email":email
        },{
            "$set":{
                "dm":1
            }
        })

    async def UpdateEmail(email_before,email_after):
        await verification.update_one({
            "email":email_before
        },{
            "$set":{
                "email":email_after
            }
        })
    
    async def UpdateUser(user_before,user_after):
        await verification.update_one({
            "user_id":user_before
        },{
            "$set":{
                "user_id":user_after
            }
        })

    async def delete_user(user):
        await verification.delete_one({"user_id":user})
    
    async def delete_email(email):
        await verification.delete_one({"email":email})

except Exception as e:
    print(f"Error connecting to MongoDB: {e}")