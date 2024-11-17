import enum
from email.policy import default

from ms_core import AbstractModel
from tortoise import fields


class UserType(enum.IntEnum):
    PUPIL = 0
    ADMIN = 1


class User(AbstractModel):
    shkolo_username = fields.CharField(64, null=True, unique=True)
    shkolo_name = fields.CharField(256, null=True)
    coins = fields.IntField(default=0)
    bulbs = fields.IntField(default=0)
    level = fields.IntField(default=1)
    type = fields.IntEnumField(UserType, default=0)

    pupil_id = fields.BigIntField()

    class Meta:
        table = "users"
