"""
Example 2: Research Agent
This example demonstrates an agent performing research and analysis tasks.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import Agent


def main():
    print("\n" + "="*70)
    print("EXAMPLE 2: RESEARCH AGENT")
    print("="*70 + "\n")
    
    # Create a research agent
    agent = Agent(
        name="ResearchBot",
        model="gpt-4",
        temperature=0.8,
        max_iterations=8,
        verbose=True
    )
    
    # Example 1: Information gathering and analysis
    print("\n🔍 Task 1: Technology Research")
    print("-" * 70)
    task1 = """
    I want to understand agentic workflows. Please:
    1. Explain what an agentic workflow is
    2. Describe the key components (agent, tools, memory, planning)
    3. Give 3 real-world use cases
    4. Summarize the benefits
    """
    result1 = agent.run(task1)
    
    # Example 2: Data analysis task
    print("\n📊 Task 2: Data Analysis")
    print("-" * 70)
    task2 = """
    Analyze this list of numbers: [45, 23, 67, 89, 12, 45, 78, 34, 45, 56]
    
    Please:
    1. Find unique values
    2. Count how many items total
    3. Tell me the first and last numbers
    Use the list_operations tool
    """
    result2 = agent.run(task2)
    
    # Example 3: Code understanding
    print("\n💻 Task 3: Code Analysis")
    print("-" * 70)
    sample_code = '''
def fibonacci(n):
    """Calculate fibonacci number at position n"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def main():
    for i in range(10):
        print(fibonacci(i))
        
if __name__ == "__main__":
    main()
    '''
    
    task3 = f"""
    Analyze this Python code and provide:
    1. What does this code do?
    2. Is the syntax valid?
    3. How many functions are defined?
    4. What would be a potential performance issue?
    5. Suggest an optimization
    
    Code:
    {sample_code}
    
    Use the code_analyzer tool to help verify syntax.
    """
    result3 = agent.run(task3)
    
    # Example 4: Complex problem solving
    print("\n🧮 Task 4: Problem Solving")
    print("-" * 70)
    task4 = """
    Solve this step by step:
    
    A company sells widgets at $5 each.
    They have a promotion: "Buy 10, get 20% off the entire purchase"
    
    Calculate:
    1. Cost of 10 widgets at regular price
    2. Cost of 10 widgets with 20% discount
    3. Amount saved
    4. If they sell 1000 widgets with this promotion, total revenue
    
    Use the calculate tool for all computations.
    """
    result4 = agent.run(task4)


if __name__ == "__main__":
    main()
