from __future__ import annotations

from datetime import date

import numpy as np
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter
from sqlmodel import Session, select

from . import models, schemas
from .database import engine

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.post("/repeat")
def repeat(item: schemas.Repeat) -> list:
    diff = relativedelta(date(2085, 10, 23), item.dt)
    start = int(item.repeat_every[:-1])
    period = item.repeat_every[-1]
    _dict = {
        "y": {"d": diff.years, "k": "years"},
        "m": {"d": diff.years * 12 + diff.months, "k": "months"},
    }
    stop = int(_dict[period]["d"] / start) * start
    return [
        {
            "dt": item.dt + relativedelta(**{_dict[period]["k"]: d}),
            **item.model_dump(include=["amount", "account", "parent_id"]),
        } for d in np.linspace(start, stop, stop // start)
    ]


@router.post("")
def create_item(item: schemas.Item) -> models.Item:
    _item = models.Item(**item.model_dump())
    with Session(engine) as session:
        session.add(_item)
        session.commit()
        session.refresh(_item)
        return _item


@router.get("")
def read_items() -> list[models.Item]:
    with Session(engine) as session:
        return session.exec(select(models.Item)).all()
