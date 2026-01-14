# Fastapi - Dependencies

**Pages:** 8

---

## Dependencies with yield¶

**URL:** https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/

**Contents:**
- Dependencies with yield¶
- A database dependency with yield¶
- A dependency with yield and try¶
- Sub-dependencies with yield¶
- Dependencies with yield and HTTPException¶
- Dependencies with yield and except¶
  - Always raise in Dependencies with yield and except¶
- Execution of dependencies with yield¶
- Early exit and scope¶
  - scope for sub-dependencies¶

FastAPI supports dependencies that do some extra steps after finishing.

To do this, use yield instead of return, and write the extra steps (code) after.

Make sure to use yield one single time per dependency.

Any function that is valid to use with:

would be valid to use as a FastAPI dependency.

In fact, FastAPI uses those two decorators internally.

For example, you could use this to create a database session and close it after finishing.

Only the code prior to and including the yield statement is executed before creating a response:

The yielded value is what is injected into path operations and other dependencies:

The code following the yield statement is executed after the response:

You can use async or regular functions.

FastAPI will do the right thing with each, the same as with normal dependencies.

If you use a try block in a dependency with yield, you'll receive any exception that was thrown when using the dependency.

For example, if some code at some point in the middle, in another dependency or in a path operation, made a database transaction "rollback" or created any other exception, you would receive the exception in your dependency.

So, you can look for that specific exception inside the dependency with except SomeException.

In the same way, you can use finally to make sure the exit steps are executed, no matter if there was an exception or not.

You can have sub-dependencies and "trees" of sub-dependencies of any size and shape, and any or all of them can use yield.

FastAPI will make sure that the "exit code" in each dependency with yield is run in the correct order.

For example, dependency_c can have a dependency on dependency_b, and dependency_b on dependency_a:

Prefer to use the Annotated version if possible.

And all of them can use yield.

In this case dependency_c, to execute its exit code, needs the value from dependency_b (here named dep_b) to still be available.

And, in turn, dependency_b needs the value from dependency_a (here named dep_a) to be available for its exit code.

Prefer to use the Annotated version if possible.

The same way, you could have some dependencies with yield and some other dependencies with return, and have some of those depend on some of the others.

And you could have a single dependency that requires several other dependencies with yield, etc.

You can have any combinations of dependencies that you want.

FastAPI will make sure everything is run in the correct order.

This works thanks to Python's Context Managers.

FastAPI uses them internally to achieve this.

You saw that you can use dependencies with yield and have try blocks that try to execute some code and then run some exit code after finally.

You can also use except to catch the exception that was raised and do something with it.

For example, you can raise a different exception, like HTTPException.

This is a somewhat advanced technique, and in most of the cases you won't really need it, as you can raise exceptions (including HTTPException) from inside of the rest of your application code, for example, in the path operation function.

But it's there for you if you need it. 🤓

Prefer to use the Annotated version if possible.

If you want to catch exceptions and create a custom response based on that, create a Custom Exception Handler.

If you catch an exception using except in a dependency with yield and you don't raise it again (or raise a new exception), FastAPI won't be able to notice there was an exception, the same way that would happen with regular Python:

Prefer to use the Annotated version if possible.

In this case, the client will see an HTTP 500 Internal Server Error response as it should, given that we are not raising an HTTPException or similar, but the server will not have any logs or any other indication of what was the error. 😱

If you catch an exception in a dependency with yield, unless you are raising another HTTPException or similar, you should re-raise the original exception.

You can re-raise the same exception using raise:

Prefer to use the Annotated version if possible.

Now the client will get the same HTTP 500 Internal Server Error response, but the server will have our custom InternalError in the logs. 😎

The sequence of execution is more or less like this diagram. Time flows from top to bottom. And each column is one of the parts interacting or executing code.

Only one response will be sent to the client. It might be one of the error responses or it will be the response from the path operation.

After one of those responses is sent, no other response can be sent.

If you raise any exception in the code from the path operation function, it will be passed to the dependencies with yield, including HTTPException. In most cases you will want to re-raise that same exception or a new one from the dependency with yield to make sure it's properly handled.

Normally the exit code of dependencies with yield is executed after the response is sent to the client.

But if you know that you won't need to use the dependency after returning from the path operation function, you can use Depends(scope="function") to tell FastAPI that it should close the dependency after the path operation function returns, but before the response is sent.

Prefer to use the Annotated version if possible.

Depends() receives a scope parameter that can be:

