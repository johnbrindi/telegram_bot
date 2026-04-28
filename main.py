"""
============================================================
main.py — Bot Entry Point
Project : Berlin Snoww Budd flakey Smokey (@Berlin_weedy)
============================================================
Fast Discreet Delivery. Premium Quality. Secure Packaging.
============================================================
"""

import asyncio
import sys

from loguru import logger
from telegram import BotCommand, Update
from telegram.request import HTTPXRequest
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    TypeHandler,
    filters,
)

import config
from config import validate_config
from handlers import (
    start_handler,
    help_handler,
    shop_handler,
    drops_handler,
    track_handler,
    faq_handler,
    about_handler,
    callback_handler,
    error_handler,
)
from task_manager import create_task_manager
from keep_alive import keep_alive


# ── Logging ───────────────────────────────────────────────
logger.remove()
logger.add(
    sys.stderr,
    level=config.LOG_LEVEL,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{line}</cyan> — "
        "<level>{message}</level>"
    ),
    colorize=True,
)
logger.add(
    "logs/bot.log",
    rotation="10 MB",
    retention="14 days",
    level="DEBUG",
    compression="zip",
)


# ══════════════════════════════════════════════════════════
# SEO Bootstrap
# ══════════════════════════════════════════════════════════

async def push_seo_on_startup() -> None:
    """
    SEO metadata push — DISABLED to prevent automated bot deletion.
    Telegram flags bots that authenticate via MTProto (Telethon) as botnet activity.
    Set your bot description manually via @BotFather:
      /setname        → Berlin Snoww Budd flakey Smokey
      /setdescription → (your description from seo_manager.py)
      /setabouttext   → (your about text from seo_manager.py)
      /setuserpic     → Upload a green/nature profile photo
    """
    logger.info("[SEO] Startup metadata push skipped (safe mode — use @BotFather manually).")


# ══════════════════════════════════════════════════════════
# Bot Commands Menu
# ══════════════════════════════════════════════════════════

BOT_COMMANDS = [
    BotCommand("start",  "🏠 Welcome & main menu"),
    BotCommand("shop",   "🌿 Browse premium menu"),
    BotCommand("drops",  "🔥 Today's exclusive drops"),
    BotCommand("track",  "📦 Track your delivery"),
    BotCommand("about",  "ℹ️ About Berlin Snoww Budd"),
    BotCommand("help",   "📖 All commands"),
]


# ══════════════════════════════════════════════════════════
# Application Factory
# ══════════════════════════════════════════════════════════

def build_application() -> Application:
    """Build and configure the PTB Application object with increased timeouts."""
    request_config = HTTPXRequest(
        connect_timeout=60.0,
        read_timeout=60.0,
        write_timeout=60.0,
        pool_timeout=60.0,
    )

    app = (
        Application.builder()
        .token(config.BOT_TOKEN)
        .request(request_config)
        .build()
    )

    # 📥 GLOBAL UPDATE LOGGER (For Debugging)
    async def log_update(update: Update, context) -> None:
        logger.info(
            f"⚡ [Update] ID: {update.update_id} | "
            f"Type: {'Message' if update.message else 'Callback/Other'}"
        )

    app.add_handler(TypeHandler(Update, log_update), group=-1)

    # Commands
    app.add_handler(CommandHandler("start",  start_handler))
    app.add_handler(CommandHandler("shop",   shop_handler))
    app.add_handler(CommandHandler("drops",  drops_handler))
    app.add_handler(CommandHandler("track",  track_handler))
    app.add_handler(CommandHandler("faq",    faq_handler))
    app.add_handler(CommandHandler("about",  about_handler))
    app.add_handler(CommandHandler("help",   help_handler))

    # Inline keyboard callbacks
    app.add_handler(CallbackQueryHandler(callback_handler))

    # Unknown commands
    app.add_handler(
        MessageHandler(
            filters.COMMAND,
            lambda u, c: u.message.reply_text(
                "❓ Unknown command. Use /help to see what's available."
            ),
        )
    )

    app.add_error_handler(error_handler)
    return app


# ══════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════

async def main() -> None:
    # 0. Start background web server for Render (Free Tier Hack)
    keep_alive()

    # 1. Validate .env completeness
    validate_config()

    logger.info("=" * 55)
    logger.info("  🌿 Berlin Snoww Budd flakey Smokey")
    logger.info("  📦 Fast Discreet Delivery. Premium Quality.")
    logger.info("  🔗 @Berlin_weedy")
    logger.info("=" * 55)

    # 2. Push SEO metadata to Telegram (safe mode — logs only)
    await push_seo_on_startup()

    # 3. Start background task engine
    task_manager = create_task_manager()
    await task_manager.start()

    # 4. Build and launch the bot
    app = build_application()

    # Set command menu safely (don't crash if network fails here)
    try:
        await app.bot.set_my_commands(BOT_COMMANDS)
        logger.info("📋 Bot command menu updated.")
    except Exception as exc:
        logger.warning(
            f"⚠️ Could not update command menu (network issue), continuing... Error: {exc}"
        )

    logger.info("🚀 Bot running — press CTRL+C to stop.")

    if config.WEBHOOK_URL:
        logger.info(f"🌐 Webhook: {config.WEBHOOK_URL}")
        async with app:
            await app.start()
            await app.bot.set_webhook(url=config.WEBHOOK_URL)
            await asyncio.Event().wait()
    else:
        logger.info("📡 Long-polling active (debug mode).")
        async with app:
            await app.start()
            await app.updater.start_polling(
                drop_pending_updates=False,
                allowed_updates=["message", "callback_query"],
            )
            await asyncio.Event().wait()

    await task_manager.stop()
    logger.info("👋 Bot shut down cleanly.")


# ══════════════════════════════════════════════════════════
# Fleet helper — run 1000+ instances
# ══════════════════════════════════════════════════════════

def run_instance(bot_token: str) -> None:
    """
    Run a single bot instance.
    Use with multiprocessing.Pool to run N instances:

        from main import run_instance
        from multiprocessing import Pool
        tokens = ["token_1", ..., "token_1000"]
        with Pool(len(tokens)) as pool:
            pool.map(run_instance, tokens)
    """
    config.BOT_TOKEN = bot_token
    asyncio.run(main())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⛔ Stopped by user.")
    except SystemExit:
        pass
