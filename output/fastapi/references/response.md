# Fastapi - Response

**Pages:** 7

---

## Response Status Code¶

**URL:** https://fastapi.tiangolo.com/tutorial/response-status-code/

**Contents:**
- Response Status Code¶
- About HTTP status codes¶
- Shortcut to remember the names¶
- Changing the default¶

The same way you can specify a response model, you can also declare the HTTP status code used for the response with the parameter status_code in any of the path operations:

Notice that status_code is a parameter of the "decorator" method (get, post, etc). Not of your path operation function, like all the parameters and body.

The status_code parameter receives a number with the HTTP status code.

status_code can alternatively also receive an IntEnum, such as Python's http.HTTPStatus.

Some response codes (see the next section) indicate that the response does not have a body.

FastAPI knows this, and will produce OpenAPI docs that state there is no response body.

If you already know what HTTP status codes are, skip to the next section.

In HTTP, you send a numeric status code of 3 digits as part of the response.

These status codes have a name associated to recognize them, but the important part is the number.

To know more about each status code and which code is for what, check the MDN documentation about HTTP status codes.

Let's see the previous example again:

201 is the status code for "Created".

But you don't have to memorize what each of these codes mean.

You can use the convenience variables from fastapi.status.

They are just a convenience, they hold the same number, but that way you can use the editor's autocomplete to find them:

You could also use from starlette import status.

FastAPI provides the same starlette.status as fastapi.status just as a convenience for you, the developer. But it comes directly from Starlette.

Later, in the Advanced User Guide, you will see how to return a different status code than the default you are declaring here.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI

app = FastAPI()


@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}
```

Example 2 (python):
```python
from fastapi import FastAPI

app = FastAPI()


@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}
```

Example 3 (python):
```python
from fastapi import FastAPI, status

