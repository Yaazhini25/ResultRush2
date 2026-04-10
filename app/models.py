import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = "students"

    reg_no = db.Column(db.String(20), primary_key=True)
    dob = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), nullable=False)


class Result(db.Model):
    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)
    reg_no = db.Column(db.String(20), db.ForeignKey("students.reg_no"))
    semester = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(10), nullable=False)
    marks = db.Column(db.Integer, nullable=False)


def init_db(app):
    """
    Initialize SQLite database inside /data/results.db
    Works for local, Docker, and Kubernetes.
    """
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    db_path = os.path.join(data_dir, "results.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()


def get_student(reg_no, dob):
    """
    Fetch student by register number + DOB
    """
    return Student.query.filter_by(
        reg_no=reg_no.strip(),
        dob=dob.strip()
    ).first()


def get_result(reg_no):
    """
    Fetch semester 4 results for a student
    """
    return Result.query.filter_by(
        reg_no=reg_no.strip(),
        semester=4
    ).all()