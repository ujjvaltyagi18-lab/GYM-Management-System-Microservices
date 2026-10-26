from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from datetime import date, datetime


class feedback(SQLModel, table=True):
  """schema for storing feedback."""
  id: int | None=Field(primary_key=True)
  message: str | None=Field(default=None)
  created_at: date | None=Field(default=None)
  updated_at: datetime | None=Field(default=None)