If not specified and the dependency has yield, it will have a scope of "request" by default.

When you declare a dependency with a scope="request" (the default), any sub-dependency needs to also have a scope of "request".

But a dependency with scope of "function" can have dependencies with scope of "function" and scope of "request".

This is because any dependency needs to be able to run its exit code before the sub-dependencies, as it might need to still use them during its exit code.

Dependencies with yield have evolved over time to cover different use cases and fix some issues.

If you want to see what has changed in different versions of FastAPI, you can read more about it in the advanced guide, in Advanced Dependencies - Dependencies with yield, HTTPException, except and Background Tasks.

"Context Managers" are any of those Python objects that you can use in a with statement.

For example, you can use with to read a file:

Underneath, the open("./somefile.txt") creates an object that is called a "Context Manager".

When the with block finishes, it makes sure to close the file, even if there were exceptions.

When you create a dependency with yield, FastAPI will internally create a context manager for it, and combine it with some other related tools.

This is, more or less, an "advanced" idea.

If you are just starting with FastAPI you might want to skip it for now.

In Python, you can create Context Managers by creating a class with two methods: __enter__() and __exit__().

You can also use them inside of FastAPI dependencies with yield by using with or async with statements inside of the dependency function:

Another way to create a context manager is with:

using them to decorate a function with a single yield.

That's what FastAPI uses internally for dependencies with yield.

But you don't have to use the decorators for FastAPI dependencies (and you shouldn't).

FastAPI will do it for you internally.

**Examples:**

Example 1 (python):
```python
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
```

Example 2 (python):
```python
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
```

Example 3 (python):
```python
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
```

Example 4 (python):
```python
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
```

---

## Dependencies¶

**URL:** https://fastapi.tiangolo.com/tutorial/dependencies/

**Contents:**
- Dependencies¶
- What is "Dependency Injection"¶
- First Steps¶
  - Create a dependency, or "dependable"¶
  - Import Depends¶
  - Declare the dependency, in the "dependant"¶
- Share Annotated dependencies¶
- To async or not to async¶
- Integrated with OpenAPI¶
- Simple usage¶

FastAPI has a very powerful but intuitive Dependency Injection system.

It is designed to be very simple to use, and to make it very easy for any developer to integrate other components with FastAPI.

"Dependency Injection" means, in programming, that there is a way for your code (in this case, your path operation functions) to declare things that it requires to work and use: "dependencies".

And then, that system (in this case FastAPI) will take care of doing whatever is needed to provide your code with those needed dependencies ("inject" the dependencies).

This is very useful when you need to:

All these, while minimizing code repetition.

Let's see a very simple example. It will be so simple that it is not very useful, for now.

But this way we can focus on how the Dependency Injection system works.

Let's first focus on the dependency.

It is just a function that can take all the same parameters that a path operation function can take:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

And it has the same shape and structure that all your path operation functions have.

You can think of it as a path operation function without the "decorator" (without the @app.get("/some-path")).

And it can return anything you want.

In this case, this dependency expects:

And then it just returns a dict containing those values.

FastAPI added support for Annotated (and started recommending it) in version 0.95.0.

If you have an older version, you would get errors when trying to use Annotated.

Make sure you Upgrade the FastAPI version to at least 0.95.1 before using Annotated.

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

The same way you use Body, Query, etc. with your path operation function parameters, use Depends with a new parameter:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Although you use Depends in the parameters of your function the same way you use Body, Query, etc, Depends works a bit differently.

You only give Depends a single parameter.

This parameter must be something like a function.

You don't call it directly (don't add the parenthesis at the end), you just pass it as a parameter to Depends().

And that function takes parameters in the same way that path operation functions do.

You'll see what other "things", apart from functions, can be used as dependencies in the next chapter.

Whenever a new request arrives, FastAPI will take care of:

This way you write shared code once and FastAPI takes care of calling it for your path operations.

Notice that you don't have to create a special class and pass it somewhere to FastAPI to "register" it or anything similar.

You just pass it to Depends and FastAPI knows how to do the rest.

In the examples above, you see that there's a tiny bit of code duplication.

When you need to use the common_parameters() dependency, you have to write the whole parameter with the type annotation and Depends():

But because we are using Annotated, we can store that Annotated value in a variable and use it in multiple places:

This is just standard Python, it's called a "type alias", it's actually not specific to FastAPI.

But because FastAPI is based on the Python standards, including Annotated, you can use this trick in your code. 😎

