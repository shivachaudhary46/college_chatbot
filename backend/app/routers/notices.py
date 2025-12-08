from fastapi import APIRouter, HTTPException, Depends
from typing import List

from models.schemas import NoticeCreate, NoticeResponse
from models.models import User, Notice
from utilities.crud import (
    create_notice_records,
    get_all_notices,
    get_notice_by_id,
    update_notice,
    delete_notice,
)
from auth.OAuth import role_required
from db.database import SessionDep
from logger.logger import logger

router = APIRouter(
    prefix="/api/v1/notices",
    tags=["notices"]
)

@router.post("/", response_model=NoticeResponse)
def post_notice(
    notice_data: NoticeCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"]))
):
    """Teachers or admins can post notices"""
    try:
        notice = Notice(
            title=notice_data.title,
            content=notice_data.content,
            created_by=user.id,
            target_batch=notice_data.target_batch,
            target_program=notice_data.target_program,
            course_id=notice_data.course_id
        )
        created_notice = create_notice_records(session, notice)
        logger.info(f"Notice '{notice_data.title}' created by user {user.username}")
        return created_notice
    except Exception as e:
        logger.error(f"Unexpected error while creating notice: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/", response_model=List[NoticeResponse])
def get_notices_endpoint(session: SessionDep):
    """All users can view all notices"""
    try:
        notices = get_all_notices(session)
        logger.info(f"Fetched {len(notices)} notices")
        return notices
    except Exception as e:
        logger.error(f"Unexpected error while fetching notices: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{notice_id}", response_model=NoticeResponse)
def get_notice_by_id_endpoint(notice_id: int, session: SessionDep):
    """Get a specific notice"""
    try:
        notice = get_notice_by_id(session, notice_id)
        if not notice:
            logger.warning(f"Notice {notice_id} not found")
            raise HTTPException(status_code=404, detail="Notice not found")
        logger.info(f"Notice {notice_id} fetched successfully")
        return notice
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while fetching notice {notice_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/{notice_id}", response_model=NoticeResponse)
def update_notice_endpoint(
    notice_id: int,
    notice_data: NoticeCreate,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"]))
):
    """Update a notice (only by teacher/admin)"""
    try:
        notice = update_notice(session, notice_id, notice_data)
        if not notice:
            logger.warning(f"Notice {notice_id} not found for update")
            raise HTTPException(status_code=404, detail="Notice not found")
        logger.info(f"Notice {notice_id} updated by user {user.username}")
        return notice
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while updating notice {notice_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{notice_id}")
def delete_notice_endpoint(
    notice_id: int,
    session: SessionDep,
    user: User = Depends(role_required(["teacher", "admin"]))
):
    """Delete a notice (admin, teacher) only"""
    try:
        if not delete_notice(session, notice_id):
            logger.warning(f"Notice {notice_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Notice not found")
        logger.info(f"Notice {notice_id} deleted by admin {user.username}")
        return {"message": "Notice deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while deleting notice {notice_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")