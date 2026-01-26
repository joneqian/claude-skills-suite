# Fastapi - Path Operations

**Pages:** 7

---

## Path Operation Advanced Configuration¶

**URL:** https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/

**Contents:**
- Path Operation Advanced Configuration¶
- OpenAPI operationId¶
  - Using the path operation function name as the operationId¶
- Exclude from OpenAPI¶
- Advanced description from docstring¶
- Additional Responses¶
- OpenAPI Extra¶
  - OpenAPI Extensions¶
  - Custom OpenAPI path operation schema¶
  - Custom OpenAPI content type¶

If you are not an "expert" in OpenAPI, you probably don't need this.

You can set the OpenAPI operationId to be used in your path operation with the parameter operation_id.

You would have to make sure that it is unique for each operation.

If you want to use your APIs' function names as operationIds, you can iterate over all of them and override each path operation's operation_id using their APIRoute.name.

You should do it after adding all your path operations.

If you manually call app.openapi(), you should update the operationIds before that.

If you do this, you have to make sure each one of your path operation functions has a unique name.

Even if they are in different modules (Python files).

To exclude a path operation from the generated OpenAPI schema (and thus, from the automatic documentation systems), use the parameter include_in_schema and set it to False:

You can limit the lines used from the docstring of a path operation function for OpenAPI.

Adding an \f (an escaped "form feed" character) causes FastAPI to truncate the output used for OpenAPI at this point.

It won't show up in the documentation, but other tools (such as Sphinx) will be able to use the rest.

You probably have seen how to declare the response_model and status_code for a path operation.

That defines the metadata about the main response of a path operation.

You can also declare additional responses with their models, status codes, etc.

There's a whole chapter here in the documentation about it, you can read it at Additional Responses in OpenAPI.

When you declare a path operation in your application, FastAPI automatically generates the relevant metadata about that path operation to be included in the OpenAPI schema.

In the OpenAPI specification it is called the Operation Object.

It has all the information about the path operation and is used to generate the automatic documentation.

It includes the tags, parameters, requestBody, responses, etc.

This path operation-specific OpenAPI schema is normally generated automatically by FastAPI, but you can also extend it.

This is a low level extension point.

If you only need to declare additional responses, a more convenient way to do it is with Additional Responses in OpenAPI.

You can extend the OpenAPI schema for a path operation using the parameter openapi_extra.

This openapi_extra can be helpful, for example, to declare OpenAPI Extensions:

If you open the automatic API docs, your extension will show up at the bottom of the specific path operation.

And if you see the resulting OpenAPI (at /openapi.json in your API), you will see your extension as part of the specific path operation too:

The dictionary in openapi_extra will be deeply merged with the automatically generated OpenAPI schema for the path operation.

So, you could add additional data to the automatically generated schema.

For example, you could decide to read and validate the request with your own code, without using the automatic features of FastAPI with Pydantic, but you could still want to define the request in the OpenAPI schema.

You could do that with openapi_extra:

In this example, we didn't declare any Pydantic model. In fact, the request body is not even parsed as JSON, it is read directly as bytes, and the function magic_data_reader() would be in charge of parsing it in some way.

Nevertheless, we can declare the expected schema for the request body.

Using this same trick, you could use a Pydantic model to define the JSON Schema that is then included in the custom OpenAPI schema section for the path operation.

And you could do this even if the data type in the request is not JSON.

For example, in this application we don't use FastAPI's integrated functionality to extract the JSON Schema from Pydantic models nor the automatic validation for JSON. In fact, we are declaring the request content type as YAML, not JSON:

Nevertheless, although we are not using the default integrated functionality, we are still using a Pydantic model to manually generate the JSON Schema for the data that we want to receive in YAML.

Then we use the request directly, and extract the body as bytes. This means that FastAPI won't even try to parse the request payload as JSON.

And then in our code, we parse that YAML content directly, and then we are again using the same Pydantic model to validate the YAML content:

Here we reuse the same Pydantic model.

But the same way, we could have validated it in some other way.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/", operation_id="some_specific_id_you_define")
async def read_items():
    return [{"item_id": "Foo"}]
```

Example 2 (python):
```python
from fastapi import FastAPI
from fastapi.routing import APIRoute

