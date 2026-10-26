from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from datetime import time, date, datetime



class Address(SQLModel, table=True):
  """schema for storing address."""
  __tablename__ = "address"
  id: int | None=Field(primary_key=True)
  name: str | None=Field(default=None)
  city: str | None=Field(default=None)
  district: str | None=Field(default=None)
  state: str | None=Field(default=None)
  pincode: str | None=Field(default=None)
  latitude: float | None=Field(default=None)
  longitude: float | None=Field(default=None)
  opening_time: time | None=Field(default=None)
  closing_time: time | None=Field(default=None)
  created_at: date | None=Field(default=None)
  updated_at: datetime | None=Field(default=None)


class Schedule(SQLModel, table=True):
  """schema for storing schedule."""
  __tablename__ = "schedule"
  id: int | None=Field(primary_key=True)
  start_time: time | None=Field(default=None)
  end_time: time | None=Field(default=None)
  created_at: date | None=Field(default=None)
  updated_at: datetime | None=Field(default=None)


class Rollcode(SQLModel, table=True):
  """schema for storing rollcode."""
  __tablename__ = "rollcode"
  id: int | None=Field(primary_key=True)
  name: str | None=Field(default=None)
  created_at: date | None=Field(default=None)
  updated_at: datetime | None=Field(default=None)


class Members(SQLModel, table=True):
  """schema for storing member."""
  __tablename__ = "members"
  id: int | None=Field(primary_key=True)
  username: str | None=Field(default=None)
  first_name: str | None=Field(default=None)
  last_name: str | None=Field(default=None)
  phone: str | None=Field(default=None)
  email: str = Field(index=True, unique=True)
  address_id: int = Field(foreign_key="address.id")
  address: Address = Relationship()
  rollcode_id: int = Field(foreign_key="rollcode.id")
  rollcode: Rollcode = Relationship()
  schedule_id: int = Field(foreign_key="schedule.id")
  schedule: Schedule = Relationship()
  password: str | None=Field(default=None)
  created_at: date | None=Field(default=None)
  updated_at: datetime | None=Field(default=None)


