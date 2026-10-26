from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from datetime import date, datetime


class search(SQLModel, table=True):
  """schema for storing search."""
  id: int | None=Field(primary_key=True)
  member_id: int
  query: str | None=Field(default=None)
  created_at: date | None=Field(default=None)
  updated_at: datetime | None=Field(default=None)