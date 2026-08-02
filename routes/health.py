from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
from datetime import date

health_bp = Blueprint("health", __name__)


def login_required():
    return "member_id" in session


@health_bp.route("/health/add", methods=["GET", "POST"])
def add_health():
    if not login_required():
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        record_date = request.form["record_date"]
        weight_kg = request.form["weight_kg"]
        body_fat_percent = request.form.get("body_fat_percent") or None

        errors = []
        if record_date > str(date.today()):
            errors.append("วันที่ห้ามเป็นอนาคต")
        try:
            if float(weight_kg) <= 0:
                errors.append("น้ำหนักต้องมากกว่า 0")
        except ValueError:
            errors.append("น้ำหนักไม่ถูกต้อง")

        if errors:
            for e in errors:
                flash(e)
            return render_template("add_health.html")

        db = current_app.config["get_db"]()
        cur = db.cursor()
        cur.execute(
            """INSERT INTO health_record (member_id, record_date, weight_kg, body_fat_percent)
               VALUES (%s, %s, %s, %s)""",
            (session["member_id"], record_date, weight_kg, body_fat_percent),
        )
        db.commit()
        cur.close()
        db.close()
        return redirect(url_for("dashboard"))

    return render_template("add_health.html")


@health_bp.route("/health/<int:record_id>/edit", methods=["GET", "POST"])
def edit_health(record_id):
    if not login_required():
        return redirect(url_for("auth.login"))

    db = current_app.config["get_db"]()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM health_record WHERE record_id = %s AND member_id = %s",
        (record_id, session["member_id"]),
    )
    record = cur.fetchone()
    if not record:
        cur.close(); db.close()
        flash("ไม่พบข้อมูล")
        return redirect(url_for("health.history"))

    if request.method == "POST":
        record_date = request.form["record_date"]
        weight_kg = request.form["weight_kg"]
        body_fat_percent = request.form.get("body_fat_percent") or None

        errors = []
        if record_date > str(date.today()):
            errors.append("วันที่ห้ามเป็นอนาคต")
        try:
            if float(weight_kg) <= 0:
                errors.append("น้ำหนักต้องมากกว่า 0")
        except ValueError:
            errors.append("น้ำหนักไม่ถูกต้อง")

        if errors:
            for e in errors:
                flash(e)
            cur.close(); db.close()
            return render_template("edit_health.html", record=record)

        cur2 = db.cursor()
        cur2.execute(
            """UPDATE health_record SET record_date=%s, weight_kg=%s, body_fat_percent=%s
               WHERE record_id=%s AND member_id=%s""",
            (record_date, weight_kg, body_fat_percent, record_id, session["member_id"]),
        )
        db.commit()
        cur2.close(); cur.close(); db.close()
        return redirect(url_for("health.history"))

    cur.close(); db.close()
    return render_template("edit_health.html", record=record)


@health_bp.route("/health/<int:record_id>/delete", methods=["POST"])
def delete_health(record_id):
    if not login_required():
        return redirect(url_for("auth.login"))
    db = current_app.config["get_db"]()
    cur = db.cursor()
    cur.execute(
        "DELETE FROM health_record WHERE record_id = %s AND member_id = %s",
        (record_id, session["member_id"]),
    )
    db.commit()
    cur.close(); db.close()
    return redirect(url_for("health.history"))


@health_bp.route("/history")
def history():
    if not login_required():
        return redirect(url_for("auth.login"))

    db = current_app.config["get_db"]()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM health_record WHERE member_id = %s ORDER BY record_date DESC",
        (session["member_id"],),
    )
    health_records = cur.fetchall()

    cur.execute(
        """SELECT w.workout_id, w.workout_date, w.duration_minutes, e.exercise_name, e.calories_per_hour
           FROM workout_log w JOIN exercise_type e ON w.exercise_id = e.exercise_id
           WHERE w.member_id = %s ORDER BY w.workout_date DESC""",
        (session["member_id"],),
    )
    workouts = cur.fetchall()
    cur.close(); db.close()

    return render_template("history.html", health_records=health_records, workouts=workouts)