app = FastAPI()


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
```

---

## Response Model - Return Type¶

**URL:** https://fastapi.tiangolo.com/tutorial/response-model/

**Contents:**
- Response Model - Return Type¶
- response_model Parameter¶
  - response_model Priority¶
- Return the same input data¶
- Add an output model¶
  - response_model or Return Type¶
- Return Type and Data Filtering¶
  - Type Annotations and Tooling¶
  - FastAPI Data Filtering¶
- See it in the docs¶

You can declare the type used for the response by annotating the path operation function return type.

You can use type annotations the same way you would for input data in function parameters, you can use Pydantic models, lists, dictionaries, scalar values like integers, booleans, etc.

FastAPI will use this return type to:

But most importantly:

There are some cases where you need or want to return some data that is not exactly what the type declares.

For example, you could want to return a dictionary or a database object, but declare it as a Pydantic model. This way the Pydantic model would do all the data documentation, validation, etc. for the object that you returned (e.g. a dictionary or database object).

If you added the return type annotation, tools and editors would complain with a (correct) error telling you that your function is returning a type (e.g. a dict) that is different from what you declared (e.g. a Pydantic model).

In those cases, you can use the path operation decorator parameter response_model instead of the return type.

You can use the response_model parameter in any of the path operations:

Notice that response_model is a parameter of the "decorator" method (get, post, etc). Not of your path operation function, like all the parameters and body.

response_model receives the same type you would declare for a Pydantic model field, so, it can be a Pydantic model, but it can also be, e.g. a list of Pydantic models, like List[Item].

FastAPI will use this response_model to do all the data documentation, validation, etc. and also to convert and filter the output data to its type declaration.

If you have strict type checks in your editor, mypy, etc, you can declare the function return type as Any.

That way you tell the editor that you are intentionally returning anything. But FastAPI will still do the data documentation, validation, filtering, etc. with the response_model.

If you declare both a return type and a response_model, the response_model will take priority and be used by FastAPI.

This way you can add correct type annotations to your functions even when you are returning a type different than the response model, to be used by the editor and tools like mypy. And still you can have FastAPI do the data validation, documentation, etc. using the response_model.

You can also use response_model=None to disable creating a response model for that path operation, you might need to do it if you are adding type annotations for things that are not valid Pydantic fields, you will see an example of that in one of the sections below.

Here we are declaring a UserIn model, it will contain a plaintext password:

To use EmailStr, first install email-validator.

Make sure you create a virtual environment, activate it, and then install it, for example:

And we are using this model to declare our input and the same model to declare our output:

Now, whenever a browser is creating a user with a password, the API will return the same password in the response.

In this case, it might not be a problem, because it's the same user sending the password.

But if we use the same model for another path operation, we could be sending our user's passwords to every client.

Never store the plain password of a user or send it in a response like this, unless you know all the caveats and you know what you are doing.

We can instead create an input model with the plaintext password and an output model without it:

Here, even though our path operation function is returning the same input user that contains the password:

...we declared the response_model to be our model UserOut, that doesn't include the password:

So, FastAPI will take care of filtering out all the data that is not declared in the output model (using Pydantic).

In this case, because the two models are different, if we annotated the function return type as UserOut, the editor and tools would complain that we are returning an invalid type, as those are different classes.

That's why in this example we have to declare it in the response_model parameter.

...but continue reading below to see how to overcome that.

Let's continue from the previous example. We wanted to annotate the function with one type, but we wanted to be able to return from the function something that actually includes more data.

We want FastAPI to keep filtering the data using the response model. So that even though the function returns more data, the response will only include the fields declared in the response model.

In the previous example, because the classes were different, we had to use the response_model parameter. But that also means that we don't get the support from the editor and tools checking the function return type.

But in most of the cases where we need to do something like this, we want the model just to filter/remove some of the data as in this example.

And in those cases, we can use classes and inheritance to take advantage of function type annotations to get better support in the editor and tools, and still get the FastAPI data filtering.

With this, we get tooling support, from editors and mypy as this code is correct in terms of types, but we also get the data filtering from FastAPI.

How does this work? Let's check that out. 🤓

First let's see how editors, mypy and other tools would see this.

BaseUser has the base fields. Then UserIn inherits from BaseUser and adds the password field, so, it will include all the fields from both models.

We annotate the function return type as BaseUser, but we are actually returning a UserIn instance.

The editor, mypy, and other tools won't complain about this because, in typing terms, UserIn is a subclass of BaseUser, which means it's a valid type when what is expected is anything that is a BaseUser.

Now, for FastAPI, it will see the return type and make sure that what you return includes only the fields that are declared in the type.

FastAPI does several things internally with Pydantic to make sure that those same rules of class inheritance are not used for the returned data filtering, otherwise you could end up returning much more data than what you expected.

This way, you can get the best of both worlds: type annotations with tooling support and data filtering.

When you see the automatic docs, you can check that the input model and output model will both have their own JSON Schema:

And both models will be used for the interactive API documentation:

There might be cases where you return something that is not a valid Pydantic field and you annotate it in the function, only to get the support provided by tooling (the editor, mypy, etc).

The most common case would be returning a Response directly as explained later in the advanced docs.

This simple case is handled automatically by FastAPI because the return type annotation is the class (or a subclass of) Response.

And tools will also be happy because both RedirectResponse and JSONResponse are subclasses of Response, so the type annotation is correct.

You can also use a subclass of Response in the type annotation:

This will also work because RedirectResponse is a subclass of Response, and FastAPI will automatically handle this simple case.

But when you return some other arbitrary object that is not a valid Pydantic type (e.g. a database object) and you annotate it like that in the function, FastAPI will try to create a Pydantic response model from that type annotation, and will fail.

The same would happen if you had something like a union between different types where one or more of them are not valid Pydantic types, for example this would fail 💥:

...this fails because the type annotation is not a Pydantic type and is not just a single Response class or subclass, it's a union (any of the two) between a Response and a dict.

Continuing from the example above, you might not want to have the default data validation, documentation, filtering, etc. that is performed by FastAPI.

But you might want to still keep the return type annotation in the function to get the support from tools like editors and type checkers (e.g. mypy).

In this case, you can disable the response model generation by setting response_model=None:

This will make FastAPI skip the response model generation and that way you can have any return type annotations you need without it affecting your FastAPI application. 🤓

Your response model could have default values, like:

but you might want to omit them from the result if they were not actually stored.

For example, if you have models with many optional attributes in a NoSQL database, but you don't want to send very long JSON responses full of default values.

You can set the path operation decorator parameter response_model_exclude_unset=True:

and those default values won't be included in the response, only the values actually set.

So, if you send a request to that path operation for the item with ID foo, the response (not including default values) will be:

as described in the Pydantic docs for exclude_defaults and exclude_none.

But if your data has values for the model's fields with default values, like the item with ID bar:

they will be included in the response.

If the data has the same values as the default ones, like the item with ID baz:

FastAPI is smart enough (actually, Pydantic is smart enough) to realize that, even though description, tax, and tags have the same values as the defaults, they were set explicitly (instead of taken from the defaults).

So, they will be included in the JSON response.

Notice that the default values can be anything, not only None.

They can be a list ([]), a float of 10.5, etc.

You can also use the path operation decorator parameters response_model_include and response_model_exclude.

They take a set of str with the name of the attributes to include (omitting the rest) or to exclude (including the rest).

This can be used as a quick shortcut if you have only one Pydantic model and want to remove some data from the output.

But it is still recommended to use the ideas above, using multiple classes, instead of these parameters.

This is because the JSON Schema generated in your app's OpenAPI (and the docs) will still be the one for the complete model, even if you use response_model_include or response_model_exclude to omit some attributes.

This also applies to response_model_by_alias that works similarly.

The syntax {"name", "description"} creates a set with those two values.

It is equivalent to set(["name", "description"]).

If you forget to use a set and use a list or tuple instead, FastAPI will still convert it to a set and it will work correctly:

Use the path operation decorator's parameter response_model to define response models and especially to ensure private data is filtered out.

Use response_model_exclude_unset to return only the values explicitly set.

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
    tags: list[str] = []


@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item


@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]
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
    tags: list[str] = []


@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item


@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]
```

