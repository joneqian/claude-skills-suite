# Fastapi - Request Data

**Pages:** 17

---

## Custom Request and APIRoute class¶

**URL:** https://fastapi.tiangolo.com/how-to/custom-request-and-route/

**Contents:**
- Custom Request and APIRoute class¶
- Use cases¶
- Handling custom request body encodings¶
  - Create a custom GzipRequest class¶
  - Create a custom GzipRoute class¶
- Accessing the request body in an exception handler¶
- Custom APIRoute class in a router¶

In some cases, you may want to override the logic used by the Request and APIRoute classes.

In particular, this may be a good alternative to logic in a middleware.

For example, if you want to read or manipulate the request body before it is processed by your application.

This is an "advanced" feature.

If you are just starting with FastAPI you might want to skip this section.

Some use cases include:

Let's see how to make use of a custom Request subclass to decompress gzip requests.

And an APIRoute subclass to use that custom request class.

This is a toy example to demonstrate how it works, if you need Gzip support, you can use the provided GzipMiddleware.

First, we create a GzipRequest class, which will overwrite the Request.body() method to decompress the body in the presence of an appropriate header.

If there's no gzip in the header, it will not try to decompress the body.

That way, the same route class can handle gzip compressed or uncompressed requests.

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Next, we create a custom subclass of fastapi.routing.APIRoute that will make use of the GzipRequest.

This time, it will overwrite the method APIRoute.get_route_handler().

This method returns a function. And that function is what will receive a request and return a response.

Here we use it to create a GzipRequest from the original request.

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

A Request has a request.scope attribute, that's just a Python dict containing the metadata related to the request.

A Request also has a request.receive, that's a function to "receive" the body of the request.

The scope dict and receive function are both part of the ASGI specification.

And those two things, scope and receive, are what is needed to create a new Request instance.

To learn more about the Request check Starlette's docs about Requests.

The only thing the function returned by GzipRequest.get_route_handler does differently is convert the Request to a GzipRequest.

Doing this, our GzipRequest will take care of decompressing the data (if necessary) before passing it to our path operations.

After that, all of the processing logic is the same.

But because of our changes in GzipRequest.body, the request body will be automatically decompressed when it is loaded by FastAPI when needed.

To solve this same problem, it's probably a lot easier to use the body in a custom handler for RequestValidationError (Handling Errors).

But this example is still valid and it shows how to interact with the internal components.

We can also use this same approach to access the request body in an exception handler.

All we need to do is handle the request inside a try/except block:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

If an exception occurs, theRequest instance will still be in scope, so we can read and make use of the request body when handling the error:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

You can also set the route_class parameter of an APIRouter:

In this example, the path operations under the router will use the custom TimedRoute class, and will have an extra X-Response-Time header in the response with the time it took to generate the response:

**Examples:**

Example 1 (python):
```python
import gzip
from collections.abc import Callable
from typing import Annotated

from fastapi import Body, FastAPI, Request, Response
from fastapi.routing import APIRoute


class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body


class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler


app = FastAPI()
app.router.route_class = GzipRoute


@app.post("/sum")
async def sum_numbers(numbers: Annotated[list[int], Body()]):
    return {"sum": sum(numbers)}
```

Example 2 (python):
```python
import gzip
from typing import Annotated, Callable

from fastapi import Body, FastAPI, Request, Response
from fastapi.routing import APIRoute


class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body


class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler


app = FastAPI()
app.router.route_class = GzipRoute


@app.post("/sum")
async def sum_numbers(numbers: Annotated[list[int], Body()]):
    return {"sum": sum(numbers)}
```

Example 3 (python):
```python
import gzip
from collections.abc import Callable

from fastapi import Body, FastAPI, Request, Response
from fastapi.routing import APIRoute


class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body


class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler


app = FastAPI()
app.router.route_class = GzipRoute


@app.post("/sum")
async def sum_numbers(numbers: list[int] = Body()):
    return {"sum": sum(numbers)}
```

Example 4 (python):
```python
import gzip
from typing import Callable

from fastapi import Body, FastAPI, Request, Response
from fastapi.routing import APIRoute


class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body


class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler


app = FastAPI()
app.router.route_class = GzipRoute


@app.post("/sum")
async def sum_numbers(numbers: list[int] = Body()):
    return {"sum": sum(numbers)}
```

---

## Body - Updates¶

**URL:** https://fastapi.tiangolo.com/tutorial/body-updates/

**Contents:**
- Body - Updates¶
- Update replacing with PUT¶
  - Warning about replacing¶
- Partial updates with PATCH¶
  - Using Pydantic's exclude_unset parameter¶
  - Using Pydantic's update parameter¶
  - Partial updates recap¶

To update an item you can use the HTTP PUT operation.

You can use the jsonable_encoder to convert the input data to data that can be stored as JSON (e.g. with a NoSQL database). For example, converting datetime to str.

PUT is used to receive data that should replace the existing data.

That means that if you want to update the item bar using PUT with a body containing:

because it doesn't include the already stored attribute "tax": 20.2, the input model would take the default value of "tax": 10.5.

And the data would be saved with that "new" tax of 10.5.

You can also use the HTTP PATCH operation to partially update data.

This means that you can send only the data that you want to update, leaving the rest intact.

PATCH is less commonly used and known than PUT.

And many teams use only PUT, even for partial updates.

You are free to use them however you want, FastAPI doesn't impose any restrictions.

But this guide shows you, more or less, how they are intended to be used.

If you want to receive partial updates, it's very useful to use the parameter exclude_unset in Pydantic's model's .model_dump().

Like item.model_dump(exclude_unset=True).

That would generate a dict with only the data that was set when creating the item model, excluding default values.

Then you can use this to generate a dict with only the data that was set (sent in the request), omitting default values:

Now, you can create a copy of the existing model using .model_copy(), and pass the update parameter with a dict containing the data to update.

Like stored_item_model.model_copy(update=update_data):

In summary, to apply partial updates you would:

You can actually use this same technique with an HTTP PUT operation.

But the example here uses PATCH because it was created for these use cases.

Notice that the input model is still validated.

So, if you want to receive partial updates that can omit all the attributes, you need to have a model with all the attributes marked as optional (with default values or None).

To distinguish from the models with all optional values for updates and models with required values for creation, you can use the ideas described in Extra Models.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded
```

Example 2 (python):
```python
from typing import Union

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: Union[str, None] = None
    description: Union[str, None] = None
    price: Union[float, None] = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded
```

Example 3 (json):
```json
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
```

Example 4 (python):
```python
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.model_dump(exclude_unset=True)
    updated_item = stored_item_model.model_copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item
```

---

## Header Parameters¶

**URL:** https://fastapi.tiangolo.com/tutorial/header-params/

**Contents:**
- Header Parameters¶
- Import Header¶
- Declare Header parameters¶
- Automatic conversion¶
- Duplicate headers¶
- Recap¶

You can define Header parameters the same way you define Query, Path and Cookie parameters.

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Then declare the header parameters using the same structure as with Path, Query and Cookie.

You can define the default value as well as all the extra validation or annotation parameters:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Header is a "sister" class of Path, Query and Cookie. It also inherits from the same common Param class.

But remember that when you import Query, Path, Header, and others from fastapi, those are actually functions that return special classes.

To declare headers, you need to use Header, because otherwise the parameters would be interpreted as query parameters.

Header has a little extra functionality on top of what Path, Query and Cookie provide.

Most of the standard headers are separated by a "hyphen" character, also known as the "minus symbol" (-).

But a variable like user-agent is invalid in Python.

So, by default, Header will convert the parameter names characters from underscore (_) to hyphen (-) to extract and document the headers.

Also, HTTP headers are case-insensitive, so, you can declare them with standard Python style (also known as "snake_case").

So, you can use user_agent as you normally would in Python code, instead of needing to capitalize the first letters as User_Agent or something similar.

If for some reason you need to disable automatic conversion of underscores to hyphens, set the parameter convert_underscores of Header to False:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Before setting convert_underscores to False, bear in mind that some HTTP proxies and servers disallow the usage of headers with underscores.

It is possible to receive duplicate headers. That means, the same header with multiple values.

You can define those cases using a list in the type declaration.

You will receive all the values from the duplicate header as a Python list.

For example, to declare a header of X-Token that can appear more than once, you can write:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

If you communicate with that path operation sending two HTTP headers like:

The response would be like:

Declare headers with Header, using the same common pattern as Query, Path and Cookie.

And don't worry about underscores in your variables, FastAPI will take care of converting them.

**Examples:**

Example 1 (python):
```python
from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
```

Example 2 (python):
```python
from typing import Annotated, Union

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Annotated[Union[str, None], Header()] = None):
    return {"User-Agent": user_agent}
```

Example 3 (python):
```python
from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: str | None = Header(default=None)):
    return {"User-Agent": user_agent}
```

Example 4 (python):
```python
from typing import Union

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Union[str, None] = Header(default=None)):
    return {"User-Agent": user_agent}
