"""
============================================================
config.py — Centralised configuration loader
Project : Berlin Snoww Budd flakey Smokey (@Berlin_weedy)
============================================================
All sensitive values are read from the .env file.
Never hard-code secrets in source files.
"""

import os
from dotenv import load_dotenv

# Load .env file from the project root
load_dotenv()


# ── Bot Credentials ──────────────────────────────────────
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
API_ID: int    = int(os.getenv("API_ID", "0"))
API_HASH: str  = os.getenv("API_HASH", "")

# ── Contact & Identity ───────────────────────────────────
ADMIN_URL: str      = os.getenv("ADMIN_URL", "https://t.me/plugjameson")
OWNER_USERNAME: str = os.getenv("OWNER_USERNAME", "plugjameson")

# ── Webhook (optional – leave empty for long-polling) ────
WEBHOOK_URL: str  = os.getenv("WEBHOOK_URL", "")
WEBHOOK_PORT: int = int(os.getenv("WEBHOOK_PORT", "8443"))

# ── Logging ──────────────────────────────────────────────
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


# ══════════════════════════════════════════════════════════
# 🔍 TELEGRAM BOT SEO — SAFE BRANDING STRATEGY (2026)
#
# Keyword strategy for maximum Telegram search ranking:
#   1. Username @Berlin_weedy targets "Berlin", "weedy", "weed"
#      search queries — high-intent buyers search these exact terms.
#   2. Bot name includes lifestyle keywords: "Snoww", "Budd", "Smokey"
#      which are organic search terms used by the target audience.
#   3. Description uses stacked SEO keywords:
#      "premium", "top shelf", "exclusive", "fast delivery",
#      "discreet", "quality" — all indexed by Telegram search.
#   4. All buttons route to admin via embedded URL (no plain @mention
#      in buttons — reduces automated scan detection surface).
#   5. Bot name + about text = keyword density for in-app search ranking.
# ══════════════════════════════════════════════════════════

# ── Bot display name (SEO-Optimised)
BOT_DISPLAY_NAME: str = "Berlin Snoww Budd flakey Smokey 🌿"

# ── Short description shown in Telegram search results (160 chars max)
BOT_SHORT_DESCRIPTION: str = (
    "🌿 Top-shelf buds. Discreet delivery. Premium quality. "
    "Fast & secure. Order in seconds. 🔥 Snoww • Flakey • Smokey"
)

# ── Full description shown on bot profile page
BOT_DESCRIPTION: str = (
    "🌿 Berlin Snoww Budd — Premium Quality, Fast & Discreet Delivery.\n\n"
    "Your #1 source for:\n"
    "• Top-shelf Buds | Flakey Premium | Smokey Imports\n"
    "• Express Discreet Delivery | Secure Packaging\n"
    "• Exclusive Drops | Flash Deals | VIP Orders\n"
    "• Verified Service | Trusted Quality | 5★ Rating\n\n"
    "📦 Order via bot → Pay → Delivered discreetly.\n"
    "🔒 100% secure, private & professional checkout.\n\n"
    "👇 Tap START to browse. Tap 'Contact' in the menu to reach our team."
)

# ── About text (short — shown under bot profile)
BOT_ABOUT_TEXT: str = (
    "🌿 Premium Buds. Fast Discreet Delivery. Snoww • Flakey • Smokey.\n"
    "Top-shelf quality. 🔥 Tap 'Contact' in the bot menu to order."
)


def validate_config() -> None:
    """Raise early if required env variables are missing."""
    missing = []
    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")
    if not API_ID:
        missing.append("API_ID")
    if not API_HASH:
        missing.append("API_HASH")

    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            "Copy .env.example → .env and fill in the values."
        )
