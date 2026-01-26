# Langchain - Chains

**Pages:** 22

---

## Long-term memory

**URL:** https://docs.langchain.com/oss/python/langchain/long-term-memory

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- Long-term memory
- ​Overview
- ​Memory storage
- ​Read long-term memory in tools

Was this page helpful?

**Examples:**

Example 1 (json):
```json
from langgraph.store.memory import InMemoryStore


def embed(texts: list[str]) -> list[list[float]]:
    # Replace with an actual embedding function or LangChain embeddings object
    return [[1.0, 2.0] * len(texts)]


# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production use.
store = InMemoryStore(index={"embed": embed, "dims": 2}) 
user_id = "my-user"
application_context = "chitchat"
namespace = (user_id, application_context) 
store.put( 
    namespace,
    "a-memory",
    {
        "rules": [
            "User likes short, direct language",
            "User only speaks English & python",
        ],
        "my-key": "my-value",
    },
)
# get the "memory" by ID
item = store.get(namespace, "a-memory") 
# search for "memories" within this namespace, filtering on content equivalence, sorted by vector similarity
items = store.search( 
    namespace, filter={"my-key": "my-value"}, query="language preferences"
)
```

Example 2 (python):
```python
from dataclasses import dataclass

from langchain_core.runnables import RunnableConfig
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langgraph.store.memory import InMemoryStore


@dataclass
class Context:
    user_id: str

# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production.
store = InMemoryStore() 

# Write sample data to the store using the put method
store.put( 
    ("users",),  # Namespace to group related data together (users namespace for user data)
    "user_123",  # Key within the namespace (user ID as key)
    {
        "name": "John Smith",
        "language": "English",
    }  # Data to store for the given user
)

@tool
def get_user_info(runtime: ToolRuntime[Context]) -> str:
    """Look up user info."""
    # Access the store - same as that provided to `create_agent`
    store = runtime.store 
    user_id = runtime.context.user_id
    # Retrieve data from store - returns StoreValue object with value and metadata
    user_info = store.get(("users",), user_id) 
    return str(user_info.value) if user_info else "Unknown user"

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[get_user_info],
    # Pass store to agent - enables agent to access store when running tools
    store=store, 
    context_schema=Context
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "look up user information"}]},
    context=Context(user_id="user_123") 
)
```

Example 3 (python):
```python
from dataclasses import dataclass
from typing_extensions import TypedDict

from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langgraph.store.memory import InMemoryStore


# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production.
store = InMemoryStore() 

@dataclass
class Context:
    user_id: str

# TypedDict defines the structure of user information for the LLM
class UserInfo(TypedDict):
    name: str

# Tool that allows agent to update user information (useful for chat applications)
@tool
def save_user_info(user_info: UserInfo, runtime: ToolRuntime[Context]) -> str:
    """Save user info."""
    # Access the store - same as that provided to `create_agent`
    store = runtime.store 
    user_id = runtime.context.user_id 
    # Store data in the store (namespace, key, data)
    store.put(("users",), user_id, user_info) 
    return "Successfully saved user info."

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[save_user_info],
    store=store, 
    context_schema=Context
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "My name is John Smith"}]},
    # user_id passed in context to identify whose information is being updated
    context=Context(user_id="user_123") 
)

# You can access the store directly to get the value
store.get(("users",), "user_123").value
```

---

## Structured output

**URL:** https://docs.langchain.com/oss/python/langchain/structured-output

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- Structured output
- ​Response format
- ​Provider strategy
- ​Tool calling strategy

Was this page helpful?

**Examples:**

Example 1 (python):
```python
def create_agent(
    ...
    response_format: Union[
        ToolStrategy[StructuredResponseT],
        ProviderStrategy[StructuredResponseT],
        type[StructuredResponseT],
        None,
    ]
```

Example 2 (json):
```json
custom_profile = {
    "structured_output": True,
    # ...
}
model = init_chat_model("...", profile=custom_profile)
```

Example 3 (php):
```php
class ProviderStrategy(Generic[SchemaT]):
    schema: type[SchemaT]
    strict: bool | None = None
```

Example 4 (python):
```python
from pydantic import BaseModel, Field
from langchain.agents import create_agent


class ContactInfo(BaseModel):
    """Contact information for a person."""
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email address of the person")
    phone: str = Field(description="The phone number of the person")

agent = create_agent(
    model="gpt-5",
    response_format=ContactInfo  # Auto-selects ProviderStrategy
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

print(result["structured_response"])
# ContactInfo(name='John Doe', email='john@example.com', phone='(555) 123-4567')
```

---

## Guardrails

**URL:** https://docs.langchain.com/oss/python/langchain/guardrails

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- Guardrails
- Deterministic guardrails
- Model-based guardrails
- ​Built-in guardrails

Implement safety checks and content filtering for your agents

