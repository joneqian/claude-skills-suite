# Fastapi - Deployment

**Pages:** 42

---

## HTTPConnection class¶

**URL:** https://fastapi.tiangolo.com/reference/httpconnection/

**Contents:**
- HTTPConnection class¶
- fastapi.requests.HTTPConnection ¶
  - scope instance-attribute ¶
  - app property ¶
  - url property ¶
  - base_url property ¶
  - headers property ¶
  - query_params property ¶
  - path_params property ¶
  - cookies property ¶

When you want to define dependencies that should be compatible with both HTTP and WebSockets, you can define a parameter that takes an HTTPConnection instead of a Request or a WebSocket.

You can import it from fastapi.requests:

Bases: Mapping[str, Any]

A base class for incoming HTTP connections, that is used to provide any functionality that is common to both Request and WebSocket.

**Examples:**

Example 1 (sql):
```sql
from fastapi.requests import HTTPConnection
```

Example 2 (rust):
```rust
HTTPConnection(scope, receive=None)
```

Example 3 (python):
```python
def __init__(self, scope: Scope, receive: Receive | None = None) -> None:
    assert scope["type"] in ("http", "websocket")
    self.scope = scope
```

Example 4 (unknown):
```unknown
scope = scope
```

---

## Cookie Parameter Models¶

**URL:** https://fastapi.tiangolo.com/tutorial/cookie-param-models/

**Contents:**
- Cookie Parameter Models¶
- Cookies with a Pydantic Model¶
- Check the Docs¶
- Forbid Extra Cookies¶
- Summary¶

If you have a group of cookies that are related, you can create a Pydantic model to declare them. 🍪

This would allow you to re-use the model in multiple places and also to declare validations and metadata for all the parameters at once. 😎

This is supported since FastAPI version 0.115.0. 🤓

This same technique applies to Query, Cookie, and Header. 😎

Declare the cookie parameters that you need in a Pydantic model, and then declare the parameter as Cookie:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

FastAPI will extract the data for each field from the cookies received in the request and give you the Pydantic model you defined.

You can see the defined cookies in the docs UI at /docs:

Have in mind that, as browsers handle cookies in special ways and behind the scenes, they don't easily allow JavaScript to touch them.

If you go to the API docs UI at /docs you will be able to see the documentation for cookies for your path operations.

But even if you fill the data and click "Execute", because the docs UI works with JavaScript, the cookies won't be sent, and you will see an error message as if you didn't write any values.

In some special use cases (probably not very common), you might want to restrict the cookies that you want to receive.

Your API now has the power to control its own cookie consent. 🤪🍪

You can use Pydantic's model configuration to forbid any extra fields:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

If a client tries to send some extra cookies, they will receive an error response.

Poor cookie banners with all their effort to get your consent for the API to reject it. 🍪

For example, if the client tries to send a santa_tracker cookie with a value of good-list-please, the client will receive an error response telling them that the santa_tracker cookie is not allowed:

You can use Pydantic models to declare cookies in FastAPI. 😎

**Examples:**

Example 1 (python):
```python
from typing import Annotated

from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None


@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies
```

Example 2 (python):
```python
from typing import Annotated, Union

from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: Union[str, None] = None
    googall_tracker: Union[str, None] = None


@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies
```

Example 3 (python):
```python
from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None


@app.get("/items/")
async def read_items(cookies: Cookies = Cookie()):
    return cookies
```

Example 4 (python):
```python
from typing import Union

from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: Union[str, None] = None
    googall_tracker: Union[str, None] = None


@app.get("/items/")
async def read_items(cookies: Cookies = Cookie()):
    return cookies
```

---

## Behind a Proxy¶

**URL:** https://fastapi.tiangolo.com/advanced/behind-a-proxy/

**Contents:**
- Behind a Proxy¶
- Proxy Forwarded Headers¶
  - Enable Proxy Forwarded Headers¶
  - Redirects with HTTPS¶
  - How Proxy Forwarded Headers Work¶
- Proxy with a stripped path prefix¶
  - Providing the root_path¶
  - Checking the current root_path¶
  - Setting the root_path in the FastAPI app¶
  - About root_path¶

In many situations, you would use a proxy like Traefik or Nginx in front of your FastAPI app.

These proxies could handle HTTPS certificates and other things.

A proxy in front of your application would normally set some headers on the fly before sending the requests to your server to let the server know that the request was forwarded by the proxy, letting it know the original (public) URL, including the domain, that it is using HTTPS, etc.

The server program (for example Uvicorn via FastAPI CLI) is capable of interpreting these headers, and then passing that information to your application.

But for security, as the server doesn't know it is behind a trusted proxy, it won't interpret those headers.

The proxy headers are:

You can start FastAPI CLI with the CLI Option --forwarded-allow-ips and pass the IP addresses that should be trusted to read those forwarded headers.

If you set it to --forwarded-allow-ips="*" it would trust all the incoming IPs.

If your server is behind a trusted proxy and only the proxy talks to it, this would make it accept whatever is the IP of that proxy.

For example, let's say you define a path operation /items/:

If the client tries to go to /items, by default, it would be redirected to /items/.

But before setting the CLI Option --forwarded-allow-ips it could redirect to http://localhost:8000/items/.

But maybe your application is hosted at https://mysuperapp.com, and the redirection should be to https://mysuperapp.com/items/.

By setting --proxy-headers now FastAPI would be able to redirect to the right location. 😎

If you want to learn more about HTTPS, check the guide About HTTPS.

Here's a visual representation of how the proxy adds forwarded headers between the client and the application server:

The proxy intercepts the original client request and adds the special forwarded headers (X-Forwarded-*) before passing the request to the application server.

These headers preserve information about the original request that would otherwise be lost:

When FastAPI CLI is configured with --forwarded-allow-ips, it trusts these headers and uses them, for example to generate the correct URLs in redirects.

You could have a proxy that adds a path prefix to your application.

In these cases you can use root_path to configure your application.

The root_path is a mechanism provided by the ASGI specification (that FastAPI is built on, through Starlette).

The root_path is used to handle these specific cases.

And it's also used internally when mounting sub-applications.

Having a proxy with a stripped path prefix, in this case, means that you could declare a path at /app in your code, but then, you add a layer on top (the proxy) that would put your FastAPI application under a path like /api/v1.

In this case, the original path /app would actually be served at /api/v1/app.

Even though all your code is written assuming there's just /app.

And the proxy would be "stripping" the path prefix on the fly before transmitting the request to the app server (probably Uvicorn via FastAPI CLI), keeping your application convinced that it is being served at /app, so that you don't have to update all your code to include the prefix /api/v1.

Up to here, everything would work as normally.

But then, when you open the integrated docs UI (the frontend), it would expect to get the OpenAPI schema at /openapi.json, instead of /api/v1/openapi.json.

So, the frontend (that runs in the browser) would try to reach /openapi.json and wouldn't be able to get the OpenAPI schema.

Because we have a proxy with a path prefix of /api/v1 for our app, the frontend needs to fetch the OpenAPI schema at /api/v1/openapi.json.

The IP 0.0.0.0 is commonly used to mean that the program listens on all the IPs available in that machine/server.

The docs UI would also need the OpenAPI schema to declare that this API server is located at /api/v1 (behind the proxy). For example:

In this example, the "Proxy" could be something like Traefik. And the server would be something like FastAPI CLI with Uvicorn, running your FastAPI application.

To achieve this, you can use the command line option --root-path like:

If you use Hypercorn, it also has the option --root-path.

The ASGI specification defines a root_path for this use case.

And the --root-path command line option provides that root_path.

You can get the current root_path used by your application for each request, it is part of the scope dictionary (that's part of the ASGI spec).

Here we are including it in the message just for demonstration purposes.

Then, if you start Uvicorn with:

The response would be something like:

Alternatively, if you don't have a way to provide a command line option like --root-path or equivalent, you can set the root_path parameter when creating your FastAPI app:

Passing the root_path to FastAPI would be the equivalent of passing the --root-path command line option to Uvicorn or Hypercorn.

Keep in mind that the server (Uvicorn) won't use that root_path for anything else than passing it to the app.

But if you go with your browser to http://127.0.0.1:8000/app you will see the normal response:

So, it won't expect to be accessed at http://127.0.0.1:8000/api/v1/app.

Uvicorn will expect the proxy to access Uvicorn at http://127.0.0.1:8000/app, and then it would be the proxy's responsibility to add the extra /api/v1 prefix on top.

Keep in mind that a proxy with stripped path prefix is only one of the ways to configure it.

Probably in many cases the default will be that the proxy doesn't have a stripped path prefix.

In a case like that (without a stripped path prefix), the proxy would listen on something like https://myawesomeapp.com, and then if the browser goes to https://myawesomeapp.com/api/v1/app and your server (e.g. Uvicorn) listens on http://127.0.0.1:8000 the proxy (without a stripped path prefix) would access Uvicorn at the same path: http://127.0.0.1:8000/api/v1/app.

You can easily run the experiment locally with a stripped path prefix using Traefik.

Download Traefik, it's a single binary, you can extract the compressed file and run it directly from the terminal.

Then create a file traefik.toml with:

This tells Traefik to listen on port 9999 and to use another file routes.toml.

We are using port 9999 instead of the standard HTTP port 80 so that you don't have to run it with admin (sudo) privileges.

Now create that other file routes.toml:

This file configures Traefik to use the path prefix /api/v1.

And then Traefik will redirect its requests to your Uvicorn running on http://127.0.0.1:8000.

And now start your app, using the --root-path option:

Now, if you go to the URL with the port for Uvicorn: http://127.0.0.1:8000/app, you will see the normal response:

Notice that even though you are accessing it at http://127.0.0.1:8000/app it shows the root_path of /api/v1, taken from the option --root-path.

And now open the URL with the port for Traefik, including the path prefix: http://127.0.0.1:9999/api/v1/app.

We get the same response:

but this time at the URL with the prefix path provided by the proxy: /api/v1.

Of course, the idea here is that everyone would access the app through the proxy, so the version with the path prefix /api/v1 is the "correct" one.

And the version without the path prefix (http://127.0.0.1:8000/app), provided by Uvicorn directly, would be exclusively for the proxy (Traefik) to access it.

That demonstrates how the Proxy (Traefik) uses the path prefix and how the server (Uvicorn) uses the root_path from the option --root-path.

But here's the fun part. ✨

The "official" way to access the app would be through the proxy with the path prefix that we defined. So, as we would expect, if you try the docs UI served by Uvicorn directly, without the path prefix in the URL, it won't work, because it expects to be accessed through the proxy.

You can check it at http://127.0.0.1:8000/docs:

But if we access the docs UI at the "official" URL using the proxy with port 9999, at /api/v1/docs, it works correctly! 🎉

You can check it at http://127.0.0.1:9999/api/v1/docs:

Right as we wanted it. ✔️

This is because FastAPI uses this root_path to create the default server in OpenAPI with the URL provided by root_path.

This is a more advanced use case. Feel free to skip it.

By default, FastAPI will create a server in the OpenAPI schema with the URL for the root_path.

But you can also provide other alternative servers, for example if you want the same docs UI to interact with both a staging and a production environment.

If you pass a custom list of servers and there's a root_path (because your API lives behind a proxy), FastAPI will insert a "server" with this root_path at the beginning of the list.

Will generate an OpenAPI schema like:

Notice the auto-generated server with a url value of /api/v1, taken from the root_path.

In the docs UI at http://127.0.0.1:9999/api/v1/docs it would look like:

The docs UI will interact with the server that you select.

The servers property in the OpenAPI specification is optional.

If you don't specify the servers parameter and root_path is equal to /, the servers property in the generated OpenAPI schema will be omitted entirely by default, which is the equivalent of a single server with a url value of /.

If you don't want FastAPI to include an automatic server using the root_path, you can use the parameter root_path_in_servers=False:

and then it won't include it in the OpenAPI schema.

If you need to mount a sub-application (as described in Sub Applications - Mounts) while also using a proxy with root_path, you can do it normally, as you would expect.

FastAPI will internally use the root_path smartly, so it will just work. ✨

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/")
def read_items():
    return ["plumbus", "portal gun"]
```

Example 2 (yaml):
```yaml
https://mysuperapp.com/items/
```

Example 3 (python):
```python
from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}
```

Example 4 (json):
```json
{
    "openapi": "3.1.0",
    // More stuff here
    "servers": [
        {
            "url": "/api/v1"
        }
    ],
    "paths": {
            // More stuff here
    }
}
```

---

## Handling Errors¶

**URL:** https://fastapi.tiangolo.com/tutorial/handling-errors/

**Contents:**
- Handling Errors¶
- Use HTTPException¶
  - Import HTTPException¶
  - Raise an HTTPException in your code¶
  - The resulting response¶
- Add custom headers¶
- Install custom exception handlers¶
- Override the default exception handlers¶
  - Override request validation exceptions¶
  - Override the HTTPException error handler¶

There are many situations in which you need to notify an error to a client that is using your API.

This client could be a browser with a frontend, a code from someone else, an IoT device, etc.

You could need to tell the client that:

In these cases, you would normally return an HTTP status code in the range of 400 (from 400 to 499).

This is similar to the 200 HTTP status codes (from 200 to 299). Those "200" status codes mean that somehow there was a "success" in the request.

The status codes in the 400 range mean that there was an error from the client.

Remember all those "404 Not Found" errors (and jokes)?

To return HTTP responses with errors to the client you use HTTPException.

HTTPException is a normal Python exception with additional data relevant for APIs.

Because it's a Python exception, you don't return it, you raise it.

This also means that if you are inside a utility function that you are calling inside of your path operation function, and you raise the HTTPException from inside of that utility function, it won't run the rest of the code in the path operation function, it will terminate that request right away and send the HTTP error from the HTTPException to the client.

The benefit of raising an exception over returning a value will be more evident in the section about Dependencies and Security.

In this example, when the client requests an item by an ID that doesn't exist, raise an exception with a status code of 404:

If the client requests http://example.com/items/foo (an item_id "foo"), that client will receive an HTTP status code of 200, and a JSON response of:

But if the client requests http://example.com/items/bar (a non-existent item_id "bar"), that client will receive an HTTP status code of 404 (the "not found" error), and a JSON response of:

When raising an HTTPException, you can pass any value that can be converted to JSON as the parameter detail, not only str.

You could pass a dict, a list, etc.

They are handled automatically by FastAPI and converted to JSON.

There are some situations in where it's useful to be able to add custom headers to the HTTP error. For example, for some types of security.

You probably won't need to use it directly in your code.

But in case you needed it for an advanced scenario, you can add custom headers:

You can add custom exception handlers with the same exception utilities from Starlette.

Let's say you have a custom exception UnicornException that you (or a library you use) might raise.

And you want to handle this exception globally with FastAPI.

You could add a custom exception handler with @app.exception_handler():

Here, if you request /unicorns/yolo, the path operation will raise a UnicornException.

But it will be handled by the unicorn_exception_handler.

So, you will receive a clean error, with an HTTP status code of 418 and a JSON content of:

You could also use from starlette.requests import Request and from starlette.responses import JSONResponse.

FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette. The same with Request.

FastAPI has some default exception handlers.

These handlers are in charge of returning the default JSON responses when you raise an HTTPException and when the request has invalid data.

You can override these exception handlers with your own.

When a request contains invalid data, FastAPI internally raises a RequestValidationError.

And it also includes a default exception handler for it.

To override it, import the RequestValidationError and use it with @app.exception_handler(RequestValidationError) to decorate the exception handler.

The exception handler will receive a Request and the exception.

Now, if you go to /items/foo, instead of getting the default JSON error with:

you will get a text version, with:

The same way, you can override the HTTPException handler.

For example, you could want to return a plain text response instead of JSON for these errors:

You could also use from starlette.responses import PlainTextResponse.

FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette.

Have in mind that the RequestValidationError contains the information of the file name and line where the validation error happens so that you can show it in your logs with the relevant information if you want to.

But that means that if you just convert it to a string and return that information directly, you could be leaking a bit of information about your system, that's why here the code extracts and shows each error independently.

The RequestValidationError contains the body it received with invalid data.

You could use it while developing your app to log the body and debug it, return it to the user, etc.

Now try sending an invalid item like:

You will receive a response telling you that the data is invalid containing the received body:

FastAPI has its own HTTPException.

And FastAPI's HTTPException error class inherits from Starlette's HTTPException error class.

The only difference is that FastAPI's HTTPException accepts any JSON-able data for the detail field, while Starlette's HTTPException only accepts strings for it.

So, you can keep raising FastAPI's HTTPException as normally in your code.

But when you register an exception handler, you should register it for Starlette's HTTPException.

This way, if any part of Starlette's internal code, or a Starlette extension or plug-in, raises a Starlette HTTPException, your handler will be able to catch and handle it.

In this example, to be able to have both HTTPExceptions in the same code, Starlette's exceptions is renamed to StarletteHTTPException:

If you want to use the exception along with the same default exception handlers from FastAPI, you can import and reuse the default exception handlers from fastapi.exception_handlers:

In this example you are just printing the error with a very expressive message, but you get the idea. You can use the exception and then just reuse the default exception handlers.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```

Example 2 (python):
```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```

Example 3 (json):
```json
{
  "item": "The Foo Wrestlers"
}
```

Example 4 (json):
```json
{
  "detail": "Item not found"
}
```

---

## Deploy FastAPI on Cloud Providers¶

**URL:** https://fastapi.tiangolo.com/deployment/cloud/

**Contents:**
- Deploy FastAPI on Cloud Providers¶
- FastAPI Cloud¶
- Cloud Providers - Sponsors¶

You can use virtually any cloud provider to deploy your FastAPI application.

In most of the cases, the main cloud providers have guides to deploy FastAPI with them.

FastAPI Cloud is built by the same author and team behind FastAPI.

It streamlines the process of building, deploying, and accessing an API with minimal effort.

It brings the same developer experience of building apps with FastAPI to deploying them to the cloud. 🎉

FastAPI Cloud is the primary sponsor and funding provider for the FastAPI and friends open source projects. ✨

Some other cloud providers ✨ sponsor FastAPI ✨ too. 🙇

You might also want to consider them to follow their guides and try their services:

---

## APIRouter class¶

**URL:** https://fastapi.tiangolo.com/reference/apirouter/

**Contents:**
- APIRouter class¶
- fastapi.APIRouter ¶
    - Example¶
  - websocket ¶
      - Example¶
  - include_router ¶
      - Example¶
  - get ¶
      - Example¶
  - put ¶

Here's the reference information for the APIRouter class, with all its parameters, attributes and methods.

You can import the APIRouter class directly from fastapi:

APIRouter class, used to group path operations, for example to structure an app in multiple files. It would then be included in the FastAPI app, or in another APIRouter (ultimately included in the app).

Read more about it in the FastAPI docs for Bigger Applications - Multiple Files.

An optional path prefix for the router.

TYPE: str DEFAULT: ''

A list of tags to be applied to all the path operations in this router.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[list[Union[str, Enum]]] DEFAULT: None

A list of dependencies (using Depends()) to be applied to all the path operations in this router.

Read more about it in the FastAPI docs for Bigger Applications - Multiple Files.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

The default response class to be used.

Read more in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: type[Response] DEFAULT: Default(JSONResponse)

Additional responses to be shown in OpenAPI.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Additional Responses in OpenAPI.

And in the FastAPI docs for Bigger Applications.

TYPE: Optional[dict[Union[int, str], dict[str, Any]]] DEFAULT: None

OpenAPI callbacks that should apply to all path operations in this router.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

Note: you probably shouldn't use this parameter, it is inherited from Starlette and supported for compatibility.

A list of routes to serve incoming HTTP and WebSocket requests.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

Whether to detect and redirect slashes in URLs when the client doesn't use the same format.

TYPE: bool DEFAULT: True

Default function handler for this router. Used to handle 404 Not Found errors.

TYPE: Optional[ASGIApp] DEFAULT: None

Only used internally by FastAPI to handle dependency overrides.

You shouldn't need to use it. It normally points to the FastAPI app object.

TYPE: Optional[Any] DEFAULT: None

Custom route (path operation) class to be used by this router.

Read more about it in the FastAPI docs for Custom Request and APIRoute class.

TYPE: type[APIRoute] DEFAULT: APIRoute

A list of startup event handler functions.

You should instead use the lifespan handlers.

Read more in the FastAPI docs for lifespan.

TYPE: Optional[Sequence[Callable[[], Any]]] DEFAULT: None

A list of shutdown event handler functions.

You should instead use the lifespan handlers.

Read more in the FastAPI docs for lifespan.

TYPE: Optional[Sequence[Callable[[], Any]]] DEFAULT: None

A Lifespan context manager handler. This replaces startup and shutdown functions with a single context manager.

Read more in the FastAPI docs for lifespan.

TYPE: Optional[Lifespan[Any]] DEFAULT: None

Mark all path operations in this router as deprecated.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[bool] DEFAULT: None

To include (or not) all the path operations in this router in the generated OpenAPI.

This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: bool DEFAULT: True

Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.

This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str] DEFAULT: Default(generate_unique_id)

Decorate a WebSocket function.

Read more about it in the FastAPI docs for WebSockets.

A name for the WebSocket. Only used internally.

TYPE: Optional[str] DEFAULT: None

A list of dependencies (using Depends()) to be used for this WebSocket.

Read more about it in the FastAPI docs for WebSockets.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

Include another APIRouter in the same current APIRouter.

Read more about it in the FastAPI docs for Bigger Applications.

The APIRouter to include.

An optional path prefix for the router.

TYPE: str DEFAULT: ''

A list of tags to be applied to all the path operations in this router.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[list[Union[str, Enum]]] DEFAULT: None

A list of dependencies (using Depends()) to be applied to all the path operations in this router.

Read more about it in the FastAPI docs for Bigger Applications - Multiple Files.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

The default response class to be used.

Read more in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: type[Response] DEFAULT: Default(JSONResponse)

Additional responses to be shown in OpenAPI.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Additional Responses in OpenAPI.

And in the FastAPI docs for Bigger Applications.

TYPE: Optional[dict[Union[int, str], dict[str, Any]]] DEFAULT: None

OpenAPI callbacks that should apply to all path operations in this router.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

Mark all path operations in this router as deprecated.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[bool] DEFAULT: None

Include (or not) all the path operations in this router in the generated OpenAPI schema.

