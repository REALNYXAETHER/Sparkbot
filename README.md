<div align="center">

# 💘 SparkBot

### A Production-Grade Telegram Dating Bot

*Find your spark — one swipe at a time.*

---

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot_API-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)
![Railway](https://img.shields.io/badge/Deployed_on-Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen?style=for-the-badge)
![Lines](https://img.shields.io/badge/Lines_of_Code-1500+-orange?style=for-the-badge)

---

```
💫 Priya, 23
📍 Mumbai
🎯 Looking for: Men
🟢 Online now

📝 Coffee addict ☕ | Book lover | Amateur chef

✨ Interests: music, travel, books, coffee, hiking

━━━━━━━━━━━━━━━━━━
❤️ Like (20 left)    💔 Pass    ⭐ Super Like    📛 Report
```

**The full Tinder experience. Inside Telegram. Built with pure Python.**

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Deployment](#-deployment-on-railway) • [Commands](#-commands-reference) • [Admin Panel](#-admin-panel) • [Premium System](#-premium--telegram-stars) • [Contributing](#-contributing)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
  - [Onboarding Flow](#1-onboarding-flow)
  - [Profile Card System](#2-profile-card-system)
  - [Swipe System](#3-swipe-system)
  - [Match System](#4-match-system)
  - [Profile Management](#5-profile-management)
  - [Reporting & Safety](#6-reporting--safety)
  - [Boost System](#7-boost-system)
  - [Daily Limits](#8-daily-limits)
  - [Premium — Telegram Stars](#9-premium--telegram-stars)
  - [Admin Panel](#10-admin-panel)
  - [Smart Matching Algorithm](#11-smart-matching-algorithm)
  - [Last Seen & Activity](#12-last-seen--activity)
  - [Notifications](#13-notifications)
  - [Undo Last Swipe](#14-undo-last-swipe)
  - [Profile Completeness Score](#15-profile-completeness-score)
  - [Conversation Starters](#16-conversation-starters)
  - [Help & FAQ](#17-help--faq)
- [Architecture](#-architecture)
  - [File Structure](#file-structure)
  - [State Machine](#state-machine)
  - [Database Design](#database-design)
  - [Polling Loop](#polling-loop)
  - [Dispatcher](#dispatcher)
- [Quick Start](#-quick-start)
  - [Prerequisites](#prerequisites)
  - [Local Setup](#local-setup)
  - [Environment Variables](#environment-variables)
- [Deployment on Railway](#-deployment-on-railway)
  - [Step 1 — Push to GitHub](#step-1--push-to-github)
  - [Step 2 — Connect Railway](#step-2--connect-railway)
  - [Step 3 — Set Environment Variables](#step-3--set-environment-variables)
  - [Step 4 — Deploy](#step-4--deploy)
  - [Persisting db.json with Railway Volumes](#persisting-dbjson-with-railway-volumes)
- [BotFather Setup](#-botfather-setup)
- [Commands Reference](#-commands-reference)
- [Admin Panel](#-admin-panel)
- [Premium System](#-premium--telegram-stars)
- [Database Schema — Full Reference](#-database-schema--full-reference)
- [Code Walkthrough](#-code-walkthrough)
  - [bot.py](#botpy)
  - [db.py](#dbpy)
  - [config.py](#configpy)
- [Smart Matching Algorithm — Deep Dive](#-smart-matching-algorithm--deep-dive)
- [Safety System](#-safety-system)
- [UX Design Principles](#-ux-design-principles)
- [Edge Cases Handled](#-edge-cases-handled)
- [Error Handling & Logging](#-error-handling--logging)
- [Performance Considerations](#-performance-considerations)
- [Roadmap](#-roadmap)
- [FAQ](#-faq)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

SparkBot is a **full-featured, production-ready Telegram dating bot** built entirely in Python using only the standard library and the `requests` package. No heavy frameworks, no external databases, no complex infrastructure — just clean, readable Python that deploys in minutes.

### Why SparkBot?

Dating apps are gated behind App Store reviews, massive servers, and years of development. SparkBot proves you can build a **complete Tinder-clone experience** inside Telegram with:

- **~1,500 lines of Python**
- **1 external dependency** (`requests`)
- **1 JSON file** as the database
- **$0 infrastructure cost** (Railway free tier is enough)

It's not a toy project. SparkBot implements every core feature you'd expect from a real dating app:

| Feature | SparkBot | Tinder |
|---------|----------|--------|
| Swipe system (like/pass) | ✅ | ✅ |
| Mutual match detection | ✅ | ✅ |
| Super likes | ✅ | ✅ |
| Profile photos | ✅ | ✅ |
| Boost system | ✅ | ✅ |
| Daily limits | ✅ | ✅ |
| Premium subscription | ✅ | ✅ |
| Who liked me | ✅ | ✅ |
| Reporting & safety | ✅ | ✅ |
| Smart queue algorithm | ✅ | ✅ |
| Admin panel | ✅ | ❓ |
| Conversation starters | ✅ | ❌ |
| Privacy-first (no ads) | ✅ | ❌ |

### Tech Stack

```
Language:     Python 3.11
HTTP Client:  requests (pure, no frameworks)
Database:     db.json (Python's built-in json module)
Hosting:      Railway
Bot API:      Telegram Bot API (long polling)
Payments:     Telegram Stars (XTR)
```

### Philosophy

> **Simple is fast. Fast ships. Shipping beats perfect.**

Every architectural decision in SparkBot prioritizes:
1. **Readability** — Any Python developer can understand the entire codebase in one sitting
2. **Deployability** — From clone to live in under 10 minutes
3. **Reliability** — Triple-retry DB writes, automatic backups, graceful error handling
4. **Extensibility** — Clean separation of concerns makes new features easy to add

---

## 🚀 Features

SparkBot implements **17 distinct feature modules**, each described in detail below.

---

### 1. Onboarding Flow

When a user sends `/start` for the first time, they enter the onboarding flow — a guided, step-by-step profile setup that collects all the information needed to start matching.

#### Flow Sequence

```
/start
  └── New user detected
        ├── Step 1: Name          (text input)
        ├── Step 2: Age           (number, rejected if <18 or >60)
        ├── Step 3: Gender        (inline buttons: Man / Woman / Non-binary)
        ├── Step 4: Looking For   (inline buttons: Men / Women / Everyone)
        ├── Step 5: City          (text input)
        ├── Step 6: Bio           (text, max 300 chars, character count shown)
        ├── Step 7: Interests     (comma-separated, max 10, stored as list)
        ├── Step 8: Photo         (Telegram photo message, stored as file_id)
        └── Preview               ("Does this look good?" → Yes / Edit)
```

#### State Transitions During Onboarding

| State | Trigger | Next State |
|-------|---------|------------|
| `setup_name` | User sends name text | `setup_age` |
| `setup_age` | User sends valid age | `setup_gender` |
| `setup_gender` | Gender button clicked | `setup_lf` |
| `setup_lf` | Looking For button clicked | `setup_city` |
| `setup_city` | User sends city text | `setup_bio` |
| `setup_bio` | User sends bio text | `setup_interests` |
| `setup_interests` | User sends interests | `setup_photo` |
| `setup_photo` | User sends photo | `setup_confirm` |
| `setup_confirm` | "Yes" clicked | `idle` (profile saved) |
| `setup_confirm` | "Edit" clicked | Returns to edit menu |

#### Validation Rules

- **Name**: 1–50 characters, no empty strings
- **Age**: Integer between 18 and 60 (inclusive). Under 18 rejected with friendly message. Over 60 rejected.
- **Bio**: Maximum 300 characters. Character count shown if exceeded.
- **Interests**: Comma-separated. Excess whitespace trimmed. Maximum 10 interests stored (rest silently discarded).
- **Photo**: Must be sent as a Telegram photo (not a document/file). Only the largest size variant's `file_id` is stored.

#### Temporary State Storage

During onboarding, collected data lives in `user["state_data"]` — a temporary dictionary — until the user confirms their profile preview. Only on confirmation does data get written to the root user fields. This prevents partial profile saves.

```json
"state_data": {
  "name": "Priya",
  "age": 23,
  "gender": "Woman",
  "looking_for": "Men",
  "city": "Mumbai",
  "bio": "Coffee addict ☕",
  "interests": ["music", "travel", "books"],
  "photo_file_id": "AgACAgI..."
}
```

#### Returning Users

If `/start` is sent by a user who already has a profile:
- State is reset to `idle`
- `state_data` is cleared
- Main menu is shown
- No re-onboarding required

This handles the common case of users sending `/start` mid-flow to reset the bot.

---

### 2. Profile Card System

Every profile shown in SparkBot uses a **consistent, standardised card format** — similar to a Tinder card. The card is always sent as a **photo message with a caption**, never as a plain text message.

#### Card Format

```
💫 Priya ✨, 23
📍 Mumbai
🎯 Looking for: Men
🟢 Online now

📝 Coffee addict ☕ | Book lover | Amateur chef

✨ Interests: music, travel, books, coffee, hiking

━━━━━━━━━━━━━━━━━━
```

#### Card Fields

| Field | Icon | Source |
|-------|------|--------|
| Name + Premium badge | 💫 ✨ | `user["name"]` + `is_premium` |
| Age | (inline) | `user["age"]` |
| City | 📍 | `user["city"]` |
| Looking For | 🎯 | `user["looking_for"]` |
| Activity Status | 🟢🕐📅💤 | Computed from `last_seen` |
| Bio | 📝 | `user["bio"]` |
| Interests | ✨ | `user["interests"]` (joined by comma) |
| Separator | ━━━━━━━ | Static |

#### Activity Status Computation

Activity status is computed dynamically from `last_seen` on every card render:

```python
def activity_label(user: dict) -> str:
    diff = (utcnow() - parse_iso(user["last_seen"])).total_seconds()
    if diff < 300:    return "🟢 Online now"       # < 5 minutes
    if diff < 86400:  return "🕐 Active today"      # < 24 hours
    if diff < 604800: return "📅 Active this week"  # < 7 days
    return "💤 A while ago"                         # older
```

#### Premium Badge

Premium users automatically get a `✨` badge after their name on the card. This is visible to everyone browsing their profile.

#### Browse Buttons

In browse mode, the card always has four action buttons attached:

```
❤️ Like (14 left)    💔 Pass    ⭐ Super Like    📛 Report
```

For premium users, the like count is hidden and replaced with just `❤️ Like`.

---

### 3. Swipe System

The swipe system is the core interaction loop of SparkBot. It's triggered by `/browse` and shows profiles one at a time.

#### How It Works

```
User runs /browse
  └── build_queue() computes sorted profile list
        └── Show first profile as photo + caption + buttons
              ├── ❤️ Like  → Record like, check mutual match, show next
              ├── 💔 Pass  → Record pass, show next
              ├── ⭐ Super Like → Record super like, notify target, show next
              └── 📛 Report → Show report reason menu
```

#### Queue Logic — Who Gets Shown

Profiles are excluded from the queue if the viewer has already:
- Liked them
- Super liked them
- Passed on them
- Matched with them
- Reported them
- Blocked them

Additionally excluded:
- The viewer's own profile
- Banned users
- Users with 3+ reports (auto-soft-banned)
- Users who have blocked the viewer

#### Gender Filtering

SparkBot applies bidirectional gender filtering — the viewer's `looking_for` preference AND the target's `looking_for` preference both need to be compatible.

```
Viewer looking for: Men
Target gender: Man ✅

Viewer looking for: Men
Target gender: Woman ❌

Viewer looking for: Everyone
Target gender: (anything) ✅

Target looking for: Women
Viewer gender: Woman ✅

Target looking for: Women
Viewer gender: Man ❌
```

This ensures both sides are compatible, not just one direction.

#### Like → Match Detection

When a user likes someone, SparkBot immediately checks if that person has already liked the viewer back:

```python
# After recording the like, reload fresh DB to avoid race conditions
fresh_db = database.load_db()
target = database.get_user(fresh_db, target_id)
if str(viewer_id) in (target.get("likes", []) + target.get("super_likes_sent", [])):
    do_match(fresh_db, viewer_id, int(target_id))
```

Note: The DB is reloaded fresh before checking — this prevents race conditions where two users like each other simultaneously and both get double-notified.

#### Super Like

Super likes are a premium-feeling gesture:
- Immediately notifies the target user that someone super liked them — **and reveals who** (unlike regular likes)
- Counts as a like for match detection purposes
- Free users: 1 per day
- Premium users: 5 per day

Super like notification sent to target:
```
⭐ You got a Super Like!

Priya from Mumbai super liked you!

Start swiping to find them! /browse
```

#### Match Notification

When a mutual match is detected:

```
🎉 It's a Match!

You and Priya both liked each other!

Their username: @priya123
Say hello! 👋

💡 Conversation Starter:
"You both love hiking! Ask them about their favourite trail. 🏔️"
```

Both matched users receive this notification (if they have match notifications enabled).

#### No More Profiles

When the queue is empty:

```
😔 No more profiles right now.
Check back later or update your preferences!
```

With buttons: `🏠 Main Menu` | `✏️ Edit Prefs`

---

### 4. Match System

Matches are stored bidirectionally — when A and B match, `A.matches` contains `B_id` and `B.matches` contains `A_id`.

#### /matches Command

Shows all current matches as a formatted list:

```
💌 Your Matches!

• Priya, 23 — Mumbai — @priya123
• Anjali, 25 — Delhi — @anjali_d
• Neha, 22 — Pune — (no username)
```

If no matches yet:

```
💌 No matches yet!

Keep swiping — your match is out there! 🔥

💡 Complete your profile to get more likes!
```

#### Match Data Stored

```json
{
  "matches": ["12345678", "87654321"]
}
```

Simple array of user IDs. On display, the full user profile is looked up from `db["users"]`.

---

### 5. Profile Management

#### Viewing Your Profile — /profile

Shows your own profile card with:
- Full profile card (photo + caption)
- Profile completeness bar
- Completeness tip
- Boost status
- Edit and Boost buttons

Example output:

```
💫 Rohan, 24
📍 Delhi
🎯 Looking for: Women
🕐 Active today

📝 Engineer by day, guitarist by night 🎸

✨ Interests: music, coding, coffee, travel, gaming

━━━━━━━━━━━━━━━━━━

Profile Strength: ██████████ 100%
🌟 Profile 100% complete!
⚡ 1 boost available this week
```

#### Editing Your Profile — /editprofile

Shows an inline keyboard menu:

```
✏️ Edit Profile

What would you like to change?

[✏️ Name]     [🎂 Age]
[📝 Bio]      [📸 Photo]
[✨ Interests] [🏙️ City]
[💘 Looking For]
[🔙 Back]
```

Each option puts the user into the corresponding edit state and prompts for input.

#### Edit States

| Button | State | Input Type |
|--------|-------|------------|
| Name | `edit_name` | Text |
| Age | `edit_age` | Number |
| Bio | `edit_bio` | Text (max 300) |
| Photo | `edit_photo` | Photo message |
| Interests | `edit_interests` | Comma-separated text |
| City | `edit_city` | Text |
| Looking For | `edit_lf` | Inline buttons |

After each edit, the user gets a confirmation message and a "Back to Edit Menu" button.

#### Deleting Your Profile — /deleteprofile

Double-confirmation flow:

```
🗑️ Delete Account

⚠️ This will permanently delete your profile, matches, and all data.

Are you sure? This cannot be undone.

[✅ Yes, delete everything]
[❌ No, keep my account]
```

On confirmation:
- User entry deleted from `db["users"]`
- User ID removed from all other users' `likes`, `passes`, `matches`, `super_likes_*`, etc.
- Database saved
- Farewell message sent

---

### 6. Reporting & Safety

Safety is built into the browse loop, not as an afterthought.

#### Reporting a Profile

Every profile card has a `📛 Report` button. Clicking it shows a reason picker:

```
📛 Report User

Reason?

[🤥 Fake Profile]     [🔞 Inappropriate Photo]
[😡 Harassment]       [💬 Spam]
[❓ Other]
[🔙 Cancel]
```

After selecting a reason:
- Report stored in `db["reports"]`
- Reporter's report added to `user["reports_made"]`
- Target's `reports_received` incremented
- Target automatically added to reporter's `passes` (won't see them again)
- **Target is NOT notified** — they won't know they were reported

#### Auto-Soft-Ban

If a user accumulates **3 or more reports from different users**, they are automatically hidden from the browse queue. This is enforced at queue-build time:

```python
if len(u.get("reports_received", [])) >= 3:
    continue  # Skip this user from queue
```

The user still exists, can still use the bot, but nobody can see their profile anymore. Admins can manually review and hard-ban or unban.

#### Blocking Users — /block

```
/block @username
```

Blocked users:
- Can no longer see your profile
- Can no longer match with you
- Stored in `user["blocked"]`

Blocking is also enforced bidirectionally in the queue builder.

#### Report Storage Structure

```json
{
  "reporter_id":   "123456",
  "reporter_name": "Rohan",
  "reported_id":   "789012",
  "reported_name": "Unknown",
  "reason":        "Fake Profile",
  "timestamp":     "2026-03-22T10:30:00+00:00"
}
```

---

### 7. Boost System

Boosts are a power-up that put your profile first in everyone's browse queue for 30 minutes.

#### How Boosts Work

1. User runs `/boost` or taps the Boost button
2. Bot confirms available boosts
3. User taps "🚀 Boost Now!"
4. `user["is_boosted"] = True`
5. `user["boost_expires"] = now + 30 minutes`
6. `user["boosts_used_this_week"] += 1`

During queue building, boosted profiles are scored highest (800+ points) and appear first.

#### Boost Expiry

Boost expiry is checked on every user interaction via `check_boost()`:

```python
def check_boost(user: dict) -> None:
    if user.get("is_boosted") and user.get("boost_expires"):
        if utcnow() > parse_iso(user["boost_expires"]):
            user["is_boosted"] = False
            user["boost_expires"] = None
```

No background job needed — the check runs inline on every update.

#### Weekly Reset

Boost usage resets every 7 days, tracked via `boost_week_reset`:

```python
if utcnow() - parse_iso(reset) > timedelta(days=7):
    user["boosts_used_this_week"] = 0
    user["boost_week_reset"] = now_iso()
```

#### Boost Quotas

| User Type | Boosts per Week |
|-----------|----------------|
| Free | 1 |
| Premium | 3 |

#### Profile Boost Status Display

In `/profile`:

```
🚀 Boosted (expires in 22 min)
```
or
```
⚡ 1 free boost available
```
or
```
❌ No boosts left this week
```

---

### 8. Daily Limits

SparkBot enforces daily usage limits to create a sustainable engagement model and encourage premium upgrades.

#### Free User Limits

| Action | Daily Limit |
|--------|-------------|
| Likes | 20 |
| Super Likes | 1 |
| Undos | 1 |

#### Premium User Limits

| Action | Daily Limit |
|--------|-------------|
| Likes | Unlimited |
| Super Likes | 5 |
| Undos | Unlimited |

#### Daily Reset Logic

Limits reset at **midnight UTC**, tracked by `limits_reset_date` (a `YYYY-MM-DD` string):

```python
def check_limits(user: dict) -> None:
    today = utcnow().strftime("%Y-%m-%d")
    if user.get("limits_reset_date") != today:
        user["likes_today"] = 0
        user["super_likes_today"] = 0
        user["undos_today"] = 0
        user["limits_reset_date"] = today
```

No cron job. No scheduler. Just a date comparison on every interaction.

#### Limit Hit Messages

When a free user hits their like limit:

```
❌ You've used all your likes today! Come back tomorrow 💔 or go Premium ⭐

[⭐ Go Premium]
```

Remaining likes shown in browse mode on the Like button:
```
❤️ Like (14 left)
```

---

### 9. Premium — Telegram Stars

SparkBot uses **Telegram's native Stars payment system** — no Stripe, no Razorpay, no external payment processor needed.

#### What is Telegram Stars?

Telegram Stars (XTR) are Telegram's in-app currency. Users purchase Stars through the Telegram app using their local payment method, then spend them inside bots. The bot receives Stars directly.

#### Premium Price

**50 Telegram Stars per month** (~$1 USD, varies by country).

#### Premium Benefits

| Feature | Free | Premium |
|---------|------|---------|
| Likes per day | 20 | Unlimited |
| Super likes per day | 1 | 5 |
| See who liked you | ❌ | ✅ |
| Boosts per week | 1 | 3 |
| Undos per day | 1 | Unlimited |
| Premium badge (✨) | ❌ | ✅ |
| Browse queue priority | Normal | Higher |

#### Payment Flow

```
User taps "⭐ Buy Premium — 50 Stars"
  └── sendInvoice called (currency: XTR)
        └── Telegram shows native payment UI
              └── User confirms payment
                    ├── pre_checkout_query received → answerPreCheckoutQuery(ok=True)
                    └── successful_payment received
                          ├── user["is_premium"] = True
                          ├── user["premium_expires"] = now + 30 days
                          └── Confirmation message sent
```

#### Premium Expiry

Premium expiry is checked on every user interaction:

```python
def check_premium(user: dict) -> None:
    if user.get("is_premium") and user.get("premium_expires"):
        if utcnow() > parse_iso(user["premium_expires"]):
            user["is_premium"] = False
            user["premium_expires"] = None
```

Users are automatically downgraded when their premium expires. No manual action needed.

#### /wholikedme — Premium Only

Premium users can see a list of people who liked them but haven't been swiped on yet:

```
❤️ People who liked you:

• Priya, 23 — Mumbai
• Anjali, 25 — Delhi
• Neha, 22 — Pune
```

If the viewer has already matched with someone in the list, they're excluded (already seen).

---

### 10. Admin Panel

SparkBot includes a comprehensive admin panel accessible only to the configured `ADMIN_CHAT_ID`.

#### Security

Admin commands are silently ignored for non-admin users — no error message, no indication that the command exists:

```python
def is_admin(cid: int) -> bool:
    return int(cid) == int(config.ADMIN_CHAT_ID or 0)

def admin_stats(cid: int, db: dict) -> None:
    if not is_admin(cid): return  # Silent ignore
    # ... rest of function
```

#### /admin_stats

```
📊 Admin Stats

👥 Total users: 1,247
🟢 Active today: 89
💌 Total matches: 3,891
📛 Reports: 12
✨ Premium users: 47
⭐ Stars earned: 2,350
```

Active today = users with `last_seen` within the last 24 hours.

#### /admin_ban [user_id]

```
/admin_ban 123456789
```

- Sets `user["is_banned"] = True`
- Sends user a suspension notice:
  ```
  🚫 Your account has been suspended. Contact support.
  ```
- Confirms to admin: `✅ Banned: 123456789 (Priya)`

#### /admin_unban [user_id]

```
/admin_unban 123456789
```

- Sets `user["is_banned"] = False`
- Confirms to admin: `✅ Unbanned: 123456789 (Priya)`

#### /admin_reports

Shows the last 20 reports with full details:

```
📛 Reports (last 20):

Reporter: Rohan (123456)
Reported: Unknown (789012)
Reason: Fake Profile | 2026-03-22T10:30:00
────
Reporter: Anjali (345678)
Reported: Priya (901234)
Reason: Harassment | 2026-03-21T15:22:00
────
```

#### /admin_broadcast [message]

```
/admin_broadcast Hey everyone! New update just dropped! 🎉
```

Sends the message to ALL users who have broadcast notifications enabled. Includes a 0.1 second delay between each message to avoid hitting Telegram's flood limits.

```
📢 Done! Sent: 1,201 | Failed: 46
```

#### /admin_user [user_id]

Full profile dump for any user:

```
👤 User 123456789

Name: Priya | Age: 23
Gender: Woman | City: Mumbai
Username: @priya123
Premium: ✅ | Banned: ✅
Matches: 3 | Likes sent: 47
Reports received: 0
Joined: 2026-03-01 | Last seen: 2026-03-22T10:30:00
```

---

### 11. Smart Matching Algorithm

SparkBot's browse queue isn't random — it uses a **priority scoring system** with 8 tiers.

#### Scoring Algorithm

```python
def build_queue(db, viewer_id):
    # Filter eligible profiles
    # Score each profile
    # Sort descending by score
    # Return sorted list of user IDs
```

#### Score Components

| Priority | Condition | Score Bonus |
|----------|-----------|-------------|
| 1st | Premium + Boosted | +1000 |
| 2nd | Boosted only | +800 |
| 3rd | Premium only | +600 |
| 4th | Common interests | +20 per shared interest |
| 5th | Same city | +100 |
| 6th | Active in last 24h | +80 |
| 7th | New profile (< 7 days) | +50 |
| 8th | Profile completeness | +0 to +100 |

#### Why This Order?

- **Premium + Boosted first**: These users have invested in the platform — showing them first rewards that investment and creates a flywheel effect.
- **Common interests high weight**: Matching on shared interests increases conversation quality and match rates.
- **Same city**: Local connections are more actionable, especially for in-person dates.
- **Recently active**: Active users are more likely to respond. Showing inactive profiles wastes everyone's time.
- **New profiles**: New user excitement is highest in the first week. Getting them matches quickly reduces churn.
- **Profile completeness**: Incomplete profiles convert poorly. Showing them last protects other users' experience while incentivizing completion.

#### Example Scoring

```
User A: Premium + Boosted, 3 common interests, same city, active today
Score = 1000 + (3×20) + 100 + 80 = 1,240

User B: Boosted, 1 common interest, different city, active this week
Score = 800 + (1×20) + 0 + 0 + 75 (completeness) = 895

User C: Free, no boost, 5 common interests, same city, new profile
Score = 0 + (5×20) + 100 + 80 + 50 + 75 = 405

Queue order: A → B → C
```

---

### 12. Last Seen & Activity

Every user interaction updates `last_seen` to the current UTC timestamp. This happens in `touch(user)`, called from `run_checks()`:

```python
def touch(user: dict) -> None:
    user["last_seen"] = now_iso()
```

`run_checks()` is called at the top of every handler, ensuring no interaction goes untracked.

#### Activity Labels in Browse

```
🟢 Online now        → last_seen < 5 minutes ago
🕐 Active today      → last_seen < 24 hours ago
📅 Active this week  → last_seen < 7 days ago
💤 A while ago       → older
```

These labels appear on every profile card, helping users make informed swipe decisions. Active users get matched faster.

---

### 13. Notifications

Users can granularly control which notifications they receive via `/notifications`.

#### Notification Types

| Type | Toggle Key | What It Controls |
|------|-----------|------------------|
| ❤️ Match notifications | `matches` | Sent when a mutual match happens |
| ⭐ Super like alerts | `super_likes` | Sent when someone super likes you |
| 📢 Broadcast messages | `broadcasts` | Admin broadcast messages |

#### Toggle UI

```
🔔 Notification Settings

[❤️ Match notifications: ✅ ON]
[⭐ Super like alerts: ✅ ON]
[📢 Broadcast messages: ❌ OFF]
[🔙 Back]
```

Tapping any button immediately toggles it and refreshes the menu.

#### Enforcement

Before sending any notification, the bot checks the recipient's preferences:

```python
if target.get("notifications", {}).get("matches", True):
    send_match_notification(target_id, ...)
```

Default is `True` for all notifications — opting out, not opting in.

---

### 14. Undo Last Swipe

The undo feature allows recovering from accidental passes.

#### Limitations

- Only **Pass** can be undone (not Like or Super Like)
- Free users: **1 undo per day**
- Premium users: **Unlimited undos**
- Only the **most recent** pass can be undone (tracked via `last_swiped_user`)

#### Flow

```
/undo
  ├── Check: last_swiped_user exists and is in passes[]?
  │     └── No → "Nothing to undo! Start swiping 👉 /browse"
  ├── Check: undo limit not exceeded (or is premium)
  │     └── No → "Get Premium for unlimited undos ⭐"
  └── Remove target from passes[]
        └── "↩️ Last pass undone! Tap /browse to see them again."
```

After undoing, the user will see that profile again on next browse (it's no longer in their passes list).

---

### 15. Profile Completeness Score

SparkBot gamifies profile completion with a visual progress bar.

#### Scoring Breakdown

| Field | Points |
|-------|--------|
| Photo | 30 |
| Bio (any text) | 25 |
| 5+ Interests | 25 |
| City | 20 |
| **Total** | **100** |

#### Visual Bar

```
Profile Strength: ████████░░ 80%
💡 Tip: Add 5+ interests (+25%)
```

The bar uses Unicode block characters (█ filled, ░ empty) — 10 blocks total, each representing 10%.

#### Impact on Browse Queue

Profile completeness directly affects browse queue position. A 100% complete profile gets +100 score bonus over an incomplete one. This incentivises users to complete their profiles — not through nagging, but through measurable dating success.

#### Completion Tips

The tip shown is always the **highest-value missing field**:
1. Photo (30 pts) — shown first if missing
2. Bio (25 pts) — shown if no bio
3. Interests (25 pts) — shown if fewer than 5
4. City (20 pts) — shown last

---

### 16. Conversation Starters

When a match happens, SparkBot automatically generates a personalised conversation starter for both users.

#### Interest-Based Starters

If both users share a common interest, a targeted starter is generated:

```
💡 Conversation Starter:
"You both love hiking! Ask them about their favourite trail. 🏔️"
```

Interest-to-starter mappings cover: music, travel, books, hiking, coffee, food, movies, gaming, fitness, art, photography, cooking, yoga, dancing, writing.

#### Generic Starters (Fallback)

If no common interests exist, one of 20 fun generic starters is randomly selected:

```
"If you could live anywhere in the world, where would it be? 🌍"
"What's the most spontaneous thing you've ever done? 🎲"
"Describe your perfect weekend in 3 words. 🌟"
```

#### Logic Flow

```python
def conversation_starter(u1, u2):
    common = (
        set(u1["interests"]) & set(u2["interests"])
    )
    for interest in common:
        if interest in _INTEREST_STARTERS:
            return _INTEREST_STARTERS[interest]
    if common:
        return f"You both love {random.choice(list(common))}! ✨"
    return random.choice(_GENERIC_STARTERS)
```

---

### 17. Help & FAQ

`/help` shows a formatted, comprehensive FAQ:

```
❓ Help & FAQ

How does matching work?
Both users must like each other. When that happens — it's a Match! 🎉

How to edit my profile?
Use /editprofile or tap Edit in /profile

What is Super Like?
Super Like immediately notifies the other person that you super liked them! ⭐

What is Boost?
Puts your profile first in everyone's browse queue for 30 minutes. 🚀

How to report someone?
Tap the 📛 Report button while browsing any profile.

How to go Premium?
Use /premium to unlock all features with Telegram Stars ⭐

How to delete my account?
Use /deleteprofile — permanent and irreversible!

📬 Contact support: @youradmin
```

---

## 🏗️ Architecture

### File Structure

```
sparkbot/
├── bot.py           → Main polling loop + all handlers + business logic
├── db.py            → Database read/write functions
├── config.py        → All constants and environment variables
├── requirements.txt → Only: requests
├── Dockerfile       → Python 3.11 slim container
├── db.json          → Live database (auto-created on first run)
├── db_backup.json   → Auto-backup written on every save
└── errors.log       → All errors with timestamps (auto-created)
```

#### Why One File for Logic?

`bot.py` contains everything — handlers, business logic, formatting, queue building, payment processing. This is an intentional choice for a project of this scale:

- **One file to read** when debugging
- **One file to search** when finding where something happens
- **No circular imports** from splitting into too many modules
- **Clear execution flow** from top to bottom

If SparkBot grows significantly (thousands of users, dozens of new features), splitting into `handlers/`, `services/`, `utils/` becomes worthwhile. At current scale, one file wins.

---

### State Machine

Every user has a `state` field that controls how their messages are interpreted. This is the heart of the bot's conversational UX.

#### All States

```
ONBOARDING
├── setup_name          → Waiting for name text
├── setup_age           → Waiting for age number
├── setup_gender        → Waiting for gender button click
├── setup_lf            → Waiting for looking_for button click
├── setup_city          → Waiting for city text
├── setup_bio           → Waiting for bio text
├── setup_interests     → Waiting for interests text
├── setup_photo         → Waiting for photo message
└── setup_confirm       → Waiting for profile confirm button

EDITING
├── edit_name           → Waiting for new name
├── edit_age            → Waiting for new age
├── edit_bio            → Waiting for new bio
├── edit_photo          → Waiting for new photo
├── edit_interests      → Waiting for new interests
├── edit_city           → Waiting for new city
└── edit_lf             → Waiting for looking_for button

ACTIVE
├── idle                → No pending action, shows main menu on commands
├── browsing            → In browse mode
└── reporting           → Showing report reason picker

DANGEROUS
└── confirming_delete   → Waiting for delete confirmation button
```

#### State Machine Flow Diagram

```
/start (new user)
     │
     ▼
setup_name ──[text]──► setup_age ──[18-60]──► setup_gender
                                     │
                               setup_lf ──[btn]──► setup_city
                                                        │
                                                   setup_bio ──[text]──► setup_interests
                                                                                │
                                                                         setup_photo ──[photo]──► setup_confirm
                                                                                                       │
                                                                                              [Yes]─────┤
                                                                                                        │
                                                                                                     idle ◄─────┐
                                                                                              [Edit]────┘        │
                                                                                                        ┌─────────┘
                                                                                                  edit_* states
```

#### State Resolution

In `on_text()`, the state machine is a simple `if/elif` chain:

```python
state = user.get("state", "idle")

if state == "setup_name":
    # handle name input
elif state == "setup_age":
    # handle age input
elif state == "edit_bio":
    # handle bio edit
# ... etc
```

When `/start` is sent mid-flow, state resets to `idle` and `state_data` is cleared — always a clean escape hatch.

#### state_data{}

A temporary scratchpad used during multi-step flows (mainly onboarding):

```json
"state_data": {
  "name": "Priya",
  "age": 23,
  "gender": "Woman"
}
```

Data accumulates here through the onboarding steps. Only on final confirmation does it get merged into the root user fields. This means an abandoned onboarding leaves no partial profile.

---

### Database Design

SparkBot uses a single `db.json` file as its entire database. This is a deliberate design choice — not a limitation.

#### Why JSON, Not SQL?

For a bot with up to ~5,000 users, a JSON file is:
- **Zero setup** — no database server, no connection strings, no migrations
- **Zero cost** — no database hosting fees
- **Readable** — you can open db.json and read it directly
- **Portable** — back it up with `cp db.json backup.json`
- **Debuggable** — edit it manually to fix data issues

The tradeoff: JSON doesn't scale beyond ~10,000 users with complex queries. At that point, migrating to Supabase (which SparkBot's code can be adapted for) becomes worthwhile.

#### Read/Write Pattern

SparkBot uses a **read-heavy, write-on-change** pattern:

```
Every update received:
  1. Load full db.json into memory
  2. Process the update (may modify user data)
  3. Write full db.json back to disk
```

This is safe because:
- Long polling means one update processed at a time per bot instance
- DB writes use `json.dump()` which is atomic at the OS level on most filesystems
- 3-retry logic handles transient write failures

#### The Backup System

Every write writes TWO files: `db.json` and `db_backup.json`. On startup:

```python
for fname in [DB_FILE, BACKUP_FILE]:
    if os.path.exists(fname):
        try:
            with open(fname) as f:
                return json.load(f)
        except:
            continue
# Both failed → return fresh empty DB
```

This handles the rare case of `db.json` getting corrupted mid-write (process killed at the wrong moment).

---

### Polling Loop

SparkBot uses **long polling** — the simplest reliable way to receive Telegram updates without a webhook server.

```python
def main():
    offset = 0
    while True:
        r = requests.get(
            f"{BASE}/getUpdates",
            params={
                "offset":  offset,
                "timeout": 30,
                "allowed_updates": ["message", "callback_query", "pre_checkout_query"],
            },
            timeout=35,
        )
        for upd in r.json().get("result", []):
            offset = upd["update_id"] + 1
            db = database.load_db()  # Fresh DB per update
            dispatch(upd, db)
```

Key details:
- `timeout=30` — Telegram holds the connection open for up to 30 seconds if no updates
- `timeout=35` — requests timeout is slightly longer to account for network latency
- `offset = update_id + 1` — tells Telegram we've processed this update, don't resend
- Fresh DB load per update — ensures no stale state between users

#### Why Not Webhooks?

Webhooks require:
- A public HTTPS URL
- SSL certificate
- A web server running (Flask/FastAPI/etc)

Long polling requires:
- Nothing extra — just an outbound HTTPS request

For a Railway deployment, long polling is simpler and equally reliable.

---

### Dispatcher

The dispatcher routes every incoming Telegram update to the correct handler:

```python
def dispatch(update, db):
    # 1. Check for pre_checkout_query (payment authorization)
    if "pre_checkout_query" in update:
        on_pre_checkout(update["pre_checkout_query"], db)
        return

    # 2. Check for callback_query (button clicks)
    if "callback_query" in update:
        on_callback(update["callback_query"], db)
        return

    # 3. Get message object
    msg = update.get("message", {})

    # 4. Check for successful_payment
    if "successful_payment" in msg:
        on_payment(cid, msg["successful_payment"], db)
        return

    # 5. Check for photo
    if "photo" in msg:
        on_photo(cid, msg["photo"], db)
        return

    # 6. Check for text
    if "text" in msg:
        on_text(cid, msg["text"], from_user, db)
        return
```

Order matters — `pre_checkout_query` must be answered immediately (Telegram has a 10-second timeout for it), so it's checked first.

---

## ⚡ Quick Start

### Prerequisites

- Python 3.11+
- A Telegram Bot Token (from @BotFather)
- Your Telegram User ID (from @userinfobot)
- Git
- `requests` library

### Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/REALNYXAETHER/Sparkbot.git
cd Sparkbot

# 2. Install dependencies
pip install requests

# 3. Set environment variables
export TELEGRAM_TOKEN="your_bot_token_here"
export ADMIN_CHAT_ID="your_telegram_user_id"
export ADMIN_USERNAME="yourusername"

# 4. Run the bot
python bot.py
```

On Windows (PowerShell):

```powershell
$env:TELEGRAM_TOKEN="your_bot_token_here"
$env:ADMIN_CHAT_ID="your_telegram_user_id"
$env:ADMIN_USERNAME="yourusername"
python bot.py
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_TOKEN` | ✅ | Bot token from @BotFather |
| `ADMIN_CHAT_ID` | ✅ | Your numeric Telegram user ID |
| `ADMIN_USERNAME` | ✅ | Your Telegram username (without @) |

#### Getting Your TELEGRAM_TOKEN

1. Open Telegram → search `@BotFather`
2. Send `/newbot`
3. Follow prompts to name your bot
4. BotFather sends you a token like: `7123456789:AAExxxxxxxxxxxxxxxxxxxxxxxxxxxx`
5. Copy it — that's your `TELEGRAM_TOKEN`

#### Getting Your ADMIN_CHAT_ID

1. Open Telegram → search `@userinfobot`
2. Send `/start`
3. It replies with your ID: `Id: 123456789`
4. That number is your `ADMIN_CHAT_ID`

---

## 🚂 Deployment on Railway

Railway is the recommended hosting platform for SparkBot. The free tier provides $5/month credit, which is more than enough for a Telegram bot.

### Step 1 — Push to GitHub

If you're on Android (using Termux):

```bash
# Navigate to your bot folder
cd '/storage/emulated/0/Dating Bot'

# Fix ownership (Android quirk)
git config --global --add safe.directory '/storage/emulated/0/Dating Bot'

# Stage all files
git add .

# Commit
git commit -m "SparkBot initial commit"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/REALNYXAETHER/Sparkbot.git

# Push
git branch -M main
git push -u origin main
```

**Authentication Note**: GitHub no longer accepts passwords via HTTPS. Use a **Personal Access Token (PAT)**:

1. Go to `github.com`
2. Click your profile picture → **Settings**
3. Left sidebar → **Developer Settings**
4. **Personal Access Tokens** → **Tokens (classic)**
5. Click **Generate new token (classic)**
6. Give it a name like `sparkbot-deploy`
7. Tick the **repo** checkbox (full repo access)
8. Scroll down → **Generate token**
9. **Copy the token immediately** — you can't see it again
10. Use this token as your password when `git push` prompts for it

### Step 2 — Connect Railway

1. Go to **railway.app**
2. Sign in with GitHub
3. Click **New Project**
4. Select **Deploy from GitHub repo**
5. Authorize Railway to access your GitHub
6. Select the `Sparkbot` repository
7. Railway auto-detects the `Dockerfile` and begins building

### Step 3 — Set Environment Variables

In your Railway project dashboard:

1. Click on your service (the Sparkbot deployment)
2. Go to the **Variables** tab
3. Add these variables:

```
TELEGRAM_TOKEN    = 7123456789:AAExxxxxxxxxxxxxxxxxxxxxxxx
ADMIN_CHAT_ID     = 123456789
ADMIN_USERNAME    = yourusername
```

Click **Add** after each one.

### Step 4 — Deploy

Railway automatically redeploys whenever:
- You push new commits to GitHub
- You change environment variables

Your first deployment starts automatically after adding variables. Watch the **Deployments** tab to see the build logs.

When you see:
```
🚀 SparkBot starting...
```

in the logs — the bot is live!

### Persisting db.json with Railway Volumes

By default, `db.json` lives inside the container and **resets on every redeploy**. This means losing all user data on every update.

**Fix: Mount a Railway Volume**

1. In your Railway project → **Add** → **Volume**
2. Name it `sparkbot-data`
3. Set mount path to `/app`
4. Railway now persists everything in `/app` across deploys

With the volume mounted, `db.json` and `db_backup.json` survive redeploys indefinitely.

**Alternative: External Database**

For a more robust solution, migrate to a free **Supabase** PostgreSQL database. This requires changing `db.py` to use `psycopg2` or `supabase-py` instead of `json`, but all the business logic in `bot.py` stays the same.

---

## 🤖 BotFather Setup

After your bot is live, configure it properly in BotFather for the best user experience.

### Set Commands

Send `/setcommands` to @BotFather, select your bot, then paste:

```
start - Start or return to main menu
browse - Start swiping
matches - View your matches
profile - View your profile
editprofile - Edit your profile
wholikedme - See who liked you (Premium)
boost - Boost your profile
undo - Undo last pass
premium - Go Premium with Telegram Stars
notifications - Manage notifications
deleteprofile - Delete your account
help - Help and FAQ
```

### Set Description

Send `/setdescription` → Select bot → Paste:

```
💘 SparkBot — Your Telegram Dating App

Find your spark, one swipe at a time. Match, chat, and connect — all inside Telegram.

✨ Features:
• Tinder-style swipe browsing
• Smart matching by interests & location
• Super Likes, Boosts, and Premium
• Safe reporting & blocking
• No personal data sold. Ever.
```

### Set About Text

Send `/setabouttext`:

```
SparkBot is a privacy-first dating bot. Your data stays in the bot — no third-party sharing, no ads.
```

### Set Profile Photo

Send `/setuserpic` to give your bot a profile image. Use a colorful heart or fire emoji rendered as an image for maximum visibility.

### Enable Inline Mode (Optional)

If you want users to be able to share their profiles inline:
Send `/setinline` → Select bot → Set inline placeholder text.

---

## 📋 Commands Reference

### User Commands

| Command | Description | Available To |
|---------|-------------|--------------|
| `/start` | Start bot or return to main menu | Everyone |
| `/browse` | Start swiping through profiles | Registered users |
| `/matches` | View all your current matches | Registered users |
| `/profile` | View your own profile card | Registered users |
| `/editprofile` | Edit profile fields via menu | Registered users |
| `/wholikedme` | See who liked you | Premium only |
| `/boost` | Boost your profile for 30 minutes | Registered users |
| `/undo` | Undo your last pass | Registered users |
| `/premium` | View Premium benefits and buy | Everyone |
| `/notifications` | Toggle notification preferences | Registered users |
| `/deleteprofile` | Permanently delete your account | Registered users |
| `/help` | Show help and FAQ | Everyone |

### Admin Commands

| Command | Description |
|---------|-------------|
| `/admin_stats` | Show platform statistics |
| `/admin_ban [user_id]` | Ban a user |
| `/admin_unban [user_id]` | Unban a user |
| `/admin_reports` | View latest 20 reports |
| `/admin_broadcast [message]` | Send message to all users |
| `/admin_user [user_id]` | View any user's full profile |

Admin commands only respond to messages from `ADMIN_CHAT_ID`. All others are silently ignored.

---

## 📊 Admin Panel

Full documentation of the admin system.

### Accessing the Admin Panel

Simply send admin commands from your Telegram account with the `ADMIN_CHAT_ID` that matches the environment variable. No passwords, no login UI — your Telegram ID is the authentication.

### Stats Explained

```
📊 Admin Stats

👥 Total users: 1,247          ← len(db["users"])
🟢 Active today: 89            ← last_seen within 24h
💌 Total matches: 3,891        ← db["total_matches"] (incremented on each match)
📛 Reports: 12                 ← len(db["reports"])
✨ Premium users: 47           ← users where is_premium == True
⭐ Stars earned: 2,350         ← db["total_stars_earned"]
```

### Banning a User

When you ban a user with `/admin_ban 123456789`:

1. `user["is_banned"] = True`
2. Bot attempts to notify the banned user
3. On next interaction, banned user sees: `🚫 Account suspended. Contact support.`
4. Banned user's profile disappears from all browse queues

The user's data is preserved — the ban is reversible via `/admin_unban`.

### Broadcasting

The broadcast system respects users' notification preferences:

```python
for uid, u in db["users"].items():
    if u.get("notifications", {}).get("broadcasts", True):
        send_msg(int(uid), f"📢 Announcement\n\n{message}")
        time.sleep(0.1)  # Anti-flood delay
```

The 0.1 second delay means broadcasting to 1,000 users takes ~1.7 minutes. For larger user bases, consider batching or async sending.

---

## ⭐ Premium — Telegram Stars

### How Telegram Stars Work

Telegram Stars are an in-app purchase system built into Telegram itself. Users don't need to enter credit card details into your bot — they buy Stars through Telegram's own payment UI.

From your perspective as a bot developer:
1. You call `sendInvoice` with `currency="XTR"` and `amount=50`
2. Telegram shows the payment UI to the user
3. Telegram sends you `pre_checkout_query` — you must answer within 10 seconds
4. If the user confirms, Telegram sends `successful_payment`
5. Stars are transferred to your bot's Stars balance
6. You withdraw Stars through BotFather

### Setting Up Stars Payments

Stars payments don't require any additional setup beyond having a bot token. You do NOT need a `provider_token` (leave it empty string `""` for Stars).

### Viewing Your Earnings

In BotFather:
- `/mybots` → Select your bot → **Payments** → View Stars balance

### Refund Policy Considerations

Telegram's Stars refund policy: Users can request refunds within 7 days if they haven't used the service. Plan your Premium terms accordingly.

### Testing Payments

During development, you can test the payment flow by:
1. Setting price to 1 Star (minimum)
2. Using your own account to purchase
3. Verifying `successful_payment` is received

---

## 🗄️ Database Schema — Full Reference

Complete documentation of every field in `db.json`.

### Top-Level Structure

```json
{
  "users": {},
  "reports": [],
  "total_matches": 0,
  "total_stars_earned": 0
}
```

### User Object — Complete Field Reference

```json
{
  "name": "Priya",
  "age": 23,
  "gender": "Woman",
  "looking_for": "Men",
  "city": "Mumbai",
  "bio": "Coffee addict ☕",
  "interests": ["music", "travel", "books"],
  "photo_file_id": "AgACAgI...",
  "username": "priya123",
  "likes": [],
  "passes": [],
  "matches": [],
  "super_likes_sent": [],
  "super_likes_received": [],
  "who_liked_me": [],
  "reports_received": [],
  "reports_made": [],
  "blocked": [],
  "is_banned": false,
  "is_premium": false,
  "premium_expires": null,
  "is_boosted": false,
  "boost_expires": null,
  "boosts_used_this_week": 0,
  "boost_week_reset": null,
  "likes_today": 0,
  "super_likes_today": 0,
  "undos_today": 0,
  "limits_reset_date": "2026-03-22",
  "last_swiped_user": null,
  "last_seen": "2026-03-22T10:30:00+00:00",
  "joined": "2026-03-20T08:00:00+00:00",
  "notifications": {
    "matches": true,
    "super_likes": true,
    "broadcasts": true
  },
  "state": "idle",
  "state_data": {}
}
```

### Field Reference Table

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | User's display name |
| `age` | integer | Age (18–60) |
| `gender` | string | "Man", "Woman", or "Non-binary" |
| `looking_for` | string | "Men", "Women", or "Everyone" |
| `city` | string | User's city |
| `bio` | string | Profile bio (max 300 chars) |
| `interests` | list[str] | Up to 10 interests |
| `photo_file_id` | string | Telegram file_id of profile photo |
| `username` | string | Telegram @username (without @) |
| `likes` | list[str] | User IDs this user has liked |
| `passes` | list[str] | User IDs this user has passed on |
| `matches` | list[str] | User IDs matched with |
| `super_likes_sent` | list[str] | User IDs super-liked |
| `super_likes_received` | list[str] | User IDs who super-liked this user |
| `who_liked_me` | list[str] | User IDs who liked this user (for /wholikedme) |
| `reports_received` | list[str] | User IDs who reported this user |
| `reports_made` | list[str] | User IDs this user has reported |
| `blocked` | list[str] | User IDs this user has blocked |
| `is_banned` | boolean | Admin hard ban flag |
| `is_premium` | boolean | Premium status |
| `premium_expires` | string\|null | ISO timestamp of premium expiry |
| `is_boosted` | boolean | Active boost flag |
| `boost_expires` | string\|null | ISO timestamp of boost expiry |
| `boosts_used_this_week` | integer | Count of boosts used this week |
| `boost_week_reset` | string\|null | ISO timestamp of last boost week reset |
| `likes_today` | integer | Likes sent today (reset at midnight UTC) |
| `super_likes_today` | integer | Super likes sent today |
| `undos_today` | integer | Undos used today |
| `limits_reset_date` | string | YYYY-MM-DD of last limit reset |
| `last_swiped_user` | string\|null | User ID of most recently passed profile |
| `last_seen` | string | ISO timestamp of last bot interaction |
| `joined` | string | ISO timestamp of account creation |
| `notifications.matches` | boolean | Match notification preference |
| `notifications.super_likes` | boolean | Super like notification preference |
| `notifications.broadcasts` | boolean | Broadcast notification preference |
| `state` | string | Current conversation state |
| `state_data` | dict | Temporary storage during multi-step flows |

### Report Object

```json
{
  "reporter_id":   "123456",
  "reporter_name": "Rohan",
  "reported_id":   "789012",
  "reported_name": "Priya",
  "reason":        "Fake Profile",
  "timestamp":     "2026-03-22T10:30:00+00:00"
}
```

---

## 📝 Code Walkthrough

A line-by-line tour of SparkBot's architecture.

### bot.py

#### Imports and Setup

```python
import json, logging, os, random, time
from datetime import datetime, timedelta, timezone
import requests
import config
import db as database
```

Only the standard library plus `requests`. The `json` import is for in-code JSON operations (not DB — that's in db.py).

#### Telegram API Layer

All Telegram API calls are wrapped in a `_post()` helper:

```python
def _post(method: str, **kwargs) -> dict:
    try:
        r = requests.post(f"{BASE}/{method}", json=kwargs, timeout=30)
        return r.json()
    except Exception as e:
        logger.error(f"TG [{method}] error: {e}")
        return {"ok": False}
```

This pattern:
- Centralizes error handling for all API calls
- Returns `{"ok": False}` on failure instead of raising (prevents crash propagation)
- Logs all failures with the method name for easy debugging

Specific wrappers built on `_post()`:

```python
def send_msg(chat_id, text, markup=None, parse_mode="HTML"):
    ...

def send_photo(chat_id, photo, caption="", markup=None, parse_mode="HTML"):
    ...

def answer_cb(cq_id, text="", alert=False):
    ...

def answer_precheckout(pq_id, ok=True, err=None):
    ...

def send_invoice(chat_id, title, description, payload, currency, prices):
    ...
```

#### Inline Keyboard Builder

```python
def ikb(*rows):
    return {
        "inline_keyboard": [
            [{"text": t, "callback_data": d} for t, d in row]
            for row in rows
        ]
    }
```

Usage:

```python
ikb(
    [("❤️ Like", "like:123"), ("💔 Pass", "pass:123")],
    [("🔙 Back", "menu:home")]
)
```

Each argument to `ikb()` is a row of `(label, callback_data)` tuples. Clean and readable.

#### Time Utilities

All timestamps are stored and compared in UTC:

```python
def utcnow() -> datetime:
    return datetime.now(timezone.utc)

def now_iso() -> str:
    return utcnow().isoformat()

def parse_iso(s: str) -> datetime:
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)
```

ISO format (`2026-03-22T10:30:00+00:00`) is used everywhere for human readability and Python's `datetime.fromisoformat()` compatibility.

#### Check Functions

These are the "guards" that run on every interaction:

```python
def check_premium(user):   # Expire premium if past date
def check_boost(user):     # Expire boost if past date
def check_boost_week(user):# Reset weekly boost count if 7 days elapsed
def check_limits(user):    # Reset daily likes/super-likes/undos if new day
def touch(user):           # Update last_seen to now

def run_checks(user):
    check_premium(user)
    check_boost(user)
    check_limits(user)
    touch(user)
```

`run_checks()` is called at the top of every handler. This means expiry logic runs inline — no background workers, no cron jobs.

#### Profile Utilities

```python
def card_text(user) -> str:
    # Formats the full profile card text
    # Used for both own profile view and browse cards

def completeness(user) -> int:
    # Returns 0-100 score

def completeness_bar(score) -> str:
    # Returns "████████░░ 80%"

def completeness_tip(user) -> str:
    # Returns the most impactful next action
```

#### Build Queue

The heart of the matching system:

```python
def build_queue(db, viewer_id) -> list[str]:
    viewer = get_user(db, viewer_id)
    excluded = (likes | super_likes | passes | matches | reports | blocked | self)

    for uid, u in db["users"].items():
        if uid in excluded: continue
        if is_banned: continue
        if 3+ reports: continue
        if viewer is blocked by u: continue
        if gender mismatch: continue
        score = compute_score(u)
        scored.append((score, uid))

    return [uid for _, uid in sorted(scored, reverse=True)]
```

#### Match Handler

```python
def do_match(db, a_id, b_id) -> bool:
    # Check not already matched
    # Bidirectional match record
    # Increment global match counter
    # Generate conversation starter
    # Send notifications to both (respecting preferences)
    # Save DB
    # Return True if new match
```

The function is idempotent — calling it twice for the same pair doesn't create duplicate matches.

#### Command Handlers

Each command is a standalone function:

```python
def cmd_start(cid, from_user, db): ...
def cmd_browse(cid, db): ...
def cmd_matches(cid, db): ...
def cmd_profile(cid, db): ...
def cmd_editprofile(cid, db): ...
def cmd_wholikedme(cid, db): ...
def cmd_boost(cid, db): ...
def cmd_undo(cid, db): ...
def cmd_premium(cid, db): ...
def cmd_notifications(cid, db): ...
def cmd_deleteprofile(cid, db): ...
def cmd_help(cid, db): ...
```

Each function follows the same pattern:
1. Get user from DB
2. Return early if no user (with helpful message)
3. Run expiry checks
4. Do the thing
5. Save updated user

#### Callback Handler

The callback handler is the largest function — it handles all button clicks:

```python
def on_callback(cq, db):
    answer_cb(cq_id)  # Always answer FIRST
    
    if data.startswith("gender:"): ...
    elif data.startswith("lf:"): ...
    elif data.startswith("setup_ok:"): ...
    elif data.startswith("menu:"): ...
    elif data.startswith("like:"): ...
    elif data.startswith("pass:"): ...
    elif data.startswith("superlike:"): ...
    elif data.startswith("report:"): ...
    elif data.startswith("rr:"): ...   # Report reason
    elif data.startswith("ef:"): ...   # Edit field
    elif data.startswith("elf:"): ...  # Edit looking for
    elif data.startswith("nt:"): ...   # Notification toggle
    elif data.startswith("boost:"): ...
    elif data.startswith("del:"): ...
    elif data.startswith("prem:"): ...
```

**Critical**: `answer_cb(cq_id)` is called immediately at the top — before any processing. Telegram shows a loading spinner on buttons until `answerCallbackQuery` is called. Answering first prevents UI lag.

#### Text Handler

Handles both commands and state machine text input:

```python
def on_text(cid, text, from_user, db):
    user = get_user(db, cid)
    state = user.get("state", "idle")
    
    if text.startswith("/"):
        # Route to command handlers
        ...
    elif state == "setup_name":
        # Handle name input
        ...
    elif state == "edit_bio":
        # Handle bio edit
        ...
    else:
        # Unexpected text
        show_buttons_hint(cid)
```

Commands always work regardless of state — they first reset state to `idle`, then execute. This ensures users can always escape a stuck flow.

---

### db.py

#### load_db()

```python
def load_db() -> dict:
    for fname in [DB_FILE, BACKUP_FILE]:
        if os.path.exists(fname):
            try:
                with open(fname, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    data.setdefault("users", {})
                    data.setdefault("reports", [])
                    data.setdefault("total_matches", 0)
                    data.setdefault("total_stars_earned", 0)
                    return data
            except Exception as e:
                logger.error(f"Failed to load {fname}: {e}")
    return fresh_db()
```

`setdefault()` calls ensure that if the DB was created with an older version of the code (missing new top-level keys), it still works correctly.

#### save_db()

```python
def save_db(db, retries=3) -> bool:
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
```

`ensure_ascii=False` — critical for non-Latin characters (Hindi, Arabic, Japanese usernames, emojis in bios).

`indent=2` — human-readable JSON. Slightly larger file, much easier to debug.

#### default_user()

```python
def default_user(user_id, username, now_iso) -> dict:
    return {
        "name": None,
        "age": None,
        # ... all fields with safe defaults
        "state": "setup_name",  # New users start onboarding
    }
```

The initial state is `setup_name` — new users go straight into onboarding.

---

### config.py

```python
import os

TELEGRAM_TOKEN           = os.environ.get("TELEGRAM_TOKEN", "")
ADMIN_CHAT_ID            = int(os.environ.get("ADMIN_CHAT_ID", "0"))
ADMIN_USERNAME           = os.environ.get("ADMIN_USERNAME", "admin")

DAILY_LIKE_LIMIT         = 20
DAILY_SUPERLIKE_LIMIT    = 1
DAILY_UNDO_LIMIT         = 1
BOOST_DURATION_MINUTES   = 30
PREMIUM_STARS_PRICE      = 50
PREMIUM_DURATION_DAYS    = 30
FREE_BOOSTS_PER_WEEK     = 1
PREMIUM_BOOSTS_PER_WEEK  = 3
```

All tunable constants in one place. Want to give free users 30 likes? Change one number.

---

## 🧠 Smart Matching Algorithm — Deep Dive

### The Problem

Dating app matching is fundamentally a **recommendation problem**: given a viewer and a pool of candidates, rank candidates by likelihood of mutual interest.

SparkBot's approach is **heuristic scoring** — we don't have enough data for ML, but we can make educated guesses based on observable signals.

### Signal Analysis

#### Premium + Boosted (1000 pts)

These users have spent real money AND activated a boost. They are:
- Highly motivated to match
- Likely to respond quickly
- Contributing to the platform's sustainability

Showing them first rewards their investment and creates a positive ROI loop.

#### Common Interests (20 pts per overlap)

Research on dating app success rates consistently shows that **shared interests are the strongest predictor of conversation quality** and continued engagement.

```python
u_ints = set(u["interests"])
v_ints = set(viewer["interests"])
score += len(u_ints & v_ints) * 20
```

Set intersection is O(min(|A|, |B|)) — fast even for many users.

#### Same City (100 pts)

Distance is the biggest friction point in online dating. Local profiles are more likely to lead to actual dates. The bonus is significant but not overwhelming — a premium boosted profile in another city still ranks above a local free profile.

#### Recently Active (80 pts)

Active users respond. Showing inactive profiles wastes the viewer's likes and kills their experience. "Active today" gets the full bonus; older than 24h gets nothing.

#### New Profile (50 pts)

New user excitement peaks in week 1. Getting them early matches keeps them on the platform. The 50-point bonus ensures new profiles get visibility even if they're incomplete.

#### Profile Completeness (0–100 pts)

Incomplete profiles (missing photo, bio, interests) have lower conversion rates. Penalizing them in the queue incentivises completion and improves the overall ecosystem quality.

### Algorithm Limitations

SparkBot's algorithm is intentionally simple. Real dating apps use:
- Machine learning on swipe history
- Collaborative filtering ("users like you liked these profiles")
- Engagement rate signals (how often does this profile get liked vs passed)
- ELO-style rating systems

These require significant data and infrastructure. SparkBot's heuristic approach gets most of the value with none of the complexity.

---

## 🛡️ Safety System

SparkBot's safety features work in layers.

### Layer 1: Gender Preference Matching

Bidirectional preference filtering ensures users only see profiles that could theoretically be interested in them. This reduces wasted swipes and inappropriate encounters.

### Layer 2: User Reporting

Four-click reporting flow:
1. Tap Report button
2. Select reason
3. System records report
4. User auto-blocked from reporter

Low friction encourages reporting. Report reasons provide data for admin review.

### Layer 3: Auto-Soft-Ban

3 reports from different users → profile hidden from browse.

This prevents bad actors from harassing the community without requiring admin review for every case. Admins can escalate to hard ban or exonerate.

### Layer 4: Manual Admin Ban

Admins can hard-ban any user. Banned users:
- See suspension message on next interaction
- Are hidden from all browse queues
- Cannot match with anyone

### Layer 5: User Blocking

Users can block anyone they've encountered. Blocked users are excluded from both users' queues permanently.

### Layer 6: Age Verification

Under-18 users are rejected during onboarding. While not cryptographically verified (Telegram bots can't verify real age), it:
- Sets a clear policy
- Creates a record of the user claiming to be 18+
- Provides legal protection for the platform

---

## 🎨 UX Design Principles

SparkBot follows 8 core UX rules.

### 1. Always Respond Within 1 Second

For callback queries, `answer_cb()` is called immediately before any processing. This removes the loading spinner on buttons instantly, even if the actual processing takes longer.

### 2. Never a Dead End

Every message includes at least one button to continue. No user should ever be stuck with no next action.

### 3. Always a Back Button

Every inline keyboard menu has `🔙 Back` where applicable. Users should always be able to retreat without sending a command.

### 4. Redirect Unexpected Input

When a user sends text during a button-expected state:
```
😊 Please use the buttons!
```

When a user sends a photo during a text-expected state:
```
📸 Please send a photo, not text! 😊
```

Never ignore unexpected input. Always acknowledge and redirect.

### 5. Consistent Emoji Vocabulary

| Emoji | Meaning |
|-------|---------|
| 💫 | Profile name |
| 📍 | Location |
| 🎯 | Preference |
| 📝 | Bio |
| ✨ | Interests / Premium |
| ❤️ | Like |
| 💔 | Pass |
| ⭐ | Super like / Premium |
| 📛 | Report |
| 🚀 | Boost |
| 🎉 | Match celebration |
| 🔙 | Back navigation |

### 6. Excited Match Notifications

Match notifications use energetic language and multiple celebration elements:
- 🎉 emoji
- **Bold formatting**
- Conversation starter
- CTA buttons

### 7. Friendly Error Messages

No Python tracebacks. No "An error occurred." Instead:
```
⚠️ Something went wrong! Please try again or use /start
```

All errors are logged internally, never shown to users.

### 8. Photo Always as Photo

Profile photos are always sent as `sendPhoto`, never as `sendDocument`. Caption always attached to the same message as the photo. Inline keyboard always attached to the same photo message.

This ensures the profile card looks like a proper card — photo + text + buttons as one unit.

---

## 🔧 Edge Cases Handled

SparkBot handles 11 specific edge cases that would break a naive implementation.

### 1. /start Mid-Flow

If a user sends `/start` while in the middle of onboarding or editing:
- `state` reset to `idle`
- `state_data` cleared
- Returning user flow triggered (show main menu)

No data corruption. Clean restart.

### 2. Old Inline Button Clicked

If a user clicks a button from a much older message (after state has changed):
- Callback is processed against current state
- If the callback data is no longer contextually valid, it's handled gracefully
- `answer_cb()` is always called immediately regardless

### 3. Simultaneous Mutual Like

If User A and User B like each other within milliseconds:

```python
# After recording the like, RELOAD fresh DB
fresh_db = database.load_db()
target = database.get_user(fresh_db, target_id)
if str(viewer_id) in (target.get("likes", []) + ...):
    do_match(fresh_db, ...)
```

And in `do_match()`:

```python
if b_str in ua.get("matches", []):
    return False  # Already matched, skip
```

This double-check (fresh DB load + match existence check) prevents duplicate match notifications even in race conditions.

### 4. Deleted Profile During Browse

If User A is browsing and User B's profile gets deleted mid-session:

```python
target = db["users"].get(target_id)
if not target:
    # Profile was deleted, skip them
    user["passes"].append(target_id)
    database.set_user(db, cid, user)
    next_profile(cid, database.load_db())  # Show next
    return
```

The viewer never sees an error — they just smoothly move to the next profile.

### 5. Photo During Text State

```python
elif state == "setup_age":
    send_msg(cid, "📸 Please send a photo, not text! 😊")
```

Wait, the inverse — text during photo-expected state:

```python
elif state == "setup_photo":
    send_msg(cid, "📸 Please send a photo, not text! 😊")
```

And in `on_photo()`:

```python
else:  # Unexpected photo
    send_msg(cid, "😊 I wasn't expecting a photo right now. Use /browse or /help!")
```

### 6. Boost Expires Mid-Session

No special handling needed — `check_boost()` runs on every interaction. The user will see updated boost status on their next action.

### 7. Premium Expires Mid-Session

Same pattern — `check_premium()` runs on every interaction. User is silently downgraded on next action. No disruptive notification.

### 8. Admin Commands From Non-Admin

```python
if not is_admin(cid): return  # Silent ignore
```

Non-admin users get no response, no error, no indication the command exists.

### 9. User Blocks Someone They've Already Matched With

Blocking a match doesn't remove the existing match — it only prevents future visibility. The existing match record stays. This is by design — abrupt removal of existing connections would be jarring.

### 10. User Sends Message With No Profile

```python
user = database.get_user(db, cid)
if not user:
    send_msg(cid, "👋 Use /start to get started!")
    return
```

Every handler has this guard. New users are always redirected to `/start`.

### 11. DB File Missing on Startup

```python
for fname in [DB_FILE, BACKUP_FILE]:
    # Try to load...

# Both missing → fresh DB
return {"users": {}, "reports": [], ...}
```

Bot starts with a fresh database rather than crashing.

---

## 📋 Error Handling & Logging

### Logging Configuration

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("errors.log"),   # File
        logging.StreamHandler(),              # Console (Railway logs)
    ],
)
```

Both file and console — Railway's dashboard shows console logs live.

### Error Log Format

```
2026-03-22 10:30:15,423 [ERROR] TG [sendMessage] error: ConnectionError
2026-03-22 10:31:02,891 [ERROR] DB save attempt 1 failed: PermissionError
2026-03-22 10:31:03,203 [ERROR] Dispatch error on update 42891: KeyError 'photo'
```

Timestamp, level, and descriptive message. Enough to debug without being overwhelming.

### Dispatch-Level Try/Except

```python
def dispatch(update, db):
    try:
        # ... handle update
    except Exception as e:
        logger.error(f"Dispatch error on update {update.get('update_id')}: {e}", exc_info=True)
        try:
            send_msg(cid, "⚠️ Something went wrong! Please try again or use /start")
        except Exception:
            pass
```

`exc_info=True` — logs the full stack trace to the file. Invaluable for debugging rare errors.

The inner try/except on `send_msg` prevents an error in error handling from crashing the loop.

### DB Write Retry Logic

```python
for attempt in range(3):
    try:
        json.dump(db, f, ...)
        return True
    except Exception:
        time.sleep(0.3)
return False  # All retries failed
```

3 attempts with 0.3 second delays between. Handles transient filesystem errors without crashing.

---

## ⚡ Performance Considerations

### DB File Size

With 1,000 users, each user object averages ~800 bytes. That's:
- 1,000 users: ~800KB
- 5,000 users: ~4MB
- 10,000 users: ~8MB

JSON parsing time for 8MB: ~50ms on Railway's hardware. Still fast enough for a Telegram bot (users don't notice anything under 200ms).

Beyond ~10,000 users, consider:
1. Migrating to Supabase (free tier: 500MB)
2. Lazy-loading users (only load the user being processed, not all users)
3. Caching the queue in memory with a TTL

### Polling Interval

With `timeout=30` in getUpdates, the bot has at most 30 seconds of latency for the first message after going quiet. In practice, Telegram pushes updates instantly — the timeout is just the hold-open duration for empty responses.

### Message Send Latency

SparkBot makes 2–4 API calls per user interaction:
1. `answerCallbackQuery` (if callback)
2. `sendMessage` or `sendPhoto`
3. Sometimes a second `sendMessage` for notifications

At ~100–200ms per call, total latency per interaction: 200–800ms. Well within the 1-second UX target.

### Queue Build Time

`build_queue()` iterates all users. For 5,000 users:
- Python dict iteration: ~1ms
- String operations: ~5ms
- Set operations: ~2ms
- Total: ~10ms

Fast enough. If it ever becomes slow, add simple caching (cache the queue per user for 60 seconds).

---

## 🗺️ Roadmap

### v1.1 — Quality of Life

- [ ] `/settings` — Unified settings menu (currently scattered across commands)
- [ ] Photo verification prompts (send selfie with hand gesture)
- [ ] Distance-based filtering (requires city→coordinates lookup)
- [ ] Profile view counter ("👁️ 47 people viewed your profile this week")
- [ ] Match expiry (unmatched if no conversation started in 7 days)

### v1.2 — Discovery Improvements

- [ ] Interest hashtag search (`/browse #music`)
- [ ] Age range filter (`/browse 20-28`)
- [ ] "Near me" mode (basic region matching from city name)
- [ ] Profile sharing (share someone's profile card to a group)

### v1.3 — Monetization Expansion

- [ ] Gift Premium to someone else
- [ ] Super Boost (2 hours, 3x visibility, 5 Stars)
- [ ] Profile Spotlight (featured section, 10 Stars)
- [ ] `/roses` — Gift a Rose to someone (1 Star, shows in their notifications)

### v2.0 — Infrastructure Upgrade

- [ ] Migrate from db.json to Supabase
- [ ] Webhook mode (switch from polling)
- [ ] Redis caching for browse queues
- [ ] Analytics dashboard (daily active users, match rate, conversion)
- [ ] A/B testing framework for algorithm variations

### v2.1 — Social Features

- [ ] Voice notes (record a 30-second intro)
- [ ] Video profiles (15-second clips)
- [ ] Group matching (bring your friend, find couples to double-date with)
- [ ] Community events ("SparkBot meetup in Mumbai — interested?")

---

## ❓ FAQ

### Why is the database a JSON file? Isn't that bad practice?

For a project at this scale, it's the right tradeoff. A single JSON file means:
- Zero infrastructure to set up
- Zero ongoing database costs
- Deployable in 5 minutes
- Debuggable by opening a file

The codebase is structured to make migrating to a real database easy — all DB operations go through `db.py`. Changing from JSON to PostgreSQL means rewriting only that one file.

### Can the bot handle multiple users simultaneously?

Yes — Python's GIL doesn't matter here because the bottleneck is network I/O (waiting for Telegram API responses), not CPU computation. The long polling loop processes one update at a time, but updates arrive at most every few hundred milliseconds, so in practice there's no meaningful queue.

If you need true parallelism (hundreds of concurrent active users), switch to an async approach with `asyncio` + `aiohttp` + `python-telegram-bot` v20+.

### Why not use python-telegram-bot?

Three reasons:
1. **Learning value** — Understanding raw API calls makes you a better developer
2. **No magic** — Every line of code does exactly what it says
3. **Dependency minimalism** — `requests` is 9KB; `python-telegram-bot` is 30MB+

For production bots with 10k+ users, `python-telegram-bot` or `aiogram` add significant value. For this scale, pure `requests` is perfect.

### What happens if Railway redeploys and db.json is lost?

Two solutions:
1. **Railway Volume** (recommended) — Mount a persistent volume at `/app`. Files survive redeploys.
2. **External database** — Migrate to Supabase. Never lose data regardless of deploy events.

Without one of these, each redeploy starts with an empty user list. Always set up persistence before going live.

### Can I use this bot commercially?

Yes. SparkBot is MIT licensed — use it however you want, commercially or otherwise. Attribution appreciated but not required.

### How do I handle GDPR / data privacy?

SparkBot stores only what users voluntarily provide. For GDPR compliance:
- Add a privacy policy URL to your BotFather description
- Implement data export (`/mydata` command returning the user's JSON blob)
- The existing `/deleteprofile` command already handles right-to-erasure

### Can I run multiple instances?

Not recommended with the JSON file backend — concurrent writes would corrupt data. If you need horizontal scaling, migrate to PostgreSQL + a proper connection pool first.

### How do I backup the database?

`db_backup.json` is automatically maintained. For external backups:

```bash
# Add this to a Railway cron job or set up GitHub Actions
cp db.json "db_backup_$(date +%Y%m%d).json"
```

Or use Railway's volume snapshot feature.

---

## 🤝 Contributing

Contributions are welcome! Here's how to get involved.

### Ways to Contribute

- **Bug reports** — Open an issue with steps to reproduce
- **Feature requests** — Open an issue with the use case
- **Code contributions** — Fork, branch, PR
- **Documentation** — Fix typos, add examples, improve clarity
- **Testing** — Test with real users and report UX issues

### Development Setup

```bash
git clone https://github.com/REALNYXAETHER/Sparkbot.git
cd Sparkbot
pip install requests
export TELEGRAM_TOKEN="your_test_bot_token"
export ADMIN_CHAT_ID="your_id"
python bot.py
```

Use a separate test bot (create one with @BotFather) for development.

### Code Style

- **PEP 8** compliance
- **Type hints** where they add clarity (return types, params)
- **Docstrings** for all public functions
- **No external dependencies** beyond `requests`
- **Comments** for non-obvious logic

### Pull Request Process

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test thoroughly with a real Telegram bot
5. Commit with a descriptive message: `git commit -m "feat: add distance filtering"`
6. Push: `git push origin feature/your-feature-name`
7. Open a PR with description of changes and testing done

### Commit Message Convention

```
feat:  New feature
fix:   Bug fix
docs:  Documentation only
style: Formatting, no logic change
refactor: Code restructure, no feature change
perf:  Performance improvement
test:  Adding tests
```

---

## 📁 Project Structure — Annotated

```
sparkbot/
│
├── bot.py                    ← The entire bot (1500+ lines)
│   ├── Imports & logging setup
│   ├── Telegram API layer (send_msg, send_photo, etc.)
│   ├── ikb() — inline keyboard builder
│   ├── Time utilities (utcnow, parse_iso)
│   ├── Check functions (premium, boost, limits)
│   ├── Profile utilities (card_text, completeness)
│   ├── Browse queue builder
│   ├── Match handler + notifications
│   ├── Conversation starters (15 interest-based + 20 generic)
│   ├── Onboarding prompts (ask_name, ask_age, etc.)
│   ├── Menu displays (show_main_menu, show_edit_menu, etc.)
│   ├── next_profile() — core browse loop
│   ├── Command handlers (cmd_start, cmd_browse, etc.)
│   ├── Admin handlers
│   ├── Callback handler (on_callback)
│   ├── Text handler + state machine (on_text)
│   ├── Photo handler (on_photo)
│   ├── Payment handlers (on_pre_checkout, on_payment)
│   ├── Dispatcher (dispatch)
│   └── Main polling loop (main)
│
├── db.py                     ← 80 lines, all DB operations
│   ├── load_db()             ← with fallback chain
│   ├── save_db()             ← with retry + backup
│   ├── get_user()            ← dict lookup by ID
│   ├── set_user()            ← write + save
│   └── default_user()        ← new user template
│
├── config.py                 ← 15 lines, all constants
│
├── requirements.txt          ← 1 line: requests
│
├── Dockerfile                ← 6 lines, python:3.11-slim
│
├── db.json                   ← Auto-created on first run
├── db_backup.json            ← Auto-maintained
└── errors.log                ← Auto-created
```

---

## 🔐 Security Considerations

### Admin Authentication

Admin access is controlled by `ADMIN_CHAT_ID` — your Telegram user ID. This is:
- **Stored as an environment variable**, not in code
- **Compared numerically** on every admin command
- **Silently ignored** for non-admins (no error response)

An attacker cannot gain admin access by guessing your ID (Telegram IDs are not guessable). Your account's security is your Telegram account's security.

### Token Security

The `TELEGRAM_TOKEN` must never be committed to GitHub. It's loaded from environment variables:

```python
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
```

If you accidentally commit your token:
1. Go to @BotFather immediately
2. `/mybots` → Select bot → `API Token` → `Revoke current token`
3. Get new token
4. Update Railway environment variables

### User Data

SparkBot stores only what users voluntarily provide. No location tracking, no message content (beyond profile fields), no device information. The only identifier is the Telegram user ID, which is public within Telegram.

Photo `file_id` values are Telegram-internal identifiers. They can only be used to send the photo through the same bot — they're not public URLs.

---

## 📊 Metrics to Track

If you run SparkBot seriously, track these KPIs:

| Metric | Formula | Target |
|--------|---------|--------|
| DAU (Daily Active Users) | users with last_seen < 24h | > 10% of total |
| Match Rate | total_matches / total_likes | > 5% |
| Profile Completion | avg completeness score | > 70% |
| Premium Conversion | premium_users / total_users | > 3% |
| Retention D7 | users active on day 7 / registered day 0 | > 20% |
| Report Rate | reports / total_swipes | < 0.5% |

Query these from db.json with a simple Python script on your admin account.

---

## 🙏 Acknowledgements

Built with:
- **Python 3.11** — For being an excellent language
- **Telegram Bot API** — For making bot development accessible
- **Railway** — For painless deployment
- **requests** — For being the perfect HTTP library

Inspired by:
- Tinder's UX and feature set
- Bumble's safety-first approach
- Hinge's conversation starter idea

---

## 📜 License

```
MIT License

Copyright (c) 2026 REALNYXAETHER

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

Built with 💘 by **REALNYXAETHER**

*If this project helped you — drop a ⭐ on the repo. It means a lot.*

---

**SparkBot** — Because everyone deserves to find their spark. 🔥

</div>

---

## 🔄 Updating SparkBot

### Pushing Updates via Termux

When you make changes to any file, push them to GitHub and Railway auto-deploys:

```bash
cd '/storage/emulated/0/Dating Bot'
git add .
git commit -m "fix: handle edge case in browse queue"
git push origin main
```

Railway detects the push, rebuilds the Docker image, and redeploys. Takes ~60 seconds. Zero downtime if you use Railway's rolling deploy.

### Version Control Best Practices

```bash
# Check what changed before committing
git diff

# Check what files are staged
git status

# View commit history
git log --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Pull latest from GitHub
git pull origin main
```

### Making a Hotfix

If something breaks in production:

```bash
# Fix the bug in bot.py
nano bot.py  # or edit in your preferred editor

# Stage and commit
git add bot.py
git commit -m "hotfix: fix crash on empty interests list"
git push origin main
```

Railway auto-redeploys. Bug fixed in under 2 minutes.

---

## 🐛 Debugging Common Issues

### Bot Not Responding

**Symptoms**: Messages sent, no reply.

**Checklist**:
1. Is the bot running? Check Railway logs for `🚀 SparkBot starting...`
2. Is `TELEGRAM_TOKEN` correct? Test: `curl https://api.telegram.org/bot<TOKEN>/getMe`
3. Did you accidentally start a second instance? Two instances with the same token fight over updates.
4. Is the bot banned? Try messaging a different user account.

```bash
# Test your token manually
curl https://api.telegram.org/bot7123456789:AAExx.../getMe
```

Expected response:
```json
{"ok":true,"result":{"id":7123456789,"is_bot":true,"first_name":"SparkBot",...}}
```

### Profile Photos Not Showing

**Symptoms**: Profile card shows text only, no photo.

**Cause**: `photo_file_id` stored but photo no longer accessible.

**Why**: Telegram `file_id` values can expire or become invalid if the bot is deleted and recreated. Always use the same bot token — never revoke and regenerate unless compromised.

**Fix**: Ask affected users to re-upload their photo via `/editprofile → Edit Photo`.

### Payments Not Working

**Symptoms**: Premium button shows invoice, but payment doesn't complete.

**Checklist**:
1. Is your bot approved for Stars payments? Check BotFather → `/mybots` → Payments
2. Did you answer `pre_checkout_query` within 10 seconds? Check logs for the answer.
3. Are you testing with the same account that owns the bot? (Self-payments may not work in test mode)
4. Is `provider_token` correctly set to `""` (empty string) for Stars?

### Database Corruption

**Symptoms**: Bot starts, immediately crashes with `JSONDecodeError`.

**Fix**:
```bash
# On Railway: use the Railway CLI or connect to the volume
# Locally:
python3 -c "
import json
try:
    with open('db.json') as f:
        json.load(f)
    print('db.json: OK')
except Exception as e:
    print(f'db.json corrupt: {e}')

try:
    with open('db_backup.json') as f:
        json.load(f)
    print('db_backup.json: OK')
except Exception as e:
    print(f'db_backup.json corrupt: {e}')
"

# If db.json is corrupt but backup is OK:
cp db_backup.json db.json
```

### Memory Usage Growing

**Symptoms**: Railway shows increasing memory usage over time.

**Cause**: `db.json` loaded on every update grows linearly with users.

**Fix at ~5,000 users**: Cache the DB in memory, refresh every 30 seconds:

```python
_db_cache = None
_db_cache_time = 0

def load_db():
    global _db_cache, _db_cache_time
    if time.time() - _db_cache_time < 30:
        return _db_cache
    _db_cache = _load_from_disk()
    _db_cache_time = time.time()
    return _db_cache
```

Or migrate to Supabase.

### Users Stuck in Wrong State

**Symptoms**: User sends `/start`, bot says "Please enter your name:" even though they have a profile.

**Cause**: State machine got into an invalid state (usually from an old bug or manual DB edit).

**Fix**: Admin can manually reset via editing `db.json`:

```python
# Quick fix script
import json
target_id = "123456789"

with open("db.json") as f:
    db = json.load(f)

db["users"][target_id]["state"] = "idle"
db["users"][target_id]["state_data"] = {}

with open("db.json", "w") as f:
    json.dump(db, f, indent=2)

print("Fixed!")
```

Or tell the user to send `/start` — this resets state regardless.

---

## 🧪 Testing Your Bot

### Manual Test Checklist

Before going live, run through this complete test sequence with two test Telegram accounts.

#### Account Setup Tests

- [ ] `/start` on a fresh account → Onboarding begins
- [ ] Enter name → Age prompt appears
- [ ] Enter age < 18 → Rejected with message
- [ ] Enter valid age → Gender prompt appears
- [ ] Click gender button → Looking For prompt appears
- [ ] Click looking for → City prompt appears
- [ ] Enter city → Bio prompt appears
- [ ] Enter bio > 300 chars → Rejected with character count
- [ ] Enter valid bio → Interests prompt appears
- [ ] Enter interests (comma-separated) → Photo prompt appears
- [ ] Send text instead of photo → Friendly redirect
- [ ] Send photo → Profile preview appears
- [ ] Click "Edit" on preview → Edit menu appears
- [ ] Click "Yes" on preview → Main menu appears

#### Browse & Match Tests

- [ ] `/browse` → Profile card appears with 4 buttons
- [ ] Click Like → Next profile appears, like count decremented
- [ ] Click Pass → Next profile appears
- [ ] Click Super Like → Notification sent to target, next profile appears
- [ ] Click Report → Reason menu appears
- [ ] Click Report reason → Report recorded, next profile shown
- [ ] Like each other (two accounts) → Match notification sent to both
- [ ] Match notification includes conversation starter
- [ ] Browse to end → "No more profiles" message

#### Daily Limit Tests

- [ ] Like 20 profiles → Limit hit message appears
- [ ] Next day → Like count reset (change system date for testing)

#### Profile Management Tests

- [ ] `/profile` → Own card shown with completeness bar
- [ ] `/editprofile` → Edit menu appears
- [ ] Edit name → Name updated, confirmation shown
- [ ] Edit photo → New photo saved
- [ ] `/deleteprofile` → Confirmation prompt
- [ ] Cancel delete → Account preserved
- [ ] Confirm delete → Account deleted, data cleaned from other users

#### Premium Tests

- [ ] `/premium` → Benefits and price shown
- [ ] `/wholikedme` without premium → Upgrade prompt
- [ ] Purchase (use 1 Star for testing) → Premium activated
- [ ] `/wholikedme` with premium → Likers shown
- [ ] Premium badge visible on profile card

#### Admin Tests

- [ ] `/admin_stats` from admin account → Stats shown
- [ ] `/admin_stats` from non-admin → Silent ignore
- [ ] `/admin_ban [id]` → User banned, notification sent
- [ ] Banned user sends message → Suspension message shown
- [ ] `/admin_unban [id]` → User unbanned
- [ ] `/admin_reports` → Reports listed
- [ ] `/admin_broadcast hello` → Message sent to all users
- [ ] `/admin_user [id]` → Full profile shown

#### Notification Tests

- [ ] `/notifications` → Toggle menu shown
- [ ] Toggle match notifications OFF → Tapping again turns ON
- [ ] Match while notifications OFF → No notification received

#### Edge Case Tests

- [ ] Send `/start` mid-onboarding → Resets, shows menu
- [ ] Click old inline button → Handled gracefully
- [ ] Send photo during text-expected state → Redirect message
- [ ] Send text during button-expected state → "Use the buttons!" message
- [ ] `/undo` with no passes → "Nothing to undo" message

---

## 📱 Running on Android Full-Time

Since you're building on Android with Termux, here's how to keep the bot running even when Termux is in the background.

### Keeping Termux Alive

**Disable battery optimization for Termux**:
- Settings → Apps → Termux → Battery → "Don't optimize"

**Acquire a wake lock** (prevents CPU sleep):
```bash
termux-wake-lock
```

Run this before starting the bot.

### Run Bot in Background with nohup

```bash
nohup python bot.py > bot.log 2>&1 &
echo "Bot PID: $!"
```

- `nohup` — keeps process running after terminal closes
- `> bot.log 2>&1` — redirect all output to log file
- `&` — run in background
- Print the PID so you can kill it later

### View Live Logs

```bash
tail -f bot.log
```

### Stop the Bot

```bash
# Find the process
ps aux | grep bot.py

# Kill it
kill <PID>
```

### Restart Automatically After Crash

```bash
# Simple crash loop in bash
while true; do
    python bot.py
    echo "Bot crashed. Restarting in 5 seconds..."
    sleep 5
done
```

Save as `run.sh`, run with `bash run.sh &`.

**Note**: This is fine for development but use Railway for production — it handles restarts, uptime, and logging professionally.

---

## 🌐 Webhook Mode (Advanced)

SparkBot uses long polling by default. For production at scale, webhooks are more efficient.

### Why Webhooks?

| | Long Polling | Webhooks |
|-|-------------|----------|
| Setup complexity | Simple | Medium |
| Latency | 0–100ms | 0–50ms |
| Server load | Higher | Lower |
| Infrastructure needed | Just outbound HTTPS | Inbound HTTPS URL |
| Works on Railway | ✅ | ✅ (with web server) |

### Setting Up Webhooks

You'll need a web framework — add `flask` to requirements.txt:

```python
# webhook_bot.py — replace polling with Flask webhook handler
from flask import Flask, request
import json

app = Flask(__name__)

@app.route(f"/webhook/{config.TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = request.json
    db = database.load_db()
    dispatch(update, db)
    return "OK", 200

# Set the webhook URL with Telegram
def set_webhook(url):
    _post("setWebhook", url=url)

if __name__ == "__main__":
    railway_url = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
    if railway_url:
        set_webhook(f"https://{railway_url}/webhook/{config.TELEGRAM_TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
```

Railway automatically provides an HTTPS URL via `RAILWAY_PUBLIC_DOMAIN`.

For now, stick with polling — it's simpler and works perfectly at SparkBot's scale.

---

## 💡 Extending SparkBot

### Adding a New Command

1. Write the handler function in `bot.py`:

```python
def cmd_myfeature(cid: int, db: dict) -> None:
    user = database.get_user(db, cid)
    if not user: return
    run_checks(user)
    
    # Your logic here
    send_msg(cid, "✨ My feature works!")
    
    database.set_user(db, cid, user)
```

2. Add it to the command routing in `on_text()`:

```python
routes = {
    # ... existing commands
    "/myfeature": cmd_myfeature,
}
```

3. Add to BotFather `/setcommands`:

```
myfeature - Description of my feature
```

Done. The new command is live on next deploy.

### Adding a New Inline Button

1. Choose a callback data prefix (e.g., `mf:`)
2. Create the button somewhere:

```python
markup = ikb([("✨ My Feature", "mf:action")])
send_msg(cid, "What would you like?", markup=markup)
```

3. Handle it in `on_callback()`:

```python
elif data.startswith("mf:"):
    action = data.split(":", 1)[1]
    # Handle the action
```

### Adding a New Profile Field

1. Add to `default_user()` in `db.py`:

```python
"height": None,
```

2. Add to onboarding flow in `bot.py` — add a new step between existing steps:

```python
# After interests
def ask_height(cid):
    send_msg(cid, "📏 How tall are you? (cm, e.g. 175)")

# In state machine
elif state == "setup_height":
    try:
        height = int(text.strip())
        assert 140 <= height <= 220
    except (ValueError, AssertionError):
        send_msg(cid, "❗ Please enter a valid height (140–220 cm)"); return
    user["state_data"]["height"] = height
    user["state"] = "setup_photo"  # or next state
    database.set_user(db, cid, user)
    ask_photo(cid)
```

3. Add to `card_text()`:

```python
height = user.get("height")
height_line = f"📏 {height}cm\n" if height else ""
```

4. Add edit option to edit menu and handle `edit_height` state.

### Adding a New Matching Signal

In `build_queue()`, add your signal to the scoring logic:

```python
# Example: bonus for users with high profile completeness
comp_score = completeness(u)
if comp_score == 100:
    s += 30  # Full profile bonus
```

Or:

```python
# Example: bonus for users who are very active (liked 50+ people)
if len(u.get("likes", [])) > 50:
    s += 25  # High engagement bonus
```

The scoring is additive — any number of signals can be combined.

---

## 📚 Telegram Bot API Reference

Key API methods used by SparkBot and their parameters.

### sendMessage

```python
{
    "chat_id": 123456789,           # Target chat ID
    "text": "Hello!",               # Message text (HTML/Markdown)
    "parse_mode": "HTML",           # HTML or MarkdownV2
    "reply_markup": {               # Optional inline keyboard
        "inline_keyboard": [[...]]
    }
}
```

HTML formatting supported:
- `<b>bold</b>`
- `<i>italic</i>`
- `<code>monospace</code>`
- `<a href="url">link</a>`

### sendPhoto

```python
{
    "chat_id": 123456789,
    "photo": "AgACAgI...",           # file_id or URL
    "caption": "Photo caption",      # Optional, max 1024 chars
    "parse_mode": "HTML",
    "reply_markup": {...}            # Buttons attached to photo
}
```

Caption + inline keyboard both attach to the photo message — this is the profile card pattern.

### answerCallbackQuery

```python
{
    "callback_query_id": "abc123",   # From callback_query.id
    "text": "Optional popup text",   # Shows as toast notification
    "show_alert": False              # True = popup dialog instead of toast
}
```

Must be called within 10 seconds of receiving the callback_query. Always call immediately.

### answerPreCheckoutQuery

```python
{
    "pre_checkout_query_id": "xyz",
    "ok": True,                      # True = approve payment
    "error_message": None            # Required if ok=False
}
```

Must be called within 10 seconds. Approving allows Telegram to process the payment.

### sendInvoice

```python
{
    "chat_id": 123456789,
    "title": "Premium Subscription",
    "description": "Unlock all features",
    "payload": "premium_monthly",    # Your internal identifier
    "provider_token": "",            # Empty for Stars (XTR)
    "currency": "XTR",               # Telegram Stars
    "prices": [
        {"label": "1 Month", "amount": 50}  # In Stars
    ]
}
```

### getUpdates (Long Polling)

```python
params = {
    "offset": last_update_id + 1,   # Acknowledge processed updates
    "timeout": 30,                   # Hold connection for 30 seconds
    "allowed_updates": [             # Only receive these update types
        "message",
        "callback_query",
        "pre_checkout_query"
    ]
}
```

`offset` is critical — without it, Telegram resends all unacknowledged updates on every poll.

---

## 🗂️ Sample db.json — Two Users, One Match

For reference, here's what a real `db.json` looks like with two matched users:

```json
{
  "users": {
    "111111111": {
      "name": "Rohan",
      "age": 24,
      "gender": "Man",
      "looking_for": "Women",
      "city": "Delhi",
      "bio": "Engineer who makes terrible dad jokes 🔧😂",
      "interests": ["music", "coffee", "coding", "travel", "gaming"],
      "photo_file_id": "AgACAgIAAxkBAAIBkWZr...",
      "username": "rohan_codes",
      "likes": ["222222222"],
      "passes": ["333333333"],
      "matches": ["222222222"],
      "super_likes_sent": [],
      "super_likes_received": [],
      "who_liked_me": ["222222222"],
      "reports_received": [],
      "reports_made": [],
      "blocked": [],
      "is_banned": false,
      "is_premium": true,
      "premium_expires": "2026-04-22T08:00:00+00:00",
      "is_boosted": false,
      "boost_expires": null,
      "boosts_used_this_week": 1,
      "boost_week_reset": "2026-03-19T08:00:00+00:00",
      "likes_today": 3,
      "super_likes_today": 0,
      "undos_today": 0,
      "limits_reset_date": "2026-03-22",
      "last_swiped_user": "333333333",
      "last_seen": "2026-03-22T10:45:00+00:00",
      "joined": "2026-03-01T08:00:00+00:00",
      "notifications": {
        "matches": true,
        "super_likes": true,
        "broadcasts": true
      },
      "state": "idle",
      "state_data": {}
    },
    "222222222": {
      "name": "Priya",
      "age": 23,
      "gender": "Woman",
      "looking_for": "Men",
      "city": "Delhi",
      "bio": "Coffee addict ☕ | Book lover | Amateur chef",
      "interests": ["music", "travel", "books", "coffee", "hiking"],
      "photo_file_id": "AgACAgIAAxkBAAIBmWZs...",
      "username": "priya_reads",
      "likes": ["111111111"],
      "passes": [],
      "matches": ["111111111"],
      "super_likes_sent": [],
      "super_likes_received": [],
      "who_liked_me": ["111111111"],
      "reports_received": [],
      "reports_made": [],
      "blocked": [],
      "is_banned": false,
      "is_premium": false,
      "premium_expires": null,
      "is_boosted": false,
      "boost_expires": null,
      "boosts_used_this_week": 0,
      "boost_week_reset": null,
      "likes_today": 7,
      "super_likes_today": 0,
      "undos_today": 0,
      "limits_reset_date": "2026-03-22",
      "last_swiped_user": null,
      "last_seen": "2026-03-22T10:40:00+00:00",
      "joined": "2026-03-05T12:00:00+00:00",
      "notifications": {
        "matches": true,
        "super_likes": true,
        "broadcasts": false
      },
      "state": "browsing",
      "state_data": {}
    }
  },
  "reports": [],
  "total_matches": 1,
  "total_stars_earned": 50
}
```

### Reading This Example

- Rohan (111) and Priya (222) have **mutually liked** each other → appear in both `matches[]`
- Rohan is **Premium** (paid 50 Stars, expires April 22)
- Priya has **broadcasts turned OFF** — admin messages won't reach her
- Priya is currently in `"state": "browsing"` — she's actively swiping
- Rohan has used **1 boost this week**, Priya has used 0
- `total_matches: 1` — only one match has happened on this platform so far
- `total_stars_earned: 50` — Rohan's purchase

---

## 🎯 Monetization Strategy

SparkBot's Premium system at 50 Stars/month creates a recurring revenue model. Here's how to think about the economics.

### Unit Economics

| Metric | Value |
|--------|-------|
| Premium price | 50 Stars |
| Stars ≈ USD | ~$0.50–$1.00 |
| Monthly revenue per premium user | $0.50–$1.00 |
| 100 premium users | $50–$100/month |
| 1000 premium users | $500–$1000/month |

### Conversion Funnel

```
New users → Complete profile → Swipe → Hit free limit → See upgrade prompt → Purchase
    100%          60%           50%          30%              20%             5%
```

5% conversion is realistic for a well-built dating bot. With 1000 users:
- 600 complete profiles
- 300 active swipers
- 90 hit the free limit daily
- 18 see the upgrade prompt
- ~1 converts per day = ~30 Premium users/month

### Improving Conversion

1. **Hit the limit at the right moment** — Currently shows "upgrade" when likes run out. Good.
2. **Show value clearly** — The `/premium` page lists every benefit explicitly.
3. **Time-limited offers** — "50% off first month" (reduce Stars price temporarily)
4. **Feature gating** — `/wholikedme` is Premium-only. If users see there are pending likes, they'll convert.
5. **Social proof** — "Join 47 Premium members" — add this to the Premium prompt.

### Additional Revenue Streams

Beyond subscriptions, Telegram Stars enable one-time purchases:

- **Super Boost** (2 hours, 3x visibility): 5 Stars
- **Profile Spotlight** (featured at top for 24h): 10 Stars
- **Roses** (send to someone you like, counts as super like): 1 Star
- **Extra Super Likes pack** (5 additional today): 3 Stars

These "consumables" can generate more revenue than subscriptions from highly engaged free users.

---

## 🌍 Localization

SparkBot is currently English-only, but built to be localizable.

### Adding Hindi Support

```python
# strings.py — add this file
STRINGS = {
    "en": {
        "welcome": "💘 Welcome to SparkBot!\n\nFind your spark — one swipe at a time. 🔥",
        "ask_name": "👋 Let's set up your profile!\n\n**What's your name?**",
        # ... all strings
    },
    "hi": {
        "welcome": "💘 SparkBot में आपका स्वागत है!\n\nएक स्वाइप में अपनी मुलाकात ढूंढें! 🔥",
        "ask_name": "👋 चलिए आपकी प्रोफ़ाइल बनाते हैं!\n\n**आपका नाम क्या है?**",
        # ... Hindi strings
    }
}

def t(user, key):
    lang = user.get("language", "en")
    return STRINGS.get(lang, STRINGS["en"]).get(key, STRINGS["en"][key])
```

Store user language in the user object, detect from Telegram's `from.language_code`.

---

## 📈 Growing Your User Base

Once SparkBot is live and working, here's how to get users.

### Organic Growth

1. **Telegram groups** — Share in local city groups, college groups, interest communities
2. **BotList directories** — Submit to `telegram.me/bots`, `storebot.me`, `botsarchive.com`
3. **Word of mouth** — The match notification includes usernames. When two people match, they naturally mention the bot.
4. **Referral program** — Give a free boost to users who refer someone who signs up (track via `/start?ref=userid`)

### Referral System Implementation

```python
# Handle /start with referral
def cmd_start(cid, from_user, db):
    # Check if referral payload in deep link
    # Telegram sends /start payload as message text: "/start ref_123456"
    if text.startswith("/start "):
        ref_id = text.split(" ", 1)[1]
        if ref_id.startswith("ref_"):
            referrer_id = ref_id.replace("ref_", "")
            referrer = database.get_user(db, referrer_id)
            if referrer:
                # Give referrer a free boost
                referrer["boosts_used_this_week"] = max(0, referrer.get("boosts_used_this_week", 1) - 1)
                database.set_user(db, referrer_id, referrer)
                send_msg(int(referrer_id), "🎁 Someone joined using your referral! You got a free boost!")
```

Generate referral links:
```
https://t.me/YourBotUsername?start=ref_123456789
```

### Retention Strategies

1. **Daily reminder** (respect notifications) — "👋 You have 20 new likes waiting. Start swiping! /browse"
2. **Reactivation** — Users inactive for 3+ days get a "We miss you!" nudge
3. **Match milestone** — "🎉 You're close to your first match! 3 people have liked you."
4. **Content** — Send weekly tips: "💡 Profiles with 5+ interests get 3x more matches!"

---

## 🔍 Analytics Queries

Quick Python scripts to run analytics on your `db.json`.

### User Funnel

```python
import json
from datetime import datetime, timezone, timedelta

with open("db.json") as f:
    db = json.load(f)

users = list(db["users"].values())
now = datetime.now(timezone.utc)

total = len(users)
has_photo = sum(1 for u in users if u.get("photo_file_id"))
has_bio = sum(1 for u in users if u.get("bio"))
has_interests = sum(1 for u in users if len(u.get("interests", [])) >= 3)
complete = sum(1 for u in users if u.get("photo_file_id") and u.get("bio") and len(u.get("interests", [])) >= 5 and u.get("city"))

print(f"Total users:         {total}")
print(f"Have photo:          {has_photo} ({has_photo/total*100:.1f}%)")
print(f"Have bio:            {has_bio} ({has_bio/total*100:.1f}%)")
print(f"Have 3+ interests:   {has_interests} ({has_interests/total*100:.1f}%)")
print(f"Fully complete:      {complete} ({complete/total*100:.1f}%)")
```

### Activity Breakdown

```python
day_ago = now - timedelta(days=1)
week_ago = now - timedelta(days=7)
month_ago = now - timedelta(days=30)

def parse(s):
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc) if s else None

dau = sum(1 for u in users if parse(u.get("last_seen")) and parse(u.get("last_seen")) > day_ago)
wau = sum(1 for u in users if parse(u.get("last_seen")) and parse(u.get("last_seen")) > week_ago)
mau = sum(1 for u in users if parse(u.get("last_seen")) and parse(u.get("last_seen")) > month_ago)

print(f"DAU (24h):  {dau} ({dau/total*100:.1f}%)")
print(f"WAU (7d):   {wau} ({wau/total*100:.1f}%)")
print(f"MAU (30d):  {mau} ({mau/total*100:.1f}%)")
```

### Match Rate

```python
total_likes = sum(len(u.get("likes", [])) for u in users)
total_matches = db.get("total_matches", 0)

if total_likes > 0:
    match_rate = (total_matches * 2) / total_likes * 100  # *2 because each match uses 2 likes
    print(f"Match rate: {match_rate:.1f}% of likes result in a match")
```

### Top Cities

```python
from collections import Counter

cities = Counter(u.get("city", "Unknown").strip().title() for u in users if u.get("city"))
print("\nTop 10 cities:")
for city, count in cities.most_common(10):
    print(f"  {city}: {count}")
```

### Interest Popularity

```python
all_interests = []
for u in users:
    all_interests.extend(i.lower() for i in u.get("interests", []))

interest_counts = Counter(all_interests)
print("\nTop 15 interests:")
for interest, count in interest_counts.most_common(15):
    print(f"  {interest}: {count}")
```

---

## 🧩 Architecture Decisions — Why Not X?

### Why Not aiogram / python-telegram-bot?

These are excellent frameworks. SparkBot doesn't use them because:

- **python-telegram-bot** adds 30MB+ of dependencies. For a bot this size, it's overkill.
- **aiogram** requires async Python. Async adds complexity (event loops, await/async everywhere) that isn't justified by SparkBot's concurrency requirements.
- **Pure requests** means: one file, one clear execution path, zero magic.

If SparkBot grows to 50k+ users with complex real-time features, `aiogram` becomes the right choice.

### Why Not SQLite Instead of JSON?

SQLite is a great middle ground between JSON and PostgreSQL. SparkBot uses JSON because:

- **json** is in the standard library. SQLite requires `sqlite3` (also stdlib, but more setup).
- JSON is **human-readable** directly. You can `cat db.json` and understand it.
- For the query patterns SparkBot needs (look up one user, iterate all users for queue), JSON is fast enough.

SQLite would be better for: complex queries, concurrent writes, large datasets. Add it when you need it.

### Why Not a Web Dashboard Instead of Admin Commands?

Telegram admin commands are:
- **Always available** — works anywhere you have Telegram
- **No server** — no web framework needed
- **Secure** — protected by Telegram's own auth

A web dashboard would need: a web server, authentication system, frontend, session management. That's 5x more code for a marginal UX improvement.

### Why Not Async?

Async Python with `asyncio` would allow SparkBot to handle many requests simultaneously without waiting. For SparkBot:

- Long polling means one request arrives and is processed at a time
- Even with 1000 users, updates arrive sequentially
- The bottleneck is Telegram API response time, not Python code speed
- Async adds significant complexity (every function needs `async def`, every call needs `await`)

Async becomes necessary when: using webhooks with high traffic, building real-time features like typing indicators, or handling 10k+ concurrent active users.

---

## 🏆 Production Checklist

Before launching SparkBot to real users:

### Security
- [ ] `TELEGRAM_TOKEN` in environment variable, NOT in code
- [ ] `ADMIN_CHAT_ID` in environment variable
- [ ] GitHub repo set to **Private**
- [ ] No sensitive data in commit history (`git log --all`)

### Infrastructure
- [ ] Railway Volume mounted for `db.json` persistence
- [ ] Bot token tested and working
- [ ] Admin commands tested from your account
- [ ] At least 2 test users have completed full onboarding

### UX
- [ ] BotFather commands set (`/setcommands`)
- [ ] Bot description set (`/setdescription`)
- [ ] Bot about text set (`/setabouttext`)
- [ ] Bot profile photo set

### Payments (if enabling Premium)
- [ ] Stars payments enabled in BotFather
- [ ] Test invoice sent and completed
- [ ] `successful_payment` handler confirmed working
- [ ] Premium benefits confirmed accessible after purchase

### Monitoring
- [ ] Railway logs accessible and readable
- [ ] `errors.log` being written (check after a few interactions)
- [ ] Admin stats command returning accurate data

### Legal (if going public)
- [ ] Privacy policy created and linked in bot description
- [ ] Terms of service created
- [ ] Age verification acknowledged in privacy policy
- [ ] Data deletion (`/deleteprofile`) tested and confirmed

---

*You're ready. Ship it. 🚀*

---

<div align="center">

**SparkBot** is open source. Star it, fork it, build on it.

Made with 💘 and way too much caffeine.

*Questions? Issues? Open a GitHub issue or find @REALNYXAETHER on Telegram.*

</div>

---

## 🔮 Future Vision — SparkBot 3.0

Where SparkBot could go in 2–3 years with serious development.

### AI-Powered Features

- **Compatibility Score**: Run a small ML model on shared interests, city, age gap, and message patterns to predict match quality. Show "92% compatible ✨" on profile cards.
- **Auto-generated bios**: "You seem like you love music, travel, and coffee — here's a bio draft for you!"
- **Smart conversation prompts**: Instead of generic starters, analyze both profiles and generate hyper-personalised openers.
- **Photo quality detection**: Reject selfies taken in bad lighting, suggest retaking.
- **Fake profile detection**: Flag accounts with stock photos using reverse image search.

### Video Features

- **Video profiles**: 15-second intro video alongside photo
- **Video matches**: Short-form video exchange before committing to full chat
- **Live streaming**: "SparkBot Live — swipe on people in real-time video"

### Social Layer

- **Groups**: Create interest-based rooms ("Coffee lovers in Mumbai")
- **Events**: "SparkBot meetup — 15 members interested"
- **Friend mode**: Browse without dating intent, just to make friends
- **Couples**: Match couples looking for couple friends

### Enterprise / White-Label

- SparkBot as a platform that universities can white-label for their campus
- Corporate "team mixer" edition for remote teams
- Community edition for online communities (Discord servers, Telegram groups)

### Geographic Expansion

- **Multi-city**: Cross-city matching for people who travel
- **NRI mode**: Match Indians across the world
- **Language packs**: Full Hindi/Urdu/Tamil/Telugu/Marathi support

---

## 💌 A Note on Building This

SparkBot was built to prove that you don't need:
- A team
- Funding
- A laptop
- A data center
- Years of experience

You need:
- A clear idea
- Python knowledge
- Termux on your phone
- 1 weekend

The gap between "idea" and "live product" is smaller than it's ever been. SparkBot is proof of that.

If you're reading this README on a phone while figuring out how to push to GitHub from Termux — keep going. The hustle is the moat.

---

## 📞 Support & Contact

- **GitHub Issues**: [github.com/REALNYXAETHER/Sparkbot/issues](https://github.com/REALNYXAETHER/Sparkbot/issues)
- **Telegram**: @REALNYXAETHER
- **Bug reports**: Open a GitHub issue with steps to reproduce + relevant log output from `errors.log`
- **Feature requests**: Open a GitHub issue with use case description

Response time: Best effort. This is a solo project built between other things.

---

## 🌟 Star History

If SparkBot helped you build something, please ⭐ the repo. It helps with discoverability and tells me the project is useful to people.

---

<div align="center">

```
💘 SparkBot
─────────────────────────────────────────
Lines of code:    ~1,500
External deps:    1  (requests)
Setup time:       10 minutes
Deployment cost:  $0/month (Railway free tier)
Features:         17 modules, 12 commands
Users supported:  Up to ~10,000 on JSON backend
─────────────────────────────────────────
Built by: REALNYXAETHER
From: Chhatarpur, Madhya Pradesh 🇮🇳
With: Python, Termux, and determination
─────────────────────────────────────────
```

*Because great software doesn't require great infrastructure. It requires great thinking.*

**[⬆ Back to Top](#-sparkbot)**

</div>

---

## 🧠 Lessons Learned Building SparkBot

### 1. State machines are underrated

Every "conversational" bot problem is a state machine problem. Once you frame it that way, everything becomes simple. User sends message → check state → handle accordingly. No spaghetti, no confusion.

### 2. JSON is a valid database

The instinct is to immediately reach for PostgreSQL or MongoDB. For most indie projects, it's overkill. A JSON file with retry logic and automatic backup handles thousands of users fine. Start simple, upgrade when you actually have the problem.

### 3. Read the API docs carefully

Half of SparkBot's features (Stars payments, Super Like notifications, Boost system) wouldn't exist if I hadn't read the Telegram Bot API docs end to end. The platform gives you more than you think.

### 4. Ship before you're ready

The first version of any bot will be missing features. Ship it. Real users give you real feedback that no amount of planning can replicate.

### 5. One file is okay

Fighting the urge to over-engineer into 20 files made SparkBot debuggable, readable, and shippable. Structure is earned, not imposed from the start.

### 6. The polling loop is enough

Everyone wants webhooks because they sound more professional. Long polling works. Use webhooks when you actually need the performance.

### 7. Error handling is a feature

The difference between a "prototype" and a "product" is mostly error handling. Handle every edge case gracefully, log everything, never show tracebacks to users.

---

## 🎓 What You Learned Building This

If you followed this project from spec to deployed bot, you learned:

- **Telegram Bot API** — sendMessage, sendPhoto, inline keyboards, payments, long polling
- **State machines** — How to manage multi-step conversational flows
- **Python data structures** — Sets for fast exclusion checks, dicts for user data
- **File I/O** — JSON read/write with retry and backup
- **Priority queues** — Scoring and sorting for the browse algorithm
- **Git workflow** — init, add, commit, push, deploy
- **Docker basics** — Simple Dockerfile for Python apps
- **Railway deployment** — Environment variables, volumes, logs
- **Product thinking** — Daily limits, premium tiers, safety systems, UX rules

That's a complete backend developer skillset. This one project — built from a phone in Chhatarpur — covers material that university courses spend a semester on.

Keep building. 🔥

