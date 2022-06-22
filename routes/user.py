from fastapi import APIRouter, Depends
from utils.token import get_current_username

user = APIRouter()


@user.get('/me', tags=["user"])
async def current_user(username: str = Depends(get_current_username)):
    return {"username": username}
