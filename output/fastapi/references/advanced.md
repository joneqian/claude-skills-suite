# Fastapi - Advanced

**Pages:** 16

---

## Including WSGI - Flask, Django, others¶

**URL:** https://fastapi.tiangolo.com/advanced/wsgi/

**Contents:**
- Including WSGI - Flask, Django, others¶
- Using WSGIMiddleware¶
- Check it¶

You can mount WSGI applications as you saw with Sub Applications - Mounts, Behind a Proxy.

For that, you can use the WSGIMiddleware and use it to wrap your WSGI application, for example, Flask, Django, etc.

You need to import WSGIMiddleware.

Then wrap the WSGI (e.g. Flask) app with the middleware.

And then mount that under a path.

Now, every request under the path /v1/ will be handled by the Flask application.

And the rest will be handled by FastAPI.

If you run it and go to http://localhost:8000/v1/ you will see the response from Flask:

And if you go to http://localhost:8000/v2 you will see the response from FastAPI:

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, request
from markupsafe import escape

flask_app = Flask(__name__)


@flask_app.route("/")
def flask_main():
    name = request.args.get("name", "World")
    return f"Hello, {escape(name)} from Flask!"


app = FastAPI()


@app.get("/v2")
def read_main():
    return {"message": "Hello World"}


app.mount("/v1", WSGIMiddleware(flask_app))
```

Example 2 (sql):
```sql
Hello, World from Flask!
```

Example 3 (json):
```json
{
    "message": "Hello World"
}
```

---

## Templates¶

**URL:** https://fastapi.tiangolo.com/advanced/templates/

**Contents:**
- Templates¶
- Install dependencies¶
- Using Jinja2Templates¶
- Writing templates¶
  - Template Context Values¶
  - Template url_for Arguments¶
- Templates and static files¶
- More details¶

You can use any template engine you want with FastAPI.

A common choice is Jinja2, the same one used by Flask and other tools.

There are utilities to configure it easily that you can use directly in your FastAPI application (provided by Starlette).

Make sure you create a virtual environment, activate it, and install jinja2:

Before FastAPI 0.108.0, Starlette 0.29.0, the name was the first parameter.

Also, before that, in previous versions, the request object was passed as part of the key-value pairs in the context for Jinja2.

By declaring response_class=HTMLResponse the docs UI will be able to know that the response will be HTML.

You could also use from starlette.templating import Jinja2Templates.

FastAPI provides the same starlette.templating as fastapi.templating just as a convenience for you, the developer. But most of the available responses come directly from Starlette. The same with Request and StaticFiles.

Then you can write a template at templates/item.html with, for example:

In the HTML that contains:

...it will show the id taken from the "context" dict you passed:

For example, with an ID of 42, this would render:

You can also use url_for() inside of the template, it takes as arguments the same arguments that would be used by your path operation function.

So, the section with:

...will generate a link to the same URL that would be handled by the path operation function read_item(id=id).

For example, with an ID of 42, this would render:

You can also use url_for() inside of the template, and use it, for example, with the StaticFiles you mounted with the name="static".

In this example, it would link to a CSS file at static/styles.css with:

And because you are using StaticFiles, that CSS file would be served automatically by your FastAPI application at the URL /static/styles.css.

For more details, including how to test templates, check Starlette's docs on templates.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )
```

Example 2 (html):
```html
<html>
<head>
    <title>Item Details</title>
    <link href="{{ url_for('static', path='/styles.css') }}" rel="stylesheet">
</head>
<body>
    <h1><a href="{{ url_for('read_item', id=id) }}">Item ID: {{ id }}</a></h1>
</body>
</html>
```

Example 3 (json):
```json
Item ID: {{ id }}
```

Example 4 (json):
```json
Item ID: 42
```

---

## Background Tasks¶

**URL:** https://fastapi.tiangolo.com/tutorial/background-tasks/

**Contents:**
- Background Tasks¶
- Using BackgroundTasks¶
- Create a task function¶
- Add the background task¶
- Dependency Injection¶
- Technical Details¶
- Caveat¶
- Recap¶

You can define background tasks to be run after returning a response.

This is useful for operations that need to happen after a request, but that the client doesn't really have to be waiting for the operation to complete before receiving the response.

This includes, for example:

First, import BackgroundTasks and define a parameter in your path operation function with a type declaration of BackgroundTasks:

FastAPI will create the object of type BackgroundTasks for you and pass it as that parameter.

Create a function to be run as the background task.

It is just a standard function that can receive parameters.

It can be an async def or normal def function, FastAPI will know how to handle it correctly.

In this case, the task function will write to a file (simulating sending an email).

And as the write operation doesn't use async and await, we define the function with normal def:

Inside of your path operation function, pass your task function to the background tasks object with the method .add_task():

.add_task() receives as arguments:

Using BackgroundTasks also works with the dependency injection system, you can declare a parameter of type BackgroundTasks at multiple levels: in a path operation function, in a dependency (dependable), in a sub-dependency, etc.

