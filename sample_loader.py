#!/usr/bin/env python3
"""
Sample Data Loader for FreelanceMax
====================================

This script loads sample freelancer jobs and tests the scheduling algorithm.
Run this to populate your application with realistic test data.

Usage:
    python sample_loader.py
"""

import json
import os
from datetime import datetime, timedelta
from scheduler_cpp_wrapper import schedule_jobs

def load_sample_jobs():
    """Load sample jobs from JSON file"""
    try:
        with open('sample_jobs.json', 'r') as f:
            jobs = json.load(f)
        print(f"✅ Loaded {len(jobs)} sample jobs from sample_jobs.json")
        return jobs
    except FileNotFoundError:
        print("❌ sample_jobs.json not found")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        return []

def calculate_days_until_deadline(deadline_str):
    """Calculate days until deadline from current date"""
    try:
        deadline = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
        now = datetime.now()
        days = (deadline - now).days
        return max(1, days)  # At least 1 day
    except ValueError:
        return 7  # Default fallback

def prepare_jobs_for_scheduler(jobs_data):
    """Convert JSON jobs to format expected by scheduler"""
    prepared_jobs = []
    for job in jobs_data:
        prepared_job = {
            'id': job['id'],
            'job_type': job['job_type'],
            'name': job['name'],
            'deadline': job['deadline'],
            'profit': job['profit'],
            'days_deadline': calculate_days_until_deadline(job['deadline'])
        }
        prepared_jobs.append(prepared_job)
    return prepared_jobs

def display_job_summary(jobs):
    """Display a summary of loaded jobs"""
    print("\n📋 SAMPLE JOBS SUMMARY")
    print("=" * 50)

    # Group by job type
    job_types = {}
    for job in jobs:
        jt = job['job_type']
        if jt not in job_types:
            job_types[jt] = []
        job_types[jt].append(job)

    for job_type, type_jobs in job_types.items():
        print(f"\n{job_type} ({len(type_jobs)} jobs):")
        for job in sorted(type_jobs, key=lambda x: x['profit'], reverse=True):
            deadline_date = job['deadline'][:10]  # Just date part
            days = calculate_days_until_deadline(job['deadline'])
            print(f"  • {job['name']} - ₹{job['profit']} (Due: {deadline_date}, {days} days)")

def test_scheduler(jobs_data):
    """Test the scheduling algorithm with sample data"""
    print("\n🔄 TESTING SCHEDULER ALGORITHM")
    print("=" * 50)

    # Prepare jobs for scheduler
    prepared_jobs = prepare_jobs_for_scheduler(jobs_data)

    # Run scheduling
    try:
        result = schedule_jobs(prepared_jobs)

        print("✅ Scheduling completed successfully!")
        print(f"💰 Total Profit: ₹{result['total_profit']}")
        print(f"📅 Scheduled Jobs: {len(result['scheduled'])}")
        print(f"⏭️  Skipped Jobs: {len(result['skipped'])}")

        if result['scheduled']:
            print("\n📅 SCHEDULED JOBS:")
            for slot, job_name in result['scheduled']:
                print(f"  Day {slot}: {job_name}")

        if result['skipped']:
            print("\n⏭️  SKIPPED JOBS:")
            for job in result['skipped']:
                print(f"  • {job['name']} (₹{job['profit']}) - Could not fit in schedule")

        return result

    except Exception as e:
        print(f"❌ Scheduling failed: {e}")
        return None

def main():
    """Main function"""
    print("🚀 FreelanceMax Sample Data Loader")
    print("=" * 40)

    # Load sample jobs
    jobs_data = load_sample_jobs()
    if not jobs_data:
        return

    # Display summary
    display_job_summary(jobs_data)

    # Test scheduler
    result = test_scheduler(jobs_data)

    if result:
        print("\n✅ Sample data loaded and tested successfully!")
        print("💡 You can now use these jobs to test your FreelanceMax application.")
        print("   Add them to your dashboard or use them for API testing.")

if __name__ == "__main__":
    main()