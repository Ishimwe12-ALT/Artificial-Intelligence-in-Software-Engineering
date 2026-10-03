"""
original_raw_sql.py
-------------------
Initial (procedural) version of the user-management script, built on
mysql.connector and raw SQL strings.

NOTE: The assignment only showed get_connection() and create_user().
The remaining functions (get_user_by_username, update_user_email,
delete_user, list_users) were elided with "...", so they are written here
in the same style (parameterized queries, manual cursors, manual commits)
so the CRUD set is complete and comparable with the ORM version.
"""

import mysql.connector
from mysql.connector import Error


def get_connection():
    """Establish and return a database connection."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",  # hardcoded credential (bad practice)
        database="example_db",
    )


def create_user(db_cursor, username, email):
    """Create a new user safely using parameterized queries."""
    if not username or not email:
        print("Username and email are required.")
        return
    sql = "INSERT INTO users (username, email) VALUES (%s, %s)"
    try:
        db_cursor.execute(sql, (username, email))
        print(f"User '{username}' created successfully.")
    except Error as e:
        print(f"Error creating user: {e}")


def get_user_by_username(db_cursor, username):
    """Return a single user row (tuple) or None."""
    sql = "SELECT id, username, email FROM users WHERE username = %s"
    try:
        db_cursor.execute(sql, (username,))
        return db_cursor.fetchone()  # tuple: row[0]=id, row[1]=username, row[2]=email
    except Error as e:
        print(f"Error fetching user: {e}")
        return None


def update_user_email(db_cursor, username, new_email):
    """Update the email of an existing user."""
    if not new_email:
        print("New email is required.")
        return
    sql = "UPDATE users SET email = %s WHERE username = %s"
    try:
        db_cursor.execute(sql, (new_email, username))
        if db_cursor.rowcount == 0:
            print(f"User '{username}' not found.")
        else:
            print(f"Email updated for user '{username}'.")
    except Error as e:
        print(f"Error updating email: {e}")


def delete_user(db_cursor, username):
    """Delete a user by username."""
    sql = "DELETE FROM users WHERE username = %s"
    try:
        db_cursor.execute(sql, (username,))
        if db_cursor.rowcount == 0:
            print(f"User '{username}' not found.")
        else:
            print(f"User '{username}' deleted.")
    except Error as e:
        print(f"Error deleting user: {e}")


def list_users(db_cursor):
    """Return all users as a list of tuples."""
    sql = "SELECT id, username, email FROM users"
    try:
        db_cursor.execute(sql)
        return db_cursor.fetchall()
    except Error as e:
        print(f"Error listing users: {e}")
        return []


if __name__ == "__main__":
    # The table must already exist (created manually with a separate .sql script):
    #   CREATE TABLE users (
    #       id INT AUTO_INCREMENT PRIMARY KEY,
    #       username VARCHAR(50) NOT NULL UNIQUE,
    #       email VARCHAR(100) NOT NULL UNIQUE
    #   );
    connection = get_connection()
    cursor = connection.cursor()
    try:
        create_user(cursor, "alice_dev", "alice@example.com")
        create_user(cursor, "bob_coder", "bob@example.com")
        connection.commit()  # must be called manually, or nothing is saved

        print(get_user_by_username(cursor, "alice_dev"))

        update_user_email(cursor, "alice_dev", "alice_new@example.com")
        connection.commit()

        for row in list_users(cursor):
            print(f"ID={row[0]}, username={row[1]}, email={row[2]}")  # index-based access

        delete_user(cursor, "bob_coder")
        connection.commit()
    finally:
        cursor.close()      # manual cleanup
        connection.close()  # manual cleanup