FastAPI knows what to do in each case and how to reuse the same object, so that all the background tasks are merged together and are run in the background afterwards:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

In this example, the messages will be written to the log.txt file after the response is sent.

If there was a query in the request, it will be written to the log in a background task.

And then another background task generated at the path operation function will write a message using the email path parameter.

The class BackgroundTasks comes directly from starlette.background.

It is imported/included directly into FastAPI so that you can import it from fastapi and avoid accidentally importing the alternative BackgroundTask (without the s at the end) from starlette.background.

By only using BackgroundTasks (and not BackgroundTask), it's then possible to use it as a path operation function parameter and have FastAPI handle the rest for you, just like when using the Request object directly.

It's still possible to use BackgroundTask alone in FastAPI, but you have to create the object in your code and return a Starlette Response including it.

You can see more details in Starlette's official docs for Background Tasks.

If you need to perform heavy background computation and you don't necessarily need it to be run by the same process (for example, you don't need to share memory, variables, etc), you might benefit from using other bigger tools like Celery.

They tend to require more complex configurations, a message/job queue manager, like RabbitMQ or Redis, but they allow you to run background tasks in multiple processes, and especially, in multiple servers.

But if you need to access variables and objects from the same FastAPI app, or you need to perform small background tasks (like sending an email notification), you can simply just use BackgroundTasks.

Import and use BackgroundTasks with parameters in path operation functions and dependencies to add background tasks.

**Examples:**

Example 1 (python):
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

Example 2 (python):
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
from typing import Annotated

from fastapi import BackgroundTasks, Depends, FastAPI

app = FastAPI()


def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


@app.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: Annotated[str, Depends(get_query)]
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}
```

---

## Middleware¶

**URL:** https://fastapi.tiangolo.com/reference/middleware/

**Contents:**
- Middleware¶
- fastapi.middleware.cors.CORSMiddleware ¶
  - app instance-attribute ¶
  - allow_origins instance-attribute ¶
  - allow_methods instance-attribute ¶
  - allow_headers instance-attribute ¶
  - allow_all_origins instance-attribute ¶
  - allow_all_headers instance-attribute ¶
  - preflight_explicit_allow_origin instance-attribute ¶
  - allow_origin_regex instance-attribute ¶

There are several middlewares available provided by Starlette directly.

Read more about them in the FastAPI docs for Middleware.

It can be imported from fastapi:

It can be imported from fastapi:

It can be imported from fastapi:

It can be imported from fastapi:

It can be imported from fastapi:

**Examples:**

Example 1 (rust):
```rust
CORSMiddleware(
    app,
    allow_origins=(),
    allow_methods=("GET",),
    allow_headers=(),
    allow_credentials=False,
    allow_origin_regex=None,
    expose_headers=(),
    max_age=600,
)
```

Example 2 (python):
```python
def __init__(
    self,
    app: ASGIApp,
    allow_origins: Sequence[str] = (),
    allow_methods: Sequence[str] = ("GET",),
    allow_headers: Sequence[str] = (),
    allow_credentials: bool = False,
    allow_origin_regex: str | None = None,
    expose_headers: Sequence[str] = (),
    max_age: int = 600,
) -> None:
    if "*" in allow_methods:
        allow_methods = ALL_METHODS

    compiled_allow_origin_regex = None
    if allow_origin_regex is not None:
        compiled_allow_origin_regex = re.compile(allow_origin_regex)

    allow_all_origins = "*" in allow_origins
    allow_all_headers = "*" in allow_headers
    preflight_explicit_allow_origin = not allow_all_origins or allow_credentials

    simple_headers = {}
    if allow_all_origins:
        simple_headers["Access-Control-Allow-Origin"] = "*"
    if allow_credentials:
        simple_headers["Access-Control-Allow-Credentials"] = "true"
    if expose_headers:
        simple_headers["Access-Control-Expose-Headers"] = ", ".join(expose_headers)

    preflight_headers = {}
    if preflight_explicit_allow_origin:
        # The origin value will be set in preflight_response() if it is allowed.
        preflight_headers["Vary"] = "Origin"
    else:
        preflight_headers["Access-Control-Allow-Origin"] = "*"
    preflight_headers.update(
        {
            "Access-Control-Allow-Methods": ", ".join(allow_methods),
            "Access-Control-Max-Age": str(max_age),
        }
    )
    allow_headers = sorted(SAFELISTED_HEADERS | set(allow_headers))
    if allow_headers and not allow_all_headers:
        preflight_headers["Access-Control-Allow-Headers"] = ", ".join(allow_headers)
    if allow_credentials:
        preflight_headers["Access-Control-Allow-Credentials"] = "true"

    self.app = app
    self.allow_origins = allow_origins
    self.allow_methods = allow_methods
    self.allow_headers = [h.lower() for h in allow_headers]
    self.allow_all_origins = allow_all_origins
    self.allow_all_headers = allow_all_headers
    self.preflight_explicit_allow_origin = preflight_explicit_allow_origin
    self.allow_origin_regex = compiled_allow_origin_regex
    self.simple_headers = simple_headers
    self.preflight_headers = preflight_headers
