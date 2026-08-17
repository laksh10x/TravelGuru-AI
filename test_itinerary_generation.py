import requests
import json
import os
import sys

def test_itinerary_generation():
    """
    Test the /api/generate-itinerary endpoint to verify it properly generates
    and saves a personalized itinerary based on selected flight and hotel data.
    """
    try:
        # Local server URL (assuming the default Flask port)
        url = "http://localhost:5000/api/generate-itinerary"
        
        # Create some sample flight and hotel data for testing
        with open('test_flight.json', 'r', encoding='utf-8') as f:
            flight_data = json.load(f)
            
        with open('test.json', 'r', encoding='utf-8') as f:
            hotel_data = json.load(f)
        
        # Get the first flight and hotel from the data
        selected_flight = flight_data.get('best_flights', [])[0] if flight_data.get('best_flights') else None
        selected_hotel = hotel_data.get('properties', [])[0] if hotel_data.get('properties') else None
        
        if not selected_flight or not selected_hotel:
            print("❌ ERROR: Could not find flight or hotel data for testing.")
            return False
        
        # Prepare the request payload
        payload = {
            "selectedFlight": selected_flight,
            "selectedHotel": selected_hotel,
            "outboundDate": "2024-05-15",
            "returnDate": "2024-05-22",
            "userPreferences": "Cultural experiences, museums, local food, and walking tours"
        }
        
        print(f"Sending request to: {url}")
        print(f"Using flight: {selected_flight.get('airline', '')} {selected_flight.get('flight_number', '')}")
        print(f"Using hotel: {selected_hotel.get('name', '')}")
        print(f"Dates: {payload['outboundDate']} to {payload['returnDate']}")
        
        # Send the request
        response = requests.post(url, json=payload, timeout=120)  # 2-minute timeout
        
        print(f"\nResponse Status Code: {response.status_code}")
        
        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            print(f"Response Status: {response_data.get('status', 'unknown')}")
            
            if response_data.get('status') == 'success':
                print("✅ SUCCESS: Itinerary generated successfully!")
                
                # Check if itinerary.json was created/updated
                itinerary_path = os.path.join(os.getcwd(), 'itinerary.json')
                if os.path.exists(itinerary_path):
                    file_size = os.path.getsize(itinerary_path)
                    file_time = os.path.getmtime(itinerary_path)
                    
                    print(f"\nItinerary file details:")
                    print(f"  Path: {itinerary_path}")
                    print(f"  Size: {file_size} bytes")
                    print(f"  Last modified: {file_time}")
                    
                    # Also check if it was copied to src/pages
                    src_pages_path = os.path.join(os.getcwd(), 'src', 'pages', 'itinerary.json')
                    if os.path.exists(src_pages_path):
                        src_file_size = os.path.getsize(src_pages_path)
                        src_file_time = os.path.getmtime(src_pages_path)
                        
                        print(f"\nItinerary copied to src/pages:")
                        print(f"  Path: {src_pages_path}")
                        print(f"  Size: {src_file_size} bytes")
                        print(f"  Last modified: {src_file_time}")
                        
                        if file_size == src_file_size:
                            print("✅ Files match in size")
                        else:
                            print("⚠️ Files have different sizes")
                    else:
                        print("\n⚠️ WARNING: Itinerary not copied to src/pages")
                    
                    # Show a sample of the generated itinerary
                    with open(itinerary_path, 'r', encoding='utf-8') as f:
                        itinerary_data = json.load(f)
                        
                    print("\nGenerated Itinerary Sample:")
                    print(f"  Destination: {itinerary_data.get('destination_info', {}).get('name', 'Unknown')}")
                    print(f"  Total Cost: {itinerary_data.get('total_cost', 'Unknown')}")
                    
                    # Show first day as sample
                    itinerary = itinerary_data.get('itinerary', {})
                    if itinerary:
                        first_day_key = list(itinerary.keys())[0]
                        print(f"  First Day: {itinerary[first_day_key].get('title', 'Unknown')}")
                        
                    return True
                else:
                    print("❌ ERROR: Itinerary file not found after generation")
                    return False
            else:
                print(f"❌ ERROR: {response_data.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ ERROR: Request failed with status code {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting itinerary generation test...")
    success = test_itinerary_generation()
    sys.exit(0 if success else 1) 