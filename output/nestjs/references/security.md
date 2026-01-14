# Nestjs - Security

**Pages:** 7

---

## 

**URL:** https://docs.nestjs.com/security/authorization

**Contents:**
  - Authorization
    - Basic RBAC implementation#
- Learn the right way!
    - Claims-based authorization#
    - Integrating CASL#
    - Advanced: Implementing a PoliciesGuard#

Authorization refers to the process that determines what a user is able to do. For example, an administrative user is allowed to create, edit, and delete posts. A non-administrative user is only authorized to read the posts.

Authorization is orthogonal and independent from authentication. However, authorization requires an authentication mechanism.

There are many different approaches and strategies to handle authorization. The approach taken for any project depends on its particular application requirements. This chapter presents a few approaches to authorization that can be adapted to a variety of different requirements.

Role-based access control (RBAC) is a policy-neutral access-control mechanism defined around roles and privileges. In this section, we'll demonstrate how to implement a very basic RBAC mechanism using Nest guards.

First, let's create a Role enum representing roles in the system:

With this in place, we can create a @Roles() decorator. This decorator allows specifying what roles are required to access specific resources.

Now that we have a custom @Roles() decorator, we can use it to decorate any route handler.

Finally, we create a RolesGuard class which will compare the roles assigned to the current user to the actual roles required by the current route being processed. In order to access the route's role(s) (custom metadata), we'll use the Reflector helper class, which is provided out of the box by the framework and exposed from the @nestjs/core package.

In this example, we assumed that request.user contains the user instance and allowed roles (under the roles property). In your app, you will probably make that association in your custom authentication guard - see authentication chapter for more details.

To make sure this example works, your User class must look as follows:

Lastly, make sure to register the RolesGuard, for example, at the controller level, or globally:

When a user with insufficient privileges requests an endpoint, Nest automatically returns the following response:

Learn the right way! 19 chapters Authn & Authz Official certificate Deep-dive sessions Purchase the Authentication course

When an identity is created it may be assigned one or more claims issued by a trusted party. A claim is a name-value pair that represents what the subject can do, not what the subject is.

To implement a Claims-based authorization in Nest, you can follow the same steps we have shown above in the RBAC section with one significant difference: instead of checking for specific roles, you should compare permissions. Every user would have a set of permissions assigned. Likewise, each resource/endpoint would define what permissions are required (for example, through a dedicated @RequirePermissions() decorator) to access them.

CASL is an isomorphic authorization library which restricts what resources a given client is allowed to access. It's designed to be incrementally adoptable and can easily scale between a simple claim based and fully featured subject and attribute based authorization.

To start, first install the @casl/ability package:

Once the installation is complete, for the sake of illustrating the mechanics of CASL, we'll define two entity classes: User and Article.

User class consists of two properties, id, which is a unique user identifier, and isAdmin, indicating whether a user has administrator privileges.

Article class has three properties, respectively id, isPublished, and authorId. id is a unique article identifier, isPublished indicates whether an article was already published or not, and authorId, which is an ID of a user who wrote the article.

Now let's review and refine our requirements for this example:

With this in mind, we can start off by creating an Action enum representing all possible actions that the users can perform with entities:

To encapsulate CASL library, let's generate the CaslModule and CaslAbilityFactory now.

With this in place, we can define the createForUser() method on the CaslAbilityFactory. This method will create the Ability object for a given user:

In the example above, we created the MongoAbility instance using the AbilityBuilder class. As you probably guessed, can and cannot accept the same arguments but have different meanings, can allows to do an action on the specified subject and cannot forbids. Both may accept up to 4 arguments. To learn more about these functions, visit the official CASL documentation.

Lastly, make sure to add the CaslAbilityFactory to the providers and exports arrays in the CaslModule module definition:

With this in place, we can inject the CaslAbilityFactory to any class using standard constructor injection as long as the CaslModule is imported in the host context:

Then use it in a class as follows.

