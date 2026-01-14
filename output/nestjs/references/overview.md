# Nestjs - Overview

**Pages:** 30

---

## 

**URL:** https://docs.nestjs.com/providers

**Contents:**
  - Providers
    - Services#
    - Dependency injection#
    - Scopes#
- Learn the right way!
    - Custom providers#
    - Optional providers#
    - Property-based injection#
    - Provider registration#
    - Manual instantiation#

Providers are a core concept in Nest. Many of the basic Nest classes, such as services, repositories, factories, and helpers, can be treated as providers. The key idea behind a provider is that it can be injected as a dependency, allowing objects to form various relationships with each other. The responsibility of "wiring up" these objects is largely handled by the Nest runtime system.

In the previous chapter, we created a simple CatsController. Controllers should handle HTTP requests and delegate more complex tasks to providers. Providers are plain JavaScript classes declared as providers in a NestJS module. For more details, refer to the "Modules" chapter.

Let's begin by creating a simple CatsService. This service will handle data storage and retrieval, and it will be used by the CatsController. Because of its role in managing the application's logic, it’s an ideal candidate to be defined as a provider.

Our CatsService is a basic class with one property and two methods. The key addition here is the @Injectable() decorator. This decorator attaches metadata to the class, signaling that CatsService is a class that can be managed by the Nest IoC container.

Additionally, this example makes use of a Cat interface, which likely looks something like this:

Now that we have a service class to retrieve cats, let's use it inside the CatsController:

The CatsService is injected through the class constructor. Notice the use of the private keyword. This shorthand allows us to both declare and initialize the catsService member in the same line, streamlining the process.

Nest is built around the powerful design pattern known as Dependency Injection. We highly recommend reading a great article about this concept in the official Angular documentation.

In Nest, thanks to TypeScript's capabilities, managing dependencies is straightforward because they are resolved based on their type. In the example below, Nest will resolve the catsService by creating and returning an instance of CatsService (or, in the case of a singleton, returning the existing instance if it has already been requested elsewhere). This dependency is then injected into your controller's constructor (or assigned to the specified property):

Providers typically have a lifetime ("scope") that aligns with the application lifecycle. When the application is bootstrapped, each dependency must be resolved, meaning every provider gets instantiated. Similarly, when the application shuts down, all providers are destroyed. However, it’s also possible to make a provider request-scoped, meaning its lifetime is tied to a specific request rather than the application's lifecycle. You can learn more about these techniques in the Injection Scopes chapter.

Learn the right way! 80+ chapters 5+ hours of videos Official certificate Deep-dive sessions Explore official courses

Nest comes with a built-in inversion of control ("IoC") container that manages the relationships between providers. This feature is the foundation of dependency injection, but it’s actually much more powerful than we've covered so far. There are several ways to define a provider: you can use plain values, classes, and both asynchronous or synchronous factories. For more examples of defining providers, check out the Dependency Injection chapter.

Occasionally, you may have dependencies that don't always need to be resolved. For example, your class might depend on a configuration object, but if none is provided, default values should be used. In such cases, the dependency is considered optional, and the absence of the configuration provider should not result in an error.

To mark a provider as optional, use the @Optional() decorator in the constructor's signature.

In the example above, we're using a custom provider, which is why we include the HTTP_OPTIONS custom token. Previous examples demonstrated constructor-based injection, where a dependency is indicated through a class in the constructor. For more details on custom providers and how their associated tokens work, check out the Custom Providers chapter.

The technique we've used so far is called constructor-based injection, where providers are injected through the constructor method. In certain specific cases, property-based injection can be useful. For example, if your top-level class depends on one or more providers, passing them all the way up through super() in sub-classes can become cumbersome. To avoid this, you can use the @Inject() decorator directly at the property level.

Now that we've defined a provider (CatsService) and a consumer (CatsController), we need to register the service with Nest so that it can handle the injection. This is done by editing the module file (app.module.ts) and adding the service to the providers array in the @Module() decorator.

Nest will now be able to resolve the dependencies of the CatsController class.

At this point, our directory structure should look like this:

So far, we've covered how Nest automatically handles most of the details of resolving dependencies. However, in some cases, you might need to step outside of the built-in Dependency Injection system and manually retrieve or instantiate providers. Two such techniques are briefly discussed below.

**Examples:**

Example 1 (typescript):
```typescript
import { Injectable } from '@nestjs/common';
import { Cat } from './interfaces/cat.interface';

@Injectable()
export class CatsService {
  private readonly cats: Cat[] = [];

  create(cat: Cat) {
    this.cats.push(cat);
  }

  findAll(): Cat[] {
    return this.cats;
  }
}
```

Example 2 (typescript):
```typescript
import { Injectable } from '@nestjs/common';

@Injectable()
export class CatsService {
  constructor() {
    this.cats = [];
  }

  create(cat) {
    this.cats.push(cat);
  }

  findAll() {
    return this.cats;
  }
}
```

Example 3 (typescript):
```typescript
export interface Cat {
  name: string;
  age: number;
  breed: string;
}
```

Example 4 (typescript):
```typescript
import { Controller, Get, Post, Body } from '@nestjs/common';
import { CreateCatDto } from './dto/create-cat.dto';
import { CatsService } from './cats.service';
import { Cat } from './interfaces/cat.interface';

@Controller('cats')
export class CatsController {
  constructor(private catsService: CatsService) {}

  @Post()
  async create(@Body() createCatDto: CreateCatDto) {
    this.catsService.create(createCatDto);
  }

  @Get()
  async findAll(): Promise<Cat[]> {
    return this.catsService.findAll();
  }
}
```

---

## 

**URL:** https://docs.nestjs.com/custom-decorators

**Contents:**
  - Custom route decorators
    - Param decorators#
    - Passing data#
    - Working with pipes#
    - Decorator composition#

Nest is built around a language feature called decorators. Decorators are a well-known concept in a lot of commonly used programming languages, but in the JavaScript world, they're still relatively new. In order to better understand how decorators work, we recommend reading this article. Here's a simple definition:

Nest provides a set of useful param decorators that you can use together with the HTTP route handlers. Below is a list of the provided decorators and the plain Express (or Fastify) objects they represent

Additionally, you can create your own custom decorators. Why is this useful?

In the node.js world, it's common practice to attach properties to the request object. Then you manually extract them in each route handler, using code like the following:

In order to make your code more readable and transparent, you can create a @User() decorator and reuse it across all of your controllers.

Then, you can simply use it wherever it fits your requirements.

When the behavior of your decorator depends on some conditions, you can use the data parameter to pass an argument to the decorator's factory function. One use case for this is a custom decorator that extracts properties from the request object by key. Let's assume, for example, that our authentication layer validates requests and attaches a user entity to the request object. The user entity for an authenticated request might look like:

Let's define a decorator that takes a property name as key, and returns the associated value if it exists (or undefined if it doesn't exist, or if the user object has not been created).

Here's how you could then access a particular property via the @User() decorator in the controller:

You can use this same decorator with different keys to access different properties. If the user object is deep or complex, this can make for easier and more readable request handler implementations.

Nest treats custom param decorators in the same fashion as the built-in ones (@Body(), @Param() and @Query()). This means that pipes are executed for the custom annotated parameters as well (in our examples, the user argument). Moreover, you can apply the pipe directly to the custom decorator:

Nest provides a helper method to compose multiple decorators. For example, suppose you want to combine all decorators related to authentication into a single decorator. This could be done with the following construction:

You can then use this custom @Auth() decorator as follows:

This has the effect of applying all four decorators with a single declaration.

**Examples:**

Example 1 (typescript):
```typescript
const user = req.user;
```

Example 2 (typescript):
```typescript
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export const User = createParamDecorator(
  (data: unknown, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    return request.user;
  },
);
```

Example 3 (typescript):
```typescript
@Get()
async findOne(@User() user: UserEntity) {
  console.log(user);
}
```

Example 4 (typescript):
```typescript
@Get()
@Bind(User())
async findOne(user) {
  console.log(user);
}
```

---

## 

**URL:** https://docs.nestjs.com/graphql/field-middleware

**Contents:**
  - Field middleware
    - Getting started#
    - Global field middleware#

Field Middleware lets you run arbitrary code before or after a field is resolved. A field middleware can be used to convert the result of a field, validate the arguments of a field, or even check field-level roles (for example, required to access a target field for which a middleware function is executed).

You can connect multiple middleware functions to a field. In this case, they will be called sequentially along the chain where the previous middleware decides to call the next one. The order of the middleware functions in the middleware array is important. The first resolver is the "most-outer" layer, so it gets executed first and last (similarly to the graphql-middleware package). The second resolver is the "second-outer" layer, so it gets executed second and second to last.

Let's start off by creating a simple middleware that will log a field value before it's sent back to the client:

Note that field middleware must match the FieldMiddleware interface. In the example above, we first run the next() function (which executes the actual field resolver and returns a field value) and then, we log this value to our terminal. Also, the value returned from the middleware function completely overrides the previous value and since we don't want to perform any changes, we simply return the original value.

With this in place, we can register our middleware directly in the @Field() decorator, as follows:

Now whenever we request the title field of Recipe object type, the original field's value will be logged to the console.

Also, as mentioned above, we can control the field's value from within the middleware function. For demonstration purposes, let's capitalise a recipe's title (if present):

In this case, every title will be automatically uppercased, when requested.

Likewise, you can bind a field middleware to a custom field resolver (a method annotated with the @ResolveField() decorator), as follows:

In addition to binding a middleware directly to a specific field, you can also register one or multiple middleware functions globally. In this case, they will be automatically connected to all fields of your object types.

**Examples:**

Example 1 (typescript):
```typescript
import { FieldMiddleware, MiddlewareContext, NextFn } from '@nestjs/graphql';

const loggerMiddleware: FieldMiddleware = async (
  ctx: MiddlewareContext,
  next: NextFn,
) => {
  const value = await next();
  console.log(value);
  return value;
};
```

Example 2 (typescript):
```typescript
@ObjectType()
export class Recipe {
  @Field({ middleware: [loggerMiddleware] })
  title: string;
}
```

Example 3 (typescript):
```typescript
const value = await next();
return value?.toUpperCase();
```

Example 4 (typescript):
```typescript
@ResolveField(() => String, { middleware: [loggerMiddleware] })
title() {
  return 'Placeholder';
}
```

---

## 

**URL:** https://docs.nestjs.com/microservices/exception-filters

**Contents:**
  - Exception filters
    - Filters#
    - Inheritance#

The only difference between the HTTP exception filter layer and the corresponding microservices layer is that instead of throwing HttpException, you should use RpcException.

With the sample above, Nest will handle the thrown exception and return the error object with the following structure:

Microservice exception filters behave similarly to HTTP exception filters, with one small difference. The catch() method must return an Observable.

The following example uses a manually instantiated method-scoped filter. Just as with HTTP based applications, you can also use controller-scoped filters (i.e., prefix the controller class with a @UseFilters() decorator).

Typically, you'll create fully customized exception filters crafted to fulfill your application requirements. However, there might be use-cases when you would like to simply extend the core exception filter, and override the behavior based on certain factors.

In order to delegate exception processing to the base filter, you need to extend BaseExceptionFilter and call the inherited catch() method.

The above implementation is just a shell demonstrating the approach. Your implementation of the extended exception filter would include your tailored business logic (e.g., handling various conditions).

**Examples:**

Example 1 (typescript):
```typescript
throw new RpcException('Invalid credentials.');
```

Example 2 (json):
```json
{
  "status": "error",
  "message": "Invalid credentials."
}
```

Example 3 (typescript):
```typescript
import { Catch, RpcExceptionFilter, ArgumentsHost } from '@nestjs/common';
import { Observable, throwError } from 'rxjs';
import { RpcException } from '@nestjs/microservices';

@Catch(RpcException)
export class ExceptionFilter implements RpcExceptionFilter<RpcException> {
  catch(exception: RpcException, host: ArgumentsHost): Observable<any> {
    return throwError(() => exception.getError());
  }
}
```

Example 4 (typescript):
```typescript
import { Catch } from '@nestjs/common';
import { throwError } from 'rxjs';

@Catch(RpcException)
export class ExceptionFilter {
  catch(exception, host) {
    return throwError(() => exception.getError());
  }
}
```

---

## 

**URL:** https://docs.nestjs.com/microservices/pipes

**Contents:**
  - Pipes
    - Binding pipes#

There is no fundamental difference between regular pipes and microservices pipes. The only difference is that instead of throwing HttpException, you should use RpcException.

The following example uses a manually instantiated method-scoped pipe. Just as with HTTP based applications, you can also use controller-scoped pipes (i.e., prefix the controller class with a @UsePipes() decorator).

**Examples:**

Example 1 (typescript):
```typescript
@UsePipes(new ValidationPipe({ exceptionFactory: (errors) => new RpcException(errors) }))
@MessagePattern({ cmd: 'sum' })
accumulate(data: number[]): number {
  return (data || []).reduce((a, b) => a + b);
}
```

Example 2 (typescript):
```typescript
@UsePipes(new ValidationPipe({ exceptionFactory: (errors) => new RpcException(errors) }))
@MessagePattern({ cmd: 'sum' })
accumulate(data) {
  return (data || []).reduce((a, b) => a + b);
}
```

---

## 

**URL:** https://docs.nestjs.com/fundamentals/lifecycle-events

**Contents:**
  - Lifecycle Events
    - Lifecycle sequence#
    - Lifecycle events#
    - Usage#
    - Asynchronous initialization#
    - Application shutdown#

A Nest application, as well as every application element, has a lifecycle managed by Nest. Nest provides lifecycle hooks that give visibility into key lifecycle events, and the ability to act (run registered code on your modules, providers or controllers) when they occur.

The following diagram depicts the sequence of key application lifecycle events, from the time the application is bootstrapped until the node process exits. We can divide the overall lifecycle into three phases: initializing, running and terminating. Using this lifecycle, you can plan for appropriate initialization of modules and services, manage active connections, and gracefully shutdown your application when it receives a termination signal.

Lifecycle events happen during application bootstrapping and shutdown. Nest calls registered lifecycle hook methods on modules, providers and controllers at each of the following lifecycle events (shutdown hooks need to be enabled first, as described below). As shown in the diagram above, Nest also calls the appropriate underlying methods to begin listening for connections, and to stop listening for connections.

In the following table, onModuleInit and onApplicationBootstrap are only triggered if you explicitly call app.init() or app.listen().

In the following table, onModuleDestroy, beforeApplicationShutdown and onApplicationShutdown are only triggered if you explicitly call app.close() or if the process receives a special system signal (such as SIGTERM) and you have correctly called enableShutdownHooks at application bootstrap (see below Application shutdown part).

* For these events, if you're not calling app.close() explicitly, you must opt-in to make them work with system signals such as SIGTERM. See Application shutdown below.

Each lifecycle hook is represented by an interface. Interfaces are technically optional because they do not exist after TypeScript compilation. Nonetheless, it's good practice to use them in order to benefit from strong typing and editor tooling. To register a lifecycle hook, implement the appropriate interface. For example, to register a method to be called during module initialization on a particular class (e.g., Controller, Provider or Module), implement the OnModuleInit interface by supplying an onModuleInit() method, as shown below:

Both the OnModuleInit and OnApplicationBootstrap hooks allow you to defer the application initialization process (return a Promise or mark the method as async and await an asynchronous method completion in the method body).

The onModuleDestroy(), beforeApplicationShutdown() and onApplicationShutdown() hooks are called in the terminating phase (in response to an explicit call to app.close() or upon receipt of system signals such as SIGTERM if opted-in). This feature is often used with Kubernetes to manage containers' lifecycles, by Heroku for dynos or similar services.

Shutdown hook listeners consume system resources, so they are disabled by default. To use shutdown hooks, you must enable listeners by calling enableShutdownHooks():

When the application receives a termination signal it will call any registered onModuleDestroy(), beforeApplicationShutdown(), then onApplicationShutdown() methods (in the sequence described above) with the corresponding signal as the first parameter. If a registered function awaits an asynchronous call (returns a promise), Nest will not continue in the sequence until the promise is resolved or rejected.

**Examples:**

Example 1 (typescript):
```typescript
import { Injectable, OnModuleInit } from '@nestjs/common';

@Injectable()
export class UsersService implements OnModuleInit {
  onModuleInit() {
    console.log(`The module has been initialized.`);
  }
}
```

