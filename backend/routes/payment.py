from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from .. import database, models, schemas
from ..services import security, unipesa

router = APIRouter(
    prefix="/payment",
    tags=["Payment"]
)

@router.post("/initiate")
def initiate_payment_route(
    payment_request: schemas.payment.PaymentRequest,
    db: Session = Depends(database.get_db),
    current_user: models.core.User = Depends(security.get_current_user)
):
    # Appelle le service Unipesa pour démarrer la transaction
    response = unipesa.initiate_payment(
        amount=payment_request.amount,
        phone_number=current_user.phone_number,
        description=payment_request.description
    )
    return response

@router.post("/webhook")
async def unipesa_webhook(
    request: Request,
    db: Session = Depends(database.get_db)
):
    payload = await unipesa.verify_unipesa_signature(request)
    
    # Ici, vous mettriez à jour votre base de données
    # Par exemple, marquer une annonce comme "boostée" ou activer un abonnement
    print("Webhook vérifié reçu :", payload)
    
    # Logique de traitement du paiement
    if payload.get("status") == "SUCCESS":
        # Mettre à jour la base de données...
        pass
        
    return {"status": "received"}