"""
db.py — all database read/write functions
Stores everything in db.json with automatic backup to db_backup.json
"""

import json
import os
import time
import logging

DB_FILE     = "db.json"
BACKUP_FILE = "db_backup.json"

logger = logging.getLogger(__name__)


# ─── LOAD ────────────────────────────────────────────────────────────────────
def load_db() -> dict:
    """Load db.json. Falls back to backup, then creates fresh."""
    for fname in [DB_FILE, BACKUP_FILE]:
        if os.path.exists(fname):
            try:
                with open(fname, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Ensure top-level keys exist
                    data.setdefault("users", {})
                    data.setdefault("reports", [])
                    data.setdefault("total_matches", 0)
                    data.setdefault("total_stars_earned", 0)
                    return data
            except Exception as e:
                logger.error(f"Failed to load {fname}: {e}")
    return {
        "users":              {},
        "reports":            [],
        "total_matches":      0,
        "total_stars_earned": 0,
    }


# ─── SAVE ────────────────────────────────────────────────────────────────────
def save_db(db: dict, retries: int = 3) -> bool:
    """Write db to disk with retry and backup."""
    for attempt in range(retries):
        try:
            with open(DB_FILE, "w", encoding="utf-8") as f:
                json.dump(db, f, ensure_ascii=False, indent=2)
            with open(BACKUP_FILE, "w", encoding="utf-8") as f:
                json.dump(db, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"DB save attempt {attempt + 1} failed: {e}")
            time.sleep(0.3)
    return False


# ─── USER HELPERS ─────────────────────────────────────────────────────────────
def get_user(db: dict, user_id) -> dict | None:
    return db["users"].get(str(user_id))


def set_user(db: dict, user_id, user_data: dict) -> None:
    db["users"][str(user_id)] = user_data
    save_db(db)


def default_user(user_id, username: str, now_iso: str) -> dict:
    return {
        "name":                   None,
        "age":                    None,
        "gender":                 None,
        "looking_for":            None,
        "city":                   None,
        "bio":                    None,
        "interests":              [],
        "photo_file_id":          None,
        "username":               username or "",
        "likes":                  [],
        "passes":                 [],
        "matches":                [],
        "super_likes_sent":       [],
        "super_likes_received":   [],
        "who_liked_me":           [],
        "reports_received":       [],
        "reports_made":           [],
        "blocked":                [],
        "is_banned":              False,
        "is_premium":             False,
        "premium_expires":        None,
        "is_boosted":             False,
        "boost_expires":          None,
        "boosts_used_this_week":  0,
        "boost_week_reset":       None,
        "likes_today":            0,
        "super_likes_today":      0,
        "undos_today":            0,
        "limits_reset_date":      now_iso[:10],
        "last_swiped_user":       None,
        "last_seen":              now_iso,
        "joined":                 now_iso,
        "notifications": {
            "matches":     True,
            "super_likes": True,
            "broadcasts":  True,
        },
        "state":      "setup_name",
        "state_data": {},
    }
