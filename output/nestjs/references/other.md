# Nestjs - Other

**Pages:** 14

---

## 

**URL:** https://docs.nestjs.com/openapi/migration-guide

**Contents:**
  - Introduction
    - Philosophy#
    - Installation#
    - Alternatives#

Nest (NestJS) is a framework for building efficient, scalable Node.js server-side applications. It uses progressive JavaScript, is built with and fully supports TypeScript (yet still enables developers to code in pure JavaScript) and combines elements of OOP (Object Oriented Programming), FP (Functional Programming), and FRP (Functional Reactive Programming).

Under the hood, Nest makes use of robust HTTP Server frameworks like Express (the default) and optionally can be configured to use Fastify as well!

Nest provides a level of abstraction above these common Node.js frameworks (Express/Fastify), but also exposes their APIs directly to the developer. This gives developers the freedom to use the myriad of third-party modules which are available for the underlying platform.

In recent years, thanks to Node.js, JavaScript has become the “lingua franca” of the web for both front and backend applications. This has given rise to awesome projects like Angular, React and Vue, which improve developer productivity and enable the creation of fast, testable, and extensible frontend applications. However, while plenty of superb libraries, helpers, and tools exist for Node (and server-side JavaScript), none of them effectively solve the main problem of architecture.

Nest provides an out-of-the-box application architecture which allows developers and teams to create highly testable, scalable, loosely coupled, and easily maintainable applications. The architecture is heavily inspired by Angular.

To get started, you can either scaffold the project with the Nest CLI, or clone a starter project (both will produce the same outcome).

To scaffold the project with the Nest CLI, run the following commands. This will create a new project directory, and populate the directory with the initial core Nest files and supporting modules, creating a conventional base structure for your project. Creating a new project with the Nest CLI is recommended for first-time users. We'll continue with this approach in First Steps.

Alternatively, to install the TypeScript starter project with Git:

Open your browser and navigate to http://localhost:3000/.

To install the JavaScript flavor of the starter project, use javascript-starter.git in the command sequence above.

You can also start a new project from scratch by installing the core and supporting packages. Keep in mind that you'll need to set up the project boilerplate files on your own. At a minimum, you'll need these dependencies: @nestjs/core, @nestjs/common, rxjs, and reflect-metadata. Check out this short article on how to create a complete project: 5 steps to create a bare minimum NestJS app from scratch!.

**Examples:**

Example 1 (bash):
```bash
$ npm i -g @nestjs/cli
$ nest new project-name
```

Example 2 (bash):
```bash
$ git clone https://github.com/nestjs/typescript-starter.git project
$ cd project
$ npm install
$ npm run start
```

---

## 

**URL:** https://docs.nestjs.com/migration-guide

**Contents:**
  - Migration guide
    - Upgrading packages#
    - Express v5#
    - Query parameters parsing#
    - Fastify v5#
    - Fastify CORS#
    - Fastify middleware registration#
    - Module resolution algorithm#
    - Reflector type inference#
    - Lifecycle hooks execution order#

This article offers a comprehensive guide for migrating from NestJS version 10 to version 11. To explore the new features introduced in v11, take a look at this article. While the update includes a few minor breaking changes, they are unlikely to impact most users. You can review the complete list of changes here.

Although you can manually upgrade your packages, we recommend using npm-check-updates (ncu) for a more streamlined process.

After years of development, Express v5 was officially released in 2024 and became a stable version in 2025. With NestJS 11, Express v5 is now the default version integrated into the framework. While this update is seamless for most users, it’s important to be aware that Express v5 introduces some breaking changes. For detailed guidance, refer to the Express v5 migration guide.

One of the most notable updates in Express v5 is the revised path route matching algorithm. The following changes have been introduced to how path strings are matched with incoming requests:

That said, routes that previously worked in Express v4 may not work in Express v5. For example:

To fix this issue, you can update the route to use a named wildcard:

Similarly, if you have a middleware that runs on all routes, you may need to update the path to use a named wildcard:

Instead, you can update the path to use a named wildcard:

Note that {*splat} is a named wildcard that matches any path including the root path. Outer braces make path optional.

In Express v5, query parameters are no longer parsed using the qs library by default. Instead, the simple parser is used, which does not support nested objects or arrays.

As a result, query strings like these:

will no longer be parsed as expected. To revert to the previous behavior, you can configure Express to use the extended parser (the default in Express v4) by setting the query parser option to extended:

@nestjs/platform-fastify v11 now finally supports Fastify v5. This update should be seamless for most users; however, Fastify v5 introduces a few breaking changes, though these are unlikely to affect the majority of NestJS users. For more detailed information, refer to the Fastify v5 migration guide.

By default, only CORS-safelisted methods are allowed. If you need to enable additional methods (such as PUT, PATCH, or DELETE), you must explicitly define them in the methods option.

NestJS 11 now uses the latest version of the path-to-regexp package to match middleware paths in @nestjs/platform-fastify. As a result, the (.*) syntax for matching all paths is no longer supported. Instead, you should use named wildcards.

For example, if you have a middleware that applies to all routes:

You'll need to update it to use a named wildcard instead:

Where splat is just an arbitrary name for the wildcard parameter. You can name it anything you like.

Starting with NestJS 11, the module resolution algorithm has been improved to enhance performance and reduce memory usage for most applications. This change does not require any manual intervention, but there are some edge cases where the behavior may differ from previous versions.

In NestJS v10 and earlier, dynamic modules were assigned a unique opaque key generated from the module's dynamic metadata. This key was used to identify the module in the module registry. For example, if you included TypeOrmModule.forFeature([User]) in multiple modules, NestJS would deduplicate the modules and treat them as a single module node in the registry. This process is known as node deduplication.

With the release of NestJS v11, we no longer generate predictable hashes for dynamic modules. Instead, object references are now used to determine if one module is equivalent to another. To share the same dynamic module across multiple modules, simply assign it to a variable and import it wherever needed. This new approach provides more flexibility and ensures that dynamic modules are handled more efficiently.

This new algorithm might impact your integration tests if you use a lot of dynamic modules, because without the manually deduplication mentioned above, your TestingModule could have multiple instances of a dependency. This makes it a bit trickier to stub a method, because you'll need to target the correct instance. Your options are to either:

NestJS 11 introduces several improvements to the Reflector class, enhancing its functionality and type inference for metadata values. These updates provide a more intuitive and robust experience when working with metadata.

