"""Picks a Bible verse whose theme matches today's overall sentiment.

Keeps the original project's approach (KJV text file, tab-separated
reference/verse, avoid repeating a verse within 365 days) and extends the
single-keyword sentiment buckets into small keyword sets per mood.
"""

import random
import re
from datetime import datetime, timedelta

BIBLE_FILE = "bible.txt"
LOG_FILE = "posted_verses.log"

# Keyword sets used to filter verses by theme, matched as whole words (not
# substrings -- "love" must not match inside "beloved") over KJV text.
SENTIMENT_KEYWORDS = {
    "positive": [
        "joy", "rejoice", "glad", "love", "blessed", "blessing",
        "praise", "thanksgiving", "hope", "delight",
    ],
    "negative": [
        "sorrow", "grief", "grieved", "mourn", "weep", "comfort",
        "afflict", "trouble", "fear not", "distress", "anguish",
    ],
    "neutral": [
        "peace", "faith", "trust", "wisdom", "understanding",
        "patience", "strength", "guidance",
    ],
}

SENTIMENT_PATTERNS = {
    label: re.compile(
        r"\b(?:" + "|".join(re.escape(keyword) for keyword in keywords) + r")\b",
        re.IGNORECASE,
    )
    for label, keywords in SENTIMENT_KEYWORDS.items()
}


def load_verses(path=BIBLE_FILE):
    """Return a list of (reference, text) tuples from the KJV text file."""
    verses = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or "\t" not in line:
                continue
            reference, text = line.split("\t", 1)
            verses.append((reference, text))
    return verses


def get_posted_verses(path=LOG_FILE, within_days=365):
    """Return the set of verse strings posted within the last `within_days`.

    Log lines are "date||mood||verse". Older entries from before mood was
    tracked are "date||verse" -- taking the last "||"-separated field as the
    verse handles both formats.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        return set()

    cutoff = datetime.now() - timedelta(days=within_days)
    posted = set()
    for line in lines:
        line = line.strip()
        if "||" not in line:
            continue
        date_str = line.split("||", 1)[0]
        verse = line.rpartition("||")[2]
        try:
            if datetime.strptime(date_str, "%Y-%m-%d") > cutoff:
                posted.add(verse)
        except ValueError:
            continue
    return posted


def update_log(mood, verse, path=LOG_FILE):
    with open(path, "a", encoding="utf-8") as file:
        file.write(f"{datetime.now().strftime('%Y-%m-%d')}||{mood}||{verse}\n")


def get_todays_logged_entry(path=LOG_FILE):
    """Return (mood, verse) already logged for today, if any, else None.

    `mood` is None for a legacy "date||verse" line logged before mood was
    tracked.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        return None

    for line in reversed(lines):
        line = line.strip()
        if not line.startswith(f"{today}||"):
            continue
        _, _, rest = line.partition("||")
        mood, sep, verse = rest.partition("||")
        return (mood, verse) if sep else (None, rest)
    return None


def select_verse(sentiment_label, verses, posted_verses):
    """Pick a verse matching the sentiment's theme, avoiding recent repeats.

    Falls back to the full unposted pool if no keyword match is available,
    so the bot always has something to say.
    """
    available = [
        (reference, text)
        for reference, text in verses
        if f"{reference} {text}" not in posted_verses
    ]
    if not available:
        # Every verse has been posted in the last year; allow repeats.
        available = verses

    pattern = SENTIMENT_PATTERNS.get(sentiment_label)
    themed = [
        (reference, text)
        for reference, text in available
        if pattern and pattern.search(text)
    ]

    pool = themed if themed else available
    return random.choice(pool)


def get_verse_of_the_day(sentiment_label):
    """Return today's (mood, verse), computing and logging it once per day.

    Repeated calls on the same day (e.g. a user re-running the /verse
    command) return the same (mood, verse) instead of re-rolling -- so the
    displayed mood always matches the mood that actually picked the verse,
    even if the live mood has since shifted -- and don't grow the log.
    `sentiment_label` is ignored once a verse has already been logged today.
    """
    todays_entry = get_todays_logged_entry()
    if todays_entry:
        mood, verse = todays_entry
        return mood or sentiment_label, verse

    verses = load_verses()
    posted = get_posted_verses()
    reference, text = select_verse(sentiment_label, verses, posted)
    verse = f"{reference} {text}"
    update_log(sentiment_label, verse)
    return sentiment_label, verse


if __name__ == "__main__":
    mood, verse = get_verse_of_the_day("neutral")
    print(f"[{mood}] {verse}")
