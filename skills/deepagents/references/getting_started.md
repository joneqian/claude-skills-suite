# Deepagents - Getting Started

**Pages:** 3

---

## Customize Deep Agents

**URL:** https://docs.langchain.com/oss/python/deepagents/customization

**Contents:**
      - Get started
      - Core capabilities
      - Command line interface
- Customize Deep Agents
- ​Model
- ​System prompt
- ​Tools

Learn how to customize deep agents with system prompts, tools, subagents, and more

Was this page helpful?

**Examples:**

Example 1 (python):
```python
from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent

model = init_chat_model(model="openai:gpt-5")
agent = create_deep_agent(model=model)
```

Example 2 (python):
```python
from deepagents import create_deep_agent

research_instructions = """\
You are an expert researcher. Your job is to conduct \
thorough research, and then write a polished report. \
"""

agent = create_deep_agent(
    system_prompt=research_instructions,
)
```

Example 3 (python):
```python
import os
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )

agent = create_deep_agent(
    tools=[internet_search]
)
```

---

## Deep Agents overview

**URL:** https://docs.langchain.com/oss/python/deepagents/overview

**Contents:**
      - Get started
      - Core capabilities
      - Command line interface
- Deep Agents overview
- ​When to use deep agents
- ​Core capabilities
- Planning and task decomposition
- Context management
- Subagent spawning
- Long-term memory

Build agents that can plan, use subagents, and leverage file systems for complex tasks

Was this page helpful?

---

## Quickstart

**URL:** https://docs.langchain.com/oss/python/deepagents/quickstart

**Contents:**
      - Get started
      - Core capabilities
      - Command line interface
- Quickstart
- ​Prerequisites
  - ​Step 1: Install dependencies
  - ​Step 2: Set up your API keys
  - ​Step 3: Create a search tool
  - ​Step 4: Create a deep agent
  - ​Step 5: Run the agent

Build your first deep agent in minutes

Was this page helpful?

**Examples:**

Example 1 (unknown):
```unknown
pip install deepagents tavily-python
```

Example 2 (unknown):
```unknown
export ANTHROPIC_API_KEY="your-api-key"
export TAVILY_API_KEY="your-tavily-api-key"
```

Example 3 (python):
```python
import os
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )
```

Example 4 (markdown):
```markdown
# System prompt to steer the agent to be an expert researcher
research_instructions = """You are an expert researcher. Your job is to conduct thorough research and then write a polished report.

You have access to an internet search tool as your primary means of gathering information.

## `internet_search`

Use this to run an internet search for a given query. You can specify the max number of results to return, the topic, and whether raw content should be included.
"""

agent = create_deep_agent(
    tools=[internet_search],
    system_prompt=research_instructions
)
```

---