```

Example 3 (unknown):
```unknown
allow_origins = allow_origins
```

Example 4 (unknown):
```unknown
allow_methods = allow_methods
```

---

## WebSockets¶

**URL:** https://fastapi.tiangolo.com/reference/websockets/

**Contents:**
- WebSockets¶
- fastapi.WebSocket ¶
  - scope instance-attribute ¶
  - app property ¶
  - url property ¶
  - base_url property ¶
  - headers property ¶
  - query_params property ¶
  - path_params property ¶
  - cookies property ¶

When defining WebSockets, you normally declare a parameter of type WebSocket and with it you can read data from the client and send data to it.

It is provided directly by Starlette, but you can import it from fastapi:

When you want to define dependencies that should be compatible with both HTTP and WebSockets, you can define a parameter that takes an HTTPConnection instead of a Request or a WebSocket.

Bases: HTTPConnection

Receive ASGI websocket messages, ensuring valid state transitions.

Send ASGI websocket messages, ensuring valid state transitions.

When a client disconnects, a WebSocketDisconnect exception is raised, you can catch it.

You can import it directly form fastapi:

Additional classes for handling WebSockets.

Provided directly by Starlette, but you can import it from fastapi:

**Examples:**

Example 1 (python):
```python
from fastapi import WebSocket
```

Example 2 (unknown):
```unknown
WebSocket(scope, receive, send)
```

Example 3 (python):
```python
def __init__(self, scope: Scope, receive: Receive, send: Send) -> None:
    super().__init__(scope)
    assert scope["type"] == "websocket"
    self._receive = receive
    self._send = send
    self.client_state = WebSocketState.CONNECTING
    self.application_state = WebSocketState.CONNECTING
```

Example 4 (unknown):
```unknown
scope = scope
```

---

## CORS (Cross-Origin Resource Sharing)¶

**URL:** https://fastapi.tiangolo.com/tutorial/cors/

**Contents:**
- CORS (Cross-Origin Resource Sharing)¶
- Origin¶
- Steps¶
- Wildcards¶
- Use CORSMiddleware¶
  - CORS preflight requests¶
  - Simple requests¶
- More info¶

CORS or "Cross-Origin Resource Sharing" refers to the situations when a frontend running in a browser has JavaScript code that communicates with a backend, and the backend is in a different "origin" than the frontend.

An origin is the combination of protocol (http, https), domain (myapp.com, localhost, localhost.tiangolo.com), and port (80, 443, 8080).

So, all these are different origins:

Even if they are all in localhost, they use different protocols or ports, so, they are different "origins".

So, let's say you have a frontend running in your browser at http://localhost:8080, and its JavaScript is trying to communicate with a backend running at http://localhost (because we don't specify a port, the browser will assume the default port 80).

Then, the browser will send an HTTP OPTIONS request to the :80-backend, and if the backend sends the appropriate headers authorizing the communication from this different origin (http://localhost:8080) then the :8080-browser will let the JavaScript in the frontend send its request to the :80-backend.

To achieve this, the :80-backend must have a list of "allowed origins".

In this case, the list would have to include http://localhost:8080 for the :8080-frontend to work correctly.

It's also possible to declare the list as "*" (a "wildcard") to say that all are allowed.

But that will only allow certain types of communication, excluding everything that involves credentials: Cookies, Authorization headers like those used with Bearer Tokens, etc.

So, for everything to work correctly, it's better to specify explicitly the allowed origins.

You can configure it in your FastAPI application using the CORSMiddleware.

You can also specify whether your backend allows:

The default parameters used by the CORSMiddleware implementation are restrictive by default, so you'll need to explicitly enable particular origins, methods, or headers, in order for browsers to be permitted to use them in a Cross-Domain context.

The following arguments are supported:

allow_credentials - Indicate that cookies should be supported for cross-origin requests. Defaults to False.

None of allow_origins, allow_methods and allow_headers can be set to ['*'] if allow_credentials is set to True. All of them must be explicitly specified.

expose_headers - Indicate any response headers that should be made accessible to the browser. Defaults to [].

The middleware responds to two particular types of HTTP request...

These are any OPTIONS request with Origin and Access-Control-Request-Method headers.

In this case the middleware will intercept the incoming request and respond with appropriate CORS headers, and either a 200 or 400 response for informational purposes.

Any request with an Origin header. In this case the middleware will pass the request through as normal, but will include appropriate CORS headers on the response.

For more info about CORS, check the Mozilla CORS documentation.

You could also use from starlette.middleware.cors import CORSMiddleware.

FastAPI provides several middlewares in fastapi.middleware just as a convenience for you, the developer. But most of the available middlewares come directly from Starlette.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}
```

---

## Advanced Middleware¶

**URL:** https://fastapi.tiangolo.com/advanced/middleware/

**Contents:**
- Advanced Middleware¶
- Adding ASGI middlewares¶
- Integrated middlewares¶
- HTTPSRedirectMiddleware¶
- TrustedHostMiddleware¶
- GZipMiddleware¶
- Other middlewares¶

