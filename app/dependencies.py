from fastapi import Header, HTTPException
from starlette import status

from app.settings import SERVICE_KEY


async def confirm_inner(service_key: str = Header(None)):
    if not service_key or (service_key != SERVICE_KEY):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied."
        )
