"""
Unit tests for the Agent framework
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import Agent
from src.tools import ToolRegistry
from src.memory import Memory
from src.llm_client import LLMClient


class TestToolRegistry:
    """Test ToolRegistry functionality"""
    
    def test_builtin_tools_registered(self):
        """Test that built-in tools are registered"""
        registry = ToolRegistry()
        tool_names = registry.get_tool_names()
        
        assert "calculate" in tool_names
        assert "string_analysis" in tool_names
        assert "list_operations" in tool_names
        assert "get_current_time" in tool_names
        assert "code_analyzer" in tool_names
    
    def test_calculate_tool(self):
        """Test calculate tool"""
        registry = ToolRegistry()
        result = registry.execute("calculate", expression="5 + 3")
        assert "8" in result
    
    def test_string_analysis_tool(self):
        """Test string analysis tool"""
        registry = ToolRegistry()
        result = registry.execute(
            "string_analysis",
            text="hello world",
            analysis_type="word_count"
        )
        assert "2" in result
    
    def test_list_operations_tool(self):
        """Test list operations tool"""
        registry = ToolRegistry()
        result = registry.execute(
            "list_operations",
            items=["apple", "banana", "apple"],
            operation="unique"
        )
        assert "apple" in result and "banana" in result


class TestMemory:
    """Test Memory functionality"""
    
    def test_add_message(self):
        """Test adding messages to memory"""
        memory = Memory()
        memory.add_message("user", "Hello")
        
        messages = memory.get_messages()
        assert len(messages) == 1
        assert messages[0]["role"] == "user"
        assert messages[0]["content"] == "Hello"
    
    def test_task_context(self):
        """Test task context management"""
        memory = Memory()
        context = {"task": "test", "priority": "high"}
        memory.set_task_context(context)
        
        retrieved = memory.get_task_context()
        assert retrieved["task"] == "test"
        assert retrieved["priority"] == "high"
    
    def test_tool_result_recording(self):
        """Test recording tool results"""
        memory = Memory()
        memory.add_tool_result("calculate", {"expr": "2+2"}, "4")
        
        results = memory.get_tool_results()
        assert len(results) == 1
        assert results[0]["tool"] == "calculate"
    
    def test_memory_clear(self):
        """Test clearing memory"""
        memory = Memory()
        memory.add_message("user", "test")
        memory.clear()
        
        messages = memory.get_messages()
        assert len(messages) == 0


class TestAgent:
    """Test Agent functionality"""
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        agent = Agent(name="TestBot")
        
        assert agent.name == "TestBot"
        assert agent.llm is not None
        assert agent.tools is not None
        assert agent.memory is not None
    
    def test_custom_tool_registration(self):
        """Test registering custom tools"""
        agent = Agent()
        
        def custom_add(a: int, b: int) -> int:
            return a + b
        
        agent.register_tool(
            name="custom_add",
            description="Add two numbers",
            func=custom_add,
            parameters={
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"}
                },
                "required": ["a", "b"]
            }
        )
        
        tool_names = agent.tools.get_tool_names()
        assert "custom_add" in tool_names
    
    def test_memory_summary(self):
        """Test getting memory summary"""
        agent = Agent()
        summary = agent.get_memory_summary()
        
        assert "total_messages" in summary
        assert "total_tool_uses" in summary
        assert "total_decisions" in summary


class TestLLMClient:
    """Test LLMClient functionality"""
    
    def test_client_initialization(self):
        """Test LLM client initialization"""
        # This test requires OPENAI_API_KEY to be set
        # Skipping if not available
        import os
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")
        
        client = LLMClient(model="gpt-4")
        assert client.model == "gpt-4"
    
    def test_message_history(self):
        """Test message history management"""
        # Skip if API key not available
        import os
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")
        
        client = LLMClient()
        client.add_to_history("user", "Hello")
        
        history = client.get_history()
        assert len(history) == 1
        assert history[0]["content"] == "Hello"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
