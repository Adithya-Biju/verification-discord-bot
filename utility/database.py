from tortoise.transactions import in_transaction
from models import Customer, CustomerOld
from tortoise.exceptions import IntegrityError

async def insert_old_premium(user_id: int, email: str):
    """
    Inserts OLD premium correctly following strict rules.

    Returns:
        {
            "status": str,
            "linked_user_id": int | None
        }

    Status : email_linked_to_other = Already exisits in the DB to some other ID
             already_in_old = Exists in the old DB so just update roles 
             old_created_existing_customer = created data in old customer db 
             created_customer_and_old = created data in both old and new customer 
    """

    async with in_transaction():

        # Email exists but linked to another user
        email_owner = await CustomerOld.get_or_none(email=email)

        if email_owner and email_owner.user_id != user_id:
            return {
                "status": "email_linked_to_other",
                "linked_user_id": email_owner.user_id
            }
        

        # User exists in customer_old
        customer_old = await CustomerOld.get_or_none(user_id=user_id)

        if customer_old:
            customer = await Customer.get(user_id=user_id)

            if not customer.has_premium_old:
                customer.has_premium_old = True
                await customer.save(update_fields=["has_premium_old"])

            return {
                "status": "already_in_old",
                "linked_user_id": None
            }
        

        # User exists in customer but not in customer_old
        customer = await Customer.get_or_none(user_id=user_id)

        if customer:
            if not customer.has_premium_old:
                customer.has_premium_old = True
                await customer.save(update_fields=["has_premium_old"])

            await CustomerOld.create(
                user_id=user_id,
                email=email
            )

            return {
                "status": "old_created_existing_customer",
                "linked_user_id": None
            }


        # User exists nowhere
        await Customer.create(
            user_id=user_id,
            has_premium_old=True
        )

        await CustomerOld.create(
            user_id=user_id,
            email=email
        )

        return {
            "status": "created_customer_and_old",
            "linked_user_id": None
        }



async def update_premium(old_data: dict, updated_data: dict):
    old_id = old_data["user_id"]
    new_id = updated_data["user_id"]

    try:
        async with in_transaction():

            customer_obj = await Customer.get(user_id=old_id)
            old_record_obj = await CustomerOld.get_or_none(user_id=old_id)

            if old_id != new_id:
                if await Customer.exists(user_id=new_id):
                    return {"success": False, "error": f"ID {new_id} is already in use."}

                await customer_obj.delete()

                await Customer.create(
                    user_id=new_id,
                    email=updated_data.get("new_email") or customer_obj.email,
                    has_premium_new=updated_data.get("has_premium_new", customer_obj.has_premium_new),
                    has_premium_old=updated_data.get("has_premium_old", customer_obj.has_premium_old),
                    created_at=customer_obj.created_at 
                )

                if updated_data.get("old_email") or old_record_obj:
                    original_old_ts = old_record_obj.created_at if old_record_obj else customer_obj.created_at
                    
                    await CustomerOld.create(
                        user_id=new_id,
                        email=updated_data.get("old_email") or (old_record_obj.email if old_record_obj else None),
                        created_at=original_old_ts 
                    )
            
            else:
                customer_updates = {}
                if updated_data.get("new_email"):
                    customer_updates["email"] = updated_data["new_email"]
                if updated_data.get("has_premium_new") is not None:
                    customer_updates["has_premium_new"] = updated_data["has_premium_new"]
                if updated_data.get("has_premium_old") is not None:
                    customer_updates["has_premium_old"] = updated_data["has_premium_old"]

                if customer_updates:
                    await Customer.filter(user_id=old_id).update(**customer_updates)

                if updated_data.get("old_email") is not None:
                    exists = await CustomerOld.filter(user_id=old_id).exists()
                    if exists:
                        await CustomerOld.filter(user_id=old_id).update(email=updated_data["old_email"])

            return {"success": True}
        
    except IntegrityError:
        return {"success": False, "error": "Email conflict: That email belongs to another user."}

    # except Exception as e:
    #     print(e)
    #     return {"success": False, "error": f"Unexpected error occured"}


