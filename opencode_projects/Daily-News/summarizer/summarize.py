import ollama
import json
import os
import re
import logging
import time
from typing import Dict, Optional
from functools import wraps

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

ollama_host = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
client = ollama.Client(host=ollama_host)

MAIN_MODEL = "gemma3:4b"
TRANSLATION_MODEL = "gemma3:4b" 

def retry(max_attempts=3, delay=1):
    """Decorator for retrying function calls with exponential backoff"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay * (attempt + 1)}s...")
                    time.sleep(delay * (attempt + 1))
        return wrapper
    return decorator


def is_hebrew(text):
    """בודק אם הטקסט מכיל אותיות עבריות"""
    return bool(re.search(r'[\u0590-\u05FF]', text))

def validate_summary_content(summary: Dict) -> bool:
    """ Validates that the summary contains meaningful content"""
    if not summary:
        return False
    
    bullets_en = summary.get("bullets_en", [])
    bullets_he = summary.get("bullets_he", [])
    
    # Check if we have at least one meaningful bullet point in each language
    meaningful_en = any(bullet and len(bullet.strip()) > 10 for bullet in bullets_en)
    meaningful_he = any(bullet and len(bullet.strip()) > 10 for bullet in bullets_he)
    
    return meaningful_en or meaningful_he

def translate_to_hebrew(text_list: list, title: str) -> Dict:
    """
    Translates content to Hebrew with automatic retry if output is English.
    """
    # 1. ניסיון ראשון: פרומפט רגיל
    prompt = f"""
    You are a professional translator. Translate the following English news summary to Hebrew.
    
    STRICT INSTRUCTIONS:
    1. The output MUST be in HEBREW language (עברית). 
    2. Do NOT output English text in the JSON values.
    3. Translate accurately and professionally.
    4. Output strictly valid JSON.
    5. Do not add any extra text or explanations.

    Input Content:
    Title: "{title}"
    Bullets: {json.dumps(text_list)}

    Output Format (JSON):
    {{
        "title_he": "כותרת בעברית",
        "bullets_he": ["נקודה בעברית", "עוד נקודה בעברית"]
    }}
    """
    
    for attempt in range(2): # שני ניסיונות
        try:
            response = client.generate(model=TRANSLATION_MODEL, prompt=prompt)
            response_text = response['response'].strip()
            
            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                data = json.loads(json_match.group())
                
                # בדיקת איכות: האם הכותרת או הבולט הראשון בעברית?
                he_title = data.get("title_he", "")
                he_bullets = data.get("bullets_he", [])
                
                check_text = he_title + " " + (he_bullets[0] if he_bullets else "")
                
                if is_hebrew(check_text):
                    return data # הצלחה!
                else:
                    logger.warning(f"Translation attempt {attempt+1} failed (returned English). Retrying...")
                    # בניסיון הבא נהיה אגרסיביים יותר
                    prompt += "\n\nSYSTEM ALERT: YOUR PREVIOUS OUTPUT WAS IN ENGLISH. YOU MUST OUTPUT HEBREW ONLY!!!!"
            
        except Exception as e:
            logger.error(f"Translation error on attempt {attempt+1}: {e}")

    # אם כל הניסיונות נכשלו, נחזיר את המקור עם הערה
    logger.error("All translation attempts failed.")
    return {"title_he": title + " (Translation Failed)", "bullets_he": text_list}


@retry(max_attempts=3, delay=2)
def summarize_article(article: Dict, model_name: str = MAIN_MODEL) -> Optional[Dict]:
    text_content = article.get('clean_text', '').strip()
    if not text_content or len(text_content) < 50:
         text_content = article.get('content', '').strip()

    if not text_content:
        logger.warning(f"No content to summarize for article: {article.get('url', 'unknown')}")
        return None

    try:
        prompt = f"""
        You are a senior news analyst. Summarize this text in a clear, factual manner.
        Input Text: {text_content[:4000]}
        
        JSON format:
        {{
            "bullets": ["fact 1", "fact 2", "fact 3", "fact 4", "fact 5"],
            "title_en": "A concise title in English" 
        }}
        
        IMPORTANT: 
        1. Only output valid JSON
        2. Bullet points should be factual, not opinionated
        3. The title should be concise and accurate
        4. Do not include any extra text or explanations
        """
        
        response = client.generate(model=model_name, prompt=prompt, format="json")
        result = json.loads(response['response'])
        
        # Validate the result
        if not result or not isinstance(result, dict):
            logger.warning(f"Invalid summary result from LLM for {article.get('url')}")
            return None
            
        # Validate content quality
        if not result.get("bullets") or not result.get("title_en"):
            logger.warning(f"Incomplete summary result from LLM for {article.get('url')}")
            return None
        
        logger.info(f"Translating summary for: {article.get('url')}")
        hebrew_data = translate_to_hebrew(result.get("bullets", []), result.get("title_en", article.get("title", "")))
        
        final_result = {
            "url": article.get("url", ""),
            "source": article.get("source", "Unknown"),
            "title_en": result.get("title_en", article.get("title")),
            "bullets_en": result.get("bullets", []),
            "title_he": hebrew_data.get("title_he", ""),
            "bullets_he": hebrew_data.get("bullets_he", [])
        }
        
        # Validate final result
        if not validate_summary_content(final_result):
            logger.warning(f"Summary content validation failed for {article.get('url')}")
            return None
            
        return final_result

    except Exception as e:
        logger.exception(f"Error processing {article.get('url')}: {e}")
        return None