Built-in PII types and configuration

Was this page helpful?

**Examples:**

Example 1 (json):
```json
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware


agent = create_agent(
    model="gpt-4o",
    tools=[customer_service_tool, email_tool],
    middleware=[
        # Redact emails in user input before sending to model
        PIIMiddleware(
            "email",
            strategy="redact",
            apply_to_input=True,
        ),
        # Mask credit cards in user input
        PIIMiddleware(
            "credit_card",
            strategy="mask",
            apply_to_input=True,
        ),
        # Block API keys - raise error if detected
        PIIMiddleware(
            "api_key",
            detector=r"sk-[a-zA-Z0-9]{32}",
            strategy="block",
            apply_to_input=True,
        ),
    ],
)

# When user provides PII, it will be handled according to the strategy
result = agent.invoke({
    "messages": [{"role": "user", "content": "My email is john.doe@example.com and card is 5105-1051-0510-5100"}]
})
```

Example 2 (json):
```json
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command


agent = create_agent(
    model="gpt-4o",
    tools=[search_tool, send_email_tool, delete_database_tool],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                # Require approval for sensitive operations
                "send_email": True,
                "delete_database": True,
                # Auto-approve safe operations
                "search": False,
            }
        ),
    ],
    # Persist the state across interrupts
    checkpointer=InMemorySaver(),
)

# Human-in-the-loop requires a thread ID for persistence
config = {"configurable": {"thread_id": "some_id"}}

# Agent will pause and wait for approval before executing sensitive tools
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Send an email to the team"}]},
    config=config
)

result = agent.invoke(
    Command(resume={"decisions": [{"type": "approve"}]}),
    config=config  # Same thread ID to resume the paused conversation
)
```

Example 3 (python):
```python
from typing import Any

from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langgraph.runtime import Runtime

class ContentFilterMiddleware(AgentMiddleware):
    """Deterministic guardrail: Block requests containing banned keywords."""

    def __init__(self, banned_keywords: list[str]):
        super().__init__()
        self.banned_keywords = [kw.lower() for kw in banned_keywords]

    @hook_config(can_jump_to=["end"])
    def before_agent(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        # Get the first user message
        if not state["messages"]:
            return None

        first_message = state["messages"][0]
        if first_message.type != "human":
            return None

        content = first_message.content.lower()

        # Check for banned keywords
        for keyword in self.banned_keywords:
            if keyword in content:
                # Block execution before any processing
                return {
                    "messages": [{
                        "role": "assistant",
                        "content": "I cannot process requests containing inappropriate content. Please rephrase your request."
                    }],
                    "jump_to": "end"
                }

        return None

# Use the custom guardrail
from langchain.agents import create_agent

agent = create_agent(
    model="gpt-4o",
    tools=[search_tool, calculator_tool],
    middleware=[
        ContentFilterMiddleware(
            banned_keywords=["hack", "exploit", "malware"]
        ),
    ],
)

# This request will be blocked before any processing
result = agent.invoke({
    "messages": [{"role": "user", "content": "How do I hack into a database?"}]
})
```

Example 4 (python):
```python
from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langgraph.runtime import Runtime
from langchain.messages import AIMessage
from langchain.chat_models import init_chat_model
from typing import Any

class SafetyGuardrailMiddleware(AgentMiddleware):
    """Model-based guardrail: Use an LLM to evaluate response safety."""

    def __init__(self):
        super().__init__()
        self.safety_model = init_chat_model("gpt-4o-mini")

    @hook_config(can_jump_to=["end"])
    def after_agent(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        # Get the final AI response
        if not state["messages"]:
            return None

        last_message = state["messages"][-1]
        if not isinstance(last_message, AIMessage):
            return None

        # Use a model to evaluate safety
        safety_prompt = f"""Evaluate if this response is safe and appropriate.
        Respond with only 'SAFE' or 'UNSAFE'.

        Response: {last_message.content}"""

        result = self.safety_model.invoke([{"role": "user", "content": safety_prompt}])

        if "UNSAFE" in result.content:
            last_message.content = "I cannot provide that response. Please rephrase your request."

        return None

# Use the safety guardrail
from langchain.agents import create_agent

agent = create_agent(
    model="gpt-4o",
    tools=[search_tool, calculator_tool],
    middleware=[SafetyGuardrailMiddleware()],
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "How do I make explosives?"}]
})
```

---

## Vector stores

**URL:** https://docs.langchain.com/oss/python/integrations/vectorstores/index

**Contents:**
      - Popular Providers
      - Integrations by component
- Vector stores
- ​Overview
  - ​Interface
  - ​Initialization
  - ​Adding documents
  - ​Deleting documents
  - ​Similarity search
  - ​Similarity metrics & indexing

Azure Cosmos DB NoSQL

Azure Cosmos DB Mongo vCore

Was this page helpful?

