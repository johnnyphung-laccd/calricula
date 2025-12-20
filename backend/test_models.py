#!/usr/bin/env python3
"""Test that all models can be imported correctly."""

from app.models import User, Course, Program, Department, Division
from app.models import UserRole, CourseStatus, ProgramType

print("All models imported successfully!")
print(f"User model: {User}")
print(f"Course model: {Course}")
print(f"Program model: {Program}")
print(f"UserRole enum values: {list(UserRole)}")
print(f"CourseStatus enum values: {list(CourseStatus)}")
