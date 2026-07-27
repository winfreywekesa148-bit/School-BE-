CREATE TABLE students (
    student_id INT PRIMARY KEY,
    studentfirst_name TEXT NOT NULL,
    studentlast_name TEXT NOT NULL,
    course TEXT,
    course_id INT,
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE mentors (
    mentor_id INT PRIMARY KEY,
    mentorfirst_name TEXT,
    mentorlast_name TEXT,
    course TEXT,
    course_id INT,
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE admins (
    admin_id INT PRIMARY KEY,
    adminfirst_name TEXT,
    adminlast_name TEXT,
    email VARCHAR,
    department TEXT
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name TEXT,
    duration TIME,
    mentor_name TEXT,
    department TEXT
);