# Langgraph - Capabilities

**Pages:** 7

---

## Durable execution

**URL:** https://docs.langchain.com/oss/python/langgraph/durable-execution

**Contents:**
      - Get started
      - Capabilities
      - Production
      - LangGraph APIs
- Durable execution
- ​Requirements
- ​Determinism and consistent replay
- ​Durability modes
- ​Using tasks in nodes
- ​Resuming workflows

Was this page helpful?

**Examples:**

Example 1 (json):
```json
graph.stream(
    {"input": "test"},
    durability="sync"
)
```

Example 2 (python):
```python
from typing import NotRequired
from typing_extensions import TypedDict
import uuid

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
import requests

# Define a TypedDict to represent the state
class State(TypedDict):
    url: str
    result: NotRequired[str]

def call_api(state: State):
    """Example node that makes an API request."""
    result = requests.get(state['url']).text[:100]  # Side-effect  #
    return {
        "result": result
    }

# Create a StateGraph builder and add a node for the call_api function
builder = StateGraph(State)
builder.add_node("call_api", call_api)

# Connect the start and end nodes to the call_api node
builder.add_edge(START, "call_api")
builder.add_edge("call_api", END)

# Specify a checkpointer
checkpointer = InMemorySaver()

# Compile the graph with the checkpointer
graph = builder.compile(checkpointer=checkpointer)

# Define a config with a thread ID.
thread_id = uuid.uuid4()
config = {"configurable": {"thread_id": thread_id}}

# Invoke the graph
graph.invoke({"url": "https://www.example.com"}, config)
```

Example 3 (python):
```python
from typing import NotRequired
from typing_extensions import TypedDict
import uuid

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import task
from langgraph.graph import StateGraph, START, END
import requests

# Define a TypedDict to represent the state
class State(TypedDict):
    urls: list[str]
    result: NotRequired[list[str]]


@task
def _make_request(url: str):
    """Make a request."""
    return requests.get(url).text[:100]  

def call_api(state: State):
    """Example node that makes an API request."""
    requests = [_make_request(url) for url in state['urls']]  
    results = [request.result() for request in requests]
    return {
        "results": results
    }

# Create a StateGraph builder and add a node for the call_api function
builder = StateGraph(State)
builder.add_node("call_api", call_api)

# Connect the start and end nodes to the call_api node
builder.add_edge(START, "call_api")
builder.add_edge("call_api", END)

# Specify a checkpointer
checkpointer = InMemorySaver()

# Compile the graph with the checkpointer
graph = builder.compile(checkpointer=checkpointer)

# Define a config with a thread ID.
thread_id = uuid.uuid4()
config = {"configurable": {"thread_id": thread_id}}

# Invoke the graph
graph.invoke({"urls": ["https://www.example.com"]}, config)
```

---

## Memory

**URL:** https://docs.langchain.com/oss/python/langgraph/add-memory

**Contents:**
      - Get started
      - Capabilities
      - Production
      - LangGraph APIs
- Memory
- ​Add short-term memory
  - ​Use in production
  - ​Use in subgraphs
- ​Add long-term memory
  - ​Use in production

Example: using Postgres checkpointer

Example: using MongoDB checkpointer

Example: using Redis checkpointer

Example: using Postgres store

Example: using Redis store

Long-term memory with semantic search

Full example: trim messages

Full example: delete messages

Full example: summarize messages

Was this page helpful?

**Examples:**

Example 1 (json):
```json
from langgraph.checkpoint.memory import InMemorySaver  
from langgraph.graph import StateGraph

checkpointer = InMemorySaver()  

builder = StateGraph(...)
graph = builder.compile(checkpointer=checkpointer)  

graph.invoke(
    {"messages": [{"role": "user", "content": "hi! i am Bob"}]},
    {"configurable": {"thread_id": "1"}},  
)
```

Example 2 (typescript):
```typescript
from langgraph.checkpoint.postgres import PostgresSaver

DB_URI = "postgresql://postgres:postgres@localhost:5442/postgres?sslmode=disable"
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:  
    builder = StateGraph(...)
    graph = builder.compile(checkpointer=checkpointer)
```

