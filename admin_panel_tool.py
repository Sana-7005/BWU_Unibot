#!/usr/bin/env python
"""
Check and manage admin panel configuration
"""
import os
from pathlib import Path
from dotenv import load_dotenv

def check_env_config():
    """Check current environment configuration"""
    print("🔍 Checking Environment Configuration")
    print("=" * 60)
    
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        return
    
    load_dotenv()
    
    # Admin panel settings
    enable_admin = os.getenv('ENABLE_ADMIN_PANEL', 'false').lower()
    admin_url = os.getenv('ADMIN_PANEL_URL', 'http://localhost:8000')
    timeout = os.getenv('ADMIN_PANEL_TIMEOUT', '2')
    
    print(f"\n📋 Current Settings:")
    print(f"   ENABLE_ADMIN_PANEL: {enable_admin}")
    print(f"   ADMIN_PANEL_URL: {admin_url}")
    print(f"   ADMIN_PANEL_TIMEOUT: {timeout}s")
    
    print(f"\n📊 Status:")
    if enable_admin == 'true':
        print("   ✅ Admin panel integration ENABLED")
        print("   ⚠️  Chatbot will try to connect to admin panel")
        print(f"   📍 Expected admin panel at: {admin_url}")
    else:
        print("   ✅ Admin panel integration DISABLED")
        print("   🚀 Chatbot running in standalone mode")
        print("   💡 No admin panel dependency")
    
    # Groq settings
    print(f"\n🤖 Groq API Configuration:")
    groq_key = os.getenv('GROQ_API_KEY', '')
    groq_model = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
    
    if groq_key:
        print(f"   ✅ API Key: {'*' * 20}...{groq_key[-6:]}")
        print(f"   ✅ Model: {groq_model}")
    else:
        print(f"   ❌ API Key: NOT SET")

def toggle_admin_panel():
    """Toggle admin panel on/off"""
    print("\n🔧 Admin Panel Toggle")
    print("=" * 60)
    
    load_dotenv()
    current = os.getenv('ENABLE_ADMIN_PANEL', 'false').lower()
    
    print(f"\nCurrent state: {current.upper()}")
    print("\nOptions:")
    print("  1. Enable admin panel")
    print("  2. Disable admin panel (standalone)")
    print("  3. Cancel")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    env_file = Path(".env")
    content = env_file.read_text()
    
    if choice == '1':
        new_content = content.replace(
            'ENABLE_ADMIN_PANEL=false',
            'ENABLE_ADMIN_PANEL=true'
        )
        env_file.write_text(new_content)
        print("\n✅ Admin panel ENABLED")
        print("📝 Remember to start admin panel server:")
        print("   cd admin && python app.py")
        
    elif choice == '2':
        new_content = content.replace(
            'ENABLE_ADMIN_PANEL=true',
            'ENABLE_ADMIN_PANEL=false'
        )
        env_file.write_text(new_content)
        print("\n✅ Admin panel DISABLED")
        print("🚀 Chatbot will run standalone")
        
    else:
        print("\n❌ Cancelled")

def check_admin_panel():
    """Check if admin panel is running"""
    print("\n📡 Checking Admin Panel Server")
    print("=" * 60)
    
    load_dotenv()
    admin_url = os.getenv('ADMIN_PANEL_URL', 'http://localhost:8000')
    
    try:
        import requests
        print(f"Attempting to connect to: {admin_url}")
        
        response = requests.get(f"{admin_url}/api/chatbot/settings", timeout=2)
        
        if response.status_code == 200:
            print(f"\n✅ Admin panel is RUNNING")
            print(f"   URL: {admin_url}")
            print(f"   Status: {response.status_code}")
            
            data = response.json()
            if data.get('success'):
                settings = data.get('data', {})
                print(f"\n⚙️  Current Settings:")
                print(f"   Chatbot Enabled: {settings.get('enabled', True)}")
                print(f"   Maintenance Mode: {settings.get('maintenance_mode', False)}")
        else:
            print(f"\n⚠️  Admin panel responded but with status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Admin panel is NOT RUNNING")
        print(f"   Cannot connect to: {admin_url}")
        print(f"\n💡 To start admin panel:")
        print(f"   cd admin")
        print(f"   python app.py")
        
    except Exception as e:
        print(f"\n❌ Error checking admin panel: {e}")

def main():
    """Main menu"""
    print("=" * 60)
    print("🔧 ADMIN PANEL CONFIGURATION TOOL")
    print("=" * 60)
    
    while True:
        print("\n📋 Menu:")
        print("  1. Check current configuration")
        print("  2. Toggle admin panel on/off")
        print("  3. Check if admin panel is running")
        print("  4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            check_env_config()
        elif choice == '2':
            toggle_admin_panel()
        elif choice == '3':
            check_admin_panel()
        elif choice == '4':
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
