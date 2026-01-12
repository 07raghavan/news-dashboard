"""
News Summarizer - Powered by OpenAI GPT-4o
Uses state-of-the-art LLM for comprehensive, high-quality news summarization.
"""

import streamlit as st
import os
from openai import OpenAI
from utils.prompts import SUMMARIZATION_SYSTEM_PROMPT, get_summary_prompt

def get_openai_client():
    """Initialize OpenRouter client"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return None
    
    # Clean the key key just in case
    api_key = api_key.strip().strip("'").strip('"')
    print(f"🔑 Loaded OpenRouter Key: {api_key[:5]}...{api_key[-3:] if len(api_key)>10 else ''}")
    
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

def summarize(text):
    """
    Generates a professional summary using OpenRouter (GPT-4o).
    """
    if not text or len(text.strip()) < 50:
        return "Text too short to summarize."
    
    client = get_openai_client()
    if not client:
        return "⚠️ OpenRouter API Key missing. Please set OPENROUTER_API_KEY in sidebar."
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o", # OpenRouter model ID
            messages=[
                {"role": "system", "content": SUMMARIZATION_SYSTEM_PROMPT},
                {"role": "user", "content": get_summary_prompt(text)}
            ],
            temperature=0.7,
            max_tokens=600,
            extra_headers={
                "HTTP-Referer": "http://localhost:8501", # Required by OpenRouter
                "X-Title": "News Intelligence App",
            }
        )
        
        summary = response.choices[0].message.content.strip()
        return summary
    
    except Exception as e:
        print(f"OpenAI Summarization error: {e}")
        return f"Error using OpenAI: {str(e)}"