Example 3 (unknown):
```unknown
pip install -U "psycopg[binary,pool]" langgraph langgraph-checkpoint-postgres
```

Example 4 (python):
```python
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.checkpoint.postgres import PostgresSaver  

model = init_chat_model(model="claude-haiku-4-5-20251001")

DB_URI = "postgresql://postgres:postgres@localhost:5442/postgres?sslmode=disable"
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:  
    # checkpointer.setup()

    def call_model(state: MessagesState):
        response = model.invoke(state["messages"])
        return {"messages": response}

    builder = StateGraph(MessagesState)
    builder.add_node(call_model)
    builder.add_edge(START, "call_model")

    graph = builder.compile(checkpointer=checkpointer)  

    config = {
        "configurable": {
            "thread_id": "1"
        }
    }

    for chunk in graph.stream(
        {"messages": [{"role": "user", "content": "hi! I'm bob"}]},
        config,  
        stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()

    for chunk in graph.stream(
        {"messages": [{"role": "user", "content": "what's my name?"}]},
        config,  
        stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()
```

---

## Subgraphs

**URL:** https://docs.langchain.com/oss/python/langgraph/use-subgraphs

**Contents:**
      - Get started
      - Capabilities
      - Production
      - LangGraph APIs
- Subgraphs
- ​Setup
- ​Invoke a graph from a node
- ​Add a graph as a node
- ​Add persistence
- ​View subgraph state

Full example: different state schemas

Full example: different state schemas (two levels of subgraphs)

Full example: shared state schemas

View interrupted subgraph state

Stream from subgraphs

Was this page helpful?

**Examples:**

Example 1 (unknown):
```unknown
pip install -U langgraph
```

Example 2 (python):
```python
from typing_extensions import TypedDict
from langgraph.graph.state import StateGraph, START

class SubgraphState(TypedDict):
    bar: str

# Subgraph

def subgraph_node_1(state: SubgraphState):
    return {"bar": "hi! " + state["bar"]}

subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph = subgraph_builder.compile()

# Parent graph

class State(TypedDict):
    foo: str

def call_subgraph(state: State):
    # Transform the state to the subgraph state
    subgraph_output = subgraph.invoke({"bar": state["foo"]})  
    # Transform response back to the parent state
    return {"foo": subgraph_output["bar"]}

builder = StateGraph(State)
builder.add_node("node_1", call_subgraph)
builder.add_edge(START, "node_1")
graph = builder.compile()
```

Example 3 (python):
```python
from typing_extensions import TypedDict
from langgraph.graph.state import StateGraph, START

# Define subgraph
class SubgraphState(TypedDict):
    # note that none of these keys are shared with the parent graph state
    bar: str
    baz: str

def subgraph_node_1(state: SubgraphState):
    return {"baz": "baz"}

def subgraph_node_2(state: SubgraphState):
    return {"bar": state["bar"] + state["baz"]}

subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_node(subgraph_node_2)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")
subgraph = subgraph_builder.compile()

# Define parent graph
class ParentState(TypedDict):
    foo: str

def node_1(state: ParentState):
    return {"foo": "hi! " + state["foo"]}

def node_2(state: ParentState):
    # Transform the state to the subgraph state
    response = subgraph.invoke({"bar": state["foo"]})
    # Transform response back to the parent state
    return {"foo": response["bar"]}


builder = StateGraph(ParentState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
graph = builder.compile()

for chunk in graph.stream({"foo": "foo"}, subgraphs=True):
    print(chunk)
```

Example 4 (json):
```json
((), {'node_1': {'foo': 'hi! foo'}})
(('node_2:577b710b-64ae-31fb-9455-6a4d4cc2b0b9',), {'subgraph_node_1': {'baz': 'baz'}})
(('node_2:577b710b-64ae-31fb-9455-6a4d4cc2b0b9',), {'subgraph_node_2': {'bar': 'hi! foobaz'}})
((), {'node_2': {'foo': 'hi! foobaz'}})
```