This affects the generated OpenAPI (e.g. visible at /docs).

TYPE: bool DEFAULT: True

Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.

This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str] DEFAULT: Default(generate_unique_id)

Add a path operation using an HTTP GET operation.

The URL path to be used for this path operation.

For example, in http://example.com/items, the path is /items.

The type to use for the response.

It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

Read more about it in the FastAPI docs for Response Model.

TYPE: Any DEFAULT: Default(None)

The default status code to be used for the response.

You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int] DEFAULT: None

A list of tags to be applied to the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[list[Union[str, Enum]]] DEFAULT: None

A list of dependencies (using Depends()) to be applied to the path operation.

Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

A summary for the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

A description for the path operation.

If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

The description for the default response.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: str DEFAULT: 'Successful Response'

Additional responses that could be returned by this path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[dict[Union[int, str], dict[str, Any]]] DEFAULT: None

Mark this path operation as deprecated.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool] DEFAULT: None

Custom operation ID to be used by this path operation.

By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str] DEFAULT: None

Configuration passed to Pydantic to include only certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to exclude certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: True

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should exclude fields set to None.

This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Include this path operation in the generated OpenAPI schema.

This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: bool DEFAULT: True

Response class to be used for this path operation.

This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: type[Response] DEFAULT: Default(JSONResponse)

Name for this path operation. Only used internally.

TYPE: Optional[str] DEFAULT: None

List of path operations that will be used as OpenAPI callbacks.

This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

Extra metadata to be included in the OpenAPI schema for this path operation.

Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[dict[str, Any]] DEFAULT: None

Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.

This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str] DEFAULT: Default(generate_unique_id)

Add a path operation using an HTTP PUT operation.

The URL path to be used for this path operation.

For example, in http://example.com/items, the path is /items.

The type to use for the response.

It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

Read more about it in the FastAPI docs for Response Model.

TYPE: Any DEFAULT: Default(None)

The default status code to be used for the response.

You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int] DEFAULT: None

A list of tags to be applied to the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[list[Union[str, Enum]]] DEFAULT: None

A list of dependencies (using Depends()) to be applied to the path operation.

Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

A summary for the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

A description for the path operation.

If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

The description for the default response.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: str DEFAULT: 'Successful Response'

Additional responses that could be returned by this path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[dict[Union[int, str], dict[str, Any]]] DEFAULT: None

Mark this path operation as deprecated.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool] DEFAULT: None

Custom operation ID to be used by this path operation.

By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str] DEFAULT: None

Configuration passed to Pydantic to include only certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to exclude certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: True

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should exclude fields set to None.

This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Include this path operation in the generated OpenAPI schema.

This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: bool DEFAULT: True

Response class to be used for this path operation.

This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: type[Response] DEFAULT: Default(JSONResponse)

Name for this path operation. Only used internally.

TYPE: Optional[str] DEFAULT: None

List of path operations that will be used as OpenAPI callbacks.

This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

Extra metadata to be included in the OpenAPI schema for this path operation.

Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[dict[str, Any]] DEFAULT: None

Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.

This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str] DEFAULT: Default(generate_unique_id)

Add a path operation using an HTTP POST operation.

The URL path to be used for this path operation.

For example, in http://example.com/items, the path is /items.

The type to use for the response.

It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

Read more about it in the FastAPI docs for Response Model.

TYPE: Any DEFAULT: Default(None)

The default status code to be used for the response.

You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int] DEFAULT: None

A list of tags to be applied to the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[list[Union[str, Enum]]] DEFAULT: None

A list of dependencies (using Depends()) to be applied to the path operation.

Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

A summary for the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

A description for the path operation.

If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

The description for the default response.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: str DEFAULT: 'Successful Response'

Additional responses that could be returned by this path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[dict[Union[int, str], dict[str, Any]]] DEFAULT: None

Mark this path operation as deprecated.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool] DEFAULT: None

Custom operation ID to be used by this path operation.

By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str] DEFAULT: None

Configuration passed to Pydantic to include only certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to exclude certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: True

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should exclude fields set to None.

This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Include this path operation in the generated OpenAPI schema.

This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: bool DEFAULT: True

Response class to be used for this path operation.

This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: type[Response] DEFAULT: Default(JSONResponse)

Name for this path operation. Only used internally.

TYPE: Optional[str] DEFAULT: None

List of path operations that will be used as OpenAPI callbacks.

This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

Extra metadata to be included in the OpenAPI schema for this path operation.

Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[dict[str, Any]] DEFAULT: None

Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.

This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str] DEFAULT: Default(generate_unique_id)

Add a path operation using an HTTP DELETE operation.

The URL path to be used for this path operation.

For example, in http://example.com/items, the path is /items.

The type to use for the response.

It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

Read more about it in the FastAPI docs for Response Model.

TYPE: Any DEFAULT: Default(None)

The default status code to be used for the response.

You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int] DEFAULT: None

A list of tags to be applied to the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[list[Union[str, Enum]]] DEFAULT: None

A list of dependencies (using Depends()) to be applied to the path operation.

Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

A summary for the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

A description for the path operation.

If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

The description for the default response.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: str DEFAULT: 'Successful Response'

Additional responses that could be returned by this path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[dict[Union[int, str], dict[str, Any]]] DEFAULT: None

Mark this path operation as deprecated.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool] DEFAULT: None

Custom operation ID to be used by this path operation.

By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str] DEFAULT: None

Configuration passed to Pydantic to include only certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to exclude certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: True

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should exclude fields set to None.

This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Include this path operation in the generated OpenAPI schema.

This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: bool DEFAULT: True

Response class to be used for this path operation.

This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: type[Response] DEFAULT: Default(JSONResponse)

Name for this path operation. Only used internally.

TYPE: Optional[str] DEFAULT: None

List of path operations that will be used as OpenAPI callbacks.

This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

Extra metadata to be included in the OpenAPI schema for this path operation.

Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[dict[str, Any]] DEFAULT: None

Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.

This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str] DEFAULT: Default(generate_unique_id)

Add a path operation using an HTTP OPTIONS operation.

The URL path to be used for this path operation.

For example, in http://example.com/items, the path is /items.

The type to use for the response.

It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

Read more about it in the FastAPI docs for Response Model.

TYPE: Any DEFAULT: Default(None)

The default status code to be used for the response.

You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int] DEFAULT: None

A list of tags to be applied to the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[list[Union[str, Enum]]] DEFAULT: None

A list of dependencies (using Depends()) to be applied to the path operation.

Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

A summary for the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

A description for the path operation.

If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

The description for the default response.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: str DEFAULT: 'Successful Response'

Additional responses that could be returned by this path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[dict[Union[int, str], dict[str, Any]]] DEFAULT: None

Mark this path operation as deprecated.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool] DEFAULT: None

Custom operation ID to be used by this path operation.

By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str] DEFAULT: None

Configuration passed to Pydantic to include only certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to exclude certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: True

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should exclude fields set to None.

This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Include this path operation in the generated OpenAPI schema.

This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: bool DEFAULT: True

Response class to be used for this path operation.

This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: type[Response] DEFAULT: Default(JSONResponse)

Name for this path operation. Only used internally.

TYPE: Optional[str] DEFAULT: None

List of path operations that will be used as OpenAPI callbacks.

This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

Extra metadata to be included in the OpenAPI schema for this path operation.

Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[dict[str, Any]] DEFAULT: None

Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.

This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str] DEFAULT: Default(generate_unique_id)

Add a path operation using an HTTP HEAD operation.

The URL path to be used for this path operation.

For example, in http://example.com/items, the path is /items.

The type to use for the response.

It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

Read more about it in the FastAPI docs for Response Model.

TYPE: Any DEFAULT: Default(None)

The default status code to be used for the response.

You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int] DEFAULT: None

A list of tags to be applied to the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[list[Union[str, Enum]]] DEFAULT: None

A list of dependencies (using Depends()) to be applied to the path operation.

Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

A summary for the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

A description for the path operation.

If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

The description for the default response.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: str DEFAULT: 'Successful Response'

Additional responses that could be returned by this path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[dict[Union[int, str], dict[str, Any]]] DEFAULT: None

Mark this path operation as deprecated.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool] DEFAULT: None

Custom operation ID to be used by this path operation.

By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str] DEFAULT: None

Configuration passed to Pydantic to include only certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to exclude certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: True

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should exclude fields set to None.

This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Include this path operation in the generated OpenAPI schema.

This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: bool DEFAULT: True

Response class to be used for this path operation.

This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: type[Response] DEFAULT: Default(JSONResponse)

Name for this path operation. Only used internally.

TYPE: Optional[str] DEFAULT: None

List of path operations that will be used as OpenAPI callbacks.

This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

Extra metadata to be included in the OpenAPI schema for this path operation.

Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[dict[str, Any]] DEFAULT: None

Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.

This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str] DEFAULT: Default(generate_unique_id)

Add a path operation using an HTTP PATCH operation.

The URL path to be used for this path operation.

For example, in http://example.com/items, the path is /items.

The type to use for the response.

It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

Read more about it in the FastAPI docs for Response Model.

TYPE: Any DEFAULT: Default(None)

The default status code to be used for the response.

You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int] DEFAULT: None

A list of tags to be applied to the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[list[Union[str, Enum]]] DEFAULT: None

A list of dependencies (using Depends()) to be applied to the path operation.

Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

A summary for the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

A description for the path operation.

If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

The description for the default response.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: str DEFAULT: 'Successful Response'

Additional responses that could be returned by this path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[dict[Union[int, str], dict[str, Any]]] DEFAULT: None

Mark this path operation as deprecated.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool] DEFAULT: None

Custom operation ID to be used by this path operation.

By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str] DEFAULT: None

Configuration passed to Pydantic to include only certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to exclude certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: True

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should exclude fields set to None.

This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Include this path operation in the generated OpenAPI schema.

This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: bool DEFAULT: True

Response class to be used for this path operation.

This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: type[Response] DEFAULT: Default(JSONResponse)

Name for this path operation. Only used internally.

TYPE: Optional[str] DEFAULT: None

List of path operations that will be used as OpenAPI callbacks.

This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

Extra metadata to be included in the OpenAPI schema for this path operation.

Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[dict[str, Any]] DEFAULT: None

Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.

This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str] DEFAULT: Default(generate_unique_id)

Add a path operation using an HTTP TRACE operation.

The URL path to be used for this path operation.

For example, in http://example.com/items, the path is /items.

The type to use for the response.

It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

Read more about it in the FastAPI docs for Response Model.

TYPE: Any DEFAULT: Default(None)

The default status code to be used for the response.

You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int] DEFAULT: None

A list of tags to be applied to the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[list[Union[str, Enum]]] DEFAULT: None

A list of dependencies (using Depends()) to be applied to the path operation.

Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

A summary for the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

A description for the path operation.

If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

The description for the default response.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: str DEFAULT: 'Successful Response'

Additional responses that could be returned by this path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[dict[Union[int, str], dict[str, Any]]] DEFAULT: None

Mark this path operation as deprecated.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool] DEFAULT: None

Custom operation ID to be used by this path operation.

By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str] DEFAULT: None

Configuration passed to Pydantic to include only certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to exclude certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: True

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should exclude fields set to None.

This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Include this path operation in the generated OpenAPI schema.

This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: bool DEFAULT: True

Response class to be used for this path operation.

This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: type[Response] DEFAULT: Default(JSONResponse)

Name for this path operation. Only used internally.

TYPE: Optional[str] DEFAULT: None

List of path operations that will be used as OpenAPI callbacks.

This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

Extra metadata to be included in the OpenAPI schema for this path operation.

Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[dict[str, Any]] DEFAULT: None

Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.

This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str] DEFAULT: Default(generate_unique_id)

Add an event handler for the router.

on_event is deprecated, use lifespan event handlers instead.

Read more about it in the FastAPI docs for Lifespan Events.

The type of event. startup or shutdown.

**Examples:**

Example 1 (python):
```python
from fastapi import APIRouter
```

Example 2 (rust):
```rust
APIRouter(
    *,
    prefix="",
    tags=None,
    dependencies=None,
    default_response_class=Default(JSONResponse),
    responses=None,
    callbacks=None,
    routes=None,
    redirect_slashes=True,
    default=None,
    dependency_overrides_provider=None,
    route_class=APIRoute,
    on_startup=None,
    on_shutdown=None,
    lifespan=None,
    deprecated=None,
    include_in_schema=True,
    generate_unique_id_function=Default(generate_unique_id)
)
```

Example 3 (python):
```python
from fastapi import APIRouter, FastAPI

app = FastAPI()
router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


app.include_router(router)
```

Example 4 (python):
```python
def __init__(
    self,
    *,
    prefix: Annotated[str, Doc("An optional path prefix for the router.")] = "",
    tags: Annotated[
        Optional[list[Union[str, Enum]]],
        Doc(
            """
            A list of tags to be applied to all the *path operations* in this
            router.

            It will be added to the generated OpenAPI (e.g. visible at `/docs`).

            Read more about it in the
            [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
            """
        ),
    ] = None,
    dependencies: Annotated[
        Optional[Sequence[params.Depends]],
        Doc(
            """
            A list of dependencies (using `Depends()`) to be applied to all the
            *path operations* in this router.

            Read more about it in the
            [FastAPI docs for Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies).
            """
        ),
    ] = None,
    default_response_class: Annotated[
        type[Response],
        Doc(
            """
            The default response class to be used.

            Read more in the
            [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class).
            """
        ),
    ] = Default(JSONResponse),
    responses: Annotated[
        Optional[dict[Union[int, str], dict[str, Any]]],
        Doc(
            """
            Additional responses to be shown in OpenAPI.

            It will be added to the generated OpenAPI (e.g. visible at `/docs`).

            Read more about it in the
            [FastAPI docs for Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/).

            And in the
            [FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies).
            """
        ),
    ] = None,
    callbacks: Annotated[
        Optional[list[BaseRoute]],
        Doc(
            """
            OpenAPI callbacks that should apply to all *path operations* in this
            router.

            It will be added to the generated OpenAPI (e.g. visible at `/docs`).

            Read more about it in the
            [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
            """
        ),
    ] = None,
    routes: Annotated[
        Optional[list[BaseRoute]],
        Doc(
            """
            **Note**: you probably shouldn't use this parameter, it is inherited
            from Starlette and supported for compatibility.

            ---

            A list of routes to serve incoming HTTP and WebSocket requests.
            """
        ),
        deprecated(
            """
            You normally wouldn't use this parameter with FastAPI, it is inherited
            from Starlette and supported for compatibility.

            In FastAPI, you normally would use the *path operation methods*,
            like `router.get()`, `router.post()`, etc.
            """
        ),
    ] = None,
    redirect_slashes: Annotated[
        bool,
        Doc(
            """
            Whether to detect and redirect slashes in URLs when the client doesn't
            use the same format.
            """
        ),
    ] = True,
    default: Annotated[
        Optional[ASGIApp],
        Doc(
            """
            Default function handler for this router. Used to handle
            404 Not Found errors.
            """
        ),
    ] = None,
    dependency_overrides_provider: Annotated[
        Optional[Any],
        Doc(
            """
            Only used internally by FastAPI to handle dependency overrides.

            You shouldn't need to use it. It normally points to the `FastAPI` app
            object.
            """
        ),
    ] = None,
    route_class: Annotated[
        type[APIRoute],
        Doc(
            """
            Custom route (*path operation*) class to be used by this router.

            Read more about it in the
            [FastAPI docs for Custom Request and APIRoute class](https://fastapi.tiangolo.com/how-to/custom-request-and-route/#custom-apiroute-class-in-a-router).
            """
        ),
    ] = APIRoute,
    on_startup: Annotated[
        Optional[Sequence[Callable[[], Any]]],
        Doc(
            """
            A list of startup event handler functions.

            You should instead use the `lifespan` handlers.

            Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
            """
        ),
    ] = None,
    on_shutdown: Annotated[
        Optional[Sequence[Callable[[], Any]]],
        Doc(
            """
            A list of shutdown event handler functions.

            You should instead use the `lifespan` handlers.

            Read more in the
            [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
            """
        ),
    ] = None,
    # the generic to Lifespan[AppType] is the type of the top level application
    # which the router cannot know statically, so we use typing.Any
    lifespan: Annotated[
        Optional[Lifespan[Any]],
        Doc(
            """
            A `Lifespan` context manager handler. This replaces `startup` and
            `shutdown` functions with a single context manager.

            Read more in the
            [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
            """
        ),
    ] = None,
    deprecated: Annotated[
        Optional[bool],
        Doc(
            """
            Mark all *path operations* in this router as deprecated.

            It will be added to the generated OpenAPI (e.g. visible at `/docs`).

            Read more about it in the
            [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
            """
        ),
    ] = None,
    include_in_schema: Annotated[
        bool,
        Doc(
            """
            To include (or not) all the *path operations* in this router in the
            generated OpenAPI.

            This affects the generated OpenAPI (e.g. visible at `/docs`).

            Read more about it in the
            [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi).
            """
        ),
    ] = True,
    generate_unique_id_function: Annotated[
        Callable[[APIRoute], str],
        Doc(
            """
            Customize the function used to generate unique IDs for the *path
            operations* shown in the generated OpenAPI.

            This is particularly useful when automatically generating clients or
            SDKs for your API.

            Read more about it in the
            [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
            """
        ),
    ] = Default(generate_unique_id),
) -> None:
    super().__init__(
        routes=routes,
        redirect_slashes=redirect_slashes,
        default=default,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        lifespan=lifespan,
    )
    if prefix:
        assert prefix.startswith("/"), "A path prefix must start with '/'"
        assert not prefix.endswith("/"), (
            "A path prefix must not end with '/', as the routes will start with '/'"
        )
    self.prefix = prefix
    self.tags: list[Union[str, Enum]] = tags or []
    self.dependencies = list(dependencies or [])
    self.deprecated = deprecated
    self.include_in_schema = include_in_schema
    self.responses = responses or {}
    self.callbacks = callbacks or []
    self.dependency_overrides_provider = dependency_overrides_provider
    self.route_class = route_class
    self.default_response_class = default_response_class
    self.generate_unique_id_function = generate_unique_id_function
```

---

## Bigger Applications - Multiple Files¶

**URL:** https://fastapi.tiangolo.com/tutorial/bigger-applications/

**Contents:**
- Bigger Applications - Multiple Files¶
- An example file structure¶
- APIRouter¶
  - Import APIRouter¶
  - Path operations with APIRouter¶
- Dependencies¶
- Another module with APIRouter¶
  - Import the dependencies¶
    - How relative imports work¶
  - Add some custom tags, responses, and dependencies¶

If you are building an application or a web API, it's rarely the case that you can put everything in a single file.

FastAPI provides a convenience tool to structure your application while keeping all the flexibility.

If you come from Flask, this would be the equivalent of Flask's Blueprints.

Let's say you have a file structure like this:

There are several __init__.py files: one in each directory or subdirectory.

This is what allows importing code from one file into another.

For example, in app/main.py you could have a line like:

The same file structure with comments:

Let's say the file dedicated to handling just users is the submodule at /app/routers/users.py.

You want to have the path operations related to your users separated from the rest of the code, to keep it organized.

But it's still part of the same FastAPI application/web API (it's part of the same "Python Package").

You can create the path operations for that module using APIRouter.

You import it and create an "instance" the same way you would with the class FastAPI:

And then you use it to declare your path operations.

Use it the same way you would use the FastAPI class:

You can think of APIRouter as a "mini FastAPI" class.

All the same options are supported.

All the same parameters, responses, dependencies, tags, etc.

In this example, the variable is called router, but you can name it however you want.

We are going to include this APIRouter in the main FastAPI app, but first, let's check the dependencies and another APIRouter.

We see that we are going to need some dependencies used in several places of the application.

So we put them in their own dependencies module (app/dependencies.py).

We will now use a simple dependency to read a custom X-Token header:

Prefer to use the Annotated version if possible.

We are using an invented header to simplify this example.

But in real cases you will get better results using the integrated Security utilities.

Let's say you also have the endpoints dedicated to handling "items" from your application in the module at app/routers/items.py.

You have path operations for:

It's all the same structure as with app/routers/users.py.

But we want to be smarter and simplify the code a bit.

We know all the path operations in this module have the same:

So, instead of adding all that to each path operation, we can add it to the APIRouter.

As the path of each path operation has to start with /, like in:

...the prefix must not include a final /.

So, the prefix in this case is /items.

We can also add a list of tags and extra responses that will be applied to all the path operations included in this router.

And we can add a list of dependencies that will be added to all the path operations in the router and will be executed/solved for each request made to them.

Note that, much like dependencies in path operation decorators, no value will be passed to your path operation function.

The end result is that the item paths are now:

Having dependencies in the APIRouter can be used, for example, to require authentication for a whole group of path operations. Even if the dependencies are not added individually to each one of them.

The prefix, tags, responses, and dependencies parameters are (as in many other cases) just a feature from FastAPI to help you avoid code duplication.

This code lives in the module app.routers.items, the file app/routers/items.py.

And we need to get the dependency function from the module app.dependencies, the file app/dependencies.py.

So we use a relative import with .. for the dependencies:

If you know perfectly how imports work, continue to the next section below.

A single dot ., like in:

But that file doesn't exist, our dependencies are in a file at app/dependencies.py.

Remember how our app/file structure looks like:

The two dots .., like in:

That works correctly! 🎉

The same way, if we had used three dots ..., like in:

That would refer to some package above app/, with its own file __init__.py, etc. But we don't have that. So, that would throw an error in our example. 🚨

But now you know how it works, so you can use relative imports in your own apps no matter how complex they are. 🤓

We are not adding the prefix /items nor the tags=["items"] to each path operation because we added them to the APIRouter.

But we can still add more tags that will be applied to a specific path operation, and also some extra responses specific to that path operation:

This last path operation will have the combination of tags: ["items", "custom"].

And it will also have both responses in the documentation, one for 404 and one for 403.

Now, let's see the module at app/main.py.

Here's where you import and use the class FastAPI.

This will be the main file in your application that ties everything together.

And as most of your logic will now live in its own specific module, the main file will be quite simple.

You import and create a FastAPI class as normally.

And we can even declare global dependencies that will be combined with the dependencies for each APIRouter:

Prefer to use the Annotated version if possible.

Now we import the other submodules that have APIRouters:

Prefer to use the Annotated version if possible.