In the main tutorial you read how to add Custom Middleware to your application.

And then you also read how to handle CORS with the CORSMiddleware.

In this section we'll see how to use other middlewares.

As FastAPI is based on Starlette and implements the ASGI specification, you can use any ASGI middleware.

A middleware doesn't have to be made for FastAPI or Starlette to work, as long as it follows the ASGI spec.

In general, ASGI middlewares are classes that expect to receive an ASGI app as the first argument.

So, in the documentation for third-party ASGI middlewares they will probably tell you to do something like:

But FastAPI (actually Starlette) provides a simpler way to do it that makes sure that the internal middlewares handle server errors and custom exception handlers work properly.

For that, you use app.add_middleware() (as in the example for CORS).

app.add_middleware() receives a middleware class as the first argument and any additional arguments to be passed to the middleware.

FastAPI includes several middlewares for common use cases, we'll see next how to use them.

For the next examples, you could also use from starlette.middleware.something import SomethingMiddleware.

FastAPI provides several middlewares in fastapi.middleware just as a convenience for you, the developer. But most of the available middlewares come directly from Starlette.

Enforces that all incoming requests must either be https or wss.

Any incoming request to http or ws will be redirected to the secure scheme instead.

Enforces that all incoming requests have a correctly set Host header, in order to guard against HTTP Host Header attacks.

The following arguments are supported:

If an incoming request does not validate correctly then a 400 response will be sent.

Handles GZip responses for any request that includes "gzip" in the Accept-Encoding header.

The middleware will handle both standard and streaming responses.

The following arguments are supported:

There are many other ASGI middlewares.

To see other available middlewares check Starlette's Middleware docs and the ASGI Awesome List.

**Examples:**

Example 1 (python):
```python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

Example 2 (python):
```python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

Example 3 (python):
```python
from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

app.add_middleware(HTTPSRedirectMiddleware)


@app.get("/")
async def main():
    return {"message": "Hello World"}
```

Example 4 (python):
```python
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"]
)


@app.get("/")
async def main():
    return {"message": "Hello World"}
```

---

## Static Files¶

**URL:** https://fastapi.tiangolo.com/tutorial/static-files/

**Contents:**
- Static Files¶
- Use StaticFiles¶
  - What is "Mounting"¶
- Details¶
- More info¶

You can serve static files automatically from a directory using StaticFiles.

You could also use from starlette.staticfiles import StaticFiles.

FastAPI provides the same starlette.staticfiles as fastapi.staticfiles just as a convenience for you, the developer. But it actually comes directly from Starlette.

"Mounting" means adding a complete "independent" application in a specific path, that then takes care of handling all the sub-paths.

This is different from using an APIRouter as a mounted application is completely independent. The OpenAPI and docs from your main application won't include anything from the mounted application, etc.

You can read more about this in the Advanced User Guide.

The first "/static" refers to the sub-path this "sub-application" will be "mounted" on. So, any path that starts with "/static" will be handled by it.

The directory="static" refers to the name of the directory that contains your static files.

The name="static" gives it a name that can be used internally by FastAPI.

All these parameters can be different than "static", adjust them with the needs and specific details of your own application.

For more details and options check Starlette's docs about Static Files.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
```

---

## Middleware¶

**URL:** https://fastapi.tiangolo.com/tutorial/middleware/

**Contents:**
- Middleware¶
- Create a middleware¶
  - Before and after the response¶
- Multiple middleware execution order¶
- Other middlewares¶

You can add middleware to FastAPI applications.

A "middleware" is a function that works with every request before it is processed by any specific path operation. And also with every response before returning it.

If you have dependencies with yield, the exit code will run after the middleware.

If there were any background tasks (covered in the Background Tasks section, you will see it later), they will run after all the middleware.

To create a middleware you use the decorator @app.middleware("http") on top of a function.

The middleware function receives:

Keep in mind that custom proprietary headers can be added using the X- prefix.

But if you have custom headers that you want a client in a browser to be able to see, you need to add them to your CORS configurations (CORS (Cross-Origin Resource Sharing)) using the parameter expose_headers documented in Starlette's CORS docs.

You could also use from starlette.requests import Request.

FastAPI provides it as a convenience for you, the developer. But it comes directly from Starlette.

You can add code to be run with the request, before any path operation receives it.

And also after the response is generated, before returning it.

For example, you could add a custom header X-Process-Time containing the time in seconds that it took to process the request and generate a response:

Here we use time.perf_counter() instead of time.time() because it can be more precise for these use cases. 🤓

When you add multiple middlewares using either @app.middleware() decorator or app.add_middleware() method, each new middleware wraps the application, forming a stack. The last middleware added is the outermost, and the first is the innermost.

On the request path, the outermost middleware runs first.

On the response path, it runs last.

This results in the following execution order:

Request: MiddlewareB → MiddlewareA → route

Response: route → MiddlewareA → MiddlewareB

This stacking behavior ensures that middlewares are executed in a predictable and controllable order.

You can later read more about other middlewares in the Advanced User Guide: Advanced Middleware.

You will read about how to handle CORS with a middleware in the next section.

**Examples:**

Example 1 (python):
```python
import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

