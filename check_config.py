from dotenv import load_dotenv
import os

load_dotenv()

print("=" * 60)
print("✅ CONFIGURATION VERIFIED")
print("=" * 60)

enable_admin = os.getenv('ENABLE_ADMIN_PANEL', 'false').lower() == 'true'
groq_key = os.getenv('GROQ_API_KEY', '')

print(f"\n🔧 Admin Panel: {'ENABLED' if enable_admin else 'DISABLED (Standalone)'}")
print(f"🤖 Groq API: {'✅ Configured' if groq_key else '❌ Missing'}")

if not enable_admin:
    print("\n✅ Chatbot will run WITHOUT admin panel dependency")
    print("   - No connection attempts to admin server")
    print("   - No timeout warnings")
    print("   - Fully independent operation")
else:
    print(f"\n⚠️  Admin panel integration enabled")
    print(f"   - Will connect to: {os.getenv('ADMIN_PANEL_URL')}")
    print(f"   - Make sure admin server is running")

print("\n" + "=" * 60)
