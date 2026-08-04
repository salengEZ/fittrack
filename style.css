from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash, Response
import csv
import io

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required():
    return session.get("is_admin") is True


@admin_bp.before_request
def check_admin():
    if "member_id" not in session:
        return redirect(url_for("auth.login"))
    if not admin_required():
        flash("หน้านี้สำหรับผู้ดูแลระบบเท่านั้น")
        return redirect(url_for("dashboard"))


@admin_bp.route("/members")
def members():
    db = current_app.config["get_db"]()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT member_id, name, email, is_active, is_admin FROM member ORDER BY member_id")
    rows = cur.fetchall()
    cur.close(); db.close()
    return render_template("admin_members.html", members=rows)


@admin_bp.route("/members/<int:member_id>/toggle", methods=["POST"])
def toggle_member(member_id):
    db = current_app.config["get_db"]()
    cur = db.cursor()
    cur.execute("UPDATE member SET is_active = NOT is_active WHERE member_id = %s", (member_id,))
    db.commit()
    cur.close(); db.close()
    return redirect(url_for("admin.members"))


@admin_bp.route("/members/<int:member_id>/delete", methods=["POST"])
def delete_member(member_id):
    db = current_app.config["get_db"]()
    cur = db.cursor()
    cur.execute("DELETE FROM member WHERE member_id = %s", (member_id,))
    db.commit()
    cur.close(); db.close()
    return redirect(url_for("admin.members"))


@admin_bp.route("/exercise-types", methods=["GET", "POST"])
def exercise_types():
    db = current_app.config["get_db"]()
    cur = db.cursor()

    if request.method == "POST":
        name = request.form["exercise_name"].strip()
        calories = request.form["calories_per_hour"]
        if name and calories:
            cur.execute(
                "INSERT INTO exercise_type (exercise_name, calories_per_hour) VALUES (%s, %s)",
                (name, calories),
            )
            db.commit()

    cur2 = db.cursor(dictionary=True)
    cur2.execute("SELECT * FROM exercise_type ORDER BY exercise_id")
    rows = cur2.fetchall()
    cur.close(); cur2.close(); db.close()
    return render_template("admin_exercise_types.html", exercise_types=rows)


@admin_bp.route("/exercise-types/<int:exercise_id>/delete", methods=["POST"])
def delete_exercise_type(exercise_id):
    db = current_app.config["get_db"]()
    cur = db.cursor()
    cur.execute("DELETE FROM exercise_type WHERE exercise_id = %s", (exercise_id,))
    db.commit()
    cur.close(); db.close()
    return redirect(url_for("admin.exercise_types"))


@admin_bp.route("/reports")
def reports():
    db = current_app.config["get_db"]()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT COUNT(*) AS n FROM member")
    total_members = cur.fetchone()["n"]

    cur.execute("SELECT COUNT(*) AS n FROM workout_log")
    total_workouts = cur.fetchone()["n"]

    cur.execute(
        """SELECT COALESCE(SUM(w.duration_minutes / 60.0 * e.calories_per_hour), 0) AS total
           FROM workout_log w JOIN exercise_type e ON w.exercise_id = e.exercise_id"""
    )
    total_calories = round(cur.fetchone()["total"] or 0)

    cur.execute(
        """SELECT e.exercise_name, COUNT(*) AS times
           FROM workout_log w JOIN exercise_type e ON w.exercise_id = e.exercise_id
           GROUP BY e.exercise_name ORDER BY times DESC"""
    )
    by_exercise = cur.fetchall()
    cur.close(); db.close()

    return render_template(
        "admin_reports.html",
        total_members=total_members,
        total_workouts=total_workouts,
        total_calories=total_calories,
        by_exercise=by_exercise,
    )


@admin_bp.route("/reports/export.csv")
def export_reports_csv():
    db = current_app.config["get_db"]()
    cur = db.cursor(dictionary=True)
    cur.execute(
        """SELECT m.name, w.workout_date, e.exercise_name, w.duration_minutes
           FROM workout_log w
           JOIN member m ON w.member_id = m.member_id
           JOIN exercise_type e ON w.exercise_id = e.exercise_id
           ORDER BY w.workout_date DESC"""
    )
    rows = cur.fetchall()
    cur.close(); db.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ชื่อสมาชิก", "วันที่", "ประเภทกิจกรรม", "ระยะเวลา (นาที)"])
    for r in rows:
        writer.writerow([r["name"], r["workout_date"], r["exercise_name"], r["duration_minutes"]])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=fittrack_report.csv"},
    )
