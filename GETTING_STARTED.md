# Getting Started Guide

## Prerequisites

- Python 3.8 or higher
- OpenAI API key (get from https://platform.openai.com/api-keys)
- pip (Python package manager)

## Step 1: Clone and Setup

### 1.1 Clone the Repository
```bash
git clone https://github.com/JagadishKRao123/agentic-workflow.git
cd agentic-workflow
```

### 1.2 Create Virtual Environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 1.3 Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 2: Configure Environment

### 2.1 Copy Environment Template
```bash
cp .env.example .env
```

### 2.2 Edit .env File
```bash
# Edit .env and add your OpenAI API key
nano .env
# or
code .env  # if using VS Code
```

Your `.env` should look like:
```
OPENAI_API_KEY=sk-...your-actual-key...
MODEL=gpt-4
TEMPERATURE=0.7
MAX_ITERATIONS=10
VERBOSE=True
```

**Getting Your API Key**:
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (you won't see it again!)
4. Paste it in your `.env` file

## Step 3: Run Your First Example

### 3.1 Basic Agent Example
```bash
python examples/01_basic_agent.py
```

This will run 3 simple tasks:
- Math calculation: 125 * 8 + 250
- String analysis: Word count and character analysis
- Multi-step problem solving

**Expected Output**:
```
==============================================================================
EXAMPLE 1: BASIC AGENT TASK EXECUTION
==============================================================================

📊 Task 1: Simple Math Problem
------------------------------------------------------
============================================================================
Agent 'BasicBot' starting task: Calculate the result of 125 * 8, then add 250 to it
============================================================================
[... agent thinking and tool execution ...]

FINAL RESULT:
The result is 1250. To break it down: 125 * 8 = 1000, then 1000 + 250 = 1250.
============================================================================
```

## Step 4: Explore Other Examples

### 4.1 Research Agent
```bash
python examples/02_research_agent.py
```
This agent performs research, analyzes data, and reviews code.

### 4.2 Code Analysis Agent
```bash
python examples/03_code_agent.py
```
This agent finds bugs, optimizes code, and provides reviews.

### 4.3 Multi-Step Workflows
```bash
python examples/04_multi_step_workflow.py
```
This agent handles complex business workflows with multiple steps.

## Step 5: Create Your First Agent

Create a new file `my_first_agent.py`:

```python
from src.agent import Agent

# Create an agent
agent = Agent(
    name="MyAgent",
    model="gpt-4",
    temperature=0.7,
    max_iterations=5,
    verbose=True
)

# Run a task
result = agent.run("Tell me about agentic workflows and give 3 examples")

print("\n✅ Task Complete!")
print(f"Result:\n{result}")
```

Run it:
```bash
python my_first_agent.py
```

## Step 6: Register Custom Tools

```python
from src.agent import Agent

def convert_temperature(celsius: float) -> str:
    """Convert Celsius to Fahrenheit"""
    fahrenheit = (celsius * 9/5) + 32
    return f"{celsius}°C = {fahrenheit}°F"

# Create agent
agent = Agent(name="TemperatureBot")

# Register custom tool
agent.register_tool(
    name="convert_temp",
    description="Convert temperature from Celsius to Fahrenheit",
    func=convert_temperature,
    parameters={
        "type": "object",
        "properties": {
            "celsius": {
                "type": "number",
                "description": "Temperature in Celsius"
            }
        },
        "required": ["celsius"]
    }
)

# Use it
result = agent.run("What is 25 degrees Celsius in Fahrenheit?")
print(result)
```

## Troubleshooting

### Issue: "OPENAI_API_KEY not found"
**Solution**: 
- Check that `.env` file exists in project root
- Verify the key is set: `echo $OPENAI_API_KEY`
- On Windows: Use `set OPENAI_API_KEY=your-key` or edit .env

### Issue: "No module named 'openai'"
**Solution**:
```bash
pip install -r requirements.txt
# or
pip install openai
```

### Issue: "Rate limit exceeded"
**Solution**:
- Wait a minute before retrying
- Reduce `MAX_ITERATIONS` in .env
- Use gpt-3.5-turbo instead of gpt-4 for testing

### Issue: "The model `gpt-4` does not exist"
**Solution**:
- Ensure you have gpt-4 access (requires paid account)
- Use gpt-3.5-turbo instead (free tier):
  ```
  MODEL=gpt-3.5-turbo
  ```

## Common Tasks

### Run Tests
```bash
pytest tests/
# or
python -m pytest tests/ -v
```

### Enable Debug Logging
Edit your script:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

agent = Agent(name="DebugBot")
result = agent.run("Your task here")
```

### Export Session Results
```python
agent = Agent()
result = agent.run("Your task")

# Export session
session_data = agent.export_session()
import json
with open("session.json", "w") as f:
    json.dump(session_data, f, indent=2)
```

### View Agent Memory
```python
agent = Agent()
result = agent.run("Your task")

# View memory
print(agent.get_memory_summary())
```

## Next Steps

1. **Read the Architecture**: `ARCHITECTURE.md`
2. **Study the Examples**: Explore all 4 examples
3. **Customize Tools**: Add tools specific to your use case
4. **Build a Workflow**: Create a multi-step workflow
5. **Deploy**: Consider deploying as a service

## Resources

- **OpenAI Documentation**: https://platform.openai.com/docs
- **Function Calling**: https://platform.openai.com/docs/guides/function-calling
- **API Reference**: https://platform.openai.com/docs/api-reference

## Need Help?

- Check existing issues: https://github.com/JagadishKRao123/agentic-workflow/issues
- Create a new issue with details about your problem
- Include: error message, steps to reproduce, your environment

Happy Building! 🚀
