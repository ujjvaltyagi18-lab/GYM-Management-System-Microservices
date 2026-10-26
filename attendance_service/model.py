from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from datetime import time, date, datetime


class attendance(SQLModel, table=True):
  """schema for storing attendance."""
  id: int | None=Field(primary_key=True)
  member_id: int 
  date: date | None=Field(default=None)
  entry_time: time | None=Field(default=None)
  exit_time: time | None=Field(default=None)
  created_at: date | None=Field(default=None)
  updated_at: datetime | None=Field(default=None)