As the files app/routers/users.py and app/routers/items.py are submodules that are part of the same Python package app, we can use a single dot . to import them using "relative imports".

The module items will have a variable router (items.router). This is the same one we created in the file app/routers/items.py, it's an APIRouter object.

And then we do the same for the module users.

We could also import them like:

The first version is a "relative import":

The second version is an "absolute import":

To learn more about Python Packages and Modules, read the official Python documentation about Modules.

We are importing the submodule items directly, instead of importing just its variable router.

This is because we also have another variable named router in the submodule users.

If we had imported one after the other, like:

the router from users would overwrite the one from items and we wouldn't be able to use them at the same time.

So, to be able to use both of them in the same file, we import the submodules directly:

Prefer to use the Annotated version if possible.

Now, let's include the routers from the submodules users and items:

Prefer to use the Annotated version if possible.

users.router contains the APIRouter inside of the file app/routers/users.py.

And items.router contains the APIRouter inside of the file app/routers/items.py.

With app.include_router() we can add each APIRouter to the main FastAPI application.

It will include all the routes from that router as part of it.

It will actually internally create a path operation for each path operation that was declared in the APIRouter.

So, behind the scenes, it will actually work as if everything was the same single app.

You don't have to worry about performance when including routers.

This will take microseconds and will only happen at startup.

So it won't affect performance. ⚡

Now, let's imagine your organization gave you the app/internal/admin.py file.

It contains an APIRouter with some admin path operations that your organization shares between several projects.

For this example it will be super simple. But let's say that because it is shared with other projects in the organization, we cannot modify it and add a prefix, dependencies, tags, etc. directly to the APIRouter:

But we still want to set a custom prefix when including the APIRouter so that all its path operations start with /admin, we want to secure it with the dependencies we already have for this project, and we want to include tags and responses.

We can declare all that without having to modify the original APIRouter by passing those parameters to app.include_router():

Prefer to use the Annotated version if possible.

That way, the original APIRouter will stay unmodified, so we can still share that same app/internal/admin.py file with other projects in the organization.

The result is that in our app, each of the path operations from the admin module will have:

But that will only affect that APIRouter in our app, not in any other code that uses it.

So, for example, other projects could use the same APIRouter with a different authentication method.

We can also add path operations directly to the FastAPI app.

Here we do it... just to show that we can 🤷:

Prefer to use the Annotated version if possible.

and it will work correctly, together with all the other path operations added with app.include_router().

Very Technical Details

Note: this is a very technical detail that you probably can just skip.

The APIRouters are not "mounted", they are not isolated from the rest of the application.

This is because we want to include their path operations in the OpenAPI schema and the user interfaces.

As we cannot just isolate them and "mount" them independently of the rest, the path operations are "cloned" (re-created), not included directly.

And open the docs at http://127.0.0.1:8000/docs.

You will see the automatic API docs, including the paths from all the submodules, using the correct paths (and prefixes) and the correct tags:

You can also use .include_router() multiple times with the same router using different prefixes.

This could be useful, for example, to expose the same API under different prefixes, e.g. /api/v1 and /api/latest.

This is an advanced usage that you might not really need, but it's there in case you do.

The same way you can include an APIRouter in a FastAPI application, you can include an APIRouter in another APIRouter using:

Make sure you do it before including router in the FastAPI app, so that the path operations from other_router are also included.

**Examples:**

Example 1 (unknown):
```unknown
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```

Example 2 (sql):
```sql
from app.routers import items
```

Example 3 (python):
```python
.
├── app                  # "app" is a Python package
│   ├── __init__.py      # this file makes "app" a "Python package"
│   ├── main.py          # "main" module, e.g. import app.main
│   ├── dependencies.py  # "dependencies" module, e.g. import app.dependencies
│   └── routers          # "routers" is a "Python subpackage"
│   │   ├── __init__.py  # makes "routers" a "Python subpackage"
│   │   ├── items.py     # "items" submodule, e.g. import app.routers.items
│   │   └── users.py     # "users" submodule, e.g. import app.routers.users
│   └── internal         # "internal" is a "Python subpackage"
│       ├── __init__.py  # makes "internal" a "Python subpackage"
│       └── admin.py     # "admin" submodule, e.g. import app.internal.admin
```

Example 4 (python):
```python
from fastapi import APIRouter

router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
```

---

## Settings and Environment Variables¶

**URL:** https://fastapi.tiangolo.com/advanced/settings/

**Contents:**
- Settings and Environment Variables¶
- Types and validation¶
- Pydantic Settings¶
  - Install pydantic-settings¶
  - Create the Settings object¶
  - Use the settings¶
  - Run the server¶
- Settings in another module¶
- Settings in a dependency¶
  - The config file¶

In many cases your application could need some external settings or configurations, for example secret keys, database credentials, credentials for email services, etc.

Most of these settings are variable (can change), like database URLs. And many could be sensitive, like secrets.

For this reason it's common to provide them in environment variables that are read by the application.

To understand environment variables you can read Environment Variables.

These environment variables can only handle text strings, as they are external to Python and have to be compatible with other programs and the rest of the system (and even with different operating systems, as Linux, Windows, macOS).

That means that any value read in Python from an environment variable will be a str, and any conversion to a different type or any validation has to be done in code.

Fortunately, Pydantic provides a great utility to handle these settings coming from environment variables with Pydantic: Settings management.

First, make sure you create your virtual environment, activate it, and then install the pydantic-settings package:

It also comes included when you install the all extras with:

Import BaseSettings from Pydantic and create a sub-class, very much like with a Pydantic model.

The same way as with Pydantic models, you declare class attributes with type annotations, and possibly default values.

You can use all the same validation features and tools you use for Pydantic models, like different data types and additional validations with Field().

If you want something quick to copy and paste, don't use this example, use the last one below.

Then, when you create an instance of that Settings class (in this case, in the settings object), Pydantic will read the environment variables in a case-insensitive way, so, an upper-case variable APP_NAME will still be read for the attribute app_name.

Next it will convert and validate the data. So, when you use that settings object, you will have data of the types you declared (e.g. items_per_user will be an int).

Then you can use the new settings object in your application:

Next, you would run the server passing the configurations as environment variables, for example you could set an ADMIN_EMAIL and APP_NAME with:

To set multiple env vars for a single command just separate them with a space, and put them all before the command.

And then the admin_email setting would be set to "deadpool@example.com".

The app_name would be "ChimichangApp".

And the items_per_user would keep its default value of 50.

You could put those settings in another module file as you saw in Bigger Applications - Multiple Files.

For example, you could have a file config.py with:

And then use it in a file main.py:

You would also need a file __init__.py as you saw in Bigger Applications - Multiple Files.

In some occasions it might be useful to provide the settings from a dependency, instead of having a global object with settings that is used everywhere.

This could be especially useful during testing, as it's very easy to override a dependency with your own custom settings.

Coming from the previous example, your config.py file could look like:

Prefer to use the Annotated version if possible.

Notice that now we don't create a default instance settings = Settings().

Now we create a dependency that returns a new config.Settings().

Prefer to use the Annotated version if possible.

We'll discuss the @lru_cache in a bit.

For now you can assume get_settings() is a normal function.

And then we can require it from the path operation function as a dependency and use it anywhere we need it.

Prefer to use the Annotated version if possible.

Then it would be very easy to provide a different settings object during testing by creating a dependency override for get_settings:

Prefer to use the Annotated version if possible.

In the dependency override we set a new value for the admin_email when creating the new Settings object, and then we return that new object.

Then we can test that it is used.

If you have many settings that possibly change a lot, maybe in different environments, it might be useful to put them on a file and then read them from it as if they were environment variables.

This practice is common enough that it has a name, these environment variables are commonly placed in a file .env, and the file is called a "dotenv".

A file starting with a dot (.) is a hidden file in Unix-like systems, like Linux and macOS.

But a dotenv file doesn't really have to have that exact filename.

Pydantic has support for reading from these types of files using an external library. You can read more at Pydantic Settings: Dotenv (.env) support.

For this to work, you need to pip install python-dotenv.

You could have a .env file with:

And then update your config.py with:

Prefer to use the Annotated version if possible.

The model_config attribute is used just for Pydantic configuration. You can read more at Pydantic: Concepts: Configuration.

Here we define the config env_file inside of your Pydantic Settings class, and set the value to the filename with the dotenv file we want to use.

Reading a file from disk is normally a costly (slow) operation, so you probably want to do it only once and then reuse the same settings object, instead of reading it for each request.

But every time we do:

a new Settings object would be created, and at creation it would read the .env file again.

If the dependency function was just like:

we would create that object for each request, and we would be reading the .env file for each request. ⚠️

But as we are using the @lru_cache decorator on top, the Settings object will be created only once, the first time it's called. ✔️

Prefer to use the Annotated version if possible.

Then for any subsequent call of get_settings() in the dependencies for the next requests, instead of executing the internal code of get_settings() and creating a new Settings object, it will return the same object that was returned on the first call, again and again.

@lru_cache modifies the function it decorates to return the same value that was returned the first time, instead of computing it again, executing the code of the function every time.

So, the function below it will be executed once for each combination of arguments. And then the values returned by each of those combinations of arguments will be used again and again whenever the function is called with exactly the same combination of arguments.

For example, if you have a function:

your program could execute like this:

In the case of our dependency get_settings(), the function doesn't even take any arguments, so it always returns the same value.

That way, it behaves almost as if it was just a global variable. But as it uses a dependency function, then we can override it easily for testing.

@lru_cache is part of functools which is part of Python's standard library, you can read more about it in the Python docs for @lru_cache.

You can use Pydantic Settings to handle the settings or configurations for your application, with all the power of Pydantic models.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50


settings = Settings()
app = FastAPI()


@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
```

Example 2 (python):
```python
from fastapi import FastAPI
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50


settings = Settings()
app = FastAPI()


@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
```

Example 3 (python):
```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50


settings = Settings()
```

Example 4 (python):
```python
from fastapi import FastAPI

from .config import settings

app = FastAPI()


@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
```

---

## FastAPI class¶

**URL:** https://fastapi.tiangolo.com/reference/fastapi/

**Contents:**
- FastAPI class¶
- fastapi.FastAPI ¶
    - Example¶
  - openapi_version instance-attribute ¶
  - webhooks instance-attribute ¶
  - state instance-attribute ¶
  - dependency_overrides instance-attribute ¶
  - openapi ¶
  - websocket ¶
  - include_router ¶

Here's the reference information for the FastAPI class, with all its parameters, attributes and methods.

You can import the FastAPI class directly from fastapi:

FastAPI app class, the main entrypoint to use FastAPI.

Read more in the FastAPI docs for First Steps.

Boolean indicating if debug tracebacks should be returned on server errors.

Read more in the Starlette docs for Applications.

TYPE: bool DEFAULT: False

Note: you probably shouldn't use this parameter, it is inherited from Starlette and supported for compatibility.

A list of routes to serve incoming HTTP and WebSocket requests.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

The title of the API.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more in the FastAPI docs for Metadata and Docs URLs.

TYPE: str DEFAULT: 'FastAPI'

A short summary of the API.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more in the FastAPI docs for Metadata and Docs URLs.

TYPE: Optional[str] DEFAULT: None

A description of the API. Supports Markdown (using CommonMark syntax).

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more in the FastAPI docs for Metadata and Docs URLs.

TYPE: str DEFAULT: ''

The version of the API.

Note This is the version of your application, not the version of the OpenAPI specification nor the version of FastAPI being used.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more in the FastAPI docs for Metadata and Docs URLs.

TYPE: str DEFAULT: '0.1.0'

The URL where the OpenAPI schema will be served from.

If you set it to None, no OpenAPI schema will be served publicly, and the default automatic endpoints /docs and /redoc will also be disabled.

Read more in the FastAPI docs for Metadata and Docs URLs.

TYPE: Optional[str] DEFAULT: '/openapi.json'

A list of tags used by OpenAPI, these are the same tags you can set in the path operations, like:

The order of the tags can be used to specify the order shown in tools like Swagger UI, used in the automatic path /docs.

It's not required to specify all the tags used.

The tags that are not declared MAY be organized randomly or based on the tools' logic. Each tag name in the list MUST be unique.

The value of each item is a dict containing:

Read more in the FastAPI docs for Metadata and Docs URLs.

TYPE: Optional[list[dict[str, Any]]] DEFAULT: None

A list of dicts with connectivity information to a target server.

You would use it, for example, if your application is served from different domains and you want to use the same Swagger UI in the browser to interact with each of them (instead of having multiple browser tabs open). Or if you want to leave fixed the possible URLs.

If the servers list is not provided, or is an empty list, the servers property in the generated OpenAPI will be:

Each item in the list is a dict containing:

Read more in the FastAPI docs for Behind a Proxy.

TYPE: Optional[list[dict[str, Union[str, Any]]]] DEFAULT: None

A list of global dependencies, they will be applied to each path operation, including in sub-routers.

Read more about it in the FastAPI docs for Global Dependencies.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

The default response class to be used.

Read more in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: type[Response] DEFAULT: Default(JSONResponse)

Whether to detect and redirect slashes in URLs when the client doesn't use the same format.

With this app, if a client goes to /items (without a trailing slash), they will be automatically redirected with an HTTP status code of 307 to /items/.

TYPE: bool DEFAULT: True

The path to the automatic interactive API documentation. It is handled in the browser by Swagger UI.

The default URL is /docs. You can disable it by setting it to None.

If openapi_url is set to None, this will be automatically disabled.

Read more in the FastAPI docs for Metadata and Docs URLs.

TYPE: Optional[str] DEFAULT: '/docs'

The path to the alternative automatic interactive API documentation provided by ReDoc.

The default URL is /redoc. You can disable it by setting it to None.

If openapi_url is set to None, this will be automatically disabled.

Read more in the FastAPI docs for Metadata and Docs URLs.

TYPE: Optional[str] DEFAULT: '/redoc'

The OAuth2 redirect endpoint for the Swagger UI.

By default it is /docs/oauth2-redirect.

This is only used if you use OAuth2 (with the "Authorize" button) with Swagger UI.

TYPE: Optional[str] DEFAULT: '/docs/oauth2-redirect'

OAuth2 configuration for the Swagger UI, by default shown at /docs.

Read more about the available configuration options in the Swagger UI docs.

TYPE: Optional[dict[str, Any]] DEFAULT: None

List of middleware to be added when creating the application.

In FastAPI you would normally do this with app.add_middleware() instead.

Read more in the FastAPI docs for Middleware.

TYPE: Optional[Sequence[Middleware]] DEFAULT: None

A dictionary with handlers for exceptions.

In FastAPI, you would normally use the decorator @app.exception_handler().

Read more in the FastAPI docs for Handling Errors.

TYPE: Optional[dict[Union[int, type[Exception]], Callable[[Request, Any], Coroutine[Any, Any, Response]]]] DEFAULT: None

A list of startup event handler functions.

You should instead use the lifespan handlers.

Read more in the FastAPI docs for lifespan.

TYPE: Optional[Sequence[Callable[[], Any]]] DEFAULT: None

A list of shutdown event handler functions.

You should instead use the lifespan handlers.

Read more in the FastAPI docs for lifespan.

TYPE: Optional[Sequence[Callable[[], Any]]] DEFAULT: None

A Lifespan context manager handler. This replaces startup and shutdown functions with a single context manager.

Read more in the FastAPI docs for lifespan.

TYPE: Optional[Lifespan[AppType]] DEFAULT: None

A URL to the Terms of Service for your API.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more at the FastAPI docs for Metadata and Docs URLs.

TYPE: Optional[str] DEFAULT: None

A dictionary with the contact information for the exposed API.

It can contain several fields.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more at the FastAPI docs for Metadata and Docs URLs.

TYPE: Optional[dict[str, Union[str, Any]]] DEFAULT: None

A dictionary with the license information for the exposed API.

It can contain several fields.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more at the FastAPI docs for Metadata and Docs URLs.

TYPE: Optional[dict[str, Union[str, Any]]] DEFAULT: None

A URL prefix for the OpenAPI URL.

TYPE: str DEFAULT: ''

A path prefix handled by a proxy that is not seen by the application but is seen by external clients, which affects things like Swagger UI.

Read more about it at the FastAPI docs for Behind a Proxy.

TYPE: str DEFAULT: ''

To disable automatically generating the URLs in the servers field in the autogenerated OpenAPI using the root_path.

Read more about it in the FastAPI docs for Behind a Proxy.

TYPE: bool DEFAULT: True

Additional responses to be shown in OpenAPI.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Additional Responses in OpenAPI.

And in the FastAPI docs for Bigger Applications.

TYPE: Optional[dict[Union[int, str], dict[str, Any]]] DEFAULT: None

OpenAPI callbacks that should apply to all path operations.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

Add OpenAPI webhooks. This is similar to callbacks but it doesn't depend on specific path operations.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Note: This is available since OpenAPI 3.1.0, FastAPI 0.99.0.

Read more about it in the FastAPI docs for OpenAPI Webhooks.

TYPE: Optional[APIRouter] DEFAULT: None

Mark all path operations as deprecated. You probably don't need it, but it's available.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[bool] DEFAULT: None

To include (or not) all the path operations in the generated OpenAPI. You probably don't need it, but it's available.

This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: bool DEFAULT: True

Parameters to configure Swagger UI, the autogenerated interactive API documentation (by default at /docs).

Read more about it in the FastAPI docs about how to Configure Swagger UI.

TYPE: Optional[dict[str, Any]] DEFAULT: None

Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.

This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str] DEFAULT: Default(generate_unique_id)

Whether to generate separate OpenAPI schemas for request body and response body when the results would be more precise.

This is particularly useful when automatically generating clients.

For example, if you have a model like:

When Item is used for input, a request body, tags is not required, the client doesn't have to provide it.

But when using Item for output, for a response body, tags is always available because it has a default value, even if it's just an empty list. So, the client should be able to always expect it.

In this case, there would be two different schemas, one for input and another one for output.

TYPE: bool DEFAULT: True

This field allows you to provide additional external documentation links. If provided, it must be a dictionary containing:

TYPE: Optional[dict[str, Any]] DEFAULT: None

Extra keyword arguments to be stored in the app, not used by FastAPI anywhere.

TYPE: Any DEFAULT: {}

The version string of OpenAPI.

FastAPI will generate OpenAPI version 3.1.0, and will output that as the OpenAPI version. But some tools, even though they might be compatible with OpenAPI 3.1.0, might not recognize it as a valid.

So you could override this value to trick those tools into using the generated OpenAPI. Have in mind that this is a hack. But if you avoid using features added in OpenAPI 3.1.0, it might work for your use case.

This is not passed as a parameter to the FastAPI class to avoid giving the false idea that FastAPI would generate a different OpenAPI schema. It is only available as an attribute.

The app.webhooks attribute is an APIRouter with the path operations that will be used just for documentation of webhooks.

Read more about it in the FastAPI docs for OpenAPI Webhooks.

A state object for the application. This is the same object for the entire application, it doesn't change from request to request.

You normally wouldn't use this in FastAPI, for most of the cases you would instead use FastAPI dependencies.

This is simply inherited from Starlette.

Read more about it in the Starlette docs for Applications.

A dictionary with overrides for the dependencies.

Each key is the original dependency callable, and the value is the actual dependency that should be called.

This is for testing, to replace expensive dependencies with testing versions.

Read more about it in the FastAPI docs for Testing Dependencies with Overrides.

Generate the OpenAPI schema of the application. This is called by FastAPI internally.

The first time it is called it stores the result in the attribute app.openapi_schema, and next times it is called, it just returns that same result. To avoid the cost of generating the schema every time.

If you need to modify the generated OpenAPI schema, you could modify it.

Read more in the FastAPI docs for OpenAPI.

Decorate a WebSocket function.

Read more about it in the FastAPI docs for WebSockets.

A name for the WebSocket. Only used internally.

TYPE: Optional[str] DEFAULT: None

A list of dependencies (using Depends()) to be used for this WebSocket.

Read more about it in the FastAPI docs for WebSockets.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

Include an APIRouter in the same app.

Read more about it in the FastAPI docs for Bigger Applications.

The APIRouter to include.

An optional path prefix for the router.

TYPE: str DEFAULT: ''

A list of tags to be applied to all the path operations in this router.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[list[Union[str, Enum]]] DEFAULT: None

A list of dependencies (using Depends()) to be applied to all the path operations in this router.

Read more about it in the FastAPI docs for Bigger Applications - Multiple Files.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

Additional responses to be shown in OpenAPI.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Additional Responses in OpenAPI.

And in the FastAPI docs for Bigger Applications.

TYPE: Optional[dict[Union[int, str], dict[str, Any]]] DEFAULT: None

Mark all the path operations in this router as deprecated.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool] DEFAULT: None

Include (or not) all the path operations in this router in the generated OpenAPI schema.

This affects the generated OpenAPI (e.g. visible at /docs).

TYPE: bool DEFAULT: True

Default response class to be used for the path operations in this router.

Read more in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: type[Response] DEFAULT: Default(JSONResponse)

List of path operations that will be used as OpenAPI callbacks.

This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.

This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str] DEFAULT: Default(generate_unique_id)

Add a path operation using an HTTP GET operation.

The URL path to be used for this path operation.

For example, in http://example.com/items, the path is /items.

The type to use for the response.

It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

Read more about it in the FastAPI docs for Response Model.

TYPE: Any DEFAULT: Default(None)

The default status code to be used for the response.

You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int] DEFAULT: None

A list of tags to be applied to the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[list[Union[str, Enum]]] DEFAULT: None

A list of dependencies (using Depends()) to be applied to the path operation.

Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

A summary for the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

A description for the path operation.

If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

The description for the default response.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: str DEFAULT: 'Successful Response'

Additional responses that could be returned by this path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[dict[Union[int, str], dict[str, Any]]] DEFAULT: None

Mark this path operation as deprecated.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool] DEFAULT: None

Custom operation ID to be used by this path operation.

By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str] DEFAULT: None

Configuration passed to Pydantic to include only certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to exclude certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: True

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should exclude fields set to None.

This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Include this path operation in the generated OpenAPI schema.

This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: bool DEFAULT: True

Response class to be used for this path operation.

This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: type[Response] DEFAULT: Default(JSONResponse)

Name for this path operation. Only used internally.

TYPE: Optional[str] DEFAULT: None

List of path operations that will be used as OpenAPI callbacks.

This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

Extra metadata to be included in the OpenAPI schema for this path operation.

Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[dict[str, Any]] DEFAULT: None

Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.

This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str] DEFAULT: Default(generate_unique_id)

Add a path operation using an HTTP PUT operation.

The URL path to be used for this path operation.

For example, in http://example.com/items, the path is /items.

The type to use for the response.

It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

Read more about it in the FastAPI docs for Response Model.

TYPE: Any DEFAULT: Default(None)

The default status code to be used for the response.

You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int] DEFAULT: None

A list of tags to be applied to the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[list[Union[str, Enum]]] DEFAULT: None

A list of dependencies (using Depends()) to be applied to the path operation.

Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

A summary for the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

A description for the path operation.

If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

The description for the default response.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: str DEFAULT: 'Successful Response'

Additional responses that could be returned by this path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[dict[Union[int, str], dict[str, Any]]] DEFAULT: None

Mark this path operation as deprecated.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool] DEFAULT: None

Custom operation ID to be used by this path operation.

By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str] DEFAULT: None

Configuration passed to Pydantic to include only certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to exclude certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: True

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should exclude fields set to None.

This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Include this path operation in the generated OpenAPI schema.

This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: bool DEFAULT: True

Response class to be used for this path operation.

This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: type[Response] DEFAULT: Default(JSONResponse)

Name for this path operation. Only used internally.

TYPE: Optional[str] DEFAULT: None

List of path operations that will be used as OpenAPI callbacks.

This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

Extra metadata to be included in the OpenAPI schema for this path operation.

Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[dict[str, Any]] DEFAULT: None

Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.

This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str] DEFAULT: Default(generate_unique_id)

Add a path operation using an HTTP POST operation.

The URL path to be used for this path operation.

For example, in http://example.com/items, the path is /items.

The type to use for the response.

It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

Read more about it in the FastAPI docs for Response Model.

TYPE: Any DEFAULT: Default(None)

The default status code to be used for the response.

You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int] DEFAULT: None

A list of tags to be applied to the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[list[Union[str, Enum]]] DEFAULT: None

A list of dependencies (using Depends()) to be applied to the path operation.

Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

A summary for the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

A description for the path operation.

If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

The description for the default response.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: str DEFAULT: 'Successful Response'

Additional responses that could be returned by this path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[dict[Union[int, str], dict[str, Any]]] DEFAULT: None

Mark this path operation as deprecated.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool] DEFAULT: None

Custom operation ID to be used by this path operation.

By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str] DEFAULT: None

Configuration passed to Pydantic to include only certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to exclude certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: True

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should exclude fields set to None.

This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Include this path operation in the generated OpenAPI schema.

This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: bool DEFAULT: True

Response class to be used for this path operation.

This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: type[Response] DEFAULT: Default(JSONResponse)

Name for this path operation. Only used internally.

TYPE: Optional[str] DEFAULT: None

List of path operations that will be used as OpenAPI callbacks.

This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

Extra metadata to be included in the OpenAPI schema for this path operation.

Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[dict[str, Any]] DEFAULT: None

Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.

This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str] DEFAULT: Default(generate_unique_id)

Add a path operation using an HTTP DELETE operation.

The URL path to be used for this path operation.

For example, in http://example.com/items, the path is /items.

The type to use for the response.

It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

Read more about it in the FastAPI docs for Response Model.

TYPE: Any DEFAULT: Default(None)

The default status code to be used for the response.

You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int] DEFAULT: None

A list of tags to be applied to the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[list[Union[str, Enum]]] DEFAULT: None

A list of dependencies (using Depends()) to be applied to the path operation.

Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

A summary for the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

A description for the path operation.

If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

The description for the default response.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: str DEFAULT: 'Successful Response'

Additional responses that could be returned by this path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[dict[Union[int, str], dict[str, Any]]] DEFAULT: None

Mark this path operation as deprecated.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool] DEFAULT: None

Custom operation ID to be used by this path operation.

By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str] DEFAULT: None

Configuration passed to Pydantic to include only certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to exclude certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: True

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should exclude fields set to None.

This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Include this path operation in the generated OpenAPI schema.

This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: bool DEFAULT: True

Response class to be used for this path operation.

This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: type[Response] DEFAULT: Default(JSONResponse)

Name for this path operation. Only used internally.

TYPE: Optional[str] DEFAULT: None

List of path operations that will be used as OpenAPI callbacks.

This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

Extra metadata to be included in the OpenAPI schema for this path operation.

Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[dict[str, Any]] DEFAULT: None

Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.

This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str] DEFAULT: Default(generate_unique_id)

Add a path operation using an HTTP OPTIONS operation.

The URL path to be used for this path operation.

For example, in http://example.com/items, the path is /items.

The type to use for the response.

It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

Read more about it in the FastAPI docs for Response Model.

TYPE: Any DEFAULT: Default(None)

The default status code to be used for the response.

You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int] DEFAULT: None

A list of tags to be applied to the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[list[Union[str, Enum]]] DEFAULT: None

A list of dependencies (using Depends()) to be applied to the path operation.

Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

A summary for the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

A description for the path operation.

If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

The description for the default response.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: str DEFAULT: 'Successful Response'

Additional responses that could be returned by this path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[dict[Union[int, str], dict[str, Any]]] DEFAULT: None

Mark this path operation as deprecated.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool] DEFAULT: None

Custom operation ID to be used by this path operation.

By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str] DEFAULT: None

Configuration passed to Pydantic to include only certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to exclude certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: True

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should exclude fields set to None.

This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Include this path operation in the generated OpenAPI schema.

This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: bool DEFAULT: True

Response class to be used for this path operation.

This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: type[Response] DEFAULT: Default(JSONResponse)

Name for this path operation. Only used internally.

TYPE: Optional[str] DEFAULT: None

List of path operations that will be used as OpenAPI callbacks.

This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

Extra metadata to be included in the OpenAPI schema for this path operation.

Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[dict[str, Any]] DEFAULT: None

Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.

This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str] DEFAULT: Default(generate_unique_id)

Add a path operation using an HTTP HEAD operation.

The URL path to be used for this path operation.

For example, in http://example.com/items, the path is /items.

The type to use for the response.

It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

Read more about it in the FastAPI docs for Response Model.

TYPE: Any DEFAULT: Default(None)

The default status code to be used for the response.

You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int] DEFAULT: None

A list of tags to be applied to the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[list[Union[str, Enum]]] DEFAULT: None

A list of dependencies (using Depends()) to be applied to the path operation.

Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

A summary for the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

A description for the path operation.

If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

The description for the default response.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: str DEFAULT: 'Successful Response'

Additional responses that could be returned by this path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[dict[Union[int, str], dict[str, Any]]] DEFAULT: None

Mark this path operation as deprecated.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool] DEFAULT: None

Custom operation ID to be used by this path operation.

By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str] DEFAULT: None

Configuration passed to Pydantic to include only certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to exclude certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: True

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should exclude fields set to None.

This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Include this path operation in the generated OpenAPI schema.

This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: bool DEFAULT: True

Response class to be used for this path operation.

This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: type[Response] DEFAULT: Default(JSONResponse)

Name for this path operation. Only used internally.

TYPE: Optional[str] DEFAULT: None

List of path operations that will be used as OpenAPI callbacks.

This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

Extra metadata to be included in the OpenAPI schema for this path operation.

Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[dict[str, Any]] DEFAULT: None

Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.

This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str] DEFAULT: Default(generate_unique_id)

Add a path operation using an HTTP PATCH operation.

The URL path to be used for this path operation.

For example, in http://example.com/items, the path is /items.

The type to use for the response.

It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

Read more about it in the FastAPI docs for Response Model.

TYPE: Any DEFAULT: Default(None)

The default status code to be used for the response.

You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int] DEFAULT: None

A list of tags to be applied to the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[list[Union[str, Enum]]] DEFAULT: None

A list of dependencies (using Depends()) to be applied to the path operation.

Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

A summary for the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

A description for the path operation.

If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

The description for the default response.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: str DEFAULT: 'Successful Response'

Additional responses that could be returned by this path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[dict[Union[int, str], dict[str, Any]]] DEFAULT: None

Mark this path operation as deprecated.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool] DEFAULT: None

Custom operation ID to be used by this path operation.

By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str] DEFAULT: None

Configuration passed to Pydantic to include only certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to exclude certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: True

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should exclude fields set to None.

This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Include this path operation in the generated OpenAPI schema.

This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: bool DEFAULT: True

Response class to be used for this path operation.

This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: type[Response] DEFAULT: Default(JSONResponse)

Name for this path operation. Only used internally.

TYPE: Optional[str] DEFAULT: None

List of path operations that will be used as OpenAPI callbacks.

This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

Extra metadata to be included in the OpenAPI schema for this path operation.

Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[dict[str, Any]] DEFAULT: None

Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.

This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str] DEFAULT: Default(generate_unique_id)

Add a path operation using an HTTP TRACE operation.

The URL path to be used for this path operation.

For example, in http://example.com/items, the path is /items.

The type to use for the response.

It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

Read more about it in the FastAPI docs for Response Model.

TYPE: Any DEFAULT: Default(None)

The default status code to be used for the response.

You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int] DEFAULT: None

A list of tags to be applied to the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[list[Union[str, Enum]]] DEFAULT: None

A list of dependencies (using Depends()) to be applied to the path operation.

Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]] DEFAULT: None

A summary for the path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

A description for the path operation.

If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str] DEFAULT: None

The description for the default response.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: str DEFAULT: 'Successful Response'

Additional responses that could be returned by this path operation.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[dict[Union[int, str], dict[str, Any]]] DEFAULT: None

Mark this path operation as deprecated.

It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool] DEFAULT: None

Custom operation ID to be used by this path operation.

By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str] DEFAULT: None

Configuration passed to Pydantic to include only certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to exclude certain fields in the response data.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx] DEFAULT: None

Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: True

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.

When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Configuration passed to Pydantic to define if the response data should exclude fields set to None.

This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: bool DEFAULT: False

Include this path operation in the generated OpenAPI schema.

This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: bool DEFAULT: True

Response class to be used for this path operation.

This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: type[Response] DEFAULT: Default(JSONResponse)

Name for this path operation. Only used internally.

TYPE: Optional[str] DEFAULT: None

List of path operations that will be used as OpenAPI callbacks.

This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[list[BaseRoute]] DEFAULT: None

Extra metadata to be included in the OpenAPI schema for this path operation.

Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[dict[str, Any]] DEFAULT: None

Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.

This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str] DEFAULT: Default(generate_unique_id)

Add an event handler for the application.

on_event is deprecated, use lifespan event handlers instead.

Read more about it in the FastAPI docs for Lifespan Events.

The type of event. startup or shutdown.

Add a middleware to the application.

Read more about it in the FastAPI docs for Middleware.

The type of middleware. Currently only supports http.

Add an exception handler to the app.

Read more about it in the FastAPI docs for Handling Errors.

The Exception class this would handle, or a status code.

TYPE: Union[int, type[Exception]]

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI
```