Example 2 (python):
```python
import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

Example 3 (unknown):
```unknown
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)
```

---

## Lifespan Events¶

**URL:** https://fastapi.tiangolo.com/advanced/events/

**Contents:**
- Lifespan Events¶
- Use Case¶
- Lifespan¶
  - Lifespan function¶
  - Async Context Manager¶
- Alternative Events (deprecated)¶
  - startup event¶
  - shutdown event¶
  - startup and shutdown together¶
- Technical Details¶

You can define logic (code) that should be executed before the application starts up. This means that this code will be executed once, before the application starts receiving requests.

The same way, you can define logic (code) that should be executed when the application is shutting down. In this case, this code will be executed once, after having handled possibly many requests.

Because this code is executed before the application starts taking requests, and right after it finishes handling requests, it covers the whole application lifespan (the word "lifespan" will be important in a second 😉).

This can be very useful for setting up resources that you need to use for the whole app, and that are shared among requests, and/or that you need to clean up afterwards. For example, a database connection pool, or loading a shared machine learning model.

Let's start with an example use case and then see how to solve it with this.

Let's imagine that you have some machine learning models that you want to use to handle requests. 🤖

The same models are shared among requests, so, it's not one model per request, or one per user or something similar.

Let's imagine that loading the model can take quite some time, because it has to read a lot of data from disk. So you don't want to do it for every request.

You could load it at the top level of the module/file, but that would also mean that it would load the model even if you are just running a simple automated test, then that test would be slow because it would have to wait for the model to load before being able to run an independent part of the code.

That's what we'll solve, let's load the model before the requests are handled, but only right before the application starts receiving requests, not while the code is being loaded.

You can define this startup and shutdown logic using the lifespan parameter of the FastAPI app, and a "context manager" (I'll show you what that is in a second).

Let's start with an example and then see it in detail.

We create an async function lifespan() with yield like this:

Here we are simulating the expensive startup operation of loading the model by putting the (fake) model function in the dictionary with machine learning models before the yield. This code will be executed before the application starts taking requests, during the startup.

And then, right after the yield, we unload the model. This code will be executed after the application finishes handling requests, right before the shutdown. This could, for example, release resources like memory or a GPU.

The shutdown would happen when you are stopping the application.

Maybe you need to start a new version, or you just got tired of running it. 🤷

The first thing to notice, is that we are defining an async function with yield. This is very similar to Dependencies with yield.

The first part of the function, before the yield, will be executed before the application starts.

And the part after the yield will be executed after the application has finished.

If you check, the function is decorated with an @asynccontextmanager.

That converts the function into something called an "async context manager".

A context manager in Python is something that you can use in a with statement, for example, open() can be used as a context manager:

In recent versions of Python, there's also an async context manager. You would use it with async with:

When you create a context manager or an async context manager like above, what it does is that, before entering the with block, it will execute the code before the yield, and after exiting the with block, it will execute the code after the yield.

In our code example above, we don't use it directly, but we pass it to FastAPI for it to use it.

The lifespan parameter of the FastAPI app takes an async context manager, so we can pass our new lifespan async context manager to it.

The recommended way to handle the startup and shutdown is using the lifespan parameter of the FastAPI app as described above. If you provide a lifespan parameter, startup and shutdown event handlers will no longer be called. It's all lifespan or all events, not both.

You can probably skip this part.

There's an alternative way to define this logic to be executed during startup and during shutdown.

You can define event handlers (functions) that need to be executed before the application starts up, or when the application is shutting down.

These functions can be declared with async def or normal def.

To add a function that should be run before the application starts, declare it with the event "startup":

In this case, the startup event handler function will initialize the items "database" (just a dict) with some values.

You can add more than one event handler function.

And your application won't start receiving requests until all the startup event handlers have completed.

To add a function that should be run when the application is shutting down, declare it with the event "shutdown":

Here, the shutdown event handler function will write a text line "Application shutdown" to a file log.txt.

In the open() function, the mode="a" means "append", so, the line will be added after whatever is on that file, without overwriting the previous contents.

Notice that in this case we are using a standard Python open() function that interacts with a file.

So, it involves I/O (input/output), that requires "waiting" for things to be written to disk.

But open() doesn't use async and await.

So, we declare the event handler function with standard def instead of async def.

There's a high chance that the logic for your startup and shutdown is connected, you might want to start something and then finish it, acquire a resource and then release it, etc.

Doing that in separated functions that don't share logic or variables together is more difficult as you would need to store values in global variables or similar tricks.

Because of that, it's now recommended to instead use the lifespan as explained above.

Just a technical detail for the curious nerds. 🤓

Underneath, in the ASGI technical specification, this is part of the Lifespan Protocol, and it defines events called startup and shutdown.

You can read more about the Starlette lifespan handlers in Starlette's Lifespan' docs.

Including how to handle lifespan state that can be used in other areas of your code.

🚨 Keep in mind that these lifespan events (startup and shutdown) will only be executed for the main application, not for Sub Applications - Mounts.

**Examples:**

Example 1 (python):
```python
from contextlib import asynccontextmanager

