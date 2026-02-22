import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.dependencies import get_current_user
from src.domains.diary.schemas import DiaryEntryCreate, DiaryEntryResponse, DiaryEntryUpdate
from src.domains.diary.service import DiaryService
from src.shared.models.user import User
from src.shared.schemas.response import PaginatedResponse, ResponseModel
from src.utils.db import get_db
from src.utils.pagination import PaginationParams, get_pagination

router = APIRouter(prefix="/cats/{cat_id}/diary", tags=["diary"])
logger = logging.getLogger(__name__)


def get_diary_service(db: Session = Depends(get_db)) -> DiaryService:
    return DiaryService(db)


@router.get("", response_model=PaginatedResponse[DiaryEntryResponse])
def list_entries(
    cat_id: str,
    user: User = Depends(get_current_user),
    service: DiaryService = Depends(get_diary_service),
    pagination: PaginationParams = Depends(get_pagination),
):
    entries, total = service.list_entries(cat_id, user, pagination.page, pagination.page_size)
    return PaginatedResponse(
        data=entries, total=total, page=pagination.page, page_size=pagination.page_size
    )


@router.get("/{entry_id}", response_model=ResponseModel[DiaryEntryResponse])
def get_entry(
    cat_id: str,
    entry_id: str,
    user: User = Depends(get_current_user),
    service: DiaryService = Depends(get_diary_service),
):
    entry = service.get_entry(cat_id, entry_id, user)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diary entry not found")
    return ResponseModel(data=entry, message="success")


@router.post("", response_model=ResponseModel[DiaryEntryResponse], status_code=status.HTTP_201_CREATED)
def create_entry(
    cat_id: str,
    payload: DiaryEntryCreate,
    user: User = Depends(get_current_user),
    service: DiaryService = Depends(get_diary_service),
):
    entry = service.create_entry(cat_id, payload, user)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found")
    return ResponseModel(data=entry, message="Diary entry created successfully")


@router.put("/{entry_id}", response_model=ResponseModel[DiaryEntryResponse])
def update_entry(
    cat_id: str,
    entry_id: str,
    payload: DiaryEntryUpdate,
    user: User = Depends(get_current_user),
    service: DiaryService = Depends(get_diary_service),
):
    entry = service.update_entry(cat_id, entry_id, payload, user)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diary entry not found")
    return ResponseModel(data=entry, message="Diary entry updated successfully")


@router.delete("/{entry_id}", response_model=ResponseModel)
def delete_entry(
    cat_id: str,
    entry_id: str,
    user: User = Depends(get_current_user),
    service: DiaryService = Depends(get_diary_service),
):
    deleted = service.delete_entry(cat_id, entry_id, user)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diary entry not found")
    return ResponseModel(data=None, message="Diary entry deleted successfully")
