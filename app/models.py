from __future__ import annotations

from datetime import date  # noqa: TCH003

from sqlmodel import Field, SQLModel


class Item(SQLModel, table=True):  # noqa: D101
    id: int | None = Field(default=None, primary_key=True)
    amount: float
    dt: date
    account: str
