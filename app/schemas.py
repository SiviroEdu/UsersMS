from pydantic_partial import create_partial_model
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import User

Tortoise.init_models(
    ["app.models"], "models"
)

UserSchema = pydantic_model_creator(User, name="UserSchema")
UserCreate = pydantic_model_creator(
    User,
    name="UserCreate",
    exclude_readonly=True,
)
UserUpdate = create_partial_model(
    pydantic_model_creator(
        User,
        name="UserUpdate",
        exclude_readonly=True,
    )
)


class UserMeResponse(pydantic_model_creator(User, name="UserMeResponse")):
    next_level_coins: int
