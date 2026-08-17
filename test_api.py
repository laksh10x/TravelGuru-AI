import requests
import json

def test_fetch_travel_data():
    url = "http://localhost:5000/api/fetch-travel-data"
    payload = {
        "departure_id": "PEK",
        "arrival_id": "AUS",
        "outbound_date": "2024-05-15",
        "return_date": "2024-05-22",
        "hotel_query": "Hotels in Austin"
    }
    
    print("Sending request to:", url)
    print("With payload:", json.dumps(payload, indent=2))
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status code: {response.status_code}")
        print("Response:", json.dumps(response.json(), indent=2))
        
        # Check if files were created
        import os
        files_to_check = ['test.json', 'test_flight.json']
        for file in files_to_check:
            if os.path.exists(file):
                file_size = os.path.getsize(file)
                print(f"File {file} exists, size: {file_size} bytes")
            else:
                print(f"File {file} does not exist")
                
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_fetch_travel_data() 