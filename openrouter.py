import os
import logging
from openai import OpenAI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Connect to OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MAX_INPUT_LENGTH = 500

def validate_input(message):
    if not isinstance(message, str): #if input is not a string
        return False
    if len(message) > MAX_INPUT_LENGTH: #if message exceeds the max length
        return False
    if not message.strip(): #check if the message is empty or only contains whitespace
        return False

    return True


def chatbot(message):
    # Input validation
    if not validate_input(message):
        logger.warning("Invalid input received for chatbot.")
        return "Invalid input."

    try:
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant whose purpose is to help users with their file upload and other queries related to the application."
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            max_completion_tokens=500, 
        )
        # Response validation
        if not response.choices:
            logger.error("OpenRouter returned no response choices.")
            return "No response received."

        content = response.choices[0].message.content

        if not content or not content.strip():
            logger.error("OpenRouter returned an empty response.")
            return "No response received."

        return content
    except Exception as e:
        # Do not expose detailed API errors to the user
        logger.error(f"OpenRouter API request failed: {e}")
        return "The chatbot service is currently unavailable."


message = input("You: ")
response = chatbot(message)

print("Chatbot:", response)