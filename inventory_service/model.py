from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from datetime import date, datetime



class equipments(SQLModel, table=True):
  """schema for storing equipment."""
  id: int | None=Field(primary_key=True)
  name: str | None=Field(default=None)
  quantity: int | None=Field(default=None)
  status: str | None=Field(default=None)
  created_at: date | None=Field(default=None)
  updated_at: datetime | None=Field(default=None)


class products(SQLModel, table=True):
  """schema for storing products."""
  id: int | None=Field(primary_key=True)
  name: str | None=Field(default=None)
  description: str | None=Field(default=None)
  price: float | None=Field(default=None)
  created_at: date | None=Field(default=None)
  updated_at: datetime | None=Field(default=None)