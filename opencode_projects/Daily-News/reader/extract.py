import trafilatura
import logging
import time
from typing import Dict, Optional

logger = logging.getLogger(__name__)

def extract_article_text(url, cache_dir="cache", max_retries=3) -> Optional[Dict]:
    """
    Extracts main content using Trafilatura with retry logic and validation.
    Ensures safe return of dictionary even if extraction yields unexpected types.
    """
    for attempt in range(max_retries):
        try:
            # Add a small delay between requests to be respectful
            if attempt > 0:
                time.sleep(1)
                
            # Fix for Trafilatura version compatibility
            try:
                downloaded = trafilatura.fetch_url(url)
            except TypeError:
                # Older versions of trafilatura don't support timeout parameter
                downloaded = trafilatura.fetch_url(url)
            
            if not downloaded:
                logger.warning(f"No content fetched from {url}")
                return None
                
            result = trafilatura.bare_extraction(
                downloaded, 
                include_comments=False, 
                include_tables=True,
                favor_recall=True
            )
            
            if result is None:
                logger.warning(f"Extraction returned None for {url}")
                return None
                
            if not isinstance(result, dict):
                if hasattr(result, 'as_dict'):
                    result = result.as_dict()
                else:
                    text = trafilatura.extract(downloaded)
                    if text and len(text.strip()) > 50:  # Only return if text is substantial
                        return {
                            "url": url,
                            "clean_text": text,
                            "title": "Extracted Text",
                            "source": "trafilatura_fallback"
                        }
                    return None

            # Validate extracted content
            text = result.get('text', '')
            if not text or len(text.strip()) < 50:  # Minimum content validation
                logger.warning(f"Insufficient text extracted from {url}")
                return None

            # Ensure title exists
            title = result.get('title') or "No Title"
            
            return {
                "url": url,
                "title": title,
                "clean_text": text,
                "published_at": result.get('date'),
                "source": "trafilatura",
                "author": result.get('author')
            }
        
        except Exception as e:
            logger.error(f"Error extracting {url} (attempt {attempt + 1}): {e}")
            if attempt == max_retries - 1:
                return None
    
    return None