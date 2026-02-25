# HOGO 2.0 – web + admin (Flask)

## Start
1) vytvoř v rootu `.env` podle `.env.example`
2) instalace:
   - python -m venv .venv
   - .venv\Scripts\activate  (Windows)
   - pip install -r requirements.txt
3) spusť:
   - python run.py
4) otevři:
   - http://127.0.0.1:5000
   - admin: http://127.0.0.1:5000/admin

## Obsah
- Hero foto: `app/static/img/hero.jpg`
- Menu: `app/static/menu/menu.jpg` (může být i více JPG)
- Galerie: vlož 6 fotek do `app/static/gallery/`
- Fotky akcí se ukládají do `app/static/uploads/events/`

## DB
SQLite se vytvoří automaticky do `instance/app.db`.
