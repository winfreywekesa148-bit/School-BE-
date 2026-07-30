# 🎨 Lupine Art Academy School Management System

A full-stack School Management System developed for **Lupine Art Academy**. The application allows teachers and students to interact through a secure online platform.

Teachers can create lesson plans, assign coursework, and grade student submissions. Students can enroll in courses, submit assignments, view lesson plans, and track their grades.

---

# 📖 Table of Contents

- Project Overview
- Features
- Technologies Used
- Project Structure
- Database Design
- API Endpoints
- Installation
- Running the Application
- Authentication
- Deployment
- Future Improvements
- Contributors
- License

---

# 📚 Project Overview

This project is built using:

- React (Frontend)
- Flask (Backend)
- SQLite Database
- SQLAlchemy ORM
- Marshmallow
- JWT Authentication

The frontend communicates with the backend through RESTful API requests using JSON.

---

# ✨ Features

## Student Features

- Register an account
- Login securely
- Reset forgotten password
- View dashboard
- View lesson plans
- View assignments
- Submit assignments
- View grades

---

## Teacher Features

- Register account
- Login securely
- Create lesson plans
- View lesson plans
- Create assignments
- Grade assignments
- View submitted work

---

## Authentication

- JWT Login
- Protected Routes
- Role-Based Access
- Teacher Dashboard
- Student Dashboard
- Password Reset

---

# 🛠 Technologies Used

## Frontend

- React
- React Router
- JavaScript
- HTML5
- CSS3
- Fetch API

---

## Backend

- Flask
- Flask SQLAlchemy
- Flask JWT Extended
- Flask Marshmallow
- Flask Migrate
- Flask CORS

---

## Database

- SQLite

---

# 📂 Project Structure

```
School-Management-System
│
├── backend
│
│   ├── app.py
│   ├── run.py
│   ├── config.py
│   ├── extensions.py
│   ├── schema.py
│   ├── requirements.txt
│
│   ├── models
│   │
│   ├── routes
│   │
│   ├── utils
│   │
│   └── instance
│
└── frontend
    │
    └── react-app
        │
        ├── src
        │
        ├── Components
        │
        ├── Pages
        │
        ├── App.jsx
        ├── main.jsx
        └── package.json
```

---

# 🗄 Database Models

## User

- id
- username
- email
- password
- role

Relationship

One User

↓

Many Courses

---

## Course

- id
- course_name
- description
- teacher_id

Relationship

One Course

↓

Many Assignments

---

## Assignment

- id
- title
- description
- due_date
- course_id

Relationship

One Assignment

↓

Many Submissions

---

## Submission

- id
- assignment_id
- student_id
- file
- status

Relationship

One Submission

↓

One Grade

---

## Lesson Plan

- id
- topic
- objectives
- materials
- teacher_id

---

# 🔗 Relationships

Teacher

One Teacher

↓

Many Courses

---

Course

One Course

↓

Many Assignments

---

Assignment

One Assignment

↓

Many Student Submissions

---

Students

Many Students

↔

Many Courses

(Many-to-Many)

---

# 🌐 API Endpoints

## Authentication

POST /register

POST /login

---

## Students

GET /students

PUT /students/<id>

DELETE /students/<id>

---

## Courses

GET /courses

POST /courses

---

## Lesson Plans

POST /lesson-plans

DELETE /lesson-plans/<id>

---

## Assignments

GET /assignments

POST /assignments

---

## Grades

GET /grades

PUT /grades/<id>

---

# 🔐 Authentication

JWT Tokens are used for authentication.

Example

```
Authorization

Bearer <your_token>
```

Protected Endpoints

- Student Dashboard
- Teacher Dashboard
- Lesson Plans
- Assignments
- Grades

---

# ⚙ Installation

Clone the repository

```bash
https://github.com/winfreywekesa148-bit/School-BE-
```

Move into the project

```bash
cd school-management-system
```

---

## Backend Setup

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install packages

```bash
pip install -r requirements.txt
```

Run Flask

```bash
python run.py
```

Server runs on

```
http://127.0.0.1:5000
```

---

## Frontend Setup

Move into the React folder

```bash
cd frontend/react-app
```

Install packages

```bash
npm install
```

Run React

```bash
npm run dev
```

React runs on

```
http://localhost:5173
```

---

# 🔄 How React Connects to Flask

React sends requests using Fetch API.

Example

```javascript
fetch("http://127.0.0.1:5000/login")
```

Flask processes the request.

Flask returns JSON.

React updates the interface.

```
React

↓

Fetch Request

↓

Flask API

↓

SQLite Database

↓

JSON Response

↓

React Screen
```

---

# 🚀 Deployment

Frontend

Deploy using

- Vercel

Backend

Deploy using

- Render

Database

- SQLite (development)
- PostgreSQL (production recommended)

---

# 🔮 Future Improvements

- Email verification
- Student attendance
- Timetable management
- Online examinations
- Notifications
- Chat between teachers and students
- Admin dashboard
- Payment integration
- File uploads
- Report cards
- Certificates

---

# 👥 Contributors

- Winfrey
- Team Members

---

# 📄 License
MIT License

Copyright (c) 2026 Winkesa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


---


Designed for educational purposes at Lupine Art Academy.
