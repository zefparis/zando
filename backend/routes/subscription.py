from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, models, schemas
from ..services import security

router = APIRouter(
    prefix="/subscription",
    tags=["Subscription"]
)

@router.get("/me", response_model=schemas.subscription.Subscription)
def get_my_subscription(
    db: Session = Depends(database.get_db),
    current_user: models.core.User = Depends(security.get_current_user)
):
    """
    Récupère les détails de l'abonnement de l'utilisateur authentifié.
    """
    subscription = db.query(models.core.Subscription).filter(models.core.Subscription.user_id == current_user.id).first()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun abonnement trouvé pour cet utilisateur."
        )
        
    return subscription