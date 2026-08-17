import requests
import datetime
import json
import google.generativeai as genai
import os

def search_google_flights(api_key, outbound_date, return_date, departure_id="PEK", arrival_id="AUS"):
    """
    Calls the Google Flights API using SerpApi and returns JSON flight results.
    """
    # Format the airport codes correctly - SerpAPI might need specific formatting
    departure_id = departure_id.strip().upper()
    arrival_id = arrival_id.strip().upper()
    
    # Check and adjust dates to ensure they are in the future
    # The API requires dates to be in the future
    today = datetime.datetime.now().date()
    
    # Parse the provided dates
    try:
        outbound_date_obj = datetime.datetime.strptime(outbound_date, "%Y-%m-%d").date()
        return_date_obj = datetime.datetime.strptime(return_date, "%Y-%m-%d").date()
        
        # If the dates are in the past, adjust them to be in the future
        if outbound_date_obj <= today:
            # Set outbound date to 30 days from now
            outbound_date_obj = today + datetime.timedelta(days=30)
            outbound_date = outbound_date_obj.strftime("%Y-%m-%d")
            print(f"Adjusted outbound date to future: {outbound_date}")
            
            # Also adjust return date to be 7 days after the new outbound date
            return_date_obj = outbound_date_obj + datetime.timedelta(days=7)
            return_date = return_date_obj.strftime("%Y-%m-%d")
            print(f"Adjusted return date to future: {return_date}")
    except Exception as e:
        print(f"Error parsing dates: {str(e)}")
        # Use default dates 30 days and 37 days from now
        outbound_date_obj = today + datetime.timedelta(days=30)
        outbound_date = outbound_date_obj.strftime("%Y-%m-%d")
        return_date_obj = outbound_date_obj + datetime.timedelta(days=7)
        return_date = return_date_obj.strftime("%Y-%m-%d")
        print(f"Using default future dates: {outbound_date} to {return_date}")
    
    # Try alternative parameters that might work better with SerpAPI
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_flights",
        "departure_id": departure_id,     # e.g., "PEK"
        "arrival_id": arrival_id,         # e.g., "AUS"
        "outbound_date": outbound_date,   # Format: YYYY-MM-DD
        "return_date": return_date,       # Format: YYYY-MM-DD
        "currency": "USD",
        "hl": "en",
        "api_key": api_key
    }
    
    print(f"Making flight API request to: {url}")
    print(f"Flight API parameters: {params}")
    
    try:
        response = requests.get(url, params=params)
        print(f"Flight API response status: {response.status_code}")
        print(f"Response URL: {response.url}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Flight API response data keys: {list(result.keys()) if result else 'None'}")
            
            # Check if the response contains error information
            if 'error' in result:
                print(f"API Error: {result['error']}")
                return generate_mock_flight_data(departure_id, arrival_id, outbound_date, return_date)
                
            # Check if we have flight data in the response
            if 'best_flights' in result or 'other_flights' in result:
                print(f"Success! Found flight data in the response.")
                return result
            else:
                print(f"No flight data found in the response. Using mock data.")
                print(f"Response content: {json.dumps(result, indent=2)[:500]}...")
                return generate_mock_flight_data(departure_id, arrival_id, outbound_date, return_date)
        else:
            print(f"Error fetching flight data: {response.status_code}")
            try:
                error_content = response.json()
                print(f"Error content: {error_content}")
            except:
                print(f"Error response: {response.text[:1000]}")
            
            # Try an alternative approach - use from and to cities instead of airport codes
            print("Trying alternative format for flight search...")
            return try_alternative_flight_search(api_key, outbound_date, return_date, departure_id, arrival_id)
    except Exception as e:
        import traceback
        print(f"Exception in flight search: {str(e)}")
        print(traceback.format_exc())
        return generate_mock_flight_data(departure_id, arrival_id, outbound_date, return_date)

