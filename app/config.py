import os


class Config:
    def __init__(self):
        self.SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

        # Admin
        self.ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
        self.ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "change-me")

        # DB
        self.DB_PATH = os.path.join(os.getcwd(), "instance", "app.db")

        # Uploads (event images)
        self.EVENT_UPLOAD_DIR = os.path.join(
            os.getcwd(), "app", "static", "uploads", "events"
        )
        self.EVENT_UPLOAD_URL = "/static/uploads/events"

        # Site content (hardcoded basics)
        self.SITE_NAME = "HOGO 2.0"

        self.ADDRESS_LINE = "Eliščino nábř., 500 03 Hradec Králové 3"

        # Simple Google Maps embed without API key
        self.MAP_EMBED_SRC = (
            "https://www.google.com/maps?q=50.2104291,15.8288614&output=embed"
        )
        # Link to open maps (your share link)
        self.MAP_OPEN_LINK = "https://maps.app.goo.gl/SDNaNbDahyZxB9Xb9"

        self.INSTAGRAM_URL = "https://www.instagram.com/hogo2bar"

        # Opening hours (as tuples)
        self.OPENING_HOURS = [
            ("Pondělí", "16–23"),
            ("Úterý", "16–23"),
            ("Středa", "16–23"),
            ("Čtvrtek", "16–23"),
            ("Pátek", "16–1"),
            ("Sobota", "17–1"),
            ("Neděle", "16–22"),
        ]

        # Menu images (add more later)
        self.MENU_IMAGES = ["menu.jpg"]
