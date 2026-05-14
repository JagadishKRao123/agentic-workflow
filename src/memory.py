"""
Memory management for agents
"""

import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class Memory:
    """Agent memory for storing context and history"""
    
    def __init__(self, max_history: int = 50):
        """
        Initialize Memory
        
        Args:
            max_history: Maximum number of messages to keep in history
        """
        self.max_history = max_history
        self.messages: List[Dict[str, Any]] = []
        self.task_context: Dict[str, Any] = {}
        self.tool_results: List[Dict[str, Any]] = []
        self.decisions: List[Dict[str, Any]] = []
    
    def add_message(self, role: str, content: str, timestamp: Optional[str] = None):
        """
        Add a message to memory
        
        Args:
            role: Message role (user, assistant, system)
            content: Message content
            timestamp: Optional timestamp (auto-generated if not provided)
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        message = {
            "role": role,
            "content": content,
            "timestamp": timestamp
        }
        self.messages.append(message)
        
        # Keep only recent messages
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
        
        logger.debug(f"Added message: {role} - {content[:50]}...")
    
    def add_tool_result(self, tool_name: str, input_params: Dict, result: str):
        """
        Record a tool execution result
        
        Args:
            tool_name: Name of the tool
            input_params: Parameters passed to tool
            result: Result from tool execution
        """
        tool_result = {
            "tool": tool_name,
            "params": input_params,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        self.tool_results.append(tool_result)
        logger.debug(f"Recorded tool result: {tool_name}")
    
    def add_decision(self, decision: str, reasoning: str, alternatives: Optional[List[str]] = None):
        """
        Record an agent decision
        
        Args:
            decision: The decision made
            reasoning: Reasoning behind the decision
            alternatives: Alternative options considered
        """
        decision_record = {
            "decision": decision,
            "reasoning": reasoning,
            "alternatives": alternatives or [],
            "timestamp": datetime.now().isoformat()
        }
        self.decisions.append(decision_record)
        logger.debug(f"Recorded decision: {decision}")
    
    def set_task_context(self, context: Dict[str, Any]):
        """Set task context"""
        self.task_context = context
        logger.debug(f"Set task context: {json.dumps(context, indent=2)}")
    
    def get_task_context(self) -> Dict[str, Any]:
        """Get task context"""
        return self.task_context.copy()
    
    def get_messages(self) -> List[Dict[str, str]]:
        """Get all messages for LLM (role and content only)"""
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.messages
        ]
    
    def get_recent_messages(self, count: int = 5) -> List[Dict[str, Any]]:
        """Get recent messages"""
        return self.messages[-count:]
    
    def get_tool_results(self) -> List[Dict[str, Any]]:
        """Get all tool results"""
        return self.tool_results.copy()
    
    def get_decisions(self) -> List[Dict[str, Any]]:
        """Get all decisions"""
        return self.decisions.copy()
    
    def get_summary(self) -> str:
        """Get a summary of memory state"""
        summary = {
            "total_messages": len(self.messages),
            "total_tool_uses": len(self.tool_results),
            "total_decisions": len(self.decisions),
            "task_context": self.task_context,
            "recent_messages": self.messages[-3:] if self.messages else [],
        }
        return json.dumps(summary, indent=2)
    
    def clear(self):
        """Clear all memory"""
        self.messages = []
        self.task_context = {}
        self.tool_results = []
        self.decisions = []
        logger.info("Memory cleared")
    
    def export(self) -> Dict[str, Any]:
        """Export memory state"""
        return {
            "messages": self.messages,
            "task_context": self.task_context,
            "tool_results": self.tool_results,
            "decisions": self.decisions,
        }
    
    def import_memory(self, data: Dict[str, Any]):
        """Import memory state"""
        self.messages = data.get("messages", [])
        self.task_context = data.get("task_context", {})
        self.tool_results = data.get("tool_results", [])
        self.decisions = data.get("decisions", [])
        logger.info("Memory imported")
