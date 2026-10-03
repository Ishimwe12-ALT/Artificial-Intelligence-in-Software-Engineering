# AI: SQL to ORM Refactoring and Security Analysis

## Overview

This task uses an AI assistant (Google Gemini) to refactor a procedural Python script that talks to MySQL through `mysql.connector` and raw SQL strings into a SQLAlchemy 2.0 ORM solution. I then reviewed the AI's output, tested my understanding of it, and analysed the security and maintainability benefits.

## Folder Contents

| File | Description |
|------|-------------|
| `original_raw_sql.py` | Initial script: `mysql.connector`, manual cursors, raw SQL, manual commits. The functions elided in the assignment (`get_user_by_username`, `update_user_email`, `delete_user`, `list_users`) were written in the same style so the CRUD set is complete. |
| `refactored_orm.py` | SQLAlchemy ORM version: declarative `User` model, engine and `sessionmaker`, `create_all`, session-based CRUD, and a runnable `main` block. |
| `README.md` | This documentation. |

## AI Interaction

**Tool used:** Google Gemini

**Prompt summary:** I supplied the original script and required the AI to:
1. Define a `User` class as a SQLAlchemy declarative model (`id`, unique and non-null `username`, unique and non-null `email`).
2. Set up the engine and `sessionmaker`, with credentials read from environment variables.
3. Create the table with `Base.metadata.create_all(engine)`.
4. Add a user with `session.add()` and `session.commit()`, with validation and `session.rollback()` on `SQLAlchemyError`.
5. Query the user by username with `select(User).where(...)`.
6. Rewrite `update_user_email`, `delete_user` and `list_users` with the ORM.
7. Include an end-to-end runnable example.
8. Explain in detail why the ORM is more professional and secure than raw SQL with string formatting (SQL injection, abstraction, portability, transactions, schema and constraints, boilerplate, testability and Alembic).

The full prompt and a screenshot of the AI's response are in the Google Doc submission.

## Key Differences: Raw SQL vs ORM

| Aspect | Original (`mysql.connector`) | Refactored (SQLAlchemy ORM) |
|--------|------------------------------|-----------------------------|
| Schema | Separate hand-written `CREATE TABLE` script | `User` model is the single source of truth; `create_all()` builds it |
| Queries | SQL strings written by hand | `select(User).where(User.username == name)` |
| Results | Tuples accessed by index (`row[0]`, `row[1]`) | Typed `User` objects (`user.username`) |
| Parameters | Developer must remember to use `%s` placeholders | Values are always sent as bound parameters |
| Transactions | Manual `commit()`, manual `rollback()` | Session tracks changes (Unit of Work); `commit()` / `rollback()` plus `with` block |
| Cleanup | Manual `cursor.close()` and `connection.close()` | `with SessionLocal() as session:` closes automatically |
| Credentials | Hardcoded in source | Read from environment variables |
| Portability | MySQL-specific placeholders and syntax | Change the connection URL to use PostgreSQL or SQLite |
| Migrations | Manual SQL scripts | Works with Alembic |

## Security and Professional Analysis

**SQL injection.** Injection happens when user input is concatenated or formatted into the SQL text (for example `f"... WHERE username = '{user_input}'"`), so input like `alice' OR '1'='1` changes the structure of the query. SQLAlchemy keeps the SQL structure and the data separate: `User.username == user_input` compiles to `WHERE users.username = %s` and the value is sent to the driver as a bound parameter, never as part of the SQL text.

*Honest note:* the original `create_user` already used a parameterized query, so it was not vulnerable. The risk in the raw-SQL approach is that safety depends on the developer remembering to use placeholders in every query. With the ORM, safe binding is the default behaviour.

**Other benefits:**
- **Maintainability:** schema, constraints and behaviour live in one class instead of being scattered across SQL strings.
- **Fewer errors:** no manual cursors, no index-based row access, no forgotten `commit()`. The original script saves nothing unless `connection.commit()` is called by hand.
- **Transaction safety:** one failed operation can be rolled back cleanly.
- **Constraint enforcement:** `unique=True` and `nullable=False` are declared in the model, and duplicates raise `IntegrityError`, which is caught and rolled back.
- **Portability, testability and migrations:** tests can use in-memory SQLite, and Alembic can generate migrations from model changes.

## Review Notes and Possible Improvements

Things I noticed while reviewing the AI's output:
- **Password fallback:** `os.getenv("DB_PASSWORD", "yourpassword")` still puts a default password in the source. In production the code should fail if the variable is missing.
- **Special characters:** the password is placed into the URL with an f-string; passwords with characters like `@` or `/` should be escaped with `sqlalchemy.engine.URL.create(...)`.
- **Rerunning the demo:** a second run hits the `UNIQUE` constraint for `alice_dev`. The error is caught and printed, and the session rolls back cleanly.
- **Email validation:** only checks for empty values; real email format validation would be a good addition.
- **Query rendering:** the AI's explanation shows `SELECT *`; SQLAlchemy actually lists each column explicitly. The key point still holds: the value is bound as a parameter.

## How to Run

```bash
pip install sqlalchemy mysql-connector-python

export DB_USER=root
export DB_PASSWORD=your_real_password
export DB_HOST=localhost
export DB_NAME=example_db

python refactored_orm.py
```

The database `example_db` must already exist (`CREATE DATABASE example_db;`). The `users` table is created automatically.

## Reflection

Moving from raw SQL to an ORM changes the unit of thinking from strings and rows to objects and attributes. In the raw version, the table structure exists only in a separate SQL script, and the Python code accesses results by position (`row[1]`), so renaming or reordering a column can break the code silently. In the ORM version the `User` class is the single definition: a typo like `user.usrname` fails immediately, and editors can autocomplete and type-check fields. Common mistakes in the original, such as forgetting `commit()`, forgetting to close cursors, or concatenating strings into a query, are handled by the Session and the `with` block. This makes the code easier to read, change and extend, because adding a column is one edit in the model (plus a migration) instead of hunting through every SQL string.

**Author:** Ishimwe