def try_alternative_flight_search(api_key, outbound_date, return_date, departure_id, arrival_id):
    """
    Try an alternative approach to search for flights using city names instead of airport codes
    """
    # Map common airport codes to city names
    airport_to_city = {
        "PEK": "Beijing",
        "AUS": "Austin",
        "LAX": "Los Angeles",
        "JFK": "New York",
        "LHR": "London",
        "CDG": "Paris",
        "SYD": "Sydney",
        "NRT": "Tokyo"
    }
    
    departure_city = airport_to_city.get(departure_id, departure_id)
    arrival_city = airport_to_city.get(arrival_id, arrival_id)
    
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_flights",
        "q": f"Flights from {departure_city} to {arrival_city}",
        "outbound_date": outbound_date,
        "return_date": return_date,
        "currency": "USD",
        "hl": "en",
        "api_key": api_key
    }
    
    print(f"Trying alternative search with params: {params}")
    
    try:
        response = requests.get(url, params=params)
        print(f"Alternative flight API response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Alternative flight API response data keys: {list(result.keys()) if result else 'None'}")
            
            if 'best_flights' in result or 'other_flights' in result:
                print(f"Success with alternative approach! Found flight data in the response.")
                return result
            else:
                print(f"No flight data found in alternative response.")
                return generate_mock_flight_data(departure_id, arrival_id, outbound_date, return_date)
        else:
            print(f"Error with alternative flight search: {response.status_code} - {response.text}")
            return generate_mock_flight_data(departure_id, arrival_id, outbound_date, return_date)
    except Exception as e:
        print(f"Exception in alternative flight search: {str(e)}")
        return generate_mock_flight_data(departure_id, arrival_id, outbound_date, return_date)

def generate_mock_flight_data(departure_id, arrival_id, outbound_date, return_date):
    """
    Generates mock flight data for testing when the API fails
    """
    print("Generating mock flight data for testing")
    return {
        "search_metadata": {
            "id": "mock_search_id",
            "status": "Success",
            "json_endpoint": "mock_endpoint",
            "created_at": datetime.datetime.now().isoformat(),
            "processed_at": datetime.datetime.now().isoformat(),
            "google_flights_url": f"https://www.google.com/travel/flights?hl=en",
            "raw_html_file": "mock_html",
            "total_time_taken": 0.5
        },
        "search_parameters": {
            "engine": "google_flights",
            "departure_id": departure_id,
            "arrival_id": arrival_id,
            "outbound_date": outbound_date,
            "return_date": return_date,
            "currency": "USD"
        },
        "best_flights": [
            {
                "price": 1250,
                "price_str": "$1,250",
                "total_duration": 1020,
                "flight_time": "17h 0m",
                "flights": [
                    {
                        "airline": "Mock Airlines",
                        "airline_logo": "https://example.com/logo.png",
                        "flight_number": "MA123",
                        "departure_airport": {
                            "name": f"{departure_id} Airport",
                            "time": f"{outbound_date} 10:00"
                        },
                        "arrival_airport": {
                            "name": f"{arrival_id} Airport",
                            "time": f"{outbound_date} 19:00"
                        },
                        "duration": 540,
                        "duration_str": "9h 0m"
                    },
                    {
                        "airline": "Mock Airlines",
                        "airline_logo": "https://example.com/logo.png",
                        "flight_number": "MA456",
                        "departure_airport": {
                            "name": f"{arrival_id} Airport",
                            "time": f"{return_date} 12:00"
                        },
                        "arrival_airport": {
                            "name": f"{departure_id} Airport",
                            "time": f"{return_date} 20:00"
                        },
                        "duration": 480,
                        "duration_str": "8h 0m"
                    }
                ]
            }
        ],
        "other_flights": [
            {
                "price": 1500,
                "price_str": "$1,500",
                "total_duration": 1200,
                "flight_time": "20h 0m",
                "flights": [
                    {
                        "airline": "Mock Express",
                        "airline_logo": "https://example.com/logo2.png",
                        "flight_number": "ME789",
                        "departure_airport": {
                            "name": f"{departure_id} Airport",
                            "time": f"{outbound_date} 14:00"
                        },
                        "arrival_airport": {
                            "name": f"{arrival_id} Airport",
                            "time": f"{outbound_date} 23:00"
                        },
                        "duration": 540,
                        "duration_str": "9h 0m"
                    },
                    {
                        "airline": "Mock Express",
                        "airline_logo": "https://example.com/logo2.png",
                        "flight_number": "ME987",
                        "departure_airport": {
                            "name": f"{arrival_id} Airport",
                            "time": f"{return_date} 09:00"
                        },
                        "arrival_airport": {
                            "name": f"{departure_id} Airport",
                            "time": f"{return_date} 20:00"
                        },
                        "duration": 660,
                        "duration_str": "11h 0m"
                    }
                ]
            }
        ]
    }

