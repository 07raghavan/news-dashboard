"""
Topic Classifier
Enhanced keyword-based classification for news articles.
"""

# Comprehensive keyword lists for each topic
TOPIC_KEYWORDS = {
    "Politics": [
        "president", "election", "congress", "senate", "government", "political", 
        "vote", "campaign", "democrat", "republican", "parliament", "minister",
        "policy", "legislation", "white house", "capitol", "governor", "mayor",
        "biden", "trump", "politics", "politician", "lawmaker", "senate", "house"
    ],
    "Technology": [
        "tech", "technology", "software", "hardware", "ai", "artificial intelligence",
        "computer", "digital", "internet", "app", "smartphone", "iphone", "android",
        "google", "apple", "microsoft", "meta", "facebook", "twitter", "x", "tesla",
        "elon musk", "coding", "programming", "cyber", "data", "cloud", "startup",
        "silicon valley", "innovation", "gadget", "device", "chip", "processor"
    ],
    "Business": [
        "business", "company", "corporate", "ceo", "stock", "market", "economy",
        "financial", "finance", "investment", "revenue", "profit", "earnings",
        "wall street", "nasdaq", "dow", "trade", "commerce", "industry", "merger",
        "acquisition", "startup", "entrepreneur", "investor", "shares", "banking"
    ],
    "Sports": [
        "sport", "sports", "game", "match", "player", "team", "coach", "league",
        "football", "basketball", "baseball", "soccer", "nfl", "nba", "mlb", "nhl",
        "championship", "tournament", "olympic", "athlete", "win", "score", "playoff",
        "cricket", "tennis", "golf", "racing", "boxing", "mma", "ufc", "fifa"
    ],
    "Health": [
        "health", "medical", "doctor", "hospital", "disease", "virus", "vaccine",
        "covid", "pandemic", "medicine", "drug", "treatment", "patient", "healthcare",
        "fda", "cdc", "who", "mental health", "fitness", "wellness", "nutrition",
        "cancer", "diabetes", "heart", "brain", "study", "research", "clinical"
    ]
}

def classify_topic(text):
    """
    Classifies text into one of the predefined topics using keyword matching.
    
    Args:
        text: Article text to classify
        
    Returns:
        dict: Classification result with label, confidence, and all scores
    """
    if not text:
        return {"label": "General", "confidence": 0.0, "all_scores": {}}
    
    text_lower = text.lower()
    
    # Count keyword matches for each topic
    topic_scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        topic_scores[topic] = score
    
    # Get the topic with highest score
    max_score = max(topic_scores.values())
    
    if max_score > 0:
        best_topic = max(topic_scores, key=topic_scores.get)
        confidence = min(max_score / 5.0, 1.0)  # Normalize confidence
        return {
            "label": best_topic,
            "confidence": confidence,
            "all_scores": topic_scores
        }
    
    # Default to General if no keywords match
    return {
        "label": "General",
        "confidence": 0.5,
        "all_scores": topic_scores
    }
