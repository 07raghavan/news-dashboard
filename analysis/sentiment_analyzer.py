"""
Sentiment Analyzer
Analyzes sentiment of news articles using transformers.
Uses @st.cache_resource to avoid re-downloading models.
"""

import streamlit as st
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download VADER lexicon if not present
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

@st.cache_resource
def load_sentiment_model():
    """Load VADER sentiment analyzer"""
    return SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """
    Analyzes sentiment using NLTK VADER (Lightweight).
    Returns label (POSITIVE/NEGATIVE/NEUTRAL) and score.
    """
    if not text or len(text.strip()) < 5:
        return {"label": "NEUTRAL", "score": 0.0}
    
    try:
        sia = load_sentiment_model()
        scores = sia.polarity_scores(text)
        compound = scores['compound']
        
        # Map compound score (-1 to 1) to labels
        if compound >= 0.05:
            label = "POSITIVE"
            score = compound
        elif compound <= -0.05:
            label = "NEGATIVE"
            score = abs(compound)
        else:
            label = "NEUTRAL"
            score = 1.0 - abs(compound) # High confidence in neutrality
            
        return {
            "label": label,
            "score": float(score)
        }
    
    except Exception as e:
        print(f"Sentiment analysis error: {e}")
        return {"label": "ERROR", "score": 0.0}