```

---

## Body - Fields¶

**URL:** https://fastapi.tiangolo.com/tutorial/body-fields/

**Contents:**
- Body - Fields¶
- Import Field¶
- Declare model attributes¶
- Add extra information¶
- Recap¶

The same way you can declare additional validation and metadata in path operation function parameters with Query, Path and Body, you can declare validation and metadata inside of Pydantic models using Pydantic's Field.

First, you have to import it:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Notice that Field is imported directly from pydantic, not from fastapi as are all the rest (Query, Path, Body, etc).

You can then use Field with model attributes:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Field works the same way as Query, Path and Body, it has all the same parameters, etc.

Actually, Query, Path and others you'll see next create objects of subclasses of a common Param class, which is itself a subclass of Pydantic's FieldInfo class.

And Pydantic's Field returns an instance of FieldInfo as well.

Body also returns objects of a subclass of FieldInfo directly. And there are others you will see later that are subclasses of the Body class.

Remember that when you import Query, Path, and others from fastapi, those are actually functions that return special classes.

Notice how each model's attribute with a type, default value and Field has the same structure as a path operation function's parameter, with Field instead of Path, Query and Body.

You can declare extra information in Field, Query, Body, etc. And it will be included in the generated JSON Schema.

You will learn more about adding extra information later in the docs, when learning to declare examples.

Extra keys passed to Field will also be present in the resulting OpenAPI schema for your application. As these keys may not necessarily be part of the OpenAPI specification, some OpenAPI tools, for example the OpenAPI validator, may not work with your generated schema.

You can use Pydantic's Field to declare extra validations and metadata for model attributes.

You can also use the extra keyword arguments to pass additional JSON Schema metadata.

**Examples:**

Example 1 (python):
```python
from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results
```

Example 2 (python):
```python
from typing import Annotated, Union

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results
```

Example 3 (python):
```python
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
```

Example 4 (python):
```python
from typing import Union

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
```

---

## Using the Request Directly¶

**URL:** https://fastapi.tiangolo.com/advanced/using-request-directly/

**Contents:**
- Using the Request Directly¶
- Details about the Request object¶
- Use the Request object directly¶
- Request documentation¶

Up to now, you have been declaring the parts of the request that you need with their types.

And by doing so, FastAPI is validating that data, converting it and generating documentation for your API automatically.

But there are situations where you might need to access the Request object directly.

As FastAPI is actually Starlette underneath, with a layer of several tools on top, you can use Starlette's Request object directly when you need to.

It would also mean that if you get data from the Request object directly (for example, read the body) it won't be validated, converted or documented (with OpenAPI, for the automatic API user interface) by FastAPI.

Although any other parameter declared normally (for example, the body with a Pydantic model) would still be validated, converted, annotated, etc.

But there are specific cases where it's useful to get the Request object.

Let's imagine you want to get the client's IP address/host inside of your path operation function.

For that you need to access the request directly.

By declaring a path operation function parameter with the type being the Request FastAPI will know to pass the Request in that parameter.

Note that in this case, we are declaring a path parameter beside the request parameter.

So, the path parameter will be extracted, validated, converted to the specified type and annotated with OpenAPI.

The same way, you can declare any other parameter as normally, and additionally, get the Request too.

You can read more details about the Request object in the official Starlette documentation site.

You could also use from starlette.requests import Request.

FastAPI provides it directly just as a convenience for you, the developer. But it comes directly from Starlette.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/items/{item_id}")
def read_root(item_id: str, request: Request):
    client_host = request.client.host
    return {"client_host": client_host, "item_id": item_id}
```

---

## Request Body¶

**URL:** https://fastapi.tiangolo.com/tutorial/body/

**Contents:**
- Request Body¶
- Import Pydantic's BaseModel¶
- Create your data model¶
- Declare it as a parameter¶
- Results¶
- Automatic docs¶
- Editor support¶
- Use the model¶
- Request body + path parameters¶
- Request body + path + query parameters¶

When you need to send data from a client (let's say, a browser) to your API, you send it as a request body.

A request body is data sent by the client to your API. A response body is the data your API sends to the client.

Your API almost always has to send a response body. But clients don't necessarily need to send request bodies all the time, sometimes they only request a path, maybe with some query parameters, but don't send a body.

To declare a request body, you use Pydantic models with all their power and benefits.

To send data, you should use one of: POST (the more common), PUT, DELETE or PATCH.

Sending a body with a GET request has an undefined behavior in the specifications, nevertheless, it is supported by FastAPI, only for very complex/extreme use cases.

As it is discouraged, the interactive docs with Swagger UI won't show the documentation for the body when using GET, and proxies in the middle might not support it.

First, you need to import BaseModel from pydantic:

Then you declare your data model as a class that inherits from BaseModel.

Use standard Python types for all the attributes:

The same as when declaring query parameters, when a model attribute has a default value, it is not required. Otherwise, it is required. Use None to make it just optional.

For example, this model above declares a JSON "object" (or Python dict) like:

...as description and tax are optional (with a default value of None), this JSON "object" would also be valid:

To add it to your path operation, declare it the same way you declared path and query parameters:

...and declare its type as the model you created, Item.

With just that Python type declaration, FastAPI will:

The JSON Schemas of your models will be part of your OpenAPI generated schema, and will be shown in the interactive API docs:

And will also be used in the API docs inside each path operation that needs them:

In your editor, inside your function you will get type hints and completion everywhere (this wouldn't happen if you received a dict instead of a Pydantic model):

You also get error checks for incorrect type operations:

This is not by chance, the whole framework was built around that design.

And it was thoroughly tested at the design phase, before any implementation, to ensure it would work with all the editors.

There were even some changes to Pydantic itself to support this.

The previous screenshots were taken with Visual Studio Code.

But you would get the same editor support with PyCharm and most of the other Python editors:

If you use PyCharm as your editor, you can use the Pydantic PyCharm Plugin.

It improves editor support for Pydantic models, with:

Inside of the function, you can access all the attributes of the model object directly:

You can declare path parameters and request body at the same time.

FastAPI will recognize that the function parameters that match path parameters should be taken from the path, and that function parameters that are declared to be Pydantic models should be taken from the request body.

You can also declare body, path and query parameters, all at the same time.

FastAPI will recognize each of them and take the data from the correct place.

The function parameters will be recognized as follows:

FastAPI will know that the value of q is not required because of the default value = None.

The str | None (Python 3.10+) or Union in Union[str, None] (Python 3.9+) is not used by FastAPI to determine that the value is not required, it will know it's not required because it has a default value of = None.

But adding the type annotations will allow your editor to give you better support and detect errors.

If you don't want to use Pydantic models, you can also use Body parameters. See the docs for Body - Multiple Parameters: Singular values in body.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item
```

Example 2 (python):
```python
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item
```

Example 3 (python):
```python
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item
```

Example 4 (python):
```python
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item
```

---

## Request Forms and Files¶

**URL:** https://fastapi.tiangolo.com/tutorial/request-forms-and-files/

**Contents:**
- Request Forms and Files¶
- Import File and Form¶
- Define File and Form parameters¶
- Recap¶

You can define files and form fields at the same time using File and Form.

To receive uploaded files and/or form data, first install python-multipart.

Make sure you create a virtual environment, activate it, and then install it, for example:

Prefer to use the Annotated version if possible.

Create file and form parameters the same way you would for Body or Query:

Prefer to use the Annotated version if possible.

The files and form fields will be uploaded as form data and you will receive the files and form fields.

And you can declare some of the files as bytes and some as UploadFile.

You can declare multiple File and Form parameters in a path operation, but you can't also declare Body fields that you expect to receive as JSON, as the request will have the body encoded using multipart/form-data instead of application/json.

This is not a limitation of FastAPI, it's part of the HTTP protocol.

Use File and Form together when you need to receive data and files in the same request.

**Examples:**

Example 1 (unknown):
```unknown
$ pip install python-multipart
```

Example 2 (python):
```python
from typing import Annotated

from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
```

Example 3 (python):
```python
from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(
    file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
```

Example 4 (python):
```python
from typing import Annotated

from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
```

---

## Cookie Parameters¶

**URL:** https://fastapi.tiangolo.com/tutorial/cookie-params/

**Contents:**
- Cookie Parameters¶
- Import Cookie¶
- Declare Cookie parameters¶
- Recap¶

You can define Cookie parameters the same way you define Query and Path parameters.

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Then declare the cookie parameters using the same structure as with Path and Query.

You can define the default value as well as all the extra validation or annotation parameters:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Cookie is a "sister" class of Path and Query. It also inherits from the same common Param class.

But remember that when you import Query, Path, Cookie and others from fastapi, those are actually functions that return special classes.

To declare cookies, you need to use Cookie, because otherwise the parameters would be interpreted as query parameters.

Have in mind that, as browsers handle cookies in special ways and behind the scenes, they don't easily allow JavaScript to touch them.

If you go to the API docs UI at /docs you will be able to see the documentation for cookies for your path operations.

But even if you fill the data and click "Execute", because the docs UI works with JavaScript, the cookies won't be sent, and you will see an error message as if you didn't write any values.

Declare cookies with Cookie, using the same common pattern as Query and Path.

**Examples:**

Example 1 (python):
```python
from typing import Annotated

from fastapi import Cookie, FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}
```

Example 2 (python):
```python
from typing import Annotated, Union

from fastapi import Cookie, FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: Annotated[Union[str, None], Cookie()] = None):
    return {"ads_id": ads_id}
```

Example 3 (python):
```python
from fastapi import Cookie, FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: str | None = Cookie(default=None)):
    return {"ads_id": ads_id}
```

Example 4 (python):
```python
from typing import Union

from fastapi import Cookie, FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: Union[str, None] = Cookie(default=None)):
    return {"ads_id": ads_id}
