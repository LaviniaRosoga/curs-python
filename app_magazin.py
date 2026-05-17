from flask import Flask, render_template_string, request, redirect, url_for, send_file
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

app = Flask(__name__)

# Folosim un fișier fizic local izolat pentru a păstra tabela creată
DATABASE_URL = "sqlite:///magazin_pantofi_v2.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Pantof(Base):
    __tablename__ = "pantofi"
    id = Column(Integer, primary_key=True, index=True)
    model: str = Column(String, nullable=False)
    brand: str = Column(String, nullable=False)
    marime: int = Column(Integer, nullable=False)
    pret: float = Column(Float, nullable=False)
    stoc: int = Column(Integer, default=0)
    este_disponibil: bool = Column(Boolean, default=True)

# Forțăm crearea tabelei pe disc la pornire
Base.metadata.create_all(bind=engine)

# Inserare date de test dacă tabela este goală
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

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <title>Gestiune Magazin Pantofi</title>
    <link href="https://jsdelivr.net" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container mt-5">
        <h1 class="text-center mb-4">👟 Gestiune Stoc Magazin Pantofi</h1>
        <div class="card mb-4 shadow-sm">
            <div class="card-header bg-primary text-white"><h5>Adaugă un produs nou</h5></div>
            <div class="card-body">
                <form action="/adauga" method="POST" class="row g-3">
                    <div class="col-md-3"><input type="text" name="brand" class="form-control" placeholder="Brand" required></div>
                    <div class="col-md-3"><input type="text" name="model" class="form-control" placeholder="Model" required></div>
                    <div class="col-md-2"><input type="number" name="marime" class="form-control" placeholder="Mărime" required></div>
                    <div class="col-md-2"><input type="number" step="0.01" name="pret" class="form-control" placeholder="Preț" required></div>
                    <div class="col-md-2"><input type="number" name="stoc" class="form-control" placeholder="Stoc" required></div>
                    <div class="col-12 text-end"><button type="submit" class="btn btn-success">Adaugă în Stoc</button></div>
                </form>
            </div>
        </div>
        <div class="mb-3 d-flex justify-content-between align-items-center">
            <div>
                <a href="/" class="btn btn-outline-secondary btn-sm me-2">Toate produsele</a>
                <a href="/?sort=brand" class="btn btn-outline-primary btn-sm me-2">Sortare după Brand</a>
                <a href="/?sort=pret_desc" class="btn btn-outline-primary btn-sm me-2">Sortare după Preț</a>
                <a href="/?filtru=42" class="btn btn-outline-info btn-sm">Doar Mărimea 42</a>
            </div>
            <a href="/raport" class="btn btn-dark btn-sm">💾 Generare Raport</a>
        </div>
        <div class="card shadow-sm">
            <table class="table table-hover align-middle mb-0">
                <thead class="table-dark">
                    <tr><th>ID</th><th>Brand</th><th>Model</th><th>Mărime</th><th>Preț (lei)</th><th>Stoc</th><th>Disponibilitate</th><th>Acțiuni</th></tr>
                </thead>
                <tbody>
                    {% for p in produse %}
                    <tr>
                        <td>{{ p.id }}</td>
                        <td><strong>{{ p.brand }}</strong></td>
                        <td>{{ p.model }}</td>
                        <td><span class="badge bg-secondary">{{ p.marime }}</span></td>
                        <td>
                            <form action="/update/{{ p.id }}" method="POST" class="d-flex" style="max-width: 140px;">
                               <input type="number" step="0.01" name="pret_nou" class="form-control form-control-sm me-1" value="{{ p.pret }}">
                               <button type="submit" class="btn btn-sm btn-outline-warning">🔄</button>
                            </form>
                        </td>
                        <td>{{ p.stoc }} buc.</td>
                        <td>{% if p.este_disponibil %}<span class="badge bg-success">Disponibil</span>{% else %}<span class="badge bg-danger">Epuizat</span>{% endif %}</td>
                        <td><a href="/sterge/{{ p.id }}" class="btn btn-sm btn-danger">Șterge</a></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
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
        brand=request.form.get("brand"), model=request.form.get("model"),
        marime=int(request.form.get("marime")), pret=float(request.form.get("pret")),
        stoc=stoc_val, este_disponibil=stoc_val > 0
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
    continut = f"=== RAPORT STOC ===\\nTotal perechi: {total_perechi}\\nValoare totala: {valoare_totala} lei"
    cale = "raport_magazin.txt"
    with open(cale, "w", encoding="utf-8") as f: f.write(continut)
    session.close()
    return send_file(cale, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)