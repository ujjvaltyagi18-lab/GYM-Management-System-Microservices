from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from datetime import date, datetime


class salary(SQLModel, table=True):
  """schema for storing salary."""
  id: int | None=Field(primary_key=True)
  user_id: int
  created_at: date | None=Field(default=None)
  updated_at: datetime | None=Field(default=None)
