#!/usr/bin/env python3
"""Script to run Alembic migrations."""

import os
import sys

# Change to the backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(backend_dir)

# Set up the path
sys.path.insert(0, backend_dir)

from alembic.config import Config
from alembic import command

# Get the alembic.ini path
alembic_cfg = Config("alembic.ini")

# Run migration
print("Running migration upgrade to head...")
command.upgrade(alembic_cfg, "head")
print("Migration complete!")
