from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    phone_number: str = Field(..., pattern=r"^\+243[0-9]{9}$")
    pin: str = Field(..., min_length=6, max_length=6)

class UserLogin(BaseModel):
    phone_number: str
    pin: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    phone_number: str | None = None