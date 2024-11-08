from models import TempKey

async def find_the_key(user_id : str):
    
    user_exists = await TempKey.filter(user_id = user_id).all()
    
    if user_exists:
        return user_exists
    
    else:
        return None