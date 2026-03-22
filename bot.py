#!/usr/bin/env python3
"""
SparkBot — Production-grade Telegram Dating Bot
Pure requests library, no frameworks.
"""

import json
import logging
import os
import random
import time
from datetime import datetime, timedelta, timezone

import requests

import config
import db as database

# ─── LOGGING ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("errors.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# ─── TELEGRAM API LAYER ───────────────────────────────────────────────────────
BASE = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}"


def _post(method: str, **kwargs) -> dict:
    try:
        r = requests.post(f"{BASE}/{method}", json=kwargs, timeout=30)
        return r.json()
    except Exception as e:
        logger.error(f"TG [{method}] error: {e}")
        return {"ok": False}


def send_msg(chat_id, text, markup=None, parse_mode="HTML"):
    p = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
    if markup:
        p["reply_markup"] = markup
    return _post("sendMessage", **p)


def send_photo(chat_id, photo, caption="", markup=None, parse_mode="HTML"):
    p = {"chat_id": chat_id, "photo": photo, "caption": caption, "parse_mode": parse_mode}
    if markup:
        p["reply_markup"] = markup
    return _post("sendPhoto", **p)


def answer_cb(cq_id, text="", alert=False):
    return _post("answerCallbackQuery", callback_query_id=cq_id, text=text, show_alert=alert)


def answer_precheckout(pq_id, ok=True, err=None):
    p = {"pre_checkout_query_id": pq_id, "ok": ok}
    if not ok and err:
        p["error_message"] = err
    return _post("answerPreCheckoutQuery", **p)


def send_invoice(chat_id, title, description, payload, currency, prices):
    return _post(
        "sendInvoice",
        chat_id=chat_id,
        title=title,
        description=description,
        payload=payload,
        provider_token="",
        currency=currency,
        prices=prices,
    )


def ikb(*rows):
    """Build inline keyboard. Each row: list of (label, callback_data) tuples."""
    return {
        "inline_keyboard": [
            [{"text": t, "callback_data": d} for t, d in row]
            for row in rows
        ]
    }


# ─── TIME HELPERS ─────────────────────────────────────────────────────────────
def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def now_iso() -> str:
    return utcnow().isoformat()


def parse_iso(s: str) -> datetime:
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)


# ─── USER STATE CHECKS ────────────────────────────────────────────────────────
def check_premium(user: dict) -> None:
    if user.get("is_premium") and user.get("premium_expires"):
        if utcnow() > parse_iso(user["premium_expires"]):
            user["is_premium"] = False
            user["premium_expires"] = None


def check_boost(user: dict) -> None:
    if user.get("is_boosted") and user.get("boost_expires"):
        if utcnow() > parse_iso(user["boost_expires"]):
            user["is_boosted"] = False
            user["boost_expires"] = None


def check_boost_week(user: dict) -> None:
    reset = user.get("boost_week_reset")
    if not reset:
        user["boost_week_reset"] = now_iso()
        user["boosts_used_this_week"] = 0
        return
    if utcnow() - parse_iso(reset) > timedelta(days=7):
        user["boosts_used_this_week"] = 0
        user["boost_week_reset"] = now_iso()


def check_limits(user: dict) -> None:
    today = utcnow().strftime("%Y-%m-%d")
    if user.get("limits_reset_date") != today:
        user["likes_today"] = 0
        user["super_likes_today"] = 0
        user["undos_today"] = 0
        user["limits_reset_date"] = today


def touch(user: dict) -> None:
    user["last_seen"] = now_iso()


def run_checks(user: dict) -> None:
    """Run all expiry/reset checks in one call."""
    check_premium(user)
    check_boost(user)
    check_limits(user)
    touch(user)


# ─── PROFILE UTILITIES ────────────────────────────────────────────────────────
def activity_label(user: dict) -> str:
    ls = user.get("last_seen")
    if not ls:
        return "💤 A while ago"
    diff = (utcnow() - parse_iso(ls)).total_seconds()
    if diff < 300:
        return "🟢 Online now"
    if diff < 86400:
        return "🕐 Active today"
    if diff < 604800:
        return "📅 Active this week"
    return "💤 A while ago"


