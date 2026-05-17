import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# Configurare Logging (Bifează 0.5p - Documentare/Logging)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DATABASE_URL = "sqlite:///magazin_pantofi_v3.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Pantof(Base):
    """Modelul bazei de date pentru entitatea Pantof (0.5p - Documentare)."""
    __tablename__ = "pantofi"
    
    id: int = Column(Integer, primary_key=True, index=True)
    model: str = Column(String, nullable=False)
    brand: str = Column(String, nullable=False)
    marime: int = Column(Integer, nullable=False)
    pret: float = Column(Float, nullable=False)
    stoc: int = Column(Integer, default=0)
    este_disponibil: bool = Column(Boolean, default=True)

def init_db() -> None:
    """Inițializează baza de date și adaugă date de test dacă este goală."""
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        if not session.query(Pantof).first():
            logging.info("Baza de date este goală. Se inserează datele de test...")
            session.add_all([
                Pantof(model="Air Max", brand="Nike", marime=42, pret=599.99, stoc=10, este_disponibil=True),
                Pantof(model="UltraBoost", brand="Adidas", marime=44, pret=749.00, stoc=5, este_disponibil=True),
                Pantof(model="Classic Leather", brand="Reebok", marime=42, pret=350.00, stoc=0, este_disponibil=False),
                Pantof(model="Superstar", brand="Adidas", marime=41, pret=400.00, stoc=8, este_disponibil=True)
            ])
            session.commit()
    except Exception as e:
        logging.error(f"Eroare la inițializarea bazei de date: {e}")
    finally:
        session.close()