**Examples:**

Example 1 (sql):
```sql
from langchain_core.vectorstores import InMemoryVectorStore
vector_store = InMemoryVectorStore(embedding=SomeEmbeddingModel())
```

Example 2 (unknown):
```unknown
vector_store.add_documents(documents=[doc1, doc2], ids=["id1", "id2"])
```

Example 3 (unknown):
```unknown
vector_store.delete(ids=["id1"])
```

Example 4 (unknown):
```unknown
similar_docs = vector_store.similarity_search("your query here")
```

---

## Models

**URL:** https://docs.langchain.com/oss/python/langchain/models

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- Models
- ​Basic usage
  - ​Initialize a model
  - ​Supported models

Advanced streaming topics

"Auto-streaming" chat models

Example: Message output alongside parsed structure

Example: Nested structures

Updating or overwriting profile data

Initialize and use a rate limiter

Key configuration attributes

Configurable model with default values

Using a configurable model declaratively

Was this page helpful?

**Examples:**

Example 1 (unknown):
```unknown
pip install -U "langchain[openai]"
```

Example 2 (sql):
```sql
import os
from langchain.chat_models import init_chat_model

os.environ["OPENAI_API_KEY"] = "sk-..."

model = init_chat_model("gpt-4.1")
```

Example 3 (unknown):
```unknown
pip install -U "langchain[anthropic]"
```

Example 4 (sql):
```sql
import os
from langchain.chat_models import init_chat_model

os.environ["ANTHROPIC_API_KEY"] = "sk-..."

model = init_chat_model("claude-sonnet-4-5-20250929")
```

---

## Multi-agent

**URL:** https://docs.langchain.com/oss/python/langchain/multi-agent/index

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- Multi-agent
- ​Why multi-agent?
- ​Patterns
  - ​Choosing a pattern

Was this page helpful?

---

## Human-in-the-loop

**URL:** https://docs.langchain.com/oss/python/langchain/human-in-the-loop

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- Human-in-the-loop
- ​Interrupt decision types
- ​Configuring interrupts
- ​Responding to interrupts

Configuration options

Was this page helpful?

**Examples:**

Example 1 (sql):
```sql
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware 
from langgraph.checkpoint.memory import InMemorySaver 


agent = create_agent(
    model="gpt-4o",
    tools=[write_file_tool, execute_sql_tool, read_data_tool],
    middleware=[
        HumanInTheLoopMiddleware( 
            interrupt_on={
                "write_file": True,  # All decisions (approve, edit, reject) allowed
                "execute_sql": {"allowed_decisions": ["approve", "reject"]},  # No editing allowed
                # Safe operation, no approval needed
                "read_data": False,
            },
            # Prefix for interrupt messages - combined with tool name and args to form the full message
            # e.g., "Tool execution pending approval: execute_sql with query='DELETE FROM...'"
            # Individual tools can override this by specifying a "description" in their interrupt config
            description_prefix="Tool execution pending approval",
        ),
    ],
    # Human-in-the-loop requires checkpointing to handle interrupts.
    # In production, use a persistent checkpointer like AsyncPostgresSaver.
    checkpointer=InMemorySaver(),  
)
```

Example 2 (sql):
```sql
from langgraph.types import Command

# Human-in-the-loop leverages LangGraph's persistence layer.
# You must provide a thread ID to associate the execution with a conversation thread,
# so the conversation can be paused and resumed (as is needed for human review).
config = {"configurable": {"thread_id": "some_id"}} 
# Run the graph until the interrupt is hit.
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Delete old records from the database",
            }
        ]
    },
    config=config 
)

# The interrupt contains the full HITL request with action_requests and review_configs
print(result['__interrupt__'])
# > [
# >    Interrupt(
# >       value={
# >          'action_requests': [
# >             {
# >                'name': 'execute_sql',
# >                'arguments': {'query': 'DELETE FROM records WHERE created_at < NOW() - INTERVAL \'30 days\';'},
# >                'description': 'Tool execution pending approval\n\nTool: execute_sql\nArgs: {...}'
# >             }
# >          ],
# >          'review_configs': [
# >             {
# >                'action_name': 'execute_sql',
# >                'allowed_decisions': ['approve', 'reject']
# >             }
# >          ]
# >       }
# >    )
# > ]


# Resume with approval decision
agent.invoke(
    Command( 
        resume={"decisions": [{"type": "approve"}]}  # or "reject"
    ), 
    config=config # Same thread ID to resume the paused conversation
)
```

Example 3 (json):
```json
agent.invoke(
    Command(
        # Decisions are provided as a list, one per action under review.
        # The order of decisions must match the order of actions
        # listed in the `__interrupt__` request.
        resume={
            "decisions": [
                {
                    "type": "approve",
                }
            ]
        }
    ),
    config=config  # Same thread ID to resume the paused conversation
)
```

