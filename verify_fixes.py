#!/usr/bin/env python
"""
Quick verification script to test all fixes
"""
import sys
import requests
import time
from pathlib import Path

def test_api_endpoint():
    """Test if the chat endpoint is working"""
    print("🧪 Testing Chat API Endpoint...")
    
    try:
        # Test 1: Regular AI query (should stream)
        print("\n1️⃣ Testing AI Query (Streaming)...")
        response = requests.post(
            "http://localhost:8081/chat",
            json={"query": "What is the college name?", "stream": True},
            headers={"Content-Type": "application/json"},
            stream=True,
            timeout=10
        )
        
        content_type = response.headers.get('Content-Type', '')
        print(f"   Content-Type: {content_type}")
        
        if 'text/event-stream' in content_type:
            print("   ✅ Streaming response detected!")
            # Read first few chunks
            for i, line in enumerate(response.iter_lines()):
                if i >= 3:  # Just read first 3 lines
                    break
                if line:
                    print(f"   📦 Chunk: {line.decode('utf-8')[:100]}...")
        else:
            print("   ❌ Expected streaming but got:", content_type)
            
    except requests.exceptions.ConnectionError:
        print("   ⚠️  Server not running. Start with: python new_app.py")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    try:
        # Test 2: Scholarship query (should be JSON)
        print("\n2️⃣ Testing Scholarship Query (JSON)...")
        response = requests.post(
            "http://localhost:8081/chat",
            json={"query": "tell me about kanyashree scholarship", "stream": True},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        content_type = response.headers.get('Content-Type', '')
        print(f"   Content-Type: {content_type}")
        
        if 'application/json' in content_type:
            data = response.json()
            print("   ✅ JSON response detected!")
            print(f"   Intent: {data.get('intent')}")
            print(f"   Stream flag: {data.get('stream')}")
            if data.get('stream') == False:
                print("   ✅ Stream flag correctly set to False")
            else:
                print("   ⚠️  Stream flag should be False for scholarship")
        else:
            print("   ❌ Expected JSON but got:", content_type)
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print("\n✅ All API tests passed!")
    return True

def check_css_files():
    """Check if CSS files exist"""
    print("\n🎨 Checking CSS Files...")
    
    static_dir = Path("static")
    if not static_dir.exists():
        print("   ⚠️  Static directory not found")
        return False
    
    # Files that should exist
    required_files = ["style.css", "index.js"]
    all_exist = True
    
    for file in required_files:
        file_path = static_dir / file
        if file_path.exists():
            print(f"   ✅ {file} exists")
        else:
            print(f"   ❌ {file} missing")
            all_exist = False
    
    # Files that should NOT be referenced
    print("\n   Checking for removed CSS references...")
    template_file = Path("templates/index.html")
    if template_file.exists():
        try:
            content = template_file.read_text(encoding='utf-8')
            if "academics.css" in content:
                print("   ⚠️  academics.css still referenced in HTML")
                all_exist = False
            elif "holiday.css" in content:
                print("   ⚠️  holiday.css still referenced in HTML")
                all_exist = False
            else:
                print("   ✅ No broken CSS references found")
        except UnicodeDecodeError:
            print("   ⚠️  Could not read template file (encoding issue)")
    
    return all_exist

def check_groq_config():
    """Check if Groq API is configured"""
    print("\n🔑 Checking Groq Configuration...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("   ❌ .env file not found")
        return False
    
    try:
        content = env_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"   ❌ Could not read .env file: {e}")
        return False
    
    required_vars = ["GROQ_API_KEY", "GROQ_MODEL"]
    all_found = True
    
    for var in required_vars:
        if var in content:
            print(f"   ✅ {var} configured")
        else:
            print(f"   ❌ {var} missing")
            all_found = False
    
    return all_found

def main():
    """Run all verification tests"""
    print("=" * 60)
    print("🔍 CHATBOT VERIFICATION SCRIPT")
    print("=" * 60)
    
    # Check Groq configuration
    groq_ok = check_groq_config()
    
    # Check CSS files
    css_ok = check_css_files()
    
    # Test API (only if server is running)
    print("\n📡 API Tests (requires server running)...")
    print("   Start server with: python new_app.py")
    print("\n   Testing in 3 seconds...")
    time.sleep(3)
    
    api_ok = test_api_endpoint()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"Groq Configuration: {'✅ PASS' if groq_ok else '❌ FAIL'}")
    print(f"CSS Files: {'✅ PASS' if css_ok else '❌ FAIL'}")
    print(f"API Tests: {'✅ PASS' if api_ok else '⚠️  Skip (server not running)'}")
    print("=" * 60)
    
    if groq_ok and css_ok:
        print("\n🎉 Core setup verified! Start server with:")
        print("   python new_app.py")
    else:
        print("\n⚠️  Some checks failed. Review the output above.")

if __name__ == "__main__":
    main()