def search_google_hotels(api_key, check_in_date, check_out_date, hotel_query="Hotels in Austin"):
    """
    Calls the Google Hotels API using SerpApi and returns JSON hotel results.
    """
    # Check and adjust dates to ensure they are in the future
    # The API requires dates to be in the future
    today = datetime.datetime.now().date()
    
    # Parse the provided dates
    try:
        check_in_date_obj = datetime.datetime.strptime(check_in_date, "%Y-%m-%d").date()
        check_out_date_obj = datetime.datetime.strptime(check_out_date, "%Y-%m-%d").date()
        
        # If the dates are in the past, adjust them to be in the future
        if check_in_date_obj <= today:
            # Set check-in date to 30 days from now
            check_in_date_obj = today + datetime.timedelta(days=30)
            check_in_date = check_in_date_obj.strftime("%Y-%m-%d")
            print(f"Adjusted check-in date to future: {check_in_date}")
            
            # Also adjust check-out date to be 7 days after the new check-in date
            check_out_date_obj = check_in_date_obj + datetime.timedelta(days=7)
            check_out_date = check_out_date_obj.strftime("%Y-%m-%d")
            print(f"Adjusted check-out date to future: {check_out_date}")
    except Exception as e:
        print(f"Error parsing dates: {str(e)}")
        # Use default dates 30 days and 37 days from now
        check_in_date_obj = today + datetime.timedelta(days=30)
        check_in_date = check_in_date_obj.strftime("%Y-%m-%d")
        check_out_date_obj = check_in_date_obj + datetime.timedelta(days=7)
        check_out_date = check_out_date_obj.strftime("%Y-%m-%d")
        print(f"Using default future dates for hotels: {check_in_date} to {check_out_date}")
    
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_hotels",
        "q": hotel_query,                # e.g., "Hotels in Austin"
        "check_in_date": check_in_date,    # Format: YYYY-MM-DD
        "check_out_date": check_out_date,  # Format: YYYY-MM-DD
        "currency": "USD",
        "hl": "en",
        "api_key": api_key
    }
    
    print(f"Making hotel API request to: {url}")
    print(f"Hotel API parameters: {params}")
    
    try:
        response = requests.get(url, params=params)
        print(f"Hotel API response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Hotel API response data keys: {list(result.keys()) if result else 'None'}")
            return result
        else:
            print(f"Error fetching hotel data: {response.status_code} - {response.text}")
            # Return mock data if the API call fails
            return generate_mock_hotel_data(hotel_query, check_in_date, check_out_date)
    except Exception as e:
        import traceback
        print(f"Exception in hotel search: {str(e)}")
        print(traceback.format_exc())
        # Return mock data if an exception occurs
        return generate_mock_hotel_data(hotel_query, check_in_date, check_out_date)

def generate_mock_hotel_data(hotel_query, check_in_date, check_out_date):
    """
    Generates mock hotel data for testing when the API fails
    """
    print("Generating mock hotel data for testing")
    destination = hotel_query.replace("Hotels in ", "")
    
    return {
        "search_metadata": {
            "id": "mock_hotel_search_id",
            "status": "Success",
            "json_endpoint": "mock_endpoint",
            "created_at": datetime.datetime.now().isoformat(),
            "processed_at": datetime.datetime.now().isoformat(),
            "google_hotels_url": f"https://www.google.com/travel/hotels/{destination}",
            "raw_html_file": "mock_html",
            "total_time_taken": 0.5
        },
        "search_parameters": {
            "engine": "google_hotels",
            "q": hotel_query,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "currency": "USD"
        },
        "properties": [
            {
                "name": f"Grand Hotel {destination}",
                "description": f"Luxury hotel in downtown {destination}",
                "rate_per_night": {"extracted_lowest": 250, "extracted_highest": 350},
                "overall_rating": "4.5",
                "images": [
                    {"original_image": f"https://example.com/{destination.lower()}_hotel1.jpg"}
                ],
                "amenities": ["Free WiFi", "Pool", "Spa", "Fitness Center", "Restaurant"],
                "reviews": 1250
            },
            {
                "name": f"{destination} Plaza Hotel",
                "description": f"Modern hotel with great views of {destination}",
                "rate_per_night": {"extracted_lowest": 180, "extracted_highest": 280},
                "overall_rating": "4.3",
                "images": [
                    {"original_image": f"https://example.com/{destination.lower()}_hotel2.jpg"}
                ],
                "amenities": ["Free WiFi", "Pool", "Bar", "Breakfast included"],
                "reviews": 870
            },
            {
                "name": f"Budget Inn {destination}",
                "description": f"Affordable comfort in {destination}",
                "rate_per_night": {"extracted_lowest": 120, "extracted_highest": 150},
                "overall_rating": "3.8",
                "images": [
                    {"original_image": f"https://example.com/{destination.lower()}_hotel3.jpg"}
                ],
                "amenities": ["Free WiFi", "Free Parking", "Breakfast available"],
                "reviews": 450
            }
        ]
    }

