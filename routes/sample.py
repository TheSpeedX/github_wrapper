from fastapi import APIRouter, Depends
from utils.token import get_current_token

user = APIRouter()


@user.get('/me', tags=["user"])
async def current_user(access_token: str = Depends(get_current_token)):
    return {"token": access_token}