The dependencies will keep working as expected, and the best part is that the type information will be preserved, which means that your editor will be able to keep providing you with autocompletion, inline errors, etc. The same for other tools like mypy.

This will be especially useful when you use it in a large code base where you use the same dependencies over and over again in many path operations.

As dependencies will also be called by FastAPI (the same as your path operation functions), the same rules apply while defining your functions.

You can use async def or normal def.

And you can declare dependencies with async def inside of normal def path operation functions, or def dependencies inside of async def path operation functions, etc.

It doesn't matter. FastAPI will know what to do.

If you don't know, check the Async: "In a hurry?" section about async and await in the docs.

All the request declarations, validations and requirements of your dependencies (and sub-dependencies) will be integrated in the same OpenAPI schema.

So, the interactive docs will have all the information from these dependencies too:

If you look at it, path operation functions are declared to be used whenever a path and operation matches, and then FastAPI takes care of calling the function with the correct parameters, extracting the data from the request.

Actually, all (or most) of the web frameworks work in this same way.

You never call those functions directly. They are called by your framework (in this case, FastAPI).

With the Dependency Injection system, you can also tell FastAPI that your path operation function also "depends" on something else that should be executed before your path operation function, and FastAPI will take care of executing it and "injecting" the results.

Other common terms for this same idea of "dependency injection" are:

Integrations and "plug-ins" can be built using the Dependency Injection system. But in fact, there is actually no need to create "plug-ins", as by using dependencies it's possible to declare an infinite number of integrations and interactions that become available to your path operation functions.

And dependencies can be created in a very simple and intuitive way that allows you to just import the Python packages you need, and integrate them with your API functions in a couple of lines of code, literally.

You will see examples of this in the next chapters, about relational and NoSQL databases, security, etc.

The simplicity of the dependency injection system makes FastAPI compatible with:

Although the hierarchical dependency injection system is very simple to define and use, it's still very powerful.

You can define dependencies that in turn can define dependencies themselves.

In the end, a hierarchical tree of dependencies is built, and the Dependency Injection system takes care of solving all these dependencies for you (and their sub-dependencies) and providing (injecting) the results at each step.

For example, let's say you have 4 API endpoints (path operations):

then you could add different permission requirements for each of them just with dependencies and sub-dependencies:

All these dependencies, while declaring their requirements, also add parameters, validations, etc. to your path operations.

FastAPI will take care of adding it all to the OpenAPI schema, so that it is shown in the interactive documentation systems.

**Examples:**

Example 1 (python):
```python
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
```

Example 2 (python):
```python
from typing import Annotated, Union

from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(
    q: Union[str, None] = None, skip: int = 0, limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
```

Example 3 (python):
```python
from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons
```

Example 4 (python):
```python
from typing import Union

from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(
    q: Union[str, None] = None, skip: int = 0, limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons
```

---

## Testing Dependencies with Overrides¶

**URL:** https://fastapi.tiangolo.com/advanced/testing-dependencies/

**Contents:**
- Testing Dependencies with Overrides¶
- Overriding dependencies during testing¶
  - Use cases: external service¶
  - Use the app.dependency_overrides attribute¶

There are some scenarios where you might want to override a dependency during testing.

You don't want the original dependency to run (nor any of the sub-dependencies it might have).

Instead, you want to provide a different dependency that will be used only during tests (possibly only some specific tests), and will provide a value that can be used where the value of the original dependency was used.

An example could be that you have an external authentication provider that you need to call.

You send it a token and it returns an authenticated user.

This provider might be charging you per request, and calling it might take some extra time than if you had a fixed mock user for tests.

You probably want to test the external provider once, but not necessarily call it for every test that runs.

In this case, you can override the dependency that calls that provider, and use a custom dependency that returns a mock user, only for your tests.

For these cases, your FastAPI application has an attribute app.dependency_overrides, it is a simple dict.

To override a dependency for testing, you put as a key the original dependency (a function), and as the value, your dependency override (another function).

And then FastAPI will call that override instead of the original dependency.

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

You can set a dependency override for a dependency used anywhere in your FastAPI application.

