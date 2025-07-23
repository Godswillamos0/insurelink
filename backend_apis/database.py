from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'postgresql://insurelink_user:BNoIrADzZ6vOC8FKrYEPeokE4mfiQjY6@dpg-d20513emcj7s73ao6p00-a.oregon-postgres.render.com/insurelink'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
