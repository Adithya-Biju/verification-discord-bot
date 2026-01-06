from tortoise import fields
from tortoise.models import Model

class Server(Model):
    server_id = fields.BigIntField(pk=True)
    server_name = fields.TextField(null=True)
    old_role_id = fields.BigIntField(null=True)
    new_role_id = fields.BigIntField(null=True)
    main_premium_role = fields.BigIntField(null=True)

    class Meta:
        table = "servers"