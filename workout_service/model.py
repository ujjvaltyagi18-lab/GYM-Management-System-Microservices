from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from datetime import date, datetime


class workout(SQLModel, table=True):
  """schema for storing workout."""
  id: int | None=Field(primary_key=True)
  name: str | None=Field(default=None)
  description: str | None=Field(default=None)
  created_at: date | None=Field(default=None)
  updated_at: datetime | None=Field(default=None)