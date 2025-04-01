# GymOS

A client relationship management webapp that helps facilities manage memberships and training sessions.

## **1. Application Domain Introduction**

The Gym Membership and Training Management System is designed to assist fitness centers in managing memberships, personal training sessions, and class schedules. This application will provide an efficient way for gym owners, trainers, and members to handle their fitness-related activities. The primary users of this system are gym administrators, personal trainers, and members.

### **Relevant Domain Knowledge:**

- Gym members need to register and subscribe to different membership plans.
- Personal trainers manage training sessions with members.
- Trainers conduct one-on-one or group fitness sessions with a maximum class enrollment of 10 members.
- Membership is divided into Basic and Premium plans, where only Premium members can enroll in scheduled classes.

## **2. Business Data Description**

The system will be built around the following entity sets and relationships:

### **Entity Sets:**

1. **Member** (MemberID, Name, ContactInfo, MembershipType, JoinDate)
2. **Trainer** (TrainerID, Name, Specialization)
3. **Class** (ClassID, Name, Schedule, TrainerID, MaxEnrollment)
4. **Membership Plan** (PlanID, Type, Duration, Cost)

### **Relationship Sets:**

- **Member-Membership Plan (M:1):** A member subscribes to only one membership plan, but a membership plan can have multiple members.
- **Trainer-Class (1:M):** A trainer can conduct multiple classes, but each class is led by only one trainer.
- **Member-Class (M:N)(Premium Members Only):** A member can enroll in multiple scheduled classes, and a scheduled class can have up to 10 members.
  <br><br><br><br>

## **3. Application (Business Logic) Requirements**

The system will include the following core functionalities:

### **1. Member Registration and Management:**

- Allow new members to register and choose a membership plan (Basic or Premium).
- View and update personal details.

### **2. Trainer Assignment and Management:**

- Assign trainers to specific classes.
- Track trainer availability and specialization.

### **3. Class Scheduling and Enrollment:**

- Schedule fitness classes with assigned trainers.
- Enable premium members to enroll or cancel class participation, ensuring a maximum enrollment of 10 members per class.

### **4. Membership Payment Processing:**

- Track membership payment status and renewals.

### **5. Performance Tracking and Reports:**

- Generate reports on member attendance, trainer schedules, and revenue.
- Provide analytics on popular classes and trainer efficiency.

## 4. Database Design

### **1. Entity-Relationship Diagram**

```mermaid
erDiagram
    MEMBER {
        int MemberID PK
        string Name
        string ContactInfo
        string MembershipType
        date JoinDate
    }

    TRAINER {
        int TrainerID PK
        string Name
        string Specialization
    }

    CLASS {
        int ClassID PK
        string Name
        int TrainerID FK
        string Schedule
        int MaxEnrollment
    }

    MEMBERSHIP_PLAN {
        int PlanID PK
        string Type
        int Duration
        decimal Cost
    }

    CLASS_ENROLLMENT {
        int EnrollmentID PK
        int MemberID FK
        int ClassID FK
    }

    MEMBER ||--|{ MEMBERSHIP_PLAN : subscribes_to
    TRAINER ||--|{ CLASS : conducts
    MEMBER ||--|{ CLASS_ENROLLMENT : enrolls
    CLASS ||--|{ CLASS_ENROLLMENT : contains

```