The original dependency could be used in a path operation function, a path operation decorator (when you don't use the return value), a .include_router() call, etc.

FastAPI will still be able to override it.

Then you can reset your overrides (remove them) by setting app.dependency_overrides to be an empty dict:

If you want to override a dependency only during some tests, you can set the override at the beginning of the test (inside the test function) and reset it at the end (at the end of the test function).

**Examples:**

Example 1 (python):
```python
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return {"message": "Hello Items!", "params": commons}


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return {"message": "Hello Users!", "params": commons}


client = TestClient(app)


async def override_dependency(q: str | None = None):
    return {"q": q, "skip": 5, "limit": 10}


app.dependency_overrides[common_parameters] = override_dependency


def test_override_in_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": None, "skip": 5, "limit": 10},
    }


def test_override_in_items_with_q():
    response = client.get("/items/?q=foo")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }


def test_override_in_items_with_params():
    response = client.get("/items/?q=foo&skip=100&limit=200")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }
```

Example 2 (python):
```python
from typing import Annotated, Union

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


async def common_parameters(
    q: Union[str, None] = None, skip: int = 0, limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return {"message": "Hello Items!", "params": commons}


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return {"message": "Hello Users!", "params": commons}


client = TestClient(app)


async def override_dependency(q: Union[str, None] = None):
    return {"q": q, "skip": 5, "limit": 10}


app.dependency_overrides[common_parameters] = override_dependency


def test_override_in_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": None, "skip": 5, "limit": 10},
    }


def test_override_in_items_with_q():
    response = client.get("/items/?q=foo")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }


def test_override_in_items_with_params():
    response = client.get("/items/?q=foo&skip=100&limit=200")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }
```

Example 3 (python):
```python
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return {"message": "Hello Items!", "params": commons}


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return {"message": "Hello Users!", "params": commons}


client = TestClient(app)


async def override_dependency(q: str | None = None):
    return {"q": q, "skip": 5, "limit": 10}


app.dependency_overrides[common_parameters] = override_dependency


def test_override_in_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": None, "skip": 5, "limit": 10},
    }


def test_override_in_items_with_q():
    response = client.get("/items/?q=foo")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }


def test_override_in_items_with_params():
    response = client.get("/items/?q=foo&skip=100&limit=200")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }
```

Example 4 (python):
```python
from typing import Union

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


async def common_parameters(
    q: Union[str, None] = None, skip: int = 0, limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return {"message": "Hello Items!", "params": commons}


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return {"message": "Hello Users!", "params": commons}


client = TestClient(app)


async def override_dependency(q: Union[str, None] = None):
    return {"q": q, "skip": 5, "limit": 10}


app.dependency_overrides[common_parameters] = override_dependency


def test_override_in_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": None, "skip": 5, "limit": 10},
    }


def test_override_in_items_with_q():
    response = client.get("/items/?q=foo")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }


def test_override_in_items_with_params():
    response = client.get("/items/?q=foo&skip=100&limit=200")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }
```

---

## Global Dependencies¶

**URL:** https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/

**Contents:**
- Global Dependencies¶
- Dependencies for groups of path operations¶

For some types of applications you might want to add dependencies to the whole application.

Similar to the way you can add dependencies to the path operation decorators, you can add them to the FastAPI application.

In that case, they will be applied to all the path operations in the application:

Prefer to use the Annotated version if possible.

And all the ideas in the section about adding dependencies to the path operation decorators still apply, but in this case, to all of the path operations in the app.

Later, when reading about how to structure bigger applications (Bigger Applications - Multiple Files), possibly with multiple files, you will learn how to declare a single dependencies parameter for a group of path operations.

**Examples:**

Example 1 (python):
```python
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException


async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])


@app.get("/items/")
async def read_items():
    return [{"item": "Portal Gun"}, {"item": "Plumbus"}]


@app.get("/users/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]
```

Example 2 (python):
```python
from fastapi import Depends, FastAPI, Header, HTTPException


async def verify_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header()):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])


@app.get("/items/")
async def read_items():
    return [{"item": "Portal Gun"}, {"item": "Plumbus"}]


@app.get("/users/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]
```

---

## Dependencies - Depends() and Security()¶

**URL:** https://fastapi.tiangolo.com/reference/dependencies/

**Contents:**
- Dependencies - Depends() and Security()¶
- Depends()¶
- fastapi.Depends ¶
- Security()¶
- fastapi.Security ¶

Dependencies are handled mainly with the special function Depends() that takes a callable.

Here is the reference for it and its parameters.

You can import it directly from fastapi:

Declare a FastAPI dependency.

It takes a single "dependable" callable (like a function).

Don't call it directly, FastAPI will call it for you.

Read more about it in the FastAPI docs for Dependencies.

A "dependable" callable (like a function).

Don't call it directly, FastAPI will call it for you, just pass the object directly.

TYPE: Optional[Callable[..., Any]] DEFAULT: None

By default, after a dependency is called the first time in a request, if the dependency is declared again for the rest of the request (for example if the dependency is needed by several dependencies), the value will be re-used for the rest of the request.

Set use_cache to False to disable this behavior and ensure the dependency is called again (if declared more than once) in the same request.

TYPE: bool DEFAULT: True

Mainly for dependencies with yield, define when the dependency function should start (the code before yield) and when it should end (the code after yield).

TYPE: Union[Literal['function', 'request'], None] DEFAULT: None

For many scenarios, you can handle security (authorization, authentication, etc.) with dependencies, using Depends().

But when you want to also declare OAuth2 scopes, you can use Security() instead of Depends().

You can import Security() directly from fastapi:

Declare a FastAPI Security dependency.

The only difference with a regular dependency is that it can declare OAuth2 scopes that will be integrated with OpenAPI and the automatic UI docs (by default at /docs).

It takes a single "dependable" callable (like a function).

Don't call it directly, FastAPI will call it for you.

Read more about it in the FastAPI docs for Security and in the FastAPI docs for OAuth2 scopes.

A "dependable" callable (like a function).

Don't call it directly, FastAPI will call it for you, just pass the object directly.

TYPE: Optional[Callable[..., Any]] DEFAULT: None

OAuth2 scopes required for the path operation that uses this Security dependency.

The term "scope" comes from the OAuth2 specification, it seems to be intentionally vague and interpretable. It normally refers to permissions, in cases to roles.

These scopes are integrated with OpenAPI (and the API docs at /docs). So they are visible in the OpenAPI specification. )

