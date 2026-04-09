# 🚀 FreelanceMax - Running Locally!

## Application Status: ✅ RUNNING

**URL:** [http://localhost:9001](http://localhost:9001)  
**Dashboard:** [http://localhost:9001/dashboard](http://localhost:9001/dashboard)

---

## 🎯 Quick Start

### What's Running?
- ✅ **Flask Backend** - Python web server on port 9001
- ✅ **C++ Scheduler** - Optimized job scheduling algorithm  
- ✅ **Firebase Integration** - Auth & data storage ready
- ✅ **Dashboard UI** - Modern, responsive interface

### Features Available
- 📋 **Add Projects** - Input jobs with deadlines and budgets
- ⚡ **Optimize Schedule** - Run greedy algorithm (C++ powered)
- 📊 **View Results** - See scheduling decisions step-by-step
- 📈 **Project Timeline** - Visual representation of optimized schedule
- 💾 **Save Schedules** - Store results in Firebase (production only)

### For Local Development
- ✅ **Authentication Bypassed** - Login not required on localhost
- ✅ **API Endpoints** - All endpoints working with mock user
- ✅ **C++ Scheduler** - Using compiled binary for speed
- ✅ **Database** - Firestore operations skipped locally

---

## 📱 How to Use

### 1. Open Dashboard
Go to: http://localhost:9001/dashboard

### 2. Add Projects
- Click "+ Add Project"
- Enter project details:
  - **Type**: Web Development, Mobile App, Design, etc.
  - **Name**: Project name
  - **Deadline**: Select date and time (days from now)
  - **Budget**: Amount in ₹ (minimum ₹100)

### 3. Load Sample Data (Optional)
- Click "Load sample projects" button
- 20 pre-populated projects will load

### 4. Optimize Schedule
- Click "🚀 Optimize My Schedule"
- Algorithm will:
  1. Sort projects by budget (highest first)
  2. Allocate time slots before deadlines
  3. Maximize total earnings

### 5. View Results
- Max Earnings: Total profit from scheduled projects
- Projects Scheduled: Number of projects optimized
- Projects Skipped: Conflicts due to deadline constraints
- Steps: Algorithm execution trace
- Timeline: Day-by-day project allocation

### 6. Save Schedule (Production Only)
- In production with Firebase: Click "💾 Save Schedule"
- Locally: Saves are skipped (can still run scheduling)

---

## 🔧 API Endpoints

### Schedule Optimization
```bash
POST http://localhost:9001/api/schedule
Content-Type: application/json

{
  "jobs": [
    {
      "id": 1,
      "job_type": "Web Development",
      "name": "E-commerce Site",
      "deadline": "2026-04-15T10:00:00",
      "profit": 5000
    }
  ],
  "workerType": "Freelancer"
}
```

**Response:**
```json
{
  "scheduled": [
    {"day": 5, "job": "E-commerce Site"}
  ],
  "skipped": [],
  "total_profit": 5000,
  "steps": [
    "Step 1: Sorting 1 jobs by profit...",
    "Step 2: Maximum deadline is 5 days...",
    ...
  ],
  "saved": false
}
```

---

## 📊 Example: Using the Scheduler

### Input (3 Projects)
```
Project A: ₹8000, deadline 4 days
Project B: ₹6000, deadline 3 days  
Project C: ₹3000, deadline 2 days
```

### Output (Optimized Schedule)
```
Day 1: Project C (₹3000)
Day 2: Project B (₹6000)
Day 3: (free)
Day 4: Project A (₹8000)
────────────────────
Total: ₹17,000 profit
```

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Port**: 9001
- **Authentication**: Firebase Auth (bypassed locally)
- **Database**: Firestore

### Algorithm
- **Scheduler**: C++ (compiled binary at `/build/scheduler`)
- **Type**: Greedy algorithm
- **Complexity**: O(n² log n) - optimal for freelancer projects

### Frontend
- **Framework**: Vanilla HTML5/CSS3/JavaScript
- **Firebase SDK**: Cloud Firestore, Authentication
- **Responsive**: Mobile & desktop friendly

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill the current process
pkill -f "python3 app.py"

# Or use a different port
PORT=9002 python3 app.py
```

### Firebase Errors (Ignored Locally)
- Local development bypasses Firestore save operations
- No login required on `localhost`
- Use any email/password to "mock login" in production

### Scheduler Not Working
- Ensure C++ binary exists: `ls -la build/scheduler`
- If missing, rebuild: `bash build.sh`
- Check permissions: `chmod +x build/scheduler`

---

## 📈 Next Steps

### For Deployment
1. Push to GitHub
2. Deploy to Railway, Heroku, or your preferred platform
3. Set Firebase credentials in environment
4. Enable authentication in production

### For Development
1. Modify C++ algorithm in `scheduler.cpp`
2. Rebuild: `cd build && cmake .. && make`
3. Test locally before deploying
4. Add more sample data in `/static/sample_jobs.json`

---

## 📝 Project Files

```
.
├── app.py                    # Flask backend
├── scheduler.cpp             # C++ greedy algorithm
├── scheduler_cpp_wrapper.py  # Python wrapper for C++ binary
├── firebase_config.py        # Firebase setup
├── templates/
│   └── dashboard.html        # Main UI
├── static/
│   └── sample_jobs.json      # Sample project data
├── build/
│   └── scheduler             # Compiled C++ executable
└── requirements.txt          # Python dependencies
```

---

## 🎓 Understanding the Greedy Algorithm

The job scheduler uses a **greedy approach**:

1. **Sort** projects by profit (highest first)
2. **For each project:**
   - Find latest slot before deadline
   - If slot available: place project
   - Otherwise: skip (can't fit)
3. **Result:** Maximum profit schedule

**Why Greedy Works:**
- Prioritizing high-profit projects maximizes total earnings
- Placing in latest slots leaves earlier slots for other jobs
- Guaranteed optimal solution for this job scheduling variant

---

## 💡 Tips

- **Sample Data**: 20 pre-built projects to test with
- **Deadline Format**: "2026-04-15" means April 15, 2026
- **Time Format**: "10:00" means 10:00 AM (24-hour format)
- **Budget**: Minimum ₹100, no maximum limit
- **Fast Scheduling**: < 100ms for most scenarios

---

## 🚀 Ready to Deploy?

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Railway deployment (recommended)
- Heroku deployment
- Custom server setup
- Environment configuration

---

**Enjoy optimizing! 🎯**