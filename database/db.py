from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://postgres:abcd@localhost/ML_Training")

base = declarative_base()

SessionLocal = sessionmaker(bind=engine)