def completeness(user: dict) -> int:
    score = 0
    if user.get("photo_file_id"):
        score += 30
    if user.get("bio"):
        score += 25
    if len(user.get("interests", [])) >= 5:
        score += 25
    if user.get("city"):
        score += 20
    return score


def completeness_bar(score: int) -> str:
    filled = score // 10
    bar = "█" * filled + "░" * (10 - filled)
    return f"Profile Strength: {bar} {score}%"


def completeness_tip(user: dict) -> str:
    if completeness(user) == 100:
        return "🌟 Profile 100% complete!"
    tips = []
    if not user.get("photo_file_id"):
        tips.append("Add a photo (+30%)")
    if not user.get("bio"):
        tips.append("Write a bio (+25%)")
    if len(user.get("interests", [])) < 5:
        tips.append("Add 5+ interests (+25%)")
    if not user.get("city"):
        tips.append("Add your city (+20%)")
    return f"💡 Tip: {tips[0]}" if tips else ""


def card_text(user: dict) -> str:
    name   = user.get("name") or "Unknown"
    age    = user.get("age") or "?"
    city   = user.get("city") or "Unknown"
    lf     = user.get("looking_for") or "Everyone"
    bio    = user.get("bio") or ""
    ints   = user.get("interests") or []
    badge  = " ✨" if user.get("is_premium") else ""
    status = activity_label(user)

    return (
        f"💫 <b>{name}{badge}</b>, {age}\n"
        f"📍 {city}\n"
        f"🎯 Looking for: {lf}\n"
        f"{status}\n\n"
        f"📝 {bio}\n\n"
        f"✨ Interests: {', '.join(ints) if ints else 'None listed'}\n\n"
        f"━━━━━━━━━━━━━━━━━━"
    )


def browse_buttons(target_id: str, likes_left: int, is_premium: bool) -> dict:
    like_label = "❤️ Like" if is_premium else f"❤️ Like ({likes_left} left)"
    return {"inline_keyboard": [[
        {"text": like_label,      "callback_data": f"like:{target_id}"},
        {"text": "💔 Pass",        "callback_data": f"pass:{target_id}"},
        {"text": "⭐ Super Like", "callback_data": f"superlike:{target_id}"},
        {"text": "📛 Report",     "callback_data": f"report:{target_id}"},
    ]]}


# ─── CONVERSATION STARTERS ────────────────────────────────────────────────────
_INTEREST_STARTERS = {
    "music":       "You both love music! Ask them what concert they'd go to if they could see anyone live. 🎵",
    "travel":      "You're both travellers! Ask them about the best place they've ever been. ✈️",
    "books":       "You're both readers! Ask them what book changed their perspective. 📚",
    "hiking":      "You both love hiking! Ask them about their favourite trail or trek. 🏔️",
    "coffee":      "You're both coffee lovers! Ask them about their go-to order. ☕",
    "food":        "You both love food! Ask them about the best meal they've ever had. 🍜",
    "movies":      "You're both film fans! Ask them about their all-time favourite movie. 🎬",
    "gaming":      "You're both gamers! Ask them what game they're obsessed with right now. 🎮",
    "fitness":     "You both love fitness! Ask them about their favourite way to work out. 💪",
    "art":         "You're both creative! Ask them about a piece of art that moved them. 🎨",
    "photography": "You're both into photography! Ask about the best shot they've ever taken. 📷",
    "cooking":     "You both love cooking! Ask them to share their signature dish. 🍳",
    "yoga":        "You both do yoga! Ask them how they first got into it. 🧘",
    "dancing":     "You both love dancing! Ask them what style they love most. 💃",
    "writing":     "You're both writers! Ask them what they're working on right now. ✍️",
}