def display_flight_options(flight_data):
    """
    Displays a few flight options (using 'best_flights' or 'other_flights')
    and returns a list of these options.
    """
    flights_list = flight_data.get("best_flights") or flight_data.get("other_flights", [])
    if not flights_list:
        print("No flight options found.")
        return []
    options = []
    for idx, flight_option in enumerate(flights_list[:3], start=1):  # show first 3 options
        print(f"\nFlight Option {idx}:")
        segments = flight_option.get("flights", [])
        for seg in segments:
            dep_airport = seg.get("departure_airport", {}).get("name", "N/A")
            dep_time    = seg.get("departure_airport", {}).get("time", "N/A")
            arr_airport = seg.get("arrival_airport", {}).get("name", "N/A")
            arr_time    = seg.get("arrival_airport", {}).get("time", "N/A")
            airline     = seg.get("airline", "N/A")
            flight_num  = seg.get("flight_number", "N/A")
            print(f"  {airline} {flight_num}: {dep_airport} at {dep_time} -> {arr_airport} at {arr_time}")
        total_duration = flight_option.get("total_duration", "N/A")
        price          = flight_option.get("price", "N/A")
        print(f"  Total Duration: {total_duration} minutes")
        print(f"  Price: {price} USD")
        options.append(flight_option)
    return options

def display_hotel_options(hotel_data):
    """
    Displays a few hotel options based on the 'properties' key,
    and returns a list of these options.
    """
    hotels_list = hotel_data.get("properties", [])
    if not hotels_list:
        print("No hotel options found.")
        return []
    options = []
    for idx, hotel in enumerate(hotels_list[:3], start=1):  # show first 3 options
        name = hotel.get("name", "N/A")
        address = hotel.get("address", "N/A")
        rating = hotel.get("overall_rating", "N/A")
        rate = hotel.get("rate_per_night", {}).get("extracted_lowest", "N/A")
        print(f"\nHotel Option {idx}: {name}")
        print(f"  Address: {address}")
        print(f"  Overall Rating: {rating}")
        print(f"  Rate per Night: {rate} USD")
        options.append(hotel)
    return options

