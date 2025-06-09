from pydantic import BaseModel
from typing import Optional

class AdBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float

class AdCreate(AdBase):
    pass

class Ad(AdBase):
    id: int
    owner_id: int
    image_url: Optional[str] = None
    currency: str
    
    class Config:
        orm_mode = True