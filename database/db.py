
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "resolveai.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT UNIQUE NOT NULL,
                customer_name TEXT NOT NULL,
                customer_email TEXT,
                issue TEXT NOT NULL,
                category TEXT DEFAULT 'Unclassified',
                sentiment TEXT DEFAULT 'Pending',
                priority TEXT DEFAULT 'Pending',
                status TEXT DEFAULT 'Open',
                ai_response TEXT,
                response_review TEXT DEFAULT 'Pending Review',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Add response_review to existing databases if missing.
        columns = [
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(tickets)"
            ).fetchall()
        ]

        if "response_review" not in columns:
            connection.execute("""
                ALTER TABLE tickets
                ADD COLUMN response_review TEXT DEFAULT 'Pending Review'
            """)


def create_ticket(ticket_id, customer_name, customer_email, issue):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO tickets
            (ticket_id, customer_name, customer_email, issue)
            VALUES (?, ?, ?, ?)
        """, (ticket_id, customer_name, customer_email, issue))


def get_all_tickets():
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT * FROM tickets
            ORDER BY created_at DESC
        """)
        return cursor.fetchall()


def get_ticket_by_id(ticket_id):
    with get_connection() as connection:
        return connection.execute("""
            SELECT
                id,
                ticket_id,
                customer_name,
                customer_email,
                issue,
                category,
                sentiment,
                priority,
                status,
                ai_response,
                created_at,
                response_review
            FROM tickets
            WHERE ticket_id = ?
        """, (ticket_id,)).fetchone()


def update_ticket_analysis(
    ticket_id, category, sentiment, priority, ai_response
):
    with get_connection() as connection:
        connection.execute("""
            UPDATE tickets
            SET category = ?,
                sentiment = ?,
                priority = ?,
                ai_response = ?
            WHERE ticket_id = ?
        """, (category, sentiment, priority, ai_response, ticket_id))


def update_response_review(ticket_id, review):
    allowed_reviews = ["Approved", "Changes Requested"]

    if review not in allowed_reviews:
        raise ValueError("Invalid response review status.")

    with get_connection() as connection:
        connection.execute("""
            UPDATE tickets
            SET response_review = ?
            WHERE ticket_id = ?
        """, (review, ticket_id))


def update_ticket_status(ticket_id, status):
    if status not in ["Open", "Resolved"]:
        raise ValueError("Invalid ticket status.")

    with get_connection() as connection:
        connection.execute("""
            UPDATE tickets
            SET status = ?
            WHERE ticket_id = ?
        """, (status, ticket_id))

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "resolveai.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT UNIQUE NOT NULL,
                customer_name TEXT NOT NULL,
                customer_email TEXT,
                issue TEXT NOT NULL,
                category TEXT DEFAULT 'Unclassified',
                sentiment TEXT DEFAULT 'Pending',
                priority TEXT DEFAULT 'Pending',
                status TEXT DEFAULT 'Open',
                ai_response TEXT,
                response_review TEXT DEFAULT 'Pending Review',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        columns = [
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(tickets)"
            ).fetchall()
        ]

        if "response_review" not in columns:
            connection.execute("""
                ALTER TABLE tickets
                ADD COLUMN response_review TEXT DEFAULT 'Pending Review'
            """)


def create_ticket(ticket_id, customer_name, customer_email, issue):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO tickets
            (ticket_id, customer_name, customer_email, issue)
            VALUES (?, ?, ?, ?)
        """, (ticket_id, customer_name, customer_email, issue))


def get_all_tickets():
    with get_connection() as connection:
        return connection.execute("""
            SELECT
                id,
                ticket_id,
                customer_name,
                customer_email,
                issue,
                category,
                sentiment,
                priority,
                status,
                ai_response,
                created_at,
                response_review
            FROM tickets
            ORDER BY created_at DESC
        """).fetchall()


def get_ticket_by_id(ticket_id):
    with get_connection() as connection:
        return connection.execute("""
            SELECT
                id,
                ticket_id,
                customer_name,
                customer_email,
                issue,
                category,
                sentiment,
                priority,
                status,
                ai_response,
                created_at,
                response_review
            FROM tickets
            WHERE ticket_id = ?
        """, (ticket_id,)).fetchone()


def update_ticket_analysis(
    ticket_id, category, sentiment, priority, ai_response
):
    with get_connection() as connection:
        connection.execute("""
            UPDATE tickets
            SET category = ?, sentiment = ?, priority = ?, ai_response = ?
            WHERE ticket_id = ?
        """, (category, sentiment, priority, ai_response, ticket_id))


def update_response_review(ticket_id, review):
    if review not in ["Approved", "Changes Requested"]:
        raise ValueError("Invalid response review status.")

    with get_connection() as connection:
        connection.execute("""
            UPDATE tickets
            SET response_review = ?
            WHERE ticket_id = ?
        """, (review, ticket_id))


def update_ticket_status(ticket_id, status):
    if status not in ["Open", "Resolved"]:
        raise ValueError("Invalid ticket status.")

    with get_connection() as connection:
        connection.execute("""
            UPDATE tickets
            SET status = ?
            WHERE ticket_id = ?
        """, (status, ticket_id))
