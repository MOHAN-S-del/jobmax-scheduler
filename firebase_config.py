"""
firebase_config.py — Firebase Admin SDK Initialization
=======================================================
Project : JobMax — Greedy Job Scheduler

This file initializes the Firebase Admin SDK once.
Import `db` and `auth` from this file wherever needed.

Setup:
  1. Go to Firebase Console → Project Settings → Service Accounts
  2. Click "Generate new private key" → download the JSON file
  3. Rename it to `serviceAccountKey.json` and place it in the project root
  4. Never commit this file to GitHub — add it to .gitignore
"""

import firebase_admin
from firebase_admin import credentials, firestore, auth as firebase_auth
import os

# ── Initialize only once ──────────────────────────────────────
if not firebase_admin._apps:
    # Path to your downloaded service account key
    SERVICE_ACCOUNT_PATH = os.path.join(
        os.path.dirname(__file__), "serviceAccountKey.json"
    )

    if not os.path.exists(SERVICE_ACCOUNT_PATH):
        raise FileNotFoundError(
            "\n[Firebase Error] 'serviceAccountKey.json' not found!\n"
            "Download it from Firebase Console → Project Settings → Service Accounts\n"
            "and place it in the project root folder.\n"
        )

    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)

# ── Export Firestore DB and Auth instances ────────────────────
db   = firestore.client()       # Firestore database
auth = firebase_auth             # Firebase Auth (for token verification)