```

---

## Form Data¶

**URL:** https://fastapi.tiangolo.com/tutorial/request-forms/

**Contents:**
- Form Data¶
- Import Form¶
- Define Form parameters¶
- About "Form Fields"¶
- Recap¶

When you need to receive form fields instead of JSON, you can use Form.

To use forms, first install python-multipart.

Make sure you create a virtual environment, activate it, and then install it, for example:

Import Form from fastapi:

Prefer to use the Annotated version if possible.

Create form parameters the same way you would for Body or Query:

Prefer to use the Annotated version if possible.

For example, in one of the ways the OAuth2 specification can be used (called "password flow") it is required to send a username and password as form fields.

The spec requires the fields to be exactly named username and password, and to be sent as form fields, not JSON.

With Form you can declare the same configurations as with Body (and Query, Path, Cookie), including validation, examples, an alias (e.g. user-name instead of username), etc.

Form is a class that inherits directly from Body.

To declare form bodies, you need to use Form explicitly, because without it the parameters would be interpreted as query parameters or body (JSON) parameters.

The way HTML forms (<form></form>) sends the data to the server normally uses a "special" encoding for that data, it's different from JSON.

FastAPI will make sure to read that data from the right place instead of JSON.

Data from forms is normally encoded using the "media type" application/x-www-form-urlencoded.

But when the form includes files, it is encoded as multipart/form-data. You'll read about handling files in the next chapter.

If you want to read more about these encodings and form fields, head to the MDN web docs for POST.

You can declare multiple Form parameters in a path operation, but you can't also declare Body fields that you expect to receive as JSON, as the request will have the body encoded using application/x-www-form-urlencoded instead of application/json.

This is not a limitation of FastAPI, it's part of the HTTP protocol.

Use Form to declare form data input parameters.

**Examples:**

Example 1 (unknown):
```unknown
$ pip install python-multipart
```

Example 2 (python):
```python
from typing import Annotated

from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}
```

Example 3 (python):
```python
from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}
```

Example 4 (python):
```python
from typing import Annotated

