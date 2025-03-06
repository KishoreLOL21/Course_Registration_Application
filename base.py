import cx_Oracle
import pandas as pd

def db_connect():
    try:
        connection = cx_Oracle.connect(
            user="Your Oracle SQL User Name here",
            password="Your Oracle SQL Password here",
            dsn="DSN of your PC here"
        )
        return connection
    except cx_Oracle.DatabaseError as e:
        print(f"Error connecting to the database: {e}")
        return None

def execute_query(connection, query, data=None):
    cursor = connection.cursor()
    try:
        if data:
            cursor.executemany(query, data)  # Use executemany for batch insertions
        else:
            cursor.execute(query)
        return cursor
    except cx_Oracle.DatabaseError as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()

def fetch_and_print_all_tables(connection):
    tables = ["departments_project", "professors_project", "students_project", 
              "courses_project", "registrations_project", "hostel"]
    for table in tables:
        try:
            print(f"\nFetching data from table: {table}")
            query = f"SELECT * FROM {table}"
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
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
        "DROP TABLE courses_project CASCADE CONSTRAINTS",
        "DROP TABLE hostel CASCADE CONSTRAINTS"
    ]
    for query in drop_queries:
        try:
            execute_query(connection, query)
        except:
            pass  # Ignore errors for non-existent tables

    # Create tables in correct dependency order
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
            DEPARTMENT VARCHAR2(10),
            ENROLLMENT_DATE DATE
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
        """,
        """
        CREATE TABLE registrations_project (
            REGISTRATION_ID NUMBER PRIMARY KEY,
            STUDENT_ID NUMBER REFERENCES students_project(STUDENT_ID),
            COURSE_ID NUMBER REFERENCES courses_project(COURSE_ID),
            REGISTRATION_DATE DATE
        )
        """,
        """
        CREATE TABLE hostel (
            hostel_id VARCHAR2(10) PRIMARY KEY,
            name VARCHAR2(20),
            capacity NUMBER,
            location VARCHAR2(20)
        )
        """
    ]
    for query in create_queries:
        execute_query(connection, query)

    # Insert sample data
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
        ("INSERT INTO students_project (STUDENT_ID, STUDENT_NAME, EMAIL, PHONE_NO, CGPA, DEPARTMENT, ENROLLMENT_DATE) VALUES (:1, :2, :3, :4, :5, :6, TO_DATE(:7, 'DD-MON-YY'))", [
            (1089, 'Kishore S', 'kishore@example.com', '7092112200', 8.74, 'CSE', '10-JAN-22'),
            (1046, 'Shahishnu J R', 'shah@example.com', '7821358990', 9.25, 'CSE', '15-JAN-22'),
            (1149, 'Rohit M', 'rohit@example.com', '1234567890', 8.91, 'ECE', '12-FEB-22'),
            (1207, 'Satvik', 'satvik@example.com', '978906734', 9.14, 'Mech', '10-MAR-22'),
            (1304, 'Bob Smith', 'bob@example.com', '135792460', 8.56, 'ECE', '05-MAR-21'),
            (1389, 'John Doe', 'john@example.com', '1234567890', 7.98, 'Mech', '20-MAR-21'),
            (101, 'John Daniel', 'john.danie@example.com', '1234567890', 8.42, 'CSE', '01-APR-21')
        ]),
        ("INSERT INTO courses_project (COURSE_ID, COURSE_NAME, PROFESSOR_ID, CREDITS, DEPT_ID) VALUES (:1, :2, :3, :4, :5)", [
            (101, "Advanced Algorithms", "F101", 3, 1),
            (102, "Data Structures and Algorithms", "F101", 3, 1),
            (103, "Database Management Systems", "F102", 3, 1)
        ]),
        ("INSERT INTO registrations_project (REGISTRATION_ID, STUDENT_ID, COURSE_ID, REGISTRATION_DATE) VALUES (:1, :2, :3, TO_DATE(:4, 'DD-MON-YY'))", [
            (1509, 1089, 101, '30-OCT-24'),
            (5422, 1046, 102, '30-OCT-24'),
            (4702, 1149, 103, '02-NOV-24'),
            (5659, 1207, 101, '02-NOV-24'),
            (1412, 1389, 102, '06-NOV-24')
        ])
    ]
    for query, data in insert_data_queries:
        execute_query(connection, query, data)

    # Insert hostel data
    hostel_query = """
    INSERT INTO hostel (hostel_id, name, capacity, location) 
    VALUES (:1, :2, :3, :4)
    """
    hostel_data = [
        ("H101", "A block", 2000, "VITCC"),
        ("H102", "B block", 3600, "VITCC"),
        ("H103", "C block", 1500, "VITCC"),
        ("H104", "D block", 5000, "VITCC"),
        ("H105", "E block", 4000, "VITCC")
    ]
    execute_query(connection, hostel_query, hostel_data)

    connection.commit()
    print("Database setup complete with sample data.")
    fetch_and_print_all_tables(connection)
    connection.close()

setup_database()