Example 2 (typescript):
```typescript
import { Injectable } from '@nestjs/common';

@Injectable()
export class UsersService {
  onModuleInit() {
    console.log(`The module has been initialized.`);
  }
}
```

Example 3 (typescript):
```typescript
async onModuleInit(): Promise<void> {
  await this.fetch();
}
```

Example 4 (typescript):
```typescript
async onModuleInit() {
  await this.fetch();
}
```

---

## 

**URL:** https://docs.nestjs.com/microservices/interceptors

**Contents:**
  - Interceptors

There is no difference between regular interceptors and microservices interceptors. The following example uses a manually instantiated method-scoped interceptor. Just as with HTTP based applications, you can also use controller-scoped interceptors (i.e., prefix the controller class with a @UseInterceptors() decorator).

**Examples:**

Example 1 (typescript):
```typescript
@UseInterceptors(new TransformInterceptor())
@MessagePattern({ cmd: 'sum' })
accumulate(data: number[]): number {
  return (data || []).reduce((a, b) => a + b);
}
```

Example 2 (typescript):
```typescript
@UseInterceptors(new TransformInterceptor())
@MessagePattern({ cmd: 'sum' })
accumulate(data) {
  return (data || []).reduce((a, b) => a + b);
}
```

---

## 

**URL:** https://docs.nestjs.com/microservices/basics

**Contents:**
  - Overview
    - Installation#
    - Getting started#
    - Message and Event Patterns#
    - Request-response#
    - Asynchronous responses#
    - Event-based#
- Official enterprise support
    - Additional request details#
    - Client (producer class)#

In addition to traditional (sometimes called monolithic) application architectures, Nest natively supports the microservice architectural style of development. Most of the concepts discussed elsewhere in this documentation, such as dependency injection, decorators, exception filters, pipes, guards and interceptors, apply equally to microservices. Wherever possible, Nest abstracts implementation details so that the same components can run across HTTP-based platforms, WebSockets, and Microservices. This section covers the aspects of Nest that are specific to microservices.

In Nest, a microservice is fundamentally an application that uses a different transport layer than HTTP.

Nest supports several built-in transport layer implementations, called transporters, which are responsible for transmitting messages between different microservice instances. Most transporters natively support both request-response and event-based message styles. Nest abstracts the implementation details of each transporter behind a canonical interface for both request-response and event-based messaging. This makes it easy to switch from one transport layer to another -- for example to leverage the specific reliability or performance features of a particular transport layer -- without impacting your application code.

To start building microservices, first install the required package:

To instantiate a microservice, use the createMicroservice() method of the NestFactory class:

The second argument of the createMicroservice() method is an options object. This object may consist of two members:

The options object is specific to the chosen transporter. The TCP transporter exposes the properties described below. For other transporters (e.g, Redis, MQTT, etc.), see the relevant chapter for a description of the available options.

Microservices recognize both messages and events by patterns. A pattern is a plain value, for example, a literal object or a string. Patterns are automatically serialized and sent over the network along with the data portion of a message. In this way, message senders and consumers can coordinate which requests are consumed by which handlers.

The request-response message style is useful when you need to exchange messages between various external services. This paradigm ensures that the service has actually received the message (without requiring you to manually implement an acknowledgment protocol). However, the request-response approach may not always be the best fit. For example, streaming transporters, such as Kafka or NATS streaming, which use log-based persistence, are optimized for addressing a different set of challenges, more aligned with the event messaging paradigm (see event-based messaging for more details).

To enable the request-response message type, Nest creates two logical channels: one for transferring data and another for waiting for incoming responses. For some underlying transports, like NATS, this dual-channel support is provided out-of-the-box. For others, Nest compensates by manually creating separate channels. While this is effective, it can introduce some overhead. Therefore, if you don’t require a request-response message style, you may want to consider using the event-based method.

To create a message handler based on the request-response paradigm, use the @MessagePattern() decorator, which is imported from the @nestjs/microservices package. This decorator should only be used within controller classes, as they serve as the entry points for your application. Using it in providers will have no effect, as they will be ignored by the Nest runtime.

In the above code, the accumulate()message handler listens for messages that match the { cmd: 'sum' } message pattern. The message handler takes a single argument, the data passed from the client. In this case, the data is an array of numbers that need to be accumulated.

Message handlers can respond either synchronously or asynchronously, meaning that async methods are supported.

A message handler can also return an Observable, in which case the result values will be emitted until the stream completes.

In the example above, the message handler will respond three times, once for each item in the array.

While the request-response method is perfect for exchanging messages between services, it is less suited for event-based messaging—when you simply want to publish events without waiting for a response. In such cases, the overhead of maintaining two channels for request-response is unnecessary.

For example, if you want to notify another service that a specific condition has occurred in this part of the system, the event-based message style is ideal.

To create an event handler, you can use the @EventPattern() decorator, which is imported from the @nestjs/microservices package.

The handleUserCreated()event handler listens for the 'user_created' event. The event handler takes a single argument, the data passed from the client (in this case, an event payload which has been sent over the network).

Official enterprise support Providing technical guidance Performing in-depth code reviews Mentoring team members Advising best practices Explore more

In more advanced scenarios, you might need to access additional details about the incoming request. For instance, when using NATS with wildcard subscriptions, you may want to retrieve the original subject that the producer sent the message to. Similarly, with Kafka, you may need to access the message headers. To achieve this, you can leverage built-in decorators as shown below:

A client Nest application can exchange messages or publish events to a Nest microservice using the ClientProxy class. This class provides several methods, such as send() (for request-response messaging) and emit() (for event-driven messaging), enabling communication with a remote microservice. You can obtain an instance of this class in the following ways:

One approach is to import the ClientsModule, which exposes the static register() method. This method takes an array of objects representing microservice transporters. Each object must include a name property, and optionally a transport property (defaulting to Transport.TCP), as well as an optional options property.

The name property acts as an injection token, which you can use to inject an instance of ClientProxy wherever needed. The value of this name property can be any arbitrary string or JavaScript symbol, as described here.

The options property is an object that includes the same properties we saw in the createMicroservice() method earlier.

Alternatively, you can use the registerAsync() method if you need to provide configuration or perform any other asynchronous processes during the setup.

Once the module has been imported, you can inject an instance of the ClientProxy configured with the specified options for the 'MATH_SERVICE' transporter using the @Inject() decorator.

At times, you may need to fetch the transporter configuration from another service (such as a ConfigService), rather than hard-coding it in your client application. To achieve this, you can register a custom provider using the ClientProxyFactory class. This class provides a static create() method that accepts a transporter options object and returns a customized ClientProxy instance.

Another option is to use the @Client() property decorator.

Using the @Client() decorator is not the preferred technique, as it is harder to test and harder to share a client instance.

The ClientProxy is lazy. It doesn't initiate a connection immediately. Instead, it will be established before the first microservice call, and then reused across each subsequent call. However, if you want to delay the application bootstrapping process until a connection is established, you can manually initiate a connection using the ClientProxy object's connect() method inside the OnApplicationBootstrap lifecycle hook.

If the connection cannot be created, the connect() method will reject with the corresponding error object.

The ClientProxy exposes a send() method. This method is intended to call the microservice and returns an Observable with its response. Thus, we can subscribe to the emitted values easily.

The send() method takes two arguments, pattern and payload. The pattern should match one defined in a @MessagePattern() decorator. The payload is a message that we want to transmit to the remote microservice. This method returns a cold Observable, which means that you have to explicitly subscribe to it before the message will be sent.

To send an event, use the ClientProxy object's emit() method. This method publishes an event to the message broker.

The emit() method takes two arguments: pattern and payload. The pattern should match one defined in an @EventPattern() decorator, while the payload represents the event data that you want to transmit to the remote microservice. This method returns a hot Observable (in contrast to the cold Observable returned by send()), meaning that regardless of whether you explicitly subscribe to the observable, the proxy will immediately attempt to deliver the event.

Explore your graph with NestJS Devtools Graph visualizer Routes navigator Interactive playground CI/CD integration Sign up

For those coming from different programming language backgrounds, it may be surprising to learn that in Nest, most things are shared across incoming requests. This includes a connection pool to the database, singleton services with global state, and more. Keep in mind that Node.js does not follow the request/response multi-threaded stateless model, where each request is processed by a separate thread. As a result, using singleton instances is safe for our applications.

However, there are edge cases where a request-based lifetime for the handler might be desirable. This could include scenarios like per-request caching in GraphQL applications, request tracking, or multi-tenancy. You can learn more about how to control scopes here.

Request-scoped handlers and providers can inject RequestContext using the @Inject() decorator in combination with the CONTEXT token:

This provides access to the RequestContext object, which has two properties:

The data property is the message payload sent by the message producer. The pattern property is the pattern used to identify an appropriate handler to handle the incoming message.

To get real-time updates on the connection and the state of the underlying driver instance, you can subscribe to the status stream. This stream provides status updates specific to the chosen driver. For instance, if you’re using the TCP transporter (the default), the status stream emits connected and disconnected events.

Similarly, you can subscribe to the server's status stream to receive notifications about the server's status.

In some cases, you might want to listen to internal events emitted by the microservice. For example, you could listen for the error event to trigger additional operations when an error occurs. To do this, use the on() method, as shown below:

Similarly, you can listen to the server's internal events:

For more advanced use cases, you may need to access the underlying driver instance. This can be useful for scenarios like manually closing the connection or using driver-specific methods. However, keep in mind that for most cases, you shouldn't need to access the driver directly.

To do so, you can use the unwrap() method, which returns the underlying driver instance. The generic type parameter should specify the type of driver instance you expect.

Here, Server is a type imported from the net module.

Similarly, you can access the server's underlying driver instance:

In distributed systems, microservices might sometimes be down or unavailable. To prevent indefinitely long waiting, you can use timeouts. A timeout is a highly useful pattern when communicating with other services. To apply timeouts to your microservice calls, you can use the RxJStimeout operator. If the microservice does not respond within the specified time, an exception is thrown, which you can catch and handle appropriately.

To implement this, you'll need to use the rxjs package. Simply use the timeout operator within the pipe:

After 5 seconds, if the microservice isn't responding, it will throw an error.

When communicating outside of a private network, it’s important to encrypt traffic to ensure security. In NestJS, this can be achieved with TLS over TCP using Node's built-in TLS module. Nest provides built-in support for TLS in its TCP transport, allowing us to encrypt communication between microservices or clients.

To enable TLS for a TCP server, you'll need both a private key and a certificate in PEM format. These are added to the server's options by setting the tlsOptions and specifying the key and cert files, as shown below:

For a client to communicate securely over TLS, we also define the tlsOptions object but this time with the CA certificate. This is the certificate of the authority that signed the server's certificate. This ensures that the client trusts the server's certificate and can establish a secure connection.

You can also pass an array of CAs if your setup involves multiple trusted authorities.

Once everything is set up, you can inject the ClientProxy as usual using the @Inject() decorator to use the client in your services. This ensures encrypted communication across your NestJS microservices, with Node's TLS module handling the encryption details.

For more information, refer to Node’s TLS documentation.

When a microservice needs to be configured using the ConfigService (from the @nestjs/config package), but the injection context is only available after the microservice instance is created, AsyncMicroserviceOptions offers a solution. This approach allows for dynamic configuration, ensuring smooth integration with the ConfigService.

**Examples:**

Example 1 (bash):
```bash
$ npm i --save @nestjs/microservices
```

Example 2 (typescript):
```typescript
import { NestFactory } from '@nestjs/core';
import { Transport, MicroserviceOptions } from '@nestjs/microservices';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.createMicroservice<MicroserviceOptions>(
    AppModule,
    {
      transport: Transport.TCP,
    },
  );
  await app.listen();
}
bootstrap();
```

Example 3 (typescript):
```typescript
import { NestFactory } from '@nestjs/core';
import { Transport } from '@nestjs/microservices';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.createMicroservice(AppModule, {
    transport: Transport.TCP,
  });
  await app.listen();
}
bootstrap();
```

Example 4 (typescript):
```typescript
import { Controller } from '@nestjs/common';
import { MessagePattern } from '@nestjs/microservices';

@Controller()
export class MathController {
  @MessagePattern({ cmd: 'sum' })
  accumulate(data: number[]): number {
    return (data || []).reduce((a, b) => a + b);
  }
}
```

---

## 

**URL:** https://docs.nestjs.com/websockets/exception-filters

**Contents:**
  - Exception filters
    - Filters#
    - Inheritance#

The only difference between the HTTP exception filter layer and the corresponding web sockets layer is that instead of throwing HttpException, you should use WsException.

With the sample above, Nest will handle the thrown exception and emit the exception message with the following structure:

Web sockets exception filters behave equivalently to HTTP exception filters. The following example uses a manually instantiated method-scoped filter. Just as with HTTP based applications, you can also use gateway-scoped filters (i.e., prefix the gateway class with a @UseFilters() decorator).

Typically, you'll create fully customized exception filters crafted to fulfill your application requirements. However, there might be use-cases when you would like to simply extend the core exception filter, and override the behavior based on certain factors.

In order to delegate exception processing to the base filter, you need to extend BaseWsExceptionFilter and call the inherited catch() method.

The above implementation is just a shell demonstrating the approach. Your implementation of the extended exception filter would include your tailored business logic (e.g., handling various conditions).

**Examples:**

Example 1 (typescript):
```typescript
throw new WsException('Invalid credentials.');
```

Example 2 (typescript):
```typescript
{
  status: 'error',
  message: 'Invalid credentials.'
}
```

Example 3 (typescript):
```typescript
@UseFilters(new WsExceptionFilter())
@SubscribeMessage('events')
onEvent(client, data: any): WsResponse<any> {
  const event = 'events';
  return { event, data };
}
```

Example 4 (typescript):
```typescript
import { Catch, ArgumentsHost } from '@nestjs/common';
import { BaseWsExceptionFilter } from '@nestjs/websockets';

@Catch()
export class AllExceptionsFilter extends BaseWsExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    super.catch(exception, host);
  }
}
```

---

## 

**URL:** https://docs.nestjs.com/pipes

**Contents:**
  - Pipes
    - Built-in pipes#
    - Binding pipes#
    - Custom pipes#
    - Schema based validation#
- Learn the right way!
    - Object schema validation#
    - Binding validation pipes#
    - Class validator#
    - Global scoped pipes#

A pipe is a class annotated with the @Injectable() decorator, which implements the PipeTransform interface.

Pipes have two typical use cases:

In both cases, pipes operate on the arguments being processed by a controller route handler. Nest interposes a pipe just before a method is invoked, and the pipe receives the arguments destined for the method and operates on them. Any transformation or validation operation takes place at that time, after which the route handler is invoked with any (potentially) transformed arguments.

Nest comes with a number of built-in pipes that you can use out-of-the-box. You can also build your own custom pipes. In this chapter, we'll introduce the built-in pipes and show how to bind them to route handlers. We'll then examine several custom-built pipes to show how you can build one from scratch.

Nest comes with several pipes available out-of-the-box:

They're exported from the @nestjs/common package.

