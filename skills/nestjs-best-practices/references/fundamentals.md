# Nestjs - Fundamentals

**Pages:** 4

---

## 

**URL:** https://docs.nestjs.com/fundamentals/injection-scopes

**Contents:**
  - Injection scopes
    - Provider scope#
    - Usage#
    - Controller scope#
    - Scope hierarchy#
- Learn the right way!
    - Request provider#
    - Inquirer provider#
    - Performance#
    - Durable providers#

For people coming from different programming language backgrounds, it might be unexpected to learn that in Nest, almost everything is shared across incoming requests. We have a connection pool to the database, singleton services with global state, etc. Remember that Node.js doesn't follow the request/response Multi-Threaded Stateless Model in which every request is processed by a separate thread. Hence, using singleton instances is fully safe for our applications.

However, there are edge cases when request-based lifetime may be the desired behavior, for instance, per-request caching in GraphQL applications, request tracking, and multi-tenancy. Injection scopes provide a mechanism to obtain the desired provider lifetime behavior.

A provider can have any of the following scopes:

Specify injection scope by passing the scope property to the @Injectable() decorator options object:

Similarly, for custom providers, set the scope property in the long-hand form for a provider registration:

Singleton scope is used by default and does not need be declared. If you do want to declare a provider as singleton scoped, use the Scope.DEFAULT value for the scope property.

Controllers can also have scope, which applies to all request method handlers declared in that controller. Like provider scope, the scope of a controller declares its lifetime. For a request-scoped controller, a new instance is created for each inbound request, and garbage-collected when the request has completed processing.

Declare controller scope with the scope property of the ControllerOptions object:

The REQUEST scope bubbles up the injection chain. A controller that depends on a request-scoped provider will, itself, be request-scoped.

Imagine the following dependency graph: CatsController <- CatsService <- CatsRepository. If CatsService is request-scoped (and the others are default singletons), the CatsController will become request-scoped as it is dependent on the injected service. The CatsRepository, which is not dependent, would remain singleton-scoped.

Transient-scoped dependencies don't follow that pattern. If a singleton-scoped DogsService injects a transient LoggerService provider, it will receive a fresh instance of it. However, DogsService will stay singleton-scoped, so injecting it anywhere would not resolve to a new instance of DogsService. In case it's desired behavior, DogsService must be explicitly marked as TRANSIENT as well.

Learn the right way! 80+ chapters 5+ hours of videos Official certificate Deep-dive sessions Explore official courses

In an HTTP server-based application (e.g., using @nestjs/platform-express or @nestjs/platform-fastify), you may want to access a reference to the original request object when using request-scoped providers. You can do this by injecting the REQUEST object.

The REQUEST provider is inherently request-scoped, meaning you don't need to specify the REQUEST scope explicitly when using it. Additionally, even if you attempt to do so, it will be disregarded. Any provider that relies on a request-scoped provider automatically adopts a request scope, and this behavior cannot be altered.

Because of underlying platform/protocol differences, you access the inbound request slightly differently for Microservice or GraphQL applications. In GraphQL applications, you inject CONTEXT instead of REQUEST:

You then configure your context value (in the GraphQLModule) to contain request as its property.

If you want to get the class where a provider was constructed, for instance in logging or metrics providers, you can inject the INQUIRER token.

And then use it as follows:

In the example above when AppService#getRoot is called, "AppService: My name is getRoot" will be logged to the console.

Using request-scoped providers will have an impact on application performance. While Nest tries to cache as much metadata as possible, it will still have to create an instance of your class on each request. Hence, it will slow down your average response time and overall benchmarking result. Unless a provider must be request-scoped, it is strongly recommended that you use the default singleton scope.

Request-scoped providers, as mentioned in the section above, may lead to increased latency since having at least 1 request-scoped provider (injected into the controller instance, or deeper - injected into one of its providers) makes the controller request-scoped as well. That means it must be recreated (instantiated) per each individual request (and garbage collected afterward). Now, that also means, that for let's say 30k requests in parallel, there will be 30k ephemeral instances of the controller (and its request-scoped providers).

Having a common provider that most providers depend on (think of a database connection, or a logger service), automatically converts all those providers to request-scoped providers as well. This can pose a challenge in multi-tenant applications, especially for those that have a central request-scoped "data source" provider that grabs headers/token from the request object and based on its values, retrieves the corresponding database connection/schema (specific to that tenant).

