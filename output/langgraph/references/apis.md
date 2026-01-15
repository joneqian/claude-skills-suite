# Langgraph - Apis

**Pages:** 1

---

## LangGraph runtime

**URL:** https://docs.langchain.com/oss/python/langgraph/pregel

**Contents:**
      - Get started
      - Capabilities
      - Production
      - LangGraph APIs
- LangGraph runtime
- ​Overview
- ​Actors
- ​Channels
- ​Examples
- ​High-level API

Was this page helpful?

**Examples:**

Example 1 (json):
```json
from langgraph.channels import EphemeralValue
from langgraph.pregel import Pregel, NodeBuilder

node1 = (
    NodeBuilder().subscribe_only("a")
    .do(lambda x: x + x)
    .write_to("b")
)

app = Pregel(
    nodes={"node1": node1},
    channels={
        "a": EphemeralValue(str),
        "b": EphemeralValue(str),
    },
    input_channels=["a"],
    output_channels=["b"],
)

app.invoke({"a": "foo"})
```

Example 2 (json):
```json
{'b': 'foofoo'}
```

Example 3 (json):
```json
from langgraph.channels import LastValue, EphemeralValue
from langgraph.pregel import Pregel, NodeBuilder

node1 = (
    NodeBuilder().subscribe_only("a")
    .do(lambda x: x + x)
    .write_to("b")
)

node2 = (
    NodeBuilder().subscribe_only("b")
    .do(lambda x: x + x)
    .write_to("c")
)


app = Pregel(
    nodes={"node1": node1, "node2": node2},
    channels={
        "a": EphemeralValue(str),
        "b": LastValue(str),
        "c": EphemeralValue(str),
    },
    input_channels=["a"],
    output_channels=["b", "c"],
)

app.invoke({"a": "foo"})
```

Example 4 (json):
```json
{'b': 'foofoo', 'c': 'foofoofoofoo'}
```

---
