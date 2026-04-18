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
from flask_cors import CORS
from firebase_config import db, auth
from scheduler_cpp_wrapper import schedule_jobs
import os
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Secret key for session management — MUST be set via environment variable
app.secret_key = os.environ.get("SECRET_KEY")
if not app.secret_key:
    raise ValueError("❌ ERROR: SECRET_KEY environment variable not set. Please set it before running the app.")


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
        logger.warning(f"Token verification failed: {e}")
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

@app.route("/admin")
def admin():
    """Admin page (protected route—requires authentication)."""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    return render_template("admin.html")


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
    """
    logger.info(f"Schedule API called from {request.host}")
    data = request.get_json()
    logger.info(f"Request data: {data}")

    # For local development, bypass authentication
    is_local = 'localhost' in request.host or '127.0.0.1' in request.host
    # FORCE authentication for testing if needed, or keep local bypass
    # To test Firebase storage locally, you can set is_local = False
    logger.info(f"Request host: {request.host}, is_local: {is_local}, method: {request.method}, path: {request.path}")
    
    if not is_local:
        # Validate token for production
        id_token = data.get("idToken")
        if not id_token:
            logger.info("No idToken provided for non-local request")
            return jsonify({"error": "Unauthorized"}), 401
        decoded = verify_token(id_token)
        if not decoded:
            logger.info("Token verification failed")
            return jsonify({"error": "Unauthorized"}), 401
        uid = decoded["uid"]
    else:
        # In local mode, try to get UID from session if user is logged in via Firebase JS SDK
        user = get_current_user()
        if user:
            uid = user["uid"]
            logger.info(f"Using session user UID: {uid}")
        else:
            uid = "dev-user-123"
            logger.info("Using mock user for local development")

    jobs = data.get("jobs", [])
    worker_type = data.get("workerType", "Worker")

    if not jobs:
        return jsonify({"error": "No jobs provided"}), 400

    # Validate job fields
    for job in jobs:
        required_fields = ["job_type", "name", "deadline", "profit"]
        if not all(k in job for k in required_fields):
            return jsonify({"error": f"Each project must have: {', '.join(required_fields)}"}), 400
        
        # Validate deadline is a valid datetime string
        try:
            from datetime import datetime
            datetime.fromisoformat(job["deadline"].replace('Z', '+00:00'))
        except:
            return jsonify({"error": "Deadline must be a valid date/time"}), 400
            
        if job["profit"] < 100:
            return jsonify({"error": "Budget must be >= ₹100"}), 400

    # ── Run Greedy Algorithm ──
    result = schedule_jobs(jobs)

    # ── Save to Firestore (enabled for authenticated users even locally) ──
    if uid != "dev-user-123":
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
            else:
                # Create user document if it doesn't exist
                user_ref.set({
                    "totalProfit"   : result["total_profit"],
                    "schedulesRun"  : 1,
                    "jobsCompleted" : len(result["scheduled"]),
                    "email"         : session.get("user", {}).get("email", ""),
                    "name"          : session.get("user", {}).get("name", "User")
                })

            result["saved"] = True
            logger.info(f"Schedule saved to Firestore for UID: {uid}")

        except Exception as e:
            logger.error(f"Could not save schedule to Firestore: {e}")
            result["saved"] = False
    else:
        result["saved"] = False
        logger.info("Bypassing Firestore save for dev-user-123")

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
        logger.error(f"Could not fetch history: {e}")
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
    port = int(os.environ.get("PORT", 5000))
    logger.info("\n" + "=" * 45)
    logger.info("   JobMax — Greedy Scheduler Server")
    logger.info("=" * 45)
    logger.info(f"  Running at: http://localhost:{port}")
    logger.info("  Press Ctrl+C to stop\n")
    app.run(debug=False, host="0.0.0.0", port=port)