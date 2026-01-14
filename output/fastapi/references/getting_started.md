# Fastapi - Getting Started

**Pages:** 8

---

## First Steps¶

**URL:** https://fastapi.tiangolo.com/tutorial/first-steps/

**Contents:**
- First Steps¶
  - Check it¶
  - Interactive API docs¶
  - Alternative API docs¶
  - OpenAPI¶
    - "Schema"¶
    - API "schema"¶
    - Data "schema"¶
    - OpenAPI and JSON Schema¶
    - Check the openapi.json¶

The simplest FastAPI file could look like this:

Copy that to a file main.py.

In the output, there's a line with something like:

That line shows the URL where your app is being served, in your local machine.

Open your browser at http://127.0.0.1:8000.

You will see the JSON response as:

Now go to http://127.0.0.1:8000/docs.

You will see the automatic interactive API documentation (provided by Swagger UI):

And now, go to http://127.0.0.1:8000/redoc.

You will see the alternative automatic documentation (provided by ReDoc):

FastAPI generates a "schema" with all your API using the OpenAPI standard for defining APIs.

A "schema" is a definition or description of something. Not the code that implements it, but just an abstract description.

In this case, OpenAPI is a specification that dictates how to define a schema of your API.

This schema definition includes your API paths, the possible parameters they take, etc.

The term "schema" might also refer to the shape of some data, like a JSON content.

In that case, it would mean the JSON attributes, and data types they have, etc.

OpenAPI defines an API schema for your API. And that schema includes definitions (or "schemas") of the data sent and received by your API using JSON Schema, the standard for JSON data schemas.

If you are curious about how the raw OpenAPI schema looks like, FastAPI automatically generates a JSON (schema) with the descriptions of all your API.

You can see it directly at: http://127.0.0.1:8000/openapi.json.

It will show a JSON starting with something like:

The OpenAPI schema is what powers the two interactive documentation systems included.

And there are dozens of alternatives, all based on OpenAPI. You could easily add any of those alternatives to your application built with FastAPI.

You could also use it to generate code automatically, for clients that communicate with your API. For example, frontend, mobile or IoT applications.

You can optionally deploy your FastAPI app to FastAPI Cloud, go and join the waiting list if you haven't. 🚀

If you already have a FastAPI Cloud account (we invited you from the waiting list 😉), you can deploy your application with one command.

Before deploying, make sure you are logged in:

Then deploy your app:

That's it! Now you can access your app at that URL. ✨

FastAPI is a Python class that provides all the functionality for your API.

FastAPI is a class that inherits directly from Starlette.

You can use all the Starlette functionality with FastAPI too.

Here the app variable will be an "instance" of the class FastAPI.

This will be the main point of interaction to create all your API.

"Path" here refers to the last part of the URL starting from the first /.

...the path would be:

A "path" is also commonly called an "endpoint" or a "route".

While building an API, the "path" is the main way to separate "concerns" and "resources".

"Operation" here refers to one of the HTTP "methods".

...and the more exotic ones:

In the HTTP protocol, you can communicate to each path using one (or more) of these "methods".

When building APIs, you normally use these specific HTTP methods to perform a specific action.

So, in OpenAPI, each of the HTTP methods is called an "operation".

We are going to call them "operations" too.

The @app.get("/") tells FastAPI that the function right below is in charge of handling requests that go to:

That @something syntax in Python is called a "decorator".