Example 4 (json):
```json
agent.invoke(
    Command(
        # Decisions are provided as a list, one per action under review.
        # The order of decisions must match the order of actions
        # listed in the `__interrupt__` request.
        resume={
            "decisions": [
                {
                    "type": "edit",
                    # Edited action with tool name and args
                    "edited_action": {
                        # Tool name to call.
                        # Will usually be the same as the original action.
                        "name": "new_tool_name",
                        # Arguments to pass to the tool.
                        "args": {"key1": "new_value", "key2": "original_value"},
                    }
                }
            ]
        }
    ),
    config=config  # Same thread ID to resume the paused conversation
)
```

---

## Context engineering in agents

**URL:** https://docs.langchain.com/oss/python/langchain/context-engineering

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- Context engineering in agents
- ​Overview
  - ​Why do agents fail?
  - ​The agent loop

Was this page helpful?

**Examples:**

Example 1 (python):
```python
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest

@dynamic_prompt
def state_aware_prompt(request: ModelRequest) -> str:
    # request.messages is a shortcut for request.state["messages"]
    message_count = len(request.messages)

    base = "You are a helpful assistant."

    if message_count > 10:
        base += "\nThis is a long conversation - be extra concise."

    return base

agent = create_agent(
    model="gpt-4o",
    tools=[...],
    middleware=[state_aware_prompt]
)
```

Example 2 (python):
```python
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langgraph.store.memory import InMemoryStore

@dataclass
class Context:
    user_id: str

@dynamic_prompt
def store_aware_prompt(request: ModelRequest) -> str:
    user_id = request.runtime.context.user_id

    # Read from Store: get user preferences
    store = request.runtime.store
    user_prefs = store.get(("preferences",), user_id)

    base = "You are a helpful assistant."

    if user_prefs:
        style = user_prefs.value.get("communication_style", "balanced")
        base += f"\nUser prefers {style} responses."

    return base

agent = create_agent(
    model="gpt-4o",
    tools=[...],
    middleware=[store_aware_prompt],
    context_schema=Context,
    store=InMemoryStore()
)
```

Example 3 (python):
```python
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest

@dataclass
class Context:
    user_role: str
    deployment_env: str

@dynamic_prompt
def context_aware_prompt(request: ModelRequest) -> str:
    # Read from Runtime Context: user role and environment
    user_role = request.runtime.context.user_role
    env = request.runtime.context.deployment_env

    base = "You are a helpful assistant."

    if user_role == "admin":
        base += "\nYou have admin access. You can perform all operations."
    elif user_role == "viewer":
        base += "\nYou have read-only access. Guide users to read operations only."

    if env == "production":
        base += "\nBe extra careful with any data modifications."

    return base

agent = create_agent(
    model="gpt-4o",
    tools=[...],
    middleware=[context_aware_prompt],
    context_schema=Context
)
```

Example 4 (python):
```python
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable

@wrap_model_call
def inject_file_context(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Inject context about files user has uploaded this session."""
    # Read from State: get uploaded files metadata
    uploaded_files = request.state.get("uploaded_files", [])  

    if uploaded_files:
        # Build context about available files
        file_descriptions = []
        for file in uploaded_files:
            file_descriptions.append(
                f"- {file['name']} ({file['type']}): {file['summary']}"
            )

        file_context = f"""Files you have access to in this conversation:
{chr(10).join(file_descriptions)}

Reference these files when answering questions."""

        # Inject file context before recent messages
        messages = [  
            *request.messages,
            {"role": "user", "content": file_context},
        ]
        request = request.override(messages=messages)  

    return handler(request)

agent = create_agent(
    model="gpt-4o",
    tools=[...],
    middleware=[inject_file_context]
)
```

---

## OpenAI

**URL:** https://docs.langchain.com/oss/python/integrations/providers/openai

**Contents:**
      - Popular Providers
      - Integrations by component
- OpenAI
- ​Model interfaces
- ChatOpenAI
- AzureChatOpenAI
- OpenAIEmbeddings
- AzureOpenAIEmbeddings
- ​Tools and toolkits
- Dall-E Image Generator

Was this page helpful?

---

## Retrieval

**URL:** https://docs.langchain.com/oss/python/langchain/retrieval

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- Retrieval
- ​Building a knowledge base
- Tutorial: Semantic search
  - ​From retrieval to RAG

Show Extended example: Agentic RAG for LangGraph's llms.txt

Was this page helpful?

**Examples:**

Example 1 (python):
```python
import requests
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent


@tool
def fetch_url(url: str) -> str:
    """Fetch text content from a URL"""
    response = requests.get(url, timeout=10.0)
    response.raise_for_status()
    return response.text

system_prompt = """\
Use fetch_url when you need to fetch information from a web-page; quote relevant snippets.
"""

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[fetch_url], # A tool for retrieval
    system_prompt=system_prompt,
)
```

