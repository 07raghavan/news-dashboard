
import streamlit as st
import pandas as pd
import altair as alt
from collections import Counter
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from analysis.sentiment_analyzer import analyze_sentiment

st.set_page_config(page_title="News Analytics", page_icon="📊", layout="wide")

st.title("📊 News Intelligence Dashboard")

# Check if articles exist
if 'articles' not in st.session_state or not st.session_state.articles:
    st.info("👋 Go to the **Home** page first to fetch some news!")
    st.stop()

articles = st.session_state.articles

# ----------------- SECTION 1: AI INSIGHTS -----------------
st.subheader("🤖 AI Insights")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🌡️ Global Sentiment Pulse")
    
    if st.button("Run Sentiment Analysis on All Headlines", type="primary"):
        with st.spinner("Analyzing headline sentiment..."):
            total_score = 0
            pos_count = 0
            neg_count = 0
            neu_count = 0
            
            # Analyze titles only (FAST)
            for article in articles:
                # We use the existing local sentiment model on titles
                # It's fast enough for 20-50 titles
                res = analyze_sentiment(article['title'])
                score = res['score']
                label = res['label']
                
                if label == 'POSITIVE':
                    total_score += score
                    pos_count += 1
                elif label == 'NEGATIVE':
                    total_score -= score
                    neg_count += 1
                else:
                    neu_count += 1
            
            # Normalize to -100 to +100
            net_sentiment = 0
            if articles:
                net_sentiment = (total_score / len(articles)) * 100
            
            # Gauge Logic
            color = "gray"
            mood = "Neutral"
            if net_sentiment > 20:
                mood = "Optimistic 🟢"
                color = "green"
            elif net_sentiment < -20:
                mood = "Grim 🔴"
                color = "red"
            
            st.metric("Global Mood", mood, delta=f"{net_sentiment:.1f} Net Score")
            
            # Breakdown
            st.write(f"**Positive:** {pos_count} | **Negative:** {neg_count} | **Neutral:** {neu_count}")
    else:
        st.write("Click button to analyze current news cycle sentiment.")

with col2:
    st.markdown("### ☁️ Trending Keywords")
    
    # Simple extraction
    all_text = " ".join([a['title'] for a in articles])
    ignore = {'the', 'a', 'in', 'to', 'of', 'and', 'is', 'for', 'on', 'with', 'at', 'by', 'an', 'be', 'from', 'as', 'it', 'that', 'this', 'after', 'will', 'says', 'new', 'us', 'are', 'has', 'not'}
    words = [w.strip(".,!?:;\"'").lower() for w in all_text.split()]
    clean_words = [w for w in words if len(w) > 3 and w not in ignore]
    
    # Top 10
    common = Counter(clean_words).most_common(10)
    
    # Display as tags
    tags_html = ""
    for word, count in common:
        size = 10 + (count * 2)
        tags_html += f"<span style='font-size:{size}px; background:#f0f2f6; padding:4px 8px; border-radius:12px; margin:4px; display:inline-block'>#{word} ({count})</span> "
    
    st.markdown(tags_html, unsafe_allow_html=True)


st.divider()

# ----------------- SECTION 2: STATISTICAL METRICS -----------------
st.subheader("📈 Market Statistics")
col3, col4 = st.columns(2)

with col3:
    st.markdown("### 📺 Topic Coverage")
    df_topics = pd.DataFrame([a['topic'] for a in articles], columns=['Topic'])
    topic_counts = df_topics['Topic'].value_counts().reset_index()
    topic_counts.columns = ['Topic', 'Count']
    
    chart_topic = alt.Chart(topic_counts).mark_bar().encode(
        x='Count',
        y=alt.Y('Topic', sort='-x'),
        color='Topic',
        tooltip=['Topic', 'Count']
    ).properties(height=300)
    
    st.altair_chart(chart_topic, use_container_width=True)

with col4:
    st.markdown("### 📢 Top Publishers")
    df_sources = pd.DataFrame([a['source'] for a in articles], columns=['Source'])
    source_counts = df_sources['Source'].value_counts().head(7).reset_index()
    source_counts.columns = ['Source', 'Count']
    
    chart_source = alt.Chart(source_counts).mark_bar(color='#FFA500').encode(
        x='Count',
        y=alt.Y('Source', sort='-x'),
        tooltip=['Source', 'Count']
    ).properties(height=300)
    
    st.altair_chart(chart_source, use_container_width=True)
