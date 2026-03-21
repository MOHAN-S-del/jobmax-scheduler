"""
app.py — Flask Backend Server
==============================
Project : JobMax — Greedy Job Scheduler
Author  : (Your Name)

Routes:
  GET  /                  → Redirect to login
  GET  /login             → Login page
  GET  /register          → Register page
  GET  /dashboard         → Dashboard (protected)
  POST /api/schedule      → Run greedy algorithm, save to Firebase
  GET  /api/history       → Fetch past schedules for logged-in user
  POST /api/logout        → Logout user

Run:
  python app.py
  Then open http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from firebase_config import db, auth
from scheduler import schedule_jobs
import os

app = Flask(__name__)

# Secret key for session management — change this in production!
app.secret_key = os.environ.get("SECRET_KEY", "jobmax-secret-key-change-me")


# ── Helper: Verify Firebase ID Token ─────────────────────────
def verify_token(id_token):
    """
    Verify Firebase ID token sent from frontend.
    Returns decoded token (user info) or None if invalid.
    """
    try:
        decoded = auth.verify_id_token(id_token)
        return decoded
    except Exception as e:
        print(f"[Auth Error] Token verification failed: {e}")
        return None


def get_current_user():
    """Get current user from session."""
    return session.get("user")


# ── Page Routes ───────────────────────────────────────────────

@app.route("/")
def index():
    """Redirect root to login page."""
    return redirect(url_for("login"))


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/parallel")
def parallel():
    return render_template("parallel.html")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ── API Routes ────────────────────────────────────────────────

@app.route("/api/session-login", methods=["POST"])
def session_login():
    """
    Called after Firebase login on frontend.
    Stores user info in Flask session.

    Body: { "idToken": "<firebase_id_token>" }
    """
    data = request.get_json()
    id_token = data.get("idToken")

    if not id_token:
        return jsonify({"error": "No ID token provided"}), 400

    decoded = verify_token(id_token)
    if not decoded:
        return jsonify({"error": "Invalid or expired token"}), 401

    # Store user in session
    session["user"] = {
        "uid": decoded["uid"],
        "email": decoded.get("email"),
        "name": decoded.get("name", "User")
    }
    return jsonify({"success": True, "uid": decoded["uid"]})


@app.route("/api/logout", methods=["POST"])
def logout():
    """Clear session and redirect to login."""
    session.clear()
    return jsonify({"success": True})


@app.route("/api/schedule", methods=["POST"])
def api_schedule():
    """
    Run the greedy scheduling algorithm and save result to Firestore.

    Body:
    {
        "idToken"    : "<firebase_id_token>",
        "jobs"       : [{ "id", "name", "deadline", "profit" }, ...],
        "workerType" : "Plumber"
    }

    Returns:
    {
        "scheduled"    : [...],
        "skipped"      : [...],
        "total_profit" : 1800,
        "steps"        : [...],
        "saved"        : true
    }
    """
    data = request.get_json()

    # Validate token
    id_token = data.get("idToken")
    decoded = verify_token(id_token)
    if not decoded:
        return jsonify({"error": "Unauthorized"}), 401

    uid = decoded["uid"]
    jobs = data.get("jobs", [])
    worker_type = data.get("workerType", "Worker")

    if not jobs:
        return jsonify({"error": "No jobs provided"}), 400

    # Validate job fields
    for job in jobs:
        if not all(k in job for k in ("name", "deadline", "profit")):
            return jsonify({"error": "Each job must have name, deadline, and profit"}), 400
        if job["deadline"] < 1 or job["profit"] < 1:
            return jsonify({"error": "Deadline and profit must be >= 1"}), 400

    # ── Run Greedy Algorithm ──
    result = schedule_jobs(jobs)

    # ── Save to Firestore ──
    try:
        from datetime import datetime

        # Save schedule document
        schedule_ref = db.collection("schedules").add({
            "userId"        : uid,
            "workerType"    : worker_type,
            "totalProfit"   : result["total_profit"],
            "totalSlots"    : len(result["slots"]),
            "scheduledJobs" : result["scheduled"],
            "skippedJobs"   : result["skipped"],
            "createdAt"     : datetime.utcnow().isoformat()
        })

        # Update user stats
        user_ref = db.collection("users").document(uid)
        user_doc = user_ref.get()
        if user_doc.exists:
            current = user_doc.to_dict()
            user_ref.update({
                "totalProfit"   : current.get("totalProfit", 0) + result["total_profit"],
                "schedulesRun"  : current.get("schedulesRun", 0) + 1,
                "jobsCompleted" : current.get("jobsCompleted", 0) + len(result["scheduled"])
            })

        result["saved"] = True

    except Exception as e:
        print(f"[Firestore Error] Could not save schedule: {e}")
        result["saved"] = False

    return jsonify(result)


@app.route("/api/history", methods=["GET"])
def api_history():
    """
    Fetch all past schedules for the logged-in user.

    Query param: ?idToken=<firebase_id_token>

    Returns:
    {
        "schedules": [ { ...schedule data... }, ... ]
    }
    """
    id_token = request.args.get("idToken")
    decoded = verify_token(id_token)
    if not decoded:
        return jsonify({"error": "Unauthorized"}), 401

    uid = decoded["uid"]

    try:
        query = (
            db.collection("schedules")
            .where("userId", "==", uid)
            .order_by("createdAt", direction="DESCENDING")
            .limit(20)
        )
        docs = query.stream()
        schedules = [{"id": doc.id, **doc.to_dict()} for doc in docs]
        return jsonify({"schedules": schedules})

    except Exception as e:
        print(f"[Firestore Error] Could not fetch history: {e}")
        return jsonify({"error": "Failed to load history"}), 500


@app.route("/api/profile", methods=["GET"])
def api_profile():
    """
    Fetch user profile from Firestore.
    Query param: ?idToken=<firebase_id_token>
    """
    id_token = request.args.get("idToken")
    decoded = verify_token(id_token)
    if not decoded:
        return jsonify({"error": "Unauthorized"}), 401

    uid = decoded["uid"]
    try:
        doc = db.collection("users").document(uid).get()
        if doc.exists:
            return jsonify(doc.to_dict())
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Run Server ────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "=" * 45)
    print("   JobMax — Greedy Scheduler Server")
    print("=" * 45)
    print("  Running at: http://localhost:5000")
    print("  Press Ctrl+C to stop\n")
   app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))