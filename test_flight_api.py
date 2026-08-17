import requests
import json
import os
import sys
from main import search_google_flights, generate_mock_flight_data

def test_flight_api():
    """
    Test the flight search API directly to diagnose issues
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise RuntimeError("SERPAPI_API_KEY environment variable is required.")
    
    # Test parameters
    outbound_date = "2024-05-15"
    return_date = "2024-05-22"
    departure_id = "PEK"
    arrival_id = "AUS"
    
    print(f"Testing flight API search with:")
    print(f"  Departure: {departure_id}")
    print(f"  Arrival: {arrival_id}")
    print(f"  Dates: {outbound_date} to {return_date}")
    print(f"  API Key: {api_key[:5]}...{api_key[-5:]}")
    
    # Call the flight search function directly
    result = search_google_flights(
        api_key=api_key,
        outbound_date=outbound_date,
        return_date=return_date,
        departure_id=departure_id,
        arrival_id=arrival_id
    )
    
    # Check if we got real data or mock data
    is_mock_data = False
    if result and 'search_metadata' in result:
        if result['search_metadata'].get('id') == 'mock_search_id':
            is_mock_data = True
    
    print("\nResult:")
    print(f"  Got {'MOCK' if is_mock_data else 'REAL'} flight data")
    print(f"  Data has {len(result.get('best_flights', []))} best flights")
    print(f"  Data has {len(result.get('other_flights', []))} other flights")
    
    # Save the result for inspection
    with open('flight_test_result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\nFlight data saved to flight_test_result.json for inspection")
    
    # Try different airport codes if the first attempt failed
    if is_mock_data:
        print("\nFirst attempt returned mock data. Testing with alternative airport codes...")
        alternative_tests = [
            ("LAX", "JFK"),  # Los Angeles to New York
            ("LHR", "CDG"),  # London to Paris
            ("NYC", "LAX"),  # New York to Los Angeles
        ]
        
        for dep, arr in alternative_tests:
            print(f"\nTrying {dep} to {arr}...")
            alt_result = search_google_flights(
                api_key=api_key,
                outbound_date=outbound_date,
                return_date=return_date,
                departure_id=dep,
                arrival_id=arr
            )
            
            # Check if we got real data
            alt_is_mock = False
            if alt_result and 'search_metadata' in alt_result:
                if alt_result['search_metadata'].get('id') == 'mock_search_id':
                    alt_is_mock = True
            
            print(f"  Got {'MOCK' if alt_is_mock else 'REAL'} flight data")
            if not alt_is_mock:
                print(f"  Success with {dep} to {arr}!")
                print(f"  Data has {len(alt_result.get('best_flights', []))} best flights")
                print(f"  Data has {len(alt_result.get('other_flights', []))} other flights")
                
                # Save the successful result
                with open(f'flight_test_{dep}_to_{arr}.json', 'w', encoding='utf-8') as f:
                    json.dump(alt_result, f, indent=2, ensure_ascii=False)
                print(f"  Result saved to flight_test_{dep}_to_{arr}.json")
                break

if __name__ == "__main__":
    test_flight_api() 
