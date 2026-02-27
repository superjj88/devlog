import json
import os
import time
import logging
import feedparser
from datetime import datetime
from typing import List, Dict
from time import mktime
import hashlib

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

WAR_KEYWORDS = [
    "Ukraine", "Russia", "Putin", "Zelensky", "Kyiv", "Moscow", "War", "Kremlin", "Donbas"
]

def load_state(cache_dir):
    """טוען את זמן הריצה האחרון מקובץ state.json"""
    state_file = os.path.join(cache_dir, "state.json")
    try:
        with open(state_file, "r") as f:
            state = json.load(f)
            return state.get("last_run_timestamp", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return time.time() - 86400

def save_state(cache_dir):
    """שומר את זמן הריצה הנוכחי"""
    state_file = os.path.join(cache_dir, "state.json")
    with open(state_file, "w") as f:
        json.dump({"last_run_timestamp": time.time()}, f)

def is_related_to_war(title: str) -> bool:
    """בודק אם הכותרת מכילה אחת ממילות המפתח"""
    if not title:
        return False
    title_lower = title.lower()
    return any(keyword.lower() in title_lower for keyword in WAR_KEYWORDS)

def generate_article_id(article: Dict) -> str:
    """יוצר מזהה ייחודי למאמר על פי URL וזמן פירסום"""
    url = article.get("url", "")
    published = article.get("published_at", "")
    # Create a hash of URL and published time to ensure uniqueness
    article_key = f"{url}_{published}"
    return hashlib.md5(article_key.encode()).hexdigest()

def fetch_articles(sources: List[Dict], cache_dir: str = "cache") -> List[Dict]:
    """
    Fetch articles filtering by war keywords, time window, and limit of 10 per source.
    """
    os.makedirs(cache_dir, exist_ok=True)
    
    last_run_ts = load_state(cache_dir)
    urls_seen_file = os.path.join(cache_dir, "urls_seen.json")
    
    try:
        with open(urls_seen_file, "r") as f:
            urls_seen = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        urls_seen = []

    articles = []
    
    logger.info(f"Filtering articles published after: {datetime.fromtimestamp(last_run_ts)}")

    for source in sources:
        # Check if source is a dict (from YAML) or a string (old format)
        if isinstance(source, str):
            logger.warning(f"Skipping invalid source: {source}")
            continue
            
        if not source.get("enabled", False):
            continue

        try:
            # Add rate limiting between sources
            time.sleep(1)
            
            feed = feedparser.parse(source["url"])
            source_count = 0 
            
            for entry in feed.entries:
                if source_count >= 10:
                    break

                url = entry.get("link", "")
                title = entry.get("title", "")
                
                if not url:
                    continue
                    
                # Check if URL already processed
                if url in urls_seen:
                    continue

                published_ts = 0
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published_ts = mktime(entry.published_parsed)
                elif hasattr(entry, 'published') and entry.published:
                    # Try to parse the published date if it's in string format
                    try:
                        parsed_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')
                        published_ts = parsed_date.timestamp()
                    except:
                        pass
                
                # Skip if article is too old
                if published_ts < last_run_ts:
                    continue

                if not is_related_to_war(title):
                    continue

                article = {
                    "url": url,
                    "title": title,
                    "source": source["name"],
                    "published_at": entry.get("published", ""),
                    "fetched_at": datetime.now().isoformat(),
                    "content": entry.get("summary", ""),
                    "article_id": generate_article_id({
                        "url": url,
                        "published_at": entry.get("published", "")
                    })
                }

                articles.append(article)
                urls_seen.append(url)
                source_count += 1
                
            logger.info(f"Source '{source['name']}': Found {source_count} relevant articles.")

        except Exception as e:
            logger.error(f"Error fetching from {source['name']}: {e}")
            continue

    raw_articles_file = os.path.join(cache_dir, "articles_raw.jsonl")
    
    # Check if article already exists in cache to prevent duplicates
    existing_urls = set()
    existing_article_ids = set()
    try:
        with open(raw_articles_file, "r") as f:
            for line in f:
                if line.strip():
                    article_data = json.loads(line)
                    existing_urls.add(article_data.get("url"))
                    existing_article_ids.add(article_data.get("article_id"))
    except FileNotFoundError:
        pass
    
    with open(raw_articles_file, "a") as f:
        for article in articles:
            # Check both URL and article_id for duplicates
            if article["url"] not in existing_urls and article["article_id"] not in existing_article_ids:
                f.write(json.dumps(article) + "\n")
                existing_urls.add(article["url"])
                existing_article_ids.add(article["article_id"])

    with open(urls_seen_file, "w") as f:
        json.dump(urls_seen[-1000:], f)

    save_state(cache_dir)

    logger.info(f"Total new relevant articles fetched: {len(articles)}")
    return articles