from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}
```

---

## Request Parameters¶

**URL:** https://fastapi.tiangolo.com/reference/parameters/

**Contents:**
- Request Parameters¶
- fastapi.Query ¶
- fastapi.Path ¶
- fastapi.Body ¶
- fastapi.Cookie ¶
- fastapi.Header ¶
- fastapi.Form ¶
- fastapi.File ¶

Here's the reference information for the request parameters.

These are the special functions that you can put in path operation function parameters or dependency functions with Annotated to get data from the request.

You can import them all directly from fastapi:

Default value if the parameter field is not set.

TYPE: Any DEFAULT: Undefined

A callable to generate the default value.

This doesn't affect Path parameters as the value is always required. The parameter is available only for compatibility.

TYPE: Union[Callable[[], Any], None] DEFAULT: _Unset

An alternative name for the parameter field.

This will be used to extract the data and for the generated OpenAPI. It is particularly useful when you can't use the name you want because it is a Python reserved keyword or similar.

TYPE: Optional[str] DEFAULT: None

Priority of the alias. This affects whether an alias generator is used.

TYPE: Union[int, None] DEFAULT: _Unset

'Whitelist' validation step. The parameter field will be the single one allowed by the alias or set of aliases defined.

TYPE: Union[str, AliasPath, AliasChoices, None] DEFAULT: None

'Blacklist' validation step. The vanilla parameter field will be the single one of the alias' or set of aliases' fields and all the other fields will be ignored at serialization time.

TYPE: Union[str, None] DEFAULT: None

Human-readable title.

TYPE: Optional[str] DEFAULT: None

Human-readable description.

TYPE: Optional[str] DEFAULT: None

Greater than. If set, value must be greater than this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Greater than or equal. If set, value must be greater than or equal to this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Less than. If set, value must be less than this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Less than or equal. If set, value must be less than or equal to this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Minimum length for strings.

TYPE: Optional[int] DEFAULT: None

Maximum length for strings.

TYPE: Optional[int] DEFAULT: None

RegEx pattern for strings.

TYPE: Optional[str] DEFAULT: None

Deprecated in FastAPI 0.100.0 and Pydantic v2, use pattern instead. RegEx pattern for strings.

TYPE: Optional[str] DEFAULT: None

Parameter field name for discriminating the type in a tagged union.

TYPE: Union[str, None] DEFAULT: None

If True, strict validation is applied to the field.

TYPE: Union[bool, None] DEFAULT: _Unset

Value must be a multiple of this. Only applicable to numbers.

TYPE: Union[float, None] DEFAULT: _Unset

Allow inf, -inf, nan. Only applicable to numbers.

TYPE: Union[bool, None] DEFAULT: _Unset

Maximum number of allow digits for strings.

TYPE: Union[int, None] DEFAULT: _Unset

Maximum number of decimal places allowed for numbers.

TYPE: Union[int, None] DEFAULT: _Unset

Example values for this field.

TYPE: Optional[list[Any]] DEFAULT: None

Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, although still supported. Use examples instead.

TYPE: Optional[Any] DEFAULT: _Unset

OpenAPI-specific examples.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Swagger UI (that provides the /docs interface) has better support for the OpenAPI-specific examples than the JSON Schema examples, that's the main use case for this.

Read more about it in the FastAPI docs for Declare Request Example Data.

TYPE: Optional[dict[str, Example]] DEFAULT: None

Mark this parameter field as deprecated.

It will affect the generated OpenAPI (e.g. visible at /docs).

TYPE: Union[deprecated, str, bool, None] DEFAULT: None

To include (or not) this parameter field in the generated OpenAPI. You probably don't need it, but it's available.

This affects the generated OpenAPI (e.g. visible at /docs).

TYPE: bool DEFAULT: True

Any additional JSON schema data.

TYPE: Union[dict[str, Any], None] DEFAULT: None

The extra kwargs is deprecated. Use json_schema_extra instead. Include extra fields used by the JSON Schema.

TYPE: Any DEFAULT: {}

Declare a path parameter for a path operation.

Read more about it in the FastAPI docs for Path Parameters and Numeric Validations.

Default value if the parameter field is not set.

This doesn't affect Path parameters as the value is always required. The parameter is available only for compatibility.

TYPE: Any DEFAULT: ...

A callable to generate the default value.

This doesn't affect Path parameters as the value is always required. The parameter is available only for compatibility.

TYPE: Union[Callable[[], Any], None] DEFAULT: _Unset

An alternative name for the parameter field.

This will be used to extract the data and for the generated OpenAPI. It is particularly useful when you can't use the name you want because it is a Python reserved keyword or similar.

TYPE: Optional[str] DEFAULT: None

Priority of the alias. This affects whether an alias generator is used.

TYPE: Union[int, None] DEFAULT: _Unset

'Whitelist' validation step. The parameter field will be the single one allowed by the alias or set of aliases defined.

TYPE: Union[str, AliasPath, AliasChoices, None] DEFAULT: None

'Blacklist' validation step. The vanilla parameter field will be the single one of the alias' or set of aliases' fields and all the other fields will be ignored at serialization time.

TYPE: Union[str, None] DEFAULT: None

Human-readable title.

TYPE: Optional[str] DEFAULT: None

Human-readable description.

TYPE: Optional[str] DEFAULT: None

Greater than. If set, value must be greater than this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Greater than or equal. If set, value must be greater than or equal to this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Less than. If set, value must be less than this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Less than or equal. If set, value must be less than or equal to this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Minimum length for strings.

TYPE: Optional[int] DEFAULT: None

Maximum length for strings.

TYPE: Optional[int] DEFAULT: None

RegEx pattern for strings.

TYPE: Optional[str] DEFAULT: None

Deprecated in FastAPI 0.100.0 and Pydantic v2, use pattern instead. RegEx pattern for strings.

TYPE: Optional[str] DEFAULT: None

Parameter field name for discriminating the type in a tagged union.

TYPE: Union[str, None] DEFAULT: None

If True, strict validation is applied to the field.

TYPE: Union[bool, None] DEFAULT: _Unset

Value must be a multiple of this. Only applicable to numbers.

TYPE: Union[float, None] DEFAULT: _Unset

Allow inf, -inf, nan. Only applicable to numbers.

TYPE: Union[bool, None] DEFAULT: _Unset

Maximum number of allow digits for strings.

TYPE: Union[int, None] DEFAULT: _Unset

Maximum number of decimal places allowed for numbers.

TYPE: Union[int, None] DEFAULT: _Unset

Example values for this field.

TYPE: Optional[list[Any]] DEFAULT: None

Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, although still supported. Use examples instead.

TYPE: Optional[Any] DEFAULT: _Unset

OpenAPI-specific examples.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Swagger UI (that provides the /docs interface) has better support for the OpenAPI-specific examples than the JSON Schema examples, that's the main use case for this.

Read more about it in the FastAPI docs for Declare Request Example Data.

TYPE: Optional[dict[str, Example]] DEFAULT: None

Mark this parameter field as deprecated.

It will affect the generated OpenAPI (e.g. visible at /docs).

TYPE: Union[deprecated, str, bool, None] DEFAULT: None

To include (or not) this parameter field in the generated OpenAPI. You probably don't need it, but it's available.

This affects the generated OpenAPI (e.g. visible at /docs).

TYPE: bool DEFAULT: True

Any additional JSON schema data.

TYPE: Union[dict[str, Any], None] DEFAULT: None

The extra kwargs is deprecated. Use json_schema_extra instead. Include extra fields used by the JSON Schema.

TYPE: Any DEFAULT: {}

Default value if the parameter field is not set.

TYPE: Any DEFAULT: Undefined

A callable to generate the default value.

This doesn't affect Path parameters as the value is always required. The parameter is available only for compatibility.

TYPE: Union[Callable[[], Any], None] DEFAULT: _Unset

When embed is True, the parameter will be expected in a JSON body as a key instead of being the JSON body itself.

This happens automatically when more than one Body parameter is declared.

Read more about it in the FastAPI docs for Body - Multiple Parameters.

TYPE: Union[bool, None] DEFAULT: None

The media type of this parameter field. Changing it would affect the generated OpenAPI, but currently it doesn't affect the parsing of the data.

TYPE: str DEFAULT: 'application/json'

An alternative name for the parameter field.

This will be used to extract the data and for the generated OpenAPI. It is particularly useful when you can't use the name you want because it is a Python reserved keyword or similar.

TYPE: Optional[str] DEFAULT: None

Priority of the alias. This affects whether an alias generator is used.

TYPE: Union[int, None] DEFAULT: _Unset

'Whitelist' validation step. The parameter field will be the single one allowed by the alias or set of aliases defined.

TYPE: Union[str, AliasPath, AliasChoices, None] DEFAULT: None

'Blacklist' validation step. The vanilla parameter field will be the single one of the alias' or set of aliases' fields and all the other fields will be ignored at serialization time.

TYPE: Union[str, None] DEFAULT: None

Human-readable title.

TYPE: Optional[str] DEFAULT: None

Human-readable description.

TYPE: Optional[str] DEFAULT: None

Greater than. If set, value must be greater than this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Greater than or equal. If set, value must be greater than or equal to this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Less than. If set, value must be less than this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Less than or equal. If set, value must be less than or equal to this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Minimum length for strings.

TYPE: Optional[int] DEFAULT: None

Maximum length for strings.

TYPE: Optional[int] DEFAULT: None

RegEx pattern for strings.

TYPE: Optional[str] DEFAULT: None

Deprecated in FastAPI 0.100.0 and Pydantic v2, use pattern instead. RegEx pattern for strings.

TYPE: Optional[str] DEFAULT: None

Parameter field name for discriminating the type in a tagged union.

TYPE: Union[str, None] DEFAULT: None

If True, strict validation is applied to the field.

TYPE: Union[bool, None] DEFAULT: _Unset

Value must be a multiple of this. Only applicable to numbers.

TYPE: Union[float, None] DEFAULT: _Unset

Allow inf, -inf, nan. Only applicable to numbers.

TYPE: Union[bool, None] DEFAULT: _Unset

Maximum number of allow digits for strings.

TYPE: Union[int, None] DEFAULT: _Unset

Maximum number of decimal places allowed for numbers.

TYPE: Union[int, None] DEFAULT: _Unset

Example values for this field.

TYPE: Optional[list[Any]] DEFAULT: None

Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, although still supported. Use examples instead.

TYPE: Optional[Any] DEFAULT: _Unset

OpenAPI-specific examples.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Swagger UI (that provides the /docs interface) has better support for the OpenAPI-specific examples than the JSON Schema examples, that's the main use case for this.

Read more about it in the FastAPI docs for Declare Request Example Data.

TYPE: Optional[dict[str, Example]] DEFAULT: None

Mark this parameter field as deprecated.

It will affect the generated OpenAPI (e.g. visible at /docs).

TYPE: Union[deprecated, str, bool, None] DEFAULT: None

To include (or not) this parameter field in the generated OpenAPI. You probably don't need it, but it's available.

This affects the generated OpenAPI (e.g. visible at /docs).

TYPE: bool DEFAULT: True

Any additional JSON schema data.

TYPE: Union[dict[str, Any], None] DEFAULT: None

The extra kwargs is deprecated. Use json_schema_extra instead. Include extra fields used by the JSON Schema.

TYPE: Any DEFAULT: {}

Default value if the parameter field is not set.

TYPE: Any DEFAULT: Undefined

A callable to generate the default value.

This doesn't affect Path parameters as the value is always required. The parameter is available only for compatibility.

TYPE: Union[Callable[[], Any], None] DEFAULT: _Unset

An alternative name for the parameter field.

This will be used to extract the data and for the generated OpenAPI. It is particularly useful when you can't use the name you want because it is a Python reserved keyword or similar.

TYPE: Optional[str] DEFAULT: None

Priority of the alias. This affects whether an alias generator is used.

TYPE: Union[int, None] DEFAULT: _Unset

'Whitelist' validation step. The parameter field will be the single one allowed by the alias or set of aliases defined.

TYPE: Union[str, AliasPath, AliasChoices, None] DEFAULT: None

'Blacklist' validation step. The vanilla parameter field will be the single one of the alias' or set of aliases' fields and all the other fields will be ignored at serialization time.

TYPE: Union[str, None] DEFAULT: None

Human-readable title.

TYPE: Optional[str] DEFAULT: None

Human-readable description.

TYPE: Optional[str] DEFAULT: None

Greater than. If set, value must be greater than this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Greater than or equal. If set, value must be greater than or equal to this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Less than. If set, value must be less than this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Less than or equal. If set, value must be less than or equal to this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Minimum length for strings.

TYPE: Optional[int] DEFAULT: None

Maximum length for strings.

TYPE: Optional[int] DEFAULT: None

RegEx pattern for strings.

TYPE: Optional[str] DEFAULT: None

Deprecated in FastAPI 0.100.0 and Pydantic v2, use pattern instead. RegEx pattern for strings.

TYPE: Optional[str] DEFAULT: None

Parameter field name for discriminating the type in a tagged union.

TYPE: Union[str, None] DEFAULT: None

If True, strict validation is applied to the field.

TYPE: Union[bool, None] DEFAULT: _Unset

Value must be a multiple of this. Only applicable to numbers.

TYPE: Union[float, None] DEFAULT: _Unset

Allow inf, -inf, nan. Only applicable to numbers.

TYPE: Union[bool, None] DEFAULT: _Unset

Maximum number of allow digits for strings.

TYPE: Union[int, None] DEFAULT: _Unset

Maximum number of decimal places allowed for numbers.

TYPE: Union[int, None] DEFAULT: _Unset

Example values for this field.

TYPE: Optional[list[Any]] DEFAULT: None

Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, although still supported. Use examples instead.

TYPE: Optional[Any] DEFAULT: _Unset

OpenAPI-specific examples.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Swagger UI (that provides the /docs interface) has better support for the OpenAPI-specific examples than the JSON Schema examples, that's the main use case for this.

Read more about it in the FastAPI docs for Declare Request Example Data.

TYPE: Optional[dict[str, Example]] DEFAULT: None

Mark this parameter field as deprecated.

It will affect the generated OpenAPI (e.g. visible at /docs).

TYPE: Union[deprecated, str, bool, None] DEFAULT: None

To include (or not) this parameter field in the generated OpenAPI. You probably don't need it, but it's available.

This affects the generated OpenAPI (e.g. visible at /docs).

TYPE: bool DEFAULT: True

Any additional JSON schema data.

TYPE: Union[dict[str, Any], None] DEFAULT: None

The extra kwargs is deprecated. Use json_schema_extra instead. Include extra fields used by the JSON Schema.

TYPE: Any DEFAULT: {}

Default value if the parameter field is not set.

TYPE: Any DEFAULT: Undefined

A callable to generate the default value.

This doesn't affect Path parameters as the value is always required. The parameter is available only for compatibility.

TYPE: Union[Callable[[], Any], None] DEFAULT: _Unset

An alternative name for the parameter field.

This will be used to extract the data and for the generated OpenAPI. It is particularly useful when you can't use the name you want because it is a Python reserved keyword or similar.

TYPE: Optional[str] DEFAULT: None

Priority of the alias. This affects whether an alias generator is used.

TYPE: Union[int, None] DEFAULT: _Unset

'Whitelist' validation step. The parameter field will be the single one allowed by the alias or set of aliases defined.

TYPE: Union[str, AliasPath, AliasChoices, None] DEFAULT: None

'Blacklist' validation step. The vanilla parameter field will be the single one of the alias' or set of aliases' fields and all the other fields will be ignored at serialization time.

TYPE: Union[str, None] DEFAULT: None

Automatically convert underscores to hyphens in the parameter field name.

Read more about it in the FastAPI docs for Header Parameters

TYPE: bool DEFAULT: True

Human-readable title.

TYPE: Optional[str] DEFAULT: None

Human-readable description.

TYPE: Optional[str] DEFAULT: None

Greater than. If set, value must be greater than this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Greater than or equal. If set, value must be greater than or equal to this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Less than. If set, value must be less than this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Less than or equal. If set, value must be less than or equal to this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Minimum length for strings.

TYPE: Optional[int] DEFAULT: None

Maximum length for strings.

TYPE: Optional[int] DEFAULT: None

RegEx pattern for strings.

TYPE: Optional[str] DEFAULT: None

Deprecated in FastAPI 0.100.0 and Pydantic v2, use pattern instead. RegEx pattern for strings.

TYPE: Optional[str] DEFAULT: None

Parameter field name for discriminating the type in a tagged union.

TYPE: Union[str, None] DEFAULT: None

If True, strict validation is applied to the field.

TYPE: Union[bool, None] DEFAULT: _Unset

Value must be a multiple of this. Only applicable to numbers.

TYPE: Union[float, None] DEFAULT: _Unset

Allow inf, -inf, nan. Only applicable to numbers.

TYPE: Union[bool, None] DEFAULT: _Unset

Maximum number of allow digits for strings.

TYPE: Union[int, None] DEFAULT: _Unset

Maximum number of decimal places allowed for numbers.

TYPE: Union[int, None] DEFAULT: _Unset

Example values for this field.

TYPE: Optional[list[Any]] DEFAULT: None

Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, although still supported. Use examples instead.

TYPE: Optional[Any] DEFAULT: _Unset

OpenAPI-specific examples.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Swagger UI (that provides the /docs interface) has better support for the OpenAPI-specific examples than the JSON Schema examples, that's the main use case for this.

Read more about it in the FastAPI docs for Declare Request Example Data.

TYPE: Optional[dict[str, Example]] DEFAULT: None

Mark this parameter field as deprecated.

It will affect the generated OpenAPI (e.g. visible at /docs).

TYPE: Union[deprecated, str, bool, None] DEFAULT: None

To include (or not) this parameter field in the generated OpenAPI. You probably don't need it, but it's available.

This affects the generated OpenAPI (e.g. visible at /docs).

TYPE: bool DEFAULT: True

Any additional JSON schema data.

TYPE: Union[dict[str, Any], None] DEFAULT: None

The extra kwargs is deprecated. Use json_schema_extra instead. Include extra fields used by the JSON Schema.

TYPE: Any DEFAULT: {}

Default value if the parameter field is not set.

TYPE: Any DEFAULT: Undefined

A callable to generate the default value.

This doesn't affect Path parameters as the value is always required. The parameter is available only for compatibility.

TYPE: Union[Callable[[], Any], None] DEFAULT: _Unset

The media type of this parameter field. Changing it would affect the generated OpenAPI, but currently it doesn't affect the parsing of the data.

TYPE: str DEFAULT: 'application/x-www-form-urlencoded'

An alternative name for the parameter field.

This will be used to extract the data and for the generated OpenAPI. It is particularly useful when you can't use the name you want because it is a Python reserved keyword or similar.

TYPE: Optional[str] DEFAULT: None

Priority of the alias. This affects whether an alias generator is used.

TYPE: Union[int, None] DEFAULT: _Unset

'Whitelist' validation step. The parameter field will be the single one allowed by the alias or set of aliases defined.

TYPE: Union[str, AliasPath, AliasChoices, None] DEFAULT: None

'Blacklist' validation step. The vanilla parameter field will be the single one of the alias' or set of aliases' fields and all the other fields will be ignored at serialization time.

TYPE: Union[str, None] DEFAULT: None

Human-readable title.

TYPE: Optional[str] DEFAULT: None

Human-readable description.

TYPE: Optional[str] DEFAULT: None

Greater than. If set, value must be greater than this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Greater than or equal. If set, value must be greater than or equal to this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Less than. If set, value must be less than this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Less than or equal. If set, value must be less than or equal to this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Minimum length for strings.

TYPE: Optional[int] DEFAULT: None

Maximum length for strings.

TYPE: Optional[int] DEFAULT: None

RegEx pattern for strings.

TYPE: Optional[str] DEFAULT: None

Deprecated in FastAPI 0.100.0 and Pydantic v2, use pattern instead. RegEx pattern for strings.

TYPE: Optional[str] DEFAULT: None

Parameter field name for discriminating the type in a tagged union.

TYPE: Union[str, None] DEFAULT: None

If True, strict validation is applied to the field.

TYPE: Union[bool, None] DEFAULT: _Unset

Value must be a multiple of this. Only applicable to numbers.

TYPE: Union[float, None] DEFAULT: _Unset

Allow inf, -inf, nan. Only applicable to numbers.

TYPE: Union[bool, None] DEFAULT: _Unset

Maximum number of allow digits for strings.

TYPE: Union[int, None] DEFAULT: _Unset

Maximum number of decimal places allowed for numbers.

TYPE: Union[int, None] DEFAULT: _Unset

Example values for this field.

TYPE: Optional[list[Any]] DEFAULT: None

Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, although still supported. Use examples instead.

TYPE: Optional[Any] DEFAULT: _Unset

OpenAPI-specific examples.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Swagger UI (that provides the /docs interface) has better support for the OpenAPI-specific examples than the JSON Schema examples, that's the main use case for this.

Read more about it in the FastAPI docs for Declare Request Example Data.

TYPE: Optional[dict[str, Example]] DEFAULT: None

Mark this parameter field as deprecated.

It will affect the generated OpenAPI (e.g. visible at /docs).

TYPE: Union[deprecated, str, bool, None] DEFAULT: None

To include (or not) this parameter field in the generated OpenAPI. You probably don't need it, but it's available.

This affects the generated OpenAPI (e.g. visible at /docs).

TYPE: bool DEFAULT: True

Any additional JSON schema data.

TYPE: Union[dict[str, Any], None] DEFAULT: None

The extra kwargs is deprecated. Use json_schema_extra instead. Include extra fields used by the JSON Schema.

TYPE: Any DEFAULT: {}

Default value if the parameter field is not set.

TYPE: Any DEFAULT: Undefined

A callable to generate the default value.

This doesn't affect Path parameters as the value is always required. The parameter is available only for compatibility.

TYPE: Union[Callable[[], Any], None] DEFAULT: _Unset

The media type of this parameter field. Changing it would affect the generated OpenAPI, but currently it doesn't affect the parsing of the data.

TYPE: str DEFAULT: 'multipart/form-data'

An alternative name for the parameter field.

This will be used to extract the data and for the generated OpenAPI. It is particularly useful when you can't use the name you want because it is a Python reserved keyword or similar.

TYPE: Optional[str] DEFAULT: None

Priority of the alias. This affects whether an alias generator is used.

TYPE: Union[int, None] DEFAULT: _Unset

'Whitelist' validation step. The parameter field will be the single one allowed by the alias or set of aliases defined.

TYPE: Union[str, AliasPath, AliasChoices, None] DEFAULT: None

'Blacklist' validation step. The vanilla parameter field will be the single one of the alias' or set of aliases' fields and all the other fields will be ignored at serialization time.

TYPE: Union[str, None] DEFAULT: None

Human-readable title.

TYPE: Optional[str] DEFAULT: None

Human-readable description.

TYPE: Optional[str] DEFAULT: None

Greater than. If set, value must be greater than this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Greater than or equal. If set, value must be greater than or equal to this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Less than. If set, value must be less than this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Less than or equal. If set, value must be less than or equal to this. Only applicable to numbers.

TYPE: Optional[float] DEFAULT: None

Minimum length for strings.

TYPE: Optional[int] DEFAULT: None

Maximum length for strings.

TYPE: Optional[int] DEFAULT: None

RegEx pattern for strings.

TYPE: Optional[str] DEFAULT: None

Deprecated in FastAPI 0.100.0 and Pydantic v2, use pattern instead. RegEx pattern for strings.

TYPE: Optional[str] DEFAULT: None

Parameter field name for discriminating the type in a tagged union.

TYPE: Union[str, None] DEFAULT: None

If True, strict validation is applied to the field.

TYPE: Union[bool, None] DEFAULT: _Unset

Value must be a multiple of this. Only applicable to numbers.

TYPE: Union[float, None] DEFAULT: _Unset

Allow inf, -inf, nan. Only applicable to numbers.

TYPE: Union[bool, None] DEFAULT: _Unset

Maximum number of allow digits for strings.

TYPE: Union[int, None] DEFAULT: _Unset

Maximum number of decimal places allowed for numbers.

TYPE: Union[int, None] DEFAULT: _Unset

Example values for this field.

TYPE: Optional[list[Any]] DEFAULT: None

Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, although still supported. Use examples instead.

TYPE: Optional[Any] DEFAULT: _Unset

OpenAPI-specific examples.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Swagger UI (that provides the /docs interface) has better support for the OpenAPI-specific examples than the JSON Schema examples, that's the main use case for this.

Read more about it in the FastAPI docs for Declare Request Example Data.

TYPE: Optional[dict[str, Example]] DEFAULT: None

Mark this parameter field as deprecated.

It will affect the generated OpenAPI (e.g. visible at /docs).

TYPE: Union[deprecated, str, bool, None] DEFAULT: None

To include (or not) this parameter field in the generated OpenAPI. You probably don't need it, but it's available.

This affects the generated OpenAPI (e.g. visible at /docs).

TYPE: bool DEFAULT: True

Any additional JSON schema data.

TYPE: Union[dict[str, Any], None] DEFAULT: None

The extra kwargs is deprecated. Use json_schema_extra instead. Include extra fields used by the JSON Schema.

TYPE: Any DEFAULT: {}

**Examples:**

Example 1 (python):
```python
from fastapi import Body, Cookie, File, Form, Header, Path, Query
```

Example 2 (rust):
```rust
Query(
    default=Undefined,
    *,
    default_factory=_Unset,
    alias=None,
    alias_priority=_Unset,
    validation_alias=None,
    serialization_alias=None,
    title=None,
    description=None,
    gt=None,
    ge=None,
    lt=None,
    le=None,
    min_length=None,
    max_length=None,
    pattern=None,
    regex=None,
    discriminator=None,
    strict=_Unset,
    multiple_of=_Unset,
    allow_inf_nan=_Unset,
    max_digits=_Unset,
    decimal_places=_Unset,
    examples=None,
    example=_Unset,
    openapi_examples=None,
    deprecated=None,
    include_in_schema=True,
    json_schema_extra=None,
    **extra
)
```

Example 3 (python):
```python
def Query(  # noqa: N802
    default: Annotated[
        Any,
        Doc(
            """
            Default value if the parameter field is not set.
            """
        ),
    ] = Undefined,
    *,
    default_factory: Annotated[
        Union[Callable[[], Any], None],
        Doc(
            """
            A callable to generate the default value.

            This doesn't affect `Path` parameters as the value is always required.
            The parameter is available only for compatibility.
            """
        ),
    ] = _Unset,
    alias: Annotated[
        Optional[str],
        Doc(
            """
            An alternative name for the parameter field.

            This will be used to extract the data and for the generated OpenAPI.
            It is particularly useful when you can't use the name you want because it
            is a Python reserved keyword or similar.
            """
        ),
    ] = None,
    alias_priority: Annotated[
        Union[int, None],
        Doc(
            """
            Priority of the alias. This affects whether an alias generator is used.
            """
        ),
    ] = _Unset,
    validation_alias: Annotated[
        Union[str, AliasPath, AliasChoices, None],
        Doc(
            """
            'Whitelist' validation step. The parameter field will be the single one
            allowed by the alias or set of aliases defined.
            """
        ),
    ] = None,
    serialization_alias: Annotated[
        Union[str, None],
        Doc(
            """
            'Blacklist' validation step. The vanilla parameter field will be the
            single one of the alias' or set of aliases' fields and all the other
            fields will be ignored at serialization time.
            """
        ),
    ] = None,
    title: Annotated[
        Optional[str],
        Doc(
            """
            Human-readable title.
            """
        ),
    ] = None,
    description: Annotated[
        Optional[str],
        Doc(
            """
            Human-readable description.
            """
        ),
    ] = None,
    gt: Annotated[
        Optional[float],
        Doc(
            """
            Greater than. If set, value must be greater than this. Only applicable to
            numbers.
            """
        ),
    ] = None,
    ge: Annotated[
        Optional[float],
        Doc(
            """
            Greater than or equal. If set, value must be greater than or equal to
            this. Only applicable to numbers.
            """
        ),
    ] = None,
    lt: Annotated[
        Optional[float],
        Doc(
            """
            Less than. If set, value must be less than this. Only applicable to numbers.
            """
        ),
    ] = None,
    le: Annotated[
        Optional[float],
        Doc(
            """
            Less than or equal. If set, value must be less than or equal to this.
            Only applicable to numbers.
            """
        ),
    ] = None,
    min_length: Annotated[
        Optional[int],
        Doc(
            """
            Minimum length for strings.
            """
        ),
    ] = None,
    max_length: Annotated[
        Optional[int],
        Doc(
            """
            Maximum length for strings.
            """
        ),
    ] = None,
    pattern: Annotated[
        Optional[str],
        Doc(
            """
            RegEx pattern for strings.
            """
        ),
    ] = None,
    regex: Annotated[
        Optional[str],
        Doc(
            """
            RegEx pattern for strings.
            """
        ),
        deprecated(
            "Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."
        ),
    ] = None,
    discriminator: Annotated[
        Union[str, None],
        Doc(
            """
            Parameter field name for discriminating the type in a tagged union.
            """
        ),
    ] = None,
    strict: Annotated[
        Union[bool, None],
        Doc(
            """
            If `True`, strict validation is applied to the field.
            """
        ),
    ] = _Unset,
    multiple_of: Annotated[
        Union[float, None],
        Doc(
            """
            Value must be a multiple of this. Only applicable to numbers.
            """
        ),
    ] = _Unset,
    allow_inf_nan: Annotated[
        Union[bool, None],
        Doc(
            """
            Allow `inf`, `-inf`, `nan`. Only applicable to numbers.
            """
        ),
    ] = _Unset,
    max_digits: Annotated[
        Union[int, None],
        Doc(
            """
            Maximum number of allow digits for strings.
            """
        ),
    ] = _Unset,
    decimal_places: Annotated[
        Union[int, None],
        Doc(
            """
            Maximum number of decimal places allowed for numbers.
            """
        ),
    ] = _Unset,
    examples: Annotated[
        Optional[list[Any]],
        Doc(
            """
            Example values for this field.
            """
        ),
    ] = None,
    example: Annotated[
        Optional[Any],
        deprecated(
            "Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, "
            "although still supported. Use examples instead."
        ),
    ] = _Unset,
    openapi_examples: Annotated[
        Optional[dict[str, Example]],
        Doc(
            """
            OpenAPI-specific examples.

            It will be added to the generated OpenAPI (e.g. visible at `/docs`).

            Swagger UI (that provides the `/docs` interface) has better support for the
            OpenAPI-specific examples than the JSON Schema `examples`, that's the main
            use case for this.

            Read more about it in the
            [FastAPI docs for Declare Request Example Data](https://fastapi.tiangolo.com/tutorial/schema-extra-example/#using-the-openapi_examples-parameter).
            """
        ),
    ] = None,
    deprecated: Annotated[
        Union[deprecated, str, bool, None],
        Doc(
            """
            Mark this parameter field as deprecated.

            It will affect the generated OpenAPI (e.g. visible at `/docs`).
            """
        ),
    ] = None,
    include_in_schema: Annotated[
        bool,
        Doc(
            """
            To include (or not) this parameter field in the generated OpenAPI.
            You probably don't need it, but it's available.

            This affects the generated OpenAPI (e.g. visible at `/docs`).
            """
        ),
    ] = True,
    json_schema_extra: Annotated[
        Union[dict[str, Any], None],
        Doc(
            """
            Any additional JSON schema data.
            """
        ),
    ] = None,
    **extra: Annotated[
        Any,
        Doc(
            """
            Include extra fields used by the JSON Schema.
            """
        ),
        deprecated(
            """
            The `extra` kwargs is deprecated. Use `json_schema_extra` instead.
            """
        ),
    ],
) -> Any:
    return params.Query(
        default=default,
        default_factory=default_factory,
        alias=alias,
        alias_priority=alias_priority,
        validation_alias=validation_alias,
        serialization_alias=serialization_alias,
        title=title,
        description=description,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        min_length=min_length,
        max_length=max_length,
        pattern=pattern,
        regex=regex,
        discriminator=discriminator,
        strict=strict,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        example=example,
        examples=examples,
        openapi_examples=openapi_examples,
        deprecated=deprecated,
        include_in_schema=include_in_schema,
        json_schema_extra=json_schema_extra,
        **extra,
    )
