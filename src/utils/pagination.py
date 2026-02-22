from fastapi import Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 20


def get_pagination(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> PaginationParams:
    return PaginationParams(page=page, page_size=page_size)
