"""LLM integration with Google Gemini API."""

import google.generativeai as genai
from typing import List, Dict, Optional
import streamlit as st

from config.settings import settings


class GeminiChatbot:
    """Gemini-based chatbot for Boeing India career guidance."""
    
    SYSTEM_PROMPT = """You are a friendly and professional career guidance chatbot for engineering students in India, 
specializing in Boeing India opportunities. Your role is to help students learn about:

1. Boeing India company insights and culture
2. Placement processes and requirements
3. Internship opportunities
4. Job roles and responsibilities
5. Career paths at Boeing India
6. Resume tips for Boeing India applications
7. Interview preparation for Boeing India
8. Skill-building recommendations for Boeing India roles
9. Project suggestions relevant to Boeing India

Guidelines:
- Be friendly, encouraging, and approachable like an engineering mentor
- Switch to formal-professional tone when discussing official processes
- Provide accurate, up-to-date information about Boeing India
- If you don't have specific information, acknowledge it and suggest where to find it
- Guide users through multi-step queries naturally
- Remember context from previous messages in the conversation
- Encourage students and provide actionable advice
- Stay on-topic - focus on Boeing India and career guidance
- Provide links to relevant resources when available

Target audience: Engineering students in India interested in Boeing India careers.

Always be helpful, accurate, and encouraging!"""
    
    def __init__(self):
        """Initialize Gemini chatbot."""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
    def generate_response(
        self, 
        user_message: str, 
        conversation_history: List[Dict[str, str]],
        context: Optional[str] = None
    ) -> str:
        """Generate response using Gemini API.
        
        Args:
            user_message: The user's current message
            conversation_history: List of previous messages [{"role": "user/assistant", "content": "..."}]
            context: Additional context from knowledge base
            
        Returns:
            Generated response from the model
        """
        try:
            # Build conversation context
            prompt_parts = [self.SYSTEM_PROMPT]
            
            # Add knowledge base context if available
            if context:
                prompt_parts.append(f"\n\nRelevant Context:\n{context}\n")
            
            # Add conversation history (limited to recent messages)
            if conversation_history:
                prompt_parts.append("\n\nConversation History:")
                for msg in conversation_history[-settings.MAX_HISTORY_MESSAGES:]:
                    role = "Student" if msg["role"] == "user" else "Assistant"
                    prompt_parts.append(f"{role}: {msg['content']}")
            
            # Add current user message
            prompt_parts.append(f"\n\nStudent: {user_message}")
            prompt_parts.append("\nAssistant:")
            
            # Generate response
            full_prompt = "\n".join(prompt_parts)
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=settings.TEMPERATURE,
                    max_output_tokens=settings.MAX_TOKENS,
                )
            )
            
            return response.text
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again in a moment."
    
    def generate_conversation_title(self, first_message: str) -> str:
        """Generate a title for the conversation based on the first message."""
        try:
            prompt = f"Generate a short, descriptive title (max 50 characters) for a conversation that starts with: '{first_message[:100]}'"
            response = self.model.generate_content(prompt)
            title = response.text.strip().replace('"', '').replace("'", "")
            return title[:100]  # Limit length
        except Exception:
            return first_message[:50] + "..." if len(first_message) > 50 else first_message


chatbot = GeminiChatbot()