```

Example 4 (rust):
```rust
Path(
    default=...,
    *,
    default_factory=_Unset,
    alias=None,
    alias_priority=_Unset,
    validation_alias=None,
    serialization_alias=None,
    title=None,
    description=None,
    gt=None,
    ge=None,
    lt=None,
    le=None,
    min_length=None,
    max_length=None,
    pattern=None,
    regex=None,
    discriminator=None,
    strict=_Unset,
    multiple_of=_Unset,
    allow_inf_nan=_Unset,
    max_digits=_Unset,
    decimal_places=_Unset,
    examples=None,
    example=_Unset,
    openapi_examples=None,
    deprecated=None,
    include_in_schema=True,
    json_schema_extra=None,
    **extra
)
```

---

## Request Files¶

**URL:** https://fastapi.tiangolo.com/tutorial/request-files/

**Contents:**
- Request Files¶
- Import File¶
- Define File Parameters¶
- File Parameters with UploadFile¶
  - UploadFile¶
- What is "Form Data"¶
- Optional File Upload¶
- UploadFile with Additional Metadata¶
- Multiple File Uploads¶
  - Multiple File Uploads with Additional Metadata¶

You can define files to be uploaded by the client using File.

To receive uploaded files, first install python-multipart.

Make sure you create a virtual environment, activate it, and then install it, for example:

This is because uploaded files are sent as "form data".

Import File and UploadFile from fastapi:

Prefer to use the Annotated version if possible.

Create file parameters the same way you would for Body or Form:

Prefer to use the Annotated version if possible.

File is a class that inherits directly from Form.

But remember that when you import Query, Path, File and others from fastapi, those are actually functions that return special classes.

To declare File bodies, you need to use File, because otherwise the parameters would be interpreted as query parameters or body (JSON) parameters.

The files will be uploaded as "form data".

If you declare the type of your path operation function parameter as bytes, FastAPI will read the file for you and you will receive the contents as bytes.

Keep in mind that this means that the whole contents will be stored in memory. This will work well for small files.

But there are several cases in which you might benefit from using UploadFile.

Define a file parameter with a type of UploadFile:

Prefer to use the Annotated version if possible.

Using UploadFile has several advantages over bytes:

UploadFile has the following attributes:

UploadFile has the following async methods. They all call the corresponding file methods underneath (using the internal SpooledTemporaryFile).

As all these methods are async methods, you need to "await" them.

For example, inside of an async path operation function you can get the contents with:

If you are inside of a normal def path operation function, you can access the UploadFile.file directly, for example:

async Technical Details

When you use the async methods, FastAPI runs the file methods in a threadpool and awaits for them.

Starlette Technical Details

FastAPI's UploadFile inherits directly from Starlette's UploadFile, but adds some necessary parts to make it compatible with Pydantic and the other parts of FastAPI.

The way HTML forms (<form></form>) sends the data to the server normally uses a "special" encoding for that data, it's different from JSON.

FastAPI will make sure to read that data from the right place instead of JSON.

Data from forms is normally encoded using the "media type" application/x-www-form-urlencoded when it doesn't include files.

But when the form includes files, it is encoded as multipart/form-data. If you use File, FastAPI will know it has to get the files from the correct part of the body.

If you want to read more about these encodings and form fields, head to the MDN web docs for POST.

You can declare multiple File and Form parameters in a path operation, but you can't also declare Body fields that you expect to receive as JSON, as the request will have the body encoded using multipart/form-data instead of application/json.

This is not a limitation of FastAPI, it's part of the HTTP protocol.

You can make a file optional by using standard type annotations and setting a default value of None:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

You can also use File() with UploadFile, for example, to set additional metadata:

Prefer to use the Annotated version if possible.

It's possible to upload several files at the same time.

They would be associated to the same "form field" sent using "form data".

To use that, declare a list of bytes or UploadFile:

Prefer to use the Annotated version if possible.

You will receive, as declared, a list of bytes or UploadFiles.

You could also use from starlette.responses import HTMLResponse.

FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette.

And the same way as before, you can use File() to set additional parameters, even for UploadFile:

Prefer to use the Annotated version if possible.

Use File, bytes, and UploadFile to declare files to be uploaded in the request, sent as form data.

**Examples:**

Example 1 (unknown):
```unknown
$ pip install python-multipart
```

Example 2 (python):
```python
from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
```

Example 3 (python):
```python
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
```

Example 4 (python):
```python
from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
```

---

## Request class¶

**URL:** https://fastapi.tiangolo.com/reference/request/

**Contents:**
- Request class¶
- fastapi.Request ¶
  - scope instance-attribute ¶
  - app property ¶
  - url property ¶
  - base_url property ¶
  - headers property ¶
  - query_params property ¶
  - path_params property ¶
  - cookies property ¶

You can declare a parameter in a path operation function or dependency to be of type Request and then you can access the raw request object directly, without any validation, etc.

You can import it directly from fastapi:

When you want to define dependencies that should be compatible with both HTTP and WebSockets, you can define a parameter that takes an HTTPConnection instead of a Request or a WebSocket.

Bases: HTTPConnection

**Examples:**

Example 1 (python):
```python
from fastapi import Request
```

Example 2 (unknown):
```unknown
Request(scope, receive=empty_receive, send=empty_send)
```

Example 3 (python):
```python
def __init__(self, scope: Scope, receive: Receive = empty_receive, send: Send = empty_send):
    super().__init__(scope)
    assert scope["type"] == "http"
    self._receive = receive
    self._send = send
    self._stream_consumed = False
    self._is_disconnected = False
    self._form = None
