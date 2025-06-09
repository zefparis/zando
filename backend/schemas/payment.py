from pydantic import BaseModel
from typing import Optional

class PaymentRequest(BaseModel):
    amount: float
    currency: str = "USD"
    description: str
    # Le numéro de téléphone du payeur sera celui de l'utilisateur authentifié

class UnipesaWebhookPayload(BaseModel):
    transaction_id: str
    status: str
    amount: float
    customer_phone: str
    reference: Optional[str] = None