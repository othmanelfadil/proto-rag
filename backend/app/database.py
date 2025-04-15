from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import os 

# Electron determines where the SQLite database will be stored when the backend is launched
# if not set app.db will be used
DB_PATH = os.getenv("DB_PATH", "app.db")
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()