TYPE: Optional[Sequence[str]] DEFAULT: None

By default, after a dependency is called the first time in a request, if the dependency is declared again for the rest of the request (for example if the dependency is needed by several dependencies), the value will be re-used for the rest of the request.

Set use_cache to False to disable this behavior and ensure the dependency is called again (if declared more than once) in the same request.

TYPE: bool DEFAULT: True

**Examples:**

Example 1 (python):
```python
from fastapi import Depends
```

Example 2 (rust):
```rust
Depends(dependency=None, *, use_cache=True, scope=None)
```

Example 3 (python):
```python
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
```

Example 4 (python):
```python
def Depends(  # noqa: N802
    dependency: Annotated[
        Optional[Callable[..., Any]],
        Doc(
            """
            A "dependable" callable (like a function).

            Don't call it directly, FastAPI will call it for you, just pass the object
            directly.
            """
        ),
    ] = None,
    *,
    use_cache: Annotated[
        bool,
        Doc(
            """
            By default, after a dependency is called the first time in a request, if
            the dependency is declared again for the rest of the request (for example
            if the dependency is needed by several dependencies), the value will be
            re-used for the rest of the request.

            Set `use_cache` to `False` to disable this behavior and ensure the
            dependency is called again (if declared more than once) in the same request.
            """
        ),
    ] = True,
    scope: Annotated[
        Union[Literal["function", "request"], None],
        Doc(
            """
            Mainly for dependencies with `yield`, define when the dependency function
            should start (the code before `yield`) and when it should end (the code
            after `yield`).

            * `"function"`: start the dependency before the *path operation function*
                that handles the request, end the dependency after the *path operation
                function* ends, but **before** the response is sent back to the client.
                So, the dependency function will be executed **around** the *path operation
                **function***.
            * `"request"`: start the dependency before the *path operation function*
                that handles the request (similar to when using `"function"`), but end
                **after** the response is sent back to the client. So, the dependency
                function will be executed **around** the **request** and response cycle.
            """
        ),
    ] = None,
) -> Any:
    """
    Declare a FastAPI dependency.

    It takes a single "dependable" callable (like a function).

    Don't call it directly, FastAPI will call it for you.

    Read more about it in the
    [FastAPI docs for Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/).

    **Example**

    ```python
    from typing import Annotated

    from fastapi import Depends, FastAPI

    app = FastAPI()


    async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
        return {"q": q, "skip": skip, "limit": limit}


    @app.get("/items/")
    async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
        return commons
    ```
    """
    return params.Depends(dependency=dependency, use_cache=use_cache, scope=scope)
```

---

## Classes as Dependencies¶

**URL:** https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/

