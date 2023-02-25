from typing import List, Union

from pydantic import BaseModel


class Item(BaseModel):
    id = int
    description = str
    amount = float
    unit = str

    class Config:
        orm_mode = True


''' keeping for later
class LocationBase(BaseModel):
    description: str


class LocationCreate(LocationBase):
    pass


class Location(LocationBase):
    id: int
    items: List[Item] = []

    class Config:
        orm_mode = True
'''
