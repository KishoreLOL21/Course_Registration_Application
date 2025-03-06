import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import cx_Oracle as db
import random

# Database connection function
def db_connect():
    try:
        connection = db.connect(
            user="Your Oracle SQL User Name here",
            password="Your Oracle SQL Password here",
            dsn="DSN of your PC here"
        )
        return connection
    except db.DatabaseError as e:
        messagebox.showerror("Database Error", f"Error connecting to the database:\n{str(e)}")
        return None

def authenticate_login(user_id, password, user_type):
    connection = db_connect()
    if connection:
        cursor = connection.cursor()
        try:
            if user_type == "student":
                cursor.execute("SELECT password FROM student_login_info WHERE student_id = :1", (user_id,))
            elif user_type == "admin":
                cursor.execute("SELECT password FROM admin_login_info WHERE admin_id = :1", (user_id,))
            elif user_type == "professor":
                cursor.execute("SELECT password FROM professor_login_info WHERE professor_id = :1", (user_id,))

            db_password = cursor.fetchone()
            if db_password and db_password[0] == password:
                return True
            else:
                return False
        except db.DatabaseError as e:
            messagebox.showerror("Database Error", f"Error executing SQL:\n{str(e)}")
            return False
        finally:
            cursor.close()
            connection.close()
    return False

def sign_up_user(user_id, password, user_type):
    connection = db_connect()
    if connection:
        cursor = connection.cursor()
        try:
            if user_type == "student":
                cursor.execute("INSERT INTO student_login_info (student_id, password) VALUES (:1, :2)", (user_id, password))
            elif user_type == "admin":
                cursor.execute("INSERT INTO admin_login_info (admin_id, password) VALUES (:1, :2)", (user_id, password))
            elif user_type == "professor":
                cursor.execute("INSERT INTO professor_login_info (professor_id, password) VALUES (:1, :2)", (user_id, password))

            connection.commit()
            return True
        except db.DatabaseError as e:
            messagebox.showerror("Database Error", f"Error executing SQL:\n{str(e)}")
            return False
        finally:
            cursor.close()
            connection.close()
    return False

# Function to handle login for different user types
def login(user_type):
    def perform_login():
        user_id = user_id_entry.get()
        password = password_entry.get()
        if authenticate_login(user_id, password, user_type):
            messagebox.showinfo("Success", f"{user_type.capitalize()} login successful!")
            if user_type == "student":
                show_frame(student_frame)
            elif user_type == "admin":
                show_frame(admin_frame)
            elif user_type == "professor":
                show_frame(professor_frame)
        else:
            messagebox.showwarning("Authentication Failed", "Invalid User ID or Password")

    def go_to_sign_up():
        sign_up(user_type)

    # Clear previous entries
    for widget in login_frame.winfo_children():
        widget.destroy()

    ttk.Label(login_frame, text=f"{user_type.capitalize()} Login", font=("Arial", 16, "bold")).pack(pady=10)
    ttk.Label(login_frame, text="User ID:").pack(pady=5)
    user_id_entry = ttk.Entry(login_frame, width=25)
    user_id_entry.pack(pady=5)

    ttk.Label(login_frame, text="Password:").pack(pady=5)
    password_entry = ttk.Entry(login_frame, show="*", width=25)
    password_entry.pack(pady=5)

    ttk.Button(login_frame, text="Login", command=perform_login).pack(pady=10)
    ttk.Button(login_frame, text="Sign Up", command=go_to_sign_up).pack(pady=10)
    ttk.Button(login_frame, text="Back", command=lambda: show_frame(main_frame)).pack(pady=10)

    show_frame(login_frame)

