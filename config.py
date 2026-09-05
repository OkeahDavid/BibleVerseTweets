"""Central configuration, loaded from environment / .env file."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

# Railway mounts the volume wherever the dashboard says and reports the path in
# RAILWAY_VOLUME_MOUNT_PATH. Honouring it means a volume attached at any path is
# picked up automatically; hardcoding /data instead would write the log to the
# container's ephemeral layer, which looks identical until a redeploy wipes it.
# Locally (no Railway env), this is just the repo root, so posted_verses.log
# stays exactly where it's always been for a plain git clone.
DATA_DIR = Path(
    os.getenv("DATA_DIR")
    or os.getenv("RAILWAY_VOLUME_MOUNT_PATH")
    or str(ROOT)
)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# True when nothing durable was found but we are clearly deployed -- the
# 365-day no-repeat log would be lost on the next redeploy.
DATA_DIR_IS_EPHEMERAL = bool(
    os.getenv("RAILWAY_ENVIRONMENT")
    and not os.getenv("RAILWAY_VOLUME_MOUNT_PATH")
    and not os.getenv("DATA_DIR")
)

LOG_PATH = DATA_DIR / "posted_verses.log"
BIBLE_PATH = ROOT / "bible.txt"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
