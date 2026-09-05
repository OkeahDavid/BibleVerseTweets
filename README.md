# BibleVerseTweets → Verse-of-the-Day Telegram Bot

## Description

Originally a script that tweeted a random daily Bible verse. Now a Telegram
bot: it reads today's general public mood, scores it as positive, negative,
or neutral, and picks a verse whose theme matches — comfort verses on a heavy
news day, verses of joy and praise on a good one. As before, it avoids
repeating the same verse within 365 days.

Twitter/X's API has required a paid tier to read tweets since 2023 (and
Reddit's unauthenticated JSON endpoints now block scripted requests outright,
even with a browser User-Agent), so the mood is read from Mastodon instead —
a genuinely Twitter-like network whose public timeline is officially open
with no authentication needed at all.

---

## How it works

1. `sentiment.py` fetches recent English-language posts from a few open
   Mastodon instances' public timelines and scores them with VADER (a
   lexicon-based sentiment model tuned for short, informal text) to get an
   overall mood for the day.
2. `verse_selector.py` filters `bible.txt` down to verses themed for that
   mood (keyword matching against a small set of words per sentiment), skips
   anything posted in the last 365 days (tracked in `posted_verses.log`), and
   picks one at random. Asking for "today's verse" more than once returns the
   same verse rather than re-rolling.
3. `telegram_bot.py` is a thin wrapper over the Telegram Bot API (send a
   message, long-poll for commands) — no extra bot framework needed.
4. `app.py` ties those together; `scheduler.py` (the deploy entrypoint) posts
   the verse on a daily schedule and answers `/verse` on demand, both from one
   always-on process. `main.py` is a manual CLI for local testing.

---

## Local setup

1. Install [uv](https://docs.astral.sh/uv/), then install dependencies:
   ```
   uv sync
   ```
2. Create a bot with [@BotFather](https://t.me/BotFather) on Telegram to get
   a bot token.
3. Copy `.env.example` to `.env` and fill in `TELEGRAM_BOT_TOKEN`. To find
   `TELEGRAM_CHAT_ID`: message your bot once, run `uv run main.py bot`
   briefly, and the chat id will appear via the `getUpdates` response — or
   just ask [@userinfobot](https://t.me/userinfobot).
4. Try it:
   ```
   uv run main.py post   # send today's verse once
   uv run main.py bot    # run the interactive /verse listener
   ```

---

## Deploy (always-on hosting)

The scheduled post and the `/verse` listener both need the process running
continuously, so it needs a small always-on host rather than your PC.
Recommended: **Railway**, same as this project's other Telegram bots.

1. Push this repo to GitHub (done).
2. Go to https://railway.app → **New Project → Deploy from GitHub repo** →
   pick `BibleVerseTweets`. Railway detects the `Dockerfile` automatically.
3. In the service → **Variables**, add `TELEGRAM_BOT_TOKEN`,
   `TELEGRAM_CHAT_ID`, and `DATA_DIR` = `/data`.
4. In the service → **Settings → Volumes**, add a volume mounted at **`/data`**
   (so `posted_verses.log` survives restarts/redeploys).
5. Deploy, then check the bot replies to `/verse` on Telegram.

`railway.toml` sets the restart policy so the worker auto-recovers from
crashes. The daily post fires at 08:00 UTC (`POST_HOUR_UTC` in `scheduler.py`).

> **Do not** put real tokens in `railway.toml` or any committed file — they
> go in the host's dashboard env-var settings only.

### Run the Docker image locally (optional)
```
docker build -t bible-verse-tweets .
docker run --env-file .env bible-verse-tweets
```

---

## Files

- `bible.txt` — KJV text, one verse per line (`reference<TAB>text`).
- `posted_verses.log` — date-stamped log of posted verses, used to avoid repeats within a year.
- `config.py` — env/`.env` settings, and the `DATA_DIR` (Railway volume) path.
- `sentiment.py` — fetches and scores today's public mood.
- `verse_selector.py` — picks (and logs) a verse matching that mood.
- `telegram_bot.py` — minimal Telegram Bot API client.
- `app.py` — shared bot logic (message building, command handling).
- `main.py` — manual CLI for local testing.
- `scheduler.py` — always-on deploy entrypoint (Docker `CMD`).

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
