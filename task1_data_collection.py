import requests
import time
import json
import os
from datetime import datetime

# Base URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Headers (required)
HEADERS = {"User-Agent": "TrendPulse/1.0"}

# Categories with keywords
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Max stories per category
MAX_PER_CATEGORY = 25


def fetch_top_story_ids(limit=500):
    """Fetch top story IDs from HackerNews"""
    try:
        response = requests.get(TOP_STORIES_URL, headers=HEADERS)
        response.raise_for_status()
        return response.json()[:limit]
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        return []


def fetch_story(story_id):
    """Fetch individual story details"""
    try:
        response = requests.get(ITEM_URL.format(story_id), headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching story {story_id}: {e}")
        return None


def assign_category(title):
    """Assign category based on keywords"""
    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category

    return None  # skip if no match


def main():
    # Fetch top IDs
    story_ids = fetch_top_story_ids()

    collected = []
    category_counts = {cat: 0 for cat in CATEGORIES}

    # Loop through categories
    for category in CATEGORIES:
        print(f"\nCollecting category: {category}")

        for story_id in story_ids:
            # Stop if category limit reached
            if category_counts[category] >= MAX_PER_CATEGORY:
                break

            story = fetch_story(story_id)

            if not story or "title" not in story:
                continue

            assigned_category = assign_category(story["title"])

            # Only collect if it matches current category
            if assigned_category == category:
                data = {
                    "post_id": story.get("id"),
                    "title": story.get("title"),
                    "category": assigned_category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by"),
                    "collected_at": datetime.now().isoformat()
                }

                collected.append(data)
                category_counts[category] += 1

        # Sleep AFTER each category loop (as required)
        time.sleep(2)

    # Create data folder if not exists
    os.makedirs("data", exist_ok=True)

    # File name with date
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    # Save to JSON
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected, f, indent=4)

    print(f"\nCollected {len(collected)} stories. Saved to {filename}")


if __name__ == "__main__":
    main()8ETW-ASLO