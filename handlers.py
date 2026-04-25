"""
============================================================
handlers.py — All Bot Command & Message Handlers
Project : Berlin Snoww Budd flakey Smokey (@Berlin_weedy)
============================================================
SEO-rich messaging. Admin contact embedded via InlineKeyboardButton
URL buttons (NOT plain @mentions) to avoid automated detection.
"""

import io
import time
import httpx
from loguru import logger
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.error import Forbidden, InvalidToken
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

import config

# ── Rate Limiter ──────────────────────────────────────────
USER_COOLDOWNS: dict[int, float] = {}
COOLDOWN_SECONDS = 5

def is_rate_limited(user_id: int) -> bool:
    """Returns True if the user is clicking too fast."""
    now = time.time()
    last_action = USER_COOLDOWNS.get(user_id, 0.0)
    if now - last_action < COOLDOWN_SECONDS:
        return True
    USER_COOLDOWNS[user_id] = now
    return False


# ══════════════════════════════════════════════════════════
# 🎴  WELCOME MESSAGE CARD  (/start)
# ══════════════════════════════════════════════════════════

# High-quality lifestyle/nature image (Unsplash — safe, royalty-free)
WELCOME_IMAGE_URL = (
    "https://images.unsplash.com/photo-1508739773434-c26b3d09e071"
    "?w=900&q=85&fit=crop"
)

# ── This is the FIRST message users see — packed with SEO keywords
#    and the admin link embedded inside buttons (not plain text).
WELCOME_CAPTION = """
🌿 *Berlin Snoww Budd flakey Smokey*

━━━━━━━━━━━━━━━━━━━━━━━
❄️ *Top-Shelf Snoww Buds*
💨 *Premium Flakey Quality*
🔥 *Smokey Imports & Exclusive Drops*
📦 *Discreet & Secure Delivery*
⚡ *Order in seconds — delivered fast*
━━━━━━━━━━━━━━━━━━━━━━━

Welcome to Berlin's #1 premium delivery service. \
Quality you can trust. Every order handled with care \
and shipped discreetly to your door.

Whether you want *Snoww*, *Flakey*, or *Smokey* — \
we've got the best selections, VIP pricing, and \
express discreet delivery that arrives in pristine condition.

👇 *Tap a button below to get started*
"""


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start — Send the Welcome Message Card."""
    user = update.effective_user

    # Apply Rate Limiting
    if is_rate_limited(user.id):
        logger.warning(f"⏳ Rate limited user: {user.id}")
        return

    if not update.message:
        logger.warning("Empty message in /start update")
        return

    # ── SEO & Deep Link Tracking ────────────────────────────
    # Extract referral code from deep link (e.g., t.me/Bot?start=ref123)
    if context.args:
        referral_payload = context.args[0]
        logger.info(f"🔗 DEEP LINK HIT: User {user.id} joined via referral: {referral_payload}")
        # Note: Here you can add Google Analytics Measurement Protocol tracking
        # e.g., track_start_event(user.id, referral_payload)
    else:
        logger.info(f"📥 RECEIVED /start FROM: {user.id} (@{user.username})")

    # ── Admin contact is ALWAYS embedded as a URL button — never as
    #    a plain @mention — to minimise automated scan detection surface.
    keyboard = InlineKeyboardMarkup(
        [
            [
                # PRIMARY CTA — routes directly to admin account via button URL
                InlineKeyboardButton(
                    text="📩 Contact / Place Order",
                    url=config.ADMIN_URL,
                )
            ],
            [
                InlineKeyboardButton(text="🌿 Browse Menu",       callback_data="shop"),
                InlineKeyboardButton(text="🔥 Today's Drops",     callback_data="drops"),
            ],
            [
                InlineKeyboardButton(text="📦 Track Delivery",    callback_data="track"),
                InlineKeyboardButton(text="💬 Help & FAQ",        callback_data="faq"),
            ],
            [
                InlineKeyboardButton(text="ℹ️ About Us",          callback_data="about"),
            ],
        ]
    )

    # ── Try to send with image ────────────────────────────
    try:
        logger.debug(f"Fetching image from {WELCOME_IMAGE_URL}")
        async with httpx.AsyncClient(timeout=15) as http:
            resp = await http.get(WELCOME_IMAGE_URL)
            resp.raise_for_status()
            image_bytes = io.BytesIO(resp.content)
            image_bytes.name = "berlin_snoww.jpg"

        logger.info(f"📤 SENDING photo card to {user.id}")
        await update.message.reply_photo(
            photo=image_bytes,
            caption=WELCOME_CAPTION,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboard,
        )
        logger.info(f"✅ SUCCESSFULLY sent /start response to {user.id}")

    except Exception as exc:
        logger.warning(f"❌ Image/Photo send failed ({exc}), falling back to text.")
        await update.message.reply_text(
            text=WELCOME_CAPTION,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboard,
        )


# ══════════════════════════════════════════════════════════
# 🌿  SHOP / MENU
# ══════════════════════════════════════════════════════════

SHOP_TEXT = """
🌿 *Berlin Snoww Budd — Premium Menu*
_Select your category below_