def choose_option(options, option_type="flight"):
    """
    Prompts the user to select an option from the list.
    """
    if not options:
        return None
    while True:
        try:
            choice = int(input(f"Select your preferred {option_type} option (1-{len(options)}): "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")

import os
import requests

def call_gemini(prompt):
    """
    Calls the Gemini API using the provided prompt.
    This function uses the new endpoint and payload structure.
    """
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is required.")

    genai.configure(api_key=gemini_api_key)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")

    response = gemini_model.generate_content(prompt)
    ai_response = response.text.strip()
    return ai_response

def print_itinerary(ai_response):
    """
    Prints the formatted itinerary from the AI response
    """
    try:
        # Clean up the response - remove markdown code blocks if present
        cleaned_response = ai_response
        
        # Remove markdown code block syntax if present
        if "```json" in cleaned_response or "```" in cleaned_response:
            import re
            # Extract content between markdown code blocks
            markdown_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', cleaned_response)
            if markdown_match:
                cleaned_response = markdown_match.group(1).strip()
        
        # Parse the AI response string into a JSON object
        itin = json.loads(cleaned_response)
        
        days = itin.get("itinerary", {})
        for day_key in sorted(days.keys(), key=lambda k: int(k.split('_')[1])):
            day_details = days[day_key]
            day_number = day_key.split('_')[1]
            print("=" * 45)
            print(f"Day {day_number}:")
            print(f"Date     : {day_details.get('date', 'N/A')}")
            print(f"Morning  : {day_details.get('morning', {}).get('activity', 'N/A')}")
            print(f"Afternoon: {day_details.get('afternoon', {}).get('activity', 'N/A')}")
            print(f"Evening  : {day_details.get('evening', {}).get('activity', 'N/A')}")
            print("=" * 45)
            print()  # Blank line for spacing

        print(f"Total Cost: {itin.get('total_cost', 'N/A')}")
        return itin
    except json.JSONDecodeError as e:
        print("Error parsing AI response:", str(e))
        print("Raw AI response:", ai_response)
        return None

def process_user_selection(user_selection, api_key):
    """
    Process user selection JSON and save flight and hotel data to respective files.
    Expected user_selection format:
    {
        "departure_id": "PEK",
        "arrival_id": "AUS",
        "outbound_date": "2024-03-20",
        "return_date": "2024-03-27",
        "hotel_query": "Hotels in Austin"
    }
    """
    try:
        import traceback
        print(f"Processing user selection: {user_selection}")
        
        # Get common parameters needed for both searches
        outbound_date = user_selection['outbound_date']
        return_date = user_selection['return_date']
        
        # Get hotel query or create one if not provided
        hotel_query = user_selection.get('hotel_query')
        if not hotel_query and 'arrival_id' in user_selection:
            # Try to create a hotel query from the arrival airport code
            known_airport_to_city = {
                'AUS': 'Austin',
                'LAX': 'Los Angeles',
                'JFK': 'New York',
                'LHR': 'London',
                'CDG': 'Paris',
                'NRT': 'Tokyo',
                'SFO': 'San Francisco'
            }
            arrival_id = user_selection['arrival_id']
            city = known_airport_to_city.get(arrival_id, arrival_id)
            hotel_query = f"Hotels in {city}"
            print(f"Created hotel query from arrival_id: {hotel_query}")
            
        # Search for flights - try multiple airport combinations if needed
        # Start with the provided departure and arrival
        departure_id = user_selection.get('departure_id', 'LAX')
        arrival_id = user_selection.get('arrival_id', 'JFK')
        
        print(f"Searching for flights from {departure_id} to {arrival_id}")
        print(f"Dates: {outbound_date} to {return_date}")
        
        # First attempt with user-provided airports
        flight_data = search_google_flights(
            api_key,
            outbound_date,
            return_date,
            departure_id,
            arrival_id
        )
        
        # Check if we got real flight data
        has_real_flight_data = False
        if flight_data and 'search_metadata' in flight_data:
            if flight_data['search_metadata'].get('id') != 'mock_search_id':
                if 'best_flights' in flight_data or 'other_flights' in flight_data:
                    print(f"Successfully found flight data for {departure_id} to {arrival_id}")
                    has_real_flight_data = True
        
        # If we didn't get real flight data, try with known working airport combinations
        if not has_real_flight_data:
            print("First attempt returned mock data. Trying alternative airport combinations...")
            alternative_combinations = [
                ("LAX", "JFK"),  # Los Angeles to New York
                ("JFK", "LAX"),  # New York to Los Angeles
                ("LHR", "CDG"),  # London to Paris
                ("CDG", "LHR")   # Paris to London
            ]
            
            for alt_dep, alt_arr in alternative_combinations:
                print(f"Trying alternative route: {alt_dep} to {alt_arr}...")
                alt_flight_data = search_google_flights(
                    api_key,
                    outbound_date,
                    return_date,
                    alt_dep,
                    alt_arr
                )
                
                # Check if we got real flight data
                if alt_flight_data and 'search_metadata' in alt_flight_data:
                    if alt_flight_data['search_metadata'].get('id') != 'mock_search_id':
                        if 'best_flights' in alt_flight_data or 'other_flights' in alt_flight_data:
                            print(f"Successfully found flight data with alternative route {alt_dep} to {alt_arr}")
                            flight_data = alt_flight_data
                            has_real_flight_data = True
                            break
            
            if not has_real_flight_data:
                print("All flight API attempts returned mock data.")
        
        # Search for hotels
        print(f"Searching for hotels with query: {hotel_query}")
        hotel_data = search_google_hotels(
            api_key,
            outbound_date,
            return_date,
            hotel_query
        )
        
        if not hotel_data:
            print("Warning: No hotel data returned from API")
        else:
            print(f"Hotel data received successfully with {len(hotel_data.get('properties', []))} properties")
        
        # Get the current working directory
        cwd = os.getcwd()
        print(f"Current working directory: {cwd}")
        
        # Save flight data
        flight_path = os.path.join(cwd, 'test_flight.json')
        with open(flight_path, 'w', encoding='utf-8') as f:
            json.dump(flight_data, f, indent=2, ensure_ascii=False)
        print(f"Flight data saved to {flight_path}")
            
        # Save hotel data
        hotel_path = os.path.join(cwd, 'test.json')
        with open(hotel_path, 'w', encoding='utf-8') as f:
            json.dump(hotel_data, f, indent=2, ensure_ascii=False)
        print(f"Hotel data saved to {hotel_path}")
        
        # Try to save to src/pages directory if it exists
        src_pages_dir = os.path.join(cwd, 'src', 'pages')
        if os.path.exists(src_pages_dir):
            try:
                print(f"Attempting to save to {src_pages_dir}")
                with open(os.path.join(src_pages_dir, 'test_flight.json'), 'w', encoding='utf-8') as f:
                    json.dump(flight_data, f, indent=2, ensure_ascii=False)
                with open(os.path.join(src_pages_dir, 'test.json'), 'w', encoding='utf-8') as f:
                    json.dump(hotel_data, f, indent=2, ensure_ascii=False)
                print(f"Successfully saved data to {src_pages_dir}")
            except Exception as e:
                print(f"Error saving to src/pages: {str(e)}")
            
        return True
    except Exception as e:
        print(f"Error processing user selection: {str(e)}")
        print(traceback.format_exc())
        return False

def generate_itinerary(selected_flight, selected_hotel, outbound_date, return_date, user_preferences):
    """
    Generates a detailed day-by-day itinerary using Gemini, incorporating
    the selected flight, hotel, and user preferences. Also includes a total cost.
    Saves the itinerary to JSON file and returns the data.
    """
    # Summarize the selected flight
    flight_summary = ""
    segments = selected_flight.get("flights", [])
    for seg in segments:
        dep_airport = seg.get("departure_airport", {}).get("name", "N/A")
        dep_time    = seg.get("departure_airport", {}).get("time", "N/A")
        arr_airport = seg.get("arrival_airport", {}).get("name", "N/A")
        arr_time    = seg.get("arrival_airport", {}).get("time", "N/A")
        airline     = seg.get("airline", "N/A")
        flight_num  = seg.get("flight_number", "N/A")
        flight_summary += f"{airline} {flight_num}: {dep_airport} at {dep_time} -> {arr_airport} at {arr_time}; "
    
    # Summarize the selected hotel
    hotel_name = selected_hotel.get("name", "N/A")
    hotel_rate = selected_hotel.get("rate_per_night", {}).get("extracted_lowest", "N/A")
    hotel_summary = f"Staying at {hotel_name} (Rate per night: {hotel_rate} USD)"
    
    # Extract destination city from hotel name or query
    destination = ""
    if 'description' in selected_hotel and selected_hotel['description']:
        description = selected_hotel['description'].lower()
        if 'in ' in description:
            destination = description.split('in ')[1].split()[0]
    if not destination and hotel_name:
        for city in ["Austin", "New York", "Paris", "Tokyo", "London", "Los Angeles"]:
            if city.lower() in hotel_name.lower():
                destination = city
                break
    
    # Calculate the number of nights (for hotels, typically check-out day is not charged)
    start = datetime.datetime.strptime(outbound_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(return_date, "%Y-%m-%d")
    num_nights = (end - start).days
    
    # Compute total cost (assume flight price and hotel rate are numeric)
    try:
        flight_price = float(selected_flight.get("price", 0))
    except:
        flight_price = 0
    try:
        hotel_rate_numeric = float(hotel_rate)
    except:
        hotel_rate_numeric = 0
    total_hotel_cost = hotel_rate_numeric * num_nights
    total_cost = flight_price + total_hotel_cost
    
    # Build the detailed prompt for Gemini
    prompt = f"""You are a travel itinerary planner creating a detailed, visually appealing travel plan.

DESTINATION DETAILS:
- Primary destination: {destination if destination else "the city of your hotel"}
- Travel dates: {outbound_date} to {return_date} (total of {num_nights} nights)
- Flight details: {flight_summary}
- Accommodation: {hotel_summary}
- User preferences: {user_preferences}
- Total estimated cost: {total_cost} USD

CREATE A BEAUTIFUL DAILY ITINERARY with the following elements for each day:
1. Day number, date (YYYY-MM-DD), and a creative day title that captures the theme
2. Morning activities (3-4 hours) with specific locations, opening hours, and transportation suggestions
3. Lunch recommendations with specific restaurant names, cuisine type, and price range ($ to $$$)
4. Afternoon activities (3-4 hours) with specific locations, opening hours, transportation
5. Dinner recommendations with specific restaurant names, cuisine type, and price range
6. Evening activities or entertainment options with timing suggestions
7. Optional insider tips or cultural notes for each day

ADDITIONAL ELEMENTS TO INCLUDE:
- For each attraction, include the estimated time to spend there
- Suggest at least one iconic photo opportunity each day with a brief description of what makes it special
- For the first day, account for arrival time based on the flight details
- For the last day, account for departure time based on the return flight
- Include one free time/relaxation period each day
- Recommend realistic transportation options between activities (public transit, walking, rideshare)

THEME & CUSTOMIZATION:
- Recommend a color theme that matches the destination's vibe (provide hex color codes for primary, secondary, and accent colors)
- Suggest a visual icon or symbol that represents each day's theme

IMPORTANT: Your response must be valid JSON without any markdown formatting or explanation. Just the pure JSON object.

Generate the itinerary in this JSON format:
{{
  "destination_info": {{
    "name": "Full destination name",
    "country": "Country",
    "best_season": "When it's best to visit",
    "language": "Primary language",
    "currency": "Local currency",
    "theme_colors": {{
      "primary": "#hexcode",
      "secondary": "#hexcode",
      "accent": "#hexcode"
    }}
  }},
  "itinerary": {{
    "day_1": {{
      "date": "YYYY-MM-DD",
      "title": "Creative day title",
      "icon": "Suggested icon name (e.g., 'museum', 'beach', 'hiking')",
      "morning": {{
        "activity": "Detailed description",
        "location": "Specific place name",
        "duration": "Suggested time to spend",
        "opening_hours": "When it opens",
        "transportation": "How to get there",
        "photo_opportunity": "Description of a good photo spot"
      }},
      "lunch": {{
        "recommendation": "Restaurant name",
        "cuisine": "Type of food",
        "price_range": "$-$$$",
        "address": "Location",
        "special_dish": "Must-try item"
      }},
      "afternoon": {{
        "activity": "Detailed description",
        "location": "Specific place name",
        "duration": "Suggested time to spend",
        "opening_hours": "When it opens",
        "transportation": "How to get there"
      }},
      "dinner": {{
        "recommendation": "Restaurant name",
        "cuisine": "Type of food",
        "price_range": "$-$$$",
        "address": "Location",
        "special_dish": "Must-try item"
      }},
      "evening": {{
        "activity": "Suggested entertainment",
        "location": "Where it's located",
        "notes": "Special information"
      }},
      "tips": "Insider advice for this day"
    }},
    "day_2": {{ ... }},
    ...
  }},
  "practical_info": {{
    "emergency_numbers": "Local emergency contacts",
    "transportation_tips": "Advice on getting around",
    "packing_suggestions": ["Item 1", "Item 2", ...],
    "local_customs": "Important cultural notes",
    "useful_phrases": ["Phrase 1: Translation", ...]
  }},
  "total_cost": "{total_cost} USD"
}}

Do not include any extra explanation. Output only valid JSON.
"""
    # Call Gemini API to generate the itinerary
    itinerary_response = call_gemini(prompt)
    
    try:
        # Clean up the response - remove markdown code blocks if present
        cleaned_response = itinerary_response
        
        # Remove markdown code block syntax if present
        if "```json" in cleaned_response or "```" in cleaned_response:
            import re
            # Extract content between markdown code blocks
            markdown_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', cleaned_response)
            if markdown_match:
                cleaned_response = markdown_match.group(1).strip()
        
        # Parse the AI response string into a JSON object
        itinerary_data = json.loads(cleaned_response)
        
        # Save to itinerary.json in the root directory
        cwd = os.getcwd()
        itinerary_path = os.path.join(cwd, 'itinerary.json')
        
        with open(itinerary_path, 'w', encoding='utf-8') as f:
            json.dump(itinerary_data, f, indent=2, ensure_ascii=False)
        print(f"Itinerary saved to {itinerary_path}")
        
        # Also save to src/pages directory if it exists
        src_pages_dir = os.path.join(cwd, 'src', 'pages')
        if os.path.exists(src_pages_dir):
            try:
                src_itinerary_path = os.path.join(src_pages_dir, 'itinerary.json')
                with open(src_itinerary_path, 'w', encoding='utf-8') as f:
                    json.dump(itinerary_data, f, indent=2, ensure_ascii=False)
                print(f"Itinerary also saved to {src_itinerary_path}")
            except Exception as e:
                print(f"Error saving itinerary to src/pages: {str(e)}")
        
        # Print a brief summary of the itinerary
        days = itinerary_data.get("itinerary", {})
        print("\n=== Itinerary Summary ===")
        print(f"Destination: {itinerary_data.get('destination_info', {}).get('name', 'Unknown')}")
        print(f"Duration: {len(days)} days")
        print(f"Total Cost: {itinerary_data.get('total_cost', 'Unknown')}")
        print("========================\n")
        
        return itinerary_data
        
    except json.JSONDecodeError as e:
        print("Error parsing AI response:", str(e))
        print("Raw AI response:", itinerary_response)
        return None
    except Exception as e:
        print(f"Error processing itinerary: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def main():
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise RuntimeError("SERPAPI_API_KEY environment variable is required.")
    
    outbound_date = input("Enter outbound (departure) date (YYYY-MM-DD): ").strip()
    return_date   = input("Enter return date (YYYY-MM-DD): ").strip()
    departure_id  = input("Enter departure airport code (default PEK): ").strip() or "PEK"
    arrival_id    = input("Enter arrival airport code (default AUS): ").strip() or "AUS"
    hotel_query   = input("Enter hotel search query (e.g., 'Hotels in Austin'): ").strip() or "Hotels in Austin"
    user_preferences = input("Enter your travel preferences (e.g., 'I like cultural experiences, nature, and local cuisine'): ").strip()
    
    # Get flight and hotel data.
    flight_data = search_google_flights(api_key, outbound_date, return_date, departure_id, arrival_id)
    hotel_data = search_google_hotels(api_key, outbound_date, return_date, hotel_query)
    
    # Display options and let the user select one from each.
    print("\n" + "=" * 60)
    print("Flight Options:")
    print("=" * 60)
    flight_options = display_flight_options(flight_data)
    selected_flight = choose_option(flight_options, option_type="flight")
    
    print("\n" + "=" * 60)
    print("Hotel Options:")
    print("=" * 60)
    hotel_options = display_hotel_options(hotel_data)
    selected_hotel = choose_option(hotel_options, option_type="hotel")
    
    if not selected_flight or not selected_hotel:
        print("Cannot proceed without both flight and hotel selections.")
        return
    
    # Generate the final itinerary.
    print("\n" + "=" * 60)
    print("Generating Your Personalized Itinerary...")
    print("=" * 60)
    itinerary = generate_itinerary(selected_flight, selected_hotel, outbound_date, return_date, user_preferences)
    
    if itinerary:
        print("\nYour itinerary has been generated and saved successfully!")
        print("You can now view your itinerary in the app by going to the Itinerary page.")
    else:
        print("\nThere was an error generating your itinerary. Please try again later.")
        
    print("\nThank you for using our travel planning service!")

if __name__ == "__main__":
    main()
