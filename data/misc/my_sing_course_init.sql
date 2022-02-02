-- Edward Prah - Portfolio Project - SQL
-- To Execute in VS code: $ cat my_sing_course.sql | docker exec -i pg_container psql -d my_sing_course
-- FOR DOCKER VERSION: To Execute in VS code: $ cat data/misc/my_sing_course_init.sql | docker exec -i pg_container2 psql -U postgres -d my_sing_course
-- Generate SQL File - docker exec pg_container pg_dump my_sing_course > my_sing_course_pg_dump.sql
-- Create Tables for my_sing_course Database
-- students Has (a) user_accounts - One to One Relationship

-- If Database exist with same name drop and the recreate. If not just create new database.
-- kill other connections
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'my_sing_course' AND pid <> pg_backend_pid();
-- Disconnect from database
\c postgres
-- Example of adding Role to database:
--CREATE ROLE postgres with PASSWORD '$(DB_PASSWORD)';
--\password postgres
-- (re)create the database
DROP DATABASE IF EXISTS my_sing_course WITH (FORCE);
CREATE DATABASE my_sing_course;
-- connect via psql
\c my_sing_course

-- database configuration
SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    age SMALLINT
);


CREATE TABLE user_accounts (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    student_id INT
);

-- students Enrolled in courses - Many to Many relationship (Create bridge table)
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    level TEXT
);
-- courses Have exercises -  Many to Many relationship (Create bridge table)
CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- progress Have exercises - One to Many relationship (foreign key references the many table - exercises)
CREATE TABLE progress (
    id SERIAL PRIMARY KEY,
    entry_date TIMESTAMPTZ,
    timbre TEXT,
    tone TEXT,
    melodic_phrasing TEXT,
    dynamics TEXT,
    range TEXT,
    feedback TEXT,
    exercise_id INT
);

-- Create Bridge Tables (Many to Many relationship) here
CREATE TABLE students_enrolled (
    student_id INT,
    course_id INT,
    PRIMARY KEY (student_id, course_id)
);

CREATE TABLE students_exercises (
    student_id INT,
    exercise_id INT,
    PRIMARY KEY (student_id, exercise_id)
);

CREATE TABLE courses_exercises (
    course_id INT,
    exercise_id INT,
    PRIMARY KEY (course_id, exercise_id)
);

CREATE TABLE students_progress (
    student_id INT,
    progress_id INT,
    Primary Key (student_id, progress_id)
);

-- Create Foreign Keys

-- One to One relationship between students and user_accounts
ALTER TABLE user_accounts
ADD CONSTRAINT fk_user_accounts_students 
FOREIGN KEY (student_id) 
REFERENCES students;

-- Many to Many relationship between students enrolled in courses
ALTER TABLE students_enrolled
ADD CONSTRAINT fk_students_enrolled_student_id
FOREIGN KEY (student_id) 
REFERENCES students;

ALTER TABLE students_enrolled
ADD CONSTRAINT fk_students_enrolled_course_id
FOREIGN KEY (course_id) 
REFERENCES courses;

-- Many to Many relationship between courses and exercises
ALTER TABLE courses_exercises
ADD CONSTRAINT fk_courses_exercises_course_id
FOREIGN KEY (course_id) 
REFERENCES courses;

ALTER TABLE courses_exercises
ADD CONSTRAINT fk_courses_exercises_exercise_id
FOREIGN KEY (exercise_id) 
REFERENCES exercises;

--One to Many relationship between progress and exercises 
ALTER TABLE progress
ADD CONSTRAINT fk_progress_exercises
FOREIGN KEY (exercise_id)
REFERENCES exercises;



-- Many to Many relationship between students and progress
ALTER TABLE students_exercises
ADD CONSTRAINT fk_students_exercises_student_id
FOREIGN KEY (student_id)
REFERENCES students;

ALTER TABLE students_exercises
ADD CONSTRAINT fk_students_exercises_exercise_id
FOREIGN KEY (exercise_id)
REFERENCES exercises;

ALTER TABLE students_progress
ADD CONSTRAINT fk_students_progress_student_id
FOREIGN KEY (student_id)
REFERENCES students;

ALTER TABLE students_progress
ADD CONSTRAINT fk_students_progress_progress_id
FOREIGN KEY (progress_id)
REFERENCES progress;