Let's take a quick look at using ParseIntPipe. This is an example of the transformation use case, where the pipe ensures that a method handler parameter is converted to a JavaScript integer (or throws an exception if the conversion fails). Later in this chapter, we'll show a simple custom implementation for a ParseIntPipe. The example techniques below also apply to the other built-in transformation pipes (ParseBoolPipe, ParseFloatPipe, ParseEnumPipe, ParseArrayPipe, ParseDatePipe, and ParseUUIDPipe, which we'll refer to as the Parse* pipes in this chapter).

To use a pipe, we need to bind an instance of the pipe class to the appropriate context. In our ParseIntPipe example, we want to associate the pipe with a particular route handler method, and make sure it runs before the method is called. We do so with the following construct, which we'll refer to as binding the pipe at the method parameter level:

This ensures that one of the following two conditions is true: either the parameter we receive in the findOne() method is a number (as expected in our call to this.catsService.findOne()), or an exception is thrown before the route handler is called.

For example, assume the route is called like:

Nest will throw an exception like this:

The exception will prevent the body of the findOne() method from executing.

In the example above, we pass a class (ParseIntPipe), not an instance, leaving responsibility for instantiation to the framework and enabling dependency injection. As with pipes and guards, we can instead pass an in-place instance. Passing an in-place instance is useful if we want to customize the built-in pipe's behavior by passing options:

Binding the other transformation pipes (all of the Parse* pipes) works similarly. These pipes all work in the context of validating route parameters, query string parameters and request body values.

For example with a query string parameter:

Here's an example of using the ParseUUIDPipe to parse a string parameter and validate if it is a UUID.

Above we've seen examples of binding the various Parse* family of built-in pipes. Binding validation pipes is a little bit different; we'll discuss that in the following section.

As mentioned, you can build your own custom pipes. While Nest provides a robust built-in ParseIntPipe and ValidationPipe, let's build simple custom versions of each from scratch to see how custom pipes are constructed.

We start with a simple ValidationPipe. Initially, we'll have it simply take an input value and immediately return the same value, behaving like an identity function.

Every pipe must implement the transform() method to fulfill the PipeTransform interface contract. This method has two parameters:

The value parameter is the currently processed method argument (before it is received by the route handling method), and metadata is the currently processed method argument's metadata. The metadata object has these properties:

These properties describe the currently processed argument.

Let's make our validation pipe a little more useful. Take a closer look at the create() method of the CatsController, where we probably would like to ensure that the post body object is valid before attempting to run our service method.

Let's focus in on the createCatDto body parameter. Its type is CreateCatDto:

We want to ensure that any incoming request to the create method contains a valid body. So we have to validate the three members of the createCatDto object. We could do this inside the route handler method, but doing so is not ideal as it would break the single responsibility principle (SRP).

Another approach could be to create a validator class and delegate the task there. This has the disadvantage that we would have to remember to call this validator at the beginning of each method.

How about creating validation middleware? This could work, but unfortunately, it's not possible to create generic middleware which can be used across all contexts across the whole application. This is because middleware is unaware of the execution context, including the handler that will be called and any of its parameters.

This is, of course, exactly the use case for which pipes are designed. So let's go ahead and refine our validation pipe.

Learn the right way! 80+ chapters 5+ hours of videos Official certificate Deep-dive sessions Explore official courses

There are several approaches available for doing object validation in a clean, DRY way. One common approach is to use schema-based validation. Let's go ahead and try that approach.

The Zod library allows you to create schemas in a straightforward way, with a readable API. Let's build a validation pipe that makes use of Zod-based schemas.

Start by installing the required package:

In the code sample below, we create a simple class that takes a schema as a constructor argument. We then apply the schema.parse() method, which validates our incoming argument against the provided schema.

As noted earlier, a validation pipe either returns the value unchanged or throws an exception.

In the next section, you'll see how we supply the appropriate schema for a given controller method using the @UsePipes() decorator. Doing so makes our validation pipe reusable across contexts, just as we set out to do.

Earlier, we saw how to bind transformation pipes (like ParseIntPipe and the rest of the Parse* pipes).

Binding validation pipes is also very straightforward.

In this case, we want to bind the pipe at the method call level. In our current example, we need to do the following to use the ZodValidationPipe:

We do that using the @UsePipes() decorator as shown below:

Let's look at an alternate implementation for our validation technique.

Nest works well with the class-validator library. This powerful library allows you to use decorator-based validation. Decorator-based validation is extremely powerful, especially when combined with Nest's Pipe capabilities since we have access to the metatype of the processed property. Before we start, we need to install the required packages:

Once these are installed, we can add a few decorators to the CreateCatDto class. Here we see a significant advantage of this technique: the CreateCatDto class remains the single source of truth for our Post body object (rather than having to create a separate validation class).

Now we can create a ValidationPipe class that uses these annotations.

Let's go through this code. First, note that the transform() method is marked as async. This is possible because Nest supports both synchronous and asynchronous pipes. We make this method async because some of the class-validator validations can be async (utilize Promises).

Next note that we are using destructuring to extract the metatype field (extracting just this member from an ArgumentMetadata) into our metatype parameter. This is just shorthand for getting the full ArgumentMetadata and then having an additional statement to assign the metatype variable.

Next, note the helper function toValidate(). It's responsible for bypassing the validation step when the current argument being processed is a native JavaScript type (these can't have validation decorators attached, so there's no reason to run them through the validation step).

Next, we use the class-transformer function plainToInstance() to transform our plain JavaScript argument object into a typed object so that we can apply validation. The reason we must do this is that the incoming post body object, when deserialized from the network request, does not have any type information (this is the way the underlying platform, such as Express, works). Class-validator needs to use the validation decorators we defined for our DTO earlier, so we need to perform this transformation to treat the incoming body as an appropriately decorated object, not just a plain vanilla object.

Finally, as noted earlier, since this is a validation pipe it either returns the value unchanged, or throws an exception.

The last step is to bind the ValidationPipe. Pipes can be parameter-scoped, method-scoped, controller-scoped, or global-scoped. Earlier, with our Zod-based validation pipe, we saw an example of binding the pipe at the method level. In the example below, we'll bind the pipe instance to the route handler @Body() decorator so that our pipe is called to validate the post body.

Parameter-scoped pipes are useful when the validation logic concerns only one specified parameter.

Since the ValidationPipe was created to be as generic as possible, we can realize its full utility by setting it up as a global-scoped pipe so that it is applied to every route handler across the entire application.

Global pipes are used across the whole application, for every controller and every route handler.

Note that in terms of dependency injection, global pipes registered from outside of any module (with useGlobalPipes() as in the example above) cannot inject dependencies since the binding has been done outside the context of any module. In order to solve this issue, you can set up a global pipe directly from any module using the following construction:

As a reminder, you don't have to build a generic validation pipe on your own since the ValidationPipe is provided by Nest out-of-the-box. The built-in ValidationPipe offers more options than the sample we built in this chapter, which has been kept basic for the sake of illustrating the mechanics of a custom-built pipe. You can find full details, along with lots of examples here.

Validation isn't the only use case for custom pipes. At the beginning of this chapter, we mentioned that a pipe can also transform the input data to the desired format. This is possible because the value returned from the transform function completely overrides the previous value of the argument.

When is this useful? Consider that sometimes the data passed from the client needs to undergo some change - for example converting a string to an integer - before it can be properly handled by the route handler method. Furthermore, some required data fields may be missing, and we would like to apply default values. Transformation pipes can perform these functions by interposing a processing function between the client request and the request handler.

Here's a simple ParseIntPipe which is responsible for parsing a string into an integer value. (As noted above, Nest has a built-in ParseIntPipe that is more sophisticated; we include this as a simple example of a custom transformation pipe).

We can then bind this pipe to the selected param as shown below:

Another useful transformation case would be to select an existing user entity from the database using an id supplied in the request:

We leave the implementation of this pipe to the reader, but note that like all other transformation pipes, it receives an input value (an id) and returns an output value (a UserEntity object). This can make your code more declarative and DRY by abstracting boilerplate code out of your handler and into a common pipe.

Parse* pipes expect a parameter's value to be defined. They throw an exception upon receiving null or undefined values. To allow an endpoint to handle missing querystring parameter values, we have to provide a default value to be injected before the Parse* pipes operate on these values. The DefaultValuePipe serves that purpose. Simply instantiate a DefaultValuePipe in the @Query() decorator before the relevant Parse* pipe, as shown below:

**Examples:**

Example 1 (typescript):
```typescript
@Get(':id')
async findOne(@Param('id', ParseIntPipe) id: number) {
  return this.catsService.findOne(id);
}
```

Example 2 (bash):
```bash
GET localhost:3000/abc
```

Example 3 (json):
```json
{
  "statusCode": 400,
  "message": "Validation failed (numeric string is expected)",
  "error": "Bad Request"
}
```

Example 4 (typescript):
```typescript
@Get(':id')
async findOne(
  @Param('id', new ParseIntPipe({ errorHttpStatusCode: HttpStatus.NOT_ACCEPTABLE }))
  id: number,
) {
  return this.catsService.findOne(id);
}
```

---

## 

**URL:** https://docs.nestjs.com/fundamentals/custom-providers

**Contents:**
  - Custom providers
    - DI fundamentals#
- Learn the right way!
    - Standard providers#
    - Custom providers#
    - Value providers: useValue#
    - Non-class-based provider tokens#
    - Class providers: useClass#
    - Factory providers: useFactory#
    - Alias providers: useExisting#

In earlier chapters, we touched on various aspects of Dependency Injection (DI) and how it is used in Nest. One example of this is the constructor based dependency injection used to inject instances (often service providers) into classes. You won't be surprised to learn that Dependency Injection is built into the Nest core in a fundamental way. So far, we've only explored one main pattern. As your application grows more complex, you may need to take advantage of the full features of the DI system, so let's explore them in more detail.

Dependency injection is an inversion of control (IoC) technique wherein you delegate instantiation of dependencies to the IoC container (in our case, the NestJS runtime system), instead of doing it in your own code imperatively. Let's examine what's happening in this example from the Providers chapter.

First, we define a provider. The @Injectable() decorator marks the CatsService class as a provider.

Then we request that Nest inject the provider into our controller class:

Finally, we register the provider with the Nest IoC container:

What exactly is happening under the covers to make this work? There are three key steps in the process:

When the Nest IoC container instantiates a CatsController, it first looks for any dependencies*. When it finds the CatsService dependency, it performs a lookup on the CatsService token, which returns the CatsService class, per the registration step (#3 above). Assuming SINGLETON scope (the default behavior), Nest will then either create an instance of CatsService, cache it, and return it, or if one is already cached, return the existing instance.

*This explanation is a bit simplified to illustrate the point. One important area we glossed over is that the process of analyzing the code for dependencies is very sophisticated, and happens during application bootstrapping. One key feature is that dependency analysis (or "creating the dependency graph"), is transitive. In the above example, if the CatsService itself had dependencies, those too would be resolved. The dependency graph ensures that dependencies are resolved in the correct order - essentially "bottom up". This mechanism relieves the developer from having to manage such complex dependency graphs.

Learn the right way! 80+ chapters 5+ hours of videos Official certificate Deep-dive sessions Explore official courses

Let's take a closer look at the @Module() decorator. In app.module, we declare:

The providers property takes an array of providers. So far, we've supplied those providers via a list of class names. In fact, the syntax providers: [CatsService] is short-hand for the more complete syntax:

Now that we see this explicit construction, we can understand the registration process. Here, we are clearly associating the token CatsService with the class CatsService. The short-hand notation is merely a convenience to simplify the most common use-case, where the token is used to request an instance of a class by the same name.

What happens when your requirements go beyond those offered by Standard providers? Here are a few examples:

Nest allows you to define Custom providers to handle these cases. It provides several ways to define custom providers. Let's walk through them.

The useValue syntax is useful for injecting a constant value, putting an external library into the Nest container, or replacing a real implementation with a mock object. Let's say you'd like to force Nest to use a mock CatsService for testing purposes.

In this example, the CatsService token will resolve to the mockCatsService mock object. useValue requires a value - in this case a literal object that has the same interface as the CatsService class it is replacing. Because of TypeScript's structural typing, you can use any object that has a compatible interface, including a literal object or a class instance instantiated with new.

So far, we've used class names as our provider tokens (the value of the provide property in a provider listed in the providers array). This is matched by the standard pattern used with constructor based injection, where the token is also a class name. (Refer back to DI Fundamentals for a refresher on tokens if this concept isn't entirely clear). Sometimes, we may want the flexibility to use strings or symbols as the DI token. For example:

In this example, we are associating a string-valued token ('CONNECTION') with a pre-existing connection object we've imported from an external file.

We've previously seen how to inject a provider using the standard constructor based injection pattern. This pattern requires that the dependency be declared with a class name. The 'CONNECTION' custom provider uses a string-valued token. Let's see how to inject such a provider. To do so, we use the @Inject() decorator. This decorator takes a single argument - the token.

While we directly use the string 'CONNECTION' in the above examples for illustration purposes, for clean code organization, it's best practice to define tokens in a separate file, such as constants.ts. Treat them much as you would symbols or enums that are defined in their own file and imported where needed.

The useClass syntax allows you to dynamically determine a class that a token should resolve to. For example, suppose we have an abstract (or default) ConfigService class. Depending on the current environment, we want Nest to provide a different implementation of the configuration service. The following code implements such a strategy.

Let's look at a couple of details in this code sample. You'll notice that we define configServiceProvider with a literal object first, then pass it in the module decorator's providers property. This is just a bit of code organization, but is functionally equivalent to the examples we've used thus far in this chapter.

Also, we have used the ConfigService class name as our token. For any class that depends on ConfigService, Nest will inject an instance of the provided class (DevelopmentConfigService or ProductionConfigService) overriding any default implementation that may have been declared elsewhere (e.g., a ConfigService declared with an @Injectable() decorator).

The useFactory syntax allows for creating providers dynamically. The actual provider will be supplied by the value returned from a factory function. The factory function can be as simple or complex as needed. A simple factory may not depend on any other providers. A more complex factory can itself inject other providers it needs to compute its result. For the latter case, the factory provider syntax has a pair of related mechanisms:

The useExisting syntax allows you to create aliases for existing providers. This creates two ways to access the same provider. In the example below, the (string-based) token 'AliasedLoggerService' is an alias for the (class-based) token LoggerService. Assume we have two different dependencies, one for 'AliasedLoggerService' and one for LoggerService. If both dependencies are specified with SINGLETON scope, they'll both resolve to the same instance.

While providers often supply services, they are not limited to that usage. A provider can supply any value. For example, a provider may supply an array of configuration objects based on the current environment, as shown below:

Like any provider, a custom provider is scoped to its declaring module. To make it visible to other modules, it must be exported. To export a custom provider, we can either use its token or the full provider object.

The following example shows exporting using the token:

Alternatively, export with the full provider object:

**Examples:**

Example 1 (typescript):
```typescript
import { Injectable } from '@nestjs/common';
import { Cat } from './interfaces/cat.interface';

@Injectable()
export class CatsService {
  private readonly cats: Cat[] = [];

  findAll(): Cat[] {
    return this.cats;
  }
}
```

Example 2 (typescript):
```typescript
import { Injectable } from '@nestjs/common';

@Injectable()
export class CatsService {
  constructor() {
    this.cats = [];
  }

  findAll() {
    return this.cats;
  }
}
```

Example 3 (typescript):
```typescript
import { Controller, Get } from '@nestjs/common';
import { CatsService } from './cats.service';
import { Cat } from './interfaces/cat.interface';

@Controller('cats')
export class CatsController {
  constructor(private catsService: CatsService) {}

  @Get()
  async findAll(): Promise<Cat[]> {
    return this.catsService.findAll();
  }
}
```

Example 4 (typescript):
```typescript
import { Controller, Get, Bind, Dependencies } from '@nestjs/common';
import { CatsService } from './cats.service';

@Controller('cats')
@Dependencies(CatsService)
export class CatsController {
  constructor(catsService) {
    this.catsService = catsService;
  }

  @Get()
  async findAll() {
    return this.catsService.findAll();
  }
}
```

---

## 

**URL:** https://docs.nestjs.com/websockets/guards

**Contents:**
  - Guards
    - Binding guards#

There is no fundamental difference between web sockets guards and regular HTTP application guards. The only difference is that instead of throwing HttpException, you should use WsException.

The following example uses a method-scoped guard. Just as with HTTP based applications, you can also use gateway-scoped guards (i.e., prefix the gateway class with a @UseGuards() decorator).

**Examples:**

Example 1 (typescript):
```typescript
@UseGuards(AuthGuard)
@SubscribeMessage('events')
handleEvent(client: Client, data: unknown): WsResponse<unknown> {
  const event = 'events';
  return { event, data };
}
```

Example 2 (typescript):
```typescript
@UseGuards(AuthGuard)
@SubscribeMessage('events')
handleEvent(client, data) {
  const event = 'events';
  return { event, data };
}
```

---

## 

**URL:** https://docs.nestjs.com/recipes/repl

**Contents:**
  - Read-Eval-Print-Loop (REPL)
    - Usage#
    - Native functions#
    - Watch mode#

REPL is a simple interactive environment that takes single user inputs, executes them, and returns the result to the user. The REPL feature lets you inspect your dependency graph and call methods on your providers (and controllers) directly from your terminal.

To run your NestJS application in REPL mode, create a new repl.ts file (alongside the existing main.ts file) and add the following code inside:

Now in your terminal, start the REPL with the following command:

Once it's up and running, you should see the following message in your console:

And now you can start interacting with your dependencies graph. For instance, you can retrieve an AppService (we are using the starter project as an example here) and call the getHello() method:

You can execute any JavaScript code from within your terminal, for example, assign an instance of the AppController to a local variable, and use await to call an asynchronous method:

To display all public methods available on a given provider or controller, use the methods() function, as follows:

To print all registered modules as a list together with their controllers and providers, use debug().

You can find more information about the existing, predefined native methods in the section below.

The built-in NestJS REPL comes with a few native functions that are globally available when you start REPL. You can call help() to list them out.

If you don't recall what's the signature (ie: expected parameters and a return type) of a function, you can call <function_name>.help. For instance:

During development it is useful to run REPL in a watch mode to reflect all the code changes automatically:

This has one flaw, the REPL's command history is discarded after each reload which might be cumbersome. Fortunately, there is a very simple solution. Modify your bootstrap function like this:

Now the history is preserved between the runs/reloads.

**Examples:**

Example 1 (typescript):
```typescript
import { repl } from '@nestjs/core';
import { AppModule } from './src/app.module';

async function bootstrap() {
  await repl(AppModule);
}
bootstrap();
```

Example 2 (typescript):
```typescript
import { repl } from '@nestjs/core';
import { AppModule } from './src/app.module';

async function bootstrap() {
  await repl(AppModule);
}
bootstrap();
```

Example 3 (bash):
```bash
$ npm run start -- --entryFile repl
```

Example 4 (bash):
```bash
LOG [NestFactory] Starting Nest application...
LOG [InstanceLoader] AppModule dependencies initialized
LOG REPL initialized
```

---

## 

**URL:** https://docs.nestjs.com/websockets/gateways

**Contents:**
  - Gateways
    - Installation#
    - Overview#
    - Multiple responses#
    - Asynchronous responses#
    - Lifecycle hooks#
    - Server and Namespace#
- Official enterprise support
    - Example#

Most of the concepts discussed elsewhere in this documentation, such as dependency injection, decorators, exception filters, pipes, guards and interceptors, apply equally to gateways. Wherever possible, Nest abstracts implementation details so that the same components can run across HTTP-based platforms, WebSockets, and Microservices. This section covers the aspects of Nest that are specific to WebSockets.

In Nest, a gateway is simply a class annotated with @WebSocketGateway() decorator. Technically, gateways are platform-agnostic which makes them compatible with any WebSockets library once an adapter is created. There are two WS platforms supported out-of-the-box: socket.io and ws. You can choose the one that best suits your needs. Also, you can build your own adapter by following this guide.

To start building WebSockets-based applications, first install the required package:

In general, each gateway is listening on the same port as the HTTP server, unless your app is not a web application, or you have changed the port manually. This default behavior can be modified by passing an argument to the @WebSocketGateway(80) decorator where 80 is a chosen port number. You can also set a namespace used by the gateway using the following construction:

You can pass any supported option to the socket constructor with the second argument to the @WebSocketGateway() decorator, as shown below:

The gateway is now listening, but we have not yet subscribed to any incoming messages. Let's create a handler that will subscribe to the events messages and respond to the user with the exact same data.

Once the gateway is created, we can register it in our module.

You can also pass in a property key to the decorator to extract it from the incoming message body:

If you would prefer not to use decorators, the following code is functionally equivalent:

In the example above, the handleEvent() function takes two arguments. The first one is a platform-specific socket instance, while the second one is the data received from the client. This approach is not recommended though, because it requires mocking the socket instance in each unit test.

Once the events message is received, the handler sends an acknowledgment with the same data that was sent over the network. In addition, it's possible to emit messages using a library-specific approach, for example, by making use of client.emit() method. In order to access a connected socket instance, use @ConnectedSocket() decorator.

However, in this case, you won't be able to leverage interceptors. If you don't want to respond to the user, you can simply skip the return statement (or explicitly return a "falsy" value, e.g. undefined).

Now when a client emits the message as follows:

The handleEvent() method will be executed. In order to listen for messages emitted from within the above handler, the client has to attach a corresponding acknowledgment listener:

While returning a value from a message handler implicitly sends an acknowledgement, advanced scenarios often require direct control over the acknowledgement callback.

The @Ack() parameter decorator allows injecting the ack callback function directly into a message handler. Without using the decorator, this callback is passed as the third argument of the method.

The acknowledgment is dispatched only once. Furthermore, it is not supported by native WebSockets implementation. To solve this limitation, you may return an object which consists of two properties. The event which is a name of the emitted event and the data that has to be forwarded to the client.

In order to listen for the incoming response(s), the client has to apply another event listener.

Message handlers are able to respond either synchronously or asynchronously. Hence, async methods are supported. A message handler is also able to return an Observable, in which case the result values will be emitted until the stream is completed.

In the example above, the message handler will respond 3 times (with each item from the array).

There are 3 useful lifecycle hooks available. All of them have corresponding interfaces and are described in the following table:

Occasionally, you may want to have a direct access to the native, platform-specific server instance. The reference to this object is passed as an argument to the afterInit() method (OnGatewayInit interface). Another option is to use the @WebSocketServer() decorator.

Also, you can retrieve the corresponding namespace using the namespace attribute, as follows:

@WebSocketServer() decorator injects a server instance by referencing the metadata stored by the @WebSocketGateway() decorator. If you provide the namespace option to the @WebSocketGateway() decorator, @WebSocketServer() decorator returns a Namespace instance instead of a Server instance.

Nest will automatically assign the server instance to this property once it is ready to use.

Official enterprise support Providing technical guidance Performing in-depth code reviews Mentoring team members Advising best practices Explore more

A working example is available here.

**Examples:**

Example 1 (typescript):
```typescript
$ npm i --save @nestjs/websockets @nestjs/platform-socket.io
```

Example 2 (typescript):
```typescript
$ npm i --save @nestjs/websockets @nestjs/platform-socket.io
```

Example 3 (typescript):
```typescript
@WebSocketGateway(80, { namespace: 'events' })
```

Example 4 (typescript):
```typescript
@WebSocketGateway(81, { transports: ['websocket'] })
```

---

## 

**URL:** https://docs.nestjs.com/fundamentals/circular-dependency

**Contents:**
  - Circular dependency
    - Forward reference#
    - ModuleRef class alternative#
    - Module forward reference#

A circular dependency occurs when two classes depend on each other. For example, class A needs class B, and class B also needs class A. Circular dependencies can arise in Nest between modules and between providers.

While circular dependencies should be avoided where possible, you can't always do so. In such cases, Nest enables resolving circular dependencies between providers in two ways. In this chapter, we describe using forward referencing as one technique, and using the ModuleRef class to retrieve a provider instance from the DI container as another.

We also describe resolving circular dependencies between modules.

A forward reference allows Nest to reference classes which aren't yet defined using the forwardRef() utility function. For example, if CatsService and CommonService depend on each other, both sides of the relationship can use @Inject() and the forwardRef() utility to resolve the circular dependency. Otherwise Nest won't instantiate them because all of the essential metadata won't be available. Here's an example:

That covers one side of the relationship. Now let's do the same with CommonService:

An alternative to using forwardRef() is to refactor your code and use the ModuleRef class to retrieve a provider on one side of the (otherwise) circular relationship. Learn more about the ModuleRef utility class here.

In order to resolve circular dependencies between modules, use the same forwardRef() utility function on both sides of the modules association. For example:

That covers one side of the relationship. Now let's do the same with CatsModule:

**Examples:**

Example 1 (typescript):
```typescript
@Injectable()
export class CatsService {
  constructor(
    @Inject(forwardRef(() => CommonService))
    private commonService: CommonService,
  ) {}
}
```

Example 2 (typescript):
```typescript
@Injectable()
@Dependencies(forwardRef(() => CommonService))
export class CatsService {
  constructor(commonService) {
    this.commonService = commonService;
  }
}
```

Example 3 (typescript):
```typescript
@Injectable()
export class CommonService {
  constructor(
    @Inject(forwardRef(() => CatsService))
    private catsService: CatsService,
  ) {}
}
```

Example 4 (typescript):
```typescript
@Injectable()
@Dependencies(forwardRef(() => CatsService))
export class CommonService {
  constructor(catsService) {
    this.catsService = catsService;
  }
}
```

---

## 

**URL:** https://docs.nestjs.com/fundamentals/dynamic-modules

**Contents:**
  - Dynamic modules
    - Introduction#
    - Dynamic module use case#
- Explore your graph with NestJS Devtools
    - Config module example#
    - Module configuration#
    - Example#
    - Community guidelines#
    - Configurable module builder#
    - Custom method key#

The Modules chapter covers the basics of Nest modules, and includes a brief introduction to dynamic modules. This chapter expands on the subject of dynamic modules. Upon completion, you should have a good grasp of what they are and how and when to use them.

Most application code examples in the Overview section of the documentation make use of regular, or static, modules. Modules define groups of components like providers and controllers that fit together as a modular part of an overall application. They provide an execution context, or scope, for these components. For example, providers defined in a module are visible to other members of the module without the need to export them. When a provider needs to be visible outside of a module, it is first exported from its host module, and then imported into its consuming module.

Let's walk through a familiar example.

First, we'll define a UsersModule to provide and export a UsersService. UsersModule is the host module for UsersService.

Next, we'll define an AuthModule, which imports UsersModule, making UsersModule's exported providers available inside AuthModule:

These constructs allow us to inject UsersService in, for example, the AuthService that is hosted in AuthModule:

We'll refer to this as static module binding. All the information Nest needs to wire together the modules has already been declared in the host and consuming modules. Let's unpack what's happening during this process. Nest makes UsersService available inside AuthModule by:

With static module binding, there's no opportunity for the consuming module to influence how providers from the host module are configured. Why does this matter? Consider the case where we have a general purpose module that needs to behave differently in different use cases. This is analogous to the concept of a "plugin" in many systems, where a generic facility requires some configuration before it can be used by a consumer.

A good example with Nest is a configuration module. Many applications find it useful to externalize configuration details by using a configuration module. This makes it easy to dynamically change the application settings in different deployments: e.g., a development database for developers, a staging database for the staging/testing environment, etc. By delegating the management of configuration parameters to a configuration module, the application source code remains independent of configuration parameters.

The challenge is that the configuration module itself, since it's generic (similar to a "plugin"), needs to be customized by its consuming module. This is where dynamic modules come into play. Using dynamic module features, we can make our configuration module dynamic so that the consuming module can use an API to control how the configuration module is customized at the time it is imported.

In other words, dynamic modules provide an API for importing one module into another, and customizing the properties and behavior of that module when it is imported, as opposed to using the static bindings we've seen so far.

Explore your graph with NestJS Devtools Graph visualizer Routes navigator Interactive playground CI/CD integration Sign up

We'll be using the basic version of the example code from the configuration chapter for this section. The completed version as of the end of this chapter is available as a working example here.

Our requirement is to make ConfigModule accept an options object to customize it. Here's the feature we want to support. The basic sample hard-codes the location of the .env file to be in the project root folder. Let's suppose we want to make that configurable, such that you can manage your .env files in any folder of your choosing. For example, imagine you want to store your various .env files in a folder under the project root called config (i.e., a sibling folder to src). You'd like to be able to choose different folders when using the ConfigModule in different projects.

Dynamic modules give us the ability to pass parameters into the module being imported so we can change its behavior. Let's see how this works. It's helpful if we start from the end-goal of how this might look from the consuming module's perspective, and then work backwards. First, let's quickly review the example of statically importing the ConfigModule (i.e., an approach which has no ability to influence the behavior of the imported module). Pay close attention to the imports array in the @Module() decorator:

Let's consider what a dynamic module import, where we're passing in a configuration object, might look like. Compare the difference in the imports array between these two examples:

Let's see what's happening in the dynamic example above. What are the moving parts?

In fact, what our register() method will return is a DynamicModule. A dynamic module is nothing more than a module created at run-time, with the same exact properties as a static module, plus one additional property called module. Let's quickly review a sample static module declaration, paying close attention to the module options passed in to the decorator:

Dynamic modules must return an object with the exact same interface, plus one additional property called module. The module property serves as the name of the module, and should be the same as the class name of the module, as shown in the example below.

What about the static register() method? We can now see that its job is to return an object that has the DynamicModule interface. When we call it, we are effectively providing a module to the imports list, similar to the way we would do so in the static case by listing a module class name. In other words, the dynamic module API simply returns a module, but rather than fix the properties in the @Module decorator, we specify them programmatically.

There are still a couple of details to cover to help make the picture complete:

Armed with this understanding, we can now look at what our dynamic ConfigModule declaration must look like. Let's take a crack at it.

It should now be clear how the pieces tie together. Calling ConfigModule.register(...) returns a DynamicModule object with properties which are essentially the same as those that, until now, we've provided as metadata via the @Module() decorator.

Our dynamic module isn't very interesting yet, however, as we haven't introduced any capability to configure it as we said we would like to do. Let's address that next.

The obvious solution for customizing the behavior of the ConfigModule is to pass it an options object in the static register() method, as we guessed above. Let's look once again at our consuming module's imports property:

That nicely handles passing an options object to our dynamic module. How do we then use that options object in the ConfigModule? Let's consider that for a minute. We know that our ConfigModule is basically a host for providing and exporting an injectable service - the ConfigService - for use by other providers. It's actually our ConfigService that needs to read the options object to customize its behavior. Let's assume for the moment that we know how to somehow get the options from the register() method into the ConfigService. With that assumption, we can make a few changes to the service to customize its behavior based on the properties from the options object. (Note: for the time being, since we haven't actually determined how to pass it in, we'll just hard-code options. We'll fix this in a minute).

