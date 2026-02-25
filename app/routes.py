import os
from flask import Blueprint, current_app, render_template
from werkzeug.utils import secure_filename

from .models import list_public_events


bp = Blueprint("public", __name__)


def _list_gallery_images(limit=6):
    folder = os.path.join(os.getcwd(), "app", "static", "gallery")
    if not os.path.isdir(folder):
        return []
    files = [
        f for f in os.listdir(folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ]
    files.sort()  # 1.jpg..6.jpg
    return [f"/static/gallery/{f}" for f in files[:limit]]


def _list_menu_images():
    imgs = current_app.config.get("MENU_IMAGES", []) or []
    out = []
    for name in imgs:
        out.append(f"/static/menu/{name}")
    return out


def _save_event_image(file_storage):
    if not file_storage or not getattr(file_storage, "filename", ""):
        return None

    filename = secure_filename(file_storage.filename)
    if not filename:
        return None

    ext = os.path.splitext(filename)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        return None

    # unique name
    import time
    final_name = f"event_{int(time.time()*1000)}{ext}"
    dest = os.path.join(current_app.config["EVENT_UPLOAD_DIR"], final_name)
    file_storage.save(dest)
    return final_name


def _delete_event_image_if_exists(image_filename: str | None):
    if not image_filename:
        return
    path = os.path.join(current_app.config["EVENT_UPLOAD_DIR"], image_filename)
    if os.path.isfile(path):
        try:
            os.remove(path)
        except OSError:
            pass


@bp.get("/")
def index():
    events = list_public_events()
    gallery = _list_gallery_images(limit=6)
    menu_images = _list_menu_images()

    return render_template(
        "index.html",
        site_name=current_app.config["SITE_NAME"],
        address=current_app.config["ADDRESS_LINE"],
        opening_hours=current_app.config["OPENING_HOURS"],
        instagram_url=current_app.config["INSTAGRAM_URL"],
        map_embed_src=current_app.config["MAP_EMBED_SRC"],
        map_open_link=current_app.config["MAP_OPEN_LINK"],
        menu_images=menu_images,
        gallery=gallery,
        events=events,
        event_upload_url=current_app.config["EVENT_UPLOAD_URL"],
    )
