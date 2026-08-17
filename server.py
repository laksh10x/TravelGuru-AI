from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import json
import os
import shutil
from main import search_google_flights, search_google_hotels, process_user_selection, generate_itinerary

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# Function to copy JSON files to src/pages directory
def copy_json_files():
    """
    Copy the test.json, test_flight.json, and itinerary.json files to the src/pages directory
    """
    try:
        # Get current directory
        current_dir = os.getcwd()
        print(f"Current directory: {current_dir}")
        
        # Define source and destination paths
        src_files = ['test.json', 'test_flight.json', 'itinerary.json']
        dest_dir = os.path.join(current_dir, 'src', 'pages')
        
        print(f"Destination directory: {dest_dir}")
        
        # Check if destination directory exists
        if not os.path.exists(dest_dir):
            print(f"Creating directory: {dest_dir}")
            os.makedirs(dest_dir, exist_ok=True)
        
        # Copy files
        for file in src_files:
            src_path = os.path.join(current_dir, file)
            dest_path = os.path.join(dest_dir, file)
            
            if os.path.exists(src_path):
                print(f"Copying {src_path} to {dest_path}")
                shutil.copy2(src_path, dest_path)
                print(f"File copied successfully: {os.path.getsize(dest_path)} bytes")
            else:
                print(f"Source file does not exist: {src_path}")
        
        return True
    except Exception as e:
        import traceback
        print(f"Error copying files: {str(e)}")
        print(traceback.format_exc())
        return False

# Store conversation histories for different sessions
conversation_histories = {}

