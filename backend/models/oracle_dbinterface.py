import oracledb
from .database_interface import *
from random import randint
from flask_login import UserMixin
import bcrypt


# Concrete User class (for admin)
class oracle_user(UserMixin):
    def __init__(self, id, email, role, password):
        self.id = id
        self.email = email
        self.password = password
        self.role = role


    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False


# Concrete Member class
class oracle_member:
    def __init__(self, id, name, join_date, membership_type, contact_info):
        self.id = id
        self.name = name
        self.join_date = join_date
        self.membership_type = membership_type
        self.contact_info = contact_info


# Concrete Trainer class
class oracle_trainer:
    def __init__(self, id, name, specialization):
        self.id = id
        self.name = name
        self.specialization = specialization


# Concrete Class class
class oracle_class(Class):
    def __init__(self, id, name, trainer_id, schedule, max_enrollment):
        self.id = id
        self.name = name
        self.trainer_id = trainer_id
        self.schedule = schedule
        self.max_enrollment = max_enrollment

# Concrete MembershipPlan class
class oracle_membership_plan(MembershipPlan):
    def __init__(self, id, type, duration, cost):
        self.id = id
        self.type = type
        self.duration = duration
        self.cost = cost

class oracle_database(Database):
    def __init__(self, dbuser, dbpass, dbpath, pool_min, pool_max, pool_inc):
        oracledb.init_oracle_client()
        self.pool = oracledb.create_pool(
            user=dbuser,
            password=dbpass,
            dsn=dbpath,
            min=pool_min,
            max=pool_max,
            increment=pool_inc
        )

    def get_user(self, email: str) -> oracle_user:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                result = cursor.execute("""
                    SELECT UserID, Email, Password, Role
                    FROM Users
                    WHERE Email = :1 AND Role = 'admin'
                """, [email]).fetchone()
                if result:
                    user = oracle_user(result[0], result[1], result[3], result[2])
                    print(f"[DEBUG] Retrieved user: {user}")
                    return user
        return None
    
    def get_user_by_id(self, user_id: str) -> Union[oracle_user, None]:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT UserID, Email, Role, Password
                    FROM Users
                    WHERE UserID = :1
                """, [user_id])
                row = cursor.fetchone()
                if row:
                    return oracle_user(row[0], row[1], row[3], row[2])
                return None




   # Create an admin user (signup)
    def create_user(self, email: str, password: str, role: str) -> Union[oracle_user, None]:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                try:
                    print(f"[DEBUG] Creating user with email: {email}, role: {role}")

                    # Check if the email already exists
                    cursor.execute("""
                        SELECT COUNT(*) FROM Users WHERE email = :1
                    """, [email])
                    email_count = cursor.fetchone()[0]

                    if email_count > 0:
                        print(f"[ERROR] Email {email} already exists.")
                        return None  # Return None if email already exists

                    # Get the next available UserID from the sequence
                    cursor.execute("""
                        SELECT user_id_seq.NEXTVAL FROM DUAL
                    """)
                    user_id = cursor.fetchone()[0]
                    print(f"[DEBUG] Generated UserID: {user_id}")

                    # Insert the new user into the Users table
                    cursor.execute("""
                        INSERT INTO Users (UserID, email, Password, Role)
                        VALUES (:1, :2, :3, :4)
                    """, [user_id, email, password, role])
                    conn.commit()

                    print(f"[DEBUG] User created with ID: {user_id}, email: {email}")
                    return oracle_user(user_id, email, role, password)
                except Exception as e:
                    print(f"[ERROR] Failed to create user: {e}")
                    return None

    # Delete member by ID
    def delete_member(self, user_id: str) -> bool:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM Member
                    WHERE MemberID = :1
                """, [user_id])
                conn.commit()
                return cursor.rowcount == 1

    # Create a new trainer
    def create_trainer(self, trainer_id: str, name: str, specialization: str) -> oracle_trainer:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Trainer (TrainerID, Name, Specialization)
                    VALUES (:1, :2, :3)
                """, [trainer_id, name, specialization])
                conn.commit()
                return self.get_user(trainer_id)

    # Delete trainer by ID
    def delete_trainer(self, trainer_id: str) -> bool:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM Trainer
                    WHERE TrainerID = :1
                """, [trainer_id])
                conn.commit()
                return cursor.rowcount == 1

    # Get all classes
    def get_class(self, class_id: str) -> oracle_class:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                result = cursor.execute("""
                    SELECT ClassID, Name, TrainerID, Schedule, MaxEnrollment
                    FROM Class
                    WHERE ClassID = :1
                """, [class_id]).fetchone()
                if result:
                    return oracle_class(*result)
        return None

    # Create a new class
    def create_class(self, name: str, trainer_id: str, schedule: str, max_enrollment: int) -> oracle_class:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                class_id = randint(10000, 99999)  # Random class ID for simplicity
                cursor.execute("""
                    INSERT INTO Class (ClassID, Name, TrainerID, Schedule, MaxEnrollment)
                    VALUES (:1, :2, :3, :4, :5)
                """, [class_id, name, trainer_id, schedule, max_enrollment])
                conn.commit()
                return self.get_class(class_id)

    # Enroll member in a class
    def enroll_member_in_class(self, user_id: str, class_id: str) -> bool:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                enrollment_id = randint(100000, 999999)
                cursor.execute("""
                    INSERT INTO Class_Enrollment (EnrollmentID, MemberID, ClassID)
                    VALUES (:1, :2, :3)
                """, [enrollment_id, user_id, class_id])
                conn.commit()
                return cursor.rowcount == 1

    # Get enrolled members for a class
    def get_enrolled_members(self, class_id: str) -> List[oracle_member]:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                results = cursor.execute("""
                    SELECT m.MemberID, m.Name, m.MembershipType, m.ContactInfo, m.JoinDate
                    FROM Member m
                    JOIN Class_Enrollment ce ON m.MemberID = ce.MemberID
                    WHERE ce.ClassID = :1
                """, [class_id]).fetchall()
                return [oracle_member(*r) for r in results]

    # Create a new membership plan
    def create_membership_plan(self, type: str, duration: int, cost: float) -> oracle_membership_plan:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                plan_id = randint(100, 999)
                cursor.execute("""
                    INSERT INTO Membership_Plan (PlanID, Type, Duration, Cost)
                    VALUES (:1, :2, :3, :4)
                """, [plan_id, type, duration, cost])
                conn.commit()
                return self.get_membership_plan(plan_id)

    # Get membership plan by ID
    def get_membership_plan(self, plan_id: str) -> oracle_membership_plan:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                result = cursor.execute("""
                    SELECT PlanID, Type, Duration, Cost
                    FROM Membership_Plan
                    WHERE PlanID = :1
                """, [plan_id]).fetchone()
                if result:
                    return oracle_membership_plan(*result)
        return None

    # Assign trainer to a class
    def assign_trainer_to_class(self, trainer_id: str, class_id: str) -> bool:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE Class
                    SET TrainerID = :1
                    WHERE ClassID = :2
                """, [trainer_id, class_id])
                conn.commit()   
                return cursor.rowcount == 1


    # Get trainer by ID
    def get_trainer(self, trainer_id: str) -> oracle_trainer:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                result = cursor.execute("""
                    SELECT TrainerID, Name, Specialization
                    FROM Trainer
                    WHERE TrainerID = :1
                """, [trainer_id]).fetchone()
                if result:
                    return oracle_trainer(*result)
        return None

    # Check if a class is full
    def is_class_full(self, class_id: str) -> bool:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                result = cursor.execute("""
                    SELECT COUNT(*)
                    FROM Class_Enrollment
                    WHERE ClassID = :1
                """, [class_id]).fetchone()
                max_enrollment = cursor.execute("""
                    SELECT MaxEnrollment
                    FROM Class
                    WHERE ClassID = :1
                """, [class_id]).fetchone()
                return result[0] >= max_enrollment[0]
            
    # Get a member by ID
    def get_member(self, member_id: str) -> oracle_member:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                result = cursor.execute("""
                    SELECT MemberID, Name, MembershipType, ContactInfo, JoinDate
                    FROM Member
                    WHERE MemberID = :1
                """, [member_id]).fetchone()
                if result:
                    return oracle_member(*result)
        return None

    # Create a new member
    def create_member(self, member_id: str, name: str, membership_type: str, contact_info: str) -> oracle_member:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Member (MemberID, Name, JoinDate, MembershipType, ContactInfo)
                    VALUES (:1, :2, SYSDATE, :3, :4)
                """, [member_id, name, membership_type, contact_info])
                conn.commit()
                return self.get_member(member_id)

    # Implementing the method to get all members
    def get_all_members(self):
        query = """
        SELECT MemberID, Name, ContactInfo, MembershipType, JoinDate FROM Member
        """
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                members = []
                for row in cursor:
                    members.append({
                        'id': row[0],
                        'name': row[1],
                        'contact_info': row[2],
                        'membership_type': row[3],
                        'join_date': row[4]
                    })
                return members

    # Implementing the method to get all trainers
    def get_all_trainers(self):
        query = """
        SELECT TrainerID, Name, Specialization FROM Trainer
        """
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                trainers = []
                for row in cursor:
                    trainers.append({
                        'id': row[0],
                        'name': row[1],
                        'specialization': row[2]
                    })
                return trainers
            
    def add_member(self, name, contact_info, membership_type, join_date):
        query = """
            INSERT INTO Member (MemberID, Name, ContactInfo, MembershipType, JoinDate)
            VALUES (LPAD(user_id_seq.NEXTVAL, 9, '0'), :1, :2, :3, :4)
        """
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (name, contact_info, membership_type, join_date))
            conn.commit()

    def add_trainer(self, name, specialization):
        query = """
            INSERT INTO Trainer (TrainerID, Name, Specialization)
            VALUES (LPAD(user_id_seq.NEXTVAL, 9, '0'), :1, :2)
        """
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (name, specialization))
            conn.commit()
