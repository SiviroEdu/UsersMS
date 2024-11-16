from ms_core import AbstractModel
from tortoise import fields


class User(AbstractModel):
    shkolo_username = fields.CharField(64, null=True, unique=True)
    shkolo_name = fields.CharField(256, null=True)
    coins = fields.IntField(default=0)
    bulbs = fields.IntField(default=0)

    pupil_id = fields.BigIntField()

    class Meta:
        table = "users"