For instance, let's say you have an application alternately used by 10 different customers. Each customer has its own dedicated data source, and you want to make sure customer A will never be able to reach customer B's database. One way to achieve this could be to declare a request-scoped "data source" provider that - based on the request object - determines what's the "current customer" and retrieves its corresponding database. With this approach, you can turn your application into a multi-tenant application in just a few minutes. But, a major downside to this approach is that since most likely a large chunk of your application' components rely on the "data source" provider, they will implicitly become "request-scoped", and therefore you will undoubtedly see an impact in your apps performance.

But what if we had a better solution? Since we only have 10 customers, couldn't we have 10 individual DI sub-trees per customer (instead of recreating each tree per request)? If your providers don't rely on any property that's truly unique for each consecutive request (e.g., request UUID) but instead there're some specific attributes that let us aggregate (classify) them, there's no reason to recreate DI sub-tree on every incoming request.

And that's exactly when the durable providers come in handy.

Before we start flagging providers as durable, we must first register a strategy that instructs Nest what are those "common request attributes", provide logic that groups requests - associates them with their corresponding DI sub-trees.

The value returned from the attach method instructs Nest what context identifier should be used for a given host. In this case, we specified that the tenantSubTreeId should be used instead of the original, auto-generated contextId object, when the host component (e.g., request-scoped controller) is flagged as durable (you can learn how to mark providers as durable below). Also, in the above example, no payload would be registered (where payload = REQUEST/CONTEXT provider that represents the "root" - parent of the sub-tree).

If you want to register the payload for a durable tree, use the following construction instead:

Now whenever you inject the REQUEST provider (or CONTEXT for GraphQL applications) using the @Inject(REQUEST)/@Inject(CONTEXT), the payload object would be injected (consisting of a single property - tenantId in this case).

Alright so with this strategy in place, you can register it somewhere in your code (as it applies globally anyway), so for example, you could place it in the main.ts file:

As long as the registration occurs before any request hits your application, everything will work as intended.

Lastly, to turn a regular provider into a durable provider, simply set the durable flag to true and change its scope to Scope.REQUEST (not needed if the REQUEST scope is in the injection chain already):

Similarly, for custom providers, set the durable property in the long-hand form for a provider registration:

**Examples:**

Example 1 (typescript):
```typescript
import { Injectable, Scope } from '@nestjs/common';

@Injectable({ scope: Scope.REQUEST })
export class CatsService {}
```

Example 2 (typescript):
```typescript
{
  provide: 'CACHE_MANAGER',
  useClass: CacheManager,
  scope: Scope.TRANSIENT,
}
```

Example 3 (typescript):
```typescript
@Controller({
  path: 'cats',
  scope: Scope.REQUEST,
})
export class CatsController {}
```

Example 4 (typescript):
```typescript
import { Injectable, Scope, Inject } from '@nestjs/common';
import { REQUEST } from '@nestjs/core';
import { Request } from 'express';

@Injectable({ scope: Scope.REQUEST })
export class CatsService {
  constructor(@Inject(REQUEST) private request: Request) {}
}
```

---

## 

**URL:** https://docs.nestjs.com/fundamentals/platform-agnosticism

**Contents:**
  - Platform agnosticism
    - Build once, use everywhere#

Nest is a platform-agnostic framework. This means you can develop reusable logical parts that can be used across different types of applications. For example, most components can be re-used without change across different underlying HTTP server frameworks (e.g., Express and Fastify), and even across different types of applications (e.g., HTTP server frameworks, Microservices with different transport layers, and Web Sockets).

The Overview section of the documentation primarily shows coding techniques using HTTP server frameworks (e.g., apps providing a REST API or providing an MVC-style server-side rendered app). However, all those building blocks can be used on top of different transport layers (microservices or websockets).

Furthermore, Nest comes with a dedicated GraphQL module. You can use GraphQL as your API layer interchangeably with providing a REST API.

In addition, the application context feature helps to create any kind of Node.js application - including things like CRON jobs and CLI apps - on top of Nest.

Nest aspires to be a full-fledged platform for Node.js apps that brings a higher-level of modularity and reusability to your applications. Build once, use everywhere!

---

## 

**URL:** https://docs.nestjs.com/fundamentals/testing