---

## Streaming

**URL:** https://docs.langchain.com/oss/python/langgraph/streaming

**Contents:**
      - Get started
      - Capabilities
      - Production
      - LangGraph APIs
- Streaming
- ​Supported stream modes
- ​Basic usage example
- ​Stream multiple modes
- ​Stream graph state
- ​Stream subgraph outputs

Extended example: streaming updates

Extended example: streaming from subgraphs

Extended example: filtering by tags

Extended example: streaming LLM tokens from specific nodes

Extended example: streaming arbitrary chat model

Extended example: async LLM call with manual config

Extended example: async custom streaming with stream writer

Was this page helpful?

**Examples:**

Example 1 (python):
```python
for chunk in graph.stream(inputs, stream_mode="updates"):
    print(chunk)
```

Example 2 (python):
```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    topic: str
    joke: str

def refine_topic(state: State):
    return {"topic": state["topic"] + " and cats"}

def generate_joke(state: State):
    return {"joke": f"This is a joke about {state['topic']}"}

graph = (
    StateGraph(State)
    .add_node(refine_topic)
    .add_node(generate_joke)
    .add_edge(START, "refine_topic")
    .add_edge("refine_topic", "generate_joke")
    .add_edge("generate_joke", END)
    .compile()
)

# The stream() method returns an iterator that yields streamed outputs
for chunk in graph.stream(  
    {"topic": "ice cream"},
    # Set stream_mode="updates" to stream only the updates to the graph state after each node
    # Other stream modes are also available. See supported stream modes for details
    stream_mode="updates",  
):
    print(chunk)
```

Example 3 (json):
```json
{'refineTopic': {'topic': 'ice cream and cats'}}
{'generateJoke': {'joke': 'This is a joke about ice cream and cats'}}
```

Example 4 (python):
```python
for mode, chunk in graph.stream(inputs, stream_mode=["updates", "custom"]):
    print(chunk)
```

---

## Use time-travel

**URL:** https://docs.langchain.com/oss/python/langgraph/use-time-travel

**Contents:**
      - Get started
      - Capabilities
      - Production
      - LangGraph APIs
- Use time-travel
- ​In a workflow
  - ​Setup
  - ​1. Run the graph
  - ​2. Identify a checkpoint
  - ​3. Update the state

Was this page helpful?

**Examples:**

Example 1 (unknown):
```unknown
%%capture --no-stderr
pip install --quiet -U langgraph langchain_anthropic
```

Example 2 (python):
```python
import getpass
import os


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")


_set_env("ANTHROPIC_API_KEY")
```

Example 3 (python):
```python
import uuid

from typing_extensions import TypedDict, NotRequired
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver


class State(TypedDict):
    topic: NotRequired[str]
    joke: NotRequired[str]


model = init_chat_model(
    "claude-sonnet-4-5-20250929",
    temperature=0,
)


def generate_topic(state: State):
    """LLM call to generate a topic for the joke"""
    msg = model.invoke("Give me a funny topic for a joke")
    return {"topic": msg.content}


def write_joke(state: State):
    """LLM call to write a joke based on the topic"""
    msg = model.invoke(f"Write a short joke about {state['topic']}")
    return {"joke": msg.content}


# Build workflow
workflow = StateGraph(State)

# Add nodes
workflow.add_node("generate_topic", generate_topic)
workflow.add_node("write_joke", write_joke)

# Add edges to connect nodes
workflow.add_edge(START, "generate_topic")
workflow.add_edge("generate_topic", "write_joke")
workflow.add_edge("write_joke", END)

# Compile
checkpointer = InMemorySaver()
graph = workflow.compile(checkpointer=checkpointer)
graph
```

Example 4 (json):
```json
config = {
    "configurable": {
        "thread_id": uuid.uuid4(),
    }
}
state = graph.invoke({}, config)

print(state["topic"])
print()
print(state["joke"])
```