Example 2 (rust):
```rust
FastAPI(
    *,
    debug=False,
    routes=None,
    title="FastAPI",
    summary=None,
    description="",
    version="0.1.0",
    openapi_url="/openapi.json",
    openapi_tags=None,
    servers=None,
    dependencies=None,
    default_response_class=Default(JSONResponse),
    redirect_slashes=True,
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect",
    swagger_ui_init_oauth=None,
    middleware=None,
    exception_handlers=None,
    on_startup=None,
    on_shutdown=None,
    lifespan=None,
    terms_of_service=None,
    contact=None,
    license_info=None,
    openapi_prefix="",
    root_path="",
    root_path_in_servers=True,
    responses=None,
    callbacks=None,
    webhooks=None,
    deprecated=None,
    include_in_schema=True,
    swagger_ui_parameters=None,
    generate_unique_id_function=Default(generate_unique_id),
    separate_input_output_schemas=True,
    openapi_external_docs=None,
    **extra
)
```

Example 3 (python):
```python
from fastapi import FastAPI

app = FastAPI()
```

Example 4 (python):
```python
from fastapi import FastAPI

app = FastAPI(title="ChimichangApp")
```

---

## Encoders - jsonable_encoder¶

**URL:** https://fastapi.tiangolo.com/reference/encoders/

**Contents:**
- Encoders - jsonable_encoder¶
- fastapi.encoders.jsonable_encoder ¶

Convert any object to something that can be encoded in JSON.

This is used internally by FastAPI to make sure anything you return can be encoded as JSON before it is sent to the client.

You can also use it yourself, for example to convert objects before saving them in a database that supports only JSON.

Read more about it in the FastAPI docs for JSON Compatible Encoder.

The input object to convert to JSON.

Pydantic's include parameter, passed to Pydantic models to set the fields to include.

TYPE: Optional[IncEx] DEFAULT: None

Pydantic's exclude parameter, passed to Pydantic models to set the fields to exclude.

TYPE: Optional[IncEx] DEFAULT: None

Pydantic's by_alias parameter, passed to Pydantic models to define if the output should use the alias names (when provided) or the Python attribute names. In an API, if you set an alias, it's probably because you want to use it in the result, so you probably want to leave this set to True.

TYPE: bool DEFAULT: True

Pydantic's exclude_unset parameter, passed to Pydantic models to define if it should exclude from the output the fields that were not explicitly set (and that only had their default values).

TYPE: bool DEFAULT: False

Pydantic's exclude_defaults parameter, passed to Pydantic models to define if it should exclude from the output the fields that had the same default value, even when they were explicitly set.

TYPE: bool DEFAULT: False

Pydantic's exclude_none parameter, passed to Pydantic models to define if it should exclude from the output any fields that have a None value.

TYPE: bool DEFAULT: False

Pydantic's custom_encoder parameter, passed to Pydantic models to define a custom encoder.

TYPE: Optional[dict[Any, Callable[[Any], Any]]] DEFAULT: None

Exclude from the output any fields that start with the name _sa.

This is mainly a hack for compatibility with SQLAlchemy objects, they store internal SQLAlchemy-specific state in attributes named with _sa, and those objects can't (and shouldn't be) serialized to JSON.

TYPE: bool DEFAULT: True

**Examples:**

Example 1 (rust):
```rust
jsonable_encoder(
    obj,
    include=None,
    exclude=None,
    by_alias=True,
    exclude_unset=False,
    exclude_defaults=False,
    exclude_none=False,
    custom_encoder=None,
    sqlalchemy_safe=True,
)
```

Example 2 (sql):
```sql
def jsonable_encoder(
    obj: Annotated[
        Any,
        Doc(
            """
            The input object to convert to JSON.
            """
        ),
    ],
    include: Annotated[
        Optional[IncEx],
        Doc(
            """
            Pydantic's `include` parameter, passed to Pydantic models to set the
            fields to include.
            """
        ),
    ] = None,
    exclude: Annotated[
        Optional[IncEx],
        Doc(
            """
            Pydantic's `exclude` parameter, passed to Pydantic models to set the
            fields to exclude.
            """
        ),
    ] = None,
    by_alias: Annotated[
        bool,
        Doc(
            """
            Pydantic's `by_alias` parameter, passed to Pydantic models to define if
            the output should use the alias names (when provided) or the Python
            attribute names. In an API, if you set an alias, it's probably because you
            want to use it in the result, so you probably want to leave this set to
            `True`.
            """
        ),
    ] = True,
    exclude_unset: Annotated[
        bool,
        Doc(
            """
            Pydantic's `exclude_unset` parameter, passed to Pydantic models to define
            if it should exclude from the output the fields that were not explicitly
            set (and that only had their default values).
            """
        ),
    ] = False,
    exclude_defaults: Annotated[
        bool,
        Doc(
            """
            Pydantic's `exclude_defaults` parameter, passed to Pydantic models to define
            if it should exclude from the output the fields that had the same default
            value, even when they were explicitly set.
            """
        ),
    ] = False,
    exclude_none: Annotated[
        bool,
        Doc(
            """
            Pydantic's `exclude_none` parameter, passed to Pydantic models to define
            if it should exclude from the output any fields that have a `None` value.
            """
        ),
    ] = False,
    custom_encoder: Annotated[
        Optional[dict[Any, Callable[[Any], Any]]],
        Doc(
            """
            Pydantic's `custom_encoder` parameter, passed to Pydantic models to define
            a custom encoder.
            """
        ),
    ] = None,
    sqlalchemy_safe: Annotated[
        bool,
        Doc(
            """
            Exclude from the output any fields that start with the name `_sa`.

            This is mainly a hack for compatibility with SQLAlchemy objects, they
            store internal SQLAlchemy-specific state in attributes named with `_sa`,
            and those objects can't (and shouldn't be) serialized to JSON.
            """
        ),
    ] = True,
) -> Any:
    """
    Convert any object to something that can be encoded in JSON.

    This is used internally by FastAPI to make sure anything you return can be
    encoded as JSON before it is sent to the client.

    You can also use it yourself, for example to convert objects before saving them
    in a database that supports only JSON.

    Read more about it in the
    [FastAPI docs for JSON Compatible Encoder](https://fastapi.tiangolo.com/tutorial/encoder/).
    """
    custom_encoder = custom_encoder or {}
    if custom_encoder:
        if type(obj) in custom_encoder:
            return custom_encoder[type(obj)](obj)
        else:
            for encoder_type, encoder_instance in custom_encoder.items():
                if isinstance(obj, encoder_type):
                    return encoder_instance(obj)
    if include is not None and not isinstance(include, (set, dict)):
        include = set(include)
    if exclude is not None and not isinstance(exclude, (set, dict)):
        exclude = set(exclude)
    if isinstance(obj, BaseModel):
        obj_dict = obj.model_dump(
            mode="json",
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_none=exclude_none,
            exclude_defaults=exclude_defaults,
        )
        return jsonable_encoder(
            obj_dict,
            exclude_none=exclude_none,
            exclude_defaults=exclude_defaults,
            sqlalchemy_safe=sqlalchemy_safe,
        )
    if dataclasses.is_dataclass(obj):
        assert not isinstance(obj, type)
        obj_dict = dataclasses.asdict(obj)
        return jsonable_encoder(
            obj_dict,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            custom_encoder=custom_encoder,
            sqlalchemy_safe=sqlalchemy_safe,
        )
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, PurePath):
        return str(obj)
    if isinstance(obj, (str, int, float, type(None))):
        return obj
    if isinstance(obj, PydanticUndefinedType):
        return None
    if isinstance(obj, dict):
        encoded_dict = {}
        allowed_keys = set(obj.keys())
        if include is not None:
            allowed_keys &= set(include)
        if exclude is not None:
            allowed_keys -= set(exclude)
        for key, value in obj.items():
            if (
                (
                    not sqlalchemy_safe
                    or (not isinstance(key, str))
                    or (not key.startswith("_sa"))
                )
                and (value is not None or not exclude_none)
                and key in allowed_keys
            ):
                encoded_key = jsonable_encoder(
                    key,
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                    exclude_none=exclude_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
                encoded_value = jsonable_encoder(
                    value,
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                    exclude_none=exclude_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
                encoded_dict[encoded_key] = encoded_value
        return encoded_dict
    if isinstance(obj, (list, set, frozenset, GeneratorType, tuple, deque)):
        encoded_list = []
        for item in obj:
            encoded_list.append(
                jsonable_encoder(
                    item,
                    include=include,
                    exclude=exclude,
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                    exclude_defaults=exclude_defaults,
                    exclude_none=exclude_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
            )
        return encoded_list

    if type(obj) in ENCODERS_BY_TYPE:
        return ENCODERS_BY_TYPE[type(obj)](obj)
    for encoder, classes_tuple in encoders_by_class_tuples.items():
        if isinstance(obj, classes_tuple):
            return encoder(obj)
    if is_pydantic_v1_model_instance(obj):
        raise PydanticV1NotSupportedError(
            "pydantic.v1 models are no longer supported by FastAPI."
            f" Please update the model {obj!r}."
        )
    try:
        data = dict(obj)
    except Exception as e:
        errors: list[Exception] = []
        errors.append(e)
        try:
            data = vars(obj)
        except Exception as e:
            errors.append(e)
            raise ValueError(errors) from e
    return jsonable_encoder(
        data,
        include=include,
        exclude=exclude,
        by_alias=by_alias,
        exclude_unset=exclude_unset,
        exclude_defaults=exclude_defaults,
        exclude_none=exclude_none,
        custom_encoder=custom_encoder,
        sqlalchemy_safe=sqlalchemy_safe,
    )
```

---

## Background Tasks - BackgroundTasks¶

**URL:** https://fastapi.tiangolo.com/reference/background/

**Contents:**
- Background Tasks - BackgroundTasks¶
- fastapi.BackgroundTasks ¶
    - Example¶
  - func instance-attribute ¶
  - args instance-attribute ¶
  - kwargs instance-attribute ¶
  - is_async instance-attribute ¶
  - tasks instance-attribute ¶
  - add_task ¶

You can declare a parameter in a path operation function or dependency function with the type BackgroundTasks, and then you can use it to schedule the execution of background tasks after the response is sent.

You can import it directly from fastapi:

Bases: BackgroundTasks

A collection of background tasks that will be called after a response has been sent to the client.

Read more about it in the FastAPI docs for Background Tasks.

Add a function to be called in the background after the response is sent.

Read more about it in the FastAPI docs for Background Tasks.

The function to call after the response is sent.

It can be a regular def function or an async def function.

TYPE: Callable[P, Any]

**Examples:**

Example 1 (python):
```python
from fastapi import BackgroundTasks
```

Example 2 (rust):
```rust
BackgroundTasks(tasks=None)
```

Example 3 (python):
```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
```

Example 4 (python):
```python
def __init__(self, tasks: Sequence[BackgroundTask] | None = None):
    self.tasks = list(tasks) if tasks else []
```

---

## About FastAPI versions¶

**URL:** https://fastapi.tiangolo.com/deployment/versions/

**Contents:**
- About FastAPI versions¶
- Pin your fastapi version¶
- Available versions¶
- About versions¶
- Upgrading the FastAPI versions¶
- About Starlette¶
- About Pydantic¶

FastAPI is already being used in production in many applications and systems. And the test coverage is kept at 100%. But its development is still moving quickly.

New features are added frequently, bugs are fixed regularly, and the code is still continuously improving.

That's why the current versions are still 0.x.x, this reflects that each version could potentially have breaking changes. This follows the Semantic Versioning conventions.

