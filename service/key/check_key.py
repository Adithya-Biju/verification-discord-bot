from models import StoreKey

async def find_the_key(user_id: int):

    key_records = await StoreKey.filter(user_id=user_id).all()

    if key_records:
        return "\n".join(f"Key: **{record.key}**" for record in key_records)

    return "Not Found"
