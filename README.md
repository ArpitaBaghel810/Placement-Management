#  Student Placement Management System

A complete **Placement & Recruitment Management System** built using **Flask**, **HTML**, **CSS**, and **JavaScript**.
This system helps manage **students, companies, job postings, and applications** in one centralized platform.

---

#  Project Members

1. Arpita Singh Bgahel+– RA2411030030048
2. Mahi Sirohi - Ra2411030030053

## 📁 Project Documents

| Sr | Description                    | Link      |
| -- | --------------                 | --------- |
| 1  | Project Code                   | [View](https://github.com/ArpitaBaghel810/Placement-Management) |
| 2  | Project Report                 | [View](https://github.com/ArpitaBaghel810/Placement-Management/blob/main/Student_Placement_Tracker_v2.docx) |
| 3  | Final PPT                      | [View](https://github.com/ArpitaBaghel810/Placement-Management/blob/main/DBMSPPT.pdf) |
| 4  | RA2411030030048_Certificate 1  | [View](https://github.com/ArpitaBaghel810/Placement-Management/blob/main/arpita%20course%20Certificate.png) |
| 5  | RA2411030030053_Certificate 2  | [View](https://github.com/ArpitaBaghel810/Placement-Management/blob/main/mahi%20course%20certificate.jpeg) |     
| 6  | RA2411030030048_CourseReport   | [View](https://github.com/ArpitaBaghel810/Placement-Management/blob/main/ARPITA_DBMS_COURSE_REPORT.pdf) |
| 7  | RA2411030030053_CourseReport   | [View](https://github.com/ArpitaBaghel810/Placement-Management/blob/main/Mahi%20DBMS%20COURSE%20REPORT%20(1).pdf) |



# 🚀 Features

| Module                      | Description                                             |
| --------------------------- | ------------------------------------------------------- |
| 🔐 **Authentication**       | Secure login system for users/admin                     |
| 🎓 **Students Management**  | Add, edit, view, and delete student records             |
| 🏢 **Companies Management** | Manage recruiter/company details                        |
| 💼 **Jobs Management**      | Post and manage available job opportunities             |
| 📄 **Applications**         | Students apply to jobs and track application status     |
| 👥 **User Management**      | Admin manages system users                              |
| 📊 **Dashboard**            | Overview of students, companies, jobs, and applications |

---

# 🛠️ Tech Stack

* **Backend:** Python Flask
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQL (via `schema.sql`)
* **Templates:** Jinja2
* **Deployment:** Vercel (configured using `vercel.json`)

---

# ⚙️ Quick Setup

## 1️⃣ Prerequisites

Make sure you have installed:

* Python **3.8+**
* pip (Python package manager)

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Setup Database

Run the SQL script to create database tables:

```bash
sqlite3 database.db < schema.sql
```

*(Or import into MySQL if using MySQL.)*

---

## 4️⃣ Run the Application

```bash
python app.py
```

Open in browser:

```
http://localhost:5000
```

---

# 🔑 System Modules Overview

## 🎓 Students

* Add new student records
* Update student details
* View student list
* Delete student entries

Files:

```
templates/student_form.html
templates/students.html
```

---

## 🏢 Companies

* Add recruiter/company details
* Manage company information
* View company list

Files:

```
templates/company_form.html
templates/companies.html
```

---

## 💼 Jobs

* Post job openings
* Edit job details
* View job listings

Files:

```
templates/job_form.html
templates/jobs.html
```

---

## 📄 Applications

* Students apply for jobs
* Track application status
* View application records

Files:

```
templates/application_form.html
templates/applications.html
```

---

## 👥 Users

* Manage system users
* Create new users
* Update user details

Files:

```
templates/user_form.html
templates/users.html
```

---

## 📊 Dashboard

Provides overview of:

* Total Students
* Total Companies
* Total Jobs
* Total Applications

File:

```
templates/dashboard.html
```

---

# 📂 Project Structure

```
project-folder/
│
├── app.py                    # Main Flask application
├── schema.sql               # Database structure
├── requirements.txt         # Python dependencies
├── vercel.json              # Deployment configuration
├── README.md                # Project documentation
│
├── static/
│   ├── css/
│   │   └── style.css        # Styling file
│   └── js/
│       └── main.js          # JavaScript functionality
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── students.html
│   ├── student_form.html
│   ├── companies.html
│   ├── company_form.html
│   ├── jobs.html
│   ├── job_form.html
│   ├── applications.html
│   ├── application_form.html
│   ├── users.html
│   └── user_form.html
```

---

# 🔒 Authentication

Users must log in before accessing the dashboard and modules.

File:

```
templates/login.html
```

---

# 🌐 Deployment

This project supports deployment using:

* **Vercel**
* **Flask backend**

Deployment configuration file:

```
vercel.json
```

---

# 📸 Screenshots *(Optional)*

You can add screenshots here:

```
Dashboard Screenshot  
Students Page Screenshot  
Jobs Page Screenshot  
```

---

# 📌 Future Enhancements

* Email Notifications
* Resume Upload Feature
* Interview Scheduling
* Role-Based Access Control
* Analytics Dashboard