**Contents:**
  - Testing
    - Installation#
    - Unit testing#
    - Testing utilities#
- Learn the right way!
    - Auto mocking#
    - End-to-end testing#
    - Overriding globally registered enhancers#
    - Testing request-scoped instances#

Automated testing is considered an essential part of any serious software development effort. Automation makes it easy to repeat individual tests or test suites quickly and easily during development. This helps ensure that releases meet quality and performance goals. Automation helps increase coverage and provides a faster feedback loop to developers. Automation both increases the productivity of individual developers and ensures that tests are run at critical development lifecycle junctures, such as source code control check-in, feature integration, and version release.

Such tests often span a variety of types, including unit tests, end-to-end (e2e) tests, integration tests, and so on. While the benefits are unquestionable, it can be tedious to set them up. Nest strives to promote development best practices, including effective testing, so it includes features such as the following to help developers and teams build and automate tests. Nest:

As mentioned, you can use any testing framework that you like, as Nest doesn't force any specific tooling. Simply replace the elements needed (such as the test runner), and you will still enjoy the benefits of Nest's ready-made testing facilities.

To get started, first install the required package:

In the following example, we test two classes: CatsController and CatsService. As mentioned, Jest is provided as the default testing framework. It serves as a test-runner and also provides assert functions and test-double utilities that help with mocking, spying, etc. In the following basic test, we manually instantiate these classes, and ensure that the controller and service fulfill their API contract.

Because the above sample is trivial, we aren't really testing anything Nest-specific. Indeed, we aren't even using dependency injection (notice that we pass an instance of CatsService to our catsController). This form of testing - where we manually instantiate the classes being tested - is often called isolated testing as it is independent from the framework. Let's introduce some more advanced capabilities that help you test applications that make more extensive use of Nest features.

The @nestjs/testing package provides a set of utilities that enable a more robust testing process. Let's rewrite the previous example using the built-in Test class:

The Test class is useful for providing an application execution context that essentially mocks the full Nest runtime, but gives you hooks that make it easy to manage class instances, including mocking and overriding. The Test class has a createTestingModule() method that takes a module metadata object as its argument (the same object you pass to the @Module() decorator). This method returns a TestingModule instance which in turn provides a few methods. For unit tests, the important one is the compile() method. This method bootstraps a module with its dependencies (similar to the way an application is bootstrapped in the conventional main.ts file using NestFactory.create()), and returns a module that is ready for testing.

TestingModule inherits from the module reference class, and therefore its ability to dynamically resolve scoped providers (transient or request-scoped). Do this with the resolve() method (the get() method can only retrieve static instances).

Instead of using the production version of any provider, you can override it with a custom provider for testing purposes. For example, you can mock a database service instead of connecting to a live database. We'll cover overrides in the next section, but they're available for unit tests as well.

Learn the right way! 80+ chapters 5+ hours of videos Official certificate Deep-dive sessions Explore official courses

Nest also allows you to define a mock factory to apply to all of your missing dependencies. This is useful for cases where you have a large number of dependencies in a class and mocking all of them will take a long time and a lot of setup. To make use of this feature, the createTestingModule() will need to be chained up with the useMocker() method, passing a factory for your dependency mocks. This factory can take in an optional token, which is an instance token, any token which is valid for a Nest provider, and returns a mock implementation. The below is an example of creating a generic mocker using jest-mock and a specific mock for CatsService using jest.fn().

You can also retrieve these mocks out of the testing container as you normally would custom providers, moduleRef.get(CatsService).

Unlike unit testing, which focuses on individual modules and classes, end-to-end (e2e) testing covers the interaction of classes and modules at a more aggregate level -- closer to the kind of interaction that end-users will have with the production system. As an application grows, it becomes hard to manually test the end-to-end behavior of each API endpoint. Automated end-to-end tests help us ensure that the overall behavior of the system is correct and meets project requirements. To perform e2e tests we use a similar configuration to the one we just covered in unit testing. In addition, Nest makes it easy to use the Supertest library to simulate HTTP requests.

In this example, we build on some of the concepts described earlier. In addition to the compile() method we used earlier, we now use the createNestApplication() method to instantiate a full Nest runtime environment.

