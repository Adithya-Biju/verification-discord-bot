from models import RoleUpdateQueue, Customer

async def enqueue(user_id: int):

    customer = await Customer.get_or_none(user_id=user_id)
    role_update = await RoleUpdateQueue.get_or_none(user_id=user_id)
    
    if not customer:
        return
    
    if role_update:
        return
    
    await RoleUpdateQueue.create(user_id=user_id)