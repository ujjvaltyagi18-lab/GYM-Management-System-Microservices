from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from datetime import date, datetime


class orders(SQLModel, table=True):
  """schema for storing order."""
  id: int | None=Field(primary_key=True)
  member_id: int 
  product_id: str | None=Field(default=None)
  status: str | None=Field(default=None)
  created_at: date | None=Field(default=None)
  updated_at: datetime | None=Field(default=None)