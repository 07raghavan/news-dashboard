
import os
import sys

try:
    from openai import OpenAI
except ImportError:
    print("❌ 'openai' library not found. Run: pip install openai")
    sys.exit(1)

def test_key():
    print("🔑 OpenAI API Key Helper")
    print("-------------------------")
    # Try to load from environment first
    from dotenv import load_dotenv
    load_dotenv()
    
    env_key = os.getenv("OPENAI_API_KEY")
    api_key = None
    
    if env_key:
        print("ℹ️ Found OPENAI_API_KEY in environment variables.")
        api_key = env_key
    else:
        print("⚠️ No OPENAI_API_KEY found in .env or environment.")
        print("Please paste your OpenAI API Key below and press Enter:")
        try:
            api_key = input().strip()
        except EOFError:
            print("❌ Could not read input.")
            return

    # Clean the key
    clean_key = api_key.strip("'").strip('"')
    
    if not clean_key:
        print("❌ No key provided.")
        return

    print(f"\nTesting key: {clean_key[:8]}...{clean_key[-4:]}")

    try:
        client = OpenAI(api_key=clean_key)
        
        # Simple test call
        print("📡 Connecting to OpenAI...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Use cheaper model for test
            messages=[{"role": "user", "content": "Say 'Success' if you can hear me."}],
            max_tokens=10
        )
        
        msg = response.choices[0].message.content
        print("\n✅ SUCCESS! Connection Established.")
        print(f"🤖 OpenAI Says: {msg}")
        print("\nYour key works properly. Please restart your Streamlit app and try again.")
        
    except Exception as e:
        print("\n❌ FAILED to connect.")
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check if the key is correct.")
        print("2. If it is a 'Project Key', ensure project permissions allow model access.")
        print("3. Check your billing status/credits.")

if __name__ == "__main__":
    test_key()
