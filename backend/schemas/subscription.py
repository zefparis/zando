from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.core import SubscriptionStatus

class Subscription(BaseModel):
    id: int
    user_id: int
    start_date: datetime
    end_date: datetime
    status: SubscriptionStatus

    class Config:
        orm_mode = True