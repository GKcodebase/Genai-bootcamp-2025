# alembic/env.py

from __future__ import print_function
import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Add the path to your app folder so we can import your models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

# Import the models and Base class
from app.models import Base  # Make sure this is the correct path for your models

# Get the Alembic configuration and connect to the database
config = context.config

# Set the SQLAlchemy URL
config.set_main_option("sqlalchemy.url", "sqlite:///./words.db")  # Update this to your database URL

# Import the `target_metadata` from the models file
target_metadata = Base.metadata  # Set this to Base.metadata

# Configure logging (this is optional, just for logging during migrations)
fileConfig(config.config_file_name)

# Create the engine and connection (used by Alembic for migrations)
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Optional: compares column types during migrations
        )

        with context.begin_transaction():
            context.run_migrations()

# Call the function to run migrations when Alembic is invoked
if context.is_offline_mode():
    # Run migrations in offline mode (not using a live connection)
    context.configure(url=config.get_main_option("sqlalchemy.url"), target_metadata=target_metadata)
    context.run_migrations()
else:
    # Run migrations in online mode (using a live connection)
    run_migrations_online()
