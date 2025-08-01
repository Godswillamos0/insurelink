from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean


class Users(Base):
    __tablename__ = 'users'
    
    id=Column(Integer, primary_key=True, index=True)
    first_name=Column(String)
    last_name=Column(String)
    email=Column(String, unique=True)
    hashed_password=Column(String)
    phone=Column(String)
    email_verified= Column(Boolean)
    is_onboarded = Column(Boolean)
    
    
class InsuranceProduct(Base):
    __tablename__='insurance'
    
    id=Column(Integer, primary_key=True, index=True)

    owner_id=Column(Integer, ForeignKey("users.id"))
    start_time=Column(String)
    end_time=Column(String)
    amount=Column(Integer)
    insurance_type=Column(String) # e.g., "monthly", "weekly"

    insurance_type=Column(String)

    
    
class Claims(Base):
    __tablename__='datas'
    
    id=Column(Integer, primary_key=True, index=True)
    owner_id=Column(Integer, ForeignKey("users.id"))
    insurance_id=Column(Integer, ForeignKey("insurance.id"))
    document_submitted=Column(Boolean)
    document_verified=Column(Boolean)


class Premium(Base):
    __tablename__='premium'
    
    id=Column(Integer, primary_key=True, index=True)
    owner_id=Column(Integer, ForeignKey("users.id"))
    insurance_id=Column(Integer, ForeignKey("insurance.id"))
    amount=Column(Integer, ForeignKey("insurance.amount"))
    due_date=Column(DateTime)
    paid_date=Column(DateTime)
    is_paid=Column(Boolean)
    
