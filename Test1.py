import json
import textwrap

def print_hotel(hotel, index):
    # Extract key details with defaults
    hotel_type = hotel.get('type', 'N/A')
    name = hotel.get('name', 'N/A')
    description = hotel.get('description', 'N/A')
    link = hotel.get('link', 'N/A')
    check_in = hotel.get('check_in_time', 'N/A')
    check_out = hotel.get('check_out_time', 'N/A')
    rate_info = hotel.get('rate_per_night', {})
    rate = rate_info.get('lowest', 'N/A')
    overall_rating = hotel.get('overall_rating', 'N/A')
    reviews = hotel.get('reviews', 'N/A')
    amenities = hotel.get('amenities', [])
    
    # Print the information
    print(f"Hotel {index}: {name}")
    print(f"  Type: {hotel_type}")
    print("  Description:")
    print(textwrap.fill(description, width=70, initial_indent="    ", subsequent_indent="    "))
    print(f"  Link: {link}")
    print(f"  Check-in: {check_in} | Check-out: {check_out}")
    print(f"  Rate per Night: {rate}")
    print(f"  Overall Rating: {overall_rating} (based on {reviews} reviews)")
    if amenities:
        print("  Amenities: " + ", ".join(amenities))
    else:
        print("  Amenities: N/A")
    print("-" * 80)

def display_hotels(data):
    # The JSON output should have a key "properties" that contains a list of hotels
    properties = data.get("properties", [])
    total_results = data.get("search_information", {}).get("total_results", "N/A")
    print(f"Total Results Found: {total_results}\n")
    
    if not properties:
        print("No hotel properties found.")
        return

    for idx, hotel in enumerate(properties, start=1):
        print_hotel(hotel, idx)

if __name__ == '__main__':
    # Replace 'hotels.json' with the file containing your JSON output or load it from another source.
    with open("test.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    display_hotels(data)