Example 3 (python):
```python
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item


@app.get("/items/", response_model=list[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]
```

Example 4 (python):
```python
from typing import Any, Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: list[str] = []


@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item


@app.get("/items/", response_model=list[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]
```

---

## Return a Response Directly¶

**URL:** https://fastapi.tiangolo.com/advanced/response-directly/

**Contents:**
- Return a Response Directly¶
- Return a Response¶
- Using the jsonable_encoder in a Response¶
- Returning a custom Response¶
- Notes¶

When you create a FastAPI path operation you can normally return any data from it: a dict, a list, a Pydantic model, a database model, etc.

By default, FastAPI would automatically convert that return value to JSON using the jsonable_encoder explained in JSON Compatible Encoder.

Then, behind the scenes, it would put that JSON-compatible data (e.g. a dict) inside of a JSONResponse that would be used to send the response to the client.

But you can return a JSONResponse directly from your path operations.

It might be useful, for example, to return custom headers or cookies.

In fact, you can return any Response or any sub-class of it.

JSONResponse itself is a sub-class of Response.

And when you return a Response, FastAPI will pass it directly.

It won't do any data conversion with Pydantic models, it won't convert the contents to any type, etc.

This gives you a lot of flexibility. You can return any data type, override any data declaration or validation, etc.

Because FastAPI doesn't make any changes to a Response you return, you have to make sure its contents are ready for it.

For example, you cannot put a Pydantic model in a JSONResponse without first converting it to a dict with all the data types (like datetime, UUID, etc) converted to JSON-compatible types.

For those cases, you can use the jsonable_encoder to convert your data before passing it to a response:

You could also use from starlette.responses import JSONResponse.

FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette.

The example above shows all the parts you need, but it's not very useful yet, as you could have just returned the item directly, and FastAPI would put it in a JSONResponse for you, converting it to a dict, etc. All that by default.

Now, let's see how you could use that to return a custom response.

Let's say that you want to return an XML response.

You could put your XML content in a string, put that in a Response, and return it:

When you return a Response directly its data is not validated, converted (serialized), or documented automatically.

But you can still document it as described in Additional Responses in OpenAPI.

You can see in later sections how to use/declare these custom Responses while still having automatic data conversion, documentation, etc.

**Examples:**

Example 1 (python):
```python
from datetime import datetime

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None


app = FastAPI()


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    return JSONResponse(content=json_compatible_item_data)
```

Example 2 (python):
```python
from datetime import datetime
from typing import Union

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Union[str, None] = None


app = FastAPI()


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    return JSONResponse(content=json_compatible_item_data)
```

Example 3 (python):
```python
from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/legacy/")
def get_legacy_data():
    data = """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
    return Response(content=data, media_type="application/xml")
```

---

## Response Cookies¶

**URL:** https://fastapi.tiangolo.com/advanced/response-cookies/

**Contents:**
- Response Cookies¶
- Use a Response parameter¶
- Return a Response directly¶
  - More info¶

You can declare a parameter of type Response in your path operation function.

And then you can set cookies in that temporal response object.

And then you can return any object you need, as you normally would (a dict, a database model, etc).

And if you declared a response_model, it will still be used to filter and convert the object you returned.

FastAPI will use that temporal response to extract the cookies (also headers and status code), and will put them in the final response that contains the value you returned, filtered by any response_model.

