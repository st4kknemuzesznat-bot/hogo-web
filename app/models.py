from .db import get_db


def list_public_events():
    db = get_db()
    rows = db.execute(
        """
        SELECT id, event_date, text, image_filename, created_at
        FROM events
        WHERE published = 1
        ORDER BY datetime(created_at) DESC
        """
    ).fetchall()
    return rows


def list_all_events():
    db = get_db()
    rows = db.execute(
        """
        SELECT id, event_date, text, image_filename, published, created_at
        FROM events
        ORDER BY datetime(created_at) DESC
        """
    ).fetchall()
    return rows


def get_event(event_id: int):
    db = get_db()
    row = db.execute(
        "SELECT id, event_date, text, image_filename, published, created_at FROM events WHERE id = ?",
        (event_id,),
    ).fetchone()
    return row


def create_event(event_date: str, text: str, image_filename: str | None):
    db = get_db()
    db.execute(
        "INSERT INTO events (event_date, text, image_filename) VALUES (?, ?, ?)",
        (event_date, text, image_filename),
    )
    db.commit()


def update_event(event_id: int, event_date: str, text: str, image_filename: str | None):
    db = get_db()
    db.execute(
        """
        UPDATE events
        SET event_date = ?, text = ?, image_filename = COALESCE(?, image_filename)
        WHERE id = ?
        """,
        (event_date, text, image_filename, event_id),
    )
    db.commit()


def delete_event(event_id: int):
    db = get_db()
    db.execute("DELETE FROM events WHERE id = ?", (event_id,))
    db.commit()


def set_published(event_id: int, published: bool):
    db = get_db()
    db.execute("UPDATE events SET published = ? WHERE id = ?", (1 if published else 0, event_id))
    db.commit()
