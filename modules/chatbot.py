"""
LLM-Based Chatbot Module
Uses OpenAI's GPT models to generate appropriate conversation responses
"""
from openai import OpenAI
from config.settings import OPENAI_API_KEY, MODEL_NAME, SYSTEM_PROMPT_TEMPLATE


class ResponseGenerator:
    """Generates socially appropriate responses using GPT-4o-mini"""

    def __init__(self, child_profile=None):
        """
        Initialize the chatbot

        Args:
            child_profile: Dictionary containing child's information
                          (age, autism_level, communication_capabilities)
        """
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = MODEL_NAME
        self.conversation_history = []
        self.child_profile = child_profile or {
            "age": "not specified",
            "autism_level": "not specified",
            "communication_capabilities": "not specified"
        }

        print(f"✓ Response generator initialized with model: {self.model}")

    def set_child_profile(self, age, autism_level, communication_capabilities):
        """
        Update child's profile

        Args:
            age: Child's age
            autism_level: Level of autism (e.g., "Level 1", "Level 2", "Level 3")
            communication_capabilities: Description of communication abilities
        """
        self.child_profile = {
            "age": age,
            "autism_level": autism_level,
            "communication_capabilities": communication_capabilities
        }

    def generate_response(self, transcript, current_expression):
        """
        Generate an appropriate response based on conversation context and facial expression

        Args:
            transcript: String containing the conversation transcript (can be empty)
            current_expression: Current facial expression of the conversation partner

        Returns:
            str: Suggested response for the child
        """
        try:
            # Create system prompt with child's profile
            system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
                age=self.child_profile["age"],
                autism_level=self.child_profile["autism_level"],
                communication_capabilities=self.child_profile["communication_capabilities"],
                expression=current_expression
            )

            # For first request, start new conversation
            if not self.conversation_history:
                self.conversation_history = [
                    {"role": "system", "content": system_prompt}
                ]

            # Add user message with transcript and expression
            if transcript and transcript.strip():
                user_message = f"Conversation so far:\n{transcript}\n\nThe other person's current expression is: {current_expression}\n\nSuggest a brief, appropriate response for the child."
            else:
                # No transcript available, focus on expression
                user_message = f"The person the child is talking to has a {current_expression} expression on their face. Suggest a brief, appropriate response or conversation starter for the child."

            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                max_tokens=50,
                temperature=0.7
            )

            # Extract the response
            suggested_response = response.choices[0].message.content.strip()

            # Add assistant's response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": suggested_response
            })

            return suggested_response

        except Exception as e:
            print(f"✗ Error generating response: {e}")
            return "I'm not sure what to say right now."

    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = []
        print("Conversation history cleared")

    def get_conversation_length(self):
        """Get the number of messages in conversation history"""
        return len(self.conversation_history)
