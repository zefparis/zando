from fastapi import FastAPI
from .database import engine
from .models import core as models
from .routes import auth, ads, payment, subscription # Importer le nouveau routeur
import os

# Crée le dossier pour les uploads s'il n'existe pas
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Crée les tables dans la base de données
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Zando API",
    description="API pour la plateforme de petites annonces Zando.",
    version="0.1.0"
)

app.include_router(auth.router)
app.include_router(ads.router)
app.include_router(payment.router)
app.include_router(subscription.router) # Inclure le routeur d'abonnement

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Zando"}