from utility.payment import new_endpoint
from models import Customer
from utility.update_queue import enqueue

async def new_ver_validation(user_id: int, email: str | None = None):
    # EMAIL TAKEN
    email_check = await Customer.filter(email=email).first()
    if email_check and email_check.user_id != user_id:
        return {
            "status": "email_taken",
            "is_old": False,
            "is_new": False
        }

    # ALREADY VERIFIED
    existing = await Customer.get_or_none(user_id=user_id)
    if existing and existing.email:
        return {
            "status": "already_verified",
            "is_old": existing.has_premium_old,
            "is_new": existing.has_premium_new
        }

    # HIT API
    data = await new_endpoint(email)
    if not data:
        return {
            "status": "none",
            "is_old": False,
            "is_new": False
        }

    # NEW PREMIUM ACTIVE
    if data.get("subscription"):
        await Customer.update_or_create(
            user_id=user_id,
            defaults={
                "has_premium_new": True,
                "email": email
            }
        )

        await enqueue(user_id)

        return {
            "status": "new_premium",
            "is_new": True,
            "is_old": False
        }

    # EMAIL EXISTS BUT NO SUBSCRIPTION
    await Customer.update_or_create(
        user_id=user_id,
        defaults={"email": email}
    )

    await enqueue(user_id)

    return {
        "status": "none",
        "is_old": False,
        "is_new": False
    }
