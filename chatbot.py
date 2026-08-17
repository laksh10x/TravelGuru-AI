import google.generativeai as genai
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable is required.")

# -----------------------------
# Part 3: Set Up Google Gemini API
# -----------------------------
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# -----------------------------
# Part 4: Chatbot Loop with Refined Prompt Instructions
# -----------------------------
print("Chatbot is ready. Type 'exit' to quit.")
conversation_history = ""

# Define refined prompt instructions for your study buddy
prompt_instructions = (
   """You are a friendly travel recommendation assistant. Your goal is to have a natural, interactive conversation with the user to learn about their travel preferences. Start by asking broad, open-ended questions such as: "What type of travel experience are you looking for?" or "Do you prefer cultural experiences, adventure, relaxation, or nature?" As the conversation continues, ask follow-up questions to clarify details like their preferred climate, travel duration, budget, and any special interests (for example, local cuisine, historical sites, outdoor activities, or art).

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
      "reason": "<Why this destination fits the user's preferences>",
      "estimated_cost_range": "<Approximate cost range for a typical trip>"
    },
    ... (more destinations)
  ]
}

Begin by asking: "What type of travel experience are you most excited about?" and use the conversation to fill in the slots. Once all required details are captured, output only the final JSON.
"""
)

while True:
    response = gemini_model.generate_content(prompt_instructions)
    ai_response = response.text.strip()
        
    print("Assistant:", ai_response)


    user_query = input("You: ")
    if user_query.lower() == "exit":
        break


    prompt_instructions = (
        f"{prompt_instructions}\n\n"
        f"User: {user_query}\n"
        f"AI: {ai_response}\n"
    )
    