One caveat to consider is that when your application is compiled using the compile() method, the HttpAdapterHost#httpAdapter will be undefined at that time. This is because there isn't an HTTP adapter or server created yet during this compilation phase. If your test requires the httpAdapter, you should use the createNestApplication() method to create the application instance, or refactor your project to avoid this dependency when initializing the dependencies graph.

Alright, let's break down the example:

We save a reference to the running app in our app variable so we can use it to simulate HTTP requests.

We simulate HTTP tests using the request() function from Supertest. We want these HTTP requests to route to our running Nest app, so we pass the request() function a reference to the HTTP listener that underlies Nest (which, in turn, may be provided by the Express platform). Hence the construction request(app.getHttpServer()). The call to request() hands us a wrapped HTTP Server, now connected to the Nest app, which exposes methods to simulate an actual HTTP request. For example, using request(...).get('/cats') will initiate a request to the Nest app that is identical to an actual HTTP request like get '/cats' coming in over the network.

In this example, we also provide an alternate (test-double) implementation of the CatsService which simply returns a hard-coded value that we can test for. Use overrideProvider() to provide such an alternate implementation. Similarly, Nest provides methods to override modules, guards, interceptors, filters and pipes with the overrideModule(), overrideGuard(), overrideInterceptor(), overrideFilter(), and overridePipe() methods respectively.

Each of the override methods (except for overrideModule()) returns an object with 3 different methods that mirror those described for custom providers:

On the other hand, overrideModule() returns an object with the useModule() method, which you can use to supply a module that will override the original module, as follows:

Each of the override method types, in turn, returns the TestingModule instance, and can thus be chained with other methods in the fluent style. You should use compile() at the end of such a chain to cause Nest to instantiate and initialize the module.

Also, sometimes you may want to provide a custom logger e.g. when the tests are run (for example, on a CI server). Use the setLogger() method and pass an object that fulfills the LoggerService interface to instruct the TestModuleBuilder how to log during tests (by default, only "error" logs will be logged to the console).

The compiled module has several useful methods, as described in the following table:

If you have a globally registered guard (or pipe, interceptor, or filter), you need to take a few more steps to override that enhancer. To recap the original registration looks like this:

This is registering the guard as a "multi"-provider through the APP_* token. To be able to replace the JwtAuthGuard here, the registration needs to use an existing provider in this slot:

Now the JwtAuthGuard is visible to Nest as a regular provider that can be overridden when creating the TestingModule:

Now all your tests will use the MockAuthGuard on every request.

Request-scoped providers are created uniquely for each incoming request. The instance is garbage-collected after the request has completed processing. This poses a problem, because we can't access a dependency injection sub-tree generated specifically for a tested request.

We know (based on the sections above) that the resolve() method can be used to retrieve a dynamically instantiated class. Also, as described here, we know we can pass a unique context identifier to control the lifecycle of a DI container sub-tree. How do we leverage this in a testing context?

The strategy is to generate a context identifier beforehand and force Nest to use this particular ID to create a sub-tree for all incoming requests. In this way we'll be able to retrieve instances created for a tested request.

To accomplish this, use jest.spyOn() on the ContextIdFactory:

Now we can use the contextId to access a single generated DI container sub-tree for any subsequent request.

**Examples:**

Example 1 (bash):
```bash
$ npm i --save-dev @nestjs/testing
```

Example 2 (typescript):
```typescript
import { CatsController } from './cats.controller';
import { CatsService } from './cats.service';

describe('CatsController', () => {
  let catsController: CatsController;
  let catsService: CatsService;

  beforeEach(() => {
    catsService = new CatsService();
    catsController = new CatsController(catsService);
  });

  describe('findAll', () => {
    it('should return an array of cats', async () => {
      const result = ['test'];
      jest.spyOn(catsService, 'findAll').mockImplementation(() => result);

      expect(await catsController.findAll()).toBe(result);
    });
  });
});
```

Example 3 (typescript):
```typescript
import { CatsController } from './cats.controller';
import { CatsService } from './cats.service';

describe('CatsController', () => {
  let catsController;
  let catsService;

  beforeEach(() => {
    catsService = new CatsService();
    catsController = new CatsController(catsService);
  });

  describe('findAll', () => {
    it('should return an array of cats', async () => {
      const result = ['test'];
      jest.spyOn(catsService, 'findAll').mockImplementation(() => result);

      expect(await catsController.findAll()).toBe(result);
    });
  });
});
```