━━━━━━━━━━━━━━━━━━━━
❄️ *Snoww Grade*    — Top-shelf premium, ultra flakey
💨 *Flakey Imports* — Hand-selected exotic strains
🔥 *Smokey Blends*  — Classic heavy-hitting selections
🎁 *VIP Bundles*    — Exclusive multi-pack deals
⚡ *Flash Deals*    — Limited-time discounted drops
━━━━━━━━━━━━━━━━━━━━

📬 All orders ship *Discreetly & Securely*
🔒 Complete *privacy* guaranteed on every package

👉 Tap *Contact* to speak with our team and place your order.
"""


async def shop_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("📩 Order Now",     url=config.ADMIN_URL),
        InlineKeyboardButton("🔥 Today's Drops", callback_data="drops"),
    ]])
    msg = update.message or update.callback_query.message
    await msg.reply_text(SHOP_TEXT, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)


# ══════════════════════════════════════════════════════════
# 🔥  TODAY'S DROPS
# ══════════════════════════════════════════════════════════

DROPS_TEXT = """
🔥 *Exclusive Drops — Limited Availability*
_Highly requested premium selections_

━━━━━━━━━━━━━━━━━━━━
❄️ *Drop 01* — Snoww Premium Bundle (Very limited)
💨 *Drop 02* — Flakey Exotic Pack ✅ Available now
🔥 *Drop 03* — Smokey VIP Collection Box ⏰ Ending soon
🎁 *Drop 04* — Berlin Special Blend ⚡ New arrival
━━━━━━━━━━━━━━━━━━━━

⚡ *Express Discreet Shipping* included on all drops.
📦 *Secure Packaging* — sealed, private & beautifully wrapped.

📩 DM to reserve your selection before it sells out.
"""


async def drops_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("🔒 Reserve Now", url=config.ADMIN_URL),
    ]])
    msg = update.message or update.callback_query.message
    await msg.reply_text(DROPS_TEXT, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)


# ══════════════════════════════════════════════════════════
# 📦  TRACK DELIVERY
# ══════════════════════════════════════════════════════════

TRACK_TEXT = """
📦 *Delivery Tracking*

To check your delivery status, contact our support desk \
with your order reference number.

📬 Delivery stages:
• ✅ Order Confirmed & Processed
• 🚚 Dispatched via Express Discreet Courier
• 🔒 Sealed & Securely Packaged
• 🏠 Delivered Privately to Your Door

All updates sent directly to you. ⏱️ \
Top-tier customer service, always.
"""


async def track_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("📩 Get Tracking Update", url=config.ADMIN_URL),
    ]])
    msg = update.message or update.callback_query.message
    await msg.reply_text(TRACK_TEXT, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)


# ══════════════════════════════════════════════════════════
# 💬  FAQ
# ══════════════════════════════════════════════════════════

FAQ_TEXT = """
💬 *Client Support & FAQ*

🔒 *Is my order private?*
100%. Every package is discreetly sealed with no external markings.

