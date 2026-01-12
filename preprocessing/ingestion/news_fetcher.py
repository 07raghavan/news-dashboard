"""
Enhanced News Fetcher with Auto-Classification
Fetches news from NewsAPI using the official library
"""

from newsapi import NewsApiClient
import pandas as pd
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from classification.topic_classifier import classify_topic

__all__ = ['fetch_news', 'fetch_default_news', 'search_news_by_query']

def fetch_news(query="India", api_key=None, language='en', page_size=20):
    """
    Fetches news articles using NewsAPI 'everything' endpoint.
    """
    if not api_key:
        print("⚠️ No API key provided!")
        return []
    
    api_key = str(api_key).strip().strip('"').strip("'")
    
    try:
        newsapi = NewsApiClient(api_key=api_key)
        
        # Use 'everything' endpoint
        response = newsapi.get_everything(
            q=query,
            language=language,
            page_size=min(page_size, 100),
            sort_by='relevancy'
        )
        
        if response.get('status') != 'ok':
            print(f"NewsAPI Error: {response.get('message', 'Unknown error')}")
            return []
            
        return _process_articles(response.get('articles', []))
        
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def search_news_by_query(query, api_key=None, language='en', page_size=20):
    """
    Dedicated search function using the 'everything' endpoint.
    """
    return fetch_news(query, api_key, language, page_size)

def fetch_default_news(api_key=None):
    """
    Fetches default news (India Headlines) with fallback.
    """
    if not api_key:
        print("⚠️ No API key provided for default news!")
        return []
    
    api_key = str(api_key).strip().strip('"').strip("'")
    print(f"🔑 Using API key: {api_key[:10]}...")
    
    try:
        newsapi = NewsApiClient(api_key=api_key)
        
        # Attempt 1: Top Headlines (India)
        response = newsapi.get_top_headlines(
            country='in',
            language='en',
            page_size=50
        )
        
        articles = response.get('articles', [])
        
        # Attempt 2: Fallback to Everything (India Query)
        if not articles:
            print("⚠️ Top headlines empty, falling back to Everything endpoint...")
            response = newsapi.get_everything(
                q='India',
                language='en',
                page_size=50,
                sort_by='publishedAt'
            )
            articles = response.get('articles', [])
            
        return _process_articles(articles)
    
    except Exception as e:
        print(f"Error fetching default news: {e}")
        return []

def _process_articles(articles):
    """Helper to process raw articles into our format"""
    if not articles:
        return []
        
    enriched_articles = []
    for idx, article in enumerate(articles):
        full_text = article.get('content') or article.get('description') or ''
        # Auto-classify topic
        topic_result = classify_topic(article.get('title', '') + ' ' + full_text)
        
        enriched_article = {
            'id': f"article_{idx}_{datetime.now().timestamp()}",
            'title': article.get('title', 'No Title'),
            'description': article.get('description', ''),
            'content': full_text,
            'url': article.get('url', ''),
            'source': article.get('source', {}).get('name', 'Unknown'),
            'published_at': article.get('publishedAt', ''),
            'image_url': article.get('urlToImage', ''),
            'topic': topic_result.get('label', 'General'),
            'summary': None,
            'sentiment': None,
            'bias': None
        }
        enriched_articles.append(enriched_article)
    
    return enriched_articles
