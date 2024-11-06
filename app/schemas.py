from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import User

Tortoise.init_models(
    ["app.models"], "models"
)

UserSchema = pydantic_model_creator(User, name="ClientSchema")
UserCreate = pydantic_model_creator(
    User,
    name="ClientCreate",
    exclude_readonly=True,
)
