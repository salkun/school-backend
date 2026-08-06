from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Membuat engine koneksi ke PostgreSQL
engine = create_engine(settings.DATABASE_URL)

# SessionLocal digunakan di tiap request API untuk interaksi ke DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class yang akan diturunkan ke semua Model (Tabel) kita
Base = declarative_base()

# Dependency function untuk dipanggil di endpoint FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()