Now our ConfigService knows how to find the .env file in the folder we've specified in options.

Our remaining task is to somehow inject the options object from the register() step into our ConfigService. And of course, we'll use dependency injection to do it. This is a key point, so make sure you understand it. Our ConfigModule is providing ConfigService. ConfigService in turn depends on the options object that is only supplied at run-time. So, at run-time, we'll need to first bind the options object to the Nest IoC container, and then have Nest inject it into our ConfigService. Remember from the Custom providers chapter that providers can include any value not just services, so we're fine using dependency injection to handle a simple options object.

Let's tackle binding the options object to the IoC container first. We do this in our static register() method. Remember that we are dynamically constructing a module, and one of the properties of a module is its list of providers. So what we need to do is define our options object as a provider. This will make it injectable into the ConfigService, which we'll take advantage of in the next step. In the code below, pay attention to the providers array:

Now we can complete the process by injecting the 'CONFIG_OPTIONS' provider into the ConfigService. Recall that when we define a provider using a non-class token we need to use the @Inject() decorator as described here.

One final note: for simplicity we used a string-based injection token ('CONFIG_OPTIONS') above, but best practice is to define it as a constant (or Symbol) in a separate file, and import that file. For example:

A full example of the code in this chapter can be found here.

You may have seen the use for methods like forRoot, register, and forFeature around some of the @nestjs/ packages and may be wondering what the difference for all of these methods are. There is no hard rule about this, but the @nestjs/ packages try to follow these guidelines:

When creating a module with:

register, you are expecting to configure a dynamic module with a specific configuration for use only by the calling module. For example, with Nest's @nestjs/axios: HttpModule.register({ baseUrl: 'someUrl' }). If, in another module you use HttpModule.register({ baseUrl: 'somewhere else' }), it will have the different configuration. You can do this for as many modules as you want.

