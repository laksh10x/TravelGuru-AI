# TravelGuru AI

TravelGuru AI is an AI-powered travel planning assistant that turns trip preferences into destination recommendations, flight and hotel search data, and day-by-day itinerary drafts. The project combines conversational AI, travel data APIs, backend orchestration, and structured JSON outputs to make trip planning faster and more personalized.

## What It Does

- Guides travelers through a short preference-gathering conversation.
- Recommends destinations based on interests, budget, timing, and travel style.
- Uses Gemini-powered prompts to generate structured travel recommendations and itinerary content.
- Integrates SerpApi-powered Google Flights and Google Hotels searches.
- Saves flight, hotel, recommendation, and itinerary data as JSON for downstream UI usage.
- Includes focused test scripts for API integration, itinerary generation, and selection processing.

## Highlights

TravelGuru AI highlights advanced knowledge across data science, software engineering, AI systems, and applied product development. The project reflects strengths in data-driven decision making, API integration, backend design, prompt engineering, feature engineering, and translating messy real-world travel inputs into structured, usable outputs.

This blend of data science and engineering matters because travel planning is not just a UI problem. It requires extracting signals from user preferences, coordinating multiple external systems, handling incomplete or changing data, and producing recommendations that are clear enough for people and structured enough for software.

## Tech Stack

- Python for travel data orchestration and itinerary generation.
- Flask and Flask-CORS for backend API endpoints.
- Google Gemini for conversational recommendations and itinerary text.
- SerpApi for Google Flights and Google Hotels data.
- React dependencies for frontend integration.
- JSON artifacts for recommendation, flight, hotel, and itinerary outputs.

## Project Structure

```text
chatbot.py                      Interactive Gemini travel assistant prototype
main.py                         Flight, hotel, recommendation, and itinerary logic
server.py                       Flask API for chat and travel-data workflows
test_*.py                       Integration and workflow test scripts
*.json                          Sample/generated recommendation and travel data
package.json                    Frontend dependency and script configuration
package-lock.json               Locked JavaScript dependency versions
```

## Environment Variables

Create local environment variables before running API-backed workflows:

```bash
GEMINI_API_KEY=your_gemini_key
SERPAPI_API_KEY=your_serpapi_key
```

These keys are intentionally read from the environment instead of being stored in source control.

## Getting Started

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Install JavaScript dependencies:

```bash
npm install
```

Run the Flask API:

```bash
python server.py
```

Run the React development script when frontend files are present:

```bash
npm start
```

## Notes

TravelGuru AI currently includes API orchestration code, backend endpoints, test workflows, and example JSON outputs. External API calls require valid Gemini and SerpApi credentials.
