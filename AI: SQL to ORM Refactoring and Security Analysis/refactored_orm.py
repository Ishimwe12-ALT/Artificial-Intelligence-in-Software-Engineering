"""
refactored_orm.py
-----------------
SQLAlchemy 2.0 ORM refactoring of original_raw_sql.py.
Generated with Google Gemini and reviewed by me.

Requirements:
    pip install sqlalchemy mysql-connector-python

Set credentials as environment variables before running (recommended):
    export DB_USER=root
    export DB_PASSWORD=your_real_password
    export DB_HOST=localhost
    export DB_NAME=example_db
"""

import os
from typing import List, Optional

from sqlalchemy import String, create_engine, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session

# ----------------------------------------------------------------------
# 1. Database Connection & Engine Setup
# ----------------------------------------------------------------------
# Securely fetch credentials from environment variables with fallbacks
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "yourpassword")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "example_db")

# Construct MySQL connection string using the mysqlconnector driver
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Create the engine and session factory
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# ----------------------------------------------------------------------
# 2. Declarative Model Definition
# ----------------------------------------------------------------------
class Base(DeclarativeBase):
    """Base class for SQLAlchemy models using DeclarativeBase."""
    pass


class User(Base):
    """Declarative model mapping to the 'users' table."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


# ----------------------------------------------------------------------
# 3. Schema Management
# ----------------------------------------------------------------------
def init_db() -> None:
    """Create tables if they do not exist."""
    Base.metadata.create_all(engine)


# ----------------------------------------------------------------------
# 4. Refactored CRUD Operations
# ----------------------------------------------------------------------
def create_user(session: Session, username: str, email: str) -> Optional[User]:
    """Create and persist a new user inside an active session."""
    if not username or not email:
        print("Validation Error: Username and email are required.")
        return None

    try:
        new_user = User(username=username, email=email)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        print(f"User '{username}' created successfully with ID {new_user.id}.")
        return new_user
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database Error creating user '{username}': {e}")
        return None


def get_user_by_username(session: Session, username: str) -> Optional[User]:
    """Retrieve a single user by username."""
    try:
        stmt = select(User).where(User.username == username)
        return session.scalar(stmt)
    except SQLAlchemyError as e:
        print(f"Database Error querying user '{username}': {e}")
        return None


def update_user_email(session: Session, username: str, new_email: str) -> bool:
    """Update the email address for an existing user."""
    if not new_email:
        print("Validation Error: New email is required.")
        return False

    user = get_user_by_username(session, username)
    if not user:
        print(f"Update failed: User '{username}' not found.")
        return False

    try:
        user.email = new_email
        session.commit()
        print(f"Successfully updated email for user '{username}'.")
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database Error updating email for user '{username}': {e}")
        return False


def delete_user(session: Session, username: str) -> bool:
    """Delete a user record by username."""
    user = get_user_by_username(session, username)
    if not user:
        print(f"Delete failed: User '{username}' not found.")
        return False

    try:
        session.delete(user)
        session.commit()
        print(f"Successfully deleted user '{username}'.")
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database Error deleting user '{username}': {e}")
        return False


def list_users(session: Session) -> List[User]:
    """Retrieve and return all users from the database."""
    try:
        stmt = select(User)
        users = list(session.scalars(stmt).all())
        return users
    except SQLAlchemyError as e:
        print(f"Database Error fetching users: {e}")
        return []


# ----------------------------------------------------------------------
# 5. End-to-End Workflow Execution
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Initialize table schema
    init_db()

    # Manage session lifecycle with a context manager
    with SessionLocal() as session:
        print("--- 1. Creating Users ---")
        create_user(session, "alice_dev", "alice@example.com")
        create_user(session, "bob_coder", "bob@example.com")

        print("\n--- 2. Querying User ---")
        user = get_user_by_username(session, "alice_dev")
        print(f"Fetched User: {user}")

        print("\n--- 3. Listing All Users ---")
        all_users = list_users(session)
        for u in all_users:
            print(u)

        print("\n--- 4. Updating User Email ---")
        update_user_email(session, "alice_dev", "alice_new@example.com")

        print("\n--- 5. Listing Users After Update ---")
        for u in list_users(session):
            print(u)

        print("\n--- 6. Deleting User ---")
        delete_user(session, "bob_coder")

        print("\n--- 7. Final User List ---")
        for u in list_users(session):
            print(u)
