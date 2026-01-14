# Nestjs - Recipes

**Pages:** 11

---

## 

**URL:** https://docs.nestjs.com/recipes/swc

**Contents:**
  - SWC
    - Installation#
    - Getting started#
    - Type checking#
    - CLI Plugins (SWC)#
    - SWC configuration#
    - Monorepo#
    - Monorepo and CLI plugins#
    - Common pitfalls#
  - Jest + SWC

SWC (Speedy Web Compiler) is an extensible Rust-based platform that can be used for both compilation and bundling. Using SWC with Nest CLI is a great and simple way to significantly speed up your development process.

To get started, first install a few packages:

Once the installation process is complete, you can use the swc builder with Nest CLI, as follows:

Instead of passing the -b flag you can also just set the compilerOptions.builder property to "swc" in your nest-cli.json file, like so:

To customize builder's behavior, you can pass an object containing two attributes, type ("swc") and options, as follows:

For example, to make the swc compile .jsx and .tsx files, do:

To run the application in watch mode, use the following command:

SWC does not perform any type checking itself (as opposed to the default TypeScript compiler), so to turn it on, you need to use the --type-check flag:

This command will instruct the Nest CLI to run tsc in noEmit mode alongside SWC, which will asynchronously perform type checking. Again, instead of passing the --type-check flag you can also just set the compilerOptions.typeCheck property to true in your nest-cli.json file, like so:

The --type-check flag will automatically execute NestJS CLI plugins and produce a serialized metadata file which then can be loaded by the application at runtime.

SWC builder is pre-configured to match the requirements of NestJS applications. However, you can customize the configuration by creating a .swcrc file in the root directory and tweaking the options as you wish.

If your repository is a monorepo, then instead of using swc builder you have to configure webpack to use swc-loader.

First, let's install the required package:

Once the installation is complete, create a webpack.config.js file in the root directory of your application with the following content:

Now if you use CLI plugins, swc-loader will not load them automatically. Instead, you have to create a separate file that will load them manually. To do so, declare a generate-metadata.ts file near the main.ts file with the following content:

The generate() method accepts the following options:

Finally, you can run the generate-metadata script in a separate terminal window with the following command:

If you use TypeORM/MikroORM or any other ORM in your application, you may stumble upon circular import issues. SWC doesn't handle circular imports well, so you should use the following workaround:

Doing this prevents the type of the property from being saved in the transpiled code in the property metadata, preventing circular dependency issues.

If your ORM does not provide a similar workaround, you can define the wrapper type yourself:

For all circular dependency injections in your project, you will also need to use the custom wrapper type described above:

To use SWC with Jest, you need to install the following packages:

Once the installation is complete, update the package.json/jest.config.js file (depending on your configuration) with the following content:

Additionally you would need to add the following transform properties to your .swcrc file: legacyDecorator, decoratorMetadata:

If you use NestJS CLI Plugins in your project, you'll have to run PluginMetadataGenerator manually. Navigate to this section to learn more.

Vitest is a fast and lightweight test runner designed to work with Vite. It provides a modern, fast, and easy-to-use testing solution that can be integrated with NestJS projects.

To get started, first install the required packages:

Create a vitest.config.ts file in the root directory of your application with the following content:

This configuration file sets up the Vitest environment, root directory, and SWC plugin. You should also create a separate configuration file for e2e tests, with an additional include field that specifies the test path regex:

Additionally, you can set the alias options to support TypeScript paths in your tests:

Unlike Jest, Vitest does not automatically resolve TypeScript path aliases like src/. This may lead to dependency resolution errors during testing. To resolve this issue, add the following resolve.alias configuration in your vitest.config.ts file:

This ensures that Vitest correctly resolves module imports, preventing errors related to missing dependencies.

Change any E2E test imports using import * as request from 'supertest' to import request from 'supertest'. This is necessary because Vitest, when bundled with Vite, expects a default import for supertest. Using a namespace import may cause issues in this specific setup.

Lastly, update the test scripts in your package.json file to the following:

These scripts configure Vitest for running tests, watching for changes, generating code coverage reports, and debugging. The test:e2e script is specifically for running E2E tests with a custom configuration file.

With this setup, you can now enjoy the benefits of using Vitest in your NestJS project, including faster test execution and a more modern testing experience.

**Examples:**

Example 1 (bash):
```bash
$ npm i --save-dev @swc/cli @swc/core
```

Example 2 (bash):
```bash
$ nest start -b swc
# OR nest start --builder swc
```

Example 3 (json):
```json
{
  "compilerOptions": {
    "builder": "swc"
  }
}
```

Example 4 (json):
```json
{
  "compilerOptions": {
    "builder": {
      "type": "swc",
      "options": {
        "swcrcPath": "infrastructure/.swcrc",
      }
    }
  }
}
```

---

## 

**URL:** https://docs.nestjs.com/recipes/passport

**Contents:**
  - Passport (authentication)
    - Authentication requirements#
    - Implementing Passport strategies#
    - Implementing Passport local#
    - Built-in Passport Guards#
- Learn the right way!
    - Login route#
    - Logout route#
    - JWT functionality#
    - Implementing Passport JWT#

Passport is the most popular node.js authentication library, well-known by the community and successfully used in many production applications. It's straightforward to integrate this library with a Nest application using the @nestjs/passport module. At a high level, Passport executes a series of steps to:

Passport has a rich ecosystem of strategies that implement various authentication mechanisms. While simple in concept, the set of Passport strategies you can choose from is large and presents a lot of variety. Passport abstracts these varied steps into a standard pattern, and the @nestjs/passport module wraps and standardizes this pattern into familiar Nest constructs.

In this chapter, we'll implement a complete end-to-end authentication solution for a RESTful API server using these powerful and flexible modules. You can use the concepts described here to implement any Passport strategy to customize your authentication scheme. You can follow the steps in this chapter to build this complete example.

Let's flesh out our requirements. For this use case, clients will start by authenticating with a username and password. Once authenticated, the server will issue a JWT that can be sent as a bearer token in an authorization header on subsequent requests to prove authentication. We'll also create a protected route that is accessible only to requests that contain a valid JWT.

We'll start with the first requirement: authenticating a user. We'll then extend that by issuing a JWT. Finally, we'll create a protected route that checks for a valid JWT on the request.

First we need to install the required packages. Passport provides a strategy called passport-local that implements a username/password authentication mechanism, which suits our needs for this portion of our use case.