Example 2 (python):
```python
import requests
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool
from markdownify import markdownify


ALLOWED_DOMAINS = ["https://langchain-ai.github.io/"]
LLMS_TXT = 'https://langchain-ai.github.io/langgraph/llms.txt'


@tool
def fetch_documentation(url: str) -> str:  
    """Fetch and convert documentation from a URL"""
    if not any(url.startswith(domain) for domain in ALLOWED_DOMAINS):
        return (
            "Error: URL not allowed. "
            f"Must start with one of: {', '.join(ALLOWED_DOMAINS)}"
        )
    response = requests.get(url, timeout=10.0)
    response.raise_for_status()
    return markdownify(response.text)


# We will fetch the content of llms.txt, so this can
# be done ahead of time without requiring an LLM request.
llms_txt_content = requests.get(LLMS_TXT).text

# System prompt for the agent
system_prompt = f"""
You are an expert Python developer and technical assistant.
Your primary role is to help users with questions about LangGraph and related tools.

Instructions:

1. If a user asks a question you're unsure about — or one that likely involves API usage,
   behavior, or configuration — you MUST use the `fetch_documentation` tool to consult the relevant docs.
2. When citing documentation, summarize clearly and include relevant context from the content.
3. Do not use any URLs outside of the allowed domain.
4. If a documentation fetch fails, tell the user and proceed with your best expert understanding.

You can access official documentation from the following approved sources:

{llms_txt_content}

You MUST consult the documentation to get up to date documentation
before answering a user's question about LangGraph.

Your answers should be clear, concise, and technically accurate.
"""

tools = [fetch_documentation]

model = init_chat_model("claude-sonnet-4-0", max_tokens=32_000)

agent = create_agent(
    model=model,
    tools=tools,  
    system_prompt=system_prompt,  
    name="Agentic RAG",
)

response = agent.invoke({
    'messages': [
        HumanMessage(content=(
            "Write a short example of a langgraph agent using the "
            "prebuilt create react agent. the agent should be able "
            "to look up stock pricing information."
        ))
    ]
})

print(response['messages'][-1].content)
```

---

## Short-term memory

**URL:** https://docs.langchain.com/oss/python/langchain/short-term-memory

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- Short-term memory
- ​Overview
- ​Usage
  - ​In production

Was this page helpful?

**Examples:**

Example 1 (json):
```json
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver  


agent = create_agent(
    "gpt-5",
    tools=[get_user_info],
    checkpointer=InMemorySaver(),  
)

agent.invoke(
    {"messages": [{"role": "user", "content": "Hi! My name is Bob."}]},
    {"configurable": {"thread_id": "1"}},  
)
```

Example 2 (unknown):
```unknown
pip install langgraph-checkpoint-postgres
```

Example 3 (sql):
```sql
from langchain.agents import create_agent

from langgraph.checkpoint.postgres import PostgresSaver  


DB_URI = "postgresql://postgres:postgres@localhost:5442/postgres?sslmode=disable"
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup() # auto create tables in PostgresSql
    agent = create_agent(
        "gpt-5",
        tools=[get_user_info],
        checkpointer=checkpointer,  
    )
```

Example 4 (json):
```json
from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver


class CustomAgentState(AgentState):  
    user_id: str
    preferences: dict

agent = create_agent(
    "gpt-5",
    tools=[get_user_info],
    state_schema=CustomAgentState,  
    checkpointer=InMemorySaver(),
)

# Custom state can be passed in invoke
result = agent.invoke(
    {
        "messages": [{"role": "user", "content": "Hello"}],
        "user_id": "user_123",  
        "preferences": {"theme": "dark"}  
    },
    {"configurable": {"thread_id": "1"}})
```

---

## Chat models

**URL:** https://docs.langchain.com/oss/python/integrations/chat/index

**Contents:**
      - Popular Providers
      - Integrations by component
- Chat models
- ​Featured models
- ​Chat completions API
- ​All chat models
- Abso
- AI21 Labs
- AI/ML API
- Alibaba Cloud PAI EAS

Was this page helpful?

**Examples:**

Example 1 (python):
```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="...",  # Specify a model available on OpenRouter
    api_key="OPENROUTER_API_KEY",
    base_url="https://openrouter.ai/api/v1",
)
```

Example 2 (json):
```json
model = ChatDeepSeek(
    model="...",
    api_key="...",
    api_base="https://openrouter.ai/api/v1",
    extra_body={"reasoning": {"enabled": True}},
)
```

---

## Custom middleware

**URL:** https://docs.langchain.com/oss/python/langchain/middleware/custom

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- Custom middleware
- ​Hooks
- Node-style hooks
- Wrap-style hooks

Was this page helpful?

**Examples:**

