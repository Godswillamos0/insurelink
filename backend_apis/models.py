from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean


class Users(Base):
    __tablename__ = 'users'
    
    id=Column(Integer, primary_key=True, index=True)
    first_name=Column(String)
    last_name=Column(String)
    username=Column(String, unique=True)
    email=Column(String, unique=True)
    hashed_password=Column(String)
    age=Column(Integer)
    budget=Column(Integer)
    gender=Column(String)
    nin=Column(Integer)
    phone=Column(String)
    
    
class Insurance(Base):
    __tablename__='insurance'
    
    id=Column(Integer, primary_key=True, index=True)
    company_name=Column(String)
    insurance_type=Column(String)
    insurance_policy= Column(String)
    
    
class Datas(Base):
    __tablename__='datas'
    
    id=Column(Integer, primary_key=True, index=True)
    owner_id=Column(Integer, ForeignKey("users.id"))
    insurance_id=Column(Integer, ForeignKey("insurance.id"))
    time_stamp=Column(DateTime)
    exp_time=Column(DateTime)
    paid=Column(Boolean)
    
