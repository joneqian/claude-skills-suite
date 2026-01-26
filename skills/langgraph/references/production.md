# Langgraph - Production

**Pages:** 6

---

## Test

**URL:** https://docs.langchain.com/oss/python/langgraph/test

**Contents:**
      - Get started
      - Capabilities
      - Production
      - LangGraph APIs
- Test
- ​Prerequisites
- ​Getting started
- ​Testing individual nodes and edges
- ​Partial execution

Was this page helpful?

**Examples:**

Example 1 (unknown):
```unknown
$ pip install -U pytest
```

Example 2 (python):
```python
import pytest

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

def create_graph() -> StateGraph:
    class MyState(TypedDict):
        my_key: str

    graph = StateGraph(MyState)
    graph.add_node("node1", lambda state: {"my_key": "hello from node1"})
    graph.add_node("node2", lambda state: {"my_key": "hello from node2"})
    graph.add_edge(START, "node1")
    graph.add_edge("node1", "node2")
    graph.add_edge("node2", END)
    return graph

def test_basic_agent_execution() -> None:
    checkpointer = MemorySaver()
    graph = create_graph()
    compiled_graph = graph.compile(checkpointer=checkpointer)
    result = compiled_graph.invoke(
        {"my_key": "initial_value"},
        config={"configurable": {"thread_id": "1"}}
    )
    assert result["my_key"] == "hello from node2"
```

Example 3 (python):
```python
import pytest

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

def create_graph() -> StateGraph:
    class MyState(TypedDict):
        my_key: str

    graph = StateGraph(MyState)
    graph.add_node("node1", lambda state: {"my_key": "hello from node1"})
    graph.add_node("node2", lambda state: {"my_key": "hello from node2"})
    graph.add_edge(START, "node1")
    graph.add_edge("node1", "node2")
    graph.add_edge("node2", END)
    return graph

def test_individual_node_execution() -> None:
    # Will be ignored in this example
    checkpointer = MemorySaver()
    graph = create_graph()
    compiled_graph = graph.compile(checkpointer=checkpointer)
    # Only invoke node 1
    result = compiled_graph.nodes["node1"].invoke(
        {"my_key": "initial_value"},
    )
    assert result["my_key"] == "hello from node1"
```

Example 4 (python):
```python
import pytest

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

def create_graph() -> StateGraph:
    class MyState(TypedDict):
        my_key: str

    graph = StateGraph(MyState)
    graph.add_node("node1", lambda state: {"my_key": "hello from node1"})
    graph.add_node("node2", lambda state: {"my_key": "hello from node2"})
    graph.add_node("node3", lambda state: {"my_key": "hello from node3"})
    graph.add_node("node4", lambda state: {"my_key": "hello from node4"})
    graph.add_edge(START, "node1")
    graph.add_edge("node1", "node2")
    graph.add_edge("node2", "node3")
    graph.add_edge("node3", "node4")
    graph.add_edge("node4", END)
    return graph

def test_partial_execution_from_node2_to_node3() -> None:
    checkpointer = MemorySaver()
    graph = create_graph()
    compiled_graph = graph.compile(checkpointer=checkpointer)
    compiled_graph.update_state(
        config={
          "configurable": {
            "thread_id": "1"
          }
        },
        # The state passed into node 2 - simulating the state at
        # the end of node 1
        values={"my_key": "initial_value"},
        # Update saved state as if it came from node 1
        # Execution will resume at node 2
        as_node="node1",
    )
    result = compiled_graph.invoke(
        # Resume execution by passing None
        None,
        config={"configurable": {"thread_id": "1"}},
        # Stop after node 3 so that node 4 doesn't run
        interrupt_after="node3",
    )
    assert result["my_key"] == "hello from node3"
```

---

## LangSmith Observability

**URL:** https://docs.langchain.com/oss/python/langgraph/observability

**Contents:**
      - Get started
      - Capabilities
      - Production
      - LangGraph APIs
- LangSmith Observability
- ​Prerequisites
- ​Enable tracing
- ​Trace selectively
- ​Log to a project
- ​Add metadata to traces

Was this page helpful?

**Examples:**

Example 1 (unknown):
```unknown
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<your-api-key>
```

Example 2 (python):
```python
import langsmith as ls

# This WILL be traced
with ls.tracing_context(enabled=True):
    agent.invoke({"messages": [{"role": "user", "content": "Send a test email to alice@example.com"}]})

# This will NOT be traced (if LANGSMITH_TRACING is not set)
agent.invoke({"messages": [{"role": "user", "content": "Send another email"}]})
```

Example 3 (unknown):
```unknown
export LANGSMITH_PROJECT=my-agent-project
```

Example 4 (typescript):
```typescript
import langsmith as ls

with ls.tracing_context(project_name="email-agent-test", enabled=True):
    response = agent.invoke({
        "messages": [{"role": "user", "content": "Send a welcome email"}]
    })
```

---

## Agent Chat UI

