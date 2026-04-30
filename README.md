# reddit-mention-tracker
A lightweight read-only tool to monitor product mentions on Reddit
# Reddit Mention Tracker

A lightweight read-only monitoring tool that tracks product mentions across specified subreddits.

## Features
- Searches posts and comments for product-related keywords
- Read-only access, no posting or voting
- Respects Reddit API rate limits
- Results stored locally for internal team review

## Usage
- Python 3.9+
- Uses Reddit OAuth2 (script type) for authentication
- Runs on a scheduled basis (e.g., every 30 minutes)

## Compliance
- Fully compliant with Reddit's API Terms of Use
- Adheres to the Responsible Builder Policy
- Rate limited to well under 100 requests/minute
