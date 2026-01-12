
import os
import sys

try:
    from openai import OpenAI
except ImportError:
    print("❌ 'openai' library not found. Run: pip install openai")
    sys.exit(1)

# The key provided by user
PROVIDED_KEY = "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"

def test_openrouter():
    print("🚀 OpenRouter API Test")
    print("----------------------")
    
    # Use provided key or fall back to env
    api_key = PROVIDED_KEY
    if not api_key:
        api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        print("❌ No API Key found.")
        return

    print(f"🔑 Testing Key: {api_key[:10]}...{api_key[-4:]}")
    print(f"🔗 Target: https://openrouter.ai/api/v1")

    try:
        # Configure client for OpenRouter
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        print("📡 Connecting to OpenRouter...")
        
        # We use a reliable model alias. 'openai/gpt-3.5-turbo' is usually available.
        # correctly routed by OpenRouter.
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo", 
            messages=[{"role": "user", "content": "Reply with 'OpenRouter is working!'"}],
            max_tokens=20,
            # OpenRouter specific headers (optional but good practice)
            extra_headers={
                "HTTP-Referer": "http://localhost:8501", # Site URL
                "X-Title": "News AI Tester", # Site Title
            },
        )
        
        msg = response.choices[0].message.content
        print("\n✅ SUCCESS! Connection Established.")
        print(f"🤖 Response: {msg}")
        
    except Exception as e:
        print("\n❌ FAILED to connect.")
        print(f"Error: {e}")

if __name__ == "__main__":
    test_openrouter()