from fastapi import FastAPI


def fake_answer_to_everything_ml_model(x: float):
    return x * 42


ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/predict")
async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    return {"result": result}
```

Example 2 (python):
```python
from contextlib import asynccontextmanager

from fastapi import FastAPI


def fake_answer_to_everything_ml_model(x: float):
    return x * 42


ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/predict")
async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    return {"result": result}
```

Example 3 (python):
```python
from contextlib import asynccontextmanager

from fastapi import FastAPI


def fake_answer_to_everything_ml_model(x: float):
    return x * 42


ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/predict")
async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    return {"result": result}
```

Example 4 (typescript):
```typescript
with open("file.txt") as file:
    file.read()
```

---

## Templating - Jinja2Templates¶

**URL:** https://fastapi.tiangolo.com/reference/templating/

**Contents:**
- Templating - Jinja2Templates¶
- fastapi.templating.Jinja2Templates ¶
  - context_processors instance-attribute ¶
  - env instance-attribute ¶
  - get_template ¶
  - TemplateResponse ¶

You can use the Jinja2Templates class to render Jinja templates.

Read more about it in the FastAPI docs for Templates.

You can import it directly from fastapi.templating:

templates = Jinja2Templates("templates")

return templates.TemplateResponse("index.html", {"request": request})

**Examples:**

Example 1 (sql):
```sql
from fastapi.templating import Jinja2Templates
```

Example 2 (rust):
```rust
Jinja2Templates(
    directory: (
        str | PathLike[str] | Sequence[str | PathLike[str]]
    ),
    *,
    context_processors: (
        list[Callable[[Request], dict[str, Any]]] | None
    ) = None,
    **env_options: Any
)
```

Example 3 (rust):
```rust
Jinja2Templates(
    *,
    env: Environment,
    context_processors: (
        list[Callable[[Request], dict[str, Any]]] | None
    ) = None
)
```

Example 4 (rust):
```rust
Jinja2Templates(
    directory=None,
    *,
    context_processors=None,
    env=None,
    **env_options
)
```

---

## Testing WebSockets¶

**URL:** https://fastapi.tiangolo.com/advanced/testing-websockets/

**Contents:**
- Testing WebSockets¶

You can use the same TestClient to test WebSockets.

For this, you use the TestClient in a with statement, connecting to the WebSocket:

For more details, check Starlette's documentation for testing WebSockets.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"msg": "Hello WebSocket"})
    await websocket.close()


def test_read_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_json()
        assert data == {"msg": "Hello WebSocket"}
```

---

## Sub Applications - Mounts¶

**URL:** https://fastapi.tiangolo.com/advanced/sub-applications/

**Contents:**
- Sub Applications - Mounts¶
- Mounting a FastAPI application¶
  - Top-level application¶
  - Sub-application¶
  - Mount the sub-application¶
  - Check the automatic API docs¶
  - Technical Details: root_path¶

If you need to have two independent FastAPI applications, with their own independent OpenAPI and their own docs UIs, you can have a main app and "mount" one (or more) sub-application(s).

"Mounting" means adding a completely "independent" application in a specific path, that then takes care of handling everything under that path, with the path operations declared in that sub-application.

First, create the main, top-level, FastAPI application, and its path operations:

Then, create your sub-application, and its path operations.

This sub-application is just another standard FastAPI application, but this is the one that will be "mounted":

In your top-level application, app, mount the sub-application, subapi.

In this case, it will be mounted at the path /subapi:

Now, run the fastapi command with your file:

And open the docs at http://127.0.0.1:8000/docs.

You will see the automatic API docs for the main app, including only its own path operations:

And then, open the docs for the sub-application, at http://127.0.0.1:8000/subapi/docs.

You will see the automatic API docs for the sub-application, including only its own path operations, all under the correct sub-path prefix /subapi:

If you try interacting with any of the two user interfaces, they will work correctly, because the browser will be able to talk to each specific app or sub-app.

When you mount a sub-application as described above, FastAPI will take care of communicating the mount path for the sub-application using a mechanism from the ASGI specification called a root_path.

That way, the sub-application will know to use that path prefix for the docs UI.

And the sub-application could also have its own mounted sub-applications and everything would work correctly, because FastAPI handles all these root_paths automatically.

You will learn more about the root_path and how to use it explicitly in the section about Behind a Proxy.

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}


subapi = FastAPI()


@subapi.get("/sub")
def read_sub():
    return {"message": "Hello World from sub API"}


app.mount("/subapi", subapi)
```

Example 2 (python):
```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}


subapi = FastAPI()


@subapi.get("/sub")
def read_sub():
    return {"message": "Hello World from sub API"}


app.mount("/subapi", subapi)
```

Example 3 (python):
```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}


