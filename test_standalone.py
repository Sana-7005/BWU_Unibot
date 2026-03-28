#!/usr/bin/env python
"""
Quick test to verify chatbot runs without admin panel
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test if all imports work"""
    print("🧪 Testing imports...")
    try:
        from app.llm.gemini_client import ask_gemini, ask_groq_stream
        from app.core.intent import detect_intent
        from app.core.retriever import retrieve
        from app.core.prompt_builder import build_prompt
        print("   ✅ All imports successful")
        return True
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False

def test_env_config():
    """Test environment configuration"""
    print("\n🔑 Testing environment configuration...")
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check Groq API key
    groq_key = os.getenv('GROQ_API_KEY')
    if groq_key:
        print(f"   ✅ GROQ_API_KEY configured ({len(groq_key)} chars)")
    else:
        print("   ❌ GROQ_API_KEY missing")
        return False
    
    # Check admin panel setting
    enable_admin = os.getenv('ENABLE_ADMIN_PANEL', 'false').lower()
    print(f"   ℹ️  ENABLE_ADMIN_PANEL = {enable_admin}")
    
    if enable_admin == 'false':
        print("   ✅ Running in standalone mode (no admin panel dependency)")
    else:
        print("   ⚠️  Admin panel integration enabled")
    
    return True

def test_groq_api():
    """Test Groq API connection"""
    print("\n🤖 Testing Groq API connection...")
    try:
        from app.llm.gemini_client import ask_groq
        
        response = ask_groq("Say 'OK' in one word")
        print(f"   Response: {response[:50]}...")
        
        if "OK" in response.upper() or response.strip():
            print("   ✅ Groq API working")
            return True
        else:
            print("   ⚠️  Unexpected response")
            return False
            
    except Exception as e:
        print(f"   ❌ Groq API error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🔍 STANDALONE CHATBOT TEST")
    print("=" * 60)
    
    results = []
    
    # Test imports
    results.append(("Imports", test_imports()))
    
    # Test environment
    results.append(("Environment", test_env_config()))
    
    # Test Groq API
    results.append(("Groq API", test_groq_api()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:20} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All tests passed! Chatbot ready to run standalone.")
        print("\n💡 Start the server with:")
        print("   python new_app.py")
        print("\n📝 Note: Admin panel is DISABLED by default")
        print("   To enable: Set ENABLE_ADMIN_PANEL=true in .env")
    else:
        print("\n⚠️  Some tests failed. Check the output above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
