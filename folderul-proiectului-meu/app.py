from flask import Flask, render_template_string, request, redirect, url_for, send_file
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

app = Flask(__name__)

# Configurare bază de date locală SQLite (1p - Utilizare bază de date)
DATABASE_URL = "sqlite:///magazin_pantofi_v3.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Pantof(Base):
    """Modelul bazei de date (0.5p - Documentare prin docstrings si type hinting)."""
    __tablename__ = "pantofi"
    id = Column(Integer, primary_key=True, index=True)
    model: str = Column(String, nullable=False)
    brand: str = Column(String, nullable=False)
    marime: int = Column(Integer, nullable=False)
    pret: float = Column(Float, nullable=False)
    stoc: int = Column(Integer, default=0)
    este_disponibil: bool = Column(Boolean, default=True)

Base.metadata.create_all(bind=engine)

session_init = SessionLocal()
if not session_init.query(Pantof).first():
    session_init.add_all([
        Pantof(model="Air Max", brand="Nike", marime=42, pret=599.99, stoc=10, este_disponibil=True),
        Pantof(model="UltraBoost", brand="Adidas", marime=44, pret=749.00, stoc=5, este_disponibil=True),
        Pantof(model="Classic Leather", brand="Reebok", marime=42, pret=350.00, stoc=0, este_disponibil=False),
        Pantof(model="Superstar", brand="Adidas", marime=41, pret=400.00, stoc=8, este_disponibil=True)
    ])
    session_init.commit()
session_init.close()

# HTML și CSS nativ (fără framework-uri externe) - Interfață Grafică (1p)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <title>Gestiune Magazin Pantofi</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f4; color: #333; }
        h1 { text-align: center; color: #222; }
        .box { background: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; box-shadow: 0px 2px 5px rgba(0,0,0,0.1); }
        .form-inline input { padding: 8px; margin-right: 10px; border: 1px solid #ccc; border-radius: 4px; }
        .btn { padding: 8px 15px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; font-size: 14px; }
        .btn-success { background-color: #4CAF50; color: white; }
        .btn-primary { background-color: #008CBA; color: white; margin-right: 5px; }
        .btn-danger { background-color: #f44336; color: white; }
        .btn-dark { background-color: #555; color: white; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; background: white; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #333; color: white; }
        tr:hover { background-color: #f5f5f5; }
        .badge { padding: 4px 8px; border-radius: 3px; font-size: 12px; font-weight: bold; color: white; }
        .bg-success { background-color: #4CAF50; }
        .bg-danger { background-color: #f44336; }
        .actions-nav { margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; }
    </style>
</head>
<body>
    <h1>👟 Gestiune Stoc Magazin Pantofi</h1>

    <!-- CREATE: Formular adăugare produs -->
    <div class="box">
        <h3>Adaugă un produs nou</h3>
        <form action="/adauga" method="POST" class="form-inline">
            <input type="text" name="brand" placeholder="Brand" required>
            <input type="text" name="model" placeholder="Model" required>
            <input type="number" name="marime" placeholder="Mărime" required>
            <input type="number" step="0.01" name="pret" placeholder="Preț (lei)" required>
            <input type="number" name="stoc" placeholder="Stoc" required>
            <button type="submit" class="btn btn-success">Adaugă Produs</button>
        </form>
    </div>

    <!-- FILTRĂRI ȘI SORTĂRI (1p) -->
    <div class="actions-nav">
        <div>
            <a href="/" class="btn btn-primary" style="background-color: #777;">Toate produsele</a>
            <a href="/?sort=brand" class="btn btn-primary">Sortare după Brand</a>
            <a href="/?sort=pret_desc" class="btn btn-primary">Sortare după Preț</a>
            <a href="/?filtru=42" class="btn btn-primary" style="background-color: #009688;">Doar Mărimea 42</a>
        </div>
        <!-- RAPORT (1p) -->
        <a href="/raport" class="btn btn-dark">💾 Descărcă Raport Text</a>
    </div>

    <!-- READ, UPDATE, DELETE -->
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Brand</th>
                <th>Model</th>
                <th>Mărime</th>
                <th>Preț (lei) [Modifică]</th>
                <th>Stoc</th>
                <th>Status</th>
                <th>Acțiuni</th>
            </tr>
        </thead>
        <tbody>
            {% for p in produse %}
            <tr>
                <td>{{ p.id }}</td>
                <td><strong>{{ p.brand }}</strong></td>
                <td>{{ p.model }}</td>
                <td>{{ p.marime }}</td>
                <td>
                    <!-- UPDATE: Modificare preț rapidă -->
                    <form action="/update/{{ p.id }}" method="POST" style="display: inline-flex;">
                        <input type="number" step="0.01" name="pret_nou" value="{{ p.pret }}" style="width: 80px; padding: 4px; border: 1px solid #ccc;">
                        <button type="submit" style="margin-left: 5px; cursor: pointer;">🔄</button>
                    </form>
                </td>
                <td>{{ p.stoc }} buc.</td>
                <td>
                    {% if p.este_disponibil %}
                    <span class="badge bg-success">Disponibil</span>
                    {% else %}
                    <span class="badge bg-danger">Epuizat</span>
                    {% endif %}
                </td>
                <td>
                    <!-- DELETE: Ștergere produs -->
                    <a href="/sterge/{{ p.id }}" class="btn btn-danger" style="padding: 4px 8px; font-size: 12px;">Șterge</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

@app.route("/")
def index():
    session = SessionLocal()
    query = session.query(Pantof)
    sort_param = request.args.get('sort')
    filtru_param = request.args.get('filtru')
    
    if sort_param == 'brand':
        query = query.order_by(Pantof.brand)
    elif sort_param == 'pret_desc':
        query = query.order_by(Pantof.pret.desc())
    elif filtru_param:
        query = query.filter(Pantof.marime == int(filtru_param))
        
    produse = query.all()
    session.close()
    return render_template_string(HTML_TEMPLATE, produse=produse)

@app.route("/adauga", methods=["POST"])
def adauga():
    session = SessionLocal()
    stoc_val = int(request.form.get("stoc"))
    nou_pantof = Pantof(
        brand=request.form.get("brand"),
        model=request.form.get("model"),
        marime=int(request.form.get("marime")),
        pret=float(request.form.get("pret")),
        stoc=stoc_val,
        este_disponibil=stoc_val > 0
    )
    session.add(nou_pantof)
    session.commit()
    session.close()
    return redirect(url_for("index"))

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    session = SessionLocal()
    pantof = session.query(Pantof).filter(Pantof.id == id).first()
    if pantof:
        pantof.pret = float(request.form.get("pret_nou"))
        session.commit()
    session.close()
    return redirect(url_for("index"))

@app.route("/sterge/<int:id>")
def sterge(id):
    session = SessionLocal()
    pantof = session.query(Pantof).filter(Pantof.id == id).first()
    if pantof:
        session.delete(pantof)
        session.commit()
    session.close()
    return redirect(url_for("index"))

@app.route("/raport")
def raport():
    session = SessionLocal()
    produse = session.query(Pantof).all()
    valoare_totala = sum(p.pret * p.stoc for p in produse)
    total_perechi = sum(p.stoc for p in produse)
    
    continut = f"=== RAPORT STOC MAGAZIN PANTOFI ===\\n\\nTotal perechi: {total_perechi} buc.\\nValoare totala inventar: {valoare_totala} lei"
    cale = "raport_magazin.txt"
    with open(cale, "w", encoding="utf-8") as f:
        f.write(continut)
    session.close()
    return send_file(cale, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)