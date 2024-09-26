from __future__ import annotations

from datetime import date  # noqa: TCH003

from pydantic import BaseModel


class Item(BaseModel):  # noqa: D101
    amount: float
    dt: date
    account: str
    repeat_every: str
    repetition_no: int | None = None
