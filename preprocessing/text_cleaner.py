import re
import html

def clean_text(text):
    """
    Performs robust preprocessing on news text:
    - Removes HTML tags and entities
    - Removes URLs
    - Normalizes whitespace
    - Removes emojis and excessive special symbols
    - Preserves case and sentence structure for Transformer models
    """
    if not text:
        return ""
        
    # 1. Unescape HTML entities (e.g., &quot; -> ")
    text = html.unescape(text)
    
    # 2. Remove HTML tags (e.g., <div>, <br>)
    text = re.sub(r'<[^>]+>', ' ', text)
    
    # 3. Remove URLs (http, https, www)
    text = re.sub(r'http[s]?://\S+|www\.\S+', '', text)
    
    # 4. Remove emojis and special graphical symbols
    # Keep alphanumeric, whitespace, and standard punctuation (.,!?;:'"()$-%)
    # \w matches unicode word characters (letters, numbers, underscore)
    text = re.sub(r'[^\w\s.,!?;:\'"()\-\$%]', '', text)
    
    # 5. Normalize whitespace (replace multiple spaces/newlines with single space)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
