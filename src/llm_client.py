"""
LLM Client for interacting with OpenAI API
"""

import os
import json
from typing import Optional, List, Dict, Any
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for OpenAI API interactions"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4",
        temperature: float = 0.7,
    ):
        """
        Initialize LLM Client
        
        Args:
            api_key: OpenAI API key (uses OPENAI_API_KEY env var if not provided)
            model: Model to use (default: gpt-4)
            temperature: Temperature for response generation (default: 0.7)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.temperature = temperature
        self.conversation_history = []
        
    def call(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Call the LLM with messages and optional tools
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            tools: List of tool definitions (OpenAI format)
            temperature: Override default temperature
            
        Returns:
            Response from the LLM
        """
        try:
            temperature = temperature or self.temperature
            
            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
            }
            
            if tools:
                kwargs["tools"] = tools
                kwargs["tool_choice"] = "auto"
            
            logger.info(f"Calling {self.model} with {len(messages)} messages")
            
            response = self.client.chat.completions.create(**kwargs)
            
            return {
                "content": response.choices[0].message.content,
                "tool_calls": response.choices[0].message.tool_calls,
                "finish_reason": response.choices[0].finish_reason,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                }
            }
        except Exception as e:
            logger.error(f"Error calling LLM: {e}")
            raise
    
    def add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get current conversation history"""
        return self.conversation_history.copy()
