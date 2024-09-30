CREATE DATABASE medical_management;
USE medical_management;

CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    patient_name VARCHAR(255) NOT NULL,
    department VARCHAR(50) NOT NULL,
    comments TEXT,
    file_path VARCHAR(255),
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to store action history (like insert, view, etc.)
select *from patients;

ALTER TABLE patients ADD COLUMN encryption_key TEXT;
ALTER TABLE patients RENAME COLUMN encrypted_key TO encryption_key;


CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    feedback_text TEXT NOT NULL,
    date_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    emp_number VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
