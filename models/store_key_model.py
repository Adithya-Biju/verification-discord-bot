from tortoise import fields, models
from datetime import datetime

class StoreKey(models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField()  
    key = fields.CharField(max_length=500)
    mod_id = fields.BigIntField(null=True) 
    mod_name = fields.CharField(max_length=255,null=True)
    created_at = fields.DatetimeField(default=datetime.utcnow)

    class Meta:
        table = "store_keys"
