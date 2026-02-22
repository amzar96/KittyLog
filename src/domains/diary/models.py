from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from src.shared.models.base import Base, CoreModel


class DiaryEntry(CoreModel, Base):
    __tablename__ = "diaryentry"

    entry_date = Column(DateTime, nullable=False)
    title = Column(String, nullable=True)
    content = Column(String, nullable=False)
    mood = Column(String, nullable=True)
    photo_urls = Column(String, nullable=True)  # JSON array stored as string
    cat_id = Column(String, ForeignKey("cat.id"), nullable=False)

    cat = relationship("Cat")
