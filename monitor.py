"""
Reddit Mention Tracker
A read-only monitoring tool that tracks product mentions across specified subreddits.
"""

import json
import time
import logging
from datetime import datetime, timezone
from pathlib import Path

import praw
from prawcore.exceptions import TooManyRequests, ResponseException

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("monitor.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Constants
CONFIG_PATH = Path("config.json")
OUTPUT_DIR = Path("data")
MAX_RESULTS_PER_RUN = 100
REQUEST_DELAY = 1.0  # seconds between API calls


def load_config() -> dict:
    """Load configuration from config.json."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            "config.json not found. Copy config.example.json and fill in your credentials."
        )
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def create_reddit_client(config: dict) -> praw.Reddit:
    """Create an authenticated Reddit client (read-only)."""
    reddit = praw.Reddit(
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        username=config["username"],
        password=config["password"],
        user_agent=config["user_agent"],
    )
    reddit.read_only = True  # Enforce read-only mode
    return reddit


def search_subreddit(reddit: praw.Reddit, subreddit_name: str, keywords: list) -> list:
    """Search a subreddit for keyword mentions. Read-only operation."""
    results = []
    subreddit = reddit.subreddit(subreddit_name)

    for keyword in keywords:
        try:
            logger.info(f"Searching r/{subreddit_name} for '{keyword}'...")
            submissions = subreddit.search(keyword, sort="new", time_filter="day", limit=25)

            for submission in submissions:
                results.append(
                    {
                        "type": "submission",
                        "subreddit": subreddit_name,
                        "keyword": keyword,
                        "title": submission.title,
                        "author": str(submission.author) if submission.author else "[deleted]",
                        "url": f"https://reddit.com{submission.permalink}",
                        "created_utc": datetime.fromtimestamp(
                            submission.created_utc, tz=timezone.utc
                        ).isoformat(),
                        "score": submission.score,
                        "num_comments": submission.num_comments,
                    }
                )

            time.sleep(REQUEST_DELAY)  # Respect rate limits

        except TooManyRequests:
            logger.warning("Rate limited. Waiting 60 seconds...")
            time.sleep(60)
        except ResponseException as e:
            logger.error(f"API error searching r/{subreddit_name}: {e}")

    return results[:MAX_RESULTS_PER_RUN]


def save_results(results: list) -> Path:
    """Save results to a local JSON file."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"mentions_{timestamp}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    logger.info(f"Saved {len(results)} results to {output_file}")
    return output_file


def main():
    """Main entry point."""
    logger.info("Starting Reddit Mention Tracker...")

    config = load_config()
    reddit = create_reddit_client(config)

    all_results = []
    for subreddit_name in config["subreddits"]:
        results = search_subreddit(reddit, subreddit_name, config["keywords"])
        all_results.extend(results)

    if all_results:
        save_results(all_results)
        logger.info(f"Run complete. Found {len(all_results)} mentions.")
    else:
        logger.info("Run complete. No new mentions found.")


if __name__ == "__main__":
    main()
