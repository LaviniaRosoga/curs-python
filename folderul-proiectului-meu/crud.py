import logging
from typing import List, Optional
from database import SessionLocal, Pantof

def obtine_produse(sort_param: Optional[str] = None, filtru_param: Optional[str] = None) -> List[Pantof]:
    """Obține produsele aplicând filtre și sortări (1p - Minim 3 opțiuni)."""
    session = SessionLocal()
    query = session.query(Pantof)
    
    # 1. Filtrare după mărime
    if filtru_param:
        query = query.filter(Pantof.marime == int(filtru_param))
    
    # 2. Sortare după brand alfabetic
    if sort_param == 'brand':
        query = query.order_by(Pantof.brand)
    # 3. Sortare după preț descrescător
    elif sort_param == 'pret_desc':
        query = query.order_by(Pantof.pret.desc())
        
    produse = query.all()
    session.close()
    return produse

def adauga_produs(brand: str, model: str, marime: int, pret: float, stoc: int) -> None:
    """Adaugă un produs nou în stoc (CREATE - 2p CRUD)."""
    session = SessionLocal()
    try:
        nou_pantof = Pantof(
            brand=brand,
            model=model,
            marime=marime,
            pret=pret,
            stoc=stoc,
            este_disponibil=stoc > 0
        )
        session.add(nou_pantof)
        session.commit()
        logging.info(f"Produs adăugat cu succes: {brand} {model}")
    except Exception as e:
        logging.error(f"Eroare la adăugarea produsului: {e}")
    finally:
        session.close()

def actualizeaza_pret(id_produs: int, pret_nou: float) -> None:
    """Modifică prețul unui produs existent după ID (UPDATE - 2p CRUD)."""
    session = SessionLocal()
    pantof = session.query(Pantof).filter(Pantof.id == id_produs).first()
    if pantof:
        pantof.pret = pret_nou
        session.commit()
        logging.info(f"Preț actualizat pentru ID {id_produs} la {pret_nou} lei.")
    session.close()

def sterge_produs(id_produs: int) -> None:
    """Șterge definitiv un produs din baza de date (DELETE - 2p CRUD)."""
    session = SessionLocal()
    pantof = session.query(Pantof).filter(Pantof.id == id_produs).first()
    if pantof:
        session.delete(pantof)
        session.commit()
        logging.info(f"Produsul cu ID {id_produs} a fost șters.")
    session.close()