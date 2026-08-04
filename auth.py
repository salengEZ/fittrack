CREATE DATABASE IF NOT EXISTS FitTrackDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE FitTrackDB;

CREATE TABLE member (
  member_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  gender CHAR(1),
  birth_date DATE,
  height_cm DECIMAL(5,2),
  is_admin TINYINT(1) NOT NULL DEFAULT 0,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (member_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE health_record (
  record_id INT NOT NULL AUTO_INCREMENT,
  member_id INT NOT NULL,
  record_date DATE NOT NULL,
  weight_kg DECIMAL(5,2) NOT NULL,
  body_fat_percent DECIMAL(4,1),
  PRIMARY KEY (record_id),
  FOREIGN KEY (member_id) REFERENCES member(member_id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE exercise_type (
  exercise_id INT NOT NULL AUTO_INCREMENT,
  exercise_name VARCHAR(50) NOT NULL,
  calories_per_hour INT NOT NULL,
  PRIMARY KEY (exercise_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE workout_log (
  workout_id INT NOT NULL AUTO_INCREMENT,
  member_id INT NOT NULL,
  exercise_id INT NOT NULL,
  workout_date DATE NOT NULL,
  duration_minutes INT NOT NULL,
  PRIMARY KEY (workout_id),
  FOREIGN KEY (member_id) REFERENCES member(member_id) ON DELETE CASCADE,
  FOREIGN KEY (exercise_id) REFERENCES exercise_type(exercise_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- seed data for exercise types
INSERT INTO exercise_type (exercise_name, calories_per_hour) VALUES
  ('วิ่ง', 600),
  ('ปั่นจักรยาน', 500),
  ('ว่ายน้ำ', 550),
  ('เดินเร็ว', 300),
  ('โยคะ', 200);

-- หลังสมัครสมาชิกคนแรกผ่านเว็บแล้ว ให้รันคำสั่งนี้เพื่อตั้งให้เป็น admin
-- UPDATE member SET is_admin = 1 WHERE email = 'your-email@example.com';
