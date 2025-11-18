-- Database Setup Script for Simple CRUD Backend
-- Run this script in your PostgreSQL database

-- Create database (run this separately if needed)
-- CREATE DATABASE smart_attendance;

-- Connect to the database and create tables
\c smart_attendance;

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS teachers CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'teacher', 'student')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create Students table
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create Teachers table
CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_students_student_id ON students(student_id);
CREATE INDEX idx_students_email ON students(email);
CREATE INDEX idx_students_department ON students(department);
CREATE INDEX idx_teachers_email ON teachers(email);
CREATE INDEX idx_teachers_department ON teachers(department);

-- Insert sample data with Indian names

-- Sample Admin User (password: admin123)
INSERT INTO users (name, email, password_hash, role) VALUES 
('Rajesh Kumar', 'admin@college.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeRb0QtJHQDdwsIva', 'admin');

-- Sample Teachers
INSERT INTO teachers (name, email, department) VALUES
('Dr. Priya Sharma', 'priya.sharma@college.edu', 'Computer Science'),
('Prof. Vikram Gupta', 'vikram.gupta@college.edu', 'Mathematics'),
('Dr. Kavita Patel', 'kavita.patel@college.edu', 'Physics'),
('Prof. Arjun Singh', 'arjun.singh@college.edu', 'Chemistry'),
('Dr. Meera Reddy', 'meera.reddy@college.edu', 'Electronics');

-- Sample Students
INSERT INTO students (student_id, name, email, department) VALUES
('CS001', 'Aarav Agarwal', 'aarav.agarwal@student.edu', 'Computer Science'),
('CS002', 'Diya Mehta', 'diya.mehta@student.edu', 'Computer Science'),
('CS003', 'Ishaan Joshi', 'ishaan.joshi@student.edu', 'Computer Science'),
('MT001', 'Ananya Iyer', 'ananya.iyer@student.edu', 'Mathematics'),
('MT002', 'Rohan Kapoor', 'rohan.kapoor@student.edu', 'Mathematics'),
('PH001', 'Sanya Nair', 'sanya.nair@student.edu', 'Physics'),
('PH002', 'Vihaan Shah', 'vihaan.shah@student.edu', 'Physics'),
('CH001', 'Kiara Bansal', 'kiara.bansal@student.edu', 'Chemistry'),
('CH002', 'Aryan Verma', 'aryan.verma@student.edu', 'Chemistry'),
('EC001', 'Myra Ghosh', 'myra.ghosh@student.edu', 'Electronics');

-- Sample Teacher Users (password: teacher123)
INSERT INTO users (name, email, password_hash, role) VALUES 
('Dr. Priya Sharma', 'priya.sharma@college.edu', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'teacher'),
('Prof. Vikram Gupta', 'vikram.gupta@college.edu', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'teacher'),
('Dr. Kavita Patel', 'kavita.patel@college.edu', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'teacher'),
('Prof. Arjun Singh', 'arjun.singh@college.edu', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'teacher'),
('Dr. Meera Reddy', 'meera.reddy@college.edu', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'teacher');

-- Sample Student Users (password: student123)
INSERT INTO users (name, email, password_hash, role) VALUES 
('Aarav Agarwal', 'aarav.agarwal@student.edu', '$2b$12$8n0FrLYjlC7zTJZJQ7VzVOWW.K9bGh.hXX0TRg7/YjwJhXw7wYU8a', 'student'),
('Diya Mehta', 'diya.mehta@student.edu', '$2b$12$8n0FrLYjlC7zTJZJQ7VzVOWW.K9bGh.hXX0TRg7/YjwJhXw7wYU8a', 'student'),
('Ishaan Joshi', 'ishaan.joshi@student.edu', '$2b$12$8n0FrLYjlC7zTJZJQ7VzVOWW.K9bGh.hXX0TRg7/YjwJhXw7wYU8a', 'student'),
('Ananya Iyer', 'ananya.iyer@student.edu', '$2b$12$8n0FrLYjlC7zTJZJQ7VzVOWW.K9bGh.hXX0TRg7/YjwJhXw7wYU8a', 'student'),
('Rohan Kapoor', 'rohan.kapoor@student.edu', '$2b$12$8n0FrLYjlC7zTJZJQ7VzVOWW.K9bGh.hXX0TRg7/YjwJhXw7wYU8a', 'student');

-- Display sample data
SELECT 'Users created:' as status;
SELECT id, name, email, role FROM users;

SELECT 'Teachers created:' as status;
SELECT id, name, email, department FROM teachers;

SELECT 'Students created:' as status;
SELECT id, student_id, name, email, department FROM students;

-- Grant permissions (adjust as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_app_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO your_app_user;

COMMIT;