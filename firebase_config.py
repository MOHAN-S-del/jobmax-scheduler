import firebase_admin
from firebase_admin import credentials, firestore, auth as firebase_auth
import os
import json

if not firebase_admin._apps:
    creds_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    if creds_json:
        cred = credentials.Certificate(json.loads(creds_json))
    else:
        SERVICE_ACCOUNT_PATH = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")
        cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()
auth = firebase_auth
