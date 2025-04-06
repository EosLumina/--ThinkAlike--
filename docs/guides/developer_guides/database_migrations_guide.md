# Database Migrations Guide (Alembic & SQLAlchemy)

---

## 1. Introduction

This guide explains how to manage database schema changes (migrations) for the ThinkAlike project using **Alembic**, the standard database migration tool for **SQLAlchemy**. As the application evolves, the database schema defined in [`docs/architecture/database/unified_data_model_schema.md`](../../architecture/database/unified_data_model_schema.md) will inevitably need updates (adding tables, columns, constraints, etc.). Migrations provide a version-controlled, repeatable way to apply these changes across different environments (local development, staging, production).

This guide assumes:
*   The backend uses SQLAlchemy as the ORM.
*   Alembic is the chosen migration tool.
*   The target production database is PostgreSQL (though Alembic also supports SQLite used for local development).

---

## 2. Setting Up Alembic

If not already set up (check for an `alembic/` directory and an `alembic.ini` file in the project root or backend directory):

1.  **Install Alembic:** Ensure it's in your `requirements.txt` and install it in your virtual environment:
    ```bash
    pip install alembic
    ```
2.  **Initialize Alembic:** Navigate to your project root (or backend directory where `alembic.ini` should reside) in your terminal (with venv activated) and run:
    ```bash
    alembic init alembic
    ```
    This creates:
    *   `alembic/`: Directory containing migration scripts and environment setup.
    *   `alembic.ini`: Configuration file for Alembic.

3.  **Configure `alembic.ini`:**
    *   Set the `sqlalchemy.url` variable to point to your database. For flexibility across environments, it's best to read this from an environment variable (like `DATABASE_URL` used by the main app).
        ```ini
        # alembic.ini
        [alembic]
        # ... other settings ...
        script_location = alembic
        # Set sqlalchemy.url to read from environment variable
        sqlalchemy.url = %(DB_URL)s

        [loggers]
        # ... logger settings ...

        # Add section to read environment variable (adjust variable name if needed)
        [post_write_hooks]
        hooks = pythonpath

        [pythonpath]
        path = .

        [command_hooks]
        on_init = alembic_hooks:load_env

        [command_hooks.load_env]
        type = generic
        fn = alembic_hooks:load_dotenv_if_present
        ```
    *   You might need a small helper script (e.g., `alembic_hooks.py`) to load `.env` if Alembic doesn't pick it up automatically, or set the `DB_URL` environment variable manually before running Alembic commands. Alternatively, modify `alembic/env.py` directly (see next step).

4.  **Configure `alembic/env.py`:** This file connects Alembic to your SQLAlchemy models.
    *   **Import Models:** Ensure your SQLAlchemy models (defined perhaps in `app/models/` or `app/db/models.py`) are imported or accessible within `env.py`. You need to point Alembic to your metadata.
        *   Find the line `target_metadata = None` and replace it.
        *   Import your base declarative class (e.g., `from app.db.base_class import Base`) and set `target_metadata = Base.metadata`.
        *   You might need to adjust Python paths so Alembic can find your `app` module (e.g., add `sys.path.append(os.path.join(config.config_file_dir, '..'))`).
    *   **Database URL:** Configure how Alembic gets the database URL. You can read it from the `.ini` file (which reads from env vars as configured above) or set it directly here from `os.environ.get('DATABASE_URL')`. Modify the `run_migrations_online` function:
        ```python
        # alembic/env.py
        import os
        from logging.config import fileConfig
        from sqlalchemy import engine_from_config, pool
        from alembic import context
        # Add imports for your models/Base
        from app.db.base_class import Base # Adjust import path as necessary
        import sys
        # Ensure app directory is in path if needed
        # sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..')) # Example

        # this is the Alembic Config object, which provides
        # access to the values within the .ini file in use.
        config = context.config

        # Interpret the config file for Python logging.
        # This line sets up loggers basically.
        if config.config_file_name is not None:
            fileConfig(config.config_file_name)

        # add your model's MetaData object here
        # for 'autogenerate' support
        # from myapp import mymodel
        # target_metadata = mymodel.Base.metadata
        target_metadata = Base.metadata # <-- SET YOUR METADATA HERE

        def get_database_url():
            # Prioritize environment variable
            db_url = os.environ.get("DATABASE_URL")
            if db_url:
                # Example fix for Render URLs that might lack driver prefix
                # if db_url.startswith("postgres://"):
                #     db_url = db_url.replace("postgres://", "postgresql://", 1)
                return db_url
            return config.get_main_option("sqlalchemy.url")

        def run_migrations_offline() -> None:
            """Run migrations in 'offline' mode."""
            url = get_database_url()
            context.configure(
                url=url,
                target_metadata=target_metadata,
                literal_binds=True,
                dialect_opts={"paramstyle": "named"},
            )

            with context.begin_transaction():
                context.run_migrations()

        def run_migrations_online() -> None:
            """Run migrations in 'online' mode."""
            configuration = config.get_section(config.config_ini_section)
            configuration['sqlalchemy.url'] = get_database_url()
            connectable = engine_from_config(
                configuration,
                prefix="sqlalchemy.",
                poolclass=pool.NullPool,
            )

            with connectable.connect() as connection:
                context.configure(
                    connection=connection,
                    target_metadata=target_metadata,
                )

                with context.begin_transaction():
                    context.run_migrations()

        if context.is_offline_mode():
            run_migrations_offline()
        else:
            run_migrations_online()
        ```

