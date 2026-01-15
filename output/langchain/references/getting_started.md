# Langchain - Getting Started

**Pages:** 7

---

## LangChain integrations packages

**URL:** https://docs.langchain.com/oss/python/integrations/providers/overview

**Contents:**
      - Popular Providers
      - Integrations by component
- LangChain integrations packages
- Chat models
- Embedding models
- Tools and toolkits
- ​Popular providers
- ​All providers

Was this page helpful?

---

## Install LangChain

**URL:** https://docs.langchain.com/oss/python/langchain/install

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- Install LangChain

Was this page helpful?

**Examples:**

Example 1 (markdown):
```markdown
pip install -U langchain
# Requires Python 3.10+
```

Example 2 (markdown):
```markdown
# Installing the OpenAI integration
pip install -U langchain-openai

# Installing the Anthropic integration
pip install -U langchain-anthropic
```

---

## Quickstart

**URL:** https://docs.langchain.com/oss/python/langchain/quickstart

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- Quickstart
- ​Requirements
- ​Build a basic agent
- ​Build a real-world agent

Define the system prompt

Define response format

Create and run the agent

Show Full example code

Was this page helpful?

**Examples:**

Example 1 (json):
```json
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```

Example 2 (sql):
```sql
SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location."""
```

Example 3 (python):
```python
from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime

@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

@dataclass
class Context:
    """Custom runtime context schema."""
    user_id: str

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"
```

Example 4 (sql):
```sql
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "claude-sonnet-4-5-20250929",
    temperature=0.5,
    timeout=10,
    max_tokens=1000
)
```

---

## Overview

**URL:** https://docs.langchain.com/oss/python/langchain/streaming/overview

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- Overview
- ​Overview
- ​Supported stream modes
- ​Agent progress

Stream real-time updates from agent runs

Was this page helpful?

**Examples:**

Example 1 (json):
```json
from langchain.agents import create_agent


def get_weather(city: str) -> str:
    """Get weather for a given city."""

    return f"It's always sunny in {city}!"

agent = create_agent(
    model="gpt-5-nano",
    tools=[get_weather],
)
for chunk in agent.stream(  
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode="updates",
):
    for step, data in chunk.items():
        print(f"step: {step}")
        print(f"content: {data['messages'][-1].content_blocks}")
```

Example 2 (yaml):
```yaml
step: model
content: [{'type': 'tool_call', 'name': 'get_weather', 'args': {'city': 'San Francisco'}, 'id': 'call_OW2NYNsNSKhRZpjW0wm2Aszd'}]

step: tools
content: [{'type': 'text', 'text': "It's always sunny in San Francisco!"}]

step: model
content: [{'type': 'text', 'text': 'It's always sunny in San Francisco!'}]
```

Example 3 (json):
```json
from langchain.agents import create_agent


def get_weather(city: str) -> str:
    """Get weather for a given city."""

    return f"It's always sunny in {city}!"

agent = create_agent(
    model="gpt-5-nano",
    tools=[get_weather],
)
for token, metadata in agent.stream(  
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode="messages",
):
    print(f"node: {metadata['langgraph_node']}")
    print(f"content: {token.content_blocks}")
    print("\n")
```

Example 4 (yaml):
```yaml
node: model
content: [{'type': 'tool_call_chunk', 'id': 'call_vbCyBcP8VuneUzyYlSBZZsVa', 'name': 'get_weather', 'args': '', 'index': 0}]


node: model
content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': '{"', 'index': 0}]


node: model
content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': 'city', 'index': 0}]


node: model
content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': '":"', 'index': 0}]


node: model
content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': 'San', 'index': 0}]


node: model
content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': ' Francisco', 'index': 0}]


node: model
content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': '"}', 'index': 0}]


node: model
content: []


node: tools
content: [{'type': 'text', 'text': "It's always sunny in San Francisco!"}]


node: model
content: []


node: model
content: [{'type': 'text', 'text': 'Here'}]


node: model
content: [{'type': 'text', 'text': ''s'}]


node: model
content: [{'type': 'text', 'text': ' what'}]


node: model
content: [{'type': 'text', 'text': ' I'}]


node: model
content: [{'type': 'text', 'text': ' got'}]


node: model
content: [{'type': 'text', 'text': ':'}]


node: model
content: [{'type': 'text', 'text': ' "'}]


node: model
content: [{'type': 'text', 'text': "It's"}]


node: model
content: [{'type': 'text', 'text': ' always'}]


node: model
content: [{'type': 'text', 'text': ' sunny'}]


node: model
content: [{'type': 'text', 'text': ' in'}]


node: model
content: [{'type': 'text', 'text': ' San'}]


node: model
content: [{'type': 'text', 'text': ' Francisco'}]


node: model
content: [{'type': 'text', 'text': '!"\n\n'}]
```

---

## Philosophy

**URL:** https://docs.langchain.com/oss/python/langchain/philosophy

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- Philosophy
- ​History

LangChain exists to be the easiest place to start building with LLMs, while also being flexible and production-ready.

We want to enable developers to build with the best models.

We want to make it easy to use models to orchestrate more complex flows that interact with other data and computation.

Was this page helpful?

---

## LangChain overview

**URL:** https://docs.langchain.com/oss/python/langchain/overview

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- LangChain overview
- ​ Create an agent
- ​ core benefits
- Standard model interface

LangChain is an open source framework with a pre-built agent architecture and integrations for any model or tool — so you can build agents that adapt as fast as the ecosystem evolves

Was this page helpful?

**Examples:**

Example 1 (json):
```json
# pip install -qU langchain "langchain[anthropic]"
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```

---

## Overview

**URL:** https://docs.langchain.com/oss/python/langchain/middleware/overview

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- Overview
- ​The agent loop
- ​Additional resources
- Built-in middleware

Control and customize agent execution at every step

Was this page helpful?

**Examples:**

Example 1 (sql):
```sql
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware, HumanInTheLoopMiddleware

agent = create_agent(
    model="gpt-4o",
    tools=[...],
    middleware=[
        SummarizationMiddleware(...),
        HumanInTheLoopMiddleware(...)
    ],
)
```

---
