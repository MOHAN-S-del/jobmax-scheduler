#!/usr/bin/env python3
"""
Quick Demo: Load Sample Jobs in FreelanceMax
==============================================

This script demonstrates how to load sample freelancer jobs
directly into your dashboard.

Usage:
    python demo_sample_jobs.py
"""

import json
import webbrowser
import time

def show_demo():
    """Show how to use sample jobs in the application"""
    print("🚀 FreelanceMax Sample Jobs Demo")
    print("=" * 40)

    # Load sample jobs
    try:
        with open('sample_jobs.json', 'r') as f:
            jobs = json.load(f)
    except FileNotFoundError:
        print("❌ sample_jobs.json not found!")
        return

    print(f"✅ Loaded {len(jobs)} sample freelancer jobs")
    print()

    # Show job categories
    categories = {}
    for job in jobs:
        cat = job['job_type']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(job)

    print("📂 Job Categories:")
    for cat, cat_jobs in categories.items():
        print(f"  • {cat}: {len(cat_jobs)} jobs")
    print()

    print("🎯 How to Use Sample Jobs:")
    print("1. Start your Flask server:")
    print("   source .venv/bin/activate")
    print("   SECRET_KEY='your-key' PORT=9090 python app.py")
    print()
    print("2. Open your browser to: http://localhost:9090")
    print()
    print("3. Login or register an account")
    print()
    print("4. In the dashboard, click 'Load sample projects'")
    print()
    print("5. You'll see 20 realistic freelancer jobs loaded!")
    print()

    print("💼 Sample Jobs Include:")
    for i, job in enumerate(jobs[:5], 1):  # Show first 5
        print(f"  {i}. {job['name']} ({job['job_type']}) - ₹{job['profit']}")
    print("  ... and 15 more!")
    print()

    print("🔄 Ready to test? Opening browser in 3 seconds...")
    time.sleep(3)

    # Try to open browser
    try:
        webbrowser.open('http://localhost:9090')
        print("🌐 Browser opened! Login and click 'Load sample projects'")
    except:
        print("🌐 Please open: http://localhost:9090")

if __name__ == "__main__":
    show_demo()