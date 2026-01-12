"""
Bias Detector - HYBRID VERSION
- Politics articles: Uses specialized political bias classifier (DistilRoBERTa)
- Other topics: Uses OpenAI GPT-4o for comprehensive analysis
"""

import streamlit as st
import os
# from transformers import pipeline (Removed)
from openai import OpenAI
from utils.prompts import BIAS_SYSTEM_PROMPT, get_bias_prompt

def get_openai_client():
    """Initialize OpenRouter client"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return None
    api_key = api_key.strip().strip("'").strip('"')
    print(f"🔑 Loaded OpenRouter Key (Bias): {api_key[:5]}...")
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )




def detect_bias(text, article_topic="General"):
    """
    Detect bias using OpenRouter GPT-4o for ALL topics.
    Unified approach provides consistent, deep analysis.
    """
    if not text or len(text.strip()) < 20:
        return {
            "label": "Insufficient Text",
            "confidence": 0.0,
            "analysis": "Text too short for bias analysis."
        }
    
    # Unified Path: Use GPT-4o for everything
    return _detect_comprehensive_bias(text)

# Removed _detect_political_bias (legacy local model)

def _detect_comprehensive_bias(text):
    """Comprehensive bias analysis using OpenRouter GPT-4o"""
    client = get_openai_client()
    if not client:
        return {"label": "Config Error", "confidence": 0.0, "analysis": "OpenRouter Key missing."}
        
    try:
        # OpenRouter Prompt for detailed bias check
        response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": BIAS_SYSTEM_PROMPT},
                {"role": "user", "content": get_bias_prompt(text)}
            ],
            temperature=0.3, # Low temp for consistency
            max_tokens=400,
            extra_headers={
                "HTTP-Referer": "http://localhost:8501", 
                "X-Title": "News Intelligence App",
            }
        )
        
        content = response.choices[0].message.content.strip()
        
        # naive parsing
        label = "Bias Detected"
        if "Label:" in content:
            try:
                # Extract explicitly labeled bias
                label_line = [line for line in content.split('\n') if 'Label:' in line][0]
                label = label_line.split("Label:")[1].strip()
            except:
                pass
        
        return {
            "label": label,
            "confidence": 0.95, # OpenAI is generally high confidence
            "analysis": content.replace("Label:", "").replace("Analysis:", "").strip()
        }

    except Exception as e:
        return {
            "label": "Error", 
            "confidence": 0.0, 
            "analysis": f"OpenAI Error: {str(e)}"
        }

        
        # Fallback
        return {
            "label": "Analysis Incomplete",
            "confidence": 0.0,
            "analysis": "Unable to generate complete bias analysis. Try again or check article length."
        }
    
    except Exception as e:
        print(f"Comprehensive bias analysis error: {e}")
        return {
            "label": "Error",
            "confidence": 0.0,
            "analysis": f"Error: {str(e)}"
        }
