"""
Example 3: Code Analysis Agent
This example demonstrates an agent specializing in code analysis and review.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import Agent


def main():
    print("\n" + "="*70)
    print("EXAMPLE 3: CODE ANALYSIS AGENT")
    print("="*70 + "\n")
    
    # Create a code analysis agent
    agent = Agent(
        name="CodeReviewer",
        model="gpt-4",
        temperature=0.5,
        max_iterations=6,
        verbose=True
    )
    
    # Example 1: Buggy code analysis
    print("\n🐛 Task 1: Bug Detection")
    print("-" * 70)
    buggy_code = '''
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total = num  # BUG: Should be += not =
    return total / len(numbers)
    '''
    
    task1 = f"""
    I have this code that's supposed to calculate average but has a bug:
    
    {buggy_code}
    
    Please:
    1. Check if the syntax is valid
    2. Identify the bug
    3. Explain what's wrong
    4. Provide the corrected code
    5. Explain how to test it
    
    Use the code_analyzer tool for syntax checking.
    """
    result1 = agent.run(task1)
    
    # Example 2: Code optimization
    print("\n⚡ Task 2: Code Optimization")
    print("-" * 70)
    slow_code = '''
def find_duplicates(lst):
    """Find duplicate items in a list - SLOW VERSION"""
    duplicates = []
    for i in range(len(lst)):
        for j in range(i+1, len(lst)):
            if lst[i] == lst[j] and lst[i] not in duplicates:
                duplicates.append(lst[i])
    return duplicates
    '''
    
    task2 = f"""
    This code finds duplicates but is inefficient:
    
    {slow_code}
    
    Please:
    1. Verify the syntax
    2. Analyze the complexity
    3. Identify performance issues
    4. Provide an optimized version
    5. Explain the improvement
    
    Use the code_analyzer tool for complexity analysis.
    """
    result2 = agent.run(task2)
    
    # Example 3: Code review request
    print("\n👀 Task 3: Code Quality Review")
    print("-" * 70)
    
    review_code = '''
def process_data(d):
    result = []
    for x in d:
        if x > 5:
            result.append(x * 2)
    return result

class DataProcessor:
    def __init__(self):
        self.data = []
    
    def add(self, item):
        self.data.append(item)
    
    def get(self):
        return self.data
    '''
    
    task3 = f"""
    Please review this code for quality:
    
    {review_code}
    
    Evaluate:
    1. Syntax validity
    2. Code style and naming conventions
    3. Function complexity
    4. Improvements for readability
    5. Documentation needs
    6. Best practices recommendations
    
    Use the code_analyzer tool for all checks.
    """
    result3 = agent.run(task3)
    
    # Export session for reference
    print("\n📁 Session Export:")
    print("-" * 70)
    session_data = agent.export_session()
    import json
    print(json.dumps(session_data, indent=2)[:500] + "...(truncated)")


if __name__ == "__main__":
    main()