---

## 3. Creating Migrations (Autogenerate)

Alembic can automatically detect changes between your SQLAlchemy models and the current database state.

1.  **Modify Models:** Make changes to your SQLAlchemy models in your Python code (e.g., add a new column to `models/user.py`).
2.  **Generate Migration Script:** Run the `revision` command with `--autogenerate`. Make sure your database is accessible and reflects the schema *before* your changes.
    ```bash
    alembic revision --autogenerate -m "Add bio column to profiles table"
    ```
3.  **Review Script:** Alembic creates a new file in `alembic/versions/`. **CRITICALLY REVIEW THIS SCRIPT.** Autogenerate is powerful but not perfect.
    *   Verify the `upgrade()` function contains the correct SQLAlchemy/SQL operations to apply your change.
    *   Verify the `downgrade()` function contains the correct operations to *reverse* the change.
    *   Manually add or modify operations if autogenerate missed something complex (e.g., data transformations, complex constraints).
4.  **Commit:** Commit the reviewed migration script along with your model changes.

---

## 4. Applying Migrations

1.  **Upgrade:** Apply pending migrations to upgrade the database to the latest version (or a specific version).
    ```bash
    alembic upgrade head
    ```
2.  **Downgrade:** Revert migrations (use cautiously, especially in production).
    ```bash
    alembic downgrade -1
    ```
3.  **Check History/Status:**
    ```bash
    alembic history --verbose
    alembic current
    ```

---

## 5. Workflow & Best Practices

*   **Development:**
    *   Modify models locally.
    *   Generate migration scripts (`alembic revision --autogenerate ...`).
    *   **Review scripts carefully.**
    *   Apply migrations locally (`alembic upgrade head`) to test them against your dev database (SQLite).
    *   Commit model changes and the migration script together.
*   **Production/Staging Deployment:**
    *   Deploy the updated code *first*.
    *   Run `alembic upgrade head` as a deployment step *after* code deployment but *before* the application starts serving traffic fully (or during a maintenance window if downtime is needed for complex migrations).
    *   **Never** run `--autogenerate` directly against a production database.
*   **Branching & Merging:** Migration scripts are linear. Handle merge conflicts in migration files carefully if multiple developers create migrations on different branches. Ensure a consistent linear history (`alembic history`). Use `alembic merge` if needed, but often simpler to coordinate or rebase.
*   **Downgrades:** Ensure `downgrade()` functions are correct and tested, but rely on backups as the primary recovery mechanism in production before attempting downgrades for complex schema changes.

---

By using Alembic consistently, you ensure that database schema changes are version-controlled, repeatable, and manageable across all development and deployment environments for the ThinkAlike project.
