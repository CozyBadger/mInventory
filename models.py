# Public imports
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Local imports
from database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    amount = Column(Integer)
    unit = Column(String)
    ''' keeing for later
    location_id = Column(Integer, ForeignKey("locations.id"))

    location = relationship("Locations", back_populates="items")


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)

    items = relationship("Item", back_populates="location")
    '''