You put it on top of a function. Like a pretty decorative hat (I guess that's where the term came from).

A "decorator" takes the function below and does something with it.

In our case, this decorator tells FastAPI that the function below corresponds to the path / with an operation get.

It is the "path operation decorator".

You can also use the other operations:

And the more exotic ones:

You are free to use each operation (HTTP method) as you wish.

FastAPI doesn't enforce any specific meaning.

The information here is presented as a guideline, not a requirement.

For example, when using GraphQL you normally perform all the actions using only POST operations.

This is our "path operation function":

This is a Python function.

It will be called by FastAPI whenever it receives a request to the URL "/" using a GET operation.

In this case, it is an async function.

You could also define it as a normal function instead of async def:

If you don't know the difference, check the Async: "In a hurry?".

You can return a dict, list, singular values as str, int, etc.

You can also return Pydantic models (you'll see more about that later).

There are many other objects and models that will be automatically converted to JSON (including ORMs, etc). Try using your favorite ones, it's highly probable that they are already supported.

Deploy your app to FastAPI Cloud with one command: fastapi deploy. 🎉

FastAPI Cloud is built by the same author and team behind FastAPI.

It streamlines the process of building, deploying, and accessing an API with minimal effort.

It brings the same developer experience of building apps with FastAPI to deploying them to the cloud. 🎉

FastAPI Cloud is the primary sponsor and funding provider for the FastAPI and friends open source projects. ✨

FastAPI is open source and based on standards. You can deploy FastAPI apps to any cloud provider you choose.

Follow your cloud provider's guides to deploy FastAPI apps with them. 🤓

**Examples:**

Example 1 (python):
```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

Example 2 (yaml):
```yaml
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Example 3 (json):
```json
{"message": "Hello World"}
```

Example 4 (json):
```json
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {



...
```

---

## Concurrency and async / await¶

**URL:** https://fastapi.tiangolo.com/async/

**Contents:**
- Concurrency and async / await¶
- In a hurry?¶
- Technical Details¶
- Asynchronous Code¶
  - Concurrency and Burgers¶
  - Concurrent Burgers¶
  - Parallel Burgers¶
  - Burger Conclusion¶
  - Is concurrency better than parallelism?¶
  - Concurrency + Parallelism: Web + Machine Learning¶

Details about the async def syntax for path operation functions and some background about asynchronous code, concurrency, and parallelism.

If you are using third party libraries that tell you to call them with await, like:

Then, declare your path operation functions with async def like:

You can only use await inside of functions created with async def.

If you are using a third party library that communicates with something (a database, an API, the file system, etc.) and doesn't have support for using await, (this is currently the case for most database libraries), then declare your path operation functions as normally, with just def, like:

If your application (somehow) doesn't have to communicate with anything else and wait for it to respond, use async def, even if you don't need to use await inside.

If you just don't know, use normal def.

Note: You can mix def and async def in your path operation functions as much as you need and define each one using the best option for you. FastAPI will do the right thing with them.

Anyway, in any of the cases above, FastAPI will still work asynchronously and be extremely fast.

But by following the steps above, it will be able to do some performance optimizations.

Modern versions of Python have support for "asynchronous code" using something called "coroutines", with async and await syntax.

Let's see that phrase by parts in the sections below:

Asynchronous code just means that the language 💬 has a way to tell the computer / program 🤖 that at some point in the code, it 🤖 will have to wait for something else to finish somewhere else. Let's say that something else is called "slow-file" 📝.

So, during that time, the computer can go and do some other work, while "slow-file" 📝 finishes.

Then the computer / program 🤖 will come back every time it has a chance because it's waiting again, or whenever it 🤖 finished all the work it had at that point. And it 🤖 will see if any of the tasks it was waiting for have already finished, doing whatever it had to do.

Next, it 🤖 takes the first task to finish (let's say, our "slow-file" 📝) and continues whatever it had to do with it.

That "wait for something else" normally refers to I/O operations that are relatively "slow" (compared to the speed of the processor and the RAM memory), like waiting for:

As the execution time is consumed mostly by waiting for I/O operations, they call them "I/O bound" operations.

It's called "asynchronous" because the computer / program doesn't have to be "synchronized" with the slow task, waiting for the exact moment that the task finishes, while doing nothing, to be able to take the task result and continue the work.

Instead of that, by being an "asynchronous" system, once finished, the task can wait in line a little bit (some microseconds) for the computer / program to finish whatever it went to do, and then come back to take the results and continue working with them.

For "synchronous" (contrary to "asynchronous") they commonly also use the term "sequential", because the computer / program follows all the steps in sequence before switching to a different task, even if those steps involve waiting.

This idea of asynchronous code described above is also sometimes called "concurrency". It is different from "parallelism".

Concurrency and parallelism both relate to "different things happening more or less at the same time".

But the details between concurrency and parallelism are quite different.

To see the difference, imagine the following story about burgers:

You go with your crush to get fast food, you stand in line while the cashier takes the orders from the people in front of you. 😍

Then it's your turn, you place your order of 2 very fancy burgers for your crush and you. 🍔🍔

The cashier says something to the cook in the kitchen so they know they have to prepare your burgers (even though they are currently preparing the ones for the previous clients).

The cashier gives you the number of your turn.

While you are waiting, you go with your crush and pick a table, you sit and talk with your crush for a long time (as your burgers are very fancy and take some time to prepare).

As you are sitting at the table with your crush, while you wait for the burgers, you can spend that time admiring how awesome, cute and smart your crush is ✨😍✨.

While waiting and talking to your crush, from time to time, you check the number displayed on the counter to see if it's your turn already.

Then at some point, it finally is your turn. You go to the counter, get your burgers and come back to the table.

You and your crush eat the burgers and have a nice time. ✨

Beautiful illustrations by Ketrina Thompson. 🎨

Imagine you are the computer / program 🤖 in that story.

While you are at the line, you are just idle 😴, waiting for your turn, not doing anything very "productive". But the line is fast because the cashier is only taking the orders (not preparing them), so that's fine.

Then, when it's your turn, you do actual "productive" work, you process the menu, decide what you want, get your crush's choice, pay, check that you give the correct bill or card, check that you are charged correctly, check that the order has the correct items, etc.

But then, even though you still don't have your burgers, your work with the cashier is "on pause" ⏸, because you have to wait 🕙 for your burgers to be ready.

But as you go away from the counter and sit at the table with a number for your turn, you can switch 🔀 your attention to your crush, and "work" ⏯ 🤓 on that. Then you are again doing something very "productive" as is flirting with your crush 😍.

Then the cashier 💁 says "I'm finished with doing the burgers" by putting your number on the counter's display, but you don't jump like crazy immediately when the displayed number changes to your turn number. You know no one will steal your burgers because you have the number of your turn, and they have theirs.

So you wait for your crush to finish the story (finish the current work ⏯ / task being processed 🤓), smile gently and say that you are going for the burgers ⏸.

Then you go to the counter 🔀, to the initial task that is now finished ⏯, pick the burgers, say thanks and take them to the table. That finishes that step / task of interaction with the counter ⏹. That in turn, creates a new task, of "eating burgers" 🔀 ⏯, but the previous one of "getting burgers" is finished ⏹.

Now let's imagine these aren't "Concurrent Burgers", but "Parallel Burgers".

You go with your crush to get parallel fast food.

You stand in line while several (let's say 8) cashiers that at the same time are cooks take the orders from the people in front of you.

Everyone before you is waiting for their burgers to be ready before leaving the counter because each of the 8 cashiers goes and prepares the burger right away before getting the next order.

Then it's finally your turn, you place your order of 2 very fancy burgers for your crush and you.

The cashier goes to the kitchen.

You wait, standing in front of the counter 🕙, so that no one else takes your burgers before you do, as there are no numbers for turns.

As you and your crush are busy not letting anyone get in front of you and take your burgers whenever they arrive, you cannot pay attention to your crush. 😞

This is "synchronous" work, you are "synchronized" with the cashier/cook 👨‍🍳. You have to wait 🕙 and be there at the exact moment that the cashier/cook 👨‍🍳 finishes the burgers and gives them to you, or otherwise, someone else might take them.

Then your cashier/cook 👨‍🍳 finally comes back with your burgers, after a long time waiting 🕙 there in front of the counter.

You take your burgers and go to the table with your crush.

You just eat them, and you are done. ⏹

There was not much talk or flirting as most of the time was spent waiting 🕙 in front of the counter. 😞

Beautiful illustrations by Ketrina Thompson. 🎨

In this scenario of the parallel burgers, you are a computer / program 🤖 with two processors (you and your crush), both waiting 🕙 and dedicating their attention ⏯ to be "waiting on the counter" 🕙 for a long time.

The fast food store has 8 processors (cashiers/cooks). While the concurrent burgers store might have had only 2 (one cashier and one cook).

But still, the final experience is not the best. 😞

This would be the parallel equivalent story for burgers. 🍔

For a more "real life" example of this, imagine a bank.

Up to recently, most of the banks had multiple cashiers 👨‍💼👨‍💼👨‍💼👨‍💼 and a big line 🕙🕙🕙🕙🕙🕙🕙🕙.

All of the cashiers doing all the work with one client after the other 👨‍💼⏯.

And you have to wait 🕙 in the line for a long time or you lose your turn.

You probably wouldn't want to take your crush 😍 with you to run errands at the bank 🏦.

In this scenario of "fast food burgers with your crush", as there is a lot of waiting 🕙, it makes a lot more sense to have a concurrent system ⏸🔀⏯.

This is the case for most of the web applications.

Many, many users, but your server is waiting 🕙 for their not-so-good connection to send their requests.

And then waiting 🕙 again for the responses to come back.

This "waiting" 🕙 is measured in microseconds, but still, summing it all, it's a lot of waiting in the end.

That's why it makes a lot of sense to use asynchronous ⏸🔀⏯ code for web APIs.

This kind of asynchronicity is what made NodeJS popular (even though NodeJS is not parallel) and that's the strength of Go as a programming language.

And that's the same level of performance you get with FastAPI.

And as you can have parallelism and asynchronicity at the same time, you get higher performance than most of the tested NodeJS frameworks and on par with Go, which is a compiled language closer to C (all thanks to Starlette).

Nope! That's not the moral of the story.

Concurrency is different than parallelism. And it is better on specific scenarios that involve a lot of waiting. Because of that, it generally is a lot better than parallelism for web application development. But not for everything.

So, to balance that out, imagine the following short story:

You have to clean a big, dirty house.

Yep, that's the whole story.

There's no waiting 🕙 anywhere, just a lot of work to be done, on multiple places of the house.

You could have turns as in the burgers example, first the living room, then the kitchen, but as you are not waiting 🕙 for anything, just cleaning and cleaning, the turns wouldn't affect anything.

It would take the same amount of time to finish with or without turns (concurrency) and you would have done the same amount of work.

But in this case, if you could bring the 8 ex-cashier/cooks/now-cleaners, and each one of them (plus you) could take a zone of the house to clean it, you could do all the work in parallel, with the extra help, and finish much sooner.

In this scenario, each one of the cleaners (including you) would be a processor, doing their part of the job.

And as most of the execution time is taken by actual work (instead of waiting), and the work in a computer is done by a CPU, they call these problems "CPU bound".

Common examples of CPU bound operations are things that require complex math processing.

With FastAPI you can take advantage of concurrency that is very common for web development (the same main attraction of NodeJS).

But you can also exploit the benefits of parallelism and multiprocessing (having multiple processes running in parallel) for CPU bound workloads like those in Machine Learning systems.

That, plus the simple fact that Python is the main language for Data Science, Machine Learning and especially Deep Learning, make FastAPI a very good match for Data Science / Machine Learning web APIs and applications (among many others).

To see how to achieve this parallelism in production see the section about Deployment.

Modern versions of Python have a very intuitive way to define asynchronous code. This makes it look just like normal "sequential" code and do the "awaiting" for you at the right moments.

When there is an operation that will require waiting before giving the results and has support for these new Python features, you can code it like:

The key here is the await. It tells Python that it has to wait ⏸ for get_burgers(2) to finish doing its thing 🕙 before storing the results in burgers. With that, Python will know that it can go and do something else 🔀 ⏯ in the meanwhile (like receiving another request).

For await to work, it has to be inside a function that supports this asynchronicity. To do that, you just declare it with async def:

With async def, Python knows that, inside that function, it has to be aware of await expressions, and that it can "pause" ⏸ the execution of that function and go do something else 🔀 before coming back.

When you want to call an async def function, you have to "await" it. So, this won't work:

So, if you are using a library that tells you that you can call it with await, you need to create the path operation functions that uses it with async def, like in:

You might have noticed that await can only be used inside of functions defined with async def.

But at the same time, functions defined with async def have to be "awaited". So, functions with async def can only be called inside of functions defined with async def too.

So, about the egg and the chicken, how do you call the first async function?

If you are working with FastAPI you don't have to worry about that, because that "first" function will be your path operation function, and FastAPI will know how to do the right thing.

But if you want to use async / await without FastAPI, you can do it as well.

Starlette (and FastAPI) are based on AnyIO, which makes it compatible with both Python's standard library asyncio and Trio.

In particular, you can directly use AnyIO for your advanced concurrency use cases that require more advanced patterns in your own code.

And even if you were not using FastAPI, you could also write your own async applications with AnyIO to be highly compatible and get its benefits (e.g. structured concurrency).

I created another library on top of AnyIO, as a thin layer on top, to improve a bit the type annotations and get better autocompletion, inline errors, etc. It also has a friendly introduction and tutorial to help you understand and write your own async code: Asyncer. It would be particularly useful if you need to combine async code with regular (blocking/synchronous) code.

This style of using async and await is relatively new in the language.

But it makes working with asynchronous code a lot easier.

This same syntax (or almost identical) was also included recently in modern versions of JavaScript (in Browser and NodeJS).

But before that, handling asynchronous code was quite more complex and difficult.

In previous versions of Python, you could have used threads or Gevent. But the code is way more complex to understand, debug, and think about.

In previous versions of NodeJS / Browser JavaScript, you would have used "callbacks". Which leads to "callback hell".

Coroutine is just the very fancy term for the thing returned by an async def function. Python knows that it is something like a function, that it can start and that it will end at some point, but that it might be paused ⏸ internally too, whenever there is an await inside of it.

But all this functionality of using asynchronous code with async and await is many times summarized as using "coroutines". It is comparable to the main key feature of Go, the "Goroutines".

Let's see the same phrase from above:

Modern versions of Python have support for "asynchronous code" using something called "coroutines", with async and await syntax.

That should make more sense now. ✨

All that is what powers FastAPI (through Starlette) and what makes it have such an impressive performance.

You can probably skip this.

These are very technical details of how FastAPI works underneath.

If you have quite some technical knowledge (coroutines, threads, blocking, etc.) and are curious about how FastAPI handles async def vs normal def, go ahead.

When you declare a path operation function with normal def instead of async def, it is run in an external threadpool that is then awaited, instead of being called directly (as it would block the server).

If you are coming from another async framework that does not work in the way described above and you are used to defining trivial compute-only path operation functions with plain def for a tiny performance gain (about 100 nanoseconds), please note that in FastAPI the effect would be quite opposite. In these cases, it's better to use async def unless your path operation functions use code that performs blocking I/O.

Still, in both situations, chances are that FastAPI will still be faster than (or at least comparable to) your previous framework.

The same applies for dependencies. If a dependency is a standard def function instead of async def, it is run in the external threadpool.

You can have multiple dependencies and sub-dependencies requiring each other (as parameters of the function definitions), some of them might be created with async def and some with normal def. It would still work, and the ones created with normal def would be called on an external thread (from the threadpool) instead of being "awaited".

Any other utility function that you call directly can be created with normal def or async def and FastAPI won't affect the way you call it.

This is in contrast to the functions that FastAPI calls for you: path operation functions and dependencies.

If your utility function is a normal function with def, it will be called directly (as you write it in your code), not in a threadpool, if the function is created with async def then you should await for that function when you call it in your code.

Again, these are very technical details that would probably be useful if you came searching for them.

Otherwise, you should be good with the guidelines from the section above: In a hurry?.

**Examples:**

Example 1 (csharp):
```csharp
results = await some_library()
```

Example 2 (python):
```python
@app.get('/')
async def read_results():
    results = await some_library()
    return results
```

Example 3 (python):
```python
@app.get('/')
def results():
    results = some_library()
    return results
```

Example 4 (csharp):
```csharp
burgers = await get_burgers(2)
```

---

## Security - First Steps¶

**URL:** https://fastapi.tiangolo.com/tutorial/security/first-steps/

**Contents:**
- Security - First Steps¶
- How it looks¶
- Create main.py¶
- Run it¶
- Check it¶
- The password flow¶
- FastAPI's OAuth2PasswordBearer¶
  - Use it¶
- What it does¶
- Recap¶

Let's imagine that you have your backend API in some domain.

And you have a frontend in another domain or in a different path of the same domain (or in a mobile application).

And you want to have a way for the frontend to authenticate with the backend, using a username and password.

We can use OAuth2 to build that with FastAPI.

But let's save you the time of reading the full long specification just to find those little pieces of information you need.

Let's use the tools provided by FastAPI to handle security.

Let's first just use the code and see how it works, and then we'll come back to understand what's happening.

Copy the example in a file main.py:

Prefer to use the Annotated version if possible.

The python-multipart package is automatically installed with FastAPI when you run the pip install "fastapi[standard]" command.

However, if you use the pip install fastapi command, the python-multipart package is not included by default.

To install it manually, make sure you create a virtual environment, activate it, and then install it with:

This is because OAuth2 uses "form data" for sending the username and password.

Run the example with:

Go to the interactive docs at: http://127.0.0.1:8000/docs.

You will see something like this:

You already have a shiny new "Authorize" button.

And your path operation has a little lock in the top-right corner that you can click.

And if you click it, you have a little authorization form to type a username and password (and other optional fields):

It doesn't matter what you type in the form, it won't work yet. But we'll get there.

This is of course not the frontend for the final users, but it's a great automatic tool to document interactively all your API.

It can be used by the frontend team (that can also be yourself).

It can be used by third party applications and systems.

And it can also be used by yourself, to debug, check and test the same application.

Now let's go back a bit and understand what is all that.

The password "flow" is one of the ways ("flows") defined in OAuth2, to handle security and authentication.

OAuth2 was designed so that the backend or API could be independent of the server that authenticates the user.

But in this case, the same FastAPI application will handle the API and the authentication.

So, let's review it from that simplified point of view:

FastAPI provides several tools, at different levels of abstraction, to implement these security features.

In this example we are going to use OAuth2, with the Password flow, using a Bearer token. We do that using the OAuth2PasswordBearer class.

A "bearer" token is not the only option.

But it's the best one for our use case.

And it might be the best for most use cases, unless you are an OAuth2 expert and know exactly why there's another option that better suits your needs.

In that case, FastAPI also provides you with the tools to build it.

When we create an instance of the OAuth2PasswordBearer class we pass in the tokenUrl parameter. This parameter contains the URL that the client (the frontend running in the user's browser) will use to send the username and password in order to get a token.

Prefer to use the Annotated version if possible.

Here tokenUrl="token" refers to a relative URL token that we haven't created yet. As it's a relative URL, it's equivalent to ./token.

Because we are using a relative URL, if your API was located at https://example.com/, then it would refer to https://example.com/token. But if your API was located at https://example.com/api/v1/, then it would refer to https://example.com/api/v1/token.

Using a relative URL is important to make sure your application keeps working even in an advanced use case like Behind a Proxy.

This parameter doesn't create that endpoint / path operation, but declares that the URL /token will be the one that the client should use to get the token. That information is used in OpenAPI, and then in the interactive API documentation systems.

We will soon also create the actual path operation.

If you are a very strict "Pythonista" you might dislike the style of the parameter name tokenUrl instead of token_url.

That's because it is using the same name as in the OpenAPI spec. So that if you need to investigate more about any of these security schemes you can just copy and paste it to find more information about it.

The oauth2_scheme variable is an instance of OAuth2PasswordBearer, but it is also a "callable".

It could be called as:

So, it can be used with Depends.

Now you can pass that oauth2_scheme in a dependency with Depends.

Prefer to use the Annotated version if possible.

This dependency will provide a str that is assigned to the parameter token of the path operation function.

FastAPI will know that it can use this dependency to define a "security scheme" in the OpenAPI schema (and the automatic API docs).

FastAPI will know that it can use the class OAuth2PasswordBearer (declared in a dependency) to define the security scheme in OpenAPI because it inherits from fastapi.security.oauth2.OAuth2, which in turn inherits from fastapi.security.base.SecurityBase.

All the security utilities that integrate with OpenAPI (and the automatic API docs) inherit from SecurityBase, that's how FastAPI can know how to integrate them in OpenAPI.

It will go and look in the request for that Authorization header, check if the value is Bearer plus some token, and will return the token as a str.

If it doesn't see an Authorization header, or the value doesn't have a Bearer token, it will respond with a 401 status code error (UNAUTHORIZED) directly.

You don't even have to check if the token exists to return an error. You can be sure that if your function is executed, it will have a str in that token.

You can try it already in the interactive docs:

We are not verifying the validity of the token yet, but that's a start already.

So, in just 3 or 4 extra lines, you already have some primitive form of security.

**Examples:**

Example 1 (python):
```python
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
```

Example 2 (python):
```python
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

Example 3 (unknown):
```unknown
$ pip install python-multipart
```

Example 4 (python):
```python
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
```

---

## Features¶

**URL:** https://fastapi.tiangolo.com/features/

**Contents:**
- Features¶
- FastAPI features¶
  - Based on open standards¶
  - Automatic docs¶
  - Just Modern Python¶
  - Editor support¶
  - Short¶
  - Validation¶
  - Security and authentication¶
  - Dependency Injection¶

FastAPI gives you the following:

Interactive API documentation and exploration web user interfaces. As the framework is based on OpenAPI, there are multiple options, 2 included by default.

It's all based on standard Python type declarations (thanks to Pydantic). No new syntax to learn. Just standard modern Python.

If you need a 2 minute refresher of how to use Python types (even if you don't use FastAPI), check the short tutorial: Python Types.

You write standard Python with types:

That can then be used like:

**second_user_data means:

Pass the keys and values of the second_user_data dict directly as key-value arguments, equivalent to: User(id=4, name="Mary", joined="2018-11-30")

All the framework was designed to be easy and intuitive to use, all the decisions were tested on multiple editors even before starting development, to ensure the best development experience.

In the Python developer surveys, it's clear that one of the most used features is "autocompletion".

The whole FastAPI framework is based to satisfy that. Autocompletion works everywhere.

You will rarely need to come back to the docs.

Here's how your editor might help you:

You will get completion in code you might even consider impossible before. As for example, the price key inside a JSON body (that could have been nested) that comes from a request.

No more typing the wrong key names, coming back and forth between docs, or scrolling up and down to find if you finally used username or user_name.

It has sensible defaults for everything, with optional configurations everywhere. All the parameters can be fine-tuned to do what you need and to define the API you need.

But by default, it all "just works".

Validation for most (or all?) Python data types, including:

Validation for more exotic types, like:

All the validation is handled by the well-established and robust Pydantic.

Security and authentication integrated. Without any compromise with databases or data models.

All the security schemes defined in OpenAPI, including:

Plus all the security features from Starlette (including session cookies).

All built as reusable tools and components that are easy to integrate with your systems, data stores, relational and NoSQL databases, etc.

FastAPI includes an extremely easy to use, but extremely powerful Dependency Injection system.

Or in other way, no need for them, import and use the code you need.

Any integration is designed to be so simple to use (with dependencies) that you can create a "plug-in" for your application in 2 lines of code using the same structure and syntax used for your path operations.

FastAPI is fully compatible with (and based on) Starlette. So, any additional Starlette code you have, will also work.

FastAPI is actually a sub-class of Starlette. So, if you already know or use Starlette, most of the functionality will work the same way.

With FastAPI you get all of Starlette's features (as FastAPI is just Starlette on steroids):

FastAPI is fully compatible with (and based on) Pydantic. So, any additional Pydantic code you have, will also work.

Including external libraries also based on Pydantic, as ORMs, ODMs for databases.

This also means that in many cases you can pass the same object you get from a request directly to the database, as everything is validated automatically.

The same applies the other way around, in many cases you can just pass the object you get from the database directly to the client.

With FastAPI you get all of Pydantic's features (as FastAPI is based on Pydantic for all the data handling):

**Examples:**

Example 1 (python):
```python
from datetime import date

from pydantic import BaseModel

# Declare a variable as a str
# and get editor support inside the function
def main(user_id: str):
    return user_id


# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

Example 2 (json):
```json
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

---

## Async Tests¶

**URL:** https://fastapi.tiangolo.com/advanced/async-tests/

**Contents:**
- Async Tests¶
- pytest.mark.anyio¶
- HTTPX¶
- Example¶
- Run it¶
- In Detail¶
- Other Asynchronous Function Calls¶

You have already seen how to test your FastAPI applications using the provided TestClient. Up to now, you have only seen how to write synchronous tests, without using async functions.

Being able to use asynchronous functions in your tests could be useful, for example, when you're querying your database asynchronously. Imagine you want to test sending requests to your FastAPI application and then verify that your backend successfully wrote the correct data in the database, while using an async database library.

Let's look at how we can make that work.

If we want to call asynchronous functions in our tests, our test functions have to be asynchronous. AnyIO provides a neat plugin for this, that allows us to specify that some test functions are to be called asynchronously.

Even if your FastAPI application uses normal def functions instead of async def, it is still an async application underneath.

The TestClient does some magic inside to call the asynchronous FastAPI application in your normal def test functions, using standard pytest. But that magic doesn't work anymore when we're using it inside asynchronous functions. By running our tests asynchronously, we can no longer use the TestClient inside our test functions.

The TestClient is based on HTTPX, and luckily, we can use it directly to test the API.

For a simple example, let's consider a file structure similar to the one described in Bigger Applications and Testing:

The file main.py would have:

The file test_main.py would have the tests for main.py, it could look like this now:

You can run your tests as usual via:

The marker @pytest.mark.anyio tells pytest that this test function should be called asynchronously:

Note that the test function is now async def instead of just def as before when using the TestClient.

Then we can create an AsyncClient with the app, and send async requests to it, using await.

This is the equivalent to:

...that we used to make our requests with the TestClient.

Note that we're using async/await with the new AsyncClient - the request is asynchronous.

If your application relies on lifespan events, the AsyncClient won't trigger these events. To ensure they are triggered, use LifespanManager from florimondmanca/asgi-lifespan.

As the testing function is now asynchronous, you can now also call (and await) other async functions apart from sending requests to your FastAPI application in your tests, exactly as you would call them anywhere else in your code.

If you encounter a RuntimeError: Task attached to a different loop when integrating asynchronous function calls in your tests (e.g. when using MongoDB's MotorClient), remember to instantiate objects that need an event loop only within async functions, e.g. an @app.on_event("startup") callback.

**Examples:**

Example 1 (unknown):
```unknown
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Example 2 (python):
```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Tomato"}
```

Example 3 (python):
```python
import pytest
from httpx import ASGITransport, AsyncClient

from .main import app


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}
```

Example 4 (python):
```python
import pytest
from httpx import ASGITransport, AsyncClient

from .main import app


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}
```

---

## Environment Variables¶

**URL:** https://fastapi.tiangolo.com/environment-variables/

**Contents:**
- Environment Variables¶
- Create and Use Env Vars¶
- Read env vars in Python¶
- Types and Validation¶
- PATH Environment Variable¶
  - Installing Python and Updating the PATH¶
- Conclusion¶

If you already know what "environment variables" are and how to use them, feel free to skip this.

An environment variable (also known as "env var") is a variable that lives outside of the Python code, in the operating system, and could be read by your Python code (or by other programs as well).

Environment variables could be useful for handling application settings, as part of the installation of Python, etc.

You can create and use environment variables in the shell (terminal), without needing Python:

You could also create environment variables outside of Python, in the terminal (or with any other method), and then read them in Python.

For example you could have a file main.py with:

The second argument to os.getenv() is the default value to return.

If not provided, it's None by default, here we provide "World" as the default value to use.

Then you could call that Python program:

As environment variables can be set outside of the code, but can be read by the code, and don't have to be stored (committed to git) with the rest of the files, it's common to use them for configurations or settings.

You can also create an environment variable only for a specific program invocation, that is only available to that program, and only for its duration.

To do that, create it right before the program itself, on the same line:

You can read more about it at The Twelve-Factor App: Config.

These environment variables can only handle text strings, as they are external to Python and have to be compatible with other programs and the rest of the system (and even with different operating systems, as Linux, Windows, macOS).

That means that any value read in Python from an environment variable will be a str, and any conversion to a different type or any validation has to be done in code.

You will learn more about using environment variables for handling application settings in the Advanced User Guide - Settings and Environment Variables.

There is a special environment variable called PATH that is used by the operating systems (Linux, macOS, Windows) to find programs to run.

The value of the variable PATH is a long string that is made of directories separated by a colon : on Linux and macOS, and by a semicolon ; on Windows.

For example, the PATH environment variable could look like this:

This means that the system should look for programs in the directories:

This means that the system should look for programs in the directories:

When you type a command in the terminal, the operating system looks for the program in each of those directories listed in the PATH environment variable.

For example, when you type python in the terminal, the operating system looks for a program called python in the first directory in that list.

If it finds it, then it will use it. Otherwise it keeps looking in the other directories.

When you install Python, you might be asked if you want to update the PATH environment variable.

Let's say you install Python and it ends up in a directory /opt/custompython/bin.

If you say yes to update the PATH environment variable, then the installer will add /opt/custompython/bin to the PATH environment variable.

It could look like this:

This way, when you type python in the terminal, the system will find the Python program in /opt/custompython/bin (the last directory) and use that one.

Let's say you install Python and it ends up in a directory C:\opt\custompython\bin.

If you say yes to update the PATH environment variable, then the installer will add C:\opt\custompython\bin to the PATH environment variable.

This way, when you type python in the terminal, the system will find the Python program in C:\opt\custompython\bin (the last directory) and use that one.

The system will find the python program in /opt/custompython/bin and run it.

It would be roughly equivalent to typing:

The system will find the python program in C:\opt\custompython\bin\python and run it.

It would be roughly equivalent to typing:

This information will be useful when learning about Virtual Environments.

With this you should have a basic understanding of what environment variables are and how to use them in Python.

You can also read more about them in the Wikipedia for Environment Variable.

In many cases it's not very obvious how environment variables would be useful and applicable right away. But they keep showing up in many different scenarios when you are developing, so it's good to know about them.

For example, you will need this information in the next section, about Virtual Environments.

**Examples:**

Example 1 (python):
```python
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

Example 2 (unknown):
```unknown
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

Example 3 (yaml):
```yaml
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32
```

Example 4 (unknown):
```unknown
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

---

## Python Types Intro¶

**URL:** https://fastapi.tiangolo.com/python-types/

**Contents:**
- Python Types Intro¶
- Motivation¶
  - Edit it¶
  - Add types¶
- More motivation¶
- Declaring types¶
  - Simple types¶
  - Generic types with type parameters¶
    - Newer versions of Python¶
    - List¶

Python has support for optional "type hints" (also called "type annotations").

These "type hints" or annotations are a special syntax that allow declaring the type of a variable.

By declaring types for your variables, editors and tools can give you better support.

This is just a quick tutorial / refresher about Python type hints. It covers only the minimum necessary to use them with FastAPI... which is actually very little.

FastAPI is all based on these type hints, they give it many advantages and benefits.

But even if you never use FastAPI, you would benefit from learning a bit about them.

If you are a Python expert, and you already know everything about type hints, skip to the next chapter.

Let's start with a simple example:

Calling this program outputs:

The function does the following:

It's a very simple program.

But now imagine that you were writing it from scratch.

At some point you would have started the definition of the function, you had the parameters ready...

But then you have to call "that method that converts the first letter to upper case".

Was it upper? Was it uppercase? first_uppercase? capitalize?

Then, you try with the old programmer's friend, editor autocompletion.

You type the first parameter of the function, first_name, then a dot (.) and then hit Ctrl+Space to trigger the completion.

But, sadly, you get nothing useful:

Let's modify a single line from the previous version.

We will change exactly this fragment, the parameters of the function, from:

Those are the "type hints":

That is not the same as declaring default values like would be with:

It's a different thing.

We are using colons (:), not equals (=).

And adding type hints normally doesn't change what happens from what would happen without them.

But now, imagine you are again in the middle of creating that function, but with type hints.

At the same point, you try to trigger the autocomplete with Ctrl+Space and you see:

With that, you can scroll, seeing the options, until you find the one that "rings a bell":

Check this function, it already has type hints:

Because the editor knows the types of the variables, you don't only get completion, you also get error checks:

Now you know that you have to fix it, convert age to a string with str(age):

You just saw the main place to declare type hints. As function parameters.

This is also the main place you would use them with FastAPI.

You can declare all the standard Python types, not only str.

You can use, for example:

There are some data structures that can contain other values, like dict, list, set and tuple. And the internal values can have their own type too.

These types that have internal types are called "generic" types. And it's possible to declare them, even with their internal types.

To declare those types and the internal types, you can use the standard Python module typing. It exists specifically to support these type hints.

The syntax using typing is compatible with all versions, from Python 3.6 to the latest ones, including Python 3.9, Python 3.10, etc.

As Python advances, newer versions come with improved support for these type annotations and in many cases you won't even need to import and use the typing module to declare the type annotations.

If you can choose a more recent version of Python for your project, you will be able to take advantage of that extra simplicity.

In all the docs there are examples compatible with each version of Python (when there's a difference).

For example "Python 3.6+" means it's compatible with Python 3.6 or above (including 3.7, 3.8, 3.9, 3.10, etc). And "Python 3.9+" means it's compatible with Python 3.9 or above (including 3.10, etc).

If you can use the latest versions of Python, use the examples for the latest version, those will have the best and simplest syntax, for example, "Python 3.10+".

For example, let's define a variable to be a list of str.

Declare the variable, with the same colon (:) syntax.

As the type, put list.

As the list is a type that contains some internal types, you put them in square brackets:

Those internal types in the square brackets are called "type parameters".

In this case, str is the type parameter passed to list.

That means: "the variable items is a list, and each of the items in this list is a str".

By doing that, your editor can provide support even while processing items from the list:

Without types, that's almost impossible to achieve.

Notice that the variable item is one of the elements in the list items.

And still, the editor knows it is a str, and provides support for that.

You would do the same to declare tuples and sets:

To define a dict, you pass 2 type parameters, separated by commas.

The first type parameter is for the keys of the dict.

The second type parameter is for the values of the dict:

You can declare that a variable can be any of several types, for example, an int or a str.

In Python 3.6 and above (including Python 3.10) you can use the Union type from typing and put inside the square brackets the possible types to accept.

In Python 3.10 there's also a new syntax where you can put the possible types separated by a vertical bar (|).

In both cases this means that item could be an int or a str.

You can declare that a value could have a type, like str, but that it could also be None.

In Python 3.6 and above (including Python 3.10) you can declare it by importing and using Optional from the typing module.

Using Optional[str] instead of just str will let the editor help you detect errors where you could be assuming that a value is always a str, when it could actually be None too.

Optional[Something] is actually a shortcut for Union[Something, None], they are equivalent.

This also means that in Python 3.10, you can use Something | None:

If you are using a Python version below 3.10, here's a tip from my very subjective point of view:

Both are equivalent and underneath they are the same, but I would recommend Union instead of Optional because the word "optional" would seem to imply that the value is optional, and it actually means "it can be None", even if it's not optional and is still required.

I think Union[SomeType, None] is more explicit about what it means.

It's just about the words and names. But those words can affect how you and your teammates think about the code.

As an example, let's take this function:

The parameter name is defined as Optional[str], but it is not optional, you cannot call the function without the parameter:

The name parameter is still required (not optional) because it doesn't have a default value. Still, name accepts None as the value:

The good news is, once you are on Python 3.10 you won't have to worry about that, as you will be able to simply use | to define unions of types:

And then you won't have to worry about names like Optional and Union. 😎

These types that take type parameters in square brackets are called Generic types or Generics, for example:

You can use the same builtin types as generics (with square brackets and types inside):

And the same as with previous Python versions, from the typing module:

In Python 3.10, as an alternative to using the generics Union and Optional, you can use the vertical bar (|) to declare unions of types, that's a lot better and simpler.

You can use the same builtin types as generics (with square brackets and types inside):

And generics from the typing module:

You can also declare a class as the type of a variable.

Let's say you have a class Person, with a name:

Then you can declare a variable to be of type Person:

And then, again, you get all the editor support:

Notice that this means "one_person is an instance of the class Person".

It doesn't mean "one_person is the class called Person".

Pydantic is a Python library to perform data validation.

You declare the "shape" of the data as classes with attributes.

And each attribute has a type.

Then you create an instance of that class with some values and it will validate the values, convert them to the appropriate type (if that's the case) and give you an object with all the data.

And you get all the editor support with that resulting object.

An example from the official Pydantic docs:

To learn more about Pydantic, check its docs.

FastAPI is all based on Pydantic.

You will see a lot more of all this in practice in the Tutorial - User Guide.

Pydantic has a special behavior when you use Optional or Union[Something, None] without a default value, you can read more about it in the Pydantic docs about Required Optional fields.

Python also has a feature that allows putting additional metadata in these type hints using Annotated.

Since Python 3.9, Annotated is a part of the standard library, so you can import it from typing.

Python itself doesn't do anything with this Annotated. And for editors and other tools, the type is still str.

But you can use this space in Annotated to provide FastAPI with additional metadata about how you want your application to behave.

The important thing to remember is that the first type parameter you pass to Annotated is the actual type. The rest, is just metadata for other tools.

For now, you just need to know that Annotated exists, and that it's standard Python. 😎

Later you will see how powerful it can be.

The fact that this is standard Python means that you will still get the best possible developer experience in your editor, with the tools you use to analyze and refactor your code, etc. ✨

And also that your code will be very compatible with many other Python tools and libraries. 🚀

FastAPI takes advantage of these type hints to do several things.

With FastAPI you declare parameters with type hints and you get:

...and FastAPI uses the same declarations to:

This might all sound abstract. Don't worry. You'll see all this in action in the Tutorial - User Guide.

The important thing is that by using standard Python types, in a single place (instead of adding more classes, decorators, etc), FastAPI will do a lot of the work for you.

If you already went through all the tutorial and came back to see more about types, a good resource is the "cheat sheet" from mypy.

**Examples:**

Example 1 (python):
```python
def get_full_name(first_name, last_name):
    full_name = first_name.title() + " " + last_name.title()
    return full_name


print(get_full_name("john", "doe"))
```

Example 2 (python):
```python
def get_full_name(first_name, last_name):
    full_name = first_name.title() + " " + last_name.title()
    return full_name


print(get_full_name("john", "doe"))
```

Example 3 (unknown):
```unknown
first_name, last_name
```

Example 4 (yaml):
```yaml
first_name: str, last_name: str
```

---

## Virtual Environments¶

**URL:** https://fastapi.tiangolo.com/virtual-environments/

**Contents:**
- Virtual Environments¶
- Create a Project¶
- Create a Virtual Environment¶
- Activate the Virtual Environment¶
- Check the Virtual Environment is Active¶
- Upgrade pip¶
- Add .gitignore¶
- Install Packages¶
  - Install Packages Directly¶
  - Install from requirements.txt¶

When you work in Python projects you probably should use a virtual environment (or a similar mechanism) to isolate the packages you install for each project.

If you already know about virtual environments, how to create them and use them, you might want to skip this section. 🤓

A virtual environment is different than an environment variable.

An environment variable is a variable in the system that can be used by programs.

A virtual environment is a directory with some files in it.

This page will teach you how to use virtual environments and how they work.

If you are ready to adopt a tool that manages everything for you (including installing Python), try uv.

First, create a directory for your project.

What I normally do is that I create a directory named code inside my home/user directory.

And inside of that I create one directory per project.

When you start working on a Python project for the first time, create a virtual environment inside your project.

You only need to do this once per project, not every time you work.

To create a virtual environment, you can use the venv module that comes with Python.

If you have uv installed, you can use it to create a virtual environment.

By default, uv will create a virtual environment in a directory called .venv.

But you could customize it passing an additional argument with the directory name.

That command creates a new virtual environment in a directory called .venv.

You could create the virtual environment in a different directory, but there's a convention of calling it .venv.

Activate the new virtual environment so that any Python command you run or package you install uses it.

Do this every time you start a new terminal session to work on the project.

Or if you use Bash for Windows (e.g. Git Bash):

Every time you install a new package in that environment, activate the environment again.

This makes sure that if you use a terminal (CLI) program installed by that package, you use the one from your virtual environment and not any other that could be installed globally, probably with a different version than what you need.

Check that the virtual environment is active (the previous command worked).

This is optional, but it's a good way to check that everything is working as expected and you are using the virtual environment you intended.

If it shows the python binary at .venv/bin/python, inside of your project (in this case awesome-project), then it worked. 🎉

If it shows the python binary at .venv\Scripts\python, inside of your project (in this case awesome-project), then it worked. 🎉

If you use uv you would use it to install things instead of pip, so you don't need to upgrade pip. 😎

If you are using pip to install packages (it comes by default with Python), you should upgrade it to the latest version.

Many exotic errors while installing a package are solved by just upgrading pip first.

You would normally do this once, right after you create the virtual environment.

Make sure the virtual environment is active (with the command above) and then run:

Sometimes, you might get a No module named pip error when trying to upgrade pip.

If this happens, install and upgrade pip using the command below:

This command will install pip if it is not already installed and also ensures that the installed version of pip is at least as recent as the one available in ensurepip.

If you are using Git (you should), add a .gitignore file to exclude everything in your .venv from Git.

If you used uv to create the virtual environment, it already did this for you, you can skip this step. 😎

Do this once, right after you create the virtual environment.

And * for Git means "everything". So, it will ignore everything in the .venv directory.

That command will create a file .gitignore with the content:

After activating the environment, you can install packages in it.

Do this once when installing or upgrading the packages your project needs.

If you need to upgrade a version or add a new package you would do this again.

If you're in a hurry and don't want to use a file to declare your project's package requirements, you can install them directly.

It's a (very) good idea to put the packages and versions your program needs in a file (for example requirements.txt or pyproject.toml).

If you have a requirements.txt, you can now use it to install its packages.

A requirements.txt with some packages could look like:

After you activated the virtual environment, you can run your program, and it will use the Python inside of your virtual environment with the packages you installed there.

You would probably use an editor, make sure you configure it to use the same virtual environment you created (it will probably autodetect it) so that you can get autocompletion and inline errors.

You normally have to do this only once, when you create the virtual environment.

Once you are done working on your project you can deactivate the virtual environment.

This way, when you run python it won't try to run it from that virtual environment with the packages installed there.

Now you're ready to start working on your project.

Do you want to understand what's all that above?

To work with FastAPI you need to install Python.

After that, you would need to install FastAPI and any other packages you want to use.

To install packages you would normally use the pip command that comes with Python (or similar alternatives).

Nevertheless, if you just use pip directly, the packages would be installed in your global Python environment (the global installation of Python).

So, what's the problem with installing packages in the global Python environment?

At some point, you will probably end up writing many different programs that depend on different packages. And some of these projects you work on will depend on different versions of the same package. 😱

For example, you could create a project called philosophers-stone, this program depends on another package called harry, using the version 1. So, you need to install harry.

Then, at some point later, you create another project called prisoner-of-azkaban, and this project also depends on harry, but this project needs harry version 3.

But now the problem is, if you install the packages globally (in the global environment) instead of in a local virtual environment, you will have to choose which version of harry to install.

If you want to run philosophers-stone you will need to first install harry version 1, for example with:

And then you would end up with harry version 1 installed in your global Python environment.

But then if you want to run prisoner-of-azkaban, you will need to uninstall harry version 1 and install harry version 3 (or just installing version 3 would automatically uninstall version 1).

And then you would end up with harry version 3 installed in your global Python environment.

And if you try to run philosophers-stone again, there's a chance it would not work because it needs harry version 1.

It's very common in Python packages to try the best to avoid breaking changes in new versions, but it's better to be safe, and install newer versions intentionally and when you can run the tests to check everything is working correctly.

Now, imagine that with many other packages that all your projects depend on. That's very difficult to manage. And you would probably end up running some projects with some incompatible versions of the packages, and not knowing why something isn't working.

Also, depending on your operating system (e.g. Linux, Windows, macOS), it could have come with Python already installed. And in that case it probably had some packages pre-installed with some specific versions needed by your system. If you install packages in the global Python environment, you could end up breaking some of the programs that came with your operating system.

When you install Python, it creates some directories with some files in your computer.

Some of these directories are the ones in charge of having all the packages you install.

That will download a compressed file with the FastAPI code, normally from PyPI.

It will also download files for other packages that FastAPI depends on.

Then it will extract all those files and put them in a directory in your computer.

By default, it will put those files downloaded and extracted in the directory that comes with your Python installation, that's the global environment.

The solution to the problems of having all the packages in the global environment is to use a virtual environment for each project you work on.

A virtual environment is a directory, very similar to the global one, where you can install the packages for a project.

This way, each project will have its own virtual environment (.venv directory) with its own packages.

When you activate a virtual environment, for example with:

Or if you use Bash for Windows (e.g. Git Bash):

That command will create or modify some environment variables that will be available for the next commands.

One of those variables is the PATH variable.

You can learn more about the PATH environment variable in the Environment Variables section.

Activating a virtual environment adds its path .venv/bin (on Linux and macOS) or .venv\Scripts (on Windows) to the PATH environment variable.

Let's say that before activating the environment, the PATH variable looked like this:

That means that the system would look for programs in:

That means that the system would look for programs in:

After activating the virtual environment, the PATH variable would look something like this:

That means that the system will now start looking first for programs in:

before looking in the other directories.

So, when you type python in the terminal, the system will find the Python program in

That means that the system will now start looking first for programs in:

before looking in the other directories.

So, when you type python in the terminal, the system will find the Python program in

An important detail is that it will put the virtual environment path at the beginning of the PATH variable. The system will find it before finding any other Python available. This way, when you run python, it will use the Python from the virtual environment instead of any other python (for example, a python from a global environment).

Activating a virtual environment also changes a couple of other things, but this is one of the most important things it does.

When you check if a virtual environment is active, for example with:

That means that the python program that will be used is the one in the virtual environment.

You use which in Linux and macOS and Get-Command in Windows PowerShell.

The way that command works is that it will go and check in the PATH environment variable, going through each path in order, looking for the program called python. Once it finds it, it will show you the path to that program.

The most important part is that when you call python, that is the exact "python" that will be executed.

So, you can confirm if you are in the correct virtual environment.

It's easy to activate one virtual environment, get one Python, and then go to another project.

And the second project wouldn't work because you are using the incorrect Python, from a virtual environment for another project.

It's useful being able to check what python is being used. 🤓

For example, you could be working on a project philosophers-stone, activate that virtual environment, install packages and work with that environment.

And then you want to work on another project prisoner-of-azkaban.

You go to that project:

If you don't deactivate the virtual environment for philosophers-stone, when you run python in the terminal, it will try to use the Python from philosophers-stone.

But if you deactivate the virtual environment and activate the new one for prisoner-of-askaban then when you run python it will use the Python from the virtual environment in prisoner-of-azkaban.

This is a simple guide to get you started and teach you how everything works underneath.

There are many alternatives to managing virtual environments, package dependencies (requirements), projects.

Once you are ready and want to use a tool to manage the entire project, packages dependencies, virtual environments, etc. I would suggest you try uv.

uv can do a lot of things, it can:

If you read and understood all this, now you know much more about virtual environments than many developers out there. 🤓

Knowing these details will most probably be useful in a future time when you are debugging something that seems complex, but you will know how it all works underneath. 😎

**Examples:**

Example 1 (unknown):
```unknown
fastapi[standard]==0.113.0
pydantic==2.8.0
```

Example 2 (unknown):
```unknown
/usr/bin:/bin:/usr/sbin:/sbin
```

Example 3 (yaml):
```yaml
C:\Windows\System32
```

Example 4 (unknown):
```unknown
/home/user/code/awesome-project/.venv/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

---
