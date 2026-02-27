import logging
import sys
import os
import yaml

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fetcher.fetch import fetch_articles
from reader.extract import extract_article_text
from summarizer.summarize import summarize_article
from composer.compose import compose_daily_report

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_sources():
    try:
        with open('config/sources.yaml', 'r') as f:
            data = yaml.safe_load(f)
            if data and 'sources' in data:
                return data['sources']
            else:
                logger.error("Invalid sources format in config file")
                return []
    except FileNotFoundError:
        logger.error("config/sources.yaml not found. Please create this file with RSS sources.")
        return []
    except Exception as e:
        logger.error(f"Error loading sources: {e}")
        return []

def main():
    print("Starting Daily News Summary Pipeline")

    # Load RSS sources
    print("Loading RSS sources...")
    sources = load_sources()
    
    if not sources:
        print("No RSS sources found. Exiting.")
        return

    # Fetch new article metadata
    print("Fetching new articles...")
    articles = fetch_articles(sources)
    print(f"Found {len(articles)} new articles.")

    if not articles:
        print("No new articles found. Exiting.")
        return

    # Extract text
    print("Extracting article text...")
    extracted_articles = []
    
    for article in articles:
        try:
            extracted_data = extract_article_text(article["url"])
            
            # --- התיקון: בדיקה שהחילוץ הצליח לפני שממשיכים ---
            if extracted_data and extracted_data.get("clean_text"):
                # Add the article to the list
                extracted_articles.append({**article, **extracted_data})
            else:
                logger.warning(f"Failed to extract text for article: {article.get('url', 'unknown')}")
        except Exception as e:
            logger.error(f"Error processing article {article.get('url', 'unknown')}: {e}")
            continue

    if not extracted_articles:
        print("No articles were successfully processed.")
        return

    # Summarize articles
    print("Summarizing articles...")
    summaries = []
    for article in extracted_articles:
        try:
            summary = summarize_article(article)
            if summary:
                summaries.append(summary)
        except Exception as e:
            logger.error(f"Error summarizing article {article.get('url', 'unknown')}: {e}")
            continue

    if not summaries:
        print("No summaries were generated.")
        return

    # Compose daily report
    print("Composing daily report...")
    compose_daily_report(summaries)

if __name__ == "__main__":
    main()
