from models import TempKey

async def find_the_key(user_id: int):

    partial_user_id = str(user_id // 100)

    key_records = await TempKey.filter(user_id__startswith=partial_user_id).all()

    if key_records:
        keys_message = "\n".join(f"Key: **{record.key}**" for record in key_records)
        return keys_message
    else:
        return "To find your key, check <#1211411223090823290>"