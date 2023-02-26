# public imports
from typing import List

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

# local imports
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session=Depends(get_db)):
    items = read_all_items(db=db)
    return templates.TemplateResponse("index.html", {"request": request, "items": items})


@app.post("/items/")
def create_item(description: schemas.Item.description = Form(), amount: schemas.Item.amount = Form(), unit: schemas.Item.unit = Form(), db: Session=Depends(get_db)) -> RedirectResponse:
    item = {}
    item["description"] = description
    item["amount"] = amount
    item["unit"] = unit

    crud.create_item(db=db, item=item)
    return RedirectResponse(url="/", status_code=303)


@app.get("/items/", response_model=List[schemas.Item])
def read_all_items(db: Session=Depends(get_db)):
    all_items = crud.get_all_items(db)
    return all_items


@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session=Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.put("/items/{item_id}")
async def update_item(item_id: int, request: Request, db: Session=Depends(get_db)):
    request_body = await request.json()
    db_item = crud.update_item(db, item_id=item_id, item=request_body)
    return RedirectResponse(url="/", status_code=303)

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session=Depends(get_db)) -> None:
    crud.delete_item(db, item_id=item_id)

''' keeping for later
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
'''