For example, let's say we have a user who is not an admin. In this case, the user should be able to read articles, but creating new ones or removing the existing articles should be prohibited.

Also, as we have specified in our requirements, the user should be able to update its articles:

As you can see, MongoAbility instance allows us to check permissions in pretty readable way. Likewise, AbilityBuilder allows us to define permissions (and specify various conditions) in a similar fashion. To find more examples, visit the official documentation.

In this section, we'll demonstrate how to build a somewhat more sophisticated guard, which checks if a user meets specific authorization policies that can be configured on the method-level (you can extend it to respect policies configured on the class-level too). In this example, we are going to use the CASL package just for illustration purposes, but using this library is not required. Also, we will use the CaslAbilityFactory provider that we've created in the previous section.

First, let's flesh out the requirements. The goal is to provide a mechanism that allows specifying policy checks per route handler. We will support both objects and functions (for simpler checks and for those who prefer more functional-style code).

Let's start off by defining interfaces for policy handlers:

As mentioned above, we provided two possible ways of defining a policy handler, an object (instance of a class that implements the IPolicyHandler interface) and a function (which meets the PolicyHandlerCallback type).

With this in place, we can create a @CheckPolicies() decorator. This decorator allows specifying what policies have to be met to access specific resources.

Now let's create a PoliciesGuard that will extract and execute all the policy handlers bound to a route handler.

Let's break this example down. The policyHandlers is an array of handlers assigned to the method through the @CheckPolicies() decorator. Next, we use the CaslAbilityFactory#create method which constructs the Ability object, allowing us to verify whether a user has sufficient permissions to perform specific actions. We are passing this object to the policy handler which is either a function or an instance of a class that implements the IPolicyHandler, exposing the handle() method that returns a boolean. Lastly, we use the Array#every method to make sure that every handler returned true value.

Finally, to test this guard, bind it to any route handler, and register an inline policy handler (functional approach), as follows:

Alternatively, we can define a class which implements the IPolicyHandler interface:

And use it as follows:

**Examples:**

Example 1 (typescript):
```typescript
export enum Role {
  User = 'user',
  Admin = 'admin',
}
```

Example 2 (typescript):
```typescript
import { SetMetadata } from '@nestjs/common';
import { Role } from '../enums/role.enum';

export const ROLES_KEY = 'roles';
export const Roles = (...roles: Role[]) => SetMetadata(ROLES_KEY, roles);
```

Example 3 (typescript):
```typescript
import { SetMetadata } from '@nestjs/common';

export const ROLES_KEY = 'roles';
export const Roles = (...roles) => SetMetadata(ROLES_KEY, roles);
```

Example 4 (typescript):
```typescript
@Post()
@Roles(Role.Admin)
create(@Body() createCatDto: CreateCatDto) {
  this.catsService.create(createCatDto);
}
```

---

## 

**URL:** https://docs.nestjs.com/security/helmet

**Contents:**
  - Helmet
    - Use with Express (default)#
    - Use with Fastify#

Helmet can help protect your app from some well-known web vulnerabilities by setting HTTP headers appropriately. Generally, Helmet is just a collection of smaller middleware functions that set security-related HTTP headers (read more).

Start by installing the required package.

Once the installation is complete, apply it as a global middleware.

If you are using the FastifyAdapter, install the @fastify/helmet package:

fastify-helmet should not be used as a middleware, but as a Fastify plugin, i.e., by using app.register():

**Examples:**

Example 1 (bash):
```bash
$ npm i --save helmet
```

Example 2 (typescript):
```typescript
import helmet from 'helmet';
// somewhere in your initialization file
app.use(helmet());
```

Example 3 (typescript):
```typescript
app.use(helmet({
  crossOriginEmbedderPolicy: false,
  contentSecurityPolicy: {
    directives: {
      imgSrc: [`'self'`, 'data:', 'apollo-server-landing-page.cdn.apollographql.com'],
      scriptSrc: [`'self'`, `https: 'unsafe-inline'`],
      manifestSrc: [`'self'`, 'apollo-server-landing-page.cdn.apollographql.com'],
      frameSrc: [`'self'`, 'sandbox.embed.apollographql.com'],
    },
  },
}));
```

