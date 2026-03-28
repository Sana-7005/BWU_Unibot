"""
Test script to verify Groq API integration
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.llm.gemini_client import ask_gemini, ask_groq, ask_groq_stream

def test_non_streaming():
    """Test non-streaming response"""
    print("=" * 60)
    print("Testing Non-Streaming Groq API...")
    print("=" * 60)
    
    prompt = "What is the capital of France? Answer in one sentence."
    response = ask_gemini(prompt)  # Uses Groq now
    
    print(f"Prompt: {prompt}")
    print(f"Response: {response}")
    print()

def test_streaming():
    """Test streaming response"""
    print("=" * 60)
    print("Testing Streaming Groq API...")
    print("=" * 60)
    
    prompt = "Explain what artificial intelligence is in 2 sentences."
    print(f"Prompt: {prompt}")
    print("Response: ", end="", flush=True)
    
    for chunk in ask_groq_stream(prompt):
        print(chunk, end="", flush=True)
    
    print("\n")

def test_direct_groq():
    """Test direct ask_groq function"""
    print("=" * 60)
    print("Testing Direct ask_groq function...")
    print("=" * 60)
    
    prompt = "List 3 programming languages in one line."
    response = ask_groq(prompt)
    
    print(f"Prompt: {prompt}")
    print(f"Response: {response}")
    print()

if __name__ == "__main__":
    print("\n🧪 Groq API Integration Test\n")
    
    try:
        test_non_streaming()
        test_direct_groq()
        test_streaming()
        
        print("=" * 60)
        print("✅ All tests completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
