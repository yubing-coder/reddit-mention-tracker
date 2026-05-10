# Reddit Mention Tracker

A lightweight, read-only monitoring tool that tracks product mentions across specified subreddits for internal team awareness.

## Purpose

This tool helps our team stay informed about community discussions related to our product. It only **reads** public data — it never posts, votes, messages, or modifies any content on Reddit.

## How It Works

1. Authenticates via Reddit OAuth2 (script-type application)
2. Periodically searches specified subreddits for keyword mentions
3. Stores results locally in JSON format for internal review
4. Respects Reddit's rate limits (< 60 requests/minute)

## Technical Details

- **Language**: Python 3.9+
- **Library**: PRAW (Python Reddit API Wrapper)
- **Auth type**: OAuth2 script application (confidential client)
- **Data access**: Read-only (uses `read` scope only)
- **Storage**: Local JSON files, no external database or redistribution
- **Schedule**: Runs every 30 minutes via cron/task scheduler

## Compliance

This project adheres to Reddit's [Responsible Builder Policy](https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy):

- **Read-only**: No write operations (no posts, comments, votes, or messages)
- **Rate-limited**: Stays well under the 100 requests/minute threshold
- **No data redistribution**: All collected data is stored locally for internal use only
- **No scraping**: Uses official API endpoints exclusively
- **User-Agent**: Follows Reddit's recommended format
- **No personal data collection**: Only tracks public post/comment text and metadata

## Installation

```bash
pip install -r requirements.txt
cp config.example.json config.json
# Edit config.json with your credentials
```

## Configuration

See `config.example.json` for the required fields. Never commit actual credentials.

## Usage

```bash
python monitor.py
```

## Rate Limiting

The tool implements exponential backoff and respects Reddit's `X-Ratelimit-*` headers. If rate limits are approached, the tool automatically pauses until the reset window.

## License

MIT
