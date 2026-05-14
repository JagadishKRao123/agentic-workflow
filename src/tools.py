"""
Tool definitions and registry for agents
"""

import json
import logging
from typing import Callable, Dict, List, Any, Optional
from datetime import datetime
import math

logger = logging.getLogger(__name__)


class Tool:
    """Base Tool class"""
    
    def __init__(
        self,
        name: str,
        description: str,
        func: Callable,
        parameters: Dict[str, Any],
    ):
        """
        Initialize a Tool
        
        Args:
            name: Tool name
            description: Tool description
            func: The actual function to execute
            parameters: Parameter definitions (OpenAI format)
        """
        self.name = name
        self.description = description
        self.func = func
        self.parameters = parameters
    
    def execute(self, **kwargs) -> str:
        """Execute the tool with given parameters"""
        try:
            logger.info(f"Executing tool: {self.name} with args: {kwargs}")
            result = self.func(**kwargs)
            logger.info(f"Tool result: {result}")
            return str(result)
        except Exception as e:
            logger.error(f"Error executing tool {self.name}: {e}")
            return f"Error: {str(e)}"
    
    def to_openai_format(self) -> Dict[str, Any]:
        """Convert tool to OpenAI format"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            }
        }


class ToolRegistry:
    """Registry for managing tools"""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self._register_builtin_tools()
    
    def register(
        self,
        name: str,
        description: str,
        func: Callable,
        parameters: Dict[str, Any],
    ):
        """Register a new tool"""
        tool = Tool(name, description, func, parameters)
        self.tools[name] = tool
        logger.info(f"Registered tool: {name}")
        return tool
    
    def get(self, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self.tools.get(name)
    
    def execute(self, name: str, **kwargs) -> str:
        """Execute a tool by name"""
        tool = self.get(name)
        if not tool:
            return f"Tool '{name}' not found"
        return tool.execute(**kwargs)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """Get list of all tools in OpenAI format"""
        return [tool.to_openai_format() for tool in self.tools.values()]
    
    def get_tool_names(self) -> List[str]:
        """Get list of all tool names"""
        return list(self.tools.keys())
    
    def _register_builtin_tools(self):
        """Register built-in tools"""
        
        # Math operations
        self.register(
            name="calculate",
            description="Perform mathematical calculations. Supports +, -, *, /, **, %, etc.",
            func=self._calculate,
            parameters={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '5 + 3', '2 ** 8')"
                    }
                },
                "required": ["expression"]
            }
        )
        
        # String operations
        self.register(
            name="string_analysis",
            description="Analyze string properties like length, word count, unique characters",
            func=self._string_analysis,
            parameters={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to analyze"
                    },
                    "analysis_type": {
                        "type": "string",
                        "description": "Type of analysis: 'length', 'word_count', 'char_analysis', 'all'",
                        "enum": ["length", "word_count", "char_analysis", "all"]
                    }
                },
                "required": ["text", "analysis_type"]
            }
        )
        
        # Data processing
        self.register(
            name="list_operations",
            description="Perform operations on lists like sort, reverse, remove duplicates",
            func=self._list_operations,
            parameters={
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of items to process"
                    },
                    "operation": {
                        "type": "string",
                        "description": "Operation to perform",
                        "enum": ["sort", "reverse", "unique", "count", "statistics"]
                    }
                },
                "required": ["items", "operation"]
            }
        )
        
        # Time operations
        self.register(
            name="get_current_time",
            description="Get current date and time",
            func=self._get_current_time,
            parameters={
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "description": "Format type: 'full', 'date_only', 'time_only'",
                        "enum": ["full", "date_only", "time_only"]
                    }
                },
                "required": ["format"]
            }
        )
        
        # Code analysis
        self.register(
            name="code_analyzer",
            description="Analyze Python code for issues and suggestions",
            func=self._code_analyzer,
            parameters={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to analyze"
                    },
                    "check_type": {
                        "type": "string",
                        "description": "Type of check to perform",
                        "enum": ["syntax", "complexity", "style", "all"]
                    }
                },
                "required": ["code", "check_type"]
            }
        )
    
    # Built-in tool implementations
    
    @staticmethod
    def _calculate(expression: str) -> str:
        """Safely evaluate mathematical expressions"""
        try:
            # Only allow safe math operations
            allowed_names = {
                'abs': abs, 'round': round, 'min': min, 'max': max,
                'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos,
                'tan': math.tan, 'pi': math.pi, 'e': math.e,
            }
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return f"Result: {result}"
        except Exception as e:
            return f"Calculation error: {str(e)}"
    
    @staticmethod
    def _string_analysis(text: str, analysis_type: str) -> str:
        """Analyze string properties"""
        results = {}
        
        if analysis_type in ["length", "all"]:
            results["length"] = len(text)
        
        if analysis_type in ["word_count", "all"]:
            results["word_count"] = len(text.split())
        
        if analysis_type in ["char_analysis", "all"]:
            results["unique_chars"] = len(set(text))
            results["spaces"] = text.count(" ")
        
        return json.dumps(results, indent=2)
    
    @staticmethod
    def _list_operations(items: List[str], operation: str) -> str:
        """Perform operations on lists"""
        if operation == "sort":
            return sorted(items)
        elif operation == "reverse":
            return list(reversed(items))
        elif operation == "unique":
            return list(set(items))
        elif operation == "count":
            return f"List contains {len(items)} items"
        elif operation == "statistics":
            return {
                "total_items": len(items),
                "unique_items": len(set(items)),
                "first": items[0] if items else None,
                "last": items[-1] if items else None,
            }
        return "Unknown operation"
    
    @staticmethod
    def _get_current_time(format: str) -> str:
        """Get current date and time"""
        now = datetime.now()
        if format == "full":
            return now.strftime("%Y-%m-%d %H:%M:%S")
        elif format == "date_only":
            return now.strftime("%Y-%m-%d")
        elif format == "time_only":
            return now.strftime("%H:%M:%S")
        return "Invalid format"
    
    @staticmethod
    def _code_analyzer(code: str, check_type: str) -> str:
        """Analyze Python code"""
        results = {}
        
        if check_type in ["syntax", "all"]:
            try:
                compile(code, '<string>', 'exec')
                results["syntax"] = "Valid Python syntax"
            except SyntaxError as e:
                results["syntax"] = f"Syntax error: {e}"
        
        if check_type in ["complexity", "all"]:
            results["lines"] = len(code.split('\n'))
            results["functions"] = code.count('def ')
            results["classes"] = code.count('class ')
        
        if check_type in ["style", "all"]:
            results["style_notes"] = [
                "Consider using meaningful variable names",
                "Keep functions small and focused",
                "Add docstrings to functions"
            ]
        
        return json.dumps(results, indent=2)