app = FastAPI()


@app.get("/items/")
async def read_items():
    return [{"item_id": "Foo"}]


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'


use_route_names_as_operation_ids(app)
```

Example 3 (python):
```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/", include_in_schema=False)
async def read_items():
    return [{"item_id": "Foo"}]
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
    tags: set[str] = set()


@app.post("/items/", response_model=Item, summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    \f
    :param item: User input.
    """
    return item
```

---

## Path Parameters¶

**URL:** https://fastapi.tiangolo.com/tutorial/path-params/

**Contents:**
- Path Parameters¶
- Path parameters with types¶
- Data conversion¶
- Data validation¶
- Documentation¶
- Standards-based benefits, alternative documentation¶
- Pydantic¶
- Order matters¶
- Predefined values¶
  - Create an Enum class¶

You can declare path "parameters" or "variables" with the same syntax used by Python format strings:

The value of the path parameter item_id will be passed to your function as the argument item_id.

So, if you run this example and go to http://127.0.0.1:8000/items/foo, you will see a response of:

You can declare the type of a path parameter in the function, using standard Python type annotations:

In this case, item_id is declared to be an int.

This will give you editor support inside of your function, with error checks, completion, etc.

If you run this example and open your browser at http://127.0.0.1:8000/items/3, you will see a response of:

Notice that the value your function received (and returned) is 3, as a Python int, not a string "3".

So, with that type declaration, FastAPI gives you automatic request "parsing".

But if you go to the browser at http://127.0.0.1:8000/items/foo, you will see a nice HTTP error of:

because the path parameter item_id had a value of "foo", which is not an int.

The same error would appear if you provided a float instead of an int, as in: http://127.0.0.1:8000/items/4.2

So, with the same Python type declaration, FastAPI gives you data validation.

Notice that the error also clearly states exactly the point where the validation didn't pass.

This is incredibly helpful while developing and debugging code that interacts with your API.

And when you open your browser at http://127.0.0.1:8000/docs, you will see an automatic, interactive, API documentation like:

Again, just with that same Python type declaration, FastAPI gives you automatic, interactive documentation (integrating Swagger UI).

Notice that the path parameter is declared to be an integer.

And because the generated schema is from the OpenAPI standard, there are many compatible tools.

Because of this, FastAPI itself provides an alternative API documentation (using ReDoc), which you can access at http://127.0.0.1:8000/redoc:

The same way, there are many compatible tools. Including code generation tools for many languages.

All the data validation is performed under the hood by Pydantic, so you get all the benefits from it. And you know you are in good hands.

You can use the same type declarations with str, float, bool and many other complex data types.

Several of these are explored in the next chapters of the tutorial.

When creating path operations, you can find situations where you have a fixed path.

Like /users/me, let's say that it's to get data about the current user.

And then you can also have a path /users/{user_id} to get data about a specific user by some user ID.

Because path operations are evaluated in order, you need to make sure that the path for /users/me is declared before the one for /users/{user_id}:

Otherwise, the path for /users/{user_id} would match also for /users/me, "thinking" that it's receiving a parameter user_id with a value of "me".

Similarly, you cannot redefine a path operation:

The first one will always be used since the path matches first.

If you have a path operation that receives a path parameter, but you want the possible valid path parameter values to be predefined, you can use a standard Python Enum.

Import Enum and create a sub-class that inherits from str and from Enum.

By inheriting from str the API docs will be able to know that the values must be of type string and will be able to render correctly.

Then create class attributes with fixed values, which will be the available valid values:

If you are wondering, "AlexNet", "ResNet", and "LeNet" are just names of Machine Learning models.

Then create a path parameter with a type annotation using the enum class you created (ModelName):

Because the available values for the path parameter are predefined, the interactive docs can show them nicely:

The value of the path parameter will be an enumeration member.

You can compare it with the enumeration member in your created enum ModelName:

You can get the actual value (a str in this case) using model_name.value, or in general, your_enum_member.value:

You could also access the value "lenet" with ModelName.lenet.value.

You can return enum members from your path operation, even nested in a JSON body (e.g. a dict).

They will be converted to their corresponding values (strings in this case) before returning them to the client:

In your client you will get a JSON response like:

Let's say you have a path operation with a path /files/{file_path}.

But you need file_path itself to contain a path, like home/johndoe/myfile.txt.

So, the URL for that file would be something like: /files/home/johndoe/myfile.txt.

OpenAPI doesn't support a way to declare a path parameter to contain a path inside, as that could lead to scenarios that are difficult to test and define.

Nevertheless, you can still do it in FastAPI, using one of the internal tools from Starlette.

And the docs would still work, although not adding any documentation telling that the parameter should contain a path.

Using an option directly from Starlette you can declare a path parameter containing a path using a URL like:

In this case, the name of the parameter is file_path, and the last part, :path, tells it that the parameter should match any path.

So, you can use it with:

You might need the parameter to contain /home/johndoe/myfile.txt, with a leading slash (/).

In that case, the URL would be: /files//home/johndoe/myfile.txt, with a double slash (//) between files and home.

With FastAPI, by using short, intuitive and standard Python type declarations, you get:

And you only have to declare them once.

That's probably the main visible advantage of FastAPI compared to alternative frameworks (apart from the raw performance).

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
```

Example 2 (json):
```json
{"item_id":"foo"}
```

Example 3 (python):
```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

Example 4 (json):
```json
{"item_id":3}
```

---

## Query Parameters¶

**URL:** https://fastapi.tiangolo.com/tutorial/query-params/

**Contents:**
- Query Parameters¶
- Defaults¶
- Optional parameters¶
- Query parameter type conversion¶
- Multiple path and query parameters¶
- Required query parameters¶

When you declare other function parameters that are not part of the path parameters, they are automatically interpreted as "query" parameters.

The query is the set of key-value pairs that go after the ? in a URL, separated by & characters.

For example, in the URL:

...the query parameters are:

As they are part of the URL, they are "naturally" strings.

But when you declare them with Python types (in the example above, as int), they are converted to that type and validated against it.

All the same process that applied for path parameters also applies for query parameters:

As query parameters are not a fixed part of a path, they can be optional and can have default values.

In the example above they have default values of skip=0 and limit=10.

So, going to the URL:

would be the same as going to:

But if you go to, for example:

The parameter values in your function will be:

The same way, you can declare optional query parameters, by setting their default to None:

In this case, the function parameter q will be optional, and will be None by default.

Also notice that FastAPI is smart enough to notice that the path parameter item_id is a path parameter and q is not, so, it's a query parameter.

You can also declare bool types, and they will be converted:

In this case, if you go to:

or any other case variation (uppercase, first letter in uppercase, etc), your function will see the parameter short with a bool value of True. Otherwise as False.

You can declare multiple path parameters and query parameters at the same time, FastAPI knows which is which.

And you don't have to declare them in any specific order.

They will be detected by name:

When you declare a default value for non-path parameters (for now, we have only seen query parameters), then it is not required.

If you don't want to add a specific value but just make it optional, set the default as None.

But when you want to make a query parameter required, you can just not declare any default value:

Here the query parameter needy is a required query parameter of type str.

If you open in your browser a URL like:

...without adding the required parameter needy, you will see an error like:

As needy is a required parameter, you would need to set it in the URL:

And of course, you can define some parameters as required, some as having a default value, and some entirely optional:

In this case, there are 3 query parameters:

You could also use Enums the same way as with Path Parameters.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
```

Example 2 (yaml):
```yaml
http://127.0.0.1:8000/items/?skip=0&limit=10
```

Example 3 (yaml):
```yaml
http://127.0.0.1:8000/items/
```

Example 4 (yaml):
```yaml
http://127.0.0.1:8000/items/?skip=0&limit=10
```

---

## Dependencies in path operation decorators¶

**URL:** https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/

**Contents:**
- Dependencies in path operation decorators¶
- Add dependencies to the path operation decorator¶
- Dependencies errors and return values¶
  - Dependency requirements¶
  - Raise exceptions¶
  - Return values¶
- Dependencies for a group of path operations¶
- Global Dependencies¶

In some cases you don't really need the return value of a dependency inside your path operation function.

Or the dependency doesn't return a value.

But you still need it to be executed/solved.

For those cases, instead of declaring a path operation function parameter with Depends, you can add a list of dependencies to the path operation decorator.

The path operation decorator receives an optional argument dependencies.

It should be a list of Depends():

Prefer to use the Annotated version if possible.

These dependencies will be executed/solved the same way as normal dependencies. But their value (if they return any) won't be passed to your path operation function.

Some editors check for unused function parameters, and show them as errors.

Using these dependencies in the path operation decorator you can make sure they are executed while avoiding editor/tooling errors.

It might also help avoid confusion for new developers that see an unused parameter in your code and could think it's unnecessary.

In this example we use invented custom headers X-Key and X-Token.

But in real cases, when implementing security, you would get more benefits from using the integrated Security utilities (the next chapter).

You can use the same dependency functions you use normally.

They can declare request requirements (like headers) or other sub-dependencies:

Prefer to use the Annotated version if possible.

These dependencies can raise exceptions, the same as normal dependencies:

Prefer to use the Annotated version if possible.

And they can return values or not, the values won't be used.

So, you can reuse a normal dependency (that returns a value) you already use somewhere else, and even though the value won't be used, the dependency will be executed:

Prefer to use the Annotated version if possible.

Later, when reading about how to structure bigger applications (Bigger Applications - Multiple Files), possibly with multiple files, you will learn how to declare a single dependencies parameter for a group of path operations.

Next we will see how to add dependencies to the whole FastAPI application, so that they apply to each path operation.

**Examples:**

Example 1 (python):
```python
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()


async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
```

Example 2 (python):
```python
from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()


async def verify_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header()):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
```

Example 3 (python):
```python
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()


async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
```

Example 4 (python):
```python
from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()


async def verify_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header()):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
```

---

## Path Operation Configuration¶

**URL:** https://fastapi.tiangolo.com/tutorial/path-operation-configuration/

**Contents:**
- Path Operation Configuration¶
- Response Status Code¶
- Tags¶
  - Tags with Enums¶
- Summary and description¶
- Description from docstring¶
- Response description¶
- Deprecate a path operation¶
- Recap¶

There are several parameters that you can pass to your path operation decorator to configure it.

Notice that these parameters are passed directly to the path operation decorator, not to your path operation function.

You can define the (HTTP) status_code to be used in the response of your path operation.

You can pass directly the int code, like 404.

But if you don't remember what each number code is for, you can use the shortcut constants in status:

That status code will be used in the response and will be added to the OpenAPI schema.

You could also use from starlette import status.

FastAPI provides the same starlette.status as fastapi.status just as a convenience for you, the developer. But it comes directly from Starlette.

You can add tags to your path operation, pass the parameter tags with a list of str (commonly just one str):

They will be added to the OpenAPI schema and used by the automatic documentation interfaces:

If you have a big application, you might end up accumulating several tags, and you would want to make sure you always use the same tag for related path operations.

In these cases, it could make sense to store the tags in an Enum.

FastAPI supports that the same way as with plain strings:

You can add a summary and description:

As descriptions tend to be long and cover multiple lines, you can declare the path operation description in the function docstring and FastAPI will read it from there.

You can write Markdown in the docstring, it will be interpreted and displayed correctly (taking into account docstring indentation).

It will be used in the interactive docs:

You can specify the response description with the parameter response_description:

Notice that response_description refers specifically to the response, the description refers to the path operation in general.

OpenAPI specifies that each path operation requires a response description.

So, if you don't provide one, FastAPI will automatically generate one of "Successful response".

If you need to mark a path operation as deprecated, but without removing it, pass the parameter deprecated:

It will be clearly marked as deprecated in the interactive docs:

Check how deprecated and non-deprecated path operations look like:

You can configure and add metadata for your path operations easily by passing parameters to the path operation decorators.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item
```

Example 2 (python):
```python
from typing import Union

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: set[str] = set()


@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item
```

Example 3 (python):
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.post("/items/", response_model=Item, tags=["items"])
async def create_item(item: Item):
    return item


@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]
```

Example 4 (python):
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
    tags: set[str] = set()


@app.post("/items/", response_model=Item, tags=["items"])
async def create_item(item: Item):
    return item


@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]
```

---

## Query Parameters and String Validations¶

**URL:** https://fastapi.tiangolo.com/tutorial/query-params-str-validations/

**Contents:**
- Query Parameters and String Validations¶
- Additional validation¶
  - Import Query and Annotated¶
- Use Annotated in the type for the q parameter¶
- Add Query to Annotated in the q parameter¶
- Alternative (old): Query as the default value¶
  - Query as the default value or in Annotated¶
  - Advantages of Annotated¶
- Add more validations¶
- Add regular expressions¶

FastAPI allows you to declare additional information and validation for your parameters.

Let's take this application as example:

The query parameter q is of type str | None, that means that it's of type str but could also be None, and indeed, the default value is None, so FastAPI will know it's not required.

FastAPI will know that the value of q is not required because of the default value = None.

Having str | None will allow your editor to give you better support and detect errors.

We are going to enforce that even though q is optional, whenever it is provided, its length doesn't exceed 50 characters.

To achieve that, first import:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

FastAPI added support for Annotated (and started recommending it) in version 0.95.0.

If you have an older version, you would get errors when trying to use Annotated.

Make sure you Upgrade the FastAPI version to at least 0.95.1 before using Annotated.

Remember I told you before that Annotated can be used to add metadata to your parameters in the Python Types Intro?

Now it's the time to use it with FastAPI. 🚀

We had this type annotation:

What we will do is wrap that with Annotated, so it becomes:

Both of those versions mean the same thing, q is a parameter that can be a str or None, and by default, it is None.

Now let's jump to the fun stuff. 🎉

Now that we have this Annotated where we can put more information (in this case some additional validation), add Query inside of Annotated, and set the parameter max_length to 50:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Notice that the default value is still None, so the parameter is still optional.

But now, having Query(max_length=50) inside of Annotated, we are telling FastAPI that we want it to have additional validation for this value, we want it to have maximum 50 characters. 😎

Here we are using Query() because this is a query parameter. Later we will see others like Path(), Body(), Header(), and Cookie(), that also accept the same arguments as Query().

Previous versions of FastAPI (before 0.95.0) required you to use Query as the default value of your parameter, instead of putting it in Annotated, there's a high chance that you will see code using it around, so I'll explain it to you.

For new code and whenever possible, use Annotated as explained above. There are multiple advantages (explained below) and no disadvantages. 🍰

This is how you would use Query() as the default value of your function parameter, setting the parameter max_length to 50:

Prefer to use the Annotated version if possible.

As in this case (without using Annotated) we have to replace the default value None in the function with Query(), we now need to set the default value with the parameter Query(default=None), it serves the same purpose of defining that default value (at least for FastAPI).

...makes the parameter optional, with a default value of None, the same as:

But the Query version declares it explicitly as being a query parameter.

Then, we can pass more parameters to Query. In this case, the max_length parameter that applies to strings:

This will validate the data, show a clear error when the data is not valid, and document the parameter in the OpenAPI schema path operation.

Keep in mind that when using Query inside of Annotated you cannot use the default parameter for Query.

Instead, use the actual default value of the function parameter. Otherwise, it would be inconsistent.

For example, this is not allowed:

...because it's not clear if the default value should be "rick" or "morty".

So, you would use (preferably):

...or in older code bases you will find:

Using Annotated is recommended instead of the default value in function parameters, it is better for multiple reasons. 🤓

The default value of the function parameter is the actual default value, that's more intuitive with Python in general. 😌

You could call that same function in other places without FastAPI, and it would work as expected. If there's a required parameter (without a default value), your editor will let you know with an error, Python will also complain if you run it without passing the required parameter.

When you don't use Annotated and instead use the (old) default value style, if you call that function without FastAPI in other places, you have to remember to pass the arguments to the function for it to work correctly, otherwise the values will be different from what you expect (e.g. QueryInfo or something similar instead of str). And your editor won't complain, and Python won't complain running that function, only when the operations inside error out.

Because Annotated can have more than one metadata annotation, you could now even use the same function with other tools, like Typer. 🚀

You can also add a parameter min_length:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

You can define a regular expression pattern that the parameter should match:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

This specific regular expression pattern checks that the received parameter value:

If you feel lost with all these "regular expression" ideas, don't worry. They are a hard topic for many people. You can still do a lot of stuff without needing regular expressions yet.

Now you know that whenever you need them you can use them in FastAPI.

You can, of course, use default values other than None.

Let's say that you want to declare the q query parameter to have a min_length of 3, and to have a default value of "fixedquery":

Prefer to use the Annotated version if possible.

Having a default value of any type, including None, makes the parameter optional (not required).

When we don't need to declare more validations or metadata, we can make the q query parameter required just by not declaring a default value, like:

But we are now declaring it with Query, for example like:

So, when you need to declare a value as required while using Query, you can simply not declare a default value:

Prefer to use the Annotated version if possible.

You can declare that a parameter can accept None, but that it's still required. This would force clients to send a value, even if the value is None.

To do that, you can declare that None is a valid type but simply do not declare a default value:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

When you define a query parameter explicitly with Query you can also declare it to receive a list of values, or said in another way, to receive multiple values.

For example, to declare a query parameter q that can appear multiple times in the URL, you can write:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Then, with a URL like:

you would receive the multiple q query parameters' values (foo and bar) in a Python list inside your path operation function, in the function parameter q.

So, the response to that URL would be:

To declare a query parameter with a type of list, like in the example above, you need to explicitly use Query, otherwise it would be interpreted as a request body.

The interactive API docs will update accordingly, to allow multiple values:

You can also define a default list of values if none are provided:

Prefer to use the Annotated version if possible.

the default of q will be: ["foo", "bar"] and your response will be:

You can also use list directly instead of list[str]:

Prefer to use the Annotated version if possible.

Keep in mind that in this case, FastAPI won't check the contents of the list.

For example, list[int] would check (and document) that the contents of the list are integers. But list alone wouldn't.

You can add more information about the parameter.

That information will be included in the generated OpenAPI and used by the documentation user interfaces and external tools.

Keep in mind that different tools might have different levels of OpenAPI support.

Some of them might not show all the extra information declared yet, although in most of the cases, the missing feature is already planned for development.

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Imagine that you want the parameter to be item-query.

But item-query is not a valid Python variable name.

The closest would be item_query.

But you still need it to be exactly item-query...

Then you can declare an alias, and that alias is what will be used to find the parameter value:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Now let's say you don't like this parameter anymore.

You have to leave it there a while because there are clients using it, but you want the docs to clearly show it as deprecated.

Then pass the parameter deprecated=True to Query:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

The docs will show it like this:

To exclude a query parameter from the generated OpenAPI schema (and thus, from the automatic documentation systems), set the parameter include_in_schema of Query to False:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

There could be cases where you need to do some custom validation that can't be done with the parameters shown above.

In those cases, you can use a custom validator function that is applied after the normal validation (e.g. after validating that the value is a str).

You can achieve that using Pydantic's AfterValidator inside of Annotated.

Pydantic also has BeforeValidator and others. 🤓

For example, this custom validator checks that the item ID starts with isbn- for an ISBN book number or with imdb- for an IMDB movie URL ID:

This is available with Pydantic version 2 or above. 😎

If you need to do any type of validation that requires communicating with any external component, like a database or another API, you should instead use FastAPI Dependencies, you will learn about them later.

These custom validators are for things that can be checked with only the same data provided in the request.

The important point is just using AfterValidator with a function inside Annotated. Feel free to skip this part. 🤸

But if you're curious about this specific code example and you're still entertained, here are some extra details.

Did you notice? a string using value.startswith() can take a tuple, and it will check each value in the tuple:

With data.items() we get an iterable object with tuples containing the key and value for each dictionary item.

We convert this iterable object into a proper list with list(data.items()).

Then with random.choice() we can get a random value from the list, so, we get a tuple with (id, name). It will be something like ("imdb-tt0371724", "The Hitchhiker's Guide to the Galaxy").

Then we assign those two values of the tuple to the variables id and name.

So, if the user didn't provide an item ID, they will still receive a random suggestion.

...we do all this in a single simple line. 🤯 Don't you love Python? 🐍

You can declare additional validations and metadata for your parameters.

Generic validations and metadata:

Validations specific for strings:

Custom validations using AfterValidator.

In these examples you saw how to declare validations for str values.

See the next chapters to learn how to declare validations for other types, like numbers.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

Example 2 (python):
```python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(q: Union[str, None] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

Example 3 (python):
```python
from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

Example 4 (python):
```python
from typing import Annotated, Union

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: Annotated[Union[str, None], Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

---

## Path Parameters and Numeric Validations¶

**URL:** https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/

**Contents:**
- Path Parameters and Numeric Validations¶
- Import Path¶
- Declare metadata¶
- Order the parameters as you need¶
- Order the parameters as you need, tricks¶
  - Better with Annotated¶
- Number validations: greater than or equal¶
- Number validations: greater than and less than or equal¶
- Number validations: floats, greater than and less than¶
- Recap¶

In the same way that you can declare more validations and metadata for query parameters with Query, you can declare the same type of validations and metadata for path parameters with Path.

First, import Path from fastapi, and import Annotated:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

FastAPI added support for Annotated (and started recommending it) in version 0.95.0.

If you have an older version, you would get errors when trying to use Annotated.

Make sure you Upgrade the FastAPI version to at least 0.95.1 before using Annotated.

You can declare all the same parameters as for Query.

For example, to declare a title metadata value for the path parameter item_id you can type:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

A path parameter is always required as it has to be part of the path. Even if you declared it with None or set a default value, it would not affect anything, it would still be always required.

This is probably not as important or necessary if you use Annotated.

Let's say that you want to declare the query parameter q as a required str.

And you don't need to declare anything else for that parameter, so you don't really need to use Query.

But you still need to use Path for the item_id path parameter. And you don't want to use Annotated for some reason.

Python will complain if you put a value with a "default" before a value that doesn't have a "default".

But you can re-order them, and have the value without a default (the query parameter q) first.

It doesn't matter for FastAPI. It will detect the parameters by their names, types and default declarations (Query, Path, etc), it doesn't care about the order.

So, you can declare your function as:

But keep in mind that if you use Annotated, you won't have this problem, it won't matter as you're not using the function parameter default values for Query() or Path().

Prefer to use the Annotated version if possible.

This is probably not as important or necessary if you use Annotated.

Here's a small trick that can be handy, but you won't need it often.

...Python has a little special syntax for that.

Pass *, as the first parameter of the function.

Python won't do anything with that *, but it will know that all the following parameters should be called as keyword arguments (key-value pairs), also known as kwargs. Even if they don't have a default value.

Keep in mind that if you use Annotated, as you are not using function parameter default values, you won't have this problem, and you probably won't need to use *.

Prefer to use the Annotated version if possible.

With Query and Path (and others you'll see later) you can declare number constraints.

Here, with ge=1, item_id will need to be an integer number "greater than or equal" to 1.

Prefer to use the Annotated version if possible.

The same applies for:

Prefer to use the Annotated version if possible.

Number validations also work for float values.

Here's where it becomes important to be able to declare gt and not just ge. As with it you can require, for example, that a value must be greater than 0, even if it is less than 1.

So, 0.5 would be a valid value. But 0.0 or 0 would not.

Prefer to use the Annotated version if possible.

With Query, Path (and others you haven't seen yet) you can declare metadata and string validations in the same ways as with Query Parameters and String Validations.

And you can also declare numeric validations:

Query, Path, and other classes you will see later are subclasses of a common Param class.

All of them share the same parameters for additional validation and metadata you have seen.

When you import Query, Path and others from fastapi, they are actually functions.

That when called, return instances of classes of the same name.

So, you import Query, which is a function. And when you call it, it returns an instance of a class also named Query.

These functions are there (instead of just using the classes directly) so that your editor doesn't mark errors about their types.

That way you can use your normal editor and coding tools without having to add custom configurations to disregard those errors.

**Examples:**

Example 1 (python):
```python
from typing import Annotated

from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

Example 2 (python):
```python
from typing import Annotated, Union

from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[Union[str, None], Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

Example 3 (python):
```python
from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: str | None = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

Example 4 (python):
```python
from typing import Union

from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: Union[str, None] = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

---