Example 1 (python):
```python
from langchain.agents.middleware import before_model, after_model, AgentState
from langchain.messages import AIMessage
from langgraph.runtime import Runtime
from typing import Any


@before_model(can_jump_to=["end"])
def check_message_limit(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    if len(state["messages"]) >= 50:
        return {
            "messages": [AIMessage("Conversation limit reached.")],
            "jump_to": "end"
        }
    return None

@after_model
def log_response(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print(f"Model returned: {state['messages'][-1].content}")
    return None
```

Example 2 (python):
```python
from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langchain.messages import AIMessage
from langgraph.runtime import Runtime
from typing import Any

class MessageLimitMiddleware(AgentMiddleware):
    def __init__(self, max_messages: int = 50):
        super().__init__()
        self.max_messages = max_messages

    @hook_config(can_jump_to=["end"])
    def before_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        if len(state["messages"]) == self.max_messages:
            return {
                "messages": [AIMessage("Conversation limit reached.")],
                "jump_to": "end"
            }
        return None

    def after_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        print(f"Model returned: {state['messages'][-1].content}")
        return None
```

Example 3 (python):
```python
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable


@wrap_model_call
def retry_model(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    for attempt in range(3):
        try:
            return handler(request)
        except Exception as e:
            if attempt == 2:
                raise
            print(f"Retry {attempt + 1}/3 after error: {e}")
```

Example 4 (python):
```python
from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse
from typing import Callable

class RetryMiddleware(AgentMiddleware):
    def __init__(self, max_retries: int = 3):
        super().__init__()
        self.max_retries = max_retries

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        for attempt in range(self.max_retries):
            try:
                return handler(request)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                print(f"Retry {attempt + 1}/{self.max_retries} after error: {e}")
```

---

## Model Context Protocol (MCP)

**URL:** https://docs.langchain.com/oss/python/langchain/mcp

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- Model Context Protocol (MCP)
- ​Quickstart
- ​Custom servers
- ​Transports

Was this page helpful?

**Examples:**

Example 1 (unknown):
```unknown
pip install langchain-mcp-adapters
```

Example 2 (json):
```json
from langchain_mcp_adapters.client import MultiServerMCPClient  
from langchain.agents import create_agent


client = MultiServerMCPClient(  
    {
        "math": {
            "transport": "stdio",  # Local subprocess communication
            "command": "python",
            # Absolute path to your math_server.py file
            "args": ["/path/to/math_server.py"],
        },
        "weather": {
            "transport": "http",  # HTTP-based remote server
            # Ensure you start your weather server on port 8000
            "url": "http://localhost:8000/mcp",
        }
    }
)

tools = await client.get_tools()  
agent = create_agent(
    "claude-sonnet-4-5-20250929",
    tools  
)
math_response = await agent.ainvoke(
    {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
)
weather_response = await agent.ainvoke(
    {"messages": [{"role": "user", "content": "what is the weather in nyc?"}]}
)
```

Example 3 (unknown):
```unknown
pip install fastmcp
```

Example 4 (python):
```python
from fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

---

## Tools and toolkits

**URL:** https://docs.langchain.com/oss/python/integrations/tools/index

**Contents:**
      - Popular Providers
      - Integrations by component
- Tools and toolkits
- ​Search
- ​Code interpreter
- ​Productivity
- ​Web browsing
- ​Database
- ​Finance
- ​Integration platforms

Was this page helpful?

---

## Agents

**URL:** https://docs.langchain.com/oss/python/langchain/agents

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- Agents
- ​Core components
  - ​Model
    - ​Static model

Example of ReAct loop

Was this page helpful?

**Examples:**

Example 1 (sql):
```sql
from langchain.agents import create_agent

agent = create_agent("openai:gpt-5", tools=tools)
```

Example 2 (python):
```python
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-5",
    temperature=0.1,
    max_tokens=1000,
    timeout=30
    # ... (other params)
)
agent = create_agent(model, tools=tools)
```

Example 3 (python):
```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse


basic_model = ChatOpenAI(model="gpt-4o-mini")
advanced_model = ChatOpenAI(model="gpt-4o")

@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """Choose model based on conversation complexity."""
    message_count = len(request.state["messages"])

    if message_count > 10:
        # Use an advanced model for longer conversations
        model = advanced_model
    else:
        model = basic_model

    return handler(request.override(model=model))

agent = create_agent(
    model=basic_model,  # Default model
    tools=tools,
    middleware=[dynamic_model_selection]
)
```

Example 4 (python):
```python
from langchain.tools import tool
from langchain.agents import create_agent


@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location}: Sunny, 72°F"

