# public imports
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

# local imports
from models import Item, Location


app = FastAPI()


@app.get("/")
def read_root():
    items = read_all_items()
    locations = read_all_locations()
    return items, locations


@app.post("/items/create")
def create_item(item: Item):
    return item


@app.get("/items/all")
def read_all_items():
    all_items = {"All": "Items"}
    return all_items


@app.get("/items/{item_id}")
def read_item(item_id: int):
    item = {"item_id": item_id}
    return item


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    entry = {
        "item_id": item_id,
        "description": item.description,
        "amount": item.amount,
        "unit": item.unit,
        "location_id": item.location_id
    }
    return entry


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"Item": "deleted"}


@app.post("/locations/create")
def create_location(description: str):
    return description


@app.get("/locations/all")
def read_all_locations():
    all_locations = {"All": "locations"}
    return all_locations


@app.get("/locations/{location_id}")
def read_location(location_id: int):
    location = {"location_id": location_id}
    return location


@app.put("/locations/{location_id}")
def update_location(location_id: int, location: Location):
    entry = {
        "location_id": location_id,
        "description": location.description
    }
    return entry


@app.delete("/locations/{location_id}")
def delete_location(location_id: int):
    return {"Location": "deleted"}
