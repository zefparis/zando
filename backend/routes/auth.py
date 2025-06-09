from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import core as models
from ..schemas import auth as schemas
from ..services import security

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.phone_number == user.phone_number).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Ce numéro de téléphone est déjà enregistré.")
    
    hashed_pin = security.get_pin_hash(user.pin)
    new_user = models.User(phone_number=user.phone_number, pin_hash=hashed_pin)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"Utilisateur {new_user.phone_number} créé avec succès."}

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.phone_number == form_data.phone_number).first()
    if not user or not security.verify_pin(form_data.pin, user.pin_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Numéro de téléphone ou code PIN incorrect.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(
        data={"sub": user.phone_number}
    )
    return {"access_token": access_token, "token_type": "bearer"}