You can create production applications with FastAPI right now (and you have probably been doing it for some time), you just have to make sure that you use a version that works correctly with the rest of your code.

The first thing you should do is to "pin" the version of FastAPI you are using to the specific latest version that you know works correctly for your application.

For example, let's say you are using version 0.112.0 in your app.

If you use a requirements.txt file you could specify the version with:

that would mean that you would use exactly the version 0.112.0.

Or you could also pin it with:

that would mean that you would use the versions 0.112.0 or above, but less than 0.113.0, for example, a version 0.112.2 would still be accepted.

If you use any other tool to manage your installations, like uv, Poetry, Pipenv, or others, they all have a way that you can use to define specific versions for your packages.

You can see the available versions (e.g. to check what is the current latest) in the Release Notes.

Following the Semantic Versioning conventions, any version below 1.0.0 could potentially add breaking changes.

FastAPI also follows the convention that any "PATCH" version change is for bug fixes and non-breaking changes.

The "PATCH" is the last number, for example, in 0.2.3, the PATCH version is 3.

So, you should be able to pin to a version like:

Breaking changes and new features are added in "MINOR" versions.

The "MINOR" is the number in the middle, for example, in 0.2.3, the MINOR version is 2.

You should add tests for your app.

With FastAPI it's very easy (thanks to Starlette), check the docs: Testing

After you have tests, then you can upgrade the FastAPI version to a more recent one, and make sure that all your code is working correctly by running your tests.

If everything is working, or after you make the necessary changes, and all your tests are passing, then you can pin your fastapi to that new recent version.

You shouldn't pin the version of starlette.

Different versions of FastAPI will use a specific newer version of Starlette.

So, you can just let FastAPI use the correct Starlette version.

Pydantic includes the tests for FastAPI with its own tests, so new versions of Pydantic (above 1.0.0) are always compatible with FastAPI.

You can pin Pydantic to any version above 1.0.0 that works for you.

**Examples:**

Example 1 (unknown):
```unknown
fastapi[standard]==0.112.0
```

Example 2 (unknown):
```unknown
fastapi[standard]>=0.112.0,<0.113.0
```

Example 3 (unknown):
```unknown
fastapi>=0.45.0,<0.46.0
```

Example 4 (unknown):
```unknown
pydantic>=2.7.0,<3.0.0
```

---

## Header Parameter Models¶

**URL:** https://fastapi.tiangolo.com/tutorial/header-param-models/

**Contents:**
- Header Parameter Models¶
- Header Parameters with a Pydantic Model¶
- Check the Docs¶
- Forbid Extra Headers¶
- Disable Convert Underscores¶
- Summary¶

If you have a group of related header parameters, you can create a Pydantic model to declare them.

This would allow you to re-use the model in multiple places and also to declare validations and metadata for all the parameters at once. 😎

This is supported since FastAPI version 0.115.0. 🤓

Declare the header parameters that you need in a Pydantic model, and then declare the parameter as Header:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

FastAPI will extract the data for each field from the headers in the request and give you the Pydantic model you defined.

You can see the required headers in the docs UI at /docs:

In some special use cases (probably not very common), you might want to restrict the headers that you want to receive.

You can use Pydantic's model configuration to forbid any extra fields:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

If a client tries to send some extra headers, they will receive an error response.

For example, if the client tries to send a tool header with a value of plumbus, they will receive an error response telling them that the header parameter tool is not allowed:

The same way as with regular header parameters, when you have underscore characters in the parameter names, they are automatically converted to hyphens.

For example, if you have a header parameter save_data in the code, the expected HTTP header will be save-data, and it will show up like that in the docs.

If for some reason you need to disable this automatic conversion, you can do it as well for Pydantic models for header parameters.

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Before setting convert_underscores to False, bear in mind that some HTTP proxies and servers disallow the usage of headers with underscores.

You can use Pydantic models to declare headers in FastAPI. 😎

**Examples:**

Example 1 (python):
```python
from typing import Annotated

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []


@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers
```

Example 2 (python):
```python
from typing import Annotated, Union

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: Union[str, None] = None
    traceparent: Union[str, None] = None
    x_tag: list[str] = []


@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers
```

Example 3 (python):
```python
from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []


@app.get("/items/")
async def read_items(headers: CommonHeaders = Header()):
    return headers
```

Example 4 (python):
```python
from typing import Union

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: Union[str, None] = None
    traceparent: Union[str, None] = None
    x_tag: list[str] = []


@app.get("/items/")
async def read_items(headers: CommonHeaders = Header()):
    return headers
```

---

## Debugging¶

**URL:** https://fastapi.tiangolo.com/tutorial/debugging/

**Contents:**
- Debugging¶
- Call uvicorn¶
  - About __name__ == "__main__"¶
    - More details¶
- Run your code with your debugger¶

You can connect the debugger in your editor, for example with Visual Studio Code or PyCharm.

In your FastAPI application, import and run uvicorn directly:

The main purpose of the __name__ == "__main__" is to have some code that is executed when your file is called with:

but is not called when another file imports it, like in:

Let's say your file is named myapp.py.

then the internal variable __name__ in your file, created automatically by Python, will have as value the string "__main__".

This won't happen if you import that module (file).

So, if you have another file importer.py with:

in that case, the automatically created variable __name__ inside of myapp.py will not have the value "__main__".

will not be executed.

For more information, check the official Python docs.

Because you are running the Uvicorn server directly from your code, you can call your Python program (your FastAPI application) directly from the debugger.

For example, in Visual Studio Code, you can:

It will then start the server with your FastAPI code, stop at your breakpoints, etc.

Here's how it might look:

If you use Pycharm, you can:

It will then start the server with your FastAPI code, stop at your breakpoints, etc.

Here's how it might look:

**Examples:**

Example 1 (python):
```python
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    a = "a"
    b = "b" + a
    return {"hello world": b}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Example 2 (python):
```python
from myapp import app
```

Example 3 (unknown):
```unknown
uvicorn.run(app, host="0.0.0.0", port=8000)
```

Example 4 (python):
```python
from myapp import app

# Some more code
```

---

## Server Workers - Uvicorn with Workers¶

**URL:** https://fastapi.tiangolo.com/deployment/server-workers/

**Contents:**
- Server Workers - Uvicorn with Workers¶
- Multiple Workers¶
- Deployment Concepts¶
- Containers and Docker¶
- Recap¶

Let's check back those deployment concepts from before:

Up to this point, with all the tutorials in the docs, you have probably been running a server program, for example, using the fastapi command, that runs Uvicorn, running a single process.

When deploying applications you will probably want to have some replication of processes to take advantage of multiple cores and to be able to handle more requests.

As you saw in the previous chapter about Deployment Concepts, there are multiple strategies you can use.

Here I'll show you how to use Uvicorn with worker processes using the fastapi command or the uvicorn command directly.

If you are using containers, for example with Docker or Kubernetes, I'll tell you more about that in the next chapter: FastAPI in Containers - Docker.

In particular, when running on Kubernetes you will probably not want to use workers and instead run a single Uvicorn process per container, but I'll tell you about it later in that chapter.

You can start multiple workers with the --workers command line option:

If you use the fastapi command:

If you prefer to use the uvicorn command directly:

The only new option here is --workers telling Uvicorn to start 4 worker processes.

You can also see that it shows the PID of each process, 27365 for the parent process (this is the process manager) and one for each worker process: 27368, 27369, 27370, and 27367.

Here you saw how to use multiple workers to parallelize the execution of the application, take advantage of multiple cores in the CPU, and be able to serve more requests.

From the list of deployment concepts from above, using workers would mainly help with the replication part, and a little bit with the restarts, but you still need to take care of the others:

In the next chapter about FastAPI in Containers - Docker I'll explain some strategies you could use to handle the other deployment concepts.

I'll show you how to build your own image from scratch to run a single Uvicorn process. It is a simple process and is probably what you would want to do when using a distributed container management system like Kubernetes.

You can use multiple worker processes with the --workers CLI option with the fastapi or uvicorn commands to take advantage of multi-core CPUs, to run multiple processes in parallel.

You could use these tools and ideas if you are setting up your own deployment system while taking care of the other deployment concepts yourself.

Check out the next chapter to learn about FastAPI with containers (e.g. Docker and Kubernetes). You will see that those tools have simple ways to solve the other deployment concepts as well. ✨

---

## Status Codes¶

**URL:** https://fastapi.tiangolo.com/reference/status/

**Contents:**
- Status Codes¶
- Example¶
- fastapi.status ¶
  - HTTP_100_CONTINUE module-attribute ¶
  - HTTP_101_SWITCHING_PROTOCOLS module-attribute ¶
  - HTTP_102_PROCESSING module-attribute ¶
  - HTTP_103_EARLY_HINTS module-attribute ¶
  - HTTP_200_OK module-attribute ¶
  - HTTP_201_CREATED module-attribute ¶
  - HTTP_202_ACCEPTED module-attribute ¶

You can import the status module from fastapi:

status is provided directly by Starlette.

It contains a group of named constants (variables) with integer status codes.

It can be convenient to quickly access HTTP (and WebSocket) status codes in your app, using autocompletion for the name without having to remember the integer status codes by memory.

Read more about it in the FastAPI docs about Response Status Code.

HTTP codes See HTTP Status Code Registry: https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml

And RFC 9110 - https://www.rfc-editor.org/rfc/rfc9110

WebSocket codes https://www.iana.org/assignments/websocket/websocket.xml#close-code-number https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent

**Examples:**

Example 1 (python):
```python
from fastapi import status
```

Example 2 (python):
```python
from fastapi import FastAPI, status

app = FastAPI()


@app.get("/items/", status_code=status.HTTP_418_IM_A_TEAPOT)
def read_items():
    return [{"name": "Plumbus"}, {"name": "Portal Gun"}]
```

Example 3 (unknown):
```unknown
HTTP_100_CONTINUE = 100
```

Example 4 (unknown):
```unknown
HTTP_101_SWITCHING_PROTOCOLS = 101
```

---

## Custom Docs UI Static Assets (Self-Hosting)¶

**URL:** https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/

**Contents:**
- Custom Docs UI Static Assets (Self-Hosting)¶
- Custom CDN for JavaScript and CSS¶
  - Disable the automatic docs¶
  - Include the custom docs¶
  - Create a path operation to test it¶
  - Test it¶
- Self-hosting JavaScript and CSS for docs¶
  - Project file structure¶
  - Download the files¶
  - Serve the static files¶

The API docs use Swagger UI and ReDoc, and each of those need some JavaScript and CSS files.

By default, those files are served from a CDN.

But it's possible to customize it, you can set a specific CDN, or serve the files yourself.

Let's say that you want to use a different CDN, for example you want to use https://unpkg.com/.

This could be useful if for example you live in a country that restricts some URLs.

The first step is to disable the automatic docs, as by default, those use the default CDN.

To disable them, set their URLs to None when creating your FastAPI app:

Now you can create the path operations for the custom docs.

You can reuse FastAPI's internal functions to create the HTML pages for the docs, and pass them the needed arguments:

And similarly for ReDoc...

The path operation for swagger_ui_redirect is a helper for when you use OAuth2.

If you integrate your API with an OAuth2 provider, you will be able to authenticate and come back to the API docs with the acquired credentials. And interact with it using the real OAuth2 authentication.

Swagger UI will handle it behind the scenes for you, but it needs this "redirect" helper.

Now, to be able to test that everything works, create a path operation:

Now, you should be able to go to your docs at http://127.0.0.1:8000/docs, and reload the page, it will load those assets from the new CDN.

Self-hosting the JavaScript and CSS could be useful if, for example, you need your app to keep working even while offline, without open Internet access, or in a local network.

Here you'll see how to serve those files yourself, in the same FastAPI app, and configure the docs to use them.

Let's say your project file structure looks like this:

Now create a directory to store those static files.

Your new file structure could look like this:

Download the static files needed for the docs and put them on that static/ directory.

You can probably right-click each link and select an option similar to "Save link as...".

Swagger UI uses the files:

And ReDoc uses the file:

After that, your file structure could look like:

Start your application and go to http://127.0.0.1:8000/static/redoc.standalone.js.

You should see a very long JavaScript file for ReDoc.

It could start with something like:

That confirms that you are being able to serve static files from your app, and that you placed the static files for the docs in the correct place.

Now we can configure the app to use those static files for the docs.

The same as when using a custom CDN, the first step is to disable the automatic docs, as those use the CDN by default.

To disable them, set their URLs to None when creating your FastAPI app:

And the same way as with a custom CDN, now you can create the path operations for the custom docs.

Again, you can reuse FastAPI's internal functions to create the HTML pages for the docs, and pass them the needed arguments:

And similarly for ReDoc...

The path operation for swagger_ui_redirect is a helper for when you use OAuth2.

If you integrate your API with an OAuth2 provider, you will be able to authenticate and come back to the API docs with the acquired credentials. And interact with it using the real OAuth2 authentication.

Swagger UI will handle it behind the scenes for you, but it needs this "redirect" helper.

Now, to be able to test that everything works, create a path operation:

Now, you should be able to disconnect your WiFi, go to your docs at http://127.0.0.1:8000/docs, and reload the page.

And even without Internet, you would be able to see the docs for your API and interact with it.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@2/bundles/redoc.standalone.js",
    )


@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}
```

Example 2 (python):
```python
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@2/bundles/redoc.standalone.js",
    )


@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}
```

Example 3 (python):
```python
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@2/bundles/redoc.standalone.js",
    )


@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}
```

Example 4 (unknown):
```unknown
.
├── app
│   ├── __init__.py
│   ├── main.py
```

---

## FastAPI in Containers - Docker¶

**URL:** https://fastapi.tiangolo.com/deployment/docker/

**Contents:**
- FastAPI in Containers - Docker¶
- What is a Container¶
- What is a Container Image¶
- Container Images¶
- Containers and Processes¶
- Build a Docker Image for FastAPI¶
  - Package Requirements¶
  - Create the FastAPI Code¶
  - Dockerfile¶
    - Use CMD - Exec Form¶

When deploying FastAPI applications a common approach is to build a Linux container image. It's normally done using Docker. You can then deploy that container image in one of a few possible ways.

Using Linux containers has several advantages including security, replicability, simplicity, and others.

In a hurry and already know this stuff? Jump to the Dockerfile below 👇.

Containers (mainly Linux containers) are a very lightweight way to package applications including all their dependencies and necessary files while keeping them isolated from other containers (other applications or components) in the same system.

Linux containers run using the same Linux kernel of the host (machine, virtual machine, cloud server, etc). This just means that they are very lightweight (compared to full virtual machines emulating an entire operating system).

This way, containers consume little resources, an amount comparable to running the processes directly (a virtual machine would consume much more).

Containers also have their own isolated running processes (commonly just one process), file system, and network, simplifying deployment, security, development, etc.

A container is run from a container image.

A container image is a static version of all the files, environment variables, and the default command/program that should be present in a container. Static here means that the container image is not running, it's not being executed, it's only the packaged files and metadata.

In contrast to a "container image" that is the stored static contents, a "container" normally refers to the running instance, the thing that is being executed.

When the container is started and running (started from a container image) it could create or change files, environment variables, etc. Those changes will exist only in that container, but would not persist in the underlying container image (would not be saved to disk).

A container image is comparable to the program file and contents, e.g. python and some file main.py.

And the container itself (in contrast to the container image) is the actual running instance of the image, comparable to a process. In fact, a container is running only when it has a process running (and normally it's only a single process). The container stops when there's no process running in it.

Docker has been one of the main tools to create and manage container images and containers.

And there's a public Docker Hub with pre-made official container images for many tools, environments, databases, and applications.

For example, there's an official Python Image.

And there are many other images for different things like databases, for example for:

By using a pre-made container image it's very easy to combine and use different tools. For example, to try out a new database. In most cases, you can use the official images, and just configure them with environment variables.

That way, in many cases you can learn about containers and Docker and reuse that knowledge with many different tools and components.

So, you would run multiple containers with different things, like a database, a Python application, a web server with a React frontend application, and connect them together via their internal network.

All the container management systems (like Docker or Kubernetes) have these networking features integrated into them.

A container image normally includes in its metadata the default program or command that should be run when the container is started and the parameters to be passed to that program. Very similar to what would be if it was in the command line.

When a container is started, it will run that command/program (although you can override it and make it run a different command/program).

A container is running as long as the main process (command or program) is running.

A container normally has a single process, but it's also possible to start subprocesses from the main process, and that way you will have multiple processes in the same container.

But it's not possible to have a running container without at least one running process. If the main process stops, the container stops.

Okay, let's build something now! 🚀

I'll show you how to build a Docker image for FastAPI from scratch, based on the official Python image.

This is what you would want to do in most cases, for example:

You would normally have the package requirements for your application in some file.

It would depend mainly on the tool you use to install those requirements.

The most common way to do it is to have a file requirements.txt with the package names and their versions, one per line.

You would of course use the same ideas you read in About FastAPI versions to set the ranges of versions.

For example, your requirements.txt could look like:

And you would normally install those package dependencies with pip, for example:

There are other formats and tools to define and install package dependencies.

Now in the same project directory create a file Dockerfile with:

Review what each line does by clicking each number bubble in the code. 👆

Make sure to always use the exec form of the CMD instruction, as explained below.

The CMD Docker instruction can be written using two forms:

Make sure to always use the exec form to ensure that FastAPI can shutdown gracefully and lifespan events are triggered.

You can read more about it in the Docker docs for shell and exec form.

This can be quite noticeable when using docker compose. See this Docker Compose FAQ section for more technical details: Why do my services take 10 seconds to recreate or stop?.

You should now have a directory structure like:

If you are running your container behind a TLS Termination Proxy (load balancer) like Nginx or Traefik, add the option --proxy-headers, this will tell Uvicorn (through the FastAPI CLI) to trust the headers sent by that proxy telling it that the application is running behind HTTPS, etc.

There's an important trick in this Dockerfile, we first copy the file with the dependencies alone, not the rest of the code. Let me tell you why is that.

Docker and other tools build these container images incrementally, adding one layer on top of the other, starting from the top of the Dockerfile and adding any files created by each of the instructions of the Dockerfile.

Docker and similar tools also use an internal cache when building the image, if a file hasn't changed since the last time building the container image, then it will reuse the same layer created the last time, instead of copying the file again and creating a new layer from scratch.

Just avoiding the copy of files doesn't necessarily improve things too much, but because it used the cache for that step, it can use the cache for the next step. For example, it could use the cache for the instruction that installs dependencies with:

The file with the package requirements won't change frequently. So, by copying only that file, Docker will be able to use the cache for that step.

And then, Docker will be able to use the cache for the next step that downloads and install those dependencies. And here's where we save a lot of time. ✨ ...and avoid boredom waiting. 😪😆

Downloading and installing the package dependencies could take minutes, but using the cache would take seconds at most.

And as you would be building the container image again and again during development to check that your code changes are working, there's a lot of accumulated time this would save.

Then, near the end of the Dockerfile, we copy all the code. As this is what changes most frequently, we put it near the end, because almost always, anything after this step will not be able to use the cache.

Now that all the files are in place, let's build the container image.

Notice the . at the end, it's equivalent to ./, it tells Docker the directory to use to build the container image.

In this case, it's the same current directory (.).

You should be able to check it in your Docker container's URL, for example: http://192.168.99.100/items/5?q=somequery or http://127.0.0.1/items/5?q=somequery (or equivalent, using your Docker host).

You will see something like:

Now you can go to http://192.168.99.100/docs or http://127.0.0.1/docs (or equivalent, using your Docker host).

You will see the automatic interactive API documentation (provided by Swagger UI):

And you can also go to http://192.168.99.100/redoc or http://127.0.0.1/redoc (or equivalent, using your Docker host).

You will see the alternative automatic documentation (provided by ReDoc):

If your FastAPI is a single file, for example, main.py without an ./app directory, your file structure could look like this:

Then you would just have to change the corresponding paths to copy the file inside the Dockerfile:

When you pass the file to fastapi run it will detect automatically that it is a single file and not part of a package and will know how to import it and serve your FastAPI app. 😎

Let's talk again about some of the same Deployment Concepts in terms of containers.

Containers are mainly a tool to simplify the process of building and deploying an application, but they don't enforce a particular approach to handle these deployment concepts, and there are several possible strategies.

The good news is that with each different strategy there's a way to cover all of the deployment concepts. 🎉

Let's review these deployment concepts in terms of containers:

If we focus just on the container image for a FastAPI application (and later the running container), HTTPS normally would be handled externally by another tool.

It could be another container, for example with Traefik, handling HTTPS and automatic acquisition of certificates.

Traefik has integrations with Docker, Kubernetes, and others, so it's very easy to set up and configure HTTPS for your containers with it.

Alternatively, HTTPS could be handled by a cloud provider as one of their services (while still running the application in a container).

There is normally another tool in charge of starting and running your container.

It could be Docker directly, Docker Compose, Kubernetes, a cloud service, etc.

In most (or all) cases, there's a simple option to enable running the container on startup and enabling restarts on failures. For example, in Docker, it's the command line option --restart.

Without using containers, making applications run on startup and with restarts can be cumbersome and difficult. But when working with containers in most cases that functionality is included by default. ✨

If you have a cluster of machines with Kubernetes, Docker Swarm Mode, Nomad, or another similar complex system to manage distributed containers on multiple machines, then you will probably want to handle replication at the cluster level instead of using a process manager (like Uvicorn with workers) in each container.

One of those distributed container management systems like Kubernetes normally has some integrated way of handling replication of containers while still supporting load balancing for the incoming requests. All at the cluster level.

In those cases, you would probably want to build a Docker image from scratch as explained above, installing your dependencies, and running a single Uvicorn process instead of using multiple Uvicorn workers.

When using containers, you would normally have some component listening on the main port. It could possibly be another container that is also a TLS Termination Proxy to handle HTTPS or some similar tool.

As this component would take the load of requests and distribute that among the workers in a (hopefully) balanced way, it is also commonly called a Load Balancer.

The same TLS Termination Proxy component used for HTTPS would probably also be a Load Balancer.

And when working with containers, the same system you use to start and manage them would already have internal tools to transmit the network communication (e.g. HTTP requests) from that load balancer (that could also be a TLS Termination Proxy) to the container(s) with your app.

When working with Kubernetes or similar distributed container management systems, using their internal networking mechanisms would allow the single load balancer that is listening on the main port to transmit communication (requests) to possibly multiple containers running your app.

Each of these containers running your app would normally have just one process (e.g. a Uvicorn process running your FastAPI application). They would all be identical containers, running the same thing, but each with its own process, memory, etc. That way you would take advantage of parallelization in different cores of the CPU, or even in different machines.

And the distributed container system with the load balancer would distribute the requests to each one of the containers with your app in turns. So, each request could be handled by one of the multiple replicated containers running your app.

And normally this load balancer would be able to handle requests that go to other apps in your cluster (e.g. to a different domain, or under a different URL path prefix), and would transmit that communication to the right containers for that other application running in your cluster.

In this type of scenario, you probably would want to have a single (Uvicorn) process per container, as you would already be handling replication at the cluster level.

So, in this case, you would not want to have a multiple workers in the container, for example with the --workers command line option. You would want to have just a single Uvicorn process per container (but probably multiple containers).

Having another process manager inside the container (as would be with multiple workers) would only add unnecessary complexity that you are most probably already taking care of with your cluster system.

Of course, there are special cases where you could want to have a container with several Uvicorn worker processes inside.

In those cases, you can use the --workers command line option to set the number of workers that you want to run:

Here are some examples of when that could make sense:

You could want a process manager in the container if your application is simple enough that can run it on a single server, not a cluster.

You could be deploying to a single server (not a cluster) with Docker Compose, so you wouldn't have an easy way to manage replication of containers (with Docker Compose) while preserving the shared network and load balancing.

Then you could want to have a single container with a process manager starting several worker processes inside.

The main point is, none of these are rules written in stone that you have to blindly follow. You can use these ideas to evaluate your own use case and decide what is the best approach for your system, checking out how to manage the concepts of:

If you run a single process per container you will have a more or less well-defined, stable, and limited amount of memory consumed by each of those containers (more than one if they are replicated).

And then you can set those same memory limits and requirements in your configurations for your container management system (for example in Kubernetes). That way it will be able to replicate the containers in the available machines taking into account the amount of memory needed by them, and the amount available in the machines in the cluster.

If your application is simple, this will probably not be a problem, and you might not need to specify hard memory limits. But if you are using a lot of memory (for example with machine learning models), you should check how much memory you are consuming and adjust the number of containers that runs in each machine (and maybe add more machines to your cluster).

If you run multiple processes per container you will have to make sure that the number of processes started doesn't consume more memory than what is available.

If you are using containers (e.g. Docker, Kubernetes), then there are two main approaches you can use.

If you have multiple containers, probably each one running a single process (for example, in a Kubernetes cluster), then you would probably want to have a separate container doing the work of the previous steps in a single container, running a single process, before running the replicated worker containers.

If you are using Kubernetes, this would probably be an Init Container.

If in your use case there's no problem in running those previous steps multiple times in parallel (for example if you are not running database migrations, but just checking if the database is ready yet), then you could also just put them in each container right before starting the main process.

If you have a simple setup, with a single container that then starts multiple worker processes (or also just one process), then you could run those previous steps in the same container, right before starting the process with the app.

There used to be an official FastAPI Docker image: tiangolo/uvicorn-gunicorn-fastapi. But it is now deprecated. ⛔️

You should probably not use this base Docker image (or any other similar one).

If you are using Kubernetes (or others) and you are already setting replication at the cluster level, with multiple containers. In those cases, you are better off building an image from scratch as described above: Build a Docker Image for FastAPI.

And if you need to have multiple workers, you can simply use the --workers command line option.

The Docker image was created when Uvicorn didn't support managing and restarting dead workers, so it was needed to use Gunicorn with Uvicorn, which added quite some complexity, just to have Gunicorn manage and restart the Uvicorn worker processes.

But now that Uvicorn (and the fastapi command) support using --workers, there's no reason to use a base Docker image instead of building your own (it's pretty much the same amount of code 😅).

