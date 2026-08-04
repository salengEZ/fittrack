import os

# ใช้เครื่องตัวเอง (local): จะอ่านค่า DB_* จาก environment variable ถ้าตั้งไว้ ไม่งั้นใช้ localhost/root ว่างๆ
# ใช้บน Railway: จะอ่านค่า MYSQLHOST/MYSQLUSER/... ที่ Railway สร้างให้อัตโนมัติแทน
DB_CONFIG = {
    "host": os.environ.get("MYSQLHOST", os.environ.get("DB_HOST", "localhost")),
    "port": int(os.environ.get("MYSQLPORT", os.environ.get("DB_PORT", "3306"))),
    "user": os.environ.get("MYSQLUSER", os.environ.get("DB_USER", "root")),
    "password": os.environ.get("MYSQLPASSWORD", os.environ.get("DB_PASSWORD", "")),
    "database": os.environ.get("MYSQLDATABASE", os.environ.get("DB_NAME", "FitTrackDB")),
    "charset": "utf8mb4",
}

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-this")