subapi = FastAPI()


@subapi.get("/sub")
def read_sub():
    return {"message": "Hello World from sub API"}


app.mount("/subapi", subapi)
```

---

## Using Dataclasses¶

**URL:** https://fastapi.tiangolo.com/advanced/dataclasses/

**Contents:**
- Using Dataclasses¶
- Dataclasses in response_model¶
- Dataclasses in Nested Data Structures¶
- Learn More¶
- Version¶

FastAPI is built on top of Pydantic, and I have been showing you how to use Pydantic models to declare requests and responses.

But FastAPI also supports using dataclasses the same way:

This is still supported thanks to Pydantic, as it has internal support for dataclasses.

So, even with the code above that doesn't use Pydantic explicitly, FastAPI is using Pydantic to convert those standard dataclasses to Pydantic's own flavor of dataclasses.

And of course, it supports the same:

This works the same way as with Pydantic models. And it is actually achieved in the same way underneath, using Pydantic.

Keep in mind that dataclasses can't do everything Pydantic models can do.

So, you might still need to use Pydantic models.

But if you have a bunch of dataclasses laying around, this is a nice trick to use them to power a web API using FastAPI. 🤓

You can also use dataclasses in the response_model parameter:

The dataclass will be automatically converted to a Pydantic dataclass.

This way, its schema will show up in the API docs user interface:

You can also combine dataclasses with other type annotations to make nested data structures.

In some cases, you might still have to use Pydantic's version of dataclasses. For example, if you have errors with the automatically generated API documentation.

In that case, you can simply swap the standard dataclasses with pydantic.dataclasses, which is a drop-in replacement:

We still import field from standard dataclasses.

pydantic.dataclasses is a drop-in replacement for dataclasses.

The Author dataclass includes a list of Item dataclasses.

The Author dataclass is used as the response_model parameter.

You can use other standard type annotations with dataclasses as the request body.

In this case, it's a list of Item dataclasses.

Here we are returning a dictionary that contains items which is a list of dataclasses.

FastAPI is still capable of serializing the data to JSON.

Here the response_model is using a type annotation of a list of Author dataclasses.

Again, you can combine dataclasses with standard type annotations.

Notice that this path operation function uses regular def instead of async def.

As always, in FastAPI you can combine def and async def as needed.

If you need a refresher about when to use which, check out the section "In a hurry?" in the docs about async and await.

This path operation function is not returning dataclasses (although it could), but a list of dictionaries with internal data.

FastAPI will use the response_model parameter (that includes dataclasses) to convert the response.

You can combine dataclasses with other type annotations in many different combinations to form complex data structures.

Check the in-code annotation tips above to see more specific details.

You can also combine dataclasses with other Pydantic models, inherit from them, include them in your own models, etc.

To learn more, check the Pydantic docs about dataclasses.

This is available since FastAPI version 0.67.0. 🔖

**Examples:**

Example 1 (python):
```python
from dataclasses import dataclass

from fastapi import FastAPI


@dataclass
class Item:
    name: str
    price: float
    description: str | None = None
    tax: float | None = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item
```

Example 2 (python):
```python
from dataclasses import dataclass
from typing import Union

from fastapi import FastAPI


@dataclass
class Item:
    name: str
    price: float
    description: Union[str, None] = None
    tax: Union[float, None] = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item
```

Example 3 (python):
```python
from dataclasses import dataclass, field

from fastapi import FastAPI


@dataclass
class Item:
    name: str
    price: float
    tags: list[str] = field(default_factory=list)
    description: str | None = None
    tax: float | None = None


app = FastAPI()


@app.get("/items/next", response_model=Item)
async def read_next_item():
    return {
        "name": "Island In The Moon",
        "price": 12.99,
        "description": "A place to be playin' and havin' fun",
        "tags": ["breater"],
    }
```

Example 4 (python):
```python
from dataclasses import dataclass, field
from typing import Union

from fastapi import FastAPI


@dataclass
class Item:
    name: str
    price: float
    tags: list[str] = field(default_factory=list)
    description: Union[str, None] = None
    tax: Union[float, None] = None


app = FastAPI()


@app.get("/items/next", response_model=Item)
async def read_next_item():
    return {
        "name": "Island In The Moon",
        "price": 12.99,
        "description": "A place to be playin' and havin' fun",
        "tags": ["breater"],
    }
