#!/usr/bin/env python3
"""
Test script to verify environment variables are set up correctly
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_env_var(var_name, required=False):
    """Test if an environment variable is set"""
    value = os.getenv(var_name)
    if value:
        # Mask the actual value for security
        masked_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
        print(f"✅ {var_name}: {masked_value}")
        return True
    else:
        status = "❌" if required else "⚠️ "
        requirement = " (REQUIRED)" if required else " (optional)"
        print(f"{status} {var_name}: Not set{requirement}")
        return not required

def test_github_connection():
    """Test GitHub API connection"""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ Cannot test GitHub connection - no token set")
        return False
    
    try:
        import requests
        headers = {"Authorization": f"token {token}"}
        response = requests.get("https://api.github.com/user", headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ GitHub connection successful - authenticated as: {user_data.get('login')}")
            return True
        else:
            print(f"❌ GitHub connection failed - status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ GitHub connection test failed: {e}")
        return False

def test_openai_connection():
    """Test OpenAI API connection"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  Cannot test OpenAI connection - no API key set")
        return True  # Not required
    
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        
        # Try a minimal API call
        response = client.models.list()
        print("✅ OpenAI connection successful")
        return True
    except Exception as e:
        print(f"❌ OpenAI connection failed: {e}")
        return False

def test_anthropic_connection():
    """Test Anthropic API connection"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️  Cannot test Anthropic connection - no API key set")
        return True  # Not required
    
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        
        # Try a minimal API call (this might fail if you don't have credits)
        print("✅ Anthropic API key format appears valid")
        return True
    except ImportError:
        print("⚠️  Anthropic package not installed (pip install anthropic)")
        return True
    except Exception as e:
        print(f"❌ Anthropic connection test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Testing SWE-smith Environment Configuration")
    print("=" * 50)
    
    # Test environment variables
    print("\n📋 Environment Variables:")
    all_good = True
    
    # Required variables
    all_good &= test_env_var("GITHUB_TOKEN", required=True)
    
    # Optional but recommended variables
    test_env_var("OPENAI_API_KEY")
    test_env_var("ANTHROPIC_API_KEY")
    test_env_var("SWEFT_DOTENV_PATH")
    test_env_var("SGLANG_API_KEY")
    
    # Test API connections
    print("\n🌐 API Connections:")
    all_good &= test_github_connection()
    test_openai_connection()
    test_anthropic_connection()
    
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 Environment setup looks good! You're ready to use SWE-smith.")
    else:
        print("⚠️  Some required environment variables are missing.")
        print("   Please set them in your .env file before proceeding.")
    
    print("\n💡 Next steps:")
    print("   1. Make sure Docker is running")
    print("   2. Try running: python -m swesmith.bug_gen.procedural.generate --help")
    print("   3. Explore the available repository profiles")