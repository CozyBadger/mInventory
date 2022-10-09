from pydantic import BaseModel


class Item(BaseModel):
    description: str
    amount: float
    unit: str
    location_id: int


class Location(BaseModel):
    description: str
