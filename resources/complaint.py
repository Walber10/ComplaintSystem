from typing import List
from fastapi import APIRouter, Depends, Request, Response
from starlette import status

from managers.auth import oauth2_scheme, is_complainer, is_admin, is_approver
from managers.complaint import ComplaintManager
from schemas.requests.complaintRequest import ComplaintRequest
from schemas.response.ComplaintResponse import ComplaintResponse

router = APIRouter(tags=["Complaints"])


@router.get("/complaints/", dependencies=[Depends(oauth2_scheme)], response_model=List[ComplaintResponse])
async def get_complaints(request: Request):
    user = request.state.user
    return await ComplaintManager.get_complaints(user)


@router.post("/complaints/", dependencies=[Depends(oauth2_scheme), Depends(is_complainer)],
             response_model=ComplaintResponse)
async def create_complaint(request: Request, complaint: ComplaintRequest):
    user = request.state.user
    return await ComplaintManager.create_complaint(complaint.dict(), user)


@router.delete("/complaints/{complaint_id}", dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
               status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_complaint(complaint_id: int):
    await ComplaintManager.delete(complaint_id)
    return None


@router.put("/complaints/{complaint_id}/approve", dependencies=[Depends(oauth2_scheme), Depends(is_approver)],
            status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def approve_complaint(complaint_id: int):
    await ComplaintManager.approve(complaint_id)
    return None


@router.put("/complaints/{complaint_id}/reject", dependencies=[Depends(oauth2_scheme), Depends(is_approver)],
            status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def reject_complaint(complaint_id: int):
    await ComplaintManager.reject(complaint_id)
    return None
