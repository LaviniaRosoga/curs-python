# 👟 Magazin de Pantofi - Proiect Python

Acesta este un proiect pentru gestiunea stocurilor unui magazin de pantofi. Aplicația are o interfață web simplă unde se pot adăuga, modifica și șterge produse în timp real.

## 🚀 Tehnologii folosite
* **Limbaj**: Python 3.11
* **Server Web**: Flask
* **Bază de date**: SQLite și SQLAlchemy
* **Interfață**: HTML și CSS pur (fără framework-uri)

## 📋 Funcționalități
* **Adăugare produs** (Formular sus)
* **Vizualizare stoc** (Tabel cu produsele existente)
* **Modificare preț** (Butonul de actualizare din tabel)
* **Ștergere produs** (Butonul roșu de ștergere)
* **Sortări și Filtrări**: Sortare după Brand, sortare după Preț și filtrare după Mărimea 42.
* **Generare raport**: Descarcă automat un fișier text cu valoarea totală a stocului.

## 🛠️ Cum se rulează proiectul

1. Instalează bibliotecile din terminal:
   ```bash
   pip install flask sqlalchemy
   ```
2. Pornește aplicația în VS Code:
   ```bash
   python app_magazin.py
   ```
3. Deschide browserul și accesează adresa: **http://localhost:5000**