agent = create_agent(model, tools=[search, get_weather])
```

---

## Anthropic (Claude)

**URL:** https://docs.langchain.com/oss/python/integrations/providers/anthropic

**Contents:**
      - Popular Providers
      - Integrations by component
- Anthropic (Claude)
- ​Model interfaces
- ChatAnthropic
- Anthropic middleware
- ​Other
- AnthropicLLM

Was this page helpful?

---

## Tools

**URL:** https://docs.langchain.com/oss/python/langchain/tools

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- Tools
- ​Create tools
  - ​Basic tool definition
  - ​Customize tool properties

Was this page helpful?

**Examples:**

Example 1 (python):
```python
from langchain.tools import tool

@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the customer database for records matching the query.

    Args:
        query: Search terms to look for
        limit: Maximum number of results to return
    """
    return f"Found {limit} results for '{query}'"
```

Example 2 (python):
```python
@tool("web_search")  # Custom name
def search(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

print(search.name)  # web_search
```

Example 3 (python):
```python
@tool("calculator", description="Performs arithmetic calculations. Use this for any math problems.")
def calc(expression: str) -> str:
    """Evaluate mathematical expressions."""
    return str(eval(expression))
```

Example 4 (python):
```python
from pydantic import BaseModel, Field
from typing import Literal

class WeatherInput(BaseModel):
    """Input for weather queries."""
    location: str = Field(description="City name or coordinates")
    units: Literal["celsius", "fahrenheit"] = Field(
        default="celsius",
        description="Temperature unit preference"
    )
    include_forecast: bool = Field(
        default=False,
        description="Include 5-day forecast"
    )

@tool(args_schema=WeatherInput)
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """Get current weather and optional forecast."""
    temp = 22 if units == "celsius" else 72
    result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
    if include_forecast:
        result += "\nNext 5 days: Sunny"
    return result
```

---

## Google

**URL:** https://docs.langchain.com/oss/python/integrations/providers/google

**Contents:**
      - Popular Providers
      - Integrations by component
- Google
- ​Google generative AI
  - ​Chat models
- ChatGoogleGenerativeAI
  - ​LLMs
- GoogleGenerativeAI
  - ​Embedding models
- GoogleGenerativeAIEmbeddings

Google Generative AI (Gemini API & Vertex AI)

Google Cloud (Vertex AI Platform Services)

VertexModelGardenLlama

VertexModelGardenMistral

GemmaChatVertexAIModelGarden

VertexAIImageCaptioningChat

VertexAIImageEditorChat

VertexAIImageGeneratorChat

VertexAIVisualQnAChat

Gemma local from Hugging Face

Gemma local from Kaggle

Gemma on Vertex AI Model Garden

Vertex AI image captioning

Vertex AI callback handler

VertexPairWiseStringEvaluator

VertexStringEvaluator

Was this page helpful?

**Examples:**

Example 1 (sql):
```sql
from langchain_google_vertexai.model_garden_maas.llama import VertexModelGardenLlama
```

Example 2 (sql):
```sql
from langchain_google_vertexai.model_garden_maas.mistral import VertexModelGardenMistral
```

Example 3 (sql):
```sql
from langchain_google_vertexai.gemma import GemmaChatLocalHF
```

Example 4 (sql):
```sql
from langchain_google_vertexai.gemma import GemmaChatLocalKaggle
```

---

## Messages

**URL:** https://docs.langchain.com/oss/python/langchain/messages

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- Messages
- ​Basic usage
  - ​Text prompts
  - ​Message prompts

Example: Using artifact for retrieval metadata

ReasoningContentBlock

PlainTextContentBlock

Server-Side Tool Execution

Provider-Specific Blocks

NonStandardContentBlock

Was this page helpful?

**Examples:**

Example 1 (sql):
```sql
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage, SystemMessage

model = init_chat_model("gpt-5-nano")

system_msg = SystemMessage("You are a helpful assistant.")
human_msg = HumanMessage("Hello, how are you?")

# Use with chat models
messages = [system_msg, human_msg]
response = model.invoke(messages)  # Returns AIMessage
```

Example 2 (unknown):
```unknown
response = model.invoke("Write a haiku about spring")
```

Example 3 (sql):
```sql
from langchain.messages import SystemMessage, HumanMessage, AIMessage

messages = [
    SystemMessage("You are a poetry expert"),
    HumanMessage("Write a haiku about spring"),
    AIMessage("Cherry blossoms bloom...")
]
response = model.invoke(messages)
```

Example 4 (json):
```json
messages = [
    {"role": "system", "content": "You are a poetry expert"},
    {"role": "user", "content": "Write a haiku about spring"},
    {"role": "assistant", "content": "Cherry blossoms bloom..."}
]
response = model.invoke(messages)
```

---

## Runtime

**URL:** https://docs.langchain.com/oss/python/langchain/runtime

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- Runtime
- ​Overview
- ​Access
  - ​Inside tools

Was this page helpful?

**Examples:**

Example 1 (python):
```python
from dataclasses import dataclass

from langchain.agents import create_agent


@dataclass
class Context:
    user_name: str

agent = create_agent(
    model="gpt-5-nano",
    tools=[...],
    context_schema=Context  
)

agent.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    context=Context(user_name="John Smith")  
)
```

Example 2 (python):
```python
from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime  

@dataclass
class Context:
    user_id: str

@tool
def fetch_user_email_preferences(runtime: ToolRuntime[Context]) -> str:  
    """Fetch the user's email preferences from the store."""
    user_id = runtime.context.user_id  

    preferences: str = "The user prefers you to write a brief and polite email."
    if runtime.store:  
        if memory := runtime.store.get(("users",), user_id):  
            preferences = memory.value["preferences"]

    return preferences
