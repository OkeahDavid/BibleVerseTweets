"""Manual CLI for local testing. See scheduler.py for the deploy entrypoint.

Usage:
    python main.py post   Send today's verse to TELEGRAM_CHAT_ID once.
    python main.py bot    Run the interactive bot (/start, /verse, /today).
"""

import sys

from app import post_verse_of_the_day, run_bot

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "post"
    if mode == "post":
        post_verse_of_the_day()
    elif mode == "bot":
        run_bot()
    else:
        raise SystemExit(f"Unknown mode: {mode!r}. Use 'post' or 'bot'.")