@app.route('/api/chat', methods=['POST'])
def chat():
    if not GEMINI_API_KEY:
        return jsonify({'error': 'GEMINI_API_KEY environment variable is not configured'}), 500

    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('sessionId', 'default')
    
    if session_id not in conversation_histories:
        # Initialize a new conversation with the travel assistant prompt
        conversation_histories[session_id] = """You are a friendly travel recommendation assistant. Your goal is to have a natural, interactive conversation with the user to learn about their travel preferences. 

CRITICAL INSTRUCTION: When providing recommendations, you MUST include EXACT and VALID 3-letter IATA airport codes for both departure and arrival locations. For example: LAX for Los Angeles, JFK for New York, CDG for Paris, LHR for London. The application relies on these codes to search for flights. Invalid or missing codes will cause flight search to fail.

You have to get details from where are they departing, exact date of going, exact date of coming back, their budget. Ask questions like : "What type of travel experience are you looking for?" or "Do you prefer cultural experiences, adventure, relaxation, or nature?" Max amount of questions you can ask is 6. Also keep the questions small, no big replies. Suggest places which have airports.
Your task is to gather enough details about the user's likings by asking cross questions and clarifying any ambiguous points. Once you feel you have sufficient information, generate a final JSON output that summarizes their preferences and includes a list of potential destination recommendations. The JSON should have the following structure:

{
  "preferences": {
    "interests": [<list of interests>],
    "mood": "<summary of mood/experience desired>",
    "preferred_climate": "<user's climate preference, if provided>",
    "travel_duration": "<duration or date range if mentioned>",
    "budget": "<budget value or range>",
    "additional_details": "<any extra preferences or details>"
  },
  "recommended_destinations": [
    {
      "name": "<Destination Name>",
      "departure_airport_code": "<EXACT AND VALID 3-LETTER IATA DEPARTURE AIRPORT CODE - THIS IS REQUIRED>",
      "arrival_airport_code": "<EXACT AND VALID 3-LETTER IATA ARRIVAL AIRPORT CODE - THIS IS REQUIRED>",
      "reason": "<Why this destination fits the user's preferences>",
      "departure_date": "<Departure date in form of YYYY-MM-DD>",
      "arrival_date": "<Arrival date in form of YYYY-MM-DD>",
      "Hotel_code": "<small text in exact form "Hotels in (arrival place name)>",
      "estimated_cost_range": "<Approximate cost range for a typical trip>"
    },
    ... (more destinations)
  ]
}

IMPORTANT: You MUST provide EXACT and VALID 3-letter IATA airport codes for both departure and arrival. For example: LAX for Los Angeles, JFK for New York, CDG for Paris, LHR for London, etc. The application will use these codes directly to search for flights. Incorrect codes will result in no flight data being found.

If the answer in the form "I want to fly from <Departure airport code> to <Arrival Airport code> from <Departure date> to <arrival date> for <x> travelers", just ask two more questions, what are your interests and what is your budget. After that, just give the JSON.
Once all required details are captured, output only the final JSON."""
    
    # Update conversation history with user message
    conversation_histories[session_id] += f"\n\nUser: {user_message}\nAI:"
    
    try:
        # Generate response from Gemini
        response = gemini_model.generate_content(conversation_histories[session_id])
        ai_response = response.text.strip()
        
        # Update conversation history with AI response
        conversation_histories[session_id] += f" {ai_response}"
        
        # Check if the response is a JSON recommendation
        is_recommendation = False
        recommendation_data = None
        
        try:
            # Check if the response contains JSON data
            if '{' in ai_response and '}' in ai_response:
                json_start = ai_response.find('{')
                json_end = ai_response.rfind('}') + 1
                json_string = ai_response[json_start:json_end]
                recommendation_data = json.loads(json_string)
                
                # Verify it has the expected structure
                if 'preferences' in recommendation_data and 'recommended_destinations' in recommendation_data:
                    is_recommendation = True
        except:
            # If JSON parsing fails, it's not a recommendation
            pass
        
        return jsonify({
            'response': ai_response,
            'isRecommendation': is_recommendation,
            'recommendationData': recommendation_data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fetch-travel-data', methods=['POST'])
def fetch_travel_data():
    try:
        # Get user selection data from request
        data = request.json
        print(f"Received data: {data}")
        
        # Extract the necessary parameters to ensure they exist
        departure_id = data.get('departure_id')
        arrival_id = data.get('arrival_id')
        outbound_date = data.get('outbound_date')
        return_date = data.get('return_date')
        hotel_query = data.get('hotel_query')
        
        # Validate required parameters
        if not all([departure_id, arrival_id, outbound_date, return_date, hotel_query]):
            missing = []
            if not departure_id: missing.append('departure_id')
            if not arrival_id: missing.append('arrival_id')
            if not outbound_date: missing.append('outbound_date')
            if not return_date: missing.append('return_date')
            if not hotel_query: missing.append('hotel_query')
            
            return jsonify({
                'status': 'error',
                'message': f"Missing required parameters: {', '.join(missing)}"
            }), 400
        
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return jsonify({
                'status': 'error',
                'message': 'SERPAPI_API_KEY environment variable is not configured'
            }), 500
        
        # Use the process_user_selection function from main.py
        success = process_user_selection(data, api_key)
        
        if success:
            # Copy the JSON files to src/pages
            copy_success = copy_json_files()
            
            # Get the current directory
            base_dir = os.path.abspath(os.path.dirname(__file__))
            flight_path = os.path.join(base_dir, 'test_flight.json')
            hotel_path = os.path.join(base_dir, 'test.json')
            
            return jsonify({
                'status': 'success',
                'message': 'Travel data fetched and saved successfully',
                'files': {
                    'flight_data': flight_path,
                    'hotel_data': hotel_path
                },
                'copied_to_src_pages': copy_success
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to process user selection'
            }), 500
        
    except Exception as e:
        import traceback
        print(f"Error fetching travel data: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    data = request.json
    session_id = data.get('sessionId', 'default')
    
    if session_id in conversation_histories:
        del conversation_histories[session_id]
    
    return jsonify({'status': 'success'})

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'service': 'WanderAI Chatbot API',
        'active_sessions': len(conversation_histories)
    })

@app.route('/api/generate-itinerary', methods=['POST'])
def create_itinerary():
    try:
        data = request.json
        print(f"Received itinerary generation request with data: {data}")
        
        # Extract required parameters
        selected_flight = data.get('selectedFlight')
        selected_hotel = data.get('selectedHotel')
        outbound_date = data.get('outboundDate')
        return_date = data.get('returnDate')
        user_preferences = data.get('userPreferences', 'Cultural experiences, local cuisine, and historical sites')
        
        # Validate required parameters
        if not all([selected_flight, selected_hotel, outbound_date, return_date]):
            missing = []
            if not selected_flight: missing.append('selectedFlight')
            if not selected_hotel: missing.append('selectedHotel')
            if not outbound_date: missing.append('outboundDate')
            if not return_date: missing.append('returnDate')
            
            return jsonify({
                'status': 'error',
                'message': f"Missing required parameters: {', '.join(missing)}"
            }), 400
        
        # Generate the itinerary
        print("Generating itinerary with the received data...")
        itinerary_data = generate_itinerary(
            selected_flight, 
            selected_hotel, 
            outbound_date, 
            return_date, 
            user_preferences
        )
        
        if not itinerary_data:
            return jsonify({
                'status': 'error',
                'message': 'Failed to generate itinerary'
            }), 500
        
        # Return the path to the generated itinerary
        base_dir = os.path.abspath(os.path.dirname(__file__))
        itinerary_path = os.path.join(base_dir, 'itinerary.json')
        
        return jsonify({
            'status': 'success',
            'message': 'Itinerary generated and saved successfully',
            'itinerary_path': itinerary_path,
            'itinerary_data': itinerary_data
        })
        
    except Exception as e:
        import traceback
        print(f"Error generating itinerary: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 
