-- ============================================================
-- Placement Cell Management System - Database Schema
-- Run this file in MySQL to set up the database
-- ============================================================

CREATE DATABASE IF NOT EXISTS placement_db;
USE placement_db;

-- Users Table (Admin / Staff)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'staff') DEFAULT 'staff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Students Table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    branch VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    cgpa DECIMAL(4,2),
    skills TEXT,
    resume_link VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Companies Table
CREATE TABLE IF NOT EXISTS companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    industry VARCHAR(100),
    website VARCHAR(255),
    contact_person VARCHAR(100),
    contact_email VARCHAR(100),
    location VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Job Postings Table
CREATE TABLE IF NOT EXISTS job_postings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    requirements TEXT,
    salary VARCHAR(50),
    location VARCHAR(100),
    deadline DATE,
    status ENUM('open', 'closed') DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- Applications Table
CREATE TABLE IF NOT EXISTS applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    job_id INT NOT NULL,
    status ENUM('applied', 'shortlisted', 'interview', 'selected', 'rejected') DEFAULT 'applied',
    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES job_postings(id) ON DELETE CASCADE
);

-- ─── Sample Data ─────────────────────────────────────────────────

-- Default admin user (password: admin123)
INSERT INTO users (name, email, password, role) VALUES
('Admin User', 'admin@university.com', 'admin123', 'admin'),
('Staff Member', 'staff@university.com', 'staff123', 'staff');

-- Sample Companies
INSERT INTO companies (name, industry, website, contact_person, contact_email, location) VALUES
('TechCorp India', 'IT Services', 'https://techcorp.com', 'Ravi Sharma', 'ravi@techcorp.com', 'Bangalore'),
('Infosys', 'IT Consulting', 'https://infosys.com', 'Priya Mehta', 'priya@infosys.com', 'Pune'),
('Amazon India', 'E-Commerce', 'https://amazon.in', 'Ankit Joshi', 'ankit@amazon.com', 'Hyderabad'),
('Wipro', 'IT Services', 'https://wipro.com', 'Neha Singh', 'neha@wipro.com', 'Chennai'),
('Google India', 'Technology', 'https://google.com', 'Arjun Nair', 'arjun@google.com', 'Bangalore');

-- Sample Students
INSERT INTO students (name, email, phone, branch, year, cgpa, skills, resume_link) VALUES
('Rahul Kumar', 'rahul@student.com', '9876543210', 'Computer Science', 4, 8.5, 'Python, Java, MySQL, React', ''),
('Priya Patel', 'priya@student.com', '9876543211', 'Information Technology', 4, 9.1, 'JavaScript, Node.js, MongoDB', ''),
('Amit Singh', 'amit@student.com', '9876543212', 'Electronics', 3, 7.8, 'C++, Embedded Systems, Python', ''),
('Sneha Gupta', 'sneha@student.com', '9876543213', 'Computer Science', 4, 8.9, 'Machine Learning, Python, SQL', ''),
('Rohit Verma', 'rohit@student.com', '9876543214', 'Mechanical', 4, 7.5, 'AutoCAD, MATLAB, C', '');

-- Sample Job Postings
INSERT INTO job_postings (company_id, title, description, requirements, salary, location, deadline, status) VALUES
(1, 'Software Engineer', 'Develop and maintain web applications', 'Python, MySQL, 7+ CGPA', '6-8 LPA', 'Bangalore', '2025-06-30', 'open'),
(2, 'Systems Engineer', 'Work on enterprise software systems', 'Java, SQL, Communication skills', '4-6 LPA', 'Pune', '2025-07-15', 'open'),
(3, 'SDE-1', 'Build scalable backend services', 'DSA, Python or Java, 8+ CGPA', '12-15 LPA', 'Hyderabad', '2025-05-30', 'open'),
(4, 'Associate Software Engineer', 'Full stack development', 'Any programming language, SQL', '3.5-5 LPA', 'Chennai', '2025-08-01', 'open'),
(5, 'Associate Product Manager', 'Product development and strategy', 'Analytical skills, Communication, 8.5+ CGPA', '18-22 LPA', 'Bangalore', '2025-06-15', 'open');

-- Sample Applications
INSERT INTO applications (student_id, job_id, status) VALUES
(1, 1, 'shortlisted'),
(1, 3, 'applied'),
(2, 1, 'selected'),
(2, 5, 'interview'),
(3, 2, 'applied'),
(4, 3, 'shortlisted'),
(4, 5, 'applied'),
(5, 4, 'applied');
