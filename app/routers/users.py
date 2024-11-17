import math
from typing import Annotated, Literal

from fastapi import Path, HTTPException, APIRouter, BackgroundTasks
from fastapi.params import Query, Depends, Body

from app import UserCRUD, UserSchema, User, UserMeResponse, UserUpdate
from app.bridges.dependencies import get_current_user
from app.dependencies import confirm_inner

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/pupil_id/{id_}")
async def get_by_pupil_id(id_: int = Path()) -> UserSchema | None:
    return await UserCRUD.get_by(pupil_id=id_)


@router.get("/username/{username}")
async def get_by_username(username: str = Path()) -> UserSchema | None:
    return await UserCRUD.get_by(shkolo_username=username)


@router.put("/@me")
async def update(
        user: Annotated[UserSchema, Depends(get_current_user)],
        payload: UserUpdate = Body()
) -> UserSchema | None:
    if user.type == 1:
        prohibited = {"shkolo_username"}
    else:
        prohibited = {
            "shkolo_username", "created_at", "id", "coins", "bulbs",
            "level", "type", "pupil_id"
        }

    keys = set(payload.model_dump(exclude_none=True, exclude_defaults=True).keys())

    if keys.intersection(prohibited):
        print(keys)
        raise HTTPException(
            status_code=403,
            detail="Editing this field is forbidden."
        )

    return await UserCRUD.update_by(payload, id=user.id)


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


def calc_level_up_coins(current_level: int) -> int:
    """Calculates experience points needed to level up.

    Args:
        `current_level` (`int`): Current level.

    Returns:
        `int`: Experience points needed to level up.
    """
    return int((current_level - 1) * 83 + math.sqrt(current_level * 10) * 83)


async def levelup_user(user: UserSchema, price: int):
    await (user_ := await User.get(id=user.id)).update_from_dict(
        {"level": user_.level + 1, "coins": user.coins - price}
    ).save()

@router.get("/@me/levelup", summary="Levelup and response next_level_coins")
async def levelup(
        user: Annotated[UserSchema, Depends(get_current_user)],
        background_tasks: BackgroundTasks
):
    if user.coins < (price := calc_level_up_coins(user.level)):
        raise HTTPException(
            status_code=400,
            detail=dict(
                message="Not enough coins.",
                next_level_coins=price
            )
        )

    background_tasks.add_task(levelup_user, user, price)

    return {"next_level_coins": calc_level_up_coins(user.level+1)}


@router.get("/@me")
async def get_me(
        user: Annotated[UserSchema, Depends(get_current_user)]
) -> UserMeResponse:
    return UserMeResponse(
        next_level_coins=calc_level_up_coins(user.level),
        **user.model_dump()
    )
