from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        gender = request.form.get("gender") or None
        birth_date = request.form.get("birth_date") or None
        height_cm = request.form.get("height_cm") or None

        if not name or not email or not password:
            flash("กรอกชื่อ อีเมล และรหัสผ่านให้ครบ")
            return render_template("register.html")

        db = current_app.config["get_db"]()
        cur = db.cursor()
        cur.execute("SELECT member_id FROM member WHERE email = %s", (email,))
        if cur.fetchone():
            flash("อีเมลนี้ถูกใช้ไปแล้ว")
            cur.close()
            db.close()
            return render_template("register.html")

        password_hash = generate_password_hash(password)
        cur.execute(
            """INSERT INTO member (name, email, password_hash, gender, birth_date, height_cm)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (name, email, password_hash, gender, birth_date, height_cm),
        )
        db.commit()
        member_id = cur.lastrowid
        cur.close()
        db.close()

        session["member_id"] = member_id
        return redirect(url_for("dashboard"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        db = current_app.config["get_db"]()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM member WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        db.close()

        if user and check_password_hash(user["password_hash"], password):
            if not user["is_active"]:
                flash("บัญชีนี้ถูกระงับการใช้งาน")
                return render_template("login.html")
            session["member_id"] = user["member_id"]
            session["member_name"] = user["name"]
            session["is_admin"] = bool(user["is_admin"])
            return redirect(url_for("dashboard"))

        flash("อีเมลหรือรหัสผ่านไม่ถูกต้อง")
        return render_template("login.html")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