---

## Persistence

**URL:** https://docs.langchain.com/oss/python/langgraph/persistence

**Contents:**
      - Get started
      - Capabilities
      - Production
      - LangGraph APIs
- Persistence
- ​Threads
- ​Checkpoints
  - ​Get state
  - ​Get state history
  - ​Replay

Was this page helpful?

**Examples:**

Example 1 (json):
```json
{"configurable": {"thread_id": "1"}}
```

Example 2 (python):
```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig
from typing import Annotated
from typing_extensions import TypedDict
from operator import add

class State(TypedDict):
    foo: str
    bar: Annotated[list[str], add]

def node_a(state: State):
    return {"foo": "a", "bar": ["a"]}

def node_b(state: State):
    return {"foo": "b", "bar": ["b"]}


workflow = StateGraph(State)
workflow.add_node(node_a)
workflow.add_node(node_b)
workflow.add_edge(START, "node_a")
workflow.add_edge("node_a", "node_b")
workflow.add_edge("node_b", END)

checkpointer = InMemorySaver()
graph = workflow.compile(checkpointer=checkpointer)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}
graph.invoke({"foo": "", "bar":[]}, config)
```

Example 3 (json):
```json
# get the latest state snapshot
config = {"configurable": {"thread_id": "1"}}
graph.get_state(config)

# get a state snapshot for a specific checkpoint_id
config = {"configurable": {"thread_id": "1", "checkpoint_id": "1ef663ba-28fe-6528-8002-5a559208592c"}}
graph.get_state(config)
```

Example 4 (json):
```json
StateSnapshot(
    values={'foo': 'b', 'bar': ['a', 'b']},
    next=(),
    config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28fe-6528-8002-5a559208592c'}},
    metadata={'source': 'loop', 'writes': {'node_b': {'foo': 'b', 'bar': ['b']}}, 'step': 2},
    created_at='2024-08-29T19:19:38.821749+00:00',
    parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f9-6ec4-8001-31981c2c39f8'}}, tasks=()
)
```

---

## Interrupts

**URL:** https://docs.langchain.com/oss/python/langgraph/interrupts

**Contents:**
      - Get started
      - Capabilities
      - Production
      - LangGraph APIs
- Interrupts
- ​Pause using interrupt
- ​Resuming interrupts
- ​Common patterns
  - ​Approve or reject
  - ​Review and edit state

Was this page helpful?

**Examples:**

Example 1 (python):
```python
from langgraph.types import interrupt

def approval_node(state: State):
    # Pause and ask for approval
    approved = interrupt("Do you approve this action?")

    # When you resume, Command(resume=...) returns that value here
    return {"approved": approved}
```

Example 2 (json):
```json
from langgraph.types import Command

# Initial run - hits the interrupt and pauses
# thread_id is the persistent pointer (stores a stable ID in production)
config = {"configurable": {"thread_id": "thread-1"}}
result = graph.invoke({"input": "data"}, config=config)

# Check what was interrupted
# __interrupt__ contains the payload that was passed to interrupt()
print(result["__interrupt__"])
# > [Interrupt(value='Do you approve this action?')]

# Resume with the human's response
# The resume payload becomes the return value of interrupt() inside the node
graph.invoke(Command(resume=True), config=config)
```

Example 3 (python):
```python
from typing import Literal
from langgraph.types import interrupt, Command

def approval_node(state: State) -> Command[Literal["proceed", "cancel"]]:
    # Pause execution; payload shows up under result["__interrupt__"]
    is_approved = interrupt({
        "question": "Do you want to proceed with this action?",
        "details": state["action_details"]
    })

    # Route based on the response
    if is_approved:
        return Command(goto="proceed")  # Runs after the resume payload is provided
    else:
        return Command(goto="cancel")
```

Example 4 (markdown):
```markdown
# To approve
graph.invoke(Command(resume=True), config=config)

# To reject
graph.invoke(Command(resume=False), config=config)
```

---