# Function to handle sign-up for different user types
def sign_up(user_type):
    def perform_sign_up():
        user_id = user_id_entry.get()
        password = password_entry.get()
        if user_id and password:
            if sign_up_user(user_id, password, user_type):
                messagebox.showinfo("Success", f"{user_type.capitalize()} sign-up successful! You can now log in.")
                show_frame(main_frame)
            else:
                messagebox.showerror("Sign Up Failed", "Error signing up. Please try again.")
        else:
            messagebox.showwarning("Input Error", "User ID and Password cannot be empty")

    # Clear previous entries
    for widget in sign_up_frame.winfo_children():
        widget.destroy()

    ttk.Label(sign_up_frame, text=f"{user_type.capitalize()} Sign Up", font=("Arial", 16, "bold")).pack(pady=10)
    ttk.Label(sign_up_frame, text="User ID:").pack(pady=5)
    user_id_entry = ttk.Entry(sign_up_frame, width=25)
    user_id_entry.pack(pady=5)

    ttk.Label(sign_up_frame, text="Create Password:").pack(pady=5)
    password_entry = ttk.Entry(sign_up_frame, show="*", width=25)
    password_entry.pack(pady=5)

    ttk.Button(sign_up_frame, text="Sign Up", command=perform_sign_up).pack(pady=10)
    ttk.Button(sign_up_frame, text="Back", command=lambda: login(user_type)).pack(pady=10)

    show_frame(sign_up_frame)

# Main application window setup
root = tk.Tk()
root.title("Course Registration System")
root.geometry("900x700")
root.configure(bg="#e6f2ff")

style = ttk.Style()
# Frame style
style.configure("TFrame", background="#f0f4f8")
# Label style
style.configure("TLabel", font=("Helvetica", 12), foreground="black", background="#f0f4f8")
# Button style with black font color
style.configure("TButton", font=("Helvetica", 12, "bold"), background="#0052cc", foreground="black")
# Button active state color mapping
style.map("TButton", background=[("active", "#003d99")])



# Define frames for each "page"
main_frame = ttk.Frame(root, padding="30 30 30 30")
login_frame = ttk.Frame(root, padding="20 20 20 20")
sign_up_frame = ttk.Frame(root, padding="20 20 20 20")
student_frame = ttk.Frame(root, padding="20 20 20 20")
admin_frame = ttk.Frame(root, padding="20 20 20 20")
professor_frame = ttk.Frame(root, padding="20 20 20 20")
courses_frame = ttk.Frame(root, padding="20 20 20 20")
view_student_frame = ttk.Frame(root, padding="20 20 20 20")
add_student_frame = ttk.Frame(root, padding="20 20 20 20")  # Add these missing frames
add_course_frame = ttk.Frame(root, padding="20 20 20 20")
delete_course_frame = ttk.Frame(root, padding="20 20 20 20")

# Function to clear current frame and show a target frame
def show_frame(frame):
    for f in (main_frame, login_frame, sign_up_frame, student_frame, admin_frame, professor_frame, 
              courses_frame, view_student_frame, add_student_frame, add_course_frame, delete_course_frame):
        f.pack_forget()  # Hide all frames
    frame.pack(fill="both", expand=True)  # Show the target frame


# Function to set up the main frame (home page)
def setup_main_frame():
    ttk.Label(main_frame, text="Course Registration System", font=("Arial", 20, "bold")).pack(pady=20)
    ttk.Button(main_frame, text="Student Login", command=lambda: login("student"), width=30).pack(pady=10)
    ttk.Button(main_frame, text="Admin Login", command=lambda: login("admin"), width=30).pack(pady=10)
    ttk.Button(main_frame, text="Professor Login", command=lambda: login("professor"), width=30).pack(pady=10)