You can also declare the Response parameter in dependencies, and set cookies (and headers) in them.

You can also create cookies when returning a Response directly in your code.

To do that, you can create a response as described in Return a Response Directly.

Then set Cookies in it, and then return it:

Keep in mind that if you return a response directly instead of using the Response parameter, FastAPI will return it directly.

So, you will have to make sure your data is of the correct type. E.g. it is compatible with JSON, if you are returning a JSONResponse.

And also that you are not sending any data that should have been filtered by a response_model.

You could also use from starlette.responses import Response or from starlette.responses import JSONResponse.

FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette.

And as the Response can be used frequently to set headers and cookies, FastAPI also provides it at fastapi.Response.

To see all the available parameters and options, check the documentation in Starlette.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI, Response

app = FastAPI()


@app.post("/cookie-and-object/")
def create_cookie(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "Come to the dark side, we have cookies"}
```

Example 2 (python):
```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post("/cookie/")
def create_cookie():
    content = {"message": "Come to the dark side, we have cookies"}
    response = JSONResponse(content=content)
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return response
```

---

## Response Headers¶

**URL:** https://fastapi.tiangolo.com/advanced/response-headers/

**Contents:**
- Response Headers¶
- Use a Response parameter¶
- Return a Response directly¶
- Custom Headers¶

You can declare a parameter of type Response in your path operation function (as you can do for cookies).

And then you can set headers in that temporal response object.

And then you can return any object you need, as you normally would (a dict, a database model, etc).

And if you declared a response_model, it will still be used to filter and convert the object you returned.

FastAPI will use that temporal response to extract the headers (also cookies and status code), and will put them in the final response that contains the value you returned, filtered by any response_model.

You can also declare the Response parameter in dependencies, and set headers (and cookies) in them.

You can also add headers when you return a Response directly.

Create a response as described in Return a Response Directly and pass the headers as an additional parameter:

You could also use from starlette.responses import Response or from starlette.responses import JSONResponse.

FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette.

And as the Response can be used frequently to set headers and cookies, FastAPI also provides it at fastapi.Response.

Keep in mind that custom proprietary headers can be added using the X- prefix.

But if you have custom headers that you want a client in a browser to be able to see, you need to add them to your CORS configurations (read more in CORS (Cross-Origin Resource Sharing)), using the parameter expose_headers documented in Starlette's CORS docs.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/headers-and-object/")
def get_headers(response: Response):
    response.headers["X-Cat-Dog"] = "alone in the world"
    return {"message": "Hello World"}
```

Example 2 (python):
```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/headers/")
def get_headers():
    content = {"message": "Hello World"}
    headers = {"X-Cat-Dog": "alone in the world", "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)
```

---

## Custom Response - HTML, Stream, File, others¶

**URL:** https://fastapi.tiangolo.com/advanced/custom-response/

**Contents:**
- Custom Response - HTML, Stream, File, others¶
- Use ORJSONResponse¶
- HTML Response¶
  - Return a Response¶
  - Document in OpenAPI and override Response¶
    - Return an HTMLResponse directly¶
- Available responses¶
  - Response¶
  - HTMLResponse¶
  - PlainTextResponse¶

By default, FastAPI will return the responses using JSONResponse.

You can override it by returning a Response directly as seen in Return a Response directly.

But if you return a Response directly (or any subclass, like JSONResponse), the data won't be automatically converted (even if you declare a response_model), and the documentation won't be automatically generated (for example, including the specific "media type", in the HTTP header Content-Type as part of the generated OpenAPI).

But you can also declare the Response that you want to be used (e.g. any Response subclass), in the path operation decorator using the response_class parameter.

The contents that you return from your path operation function will be put inside of that Response.

And if that Response has a JSON media type (application/json), like is the case with the JSONResponse and UJSONResponse, the data you return will be automatically converted (and filtered) with any Pydantic response_model that you declared in the path operation decorator.

If you use a response class with no media type, FastAPI will expect your response to have no content, so it will not document the response format in its generated OpenAPI docs.

For example, if you are squeezing performance, you can install and use orjson and set the response to be ORJSONResponse.

Import the Response class (sub-class) you want to use and declare it in the path operation decorator.

For large responses, returning a Response directly is much faster than returning a dictionary.

This is because by default, FastAPI will inspect every item inside and make sure it is serializable as JSON, using the same JSON Compatible Encoder explained in the tutorial. This is what allows you to return arbitrary objects, for example database models.