Example 4 (typescript):
```typescript
import { Test } from '@nestjs/testing';
import { CatsController } from './cats.controller';
import { CatsService } from './cats.service';

describe('CatsController', () => {
  let catsController: CatsController;
  let catsService: CatsService;

  beforeEach(async () => {
    const moduleRef = await Test.createTestingModule({
        controllers: [CatsController],
        providers: [CatsService],
      }).compile();

    catsService = moduleRef.get(CatsService);
    catsController = moduleRef.get(CatsController);
  });

  describe('findAll', () => {
    it('should return an array of cats', async () => {
      const result = ['test'];
      jest.spyOn(catsService, 'findAll').mockImplementation(() => result);

      expect(await catsController.findAll()).toBe(result);
    });
  });
});
```

---

## 

**URL:** https://docs.nestjs.com/fundamentals/module-ref

**Contents:**
  - Module reference
    - Retrieving instances#
    - Resolving scoped providers#
    - Registering REQUEST provider#
    - Getting current sub-tree#
    - Instantiating custom classes dynamically#
- Explore your graph with NestJS Devtools

Nest provides the ModuleRef class to navigate the internal list of providers and obtain a reference to any provider using its injection token as a lookup key. The ModuleRef class also provides a way to dynamically instantiate both static and scoped providers. ModuleRef can be injected into a class in the normal way:

The ModuleRef instance (hereafter we'll refer to it as the module reference) has a get() method. By default, this method returns a provider, controller, or injectable (e.g., guard, interceptor, etc.) that was registered and has been instantiated in the current module using its injection token/class name. If the instance is not found, an exception will be raised.

To retrieve a provider from the global context (for example, if the provider has been injected in a different module), pass the { strict: false } option as a second argument to get().

To dynamically resolve a scoped provider (transient or request-scoped), use the resolve() method, passing the provider's injection token as an argument.

The resolve() method returns a unique instance of the provider, from its own DI container sub-tree. Each sub-tree has a unique context identifier. Thus, if you call this method more than once and compare instance references, you will see that they are not equal.

To generate a single instance across multiple resolve() calls, and ensure they share the same generated DI container sub-tree, you can pass a context identifier to the resolve() method. Use the ContextIdFactory class to generate a context identifier. This class provides a create() method that returns an appropriate unique identifier.

Manually generated context identifiers (with ContextIdFactory.create()) represent DI sub-trees in which REQUEST provider is undefined as they are not instantiated and managed by the Nest dependency injection system.

To register a custom REQUEST object for a manually created DI sub-tree, use the ModuleRef#registerRequestByContextId() method, as follows:

Occasionally, you may want to resolve an instance of a request-scoped provider within a request context. Let's say that CatsService is request-scoped and you want to resolve the CatsRepository instance which is also marked as a request-scoped provider. In order to share the same DI container sub-tree, you must obtain the current context identifier instead of generating a new one (e.g., with the ContextIdFactory.create() function, as shown above). To obtain the current context identifier, start by injecting the request object using @Inject() decorator.

Now, use the getByRequest() method of the ContextIdFactory class to create a context id based on the request object, and pass this to the resolve() call:

To dynamically instantiate a class that wasn't previously registered as a provider, use the module reference's create() method.

This technique enables you to conditionally instantiate different classes outside of the framework container.

Explore your graph with NestJS Devtools Graph visualizer Routes navigator Interactive playground CI/CD integration Sign up

**Examples:**

Example 1 (typescript):
```typescript
@Injectable()
export class CatsService {
  constructor(private moduleRef: ModuleRef) {}
}
```

Example 2 (typescript):
```typescript
@Injectable()
@Dependencies(ModuleRef)
export class CatsService {
  constructor(moduleRef) {
    this.moduleRef = moduleRef;
  }
}
```

Example 3 (typescript):
```typescript
@Injectable()
export class CatsService implements OnModuleInit {
  private service: Service;
  constructor(private moduleRef: ModuleRef) {}

  onModuleInit() {
    this.service = this.moduleRef.get(Service);
  }
}
```

Example 4 (typescript):
```typescript
@Injectable()
@Dependencies(ModuleRef)
export class CatsService {
  constructor(moduleRef) {
    this.moduleRef = moduleRef;
  }

  onModuleInit() {
    this.service = this.moduleRef.get(Service);
  }
}
```

---