```

Example 3 (python):
```python
from dataclasses import dataclass

from langchain.messages import AnyMessage
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import dynamic_prompt, ModelRequest, before_model, after_model
from langgraph.runtime import Runtime


@dataclass
class Context:
    user_name: str

# Dynamic prompts
@dynamic_prompt
def dynamic_system_prompt(request: ModelRequest) -> str:
    user_name = request.runtime.context.user_name  
    system_prompt = f"You are a helpful assistant. Address the user as {user_name}."
    return system_prompt

# Before model hook
@before_model
def log_before_model(state: AgentState, runtime: Runtime[Context]) -> dict | None:  
    print(f"Processing request for user: {runtime.context.user_name}")  
    return None

# After model hook
@after_model
def log_after_model(state: AgentState, runtime: Runtime[Context]) -> dict | None:  
    print(f"Completed request for user: {runtime.context.user_name}")  
    return None

agent = create_agent(
    model="gpt-5-nano",
    tools=[...],
    middleware=[dynamic_system_prompt, log_before_model, log_after_model],  
    context_schema=Context
)

agent.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    context=Context(user_name="John Smith")
)
```

---

## Built-in middleware

**URL:** https://docs.langchain.com/oss/python/langchain/middleware/built-in

**Contents:**
      - Get started
      - Core components
      - Middleware
      - Advanced usage
      - Agent development
      - Deploy with LangSmith
- Built-in middleware
- ​Provider-agnostic middleware
  - ​Summarization
  - ​Human-in-the-loop

Prebuilt middleware for common agent use cases

Configuration options

Configuration options

Configuration options

Configuration options

Configuration options

Configuration options

Configuration options

Configuration options

Configuration options

Configuration options

Configuration options

Configuration options

Configuration options

Was this page helpful?

**Examples:**

Example 1 (sql):
```sql
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware

agent = create_agent(
    model="gpt-4o",
    tools=[your_weather_tool, your_calculator_tool],
    middleware=[
        SummarizationMiddleware(
            model="gpt-4o-mini",
            trigger=("tokens", 4000),
            keep=("messages", 20),
        ),
    ],
)
```

Example 2 (json):
```json
from langchain.chat_models import init_chat_model

custom_profile = {
    "max_input_tokens": 100_000,
    # ...
}
model = init_chat_model("gpt-4o", profile=custom_profile)
```

Example 3 (julia):
```julia
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware


# Single condition: trigger if tokens >= 4000
agent = create_agent(
    model="gpt-4o",
    tools=[your_weather_tool, your_calculator_tool],
    middleware=[
        SummarizationMiddleware(
            model="gpt-4o-mini",
            trigger=("tokens", 4000),
            keep=("messages", 20),
        ),
    ],
)

# Multiple conditions: trigger if number of tokens >= 3000 OR messages >= 6
agent2 = create_agent(
    model="gpt-4o",
    tools=[your_weather_tool, your_calculator_tool],
    middleware=[
        SummarizationMiddleware(
            model="gpt-4o-mini",
            trigger=[
                ("tokens", 3000),
                ("messages", 6),
            ],
            keep=("messages", 20),
        ),
    ],
)

# Using fractional limits
agent3 = create_agent(
    model="gpt-4o",
    tools=[your_weather_tool, your_calculator_tool],
    middleware=[
        SummarizationMiddleware(
            model="gpt-4o-mini",
            trigger=("fraction", 0.8),
            keep=("fraction", 0.3),
        ),
    ],
)
```

Example 4 (python):
```python
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver


def read_email_tool(email_id: str) -> str:
    """Mock function to read an email by its ID."""
    return f"Email content for ID: {email_id}"

def send_email_tool(recipient: str, subject: str, body: str) -> str:
    """Mock function to send an email."""
    return f"Email sent to {recipient} with subject '{subject}'"

agent = create_agent(
    model="gpt-4o",
    tools=[your_read_email_tool, your_send_email_tool],
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "your_send_email_tool": {
                    "allowed_decisions": ["approve", "edit", "reject"],
                },
                "your_read_email_tool": False,
            }
        ),
    ],
)
```

---
