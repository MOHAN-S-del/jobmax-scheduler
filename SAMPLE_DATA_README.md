# FreelanceMax Sample Data

This directory contains sample data and utilities to help you test the FreelanceMax job scheduling application.

## 📁 Files

- `sample_jobs.json` - 20 realistic freelancer job samples
- `sample_loader.py` - Python script to load and test sample jobs
- `seed_firebase.py` - Script to populate Firebase with test users and schedules
- `demo_sample_jobs.py` - Quick demo showing how to use sample jobs in the web interface
- `static/sample_jobs.json` - Web-accessible copy for dashboard loading

## 🚀 Quick Start

### 1. Test the Scheduler Algorithm

```bash
# Activate virtual environment
source .venv/bin/activate

# Run sample loader to test scheduling
python sample_loader.py
```

This will:
- Load 20 sample freelancer jobs
- Display job summaries by category
- Test the C++ scheduling algorithm
- Show scheduled vs skipped jobs

### 2. Populate Firebase with Test Data

```bash
# Seed Firebase with sample users and schedules
python seed_firebase.py
```

This creates:
- 3 sample user accounts in Firebase Auth
- User profiles in Firestore
- Sample schedules for each user

### 3. Load Sample Jobs in Dashboard

```bash
# Run the demo
python demo_sample_jobs.py

# Or manually:
# 1. Start server: SECRET_KEY='key' PORT=9090 python app.py
# 2. Visit: http://localhost:9090
# 3. Login and click "Load sample projects"
```

This loads all 20 sample jobs directly into your dashboard interface!

## 👥 Sample User Accounts

After running `seed_firebase.py`, you can login with:

| Email | Password | Name | Role |
|-------|----------|------|------|
| freelancer1@example.com | password123 | Alex Johnson | Web Developer |
| designer@example.com | password123 | Sarah Chen | UI/UX Designer |
| mobiledev@example.com | password123 | Mike Rodriguez | Mobile Developer |

## 💼 Sample Jobs Included

### Web Development (6 jobs)
- E-commerce Website Redesign - ₹2,500
- Portfolio Website for Photographer - ₹1,200
- Blog Platform with CMS - ₹2,200
- Real Estate Listing Site - ₹3,800
- Corporate Website with Animations - ₹3,300
- E-learning Platform - ₹4,500

### Mobile Apps (7 jobs)
- iOS Fitness Tracking App - ₹3,200
- Android Chat Application - ₹2,800
- Cross-platform Shopping App - ₹4,100
- Travel Planning App - ₹2,600
- Social Media Management App - ₹1,900
- Recipe Sharing App - ₹1,600
- Productivity Task Manager - ₹2,700

### UI/UX Design (7 jobs)
- Restaurant App Interface - ₹1,800
- Banking App Redesign - ₹3,500
- SaaS Dashboard Design - ₹2,900
- Educational Platform UI - ₹2,100
- Fintech App Interface - ₹4,200
- Healthcare App Design - ₹3,100
- Startup Landing Page - ₹1,400

## 🔧 Features Tested

✅ **Job Scheduling Algorithm** - Greedy optimization with deadlines
✅ **Firebase Authentication** - User login/registration
✅ **Firestore Database** - Data persistence
✅ **Real Date/Time Deadlines** - ISO datetime handling
✅ **Job Type Categorization** - Web, Mobile, Design
✅ **Budget Validation** - Minimum ₹100 per job
✅ **C++ Performance** - 7x faster than Python implementation

## 📊 Sample Output

Running `python sample_loader.py` shows:
```
📋 SAMPLE JOBS SUMMARY
==================================================

Web Development (6 jobs):
  • E-learning Platform - ₹4500 (Due: 2026-05-10, 32 days)
  • Real Estate Listing Site - ₹3800 (Due: 2026-04-30, 22 days)
  • Corporate Website with Animations - ₹3300 (Due: 2026-05-08, 30 days)
  • E-commerce Website Redesign - ₹2500 (Due: 2026-04-15, 7 days)
  • Blog Platform with CMS - ₹2200 (Due: 2026-04-28, 20 days)
  • Portfolio Website for Photographer - ₹1200 (Due: 2026-04-18, 10 days)

🔄 TESTING SCHEDULER ALGORITHM
==================================================
✅ Scheduling completed successfully!
💰 Total Profit: ₹xxxx
📅 Scheduled Jobs: X
⏭️  Skipped Jobs: Y
```

## 🐛 Troubleshooting

**Firebase Connection Issues:**
- Check `serviceAccountKey.json` is present
- Verify Firebase project configuration
- Ensure proper permissions

**Port Already in Use:**
- Try different ports: 5000, 8000, 9000, etc.
- Kill existing processes: `lsof -ti:PORT | xargs kill`

**Import Errors:**
- Activate virtual environment: `source .venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

## 🎯 Next Steps

1. **Test the Web Interface** - Login with sample accounts
2. **Create Custom Jobs** - Add your own projects
3. **Monitor Performance** - Compare C++ vs Python scheduling
4. **Explore Analytics** - Check schedule history and statistics

Happy freelancing! 🎉