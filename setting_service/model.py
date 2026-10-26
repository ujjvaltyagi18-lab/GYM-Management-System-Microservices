from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from datetime import date, datetime


class setting(SQLModel, table=True):
  """schema for storing setting."""
  id: int | None=Field(primary_key=True)
  key: str | None=Field(default=None)
  value: str | None=Field(default=None)
  created_at: date | None=Field(default=None)
  updated_at: datetime | None=Field(default=None)