After having a Container (Docker) Image there are several ways to deploy it.

If you are using uv to install and manage your project, you can follow their uv Docker guide.

Using container systems (e.g. with Docker and Kubernetes) it becomes fairly straightforward to handle all the deployment concepts:

In most cases, you probably won't want to use any base image, and instead build a container image from scratch based on the official Python Docker image.

Taking care of the order of instructions in the Dockerfile and the Docker cache you can minimize build times, to maximize your productivity (and avoid boredom). 😎

**Examples:**

Example 1 (sql):
```sql
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
```

Example 2 (unknown):
```unknown
fastapi[standard]>=0.113.0,<0.114.0
pydantic>=2.7.0,<3.0.0
```

Example 3 (python):
```python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

Example 4 (sql):
```sql
FROM python:3.9


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./app /code/app


CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

---

## FastAPI¶

**URL:** https://fastapi.tiangolo.com/

**Contents:**
- FastAPI¶
- Sponsors¶
  - Keystone Sponsor¶
  - Gold and Silver Sponsors¶
- Opinions¶
- FastAPI mini documentary¶
- Typer, the FastAPI of CLIs¶
- Requirements¶
- Installation¶
- Example¶

FastAPI framework, high performance, easy to learn, fast to code, ready for production

Documentation: https://fastapi.tiangolo.com

Source Code: https://github.com/fastapi/fastapi

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.

The key features are:

* estimation based on tests conducted by an internal development team, building production applications.

"[...] I'm using FastAPI a ton these days. [...] I'm actually planning to use it for all of my team's ML services at Microsoft. Some of them are getting integrated into the core Windows product and some Office products."

"We adopted the FastAPI library to spawn a REST server that can be queried to obtain predictions. [for Ludwig]"

"Netflix is pleased to announce the open-source release of our crisis management orchestration framework: Dispatch! [built with FastAPI]"

"I’m over the moon excited about FastAPI. It’s so fun!"

"Honestly, what you've built looks super solid and polished. In many ways, it's what I wanted Hug to be - it's really inspiring to see someone build that."

"If you're looking to learn one modern framework for building REST APIs, check out FastAPI [...] It's fast, easy to use and easy to learn [...]"

"We've switched over to FastAPI for our APIs [...] I think you'll like it [...]"

"If anyone is looking to build a production Python API, I would highly recommend FastAPI. It is beautifully designed, simple to use and highly scalable, it has become a key component in our API first development strategy and is driving many automations and services such as our Virtual TAC Engineer."

There's a FastAPI mini documentary released at the end of 2025, you can watch it online:

If you are building a CLI app to be used in the terminal instead of a web API, check out Typer.

Typer is FastAPI's little sibling. And it's intended to be the FastAPI of CLIs. ⌨️ 🚀

FastAPI stands on the shoulders of giants:

Create and activate a virtual environment and then install FastAPI:

Note: Make sure you put "fastapi[standard]" in quotes to ensure it works in all terminals.

Create a file main.py with:

If your code uses async / await, use async def:

If you don't know, check the "In a hurry?" section about async and await in the docs.

The command fastapi dev reads your main.py file, detects the FastAPI app in it, and starts a server using Uvicorn.

By default, fastapi dev will start with auto-reload enabled for local development.

You can read more about it in the FastAPI CLI docs.

Open your browser at http://127.0.0.1:8000/items/5?q=somequery.

You will see the JSON response as:

You already created an API that:

Now go to http://127.0.0.1:8000/docs.

You will see the automatic interactive API documentation (provided by Swagger UI):

And now, go to http://127.0.0.1:8000/redoc.

You will see the alternative automatic documentation (provided by ReDoc):

Now modify the file main.py to receive a body from a PUT request.

Declare the body using standard Python types, thanks to Pydantic.

The fastapi dev server should reload automatically.

Now go to http://127.0.0.1:8000/docs.

And now, go to http://127.0.0.1:8000/redoc.

In summary, you declare once the types of parameters, body, etc. as function parameters.

You do that with standard modern Python types.

You don't have to learn a new syntax, the methods or classes of a specific library, etc.

Just standard Python.

For example, for an int:

or for a more complex Item model:

...and with that single declaration you get:

Coming back to the previous code example, FastAPI will:

We just scratched the surface, but you already get the idea of how it all works.

Try changing the line with:

...and see how your editor will auto-complete the attributes and know their types:

For a more complete example including more features, see the Tutorial - User Guide.

Spoiler alert: the tutorial - user guide includes:

You can optionally deploy your FastAPI app to FastAPI Cloud, go and join the waiting list if you haven't. 🚀

If you already have a FastAPI Cloud account (we invited you from the waiting list 😉), you can deploy your application with one command.

Before deploying, make sure you are logged in:

Then deploy your app:

That's it! Now you can access your app at that URL. ✨

FastAPI Cloud is built by the same author and team behind FastAPI.

It streamlines the process of building, deploying, and accessing an API with minimal effort.

It brings the same developer experience of building apps with FastAPI to deploying them to the cloud. 🎉

FastAPI Cloud is the primary sponsor and funding provider for the FastAPI and friends open source projects. ✨

FastAPI is open source and based on standards. You can deploy FastAPI apps to any cloud provider you choose.

Follow your cloud provider's guides to deploy FastAPI apps with them. 🤓

Independent TechEmpower benchmarks show FastAPI applications running under Uvicorn as one of the fastest Python frameworks available, only below Starlette and Uvicorn themselves (used internally by FastAPI). (*)

To understand more about it, see the section Benchmarks.

FastAPI depends on Pydantic and Starlette.

When you install FastAPI with pip install "fastapi[standard]" it comes with the standard group of optional dependencies:

If you don't want to include the standard optional dependencies, you can install with pip install fastapi instead of pip install "fastapi[standard]".

If you want to install FastAPI with the standard dependencies but without the fastapi-cloud-cli, you can install with pip install "fastapi[standard-no-fastapi-cloud-cli]".

There are some additional dependencies you might want to install.

Additional optional Pydantic dependencies:

Additional optional FastAPI dependencies:

This project is licensed under the terms of the MIT license.

**Examples:**

Example 1 (python):
```python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

Example 2 (python):
```python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

Example 3 (json):
```json
{"item_id": 5, "q": "somequery"}
```

Example 4 (python):
```python
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

---

## GraphQL¶

**URL:** https://fastapi.tiangolo.com/how-to/graphql/

**Contents:**
- GraphQL¶
- GraphQL Libraries¶
- GraphQL with Strawberry¶
- Older GraphQLApp from Starlette¶
- Learn More¶

As FastAPI is based on the ASGI standard, it's very easy to integrate any GraphQL library also compatible with ASGI.

You can combine normal FastAPI path operations with GraphQL on the same application.

GraphQL solves some very specific use cases.

It has advantages and disadvantages when compared to common web APIs.

Make sure you evaluate if the benefits for your use case compensate the drawbacks. 🤓

Here are some of the GraphQL libraries that have ASGI support. You could use them with FastAPI:

If you need or want to work with GraphQL, Strawberry is the recommended library as it has the design closest to FastAPI's design, it's all based on type annotations.

Depending on your use case, you might prefer to use a different library, but if you asked me, I would probably suggest you try Strawberry.

Here's a small preview of how you could integrate Strawberry with FastAPI:

You can learn more about Strawberry in the Strawberry documentation.

And also the docs about Strawberry with FastAPI.

Previous versions of Starlette included a GraphQLApp class to integrate with Graphene.

It was deprecated from Starlette, but if you have code that used it, you can easily migrate to starlette-graphene3, that covers the same use case and has an almost identical interface.

If you need GraphQL, I still would recommend you check out Strawberry, as it's based on type annotations instead of custom classes and types.

You can learn more about GraphQL in the official GraphQL documentation.

You can also read more about each those libraries described above in their links.

**Examples:**

Example 1 (python):
```python
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter


@strawberry.type
class User:
    name: str
    age: int


@strawberry.type
class Query:
    @strawberry.field
    def user(self) -> User:
        return User(name="Patrick", age=100)


schema = strawberry.Schema(query=Query)


graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
```

---

## Reference¶

**URL:** https://fastapi.tiangolo.com/reference/

**Contents:**
- Reference¶

Here's the reference or code API, the classes, functions, parameters, attributes, and all the FastAPI parts you can use in your applications.

If you want to learn FastAPI you are much better off reading the FastAPI Tutorial.

---

## Deployment¶

**URL:** https://fastapi.tiangolo.com/deployment/

**Contents:**
- Deployment¶
- What Does Deployment Mean¶
- Deployment Strategies¶

Deploying a FastAPI application is relatively easy.

To deploy an application means to perform the necessary steps to make it available to the users.

For a web API, it normally involves putting it in a remote machine, with a server program that provides good performance, stability, etc, so that your users can access the application efficiently and without interruptions or problems.

This is in contrast to the development stages, where you are constantly changing the code, breaking it and fixing it, stopping and restarting the development server, etc.

There are several ways to do it depending on your specific use case and the tools that you use.

You could deploy a server yourself using a combination of tools, you could use a cloud service that does part of the work for you, or other possible options.

For example, we, the team behind FastAPI, built FastAPI Cloud, to make deploying FastAPI apps to the cloud as streamlined as possible, with the same developer experience of working with FastAPI.

I will show you some of the main concepts you should probably keep in mind when deploying a FastAPI application (although most of it applies to any other type of web application).

You will see more details to keep in mind and some of the techniques to do it in the next sections. ✨

---

## Additional Status Codes¶

**URL:** https://fastapi.tiangolo.com/advanced/additional-status-codes/

**Contents:**
- Additional Status Codes¶
- Additional status codes¶
- OpenAPI and API docs¶

By default, FastAPI will return the responses using a JSONResponse, putting the content you return from your path operation inside of that JSONResponse.

It will use the default status code or the one you set in your path operation.

If you want to return additional status codes apart from the main one, you can do that by returning a Response directly, like a JSONResponse, and set the additional status code directly.

For example, let's say that you want to have a path operation that allows to update items, and returns HTTP status codes of 200 "OK" when successful.

But you also want it to accept new items. And when the items didn't exist before, it creates them, and returns an HTTP status code of 201 "Created".

To achieve that, import JSONResponse, and return your content there directly, setting the status_code that you want:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

When you return a Response directly, like in the example above, it will be returned directly.

It won't be serialized with a model, etc.

Make sure it has the data you want it to have, and that the values are valid JSON (if you are using JSONResponse).

You could also use from starlette.responses import JSONResponse.

FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette. The same with status.

If you return additional status codes and responses directly, they won't be included in the OpenAPI schema (the API docs), because FastAPI doesn't have a way to know beforehand what you are going to return.

But you can document that in your code, using: Additional Responses.

**Examples:**

Example 1 (python):
```python
from typing import Annotated

from fastapi import Body, FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

items = {"foo": {"name": "Fighters", "size": 6}, "bar": {"name": "Tenders", "size": 3}}


@app.put("/items/{item_id}")
async def upsert_item(
    item_id: str,
    name: Annotated[str | None, Body()] = None,
    size: Annotated[int | None, Body()] = None,
):
    if item_id in items:
        item = items[item_id]
        item["name"] = name
        item["size"] = size
        return item
    else:
        item = {"name": name, "size": size}
        items[item_id] = item
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)
```

Example 2 (python):
```python
from typing import Annotated, Union

from fastapi import Body, FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

items = {"foo": {"name": "Fighters", "size": 6}, "bar": {"name": "Tenders", "size": 3}}


@app.put("/items/{item_id}")
async def upsert_item(
    item_id: str,
    name: Annotated[Union[str, None], Body()] = None,
    size: Annotated[Union[int, None], Body()] = None,
):
    if item_id in items:
        item = items[item_id]
        item["name"] = name
        item["size"] = size
        return item
    else:
        item = {"name": name, "size": size}
        items[item_id] = item
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)
```

Example 3 (python):
```python
from fastapi import Body, FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

items = {"foo": {"name": "Fighters", "size": 6}, "bar": {"name": "Tenders", "size": 3}}


@app.put("/items/{item_id}")
async def upsert_item(
    item_id: str,
    name: str | None = Body(default=None),
    size: int | None = Body(default=None),
):
    if item_id in items:
        item = items[item_id]
        item["name"] = name
        item["size"] = size
        return item
    else:
        item = {"name": name, "size": size}
        items[item_id] = item
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)
```

Example 4 (python):
```python
from typing import Union

from fastapi import Body, FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

items = {"foo": {"name": "Fighters", "size": 6}, "bar": {"name": "Tenders", "size": 3}}


@app.put("/items/{item_id}")
async def upsert_item(
    item_id: str,
    name: Union[str, None] = Body(default=None),
    size: Union[int, None] = Body(default=None),
):
    if item_id in items:
        item = items[item_id]
        item["name"] = name
        item["size"] = size
        return item
    else:
        item = {"name": name, "size": size}
        items[item_id] = item
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)
```

---

## UploadFile class¶

**URL:** https://fastapi.tiangolo.com/reference/uploadfile/

**Contents:**
- UploadFile class¶
- fastapi.UploadFile ¶
    - Example¶
  - file instance-attribute ¶
  - filename instance-attribute ¶
  - size instance-attribute ¶
  - headers instance-attribute ¶
  - content_type instance-attribute ¶
  - read async ¶
  - write async ¶

You can define path operation function parameters to be of the type UploadFile to receive files from the request.

You can import it directly from fastapi:

A file uploaded in a request.

Define it as a path operation function (or dependency) parameter.

If you are using a regular def function, you can use the upload_file.file attribute to access the raw standard Python file (blocking, not async), useful and needed for non-async code.

Read more about it in the FastAPI docs for Request Files.

The standard Python file object (non-async).

The original file name.

The size of the file in bytes.

The headers of the request.

The content type of the request, from the headers.

Read some bytes from the file.

To be awaitable, compatible with async, this is run in threadpool.

The number of bytes to read from the file.

TYPE: int DEFAULT: -1

Write some bytes to the file.

You normally wouldn't use this from a file you read in a request.

To be awaitable, compatible with async, this is run in threadpool.

The bytes to write to the file.

Move to a position in the file.

Any next read or write will be done from that position.

To be awaitable, compatible with async, this is run in threadpool.

The position in bytes to seek to in the file.

To be awaitable, compatible with async, this is run in threadpool.

**Examples:**

Example 1 (python):
```python
from fastapi import UploadFile
```

Example 2 (rust):
```rust
UploadFile(file, *, size=None, filename=None, headers=None)
```

Example 3 (python):
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

Example 4 (python):
```python
def __init__(
    self,
    file: BinaryIO,
    *,
    size: int | None = None,
    filename: str | None = None,
    headers: Headers | None = None,
) -> None:
    self.filename = filename
    self.file = file
    self.size = size
    self.headers = headers or Headers()

    # Capture max size from SpooledTemporaryFile if one is provided. This slightly speeds up future checks.
    # Note 0 means unlimited mirroring SpooledTemporaryFile's __init__
    self._max_mem_size = getattr(self.file, "_max_size", 0)
```

---

## How To - Recipes¶

**URL:** https://fastapi.tiangolo.com/how-to/

**Contents:**
- How To - Recipes¶

Here you will see different recipes or "how to" guides for several topics.

Most of these ideas would be more or less independent, and in most cases you should only need to study them if they apply directly to your project.

If something seems interesting and useful to your project, go ahead and check it, but otherwise, you might probably just skip them.

If you want to learn FastAPI in a structured way (recommended), go and read the Tutorial - User Guide chapter by chapter instead.

---

## Response - Change Status Code¶

**URL:** https://fastapi.tiangolo.com/advanced/response-change-status-code/

**Contents:**
- Response - Change Status Code¶
- Use case¶
- Use a Response parameter¶

You probably read before that you can set a default Response Status Code.

But in some cases you need to return a different status code than the default.

For example, imagine that you want to return an HTTP status code of "OK" 200 by default.

But if the data didn't exist, you want to create it, and return an HTTP status code of "CREATED" 201.

But you still want to be able to filter and convert the data you return with a response_model.

For those cases, you can use a Response parameter.

You can declare a parameter of type Response in your path operation function (as you can do for cookies and headers).

And then you can set the status_code in that temporal response object.

And then you can return any object you need, as you normally would (a dict, a database model, etc).

And if you declared a response_model, it will still be used to filter and convert the object you returned.

FastAPI will use that temporal response to extract the status code (also cookies and headers), and will put them in the final response that contains the value you returned, filtered by any response_model.

You can also declare the Response parameter in dependencies, and set the status code in them. But keep in mind that the last one to be set will win.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI, Response, status

app = FastAPI()

tasks = {"foo": "Listen to the Bar Fighters"}


@app.put("/get-or-create-task/{task_id}", status_code=200)
def get_or_create_task(task_id: str, response: Response):
    if task_id not in tasks:
        tasks[task_id] = "This didn't exist before"
        response.status_code = status.HTTP_201_CREATED
    return tasks[task_id]
```

---

## Tutorial - User Guide¶

**URL:** https://fastapi.tiangolo.com/tutorial/

**Contents:**
- Tutorial - User Guide¶
- Run the code¶
- Install FastAPI¶
- Advanced User Guide¶

This tutorial shows you how to use FastAPI with most of its features, step by step.

Each section gradually builds on the previous ones, but it's structured to separate topics, so that you can go directly to any specific one to solve your specific API needs.

It is also built to work as a future reference so you can come back and see exactly what you need.

All the code blocks can be copied and used directly (they are actually tested Python files).

To run any of the examples, copy the code to a file main.py, and start fastapi dev with:

It is HIGHLY encouraged that you write or copy the code, edit it and run it locally.

Using it in your editor is what really shows you the benefits of FastAPI, seeing how little code you have to write, all the type checks, autocompletion, etc.

The first step is to install FastAPI.

Make sure you create a virtual environment, activate it, and then install FastAPI:

When you install with pip install "fastapi[standard]" it comes with some default optional standard dependencies, including fastapi-cloud-cli, which allows you to deploy to FastAPI Cloud.

If you don't want to have those optional dependencies, you can instead install pip install fastapi.

If you want to install the standard dependencies but without the fastapi-cloud-cli, you can install with pip install "fastapi[standard-no-fastapi-cloud-cli]".

There is also an Advanced User Guide that you can read later after this Tutorial - User guide.

The Advanced User Guide builds on this one, uses the same concepts, and teaches you some extra features.

But you should first read the Tutorial - User Guide (what you are reading right now).

It's designed so that you can build a complete application with just the Tutorial - User Guide, and then extend it in different ways, depending on your needs, using some of the additional ideas from the Advanced User Guide.