⚡ *How fast is delivery?*
Express fulfillment. Most orders delivered within 24-48 hours.

💳 *How do I place an order?*
Tap the *Contact* button — our team handles everything directly.

📦 *What about packaging?*
Every order ships in secure, unmarked packaging. Total privacy.

🌿 *What strains/grades are available?*
Snoww, Flakey, Smokey grades plus VIP exotic imports. Ask our team.

🛒 *Do you do bulk/VIP orders?*
Yes. Our concierge service handles custom volume requests.

━━━━━━━━━━━━━━━━━━━━
Need more info? Contact us directly 👇
"""


async def faq_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("💬 Contact Support", url=config.ADMIN_URL),
    ]])
    msg = update.message or update.callback_query.message
    await msg.reply_text(FAQ_TEXT, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)


# ══════════════════════════════════════════════════════════
# ℹ️  ABOUT
# ══════════════════════════════════════════════════════════

ABOUT_TEXT = """
ℹ️ *About Berlin Snoww Budd flakey Smokey*

🌿 Berlin's #1 premium delivery service for top-shelf quality.

━━━━━━━━━━━━━━━━━━━━
❄️ *Snoww Grade* — Ultra-premium top-shelf selection
💨 *Flakey Imports* — Hand-picked exotic quality
🔥 *Smokey Classics* — Heavy-hitting trusted blends
📦 *Express Discreet Delivery* — Fast & fully private
🔒 *Secure Packaging* — Unmarked, professional
⭐ *Trusted by VIP clients across Berlin & beyond*
━━━━━━━━━━━━━━━━━━━━

📩 *Browse via bot → Order via DM → Delivered discreetly*

🔗 Tap below to reach our team directly:
"""


async def about_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("📞 Contact Our Team", url=config.ADMIN_URL),
    ]])
    msg = update.message or (update.callback_query.message if update.callback_query else None)
    if msg:
        await msg.reply_text(ABOUT_TEXT, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)


# ══════════════════════════════════════════════════════════
# 📖  HELP
# ══════════════════════════════════════════════════════════

HELP_TEXT = """
📖 *Commands & Navigation*

/start  — 🏠 Welcome & main menu
/shop   — 🌿 Browse premium menu
/drops  — 🔥 Today's exclusive drops
/track  — 📦 Track your delivery
/about  — ℹ️ About Berlin Snoww Budd
/help   — 📖 Show this menu

━━━━━━━━━━━━━━━━━━━━
📩 For immediate assistance, tap the button below:
"""


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("📩 Contact / Order Now", url=config.ADMIN_URL),
    ]])
    await update.message.reply_text(
        HELP_TEXT,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard,
    )


# ══════════════════════════════════════════════════════════
# 🔘  CALLBACK QUERY HANDLER  (Inline Button Clicks)
# ══════════════════════════════════════════════════════════

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Route inline keyboard button presses."""
    query = update.callback_query
    data  = query.data
    user  = update.effective_user

    # Apply Rate Limiting for buttons
    if is_rate_limited(user.id):
        await query.answer("⏳ Please wait a few seconds before clicking again.", show_alert=True)
        return

    await query.answer()

    dispatch = {
        "shop"  : shop_handler,
        "drops" : drops_handler,
        "track" : track_handler,
        "faq"   : faq_handler,
        "about" : about_handler,
    }

    handler_func = dispatch.get(data)
    if handler_func:
        await handler_func(update, context)
    else:
        await query.message.reply_text("❓ Unknown option. Use /help.")


# ══════════════════════════════════════════════════════════
# 🛡️  ERROR HANDLER
# ══════════════════════════════════════════════════════════

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Exception: {context.error}")

    # Graceful shutdown if Telegram revokes the token
    if isinstance(context.error, (InvalidToken, Forbidden)):
        logger.critical("🛑 BOT TOKEN REVOKED OR UNAUTHORIZED! Shutting down.")
        import sys
        sys.exit(1)

    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "⚠️ A system error occurred. Please try again or type /start."
            )
        except (InvalidToken, Forbidden):
            pass
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")
