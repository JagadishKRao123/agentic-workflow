"""
Example 1: Basic Agent Task Execution
This example demonstrates a simple agent performing basic tasks using built-in tools.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import Agent


def main():
    print("\n" + "="*70)
    print("EXAMPLE 1: BASIC AGENT TASK EXECUTION")
    print("="*70 + "\n")
    
    # Create an agent
    agent = Agent(
        name="BasicBot",
        model="gpt-4",
        temperature=0.7,
        max_iterations=5,
        verbose=True
    )
    
    # Example 1: Simple math problem
    print("\n📊 Task 1: Simple Math Problem")
    print("-" * 70)
    task1 = "Calculate the result of 125 * 8, then add 250 to it"
    result1 = agent.run(task1)
    
    # Example 2: String analysis
    print("\n📝 Task 2: String Analysis")
    print("-" * 70)
    task2 = "Analyze the text 'Agentic workflow is a powerful paradigm for building AI systems' and tell me word count, character count, and unique characters"
    result2 = agent.run(task2)
    
    # Example 3: Multi-step problem
    print("\n🔄 Task 3: Multi-step Problem")
    print("-" * 70)
    task3 = """
    I need to:
    1. Calculate 2^10 (2 to the power of 10)
    2. Add 500 to the result
    3. Tell me the final number
    Please use the calculate tool to help.
    """
    result3 = agent.run(task3)
    
    # Print memory summary from the last task
    print("\n📊 Memory Summary from Last Task:")
    print("-" * 70)
    print(agent.get_memory_summary())


if __name__ == "__main__":
    main()
