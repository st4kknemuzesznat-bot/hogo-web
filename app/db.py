import sqlite3
from flask import g, current_app


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_date TEXT NOT NULL,
  text TEXT NOT NULL,
  image_filename TEXT,
  published INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_events_published_created
ON events (published, created_at);
"""


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DB_PATH"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    @app.before_request
    def _ensure_db():
        db = get_db()
        db.executescript(SCHEMA_SQL)
        db.commit()

    app.teardown_appcontext(close_db)