---

## JSON Compatible Encoder¶

**URL:** https://fastapi.tiangolo.com/tutorial/encoder/

**Contents:**
- JSON Compatible Encoder¶
- Using the jsonable_encoder¶

There are some cases where you might need to convert a data type (like a Pydantic model) to something compatible with JSON (like a dict, list, etc).

For example, if you need to store it in a database.

For that, FastAPI provides a jsonable_encoder() function.

Let's imagine that you have a database fake_db that only receives JSON compatible data.

For example, it doesn't receive datetime objects, as those are not compatible with JSON.

So, a datetime object would have to be converted to a str containing the data in ISO format.

The same way, this database wouldn't receive a Pydantic model (an object with attributes), only a dict.

You can use jsonable_encoder for that.

It receives an object, like a Pydantic model, and returns a JSON compatible version:

In this example, it would convert the Pydantic model to a dict, and the datetime to a str.

The result of calling it is something that can be encoded with the Python standard json.dumps().

It doesn't return a large str containing the data in JSON format (as a string). It returns a Python standard data structure (e.g. a dict) with values and sub-values that are all compatible with JSON.

jsonable_encoder is actually used by FastAPI internally to convert data. But it is useful in many other scenarios.

**Examples:**

Example 1 (python):
```python
from datetime import datetime

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None


app = FastAPI()


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
```

Example 2 (python):
```python
from datetime import datetime
from typing import Union

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Union[str, None] = None


app = FastAPI()


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
```

---

## Extra Data Types¶

**URL:** https://fastapi.tiangolo.com/tutorial/extra-data-types/

**Contents:**
- Extra Data Types¶
- Other data types¶
- Example¶

Up to now, you have been using common data types, like:

But you can also use more complex data types.

And you will still have the same features as seen up to now:

Here are some of the additional data types you can use:

Here's an example path operation with parameters using some of the above types.

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

Note that the parameters inside the function have their natural data type, and you can, for example, perform normal date manipulations, like:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

**Examples:**

Example 1 (python):
```python
from datetime import datetime, time, timedelta
from typing import Annotated
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()


@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[time | None, Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }
```

Example 2 (python):
```python
from datetime import datetime, time, timedelta
from typing import Annotated, Union
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()


@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[Union[time, None], Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }
```

Example 3 (python):
```python
from datetime import datetime, time, timedelta
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()


@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: datetime = Body(),
    end_datetime: datetime = Body(),
    process_after: timedelta = Body(),
    repeat_at: time | None = Body(default=None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }
```

Example 4 (python):
```python
from datetime import datetime, time, timedelta
from typing import Union
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()


@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: datetime = Body(),
    end_datetime: datetime = Body(),
    process_after: timedelta = Body(),
    repeat_at: Union[time, None] = Body(default=None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }
```

---

## Generating SDKs¶

**URL:** https://fastapi.tiangolo.com/advanced/generate-clients/

**Contents:**
- Generating SDKs¶
- Open Source SDK Generators¶
- SDK Generators from FastAPI Sponsors¶
- Create a TypeScript SDK¶
  - API Docs¶
  - Hey API¶
  - Using the SDK¶
- FastAPI App with Tags¶
  - Generate a TypeScript Client with Tags¶
  - Client Method Names¶

Because FastAPI is based on the OpenAPI specification, its APIs can be described in a standard format that many tools understand.

This makes it easy to generate up-to-date documentation, client libraries (SDKs) in multiple languages, and testing or automation workflows that stay in sync with your code.

In this guide, you'll learn how to generate a TypeScript SDK for your FastAPI backend.

A versatile option is the OpenAPI Generator, which supports many programming languages and can generate SDKs from your OpenAPI specification.

For TypeScript clients, Hey API is a purpose-built solution, providing an optimized experience for the TypeScript ecosystem.

You can discover more SDK generators on OpenAPI.Tools.

FastAPI automatically generates OpenAPI 3.1 specifications, so any tool you use must support this version.

This section highlights venture-backed and company-supported solutions from companies that sponsor FastAPI. These products provide additional features and integrations on top of high-quality generated SDKs.

By ✨ sponsoring FastAPI ✨, these companies help ensure the framework and its ecosystem remain healthy and sustainable.

Their sponsorship also demonstrates a strong commitment to the FastAPI community (you), showing that they care not only about offering a great service but also about supporting a robust and thriving framework, FastAPI. 🙇

For example, you might want to try:

Some of these solutions may also be open source or offer free tiers, so you can try them without a financial commitment. Other commercial SDK generators are available and can be found online. 🤓

Let's start with a simple FastAPI application:

Notice that the path operations define the models they use for request payload and response payload, using the models Item and ResponseMessage.

If you go to /docs, you will see that it has the schemas for the data to be sent in requests and received in responses:

You can see those schemas because they were declared with the models in the app.

That information is available in the app's OpenAPI schema, and then shown in the API docs.

That same information from the models that is included in OpenAPI is what can be used to generate the client code.

Once we have a FastAPI app with the models, we can use Hey API to generate a TypeScript client. The fastest way to do that is via npx.

This will generate a TypeScript SDK in ./src/client.

You can learn how to install @hey-api/openapi-ts and read about the generated output on their website.

Now you can import and use the client code. It could look like this, notice that you get autocompletion for the methods:

You will also get autocompletion for the payload to send:

Notice the autocompletion for name and price, that was defined in the FastAPI application, in the Item model.

You will have inline errors for the data that you send:

The response object will also have autocompletion:

In many cases, your FastAPI app will be bigger, and you will probably use tags to separate different groups of path operations.

For example, you could have a section for items and another section for users, and they could be separated by tags:

If you generate a client for a FastAPI app using tags, it will normally also separate the client code based on the tags.

This way, you will be able to have things ordered and grouped correctly for the client code:

In this case, you have:

Right now, the generated method names like createItemItemsPost don't look very clean:

...that's because the client generator uses the OpenAPI internal operation ID for each path operation.

OpenAPI requires that each operation ID is unique across all the path operations, so FastAPI uses the function name, the path, and the HTTP method/operation to generate that operation ID, because that way it can make sure that the operation IDs are unique.

But I'll show you how to improve that next. 🤓

You can modify the way these operation IDs are generated to make them simpler and have simpler method names in the clients.

In this case, you will have to ensure that each operation ID is unique in some other way.

For example, you could make sure that each path operation has a tag, and then generate the operation ID based on the tag and the path operation name (the function name).

FastAPI uses a unique ID for each path operation, which is used for the operation ID and also for the names of any needed custom models, for requests or responses.

You can customize that function. It takes an APIRoute and outputs a string.

For example, here it is using the first tag (you will probably have only one tag) and the path operation name (the function name).

You can then pass that custom function to FastAPI as the generate_unique_id_function parameter:

Now, if you generate the client again, you will see that it has the improved method names:

As you see, the method names now have the tag and then the function name, now they don't include information from the URL path and the HTTP operation.

The generated code still has some duplicated information.

We already know that this method is related to the items because that word is in the ItemsService (taken from the tag), but we still have the tag name prefixed in the method name too. 😕

We will probably still want to keep it for OpenAPI in general, as that will ensure that the operation IDs are unique.

But for the generated client, we could modify the OpenAPI operation IDs right before generating the clients, just to make those method names nicer and cleaner.

We could download the OpenAPI JSON to a file openapi.json and then we could remove that prefixed tag with a script like this:

With that, the operation IDs would be renamed from things like items-get_items to just get_items, that way the client generator can generate simpler method names.

Since the end result is now in an openapi.json file, you need to update your input location:

After generating the new client, you would now have clean method names, with all the autocompletion, inline errors, etc:

When using the automatically generated clients, you would get autocompletion for:

You would also have inline errors for everything.

And whenever you update the backend code, and regenerate the frontend, it would have any new path operations available as methods, the old ones removed, and any other change would be reflected on the generated code. 🤓

This also means that if something changed, it will be reflected on the client code automatically. And if you build the client, it will error out if you have any mismatch in the data used.

So, you would detect many errors very early in the development cycle instead of having to wait for the errors to show up to your final users in production and then trying to debug where the problem is. ✨

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


class ResponseMessage(BaseModel):
    message: str


@app.post("/items/", response_model=ResponseMessage)
async def create_item(item: Item):
    return {"message": "item received"}


@app.get("/items/", response_model=list[Item])
async def get_items():
    return [
        {"name": "Plumbus", "price": 3},
        {"name": "Portal Gun", "price": 9001},
    ]
```

Example 2 (python):
```python
npx @hey-api/openapi-ts -i http://localhost:8000/openapi.json -o src/client
```

Example 3 (python):
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


class ResponseMessage(BaseModel):
    message: str


class User(BaseModel):
    username: str
    email: str


@app.post("/items/", response_model=ResponseMessage, tags=["items"])
async def create_item(item: Item):
    return {"message": "Item received"}


@app.get("/items/", response_model=list[Item], tags=["items"])
async def get_items():
    return [
        {"name": "Plumbus", "price": 3},
        {"name": "Portal Gun", "price": 9001},
    ]


@app.post("/users/", response_model=ResponseMessage, tags=["users"])
async def create_user(user: User):
    return {"message": "User received"}
```

Example 4 (css):
```css
ItemsService.createItemItemsPost({name: "Plumbus", price: 5})
```

---

## Static Files - StaticFiles¶

**URL:** https://fastapi.tiangolo.com/reference/staticfiles/

**Contents:**
- Static Files - StaticFiles¶
- fastapi.staticfiles.StaticFiles ¶
  - directory instance-attribute ¶
  - packages instance-attribute ¶
  - all_directories instance-attribute ¶
  - html instance-attribute ¶
  - config_checked instance-attribute ¶
  - follow_symlink instance-attribute ¶
  - get_directories ¶
  - get_path ¶

You can use the StaticFiles class to serve static files, like JavaScript, CSS, images, etc.

Read more about it in the FastAPI docs for Static Files.

You can import it directly from fastapi.staticfiles:

Given directory and packages arguments, return a list of all the directories that should be used for serving static files from.

Given the ASGI scope, return the path string to serve up, with OS specific path separators, and any '..', '.' components removed.

Returns an HTTP response, given the incoming path, method and request headers.

Perform a one-off configuration check that StaticFiles is actually pointed at a directory, so that we can raise loud errors rather than just returning 404 responses.

Given the request and response headers, return True if an HTTP "Not Modified" response could be returned instead.

**Examples:**

Example 1 (sql):
```sql
from fastapi.staticfiles import StaticFiles
```

Example 2 (rust):
```rust
StaticFiles(
    *,
    directory=None,
    packages=None,
    html=False,
    check_dir=True,
    follow_symlink=False
)
```

Example 3 (python):
```python
def __init__(
    self,
    *,
    directory: PathLike | None = None,
    packages: list[str | tuple[str, str]] | None = None,
    html: bool = False,
    check_dir: bool = True,
    follow_symlink: bool = False,
) -> None:
    self.directory = directory
    self.packages = packages
    self.all_directories = self.get_directories(directory, packages)
    self.html = html
    self.config_checked = False
    self.follow_symlink = follow_symlink
    if check_dir and directory is not None and not os.path.isdir(directory):
        raise RuntimeError(f"Directory '{directory}' does not exist")
```

Example 4 (unknown):
```unknown
directory = directory
```

---

## General - How To - Recipes¶

**URL:** https://fastapi.tiangolo.com/how-to/general/

**Contents:**
- General - How To - Recipes¶
- Filter Data - Security¶
- Documentation Tags - OpenAPI¶
- Documentation Summary and Description - OpenAPI¶
- Documentation Response description - OpenAPI¶
- Documentation Deprecate a Path Operation - OpenAPI¶
- Convert any Data to JSON-compatible¶
- OpenAPI Metadata - Docs¶
- OpenAPI Custom URL¶
- OpenAPI Docs URLs¶

Here are several pointers to other places in the docs, for general or frequent questions.

To ensure that you don't return more data than you should, read the docs for Tutorial - Response Model - Return Type.

To add tags to your path operations, and group them in the docs UI, read the docs for Tutorial - Path Operation Configurations - Tags.

To add a summary and description to your path operations, and show them in the docs UI, read the docs for Tutorial - Path Operation Configurations - Summary and Description.

To define the description of the response, shown in the docs UI, read the docs for Tutorial - Path Operation Configurations - Response description.

To deprecate a path operation, and show it in the docs UI, read the docs for Tutorial - Path Operation Configurations - Deprecation.

To convert any data to JSON-compatible, read the docs for Tutorial - JSON Compatible Encoder.

To add metadata to your OpenAPI schema, including a license, version, contact, etc, read the docs for Tutorial - Metadata and Docs URLs.

To customize the OpenAPI URL (or remove it), read the docs for Tutorial - Metadata and Docs URLs.

To update the URLs used for the automatically generated docs user interfaces, read the docs for Tutorial - Metadata and Docs URLs.

---

## About HTTPS¶

**URL:** https://fastapi.tiangolo.com/deployment/https/

**Contents:**
- About HTTPS¶
- Let's Encrypt¶
- HTTPS for Developers¶
  - Domain Name¶
  - DNS¶
  - TLS Handshake Start¶
  - TLS with SNI Extension¶
  - HTTPS Request¶
  - Decrypt the Request¶
  - HTTP Response¶

It is easy to assume that HTTPS is something that is just "enabled" or not.

But it is way more complex than that.

If you are in a hurry or don't care, continue with the next sections for step by step instructions to set everything up with different techniques.

To learn the basics of HTTPS, from a consumer perspective, check https://howhttps.works/.

Now, from a developer's perspective, here are several things to keep in mind while thinking about HTTPS:

It is a common practice to have one program/HTTP server running on the server (the machine, host, etc.) and managing all the HTTPS parts: receiving the encrypted HTTPS requests, sending the decrypted HTTP requests to the actual HTTP application running in the same server (the FastAPI application, in this case), take the HTTP response from the application, encrypt it using the appropriate HTTPS certificate and sending it back to the client using HTTPS. This server is often called a TLS Termination Proxy.

Some of the options you could use as a TLS Termination Proxy are:

Before Let's Encrypt, these HTTPS certificates were sold by trusted third parties.

The process to acquire one of these certificates used to be cumbersome, require quite some paperwork and the certificates were quite expensive.

But then Let's Encrypt was created.

It is a project from the Linux Foundation. It provides HTTPS certificates for free, in an automated way. These certificates use all the standard cryptographic security, and are short-lived (about 3 months), so the security is actually better because of their reduced lifespan.

The domains are securely verified and the certificates are generated automatically. This also allows automating the renewal of these certificates.

The idea is to automate the acquisition and renewal of these certificates so that you can have secure HTTPS, for free, forever.

Here's an example of how an HTTPS API could look like, step by step, paying attention mainly to the ideas important for developers.

It would probably all start by you acquiring some domain name. Then, you would configure it in a DNS server (possibly your same cloud provider).

You would probably get a cloud server (a virtual machine) or something similar, and it would have a fixed public IP address.

In the DNS server(s) you would configure a record (an "A record") to point your domain to the public IP address of your server.

You would probably do this just once, the first time, when setting everything up.

This Domain Name part is way before HTTPS, but as everything depends on the domain and the IP address, it's worth mentioning it here.

Now let's focus on all the actual HTTPS parts.

First, the browser would check with the DNS servers what is the IP for the domain, in this case, someapp.example.com.

The DNS servers would tell the browser to use some specific IP address. That would be the public IP address used by your server, that you configured in the DNS servers.

The browser would then communicate with that IP address on port 443 (the HTTPS port).

The first part of the communication is just to establish the connection between the client and the server and to decide the cryptographic keys they will use, etc.

This interaction between the client and the server to establish the TLS connection is called the TLS handshake.

Only one process in the server can be listening on a specific port in a specific IP address. There could be other processes listening on other ports in the same IP address, but only one for each combination of IP address and port.

TLS (HTTPS) uses the specific port 443 by default. So that's the port we would need.

As only one process can be listening on this port, the process that would do it would be the TLS Termination Proxy.

The TLS Termination Proxy would have access to one or more TLS certificates (HTTPS certificates).

Using the SNI extension discussed above, the TLS Termination Proxy would check which of the TLS (HTTPS) certificates available it should use for this connection, using the one that matches the domain expected by the client.

In this case, it would use the certificate for someapp.example.com.

The client already trusts the entity that generated that TLS certificate (in this case Let's Encrypt, but we'll see about that later), so it can verify that the certificate is valid.

Then, using the certificate, the client and the TLS Termination Proxy decide how to encrypt the rest of the TCP communication. This completes the TLS Handshake part.

After this, the client and the server have an encrypted TCP connection, this is what TLS provides. And then they can use that connection to start the actual HTTP communication.

And that's what HTTPS is, it's just plain HTTP inside a secure TLS connection instead of a pure (unencrypted) TCP connection.

Notice that the encryption of the communication happens at the TCP level, not at the HTTP level.

Now that the client and server (specifically the browser and the TLS Termination Proxy) have an encrypted TCP connection, they can start the HTTP communication.

So, the client sends an HTTPS request. This is just an HTTP request through an encrypted TLS connection.

The TLS Termination Proxy would use the encryption agreed to decrypt the request, and would transmit the plain (decrypted) HTTP request to the process running the application (for example a process with Uvicorn running the FastAPI application).

The application would process the request and send a plain (unencrypted) HTTP response to the TLS Termination Proxy.

The TLS Termination Proxy would then encrypt the response using the cryptography agreed before (that started with the certificate for someapp.example.com), and send it back to the browser.

Next, the browser would verify that the response is valid and encrypted with the right cryptographic key, etc. It would then decrypt the response and process it.

The client (browser) will know that the response comes from the correct server because it is using the cryptography they agreed using the HTTPS certificate before.

In the same server (or servers), there could be multiple applications, for example, other API programs or a database.

Only one process can be handling the specific IP and port (the TLS Termination Proxy in our example) but the other applications/processes can be running on the server(s) too, as long as they don't try to use the same combination of public IP and port.

That way, the TLS Termination Proxy could handle HTTPS and certificates for multiple domains, for multiple applications, and then transmit the requests to the right application in each case.

At some point in the future, each certificate would expire (about 3 months after acquiring it).

