from models import Customer
from utility.update_queue import enqueue

#   WEBHOOK HANDLER
async def handle_subscription(email, subscription_list):

    customer = await Customer.get_or_none(email=email)

    if not customer:
        # Webhook for someone who never logged in → ignore
        print(f"[IGNORED] Email not mapped to user: {email}")
        return

    user_id = customer.user_id

    # No active subscriptions
    if not subscription_list or len(subscription_list) == 0:
        print(f"[PREMIUM REMOVED] {email}")

        customer.has_premium_new = False
        await customer.save()

        await enqueue(user_id)
        return


    # Subscription exists (active premium)
    print(f"[PREMIUM ACTIVE] {email}")

    if not customer.has_premium_new:
        customer.has_premium_new = True
        await customer.save()

    await enqueue(user_id)


#   USER DELETED 
async def handle_user_deleted(email):
    """
    When EXM deletes a user account:
        - Remove their email
        - Disable new premium
        - Sync roles
        - Keep the customer record (user_id stays the same)
    """

    customer = await Customer.get_or_none(email=email)
    if not customer:
        print(f"[IGNORED] Delete event for unknown email: {email}")
        return

    user_id = customer.user_id

    print(f"[USER DELETED] Removing email + premium for {email}")

    customer.email = None
    customer.has_premium_new = False
    await customer.save()

    await enqueue(user_id)
