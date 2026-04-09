#!/usr/bin/env python3
"""
Firebase Sample Data Seeder for FreelanceMax
=============================================

This script populates Firebase Firestore with sample users and schedules
for testing the FreelanceMax application.

Usage:
    python seed_firebase.py
"""

import json
import os
from datetime import datetime, timedelta
from firebase_config import db, auth
import firebase_admin
from firebase_admin import auth as firebase_auth

def create_sample_users():
    """Create sample user accounts in Firebase Auth and Firestore"""
    print("👥 Creating sample users...")

    sample_users = [
        {
            "email": "freelancer1@example.com",
            "password": "password123",
            "display_name": "Alex Johnson",
            "worker_type": "Web Developer"
        },
        {
            "email": "designer@example.com",
            "password": "password123",
            "display_name": "Sarah Chen",
            "worker_type": "UI/UX Designer"
        },
        {
            "email": "mobiledev@example.com",
            "password": "password123",
            "display_name": "Mike Rodriguez",
            "worker_type": "Mobile Developer"
        }
    ]

    created_users = []

    for user_data in sample_users:
        try:
            # Create user in Firebase Auth
            user = firebase_auth.create_user(
                email=user_data["email"],
                password=user_data["password"],
                display_name=user_data["display_name"]
            )

            # Create user document in Firestore
            user_doc = {
                "email": user_data["email"],
                "displayName": user_data["display_name"],
                "workerType": user_data["worker_type"],
                "createdAt": datetime.utcnow().isoformat(),
                "totalSchedules": 0,
                "totalProfit": 0
            }

            db.collection("users").document(user.uid).set(user_doc)

            created_users.append({
                "uid": user.uid,
                "email": user_data["email"],
                "display_name": user_data["display_name"]
            })

            print(f"  ✅ Created user: {user_data['display_name']} ({user_data['email']})")

        except Exception as e:
            print(f"  ❌ Failed to create user {user_data['email']}: {e}")

    return created_users

def create_sample_schedules(users):
    """Create sample schedules for the users"""
    print("\n📅 Creating sample schedules...")

    # Load sample jobs
    try:
        with open('sample_jobs.json', 'r') as f:
            sample_jobs = json.load(f)
    except FileNotFoundError:
        print("❌ sample_jobs.json not found. Run sample_loader.py first.")
        return

    # Create schedules for each user
    for user in users:
        uid = user["uid"]
        user_name = user["display_name"]

        # Select random subset of jobs for this user
        import random
        num_jobs = random.randint(3, 8)
        selected_jobs = random.sample(sample_jobs, num_jobs)

        # Prepare jobs for scheduler
        from scheduler_cpp_wrapper import schedule_jobs

        prepared_jobs = []
        for job in selected_jobs:
            prepared_job = {
                'id': job['id'],
                'job_type': job['job_type'],
                'name': job['name'],
                'deadline': job['deadline'],
                'profit': job['profit'],
                'days_deadline': 7  # Simplified for demo
            }
            prepared_jobs.append(prepared_job)

        # Run scheduling
        try:
            result = schedule_jobs(prepared_jobs)

            # Save schedule to Firestore
            schedule_data = {
                "userId": uid,
                "workerType": user_name.split()[1] + " Work",  # Simple worker type
                "totalProfit": result["total_profit"],
                "totalSlots": len(result["scheduled"]),
                "scheduledJobs": result["scheduled"],
                "skippedJobs": [{"id": j["id"], "name": j["name"], "profit": j["profit"]}
                               for j in result["skipped"]],
                "createdAt": datetime.utcnow().isoformat()
            }

            db.collection("schedules").add(schedule_data)

            print(f"  ✅ Created schedule for {user_name}: ₹{result['total_profit']} profit, {len(result['scheduled'])} jobs scheduled")

            # Update user stats
            user_ref = db.collection("users").document(uid)
            user_ref.update({
                "totalSchedules": firebase_admin.firestore.Increment(1),
                "totalProfit": firebase_admin.firestore.Increment(result["total_profit"])
            })

        except Exception as e:
            print(f"  ❌ Failed to create schedule for {user_name}: {e}")

def display_usage_info(users):
    """Display information about how to use the sample data"""
    print("\n🎯 SAMPLE DATA READY!")
    print("=" * 40)
    print("You can now test FreelanceMax with these accounts:")
    print()

    for user in users:
        print(f"📧 {user['email']}")
        print(f"🔑 Password: password123")
        print(f"👤 {user['display_name']}")
        print()

    print("🌐 Access your app at: http://localhost:9000")
    print("📱 Test login, dashboard, and scheduling features!")

def main():
    """Main function"""
    print("🚀 FreelanceMax Firebase Seeder")
    print("=" * 35)

    try:
        # Create sample users
        users = create_sample_users()

        if users:
            # Create sample schedules
            create_sample_schedules(users)

            # Display usage info
            display_usage_info(users)
        else:
            print("❌ No users were created. Check Firebase configuration.")

    except Exception as e:
        print(f"❌ Seeding failed: {e}")
        print("💡 Make sure Firebase is properly configured and you have admin privileges.")

if __name__ == "__main__":
    main()