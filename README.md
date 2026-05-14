# Agentic Workflow Framework

A Python-based framework for building autonomous agents that can decompose tasks, make decisions, and execute actions in a structured workflow.

## 🎯 Project Overview

This framework enables you to:
- Create autonomous agents that think and act
- Decompose complex tasks into steps
- Execute tools and evaluate results
- Build multi-step workflows with decision-making
- Learn agent patterns and design principles

## 📁 Project Structure

```
agentic-workflow/
├── README.md
├── requirements.txt
├── .env.example
├── src/
│   ├── __init__.py
│   ├── agent.py                 # Core agent implementation
│   ├── tools.py                 # Tool definitions and registry
│   ├── memory.py                # Agent memory and context
│   └── llm_client.py           # LLM integration (OpenAI)
├── examples/
│   ├── __init__.py
│   ├── 01_basic_agent.py       # Simple task execution
│   ├── 02_research_agent.py    # Information gathering
│   ├── 03_code_agent.py        # Code analysis
│   └── 04_multi_step_workflow.py # Complex workflows
└── tests/
    └── test_agent.py
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository
```bash
git clone https://github.com/JagadishKRao123/agentic-workflow.git
cd agentic-workflow
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Setup environment variables
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

## 🧠 Core Concepts

### Agent
The main entity that:
- Receives tasks/goals
- Plans actions using an LLM
- Executes tools
- Evaluates outcomes
- Iterates until task is complete

### Tools
Reusable functions that agents can call:
- Web search
- File operations
- Code execution
- Data processing
- etc.

### Memory
Stores:
- Conversation history
- Task context
- Tool execution results
- Learned patterns

## 💡 Usage Examples

### Example 1: Basic Task Execution
```python
from src.agent import Agent

agent = Agent(name="TaskBot")
result = agent.run("What is 5 + 3 and tell me about Python?")
print(result)
```

### Example 2: Research Workflow
```python
from src.agent import Agent

agent = Agent(name="ResearchBot")
result = agent.run(
    "Research and summarize the latest trends in AI for 2026"
)
```

### Example 3: Code Analysis
```python
from src.agent import Agent

agent = Agent(name="CodeAnalyzer")
code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
result = agent.run(f"Analyze this code and suggest optimizations:\n{code}")
```

Run examples:
```bash
python examples/01_basic_agent.py
python examples/02_research_agent.py
python examples/03_code_agent.py
python examples/04_multi_step_workflow.py
```

## 🛠️ Key Features

- **Tool Integration**: Easy registration and execution of custom tools
- **Memory Management**: Persistent context and conversation history
- **Error Handling**: Graceful failure recovery and retry logic
- **Logging**: Detailed logging of agent decisions and actions
- **Extensible**: Simple to add new tools and capabilities

## 📚 Learning Path

1. Start with `01_basic_agent.py` - Understand basic agent flow
2. Explore `02_research_agent.py` - Learn about tool usage
3. Review `03_code_agent.py` - See specialized agent patterns
4. Study `04_multi_step_workflow.py` - Complex multi-step processes

## 🔧 Architecture

```
User Task
    ↓
Agent (Planner & Executor)
    ├─→ LLM (Think & Plan)
    ├─→ Tool Registry (Execute)
    ├─→ Memory (Store & Retrieve)
    └─→ Evaluator (Check Progress)
    ↓
Result
```

## 📝 Configuration

Edit `.env`:
```
OPENAI_API_KEY=your-key-here
MODEL=gpt-4
MAX_ITERATIONS=10
TEMPERATURE=0.7
```

## 🚦 Running Tests

```bash
python -m pytest tests/
```

## 📖 Further Reading

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Agent Design Patterns](https://en.wikipedia.org/wiki/Intelligent_agent)
- [Autonomous Agents Research](https://arxiv.org/)

## 🤝 Contributing

Feel free to extend this framework with:
- New tool implementations
- Additional example workflows
- Performance optimizations
- Documentation improvements

## 📄 License

MIT License

---

**Happy Building! 🚀**
