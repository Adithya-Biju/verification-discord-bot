from utility.payment import old_endpoint
from models import CustomerOld, Customer
from utility.update_queue import enqueue


async def old_ver_validation(user_id: int, email: str | None = None):
    # EMAIL TAKEN BY OTHER USER
    email_check = await CustomerOld.filter(email=email).first()
    if email_check and email_check.user_id != user_id:
        return {
            "status": "email_taken",
            "is_old": False,
            "is_new": False
        }

    # ALREADY VERIFIED (OLD)
    existing_old = await CustomerOld.get_or_none(user_id=user_id)
    if existing_old:
        return {
            "status": "already_verified",
            "is_old": True,
            "is_new": False
        }

    # HIT OLD ENDPOINT
    is_old_premium = await old_endpoint(email)

    if is_old_premium:
        await Customer.update_or_create(
            user_id=user_id,
            defaults={"has_premium_old": True}
        )

        await CustomerOld.update_or_create(
            user_id=user_id,
            defaults={"email": email}
        )

        await enqueue(user_id)

        return {
            "status": "old_premium",
            "is_old": True,
            "is_new": False
        }

    # NOT FOUND
    return {
        "status": "none",
        "is_old": False,
        "is_new": False
    }
