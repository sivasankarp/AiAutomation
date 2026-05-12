"""
routes.py - Flask URL routes / views
"""

import logging
from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from models import ContactSubmission
from forms import ContactForm

logger = logging.getLogger(__name__)

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def index():
    """Render the contact form (GET) and process submissions (POST)."""
    form = ContactForm()

    if form.validate_on_submit():
        try:
            # Build model instance from validated form data
            submission = ContactSubmission(
                name=form.name.data.strip(),
                email=form.email.data.strip().lower(),
                phone=form.phone.data.strip(),
                message=form.message.data.strip(),
                ip_address=request.remote_addr,
            )
            db.session.add(submission)
            db.session.commit()

            logger.info(
                "New submission saved: id=%s email=%s ip=%s",
                submission.id,
                submission.email,
                submission.ip_address,
            )

            flash(
                "✅ Thank you! Your message has been received. We will get back to you soon.",
                "success",
            )
            return redirect(url_for("main.index"))

        except Exception as exc:
            db.session.rollback()
            logger.exception("Failed to save submission: %s", exc)
            flash(
                "❌ An unexpected error occurred. Please try again later.",
                "danger",
            )

    elif request.method == "POST":
        # Form was submitted but failed validation — errors shown in template
        logger.warning(
            "Form validation failed from ip=%s errors=%s",
            request.remote_addr,
            form.errors,
        )

    return render_template("index.html", form=form)


@main_bp.route("/submissions")
def submissions():
    """Simple admin view listing all saved submissions (latest first)."""
    all_submissions = (
        ContactSubmission.query.order_by(ContactSubmission.submitted_at.desc()).all()
    )
    return render_template("submissions.html", submissions=all_submissions)
