"""Test script for notifications API."""
import requests
import uuid
from datetime import datetime

# Database test
from sqlmodel import Session, select
from app.core.database import engine
from app.models.notification import Notification, NotificationType
from app.models.user import User

BASE_URL = "http://localhost:8000/api"
# Use dev mode token for auth (mapped in firebase.py)
HEADERS = {"Authorization": "Bearer dev-admin-001"}

# First, create a test notification directly in DB
print("Creating test notification in database...")
with Session(engine) as session:
    # Get admin user
    admin = session.exec(select(User).where(User.email == "admin@lamc.edu")).first()
    faculty = session.exec(select(User).where(User.email == "faculty@lamc.edu")).first()

    if admin and faculty:
        # Create test notification
        notif = Notification(
            user_id=admin.id,
            actor_id=faculty.id,
            type=NotificationType.COURSE_SUBMITTED,
            title="Course Submitted for Review",
            message="MATH 261 - Calculus I has been submitted for review.",
            entity_type="Course",
            entity_title="MATH 261 - Calculus I",
        )
        session.add(notif)
        session.commit()
        print(f"Created notification: {notif.id}")
    else:
        print(f"Users not found: admin={admin}, faculty={faculty}")

# Test counts endpoint
print("\nTesting GET /notifications/counts...")
r = requests.get(f"{BASE_URL}/notifications/counts", headers=HEADERS)
print(f"Status: {r.status_code}")
print(f"Response: {r.json()}")

# Test list endpoint
print("\nTesting GET /notifications...")
r = requests.get(f"{BASE_URL}/notifications", headers=HEADERS)
print(f"Status: {r.status_code}")
data = r.json()
if data:
    print(f"Found {len(data)} notification(s)")
    for n in data[:3]:
        print(f"  - {n['title']}: {n['message'][:50]}...")
else:
    print("No notifications found")

# Test mark as read
if data:
    notif_id = data[0]['id']
    print(f"\nTesting PATCH /notifications/{notif_id}/read...")
    r = requests.patch(f"{BASE_URL}/notifications/{notif_id}/read", headers=HEADERS)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")

    # Verify count updated
    print("\nVerifying counts after mark read...")
    r = requests.get(f"{BASE_URL}/notifications/counts", headers=HEADERS)
    print(f"Counts: {r.json()}")

print("\nNotifications API test complete!")
