from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base


class ProcessingHistory(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_format = Column(String, nullable=False)
    converted_format = Column(String, nullable=False)
    original_size = Column(Float, nullable=False)
    final_size = Column(Float, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    dpi = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
