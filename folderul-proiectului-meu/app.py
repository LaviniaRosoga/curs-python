from flask import Flask, render_template, request, redirect, url_for, send_file
from database import init_db, SessionLocal, Pantof
import crud

app = Flask(__name__)

# Inițializăm baza de date la pornire (1p - Utilizare DB)
init_db()

@app.route("/")
def index():
    """Ruta principală care afișează tabelul (READ - 2p CRUD)."""
    sort_param = request.args.get('sort')
    filtru_param = request.args.get('filtru')
    produse = crud.obtine_produse(sort_param, filtru_param)
    return render_template("index.html", produse=produse)

@app.route("/adauga", methods=["POST"])
def adauga():
    """Ruta pentru adăugarea unui pantof nou."""
    crud.adauga_produs(
        brand=request.form.get("brand"),
        model=request.form.get("model"),
        marime=int(request.form.get("marime")),
        pret=float(request.form.get("pret")),
        stoc=int(request.form.get("stoc"))
    )
    return redirect(url_for("index"))

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    """Ruta pentru actualizarea prețului."""
    pret_nou = float(request.form.get("pret_nou"))
    crud.actualizeaza_pret(id, pret_nou)
    return redirect(url_for("index"))

@app.route("/sterge/<int:id>")
def sterge(id):
    """Ruta pentru ștergerea unui produs."""
    crud.sterge_produs(id)
    return redirect(url_for("index"))

@app.route("/raport")
def raport():
    """Generare raport text pe baza datelor din stoc (1p - Generare Raport)."""
    session = SessionLocal()
    produse = session.query(Pantof).all()
    
    valoare_totala = sum(p.pret * p.stoc for p in produse)
    total_perechi = sum(p.stoc for p in produse)
    
    file_path = "raport_stoc_magazin.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("=== RAPORT INVENTAR / VALOARE STOC ===\n\n")
        f.write(f"Total modele unice in baza de date: {len(produse)}\n")
        f.write(f"Total perechi de incaltaminte fizice: {total_perechi} buc.\n")
        f.write(f"Valoarea totala estimata a stocului: {valoare_totala:.2f} RON\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'ID':<4} | {'Brand':<12} | {'Model':<15} | {'Marime':<6} | {'Pret':<10} | {'Stoc':<6}\n")
        f.write("-" * 50 + "\n")
        for p in produse:
            f.write(f"{p.id:<4} | {p.brand:<12} | {p.model:<15} | {p.marime:<6} | {p.pret:<10.2f} | {p.stoc:<6}\n")
            
    session.close()
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
   app.run(debug=True, port=8080)