But if you are certain that the content that you are returning is serializable with JSON, you can pass it directly to the response class and avoid the extra overhead that FastAPI would have by passing your return content through the jsonable_encoder before passing it to the response class.

The parameter response_class will also be used to define the "media type" of the response.

In this case, the HTTP header Content-Type will be set to application/json.

And it will be documented as such in OpenAPI.

The ORJSONResponse is only available in FastAPI, not in Starlette.

To return a response with HTML directly from FastAPI, use HTMLResponse.

The parameter response_class will also be used to define the "media type" of the response.

In this case, the HTTP header Content-Type will be set to text/html.

And it will be documented as such in OpenAPI.

As seen in Return a Response directly, you can also override the response directly in your path operation, by returning it.

The same example from above, returning an HTMLResponse, could look like:

A Response returned directly by your path operation function won't be documented in OpenAPI (for example, the Content-Type won't be documented) and won't be visible in the automatic interactive docs.

Of course, the actual Content-Type header, status code, etc, will come from the Response object you returned.

If you want to override the response from inside of the function but at the same time document the "media type" in OpenAPI, you can use the response_class parameter AND return a Response object.

The response_class will then be used only to document the OpenAPI path operation, but your Response will be used as is.

For example, it could be something like:

In this example, the function generate_html_response() already generates and returns a Response instead of returning the HTML in a str.

By returning the result of calling generate_html_response(), you are already returning a Response that will override the default FastAPI behavior.

But as you passed the HTMLResponse in the response_class too, FastAPI will know how to document it in OpenAPI and the interactive docs as HTML with text/html:

Here are some of the available responses.

Keep in mind that you can use Response to return anything else, or even create a custom sub-class.

You could also use from starlette.responses import HTMLResponse.

FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette.

The main Response class, all the other responses inherit from it.

You can return it directly.

It accepts the following parameters:

FastAPI (actually Starlette) will automatically include a Content-Length header. It will also include a Content-Type header, based on the media_type and appending a charset for text types.

Takes some text or bytes and returns an HTML response, as you read above.

Takes some text or bytes and returns a plain text response.

Takes some data and returns an application/json encoded response.

This is the default response used in FastAPI, as you read above.

A fast alternative JSON response using orjson, as you read above.

This requires installing orjson for example with pip install orjson.

An alternative JSON response using ujson.

This requires installing ujson for example with pip install ujson.

ujson is less careful than Python's built-in implementation in how it handles some edge-cases.

It's possible that ORJSONResponse might be a faster alternative.

Returns an HTTP redirect. Uses a 307 status code (Temporary Redirect) by default.

You can return a RedirectResponse directly:

Or you can use it in the response_class parameter:

If you do that, then you can return the URL directly from your path operation function.

In this case, the status_code used will be the default one for the RedirectResponse, which is 307.

You can also use the status_code parameter combined with the response_class parameter:

Takes an async generator or a normal generator/iterator and streams the response body.

If you have a file-like object (e.g. the object returned by open()), you can create a generator function to iterate over that file-like object.

That way, you don't have to read it all first in memory, and you can pass that generator function to the StreamingResponse, and return it.

This includes many libraries to interact with cloud storage, video processing, and others.

This yield from tells the function to iterate over that thing named file_like. And then, for each part iterated, yield that part as coming from this generator function (iterfile).

So, it is a generator function that transfers the "generating" work to something else internally.

By doing it this way, we can put it in a with block, and that way, ensure that the file-like object is closed after finishing.

Notice that here as we are using standard open() that doesn't support async and await, we declare the path operation with normal def.

Asynchronously streams a file as the response.

Takes a different set of arguments to instantiate than the other response types:

File responses will include appropriate Content-Length, Last-Modified and ETag headers.

You can also use the response_class parameter:

In this case, you can return the file path directly from your path operation function.

You can create your own custom response class, inheriting from Response and using it.

For example, let's say that you want to use orjson, but with some custom settings not used in the included ORJSONResponse class.

Let's say you want it to return indented and formatted JSON, so you want to use the orjson option orjson.OPT_INDENT_2.

You could create a CustomORJSONResponse. The main thing you have to do is create a Response.render(content) method that returns the content as bytes:

Now instead of returning:

...this response will return:

Of course, you will probably find much better ways to take advantage of this than formatting JSON. 😉

When creating a FastAPI class instance or an APIRouter you can specify which response class to use by default.

The parameter that defines this is default_response_class.

In the example below, FastAPI will use ORJSONResponse by default, in all path operations, instead of JSONResponse.

