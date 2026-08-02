from flask import Flask, render_template, session, redirect, url_for
import mysql.connector
from config import DB_CONFIG, SECRET_KEY

from routes.auth import auth_bp
from routes.health import health_bp
from routes.workout import workout_bp
from routes.admin import admin_bp


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.config["get_db"] = get_db

    app.register_blueprint(auth_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(workout_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_user():
        return {"is_admin": session.get("is_admin", False)}

    @app.route("/")
    def dashboard():
        if "member_id" not in session:
            return redirect(url_for("auth.login"))

        db = get_db()
        cur = db.cursor(dictionary=True)

        cur.execute(
            "SELECT name, height_cm FROM member WHERE member_id = %s",
            (session["member_id"],),
        )
        member = cur.fetchone()

        cur.execute(
            """SELECT weight_kg, body_fat_percent, record_date
               FROM health_record WHERE member_id = %s
               ORDER BY record_date DESC LIMIT 1""",
            (session["member_id"],),
        )
        latest = cur.fetchone()

        bmi = None
        if latest and member["height_cm"]:
            h = float(member["height_cm"]) / 100
            bmi = round(float(latest["weight_kg"]) / (h * h), 1)

        cur.execute(
            """SELECT record_date, weight_kg, body_fat_percent
               FROM health_record WHERE member_id = %s
               ORDER BY record_date DESC LIMIT 10""",
            (session["member_id"],),
        )
        history = cur.fetchall()

        cur.execute(
            """SELECT w.workout_date, w.duration_minutes, e.exercise_name, e.calories_per_hour
               FROM workout_log w JOIN exercise_type e ON w.exercise_id = e.exercise_id
               WHERE w.member_id = %s ORDER BY w.workout_date DESC LIMIT 5""",
            (session["member_id"],),
        )
        workouts = cur.fetchall()

        cur.close()
        db.close()

        return render_template(
            "dashboard.html",
            member=member,
            bmi=bmi,
            latest=latest,
            history=history,
            workouts=workouts,
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
