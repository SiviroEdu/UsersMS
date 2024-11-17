from typing import Annotated, LiteralString, Literal

from fastapi import Path, HTTPException, status
from fastapi.params import Query, Depends
from ms_core import BaseCRUDRouter

from app import UserCRUD, UserCreate, UserSchema, User
from app.bridges.dependencies import get_current_user
from app.dependencies import confirm_inner

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


@router.post("/{item_id}/{currency}/add", tags=["currency"])
async def inc_currency(
        _: Annotated[None, Depends(confirm_inner)],
        item_id: int = Path(),
        currency: Literal["coins", "bulbs"] = Path(),
        value: int = Query()
) -> int:
    if not (user := await User.get_or_none(id=item_id)):
        raise HTTPException(
            status_code=400,
            detail="No such user"
        )

    if currency == "coins":
        summed = user.coins + value
    elif currency == "bulbs":
        summed = user.bulbs + value
    else:
        raise HTTPException(
            status_code=400,
            detail="Unknown currency"
        )

    await user.update_from_dict({currency: summed}).save()

    return summed
