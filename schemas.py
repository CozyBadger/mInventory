from typing import List, Union

from pydantic import BaseModel


class ItemBase(BaseModel):
    description: str
    amount: float
    unit: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    location_id: int

    class Config:
        orm_mode = True


class LocationBase(BaseModel):
    description: str


class LocationCreate(LocationBase):
    pass


class Location(LocationBase):
    id: int
    items: List[Item] = []

    class Config:
        orm_mode = True