```

---

## WebSockets¶

**URL:** https://fastapi.tiangolo.com/advanced/websockets/

**Contents:**
- WebSockets¶
- Install websockets¶
- WebSockets client¶
  - In production¶
- Create a websocket¶
- Await for messages and send messages¶
- Try it¶
- Using Depends and others¶
  - Try the WebSockets with dependencies¶
- Handling disconnections and multiple clients¶

You can use WebSockets with FastAPI.

Make sure you create a virtual environment, activate it, and install websockets (a Python library that makes it easy to use the "WebSocket" protocol):

In your production system, you probably have a frontend created with a modern framework like React, Vue.js or Angular.

And to communicate using WebSockets with your backend you would probably use your frontend's utilities.

Or you might have a native mobile application that communicates with your WebSocket backend directly, in native code.

Or you might have any other way to communicate with the WebSocket endpoint.

But for this example, we'll use a very simple HTML document with some JavaScript, all inside a long string.

This, of course, is not optimal and you wouldn't use it for production.

In production you would have one of the options above.

But it's the simplest way to focus on the server-side of WebSockets and have a working example:

In your FastAPI application, create a websocket:

You could also use from starlette.websockets import WebSocket.

FastAPI provides the same WebSocket directly just as a convenience for you, the developer. But it comes directly from Starlette.

In your WebSocket route you can await for messages and send messages.

You can receive and send binary, text, and JSON data.

If your file is named main.py, run your application with:

Open your browser at http://127.0.0.1:8000.

You will see a simple page like:

You can type messages in the input box, and send them:

And your FastAPI application with WebSockets will respond back:

You can send (and receive) many messages:

And all of them will use the same WebSocket connection.

In WebSocket endpoints you can import from fastapi and use:

They work the same way as for other FastAPI endpoints/path operations:

Prefer to use the Annotated version if possible.

Prefer to use the Annotated version if possible.

As this is a WebSocket it doesn't really make sense to raise an HTTPException, instead we raise a WebSocketException.

You can use a closing code from the valid codes defined in the specification.

If your file is named main.py, run your application with:

Open your browser at http://127.0.0.1:8000.

Notice that the query token will be handled by a dependency.

With that you can connect the WebSocket and then send and receive messages:

When a WebSocket connection is closed, the await websocket.receive_text() will raise a WebSocketDisconnect exception, which you can then catch and handle like in this example.

That will raise the WebSocketDisconnect exception, and all the other clients will receive a message like:

The app above is a minimal and simple example to demonstrate how to handle and broadcast messages to several WebSocket connections.

But keep in mind that, as everything is handled in memory, in a single list, it will only work while the process is running, and will only work with a single process.

If you need something easy to integrate with FastAPI but that is more robust, supported by Redis, PostgreSQL or others, check encode/broadcaster.

To learn more about the options, check Starlette's documentation for:

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
```

Example 2 (python):
```python
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
```

Example 3 (python):
```python
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
```

Example 4 (python):
```python
from typing import Annotated

from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Query,
    WebSocket,
    WebSocketException,
    status,
)
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
            <button onclick="connect(event)">Connect</button>
            <hr>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var ws = null;
            function connect(event) {
                var itemId = document.getElementById("itemId")
                var token = document.getElementById("token")
                ws = new WebSocket("ws://localhost:8000/items/" + itemId.value + "/ws?token=" + token.value);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


async def get_cookie_or_token(
    websocket: WebSocket,
    session: Annotated[str | None, Cookie()] = None,
    token: Annotated[str | None, Query()] = None,
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@app.websocket("/items/{item_id}/ws")
async def websocket_endpoint(
    *,
    websocket: WebSocket,
    item_id: str,
    q: int | None = None,
    cookie_or_token: Annotated[str, Depends(get_cookie_or_token)],
):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(
            f"Session cookie or query token value is: {cookie_or_token}"
        )
        if q is not None:
            await websocket.send_text(f"Query parameter q is: {q}")
        await websocket.send_text(f"Message text was: {data}, for item ID: {item_id}")
```

---

## Testing Events: lifespan and startup - shutdown¶

**URL:** https://fastapi.tiangolo.com/advanced/testing-events/

**Contents:**
- Testing Events: lifespan and startup - shutdown¶

When you need lifespan to run in your tests, you can use the TestClient with a with statement:

You can read more details about the "Running lifespan in tests in the official Starlette documentation site."

For the deprecated startup and shutdown events, you can use the TestClient as follows:

**Examples:**

Example 1 (python):
```python
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.testclient import TestClient

items = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}
    yield
    # clean up items
    items.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/items/{item_id}")
async def read_items(item_id: str):
    return items[item_id]


def test_read_items():
    # Before the lifespan starts, "items" is still empty
    assert items == {}

    with TestClient(app) as client:
        # Inside the "with TestClient" block, the lifespan starts and items added
        assert items == {"foo": {"name": "Fighters"}, "bar": {"name": "Tenders"}}

        response = client.get("/items/foo")
        assert response.status_code == 200
        assert response.json() == {"name": "Fighters"}

        # After the requests is done, the items are still there
        assert items == {"foo": {"name": "Fighters"}, "bar": {"name": "Tenders"}}

    # The end of the "with TestClient" block simulates terminating the app, so
    # the lifespan ends and items are cleaned up
    assert items == {}
```

Example 2 (python):
```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

items = {}


@app.on_event("startup")
async def startup_event():
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}


@app.get("/items/{item_id}")
async def read_items(item_id: str):
    return items[item_id]


def test_read_items():
    with TestClient(app) as client:
        response = client.get("/items/foo")
        assert response.status_code == 200
        assert response.json() == {"name": "Fighters"}
```

---
