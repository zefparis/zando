# Utiliser une image Python officielle
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application
COPY . .

# Exposer le port que Railway utilisera
EXPOSE 8000

# Commande pour lancer l'application. Railway injectera la variable $PORT.
CMD uvicorn main:app --host 0.0.0.0 --port $PORT