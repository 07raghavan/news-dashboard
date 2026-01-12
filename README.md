# AI News Intelligence Dashboard

This project is an AI-powered News Intelligence Dashboard that analyzes news articles to extract summaries, topics, sentiment, and potential bias using Hugging Face Transformers and Streamlit.

## Features
- **Topic Classification**: Categorizes news into Politics, Technology, Business, Sports, or Health (Zero-Shot).
- **Summarization**: Generates concise executive summaries using BART.
- **Sentiment Analysis**: Determines if the news is Positive, Negative, or Neutral with intensity scoring.
- **Bias Detection**: Uses Flan-T5 Reasoning to analyze political leaning, tone, and loaded language.
- **NewsAPI Integration**: Optional built-in news fetching.

## Setup Instructions

### Step 1: Create Virtual Environment

It is **highly recommended** to use a virtual environment to avoid dependency conflicts.

**For Windows:**
```bash
python -m venv genai_env
genai_env\Scripts\activate
```

**For Linux/Mac:**
```bash
python -m venv genai_env
source genai_env/bin/activate
```

### Step 2: Install Dependencies

Once the virtual environment is activated, install all required packages:

```bash
pip install transformers streamlit pandas nltk torch requests plotly numpy
```

**OR** use the requirements file:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

Run the Streamlit app from the project root directory:

```bash
streamlit run app/streamlit_app.py
```

The dashboard will open automatically in your default browser at `http://localhost:8501`

### Step 4 (Optional): Deactivate Virtual Environment

When you're done working, deactivate the virtual environment:

```bash
deactivate
```

### Verification (Optional but Recommended)

After installing dependencies, verify your setup by running:

```bash
python verify_setup.py
```

This will check that all required packages are installed correctly.

## Quick Start Example

Once the app is running, you can test it with this sample news article:

```
Breaking News: Tech Giant Unveils Revolutionary AI Assistant

In a groundbreaking announcement today, a leading technology company revealed its latest artificial intelligence assistant, promising to transform how people interact with technology. The new AI system, powered by advanced machine learning algorithms, can understand context, learn from interactions, and provide personalized responses across multiple languages.

Industry experts have praised the innovation, noting its potential impact on productivity and accessibility. However, privacy advocates have raised concerns about data collection practices. The company maintains that user privacy is a top priority and that all data is encrypted and anonymized.

The AI assistant will be available to consumers starting next month, with enterprise solutions rolling out later this year.
```

Try pasting this into the dashboard to see all features in action!

## Project Structure
- `app/`: Contains the Streamlit user interface.
- `classification/`: Topic classification logic.
- `analysis/`: Sentiment and bias analysis modules.
- `generation/`: Summarization logic using Transformers.
- `preprocessing/`: Text cleaning and NewsAPI ingestion.