Example 4 (bash):
```bash
$ npm i --save @fastify/helmet
```

---

## 

**URL:** https://docs.nestjs.com/security/authentication

**Contents:**
  - Authentication
    - Creating an authentication module#
    - Implementing the "Sign in" endpoint#
- Learn the right way!
    - JWT token#
    - Implementing the authentication guard#
    - Enable authentication globally#
    - Passport integration#
    - Example#

Authentication is an essential part of most applications. There are many different approaches and strategies to handle authentication. The approach taken for any project depends on its particular application requirements. This chapter presents several approaches to authentication that can be adapted to a variety of different requirements.

Let's flesh out our requirements. For this use case, clients will start by authenticating with a username and password. Once authenticated, the server will issue a JWT that can be sent as a bearer token in an authorization header on subsequent requests to prove authentication. We'll also create a protected route that is accessible only to requests that contain a valid JWT.

We'll start with the first requirement: authenticating a user. We'll then extend that by issuing a JWT. Finally, we'll create a protected route that checks for a valid JWT on the request.

We'll start by generating an AuthModule and in it, an AuthService and an AuthController. We'll use the AuthService to implement the authentication logic, and the AuthController to expose the authentication endpoints.

As we implement the AuthService, we'll find it useful to encapsulate user operations in a UsersService, so let's generate that module and service now:

Replace the default contents of these generated files as shown below. For our sample app, the UsersService simply maintains a hard-coded in-memory list of users, and a find method to retrieve one by username. In a real app, this is where you'd build your user model and persistence layer, using your library of choice (e.g., TypeORM, Sequelize, Mongoose, etc.).

