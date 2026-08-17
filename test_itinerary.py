import json
from main import generate_itinerary

def test_generate_itinerary():
    """
    Test the generate_itinerary function to ensure it works after the f-string fix.
    """
    try:
        print("Testing generate_itinerary function...")
        
        # Sample data for testing
        sample_flight = {
            "price": 500,
            "flights": [
                {
                    "airline": "Test Airlines",
                    "flight_number": "TA123",
                    "departure_airport": {
                        "name": "Los Angeles International Airport",
                        "time": "2024-12-01 10:00"
                    },
                    "arrival_airport": {
                        "name": "Paris Charles de Gaulle Airport",
                        "time": "2024-12-01 18:00"
                    }
                },
                {
                    "airline": "Test Airlines",
                    "flight_number": "TA456",
                    "departure_airport": {
                        "name": "Paris Charles de Gaulle Airport",
                        "time": "2024-12-08 20:00"
                    },
                    "arrival_airport": {
                        "name": "Los Angeles International Airport",
                        "time": "2024-12-09 04:00"
                    }
                }
            ]
        }
        
        sample_hotel = {
            "name": "Grand Hotel Paris",
            "description": "Luxury hotel in Paris, France",
            "rate_per_night": {
                "extracted_lowest": 250
            }
        }
        
        outbound_date = "2024-12-01"
        return_date = "2024-12-08"
        user_preferences = "I enjoy museums, fine dining, and walking tours. I prefer to avoid crowds when possible."
        
        # Call the function
        print("Calling generate_itinerary with sample data...")
        result = generate_itinerary(sample_flight, sample_hotel, outbound_date, return_date, user_preferences)
        
        # Check if the result is valid JSON
        if result:
            print("\n✅ SUCCESS: generate_itinerary function returned a result!")
            # Print just a snippet of the result to confirm it's working
            if isinstance(result, dict):
                print(f"\nDestination: {result.get('destination_info', {}).get('name', 'Not specified')}")
                print(f"Total Cost: {result.get('total_cost', 'Not specified')}")
                
                # Check number of days in itinerary
                itinerary = result.get('itinerary', {})
                print(f"Number of days in itinerary: {len(itinerary)}")
                
                # Display the first day as a sample
                if itinerary:
                    first_day_key = list(itinerary.keys())[0]
                    first_day = itinerary[first_day_key]
                    print(f"\nSample day ({first_day_key}):")
                    print(f"Title: {first_day.get('title', 'No title')}")
                    print(f"Morning activity: {first_day.get('morning', {}).get('activity', 'Not specified')}")
            else:
                print("Result is not a dictionary, possibly a string?")
                print(f"Type: {type(result)}")
                print(f"Length: {len(str(result)) if result else 0} characters")
            return True
        else:
            print("\n⚠️ WARNING: generate_itinerary function returned None or empty result.")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: Failed to test generate_itinerary: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_generate_itinerary() 