from __future__ import annotations

from datetime import UTC, date, datetime

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


@router.post("")
def create_item(item: schemas.Item):
    diff = relativedelta(date(2085, 10, 23), item.dt)
    time_period = item.repeat_every[-1]
    return int(item.repeat_every[:-1])
    # _item = models.Item(**item.model_dump())
    # with Session(engine) as session:
    #     session.add(_item)
    #     session.commit()
    #     session.refresh(_item)
    #     return _item


@router.get("")
def read_items() -> list:
    with Session(engine) as session:
        return session.exec(select(models.Item)).all()
