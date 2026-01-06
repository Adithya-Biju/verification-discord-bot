from models import RoleUpdateQueue, Customer

async def enqueue(user_id: int):


    if not await Customer.filter(user_id=user_id).exists():
        return

    already_queued = await RoleUpdateQueue.filter(user_id=user_id).exists()
    if already_queued:
        return

    await RoleUpdateQueue.create(user_id=user_id)
