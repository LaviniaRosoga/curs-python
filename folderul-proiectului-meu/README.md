# 👟 Sistem de Gestiune Stoc Magazin Pantofi

Proiect final realizat în Python utilizând framework-ul Flask și ORM-ul SQLAlchemy.

## 🚀 Tehnologii Utilizate
* **Limbaj:** Python 3.x
* **Backend Framework:** Flask
* **Bază de date:** SQLite
* **ORM:** SQLAlchemy (pentru o mapare curată a obiectelor pe tabele)
* **Frontend:** HTML5 & CSS3 nativ cu template-uri Jinja2

## 🛠️ Mod de utilizare și instalare

1. Clonează acest repository:
   ```bash
   git clone <link_repo_github>
   cd <nume_folder>
   ```
2. Instalează dependențele necesare:
   ```bash
   pip install -r requirements.txt
   ```
3. Pornește aplicația locală:
   ```bash
   python app.py
   ```
4. Deschide în browser adresa: `http://127.0.0`

## 📊 Funcționalități implementate (Conform Barem)
* **CRUD Complet**: Adăugare, Vizualizare, Modificare preț rapidă, Ștergere produs (2p).
* **Separation of Concerns**: Cod împărțit în module clare (`database.py`, `crud.py`, `app.py`) (1p).
* **Filtrare și Sortare**: Sortare după brand, preț descrescător și filtrare rapidă după mărime (1p).
* **Generare Raport**: Descărcare fișier text automat cu statistici complete despre valoarea stocului (1p).
* **Documentare**: Docstrings prezente, type hinting complet și sistem de logging integrat (0.5p).