from sqlalchemy.orm import Session

import models, schemas


def create_item(db: Session, item: schemas.Item):
    db_item = models.Item(**item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_all_items(db: Session):
    return db.query(models.Item).all()


def update_item(db: Session, item_id: int, item: schemas.Item):
    db_item = db.query(models.Item).filter(models.Item.id == item_id)
    db_item.update(item.dict())
    db.commit()
    return db_item.first()


def delete_item(db: Session, item_id: int) -> None:
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is not None:
        db.delete(db_item)
    db.commit()


def create_location(db: Session):
    db_location = models.Location(description=schemas.LocationCreate)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


def get_location(db: Session, location_id: int):
    return db.query(models.Location).filter(models.Location.id == location_id).first()


def get_all_locations(db: Session):
    return db.query(models.Location).all()
