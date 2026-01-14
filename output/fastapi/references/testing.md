# Fastapi - Testing

**Pages:** 1

---

## Testing¶

**URL:** https://fastapi.tiangolo.com/tutorial/testing/

**Contents:**
- Testing¶
- Using TestClient¶
- Separating tests¶
  - FastAPI app file¶
  - Testing file¶
- Testing: extended example¶
  - Extended FastAPI app file¶
  - Extended testing file¶
- Run it¶

Thanks to Starlette, testing FastAPI applications is easy and enjoyable.

It is based on HTTPX, which in turn is designed based on Requests, so it's very familiar and intuitive.

With it, you can use pytest directly with FastAPI.

To use TestClient, first install httpx.

Make sure you create a virtual environment, activate it, and then install it, for example:

Create a TestClient by passing your FastAPI application to it.

Create functions with a name that starts with test_ (this is standard pytest conventions).

Use the TestClient object the same way as you do with httpx.

Write simple assert statements with the standard Python expressions that you need to check (again, standard pytest).

Notice that the testing functions are normal def, not async def.

And the calls to the client are also normal calls, not using await.

This allows you to use pytest directly without complications.

You could also use from starlette.testclient import TestClient.

FastAPI provides the same starlette.testclient as fastapi.testclient just as a convenience for you, the developer. But it comes directly from Starlette.

If you want to call async functions in your tests apart from sending requests to your FastAPI application (e.g. asynchronous database functions), have a look at the Async Tests in the advanced tutorial.

In a real application, you probably would have your tests in a different file.

And your FastAPI application might also be composed of several files/modules, etc.

Let's say you have a file structure as described in Bigger Applications:

In the file main.py you have your FastAPI app:

Then you could have a file test_main.py with your tests. It could live on the same Python package (the same directory with a __init__.py file):

Because this file is in the same package, you can use relative imports to import the object app from the main module (main.py):

...and have the code for the tests just like before.

Now let's extend this example and add more details to see how to test different parts.

Let's continue with the same file structure as before:

Let's say that now the file main.py with your FastAPI app has some other path operations.

It has a GET operation that could return an error.

It has a POST operation that could return several errors.

Both path operations require an X-Token header.

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

You could then update test_main.py with the extended tests:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Whenever you need the client to pass information in the request and you don't know how to, you can search (Google) how to do it in httpx, or even how to do it with requests, as HTTPX's design is based on Requests' design.

Then you just do the same in your tests.

For more information about how to pass data to the backend (using httpx or the TestClient) check the HTTPX documentation.

Note that the TestClient receives data that can be converted to JSON, not Pydantic models.

If you have a Pydantic model in your test and you want to send its data to the application during testing, you can use the jsonable_encoder described in JSON Compatible Encoder.

After that, you just need to install pytest.

Make sure you create a virtual environment, activate it, and then install it, for example:

It will detect the files and tests automatically, execute them, and report the results back to you.

**Examples:**

Example 1 (unknown):
```unknown
$ pip install httpx
```

Example 2 (python):
```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

Example 3 (unknown):
```unknown
.
├── app
│   ├── __init__.py
│   └── main.py
```

Example 4 (python):
```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}
```

---