_GENERIC_STARTERS = [
    "What's the most spontaneous thing you've ever done? 🎲",
    "If you could live anywhere in the world, where would it be? 🌍",
    "What's your favourite movie of all time and why? 🎬",
    "Tea or coffee — and what does your morning look like? ☕",
    "What's something you're weirdly good at? 😄",
    "Last book you couldn't put down? 📚",
    "If you had a superpower, what would it be? 🦸",
    "What's your go-to comfort food? 🍜",
    "Best trip you've ever taken? 🗺️",
    "Are you a morning person or a night owl? 🌅🦉",
    "What's a skill you've always wanted to learn? 🎸",
    "What's your favourite thing about your city? 🏙️",
    "Describe your perfect weekend in 3 words. 🌟",
    "What's the last thing that made you laugh really hard? 😂",
    "If you could have dinner with anyone, who'd it be? 🍽️",
    "What's the most underrated thing people should try? ✨",
    "Cats or dogs — defend your answer. 🐶🐱",
    "What song is always in your head lately? 🎵",
    "What are you most passionate about right now? 🔥",
    "If your life was a movie, what genre would it be? 🎭",
]


def conversation_starter(u1: dict, u2: dict) -> str:
    common = (
        set(i.lower() for i in u1.get("interests", []))
        & set(i.lower() for i in u2.get("interests", []))
    )
    for interest in common:
        if interest in _INTEREST_STARTERS:
            return _INTEREST_STARTERS[interest]
    if common:
        pick = random.choice(list(common))
        return f"You both love {pick}! Ask them about their experience with it. ✨"
    return random.choice(_GENERIC_STARTERS)


# ─── BROWSE QUEUE ─────────────────────────────────────────────────────────────
def build_queue(db: dict, viewer_id: int) -> list[str]:
    """Return sorted list of user IDs for viewer to browse."""
    viewer    = database.get_user(db, viewer_id)
    vid       = str(viewer_id)
    lf        = viewer.get("looking_for", "Everyone")
    vgender   = viewer.get("gender", "")
    vcity     = (viewer.get("city") or "").lower()
    v_ints    = set(i.lower() for i in viewer.get("interests", []))
    excluded  = (
        set(viewer.get("likes", []))
        | set(viewer.get("super_likes_sent", []))
        | set(viewer.get("passes", []))
        | set(viewer.get("matches", []))
        | set(viewer.get("reports_made", []))
        | set(viewer.get("blocked", []))
        | {vid}
    )
    now = utcnow()
    scored = []

    for uid, u in db["users"].items():
        if uid in excluded:
            continue
        if u.get("is_banned"):
            continue
        if len(u.get("reports_received", [])) >= 3:
            continue
        if vid in u.get("blocked", []):
            continue

        # Gender filter
        ugender = u.get("gender", "")
        u_lf    = u.get("looking_for", "Everyone")

        if lf != "Everyone":
            if lf == "Men"   and ugender != "Man":   continue
            if lf == "Women" and ugender != "Woman": continue

        if u_lf != "Everyone":
            if u_lf == "Men"   and vgender != "Man":   continue
            if u_lf == "Women" and vgender != "Woman": continue

        # Score
        s = 0
        boosted  = u.get("is_boosted")
        premium  = u.get("is_premium")

        if premium and boosted: s += 1000
        elif boosted:           s += 800
        elif premium:           s += 600

        u_ints = set(i.lower() for i in u.get("interests", []))
        s += len(v_ints & u_ints) * 20

        if (u.get("city") or "").lower() == vcity and vcity:
            s += 100

        ls = u.get("last_seen")
        if ls:
            diff = (now - parse_iso(ls)).total_seconds()
            if diff < 86400:  s += 80

        joined = u.get("joined")
        if joined and (now - parse_iso(joined)).days < 7:
            s += 50

        s += completeness(u)
        scored.append((s, uid))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [uid for _, uid in scored]


