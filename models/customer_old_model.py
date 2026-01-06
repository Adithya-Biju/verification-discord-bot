from tortoise import fields, models
from datetime import datetime 

class CustomerOld(models.Model):
    user = fields.ForeignKeyField(
        "models.Customer",
        on_delete=fields.CASCADE,
        pk=True
    )
    email = fields.CharField(max_length=255, unique=True)
    created_at = fields.DatetimeField(default=datetime.utcnow)

    class Meta:
        table = "customer_old"
