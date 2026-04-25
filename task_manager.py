"""
============================================================
task_manager.py — Modular Task Automation Engine
Project : Berlin Snoww Budd flakey Smokey (@Berlin_weedy)
============================================================
Handles background jobs: health checks, drop notifications, etc.
Designed for horizontal scaling to 1,000+ bot instances.
"""

import asyncio
from datetime import datetime, timezone
from typing import Callable, Awaitable, Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger


AsyncTask = Callable[..., Awaitable[Any]]


class TaskManager:
    """
    Central hub that registers and runs background tasks.

    Usage:
        tm = TaskManager()
        tm.register_task("health_check", my_task, interval_seconds=300)
        await tm.start()
        ...
        await tm.stop()
    """

    def __init__(self) -> None:
        self._scheduler = AsyncIOScheduler(timezone="UTC")
        self._tasks: dict[str, dict] = {}

    def register_task(
        self,
        task_id: str,
        coro_func: AsyncTask,
        interval_seconds: int = 60,
        **kwargs: Any,
    ) -> None:
        if task_id in self._tasks:
            logger.warning(f"Task '{task_id}' already registered — skipping.")
            return

        self._tasks[task_id] = {
            "func": coro_func,
            "interval": interval_seconds,
            "kwargs": kwargs,
        }

        self._scheduler.add_job(
            func=coro_func,
            trigger=IntervalTrigger(seconds=interval_seconds),
            id=task_id,
            name=task_id,
            kwargs=kwargs,
            replace_existing=True,
            misfire_grace_time=30,
        )
        logger.info(f"📋 Task '{task_id}' registered — every {interval_seconds}s.")

    def unregister_task(self, task_id: str) -> None:
        if task_id in self._tasks:
            self._scheduler.remove_job(task_id)
            del self._tasks[task_id]
            logger.info(f"🗑️  Task '{task_id}' removed.")

    async def start(self) -> None:
        self._scheduler.start()
        logger.info("🚀 TaskManager started.")

    async def stop(self) -> None:
        self._scheduler.shutdown(wait=False)
        logger.info("🛑 TaskManager stopped.")

    def list_tasks(self) -> list[str]:
        return list(self._tasks.keys())


# ══════════════════════════════════════════════════════════
# Built-in Tasks
# ══════════════════════════════════════════════════════════

async def refresh_seo_metadata() -> None:
    """
    SEO refresh — DISABLED (MTProto Telethon triggers bot deletion).
    Update bot info manually via @BotFather instead.
    """
    now = datetime.now(tz=timezone.utc).strftime("%H:%M UTC")
    logger.debug(f"[{now}] [SEO] Refresh skipped (safe mode).")


async def health_check() -> None:
    """🩺 Heartbeat — logs that the instance is alive."""
    now = datetime.now(tz=timezone.utc).strftime("%H:%M UTC")
    logger.debug(f"[{now}] 🩺 Instance alive — Berlin Snoww Budd (@Berlin_weedy)")


async def notify_new_drop() -> None:
    """
    🔥 Stub: broadcast new drop announcements to subscribers.
    TODO: Query drops database, compare with last broadcast,
          send new drops to subscribed user IDs via bot.send_message().
    """
    now = datetime.now(tz=timezone.utc).strftime("%H:%M UTC")
    logger.info(f"[{now}] 🔥 Checking for new drops to broadcast …")
    await asyncio.sleep(0)   # placeholder


def create_task_manager() -> TaskManager:
    """
    Factory: wire all built-in tasks and return a ready TaskManager.
    Call once per bot instance.
    """
    tm = TaskManager()
    # SEO refresh DISABLED — Telethon MTProto causes automated bot deletion
    # tm.register_task("seo_refresh", refresh_seo_metadata, interval_seconds=86400)
    # Drop notifications — every 6 hours
    tm.register_task("notify_drops", notify_new_drop, interval_seconds=21600)
    # Health check — every 5 minutes
    tm.register_task("health_check", health_check,    interval_seconds=300)
    return tm