You can still override response_class in path operations as before.

You can also declare the media type and many other details in OpenAPI using responses: Additional Responses in OpenAPI.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI()


@app.get("/items/", response_class=ORJSONResponse)
async def read_items():
    return ORJSONResponse([{"item_id": "Foo"}])
```

Example 2 (python):
```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/items/", response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
```

Example 3 (python):
```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/items/")
async def read_items():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
```

Example 4 (python):
```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


def generate_html_response():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/items/", response_class=HTMLResponse)
async def read_items():
    return generate_html_response()
```

---

## Extra Models¶

**URL:** https://fastapi.tiangolo.com/tutorial/extra-models/

**Contents:**
- Extra Models¶
- Multiple models¶
  - About **user_in.model_dump()¶
    - Pydantic's .model_dump()¶
    - Unpacking a dict¶
    - A Pydantic model from the contents of another¶
    - Unpacking a dict and extra keywords¶
- Reduce duplication¶
- Union or anyOf¶
  - Union in Python 3.10¶

Continuing with the previous example, it will be common to have more than one related model.

This is especially the case for user models, because:

Never store user's plaintext passwords. Always store a "secure hash" that you can then verify.

If you don't know, you will learn what a "password hash" is in the security chapters.

Here's a general idea of how the models could look like with their password fields and the places where they are used:

user_in is a Pydantic model of class UserIn.

Pydantic models have a .model_dump() method that returns a dict with the model's data.

So, if we create a Pydantic object user_in like:

we now have a dict with the data in the variable user_dict (it's a dict instead of a Pydantic model object).

we would get a Python dict with:

If we take a dict like user_dict and pass it to a function (or class) with **user_dict, Python will "unpack" it. It will pass the keys and values of the user_dict directly as key-value arguments.

So, continuing with the user_dict from above, writing:

would result in something equivalent to:

Or more exactly, using user_dict directly, with whatever contents it might have in the future:

As in the example above we got user_dict from user_in.model_dump(), this code:

would be equivalent to:

...because user_in.model_dump() is a dict, and then we make Python "unpack" it by passing it to UserInDB prefixed with **.

So, we get a Pydantic model from the data in another Pydantic model.

And then adding the extra keyword argument hashed_password=hashed_password, like in:

...ends up being like:

The supporting additional functions fake_password_hasher and fake_save_user are just to demo a possible flow of the data, but they of course are not providing any real security.

Reducing code duplication is one of the core ideas in FastAPI.

As code duplication increments the chances of bugs, security issues, code desynchronization issues (when you update in one place but not in the others), etc.

And these models are all sharing a lot of the data and duplicating attribute names and types.

We can declare a UserBase model that serves as a base for our other models. And then we can make subclasses of that model that inherit its attributes (type declarations, validation, etc).

All the data conversion, validation, documentation, etc. will still work as normally.

That way, we can declare just the differences between the models (with plaintext password, with hashed_password and without password):

You can declare a response to be the Union of two or more types, that means, that the response would be any of them.

It will be defined in OpenAPI with anyOf.

To do that, use the standard Python type hint typing.Union:

When defining a Union, include the most specific type first, followed by the less specific type. In the example below, the more specific PlaneItem comes before CarItem in Union[PlaneItem, CarItem].

In this example we pass Union[PlaneItem, CarItem] as the value of the argument response_model.

Because we are passing it as a value to an argument instead of putting it in a type annotation, we have to use Union even in Python 3.10.

If it was in a type annotation we could have used the vertical bar, as:

But if we put that in the assignment response_model=PlaneItem | CarItem we would get an error, because Python would try to perform an invalid operation between PlaneItem and CarItem instead of interpreting that as a type annotation.

The same way, you can declare responses of lists of objects.

For that, use the standard Python typing.List (or just list in Python 3.9 and above):

You can also declare a response using a plain arbitrary dict, declaring just the type of the keys and values, without using a Pydantic model.

This is useful if you don't know the valid field/attribute names (that would be needed for a Pydantic model) beforehand.

In this case, you can use typing.Dict (or just dict in Python 3.9 and above):

Use multiple Pydantic models and inherit freely for each case.

You don't need to have a single data model per entity if that entity must be able to have different "states". As the case with the user "entity" with a state including password, password_hash and no password.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
```

Example 2 (python):
```python
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Union[str, None] = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
```

Example 3 (python):
```python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

Example 4 (unknown):
```unknown
user_dict = user_in.model_dump()
```

---
