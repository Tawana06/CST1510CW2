import os
from dotenv import load_dotenv
from google import genai
load_dotenv("C:/Users/gwati/PycharmProjects/newproject/CW2_M01018151_CST1510/apikey.env")
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key= api_key)

while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        print("Goodbye!")
        break

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[user_input],)


    print(f"AI: {response.text}")