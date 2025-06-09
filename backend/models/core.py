from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime

Base = declarative_base()

class AdStatus(enum.Enum):
    GRATUITE = "gratuite"
    BOOSTEE = "boostée"
    ABONNEE = "abonnée"

class SubscriptionStatus(enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    pin_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    ads = relationship("Ad", back_populates="owner")
    subscription = relationship("Subscription", back_populates="user", uselist=False)

class Ad(Base):
    __tablename__ = "ads"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    currency = Column(String, default="USD", nullable=False)
    status = Column(SQLAlchemyEnum(AdStatus), default=AdStatus.GRATUITE, nullable=False)
    image_url = Column(String, nullable=True) # URL de la première image gratuite
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="ads")

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=False)
    status = Column(SQLAlchemyEnum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    user = relationship("User", back_populates="subscription")