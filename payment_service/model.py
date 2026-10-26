from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from datetime import date, datetime


class payment(SQLModel, table=True):
  """schema for storing payment."""
  id: int | None=Field(primary_key=True)
  member_id: int 
  membership_id: int 
  amount: int | None=Field(default=None)
  date: date | None=Field(default=None)
  method: str | None=Field(default=None)
  status: str | None=Field(default=None)
  due: date | None=Field(default=None)
  created_at: date | None=Field(default=None)
  updated_at: datetime | None=Field(default=None)