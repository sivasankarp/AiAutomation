"""
app.py - Main Flask application entry point
Production-ready Flask contact form application
"""

import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize extensions (no app bound yet)
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """Application factory pattern for better testability and flexibility."""
    app = Flask(__name__)

    # ── Configuration ────────────────────────────────────────────────────────
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-me-in-production")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:postgres@db:5432/contactdb",
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["WTF_CSRF_ENABLED"] = True

    # ── Logging ──────────────────────────────────────────────────────────────
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    app.logger.setLevel(logging.INFO)

    # ── Init extensions ──────────────────────────────────────────────────────
    db.init_app(app)
    migrate.init_app(app, db)

    # ── Register blueprints ──────────────────────────────────────────────────
    from routes import main_bp  # noqa: E402  (local import keeps factory clean)
    app.register_blueprint(main_bp)

    # ── Health-check route (used by Docker) ──────────────────────────────────
    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    app.logger.info("Flask application created successfully.")
    return app


# ── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    application = create_app()
    application.run(
        host="0.0.0.0",
        port=int(os.environ.get("FLASK_PORT", 5000)),
        debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true",
    )
