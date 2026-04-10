from flask import Blueprint, render_template, request
from .models import get_student, get_result
import time
import random
import os

routes = Blueprint("routes", __name__)


def simulate_delay():
    base_delay = 0.5

    # Simulate overload in before-DevOps case
    if os.getenv("HIGH_LOAD_SIM", "false").lower() == "true":
        base_delay += 5

    time.sleep(base_delay + random.uniform(0, 0.6))


@routes.route("/", methods=["GET"])
def login_page():
    return render_template("login.html")


@routes.route("/view-result", methods=["POST"])
def view_result():
    reg_no = request.form.get("reg_no", "").strip()
    dob = request.form.get("dob", "").strip()

    simulate_delay()

    student = get_student(reg_no, dob)

    if not student:
        return render_template(
            "login.html",
            error="Invalid Register Number or Date of Birth"
        )

    raw_results = get_result(reg_no)

    if not raw_results:
        return render_template(
            "login.html",
            error="No results found"
        )

    # Convert SQLAlchemy objects → tuple format for existing HTML
    results = [
        (r.subject, r.grade, r.marks)
        for r in raw_results
    ]

    response_time = round((time.time() - request.start_time) * 1000, 2)

    return render_template(
        "result.html",
        name=student.name,
        reg_no=student.reg_no,
        results=results,
        response_time=response_time
    )