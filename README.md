Course Registration System 🎓
This Tkinter-based Course Registration System is a desktop application that enables students to register for courses, view enrollments, and allows administrators to manage courses, student records, and execute SQL queries. The system is built using Python, Tkinter for the GUI, and Oracle SQL (via cx_Oracle) as the database backend.

📌 Features
✅ User Authentication – Login & sign-up for Students, Professors, and Admins.
✅ Student Functionalities – Register for courses, view enrolled courses.
✅ Admin Functionalities – Manage courses, add/delete courses, view student details, and run SQL queries.
✅ Database Integration – Uses Oracle SQL for handling student, course, and registration data.
✅ GUI-Based Interface – Built with Tkinter, featuring an intuitive and user-friendly design.

🛠️ Tech Stack
Python – Tkinter for GUI, cx_Oracle for database connection, pandas for data handling.
Oracle SQL – Database management and query execution.
⚙️ Prerequisites
Before running the application, ensure the following:

1️⃣ Install Required Libraries
pip install cx_Oracle pandas

2️⃣ Set Up Oracle Database
You need the host address and service name of your Oracle Database. Run the following commands in SQL*Plus to retrieve them:

Get Oracle Host Address
SELECT UTL_INADDR.GET_HOST_ADDRESS FROM DUAL;

Get Oracle Service Name
SELECT SYS_CONTEXT('USERENV', 'SERVICE_NAME') FROM DUAL;

Use these details to configure the database connection in base.py and UI.py.

📂 Cloning the Repository
To get started, clone the repository from GitHub:

git clone https://github.com/KishoreLOL21/Course_Registration_Application.git
cd Course_Registration_Application

🚀 Running the Application
1️⃣ Configure Database Connection
Update base.py and UI.py with your Oracle database credentials (user, password, host, and service name).

2️⃣ Run the Application
python UI.py
This will launch the Course Registration System, where users can log in and interact with the system.

📂 Project Structure
UI.py → Graphical User Interface (Tkinter) & user interactions.
base.py → Database setup, table creation, and sample data insertion.
Schema.pu -> Aditional DB Setup

🔧 Future Enhancements
🔹 Implement role-based access control for better security.
🔹 Add course prerequisites handling for structured registrations.
🔹 Improve UI with advanced Tkinter styling & validation.🚀


