"""
Core Agent implementation for agentic workflows
"""

import json
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
import os

from .llm_client import LLMClient
from .tools import ToolRegistry
from .memory import Memory

# Setup logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Agent:
    """
    Autonomous Agent that can plan, execute tools, and learn
    """
    
    def __init__(
        self,
        name: str = "Agent",
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_iterations: int = 10,
        verbose: bool = True,
    ):
        """
        Initialize an Agent
        
        Args:
            name: Agent name
            model: LLM model to use
            temperature: Temperature for LLM responses
            max_iterations: Maximum iterations for task execution
            verbose: Enable verbose logging
        """
        self.name = name
        self.model = model
        self.temperature = temperature
        self.max_iterations = max_iterations
        self.verbose = verbose
        
        # Initialize components
        self.llm = LLMClient(model=model, temperature=temperature)
        self.tools = ToolRegistry()
        self.memory = Memory()
        
        logger.info(f"Initialized agent: {name}")
    
    def run(self, task: str) -> str:
        """
        Execute a task
        
        Args:
            task: The task/goal to accomplish
            
        Returns:
            Final result or conclusion
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Agent '{self.name}' starting task: {task}")
        logger.info(f"{'='*60}\n")
        
        # Clear memory and set up context
        self.memory.clear()
        self.memory.set_task_context({
            "task": task,
            "start_time": datetime.now().isoformat(),
            "status": "in_progress"
        })
        
        # Add system message
        system_message = self._build_system_message()
        self.memory.add_message("system", system_message)
        
        # Add user task
        self.memory.add_message("user", task)
        
        # Main agent loop
        iteration = 0
        final_result = None
        
        while iteration < self.max_iterations:
            iteration += 1
            
            if self.verbose:
                logger.info(f"\n--- Iteration {iteration}/{self.max_iterations} ---")
            
            # Get LLM response
            response = self._get_llm_response()
            
            if not response:
                break
            
            # Add assistant response to memory
            self.memory.add_message("assistant", response.get("content", ""))
            
            # Check if task is complete
            finish_reason = response.get("finish_reason")
            
            if finish_reason == "stop":
                # No tool calls, task complete
                final_result = response.get("content")
                logger.info("Task completed - LLM finished response")
                break
            
            if finish_reason == "tool_calls":
                # Execute tool calls
                tool_calls = response.get("tool_calls")
                
                if not tool_calls:
                    final_result = response.get("content")
                    break
                
                # Process each tool call
                for tool_call in tool_calls:
                    self._process_tool_call(tool_call)
            
            if self.verbose:
                logger.info(f"Iteration {iteration} completed")
        
        # Finalize
        context = self.memory.get_task_context()
        context["status"] = "completed"
        context["end_time"] = datetime.now().isoformat()
        context["iterations"] = iteration
        self.memory.set_task_context(context)
        
        if final_result is None:
            final_result = "Task execution completed (max iterations reached)"
        
        logger.info(f"\n{'='*60}")
        logger.info(f"FINAL RESULT:\n{final_result}")
        logger.info(f"{'='*60}\n")
        
        return final_result
    
    def _build_system_message(self) -> str:
        """Build the system prompt for the agent"""
        tool_names = self.tools.get_tool_names()
        tool_list = "\n".join([f"- {name}" for name in tool_names])
        
        system_prompt = f"""You are {self.name}, an autonomous AI agent.

Your goal is to help users complete tasks by thinking through problems and using available tools.

IMPORTANT INSTRUCTIONS:
1. Analyze the task carefully
2. Break down complex tasks into steps
3. Use tools when needed to gather information or perform calculations
4. Think before acting - explain your reasoning
5. Verify tool results and adjust your approach if needed
6. Continue until the task is fully completed
7. Provide a clear final answer

AVAILABLE TOOLS:
{tool_list}

When using tools:
- Call tools with exact parameter names
- Analyze the results carefully
- Ask follow-up questions if needed
- Adapt your strategy based on results

Always be thorough and accurate in your responses."""
        
        return system_prompt
    
    def _get_llm_response(self) -> Optional[Dict[str, Any]]:
        """Get response from LLM"""
        try:
            messages = self.memory.get_messages()
            tools = self.tools.list_tools()
            
            if self.verbose:
                logger.debug(f"Sending {len(messages)} messages to LLM")
            
            response = self.llm.call(
                messages=messages,
                tools=tools if tools else None,
                temperature=self.temperature,
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting LLM response: {e}")
            return None
    
    def _process_tool_call(self, tool_call: Any):
        """Process a tool call from the LLM"""
        try:
            tool_name = tool_call.function.name
            tool_args_str = tool_call.function.arguments
            
            # Parse arguments
            try:
                tool_args = json.loads(tool_args_str)
            except json.JSONDecodeError:
                tool_args = {"input": tool_args_str}
            
            if self.verbose:
                logger.info(f"Executing tool: {tool_name}")
                logger.info(f"Arguments: {json.dumps(tool_args, indent=2)}")
            
            # Execute tool
            result = self.tools.execute(tool_name, **tool_args)
            
            # Record in memory
            self.memory.add_tool_result(tool_name, tool_args, result)
            
            # Add tool result to conversation
            tool_result_message = f"Tool '{tool_name}' executed successfully.\nResult: {result}"
            self.memory.add_message("user", tool_result_message)
            
            if self.verbose:
                logger.info(f"Tool result: {result[:100]}...")
            
        except Exception as e:
            logger.error(f"Error processing tool call: {e}")
            error_message = f"Error executing tool: {str(e)}"
            self.memory.add_message("user", error_message)
    
    def register_tool(
        self,
        name: str,
        description: str,
        func: callable,
        parameters: Dict[str, Any],
    ):
        """Register a custom tool"""
        self.tools.register(name, description, func, parameters)
        logger.info(f"Registered custom tool: {name}")
    
    def get_memory_summary(self) -> str:
        """Get a summary of agent's memory"""
        return self.memory.get_summary()
    
    def export_session(self) -> Dict[str, Any]:
        """Export current session data"""
        return {
            "agent_name": self.name,
            "model": self.model,
            "context": self.memory.get_task_context(),
            "memory": self.memory.export(),
        }
