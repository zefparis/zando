import shutil
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from .. import database, models, schemas
from ..services import security

router = APIRouter(
    prefix="/ads",
    tags=["Ads"]
)

@router.post("/", response_model=schemas.ads.Ad, status_code=status.HTTP_201_CREATED)
def create_ad(
    title: str,
    description: str,
    price: float,
    image: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: models.core.User = Depends(security.get_current_user)
):
    # Sauvegarde simple de l'image sur le disque
    file_path = f"uploads/{image.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    new_ad = models.core.Ad(
        title=title,
        description=description,
        price=price,
        owner_id=current_user.id,
        image_url=file_path
    )
    db.add(new_ad)
    db.commit()
    db.refresh(new_ad)
    return new_ad

@router.get("/", response_model=List[schemas.ads.Ad])
def read_ads(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    ads = db.query(models.core.Ad).offset(skip).limit(limit).all()
    return ads

@router.get("/{ad_id}", response_model=schemas.ads.Ad)
def read_ad(ad_id: int, db: Session = Depends(database.get_db)):
    ad = db.query(models.core.Ad).filter(models.core.Ad.id == ad_id).first()
    if ad is None:
        raise HTTPException(status_code=404, detail="Ad not found")
    return ad