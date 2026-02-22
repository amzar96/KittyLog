import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.dependencies import get_current_user
from src.domains.cats.schemas import CatCreate, CatResponse, CatUpdate
from src.domains.cats.service import CatService
from src.shared.models.user import User
from src.shared.rbac import require_permission
from src.shared.schemas.response import PaginatedResponse, ResponseModel
from src.utils.db import get_db

router = APIRouter(prefix="/cats", tags=["cats"])
logger = logging.getLogger(__name__)


def get_cat_service(db: Session = Depends(get_db)) -> CatService:
    return CatService(db)


@router.get("", response_model=PaginatedResponse[CatResponse])
def list_cats(
    user: User = Depends(get_current_user),
    service: CatService = Depends(get_cat_service),
    _: None = Depends(require_permission("can_read", "cat")),
):
    cats = service.get_cats_by_owner(user)
    return PaginatedResponse(data=cats, total=len(cats), page=1, page_size=len(cats))


@router.get("/{cat_id}", response_model=ResponseModel[CatResponse])
def get_cat(
    cat_id: str,
    user: User = Depends(get_current_user),
    service: CatService = Depends(get_cat_service),
    _: None = Depends(require_permission("can_read", "cat")),
):
    cat = service.get_cat_by_id(cat_id, user)
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found")
    return ResponseModel(data=cat, message="success")


@router.post("", response_model=ResponseModel[CatResponse], status_code=status.HTTP_201_CREATED)
def create_cat(
    payload: CatCreate,
    user: User = Depends(get_current_user),
    service: CatService = Depends(get_cat_service),
    _: None = Depends(require_permission("can_create", "cat")),
):
    try:
        cat = service.create_cat(payload, user)
        return ResponseModel(data=cat, message="Cat created successfully")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{cat_id}", response_model=ResponseModel[CatResponse])
def update_cat(
    cat_id: str,
    payload: CatUpdate,
    user: User = Depends(get_current_user),
    service: CatService = Depends(get_cat_service),
    _: None = Depends(require_permission("can_edit", "cat")),
):
    cat = service.update_cat(cat_id, payload, user)
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found")
    return ResponseModel(data=cat, message="Cat updated successfully")


@router.delete("/{cat_id}", response_model=ResponseModel)
def delete_cat(
    cat_id: str,
    user: User = Depends(get_current_user),
    service: CatService = Depends(get_cat_service),
    _: None = Depends(require_permission("can_delete", "cat")),
):
    deleted = service.delete_cat(cat_id, user)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found")
    return ResponseModel(data=None, message="Cat deleted successfully")
