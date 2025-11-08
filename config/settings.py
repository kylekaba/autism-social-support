"""
Configuration settings for Autism Social Support Application
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

# Expression Recognition Settings
EXPRESSION_UPDATE_INTERVAL = int(os.getenv("EXPRESSION_UPDATE_INTERVAL", "10"))

# Supported emotions (from Py-Feat)
EMOTIONS = ["happiness", "sadness", "surprise", "anger", "disgust", "fear", "neutral"]

# Emoticon mappings
EMOTICON_MAP = {
    "happiness": "😊",
    "sadness": "😢",
    "surprise": "😮",
    "anger": "😠",
    "disgust": "🤢",
    "fear": "😨",
    "neutral": "😐"
}

# GUI Settings
WINDOW_TITLE = "Karitas"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Response generation settings
MAX_RESPONSE_LENGTH = 50  # Keep responses short for children
SYSTEM_PROMPT_TEMPLATE = """You are a helpful assistant supporting an autistic child during a conversation.
Based on the conversation context and the other person's facial expression, suggest an appropriate response
for the child to say. Keep your suggestion to ONE sentence or just a few words to avoid overwhelming the child.

Child's Profile:
- Age: {age}
- Autism Level: {autism_level}
- Communication Capabilities: {communication_capabilities}

Current facial expression of conversation partner: {expression}
"""