And then, there would be another program (in some cases it's another program, in some cases it could be the same TLS Termination Proxy) that would talk to Let's Encrypt, and renew the certificate(s).

The TLS certificates are associated with a domain name, not with an IP address.

So, to renew the certificates, the renewal program needs to prove to the authority (Let's Encrypt) that it indeed "owns" and controls that domain.

To do that, and to accommodate different application needs, there are several ways it can do it. Some popular ways are:

All this renewal process, while still serving the app, is one of the main reasons why you would want to have a separate system to handle HTTPS with a TLS Termination Proxy instead of just using the TLS certificates with the application server directly (e.g. Uvicorn).

When using a proxy to handle HTTPS, your application server (for example Uvicorn via FastAPI CLI) doesn't known anything about the HTTPS process, it communicates with plain HTTP with the TLS Termination Proxy.

This proxy would normally set some HTTP headers on the fly before transmitting the request to the application server, to let the application server know that the request is being forwarded by the proxy.

The proxy headers are:

Nevertheless, as the application server doesn't know it is behind a trusted proxy, by default, it wouldn't trust those headers.

But you can configure the application server to trust the forwarded headers sent by the proxy. If you are using FastAPI CLI, you can use the CLI Option --forwarded-allow-ips to tell it from which IPs it should trust those forwarded headers.

For example, if the application server is only receiving communication from the trusted proxy, you can set it to --forwarded-allow-ips="*" to make it trust all incoming IPs, as it will only receive requests from whatever is the IP used by the proxy.

This way the application would be able to know what is its own public URL, if it is using HTTPS, the domain, etc.

This would be useful for example to properly handle redirects.

You can learn more about this in the documentation for Behind a Proxy - Enable Proxy Forwarded Headers

Having HTTPS is very important, and quite critical in most cases. Most of the effort you as a developer have to put around HTTPS is just about understanding these concepts and how they work.

But once you know the basic information of HTTPS for developers you can easily combine and configure different tools to help you manage everything in a simple way.

In some of the next chapters, I'll show you several concrete examples of how to set up HTTPS for FastAPI applications. 🔒

---

## FastAPI CLI¶

**URL:** https://fastapi.tiangolo.com/fastapi-cli/

**Contents:**
- FastAPI CLI¶
- fastapi dev¶
- fastapi run¶

FastAPI CLI is a command line program that you can use to serve your FastAPI app, manage your FastAPI project, and more.

When you install FastAPI (e.g. with pip install "fastapi[standard]"), it includes a package called fastapi-cli, this package provides the fastapi command in the terminal.

To run your FastAPI app for development, you can use the fastapi dev command:

The command line program called fastapi is FastAPI CLI.

FastAPI CLI takes the path to your Python program (e.g. main.py) and automatically detects the FastAPI instance (commonly named app), determines the correct import process, and then serves it.

For production you would use fastapi run instead. 🚀

Internally, FastAPI CLI uses Uvicorn, a high-performance, production-ready, ASGI server. 😎

Running fastapi dev initiates development mode.

By default, auto-reload is enabled, automatically reloading the server when you make changes to your code. This is resource-intensive and could be less stable than when it's disabled. You should only use it for development. It also listens on the IP address 127.0.0.1, which is the IP for your machine to communicate with itself alone (localhost).

Executing fastapi run starts FastAPI in production mode by default.

By default, auto-reload is disabled. It also listens on the IP address 0.0.0.0, which means all the available IP addresses, this way it will be publicly accessible to anyone that can communicate with the machine. This is how you would normally run it in production, for example, in a container.

In most cases you would (and should) have a "termination proxy" handling HTTPS for you on top, this will depend on how you deploy your application, your provider might do this for you, or you might need to set it up yourself.

You can learn more about it in the deployment documentation.

---

## Custom Response Classes - File, HTML, Redirect, Streaming, etc.¶

**URL:** https://fastapi.tiangolo.com/reference/responses/

**Contents:**
- Custom Response Classes - File, HTML, Redirect, Streaming, etc.¶
- FastAPI Responses¶
- fastapi.responses.UJSONResponse ¶
  - charset class-attribute instance-attribute ¶
  - status_code instance-attribute ¶
  - media_type class-attribute instance-attribute ¶
  - body instance-attribute ¶
  - background instance-attribute ¶
  - headers property ¶
  - render ¶

There are several custom response classes you can use to create an instance and return them directly from your path operations.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

You can import them directly from fastapi.responses:

There are a couple of custom FastAPI response classes, you can use them to optimize JSON performance.

JSON response using the high-performance ujson library to serialize data to JSON.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

JSON response using the high-performance orjson library to serialize data to JSON.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

**Examples:**

Example 1 (sql):
```sql
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    ORJSONResponse,
    PlainTextResponse,
    RedirectResponse,
    Response,
    StreamingResponse,
    UJSONResponse,
)
```

Example 2 (rust):
```rust
UJSONResponse(
    content,
    status_code=200,
    headers=None,
    media_type=None,
    background=None,
)
```

Example 3 (python):
```python
def __init__(
    self,
    content: Any,
    status_code: int = 200,
    headers: Mapping[str, str] | None = None,
    media_type: str | None = None,
    background: BackgroundTask | None = None,
) -> None:
    super().__init__(content, status_code, headers, media_type, background)
```

Example 4 (unknown):
```unknown
charset = 'utf-8'
```

---

## Query Parameter Models¶

**URL:** https://fastapi.tiangolo.com/tutorial/query-param-models/

**Contents:**
- Query Parameter Models¶
- Query Parameters with a Pydantic Model¶
- Check the Docs¶
- Forbid Extra Query Parameters¶
- Summary¶

If you have a group of query parameters that are related, you can create a Pydantic model to declare them.

This would allow you to re-use the model in multiple places and also to declare validations and metadata for all the parameters at once. 😎

This is supported since FastAPI version 0.115.0. 🤓

Declare the query parameters that you need in a Pydantic model, and then declare the parameter as Query:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

FastAPI will extract the data for each field from the query parameters in the request and give you the Pydantic model you defined.

You can see the query parameters in the docs UI at /docs:

In some special use cases (probably not very common), you might want to restrict the query parameters that you want to receive.

You can use Pydantic's model configuration to forbid any extra fields:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

If a client tries to send some extra data in the query parameters, they will receive an error response.

For example, if the client tries to send a tool query parameter with a value of plumbus, like:

They will receive an error response telling them that the query parameter tool is not allowed:

You can use Pydantic models to declare query parameters in FastAPI. 😎

Spoiler alert: you can also use Pydantic models to declare cookies and headers, but you will read about that later in the tutorial. 🤫

**Examples:**

Example 1 (python):
```python
from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query
```

Example 2 (python):
```python
from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query
```

Example 3 (python):
```python
from typing import Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items/")
async def read_items(filter_query: FilterParams = Query()):
    return filter_query
```

Example 4 (python):
```python
from typing import Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items/")
async def read_items(filter_query: FilterParams = Query()):
    return filter_query
```

---

## Test Client - TestClient¶

**URL:** https://fastapi.tiangolo.com/reference/testclient/

**Contents:**
- Test Client - TestClient¶
- fastapi.testclient.TestClient ¶
  - headers property writable ¶
  - follow_redirects instance-attribute ¶
  - max_redirects instance-attribute ¶
  - is_closed property ¶
  - trust_env property ¶
  - timeout property writable ¶
  - event_hooks property writable ¶
  - auth property writable ¶

You can use the TestClient class to test FastAPI applications without creating an actual HTTP and socket connection, just communicating directly with the FastAPI code.

Read more about it in the FastAPI docs for Testing.

You can import it directly from fastapi.testclient:

HTTP headers to include when sending requests.

Check if the client being closed

Authentication class used when none is passed at the request-level.

See also Authentication.

Base URL to use when sending requests with relative URLs.

Cookie values to include when sending requests.

Query parameters to include in the URL when sending requests.

Build and return a request instance.

See also: Request instances

Alternative to httpx.request() that streams the response body instead of loading it into memory at once.

Parameters: See httpx.request.

See also: Streaming Responses

The request is sent as-is, unmodified.

Typically you'll want to build one with Client.build_request() so that any client-level configuration is merged into the request, but passing an explicit httpx.Request() is supported as well.

See also: Request instances

Close transport and proxies.

**Examples:**

Example 1 (sql):
```sql
from fastapi.testclient import TestClient
```

Example 2 (rust):
```rust
TestClient(
    app,
    base_url="http://testserver",
    raise_server_exceptions=True,
    root_path="",
    backend="asyncio",
    backend_options=None,
    cookies=None,
    headers=None,
    follow_redirects=True,
    client=("testclient", 50000),
)
```

Example 3 (python):
```python
def __init__(
    self,
    app: ASGIApp,
    base_url: str = "http://testserver",
    raise_server_exceptions: bool = True,
    root_path: str = "",
    backend: Literal["asyncio", "trio"] = "asyncio",
    backend_options: dict[str, Any] | None = None,
    cookies: httpx._types.CookieTypes | None = None,
    headers: dict[str, str] | None = None,
    follow_redirects: bool = True,
    client: tuple[str, int] = ("testclient", 50000),
) -> None:
    self.async_backend = _AsyncBackend(backend=backend, backend_options=backend_options or {})
    if _is_asgi3(app):
        asgi_app = app
    else:
        app = cast(ASGI2App, app)  # type: ignore[assignment]
        asgi_app = _WrapASGI2(app)  # type: ignore[arg-type]
    self.app = asgi_app
    self.app_state: dict[str, Any] = {}
    transport = _TestClientTransport(
        self.app,
        portal_factory=self._portal_factory,
        raise_server_exceptions=raise_server_exceptions,
        root_path=root_path,
        app_state=self.app_state,
        client=client,
    )
    if headers is None:
        headers = {}
    headers.setdefault("user-agent", "testclient")
    super().__init__(
        base_url=base_url,
        headers=headers,
        transport=transport,
        follow_redirects=follow_redirects,
        cookies=cookies,
    )
```

Example 4 (unknown):
```unknown
follow_redirects = follow_redirects
```

---

## Response class¶

**URL:** https://fastapi.tiangolo.com/reference/response/

**Contents:**
- Response class¶
- fastapi.Response ¶
  - media_type class-attribute instance-attribute ¶
  - charset class-attribute instance-attribute ¶
  - status_code instance-attribute ¶
  - background instance-attribute ¶
  - body instance-attribute ¶
  - headers property ¶
  - render ¶
  - init_headers ¶

You can declare a parameter in a path operation function or dependency to be of type Response and then you can set data for the response like headers or cookies.

You can also use it directly to create an instance of it and return it from your path operations.

You can import it directly from fastapi:

**Examples:**

Example 1 (python):
```python
from fastapi import Response
```

Example 2 (rust):
```rust
Response(
    content=None,
    status_code=200,
    headers=None,
    media_type=None,
    background=None,
)
```

Example 3 (python):
```python
def __init__(
    self,
    content: Any = None,
    status_code: int = 200,
    headers: Mapping[str, str] | None = None,
    media_type: str | None = None,
    background: BackgroundTask | None = None,
) -> None:
    self.status_code = status_code
    if media_type is not None:
        self.media_type = media_type
    self.background = background
    self.body = self.render(content)
    self.init_headers(headers)
```

Example 4 (rust):
```rust
media_type = None
```

---

## Deployments Concepts¶

**URL:** https://fastapi.tiangolo.com/deployment/concepts/

**Contents:**
- Deployments Concepts¶
- Security - HTTPS¶
  - Example Tools for HTTPS¶
- Program and Process¶
  - What is a Program¶
  - What is a Process¶
- Running on Startup¶
  - In a Remote Server¶
  - Run Automatically on Startup¶
  - Separate Program¶

When deploying a FastAPI application, or actually, any type of web API, there are several concepts that you probably care about, and using them you can find the most appropriate way to deploy your application.

Some of the important concepts are:

We'll see how they would affect deployments.

In the end, the ultimate objective is to be able to serve your API clients in a way that is secure, to avoid disruptions, and to use the compute resources (for example remote servers/virtual machines) as efficiently as possible. 🚀

I'll tell you a bit more about these concepts here, and that would hopefully give you the intuition you would need to decide how to deploy your API in very different environments, possibly even in future ones that don't exist yet.

By considering these concepts, you will be able to evaluate and design the best way to deploy your own APIs.

In the next chapters, I'll give you more concrete recipes to deploy FastAPI applications.

But for now, let's check these important conceptual ideas. These concepts also apply to any other type of web API. 💡

In the previous chapter about HTTPS we learned about how HTTPS provides encryption for your API.

We also saw that HTTPS is normally provided by a component external to your application server, a TLS Termination Proxy.

And there has to be something in charge of renewing the HTTPS certificates, it could be the same component or it could be something different.

Some of the tools you could use as a TLS Termination Proxy are:

Another option is that you could use a cloud service that does more of the work including setting up HTTPS. It could have some restrictions or charge you more, etc. But in that case, you wouldn't have to set up a TLS Termination Proxy yourself.

I'll show you some concrete examples in the next chapters.

Then the next concepts to consider are all about the program running your actual API (e.g. Uvicorn).

We will talk a lot about the running "process", so it's useful to have clarity about what it means, and what's the difference with the word "program".

The word program is commonly used to describe many things:

The word process is normally used in a more specific way, only referring to the thing that is running in the operating system (like in the last point above):

If you check out the "task manager" or "system monitor" (or similar tools) in your operating system, you will be able to see many of those processes running.

And, for example, you will probably see that there are multiple processes running the same browser program (Firefox, Chrome, Edge, etc). They normally run one process per tab, plus some other extra processes.

Now that we know the difference between the terms process and program, let's continue talking about deployments.

In most cases, when you create a web API, you want it to be always running, uninterrupted, so that your clients can always access it. This is of course, unless you have a specific reason why you want it to run only in certain situations, but most of the time you want it constantly running and available.

When you set up a remote server (a cloud server, a virtual machine, etc.) the simplest thing you can do is use fastapi run (which uses Uvicorn) or something similar, manually, the same way you do when developing locally.

And it will work and will be useful during development.

But if your connection to the server is lost, the running process will probably die.

And if the server is restarted (for example after updates, or migrations from the cloud provider) you probably won't notice it. And because of that, you won't even know that you have to restart the process manually. So, your API will just stay dead. 😱

In general, you will probably want the server program (e.g. Uvicorn) to be started automatically on server startup, and without needing any human intervention, to have a process always running with your API (e.g. Uvicorn running your FastAPI app).

To achieve this, you will normally have a separate program that would make sure your application is run on startup. And in many cases, it would also make sure other components or applications are also run, for example, a database.

Some examples of the tools that can do this job are:

I'll give you more concrete examples in the next chapters.

Similar to making sure your application is run on startup, you probably also want to make sure it is restarted after failures.

We, as humans, make mistakes, all the time. Software almost always has bugs hidden in different places. 🐛

And we as developers keep improving the code as we find those bugs and as we implement new features (possibly adding new bugs too 😅).

When building web APIs with FastAPI, if there's an error in our code, FastAPI will normally contain it to the single request that triggered the error. 🛡

The client will get a 500 Internal Server Error for that request, but the application will continue working for the next requests instead of just crashing completely.

Nevertheless, there might be cases where we write some code that crashes the entire application making Uvicorn and Python crash. 💥

And still, you would probably not want the application to stay dead because there was an error in one place, you probably want it to continue running at least for the path operations that are not broken.

But in those cases with really bad errors that crash the running process, you would want an external component that is in charge of restarting the process, at least a couple of times...

...Although if the whole application is just crashing immediately it probably doesn't make sense to keep restarting it forever. But in those cases, you will probably notice it during development, or at least right after deployment.

So let's focus on the main cases, where it could crash entirely in some particular cases in the future, and it still makes sense to restart it.

You would probably want to have the thing in charge of restarting your application as an external component, because by that point, the same application with Uvicorn and Python already crashed, so there's nothing in the same code of the same app that could do anything about it.

In most cases, the same tool that is used to run the program on startup is also used to handle automatic restarts.

For example, this could be handled by:

With a FastAPI application, using a server program like the fastapi command that runs Uvicorn, running it once in one process can serve multiple clients concurrently.

But in many cases, you will want to run several worker processes at the same time.

If you have more clients than what a single process can handle (for example if the virtual machine is not too big) and you have multiple cores in the server's CPU, then you could have multiple processes running with the same application at the same time, and distribute all the requests among them.

When you run multiple processes of the same API program, they are commonly called workers.

Remember from the docs About HTTPS that only one process can be listening on one combination of port and IP address in a server?

So, to be able to have multiple processes at the same time, there has to be a single process listening on a port that then transmits the communication to each worker process in some way.

Now, when the program loads things in memory, for example, a machine learning model in a variable, or the contents of a large file in a variable, all that consumes a bit of the memory (RAM) of the server.

And multiple processes normally don't share any memory. This means that each running process has its own things, variables, and memory. And if you are consuming a large amount of memory in your code, each process will consume an equivalent amount of memory.

For example, if your code loads a Machine Learning model with 1 GB in size, when you run one process with your API, it will consume at least 1 GB of RAM. And if you start 4 processes (4 workers), each will consume 1 GB of RAM. So in total, your API will consume 4 GB of RAM.

And if your remote server or virtual machine only has 3 GB of RAM, trying to load more than 4 GB of RAM will cause problems. 🚨

In this example, there's a Manager Process that starts and controls two Worker Processes.

This Manager Process would probably be the one listening on the port in the IP. And it would transmit all the communication to the worker processes.

Those worker processes would be the ones running your application, they would perform the main computations to receive a request and return a response, and they would load anything you put in variables in RAM.

And of course, the same machine would probably have other processes running as well, apart from your application.

An interesting detail is that the percentage of the CPU used by each process can vary a lot over time, but the memory (RAM) normally stays more or less stable.

If you have an API that does a comparable amount of computations every time and you have a lot of clients, then the CPU utilization will probably also be stable (instead of constantly going up and down quickly).

There can be several approaches to achieve this, and I'll tell you more about specific strategies in the next chapters, for example when talking about Docker and containers.

The main constraint to consider is that there has to be a single component handling the port in the public IP. And then it has to have a way to transmit the communication to the replicated processes/workers.

Here are some possible combinations and strategies:

Don't worry if some of these items about containers, Docker, or Kubernetes don't make a lot of sense yet.

I'll tell you more about container images, Docker, Kubernetes, etc. in a future chapter: FastAPI in Containers - Docker.

There are many cases where you want to perform some steps before starting your application.

For example, you might want to run database migrations.

But in most cases, you will want to perform these steps only once.

So, you will want to have a single process to perform those previous steps, before starting the application.

And you will have to make sure that it's a single process running those previous steps even if afterwards, you start multiple processes (multiple workers) for the application itself. If those steps were run by multiple processes, they would duplicate the work by running it in parallel, and if the steps were something delicate like a database migration, they could cause conflicts with each other.

Of course, there are some cases where there's no problem in running the previous steps multiple times, in that case, it's a lot easier to handle.

Also, keep in mind that depending on your setup, in some cases you might not even need any previous steps before starting your application.

In that case, you wouldn't have to worry about any of this. 🤷

This will depend heavily on the way you deploy your system, and it would probably be connected to the way you start programs, handling restarts, etc.

Here are some possible ideas:

I'll give you more concrete examples for doing this with containers in a future chapter: FastAPI in Containers - Docker.

Your server(s) is (are) a resource, you can consume or utilize, with your programs, the computation time on the CPUs, and the RAM memory available.

How much of the system resources do you want to be consuming/utilizing? It might be easy to think "not much", but in reality, you will probably want to consume as much as possible without crashing.

If you are paying for 3 servers but you are using only a little bit of their RAM and CPU, you are probably wasting money 💸, and probably wasting server electric power 🌎, etc.

In that case, it could be better to have only 2 servers and use a higher percentage of their resources (CPU, memory, disk, network bandwidth, etc).

On the other hand, if you have 2 servers and you are using 100% of their CPU and RAM, at some point one process will ask for more memory, and the server will have to use the disk as "memory" (which can be thousands of times slower), or even crash. Or one process might need to do some computation and would have to wait until the CPU is free again.

In this case, it would be better to get one extra server and run some processes on it so that they all have enough RAM and CPU time.

There's also the chance that for some reason you have a spike of usage of your API. Maybe it went viral, or maybe some other services or bots start using it. And you might want to have extra resources to be safe in those cases.

You could put an arbitrary number to target, for example, something between 50% to 90% of resource utilization. The point is that those are probably the main things you will want to measure and use to tweak your deployments.

You can use simple tools like htop to see the CPU and RAM used in your server or the amount used by each process. Or you can use more complex monitoring tools, which may be distributed across servers, etc.

You have been reading here some of the main concepts that you would probably need to keep in mind when deciding how to deploy your application:

Understanding these ideas and how to apply them should give you the intuition necessary to take any decisions when configuring and tweaking your deployments. 🤓

In the next sections, I'll give you more concrete examples of possible strategies you can follow. 🚀

---

## Exceptions - HTTPException and WebSocketException¶

**URL:** https://fastapi.tiangolo.com/reference/exceptions/

**Contents:**
- Exceptions - HTTPException and WebSocketException¶
- fastapi.HTTPException ¶
    - Example¶
  - status_code instance-attribute ¶
  - detail instance-attribute ¶
  - headers instance-attribute ¶
- fastapi.WebSocketException ¶
    - Example¶
  - code instance-attribute ¶
  - reason instance-attribute ¶

These are the exceptions that you can raise to show errors to the client.

When you raise an exception, as would happen with normal Python, the rest of the execution is aborted. This way you can raise these exceptions from anywhere in the code to abort a request and show the error to the client.

These exceptions can be imported directly from fastapi:

An HTTP exception you can raise in your own code to show errors to the client.

This is for client errors, invalid authentication, invalid data, etc. Not for server errors in your code.

Read more about it in the FastAPI docs for Handling Errors.

HTTP status code to send to the client.

Any data to be sent to the client in the detail key of the JSON response.

TYPE: Any DEFAULT: None

Any headers to send to the client in the response.

TYPE: Optional[dict[str, str]] DEFAULT: None

Bases: WebSocketException

A WebSocket exception you can raise in your own code to show errors to the client.

This is for client errors, invalid authentication, invalid data, etc. Not for server errors in your code.

Read more about it in the FastAPI docs for WebSockets.

A closing code from the valid codes defined in the specification.

The reason to close the WebSocket connection.

It is UTF-8-encoded data. The interpretation of the reason is up to the application, it is not specified by the WebSocket specification.

It could contain text that could be human-readable or interpretable by the client code, etc.

TYPE: Union[str, None] DEFAULT: None

**Examples:**

Example 1 (python):
```python
from fastapi import HTTPException, WebSocketException
```

Example 2 (rust):
```rust
HTTPException(status_code, detail=None, headers=None)
```

Example 3 (python):
```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```

Example 4 (python):
```python
def __init__(
    self,
    status_code: Annotated[
        int,
        Doc(
            """
            HTTP status code to send to the client.
            """
        ),
    ],
    detail: Annotated[
        Any,
        Doc(
            """
            Any data to be sent to the client in the `detail` key of the JSON
            response.
            """
        ),
    ] = None,
    headers: Annotated[
        Optional[dict[str, str]],
        Doc(
            """
            Any headers to send to the client in the response.
            """
        ),
    ] = None,
) -> None:
    super().__init__(status_code=status_code, detail=detail, headers=headers)
```

---

## Advanced User Guide¶

**URL:** https://fastapi.tiangolo.com/advanced/

**Contents:**
- Advanced User Guide¶
- Additional Features¶
- Read the Tutorial first¶

The main Tutorial - User Guide should be enough to give you a tour through all the main features of FastAPI.

In the next sections you will see other options, configurations, and additional features.

The next sections are not necessarily "advanced".

And it's possible that for your use case, the solution is in one of them.

You could still use most of the features in FastAPI with the knowledge from the main Tutorial - User Guide.

And the next sections assume you already read it, and assume that you know those main ideas.

---

## Run a Server Manually¶

**URL:** https://fastapi.tiangolo.com/deployment/manually/

**Contents:**
- Run a Server Manually¶
- Use the fastapi run Command¶
- ASGI Servers¶
- Server Machine and Server Program¶
- Install the Server Program¶
- Run the Server Program¶
- Deployment Concepts¶

In short, use fastapi run to serve your FastAPI application:

That would work for most of the cases. 😎

You could use that command for example to start your FastAPI app in a container, in a server, etc.

Let's go a little deeper into the details.

FastAPI uses a standard for building Python web frameworks and servers called ASGI. FastAPI is an ASGI web framework.

The main thing you need to run a FastAPI application (or any other ASGI application) in a remote server machine is an ASGI server program like Uvicorn, this is the one that comes by default in the fastapi command.

There are several alternatives, including:

There's a small detail about names to keep in mind. 💡

The word "server" is commonly used to refer to both the remote/cloud computer (the physical or virtual machine) and also the program that is running on that machine (e.g. Uvicorn).

Just keep in mind that when you read "server" in general, it could refer to one of those two things.

When referring to the remote machine, it's common to call it server, but also machine, VM (virtual machine), node. Those all refer to some type of remote machine, normally running Linux, where you run programs.

When you install FastAPI, it comes with a production server, Uvicorn, and you can start it with the fastapi run command.

But you can also install an ASGI server manually.

Make sure you create a virtual environment, activate it, and then you can install the server application.

For example, to install Uvicorn:

A similar process would apply to any other ASGI server program.

By adding the standard, Uvicorn will install and use some recommended extra dependencies.

That including uvloop, the high-performance drop-in replacement for asyncio, that provides the big concurrency performance boost.

When you install FastAPI with something like pip install "fastapi[standard]" you already get uvicorn[standard] as well.

If you installed an ASGI server manually, you would normally need to pass an import string in a special format for it to import your FastAPI application:

The command uvicorn main:app refers to:

Each alternative ASGI server program would have a similar command, you can read more in their respective documentation.

Uvicorn and other servers support a --reload option that is useful during development.

The --reload option consumes much more resources, is more unstable, etc.

It helps a lot during development, but you shouldn't use it in production.

These examples run the server program (e.g Uvicorn), starting a single process, listening on all the IPs (0.0.0.0) on a predefined port (e.g. 80).

This is the basic idea. But you will probably want to take care of some additional things, like:

I'll tell you more about each of these concepts, how to think about them, and some concrete examples with strategies to handle them in the next chapters. 🚀

**Examples:**

Example 1 (python):
```python
from main import app
```

---
