# JobMax — Greedy Job Scheduler
### Setup & Firebase Configuration Guide

---

## Project Structure

```
job-scheduler/
│
├── app.py                   ← Flask server (routes & API)
├── scheduler.py             ← Greedy algorithm (core logic)
├── firebase_config.py       ← Firebase Admin SDK setup
├── requirements.txt         ← Python dependencies
├── serviceAccountKey.json   ← Firebase key (DO NOT share)
│
├── templates/
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
│
└── static/
    └── (css/js if needed)
```

---

## Step 1 — Create Firebase Project

1. Go to https://console.firebase.google.com
2. Click **"Add project"** → name it `jobmax-scheduler`
3. Disable Google Analytics (not needed) → Click **"Create project"**

---

## Step 2 — Enable Firebase Authentication

1. In Firebase Console → click **"Authentication"** (left sidebar)
2. Click **"Get started"**
3. Under **Sign-in method**, enable:
   - ✅ **Email/Password**
   - ✅ **Google** (optional, for Google login)
4. Click **Save**

---

## Step 3 — Create Firestore Database

1. In Firebase Console → click **"Firestore Database"**
2. Click **"Create database"**
3. Choose **"Start in test mode"** (fine for college project)
4. Select a location → Click **"Enable"**

Your Firestore will have two collections automatically created by the app:
- `users` — stores user profiles
- `schedules` — stores scheduling results

---

## Step 4 — Get Firebase Web Config (for HTML files)

1. In Firebase Console → click the **gear icon** → **Project Settings**
2. Scroll to **"Your apps"** → click **"</> Web"**
3. Register app with name `jobmax-web` → click **"Register app"**
4. Copy the config object and paste it into **all 3 HTML files**:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSy...",
  authDomain: "jobmax-scheduler.firebaseapp.com",
  projectId: "jobmax-scheduler",
  storageBucket: "jobmax-scheduler.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123"
};
```

Replace `YOUR_API_KEY`, `YOUR_PROJECT`, etc. in:
- `login.html`
- `register.html`
- `dashboard.html`

---

## Step 5 — Get Service Account Key (for Flask backend)

1. In Firebase Console → **Project Settings** → **Service Accounts** tab
2. Click **"Generate new private key"** → **"Generate key"**
3. A JSON file downloads — rename it to `serviceAccountKey.json`
4. Place it in the **project root folder** (same folder as `app.py`)

⚠️ IMPORTANT: Never upload this file to GitHub!
Add to `.gitignore`:
```
serviceAccountKey.json
.env
__pycache__/
```

---

## Step 6 — Install Python Dependencies

Open terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

---

## Step 7 — Run the Project

```bash
python app.py
```

Open your browser and go to:
```
http://localhost:5000
```

---

## Step 8 — Test the App

1. Go to `http://localhost:5000/register` → create an account
2. Login at `http://localhost:5000/login`
3. On the Dashboard → add jobs → click **Run Greedy Scheduler**
4. Click **Save to Firebase** → check History tab
5. Check Firebase Console → Firestore → see data saved in real time

---

## Algorithm Summary (for report)

| Property | Value |
|---|---|
| Algorithm | Greedy Job Sequencing with Deadlines |
| Time Complexity | O(n log n) |
| Space Complexity | O(n) |
| Strategy | Sort by profit descending, assign to latest available slot |
| Optimal | Yes — produces maximum profit for unit-time jobs |

### Pseudocode
```
GREEDY-JOB-SCHEDULER(jobs):
  1. Sort jobs by profit in descending order
  2. maxDeadline = max deadline among all jobs
  3. slots[1..maxDeadline] = EMPTY
  4. FOR each job in sorted order:
       FOR t = min(job.deadline, maxDeadline) DOWN TO 1:
         IF slots[t] is EMPTY:
           slots[t] = job
           BREAK
  5. RETURN scheduled jobs and total profit
```

---

## Firestore Rules (for test mode)

In Firebase Console → Firestore → Rules, use this for development:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

This ensures only logged-in users can read/write data.

---

*JobMax — Built with Flask + Firebase + Greedy Algorithm*
