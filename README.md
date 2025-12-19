Copy-paste this single file as README.md:

 FLIPR Full-Stack Business Manager

FLIPR Full-Stack Business Manager is a local full-stack web application built using Python and Streamlit, with SQLite as the database.  
It provides a public landing page and an admin panel to manage projects, clients, contact form responses, and newsletter subscriptions.

---

 1. System Requirements

 Operating System
- Windows 10 / 11 (tested)
- macOS / Linux (Python required)

 Python
- Version 3.8 or higher
- Developed and tested with Python 3.13.6

 Hardware
- Minimum 4 GB RAM
- ~200 MB free disk space (Python, virtual environment, database, images)

 Network
- Internet connection required only to install dependencies
- Application runs locally at: http://localhost:8501

 Optional Tools
- Visual Studio Code (or any editor)
- Git

---

 2. Python Dependencies

Install the required packages:

pip install streamlit
pip install pillow


streamlit – Web UI framework for landing page and admin panel

pillow – Image loading and display

SQLite is used via Python’s built-in sqlite3 module. No separate installation required.

3. Environment Setup
3.1 Clone or Download the Project
git clone <YOUR_REPOSITORY_URL> FLIPR_Full-Stack_Business_Manager
cd FLIPR_Full-Stack_Business_Manager


Replace <YOUR_REPOSITORY_URL> with your repository URL.

3.2 Create a Virtual Environment

Windows

python -m venv venv
venv\Scripts\activate


macOS / Linux

python3 -m venv venv
source venv/bin/activate


(venv) should appear in the terminal after activation.

3.3 Install Dependencies
pip install streamlit
pip install pillow

4. Project Structure and Database

Expected structure:

FLIPR_Full-Stack_Business_Manager/
├─ main.py
├─ app/
│  ├─ __init__.py
│  ├─ database.py
│  ├─ landing_page.py
│  └─ admin_panel.py
├─ data/
│  └─ app.db
└─ assets/


If missing, create folders:

mkdir data
mkdir assets


app.db is created automatically on first run.

5. Running the Application
Step 1: Activate Virtual Environment

Windows:

venv\Scripts\activate


macOS / Linux:

source venv/bin/activate

Step 2: Run the App

From the project root:

streamlit run main.py

Step 3: Open in Browser

If it doesn’t open automatically:

http://localhost:8501

6. Application Usage
Sidebar

Landing Page – Public landing page

Admin Panel – Admin login and management

Admin Login

Any email

Any password

Correct captcha

Click Login

Admin Panel Features

Add / Edit / Delete / View projects

Add / Edit / Delete / View clients

View contact form responses

View newsletter subscribers

7. Stop the Application

Press:

Ctrl + C


To run again:

Activate the virtual environment

Run streamlit run main.py

8. Notes

No external database server required

Streamlit auto-updates UI when backend logic changes

Charts and UI elements are generated automatically
