from src.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from src.database.models import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()

def get_engine():
    db_url = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    return create_engine(db_url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=get_engine()
)

def init_db():
    Base.metadata.create_all(bind=get_engine())

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()