from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
from datetime import date

workout_bp = Blueprint("workout", __name__)


@workout_bp.route("/workout/add", methods=["GET", "POST"])
def add_workout():
    if "member_id" not in session:
        return redirect(url_for("auth.login"))

    db = current_app.config["get_db"]()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT exercise_id, exercise_name FROM exercise_type ORDER BY exercise_name")
    exercise_types = cur.fetchall()

    if request.method == "POST":
        exercise_id = request.form["exercise_id"]
        workout_date = request.form["workout_date"]
        duration_minutes = request.form["duration_minutes"]

        errors = []
        if workout_date > str(date.today()):
            errors.append("วันที่ห้ามเป็นอนาคต")
        try:
            if int(duration_minutes) <= 0:
                errors.append("ระยะเวลาต้องมากกว่า 0 นาที")
        except ValueError:
            errors.append("ระยะเวลาไม่ถูกต้อง")

        if errors:
            for e in errors:
                flash(e)
            cur.close()
            db.close()
            return render_template("add_workout.html", exercise_types=exercise_types)

        cur2 = db.cursor()
        cur2.execute(
            """INSERT INTO workout_log (member_id, exercise_id, workout_date, duration_minutes)
               VALUES (%s, %s, %s, %s)""",
            (session["member_id"], exercise_id, workout_date, duration_minutes),
        )
        db.commit()
        cur2.close()
        cur.close()
        db.close()
        return redirect(url_for("dashboard"))

    cur.close()
    db.close()
    return render_template("add_workout.html", exercise_types=exercise_types)


@workout_bp.route("/workout/<int:workout_id>/edit", methods=["GET", "POST"])
def edit_workout(workout_id):
    if "member_id" not in session:
        return redirect(url_for("auth.login"))

    db = current_app.config["get_db"]()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM workout_log WHERE workout_id = %s AND member_id = %s",
        (workout_id, session["member_id"]),
    )
    record = cur.fetchone()
    if not record:
        cur.close(); db.close()
        flash("ไม่พบข้อมูล")
        return redirect(url_for("health.history"))

    cur.execute("SELECT exercise_id, exercise_name FROM exercise_type ORDER BY exercise_name")
    exercise_types = cur.fetchall()

    if request.method == "POST":
        exercise_id = request.form["exercise_id"]
        workout_date = request.form["workout_date"]
        duration_minutes = request.form["duration_minutes"]

        errors = []
        if workout_date > str(date.today()):
            errors.append("วันที่ห้ามเป็นอนาคต")
        try:
            if int(duration_minutes) <= 0:
                errors.append("ระยะเวลาต้องมากกว่า 0 นาที")
        except ValueError:
            errors.append("ระยะเวลาไม่ถูกต้อง")

        if errors:
            for e in errors:
                flash(e)
            cur.close(); db.close()
            return render_template("edit_workout.html", record=record, exercise_types=exercise_types)

        cur2 = db.cursor()
        cur2.execute(
            """UPDATE workout_log SET exercise_id=%s, workout_date=%s, duration_minutes=%s
               WHERE workout_id=%s AND member_id=%s""",
            (exercise_id, workout_date, duration_minutes, workout_id, session["member_id"]),
        )
        db.commit()
        cur2.close(); cur.close(); db.close()
        return redirect(url_for("health.history"))

    cur.close(); db.close()
    return render_template("edit_workout.html", record=record, exercise_types=exercise_types)


@workout_bp.route("/workout/<int:workout_id>/delete", methods=["POST"])
def delete_workout(workout_id):
    if "member_id" not in session:
        return redirect(url_for("auth.login"))
    db = current_app.config["get_db"]()
    cur = db.cursor()
    cur.execute(
        "DELETE FROM workout_log WHERE workout_id = %s AND member_id = %s",
        (workout_id, session["member_id"]),
    )
    db.commit()
    cur.close(); db.close()
    return redirect(url_for("health.history"))
