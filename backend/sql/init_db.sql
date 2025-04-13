-- Create the user_id sequence
CREATE SEQUENCE user_id_seq
START WITH 100000001
INCREMENT BY 1
NOCACHE;

-- Drop existing tables if they exist
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Class_Enrollment CASCADE CONSTRAINTS';
    EXECUTE IMMEDIATE 'DROP TABLE Class CASCADE CONSTRAINTS';
    EXECUTE IMMEDIATE 'DROP TABLE Member CASCADE CONSTRAINTS';
    EXECUTE IMMEDIATE 'DROP TABLE Trainer CASCADE CONSTRAINTS';
    EXECUTE IMMEDIATE 'DROP TABLE Membership_Plan CASCADE CONSTRAINTS';
    EXECUTE IMMEDIATE 'DROP TABLE Users CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN
        NULL; -- Skip if table doesn't exist
END;
/

-- 1. Member Table
CREATE TABLE Member (
    MemberID        CHAR(9) PRIMARY KEY,
    Name            VARCHAR2(100),
    ContactInfo     VARCHAR2(100),
    MembershipType  VARCHAR2(20), -- 'Basic' or 'Premium'
    JoinDate        DATE
);

-- 2. Trainer Table
CREATE TABLE Trainer (
    TrainerID       CHAR(9) PRIMARY KEY,
    Name            VARCHAR2(100),
    Specialization  VARCHAR2(100)
);

-- 3. Membership_Plan Table
CREATE TABLE Membership_Plan (
    PlanID          CHAR(9) PRIMARY KEY,
    Type            VARCHAR2(20), -- 'Basic' or 'Premium'
    Duration        NUMBER,       -- In months
    Cost            NUMBER(8,2)
);

-- 4. Class Table
CREATE TABLE Class (
    ClassID         CHAR(9) PRIMARY KEY,
    Name            VARCHAR2(100),
    Schedule        VARCHAR2(100),
    TrainerID       CHAR(9) REFERENCES Trainer,
    MaxEnrollment   NUMBER DEFAULT 10
);

-- 5. Class_Enrollment Table
CREATE TABLE Class_Enrollment (
    EnrollmentID    CHAR(9) PRIMARY KEY,
    MemberID        CHAR(9) REFERENCES Member,
    ClassID         CHAR(9) REFERENCES Class
);

-- 6. Users Table (for Admin/Trainer login)
CREATE TABLE Users (
    UserID          CHAR(9) PRIMARY KEY,
    email           VARCHAR2(100) UNIQUE NOT NULL,
    Password        VARCHAR2(255) NOT NULL,
    Role            VARCHAR2(20) CHECK (Role IN ('admin', 'trainer'))
);
