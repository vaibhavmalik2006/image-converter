from typing import Optional
from pydantic import BaseModel, Field


class HistoryCreate(BaseModel):
    filename: str
    original_format: str
    converted_format: str
    original_size: float
    final_size: float
    width: int
    height: int
    dpi: int


class HistoryOut(BaseModel):
    id: int
    filename: str
    original_format: str
    converted_format: str
    original_size: float
    final_size: float
    width: int
    height: int
    dpi: int
    created_at: str

    class Config:
        from_attributes = True
