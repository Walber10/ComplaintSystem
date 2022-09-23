from typing import Optional, List

from fastapi import Depends, APIRouter
from fastapi.openapi.models import Response
from starlette import status

from managers.auth import oauth2_scheme, is_admin
from managers.user import UserManager
from models import RoleType
from schemas.response.user import UserResponse
from fastapi import Response

router = APIRouter(tags=["Users"])


@router.get("/users/", dependencies=[Depends(oauth2_scheme), Depends(is_admin)], response_model=List[UserResponse])
async def get_users(email: Optional[str] = None):
    if email:
        return await UserManager.get_user_by_email(email)
    return await UserManager.get_all_users()


@router.put("/users/{user_id}/make-admin", dependencies=[Depends(oauth2_scheme), Depends(is_admin)], status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def make_admin(user_id: int):
    await UserManager.change_role(RoleType.admin, user_id)
    return None



@router.put("/users/{user_id}/make-approver", dependencies=[Depends(oauth2_scheme), Depends(is_admin)], status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def make_admin(user_id: int):
    await UserManager.change_role(RoleType.approver, user_id)
    return None
