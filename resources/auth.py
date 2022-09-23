from fastapi import APIRouter

from managers.user import UserManager
from schemas.requests.user import UserRegisterIn, UserLogin

router = APIRouter(tags=["Auth"])


@router.post("/register/", status_code=201)
async def register(user_data: UserRegisterIn):
    token = await UserManager.register(user_data.dict())
    return {"token": token}


@router.post("/login/")
async def login(user_data: UserLogin):
    token = await UserManager.login(user_data.dict())
    return {"token": token}