forRoot, you are expecting to configure a dynamic module once and reuse that configuration in multiple places (though possibly unknowingly as it's abstracted away). This is why you have one GraphQLModule.forRoot(), one TypeOrmModule.forRoot(), etc.

forFeature, you are expecting to use the configuration of a dynamic module's forRoot but need to modify some configuration specific to the calling module's needs (i.e. which repository this module should have access to, or the context that a logger should use.)

All of these, usually, have their async counterparts as well, registerAsync, forRootAsync, and forFeatureAsync, that mean the same thing, but use Nest's Dependency Injection for the configuration as well.

As manually creating highly configurable, dynamic modules that expose async methods (registerAsync, forRootAsync, etc.) is quite complicated, especially for newcomers, Nest exposes the ConfigurableModuleBuilder class that facilitates this process and lets you construct a module "blueprint" in just a few lines of code.

For example, let's take the example we used above (ConfigModule) and convert it to use the ConfigurableModuleBuilder. Before we start, let's make sure we create a dedicated interface that represents what options our ConfigModule takes in.

With this in place, create a new dedicated file (alongside the existing config.module.ts file) and name it config.module-definition.ts. In this file, let's utilize the ConfigurableModuleBuilder to construct ConfigModule definition.

Now let's open up the config.module.ts file and modify its implementation to leverage the auto-generated ConfigurableModuleClass:

Extending the ConfigurableModuleClass means that ConfigModule provides now not only the register method (as previously with the custom implementation), but also the registerAsync method which allows consumers asynchronously configure that module, for example, by supplying async factories:

The registerAsync method takes the following object as an argument:

Let's go through the above properties one by one:

Always choose one of the above options (useFactory, useClass, or useExisting), as they are mutually exclusive.

Lastly, let's update the ConfigService class to inject the generated module options' provider instead of the 'CONFIG_OPTIONS' that we used so far.

ConfigurableModuleClass by default provides the register and its counterpart registerAsync methods. To use a different method name, use the ConfigurableModuleBuilder#setClassMethodName method, as follows:

This construction will instruct ConfigurableModuleBuilder to generate a class that exposes forRoot and forRootAsync instead. Example:

Since the registerAsync method (or forRootAsync or any other name, depending on the configuration) lets consumer pass a provider definition that resolves to the module configuration, a library consumer could potentially supply a class to be used to construct the configuration object.

This class, by default, must provide the create() method that returns a module configuration object. However, if your library follows a different naming convention, you can change that behavior and instruct ConfigurableModuleBuilder to expect a different method, for example, createConfigOptions, using the ConfigurableModuleBuilder#setFactoryMethodName method:

Now, ConfigModuleOptionsFactory class must expose the createConfigOptions method (instead of create):

There are edge-cases when your module may need to take extra options that determine how it is supposed to behave (a nice example of such an option is the isGlobal flag - or just global) that at the same time, shouldn't be included in the MODULE_OPTIONS_TOKEN provider (as they are irrelevant to services/providers registered within that module, for example, ConfigService does not need to know whether its host module is registered as a global module).

In such cases, the ConfigurableModuleBuilder#setExtras method can be used. See the following example:

In the example above, the first argument passed into the setExtras method is an object containing default values for the "extra" properties. The second argument is a function that takes an auto-generated module definitions (with provider, exports, etc.) and extras object which represents extra properties (either specified by the consumer or defaults). The returned value of this function is a modified module definition. In this specific example, we're taking the extras.isGlobal property and assigning it to the global property of the module definition (which in turn determines whether a module is global or not, read more here).

Now when consuming this module, the additional isGlobal flag can be passed in, as follows:

However, since isGlobal is declared as an "extra" property, it won't be available in the MODULE_OPTIONS_TOKEN provider:

The auto-generated static methods (register, registerAsync, etc.) can be extended if needed, as follows:

Note the use of OPTIONS_TYPE and ASYNC_OPTIONS_TYPE types that must be exported from the module definition file:

**Examples:**

Example 1 (typescript):
```typescript
import { Module } from '@nestjs/common';
import { UsersService } from './users.service';

@Module({
  providers: [UsersService],
  exports: [UsersService],
})
export class UsersModule {}
```

Example 2 (typescript):
```typescript
import { Module } from '@nestjs/common';
import { AuthService } from './auth.service';
import { UsersModule } from '../users/users.module';

@Module({
  imports: [UsersModule],
  providers: [AuthService],
  exports: [AuthService],
})
export class AuthModule {}
```

Example 3 (typescript):
```typescript
import { Injectable } from '@nestjs/common';
import { UsersService } from '../users/users.service';

@Injectable()
export class AuthService {
  constructor(private usersService: UsersService) {}
  /*
    Implementation that makes use of this.usersService
  */
}
```

Example 4 (typescript):
```typescript
import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ConfigModule } from './config/config.module';

@Module({
  imports: [ConfigModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
```

---

## 

**URL:** https://docs.nestjs.com/interceptors

**Contents:**
  - Interceptors
    - Basics#
    - Execution context#
    - Call handler#
- Explore your graph with NestJS Devtools
    - Aspect interception#
    - Binding interceptors#
    - Response mapping#
    - Exception mapping#
    - Stream overriding#

An interceptor is a class annotated with the @Injectable() decorator and implements the NestInterceptor interface.

Interceptors have a set of useful capabilities which are inspired by the Aspect Oriented Programming (AOP) technique. They make it possible to:

Each interceptor implements the intercept() method, which takes two arguments. The first one is the ExecutionContext instance (exactly the same object as for guards). The ExecutionContext inherits from ArgumentsHost. We saw ArgumentsHost before in the exception filters chapter. There, we saw that it's a wrapper around arguments that have been passed to the original handler, and contains different arguments arrays based on the type of the application. You can refer back to the exception filters for more on this topic.

By extending ArgumentsHost, ExecutionContext also adds several new helper methods that provide additional details about the current execution process. These details can be helpful in building more generic interceptors that can work across a broad set of controllers, methods, and execution contexts. Learn more about ExecutionContexthere.

The second argument is a CallHandler. The CallHandler interface implements the handle() method, which you can use to invoke the route handler method at some point in your interceptor. If you don't call the handle() method in your implementation of the intercept() method, the route handler method won't be executed at all.

This approach means that the intercept() method effectively wraps the request/response stream. As a result, you may implement custom logic both before and after the execution of the final route handler. It's clear that you can write code in your intercept() method that executes before calling handle(), but how do you affect what happens afterward? Because the handle() method returns an Observable, we can use powerful RxJS operators to further manipulate the response. Using Aspect Oriented Programming terminology, the invocation of the route handler (i.e., calling handle()) is called a Pointcut, indicating that it's the point at which our additional logic is inserted.

Consider, for example, an incoming POST /cats request. This request is destined for the create() handler defined inside the CatsController. If an interceptor which does not call the handle() method is called anywhere along the way, the create() method won't be executed. Once handle() is called (and its Observable has been returned), the create() handler will be triggered. And once the response stream is received via the Observable, additional operations can be performed on the stream, and a final result returned to the caller.

Explore your graph with NestJS Devtools Graph visualizer Routes navigator Interactive playground CI/CD integration Sign up

The first use case we'll look at is to use an interceptor to log user interaction (e.g., storing user calls, asynchronously dispatching events or calculating a timestamp). We show a simple LoggingInterceptor below:

Since handle() returns an RxJS Observable, we have a wide choice of operators we can use to manipulate the stream. In the example above, we used the tap() operator, which invokes our anonymous logging function upon graceful or exceptional termination of the observable stream, but doesn't otherwise interfere with the response cycle.

In order to set up the interceptor, we use the @UseInterceptors() decorator imported from the @nestjs/common package. Like pipes and guards, interceptors can be controller-scoped, method-scoped, or global-scoped.

Using the above construction, each route handler defined in CatsController will use LoggingInterceptor. When someone calls the GET /cats endpoint, you'll see the following output in your standard output:

Note that we passed the LoggingInterceptor class (instead of an instance), leaving responsibility for instantiation to the framework and enabling dependency injection. As with pipes, guards, and exception filters, we can also pass an in-place instance:

As mentioned, the construction above attaches the interceptor to every handler declared by this controller. If we want to restrict the interceptor's scope to a single method, we simply apply the decorator at the method level.

In order to set up a global interceptor, we use the useGlobalInterceptors() method of the Nest application instance:

Global interceptors are used across the whole application, for every controller and every route handler. In terms of dependency injection, global interceptors registered from outside of any module (with useGlobalInterceptors(), as in the example above) cannot inject dependencies since this is done outside the context of any module. In order to solve this issue, you can set up an interceptor directly from any module using the following construction:

We already know that handle() returns an Observable. The stream contains the value returned from the route handler, and thus we can easily mutate it using RxJS's map() operator.

Let's create the TransformInterceptor, which will modify each response in a trivial way to demonstrate the process. It will use RxJS's map() operator to assign the response object to the data property of a newly created object, returning the new object to the client.

With the above construction, when someone calls the GET /cats endpoint, the response would look like the following (assuming that route handler returns an empty array []):

Interceptors have great value in creating re-usable solutions to requirements that occur across an entire application. For example, imagine we need to transform each occurrence of a null value to an empty string ''. We can do it using one line of code and bind the interceptor globally so that it will automatically be used by each registered handler.

Another interesting use-case is to take advantage of RxJS's catchError() operator to override thrown exceptions:

There are several reasons why we may sometimes want to completely prevent calling the handler and return a different value instead. An obvious example is to implement a cache to improve response time. Let's take a look at a simple cache interceptor that returns its response from a cache. In a realistic example, we'd want to consider other factors like TTL, cache invalidation, cache size, etc., but that's beyond the scope of this discussion. Here we'll provide a basic example that demonstrates the main concept.

Our CacheInterceptor has a hardcoded isCached variable and a hardcoded response [] as well. The key point to note is that we return a new stream here, created by the RxJS of() operator, therefore the route handler won't be called at all. When someone calls an endpoint that makes use of CacheInterceptor, the response (a hardcoded, empty array) will be returned immediately. In order to create a generic solution, you can take advantage of Reflector and create a custom decorator. The Reflector is well described in the guards chapter.

The possibility of manipulating the stream using RxJS operators gives us many capabilities. Let's consider another common use case. Imagine you would like to handle timeouts on route requests. When your endpoint doesn't return anything after a period of time, you want to terminate with an error response. The following construction enables this:

After 5 seconds, request processing will be canceled. You can also add custom logic before throwing RequestTimeoutException (e.g. release resources).

**Examples:**

Example 1 (typescript):
```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    console.log('Before...');

    const now = Date.now();
    return next
      .handle()
      .pipe(
        tap(() => console.log(`After... ${Date.now() - now}ms`)),
      );
  }
}
```

Example 2 (typescript):
```typescript
import { Injectable } from '@nestjs/common';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable()
export class LoggingInterceptor {
  intercept(context, next) {
    console.log('Before...');

    const now = Date.now();
    return next
      .handle()
      .pipe(
        tap(() => console.log(`After... ${Date.now() - now}ms`)),
      );
  }
}
```

Example 3 (typescript):
```typescript
@UseInterceptors(LoggingInterceptor)
export class CatsController {}
```

Example 4 (typescript):
```typescript
Before...
After... 1ms
```

---

## 

**URL:** https://docs.nestjs.com/controllers

**Contents:**
  - Controllers
    - Routing#
- Explore your graph with NestJS Devtools
    - Request object#
    - Resources#
    - Route wildcards#
    - Status code#
    - Response headers#
    - Redirection#
    - Route parameters#

Controllers are responsible for handling incoming requests and sending responses back to the client.

A controller's purpose is to handle specific requests for the application. The routing mechanism determines which controller will handle each request. Often, a controller has multiple routes, and each route can perform a different action.

To create a basic controller, we use classes and decorators. Decorators link classes with the necessary metadata, allowing Nest to create a routing map that connects requests to their corresponding controllers.

In the following example, we’ll use the @Controller() decorator, which is required to define a basic controller. We'll specify an optional route path prefix of cats. Using a path prefix in the @Controller() decorator helps us group related routes together and reduces repetitive code. For example, if we want to group routes that manage interactions with a cat entity under the /cats path, we can specify the cats path prefix in the @Controller() decorator. This way, we don't need to repeat that portion of the path for each route in the file.

The @Get() HTTP request method decorator placed before the findAll() method tells Nest to create a handler for a specific endpoint for HTTP requests. This endpoint is defined by the HTTP request method (GET in this case) and the route path. So, what is the route path? The route path for a handler is determined by combining the (optional) prefix declared for the controller with any path specified in the method's decorator. Since we've set a prefix (cats) for every route and haven't added any specific path in the method decorator, Nest will map GET /cats requests to this handler.

As mentioned, the route path includes both the optional controller path prefix and any path string specified in the method's decorator. For example, if the controller prefix is cats and the method decorator is @Get('breed'), the resulting route will be GET /cats/breed.

In our example above, when a GET request is made to this endpoint, Nest routes the request to the user-defined findAll() method. Note that the method name we choose here is entirely arbitrary. While we must declare a method to bind the route to, Nest doesn’t attach any specific significance to the method name.

This method will return a 200 status code along with the associated response, which in this case is just a string. Why does this happen? To explain, we first need to introduce the concept that Nest uses two different options for manipulating responses:

Explore your graph with NestJS Devtools Graph visualizer Routes navigator Interactive playground CI/CD integration Sign up

Handlers often need access to the client’s request details. Nest provides access to the request object from the underlying platform (Express by default). You can access the request object by instructing Nest to inject it using the @Req() decorator in the handler’s signature.

The request object represents the HTTP request and contains properties for the query string, parameters, HTTP headers, and body (read more here). In most cases, you don't need to manually access these properties. Instead, you can use dedicated decorators like @Body() or @Query(), which are available out of the box. Below is a list of the provided decorators and the corresponding platform-specific objects they represent.

* For compatibility with typings across underlying HTTP platforms (e.g., Express and Fastify), Nest provides @Res() and @Response() decorators. @Res() is simply an alias for @Response(). Both directly expose the underlying native platform response object interface. When using them, you should also import the typings for the underlying library (e.g., @types/express) to take full advantage. Note that when you inject either @Res() or @Response() in a method handler, you put Nest into Library-specific mode for that handler, and you become responsible for managing the response. When doing so, you must issue some kind of response by making a call on the response object (e.g., res.json(...) or res.send(...)), or the HTTP server will hang.

Earlier, we defined an endpoint to fetch the cats resource (GET route). We'll typically also want to provide an endpoint that creates new records. For this, let's create the POST handler:

It's that simple. Nest provides decorators for all of the standard HTTP methods: @Get(), @Post(), @Put(), @Delete(), @Patch(), @Options(), and @Head(). In addition, @All() defines an endpoint that handles all of them.

Pattern-based routes are also supported in NestJS. For example, the asterisk (*) can be used as a wildcard to match any combination of characters in a route at the end of a path. In the following example, the findAll() method will be executed for any route that starts with abcd/, regardless of the number of characters that follow.

The 'abcd/*' route path will match abcd/, abcd/123, abcd/abc, and so on. The hyphen ( -) and the dot (.) are interpreted literally by string-based paths.

This approach works on both Express and Fastify. However, with the latest release of Express (v5), the routing system has become more strict. In pure Express, you must use a named wildcard to make the route work—for example, abcd/*splat, where splat is simply the name of the wildcard parameter and has no special meaning. You can name it anything you like. That said, since Nest provides a compatibility layer for Express, you can still use the asterisk (*) as a wildcard.

When it comes to asterisks used in the middle of a route, Express requires named wildcards (e.g., ab{*splat}cd), while Fastify does not support them at all.

As mentioned, the default status code for responses is always 200, except for POST requests, which default to 201. You can easily change this behavior by using the @HttpCode(...) decorator at the handler level.

Often, your status code isn't static but depends on various factors. In that case, you can use a library-specific response (inject using @Res()) object (or, in case of an error, throw an exception).

To specify a custom response header, you can either use a @Header() decorator or a library-specific response object (and call res.header() directly).

To redirect a response to a specific URL, you can either use a @Redirect() decorator or a library-specific response object (and call res.redirect() directly).

@Redirect() takes two arguments, url and statusCode, both are optional. The default value of statusCode is 302 (Found) if omitted.

Returned values will override any arguments passed to the @Redirect() decorator. For example:

Routes with static paths won’t work when you need to accept dynamic data as part of the request (e.g., GET /cats/1 to get the cat with id 1). To define routes with parameters, you can add route parameter tokens in the route path to capture the dynamic values from the URL. The route parameter token in the @Get() decorator example below illustrates this approach. These route parameters can then be accessed using the @Param() decorator, which should be added to the method signature.

The @Param() decorator is used to decorate a method parameter (in the example above, params), making the route parameters accessible as properties of that decorated method parameter inside the method. As shown in the code, you can access the id parameter by referencing params.id. Alternatively, you can pass a specific parameter token to the decorator and directly reference the route parameter by name within the method body.

The @Controller decorator can take a host option to require that the HTTP host of the incoming requests matches some specific value.

Similar to a route path, the host option can use tokens to capture the dynamic value at that position in the host name. The host parameter token in the @Controller() decorator example below demonstrates this usage. Host parameters declared in this way can be accessed using the @HostParam() decorator, which should be added to the method signature.

For developers coming from other programming languages, it might be surprising to learn that in Nest, nearly everything is shared across incoming requests. This includes resources like the database connection pool, singleton services with global state, and more. It's important to understand that Node.js doesn't use the request/response Multi-Threaded Stateless Model, where each request is handled by a separate thread. As a result, using singleton instances in Nest is completely safe for our applications.

That said, there are specific edge cases where having request-based lifetimes for controllers may be necessary. Examples include per-request caching in GraphQL applications, request tracking, or implementing multi-tenancy. You can learn more about controlling injection scopes here.

We love modern JavaScript, especially its emphasis on asynchronous data handling. That’s why Nest fully supports async functions. Every async function must return a Promise, which allows you to return a deferred value that Nest can resolve automatically. Here's an example:

This code is perfectly valid. But Nest takes it a step further by allowing route handlers to return RxJS observable streams as well. Nest will handle the subscription internally and resolve the final emitted value once the stream completes.

Both approaches are valid, and you can choose the one that best suits your needs.

In our previous example, the POST route handler didn’t accept any client parameters. Let's fix that by adding the @Body() decorator.

Before we proceed (if you're using TypeScript), we need to define the DTO (Data Transfer Object) schema. A DTO is an object that specifies how data should be sent over the network. We could define the DTO schema using TypeScript interfaces or simple classes. However, we recommend using classes here. Why? Classes are part of the JavaScript ES6 standard, so they remain intact as real entities in the compiled JavaScript. In contrast, TypeScript interfaces are removed during transpilation, meaning Nest can't reference them at runtime. This is important because features like Pipes rely on having access to the metatype of variables at runtime, which is only possible with classes.

Let's create the CreateCatDto class:

It has only three basic properties. Thereafter we can use the newly created DTO inside the CatsController:

When handling query parameters in your routes, you can use the @Query() decorator to extract them from incoming requests. Let's see how this works in practice.

Consider a route where we want to filter a list of cats based on query parameters like age and breed. First, define the query parameters in the CatsController:

In this example, the @Query() decorator is used to extract the values of age and breed from the query string. For example, a request to:

would result in age being 2 and breed being Persian.

If your application requires handling more complex query parameters, such as nested objects or arrays:

you'll need to configure your HTTP adapter (Express or Fastify) to use an appropriate query parser. In Express, you can use the extended parser, which allows for rich query objects:

In Fastify, you can use the querystringParser option:

There's a separate chapter about handling errors (i.e., working with exceptions) here.

Below is an example that demonstrates the use of several available decorators to create a basic controller. This controller provides a few methods to access and manipulate internal data.

Even with the CatsController fully defined, Nest doesn't yet know about it and won't automatically create an instance of the class.

Controllers must always be part of a module, which is why we include the controllers array within the @Module() decorator. Since we haven’t defined any other modules apart from the root AppModule, we’ll use it to register the CatsController:

We attached the metadata to the module class using the @Module() decorator, and now Nest can easily determine which controllers need to be mounted.

So far, we've covered the standard Nest way of manipulating responses. Another approach is to use a library-specific response object. To inject a specific response object, we can use the @Res() decorator. To highlight the differences, let’s rewrite the CatsController like this:

While this approach works and offers more flexibility by giving full control over the response object (such as header manipulation and access to library-specific features), it should be used with caution. Generally, this method is less clear and comes with some downsides. The main disadvantage is that your code becomes platform-dependent, as different underlying libraries may have different APIs for the response object. Additionally, it can make testing more challenging, as you'll need to mock the response object, among other things.

Furthermore, by using this approach, you lose compatibility with Nest features that rely on standard response handling, such as Interceptors and the @HttpCode() / @Header() decorators. To address this, you can enable the passthrough option like this:

With this approach, you can interact with the native response object (for example, setting cookies or headers based on specific conditions), while still allowing the framework to handle the rest.

**Examples:**

Example 1 (typescript):
```typescript
import { Controller, Get } from '@nestjs/common';

@Controller('cats')
export class CatsController {
  @Get()
  findAll(): string {
    return 'This action returns all cats';
  }
}
```

Example 2 (typescript):
```typescript
import { Controller, Get } from '@nestjs/common';

@Controller('cats')
export class CatsController {
  @Get()
  findAll() {
    return 'This action returns all cats';
  }
}
```

Example 3 (typescript):
```typescript
import { Controller, Get, Req } from '@nestjs/common';
import type { Request } from 'express';

@Controller('cats')
export class CatsController {
  @Get()
  findAll(@Req() request: Request): string {
    return 'This action returns all cats';
  }
}
```

Example 4 (typescript):
```typescript
import { Controller, Bind, Get, Req } from '@nestjs/common';

@Controller('cats')
export class CatsController {
  @Get()
  @Bind(Req())
  findAll(request) {
    return 'This action returns all cats';
  }
}
```

---

## 

**URL:** https://docs.nestjs.com/exception-filters

**Contents:**
  - Exception filters
    - Throwing standard exceptions#
    - Exceptions logging#
    - Custom exceptions#
    - Built-in HTTP exceptions#
    - Exception filters#
    - Arguments host#
- Learn the right way!
    - Binding filters#
    - Catch everything#

Nest comes with a built-in exceptions layer which is responsible for processing all unhandled exceptions across an application. When an exception is not handled by your application code, it is caught by this layer, which then automatically sends an appropriate user-friendly response.

Out of the box, this action is performed by a built-in global exception filter, which handles exceptions of type HttpException (and subclasses of it). When an exception is unrecognized (is neither HttpException nor a class that inherits from HttpException), the built-in exception filter generates the following default JSON response:

Nest provides a built-in HttpException class, exposed from the @nestjs/common package. For typical HTTP REST/GraphQL API based applications, it's best practice to send standard HTTP response objects when certain error conditions occur.

For example, in the CatsController, we have a findAll() method (a GET route handler). Let's assume that this route handler throws an exception for some reason. To demonstrate this, we'll hard-code it as follows:

When the client calls this endpoint, the response looks like this:

The HttpException constructor takes two required arguments which determine the response:

By default, the JSON response body contains two properties:

To override just the message portion of the JSON response body, supply a string in the response argument. To override the entire JSON response body, pass an object in the response argument. Nest will serialize the object and return it as the JSON response body.

The second constructor argument - status - should be a valid HTTP status code. Best practice is to use the HttpStatus enum imported from @nestjs/common.

There is a third constructor argument (optional) - options - that can be used to provide an error cause. This cause object is not serialized into the response object, but it can be useful for logging purposes, providing valuable information about the inner error that caused the HttpException to be thrown.

Here's an example overriding the entire response body and providing an error cause:

Using the above, this is how the response would look:

By default, the exception filter does not log built-in exceptions like HttpException (and any exceptions that inherit from it). When these exceptions are thrown, they won't appear in the console, as they are treated as part of the normal application flow. The same behavior applies to other built-in exceptions such as WsException and RpcException.

These exceptions all inherit from the base IntrinsicException class, which is exported from the @nestjs/common package. This class helps differentiate between exceptions that are part of normal application operation and those that are not.

If you want to log these exceptions, you can create a custom exception filter. We'll explain how to do this in the next section.

In many cases, you will not need to write custom exceptions, and can use the built-in Nest HTTP exception, as described in the next section. If you do need to create customized exceptions, it's good practice to create your own exceptions hierarchy, where your custom exceptions inherit from the base HttpException class. With this approach, Nest will recognize your exceptions, and automatically take care of the error responses. Let's implement such a custom exception:

Since ForbiddenException extends the base HttpException, it will work seamlessly with the built-in exception handler, and therefore we can use it inside the findAll() method.

Nest provides a set of standard exceptions that inherit from the base HttpException. These are exposed from the @nestjs/common package, and represent many of the most common HTTP exceptions:

All the built-in exceptions can also provide both an error cause and an error description using the options parameter:

Using the above, this is how the response would look:

While the base (built-in) exception filter can automatically handle many cases for you, you may want full control over the exceptions layer. For example, you may want to add logging or use a different JSON schema based on some dynamic factors. Exception filters are designed for exactly this purpose. They let you control the exact flow of control and the content of the response sent back to the client.

Let's create an exception filter that is responsible for catching exceptions which are an instance of the HttpException class, and implementing custom response logic for them. To do this, we'll need to access the underlying platform Request and Response objects. We'll access the Request object so we can pull out the original url and include that in the logging information. We'll use the Response object to take direct control of the response that is sent, using the response.json() method.

The @Catch(HttpException) decorator binds the required metadata to the exception filter, telling Nest that this particular filter is looking for exceptions of type HttpException and nothing else. The @Catch() decorator may take a single parameter, or a comma-separated list. This lets you set up the filter for several types of exceptions at once.

Let's look at the parameters of the catch() method. The exception parameter is the exception object currently being processed. The host parameter is an ArgumentsHost object. ArgumentsHost is a powerful utility object that we'll examine further in the execution context chapter*. In this code sample, we use it to obtain a reference to the Request and Response objects that are being passed to the original request handler (in the controller where the exception originates). In this code sample, we've used some helper methods on ArgumentsHost to get the desired Request and Response objects. Learn more about ArgumentsHosthere.

*The reason for this level of abstraction is that ArgumentsHost functions in all contexts (e.g., the HTTP server context we're working with now, but also Microservices and WebSockets). In the execution context chapter we'll see how we can access the appropriate underlying arguments for any execution context with the power of ArgumentsHost and its helper functions. This will allow us to write generic exception filters that operate across all contexts.

Learn the right way! 80+ chapters 5+ hours of videos Official certificate Deep-dive sessions Explore official courses

Let's tie our new HttpExceptionFilter to the CatsController's create() method.

We have used the @UseFilters() decorator here. Similar to the @Catch() decorator, it can take a single filter instance, or a comma-separated list of filter instances. Here, we created the instance of HttpExceptionFilter in place. Alternatively, you may pass the class (instead of an instance), leaving responsibility for instantiation to the framework, and enabling dependency injection.

In the example above, the HttpExceptionFilter is applied only to the single create() route handler, making it method-scoped. Exception filters can be scoped at different levels: method-scoped of the controller/resolver/gateway, controller-scoped, or global-scoped. For example, to set up a filter as controller-scoped, you would do the following:

This construction sets up the HttpExceptionFilter for every route handler defined inside the CatsController.

To create a global-scoped filter, you would do the following:

Global-scoped filters are used across the whole application, for every controller and every route handler. In terms of dependency injection, global filters registered from outside of any module (with useGlobalFilters() as in the example above) cannot inject dependencies since this is done outside the context of any module. In order to solve this issue, you can register a global-scoped filter directly from any module using the following construction:

You can add as many filters with this technique as needed; simply add each to the providers array.

In order to catch every unhandled exception (regardless of the exception type), leave the @Catch() decorator's parameter list empty, e.g., @Catch().

In the example below we have a code that is platform-agnostic because it uses the HTTP adapter to deliver the response, and doesn't use any of the platform-specific objects (Request and Response) directly:

Typically, you'll create fully customized exception filters crafted to fulfill your application requirements. However, there might be use-cases when you would like to simply extend the built-in default global exception filter, and override the behavior based on certain factors.

In order to delegate exception processing to the base filter, you need to extend BaseExceptionFilter and call the inherited catch() method.

Global filters can extend the base filter. This can be done in either of two ways.

The first method is to inject the HttpAdapter reference when instantiating the custom global filter:

The second method is to use the APP_FILTER token as shown here.

**Examples:**

Example 1 (json):
```json
{
  "statusCode": 500,
  "message": "Internal server error"
}
```

Example 2 (typescript):
```typescript
@Get()
async findAll() {
  throw new HttpException('Forbidden', HttpStatus.FORBIDDEN);
}
```

Example 3 (json):
```json
{
  "statusCode": 403,
  "message": "Forbidden"
}
```

Example 4 (typescript):
```typescript
@Get()
async findAll() {
  try {
    await this.service.findAll()
  } catch (error) {
    throw new HttpException({
      status: HttpStatus.FORBIDDEN,
      error: 'This is a custom message',
    }, HttpStatus.FORBIDDEN, {
      cause: error
    });
  }
}
```

---

## 

**URL:** https://docs.nestjs.com/fundamentals/lazy-loading-modules

**Contents:**
  - Lazy loading modules
    - Getting started#
    - Lazy loading controllers, gateways, and resolvers#
    - Common use-cases#

By default, modules are eagerly loaded, which means that as soon as the application loads, so do all the modules, whether or not they are immediately necessary. While this is fine for most applications, it may become a bottleneck for apps/workers running in the serverless environment, where the startup latency ("cold start") is crucial.

Lazy loading can help decrease bootstrap time by loading only modules required by the specific serverless function invocation. In addition, you could also load other modules asynchronously once the serverless function is "warm" to speed-up the bootstrap time for subsequent calls even further (deferred modules registration).

To load modules on-demand, Nest provides the LazyModuleLoader class that can be injected into a class in the normal way:

Alternatively, you can obtain a reference to the LazyModuleLoader provider from within your application bootstrap file (main.ts), as follows:

With this in place, you can now load any module using the following construction:

Also, "lazy loaded" modules share the same modules graph as those eagerly loaded on the application bootstrap as well as any other lazy modules registered later in your app.

Where lazy.module.ts is a TypeScript file that exports a regular Nest module (no extra changes are required).

The LazyModuleLoader#load method returns the module reference (of LazyModule) that lets you navigate the internal list of providers and obtain a reference to any provider using its injection token as a lookup key.

For example, let's say we have a LazyModule with the following definition:

With this, we could obtain a reference to the LazyService provider, as follows:

With these options set up, you'll be able to leverage the code splitting feature.

Since controllers (or resolvers in GraphQL applications) in Nest represent sets of routes/paths/topics (or queries/mutations), you cannot lazy load them using the LazyModuleLoader class.

For example, let's say you're building a REST API (HTTP application) with a Fastify driver under the hood (using the @nestjs/platform-fastify package). Fastify does not let you register routes after the application is ready/successfully listening to messages. That means even if we analyzed route mappings registered in the module's controllers, all lazy loaded routes wouldn't be accessible since there is no way to register them at runtime.

Likewise, some transport strategies we provide as part of the @nestjs/microservices package (including Kafka, gRPC, or RabbitMQ) require to subscribe/listen to specific topics/channels before the connection is established. Once your application starts listening to messages, the framework would not be able to subscribe/listen to new topics.

Lastly, the @nestjs/graphql package with the code first approach enabled automatically generates the GraphQL schema on-the-fly based on the metadata. That means, it requires all classes to be loaded beforehand. Otherwise, it would not be doable to create the appropriate, valid schema.

Most commonly, you will see lazy loaded modules in situations when your worker/cron job/lambda & serverless function/webhook must trigger different services (different logic) based on the input arguments (route path/date/query parameters, etc.). On the other hand, lazy loading modules may not make too much sense for monolithic applications, where the startup time is rather irrelevant.

**Examples:**

Example 1 (typescript):
```typescript
@Injectable()
export class CatsService {
  constructor(private lazyModuleLoader: LazyModuleLoader) {}
}
```

Example 2 (typescript):
```typescript
@Injectable()
@Dependencies(LazyModuleLoader)
export class CatsService {
  constructor(lazyModuleLoader) {
    this.lazyModuleLoader = lazyModuleLoader;
  }
}
```

Example 3 (typescript):
```typescript
// "app" represents a Nest application instance
const lazyModuleLoader = app.get(LazyModuleLoader);
```

Example 4 (typescript):
```typescript
const { LazyModule } = await import('./lazy.module');
const moduleRef = await this.lazyModuleLoader.load(() => LazyModule);
```

---

## 

**URL:** https://docs.nestjs.com/middleware

**Contents:**
  - Middleware
    - Dependency injection#
    - Applying middleware#
    - Route wildcards#
    - Middleware consumer#
    - Excluding routes#
    - Functional middleware#
    - Multiple middleware#
    - Global middleware#

Middleware is a function which is called before the route handler. Middleware functions have access to the request and response objects, and the next() middleware function in the application’s request-response cycle. The next middleware function is commonly denoted by a variable named next.

Nest middleware are, by default, equivalent to express middleware. The following description from the official express documentation describes the capabilities of middleware:

You implement custom Nest middleware in either a function, or in a class with an @Injectable() decorator. The class should implement the NestMiddleware interface, while the function does not have any special requirements. Let's start by implementing a simple middleware feature using the class method.

Nest middleware fully supports Dependency Injection. Just as with providers and controllers, they are able to inject dependencies that are available within the same module. As usual, this is done through the constructor.

There is no place for middleware in the @Module() decorator. Instead, we set them up using the configure() method of the module class. Modules that include middleware have to implement the NestModule interface. Let's set up the LoggerMiddleware at the AppModule level.

In the above example we have set up the LoggerMiddleware for the /cats route handlers that were previously defined inside the CatsController. We may also further restrict a middleware to a particular request method by passing an object containing the route path and request method to the forRoutes() method when configuring the middleware. In the example below, notice that we import the RequestMethod enum to reference the desired request method type.

Pattern-based routes are also supported in NestJS middleware. For example, the named wildcard (*splat) can be used as a wildcard to match any combination of characters in a route. In the following example, the middleware will be executed for any route that starts with abcd/, regardless of the number of characters that follow.

The 'abcd/*' route path will match abcd/1, abcd/123, abcd/abc, and so on. The hyphen ( -) and the dot (.) are interpreted literally by string-based paths. However, abcd/ with no additional characters will not match the route. For this, you need to wrap the wildcard in braces to make it optional:

The MiddlewareConsumer is a helper class. It provides several built-in methods to manage middleware. All of them can be simply chained in the fluent style. The forRoutes() method can take a single string, multiple strings, a RouteInfo object, a controller class and even multiple controller classes. In most cases you'll probably just pass a list of controllers separated by commas. Below is an example with a single controller:

At times, we may want to exclude certain routes from having middleware applied. This can be easily achieved using the exclude() method. The exclude() method accepts a single string, multiple strings, or a RouteInfo object to identify the routes to be excluded.

Here's an example of how to use it:

With the example above, LoggerMiddleware will be bound to all routes defined inside CatsControllerexcept the three passed to the exclude() method.

This approach provides flexibility in applying or excluding middleware based on specific routes or route patterns.

The LoggerMiddleware class we've been using is quite simple. It has no members, no additional methods, and no dependencies. Why can't we just define it in a simple function instead of a class? In fact, we can. This type of middleware is called functional middleware. Let's transform the logger middleware from class-based into functional middleware to illustrate the difference:

And use it within the AppModule:

As mentioned above, in order to bind multiple middleware that are executed sequentially, simply provide a comma separated list inside the apply() method:

If we want to bind middleware to every registered route at once, we can use the use() method that is supplied by the INestApplication instance:

**Examples:**

Example 1 (typescript):
```typescript
import { Injectable, NestMiddleware } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';

@Injectable()
export class LoggerMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    console.log('Request...');
    next();
  }
}
```

Example 2 (typescript):
```typescript
import { Injectable } from '@nestjs/common';

@Injectable()
export class LoggerMiddleware {
  use(req, res, next) {
    console.log('Request...');
    next();
  }
}
```

Example 3 (typescript):
```typescript
import { Module, NestModule, MiddlewareConsumer } from '@nestjs/common';
import { LoggerMiddleware } from './common/middleware/logger.middleware';
import { CatsModule } from './cats/cats.module';

@Module({
  imports: [CatsModule],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer
      .apply(LoggerMiddleware)
      .forRoutes('cats');
  }
}
```

Example 4 (typescript):
```typescript
import { Module } from '@nestjs/common';
import { LoggerMiddleware } from './common/middleware/logger.middleware';
import { CatsModule } from './cats/cats.module';

@Module({
  imports: [CatsModule],
})
export class AppModule {
  configure(consumer) {
    consumer
      .apply(LoggerMiddleware)
      .forRoutes('cats');
  }
}
```

---

## 

**URL:** https://docs.nestjs.com/websockets/pipes

**Contents:**
  - Pipes
    - Binding pipes#

There is no fundamental difference between regular pipes and web sockets pipes. The only difference is that instead of throwing HttpException, you should use WsException. In addition, all pipes will be only applied to the data parameter (because validating or transforming client instance is useless).

The following example uses a manually instantiated method-scoped pipe. Just as with HTTP based applications, you can also use gateway-scoped pipes (i.e., prefix the gateway class with a @UsePipes() decorator).

**Examples:**

Example 1 (typescript):
```typescript
@UsePipes(new ValidationPipe({ exceptionFactory: (errors) => new WsException(errors) }))
@SubscribeMessage('events')
handleEvent(client: Client, data: unknown): WsResponse<unknown> {
  const event = 'events';
  return { event, data };
}
```

Example 2 (typescript):
```typescript
@UsePipes(new ValidationPipe({ exceptionFactory: (errors) => new WsException(errors) }))
@SubscribeMessage('events')
handleEvent(client, data) {
  const event = 'events';
  return { event, data };
}
```

---

## 

**URL:** https://docs.nestjs.com/first-steps

**Contents:**
  - First steps
    - Language#
    - Prerequisites#
    - Setup#
- Learn the right way!
    - Platform#
    - Running the application#
    - Linting and formatting#

In this set of articles, you'll learn the core fundamentals of Nest. To get familiar with the essential building blocks of Nest applications, we'll build a basic CRUD application with features that cover a lot of ground at an introductory level.

We're in love with TypeScript, but above all - we love Node.js. That's why Nest is compatible with both TypeScript and pure JavaScript. Nest takes advantage of the latest language features, so to use it with vanilla JavaScript we need a Babel compiler.

We'll mostly use TypeScript in the examples we provide, but you can always switch the code snippets to vanilla JavaScript syntax (simply click to toggle the language button in the upper right hand corner of each snippet).

Please make sure that Node.js (version >= 20) is installed on your operating system.

Setting up a new project is quite simple with the Nest CLI. With npm installed, you can create a new Nest project with the following commands in your OS terminal:

The project-name directory will be created, node modules and a few other boilerplate files will be installed, and a src/ directory will be created and populated with several core files.

Here's a brief overview of those core files:

The main.ts includes an async function, which will bootstrap our application:

To create a Nest application instance, we use the core NestFactory class. NestFactory exposes a few static methods that allow creating an application instance. The create() method returns an application object, which fulfills the INestApplication interface. This object provides a set of methods which are described in the coming chapters. In the main.ts example above, we simply start up our HTTP listener, which lets the application await inbound HTTP requests.

Note that a project scaffolded with the Nest CLI creates an initial project structure that encourages developers to follow the convention of keeping each module in its own dedicated directory.

Learn the right way! 80+ chapters 5+ hours of videos Official certificate Deep-dive sessions Explore official courses

Nest aims to be a platform-agnostic framework. Platform independence makes it possible to create reusable logical parts that developers can take advantage of across several different types of applications. Technically, Nest is able to work with any Node HTTP framework once an adapter is created. There are two HTTP platforms supported out-of-the-box: express and fastify. You can choose the one that best suits your needs.

Whichever platform is used, it exposes its own application interface. These are seen respectively as NestExpressApplication and NestFastifyApplication.

When you pass a type to the NestFactory.create() method, as in the example below, the app object will have methods available exclusively for that specific platform. Note, however, you don't need to specify a type unless you actually want to access the underlying platform API.

Once the installation process is complete, you can run the following command at your OS command prompt to start the application listening for inbound HTTP requests:

This command starts the app with the HTTP server listening on the port defined in the src/main.ts file. Once the application is running, open your browser and navigate to http://localhost:3000/. You should see the Hello World! message.

To watch for changes in your files, you can run the following command to start the application:

This command will watch your files, automatically recompiling and reloading the server.

CLI provides best effort to scaffold a reliable development workflow at scale. Thus, a generated Nest project comes with both a code linter and formatter preinstalled (respectively eslint and prettier).

To ensure maximum stability and extensibility, we use the base eslint and prettier cli packages. This setup allows neat IDE integration with official extensions by design.

For headless environments where an IDE is not relevant (Continuous Integration, Git hooks, etc.) a Nest project comes with ready-to-use npm scripts.

**Examples:**

Example 1 (bash):
```bash
$ npm i -g @nestjs/cli
$ nest new project-name
```

Example 2 (typescript):
```typescript
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();
```

Example 3 (typescript):
```typescript
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();
```

Example 4 (typescript):
```typescript
const app = await NestFactory.create<NestExpressApplication>(AppModule);
```

---

## 

**URL:** https://docs.nestjs.com/websockets/interceptors

**Contents:**
  - Interceptors

There is no difference between regular interceptors and web sockets interceptors. The following example uses a manually instantiated method-scoped interceptor. Just as with HTTP based applications, you can also use gateway-scoped interceptors (i.e., prefix the gateway class with a @UseInterceptors() decorator).

**Examples:**

Example 1 (typescript):
```typescript
@UseInterceptors(new TransformInterceptor())
@SubscribeMessage('events')
handleEvent(client: Client, data: unknown): WsResponse<unknown> {
  const event = 'events';
  return { event, data };
}
```

Example 2 (typescript):
```typescript
@UseInterceptors(new TransformInterceptor())
@SubscribeMessage('events')
handleEvent(client, data) {
  const event = 'events';
  return { event, data };
}
```

---

## 

**URL:** https://docs.nestjs.com/guards

**Contents:**
  - Guards
    - Authorization guard#
- Official enterprise support
    - Execution context#
    - Role-based authentication#
    - Binding guards#
    - Setting roles per handler#
    - Putting it all together#

A guard is a class annotated with the @Injectable() decorator, which implements the CanActivate interface.

Guards have a single responsibility. They determine whether a given request will be handled by the route handler or not, depending on certain conditions (like permissions, roles, ACLs, etc.) present at run-time. This is often referred to as authorization. Authorization (and its cousin, authentication, with which it usually collaborates) has typically been handled by middleware in traditional Express applications. Middleware is a fine choice for authentication, since things like token validation and attaching properties to the request object are not strongly connected with a particular route context (and its metadata).

But middleware, by its nature, is dumb. It doesn't know which handler will be executed after calling the next() function. On the other hand, Guards have access to the ExecutionContext instance, and thus know exactly what's going to be executed next. They're designed, much like exception filters, pipes, and interceptors, to let you interpose processing logic at exactly the right point in the request/response cycle, and to do so declaratively. This helps keep your code DRY and declarative.

As mentioned, authorization is a great use case for Guards because specific routes should be available only when the caller (usually a specific authenticated user) has sufficient permissions. The AuthGuard that we'll build now assumes an authenticated user (and that, therefore, a token is attached to the request headers). It will extract and validate the token, and use the extracted information to determine whether the request can proceed or not.

The logic inside the validateRequest() function can be as simple or sophisticated as needed. The main point of this example is to show how guards fit into the request/response cycle.

Every guard must implement a canActivate() function. This function should return a boolean, indicating whether the current request is allowed or not. It can return the response either synchronously or asynchronously (via a Promise or Observable). Nest uses the return value to control the next action:

Official enterprise support Providing technical guidance Performing in-depth code reviews Mentoring team members Advising best practices Explore more

The canActivate() function takes a single argument, the ExecutionContext instance. The ExecutionContext inherits from ArgumentsHost. We saw ArgumentsHost previously in the exception filters chapter. In the sample above, we are just using the same helper methods defined on ArgumentsHost that we used earlier, to get a reference to the Request object. You can refer back to the Arguments host section of the exception filters chapter for more on this topic.

By extending ArgumentsHost, ExecutionContext also adds several new helper methods that provide additional details about the current execution process. These details can be helpful in building more generic guards that can work across a broad set of controllers, methods, and execution contexts. Learn more about ExecutionContexthere.

Let's build a more functional guard that permits access only to users with a specific role. We'll start with a basic guard template, and build on it in the coming sections. For now, it allows all requests to proceed:

Like pipes and exception filters, guards can be controller-scoped, method-scoped, or global-scoped. Below, we set up a controller-scoped guard using the @UseGuards() decorator. This decorator may take a single argument, or a comma-separated list of arguments. This lets you easily apply the appropriate set of guards with one declaration.

Above, we passed the RolesGuard class (instead of an instance), leaving responsibility for instantiation to the framework and enabling dependency injection. As with pipes and exception filters, we can also pass an in-place instance:

The construction above attaches the guard to every handler declared by this controller. If we wish the guard to apply only to a single method, we apply the @UseGuards() decorator at the method level.

In order to set up a global guard, use the useGlobalGuards() method of the Nest application instance:

Global guards are used across the whole application, for every controller and every route handler. In terms of dependency injection, global guards registered from outside of any module (with useGlobalGuards() as in the example above) cannot inject dependencies since this is done outside the context of any module. In order to solve this issue, you can set up a guard directly from any module using the following construction:

Our RolesGuard is working, but it's not very smart yet. We're not yet taking advantage of the most important guard feature - the execution context. It doesn't yet know about roles, or which roles are allowed for each handler. The CatsController, for example, could have different permission schemes for different routes. Some might be available only for an admin user, and others could be open for everyone. How can we match roles to routes in a flexible and reusable way?

This is where custom metadata comes into play (learn more here). Nest provides the ability to attach custom metadata to route handlers through either decorators created via Reflector.createDecorator static method, or the built-in @SetMetadata() decorator.

For example, let's create a @Roles() decorator using the Reflector.createDecorator method that will attach the metadata to the handler. Reflector is provided out of the box by the framework and exposed from the @nestjs/core package.

The Roles decorator here is a function that takes a single argument of type string[].

Now, to use this decorator, we simply annotate the handler with it:

Here we've attached the Roles decorator metadata to the create() method, indicating that only users with the admin role should be allowed to access this route.

Alternatively, instead of using the Reflector.createDecorator method, we could use the built-in @SetMetadata() decorator. Learn more about here.

Let's now go back and tie this together with our RolesGuard. Currently, it simply returns true in all cases, allowing every request to proceed. We want to make the return value conditional based on comparing the roles assigned to the current user to the actual roles required by the current route being processed. In order to access the route's role(s) (custom metadata), we'll use the Reflector helper class again, as follows:

Refer to the Reflection and metadata section of the Execution context chapter for more details on utilizing Reflector in a context-sensitive way.

When a user with insufficient privileges requests an endpoint, Nest automatically returns the following response:

Note that behind the scenes, when a guard returns false, the framework throws a ForbiddenException. If you want to return a different error response, you should throw your own specific exception. For example:

Any exception thrown by a guard will be handled by the exceptions layer (global exceptions filter and any exceptions filters that are applied to the current context).

**Examples:**

Example 1 (typescript):
```typescript
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Observable } from 'rxjs';

@Injectable()
export class AuthGuard implements CanActivate {
  canActivate(
    context: ExecutionContext,
  ): boolean | Promise<boolean> | Observable<boolean> {
    const request = context.switchToHttp().getRequest();
    return validateRequest(request);
  }
}
```

Example 2 (typescript):
```typescript
import { Injectable } from '@nestjs/common';

@Injectable()
export class AuthGuard {
  async canActivate(context) {
    const request = context.switchToHttp().getRequest();
    return validateRequest(request);
  }
}
```

Example 3 (typescript):
```typescript
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Observable } from 'rxjs';

@Injectable()
export class RolesGuard implements CanActivate {
  canActivate(
    context: ExecutionContext,
  ): boolean | Promise<boolean> | Observable<boolean> {
    return true;
  }
}
```

Example 4 (typescript):
```typescript
import { Injectable } from '@nestjs/common';

@Injectable()
export class RolesGuard {
  canActivate(context) {
    return true;
  }
}
```

---

## 

**URL:** https://docs.nestjs.com/faq/request-lifecycle

**Contents:**
  - Request lifecycle
    - Middleware#
    - Guards#
    - Interceptors#
    - Pipes#
    - Filters#
    - Summary#

Nest applications handle requests and produce responses in a sequence we refer to as the request lifecycle. With the use of middleware, pipes, guards, and interceptors, it can be challenging to track down where a particular piece of code executes during the request lifecycle, especially as global, controller level, and route level components come into play. In general, a request flows through middleware to guards, then to interceptors, then to pipes and finally back to interceptors on the return path (as the response is generated).

Middleware is executed in a particular sequence. First, Nest runs globally bound middleware (such as middleware bound with app.use) and then it runs module bound middleware, which are determined on paths. Middleware are run sequentially in the order they are bound, similar to the way middleware in Express works. In the case of middleware bound across different modules, the middleware bound to the root module will run first, and then middleware will run in the order that the modules are added to the imports array.

Guard execution starts with global guards, then proceeds to controller guards, and finally to route guards. As with middleware, guards run in the order in which they are bound. For example:

Guard1 will execute before Guard2 and both will execute before Guard3.

Interceptors, for the most part, follow the same pattern as guards, with one catch: as interceptors return RxJS Observables, the observables will be resolved in a first in last out manner. So inbound requests will go through the standard global, controller, route level resolution, but the response side of the request (i.e., after returning from the controller method handler) will be resolved from route to controller to global. Also, any errors thrown by pipes, controllers, or services can be read in the catchError operator of an interceptor.

Pipes follow the standard global to controller to route bound sequence, with the same first in first out in regards to the @UsePipes() parameters. However, at a route parameter level, if you have multiple pipes running, they will run in the order of the last parameter with a pipe to the first. This also applies to the route level and controller level pipes. For example, if we have the following controller:

then the GeneralValidationPipe will run for the query, then the params, and then the body objects before moving on to the RouteSpecificPipe, which follows the same order. If any parameter-specific pipes were in place, they would run (again, from the last to first parameter) after the controller and route level pipes.

Filters are the only component that do not resolve global first. Instead, filters resolve from the lowest level possible, meaning execution starts with any route bound filters and proceeding next to controller level, and finally to global filters. Note that exceptions cannot be passed from filter to filter; if a route level filter catches the exception, a controller or global level filter cannot catch the same exception. The only way to achieve an effect like this is to use inheritance between the filters.

In general, the request lifecycle looks like the following:

**Examples:**

Example 1 (typescript):
```typescript
@UseGuards(Guard1, Guard2)
@Controller('cats')
export class CatsController {
  constructor(private catsService: CatsService) {}

  @UseGuards(Guard3)
  @Get()
  getCats(): Cats[] {
    return this.catsService.getCats();
  }
}
```

Example 2 (typescript):
```typescript
@UsePipes(GeneralValidationPipe)
@Controller('cats')
export class CatsController {
  constructor(private catsService: CatsService) {}

  @UsePipes(RouteSpecificPipe)
  @Patch(':id')
  updateCat(
    @Body() body: UpdateCatDTO,
    @Param() params: UpdateCatParams,
    @Query() query: UpdateCatQuery,
  ) {
    return this.catsService.updateCat(body, params, query);
  }
}
```

---

## 

**URL:** https://docs.nestjs.com/microservices/guards

**Contents:**
  - Guards
    - Binding guards#

There is no fundamental difference between microservices guards and regular HTTP application guards. The only difference is that instead of throwing HttpException, you should use RpcException.

The following example uses a method-scoped guard. Just as with HTTP based applications, you can also use controller-scoped guards (i.e., prefix the controller class with a @UseGuards() decorator).

**Examples:**

Example 1 (typescript):
```typescript
@UseGuards(AuthGuard)
@MessagePattern({ cmd: 'sum' })
accumulate(data: number[]): number {
  return (data || []).reduce((a, b) => a + b);
}
```

Example 2 (typescript):
```typescript
@UseGuards(AuthGuard)
@MessagePattern({ cmd: 'sum' })
accumulate(data) {
  return (data || []).reduce((a, b) => a + b);
}
```

---

## 

**URL:** https://docs.nestjs.com/fundamentals/execution-context

**Contents:**
  - Execution context
    - ArgumentsHost class#
    - Current application context#
    - Host handler arguments#
    - ExecutionContext class#
- Official enterprise support
    - Reflection and metadata#
    - Low-level approach#

Nest provides several utility classes that help make it easy to write applications that function across multiple application contexts (e.g., Nest HTTP server-based, microservices and WebSockets application contexts). These utilities provide information about the current execution context which can be used to build generic guards, filters, and interceptors that can work across a broad set of controllers, methods, and execution contexts.

We cover two such classes in this chapter: ArgumentsHost and ExecutionContext.

The ArgumentsHost class provides methods for retrieving the arguments being passed to a handler. It allows choosing the appropriate context (e.g., HTTP, RPC (microservice), or WebSockets) to retrieve the arguments from. The framework provides an instance of ArgumentsHost, typically referenced as a host parameter, in places where you may want to access it. For example, the catch() method of an exception filter is called with an ArgumentsHostinstance.

ArgumentsHost simply acts as an abstraction over a handler's arguments. For example, for HTTP server applications (when @nestjs/platform-express is being used), the host object encapsulates Express's [request, response, next] array, where request is the request object, response is the response object, and next is a function that controls the application's request-response cycle. On the other hand, for GraphQL applications, the host object contains the [root, args, context, info] array.

When building generic guards, filters, and interceptors which are meant to run across multiple application contexts, we need a way to determine the type of application that our method is currently running in. Do this with the getType() method of ArgumentsHost:

With the application type available, we can write more generic components, as shown below.

To retrieve the array of arguments being passed to the handler, one approach is to use the host object's getArgs() method.

You can pluck a particular argument by index using the getArgByIndex() method:

In these examples we retrieved the request and response objects by index, which is not typically recommended as it couples the application to a particular execution context. Instead, you can make your code more robust and reusable by using one of the host object's utility methods to switch to the appropriate application context for your application. The context switch utility methods are shown below.

Let's rewrite the previous example using the switchToHttp() method. The host.switchToHttp() helper call returns an HttpArgumentsHost object that is appropriate for the HTTP application context. The HttpArgumentsHost object has two useful methods we can use to extract the desired objects. We also use the Express type assertions in this case to return native Express typed objects:

Similarly WsArgumentsHost and RpcArgumentsHost have methods to return appropriate objects in the microservices and WebSockets contexts. Here are the methods for WsArgumentsHost:

Following are the methods for RpcArgumentsHost:

ExecutionContext extends ArgumentsHost, providing additional details about the current execution process. Like ArgumentsHost, Nest provides an instance of ExecutionContext in places you may need it, such as in the canActivate() method of a guard and the intercept() method of an interceptor. It provides the following methods:

The getHandler() method returns a reference to the handler about to be invoked. The getClass() method returns the type of the Controller class which this particular handler belongs to. For example, in an HTTP context, if the currently processed request is a POST request, bound to the create() method on the CatsController, getHandler() returns a reference to the create() method and getClass() returns the CatsControllerclass (not instance).

The ability to access references to both the current class and handler method provides great flexibility. Most importantly, it gives us the opportunity to access the metadata set through either decorators created via Reflector#createDecorator or the built-in @SetMetadata() decorator from within guards or interceptors. We cover this use case below.

Official enterprise support Providing technical guidance Performing in-depth code reviews Mentoring team members Advising best practices Explore more

Nest provides the ability to attach custom metadata to route handlers through decorators created via Reflector#createDecorator method, and the built-in @SetMetadata() decorator. In this section, let's compare the two approaches and see how to access the metadata from within a guard or interceptor.

To create strongly-typed decorators using Reflector#createDecorator, we need to specify the type argument. For example, let's create a Roles decorator that takes an array of strings as an argument.

The Roles decorator here is a function that takes a single argument of type string[].

Now, to use this decorator, we simply annotate the handler with it:

Here we've attached the Roles decorator metadata to the create() method, indicating that only users with the admin role should be allowed to access this route.

To access the route's role(s) (custom metadata), we'll use the Reflector helper class again. Reflector can be injected into a class in the normal way:

Now, to read the handler metadata, use the get() method:

The Reflector#get method allows us to easily access the metadata by passing in two arguments: a decorator reference and a context (decorator target) to retrieve the metadata from. In this example, the specified decorator is Roles (refer back to the roles.decorator.ts file above). The context is provided by the call to context.getHandler(), which results in extracting the metadata for the currently processed route handler. Remember, getHandler() gives us a reference to the route handler function.

Alternatively, we may organize our controller by applying metadata at the controller level, applying to all routes in the controller class.

In this case, to extract controller metadata, we pass context.getClass() as the second argument (to provide the controller class as the context for metadata extraction) instead of context.getHandler():

Given the ability to provide metadata at multiple levels, you may need to extract and merge metadata from several contexts. The Reflector class provides two utility methods used to help with this. These methods extract both controller and method metadata at once, and combine them in different ways.

Consider the following scenario, where you've supplied Roles metadata at both levels.

If your intent is to specify 'user' as the default role, and override it selectively for certain methods, you would probably use the getAllAndOverride() method.

A guard with this code, running in the context of the create() method, with the above metadata, would result in roles containing ['admin'].

To get metadata for both and merge it (this method merges both arrays and objects), use the getAllAndMerge() method:

This would result in roles containing ['user', 'admin'].

For both of these merge methods, you pass the metadata key as the first argument, and an array of metadata target contexts (i.e., calls to the getHandler() and/or getClass() methods) as the second argument.

As mentioned earlier, instead of using Reflector#createDecorator, you can also use the built-in @SetMetadata() decorator to attach metadata to a handler.

With the construction above, we attached the roles metadata (roles is a metadata key and ['admin'] is the associated value) to the create() method. While this works, it's not good practice to use @SetMetadata() directly in your routes. Instead, you can create your own decorators, as shown below:

This approach is much cleaner and more readable, and somewhat resembles the Reflector#createDecorator approach. The difference is that with @SetMetadata you have more control over the metadata key and value, and also can create decorators that take more than one argument.

Now that we have a custom @Roles() decorator, we can use it to decorate the create() method.

To access the route's role(s) (custom metadata), we'll use the Reflector helper class again:

Now, to read the handler metadata, use the get() method.

Here instead of passing a decorator reference, we pass the metadata key as the first argument (which in our case is 'roles'). Everything else remains the same as in the Reflector#createDecorator example.

**Examples:**

Example 1 (typescript):
```typescript
if (host.getType() === 'http') {
  // do something that is only important in the context of regular HTTP requests (REST)
} else if (host.getType() === 'rpc') {
  // do something that is only important in the context of Microservice requests
} else if (host.getType<GqlContextType>() === 'graphql') {
  // do something that is only important in the context of GraphQL requests
}
```

Example 2 (typescript):
```typescript
const [req, res, next] = host.getArgs();
```

Example 3 (typescript):
```typescript
const request = host.getArgByIndex(0);
const response = host.getArgByIndex(1);
```

Example 4 (typescript):
```typescript
/**
 * Switch context to RPC.
 */
switchToRpc(): RpcArgumentsHost;
/**
 * Switch context to HTTP.
 */
switchToHttp(): HttpArgumentsHost;
/**
 * Switch context to WebSockets.
 */
switchToWs(): WsArgumentsHost;
```

---

## 

**URL:** https://docs.nestjs.com/modules

**Contents:**
  - Modules
    - Feature modules#
    - Shared modules#
- Explore your graph with NestJS Devtools
    - Module re-exporting#
    - Dependency injection#
    - Global modules#
    - Dynamic modules#

A module is a class that is annotated with the @Module() decorator. This decorator provides metadata that Nest uses to organize and manage the application structure efficiently.

Every Nest application has at least one module, the root module, which serves as the starting point for Nest to build the application graph. This graph is an internal structure that Nest uses to resolve relationships and dependencies between modules and providers. While small applications might only have a root module, this is generally not the case. Modules are highly recommended as an effective way to organize your components. For most applications, you'll likely have multiple modules, each encapsulating a closely related set of capabilities.

The @Module() decorator takes a single object with properties that describe the module:

The module encapsulates providers by default, meaning you can only inject providers that are either part of the current module or explicitly exported from other imported modules. The exported providers from a module essentially serve as the module's public interface or API.

In our example, the CatsController and CatsService are closely related and serve the same application domain. It makes sense to group them into a feature module. A feature module organizes code that is relevant to a specific feature, helping to maintain clear boundaries and better organization. This is particularly important as the application or team grows, and it aligns with the SOLID principles.

Next, we'll create the CatsModule to demonstrate how to group the controller and service.

Above, we defined the CatsModule in the cats.module.ts file, and moved everything related to this module into the cats directory. The last thing we need to do is import this module into the root module (the AppModule, defined in the app.module.ts file).

Here is how our directory structure looks now:

In Nest, modules are singletons by default, and thus you can share the same instance of any provider between multiple modules effortlessly.

Every module is automatically a shared module. Once created it can be reused by any module. Let's imagine that we want to share an instance of the CatsService between several other modules. In order to do that, we first need to export the CatsService provider by adding it to the module's exports array, as shown below:

Now any module that imports the CatsModule has access to the CatsService and will share the same instance with all other modules that import it as well.

If we were to directly register the CatsService in every module that requires it, it would indeed work, but it would result in each module getting its own separate instance of the CatsService. This can lead to increased memory usage since multiple instances of the same service are created, and it could also cause unexpected behavior, such as state inconsistency if the service maintains any internal state.

By encapsulating the CatsService inside a module, such as the CatsModule, and exporting it, we ensure that the same instance of CatsService is reused across all modules that import CatsModule. This not only reduces memory consumption but also leads to more predictable behavior, as all modules share the same instance, making it easier to manage shared states or resources. This is one of the key benefits of modularity and dependency injection in frameworks like NestJS—allowing services to be efficiently shared throughout the application.

Explore your graph with NestJS Devtools Graph visualizer Routes navigator Interactive playground CI/CD integration Sign up

As seen above, Modules can export their internal providers. In addition, they can re-export modules that they import. In the example below, the CommonModule is both imported into and exported from the CoreModule, making it available for other modules which import this one.

A module class can inject providers as well (e.g., for configuration purposes):

However, module classes themselves cannot be injected as providers due to circular dependency .

If you have to import the same set of modules everywhere, it can get tedious. Unlike in Nest, Angularproviders are registered in the global scope. Once defined, they're available everywhere. Nest, however, encapsulates providers inside the module scope. You aren't able to use a module's providers elsewhere without first importing the encapsulating module.

When you want to provide a set of providers which should be available everywhere out-of-the-box (e.g., helpers, database connections, etc.), make the module global with the @Global() decorator.

The @Global() decorator makes the module global-scoped. Global modules should be registered only once, generally by the root or core module. In the above example, the CatsService provider will be ubiquitous, and modules that wish to inject the service will not need to import the CatsModule in their imports array.

Dynamic modules in Nest allow you to create modules that can be configured at runtime. This is especially useful when you need to provide flexible, customizable modules where the providers can be created based on certain options or configurations. Here's a brief overview of how dynamic modules work.

This module defines the Connection provider by default (in the @Module() decorator metadata), but additionally - depending on the entities and options objects passed into the forRoot() method - exposes a collection of providers, for example, repositories. Note that the properties returned by the dynamic module extend (rather than override) the base module metadata defined in the @Module() decorator. That's how both the statically declared Connection provider and the dynamically generated repository providers are exported from the module.

If you want to register a dynamic module in the global scope, set the global property to true.

The DatabaseModule can be imported and configured in the following manner:

If you want to in turn re-export a dynamic module, you can omit the forRoot() method call in the exports array:

The Dynamic modules chapter covers this topic in greater detail, and includes a working example.

**Examples:**

Example 1 (typescript):
```typescript
import { Module } from '@nestjs/common';
import { CatsController } from './cats.controller';
import { CatsService } from './cats.service';

@Module({
  controllers: [CatsController],
  providers: [CatsService],
})
export class CatsModule {}
```

Example 2 (typescript):
```typescript
import { Module } from '@nestjs/common';
import { CatsModule } from './cats/cats.module';

@Module({
  imports: [CatsModule],
})
export class AppModule {}
```

Example 3 (typescript):
```typescript
import { Module } from '@nestjs/common';
import { CatsController } from './cats.controller';
import { CatsService } from './cats.service';

@Module({
  controllers: [CatsController],
  providers: [CatsService],
  exports: [CatsService]
})
export class CatsModule {}
```

Example 4 (typescript):
```typescript
@Module({
  imports: [CommonModule],
  exports: [CommonModule],
})
export class CoreModule {}
```

---

## 

**URL:** https://docs.nestjs.com/fundamentals/async-providers

**Contents:**
  - Asynchronous providers
    - Injection#
    - Example#

At times, the application start should be delayed until one or more asynchronous tasks are completed. For example, you may not want to start accepting requests until the connection with the database has been established. You can achieve this using asynchronous providers.

The syntax for this is to use async/await with the useFactory syntax. The factory returns a Promise, and the factory function can await asynchronous tasks. Nest will await resolution of the promise before instantiating any class that depends on (injects) such a provider.

Asynchronous providers are injected to other components by their tokens, like any other provider. In the example above, you would use the construct @Inject('ASYNC_CONNECTION').

The TypeORM recipe has a more substantial example of an asynchronous provider.

**Examples:**

Example 1 (typescript):
```typescript
{
  provide: 'ASYNC_CONNECTION',
  useFactory: async () => {
    const connection = await createConnection(options);
    return connection;
  },
}
```

---
