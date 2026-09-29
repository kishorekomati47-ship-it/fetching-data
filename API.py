import requests
import time
import json
from pathlib import Path
from datetime import datetime

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {
    "User-Agent": "TrendPulse/1.0"
}

keywords = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

try:
    response = requests.get(
        TOP_STORIES_URL,
        headers=headers,
        timeout=10
    )
    response.raise_for_status()
    story_ids = response.json()[:500]

except requests.RequestException as error:
    print("Failed to fetch top stories:", error)
    story_ids = []

stories = []
category_counts = {
    category: 0 for category in keywords
}

for category, category_keywords in keywords.items():

    for story_id in story_ids:

        if category_counts[category] >= 25:
            break

        try:
            response = requests.get(
                ITEM_URL.format(story_id),
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            story = response.json()

        except requests.RequestException as error:
            print(f"Failed to fetch story {story_id}: {error}")
            continue

        title = story.get("title")

        if not title:
            continue

        title_lower = title.lower()

        matched = False

        for keyword in category_keywords:
            if keyword.lower() in title_lower:
                matched = True
                break

        if not matched:
            continue

        story_data = {
            "post_id": story.get("id"),
            "title": title,
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": datetime.now().isoformat()
        }

        stories.append(story_data)
        category_counts[category] += 1

    if category != "entertainment":
        time.sleep(2)

data_folder = Path("data")
data_folder.mkdir(exist_ok=True)

date = datetime.now().strftime("%Y%m%d")
file_path = data_folder / f"trends_{date}.json"

with open(file_path, "w", encoding="utf-8") as file:
    json.dump(stories, file, indent=4)

print(f"Collected {len(stories)} stories. Saved to {file_path}")
