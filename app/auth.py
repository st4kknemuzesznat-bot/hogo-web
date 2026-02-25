import os
from functools import wraps
from flask import Blueprint, current_app, render_template, request, redirect, url_for, session, flash

from werkzeug.security import safe_join

from .models import (
    list_all_events,
    get_event,
    create_event,
    update_event,
    delete_event,
    set_published,
)
from .routes import _save_event_image, _delete_event_image_if_exists


bp = Blueprint("admin", __name__)


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin.login"))
        return fn(*args, **kwargs)
    return wrapper


@bp.get("/admin")
def admin_root():
    if session.get("is_admin"):
        return redirect(url_for("admin.events_list"))
    return redirect(url_for("admin.login"))


@bp.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = (request.form.get("password") or "").strip()

        if username == current_app.config["ADMIN_USERNAME"] and password == current_app.config["ADMIN_PASSWORD"]:
            session["is_admin"] = True
            return redirect(url_for("admin.events_list"))

        flash("Špatné přihlašovací údaje.", "error")

    return render_template("admin/login.html")


@bp.post("/admin/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("admin.login"))


@bp.get("/admin/events")
@login_required
def events_list():
    events = list_all_events()
    return render_template("admin/events_list.html", events=events)


@bp.route("/admin/events/new", methods=["GET", "POST"])
@login_required
def events_new():
    if request.method == "POST":
        event_date = (request.form.get("event_date") or "").strip()
        text = (request.form.get("text") or "").strip()

        if not event_date or not text:
            flash("Vyplň datum a text.", "error")
            return render_template("admin/event_form.html", mode="new", event=None)

        image_filename = _save_event_image(request.files.get("image"))
        create_event(event_date, text, image_filename)

        flash("Akce vytvořena.", "ok")
        return redirect(url_for("admin.events_list"))

    return render_template("admin/event_form.html", mode="new", event=None)


@bp.route("/admin/events/<int:event_id>/edit", methods=["GET", "POST"])
@login_required
def events_edit(event_id):
    event = get_event(event_id)
    if not event:
        flash("Akce nenalezena.", "error")
        return redirect(url_for("admin.events_list"))

    if request.method == "POST":
        event_date = (request.form.get("event_date") or "").strip()
        text = (request.form.get("text") or "").strip()

        if not event_date or not text:
            flash("Vyplň datum a text.", "error")
            return render_template("admin/event_form.html", mode="edit", event=event)

        new_image = request.files.get("image")
        image_filename = None
        if new_image and new_image.filename:
            # delete old
            _delete_event_image_if_exists(event["image_filename"])
            image_filename = _save_event_image(new_image)

        update_event(event_id, event_date, text, image_filename)
        flash("Uloženo.", "ok")
        return redirect(url_for("admin.events_list"))

    return render_template("admin/event_form.html", mode="edit", event=event)


@bp.post("/admin/events/<int:event_id>/delete")
@login_required
def events_delete(event_id):
    event = get_event(event_id)
    if event:
        _delete_event_image_if_exists(event["image_filename"])
        delete_event(event_id)
        flash("Smazáno.", "ok")
    return redirect(url_for("admin.events_list"))


@bp.post("/admin/events/<int:event_id>/toggle")
@login_required
def events_toggle(event_id):
    event = get_event(event_id)
    if event:
        set_published(event_id, not bool(event["published"]))
        flash("Stav publikace změněn.", "ok")
    return redirect(url_for("admin.events_list"))