In the UsersModule, the only change needed is to add the UsersService to the exports array of the @Module decorator so that it is visible outside this module (we'll soon use it in our AuthService).

Our AuthService has the job of retrieving a user and verifying the password. We create a signIn() method for this purpose. In the code below, we use a convenient ES6 spread operator to strip the password property from the user object before returning it. This is a common practice when returning user objects, as you don't want to expose sensitive fields like passwords or other security keys.

Now, we update our AuthModule to import the UsersModule.

With this in place, let's open up the AuthController and add a signIn() method to it. This method will be called by the client to authenticate a user. It will receive the username and password in the request body, and will return a JWT token if the user is authenticated.

Learn the right way! 19 chapters Authn & Authz Official certificate Deep-dive sessions Purchase the Authentication course

We're ready to move on to the JWT portion of our auth system. Let's review and refine our requirements:

We'll need to install one additional package to support our JWT requirements:

To keep our services cleanly modularized, we'll handle generating the JWT in the authService. Open the auth.service.ts file in the auth folder, inject the JwtService, and update the signIn method to generate a JWT token as shown below:

We're using the @nestjs/jwt library, which supplies a signAsync() function to generate our JWT from a subset of the user object properties, which we then return as a simple object with a single access_token property. Note: we choose a property name of sub to hold our userId value to be consistent with JWT standards.

We now need to update the AuthModule to import the new dependencies and configure the JwtModule.

First, create constants.ts in the auth folder, and add the following code:

We'll use this to share our key between the JWT signing and verifying steps.

Now, open auth.module.ts in the auth folder and update it to look like this:

We configure the JwtModule using register(), passing in a configuration object. See here for more on the Nest JwtModule and here for more details on the available configuration options.

Let's go ahead and test our routes using cURL again. You can test with any of the user objects hard-coded in the UsersService.

We can now address our final requirement: protecting endpoints by requiring a valid JWT be present on the request. We'll do this by creating an AuthGuard that we can use to protect our routes.

We can now implement our protected route and register our AuthGuard to protect it.

Open the auth.controller.ts file and update it as shown below:

We're applying the AuthGuard that we just created to the GET /profile route so that it will be protected.

Ensure the app is running, and test the routes using cURL.

Note that in the AuthModule, we configured the JWT to have an expiration of 60 seconds. This is too short an expiration, and dealing with the details of token expiration and refresh is beyond the scope of this article. However, we chose that to demonstrate an important quality of JWTs. If you wait 60 seconds after authenticating before attempting a GET /auth/profile request, you'll receive a 401 Unauthorized response. This is because @nestjs/jwt automatically checks the JWT for its expiration time, saving you the trouble of doing so in your application.

We've now completed our JWT authentication implementation. JavaScript clients (such as Angular/React/Vue), and other JavaScript apps, can now authenticate and communicate securely with our API Server.

If the vast majority of your endpoints should be protected by default, you can register the authentication guard as a global guard and instead of using @UseGuards() decorator on top of each controller, you could simply flag which routes should be public.

First, register the AuthGuard as a global guard using the following construction (in any module, for example, in the AuthModule):

With this in place, Nest will automatically bind AuthGuard to all endpoints.

Now we must provide a mechanism for declaring routes as public. For this, we can create a custom decorator using the SetMetadata decorator factory function.

In the file above, we exported two constants. One being our metadata key named IS_PUBLIC_KEY, and the other being our new decorator itself that we’re going to call Public (you can alternatively name it SkipAuth or AllowAnon, whatever fits your project).

Now that we have a custom @Public() decorator, we can use it to decorate any method, as follows:

Lastly, we need the AuthGuard to return true when the "isPublic" metadata is found. For this, we'll use the Reflector class (read more here).

Passport is the most popular node.js authentication library, well-known by the community and successfully used in many production applications. It's straightforward to integrate this library with a Nest application using the @nestjs/passport module.

To learn how you can integrate Passport with NestJS, check out this chapter.

You can find a complete version of the code in this chapter here.

**Examples:**

Example 1 (bash):
```bash
$ nest g module auth
$ nest g controller auth
$ nest g service auth
```

Example 2 (bash):
```bash
$ nest g module users
$ nest g service users
```

Example 3 (typescript):
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

Example 4 (typescript):
```typescript
import { Injectable } from '@nestjs/common';

@Injectable()
export class UsersService {
  constructor() {
    this.users = [
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
  }

  async findOne(username) {
    return this.users.find(user => user.username === username);
  }
}
```

---

## 

**URL:** https://docs.nestjs.com/security/rate-limiting

**Contents:**
  - Rate Limiting
    - Multiple Throttler Definitions#
    - Customization#
    - Proxies#
    - Websockets#
    - GraphQL#
    - Configuration#
    - Async Configuration#
    - Storages#
    - Time Helpers#

A common technique to protect applications from brute-force attacks is rate-limiting. To get started, you'll need to install the @nestjs/throttler package.

Once the installation is complete, the ThrottlerModule can be configured as any other Nest package with forRoot or forRootAsync methods.

The above will set the global options for the ttl, the time to live in milliseconds, and the limit, the maximum number of requests within the ttl, for the routes of your application that are guarded.

Once the module has been imported, you can then choose how you would like to bind the ThrottlerGuard. Any kind of binding as mentioned in the guards section is fine. If you wanted to bind the guard globally, for example, you could do so by adding this provider to any module:

There may come upon times where you want to set up multiple throttling definitions, like no more than 3 calls in a second, 20 calls in 10 seconds, and 100 calls in a minute. To do so, you can set up your definitions in the array with named options, that can later be referenced in the @SkipThrottle() and @Throttle() decorators to change the options again.

There may be a time where you want to bind the guard to a controller or globally, but want to disable rate limiting for one or more of your endpoints. For that, you can use the @SkipThrottle() decorator, to negate the throttler for an entire class or a single route. The @SkipThrottle() decorator can also take in an object of string keys with boolean values for if there is a case where you want to exclude most of a controller, but not every route, and configure it per throttler set if you have more than one. If you do not pass an object, the default is to use { default: true }

This @SkipThrottle() decorator can be used to skip a route or a class or to negate the skipping of a route in a class that is skipped.

There is also the @Throttle() decorator which can be used to override the limit and ttl set in the global module, to give tighter or looser security options. This decorator can be used on a class or a function as well. With version 5 and onwards, the decorator takes in an object with the string relating to the name of the throttler set, and an object with the limit and ttl keys and integer values, similar to the options passed to the root module. If you do not have a name set in your original options, use the string default. You have to configure it like this:

If your application is running behind a proxy server, it’s essential to configure the HTTP adapter to trust the proxy. You can refer to the specific HTTP adapter options for Express and Fastify to enable the trust proxy setting.

Here's an example that demonstrates how to enable trust proxy for the Express adapter:

Enabling trust proxy allows you to retrieve the original IP address from the X-Forwarded-For header. You can also customize the behavior of your application by overriding the getTracker() method to extract the IP address from this header instead of relying on req.ip. The following example demonstrates how to achieve this for both Express and Fastify:

This module can work with websockets, but it requires some class extension. You can extend the ThrottlerGuard and override the handleRequest method like so:

There's a few things to keep in mind when working with WebSockets:

The ThrottlerGuard can also be used to work with GraphQL requests. Again, the guard can be extended, but this time the getRequestResponse method will be overridden

The following options are valid for the object passed to the array of the ThrottlerModule's options:

If you need to set up storage instead, or want to use some of the above options in a more global sense, applying to each throttler set, you can pass the options above via the throttlers option key and use the below table

You may want to get your rate-limiting configuration asynchronously instead of synchronously. You can use the forRootAsync() method, which allows for dependency injection and async methods.

One approach would be to use a factory function:

You can also use the useClass syntax:

This is doable, as long as ThrottlerConfigService implements the interface ThrottlerOptionsFactory.

The built in storage is an in memory cache that keeps track of the requests made until they have passed the TTL set by the global options. You can drop in your own storage option to the storage option of the ThrottlerModule so long as the class implements the ThrottlerStorage interface.

For distributed servers you could use the community storage provider for Redis to have a single source of truth.

There are a couple of helper methods to make the timings more readable if you prefer to use them over the direct definition. @nestjs/throttler exports five different helpers, seconds, minutes, hours, days, and weeks. To use them, simply call seconds(5) or any of the other helpers, and the correct number of milliseconds will be returned.

For most people, wrapping your options in an array will be enough.

If you are using a custom storage, you should wrap your ttl and limit in an array and assign it to the throttlers property of the options object.

Any @SkipThrottle() decorator can be used to bypass throttling for specific routes or methods. It accepts an optional boolean parameter, which defaults to true. This is useful when you want to skip rate limiting on particular endpoints.

Any @Throttle() decorators should also now take in an object with string keys, relating to the names of the throttler contexts (again, 'default' if no name) and values of objects that have limit and ttl keys.

For more info, see the Changelog

**Examples:**

Example 1 (bash):
```bash
$ npm i --save @nestjs/throttler
```

Example 2 (typescript):
```typescript
@Module({
  imports: [
     ThrottlerModule.forRoot({
      throttlers: [
        {
          ttl: 60000,
          limit: 10,
        },
      ],
    }),
  ],
})
export class AppModule {}
```

Example 3 (typescript):
```typescript
{
  provide: APP_GUARD,
  useClass: ThrottlerGuard
}
```

Example 4 (typescript):
```typescript
@Module({
  imports: [
    ThrottlerModule.forRoot([
      {
        name: 'short',
        ttl: 1000,
        limit: 3,
      },
      {
        name: 'medium',
        ttl: 10000,
        limit: 20
      },
      {
        name: 'long',
        ttl: 60000,
        limit: 100
      }
    ]),
  ],
})
export class AppModule {}
```

---

## 

**URL:** https://docs.nestjs.com/security/cors

**Contents:**
  - CORS
    - Getting started#

Cross-origin resource sharing (CORS) is a mechanism that allows resources to be requested from another domain. Under the hood, Nest makes use of the Express cors or Fastify @fastify/cors packages depending on the underlying platform. These packages provide various options that you can customize based on your requirements.

To enable CORS, call the enableCors() method on the Nest application object.

The enableCors() method takes an optional configuration object argument. The available properties of this object are described in the official CORS documentation. Another way is to pass a callback function that lets you define the configuration object asynchronously based on the request (on the fly).

Alternatively, enable CORS via the create() method's options object. Set the cors property to true to enable CORS with default settings. Or, pass a CORS configuration object or callback function as the cors property value to customize its behavior.

**Examples:**

Example 1 (typescript):
```typescript
const app = await NestFactory.create(AppModule);
app.enableCors();
await app.listen(process.env.PORT ?? 3000);
```

Example 2 (typescript):
```typescript
const app = await NestFactory.create(AppModule, { cors: true });
await app.listen(process.env.PORT ?? 3000);
```

---

## 

**URL:** https://docs.nestjs.com/security/csrf-protection

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

**URL:** https://docs.nestjs.com/security/encryption-and-hashing

**Contents:**
  - Encryption and Hashing
    - Encryption#
    - Hashing#

Encryption is the process of encoding information. This process converts the original representation of the information, known as plaintext, into an alternative form known as ciphertext. Ideally, only authorized parties can decipher a ciphertext back to plaintext and access the original information. Encryption does not itself prevent interference but denies the intelligible content to a would-be interceptor. Encryption is a two-way function; what is encrypted can be decrypted with the proper key.

Hashing is the process of converting a given key into another value. A hash function is used to generate the new value according to a mathematical algorithm. Once hashing has been done, it should be impossible to go from the output to the input.

Node.js provides a built-in crypto module that you can use to encrypt and decrypt strings, numbers, buffers, streams, and more. Nest itself does not provide any additional package on top of this module to avoid introducing unnecessary abstractions.

As an example, let's use AES (Advanced Encryption System) 'aes-256-ctr' algorithm CTR encryption mode.

Now to decrypt encryptedText value:

For hashing, we recommend using either the bcrypt or argon2 packages. Nest itself does not provide any additional wrappers on top of these modules to avoid introducing unnecessary abstractions (making the learning curve short).

As an example, let's use bcrypt to hash a random password.

First install required packages:

Once the installation is complete, you can use the hash function, as follows:

To generate a salt, use the genSalt function:

To compare/check a password, use the compare function:

You can read more about available functions here.

**Examples:**

Example 1 (typescript):
```typescript
import { createCipheriv, randomBytes, scrypt } from 'node:crypto';
import { promisify } from 'node:util';

const iv = randomBytes(16);
const password = 'Password used to generate key';

// The key length is dependent on the algorithm.
// In this case for aes256, it is 32 bytes.
const key = (await promisify(scrypt)(password, 'salt', 32)) as Buffer;
const cipher = createCipheriv('aes-256-ctr', key, iv);

const textToEncrypt = 'Nest';
const encryptedText = Buffer.concat([
  cipher.update(textToEncrypt),
  cipher.final(),
]);
```

Example 2 (typescript):
```typescript
import { createDecipheriv } from 'node:crypto';

const decipher = createDecipheriv('aes-256-ctr', key, iv);
const decryptedText = Buffer.concat([
  decipher.update(encryptedText),
  decipher.final(),
]);
```

Example 3 (shell):
```shell
$ npm i bcrypt
$ npm i -D @types/bcrypt
```

Example 4 (typescript):
```typescript
import * as bcrypt from 'bcrypt';

const saltOrRounds = 10;
const password = 'random_password';
const hash = await bcrypt.hash(password, saltOrRounds);
```

---