# Function to set up the student frame (page after successful login)
def setup_student_frame():
    ttk.Label(student_frame, text="Course Registration", font=("Arial", 16, "bold")).pack(pady=10)
    ttk.Label(student_frame, text="Student ID:").pack(pady=5)
    student_id_entry = ttk.Entry(student_frame, width=25)
    student_id_entry.pack(pady=5)

    ttk.Label(student_frame, text="Course ID:").pack(pady=5)
    course_id_entry = ttk.Entry(student_frame, width=25)
    course_id_entry.pack(pady=5)

    def generate_registration_id():
        # Generate a unique registration ID between 1000 and 9999
        return random.randint(1000, 9999)

    def register_course():
        student_id = student_id_entry.get()
        course_id = course_id_entry.get()
        if not student_id or not course_id:
            messagebox.showwarning("Input Error", "Please enter Student ID and Course ID.")
            return

        registration_id = generate_registration_id()  # Generate the registration ID

        connection = db_connect()
        if connection:
            cursor = connection.cursor()
            try:
                # Insert registration data into the database with the generated registration ID and SYSDATE for the current date
                cursor.execute(
                    """
                    INSERT INTO registrations (registration_id, student_id, course_id, registration_date)
                    VALUES (:1, :2, :3, SYSDATE)
                    """,
                    (registration_id, student_id, course_id)
                )
                connection.commit()
                messagebox.showinfo("Success", f"Course {course_id} registered successfully!\n"
                                            f"Registration ID: {registration_id}")
                show_frame(main_frame)
            except db.DatabaseError as e:
                messagebox.showerror("Database Error", f"Error executing SQL:\n{str(e)}")
            finally:
                cursor.close()
                connection.close()

    # Function to view registered courses for the student
    def show_registered_courses():
        student_id = student_id_entry.get()
        if not student_id:
            messagebox.showwarning("Input Error", "Please enter your Student ID.")
            return

        connection = db_connect()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    """
                    SELECT registration_id, course_id, registration_date
                    FROM registrations
                    WHERE student_id = :1
                    """,
                    (student_id,)
                )
                results = cursor.fetchall()
                if results:
                    display_results("Registration ID", "Course ID", "Registration Date", results)
                else:
                    messagebox.showinfo("No Registrations", "No courses registered yet.")
            except db.DatabaseError as e:
                messagebox.showerror("Database Error", f"Error fetching data:\n{str(e)}")
            finally:
                cursor.close()
                connection.close()

    # Function to display results in a new window
    def display_results(col1, col2, col3, results):
        results_window = tk.Toplevel(root)
        results_window.title("Registered Courses")

        tree = ttk.Treeview(results_window, columns=(col1, col2, col3), show="headings")
        tree.heading(col1, text=col1)
        tree.heading(col2, text=col2)
        tree.heading(col3, text=col3)

        for row in results:
            tree.insert("", "end", values=row)

        tree.pack(fill="both", expand=True)

    # Buttons
    ttk.Button(student_frame, text="Register Course", command=register_course).pack(pady=10)
    ttk.Button(student_frame, text="View Registered Courses", command=show_registered_courses).pack(pady=10)
    ttk.Button(student_frame, text="Back", command=lambda: show_frame(main_frame)).pack(pady=10)

# Admin Page for managing courses, students, and registrations
# Admin Page for managing courses, students, and registrations

def execute_sql_query(option):
    connection = db_connect()
    if not connection:
        return

    cursor = connection.cursor()
    try:
        if option == "1. Create a table for the 'Student' entity":
            cursor.execute("""
                CREATE TABLE Student (
                    Student_ID varchar(15) PRIMARY KEY,
                    Student_Name VARCHAR2(50) NOT NULL,
                    Email VARCHAR2(50),
                    Phone_No NUMBER,
                    Department VARCHAR2(50),
                    Enrollment_Date DATE DEFAULT SYSDATE
                )
            """)
            messagebox.showinfo("Success", "Table 'Student' created successfully.")

        elif option == "2. Alter the 'Course' table to add a new attribute, 'Prerequisite'":
            cursor.execute("ALTER TABLE Courses ADD Prerequisite VARCHAR2(50)")
            messagebox.showinfo("Success", "Attribute 'Prerequisite' added to 'Course' table.")

        elif option == "3. Insert a new student record":
            cursor.execute("""
                INSERT INTO Students (Student_ID, Student_Name, Email, Phone_No, Department) 
                VALUES (101, 'John Doe', 'john.doe@example.com', 1234567890, 'CSE')
            """)
            connection.commit()
            messagebox.showinfo("Success", "New student record inserted successfully.")

        elif option == "4. Update the course name":
            cursor.execute("UPDATE Courses SET Course_Name = 'Advanced Algorithms' WHERE Course_ID = 101")
            connection.commit()
            messagebox.showinfo("Success", "Course name updated successfully.")

        elif option == "5. Delete a graduated student record":
            cursor.execute("DELETE FROM Student WHERE Student_ID = 1306")
            connection.commit()
            messagebox.showinfo("Success", "Graduated student record deleted successfully.")

        elif option == "6. Find average grade of students in a course":
            cursor.execute("SELECT DEPARTMENT,AVG(CGPA) AS \"AVERAGE GRADE\" FROM STUDENTS GROUP BY DEPARTMENT")
            result = cursor.fetchone()
            messagebox.showinfo("Result", f"Average grade: {result[0] if result[0] is not None else 'No Data'}")

        elif option == "7. Count total number of students in each department":
            cursor.execute("SELECT Department, COUNT(*) FROM Student GROUP BY Department")
            results = cursor.fetchall()
            display_results("Department", "Count", results)

        elif option == "8. List students and their courses (using inner join)":
            cursor.execute("""
                SELECT s.Student_Name, c.Course_Name
                FROM Student s
                INNER JOIN Registrations r ON s.Student_ID = r.Student_ID
                INNER JOIN Courses c ON r.Course_ID = c.Course_ID
            """)
            results = cursor.fetchall()
            display_results("Student Name", "Course Name", results)

        elif option == "9. List all professors and courses (using left join)":
            cursor.execute("""
                SELECT p.Professor_Name, c.Course_Name
                FROM Professor p
                LEFT JOIN Course c ON p.Professor_ID = c.Professor_ID
            """)
            results = cursor.fetchall()
            display_results("Professor Name", "Course Name", results)

        elif option == "10. List students who enrolled after a specific date":
            specific_date = "2022-01-01"  # For demonstration, we use a fixed date
            cursor.execute("SELECT * FROM Students WHERE Enrollment_Date > TO_DATE(:1, 'YYYY-MM-DD')", (specific_date,))
            results = cursor.fetchall()
            display_results("Student ID", "Student Name", results)

        elif option == "11. Find the number of days remaining until a project deadline":
            cursor.execute("""
                SELECT Project_Name, (Deadline - SYSDATE) AS Days_Left 
                FROM Projects
            """)
            results = cursor.fetchall()
            display_results("Project Name", "Days Left", results)

    except db.DatabaseError as e:
        messagebox.showerror("Database Error", f"Error executing SQL:\n{str(e)}")
    finally:
        cursor.close()
        connection.close()

