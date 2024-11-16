from fastapi import Path
from ms_core import BaseCRUDRouter

from app import UserCRUD, UserCreate, UserSchema

router = BaseCRUDRouter[UserSchema, UserCreate](
    crud=UserCRUD,
    schema=UserSchema,
    schema_create=UserCreate,
    prefix="/users",
    tags=["users"]
)

@router.get("/pupil_id/{id_}")
async def get_by_pupil_id(id_: int = Path()) -> UserSchema | None:
    return await UserCRUD.get_by(pupil_id=id_)


@router.get("/username/{username}")
async def get_by_username(username: str = Path()) -> UserSchema | None:
    return await UserCRUD.get_by(shkolo_username=username)
