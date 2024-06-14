import requests
from datetime import datetime, timedelta
import random
from flask import jsonify
from requests_oauthlib import OAuth1

API_KEY = 'YOUR_API_KEY'
API_SECRET_KEY = 'YOUR_API_SECRET_KEY'
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
ACCESS_TOKEN_SECRET = 'YOUR_ACCESS_TOKEN_SECRET'

auth = OAuth1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

LOG_FILE = 'posted_verses.log'
BIBLE_FILE = 'bible.txt'

def post_tweet(content):
    url = "https://api.twitter.com/2/tweets"
    
    payload = {
        "text": content
    }
    
    headers = {
        "Content-type": "application/json"
    }
    
    response = requests.post(url, auth=auth, headers=headers, json=payload)
    
    if response.status_code != 201:
        print(f"Failed to post tweet with error: {response.text}")
        return None
    return response.json()

def get_daily_quote():
    with open(BIBLE_FILE, 'r') as file:
        quotes = file.readlines()

    posted_quotes = get_posted_quotes()

    # Filter out verses that have been posted in the last year
    available_quotes = [q for q in quotes if q not in posted_quotes]

    return random.choice(available_quotes).replace('\t', ' ').strip()

def get_posted_quotes():
    try:
        with open(LOG_FILE, 'r') as file:
            lines = file.readlines()
            one_year_ago = datetime.now() - timedelta(days=365)
            return [line.split('||')[1].strip() for line in lines if datetime.strptime(line.split('||')[0], '%Y-%m-%d') > one_year_ago]
    except FileNotFoundError:
        return []

def update_log(quote):
    with open(LOG_FILE, 'a') as file:
        file.write(f"{datetime.now().strftime('%Y-%m-%d')}||{quote}\n")

def main():
    quote = get_daily_quote()
    result = post_tweet(quote)
    if result:
        print(f"Successfully posted tweet with ID: {result['data']['id']}")
        update_log(quote)

if __name__ == "__main__":
    main()
