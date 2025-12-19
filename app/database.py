import sqlite3
from pathlib import Path

# Path to database file (../data/app.db relative to this file)
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "app.db"


def get_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # enables dict-like access
    return conn


def init_db():
    """Create tables if they do not exist."""
    conn = get_connection()
    cur = conn.cursor()

    # Projects table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT,
            name TEXT NOT NULL,
            description TEXT NOT NULL
        );
        """
    )

    # Clients table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            designation TEXT NOT NULL
        );
        """
    )

    # Contact form submissions
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            mobile TEXT NOT NULL,
            city TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    # Newsletter subscriptions
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS newsletter (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    conn.commit()
    conn.close()


# ---------- CRUD helper functions ----------

# Projects
def add_project(image_path, name, description):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO projects (image_path, name, description) VALUES (?, ?, ?)",
        (image_path, name, description),
    )
    conn.commit()
    conn.close()


def get_projects():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def update_project(project_id, image_path, name, description):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE projects
        SET image_path = ?, name = ?, description = ?
        WHERE id = ?
        """,
        (image_path, name, description, project_id),
    )
    conn.commit()
    conn.close()


def delete_project(project_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    conn.commit()
    conn.close()


# Clients
def add_client(image_path, name, description, designation):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO clients (image_path, name, description, designation)
        VALUES (?, ?, ?, ?)
        """,
        (image_path, name, description, designation),
    )
    conn.commit()
    conn.close()


def get_clients():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def update_client(client_id, image_path, name, description, designation):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE clients
        SET image_path = ?, name = ?, description = ?, designation = ?
        WHERE id = ?
        """,
        (image_path, name, description, designation, client_id),
    )
    conn.commit()
    conn.close()


def delete_client(client_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM clients WHERE id = ?", (client_id,))
    conn.commit()
    conn.close()


# Contacts
def add_contact(full_name, email, mobile, city):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO contacts (full_name, email, mobile, city)
        VALUES (?, ?, ?, ?)
        """,
        (full_name, email, mobile, city),
    )
    conn.commit()
    conn.close()


def get_contacts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


# Newsletter
def add_newsletter_email(email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO newsletter (email) VALUES (?)",
        (email,),
    )
    conn.commit()
    conn.close()


def get_newsletter_emails():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM newsletter ORDER BY subscribed_at DESC")
    rows = cur.fetchall()
    conn.close()
    return rows