**URL:** https://docs.langchain.com/oss/python/langgraph/ui

**Contents:**
      - Get started
      - Capabilities
      - Production
      - LangGraph APIs
- Agent Chat UI
  - ​Quick start
  - ​Local development
  - ​Connect to your agent

Was this page helpful?

**Examples:**

Example 1 (markdown):
```markdown
# Create a new Agent Chat UI project
npx create-agent-chat-app --project-name my-chat-ui
cd my-chat-ui

# Install dependencies and start
pnpm install
pnpm dev
```

---

## Application structure

**URL:** https://docs.langchain.com/oss/python/langgraph/application-structure

**Contents:**
      - Get started
      - Capabilities
      - Production
      - LangGraph APIs
- Application structure
- ​Key concepts
- ​File structure
- ​Configuration file
  - ​Examples
- ​Dependencies

Was this page helpful?

**Examples:**

Example 1 (go):
```go
my-app/
├── my_agent # all project code lies within here
│   ├── utils # utilities for your graph
│   │   ├── __init__.py
│   │   ├── tools.py # tools for your graph
│   │   ├── nodes.py # node functions for your graph
│   │   └── state.py # state definition of your graph
│   ├── __init__.py
│   └── agent.py # code for constructing your graph
├── .env # environment variables
├── requirements.txt # package dependencies
└── langgraph.json # configuration file for LangGraph
```

Example 2 (unknown):
```unknown
my-app/
├── my_agent # all project code lies within here
│   ├── utils # utilities for your graph
│   │   ├── __init__.py
│   │   ├── tools.py # tools for your graph
│   │   ├── nodes.py # node functions for your graph
│   │   └── state.py # state definition of your graph
│   ├── __init__.py
│   └── agent.py # code for constructing your graph
├── .env # environment variables
├── langgraph.json  # configuration file for LangGraph
└── pyproject.toml # dependencies for your project
```

Example 3 (json):
```json
{
  "dependencies": ["langchain_openai", "./your_package"],
  "graphs": {
    "my_agent": "./your_package/your_file.py:agent"
  },
  "env": "./.env"
}
```

---

## LangSmith Deployment

**URL:** https://docs.langchain.com/oss/python/langgraph/deploy

**Contents:**
      - Get started
      - Capabilities
      - Production
      - LangGraph APIs
- LangSmith Deployment
- ​Prerequisites
- ​Deploy your agent
  - ​1. Create a repository on GitHub
  - ​2. Deploy to LangSmith
  - ​3. Test your application in Studio

Navigate to LangSmith Deployment

Create new deployment

Was this page helpful?

**Examples:**

Example 1 (unknown):
```unknown
pip install langgraph-sdk
```

Example 2 (python):
```python
from langgraph_sdk import get_sync_client # or get_client for async

client = get_sync_client(url="your-deployment-url", api_key="your-langsmith-api-key")

for chunk in client.runs.stream(
    None,    # Threadless run
    "agent", # Name of agent. Defined in langgraph.json.
    input={
        "messages": [{
            "role": "human",
            "content": "What is LangGraph?",
        }],
    },
    stream_mode="updates",
):
    print(f"Receiving new event of type: {chunk.event}...")
    print(chunk.data)
    print("\n\n")
```

Example 3 (json):
```json
curl -s --request POST \
    --url <DEPLOYMENT_URL>/runs/stream \
    --header 'Content-Type: application/json' \
    --header "X-Api-Key: <LANGSMITH API KEY> \
    --data "{
        \"assistant_id\": \"agent\", `# Name of agent. Defined in langgraph.json.`
        \"input\": {
            \"messages\": [
                {
                    \"role\": \"human\",
                    \"content\": \"What is LangGraph?\"
                }
            ]
        },
        \"stream_mode\": \"updates\"
    }"
```

---

## LangSmith Studio

**URL:** https://docs.langchain.com/oss/python/langgraph/studio

**Contents:**
      - Get started
      - Capabilities
      - Production
      - LangGraph APIs
- LangSmith Studio
- ​Prerequisites
- ​Set up local Agent server
  - ​1. Install the LangGraph CLI
  - ​2. Prepare your agent
  - ​3. Environment variables

Was this page helpful?

**Examples:**

Example 1 (markdown):
```markdown
# Python >= 3.11 is required.
pip install --upgrade "langgraph-cli[inmem]"
```

Example 2 (python):
```python
from langchain.agents import create_agent

def send_email(to: str, subject: str, body: str):
    """Send an email"""
    email = {
        "to": to,
        "subject": subject,
        "body": body
    }
    # ... email sending logic

    return f"Email sent to {to}"

agent = create_agent(
    "gpt-4o",
    tools=[send_email],
    system_prompt="You are an email assistant. Always use the send_email tool.",
)
```

Example 3 (unknown):
```unknown
LANGSMITH_API_KEY=lsv2...
```

Example 4 (json):
```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./src/agent.py:agent"
  },
  "env": ".env"
}
```

---
