import oracledb
from database_interface import *
from random import randint

class oracle_user(user):
    def __init__(self, id, name, password, join_date):
        self.id = id
        self.name = name
        self.__password__ = password
        self.__join_date__ = join_date

class oracle_member(member):
    def __init__(self, id, name, join_date, membership_type):
        self.id = id
        self.name = name
        self.join_date = join_date
        self.membership_type = membership_type

class oracle_trainer(trainer):
    def __init__(self, id, name, certification):
        self.id = id
        self.name = name
        self.certification = certification

class oracle_database(database):
    def __init__(self, dbuser:str, dbpass:str, dbpath:str, pool_min:int, pool_max:int, pool_inc:int):
        oracledb.init_oracle_client()
        self.pool = oracledb.create_pool(
            user=dbuser,
            password=dbpass,
            dsn=dbpath,
            min=pool_min,
            max=pool_max,
            increment=pool_inc
        )

    # Get member by ID
    def get_member(self, member_id) -> oracle_member:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                members = [oracle_member(*r) for r in cursor.execute(
                    '''
                    select * from Members
                    where MemberID = :1
                    ''',
                    [member_id]
                )]
                if len(members) == 1:
                    return members[0]
        return None

    # Create a new member
    def create_member(self, member_id, name, membership_type) -> oracle_member:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    '''
                    insert into Members (MemberID, Name, JoinDate, MembershipType)
                    values (:1, :2, sysdate, :3)
                    ''',
                    [member_id, name, membership_type]
                )
                if cursor.rowcount == 1:
                    conn.commit()
                    return self.get_member(member_id)
        return None

    # Delete member by ID
    def delete_member(self, member_id) -> bool:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    '''
                    delete from Members
                    where MemberID = :1
                    ''',
                    [member_id]
                )
                if cursor.rowcount == 1:
                    conn.commit()
                    return True
        return False

    # Get trainer by ID
    def get_trainer(self, trainer_id) -> oracle_trainer:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                trainers = [oracle_trainer(*r) for r in cursor.execute(
                    '''
                    select * from Trainers
                    where TrainerID = :1
                    ''',
                    [trainer_id]
                )]
                if len(trainers) == 1:
                    return trainers[0]
        return None

    # Create a new trainer
    def create_trainer(self, trainer_id, name, certification) -> oracle_trainer:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    '''
                    insert into Trainers (TrainerID, Name, Certification)
                    values (:1, :2, :3)
                    ''',
                    [trainer_id, name, certification]
                )
                if cursor.rowcount == 1:
                    conn.commit()
                    return self.get_trainer(trainer_id)
        return None

    # Delete trainer by ID
    def delete_trainer(self, trainer_id) -> bool:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    '''
                    delete from Trainers
                    where TrainerID = :1
                    ''',
                    [trainer_id]
                )
                if cursor.rowcount == 1:
                    conn.commit()
                    return True
        return False

    # Create a new training session
    def create_training_session(self, session_id, trainer_id, member_id, session_date, session_time, session_type) -> bool:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    '''
                    insert into TrainingSessions (SessionID, TrainerID, MemberID, SessionDate, SessionTime, SessionType)
                    values (:1, :2, :3, :4, :5, :6)
                    ''',
                    [session_id, trainer_id, member_id, session_date, session_time, session_type]
                )
                if cursor.rowcount == 1:
                    conn.commit()
                    return True
        return False

    # Get all training sessions for a member
    def get_training_sessions(self, member_id) -> list[oracle_trainer]:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                sessions = [session for session in cursor.execute(
                    '''
                    select * from TrainingSessions
                    where MemberID = :1
                    ''',
                    [member_id]
                )]
                return sessions
        return None

    # Delete a training session
    def delete_training_session(self, session_id) -> bool:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    '''
                    delete from TrainingSessions
                    where SessionID = :1
                    ''',
                    [session_id]
                )
                if cursor.rowcount == 1:
                    conn.commit()
                    return True
        return False

    # Update training session details
    def update_training_session(self, session_id, session_date=None, session_time=None, session_type=None) -> bool:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                if session_date:
                    cursor.execute(
                        '''
                        update TrainingSessions
                        set SessionDate = :1
                        where SessionID = :2
                        ''',
                        [session_date, session_id]
                    )
                    if cursor.rowcount != 1:
                        return False
                if session_time:
                    cursor.execute(
                        '''
                        update TrainingSessions
                        set SessionTime = :1
                        where SessionID = :2
                        ''',
                        [session_time, session_id]
                    )
                    if cursor.rowcount != 1:
                        return False
                if session_type:
                    cursor.execute(
                        '''
                        update TrainingSessions
                        set SessionType = :1
                        where SessionID = :2
                        ''',
                        [session_type, session_id]
                    )
                    if cursor.rowcount != 1:
                        return False
                conn.commit()
        return True

    # Get available trainers for a particular session type
    def get_available_trainers(self, session_type) -> list[oracle_trainer]:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                trainers = [oracle_trainer(*r) for r in cursor.execute(
                    '''
                    select * from Trainers
                    where Certification like :1
                    ''',
                    [session_type]
                )]
                return trainers
        return None

    # Search for members based on name or membership type
    def search_members(self, query:str) -> list[oracle_member]:
        with self.pool.acquire() as conn:
            with conn.cursor() as cursor:
                members = [oracle_member(*r) for r in cursor.execute(
                    '''
                    select * from Members
                    where lower(Name) like '%'||lower(:1)||'%'
                    or lower(MembershipType) like '%'||lower(:1)||'%'
                    ''',
                    [query]
                )]
                return members
        return None