```

Example 4 (unknown):
```unknown
scope = scope
```

---

## Body - Nested Models¶

**URL:** https://fastapi.tiangolo.com/tutorial/body-nested-models/

**Contents:**
- Body - Nested Models¶
- List fields¶
- List fields with type parameter¶
  - Declare a list with a type parameter¶
- Set types¶
- Nested Models¶
  - Define a submodel¶
  - Use the submodel as a type¶
- Special types and validation¶
- Attributes with lists of submodels¶

With FastAPI, you can define, validate, document, and use arbitrarily deeply nested models (thanks to Pydantic).

You can define an attribute to be a subtype. For example, a Python list:

This will make tags be a list, although it doesn't declare the type of the elements of the list.

But Python has a specific way to declare lists with internal types, or "type parameters":

To declare types that have type parameters (internal types), like list, dict, tuple, pass the internal type(s) as "type parameters" using square brackets: [ and ]

That's all standard Python syntax for type declarations.

Use that same standard syntax for model attributes with internal types.

So, in our example, we can make tags be specifically a "list of strings":

But then we think about it, and realize that tags shouldn't repeat, they would probably be unique strings.

And Python has a special data type for sets of unique items, the set.

Then we can declare tags as a set of strings:

With this, even if you receive a request with duplicate data, it will be converted to a set of unique items.

And whenever you output that data, even if the source had duplicates, it will be output as a set of unique items.

And it will be annotated / documented accordingly too.

Each attribute of a Pydantic model has a type.

But that type can itself be another Pydantic model.

So, you can declare deeply nested JSON "objects" with specific attribute names, types and validations.

All that, arbitrarily nested.

For example, we can define an Image model:

And then we can use it as the type of an attribute:

This would mean that FastAPI would expect a body similar to:

Again, doing just that declaration, with FastAPI you get:

Apart from normal singular types like str, int, float, etc. you can use more complex singular types that inherit from str.

To see all the options you have, checkout Pydantic's Type Overview. You will see some examples in the next chapter.

For example, as in the Image model we have a url field, we can declare it to be an instance of Pydantic's HttpUrl instead of a str:

The string will be checked to be a valid URL, and documented in JSON Schema / OpenAPI as such.

You can also use Pydantic models as subtypes of list, set, etc.:

This will expect (convert, validate, document, etc.) a JSON body like:

Notice how the images key now has a list of image objects.

You can define arbitrarily deeply nested models:

Notice how Offer has a list of Items, which in turn have an optional list of Images

If the top level value of the JSON body you expect is a JSON array (a Python list), you can declare the type in the parameter of the function, the same as in Pydantic models:

And you get editor support everywhere.

Even for items inside of lists:

You couldn't get this kind of editor support if you were working directly with dict instead of Pydantic models.

But you don't have to worry about them either, incoming dicts are converted automatically and your output is converted automatically to JSON too.

You can also declare a body as a dict with keys of some type and values of some other type.

This way, you don't have to know beforehand what the valid field/attribute names are (as would be the case with Pydantic models).

This would be useful if you want to receive keys that you don't already know.

Another useful case is when you want to have keys of another type (e.g., int).

That's what we are going to see here.

In this case, you would accept any dict as long as it has int keys with float values:

Keep in mind that JSON only supports str as keys.

But Pydantic has automatic data conversion.

This means that, even though your API clients can only send strings as keys, as long as those strings contain pure integers, Pydantic will convert them and validate them.

And the dict you receive as weights will actually have int keys and float values.

With FastAPI you have the maximum flexibility provided by Pydantic models, while keeping your code simple, short and elegant.

But with all the benefits:

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list = []


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

Example 2 (python):
```python
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: list = []


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