# ─── MATCH HANDLER ────────────────────────────────────────────────────────────
def do_match(db: dict, a_id: int, b_id: int) -> bool:
    """Mutually add match, send notifications. Returns True if new match."""
    a_str, b_str = str(a_id), str(b_id)
    ua = database.get_user(db, a_id)
    ub = database.get_user(db, b_id)
    if not ua or not ub:
        return False
    if b_str in ua.get("matches", []):
        return False  # Already matched

    ua.setdefault("matches", []).append(b_str)
    ub.setdefault("matches", []).append(a_str)
    db["total_matches"] = db.get("total_matches", 0) + 1

    starter = conversation_starter(ua, ub)

    def _notify(to_id: int, other: dict):
        uname = f"@{other['username']}" if other.get("username") else "(no username set)"
        send_msg(
            to_id,
            f"🎉 <b>It's a Match!</b>\n\n"
            f"You and <b>{other.get('name', '?')}</b> both liked each other!\n\n"
            f"Their username: {uname}\n"
            f"Say hello! 👋\n\n"
            f"💡 <b>Conversation Starter:</b>\n\"{starter}\"",
            markup=ikb([("🔥 Keep Swiping", "menu:browse"), ("💌 See Matches", "menu:matches")]),
        )

    if ua.get("notifications", {}).get("matches", True):
        _notify(a_id, ub)
    if ub.get("notifications", {}).get("matches", True):
        _notify(b_id, ua)

    database.set_user(db, a_id, ua)
    database.set_user(db, b_id, ub)
    return True


# ─── ONBOARDING PROMPTS ───────────────────────────────────────────────────────
def ask_name(cid):
    send_msg(cid, "👋 Let's set up your profile!\n\n<b>What's your name?</b>")

def ask_age(cid):
    send_msg(cid, "🎂 <b>How old are you?</b>\n\n(Must be 18–60)")

def ask_gender(cid):
    send_msg(cid, "🧑‍🤝‍🧑 <b>What's your gender?</b>",
        markup=ikb([("Man", "gender:Man"), ("Woman", "gender:Woman"), ("Non-binary", "gender:Non-binary")]))

def ask_looking_for(cid):
    send_msg(cid, "💘 <b>Who are you looking to meet?</b>",
        markup=ikb([("Men", "lf:Men"), ("Women", "lf:Women"), ("Everyone", "lf:Everyone")]))

def ask_city(cid):
    send_msg(cid, "🏙️ <b>Which city are you in?</b>")

def ask_bio(cid):
    send_msg(cid, "📝 <b>Write your bio</b> — tell people a bit about yourself!\n\n(Max 300 characters)")

def ask_interests(cid):
    send_msg(cid, "✨ <b>What are your interests?</b>\n\nComma-separated list, up to 10.\n<i>Example: music, travel, coffee, hiking, books</i>")

def ask_photo(cid):
    send_msg(cid, "📸 <b>Send your best photo!</b>\n\nJust send a photo directly in this chat.")

def show_preview(cid, user: dict):
    temp = {**user, **user.get("state_data", {})}
    caption = card_text(temp) + "\n\n<i>Does this look good?</i>"
    markup = ikb(
        [("✅ Yes, looks great!", "setup_ok:yes")],
        [("✏️ Edit",              "setup_ok:edit")],
    )
    if temp.get("photo_file_id"):
        send_photo(cid, temp["photo_file_id"], caption, markup=markup)
    else:
        send_msg(cid, caption, markup=markup)

def show_main_menu(cid, user: dict):
    name   = user.get("name") or "there"
    extras = (" ✨" if user.get("is_premium") else "") + (" 🚀" if user.get("is_boosted") else "")
    send_msg(
        cid,
        f"🏠 <b>Welcome back, {name}{extras}!</b>\n\nWhat would you like to do?",
        markup=ikb(
            [("🔥 Browse",     "menu:browse"),  ("💌 Matches",  "menu:matches")],
            [("👤 Profile",    "menu:profile"), ("⭐ Premium",  "menu:premium")],
            [("🔔 Notifications", "menu:notifs"), ("❓ Help",   "menu:help")],
        ),
    )

def show_edit_menu(cid):
    send_msg(
        cid,
        "✏️ <b>Edit Profile</b>\n\nWhat would you like to change?",
        markup=ikb(
            [("✏️ Name",         "ef:name"),       ("🎂 Age",        "ef:age")],
            [("📝 Bio",          "ef:bio"),         ("📸 Photo",      "ef:photo")],
            [("✨ Interests",    "ef:interests"),   ("🏙️ City",       "ef:city")],
            [("💘 Looking For", "ef:looking_for")],
            [("🔙 Back",        "menu:home")],
        ),
    )

