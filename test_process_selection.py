import json
import os
from main import process_user_selection

def test_process_user_selection():
    """
    Test the process_user_selection function directly with various destination parameters.
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise RuntimeError("SERPAPI_API_KEY environment variable is required.")
    
    # Future dates
    from datetime import datetime, timedelta
    today = datetime.now().date()
    future_date = today + timedelta(days=30)
    future_end_date = future_date + timedelta(days=7)
    outbound_date = future_date.strftime('%Y-%m-%d')
    return_date = future_end_date.strftime('%Y-%m-%d')
    
    # Define test cases with different destination parameters
    test_cases = [
        {
            "name": "Popular city pair (Los Angeles to New York)",
            "data": {
                "departure_id": "LAX",
                "arrival_id": "JFK",
                "outbound_date": outbound_date,
                "return_date": return_date,
                "hotel_query": "Hotels in New York"
            }
        },
        {
            "name": "International route (London to Paris)",
            "data": {
                "departure_id": "LHR",
                "arrival_id": "CDG",
                "outbound_date": outbound_date,
                "return_date": return_date,
                "hotel_query": "Hotels in Paris"
            }
        },
        {
            "name": "West Coast to East Coast (San Francisco to Boston)",
            "data": {
                "departure_id": "SFO",
                "arrival_id": "BOS",
                "outbound_date": outbound_date,
                "return_date": return_date,
                "hotel_query": "Hotels in Boston"
            }
        }
    ]
    
    # Run each test case
    for test_case in test_cases:
        print(f"\n\n=== Testing: {test_case['name']} ===")
        success = process_user_selection(test_case['data'], api_key)
        
        if success:
            print(f"✅ Test successful for {test_case['name']}")
            
            # Check if we got real flight data or mock data
            with open('test_flight.json', 'r', encoding='utf-8') as f:
                flight_data = json.load(f)
                
            if flight_data and 'search_metadata' in flight_data:
                is_mock = flight_data['search_metadata'].get('id') == 'mock_search_id'
                print(f"Flight data is {'MOCK' if is_mock else 'REAL'}")
                
                if not is_mock:
                    # Check how many flights were found
                    best_flights = len(flight_data.get('best_flights', []))
                    other_flights = len(flight_data.get('other_flights', []))
                    print(f"Found {best_flights} best flights and {other_flights} other flights")
        else:
            print(f"❌ Test failed for {test_case['name']}")
    
    print("\nChecking the files created:")
    for file_name in ['test.json', 'test_flight.json']:
        file_size = os.path.getsize(file_name) if os.path.exists(file_name) else 0
        print(f"{file_name}: {file_size} bytes")
    
    # Check if files were copied to src/pages
    src_pages_dir = os.path.join(os.getcwd(), 'src', 'pages')
    if os.path.exists(src_pages_dir):
        for file_name in ['test.json', 'test_flight.json']:
            file_path = os.path.join(src_pages_dir, file_name)
            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            print(f"src/pages/{file_name}: {file_size} bytes")

if __name__ == "__main__":
    test_process_user_selection() 
