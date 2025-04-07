-- Insert Membership Plans
INSERT INTO Membership_Plan (Type, Duration, Cost)
VALUES ('Basic', 1, 30.00);
INSERT INTO Membership_Plan (Type, Duration, Cost)
VALUES ('Premium', 1, 60.00);

-- Insert Members
INSERT INTO Member (Name, ContactInfo, MembershipType, JoinDate)
VALUES ('Alice Johnson', 'alice@example.com', 'Premium', TO_DATE('2024-01-15', 'YYYY-MM-DD'));

INSERT INTO Member (Name, ContactInfo, MembershipType, JoinDate)
VALUES ('Bob Smith', 'bob@example.com', 'Basic', TO_DATE('2024-02-10', 'YYYY-MM-DD'));

-- Insert Trainers
INSERT INTO Trainer (Name, Specialization)
VALUES ('Charlie Trainer', 'Strength Training');

INSERT INTO Trainer (Name, Specialization)
VALUES ('Diana Coach', 'Cardio & HIIT');

-- Insert Classes
INSERT INTO Class (Name, Schedule, TrainerID, MaxEnrollment)
VALUES ('Morning Bootcamp', 'Mon/Wed/Fri 7:00 AM', 1, 10);

INSERT INTO Class (Name, Schedule, TrainerID, MaxEnrollment)
VALUES ('Evening HIIT', 'Tue/Thu 6:00 PM', 2, 10);

-- Enroll Premium Member in Class
INSERT INTO Class_Enrollment (MemberID, ClassID)
VALUES (1, 1); -- Alice in Morning Bootcamp