We're now ready to implement the authentication feature. We'll start with an overview of the process used for any Passport strategy. It's helpful to think of Passport as a mini framework in itself. The elegance of the framework is that it abstracts the authentication process into a few basic steps that you customize based on the strategy you're implementing. It's like a framework because you configure it by supplying customization parameters (as plain JSON objects) and custom code in the form of callback functions, which Passport calls at the appropriate time. The @nestjs/passport module wraps this framework in a Nest style package, making it easy to integrate into a Nest application. We'll use @nestjs/passport below, but first let's consider how vanilla Passport works.

In vanilla Passport, you configure a strategy by providing two things:

With @nestjs/passport, you configure a Passport strategy by extending the PassportStrategy class. You pass the strategy options (item 1 above) by calling the super() method in your subclass, optionally passing in an options object. You provide the verify callback (item 2 above) by implementing a validate() method in your subclass.

We'll start by generating an AuthModule and in it, an AuthService:

As we implement the AuthService, we'll find it useful to encapsulate user operations in a UsersService, so let's generate that module and service now:

Replace the default contents of these generated files as shown below. For our sample app, the UsersService simply maintains a hard-coded in-memory list of users, and a find method to retrieve one by username. In a real app, this is where you'd build your user model and persistence layer, using your library of choice (e.g., TypeORM, Sequelize, Mongoose, etc.).

