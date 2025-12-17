from .customer_validation.old_customer_verify import old_ver_validation
from .customer_validation.new_customer_verify import new_ver_validation

async def validation(user_id, email=None):

    new_res = await new_ver_validation(user_id, email)
    old_res = await old_ver_validation(user_id, email)
    
    # Both say email taken
    if new_res["status"] == "email_taken" and old_res["status"] == "email_taken":
        return {
            "status": "email_taken"
        }

    # Both say email already entered or existing 
    if new_res["status"] == "already_verified" and old_res["status"] == "already_verified":
        return {
            "status": "already_verified"
        }
    

    # Both verified (1.3 + 2.0)
    if new_res["is_new"] and old_res["is_old"]:
        return {
            "status": "both_verified",
            "log": {
                "type": "Verified to both",
                "user_id": user_id,
                "email": email
            }
        }

    # Only NEW
    if new_res["status"] == "new_premium":
        return {
            "status": "new_only",
            "log": {
                "type": "New Premium",
                "user_id": user_id,
                "email": email
            }
        }

    # Only OLD
    if old_res["status"] == "old_premium":
        return {
            "status": "old_only",
            "log": {
                "type": "Old Premium",
                "user_id": user_id,
                "email": email
            }
        }

    # Nothing matched
    return {
        "status": "not_found"
    }
