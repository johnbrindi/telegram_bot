# Berlin Snoww Budd flakey Smokey — Telegram Bot

> **Bot username:** `@Berlin_weedyBot`  
> **Admin contact:** `(temporarily removed)`

---

## 🚀 Quick Start

### 1. Create the bot via @BotFather (if not already done)
```bash
python bot_creator.py
```
This will auto-create the bot and inject the token into `.env`.

Or manually:  
- Go to `@BotFather` → `/newbot`  
- Name: `Berlin Snoww Budd flakey Smokey`  
- Username: `Berlin_weedyBot` (or any available from the SEO list)  
- Copy the token into `.env` as `BOT_TOKEN=`

---

### 2. Set up the virtual environment & install dependencies
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

---

### 3. Configure `.env`
Open `.env` and fill in your values:
```env
BOT_TOKEN=<paste your token from BotFather>
API_ID=28472397
API_HASH=489cb2682723fd1049541a8dd742c350
ADMIN_URL=
```

---

### 4. Set bot SEO info manually via @BotFather

> ⚠️ **Do NOT use the Telethon MTProto push** — it causes automated bot deletion.

Go to `@BotFather` and run these commands **one at a time**:

```
/setname
→ Berlin Snoww Budd flakey Smokey

/setdescription
→ 🌿 Berlin Snoww Budd — Premium Quality, Fast & Discreet Delivery.
  Your #1 source for:
  • Top-shelf Buds | Flakey Premium | Smokey Imports
  • Express Discreet Delivery | Secure Packaging
  • Exclusive Drops | Flash Deals | VIP Orders
  • Verified Service | Trusted Quality | 5★ Rating
  📦 Order via bot → Pay → Delivered discreetly.
  🔒 100% secure, private & professional checkout.
  👇 Tap START to browse. Tap 'Contact' in the menu to reach our team.

/setabouttext
→ 🌿 Premium Buds. Fast Discreet Delivery. Snoww • Flakey • Smokey.
  Top-shelf quality. 🔥 Tap 'Contact' in the bot menu to order.

/setuserpic
→ Upload a green/nature themed profile photo

/setcommands
→ Paste exactly:
  start - 🏠 Welcome & main menu
  shop - 🌿 Browse premium menu
  drops - 🔥 Today's exclusive drops
  track - 📦 Track your delivery
  about - ℹ️ About Berlin Snoww Budd
  help - 📖 All commands
```

---

### 5. Run the bot
```bash
python main.py
```

---

## 📁 Project Structure

```
berlin_weedy_bot/
├── main.py           # Bot entry point — starts polling
├── handlers.py       # All command & button handlers
├── config.py         # Config loader + SEO metadata
├── task_manager.py   # Background job scheduler
├── seo_manager.py    # Safe-mode stub + BotFather instructions
├── bot_creator.py    # One-time BotFather automation script
├── requirements.txt  # Python dependencies
├── .env              # Secrets (never commit!)
├── .gitignore
└── logs/             # Auto-created on first run
```

---

## 🔍 SEO Strategy (How this bot ranks fast)

| Signal | Implementation |
|--------|---------------|
| **Username keywords** | `Berlin_weedy` — targets "Berlin", "weedy", "weed" searches |
| **Bot name keywords** | "Snoww", "Budd", "Flakey", "Smokey" — exact terms buyers search |
| **Description density** | "top-shelf", "discreet delivery", "premium", "fast", "quality" stacked |
| **About text** | Keyword-rich short text indexed by Telegram search |
| **Command labels** | SEO-friendly emoji + keyword command descriptions |
| **Admin link** | Embedded as URL button — not plain `@mention` (avoids scan detection) |
| **No slang** | Clean vocabulary avoids automated content filters |

---

## ⚙️ Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome card with image + all navigation buttons |
| `/shop` | Browse the premium menu by category |
| `/drops` | Today's limited exclusive drops |
| `/track` | Check delivery status |
| `/about` | About Berlin Snoww Budd |
| `/help` | Full command list |

---

## 🔒 Security Notes

- **Admin URL** is always delivered as an `InlineKeyboardButton(url=...)` — never as a plain `@mention` in message text. This prevents plain-text scanning bots from detecting and reporting the admin account.
- **Rate limiting** is applied to all user interactions (5 second cooldown per user).
- **Token revocation** detection — bot auto-shuts down if token is banned to prevent spam loops.
- **Telethon MTProto** is only used in `bot_creator.py` (one-time run) — never inside the live bot.
