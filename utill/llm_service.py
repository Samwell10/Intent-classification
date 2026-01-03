import os
from anthropic import Anthropic
from typing import Optional

class ClaudeLLMService:
    """
    Service for generating personalized customer service responses using Claude.
    Uses the detected intent and predefined context to generate natural, helpful responses.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Claude client.

        Args:
            api_key: Anthropic API key. If None, reads from ANTHROPIC_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-5-20250929"  # Claude Sonnet 4.5 (latest)

    def generate_response(
        self,
        user_query: str,
        detected_intent: str,
        template_response: str,
        max_tokens: int = 300
    ) -> str:
        """
        Generate a personalized response using Claude based on the detected intent.

        Args:
            user_query: The original user message
            detected_intent: The intent detected by your ML model
            template_response: The template response from response.json
            max_tokens: Maximum tokens in the response

        Returns:
            Personalized response from Claude
        """

        system_prompt = """You are a helpful banking customer service assistant.
Your job is to provide clear, friendly, and professional responses to customer queries.

Guidelines:
- Be concise but thorough
- Use a warm, professional tone
- Address the specific question asked
- If the template provides key information, incorporate it naturally
- Don't make up information - stick to what's provided
- Keep responses under 100 words unless more detail is needed
"""

        user_prompt = f"""The customer asked: "{user_query}"

We've identified this as a "{detected_intent}" query.

Our standard response template says: "{template_response}"

Please generate a personalized, natural response that:
1. Directly addresses their specific question
2. Incorporates the key information from the template
3. Sounds conversational and helpful
4. Matches the tone of a professional banking support agent

Response:"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            # Extract text from the response
            response_text = message.content[0].text
            return response_text.strip()

        except Exception as e:
            # Fallback to template response if LLM fails
            print(f"LLM generation failed: {e}")
            return template_response

    def generate_contextual_response(
        self,
        user_query: str,
        conversation_history: Optional[list] = None,
        max_tokens: int = 300
    ) -> str:
        """
        Generate a response with conversation context (for future use).

        Args:
            user_query: The current user message
            conversation_history: List of previous messages [{"role": "user"/"assistant", "content": "..."}]
            max_tokens: Maximum tokens in the response

        Returns:
            Contextual response from Claude
        """
        system_prompt = """You are a helpful banking customer service assistant.
Provide clear, accurate, and professional responses to customer queries."""

        messages = conversation_history or []
        messages.append({"role": "user", "content": user_query})

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=messages
            )

            return message.content[0].text.strip()

        except Exception as e:
            print(f"LLM generation failed: {e}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again or contact support."
