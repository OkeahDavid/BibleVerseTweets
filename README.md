# BibleVerseTweets
Feel free to follow the twitter page:


https://twitter.com/DOkeah60511
---

## Description

The **BibleVerseTweets** script is designed to post a daily Bible quote to Twitter. Every day, it selects a random quote from a provided text file and tweets it. To avoid repetition, the script ensures that the same quote is not posted within a 365-day timeframe.

---

## Prerequisites

- Python 3.x
- `requests` library
- `flask` library
- `requests_oauthlib` library

You can install the required libraries using pip:

```
pip install requests flask requests_oauthlib
```

---

## Configuration

1. You need to set up a Twitter developer account and create an App. This will provide you with the required tokens and keys.
2. Replace the placeholders for `API_KEY`, `API_SECRET_KEY`, `ACCESS_TOKEN`, and `ACCESS_TOKEN_SECRET` in the script with your actual keys and tokens.

---

## Files

- `bible.txt`: This file should contain Bible quotes, one per line.
- `posted_verses.log`: This is a log file that keeps track of the quotes that have been tweeted. The script reads this file to ensure that the same quote is not posted twice within a year.

---

## How to Use

1. Ensure you have all the prerequisites installed and the necessary files in place.
2. Run the script:

```
python main.py
```

This will select a random quote from `bible.txt` and post it to Twitter.

---

## Functions

- `post_tweet(content)`: Posts the content to Twitter.
- `get_daily_quote()`: Retrieves a random quote from `bible.txt` that hasn't been posted in the past year.
- `get_posted_quotes()`: Fetches the list of quotes that have been posted in the last year.
- `update_log(quote)`: Adds the posted quote to the `posted_verses.log` file.

---

## Deployment

The script can be integrated into a web server using Flask or any other web framework. The `main(request)` function is designed to work as an endpoint for a web application.

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
