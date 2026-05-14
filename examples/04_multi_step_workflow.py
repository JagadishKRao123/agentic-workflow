"""
Example 4: Multi-Step Workflow
This example demonstrates complex workflows with multiple steps and decision points.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import Agent


def main():
    print("\n" + "="*70)
    print("EXAMPLE 4: MULTI-STEP WORKFLOW")
    print("="*70 + "\n")
    
    # Create a workflow agent
    agent = Agent(
        name="WorkflowEngine",
        model="gpt-4",
        temperature=0.7,
        max_iterations=10,
        verbose=True
    )
    
    # Example 1: Business analytics workflow
    print("\n📈 Workflow 1: Business Analytics")
    print("-" * 70)
    workflow1 = """
    BUSINESS ANALYTICS TASK:
    
    A retail company reports these quarterly sales figures:
    Q1: 50000, Q2: 65000, Q3: 58000, Q4: 72000
    
    Please complete this analysis:
    1. Convert to list format: [50000, 65000, 58000, 72000]
    2. Use list_operations with 'statistics' to get insights
    3. Calculate the total revenue using calculate tool
    4. Calculate the average revenue
    5. Identify the best and worst performing quarters
    6. Suggest 2 business insights based on the data
    7. Provide recommendations
    """
    result1 = agent.run(workflow1)
    
    # Example 2: Text processing workflow
    print("\n🔤 Workflow 2: Text Processing")
    print("-" * 70)
    workflow2 = """
    TEXT ANALYSIS WORKFLOW:
    
    You need to analyze this text for a content marketing report:
    "Artificial intelligence and machine learning are revolutionizing industries worldwide. 
    AI agents are becoming more sophisticated, enabling automation of complex tasks. 
    The future of work will be shaped by human-AI collaboration."
    
    Complete these steps:
    1. Use string_analysis to get the text length
    2. Count the word count
    3. Analyze unique characters
    4. Identify key themes:
       - AI/ML technologies mentioned
       - Business impact areas
       - Future outlook
    5. Suggest 3 related topics for further content
    6. Rate the text quality (1-10) and explain
    """
    result2 = agent.run(workflow2)
    
    # Example 3: Problem solving workflow
    print("\n🧩 Workflow 3: Complex Problem Solving")
    print("-" * 70)
    workflow3 = """
    ENGINEERING PROBLEM:
    
    A technology startup is planning infrastructure:
    - Initial setup cost: $50,000
    - Monthly operational cost: $3,500
    - Monthly revenue per customer: $500
    - Target: Break even in 12 months
    
    Calculate:
    1. Total costs for 12 months
    2. Number of customers needed for break-even
    3. If they acquire 150 customers in 12 months, will they break even?
    4. If margin improves by 10%, how many fewer customers are needed?
    5. Create a business case recommendation
    
    Use the calculate tool for all math operations.
    """
    result3 = agent.run(workflow3)
    
    # Example 4: Decision-making workflow
    print("\n🎯 Workflow 4: Decision-Making")
    print("-" * 70)
    workflow4 = """
    STRATEGIC DECISION WORKFLOW:
    
    A company is evaluating 3 tech stack options:
    
    OPTION A (Python + Django):
    - Setup time: 2 weeks
    - Monthly maintenance: 40 hours
    - Cost per hour: $100
    
    OPTION B (Go + Gin):
    - Setup time: 3 weeks
    - Monthly maintenance: 25 hours
    - Cost per hour: $120
    
    OPTION C (Node.js + Express):
    - Setup time: 1.5 weeks
    - Monthly maintenance: 45 hours
    - Cost per hour: $90
    
    Analysis needed:
    1. Calculate total setup cost for each (using $150/hour)
    2. Calculate annual maintenance cost for each
    3. Calculate total first-year cost for each
    4. Create a comparison table
    5. Make a recommendation with reasoning
    6. Identify any risks for each option
    """
    result4 = agent.run(workflow4)
    
    # Print comprehensive summary
    print("\n" + "="*70)
    print("WORKFLOW COMPLETION SUMMARY")
    print("="*70)
    print(f"Agent: {agent.name}")
    print(f"Model: {agent.model}")
    print(f"Total workflows executed: 4")
    print("\nAgent Memory Summary:")
    print(agent.get_memory_summary())


if __name__ == "__main__":
    main()
