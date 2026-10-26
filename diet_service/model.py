from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from datetime import date, datetime


class diet(SQLModel, table=True):
  """schema for storing diet."""
  id: int | None=Field(primary_key=True)
  member_id: int
  nutritionist_id: int
  diet_plan: str | None=Field(default=None)
  start_date: date | None=Field(default=None)
  end_date: date | None=Field(default=None)
  created_at: date | None=Field(default=None)
  updated_at: datetime | None=Field(default=None)