**Contents:**
- Classes as Dependencies¶
- A dict from the previous example¶
- What makes a dependency¶
- Classes as dependencies¶
- Use it¶
- Type annotation vs Depends¶
- Shortcut¶

Before diving deeper into the Dependency Injection system, let's upgrade the previous example.

In the previous example, we were returning a dict from our dependency ("dependable"):

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

But then we get a dict in the parameter commons of the path operation function.

And we know that editors can't provide a lot of support (like completion) for dicts, because they can't know their keys and value types.

Up to now you have seen dependencies declared as functions.

But that's not the only way to declare dependencies (although it would probably be the more common).

The key factor is that a dependency should be a "callable".

A "callable" in Python is anything that Python can "call" like a function.

So, if you have an object something (that might not be a function) and you can "call" it (execute it) like:

then it is a "callable".

You might notice that to create an instance of a Python class, you use that same syntax.

In this case, fluffy is an instance of the class Cat.

And to create fluffy, you are "calling" Cat.

So, a Python class is also a callable.

Then, in FastAPI, you could use a Python class as a dependency.

What FastAPI actually checks is that it is a "callable" (function, class or anything else) and the parameters defined.

If you pass a "callable" as a dependency in FastAPI, it will analyze the parameters for that "callable", and process them in the same way as the parameters for a path operation function. Including sub-dependencies.

That also applies to callables with no parameters at all. The same as it would be for path operation functions with no parameters.

Then, we can change the dependency "dependable" common_parameters from above to the class CommonQueryParams:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Pay attention to the __init__ method used to create the instance of the class:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

...it has the same parameters as our previous common_parameters:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Those parameters are what FastAPI will use to "solve" the dependency.

In both cases, it will have:

In both cases the data will be converted, validated, documented on the OpenAPI schema, etc.

Now you can declare your dependency using this class.

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

FastAPI calls the CommonQueryParams class. This creates an "instance" of that class and the instance will be passed as the parameter commons to your function.

Notice how we write CommonQueryParams twice in the above code:

Prefer to use the Annotated version if possible.

The last CommonQueryParams, in:

...is what FastAPI will actually use to know what is the dependency.

It is from this one that FastAPI will extract the declared parameters and that is what FastAPI will actually call.

In this case, the first CommonQueryParams, in:

Prefer to use the Annotated version if possible.

...doesn't have any special meaning for FastAPI. FastAPI won't use it for data conversion, validation, etc. (as it is using the Depends(CommonQueryParams) for that).

You could actually write just:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

But declaring the type is encouraged as that way your editor will know what will be passed as the parameter commons, and then it can help you with code completion, type checks, etc:

But you see that we are having some code repetition here, writing CommonQueryParams twice:

Prefer to use the Annotated version if possible.

FastAPI provides a shortcut for these cases, in where the dependency is specifically a class that FastAPI will "call" to create an instance of the class itself.

For those specific cases, you can do the following:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

You declare the dependency as the type of the parameter, and you use Depends() without any parameter, instead of having to write the full class again inside of Depends(CommonQueryParams).

The same example would then look like:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

...and FastAPI will know what to do.

If that seems more confusing than helpful, disregard it, you don't need it.

It is just a shortcut. Because FastAPI cares about helping you minimize code repetition.

**Examples:**

Example 1 (python):
```python
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
```

Example 2 (python):
```python
from typing import Annotated, Union

from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(
    q: Union[str, None] = None, skip: int = 0, limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
```

Example 3 (python):
```python
from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons
```

Example 4 (python):
```python
from typing import Union

from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(
    q: Union[str, None] = None, skip: int = 0, limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons
```

---

## Sub-dependencies¶

**URL:** https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/

**Contents:**
- Sub-dependencies¶
- First dependency "dependable"¶
- Second dependency, "dependable" and "dependant"¶
- Use the dependency¶
- Using the same dependency multiple times¶
- Recap¶

You can create dependencies that have sub-dependencies.

They can be as deep as you need them to be.

FastAPI will take care of solving them.

You could create a first dependency ("dependable") like:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

It declares an optional query parameter q as a str, and then it just returns it.

This is quite simple (not very useful), but will help us focus on how the sub-dependencies work.

Then you can create another dependency function (a "dependable") that at the same time declares a dependency of its own (so it is a "dependant" too):

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Let's focus on the parameters declared:

Then we can use the dependency with:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Notice that we are only declaring one dependency in the path operation function, the query_or_cookie_extractor.

