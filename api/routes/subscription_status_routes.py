from fastapi import APIRouter, Request, HTTPException, Header
from api.service.subscription_status_service import handle_subscription, handle_user_deleted
from settings import WEBHOOK_API_KEY
router = APIRouter()

EXM_WEBHOOK_SECRET = WEBHOOK_API_KEY


#WEBHOOK ENTRY ENDPOINT
@router.post("/webhook/subscription_status")
async def exm_webhook(
    request: Request,
    x_exm_key: str = Header(None),
):
    """EXM → Discord Bot Webhook (2.0 only)."""

    from api.main import _bot

    # Validate secret key
    if x_exm_key != EXM_WEBHOOK_SECRET:
        raise HTTPException(401, "Unauthorized")

    payload = await request.json()
    print("[WEBHOOK RECEIVED]", payload)

    event = payload.get("event")
    email = payload.get("email")

    if not email:
        raise HTTPException(400, "Missing email in webhook")

    # EVENT: subscription-updated
    if event == "subscription-updated":
        subscription_list = payload.get("subscriptions", [])
        print(subscription_list)

        await handle_subscription(_bot, email, subscription_list)
        return {"success": True}

    # EVENT: user-deleted
    if event == "user-deleted":
        await handle_user_deleted(_bot, email)
        return {"success": True}
    

    raise HTTPException(400, "Unknown event")
