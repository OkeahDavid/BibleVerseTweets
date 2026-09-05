"""Always-on worker: this is the Docker deploy entrypoint (see Dockerfile).

Posts the verse of the day on a fixed daily schedule, and answers /verse on
demand in a background thread, so one process covers both without needing
Railway's (paid) cron plugin.
"""
from __future__ import annotations

import threading

from apscheduler.schedulers.blocking import BlockingScheduler

from app import post_verse_of_the_day, run_bot

# UTC hour to post the daily verse. Sentiment is read fresh at this moment,
# so this is "when the day's mood snapshot is taken", not just a reminder time.
POST_HOUR_UTC = 8


def start_command_listener_in_background() -> threading.Thread:
    thread = threading.Thread(target=run_bot, daemon=True, name="tg-commands")
    thread.start()
    return thread


def schedule() -> None:
    sched = BlockingScheduler(timezone="UTC")

    start_command_listener_in_background()

    sched.add_job(
        post_verse_of_the_day, "cron", hour=POST_HOUR_UTC, minute=0,
        id="daily-verse", misfire_grace_time=3600,
    )
    print(f"[schedule] daily verse post set for {POST_HOUR_UTC:02d}:00 UTC", flush=True)
    sched.start()


if __name__ == "__main__":
    schedule()
