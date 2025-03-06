import cx_Oracle
import pandas as pd

def db_connect():
    try:
        connection = cx_Oracle.connect(
            user="system",
            password="921729",
            dsn="Kishore_PC:1521/XE"
        )
        return connection
    except cx_Oracle.DatabaseError as e:
        print(f"Error connecting to the database: {e}")
        return None

def execute_query(connection, query, data=None):
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        return cursor
    except cx_Oracle.DatabaseError as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()

def fetch_and_print_all_tables(connection):
    tables = [
        "departments_project", 
        "professors_project", 
        "students_project", 
        "registrations_project",
        "courses_project"
    ]
    for table in tables:
        try:
            print(f"\nFetching data from table: {table}")
            query = f"SELECT * FROM {table}"
            cursor = connection.cursor()
            cursor.execute(query)
            # Fetch data and column names
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            # Use pandas for pretty formatting
            df = pd.DataFrame(rows, columns=columns)
            print(df)
        except cx_Oracle.DatabaseError as e:
            print(f"Error fetching data from {table}: {e}")
        finally:
            cursor.close()

def setup_database():
    connection = db_connect()
    if connection is None:
        return
    
    # Drop tables if they exist
    drop_queries = [
        "DROP TABLE registrations_project CASCADE CONSTRAINTS",
        "DROP TABLE students_project CASCADE CONSTRAINTS",
        "DROP TABLE professors_project CASCADE CONSTRAINTS",
        "DROP TABLE departments_project CASCADE CONSTRAINTS",
        "DROP TABLE courses_project CASCADE CONSTRAINTS"
    ]
    for query in drop_queries:
        execute_query(connection, query)

    # Create tables
    create_queries = [
        """
        CREATE TABLE departments_project (
            DEPT_ID NUMBER PRIMARY KEY,
            DEPT_NAME VARCHAR2(10)
        )
        """,
        """
        CREATE TABLE professors_project (
            EMP_ID VARCHAR2(10) PRIMARY KEY,
            NAME VARCHAR2(20),
            DEPT_ID NUMBER REFERENCES departments_project(DEPT_ID),
            HIRE_DATE DATE,
            PHNO VARCHAR2(10)
        )
        """,
        """
        CREATE TABLE students_project (
            STUDENT_ID NUMBER PRIMARY KEY,
            STUDENT_NAME VARCHAR2(15),
            EMAIL VARCHAR2(20),
            PHONE_NO VARCHAR2(11),
            CGPA NUMBER(3,2),
            DEPARTMENT VARCHAR2(10)
        )
        """,
        """
        CREATE TABLE registrations_project (
            REGISTRATION_ID NUMBER PRIMARY KEY,
            STUDENT_ID NUMBER REFERENCES students_project(STUDENT_ID),
            COURSE_ID NUMBER,
            REGISTRATION_DATE DATE
        )
        """,
        """
        CREATE TABLE courses_project (
            COURSE_ID NUMBER PRIMARY KEY,
            COURSE_NAME VARCHAR2(50),
            PROFESSOR_ID VARCHAR2(10) REFERENCES professors_project(EMP_ID),
            CREDITS NUMBER,
            DEPT_ID NUMBER REFERENCES departments_project(DEPT_ID)
        )
        """
    ]
    for query in create_queries:
        execute_query(connection, query)

    # Delete existing data
    delete_queries = [
        "DELETE FROM departments_project",
        "DELETE FROM professors_project",
        "DELETE FROM students_project",
        "DELETE FROM registrations_project",
        "DELETE FROM courses_project"
    ]
    for query in delete_queries:
        execute_query(connection, query)

    # Insert data
    insert_data_queries = [
        ("INSERT INTO departments_project (DEPT_ID, DEPT_NAME) VALUES (:1, :2)", [
            (1, 'CSE'), (2, 'ECE'), (3, 'EEE'), (4, 'Mech'), (5, 'Civil')
        ]),
        ("INSERT INTO professors_project (EMP_ID, NAME, DEPT_ID, HIRE_DATE, PHNO) VALUES (:1, :2, :3, TO_DATE(:4, 'DD-MON-YY'), :5)", [
            ('F101', 'AAA', 1, '01-JAN-17', '9078234532'),
            ('F102', 'BBB', 1, '02-FEB-16', '9978334432'),
            ('F103', 'CCC', 2, '06-MAR-15', '9878635132'),
            ('F104', 'DDD', 2, '02-DEC-17', '8778600000'),
            ('F105', 'EEE', 3, '04-JUL-20', '8778600000'),
            ('F106', 'FFF', 3, '04-JUL-20', '9778600000')
        ]),
        ("INSERT INTO students_project (STUDENT_ID, STUDENT_NAME, EMAIL, PHONE_NO, CGPA, DEPARTMENT) VALUES (:1, :2, :3, :4, :5, :6)", [
            (1089, 'kishore S', 'kishore@example.com', '7092112200', 8.74, 'CSE'),
            (1046, 'Shahishnu J R', 'shah@example.com', '7821358990', 9.25, 'CSE'),
            (1149, 'Rohit M', 'rohit@example.com', '1234567890', 8.91, 'ECE'),
            (1207, 'Satvik', 'satvik@example.com', '978906734', 9.14, 'Mech'),
            (1304, 'Bob Smith', 'bob@example.com', '135792460', 8.56, 'ECE'),
            (1389, 'John Doe', 'john@example.com', '1234567890', 7.98, 'Mech'),
            (101, 'John Doe', 'john.doe@example.com', '1234567890', 8.42, 'CSE')
        ]),
        ("INSERT INTO registrations_project (REGISTRATION_ID, STUDENT_ID, COURSE_ID, REGISTRATION_DATE) VALUES (:1, :2, :3, TO_DATE(:4, 'DD-MON-YY'))", [
            (1509, 1089, 102, '30-OCT-24'),
            (5422, 1046, 101, '30-OCT-24'),
            (4702, 1089, 102, '02-NOV-24'),
            (5659, 1089, 103, '02-NOV-24'),
            (1412, 1089, 101, '06-NOV-24')
        ]),
        ("INSERT INTO courses_project (COURSE_ID, COURSE_NAME, PROFESSOR_ID, CREDITS, DEPT_ID) VALUES (:1, :2, :3, :4, :5)", [
            (101, "Advanced Algorithms", "F101", 3, 1),
            (102, "Data Structures and Algorithms", "F101", 3, 1),
            (103, "Database Management Systems", "F102", 3, 1)
        ])
    ]

    for query, data in insert_data_queries:
        for row in data:
            execute_query(connection, query, row)

    connection.commit()
    print("Database setup complete with sample data.")

    # Fetch and print data from all tables
    fetch_and_print_all_tables(connection)
    connection.close()

# Run the database setup
setup_database()