But FastAPI will know that it has to solve query_extractor first, to pass the results of that to query_or_cookie_extractor while calling it.

If one of your dependencies is declared multiple times for the same path operation, for example, multiple dependencies have a common sub-dependency, FastAPI will know to call that sub-dependency only once per request.

And it will save the returned value in a "cache" and pass it to all the "dependants" that need it in that specific request, instead of calling the dependency multiple times for the same request.

In an advanced scenario where you know you need the dependency to be called at every step (possibly multiple times) in the same request instead of using the "cached" value, you can set the parameter use_cache=False when using Depends:

Prefer to use the Annotated version if possible.

Apart from all the fancy words used here, the Dependency Injection system is quite simple.

Just functions that look the same as the path operation functions.

But still, it is very powerful, and allows you to declare arbitrarily deeply nested dependency "graphs" (trees).

All this might not seem as useful with these simple examples.

But you will see how useful it is in the chapters about security.

And you will also see the amounts of code it will save you.

**Examples:**

Example 1 (python):
```python
from typing import Annotated

from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


def query_extractor(q: str | None = None):
    return q


def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
):
    return {"q_or_cookie": query_or_default}
```

Example 2 (python):
```python
from typing import Annotated, Union

from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


def query_extractor(q: Union[str, None] = None):
    return q


def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[Union[str, None], Cookie()] = None,
):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
):
    return {"q_or_cookie": query_or_default}
```

Example 3 (python):
```python
from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


def query_extractor(q: str | None = None):
    return q


def query_or_cookie_extractor(
    q: str = Depends(query_extractor), last_query: str | None = Cookie(default=None)
):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}
```

Example 4 (python):
```python
from typing import Union

from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


def query_extractor(q: Union[str, None] = None):
    return q


def query_or_cookie_extractor(
    q: str = Depends(query_extractor),
    last_query: Union[str, None] = Cookie(default=None),
):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}
```

---

## Advanced Dependencies¶

**URL:** https://fastapi.tiangolo.com/advanced/advanced-dependencies/

**Contents:**
- Advanced Dependencies¶
- Parameterized dependencies¶
- A "callable" instance¶
- Parameterize the instance¶
- Create an instance¶
- Use the instance as a dependency¶
- Dependencies with yield, HTTPException, except and Background Tasks¶
  - Dependencies with yield and scope¶
  - Dependencies with yield and StreamingResponse, Technical Details¶
    - Use Cases with Early Exit Code¶

All the dependencies we have seen are a fixed function or class.

But there could be cases where you want to be able to set parameters on the dependency, without having to declare many different functions or classes.

Let's imagine that we want to have a dependency that checks if the query parameter q contains some fixed content.

But we want to be able to parameterize that fixed content.

In Python there's a way to make an instance of a class a "callable".

Not the class itself (which is already a callable), but an instance of that class.

To do that, we declare a method __call__:

Prefer to use the Annotated version if possible.

In this case, this __call__ is what FastAPI will use to check for additional parameters and sub-dependencies, and this is what will be called to pass a value to the parameter in your path operation function later.

And now, we can use __init__ to declare the parameters of the instance that we can use to "parameterize" the dependency:

Prefer to use the Annotated version if possible.

In this case, FastAPI won't ever touch or care about __init__, we will use it directly in our code.

We could create an instance of this class with:

Prefer to use the Annotated version if possible.

And that way we are able to "parameterize" our dependency, that now has "bar" inside of it, as the attribute checker.fixed_content.

Then, we could use this checker in a Depends(checker), instead of Depends(FixedContentQueryChecker), because the dependency is the instance, checker, not the class itself.

And when solving the dependency, FastAPI will call this checker like:

...and pass whatever that returns as the value of the dependency in our path operation function as the parameter fixed_content_included:

Prefer to use the Annotated version if possible.

All this might seem contrived. And it might not be very clear how is it useful yet.

These examples are intentionally simple, but show how it all works.

In the chapters about security, there are utility functions that are implemented in this same way.

If you understood all this, you already know how those utility tools for security work underneath.

You most probably don't need these technical details.

These details are useful mainly if you had a FastAPI application older than 0.121.0 and you are facing issues with dependencies with yield.

Dependencies with yield have evolved over time to account for the different use cases and to fix some issues, here's a summary of what has changed.

In version 0.121.0, FastAPI added support for Depends(scope="function") for dependencies with yield.

Using Depends(scope="function"), the exit code after yield is executed right after the path operation function is finished, before the response is sent back to the client.

