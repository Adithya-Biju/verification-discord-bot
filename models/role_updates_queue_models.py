from tortoise import fields
from tortoise.models import Model

class RoleUpdateQueue(Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField()

    class Meta:
        table = "role_update_queue"