In the UsersModule, the only change needed is to add the UsersService to the exports array of the @Module decorator so that it is visible outside this module (we'll soon use it in our AuthService).

Our AuthService has the job of retrieving a user and verifying the password. We create a validateUser() method for this purpose. In the code below, we use a convenient ES6 spread operator to strip the password property from the user object before returning it. We'll be calling into the validateUser() method from our Passport local strategy in a moment.

Now, we update our AuthModule to import the UsersModule.

Now we can implement our Passport local authentication strategy. Create a file called local.strategy.ts in the auth folder, and add the following code:

We've followed the recipe described earlier for all Passport strategies. In our use case with passport-local, there are no configuration options, so our constructor simply calls super(), without an options object.

We've also implemented the validate() method. For each strategy, Passport will call the verify function (implemented with the validate() method in @nestjs/passport) using an appropriate strategy-specific set of parameters. For the local-strategy, Passport expects a validate() method with the following signature: validate(username: string, password:string): any.

Most of the validation work is done in our AuthService (with the help of our UsersService), so this method is quite straightforward. The validate() method for any Passport strategy will follow a similar pattern, varying only in the details of how credentials are represented. If a user is found and the credentials are valid, the user is returned so Passport can complete its tasks (e.g., creating the user property on the Request object), and the request handling pipeline can continue. If it's not found, we throw an exception and let our exceptions layer handle it.

Typically, the only significant difference in the validate() method for each strategy is how you determine if a user exists and is valid. For example, in a JWT strategy, depending on requirements, we may evaluate whether the userId carried in the decoded token matches a record in our user database, or matches a list of revoked tokens. Hence, this pattern of sub-classing and implementing strategy-specific validation is consistent, elegant and extensible.

We need to configure our AuthModule to use the Passport features we just defined. Update auth.module.ts to look like this:

The Guards chapter describes the primary function of Guards: to determine whether a request will be handled by the route handler or not. That remains true, and we'll use that standard capability soon. However, in the context of using the @nestjs/passport module, we will also introduce a slight new wrinkle that may at first be confusing, so let's discuss that now. Consider that your app can exist in two states, from an authentication perspective:

In the first case (user is not logged in), we need to perform two distinct functions:

Restrict the routes an unauthenticated user can access (i.e., deny access to restricted routes). We'll use Guards in their familiar capacity to handle this function, by placing a Guard on the protected routes. As you may anticipate, we'll be checking for the presence of a valid JWT in this Guard, so we'll work on this Guard later, once we are successfully issuing JWTs.

Initiate the authentication step itself when a previously unauthenticated user attempts to login. This is the step where we'll issue a JWT to a valid user. Thinking about this for a moment, we know we'll need to POST username/password credentials to initiate authentication, so we'll set up a POST /auth/login route to handle that. This raises the question: how exactly do we invoke the passport-local strategy in that route?

The answer is straightforward: by using another, slightly different type of Guard. The @nestjs/passport module provides us with a built-in Guard that does this for us. This Guard invokes the Passport strategy and kicks off the steps described above (retrieving credentials, running the verify function, creating the user property, etc).

The second case enumerated above (logged in user) simply relies on the standard type of Guard we already discussed to enable access to protected routes for logged in users.

Learn the right way! 19 chapters Authn & Authz Official certificate Deep-dive sessions Purchase the Authentication course

With the strategy in place, we can now implement a bare-bones /auth/login route, and apply the built-in Guard to initiate the passport-local flow.

Open the app.controller.ts file and replace its contents with the following:

With @UseGuards(AuthGuard('local')) we are using an AuthGuard that @nestjs/passportautomatically provisioned for us when we extended the passport-local strategy. Let's break that down. Our Passport local strategy has a default name of 'local'. We reference that name in the @UseGuards() decorator to associate it with code supplied by the passport-local package. This is used to disambiguate which strategy to invoke in case we have multiple Passport strategies in our app (each of which may provision a strategy-specific AuthGuard). While we only have one such strategy so far, we'll shortly add a second, so this is needed for disambiguation.

In order to test our route we'll have our /auth/login route simply return the user for now. This also lets us demonstrate another Passport feature: Passport automatically creates a user object, based on the value we return from the validate() method, and assigns it to the Request object as req.user. Later, we'll replace this with code to create and return a JWT instead.

Since these are API routes, we'll test them using the commonly available cURL library. You can test with any of the user objects hard-coded in the UsersService.

While this works, passing the strategy name directly to the AuthGuard() introduces magic strings in the codebase. Instead, we recommend creating your own class, as shown below:

Now, we can update the /auth/login route handler and use the LocalAuthGuard instead:

To log out, we can create an additional route that invokes req.logout() to clear the user's session. This is a typical approach used in session-based authentication, but it does not apply to JWTs.

We're ready to move on to the JWT portion of our auth system. Let's review and refine our requirements:

We'll need to install a couple more packages to support our JWT requirements:

The @nestjs/jwt package (see more here) is a utility package that helps with JWT manipulation. The passport-jwt package is the Passport package that implements the JWT strategy and @types/passport-jwt provides the TypeScript type definitions.

Let's take a closer look at how a POST /auth/login request is handled. We've decorated the route using the built-in AuthGuard provided by the passport-local strategy. This means that:

With this in mind, we can now finally generate a real JWT, and return it in this route. To keep our services cleanly modularized, we'll handle generating the JWT in the authService. Open the auth.service.ts file in the auth folder, and add the login() method, and import the JwtService as shown:

We're using the @nestjs/jwt library, which supplies a sign() function to generate our JWT from a subset of the user object properties, which we then return as a simple object with a single access_token property. Note: we choose a property name of sub to hold our userId value to be consistent with JWT standards. Don't forget to inject the JwtService provider into the AuthService.

We now need to update the AuthModule to import the new dependencies and configure the JwtModule.

First, create constants.ts in the auth folder, and add the following code:

We'll use this to share our key between the JWT signing and verifying steps.

Now, open auth.module.ts in the auth folder and update it to look like this:

We configure the JwtModule using register(), passing in a configuration object. See here for more on the Nest JwtModule and here for more details on the available configuration options.

Now we can update the /auth/login route to return a JWT.

Let's go ahead and test our routes using cURL again. You can test with any of the user objects hard-coded in the UsersService.

We can now address our final requirement: protecting endpoints by requiring a valid JWT be present on the request. Passport can help us here too. It provides the passport-jwt strategy for securing RESTful endpoints with JSON Web Tokens. Start by creating a file called jwt.strategy.ts in the auth folder, and add the following code:

With our JwtStrategy, we've followed the same recipe described earlier for all Passport strategies. This strategy requires some initialization, so we do that by passing in an options object in the super() call. You can read more about the available options here. In our case, these options are:

The validate() method deserves some discussion. For the jwt-strategy, Passport first verifies the JWT's signature and decodes the JSON. It then invokes our validate() method passing the decoded JSON as its single parameter. Based on the way JWT signing works, we're guaranteed that we're receiving a valid token that we have previously signed and issued to a valid user.

As a result of all this, our response to the validate() callback is trivial: we simply return an object containing the userId and username properties. Recall again that Passport will build a user object based on the return value of our validate() method, and attach it as a property on the Request object.

Additionally, you can return an array, where the first value is used to create a user object and the second value is used to create an authInfo object.

It's also worth pointing out that this approach leaves us room ('hooks' as it were) to inject other business logic into the process. For example, we could do a database lookup in our validate() method to extract more information about the user, resulting in a more enriched user object being available in our Request. This is also the place we may decide to do further token validation, such as looking up the userId in a list of revoked tokens, enabling us to perform token revocation. The model we've implemented here in our sample code is a fast, "stateless JWT" model, where each API call is immediately authorized based on the presence of a valid JWT, and a small bit of information about the requester (its userId and username) is available in our Request pipeline.

Add the new JwtStrategy as a provider in the AuthModule:

By importing the same secret used when we signed the JWT, we ensure that the verify phase performed by Passport, and the sign phase performed in our AuthService, use a common secret.

Finally, we define the JwtAuthGuard class which extends the built-in AuthGuard:

We can now implement our protected route and its associated Guard.

Open the app.controller.ts file and update it as shown below:

Once again, we're applying the AuthGuard that the @nestjs/passport module has automatically provisioned for us when we configured the passport-jwt module. This Guard is referenced by its default name, jwt. When our GET /profile route is hit, the Guard will automatically invoke our passport-jwt custom configured strategy, validate the JWT, and assign the user property to the Request object.

Ensure the app is running, and test the routes using cURL.

Note that in the AuthModule, we configured the JWT to have an expiration of 60 seconds. This is probably too short an expiration, and dealing with the details of token expiration and refresh is beyond the scope of this article. However, we chose that to demonstrate an important quality of JWTs and the passport-jwt strategy. If you wait 60 seconds after authenticating before attempting a GET /profile request, you'll receive a 401 Unauthorized response. This is because Passport automatically checks the JWT for its expiration time, saving you the trouble of doing so in your application.

We've now completed our JWT authentication implementation. JavaScript clients (such as Angular/React/Vue), and other JavaScript apps, can now authenticate and communicate securely with our API Server.

In most cases, using a provided AuthGuard class is sufficient. However, there might be use-cases when you would like to simply extend the default error handling or authentication logic. For this, you can extend the built-in class and override methods within a sub-class.

In addition to extending the default error handling and authentication logic, we can allow authentication to go through a chain of strategies. The first strategy to succeed, redirect, or error will halt the chain. Authentication failures will proceed through each strategy in series, ultimately failing if all strategies fail.

If the vast majority of your endpoints should be protected by default, you can register the authentication guard as a global guard and instead of using @UseGuards() decorator on top of each controller, you could simply flag which routes should be public.

First, register the JwtAuthGuard as a global guard using the following construction (in any module):

With this in place, Nest will automatically bind JwtAuthGuard to all endpoints.

Now we must provide a mechanism for declaring routes as public. For this, we can create a custom decorator using the SetMetadata decorator factory function.

In the file above, we exported two constants. One being our metadata key named IS_PUBLIC_KEY, and the other being our new decorator itself that we’re going to call Public (you can alternatively name it SkipAuth or AllowAnon, whatever fits your project).

Now that we have a custom @Public() decorator, we can use it to decorate any method, as follows:

Lastly, we need the JwtAuthGuard to return true when the "isPublic" metadata is found. For this, we'll use the Reflector class (read more here).

The passport API is based on registering strategies to the global instance of the library. Therefore strategies are not designed to have request-dependent options or to be dynamically instantiated per request (read more about the request-scoped providers). When you configure your strategy to be request-scoped, Nest will never instantiate it since it's not tied to any specific route. There is no physical way to determine which "request-scoped" strategies should be executed per request.

However, there are ways to dynamically resolve request-scoped providers within the strategy. For this, we leverage the module reference feature.

First, open the local.strategy.ts file and inject the ModuleRef in the normal way:

Be sure to set the passReqToCallback configuration property to true, as shown above.

In the next step, the request instance will be used to obtain the current context identifier, instead of generating a new one (read more about request context here).

Now, inside the validate() method of the LocalStrategy class, use the getByRequest() method of the ContextIdFactory class to create a context id based on the request object, and pass this to the resolve() call:

In the example above, the resolve() method will asynchronously return the request-scoped instance of the AuthService provider (we assumed that AuthService is marked as a request-scoped provider).

Any standard Passport customization options can be passed the same way, using the register() method. The available options depend on the strategy being implemented. For example:

You can also pass strategies an options object in their constructors to configure them. For the local strategy you can pass e.g.:

Take a look at the official Passport Website for property names.

When implementing a strategy, you can provide a name for it by passing a second argument to the PassportStrategy function. If you don't do this, each strategy will have a default name (e.g., 'jwt' for jwt-strategy):

Then, you refer to this via a decorator like @UseGuards(AuthGuard('myjwt')).

In order to use an AuthGuard with GraphQL, extend the built-in AuthGuard class and override the getRequest() method.

To get the current authenticated user in your graphql resolver, you can define a @CurrentUser() decorator:

To use above decorator in your resolver, be sure to include it as a parameter of your query or mutation:

For the passport-local strategy, you'll also need to add the GraphQL context's arguments to the request body so Passport can access them for validation. Otherwise, you'll get an Unauthorized error.

**Examples:**

Example 1 (bash):
```bash
$ npm install --save @nestjs/passport passport passport-local
$ npm install --save-dev @types/passport-local
```

Example 2 (bash):
```bash
$ nest g module auth
$ nest g service auth
```

Example 3 (bash):
```bash
$ nest g module users
$ nest g service users
```

Example 4 (typescript):
```typescript
import { Injectable } from '@nestjs/common';

// This should be a real class/interface representing a user entity
export type User = any;

@Injectable()
export class UsersService {
  private readonly users = [
    {
      userId: 1,
      username: 'john',
      password: 'changeme',
    },
    {
      userId: 2,
      username: 'maria',
      password: 'guess',
    },
  ];

  async findOne(username: string): Promise<User | undefined> {
    return this.users.find(user => user.username === username);
  }
}
```

---

## 

**URL:** https://docs.nestjs.com/recipes/async-local-storage

**Contents:**
  - Async Local Storage
    - Custom implementation#
  - NestJS CLS
    - Installation#
    - Usage#
    - Testing#
    - More information#

AsyncLocalStorage is a Node.js API (based on the async_hooks API) that provides an alternative way of propagating local state through the application without the need to explicitly pass it as a function parameter. It is similar to a thread-local storage in other languages.

The main idea of Async Local Storage is that we can wrap some function call with the AsyncLocalStorage#run call. All code that is invoked within the wrapped call gets access to the same store, which will be unique to each call chain.

In the context of NestJS, that means if we can find a place within the request's lifecycle where we can wrap the rest of the request's code, we will be able to access and modify state visible only to that request, which may serve as an alternative to REQUEST-scoped providers and some of their limitations.

Alternatively, we can use ALS to propagate context for only a part of the system (for example the transaction object) without passing it around explicitly across services, which can increase isolation and encapsulation.

NestJS itself does not provide any built-in abstraction for AsyncLocalStorage, so let's walk through how we could implement it ourselves for the simplest HTTP case to get a better understanding of the whole concept:

The nestjs-cls package provides several DX improvements over using plain AsyncLocalStorage (CLS is an abbreviation of the term continuation-local storage). It abstracts the implementation into a ClsModule that offers various ways of initializing the store for different transports (not only HTTP), as well as a strong-typing support.

The store can then be accessed with an injectable ClsService, or entirely abstracted away from the business logic by using Proxy Providers.

Apart from a peer dependency on the @nestjs libs, it only uses the built-in Node.js API. Install it as any other package.

A similar functionality as described above can be implemented using nestjs-cls as follows:

Since the ClsService is just another injectable provider, it can be entirely mocked out in unit tests.

However, in certain integration tests, we might still want to use the real ClsService implementation. In that case, we will need to wrap the context-aware piece of code with a call to ClsService#run or ClsService#runWith.

Visit the NestJS CLS GitHub Page for the full API documentation and more code examples.

**Examples:**

Example 1 (json):
```json
@Module({
  providers: [
    {
      provide: AsyncLocalStorage,
      useValue: new AsyncLocalStorage(),
    },
  ],
  exports: [AsyncLocalStorage],
})
export class AlsModule {}
```

Example 2 (typescript):
```typescript
@Module({
  imports: [AlsModule],
  providers: [CatsService],
  controllers: [CatsController],
})
export class AppModule implements NestModule {
  constructor(
    // inject the AsyncLocalStorage in the module constructor,
    private readonly als: AsyncLocalStorage
  ) {}

  configure(consumer: MiddlewareConsumer) {
    // bind the middleware,
    consumer
      .apply((req, res, next) => {
        // populate the store with some default values
        // based on the request,
        const store = {
          userId: req.headers['x-user-id'],
        };
        // and pass the "next" function as callback
        // to the "als.run" method together with the store.
        this.als.run(store, () => next());
      })
      .forRoutes('*path');
  }
}
```

Example 3 (typescript):
```typescript
@Module({
  imports: [AlsModule],
  providers: [CatsService],
  controllers: [CatsController],
})
@Dependencies(AsyncLocalStorage)
export class AppModule {
  constructor(als) {
    // inject the AsyncLocalStorage in the module constructor,
    this.als = als
  }

  configure(consumer) {
    // bind the middleware,
    consumer
      .apply((req, res, next) => {
        // populate the store with some default values
        // based on the request,
        const store = {
          userId: req.headers['x-user-id'],
        };
        // and pass the "next" function as callback
        // to the "als.run" method together with the store.
        this.als.run(store, () => next());
      })
      .forRoutes('*path');
  }
}
```

Example 4 (typescript):
```typescript
@Injectable()
export class CatsService {
  constructor(
    // We can inject the provided ALS instance.
    private readonly als: AsyncLocalStorage,
    private readonly catsRepository: CatsRepository,
  ) {}

  getCatForUser() {
    // The "getStore" method will always return the
    // store instance associated with the given request.
    const userId = this.als.getStore()["userId"] as number;
    return this.catsRepository.getForUser(userId);
  }
}
```

---

## 

**URL:** https://docs.nestjs.com/recipes/router-module

**Contents:**
  - Router module

In an HTTP application (for example, REST API), the route path for a handler is determined by concatenating the (optional) prefix declared for the controller (inside the @Controller decorator), and any path specified in the method's decorator (e.g, @Get('users')). You can learn more about that in this section. Additionally, you can define a global prefix for all routes registered in your application, or enable versioning.

Also, there are edge-cases when defining a prefix at a module-level (and so for all controllers registered inside that module) may come in handy. For example, imagine a REST application that exposes several different endpoints being used by a specific portion of your application called "Dashboard". In such a case, instead of repeating the /dashboard prefix within each controller, you could use a utility RouterModule module, as follows:

In addition, you can define hierarchical structures. This means each module can have children modules. The children modules will inherit their parent's prefix. In the following example, we'll register the AdminModule as a parent module of DashboardModule and MetricsModule.

In the example above, any controller registered inside the DashboardModule will have an extra /admin/dashboard prefix (as the module concatenates paths from top to bottom - recursively - parent to children). Likewise, each controller defined inside the MetricsModule will have an additional module-level prefix /admin/metrics.

**Examples:**

Example 1 (typescript):
```typescript
@Module({
  imports: [
    DashboardModule,
    RouterModule.register([
      {
        path: 'dashboard',
        module: DashboardModule,
      },
    ]),
  ],
})
export class AppModule {}
```

Example 2 (typescript):
```typescript
@Module({
  imports: [
    AdminModule,
    DashboardModule,
    MetricsModule,
    RouterModule.register([
      {
        path: 'admin',
        module: AdminModule,
        children: [
          {
            path: 'dashboard',
            module: DashboardModule,
          },
          {
            path: 'metrics',
            module: MetricsModule,
          },
        ],
      },
    ])
  ],
});
```

---

## 

**URL:** https://docs.nestjs.com/recipes/automock

**Contents:**
  - Suites
    - Getting started#
    - Install Suites#
    - Set up type definitions#
    - Create a sample service#
    - Write a unit test#
    - Pre-compile mock configuration#
    - Testing with real dependencies#
    - Token-based dependencies#
    - Using mock() and stub() directly#

Suites is an open-source unit-testing framework for TypeScript dependency injection frameworks. It is used as an alternative to manually creating mocks, verbose test setup with multiple mock configurations, or working with untyped test doubles (like mocks and stubs).

Suites reads metadata from nestjs services at runtime and automatically generates fully-typed mocks for all dependencies. This removes boilerplate mock setup and ensures type-safe tests. While Suites can be used alongside Test.createTestingModule(), it excels at focused unit testing. Use Test.createTestingModule() when validating module wiring, decorators, guards, and interceptors. Use Suites for fast unit tests with automatic mock generation.

For more information on module-based testing, see the testing fundamentals chapter.

This guide demonstrates using Suites to test NestJS services. It covers both isolated testing (all dependencies mocked) and sociable testing (selected real implementations).

Verify NestJS runtime dependencies are installed:

Install Suites core, the NestJS adapter, and the doubles adapter:

The doubles adapter (@suites/doubles.jest) provides wrappers around Jest's mocking capabilities. It exposes mock() and stub() functions that create type-safe test doubles.

Ensure Jest and TypeScript are available:

Create global.d.ts at your project root:

This guide uses a simple UserService with two dependencies:

Use TestBed.solitary() to create isolated tests with all dependencies mocked:

TestBed.solitary() analyzes the constructor and creates typed mocks for all dependencies. The Mocked<T> type provides IntelliSense support for mock configuration.

Configure mock behavior before compilation using .mock().impl():

The stubFn parameter corresponds to the installed doubles adapter (jest.fn() for Jest, vi.fn() for Vitest, sinon.stub() for Sinon).

Use TestBed.sociable() with .expose() to use real implementations for specific dependencies:

.expose(Logger) instantiates Logger with its real implementation while keeping other dependencies mocked.

Suites handles custom injection tokens (strings or symbols):

Access token-based dependencies with unitRef.get():

For those who prefer direct control without TestBed, the doubles adapter package provides mock() and stub() functions:

mock() creates a typed mock object, and stub() wraps the underlying mocking library (Jest in this example) to provide methods like mockResolvedValue() These functions come from the installed doubles adapter (@suites/doubles.jest), which adapts the native mocking capabilities of the test framework.

Use Test.createTestingModule() for:

Organize tests by purpose: use Suites for unit tests verifying individual service behavior, and use Test.createTestingModule() for integration tests verifying module configuration.

For more information:

**Examples:**

Example 1 (bash):
```bash
$ npm install @nestjs/common @nestjs/core reflect-metadata
```

Example 2 (bash):
```bash
$ npm install --save-dev @suites/unit @suites/di.nestjs @suites/doubles.jest
```

Example 3 (bash):
```bash
$ npm install --save-dev ts-jest @types/jest jest typescript
```

Example 4 (bash):
```bash
$ npm install --save-dev @suites/unit @suites/di.nestjs @suites/doubles.vitest
```

---

## 

**URL:** https://docs.nestjs.com/recipes/health-checks

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

**URL:** https://docs.nestjs.com/recipes/hot-reload

**Contents:**
  - Hot Reload
  - With CLI
    - Installation#
    - Configuration#
    - Hot-Module Replacement#
  - Without CLI
    - Installation#
    - Configuration#
    - Hot-Module Replacement#
    - Example#

The highest impact on your application's bootstrapping process is TypeScript compilation. Fortunately, with webpack HMR (Hot-Module Replacement), we don't need to recompile the entire project each time a change occurs. This significantly decreases the amount of time necessary to instantiate your application, and makes iterative development a lot easier.

If you are using the Nest CLI, the configuration process is pretty straightforward. The CLI wraps webpack, which allows use of the HotModuleReplacementPlugin.

First install the required packages:

Once the installation is complete, create a webpack-hmr.config.js file in the root directory of your application.

This function takes the original object containing the default webpack configuration as a first argument, and the reference to the underlying webpack package used by the Nest CLI as the second one. Also, it returns a modified webpack configuration with the HotModuleReplacementPlugin, WatchIgnorePlugin, and RunScriptWebpackPlugin plugins.

To enable HMR, open the application entry file (main.ts) and add the following webpack-related instructions:

To simplify the execution process, add a script to your package.json file.

Now simply open your command line and run the following command:

If you are not using the Nest CLI, the configuration will be slightly more complex (will require more manual steps).

First install the required packages:

Once the installation is complete, create a webpack.config.js file in the root directory of your application.

This configuration tells webpack a few essential things about your application: location of the entry file, which directory should be used to hold compiled files, and what kind of loader we want to use to compile source files. Generally, you should be able to use this file as-is, even if you don't fully understand all of the options.

To enable HMR, open the application entry file (main.ts) and add the following webpack-related instructions:

To simplify the execution process, add a script to your package.json file.

Now simply open your command line and run the following command:

A working example is available here.

**Examples:**

Example 1 (bash):
```bash
$ npm i --save-dev webpack-node-externals run-script-webpack-plugin webpack
```

Example 2 (typescript):
```typescript
const nodeExternals = require('webpack-node-externals');
const { RunScriptWebpackPlugin } = require('run-script-webpack-plugin');

module.exports = function (options, webpack) {
  return {
    ...options,
    entry: ['webpack/hot/poll?100', options.entry],
    externals: [
      nodeExternals({
        allowlist: ['webpack/hot/poll?100'],
      }),
    ],
    plugins: [
      ...options.plugins,
      new webpack.HotModuleReplacementPlugin(),
      new webpack.WatchIgnorePlugin({
        paths: [/\.js$/, /\.d\.ts$/],
      }),
      new RunScriptWebpackPlugin({ name: options.output.filename, autoRestart: false }),
    ],
  };
};
```

Example 3 (typescript):
```typescript
declare const module: any;

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(process.env.PORT ?? 3000);

  if (module.hot) {
    module.hot.accept();
    module.hot.dispose(() => app.close());
  }
}
bootstrap();
```

Example 4 (json):
```json
"start:dev": "nest build --webpack --webpackPath webpack-hmr.config.js --watch"
```

---

## 

**URL:** https://docs.nestjs.com/recipes/sql-typeorm

**Contents:**
  - SQL (TypeORM)
      - This chapter applies only to TypeScript
    - Getting started#
    - Repository pattern#

TypeORM is definitely the most mature Object Relational Mapper (ORM) available in the node.js world. Since it's written in TypeScript, it works pretty well with the Nest framework.

To start the adventure with this library we have to install all required dependencies:

The first step we need to do is to establish the connection with our database using new DataSource().initialize() class imported from the typeorm package. The initialize() function returns a Promise, and therefore we have to create an async provider.

Then, we need to export these providers to make them accessible for the rest of the application.

Now we can inject the DATA_SOURCE object using @Inject() decorator. Each class that would depend on the DATA_SOURCE async provider will wait until a Promise is resolved.

The TypeORM supports the repository design pattern, thus each entity has its own Repository. These repositories can be obtained from the database connection.

But firstly, we need at least one entity. We are going to reuse the Photo entity from the official documentation.

The Photo entity belongs to the photo directory. This directory represents the PhotoModule. Now, let's create a Repository provider:

Now we can inject the Repository<Photo> to the PhotoService using the @Inject() decorator:

The database connection is asynchronous, but Nest makes this process completely invisible for the end-user. The PhotoRepository is waiting for the db connection, and the PhotoService is delayed until repository is ready to use. The entire application can start when each class is instantiated.

Here is a final PhotoModule:

**Examples:**

Example 1 (bash):
```bash
$ npm install --save typeorm mysql2
```

Example 2 (typescript):
```typescript
import { DataSource } from 'typeorm';

export const databaseProviders = [
  {
    provide: 'DATA_SOURCE',
    useFactory: async () => {
      const dataSource = new DataSource({
        type: 'mysql',
        host: 'localhost',
        port: 3306,
        username: 'root',
        password: 'root',
        database: 'test',
        entities: [
            __dirname + '/../**/*.entity{.ts,.js}',
        ],
        synchronize: true,
      });

      return dataSource.initialize();
    },
  },
];
```

Example 3 (typescript):
```typescript
import { Module } from '@nestjs/common';
import { databaseProviders } from './database.providers';

@Module({
  providers: [...databaseProviders],
  exports: [...databaseProviders],
})
export class DatabaseModule {}
```

Example 4 (typescript):
```typescript
import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class Photo {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ length: 500 })
  name: string;

  @Column('text')
  description: string;

  @Column()
  filename: string;

  @Column('int')
  views: number;

  @Column()
  isPublished: boolean;
}
```

---

## 

**URL:** https://docs.nestjs.com/recipes/nest-commander

**Contents:**
  - Nest Commander
    - Installation#
    - A Command file#
    - Running the Command#
    - Testing#
    - Putting it all together#
    - More Information#

Expanding on the standalone application docs there's also the nest-commander package for writing command line applications in a structure similar to your typical Nest application.

Just like any other package, you've got to install it before you can use it.

nest-commander makes it easy to write new command-line applications with decorators via the @Command() decorator for classes and the @Option() decorator for methods of that class. Every command file should implement the CommandRunner abstract class and should be decorated with a @Command() decorator.

Every command is seen as an @Injectable() by Nest, so your normal Dependency Injection still works as you would expect it to. The only thing to take note of is the abstract class CommandRunner, which should be implemented by each command. The CommandRunner abstract class ensures that all commands have a run method that returns a Promise<void> and takes in the parameters string[], Record<string, any>. The run command is where you can kick all of your logic off from, it will take in whatever parameters did not match option flags and pass them in as an array, just in case you are really meaning to work with multiple parameters. As for the options, the Record<string, any>, the names of these properties match the name property given to the @Option() decorators, while their value matches the return of the option handler. If you'd like better type safety, you are welcome to create an interface for your options as well.

Similar to how in a NestJS application we can use the NestFactory to create a server for us, and run it using listen, the nest-commander package exposes a simple to use API to run your server. Import the CommandFactory and use the static method run and pass in the root module of your application. This would probably look like below

By default, Nest's logger is disabled when using the CommandFactory. It's possible to provide it though, as the second argument to the run function. You can either provide a custom NestJS logger, or an array of log levels you want to keep - it might be useful to at least provide ['error'] here, if you only want to print out Nest's error logs.

And that's it. Under the hood, CommandFactory will worry about calling NestFactory for you and calling app.close() when necessary, so you shouldn't need to worry about memory leaks there. If you need to add in some error handling, there's always try/catch wrapping the run command, or you can chain on some .catch() method to the bootstrap() call.

So what's the use of writing a super awesome command line script if you can't test it super easily, right? Fortunately, nest-commander has some utilities you can make use of that fits in perfectly with the NestJS ecosystem, it'll feel right at home to any Nestlings out there. Instead of using the CommandFactory for building the command in test mode, you can use CommandTestFactory and pass in your metadata, very similarly to how Test.createTestingModule from @nestjs/testing works. In fact, it uses this package under the hood. You're also still able to chain on the overrideProvider methods before calling compile() so you can swap out DI pieces right in the test.

The following class would equate to having a CLI command that can take in the subcommand basic or be called directly, with -n, -s, and -b (along with their long flags) all being supported and with custom parsers for each option. The --help flag is also supported, as is customary with commander.

Make sure the command class is added to a module

And now to be able to run the CLI in your main.ts you can do the following

And just like that, you've got a command line application.

Visit the nest-commander docs site for more information, examples, and API documentation.

**Examples:**

Example 1 (bash):
```bash
$ npm i nest-commander
```

Example 2 (javascript):
```javascript
import { CommandFactory } from 'nest-commander';
import { AppModule } from './app.module';

async function bootstrap() {
  await CommandFactory.run(AppModule);
}

bootstrap();
```

Example 3 (javascript):
```javascript
import { CommandFactory } from 'nest-commander';
import { AppModule } from './app.module';
import { LogService } './log.service';

async function bootstrap() {
  await CommandFactory.run(AppModule, new LogService());

  // or, if you only want to print Nest's warnings and errors
  await CommandFactory.run(AppModule, ['warn', 'error']);
}

bootstrap();
```

Example 4 (typescript):
```typescript
import { Command, CommandRunner, Option } from 'nest-commander';
import { LogService } from './log.service';

interface BasicCommandOptions {
  string?: string;
  boolean?: boolean;
  number?: number;
}

@Command({ name: 'basic', description: 'A parameter parse' })
export class BasicCommand extends CommandRunner {
  constructor(private readonly logService: LogService) {
    super()
  }

  async run(
    passedParam: string[],
    options?: BasicCommandOptions,
  ): Promise<void> {
    if (options?.boolean !== undefined && options?.boolean !== null) {
      this.runWithBoolean(passedParam, options.boolean);
    } else if (options?.number) {
      this.runWithNumber(passedParam, options.number);
    } else if (options?.string) {
      this.runWithString(passedParam, options.string);
    } else {
      this.runWithNone(passedParam);
    }
  }

  @Option({
    flags: '-n, --number [number]',
    description: 'A basic number parser',
  })
  parseNumber(val: string): number {
    return Number(val);
  }

  @Option({
    flags: '-s, --string [string]',
    description: 'A string return',
  })
  parseString(val: string): string {
    return val;
  }

  @Option({
    flags: '-b, --boolean [boolean]',
    description: 'A boolean parser',
  })
  parseBoolean(val: string): boolean {
    return JSON.parse(val);
  }

  runWithString(param: string[], option: string): void {
    this.logService.log({ param, string: option });
  }

  runWithNumber(param: string[], option: number): void {
    this.logService.log({ param, number: option });
  }

  runWithBoolean(param: string[], option: boolean): void {
    this.logService.log({ param, boolean: option });
  }

  runWithNone(param: string[]): void {
    this.logService.log({ param });
  }
}
```

---

## 

**URL:** https://docs.nestjs.com/recipes/serve-static

**Contents:**
  - Serve Static
    - Installation#
    - Bootstrap#
    - Configuration#
    - Example#

In order to serve static content like a Single Page Application (SPA) we can use the ServeStaticModule from the @nestjs/serve-static package.

First we need to install the required package:

Once the installation process is done, we can import the ServeStaticModule into the root AppModule and configure it by passing in a configuration object to the forRoot() method.

With this in place, build the static website and place its content in the location specified by the rootPath property.

ServeStaticModule can be configured with a variety of options to customize its behavior. You can set the path to render your static app, specify excluded paths, enable or disable setting Cache-Control response header, etc. See the full list of options here.

A working example is available here.

**Examples:**

Example 1 (bash):
```bash
$ npm install --save @nestjs/serve-static
```

Example 2 (typescript):
```typescript
import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ServeStaticModule } from '@nestjs/serve-static';
import { join } from 'path';

@Module({
  imports: [
    ServeStaticModule.forRoot({
      rootPath: join(__dirname, '..', 'client'),
    }),
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
```

---

## 

**URL:** https://docs.nestjs.com/recipes/cqrs

**Contents:**
  - CQRS
    - Installation#
    - Commands#
    - Queries#
    - Events#
    - Sagas#
    - Unhandled exceptions#
    - Subscribing to all events#
    - Request-scoping#
    - Example#

The flow of simple CRUD (Create, Read, Update and Delete) applications can be described as follows:

While this pattern is usually sufficient for small and medium-sized applications, it may not be the best choice for larger, more complex applications. In such cases, the CQRS (Command and Query Responsibility Segregation) model may be more appropriate and scalable (depending on the application's requirements). Benefits of this model include:

To facilitate that model, Nest provides a lightweight CQRS module. This chapter describes how to use it.

First install the required package:

Once the installation is complete, navigate to the root module of your application (usually AppModule), and import the CqrsModule.forRoot():

This module accepts an optional configuration object. The following options are available:

Commands are used to change the application state. They should be task-based, rather than data centric. When a command is dispatched, it is handled by a corresponding Command Handler. The handler is responsible for updating the application state.

In the code snippet above, we instantiate the KillDragonCommand class and pass it to the CommandBus's execute() method. This is the demonstrated command class:

As you can see, the KillDragonCommand class extends the Command class. The Command class is a simple utility class exported from the @nestjs/cqrs package that lets you define the command's return type. In this case, the return type is an object with an actionId property. Now, whenever the KillDragonCommand command is dispatched, the CommandBus#execute() method return-type will be inferred as Promise<{ actionId: string }>. This is useful when you want to return some data from the command handler.

The CommandBus represents a stream of commands. It is responsible for dispatching commands to the appropriate handlers. The execute() method returns a promise, which resolves to the value returned by the handler.

Let's create a handler for the KillDragonCommand command.

This handler retrieves the Hero entity from the repository, calls the killEnemy() method, and then persists the changes. The KillDragonHandler class implements the ICommandHandler interface, which requires the implementation of the execute() method. The execute() method receives the command object as an argument.

Note that ICommandHandler<KillDragonCommand> forces you to return a value that matches the command's return type. In this case, the return type is an object with an actionId property. This only applies to commands that inherit from the Command class. Otherwise, you can return whatever you want.

Lastly, make sure to register the KillDragonHandler as a provider in a module:

Queries are used to retrieve data from the application state. They should be data centric, rather than task-based. When a query is dispatched, it is handled by a corresponding Query Handler. The handler is responsible for retrieving the data.

The QueryBus follows the same pattern as the CommandBus. Query handlers should implement the IQueryHandler interface and be annotated with the @QueryHandler() decorator. See the following example:

Similar to the Command class, the Query class is a simple utility class exported from the @nestjs/cqrs package that lets you define the query's return type. In this case, the return type is a Hero object. Now, whenever the GetHeroQuery query is dispatched, the QueryBus#execute() method return-type will be inferred as Promise<Hero>.

To retrieve the hero, we need to create a query handler:

The GetHeroHandler class implements the IQueryHandler interface, which requires the implementation of the execute() method. The execute() method receives the query object as an argument, and must return the data that matches the query's return type (in this case, a Hero object).

Lastly, make sure to register the GetHeroHandler as a provider in a module:

Now, to dispatch the query, use the QueryBus:

Events are used to notify other parts of the application about changes in the application state. They are dispatched by models or directly using the EventBus. When an event is dispatched, it is handled by corresponding Event Handlers. Handlers can then, for example, update the read model.

For demonstration purposes, let's create an event class:

Now while events can be dispatched directly using the EventBus.publish() method, we can also dispatch them from the model. Let's update the Hero model to dispatch the HeroKilledDragonEvent event when the killEnemy() method is called.

The apply() method is used to dispatch events. It accepts an event object as an argument. However, since our model is not aware of the EventBus, we need to associate it with the model. We can do that by using the EventPublisher class.

The EventPublisher#mergeObjectContext method merges the event publisher into the provided object, which means that the object will now be able to publish events to the events stream.

Notice that in this example we also call the commit() method on the model. This method is used to dispatch any outstanding events. To automatically dispatch events, we can set the autoCommit property to true:

In case we want to merge the event publisher into a non-existing object, but rather into a class, we can use the EventPublisher#mergeClassContext method:

Now every instance of the HeroModel class will be able to publish events without using mergeObjectContext() method.

Additionally, we can emit events manually using EventBus:

Each event can have multiple Event Handlers.

As with commands and queries, make sure to register the HeroKilledDragonHandler as a provider in a module:

Saga is a long-running process that listens to events and may trigger new commands. It is usually used to manage complex workflows in the application. For example, when a user signs up, a saga may listen to the UserRegisteredEvent and send a welcome email to the user.

Sagas are an extremely powerful feature. A single saga may listen for 1..* events. Using the RxJS library, we can filter, map, fork, and merge event streams to create sophisticated workflows. Each saga returns an Observable which produces a command instance. This command is then dispatched asynchronously by the CommandBus.

Let's create a saga that listens to the HeroKilledDragonEvent and dispatches the DropAncientItemCommand command.

The @Saga() decorator marks the method as a saga. The events$ argument is an Observable stream of all events. The ofType operator filters the stream by the specified event type. The map operator maps the event to a new command instance.

In this example, we map the HeroKilledDragonEvent to the DropAncientItemCommand command. The DropAncientItemCommand command is then auto-dispatched by the CommandBus.

As with query, command, and event handlers, make sure to register the HeroesGameSagas as a provider in a module:

Event handlers are executed asynchronously, so they must always handle exceptions properly to prevent the application from entering an inconsistent state. If an exception is not handled, the EventBus will create an UnhandledExceptionInfo object and push it to the UnhandledExceptionBus stream. This stream is an Observable that can be used to process unhandled exceptions.

To filter out exceptions, we can use the ofType operator, as follows:

Where TransactionNotAllowedException is the exception we want to filter out.

The UnhandledExceptionInfo object contains the following properties:

CommandBus, QueryBus and EventBus are all Observables. This means that we can subscribe to the entire stream and, for example, process all events. For example, we can log all events to the console, or save them to the event store.

For those coming from different programming language backgrounds, it may be surprising to learn that in Nest, most things are shared across incoming requests. This includes a connection pool to the database, singleton services with global state, and more. Keep in mind that Node.js does not follow the request/response multi-threaded stateless model, where each request is processed by a separate thread. As a result, using singleton instances is safe for our applications.

However, there are edge cases where a request-based lifetime for the handler might be desirable. This could include scenarios like per-request caching in GraphQL applications, request tracking, or multi-tenancy. You can learn more about how to control scopes here.

Using request-scoped providers alongside CQRS can be complex because the CommandBus, QueryBus, and EventBus are singletons. Thankfully, the @nestjs/cqrs package simplifies this by automatically creating a new instance of request-scoped handlers for each processed command, query, or event.

To make a handler request-scoped, you can either:

To inject the request payload into any request-scoped provider, you use the @Inject(REQUEST) decorator. However, the nature of the request payload in CQRS depends on the context—it could be an HTTP request, a scheduled job, or any other operation that triggers a command.

The payload must be an instance of a class extending AsyncContext (provided by @nestjs/cqrs), which acts as the request context and holds data accessible throughout the request lifecycle.

When executing a command, pass the custom request context as the second argument to the CommandBus#execute method:

This makes the MyRequest instance available as the REQUEST provider to the corresponding handler:

You can follow the same approach for queries:

And in the query handler:

For events, while you can pass the request provider to EventBus#publish, this is less common. Instead, use EventPublisher to merge the request provider into a model:

Request-scoped event handlers subscribing to these events will have access to the request provider.

Sagas are always singleton instances because they manage long-running processes. However, you can retrieve the request provider from event objects:

Alternatively, use the request.attachTo(command) method to tie the request context to the command.

A working example is available here.

**Examples:**

Example 1 (bash):
```bash
$ npm install --save @nestjs/cqrs
```

Example 2 (typescript):
```typescript
import { Module } from '@nestjs/common';
import { CqrsModule } from '@nestjs/cqrs';

@Module({
  imports: [CqrsModule.forRoot()],
})
export class AppModule {}
```

Example 3 (typescript):
```typescript
@Injectable()
export class HeroesGameService {
  constructor(private commandBus: CommandBus) {}

  async killDragon(heroId: string, killDragonDto: KillDragonDto) {
    return this.commandBus.execute(
      new KillDragonCommand(heroId, killDragonDto.dragonId)
    );
  }
}
```

Example 4 (typescript):
```typescript
@Injectable()
@Dependencies(CommandBus)
export class HeroesGameService {
  constructor(commandBus) {
    this.commandBus = commandBus;
  }

  async killDragon(heroId, killDragonDto) {
    return this.commandBus.execute(
      new KillDragonCommand(heroId, killDragonDto.dragonId)
    );
  }
}
```

---
