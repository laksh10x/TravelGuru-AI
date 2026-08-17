import requests
import json

def test_chat_endpoint():
    """
    Test the /api/chat endpoint of the server to verify if Gemini API integration is working properly.
    """
    try:
        print("Testing chat endpoint with Gemini API integration...")
        
        # Local server URL (assuming the default Flask port)
        url = "http://localhost:5000/api/chat"
        
        # Generate a random session ID for testing
        import random
        import string
        session_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        
        # Test payload
        payload = {
            "message": "Tell me about Paris, France as a travel destination",
            "sessionId": session_id
        }
        
        # Send POST request to the chat endpoint
        print(f"Sending request to: {url}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, json=payload)
        
        # Check the response
        if response.status_code == 200:
            print("\n✅ Chat endpoint responded with status 200 OK")
            
            # Parse the JSON response
            response_data = response.json()
            
            print("\nAPI Response:")
            print("-" * 50)
            print(f"AI Response snippet: {response_data.get('response', '')[:200]}...")
            print(f"Is Recommendation: {response_data.get('isRecommendation', False)}")
            if response_data.get('recommendationData'):
                print("Recommendation data is included in the response.")
            print("-" * 50)
            
            # Check if there's a meaningful response (more than just error messages)
            if len(response_data.get('response', '')) > 50:
                print("\n✅ SUCCESS: Gemini API integration in the server is working correctly!")
                return True
            else:
                print("\n⚠️ WARNING: API responded but the response seems too short or empty.")
                return False
        else:
            print(f"\n❌ ERROR: Chat endpoint returned status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: Failed to test chat endpoint: {str(e)}")
        return False

if __name__ == "__main__":
    test_chat_endpoint() 