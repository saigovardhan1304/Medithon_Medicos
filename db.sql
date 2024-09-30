-- Database: medical_management

CREATE DATABASE medical_management;
USE medical_management;

-- Table to store patient details and file records
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
CREATE TABLE action_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    action VARCHAR(255),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    emp_number VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);