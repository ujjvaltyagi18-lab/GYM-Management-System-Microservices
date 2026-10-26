from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from datetime import date, datetime


class Plan(SQLModel, table=True):
  """schema for storing plan."""
  __tablename__ = "plan"
  id: int | None=Field(primary_key=True)
  name: str | None=Field(default=None)
  description: str | None=Field(default=None)
  price: float | None=Field(default=None)
  duration: int | None=Field(default=None)
  created_at: date | None=Field(default=None)
  updated_at: datetime | None=Field(default=None)


class Membership(SQLModel, table=True):
  """schema for storing membership."""
  __tablename__ = "membership"

  id: int | None=Field(primary_key=True)
  plan_id: int = Field(foreign_key="plan.id")
  plan: Plan = Relationship()
  created_at: date | None=Field(default=None)
  updated_at: datetime | None=Field(default=None)