These enhancements improve the overall developer experience by providing better type safety and handling of metadata in NestJS 11.

Termination lifecycle hooks are now executed in the reverse order to their initialization counterparts. That said, hooks like OnModuleDestroy, BeforeApplicationShutdown, and OnApplicationShutdown are now executed in the reverse order.

Imagine the following scenario:

In this case, the OnModuleInit hooks are executed in the following order:

While the OnModuleDestroy hooks are executed in the reverse order:

In NestJS v11, the behavior of middleware registration has been updated. Previously, the order of middleware registration was determined by the topological sort of the module dependency graph, where the distance from the root module defined the order of middleware registration, regardless of whether the middleware was registered in a global module or a regular module. Global modules were treated like regular modules in this respect, which led to inconsistent behavior, especially when compared to other framework features.

From v11 onwards, middleware registered in global modules is now executed first, regardless of its position in the module dependency graph. This change ensures that global middleware always runs before any middleware from imported modules, maintaining a consistent and predictable order.

The CacheModule (from the @nestjs/cache-manager package) has been updated to support the latest version of the cache-manager package. This update brings a few breaking changes, including a migration to Keyv, which offers a unified interface for key-value storage across multiple backend stores through storage adapters.

The key difference between the previous version and the new version lies in the configuration of external stores. In the previous version, to register a Redis store, you would have likely configured it like this:

In the new version, you should use the Keyv adapter to configure the store:

Where KeyvRedis is imported from the @keyv/redis package. See the Caching documentation to learn more.

If you're using the ConfigModule from the @nestjs/config package, be aware of several breaking changes introduced in @nestjs/config@4.0.0. Most notably, the order in which configuration variables are read by the ConfigService#get method has been updated. The new order is:

Previously, validated environment variables and the process.env object were read first, preventing them from being overridden by internal configuration. With this update, internal configuration will now always take precedence over environment variables.

Additionally, the ignoreEnvVars configuration option, which previously allowed disabling validation of the process.env object, has been deprecated. Instead, use the validatePredefined option (set to false to disable validation of predefined environment variables). Predefined environment variables refer to process.env variables that were set before the module was imported. For example, if you start your application with PORT=3000 node main.js, the PORT variable is considered predefined. However, variables loaded by the ConfigModule from a .env file are not classified as predefined.

A new skipProcessEnv option has also been introduced. This option allows you to prevent the ConfigService#get method from accessing the process.env object entirely, which can be helpful when you want to restrict the service from reading environment variables directly.

If you are using the TerminusModule and have built your own custom health indicator, a new API has been introduced in version 11. The new HealthIndicatorService is designed to enhance the readability and testability of custom health indicators.

Before version 11, a health indicator might have looked like this:

Starting with version 11, it is recommended to use the new HealthIndicatorService API, which streamlines the implementation process. Here's how the same health indicator can now be implemented:

Starting with NestJS 11, Node.js v16 is no longer supported, as it reached its end-of-life (EOL) on September 11, 2023. Likewise, the security support is scheduled to end on April 30, 2025 for Node.js v18, so we went ahead and dropped support for it as well.

NestJS 11 now requires Node.js v20 or higher.

To ensure the best experience, we strongly recommend using the latest LTS version of Node.js.

In case you missed the announcement, we launched our official deployment platform, Mau, in 2024. Mau is a fully managed platform that simplifies the deployment process for NestJS applications. With Mau, you can deploy your applications to the cloud (AWS; Amazon Web Services) with a single command, manage your environment variables, and monitor your application's performance in real-time.

Mau makes provisioning and maintaining your infrastructure as simple as clicking just a few buttons. Mau is designed to be simple and intuitive, so you can focus on building your applications and not worry about the underlying infrastructure. Under the hood, we use Amazon Web Services to provide you with a powerful and reliable platform, while abstracting away all the complexity of AWS. We take care of all the heavy lifting for you, so you can focus on building your applications and growing your business.

You can learn more about Mau in this chapter.

**Examples:**

Example 1 (typescript):
```typescript
@Get('users/*')
findAll() {
  // In NestJS 11, this will be automatically converted to a valid Express v5 route.
  // While it may still work, it's no longer advisable to use this wildcard syntax in Express v5.
  return 'This route should not work in Express v5';
}
```

Example 2 (typescript):
```typescript
@Get('users/*splat')
findAll() {
  return 'This route will work in Express v5';
}
```

Example 3 (typescript):
```typescript
// In NestJS 11, this will be automatically converted to a valid Express v5 route.
// While it may still work, it's no longer advisable to use this wildcard syntax in Express v5.
forRoutes('*'); // <-- This should not work in Express v5
```

Example 4 (typescript):
```typescript
forRoutes('{*splat}'); // <-- This will work in Express v5
```

---

## 

**URL:** https://docs.nestjs.com/faq/hybrid-application

**Contents:**
  - Hybrid application
    - Sharing configuration#

A hybrid application is one that listens for requests from two or more different sources. This can combine an HTTP server with a microservice listener or even just multiple different microservice listeners. The default createMicroservice method does not allow for multiple servers so in this case each microservice must be created and started manually. In order to do this, the INestApplication instance can be connected with INestMicroservice instances through the connectMicroservice() method.

To connect multiple microservice instances, issue the call to connectMicroservice() for each microservice:

To bind @MessagePattern() to only one transport strategy (for example, MQTT) in a hybrid application with multiple microservices, we can pass the second argument of type Transport which is an enum with all the built-in transport strategies defined.

By default a hybrid application will not inherit global pipes, interceptors, guards and filters configured for the main (HTTP-based) application. To inherit these configuration properties from the main application, set the inheritAppConfig property in the second argument (an optional options object) of the connectMicroservice() call, as follow:

**Examples:**

Example 1 (typescript):
```typescript
const app = await NestFactory.create(AppModule);
const microservice = app.connectMicroservice<MicroserviceOptions>({
  transport: Transport.TCP,
});

await app.startAllMicroservices();
await app.listen(3001);
```

Example 2 (typescript):
```typescript
const app = await NestFactory.create(AppModule);
// microservice #1
const microserviceTcp = app.connectMicroservice<MicroserviceOptions>({
  transport: Transport.TCP,
  options: {
    port: 3001,
  },
});
// microservice #2
const microserviceRedis = app.connectMicroservice<MicroserviceOptions>({
  transport: Transport.REDIS,
  options: {
    host: 'localhost',
    port: 6379,
  },
});

await app.startAllMicroservices();
await app.listen(3001);
```