Example 3 (yaml):
```yaml
my_list: list[str]
```

Example 4 (python):
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

---

## Form Models¶

**URL:** https://fastapi.tiangolo.com/tutorial/request-form-models/

**Contents:**
- Form Models¶
- Pydantic Models for Forms¶
- Check the Docs¶
- Forbid Extra Form Fields¶
- Summary¶

You can use Pydantic models to declare form fields in FastAPI.

To use forms, first install python-multipart.

Make sure you create a virtual environment, activate it, and then install it, for example:

This is supported since FastAPI version 0.113.0. 🤓

You just need to declare a Pydantic model with the fields you want to receive as form fields, and then declare the parameter as Form:

Prefer to use the Annotated version if possible.

FastAPI will extract the data for each field from the form data in the request and give you the Pydantic model you defined.

You can verify it in the docs UI at /docs:

In some special use cases (probably not very common), you might want to restrict the form fields to only those declared in the Pydantic model. And forbid any extra fields.

This is supported since FastAPI version 0.114.0. 🤓

You can use Pydantic's model configuration to forbid any extra fields:

Prefer to use the Annotated version if possible.

If a client tries to send some extra data, they will receive an error response.

For example, if the client tries to send the form fields:

They will receive an error response telling them that the field extra is not allowed:

You can use Pydantic models to declare form fields in FastAPI. 😎

**Examples:**

Example 1 (unknown):
```unknown
$ pip install python-multipart
```

Example 2 (python):
```python
from typing import Annotated

from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


class FormData(BaseModel):
    username: str
    password: str


@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data
```

Example 3 (python):
```python
from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


class FormData(BaseModel):
    username: str
    password: str


@app.post("/login/")
async def login(data: FormData = Form()):
    return data
```

Example 4 (python):
```python
from typing import Annotated

from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


class FormData(BaseModel):
    username: str
    password: str
    model_config = {"extra": "forbid"}


@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data
```

---

## Declare Request Example Data¶

**URL:** https://fastapi.tiangolo.com/tutorial/schema-extra-example/

**Contents:**
- Declare Request Example Data¶
- Extra JSON Schema data in Pydantic models¶
- Field additional arguments¶
- examples in JSON Schema - OpenAPI¶
  - Body with examples¶
  - Example in the docs UI¶
  - Body with multiple examples¶
  - OpenAPI-specific examples¶
  - Using the openapi_examples Parameter¶
  - OpenAPI Examples in the Docs UI¶

You can declare examples of the data your app can receive.

Here are several ways to do it.

You can declare examples for a Pydantic model that will be added to the generated JSON Schema.

That extra info will be added as-is to the output JSON Schema for that model, and it will be used in the API docs.

You can use the attribute model_config that takes a dict as described in Pydantic's docs: Configuration.

You can set "json_schema_extra" with a dict containing any additional data you would like to show up in the generated JSON Schema, including examples.

You could use the same technique to extend the JSON Schema and add your own custom extra info.

For example you could use it to add metadata for a frontend user interface, etc.

OpenAPI 3.1.0 (used since FastAPI 0.99.0) added support for examples, which is part of the JSON Schema standard.

Before that, it only supported the keyword example with a single example. That is still supported by OpenAPI 3.1.0, but is deprecated and is not part of the JSON Schema standard. So you are encouraged to migrate example to examples. 🤓

You can read more at the end of this page.

When using Field() with Pydantic models, you can also declare additional examples:

you can also declare a group of examples with additional information that will be added to their JSON Schemas inside of OpenAPI.

Here we pass examples containing one example of the data expected in Body():

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

With any of the methods above it would look like this in the /docs:

You can of course also pass multiple examples:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

When you do this, the examples will be part of the internal JSON Schema for that body data.

Nevertheless, at the time of writing this, Swagger UI, the tool in charge of showing the docs UI, doesn't support showing multiple examples for the data in JSON Schema. But read below for a workaround.

Since before JSON Schema supported examples OpenAPI had support for a different field also called examples.

This OpenAPI-specific examples goes in another section in the OpenAPI specification. It goes in the details for each path operation, not inside each JSON Schema.

And Swagger UI has supported this particular examples field for a while. So, you can use it to show different examples in the docs UI.

The shape of this OpenAPI-specific field examples is a dict with multiple examples (instead of a list), each with extra information that will be added to OpenAPI too.

This doesn't go inside of each JSON Schema contained in OpenAPI, this goes outside, in the path operation directly.

You can declare the OpenAPI-specific examples in FastAPI with the parameter openapi_examples for:

The keys of the dict identify each example, and each value is another dict.

Each specific example dict in the examples can contain:

You can use it like this:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

With openapi_examples added to Body() the /docs would look like:

If you are already using FastAPI version 0.99.0 or above, you can probably skip these details.

They are more relevant for older versions, before OpenAPI 3.1.0 was available.

You can consider this a brief OpenAPI and JSON Schema history lesson. 🤓

These are very technical details about the standards JSON Schema and OpenAPI.

If the ideas above already work for you, that might be enough, and you probably don't need these details, feel free to skip them.

Before OpenAPI 3.1.0, OpenAPI used an older and modified version of JSON Schema.

JSON Schema didn't have examples, so OpenAPI added its own example field to its own modified version.

OpenAPI also added example and examples fields to other parts of the specification:

This old OpenAPI-specific examples parameter is now openapi_examples since FastAPI 0.103.0.

But then JSON Schema added an examples field to a new version of the specification.

And then the new OpenAPI 3.1.0 was based on the latest version (JSON Schema 2020-12) that included this new field examples.

And now this new examples field takes precedence over the old single (and custom) example field, that is now deprecated.

This new examples field in JSON Schema is just a list of examples, not a dict with extra metadata as in the other places in OpenAPI (described above).

Even after OpenAPI 3.1.0 was released with this new simpler integration with JSON Schema, for a while, Swagger UI, the tool that provides the automatic docs, didn't support OpenAPI 3.1.0 (it does since version 5.0.0 🎉).

Because of that, versions of FastAPI previous to 0.99.0 still used versions of OpenAPI lower than 3.1.0.

When you add examples inside a Pydantic model, using schema_extra or Field(examples=["something"]) that example is added to the JSON Schema for that Pydantic model.

And that JSON Schema of the Pydantic model is included in the OpenAPI of your API, and then it's used in the docs UI.

In versions of FastAPI before 0.99.0 (0.99.0 and above use the newer OpenAPI 3.1.0) when you used example or examples with any of the other utilities (Query(), Body(), etc.) those examples were not added to the JSON Schema that describes that data (not even to OpenAPI's own version of JSON Schema), they were added directly to the path operation declaration in OpenAPI (outside the parts of OpenAPI that use JSON Schema).

But now that FastAPI 0.99.0 and above uses OpenAPI 3.1.0, that uses JSON Schema 2020-12, and Swagger UI 5.0.0 and above, everything is more consistent and the examples are included in JSON Schema.

Now, as Swagger UI didn't support multiple JSON Schema examples (as of 2023-08-26), users didn't have a way to show multiple examples in the docs.

To solve that, FastAPI 0.103.0 added support for declaring the same old OpenAPI-specific examples field with the new parameter openapi_examples. 🤓

I used to say I didn't like history that much... and look at me now giving "tech history" lessons. 😅

In short, upgrade to FastAPI 0.99.0 or above, and things are much simpler, consistent, and intuitive, and you don't have to know all these historic details. 😎

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

Example 2 (python):
```python
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

Example 3 (python):
```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.2])


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

Example 4 (python):
```python
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: Union[str, None] = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: Union[float, None] = Field(default=None, examples=[3.2])


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

---

## Body - Multiple Parameters¶

**URL:** https://fastapi.tiangolo.com/tutorial/body-multiple-params/

**Contents:**
- Body - Multiple Parameters¶
- Mix Path, Query and body parameters¶
- Multiple body parameters¶
- Singular values in body¶
- Multiple body params and query¶
- Embed a single body parameter¶
- Recap¶

Now that we have seen how to use Path and Query, let's see more advanced uses of request body declarations.

First, of course, you can mix Path, Query and request body parameter declarations freely and FastAPI will know what to do.

And you can also declare body parameters as optional, by setting the default to None:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Notice that, in this case, the item that would be taken from the body is optional. As it has a None default value.

In the previous example, the path operations would expect a JSON body with the attributes of an Item, like:

But you can also declare multiple body parameters, e.g. item and user:

In this case, FastAPI will notice that there is more than one body parameter in the function (there are two parameters that are Pydantic models).

So, it will then use the parameter names as keys (field names) in the body, and expect a body like:

Notice that even though the item was declared the same way as before, it is now expected to be inside of the body with a key item.

FastAPI will do the automatic conversion from the request, so that the parameter item receives its specific content and the same for user.

It will perform the validation of the compound data, and will document it like that for the OpenAPI schema and automatic docs.

The same way there is a Query and Path to define extra data for query and path parameters, FastAPI provides an equivalent Body.

For example, extending the previous model, you could decide that you want to have another key importance in the same body, besides the item and user.

If you declare it as is, because it is a singular value, FastAPI will assume that it is a query parameter.

But you can instruct FastAPI to treat it as another body key using Body:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

In this case, FastAPI will expect a body like:

Again, it will convert the data types, validate, document, etc.

Of course, you can also declare additional query parameters whenever you need, additional to any body parameters.

As, by default, singular values are interpreted as query parameters, you don't have to explicitly add a Query, you can just do:

Or in Python 3.10 and above:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Body also has all the same extra validation and metadata parameters as Query, Path and others you will see later.

Let's say you only have a single item body parameter from a Pydantic model Item.

By default, FastAPI will then expect its body directly.

But if you want it to expect a JSON with a key item and inside of it the model contents, as it does when you declare extra body parameters, you can use the special Body parameter embed:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

In this case FastAPI will expect a body like:

You can add multiple body parameters to your path operation function, even though a request can only have a single body.

But FastAPI will handle it, give you the correct data in your function, and validate and document the correct schema in the path operation.

You can also declare singular values to be received as part of the body.

And you can instruct FastAPI to embed the body in a key even when there is only a single parameter declared.

**Examples:**

Example 1 (python):
```python
from typing import Annotated

from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results
```

Example 2 (python):
```python
from typing import Annotated, Union

from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: Union[str, None] = None,
    item: Union[Item, None] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results
```

Example 3 (python):
```python
from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results
```

Example 4 (python):
```python
from typing import Union

from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: Union[str, None] = None,
    item: Union[Item, None] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results
```

---

## OpenAPI Webhooks¶

**URL:** https://fastapi.tiangolo.com/advanced/openapi-webhooks/

**Contents:**
- OpenAPI Webhooks¶
- Webhooks steps¶
- Documenting webhooks with FastAPI and OpenAPI¶
- An app with webhooks¶
  - Check the docs¶

There are cases where you want to tell your API users that your app could call their app (sending a request) with some data, normally to notify of some type of event.

This means that instead of the normal process of your users sending requests to your API, it's your API (or your app) that could send requests to their system (to their API, their app).

This is normally called a webhook.

The process normally is that you define in your code what is the message that you will send, the body of the request.

You also define in some way at which moments your app will send those requests or events.

And your users define in some way (for example in a web dashboard somewhere) the URL where your app should send those requests.

All the logic about how to register the URLs for webhooks and the code to actually send those requests is up to you. You write it however you want to in your own code.

With FastAPI, using OpenAPI, you can define the names of these webhooks, the types of HTTP operations that your app can send (e.g. POST, PUT, etc.) and the request bodies that your app would send.

This can make it a lot easier for your users to implement their APIs to receive your webhook requests, they might even be able to autogenerate some of their own API code.

Webhooks are available in OpenAPI 3.1.0 and above, supported by FastAPI 0.99.0 and above.

When you create a FastAPI application, there is a webhooks attribute that you can use to define webhooks, the same way you would define path operations, for example with @app.webhooks.post().

The webhooks that you define will end up in the OpenAPI schema and the automatic docs UI.

The app.webhooks object is actually just an APIRouter, the same type you would use when structuring your app with multiple files.

Notice that with webhooks you are actually not declaring a path (like /items/), the text you pass there is just an identifier of the webhook (the name of the event), for example in @app.webhooks.post("new-subscription"), the webhook name is new-subscription.

This is because it is expected that your users would define the actual URL path where they want to receive the webhook request in some other way (e.g. a web dashboard).

Now you can start your app and go to http://127.0.0.1:8000/docs.

You will see your docs have the normal path operations and now also some webhooks:

**Examples:**

Example 1 (python):
```python
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Subscription(BaseModel):
    username: str
    monthly_fee: float
    start_date: datetime


@app.webhooks.post("new-subscription")
def new_subscription(body: Subscription):
    """
    When a new user subscribes to your service we'll send you a POST request with this
    data to the URL that you register for the event `new-subscription` in the dashboard.
    """


@app.get("/users/")
def read_users():
    return ["Rick", "Morty"]
```

---
