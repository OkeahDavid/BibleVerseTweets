"""Pulls a sample of current public posts and scores the overall mood.

Twitter/X's search API now requires a paid tier to read tweets, and Reddit's
public JSON endpoints block scripted requests outright regardless of
User-Agent (confirmed: even a full browser User-Agent gets a bot-challenge
page). Mastodon is a genuine Twitter-like network -- short posts, replies,
reactions, news -- and its public timeline is officially open with no
authentication at all, so this reads from a few open instances instead.
"""

import re

import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

USER_AGENT = "verse-of-the-day-bot/1.0 (personal project)"

# A few general-purpose (not single-topic) instances that keep their public
# timeline open to unauthenticated requests. Querying more than one gives a
# broader sample and some redundancy if one instance changes its policy.
INSTANCES = ["fosstodon.org", "mstdn.social", "hachyderm.io"]

_TAG_RE = re.compile(r"<[^<]+?>")
_analyzer = SentimentIntensityAnalyzer()


def _strip_html(content):
    return _TAG_RE.sub("", content).strip()


def fetch_posts(limit_per_instance=40):
    """Fetch recent English-language public post text from a few instances."""
    texts = []
    for instance in INSTANCES:
        url = f"https://{instance}/api/v1/timelines/public"
        try:
            response = requests.get(
                url,
                headers={"User-Agent": USER_AGENT},
                params={"limit": limit_per_instance},
                timeout=10,
            )
            response.raise_for_status()
            for post in response.json():
                if post.get("language") != "en":
                    continue
                text = _strip_html(post.get("content", ""))
                if text:
                    texts.append(text)
        except (requests.RequestException, ValueError) as error:
            print(f"Warning: failed to fetch {instance}: {error}")
    return texts


def analyze_sentiment(texts):
    """Score a list of texts and return an overall label plus the raw score.

    Returns a dict: {"label": "positive"|"negative"|"neutral", "compound": float}
    using VADER's compound score averaged across all texts, and its standard
    thresholds (+/-0.05) for classifying the result.
    """
    if not texts:
        return {"label": "neutral", "compound": 0.0}

    scores = [_analyzer.polarity_scores(text)["compound"] for text in texts]
    average = sum(scores) / len(scores)

    if average >= 0.05:
        label = "positive"
    elif average <= -0.05:
        label = "negative"
    else:
        label = "neutral"

    return {"label": label, "compound": average}


def get_current_sentiment():
    """Fetch current public posts and return today's overall sentiment."""
    texts = fetch_posts()
    return analyze_sentiment(texts)


if __name__ == "__main__":
    result = get_current_sentiment()
    print(f"Sentiment: {result['label']} (compound score: {result['compound']:.3f})")
