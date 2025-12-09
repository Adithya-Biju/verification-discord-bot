from tortoise import fields
from tortoise.models import Model

class TempKey(Model):
    user_id = fields.BigIntField(pk=True)  
    key = fields.CharField(max_length=500)  

    class Meta:
        table = "temp_key"