Example 3 (typescript):
```typescript
@MessagePattern('time.us.*', Transport.NATS)
getDate(@Payload() data: number[], @Ctx() context: NatsContext) {
  console.log(`Subject: ${context.getSubject()}`); // e.g. "time.us.east"
  return new Date().toLocaleTimeString(...);
}
@MessagePattern({ cmd: 'time.us' }, Transport.TCP)
getTCPDate(@Payload() data: number[]) {
  return new Date().toLocaleTimeString(...);
}
```

Example 4 (typescript):
```typescript
@Bind(Payload(), Ctx())
@MessagePattern('time.us.*', Transport.NATS)
getDate(data, context) {
  console.log(`Subject: ${context.getSubject()}`); // e.g. "time.us.east"
  return new Date().toLocaleTimeString(...);
}
@Bind(Payload(), Ctx())
@MessagePattern({ cmd: 'time.us' }, Transport.TCP)
getTCPDate(data, context) {
  return new Date().toLocaleTimeString(...);
}
```

---

## 

**URL:** https://docs.nestjs.com/recipes/documentation

**Contents:**
  - Documentation
    - Setup#
    - Generation#
    - Contribute#

Compodoc is a documentation tool for Angular applications. Since Nest and Angular share similar project and code structures, Compodoc works with Nest applications as well.

Setting up Compodoc inside an existing Nest project is very simple. Start by adding the dev-dependency with the following command in your OS terminal:

Generate project documentation using the following command (npm 6 is required for npx support). See the official documentation for more options.

Open your browser and navigate to http://localhost:8080. You should see an initial Nest CLI project:

You can participate and contribute to the Compodoc project here.

**Examples:**

Example 1 (bash):
```bash
$ npm i -D @compodoc/compodoc
```

Example 2 (bash):
```bash
$ npx @compodoc/compodoc -p tsconfig.json -s
```

---

## 

**URL:** https://docs.nestjs.com/faq/serverless

**Contents:**
  - Serverless
    - Cold start#
    - Benchmarks#
    - Runtime optimizations#
    - Example integration#
    - Using standalone application feature#

Serverless computing is a cloud computing execution model in which the cloud provider allocates machine resources on-demand, taking care of the servers on behalf of their customers. When an app is not in use, there are no computing resources allocated to the app. Pricing is based on the actual amount of resources consumed by an application (source).

With a serverless architecture, you focus purely on the individual functions in your application code. Services such as AWS Lambda, Google Cloud Functions, and Microsoft Azure Functions take care of all the physical hardware, virtual machine operating system, and web server software management.

A cold start is the first time your code has been executed in a while. Depending on a cloud provider you use, it may span several different operations, from downloading the code and bootstrapping the runtime to eventually running your code. This process adds significant latency depending on several factors, the language, the number of packages your application require, etc.

The cold start is important and although there are things which are beyond our control, there's still a lot of things we can do on our side to make it as short as possible.

While you can think of Nest as a fully-fledged framework designed to be used in complex, enterprise applications, it is also suitable for much "simpler" applications (or scripts). For example, with the use of Standalone applications feature, you can take advantage of Nest's DI system in simple workers, CRON jobs, CLIs, or serverless functions.

To better understand what's the cost of using Nest or other, well-known libraries (like express) in the context of serverless functions, let's compare how much time Node runtime needs to run the following scripts:

For all these scripts, we used the tsc (TypeScript) compiler and so the code remains unbundled (webpack isn't used).

Now, let's repeat all benchmarks but this time, using webpack (if you have Nest CLI installed, you can run nest build --webpack) to bundle our application into a single executable JavaScript file. However, instead of using the default webpack configuration that Nest CLI ships with, we'll make sure to bundle all dependencies (node_modules) together, as follows:

With this configuration, we received the following results:

As you can see, the way you compile (and whether you bundle your code) is crucial and has a significant impact on the overall startup time. With webpack, you can get the bootstrap time of a standalone Nest application (starter project with one module, controller, and service) down to ~32ms on average, and down to ~81.5ms for a regular HTTP, express-based NestJS app.

For more complicated Nest applications, for example, with 10 resources (generated through $ nest g resource schematic = 10 modules, 10 controllers, 10 services, 20 DTO classes, 50 HTTP endpoints + AppModule), the overall startup on MacBook Pro Mid 2014, 2.5 GHz Quad-Core Intel Core i7, 16 GB 1600 MHz DDR3, SSD is approximately 0.1298s (129.8ms). Running a monolithic application as a serverless function typically doesn't make too much sense anyway, so think of this benchmark more as an example of how the bootstrap time may potentially increase as your application grows.

Thus far we covered compile-time optimizations. These are unrelated to the way you define providers and load Nest modules in your application, and that plays an essential role as your application gets bigger.

For example, imagine having a database connection defined as an asynchronous provider. Async providers are designed to delay the application start until one or more asynchronous tasks are completed. That means, if your serverless function on average requires 2s to connect to the database (on bootstrap), your endpoint will need at least two extra seconds (because it must wait till the connection is established) to send a response back (when it's a cold start and your application wasn't running already).

As you can see, the way you structure your providers is somewhat different in a serverless environment where bootstrap time is important. Another good example is if you use Redis for caching, but only in certain scenarios. Perhaps, in this case, you should not define a Redis connection as an async provider, as it would slow down the bootstrap time, even if it's not required for this specific function invocation.

Also, sometimes you could lazy load entire modules, using the LazyModuleLoader class, as described in this chapter. Caching is a great example here too. Imagine that your application has, let's say, CacheModule which internally connects to Redis and also, exports the CacheService to interact with the Redis storage. If you don't need it for all potential function invocations, you can just load it on-demand, lazily. This way you'll get a faster startup time (when a cold start occurs) for all invocations that don't require caching.

Another great example is a webhook or worker, which depending on some specific conditions (e.g., input arguments), may perform different operations. In such a case, you could specify a condition inside your route handler that lazily loads an appropriate module for the specific function invocation, and just load every other module lazily.

The way your application's entry file (typically main.ts file) is supposed to look like depends on several factors and so there's no single template that just works for every scenario. For example, the initialization file required to spin up your serverless function varies by cloud providers (AWS, Azure, GCP, etc.). Also, depending on whether you want to run a typical HTTP application with multiple routes/endpoints or just provide a single route (or execute a specific portion of code), your application's code will look different (for example, for the endpoint-per-function approach you could use the NestFactory.createApplicationContext instead of booting the HTTP server, setting up middleware, etc.).

Just for illustration purposes, we'll integrate Nest (using @nestjs/platform-express and so spinning up the whole, fully functional HTTP router) with the Serverless framework (in this case, targeting AWS Lambda). As we've mentioned earlier, your code will differ depending on the cloud provider you choose, and many other factors.

First, let's install the required packages:

Once the installation process is complete, let's create the serverless.yml file to configure the Serverless framework:

With this in place, we can now navigate to the main.ts file and update our bootstrap code with the required boilerplate:

Next, open up the tsconfig.json file and make sure to enable the esModuleInterop option to make the @codegenie/serverless-express package load properly.

Now we can build our application (with nest build or tsc) and use the serverless CLI to start our lambda function locally:

Once the application is running, open your browser and navigate to http://localhost:3000/dev/[ANY_ROUTE] (where [ANY_ROUTE] is any endpoint registered in your application).

In the sections above, we've shown that using webpack and bundling your app can have significant impact on the overall bootstrap time. However, to make it work with our example, there are a few additional configurations you must add in your webpack.config.js file. Generally, to make sure our handler function will be picked up, we must change the output.libraryTarget property to commonjs2.

With this in place, you can now use $ nest build --webpack to compile your function's code (and then $ npx serverless offline to test it).

It's also recommended (but not required as it will slow down your build process) to install the terser-webpack-plugin package and override its configuration to keep classnames intact when minifying your production build. Not doing so can result in incorrect behavior when using class-validator within your application.

Alternatively, if you want to keep your function very lightweight and you don't need any HTTP-related features (routing, but also guards, interceptors, pipes, etc.), you can just use NestFactory.createApplicationContext (as mentioned earlier) instead of running the entire HTTP server (and express under the hood), as follows:

You could also pass the event object down to, let's say, EventsService provider that could process it and return a corresponding value (depending on the input value and your business logic).

**Examples:**

Example 1 (typescript):
```typescript
// #1 Express
import * as express from 'express';

async function bootstrap() {
  const app = express();
  app.get('/', (req, res) => res.send('Hello world!'));
  await new Promise<void>((resolve) => app.listen(3000, resolve));
}
bootstrap();

// #2 Nest (with @nestjs/platform-express)
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule, { logger: ['error'] });
  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();

// #3 Nest as a Standalone application (no HTTP server)
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { AppService } from './app.service';

async function bootstrap() {
  const app = await NestFactory.createApplicationContext(AppModule, {
    logger: ['error'],
  });
  console.log(app.get(AppService).getHello());
}
bootstrap();

// #4 Raw Node.js script
async function bootstrap() {
  console.log('Hello world!');
}
bootstrap();
```

Example 2 (javascript):
```javascript
module.exports = (options, webpack) => {
  const lazyImports = [
    '@nestjs/microservices/microservices-module',
    '@nestjs/websockets/socket-module',
  ];

  return {
    ...options,
    externals: [],
    plugins: [
      ...options.plugins,
      new webpack.IgnorePlugin({
        checkResource(resource) {
          if (lazyImports.includes(resource)) {
            try {
              require.resolve(resource);
            } catch (err) {
              return true;
            }
          }
          return false;
        },
      }),
    ],
  };
};
```

Example 3 (typescript):
```typescript
if (request.method === RequestMethod[RequestMethod.GET]) {
  const { CacheModule } = await import('./cache.module');
  const moduleRef = await this.lazyModuleLoader.load(() => CacheModule);

  const { CacheService } = await import('./cache.service');
  const cacheService = moduleRef.get(CacheService);

  return cacheService.get(ENDPOINT_KEY);
}
```

Example 4 (typescript):
```typescript
if (workerType === WorkerType.A) {
  const { WorkerAModule } = await import('./worker-a.module');
  const moduleRef = await this.lazyModuleLoader.load(() => WorkerAModule);
  // ...
} else if (workerType === WorkerType.B) {
  const { WorkerBModule } = await import('./worker-b.module');
  const moduleRef = await this.lazyModuleLoader.load(() => WorkerBModule);
  // ...
}
```

---

## 

**URL:** https://docs.nestjs.com/faq/global-prefix

**Contents:**
  - Global prefix

To set a prefix for every route registered in an HTTP application, use the setGlobalPrefix() method of the INestApplication instance.

You can exclude routes from the global prefix using the following construction:

Alternatively, you can specify route as a string (it will apply to every request method):

**Examples:**

Example 1 (typescript):
```typescript
const app = await NestFactory.create(AppModule);
app.setGlobalPrefix('v1');
```

Example 2 (typescript):
```typescript
app.setGlobalPrefix('v1', {
  exclude: [{ path: 'health', method: RequestMethod.GET }],
});
```

Example 3 (typescript):
```typescript
app.setGlobalPrefix('v1', { exclude: ['cats'] });
```

---

## 

**URL:** https://docs.nestjs.com/graphql/quick-start

**Contents:**
- Harnessing the power of TypeScript & GraphQL
    - Installation#
    - Overview#
- Learn the right way!
    - Getting started with GraphQL & TypeScript#
    - GraphQL playground#
    - Code first#
    - Example#
    - Schema first#
    - Apollo Sandbox#

GraphQL is a powerful query language for APIs and a runtime for fulfilling those queries with your existing data. It's an elegant approach that solves many problems typically found with REST APIs. For background, we suggest reading this comparison between GraphQL and REST. GraphQL combined with TypeScript helps you develop better type safety with your GraphQL queries, giving you end-to-end typing.

In this chapter, we assume a basic understanding of GraphQL, and focus on how to work with the built-in @nestjs/graphql module. The GraphQLModule can be configured to use Apollo server (with the @nestjs/apollo driver) and Mercurius (with the @nestjs/mercurius). We provide official integrations for these proven GraphQL packages to provide a simple way to use GraphQL with Nest (see more integrations here).

You can also build your own dedicated driver (read more on that here).

Start by installing the required packages:

Nest offers two ways of building GraphQL applications, the code first and the schema first methods. You should choose the one that works best for you. Most of the chapters in this GraphQL section are divided into two main parts: one you should follow if you adopt code first, and the other to be used if you adopt schema first.

In the code first approach, you use decorators and TypeScript classes to generate the corresponding GraphQL schema. This approach is useful if you prefer to work exclusively with TypeScript and avoid context switching between language syntaxes.

In the schema first approach, the source of truth is GraphQL SDL (Schema Definition Language) files. SDL is a language-agnostic way to share schema files between different platforms. Nest automatically generates your TypeScript definitions (using either classes or interfaces) based on the GraphQL schemas to reduce the need to write redundant boilerplate code.

Learn the right way! 20+ chapters GraphQL fundamentals Official certificate Deep-dive sessions Explore official GraphQL extensions

Once the packages are installed, we can import the GraphQLModule and configure it with the forRoot() static method.

The forRoot() method takes an options object as an argument. These options are passed through to the underlying driver instance (read more about available settings here: Apollo and Mercurius). For example, if you want to disable the playground and turn off debug mode (for Apollo), pass the following options:

In this case, these options will be forwarded to the ApolloServer constructor.

The playground is a graphical, interactive, in-browser GraphQL IDE, available by default on the same URL as the GraphQL server itself. To access the playground, you need a basic GraphQL server configured and running. To see it now, you can install and build the working example here. Alternatively, if you're following along with these code samples, once you've completed the steps in the Resolvers chapter, you can access the playground.

With that in place, and with your application running in the background, you can then open your web browser and navigate to http://localhost:3000/graphql (host and port may vary depending on your configuration). You will then see the GraphQL playground, as shown below.

If your application uses subscriptions, be sure to use graphql-ws, as subscriptions-transport-ws isn't supported by GraphiQL.

In the code first approach, you use decorators and TypeScript classes to generate the corresponding GraphQL schema.

To use the code first approach, start by adding the autoSchemaFile property to the options object:

The autoSchemaFile property value is the path where your automatically generated schema will be created. Alternatively, the schema can be generated on-the-fly in memory. To enable this, set the autoSchemaFile property to true:

By default, the types in the generated schema will be in the order they are defined in the included modules. To sort the schema lexicographically, set the sortSchema property to true:

A fully working code first sample is available here.

To use the schema first approach, start by adding a typePaths property to the options object. The typePaths property indicates where the GraphQLModule should look for GraphQL SDL schema definition files you'll be writing. These files will be combined in memory; this allows you to split your schemas into several files and locate them near their resolvers.

You will typically also need to have TypeScript definitions (classes and interfaces) that correspond to the GraphQL SDL types. Creating the corresponding TypeScript definitions by hand is redundant and tedious. It leaves us without a single source of truth -- each change made within SDL forces us to adjust TypeScript definitions as well. To address this, the @nestjs/graphql package can automatically generate TypeScript definitions from the abstract syntax tree (AST). To enable this feature, add the definitions options property when configuring the GraphQLModule.

The path property of the definitions object indicates where to save generated TypeScript output. By default, all generated TypeScript types are created as interfaces. To generate classes instead, specify the outputAs property with a value of 'class'.

The above approach dynamically generates TypeScript definitions each time the application starts. Alternatively, it may be preferable to build a simple script to generate these on demand. For example, assume we create the following script as generate-typings.ts:

Now you can run this script on demand:

To enable watch mode for the script (to automatically generate typings whenever any .graphql file changes), pass the watch option to the generate() method.

To automatically generate the additional __typename field for every object type, enable the emitTypenameField option:

To generate resolvers (queries, mutations, subscriptions) as plain fields without arguments, enable the skipResolverArgs option:

To generate enums as TypeScript union types instead of regular TypeScript enums, set the enumsAsTypes option to true:

To use Apollo Sandbox instead of the graphql-playground as a GraphQL IDE for local development, use the following configuration:

A fully working schema first sample is available here.

In some circumstances (for example end-to-end tests), you may want to get a reference to the generated schema object. In end-to-end tests, you can then run queries using the graphql object without using any HTTP listeners.

You can access the generated schema (in either the code first or schema first approach), using the GraphQLSchemaHost class:

When you need to pass module options asynchronously instead of statically, use the forRootAsync() method. As with most dynamic modules, Nest provides several techniques to deal with async configuration.

One technique is to use a factory function:

Like other factory providers, our factory function can be async and can inject dependencies through inject.

Alternatively, you can configure the GraphQLModule using a class instead of a factory, as shown below:

The construction above instantiates GqlConfigService inside GraphQLModule, using it to create options object. Note that in this example, the GqlConfigService has to implement the GqlOptionsFactory interface, as shown below. The GraphQLModule will call the createGqlOptions() method on the instantiated object of the supplied class.

If you want to reuse an existing options provider instead of creating a private copy inside the GraphQLModule, use the useExisting syntax.

Instead of using Apollo, Fastify users (read more here) can alternatively use the @nestjs/mercurius driver.

The forRoot() method takes an options object as an argument. These options are passed through to the underlying driver instance. Read more about available settings here.

Another useful feature of the @nestjs/graphql module is the ability to serve multiple endpoints at once. This lets you decide which modules should be included in which endpoint. By default, GraphQL searches for resolvers throughout the whole app. To limit this scan to only a subset of modules, use the include property.

A working example is available here.

**Examples:**

Example 1 (bash):
```bash
# For Express and Apollo (default)
$ npm i @nestjs/graphql @nestjs/apollo @apollo/server @as-integrations/express5 graphql

# For Fastify and Apollo
# npm i @nestjs/graphql @nestjs/apollo @apollo/server @as-integrations/fastify graphql

# For Fastify and Mercurius
# npm i @nestjs/graphql @nestjs/mercurius graphql mercurius
```

Example 2 (typescript):
```typescript
import { Module } from '@nestjs/common';
import { GraphQLModule } from '@nestjs/graphql';
import { ApolloDriver, ApolloDriverConfig } from '@nestjs/apollo';

@Module({
  imports: [
    GraphQLModule.forRoot<ApolloDriverConfig>({
      driver: ApolloDriver,
    }),
  ],
})
export class AppModule {}
```

Example 3 (typescript):
```typescript
import { Module } from '@nestjs/common';
import { GraphQLModule } from '@nestjs/graphql';
import { ApolloDriver, ApolloDriverConfig } from '@nestjs/apollo';

@Module({
  imports: [
    GraphQLModule.forRoot<ApolloDriverConfig>({
      driver: ApolloDriver,
      playground: false,
    }),
  ],
})
export class AppModule {}
```

Example 4 (typescript):
```typescript
GraphQLModule.forRoot<ApolloDriverConfig>({
  driver: ApolloDriver,
  graphiql: true,
}),
```

---

## 

**URL:** https://docs.nestjs.com/faq/common-errors

**Contents:**
  - Common errors
    - "Cannot resolve dependency" error#
- Explore your graph with NestJS Devtools
    - "Circular dependency" error#
    - Debugging dependency errors#
    - "File change detected" loops endlessly#

During your development with NestJS, you may encounter various errors as you learn the framework.

Probably the most common error message is about Nest not being able to resolve dependencies of a provider. The error message usually looks something like this:

The most common culprit of the error, is not having the <provider> in the module's providers array. Please make sure that the provider is indeed in the providers array and following standard NestJS provider practices.

There are a few gotchas, that are common. One is putting a provider in an imports array. If this is the case, the error will have the provider's name where <module> should be.

If you run across this error while developing, take a look at the module mentioned in the error message and look at its providers. For each provider in the providers array, make sure the module has access to all of the dependencies. Often times, providers are duplicated in a "Feature Module" and a "Root Module" which means Nest will try to instantiate the provider twice. More than likely, the module containing the <provider> being duplicated should be added in the "Root Module"'s imports array instead.

If the <unknown_token> above is dependency, you might have a circular file import. This is different from the circular dependency below because instead of having providers depend on each other in their constructors, it just means that two files end up importing each other. A common case would be a module file declaring a token and importing a provider, and the provider import the token constant from the module file. If you are using barrel files, ensure that your barrel imports do not end up creating these circular imports as well.

If the <unknown_token> above is Object, it means that you're injecting using an type/interface without a proper provider's token. To fix that, make sure that:

Also, make sure you didn't end up injecting the provider on itself because self-injections are not allowed in NestJS. When this happens, <unknown_token> will likely be equal to <provider>.

Explore your graph with NestJS Devtools Graph visualizer Routes navigator Interactive playground CI/CD integration Sign up

If you are in a monorepo setup, you may face the same error as above but for core provider called ModuleRef as a <unknown_token>:

This likely happens when your project end up loading two Node modules of the package @nestjs/core, like this:

Occasionally you'll find it difficult to avoid circular dependencies in your application. You'll need to take some steps to help Nest resolve these. Errors that arise from circular dependencies look like this:

Circular dependencies can arise from both providers depending on each other, or typescript files depending on each other for constants, such as exporting constants from a module file and importing them in a service file. In the latter case, it is advised to create a separate file for your constants. In the former case, please follow the guide on circular dependencies and make sure that both the modules and the providers are marked with forwardRef.

Along with just manually verifying your dependencies are correct, as of Nest 8.1.0 you can set the NEST_DEBUG environment variable to a string that resolves as truthy, and get extra logging information while Nest is resolving all of the dependencies for the application.

In the above image, the string in yellow is the host class of the dependency being injected, the string in blue is the name of the injected dependency, or its injection token, and the string in purple is the module in which the dependency is being searched for. Using this, you can usually trace back the dependency resolution for what's happening and why you're getting dependency injection problems.

Windows users who are using TypeScript version 4.9 and up may encounter this problem. This happens when you're trying to run your application in watch mode, e.g npm run start:dev and see an endless loop of the log messages:

When you're using the NestJS CLI to start your application in watch mode it is done by calling tsc --watch, and as of version 4.9 of TypeScript, a new strategy for detecting file changes is used which is likely to be the cause of this problem. In order to fix this problem, you need to add a setting to your tsconfig.json file after the "compilerOptions" option as follows:

This tells TypeScript to use the polling method for checking for file changes instead of file system events (the new default method), which can cause issues on some machines. You can read more about the "watchFile" option in TypeScript documentation.

**Examples:**

Example 1 (bash):
```bash
Nest can't resolve dependencies of the <provider> (?). Please make sure that the argument <unknown_token> at index [<index>] is available in the <module> context.

Potential solutions:
- Is <module> a valid NestJS module?
- If <unknown_token> is a provider, is it part of the current <module>?
- If <unknown_token> is exported from a separate @Module, is that module imported within <module>?
  @Module({
    imports: [ /* the Module containing <unknown_token> */ ]
  })
```

Example 2 (bash):
```bash
Nest can't resolve dependencies of the <provider> (?).
Please make sure that the argument ModuleRef at index [<index>] is available in the <module> context.
...
```

Example 3 (python):
```python
.
├── package.json
├── apps
│   └── api
│       └── node_modules
│           └── @nestjs/bull
│               └── node_modules
│                   └── @nestjs/core
└── node_modules
    ├── (other packages)
    └── @nestjs/core
```

Example 4 (bash):
```bash
Nest cannot create the <module> instance.
The module at index [<index>] of the <module> "imports" array is undefined.

Potential causes:
- A circular dependency between modules. Use forwardRef() to avoid it. Read more: https://docs.nestjs.com/fundamentals/circular-dependency
- The module at index [<index>] is of type "undefined". Check your import statements and the type of the module.

Scope [<module_import_chain>]
# example chain AppModule -> FooModule
```

---

## 

**URL:** https://docs.nestjs.com/cli/overview

**Contents:**
  - Overview
    - Installation#
    - Basic workflow#
    - Project structure#
- Learn the right way!
    - CLI command syntax#
    - Command overview#
    - Requirements#

The Nest CLI is a command-line interface tool that helps you to initialize, develop, and maintain your Nest applications. It assists in multiple ways, including scaffolding the project, serving it in development mode, and building and bundling the application for production distribution. It embodies best-practice architectural patterns to encourage well-structured apps.

Note: In this guide we describe using npm to install packages, including the Nest CLI. Other package managers may be used at your discretion. With npm, you have several options available for managing how your OS command line resolves the location of the nest CLI binary file. Here, we describe installing the nest binary globally using the -g option. This provides a measure of convenience, and is the approach we assume throughout the documentation. Note that installing anynpm package globally leaves the responsibility of ensuring they're running the correct version up to the user. It also means that if you have different projects, each will run the same version of the CLI. A reasonable alternative is to use the npx program, built into the npm cli (or similar features with other package managers) to ensure that you run a managed version of the Nest CLI. We recommend you consult the npx documentation and/or your DevOps support staff for more information.

Install the CLI globally using the npm install -g command (see the Note above for details about global installs).

Once installed, you can invoke CLI commands directly from your OS command line through the nest executable. See the available nest commands by entering the following:

Get help on an individual command using the following construct. Substitute any command, like new, add, etc., where you see generate in the example below to get detailed help on that command:

To create, build and run a new basic Nest project in development mode, go to the folder that should be the parent of your new project, and run the following commands:

In your browser, open http://localhost:3000 to see the new application running. The app will automatically recompile and reload when you change any of the source files.

When you run nest new, Nest generates a boilerplate application structure by creating a new folder and populating an initial set of files. You can continue working in this default structure, adding new components, as described throughout this documentation. We refer to the project structure generated by nest new as standard mode. Nest also supports an alternate structure for managing multiple projects and libraries called monorepo mode.

Aside from a few specific considerations around how the build process works (essentially, monorepo mode simplifies build complexities that can sometimes arise from monorepo-style project structures), and built-in library support, the rest of the Nest features, and this documentation, apply equally to both standard and monorepo mode project structures. In fact, you can easily switch from standard mode to monorepo mode at any time in the future, so you can safely defer this decision while you're still learning about Nest.

You can use either mode to manage multiple projects. Here's a quick summary of the differences:

Read the sections on Workspaces and Libraries for more detailed information to help you decide which mode is most suitable for you.

Learn the right way! 80+ chapters 5+ hours of videos Official certificate Deep-dive sessions Explore official courses

All nest commands follow the same format:

Here, new is the commandOrAlias. The new command has an alias of n. my-nest-project is the requiredArg. If a requiredArg is not supplied on the command line, nest will prompt for it. Also, --dry-run has an equivalent short-hand form -d. With this in mind, the following command is the equivalent of the above:

Most commands, and some options, have aliases. Try running nest new --help to see these options and aliases, and to confirm your understanding of the above constructs.

Run nest <command> --help for any of the following commands to see command-specific options.

See usage for detailed descriptions for each command.

Nest CLI requires a Node.js binary built with internationalization support (ICU), such as the official binaries from the Node.js project page. If you encounter errors related to ICU, check that your binary meets this requirement.

If the command prints undefined, your Node.js binary has no internationalization support.

**Examples:**

Example 1 (bash):
```bash
$ npm install -g @nestjs/cli
```

Example 2 (bash):
```bash
$ nest --help
```

Example 3 (bash):
```bash
$ nest generate --help
```

Example 4 (bash):
```bash
$ nest new my-nest-project
$ cd my-nest-project
$ npm run start:dev
```

---

## 

**URL:** https://docs.nestjs.com/

**Contents:**
  - Introduction
    - Philosophy#
    - Installation#
    - Alternatives#

Nest (NestJS) is a framework for building efficient, scalable Node.js server-side applications. It uses progressive JavaScript, is built with and fully supports TypeScript (yet still enables developers to code in pure JavaScript) and combines elements of OOP (Object Oriented Programming), FP (Functional Programming), and FRP (Functional Reactive Programming).

Under the hood, Nest makes use of robust HTTP Server frameworks like Express (the default) and optionally can be configured to use Fastify as well!

Nest provides a level of abstraction above these common Node.js frameworks (Express/Fastify), but also exposes their APIs directly to the developer. This gives developers the freedom to use the myriad of third-party modules which are available for the underlying platform.

In recent years, thanks to Node.js, JavaScript has become the “lingua franca” of the web for both front and backend applications. This has given rise to awesome projects like Angular, React and Vue, which improve developer productivity and enable the creation of fast, testable, and extensible frontend applications. However, while plenty of superb libraries, helpers, and tools exist for Node (and server-side JavaScript), none of them effectively solve the main problem of architecture.

Nest provides an out-of-the-box application architecture which allows developers and teams to create highly testable, scalable, loosely coupled, and easily maintainable applications. The architecture is heavily inspired by Angular.

To get started, you can either scaffold the project with the Nest CLI, or clone a starter project (both will produce the same outcome).

To scaffold the project with the Nest CLI, run the following commands. This will create a new project directory, and populate the directory with the initial core Nest files and supporting modules, creating a conventional base structure for your project. Creating a new project with the Nest CLI is recommended for first-time users. We'll continue with this approach in First Steps.

Alternatively, to install the TypeScript starter project with Git:

Open your browser and navigate to http://localhost:3000/.

To install the JavaScript flavor of the starter project, use javascript-starter.git in the command sequence above.

You can also start a new project from scratch by installing the core and supporting packages. Keep in mind that you'll need to set up the project boilerplate files on your own. At a minimum, you'll need these dependencies: @nestjs/core, @nestjs/common, rxjs, and reflect-metadata. Check out this short article on how to create a complete project: 5 steps to create a bare minimum NestJS app from scratch!.

**Examples:**

Example 1 (bash):
```bash
$ npm i -g @nestjs/cli
$ nest new project-name
```

Example 2 (bash):
```bash
$ git clone https://github.com/nestjs/typescript-starter.git project
$ cd project
$ npm install
$ npm run start
```

---

## 

**URL:** https://docs.nestjs.com/discover/companies

**Contents:**
  - Who is using Nest?
    - Companies#

We are proudly helping various companies building their products at scale. If you are using Nest and would you like to be listed here, see this thread. We are willing to put your logo here!

According to our knowledge, all the following companies have built awesome projects on top of our framework:

---

## 

**URL:** https://docs.nestjs.com/standalone-applications

**Contents:**
  - Standalone applications
    - Getting started#
    - Retrieving providers from static modules#
    - Retrieving providers from dynamic modules#
    - Terminating phase#
    - Example#

There are several ways of mounting a Nest application. You can create a web app, a microservice or just a bare Nest standalone application (without any network listeners). The Nest standalone application is a wrapper around the Nest IoC container, which holds all instantiated classes. We can obtain a reference to any existing instance from within any imported module directly using the standalone application object. Thus, you can take advantage of the Nest framework anywhere, including, for example, scripted CRON jobs. You can even build a CLI on top of it.

To create a Nest standalone application, use the following construction:

The standalone application object allows you to obtain a reference to any instance registered within the Nest application. Let's imagine that we have a TasksService provider in the TasksModule module that was imported by our AppModule module. This class provides a set of methods that we want to call from within a CRON job.

To access the TasksService instance we use the get() method. The get() method acts like a query that searches for an instance in each registered module. You can pass any provider's token to it. Alternatively, for strict context checking, pass an options object with the strict: true property. With this option in effect, you have to navigate through specific modules to obtain a particular instance from the selected context.

Following is a summary of the methods available for retrieving instance references from the standalone application object.

Keep in mind that a standalone application does not have any network listeners, so any Nest features related to HTTP (e.g., middleware, interceptors, pipes, guards, etc.) are not available in this context.

For example, even if you register a global interceptor in your application and then retrieve a controller's instance using the app.get() method, the interceptor will not be executed.

When dealing with dynamic modules, we should supply the same object that represents the registered dynamic module in the application to app.select. For example:

Then you can select that module later on:

If you want the Node application to close after the script finishes (e.g., for a script running CRON jobs), you must call the app.close() method in the end of your bootstrap function like this:

And as mentioned in the Lifecycle events chapter, that will trigger lifecycle hooks.

A working example is available here.

**Examples:**

Example 1 (typescript):
```typescript
async function bootstrap() {
  const app = await NestFactory.createApplicationContext(AppModule);
  // your application logic here ...
}
bootstrap();
```

Example 2 (typescript):
```typescript
const tasksService = app.get(TasksService);
```

Example 3 (typescript):
```typescript
const tasksService = app.select(TasksModule).get(TasksService, { strict: true });
```

Example 4 (typescript):
```typescript
export const dynamicConfigModule = ConfigModule.register({ folder: './config' });

@Module({
  imports: [dynamicConfigModule],
})
export class AppModule {}
```

---

## 

**URL:** https://docs.nestjs.com/faq/raw-body

**Contents:**
  - Raw body
    - Use with Express#
    - Registering a different parser#
    - Body parser size limit#
    - Use with Fastify#
    - Registering a different parser#
    - Body parser size limit#

One of the most common use-case for having access to the raw request body is performing webhook signature verifications. Usually to perform webhook signature validations the unserialized request body is required to calculate an HMAC hash.

First enable the option when creating your Nest Express application:

To access the raw request body in a controller, a convenience interface RawBodyRequest is provided to expose a rawBody field on the request: use the interface RawBodyRequest type:

By default, only json and urlencoded parsers are registered. If you want to register a different parser on the fly, you will need to do so explicitly.

For example, to register a text parser, you can use the following code:

If your application needs to parse a body larger than the default 100kb of Express, use the following:

The .useBodyParser method will respect the rawBody option that is passed in the application options.

First enable the option when creating your Nest Fastify application:

To access the raw request body in a controller, a convenience interface RawBodyRequest is provided to expose a rawBody field on the request: use the interface RawBodyRequest type:

By default, only application/json and application/x-www-form-urlencoded parsers are registered. If you want to register a different parser on the fly, you will need to do so explicitly.

For example, to register a text/plain parser, you can use the following code:

If your application needs to parse a body larger than the default 1MiB of Fastify, use the following:

The .useBodyParser method will respect the rawBody option that is passed in the application options.

**Examples:**

Example 1 (typescript):
```typescript
import { NestFactory } from '@nestjs/core';
import type { NestExpressApplication } from '@nestjs/platform-express';
import { AppModule } from './app.module';

// in the "bootstrap" function
const app = await NestFactory.create<NestExpressApplication>(AppModule, {
  rawBody: true,
});
await app.listen(process.env.PORT ?? 3000);
```

Example 2 (typescript):
```typescript
import { Controller, Post, RawBodyRequest, Req } from '@nestjs/common';
import { Request } from 'express';

@Controller('cats')
class CatsController {
  @Post()
  create(@Req() req: RawBodyRequest<Request>) {
    const raw = req.rawBody; // returns a `Buffer`.
  }
}
```

Example 3 (typescript):
```typescript
app.useBodyParser('text');
```

Example 4 (typescript):
```typescript
app.useBodyParser('json', { limit: '10mb' });
```

---

## 

**URL:** https://docs.nestjs.com/faq/multiple-servers

**Contents:**
  - HTTPS
    - Multiple simultaneous servers#

To create an application that uses the HTTPS protocol, set the httpsOptions property in the options object passed to the create() method of the NestFactory class:

If you use the FastifyAdapter, create the application as follows:

The following recipe shows how to instantiate a Nest application that listens on multiple ports (for example, on a non-HTTPS port and an HTTPS port) simultaneously.

Because we called http.createServer / https.createServer ourselves, NestJS doesn't close them when calling app.close / on termination signal. We need to do this ourselves:

**Examples:**

Example 1 (typescript):
```typescript
const httpsOptions = {
  key: fs.readFileSync('./secrets/private-key.pem'),
  cert: fs.readFileSync('./secrets/public-certificate.pem'),
};
const app = await NestFactory.create(AppModule, {
  httpsOptions,
});
await app.listen(process.env.PORT ?? 3000);
```

Example 2 (typescript):
```typescript
const app = await NestFactory.create<NestFastifyApplication>(
  AppModule,
  new FastifyAdapter({ https: httpsOptions }),
);
```

Example 3 (typescript):
```typescript
const httpsOptions = {
  key: fs.readFileSync('./secrets/private-key.pem'),
  cert: fs.readFileSync('./secrets/public-certificate.pem'),
};

const server = express();
const app = await NestFactory.create(AppModule, new ExpressAdapter(server));
await app.init();

const httpServer = http.createServer(server).listen(3000);
const httpsServer = https.createServer(httpsOptions, server).listen(443);
```

Example 4 (typescript):
```typescript
@Injectable()
export class ShutdownObserver implements OnApplicationShutdown {
  private httpServers: http.Server[] = [];

  public addHttpServer(server: http.Server): void {
    this.httpServers.push(server);
  }

  public async onApplicationShutdown(): Promise<void> {
    await Promise.all(
      this.httpServers.map(
        (server) =>
          new Promise((resolve, reject) => {
            server.close((error) => {
              if (error) {
                reject(error);
              } else {
                resolve(null);
              }
            });
          }),
      ),
    );
  }
}

const shutdownObserver = app.get(ShutdownObserver);
shutdownObserver.addHttpServer(httpServer);
shutdownObserver.addHttpServer(httpsServer);
```

---
