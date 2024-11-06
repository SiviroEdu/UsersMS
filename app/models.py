from ms_core import AbstractModel
from tortoise import fields


class User(AbstractModel):
    name = fields.CharField(64, null=True)

    class Meta:
        table = "users"
