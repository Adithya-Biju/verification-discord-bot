from tortoise import fields
from tortoise.models import Model
from datetime import datetime 

class Customer(Model):
    user_id = fields.BigIntField(pk=True)
    has_premium_old = fields.BooleanField(default=False)
    has_premium_new = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(default=datetime.utcnow)
    email = fields.CharField(max_length=255, unique=True, null=True)

    class Meta:
        table = "customer"