def show_notif_menu(cid, user: dict):
    n = user.get("notifications", {})
    def tog(k): return "✅ ON" if n.get(k, True) else "❌ OFF"
    send_msg(
        cid,
        "🔔 <b>Notification Settings</b>",
        markup=ikb(
            [(f"❤️ Match notifications: {tog('matches')}",    "nt:matches")],
            [(f"⭐ Super like alerts: {tog('super_likes')}",  "nt:super_likes")],
            [(f"📢 Broadcast messages: {tog('broadcasts')}",  "nt:broadcasts")],
            [("🔙 Back", "menu:home")],
        ),
    )


# ─── BROWSE: SHOW NEXT PROFILE ────────────────────────────────────────────────
def next_profile(cid: int, db: dict) -> None:
    user = database.get_user(db, cid)
    if not user:
        return
    check_limits(user)
    queue = build_queue(db, cid)

    if not queue:
        user["state"] = "idle"
        database.set_user(db, cid, user)
        send_msg(
            cid,
            "😔 <b>No more profiles right now.</b>\n\nCheck back later or update your preferences!",
            markup=ikb([("🏠 Main Menu", "menu:home"), ("✏️ Edit Prefs", "menu:edit")]),
        )
        return

    target_id = queue[0]
    target    = db["users"].get(target_id)
    if not target:
        # Profile was deleted, skip
        user.setdefault("passes", []).append(target_id)
        database.set_user(db, cid, user)
        next_profile(cid, database.load_db())
        return

    is_prem   = user.get("is_premium", False)
    likes_lft = max(0, config.DAILY_LIKE_LIMIT - user.get("likes_today", 0))
    caption   = card_text(target)
    markup    = browse_buttons(target_id, likes_lft, is_prem)

    if target.get("photo_file_id"):
        send_photo(cid, target["photo_file_id"], caption, markup=markup)
    else:
        send_msg(cid, caption, markup=markup)


# ─── COMMANDS ─────────────────────────────────────────────────────────────────
def cmd_start(cid: int, from_user: dict, db: dict) -> None:
    user = database.get_user(db, cid)
    if not user:
        user = database.default_user(cid, from_user.get("username", ""), now_iso())
        database.set_user(db, cid, user)
        send_msg(
            cid,
            "💘 <b>Welcome to SparkBot!</b>\n\n"
            "Find your spark — one swipe at a time. 🔥\n\n"
            "Let's set up your profile first!",
        )
        ask_name(cid)
    else:
        run_checks(user)
        user["username"]   = from_user.get("username", user.get("username", ""))
        user["state"]      = "idle"
        user["state_data"] = {}
        database.set_user(db, cid, user)
        show_main_menu(cid, user)


def cmd_browse(cid: int, db: dict) -> None:
    user = database.get_user(db, cid)
    if not user or not user.get("name"):
        send_msg(cid, "❗ Please complete your profile first! Use /start"); return
    if user.get("is_banned"):
        send_msg(cid, f"🚫 Account suspended. Contact support: @{config.ADMIN_USERNAME}"); return
    run_checks(user)
    user["state"] = "browsing"
    database.set_user(db, cid, user)
    next_profile(cid, database.load_db())


def cmd_matches(cid: int, db: dict) -> None:
    user = database.get_user(db, cid)
    if not user: send_msg(cid, "❗ No profile found. Use /start"); return
    run_checks(user)
    matches = user.get("matches", [])

    if not matches:
        send_msg(
            cid,
            "💌 <b>No matches yet!</b>\n\n"
            "Keep swiping — your match is out there! 🔥\n\n"
            "💡 Complete your profile to get more likes!",
            markup=ikb([("🔥 Start Swiping", "menu:browse")]),
        )
        database.set_user(db, cid, user); return

    lines = ["💌 <b>Your Matches!</b>\n"]
    for mid in matches:
        m = db["users"].get(mid)
        if not m: continue
        uname = f"@{m['username']}" if m.get("username") else "(no usernam