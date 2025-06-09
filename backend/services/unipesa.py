import hashlib
import hmac
import os
import json
from fastapi import Request, HTTPException, status
from dotenv import load_dotenv

load_dotenv()

UNIPESA_SECRET = os.getenv("UNIPESA_SECRET")

def initiate_payment(amount: float, phone_number: str, description: str):
    """
    Simule une requête à l'API Unipesa pour initier un paiement.
    Dans une vraie application, cette fonction contiendrait un appel HTTP
    avec `requests` ou `httpx` à l'endpoint d'Unipesa.
    """
    print(f"Initiating payment of {amount} USD for {phone_number} for: {description}")
    # Simule une réponse réussie de l'API
    return {"status": "success", "transaction_id": "mock_tx_12345"}

async def verify_unipesa_signature(request: Request):
    """
    Vérifie la signature HMAC SHA512 du webhook Unipesa.
    """
    signature_header = request.headers.get("X-Unipesa-Signature")
    if not signature_header:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Unipesa-Signature header manquant.")

    raw_body = await request.body()
    
    expected_signature = hmac.new(
        UNIPESA_SECRET.encode('utf-8'),
        msg=raw_body,
        digestmod=hashlib.sha512
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, signature_header):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Signature invalide.")
    
    return json.loads(raw_body)