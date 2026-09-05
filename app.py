"""Shared logic between the manual CLI (main.py) and the deploy worker (scheduler.py)."""

import sentiment
import telegram_bot
import verse_selector
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

WELCOME_MESSAGE = (
    "Hi! I read today's public mood and pick a Bible verse to match it.\n\n"
    "Send /verse to get today's verse."
)


def build_verse_of_the_day_message():
    todays_entry = verse_selector.get_todays_logged_entry()
    if todays_entry:
        mood_label, verse = todays_entry
    else:
        mood_label = sentiment.get_current_sentiment()["label"]
        _, verse = verse_selector.get_verse_of_the_day(mood_label)
    return f"Today's mood: {mood_label}\n\nVerse of the day:\n{verse}"


def post_verse_of_the_day():
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise SystemExit(
            "Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID (see .env.example) before running 'post'."
        )
    message = build_verse_of_the_day_message()
    telegram_bot.send_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)
    print(f"Sent: {message}")


def handle_command(command, chat_id):
    # Once TELEGRAM_CHAT_ID is set, only that chat is honoured -- otherwise
    # anyone who finds the bot's username could message it. Left open while
    # unset so the initial setup flow (message the bot to discover your own
    # chat id) still works.
    if TELEGRAM_CHAT_ID and str(chat_id) != str(TELEGRAM_CHAT_ID):
        return None

    if command in ("start", "help"):
        return WELCOME_MESSAGE
    if command in ("verse", "today"):
        return build_verse_of_the_day_message()
    return "Unknown command. Try /verse."


def run_bot():
    if not TELEGRAM_BOT_TOKEN:
        raise SystemExit("Set TELEGRAM_BOT_TOKEN (see .env.example) before running 'bot'.")
    telegram_bot.run_bot(TELEGRAM_BOT_TOKEN, handle_command)