def display_results(col1, col2, results):
    results_window = tk.Toplevel(root)
    results_window.title("Query Results")

    tree = ttk.Treeview(results_window, columns=(col1, col2), show="headings")
    tree.heading(col1, text=col1)
    tree.heading(col2, text=col2)

    for row in results:
        tree.insert("", "end", values=row)

    tree.pack(fill="both", expand=True)


def setup_admin_frame():
    ttk.Label(admin_frame, text="Admin Dashboard", font=("Arial", 16, "bold")).pack(pady=10)

    ttk.Label(admin_frame, text="Select a functionality:").pack(pady=5)
    functionalities = [
        "1. Create a table for the 'Student' entity",
        "2. Alter the 'Course' table to add a new attribute, 'Prerequisite'",
        "3. Insert a new student record",
        "4. Update the course name",
        "5. Delete a graduated student record",
        "6. Find average grade of students in a course",
        "7. Count total number of students in each department",
        "8. List students and their courses (using inner join)",
        "9. List all professors and courses (using left join)",
        "10. List students who enrolled after a specific date",
        "11. Find number of days remaining until a project's submission deadline"
    ]

    selected_functionality = tk.StringVar()
    functionality_combo = ttk.Combobox(admin_frame, textvariable=selected_functionality, values=functionalities, width=70)
    functionality_combo.pack(pady=5)

    def on_execute():
        selected_option = functionality_combo.get()
        if selected_option:
            execute_sql_query(selected_option)

    ttk.Button(admin_frame, text="Execute", command=on_execute).pack(pady=10)
    ttk.Button(admin_frame, text="Back", command=lambda: show_frame(main_frame)).pack(pady=10)


    def view_courses():
        # Clear previous content in the courses_frame
        for widget in courses_frame.winfo_children():
            widget.destroy()

        connection = db_connect()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT course_id, course_name, credits FROM courses")
                courses = cursor.fetchall()

                tree = ttk.Treeview(courses_frame, columns=("Course ID", "Course Name", "Credits"), show="headings")
                tree.heading("Course ID", text="Course ID")
                tree.heading("Course Name", text="Course Name")
                tree.heading("Credits",text = "Credits")
                for course in courses:
                    tree.insert("", "end", values=course)
                tree.pack(fill="both", expand=True)

                ttk.Button(courses_frame, text="Back", command=lambda: show_frame(admin_frame)).pack(pady=10)
                show_frame(courses_frame)
            except db.DatabaseError as e:
                messagebox.showerror("Database Error", f"Error executing SQL:\n{str(e)}")
            finally:
                cursor.close()
                connection.close()

    def view_student_info():
        # Clear previous content in the view_student_frame
        for widget in view_student_frame.winfo_children():
            widget.destroy()

        connection = db_connect()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT student_id, student_name, email, phone_no FROM students")
                students = cursor.fetchall()

                tree = ttk.Treeview(view_student_frame, columns=("Student ID", "Student Name", "Email", "Phone No"), show="headings")
                tree.heading("Student ID", text="Student ID")
                tree.heading("Student Name", text="Student Name")
                tree.heading("Email", text="Email")
                tree.heading("Phone No", text="Phone No")
                for student in students:
                    tree.insert("", "end", values=student)
                tree.pack(fill="both", expand=True)

                ttk.Button(view_student_frame, text="Back", command=lambda: show_frame(admin_frame)).pack(pady=10)
                show_frame(view_student_frame)
            except db.DatabaseError as e:
                messagebox.showerror("Database Error", f"Error executing SQL:\n{str(e)}")
            finally:
                cursor.close()
                connection.close()

    def show_add_student_form():
        # Clear previous entries and show the add_student_frame
        for widget in add_student_frame.winfo_children():
            widget.destroy()

        ttk.Label(add_student_frame, text="Add Student Details", font=("Arial", 16, "bold")).pack(pady=10)

        ttk.Label(add_student_frame, text="Student ID:").pack(pady=5)
        student_id_entry = ttk.Entry(add_student_frame, width=25)
        student_id_entry.pack(pady=5)

        ttk.Label(add_student_frame, text="Student Name:").pack(pady=5)
        student_name_entry = ttk.Entry(add_student_frame, width=25)
        student_name_entry.pack(pady=5)

        ttk.Label(add_student_frame, text="Email:").pack(pady=5)
        email_entry = ttk.Entry(add_student_frame, width=25)
        email_entry.pack(pady=5)

        ttk.Label(add_student_frame, text="Phone Number:").pack(pady=5)
        phone_no_entry = ttk.Entry(add_student_frame, width=25)
        phone_no_entry.pack(pady=5)

        def add_student():
            student_id = student_id_entry.get()
            student_name = student_name_entry.get()
            email = email_entry.get()
            phone_no = phone_no_entry.get()

            if not student_id or not student_name:
                messagebox.showwarning("Input Error", "Student ID and Name are required.")
                return

            try:
                phone_no_int = int(phone_no)  # Validate phone number as integer
            except ValueError:
                messagebox.showwarning("Input Error", "Phone Number must be a valid number.")
                return

            connection = db_connect()
            if connection:
                cursor = connection.cursor()
                try:
                    cursor.execute(
                        "INSERT INTO students (student_id, student_name, email, phone_no) VALUES (:1, :2, :3, :4)",
                        (student_id, student_name, email, phone_no_int)
                    )
                    connection.commit()
                    messagebox.showinfo("Success", "Student added successfully!")
                    show_frame(admin_frame)
                except db.DatabaseError as e:
                    messagebox.showerror("Database Error", f"Error executing SQL:\n{str(e)}")
                finally:
                    cursor.close()
                    connection.close()

        ttk.Button(add_student_frame, text="Add Student", command=add_student).pack(pady=10)
        ttk.Button(add_student_frame, text="Back", command=lambda: show_frame(admin_frame)).pack(pady=10)

        show_frame(add_student_frame)

    def show_add_course_form():
    # Clear previous entries and show the add_course_frame
        for widget in add_course_frame.winfo_children():
            widget.destroy()

        ttk.Label(add_course_frame, text="Add Course Details", font=("Arial", 16, "bold")).pack(pady=10)

        # Course ID
        ttk.Label(add_course_frame, text="Course ID:").pack(pady=5)
        course_id_entry = ttk.Entry(add_course_frame, width=25)
        course_id_entry.pack(pady=5)

        # Course Name
        ttk.Label(add_course_frame, text="Course Name:").pack(pady=5)
        course_name_entry = ttk.Entry(add_course_frame, width=25)
        course_name_entry.pack(pady=5)

        # Credits
        ttk.Label(add_course_frame, text="Credits:").pack(pady=5)
        credits_entry = ttk.Entry(add_course_frame, width=25)
        credits_entry.pack(pady=5)

        # Department ID
        ttk.Label(add_course_frame, text="Department ID:").pack(pady=5)
        department_id_entry = ttk.Entry(add_course_frame, width=25)
        department_id_entry.pack(pady=5)

        def add_course():
            course_id = course_id_entry.get()
            course_name = course_name_entry.get()
            credits = credits_entry.get()
            department_id = department_id_entry.get()

            # Validate input
            if not course_id or not course_name or not credits or not department_id:
                messagebox.showwarning("Input Error", "All fields are required.")
                return

            try:
                credits = int(credits)  # Ensure credits is an integer
                department_id = int(department_id)  # Ensure department_id is an integer
            except ValueError:
                messagebox.showwarning("Input Error", "Credits and Department ID must be valid integers.")
                return

            # Insert into the database
            connection = db_connect()
            if connection:
                cursor = connection.cursor()
                try:
                    cursor.execute(
                        """
                        INSERT INTO courses (course_id, course_name, credits, department_id)
                        VALUES (:1, :2, :3, :4)
                        """,
                        (course_id, course_name, credits, department_id)
                    )
                    connection.commit()
                    messagebox.showinfo("Success", "Course added successfully!")
                    show_frame(admin_frame)
                except db.DatabaseError as e:
                    messagebox.showerror("Database Error", f"Error executing SQL:\n{str(e)}")
                finally:
                    cursor.close()
                    connection.close()

        ttk.Button(add_course_frame, text="Add Course", command=add_course).pack(pady=10)
        ttk.Button(add_course_frame, text="Back", command=lambda: show_frame(admin_frame)).pack(pady=10)

    show_frame(add_course_frame)
    def show_delete_course_form():
        # Clear previous entries and show the delete_course_frame
        for widget in delete_course_frame.winfo_children():
            widget.destroy()

        ttk.Label(delete_course_frame, text="Delete Course", font=("Arial", 16, "bold")).pack(pady=10)
        ttk.Label(delete_course_frame, text="Course ID:").pack(pady=5)
        delete_course_id_entry = ttk.Entry(delete_course_frame, width=25)
        delete_course_id_entry.pack(pady=5)

        def delete_course():
            course_id = delete_course_id_entry.get()

            if not course_id:
                messagebox.showwarning("Input Error", "Course ID is required.")
                return

            connection = db_connect()
            if connection:
                cursor = connection.cursor()
                try:
                    cursor.execute("DELETE FROM courses WHERE course_id = :1", (course_id,))
                    if cursor.rowcount == 0:
                        messagebox.showwarning("Not Found", f"No course found with ID {course_id}")
                    else:
                        connection.commit()
                        messagebox.showinfo("Success", f"Course {course_id} deleted successfully!")
                    show_frame(admin_frame)
                except db.DatabaseError as e:
                    messagebox.showerror("Database Error", f"Error executing SQL:\n{str(e)}")
                finally:
                    cursor.close()
                    connection.close()

        ttk.Button(delete_course_frame, text="Delete Course", command=delete_course).pack(pady=10)
        ttk.Button(delete_course_frame, text="Back", command=lambda: show_frame(admin_frame)).pack(pady=10)

        show_frame(delete_course_frame)

    ttk.Button(admin_frame, text="View Courses", command=view_courses).pack(pady=10)
    ttk.Button(admin_frame, text="View Student Info", command=view_student_info).pack(pady=10)
    ttk.Button(admin_frame, text="Add Course", command=show_add_course_form).pack(pady=10)
    ttk.Button(admin_frame, text="Delete Course", command=show_delete_course_form).pack(pady=10)
    ttk.Button(admin_frame, text="Add Student", command=show_add_student_form).pack(pady=10)
    ttk.Button(admin_frame, text="Back", command=lambda: show_frame(main_frame)).pack(pady=10)

# Set up each frame and show the main frame initially
setup_main_frame()
setup_student_frame()
setup_admin_frame()
show_frame(main_frame)

root.mainloop()
