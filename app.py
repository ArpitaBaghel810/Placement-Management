from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector
import os
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'placement_secret_key_2024')

# ─── DB Connection ───────────────────────────────────────────────
def get_db():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'root@123'),
        database=os.environ.get('DB_NAME', 'placement_db')
    )

# ─── Login Required Decorator ────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated

# ─── Auth Routes ─────────────────────────────────────────────────
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        db.close()
        if user:
            session['user_id'] = user['id']
            session['name'] = user['name']
            session['role'] = user['role']
            session['email'] = user['email']
            return redirect(url_for('dashboard'))
        flash('Invalid credentials!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ─── Dashboard ───────────────────────────────────────────────────
@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM students")
    total_students = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM companies")
    total_companies = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM job_postings WHERE status='open'")
    open_jobs = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM applications WHERE status='selected'")
    placed = cursor.fetchone()['total']
    cursor.execute("""
        SELECT a.id, s.name as student_name, c.name as company_name, 
               j.title as job_title, a.status, a.applied_date
        FROM applications a
        JOIN students s ON a.student_id = s.id
        JOIN job_postings j ON a.job_id = j.id
        JOIN companies c ON j.company_id = c.id
        ORDER BY a.applied_date DESC LIMIT 5
    """)
    recent_apps = cursor.fetchall()
    db.close()
    return render_template('dashboard.html',
        total_students=total_students,
        total_companies=total_companies,
        open_jobs=open_jobs,
        placed=placed,
        recent_apps=recent_apps
    )

# ─── Students ────────────────────────────────────────────────────
@app.route('/students')
@login_required
def students():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students ORDER BY created_at DESC")
    students = cursor.fetchall()
    db.close()
    return render_template('students.html', students=students)

@app.route('/students/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_student():
    if request.method == 'POST':
        data = (
            request.form['name'], request.form['email'],
            request.form['phone'], request.form['branch'],
            request.form['year'], request.form['cgpa'],
            request.form['skills'], request.form.get('resume_link', '')
        )
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO students (name, email, phone, branch, year, cgpa, skills, resume_link)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, data)
        db.commit()
        db.close()
        flash('Student added successfully!', 'success')
        return redirect(url_for('students'))
    return render_template('student_form.html', student=None)

@app.route('/students/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_student(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        data = (
            request.form['name'], request.form['email'],
            request.form['phone'], request.form['branch'],
            request.form['year'], request.form['cgpa'],
            request.form['skills'], request.form.get('resume_link', ''), id
        )
        cursor.execute("""
            UPDATE students SET name=%s, email=%s, phone=%s, branch=%s,
            year=%s, cgpa=%s, skills=%s, resume_link=%s WHERE id=%s
        """, data)
        db.commit()
        db.close()
        flash('Student updated!', 'success')
        return redirect(url_for('students'))
    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cursor.fetchone()
    db.close()
    return render_template('student_form.html', student=student)

@app.route('/students/delete/<int:id>')
@login_required
@admin_required
def delete_student(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    db.commit()
    db.close()
    flash('Student deleted!', 'info')
    return redirect(url_for('students'))

# ─── Companies ───────────────────────────────────────────────────
@app.route('/companies')
@login_required
def companies():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM companies ORDER BY created_at DESC")
    companies = cursor.fetchall()
    db.close()
    return render_template('companies.html', companies=companies)

@app.route('/companies/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_company():
    if request.method == 'POST':
        data = (
            request.form['name'], request.form['industry'],
            request.form['website'], request.form['contact_person'],
            request.form['contact_email'], request.form['location']
        )
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO companies (name, industry, website, contact_person, contact_email, location)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, data)
        db.commit()
        db.close()
        flash('Company added!', 'success')
        return redirect(url_for('companies'))
    return render_template('company_form.html', company=None)

@app.route('/companies/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_company(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        data = (
            request.form['name'], request.form['industry'],
            request.form['website'], request.form['contact_person'],
            request.form['contact_email'], request.form['location'], id
        )
        cursor.execute("""
            UPDATE companies SET name=%s, industry=%s, website=%s,
            contact_person=%s, contact_email=%s, location=%s WHERE id=%s
        """, data)
        db.commit()
        db.close()
        flash('Company updated!', 'success')
        return redirect(url_for('companies'))
    cursor.execute("SELECT * FROM companies WHERE id=%s", (id,))
    company = cursor.fetchone()
    db.close()
    return render_template('company_form.html', company=company)

@app.route('/companies/delete/<int:id>')
@login_required
@admin_required
def delete_company(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM companies WHERE id=%s", (id,))
    db.commit()
    db.close()
    flash('Company deleted!', 'info')
    return redirect(url_for('companies'))

# ─── Job Postings ────────────────────────────────────────────────
@app.route('/jobs')
@login_required
def jobs():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT j.*, c.name as company_name FROM job_postings j
        JOIN companies c ON j.company_id = c.id
        ORDER BY j.created_at DESC
    """)
    jobs = cursor.fetchall()
    db.close()
    return render_template('jobs.html', jobs=jobs)

@app.route('/jobs/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_job():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM companies")
    companies = cursor.fetchall()
    if request.method == 'POST':
        data = (
            request.form['company_id'], request.form['title'],
            request.form['description'], request.form['requirements'],
            request.form['salary'], request.form['location'],
            request.form['deadline'], request.form['status']
        )
        cursor.execute("""
            INSERT INTO job_postings (company_id, title, description, requirements, salary, location, deadline, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, data)
        db.commit()
        db.close()
        flash('Job posted!', 'success')
        return redirect(url_for('jobs'))
    db.close()
    return render_template('job_form.html', job=None, companies=companies)

@app.route('/jobs/delete/<int:id>')
@login_required
@admin_required
def delete_job(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM job_postings WHERE id=%s", (id,))
    db.commit()
    db.close()
    flash('Job deleted!', 'info')
    return redirect(url_for('jobs'))

# ─── Applications ────────────────────────────────────────────────
@app.route('/applications')
@login_required
def applications():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.*, s.name as student_name, s.branch, s.cgpa,
               j.title as job_title, c.name as company_name
        FROM applications a
        JOIN students s ON a.student_id = s.id
        JOIN job_postings j ON a.job_id = j.id
        JOIN companies c ON j.company_id = c.id
        ORDER BY a.applied_date DESC
    """)
    apps = cursor.fetchall()
    db.close()
    return render_template('applications.html', apps=apps)

@app.route('/applications/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_application():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM students")
    students = cursor.fetchall()
    cursor.execute("SELECT j.id, j.title, c.name as company_name FROM job_postings j JOIN companies c ON j.company_id=c.id WHERE j.status='open'")
    jobs = cursor.fetchall()
    if request.method == 'POST':
        data = (request.form['student_id'], request.form['job_id'], 'applied')
        cursor.execute("INSERT INTO applications (student_id, job_id, status) VALUES (%s,%s,%s)", data)
        db.commit()
        db.close()
        flash('Application added!', 'success')
        return redirect(url_for('applications'))
    db.close()
    return render_template('application_form.html', students=students, jobs=jobs)

@app.route('/applications/update/<int:id>', methods=['POST'])
@login_required
@admin_required
def update_application(id):
    status = request.form['status']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE applications SET status=%s WHERE id=%s", (status, id))
    db.commit()
    db.close()
    flash('Status updated!', 'success')
    return redirect(url_for('applications'))

# ─── Users (Admin only) ──────────────────────────────────────────
@app.route('/users')
@login_required
@admin_required
def users():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, role, created_at FROM users")
    users = cursor.fetchall()
    db.close()
    return render_template('users.html', users=users)

@app.route('/users/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    if request.method == 'POST':
        data = (request.form['name'], request.form['email'], request.form['password'], request.form['role'])
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (name, email, password, role) VALUES (%s,%s,%s,%s)", data)
        db.commit()
        db.close()
        flash('User created!', 'success')
        return redirect(url_for('users'))
    return render_template('user_form.html')

if __name__ == '__main__':
    app.run(debug=True)
