import google.generativeai as genai
import os
import sys

def test_gemini_api():
    """
    Simple test for the Gemini API to check if it's working properly.
    """
    try:
        # Configure the API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY environment variable is required.")

        genai.configure(api_key=api_key)
        
        # Create a model instance
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Send a simple test prompt
        response = model.generate_content("Please respond with 'Gemini API is working properly!' if you receive this message.")
        
        # Print the response
        print("\nGemini API Response:")
        print("-" * 50)
        print(response.text.strip())
        print("-" * 50)
        
        # Check if the response contains expected text
        if "working" in response.text.lower() and "gemini" in response.text.lower():
            print("\n✅ SUCCESS: Gemini API is working correctly!")
            return True
        else:
            print("\n⚠️ WARNING: Gemini API returned an unexpected response.")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: Gemini API test failed with exception: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Gemini API connection...")
    success = test_gemini_api()
    sys.exit(0 if success else 1) 