And when using Depends(scope="request") (the default), the exit code after yield is executed after the response is sent.

You can read more about it in the docs for Dependencies with yield - Early exit and scope.

Before FastAPI 0.118.0, if you used a dependency with yield, it would run the exit code after the path operation function returned but right before sending the response.

The intention was to avoid holding resources for longer than necessary, waiting for the response to travel through the network.

This change also meant that if you returned a StreamingResponse, the exit code of the dependency with yield would have been already run.

For example, if you had a database session in a dependency with yield, the StreamingResponse would not be able to use that session while streaming data because the session would have already been closed in the exit code after yield.

This behavior was reverted in 0.118.0, to make the exit code after yield be executed after the response is sent.

As you will see below, this is very similar to the behavior before version 0.106.0, but with several improvements and bug fixes for corner cases.

There are some use cases with specific conditions that could benefit from the old behavior of running the exit code of dependencies with yield before sending the response.

For example, imagine you have code that uses a database session in a dependency with yield only to verify a user, but the database session is never used again in the path operation function, only in the dependency, and the response takes a long time to be sent, like a StreamingResponse that sends data slowly, but for some reason doesn't use the database.

In this case, the database session would be held until the response is finished being sent, but if you don't use it, then it wouldn't be necessary to hold it.

Here's how it could look like:

The exit code, the automatic closing of the Session in:

...would be run after the the response finishes sending the slow data:

But as generate_stream() doesn't use the database session, it is not really necessary to keep the session open while sending the response.

If you have this specific use case using SQLModel (or SQLAlchemy), you could explicitly close the session after you don't need it anymore:

That way the session would release the database connection, so other requests could use it.

If you have a different use case that needs to exit early from a dependency with yield, please create a GitHub Discussion Question with your specific use case and why you would benefit from having early closing for dependencies with yield.

If there are compelling use cases for early closing in dependencies with yield, I would consider adding a new way to opt in to early closing.

Before FastAPI 0.110.0, if you used a dependency with yield, and then you captured an exception with except in that dependency, and you didn't raise the exception again, the exception would be automatically raised/forwarded to any exception handlers or the internal server error handler.

This was changed in version 0.110.0 to fix unhandled memory consumption from forwarded exceptions without a handler (internal server errors), and to make it consistent with the behavior of regular Python code.

Before FastAPI 0.106.0, raising exceptions after yield was not possible, the exit code in dependencies with yield was executed after the response was sent, so Exception Handlers would have already run.

This was designed this way mainly to allow using the same objects "yielded" by dependencies inside of background tasks, because the exit code would be executed after the background tasks were finished.

This was changed in FastAPI 0.106.0 with the intention to not hold resources while waiting for the response to travel through the network.

Additionally, a background task is normally an independent set of logic that should be handled separately, with its own resources (e.g. its own database connection).

So, this way you will probably have cleaner code.

If you used to rely on this behavior, now you should create the resources for background tasks inside the background task itself, and use internally only data that doesn't depend on the resources of dependencies with yield.

For example, instead of using the same database session, you would create a new database session inside of the background task, and you would obtain the objects from the database using this new session. And then instead of passing the object from the database as a parameter to the background task function, you would pass the ID of that object and then obtain the object again inside the background task function.

**Examples:**

Example 1 (python):
```python
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False


checker = FixedContentQueryChecker("bar")


@app.get("/query-checker/")
async def read_query_check(fixed_content_included: Annotated[bool, Depends(checker)]):
    return {"fixed_content_in_query": fixed_content_included}
```

Example 2 (python):
```python
from fastapi import Depends, FastAPI

app = FastAPI()


class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False


checker = FixedContentQueryChecker("bar")


@app.get("/query-checker/")
async def read_query_check(fixed_content_included: bool = Depends(checker)):
    return {"fixed_content_in_query": fixed_content_included}
```

Example 3 (python):
```python
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False


checker = FixedContentQueryChecker("bar")


@app.get("/query-checker/")
async def read_query_check(fixed_content_included: Annotated[bool, Depends(checker)]):
    return {"fixed_content_in_query": fixed_content_included}
```

Example 4 (python):
```python
from fastapi import Depends, FastAPI

app = FastAPI()


class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False


checker = FixedContentQueryChecker("bar")


@app.get("/query-checker/")
async def read_query_check(fixed_content_included: bool = Depends(checker)):
    return {"fixed_content_in_query": fixed_content_included}
```

---
