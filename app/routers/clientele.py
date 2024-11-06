from ms_core import BaseCRUDRouter

from app import UserCRUD, UserCreate, UserSchema

router = BaseCRUDRouter[UserSchema, UserCreate](
    crud=UserCRUD,
    schema=UserSchema,
    schema_create=UserCreate,
    prefix="/users",
    tags=["users"]
)
