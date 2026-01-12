import streamlit as st
import sys
import os
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh
from newspaper import Article as NewsArticle
import pandas as pd
from collections import Counter

# Load environment variables from project root
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

# Ensure the root directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classification.topic_classifier import classify_topic
from analysis.sentiment_analyzer import analyze_sentiment
from analysis.bias_detector import detect_bias
from generation.summarizer import summarize
from preprocessing.text_cleaner import clean_text
from preprocessing.ingestion.news_fetcher import fetch_news, fetch_default_news, search_news_by_query
# Page Config
# Page Config handled by router

# Custom CSS - Modern Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Remove default Streamlit padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Search Container */
    .search-container {
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
        border: 1px solid #e5e7eb;
    }
    
    /* Fix input and button heights - STRICT ENFORCEMENT */
    .stTextInput > div > div > input {
        min-height: 48px !important;
        height: 48px !important;
        line-height: 48px !important;
        font-size: 1rem !important;
        padding: 0 1rem !important;
        border-radius: 8px !important;
        border: 1.5px solid #d1d5db !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Primary buttons (Search) */
    .stButton > button[kind="primary"] {
        min-height: 48px !important;
        height: 48px !important;
        line-height: 48px !important;
        background: linear-gradient(135deg, #3b82f6 0%, #1e3a8a 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0 2rem !important;
        transition: all 0.3s ease !important;
        margin-top: 0px !important; /* Align with input */
    }
    
    /* Carousel Arrow Buttons (Secondary) - Target default buttons */
    .stButton > button:not([kind="primary"]) {
        height: 36px !important;
        min-height: 36px !important;
        max-height: 36px !important;
        padding: 0 0.5rem !important;
        border: none !important;
        background: transparent !important;
        color: #6b7280 !important;
        font-size: 1.2rem !important;
        line-height: 36px !important;
        margin: 0 !important;
        vertical-align: middle !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* Force all carousel control columns to align */
    div[data-testid="column"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 36px !important;
    }
    
    /* Dots container alignment */
    .stMarkdown p {
        margin: 0 !important;
        padding: 0 !important;
        line-height: 36px !important;
    }
    
    /* Carousel Styles */
    .carousel-container {
        position: relative;
        width: 100%;
        height: 450px;
        border-radius: 16px;
        overflow: hidden;
        margin-bottom: 2rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }
    
    .carousel-slide:hover {
        transform: scale(1.02);
    }
    
    .carousel-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .carousel-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(to top, rgba(0,0,0,0.85), transparent);
        padding: 2rem;
        color: white;
    }
    
    .carousel-headline {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.3;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    .carousel-meta {
        font-size: 0.875rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Topic Badges */
    .topic-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    
    .badge-politics { background: #FEE2E2; color: #991B1B; }
    .badge-technology { background: #DBEAFE; color: #1E40AF; }
    .badge-business { background: #D1FAE5; color: #065F46; }
    .badge-sports { background: #FEF3C7; color: #92400E; }
    .badge-health { background: #FCE7F3; color: #9F1239; }
    .badge-general { background: #E5E7EB; color: #374151; }
    
    /* Article Cards */
    .article-card {
        background: white;
        padding: 1.25rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 1.25rem;
        border: 1px solid #f3f4f6;
        transition: all 0.2s ease;
    }
    
    .article-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .stImage > img {
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .article-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #111827;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    
    .article-meta {
        color: #6B7280;
        font-size: 0.875rem;
        margin-bottom: 0.75rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        margin-bottom: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        background-color: #f9fafb;
        border-radius: 8px;
        padding: 0 20px;
        font-weight: 500;
        color: #6b7280;
        border: 1px solid #e5e7eb;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #1e3a8a 100%);
        color: white;
        border-color: transparent;
    }
    
    /* Result boxes */
    .result-box {
        background: #f9fafb;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
        border-left: 3px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'articles' not in st.session_state:
    st.session_state.articles = []
if 'newsapi_key' not in st.session_state:
    st.session_state.newsapi_key = os.getenv('NEWSAPI_KEY', '')
if 'auto_loaded' not in st.session_state:
    st.session_state.auto_loaded = False
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'home'  # 'home' or 'article'
if 'selected_article' not in st.session_state:
    st.session_state.selected_article = None
if 'num_articles' not in st.session_state:
    st.session_state.num_articles = 50

# Sidebar
with st.sidebar:
    # About Section (Now at Top)
    st.image("https://cdn-icons-png.flaticon.com/512/2965/2965879.png", width=80)
    st.title("About")
    st.markdown("""
    This dashboard uses transformer models to analyze news articles.
    
    **Models Used:**
    - **Topic**: Keyword Analysis
    - **Summarization**: OpenRouter (GPT-4o)
    - **Bias**: OpenRouter (GPT-4o)
    - **Sentiment**: DistilBERT (HuggingFace)
    
    **Features:**
    - Auto-fetch latest news
    - Topic categorization
    - On-demand analysis
    - Streamlit Analytics Dashboard
    """)
    
    st.markdown("---")
    
    # Settings Section (Now at Bottom)
    st.title("Settings")
    st.markdown("### 🔑 API Configuration")
    api_key_input = st.text_input(
        "NewsAPI Key", 
        type="password", 
        value=st.session_state.newsapi_key,
        help="Get your free API key from newsapi.org"
    )
    if api_key_input:
        st.session_state.newsapi_key = api_key_input

    openrouter_key_input = st.text_input(
        "OpenRouter API Key (Required)",
        type="password",
        value=os.getenv("OPENROUTER_API_KEY", ""),
        help="Get your key at openrouter.ai. Required for AI features."
    )
    if openrouter_key_input:
        os.environ["OPENROUTER_API_KEY"] = openrouter_key_input
    
    st.markdown("### ⚙️ Search Settings")
    st.session_state.num_articles = st.slider(
        "Number of Articles",
        min_value=5,
        max_value=50,
        value=50,
        step=5,
        help="How many articles to fetch per search"
    )
    
    if st.session_state.articles:
        st.markdown("---")
        st.metric("Total Articles", len(st.session_state.articles))
    
# Check for keys
if not st.session_state.newsapi_key:
    st.warning("⚠️ **Unlock the Dashboard:** Please enter your **NewsAPI Key** in the sidebar settings.", icon="🔑")

# SEARCH BAR - Properly Aligned
# Container removed to fix layout issues
col1, col2 = st.columns([6, 1])

with col1:
    search_query = st.text_input(
        "Search",
        placeholder="Search for news topics...",
        label_visibility="collapsed",
        key="search_input"
    )

with col2:
    # Button text changed to "Search" (no emoji)
    search_btn = st.button("Search", use_container_width=True, type="primary")

# Auto-load default news on first load (Logic moved before Search Handling)
if not st.session_state.auto_loaded and st.session_state.newsapi_key:
    with st.spinner("Loading top headlines..."):
        refresh_articles = fetch_default_news(api_key=st.session_state.newsapi_key)
        if refresh_articles:
            st.session_state.articles = refresh_articles
            st.session_state.auto_loaded = True
        else:
             st.error("❌ Failed to load news. Check your API Key or connection.")

# Handle search button
if search_btn:
    if not st.session_state.newsapi_key:
        st.error("⚠️ Please enter your NewsAPI key in the sidebar. Get one free at https://newsapi.org")
    elif not search_query:
        st.warning("⚠️ Please enter a search query")
    else:
        with st.spinner(f"Fetching news about '{search_query}'..."):
            try:
                results = search_news_by_query(
                    query=search_query,
                    api_key=st.session_state.newsapi_key,
                    page_size=st.session_state.num_articles
                )
                
                if not results:
                    st.warning(f"No articles found for '{search_query}'. This topic might not be in the top headlines right now.")
                else:
                    st.session_state.articles = results
                    # Reset carousel
                    if 'carousel_index' in st.session_state:
                        st.session_state.carousel_index = 0
                    st.rerun()
            except Exception as e:
                st.error(f"❌ {str(e)}")


# Check if we're viewing an article detail page
if st.session_state.current_view == 'article' and st.session_state.selected_article:
    # Back button
    if st.button("← Back to News Feed", type="secondary"):
        st.session_state.current_view = 'home'
        st.session_state.selected_article = None
        st.rerun()
    
    article = st.session_state.selected_article
    
    # Article Detail Page
    st.markdown("---")
    
    # Full-width image
    if article.get('image_url'):
        st.image(article['image_url'], width='stretch')
    
    # Title and metadata
    topic_class = article.get('topic', 'general').lower()
    st.markdown(f"""
    <div style="margin-top: 1.5rem;">
        <h1 style="font-size: 2rem; font-weight: 700; color: #1F2937; margin-bottom: 1rem;">
            {article['title']}
        </h1>
        <div style="display: flex; gap: 1rem; align-items: center; margin-bottom: 1.5rem;">
            <span class="topic-badge badge-{topic_class}">{article['topic']}</span>
            <span style="color: #6B7280;">{article['source']} • {article['published_at'][:10] if article['published_at'] else 'Recently'}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch full article BEFORE displaying anything
    article_text = article.get('content') or article.get('description') or ''
    article_text = article_text.replace('[+', '').replace(' chars]', '').strip()
    
    # Try to fetch full article from source if content is truncated
    if len(article_text) < 500 or '[+' in str(article.get('content', '')):
        try:
            with st.spinner("Loading full article..."):
                news_article = NewsArticle(article['url'])
                news_article.download()
                news_article.parse()
                if news_article.text and len(news_article.text) > len(article_text):
                    # Clean the scraped text
                    full_text = news_article.text
                    
                    # Remove common junk patterns
                    junk_patterns = [
                        'Share', 'Save', 'Getty Images', 'Share Save',
                        'Related Topics', 'More on this story',
                        'Sign up for', 'Subscribe to', 'Follow us on'
                    ]
                    
                    # Split into lines and filter
                    lines = full_text.split('\n')
                    cleaned_lines = []
                    
                    for line in lines:
                        line = line.strip()
                        # Skip empty lines
                        if not line:
                            continue
                        # Skip lines that are just junk
                        if any(junk in line for junk in junk_patterns) and len(line) < 50:
                            continue
                        # Skip very short lines at the start (likely metadata)
                        if len(cleaned_lines) < 3 and len(line) < 30:
                            continue
                        cleaned_lines.append(line)
                    
                    article_text = '\n\n'.join(cleaned_lines)
                    
                    # UPDATE: Store the full text in the article object for analysis
                    article['content'] = article_text
                    st.session_state.selected_article['content'] = article_text
        except Exception as e:
            st.warning(f"⚠️ Could not fetch full article. Showing available preview.")
    
    # Now display the article (either full or preview)
    st.markdown(f"""
    <div style="font-size: 1.1rem; line-height: 1.8; color: #374151; margin-bottom: 2rem; white-space: pre-wrap;">
        {article_text}
    </div>
    """, unsafe_allow_html=True)
    
    
    # Analysis buttons
    st.markdown("### AI Analysis")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Summarize", key="detail_summarize", width='stretch', type="primary"):
            with st.spinner("Generating summary..."):
                # Preprocess text before analysis
                clean_content = clean_text(article['content'])
                article['summary'] = summarize(clean_content)
                st.session_state.selected_article = article
    
    with col2:
        if st.button("Sentiment Analysis", key="detail_sentiment", width='stretch', type="primary"):
            with st.spinner("Analyzing sentiment..."):
                clean_content = clean_text(article['content'])
                article['sentiment'] = analyze_sentiment(clean_content)
                st.session_state.selected_article = article
    
    with col3:
        if st.button("Bias Detection", key="detail_bias", width='stretch', type="primary"):
            with st.spinner("Detecting bias..."):
                # Pass article topic for hybrid bias detection
                article_topic = article.get('topic', 'General')
                clean_content = clean_text(article['content'])
                article['bias'] = detect_bias(clean_content, article_topic)
                st.session_state.selected_article = article
    
    # Display results
    if article.get('summary'):
        st.markdown("#### Summary")
        st.info(article['summary'])
    
    if article.get('sentiment'):
        st.markdown("#### Sentiment")
        sentiment_label = article['sentiment'].get('label', 'Unknown')
        sentiment_score = article['sentiment'].get('score', 0)
        st.success(f"**{sentiment_label}** (Confidence: {sentiment_score:.2%})")
    
    
    if article.get('bias'):
        st.markdown("#### Bias Analysis")
        bias_data = article['bias']
        
        # Handle both old (string) and new (dict) formats
        if isinstance(bias_data, dict):
            bias_label = bias_data.get('label', 'Unknown')
            bias_analysis = bias_data.get('analysis', '')
            st.warning(f"**{bias_label}**")
            if bias_analysis:
                st.write(bias_analysis)
        else:
            # Old string format
            st.warning("**Bias Detected**")
            st.write(str(bias_data))
    
    # Source link
    st.markdown("---")
    st.markdown(f"[📰 Read full article on {article['source']}]({article['url']})", unsafe_allow_html=True)
    
    # Stop here - don't show the main feed
    st.stop()

# HOME VIEW - Continue with normal feed
# Auto-Carousel for Top News (SHOW IMMEDIATELY)
if st.session_state.articles and len(st.session_state.articles) > 0:
    # Get top 5 articles with images AND content for carousel
    carousel_articles = [
        a for a in st.session_state.articles 
        if a.get('image_url') and (a.get('description') or a.get('content'))
    ][:5]
    
    if carousel_articles:
        # Initialize carousel index
        if 'carousel_index' not in st.session_state:
            st.session_state.carousel_index = 0
        
        # Auto-refresh every 5 seconds ONLY for carousel
        count = st_autorefresh(interval=5000, key="carousel_refresh")
        
        # Advance carousel on each refresh
        if count > 0:
            st.session_state.carousel_index = (st.session_state.carousel_index + 1) % len(carousel_articles)
        
        current_article = carousel_articles[st.session_state.carousel_index]
        
        # Carousel Display
        st.markdown(f"""
        <div class="carousel-container" onclick="window.open('{current_article['url']}', '_blank')">
            <img src="{current_article['image_url']}" class="carousel-image" alt="News image">
            <div class="carousel-overlay">
                <h2 class="carousel-headline">{current_article['title']}</h2>
                <div class="carousel-meta">
                    <span class="topic-badge badge-{current_article['topic'].lower()}">{current_article['topic']}</span>
                    {current_article['source']} • {current_article['published_at'][:10] if current_article['published_at'] else 'Recently'}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Carousel controls: Only arrows, no dots
        # Layout: [Spacer, Left Arrow, Spacer, Right Arrow, Spacer]
        c1, c2, c3, c4, c5 = st.columns([3, 0.5, 1, 0.5, 3])
        
        with c2:
            if st.button("◀", key="carousel_prev", type="secondary"):
                st.session_state.carousel_index = (st.session_state.carousel_index - 1) % len(carousel_articles)
                st.rerun()
        
        with c4:
            if st.button("▶", key="carousel_next", type="secondary"):
                st.session_state.carousel_index = (st.session_state.carousel_index + 1) % len(carousel_articles)
                st.rerun()



# Display articles
if st.session_state.articles:
    # Topic filter tabs
    topics = ["All", "Politics", "Technology", "Business", "Sports", "Health", "General"]
    topic_counts = {topic: 0 for topic in topics[1:]}
    topic_counts["All"] = len(st.session_state.articles)
   
    for article in st.session_state.articles:
        topic = article.get('topic', 'General')
        if topic in topic_counts:
            topic_counts[topic] += 1
    
    tab_labels = [f"{topic} ({topic_counts.get(topic, 0)})" for topic in topics]
    tabs = st.tabs(tab_labels)
    
    for tab_idx, topic in enumerate(topics):
        with tabs[tab_idx]:
            # Filter out articles with no description/content
            filtered_articles = st.session_state.articles if topic == "All" else [
                a for a in st.session_state.articles if a.get('topic') == topic
            ]
            
            # Remove articles with no meaningful content
            filtered_articles = [
                a for a in filtered_articles 
                if a.get('description') or a.get('content')
            ]
            
            if not filtered_articles:
                st.info(f"No articles in {topic} category")
            else:
                for art_idx, article in enumerate(filtered_articles):
                    article_id = article['id']
                    topic_class = article.get('topic', 'general').lower()
                    
                    # Create unique key with tab and article index
                    unique_key = f"{tab_idx}_{art_idx}_{article_id}"
                    
                    # Article Card with Image
                    image_url = article.get('image_url', '')
                    
                    # Create columns for image and content
                    if image_url:
                        # Two-column layout: image on left, content on right
                        img_col, content_col = st.columns([1, 2])
                        
                        with img_col:
                            st.image(image_url, width='stretch')
                        
                        with content_col:
                            # Get preview (first 200 chars)
                            article_text = article.get('content') or article.get('description') or ''
                            article_text = article_text.replace('[+', '').replace(' chars]', '').strip()
                            preview_text = article_text[:200] + "..." if len(article_text) > 200 else article_text
                            
                            st.markdown(f"""
                            <div class="article-title">{article['title']}</div>
                            <div class="article-meta">
                                <span class="topic-badge badge-{topic_class}">{article['topic']}</span>
                                {article['source']} • {article['published_at'][:10] if article['published_at'] else 'Recently'}
                            </div>
                            <p style="color: #6B7280; line-height: 1.6; margin-top: 0.5rem;">
                                {preview_text}
                            </p>
                            """, unsafe_allow_html=True)
                            
                            # Read More button
                            if st.button("Read More", key=f"read_{unique_key}", type="primary"):
                                st.session_state.current_view = 'article'
                                st.session_state.selected_article = article
                                st.rerun()
                    else:
                        # No image - full width content
                        article_text = article.get('content') or article.get('description') or ''
                        article_text = article_text.replace('[+', '').replace(' chars]', '').strip()
                        preview_text = article_text[:200] + "..." if len(article_text) > 200 else article_text
                        
                        st.markdown(f"""
                        <div class="article-card">
                            <div class="article-title">{article['title']}</div>
                            <div class="article-meta">
                                <span class="topic-badge badge-{topic_class}">{article['topic']}</span>
                                {article['source']} • {article['published_at'][:10] if article['published_at'] else 'Recently'}
                            </div>
                            <p>{preview_text}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Read More button
                        if st.button("Read More", key=f"read_{unique_key}", type="primary"):
                            st.session_state.current_view = 'article'
                            st.session_state.selected_article = article
                            st.rerun()
                    
                    st.markdown("---")

else:
    # Empty state
    if not st.session_state.newsapi_key:
        st.info("👋 Welcome! Enter your NewsAPI key in the **sidebar** to get started. Get a free key at https://newsapi.org")
    else:
        st.info("🔍 Enter a search query above to find news articles, or we'll load default India news automatically!")
