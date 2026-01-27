# Nestjs - Techniques

**Pages:** 22

---

## 

**URL:** https://docs.nestjs.com/techniques/mongodb

**Contents:**
  - Mongo
    - Model injection#
    - Connection#
    - Sessions#
    - Multiple databases#
    - Hooks (middleware)#
    - Plugins#
    - Discriminators#
    - Testing#
- Learn the right way!

Nest supports two methods for integrating with the MongoDB database. You can either use the built-in TypeORM module described here, which has a connector for MongoDB, or use Mongoose, the most popular MongoDB object modeling tool. In this chapter we'll describe the latter, using the dedicated @nestjs/mongoose package.

Start by installing the required dependencies:

Once the installation process is complete, we can import the MongooseModule into the root AppModule.

The forRoot() method accepts the same configuration object as mongoose.connect() from the Mongoose package, as described here.

With Mongoose, everything is derived from a Schema. Each schema maps to a MongoDB collection and defines the shape of the documents within that collection. Schemas are used to define Models. Models are responsible for creating and reading documents from the underlying MongoDB database.

Schemas can be created with NestJS decorators, or with Mongoose itself manually. Using decorators to create schemas greatly reduces boilerplate and improves overall code readability.

Let's define the CatSchema:

The @Schema() decorator marks a class as a schema definition. It maps our Cat class to a MongoDB collection of the same name, but with an additional “s” at the end - so the final mongo collection name will be cats. This decorator accepts a single optional argument which is a schema options object. Think of it as the object you would normally pass as a second argument of the mongoose.Schema class' constructor (e.g., new mongoose.Schema(_, options))). To learn more about available schema options, see this chapter.

The @Prop() decorator defines a property in the document. For example, in the schema definition above, we defined three properties: name, age, and breed. The schema types for these properties are automatically inferred thanks to TypeScript metadata (and reflection) capabilities. However, in more complex scenarios in which types cannot be implicitly reflected (for example, arrays or nested object structures), types must be indicated explicitly, as follows:

Alternatively, the @Prop() decorator accepts an options object argument (read more about the available options). With this, you can indicate whether a property is required or not, specify a default value, or mark it as immutable. For example:

In case you want to specify relation to another model, later for populating, you can use @Prop() decorator as well. For example, if Cat has Owner which is stored in a different collection called owners, the property should have type and ref. For example:

In case there are multiple owners, your property configuration should look as follows:

If you don’t intend to always populate a reference to another collection, consider using mongoose.Types.ObjectId as the type instead:

Then, when you need to selectively populate it later, you can use a repository function that specifies the correct type:

Finally, the raw schema definition can also be passed to the decorator. This is useful when, for example, a property represents a nested object which is not defined as a class. For this, use the raw() function from the @nestjs/mongoose package, as follows:

Alternatively, if you prefer not using decorators, you can define a schema manually. For example:

The cat.schema file resides in a folder in the cats directory, where we also define the CatsModule. While you can store schema files wherever you prefer, we recommend storing them near their related domain objects, in the appropriate module directory.

Let's look at the CatsModule:

The MongooseModule provides the forFeature() method to configure the module, including defining which models should be registered in the current scope. If you also want to use the models in another module, add MongooseModule to the exports section of CatsModule and import CatsModule in the other module.

Once you've registered the schema, you can inject a Cat model into the CatsService using the @InjectModel() decorator:

At times you may need to access the native Mongoose Connection object. For example, you may want to make native API calls on the connection object. You can inject the Mongoose Connection by using the @InjectConnection() decorator as follows:

To start a session with Mongoose, it's recommended to inject the database connection using @InjectConnection rather than calling mongoose.startSession() directly. This approach allows better integration with the NestJS dependency injection system, ensuring proper connection management.

Here's an example of how to start a session:

In this example, @InjectConnection() is used to inject the Mongoose connection into the service. Once the connection is injected, you can use connection.startSession() to begin a new session. This session can be used to manage database transactions, ensuring atomic operations across multiple queries. After starting the session, remember to commit or abort the transaction based on your logic.

Some projects require multiple database connections. This can also be achieved with this module. To work with multiple connections, first create the connections. In this case, connection naming becomes mandatory.

With this setup, you have to tell the MongooseModule.forFeature() function which connection should be used.

You can also inject the Connection for a given connection:

To inject a given Connection to a custom provider (for example, factory provider), use the getConnectionToken() function passing the name of the connection as an argument.

If you are just looking to inject the model from a named database, you can use the connection name as a second parameter to the @InjectModel() decorator.

Middleware (also called pre and post hooks) are functions which are passed control during execution of asynchronous functions. Middleware is specified on the schema level and is useful for writing plugins (source). Calling pre() or post() after compiling a model does not work in Mongoose. To register a hook before model registration, use the forFeatureAsync() method of the MongooseModule along with a factory provider (i.e., useFactory). With this technique, you can access a schema object, then use the pre() or post() method to register a hook on that schema. See example below:

Like other factory providers, our factory function can be async and can inject dependencies through inject.

To register a plugin for a given schema, use the forFeatureAsync() method.

To register a plugin for all schemas at once, call the .plugin() method of the Connection object. You should access the connection before models are created; to do this, use the connectionFactory:

Discriminators are a schema inheritance mechanism. They enable you to have multiple models with overlapping schemas on top of the same underlying MongoDB collection.

Suppose you wanted to track different types of events in a single collection. Every event will have a timestamp.

SignedUpEvent and ClickedLinkEvent instances will be stored in the same collection as generic events.

Now, let's define the ClickedLinkEvent class, as follows:

And SignUpEvent class:

With this in place, use the discriminators option to register a discriminator for a given schema. It works on both MongooseModule.forFeature and MongooseModule.forFeatureAsync:

When unit testing an application, we usually want to avoid any database connection, making our test suites simpler to set up and faster to execute. But our classes might depend on models that are pulled from the connection instance. How do we resolve these classes? The solution is to create mock models.

To make this easier, the @nestjs/mongoose package exposes a getModelToken() function that returns a prepared injection token based on a token name. Using this token, you can easily provide a mock implementation using any of the standard custom provider techniques, including useClass, useValue, and useFactory. For example:

In this example, a hardcoded catModel (object instance) will be provided whenever any consumer injects a Model<Cat> using an @InjectModel() decorator.

Learn the right way! 80+ chapters 5+ hours of videos Official certificate Deep-dive sessions Explore official courses

When you need to pass module options asynchronously instead of statically, use the forRootAsync() method. As with most dynamic modules, Nest provides several techniques to deal with async configuration.

One technique is to use a factory function:

Like other factory providers, our factory function can be async and can inject dependencies through inject.

Alternatively, you can configure the MongooseModule using a class instead of a factory, as shown below:

The construction above instantiates MongooseConfigService inside MongooseModule, using it to create the required options object. Note that in this example, the MongooseConfigService has to implement the MongooseOptionsFactory interface, as shown below. The MongooseModule will call the createMongooseOptions() method on the instantiated object of the supplied class.

If you want to reuse an existing options provider instead of creating a private copy inside the MongooseModule, use the useExisting syntax.

You can listen to Mongoose connection events by using the onConnectionCreate configuration option. This allows you to implement custom logic whenever a connection is established. For instance, you can register event listeners for the connected, open, disconnected, reconnected, and disconnecting events, as demonstrated below:

In this code snippet, we are establishing a connection to a MongoDB database at mongodb://localhost/test. The onConnectionCreate option enables you to set up specific event listeners for monitoring the connection's status:

You can also incorporate the onConnectionCreate property into async configurations created with MongooseModule.forRootAsync():

This provides a flexible way to manage connection events, enabling you to handle changes in connection status effectively.

To nest subdocuments within a parent document, you can define your schemas as follows:

And then reference the subdocument in the parent schema:

If you want to include multiple subdocuments, you can use an array of subdocuments. It's important to override the type of the property accordingly:

In Mongoose, a virtual is a property that exists on a document but is not persisted to MongoDB. It is not stored in the database but is computed dynamically whenever it's accessed. Virtuals are typically used for derived or computed values, like combining fields (e.g., creating a fullName property by concatenating firstName and lastName), or for creating properties that rely on existing data in the document.

In this example, the fullName virtual is derived from firstName and lastName. Even though it behaves like a normal property when accessed, it’s never saved to the MongoDB document.:

A working example is available here.

**Examples:**

Example 1 (bash):
```bash
$ npm i @nestjs/mongoose mongoose
```

Example 2 (typescript):
```typescript
import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';

@Module({
  imports: [MongooseModule.forRoot('mongodb://localhost/nest')],
})
export class AppModule {}
```

Example 3 (typescript):
```typescript
import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { HydratedDocument } from 'mongoose';

export type CatDocument = HydratedDocument<Cat>;

@Schema()
export class Cat {
  @Prop()
  name: string;

  @Prop()
  age: number;

  @Prop()
  breed: string;
}

export const CatSchema = SchemaFactory.createForClass(Cat);
```

Example 4 (typescript):
```typescript
@Prop([String])
tags: string[];
```

---

## 

**URL:** https://docs.nestjs.com/techniques/versioning

**Contents:**
  - Versioning
    - URI Versioning Type#
    - Header Versioning Type#
    - Media Type Versioning Type#
    - Custom Versioning Type#
    - Usage#
    - Controller versions#
    - Route versions#
    - Multiple versions#
    - Version "Neutral"#

Versioning allows you to have different versions of your controllers or individual routes running within the same application. Applications change very often and it is not unusual that there are breaking changes that you need to make while still needing to support the previous version of the application.

There are 4 types of versioning that are supported:

URI Versioning uses the version passed within the URI of the request, such as https://example.com/v1/route and https://example.com/v2/route.

To enable URI Versioning for your application, do the following:

Header Versioning uses a custom, user specified, request header to specify the version where the value of the header will be the version to use for the request.

Example HTTP Requests for Header Versioning:

To enable Header Versioning for your application, do the following:

The header property should be the name of the header that will contain the version of the request.

Media Type Versioning uses the Accept header of the request to specify the version.

Within the Accept header, the version will be separated from the media type with a semi-colon, ;. It should then contain a key-value pair that represents the version to use for the request, such as Accept: application/json;v=2. They key is treated more as a prefix when determining the version will to be configured to include the key and separator.

To enable Media Type Versioning for your application, do the following:

The key property should be the key and separator of the key-value pair that contains the version. For the example Accept: application/json;v=2, the key property would be set to v=.

Custom Versioning uses any aspect of the request to specify the version (or versions). The incoming request is analyzed using an extractor function that returns a string or array of strings.

If multiple versions are provided by the requester, the extractor function can return an array of strings, sorted in order of greatest/highest version to smallest/lowest version. Versions are matched to routes in order from highest to lowest.

If an empty string or array is returned from the extractor, no routes are matched and a 404 is returned.

For example, if an incoming request specifies it supports versions 1, 2, and 3, the extractorMUST return [3, 2, 1]. This ensures that the highest possible route version is selected first.

If versions [3, 2, 1] are extracted, but routes only exist for version 2 and 1, the route that matches version 2 is selected (version 3 is automatically ignored).

To enable Custom Versioning for your application, create an extractor function and pass it into your application like so:

Versioning allows you to version controllers, individual routes, and also provides a way for certain resources to opt-out of versioning. The usage of versioning is the same regardless of the Versioning Type your application uses.

A version can be applied to a controller, setting the version for all routes within the controller.

To add a version to a controller do the following:

A version can be applied to an individual route. This version will override any other version that would effect the route, such as the Controller Version.

To add a version to an individual route do the following:

Multiple versions can be applied to a controller or route. To use multiple versions, you would set the version to be an Array.

To add multiple versions do the following:

Some controllers or routes may not care about the version and would have the same functionality regardless of the version. To accommodate this, the version can be set to VERSION_NEUTRAL symbol.

An incoming request will be mapped to a VERSION_NEUTRAL controller or route regardless of the version sent in the request in addition to if the request does not contain a version at all.

To add a version neutral controller or route do the following:

If you do not want to provide a version for each controller/or individual routes, or if you want to have a specific version set as the default version for every controller/route that don't have the version specified, you could set the defaultVersion as follows:

Middlewares can also use versioning metadata to configure the middleware for a specific route's version. To do so, provide the version number as one of the parameters for the MiddlewareConsumer.forRoutes() method:

With the code above, the LoggerMiddleware will only be applied to the version '2' of /cats endpoint.

**Examples:**

Example 1 (typescript):
```typescript
const app = await NestFactory.create(AppModule);
// or "app.enableVersioning()"
app.enableVersioning({
  type: VersioningType.URI,
});
await app.listen(process.env.PORT ?? 3000);
```

Example 2 (typescript):
```typescript
const app = await NestFactory.create(AppModule);
app.enableVersioning({
  type: VersioningType.HEADER,
  header: 'Custom-Header',
});
await app.listen(process.env.PORT ?? 3000);
```

Example 3 (typescript):
```typescript
const app = await NestFactory.create(AppModule);
app.enableVersioning({
  type: VersioningType.MEDIA_TYPE,
  key: 'v=',
});
await app.listen(process.env.PORT ?? 3000);
```

Example 4 (typescript):
```typescript
// Example extractor that pulls out a list of versions from a custom header and turns it into a sorted array.
// This example uses Fastify, but Express requests can be processed in a similar way.
const extractor = (request: FastifyRequest): string | string[] =>
  [request.headers['custom-versioning-field'] ?? '']
     .flatMap(v => v.split(','))
     .filter(v => !!v)
     .sort()
     .reverse()

const app = await NestFactory.create(AppModule);
app.enableVersioning({
  type: VersioningType.CUSTOM,
  extractor,
});
await app.listen(process.env.PORT ?? 3000);
```

---

## 

**URL:** https://docs.nestjs.com/techniques/cookies

**Contents:**
  - Cookies
    - Use with Express (default)#
    - Use with Fastify#
    - Creating a custom decorator (cross-platform)#

An HTTP cookie is a small piece of data stored by the user's browser. Cookies were designed to be a reliable mechanism for websites to remember stateful information. When the user visits the website again, the cookie is automatically sent with the request.

First install the required package (and its types for TypeScript users):

Once the installation is complete, apply the cookie-parser middleware as global middleware (for example, in your main.ts file).

You can pass several options to the cookieParser middleware:

The middleware will parse the Cookie header on the request and expose the cookie data as the property req.cookies and, if a secret was provided, as the property req.signedCookies. These properties are name value pairs of the cookie name to cookie value.

When a secret is provided, this module will unsign and validate any signed cookie values and move those name value pairs from req.cookies into req.signedCookies. A signed cookie is a cookie that has a value prefixed with s:. Signed cookies that fail signature validation will have the value false instead of the tampered value.

With this in place, you can now read cookies from within the route handlers, as follows:

To attach a cookie to an outgoing response, use the Response#cookie() method:

First install the required package:

Once the installation is complete, register the @fastify/cookie plugin:

With this in place, you can now read cookies from within the route handlers, as follows:

To attach a cookie to an outgoing response, use the FastifyReply#setCookie() method:

To read more about FastifyReply#setCookie() method, check out this page.

To provide a convenient, declarative way of accessing incoming cookies, we can create a custom decorator.

The @Cookies() decorator will extract all cookies, or a named cookie from the req.cookies object and populate the decorated parameter with that value.

With this in place, we can now use the decorator in a route handler signature, as follows:

**Examples:**

Example 1 (shell):
```shell
$ npm i cookie-parser
$ npm i -D @types/cookie-parser
```

Example 2 (typescript):
```typescript
import * as cookieParser from 'cookie-parser';
// somewhere in your initialization file
app.use(cookieParser());
```

Example 3 (typescript):
```typescript
@Get()
findAll(@Req() request: Request) {
  console.log(request.cookies); // or "request.cookies['cookieKey']"
  // or console.log(request.signedCookies);
}
```

Example 4 (typescript):
```typescript
@Get()
findAll(@Res({ passthrough: true }) response: Response) {
  response.cookie('key', 'value')
}
```

---

## 

**URL:** https://docs.nestjs.com/techniques/compression

**Contents:**
  - Compression
    - Use with Express (default)#
    - Use with Fastify#

Compression can greatly decrease the size of the response body, thereby increasing the speed of a web app.

For high-traffic websites in production, it is strongly recommended to offload compression from the application server - typically in a reverse proxy (e.g., Nginx). In that case, you should not use compression middleware.

Use the compression middleware package to enable gzip compression.

First install the required package:

Once the installation is complete, apply the compression middleware as global middleware.

If using the FastifyAdapter, you'll want to use fastify-compress:

Once the installation is complete, apply the @fastify/compress middleware as global middleware.

By default, @fastify/compress will use Brotli compression (on Node >= 11.7.0) when browsers indicate support for the encoding. While Brotli can be quite efficient in terms of compression ratio, it can also be quite slow. By default, Brotli sets a maximum compression quality of 11, although it can be adjusted to reduce compression time in lieu of compression quality by adjusting the BROTLI_PARAM_QUALITY between 0 min and 11 max. This will require fine tuning to optimize space/time performance. An example with quality 4:

To simplify, you may want to tell fastify-compress to only use deflate and gzip to compress responses; you'll end up with potentially larger responses but they'll be delivered much more quickly.

To specify encodings, provide a second argument to app.register:

The above tells fastify-compress to only use gzip and deflate encodings, preferring gzip if the client supports both.

**Examples:**

Example 1 (bash):
```bash
$ npm i --save compression
$ npm i --save-dev @types/compression
```

Example 2 (typescript):
```typescript
import * as compression from 'compression';
// somewhere in your initialization file
app.use(compression());
```

Example 3 (bash):
```bash
$ npm i --save @fastify/compress
```

Example 4 (typescript):
```typescript
import { FastifyAdapter, NestFastifyApplication } from '@nestjs/platform-fastify';

import compression from '@fastify/compress';

// inside bootstrap()
const app = await NestFactory.create<NestFastifyApplication>(AppModule, new FastifyAdapter());
await app.register(compression);
```

---

## 

**URL:** https://docs.nestjs.com/techniques/task-scheduling

**Contents:**
  - Task scheduling
    - Installation#
    - Declarative cron jobs#
    - Declarative intervals#
- Official enterprise support
    - Declarative timeouts#
    - Dynamic schedule module API#
    - Dynamic cron jobs#
    - Dynamic intervals#
    - Dynamic timeouts#

Task scheduling allows you to schedule arbitrary code (methods/functions) to execute at a fixed date/time, at recurring intervals, or once after a specified interval. In the Linux world, this is often handled by packages like cron at the OS level. For Node.js apps, there are several packages that emulate cron-like functionality. Nest provides the @nestjs/schedule package, which integrates with the popular Node.js cron package. We'll cover this package in the current chapter.

To begin using it, we first install the required dependencies.

To activate job scheduling, import the ScheduleModule into the root AppModule and run the forRoot() static method as shown below:

The .forRoot() call initializes the scheduler and registers any declarative cron jobs, timeouts and intervals that exist within your app. Registration occurs when the onApplicationBootstrap lifecycle hook occurs, ensuring that all modules have loaded and declared any scheduled jobs.

A cron job schedules an arbitrary function (method call) to run automatically. Cron jobs can run:

Declare a cron job with the @Cron() decorator preceding the method definition containing the code to be executed, as follows:

In this example, the handleCron() method will be called each time the current second is 45. In other words, the method will be run once per minute, at the 45 second mark.

The @Cron() decorator supports the following standard cron patterns:

In the example above, we passed 45 * * * * * to the decorator. The following key shows how each position in the cron pattern string is interpreted:

Some sample cron patterns are:

The @nestjs/schedule package provides a convenient enum with commonly used cron patterns. You can use this enum as follows:

In this example, the handleCron() method will be called every 30 seconds. If an exception occurs, it will be logged to the console, as every method annotated with @Cron() is automatically wrapped in a try-catch block.

Alternatively, you can supply a JavaScript Date object to the @Cron() decorator. Doing so causes the job to execute exactly once, at the specified date.

Also, you can supply additional options as the second parameter to the @Cron() decorator.

You can access and control a cron job after it's been declared, or dynamically create a cron job (where its cron pattern is defined at runtime) with the Dynamic API. To access a declarative cron job via the API, you must associate the job with a name by passing the name property in an optional options object as the second argument of the decorator.

To declare that a method should run at a (recurring) specified interval, prefix the method definition with the @Interval() decorator. Pass the interval value, as a number in milliseconds, to the decorator as shown below:

If you want to control your declarative interval from outside the declaring class via the Dynamic API, associate the interval with a name using the following construction:

If an exception occurs, it will be logged to the console, as every method annotated with @Interval() is automatically wrapped in a try-catch block.

The Dynamic API also enables creating dynamic intervals, where the interval's properties are defined at runtime, and listing and deleting them.

Official enterprise support Providing technical guidance Performing in-depth code reviews Mentoring team members Advising best practices Explore more

To declare that a method should run (once) at a specified timeout, prefix the method definition with the @Timeout() decorator. Pass the relative time offset (in milliseconds), from application startup, to the decorator as shown below:

If an exception occurs, it will be logged to the console, as every method annotated with @Timeout() is automatically wrapped in a try-catch block.

If you want to control your declarative timeout from outside the declaring class via the Dynamic API, associate the timeout with a name using the following construction:

The Dynamic API also enables creating dynamic timeouts, where the timeout's properties are defined at runtime, and listing and deleting them.

The @nestjs/schedule module provides a dynamic API that enables managing declarative cron jobs, timeouts and intervals. The API also enables creating and managing dynamic cron jobs, timeouts and intervals, where the properties are defined at runtime.

Obtain a reference to a CronJob instance by name from anywhere in your code using the SchedulerRegistry API. First, inject SchedulerRegistry using standard constructor injection:

Then use it in a class as follows. Assume a cron job was created with the following declaration:

Access this job using the following:

The getCronJob() method returns the named cron job. The returned CronJob object has the following methods:

Create a new cron job dynamically using the SchedulerRegistry#addCronJob method, as follows:

In this code, we use the CronJob object from the cron package to create the cron job. The CronJob constructor takes a cron pattern (just like the @Cron()decorator) as its first argument, and a callback to be executed when the cron timer fires as its second argument. The SchedulerRegistry#addCronJob method takes two arguments: a name for the CronJob, and the CronJob object itself.

Delete a named cron job using the SchedulerRegistry#deleteCronJob method, as follows:

List all cron jobs using the SchedulerRegistry#getCronJobs method as follows:

The getCronJobs() method returns a map. In this code, we iterate over the map and attempt to access the nextDate() method of each CronJob. In the CronJob API, if a job has already fired and has no future firing date, it throws an exception.

Obtain a reference to an interval with the SchedulerRegistry#getInterval method. As above, inject SchedulerRegistry using standard constructor injection:

And use it as follows:

Create a new interval dynamically using the SchedulerRegistry#addInterval method, as follows:

In this code, we create a standard JavaScript interval, then pass it to the SchedulerRegistry#addInterval method. That method takes two arguments: a name for the interval, and the interval itself.

Delete a named interval using the SchedulerRegistry#deleteInterval method, as follows:

List all intervals using the SchedulerRegistry#getIntervals method as follows:

Obtain a reference to a timeout with the SchedulerRegistry#getTimeout method. As above, inject SchedulerRegistry using standard constructor injection:

And use it as follows:

Create a new timeout dynamically using the SchedulerRegistry#addTimeout method, as follows:

In this code, we create a standard JavaScript timeout, then pass it to the SchedulerRegistry#addTimeout method. That method takes two arguments: a name for the timeout, and the timeout itself.

Delete a named timeout using the SchedulerRegistry#deleteTimeout method, as follows:

List all timeouts using the SchedulerRegistry#getTimeouts method as follows:

A working example is available here.

**Examples:**

Example 1 (bash):
```bash
$ npm install --save @nestjs/schedule
```

Example 2 (typescript):
```typescript
import { Module } from '@nestjs/common';
import { ScheduleModule } from '@nestjs/schedule';

@Module({
  imports: [
    ScheduleModule.forRoot()
  ],
})
export class AppModule {}
```

Example 3 (typescript):
```typescript
import { Injectable, Logger } from '@nestjs/common';
import { Cron } from '@nestjs/schedule';

@Injectable()
export class TasksService {
  private readonly logger = new Logger(TasksService.name);

  @Cron('45 * * * * *')
  handleCron() {
    this.logger.debug('Called when the current second is 45');
  }
}
```

Example 4 (javascript):
```javascript
* * * * * *
| | | | | |
| | | | | day of week
| | | | months
| | | day of month
| | hours
| minutes
seconds (optional)
```

---

## 

**URL:** https://docs.nestjs.com/techniques/file-upload

**Contents:**
  - File upload
    - Basic example#
    - File validation#
    - Array of files#
    - Multiple files#
    - Any files#
    - No files#
    - Default options#
    - Async configuration#
    - Example#

To handle file uploading, Nest provides a built-in module based on the multer middleware package for Express. Multer handles data posted in the multipart/form-data format, which is primarily used for uploading files via an HTTP POST request. This module is fully configurable and you can adjust its behavior to your application requirements.

For better type safety, let's install Multer typings package:

With this package installed, we can now use the Express.Multer.File type (you can import this type as follows: import { Express } from 'express').

To upload a single file, simply tie the FileInterceptor() interceptor to the route handler and extract file from the request using the @UploadedFile() decorator.

The FileInterceptor() decorator takes two arguments:

Often times it can be useful to validate incoming file metadata, like file size or file mime-type. For this, you can create your own Pipe and bind it to the parameter annotated with the UploadedFile decorator. The example below demonstrates how a basic file size validator pipe could be implemented:

This can be used in conjunction with the FileInterceptor as follows:

Nest provides a built-in pipe to handle common use cases and facilitate/standardize the addition of new ones. This pipe is called ParseFilePipe, and you can use it as follows:

As you can see, it's required to specify an array of file validators that will be executed by the ParseFilePipe. We'll discuss the interface of a validator, but it's worth mentioning this pipe also has two additional optional options:

Now, back to the FileValidator interface. To integrate validators with this pipe, you have to either use built-in implementations or provide your own custom FileValidator. See example below:

FileValidator is a regular class that has access to the file object and validates it according to the options provided by the client. Nest has two built-in FileValidator implementations you can use in your project:

To understand how these can be used in conjunction with the aforementioned FileParsePipe, we'll use an altered snippet of the last presented example:

Finally, you can use the special ParseFilePipeBuilder class that lets you compose & construct your validators. By using it as shown below you can avoid manual instantiation of each validator and just pass their options directly:

To upload an array of files (identified with a single field name), use the FilesInterceptor() decorator (note the plural Files in the decorator name). This decorator takes three arguments:

When using FilesInterceptor(), extract files from the request with the @UploadedFiles() decorator.

To upload multiple files (all with different field name keys), use the FileFieldsInterceptor() decorator. This decorator takes two arguments:

When using FileFieldsInterceptor(), extract files from the request with the @UploadedFiles() decorator.

To upload all fields with arbitrary field name keys, use the AnyFilesInterceptor() decorator. This decorator can accept an optional options object as described above.

When using AnyFilesInterceptor(), extract files from the request with the @UploadedFiles() decorator.

To accept multipart/form-data but not allow any files to be uploaded, use the NoFilesInterceptor. This sets multipart data as attributes on the request body. Any files sent with the request will throw a BadRequestException.

You can specify multer options in the file interceptors as described above. To set default options, you can call the static register() method when you import the MulterModule, passing in supported options. You can use all options listed here.

When you need to set MulterModule options asynchronously instead of statically, use the registerAsync() method. As with most dynamic modules, Nest provides several techniques to deal with async configuration.

One technique is to use a factory function:

Like other factory providers, our factory function can be async and can inject dependencies through inject.

Alternatively, you can configure the MulterModule using a class instead of a factory, as shown below:

The construction above instantiates MulterConfigService inside MulterModule, using it to create the required options object. Note that in this example, the MulterConfigService has to implement the MulterOptionsFactory interface, as shown below. The MulterModule will call the createMulterOptions() method on the instantiated object of the supplied class.

If you want to reuse an existing options provider instead of creating a private copy inside the MulterModule, use the useExisting syntax.

You can also pass so-called extraProviders to the registerAsync() method. These providers will be merged with the module providers.

This is useful when you want to provide additional dependencies to the factory function or the class constructor.

A working example is available here.

**Examples:**

Example 1 (shell):
```shell
$ npm i -D @types/multer
```

Example 2 (typescript):
```typescript
@Post('upload')
@UseInterceptors(FileInterceptor('file'))
uploadFile(@UploadedFile() file: Express.Multer.File) {
  console.log(file);
}
```

Example 3 (typescript):
```typescript
@Post('upload')
@UseInterceptors(FileInterceptor('file'))
@Bind(UploadedFile())
uploadFile(file) {
  console.log(file);
}
```

Example 4 (typescript):
```typescript
import { PipeTransform, Injectable, ArgumentMetadata } from '@nestjs/common';

@Injectable()
export class FileSizeValidationPipe implements PipeTransform {
  transform(value: any, metadata: ArgumentMetadata) {
    // "value" is an object containing the file's attributes and metadata
    const oneKb = 1000;
    return value.size < oneKb;
  }
}
```

---

## 

**URL:** https://docs.nestjs.com/techniques/validation

**Contents:**
  - Validation
    - Overview#
    - Using the built-in ValidationPipe#
    - Auto-validation#
    - Disable detailed errors#
    - Stripping properties#
- Learn the right way!
    - Transform payload objects#
    - Explicit conversion#
    - Mapped types#

It is best practice to validate the correctness of any data sent into a web application. To automatically validate incoming requests, Nest provides several pipes available right out-of-the-box:

The ValidationPipe makes use of the powerful class-validator package and its declarative validation decorators. The ValidationPipe provides a convenient approach to enforce validation rules for all incoming client payloads, where the specific rules are declared with simple annotations in local class/DTO declarations in each module.

In the Pipes chapter, we went through the process of building simple pipes and binding them to controllers, methods or to the global app to demonstrate how the process works. Be sure to review that chapter to best understand the topics of this chapter. Here, we'll focus on various real world use cases of the ValidationPipe, and show how to use some of its advanced customization features.

To begin using it, we first install the required dependency.

Because this pipe uses the class-validator and class-transformer libraries, there are many options available. You configure these settings via a configuration object passed to the pipe. Following are the built-in options:

In addition to these, all class-validator options (inherited from the ValidatorOptions interface) are available:

We'll start by binding ValidationPipe at the application level, thus ensuring all endpoints are protected from receiving incorrect data.

To test our pipe, let's create a basic endpoint.

Now we can add a few validation rules in our CreateUserDto. We do this using decorators provided by the class-validator package, described in detail here. In this fashion, any route that uses the CreateUserDto will automatically enforce these validation rules.

With these rules in place, if a request hits our endpoint with an invalid email property in the request body, the application will automatically respond with a 400 Bad Request code, along with the following response body:

In addition to validating request bodies, the ValidationPipe can be used with other request object properties as well. Imagine that we would like to accept :id in the endpoint path. To ensure that only numbers are accepted for this request parameter, we can use the following construct:

FindOneParams, like a DTO, is simply a class that defines validation rules using class-validator. It would look like this:

Error messages can be helpful to explain what was incorrect in a request. However, some production environments prefer to disable detailed errors. Do this by passing an options object to the ValidationPipe:

As a result, detailed error messages won't be displayed in the response body.

Our ValidationPipe can also filter out properties that should not be received by the method handler. In this case, we can whitelist the acceptable properties, and any property not included in the whitelist is automatically stripped from the resulting object. For example, if our handler expects email and password properties, but a request also includes an age property, this property can be automatically removed from the resulting DTO. To enable such behavior, set whitelist to true.

When set to true, this will automatically remove non-whitelisted properties (those without any decorator in the validation class).

Alternatively, you can stop the request from processing when non-whitelisted properties are present, and return an error response to the user. To enable this, set the forbidNonWhitelisted option property to true, in combination with setting whitelist to true.

Learn the right way! 80+ chapters 5+ hours of videos Official certificate Deep-dive sessions Explore official courses

Payloads coming in over the network are plain JavaScript objects. The ValidationPipe can automatically transform payloads to be objects typed according to their DTO classes. To enable auto-transformation, set transform to true. This can be done at a method level:

To enable this behavior globally, set the option on a global pipe:

With the auto-transformation option enabled, the ValidationPipe will also perform conversion of primitive types. In the following example, the findOne() method takes one argument which represents an extracted id path parameter:

By default, every path parameter and query parameter comes over the network as a string. In the above example, we specified the id type as a number (in the method signature). Therefore, the ValidationPipe will try to automatically convert a string identifier to a number.

In the above section, we showed how the ValidationPipe can implicitly transform query and path parameters based on the expected type. However, this feature requires having auto-transformation enabled.

Alternatively (with auto-transformation disabled), you can explicitly cast values using the ParseIntPipe or ParseBoolPipe (note that ParseStringPipe is not needed because, as mentioned earlier, every path parameter and query parameter comes over the network as a string by default).

As you build out features like CRUD (Create/Read/Update/Delete) it's often useful to construct variants on a base entity type. Nest provides several utility functions that perform type transformations to make this task more convenient.

When building input validation types (also called DTOs), it's often useful to build create and update variations on the same type. For example, the create variant may require all fields, while the update variant may make all fields optional.

Nest provides the PartialType() utility function to make this task easier and minimize boilerplate.

The PartialType() function returns a type (class) with all the properties of the input type set to optional. For example, suppose we have a create type as follows:

By default, all of these fields are required. To create a type with the same fields, but with each one optional, use PartialType() passing the class reference (CreateCatDto) as an argument:

The PickType() function constructs a new type (class) by picking a set of properties from an input type. For example, suppose we start with a type like:

We can pick a set of properties from this class using the PickType() utility function:

The OmitType() function constructs a type by picking all properties from an input type and then removing a particular set of keys. For example, suppose we start with a type like:

We can generate a derived type that has every property exceptname as shown below. In this construct, the second argument to OmitType is an array of property names.

The IntersectionType() function combines two types into one new type (class). For example, suppose we start with two types like:

We can generate a new type that combines all properties in both types.

The type mapping utility functions are composable. For example, the following will produce a type (class) that has all of the properties of the CreateCatDto type except for name, and those properties will be set to optional:

TypeScript does not store metadata about generics or interfaces, so when you use them in your DTOs, ValidationPipe may not be able to properly validate incoming data. For instance, in the following code, createUserDtos won't be correctly validated:

To validate the array, create a dedicated class which contains a property that wraps the array, or use the ParseArrayPipe.

In addition, the ParseArrayPipe may come in handy when parsing query parameters. Let's consider a findByIds() method that returns users based on identifiers passed as query parameters.

This construction validates the incoming query parameters from an HTTP GET request like the following:

While this chapter shows examples using HTTP style applications (e.g., Express or Fastify), the ValidationPipe works the same for WebSockets and microservices, regardless of the transport method that is used.

Read more about custom validators, error messages, and available decorators as provided by the class-validator package here.

**Examples:**

Example 1 (bash):
```bash
$ npm i --save class-validator class-transformer
```

Example 2 (typescript):
```typescript
export interface ValidationPipeOptions extends ValidatorOptions {
  transform?: boolean;
  disableErrorMessages?: boolean;
  exceptionFactory?: (errors: ValidationError[]) => any;
}
```

Example 3 (typescript):
```typescript
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalPipes(new ValidationPipe());
  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();
```

Example 4 (typescript):
```typescript
@Post()
create(@Body() createUserDto: CreateUserDto) {
  return 'This action adds a new user';
}
```

---

## 

**URL:** https://docs.nestjs.com/graphql/plugins

**Contents:**
  - Plugins with Apollo
    - Custom plugins#
    - Using external plugins#
    - Plugins with Mercurius#

Plugins enable you to extend Apollo Server's core functionality by performing custom operations in response to certain events. Currently, these events correspond to individual phases of the GraphQL request lifecycle, and to the startup of Apollo Server itself (read more here). For example, a basic logging plugin might log the GraphQL query string associated with each request that's sent to Apollo Server.

To create a plugin, declare a class annotated with the @Plugin decorator exported from the @nestjs/apollo package. Also, for better code autocompletion, implement the ApolloServerPlugin interface from the @apollo/server package.

With this in place, we can register the LoggingPlugin as a provider.

Nest will automatically instantiate a plugin and apply it to the Apollo Server.

There are several plugins provided out-of-the-box. To use an existing plugin, simply import it and add it to the plugins array:

Some of the existing mercurius-specific Fastify plugins must be loaded after the mercurius plugin (read more here) on the plugin tree.

For this, MercuriusDriver exposes an optional plugins configuration option. It represents an array of objects that consist of two attributes: plugin and its options. Therefore, registering the cache plugin would look like this:

**Examples:**

Example 1 (typescript):
```typescript
import { ApolloServerPlugin, GraphQLRequestListener } from '@apollo/server';
import { Plugin } from '@nestjs/apollo';

@Plugin()
export class LoggingPlugin implements ApolloServerPlugin {
  async requestDidStart(): Promise<GraphQLRequestListener<any>> {
    console.log('Request started');
    return {
      async willSendResponse() {
        console.log('Will send response');
      },
    };
  }
}
```

Example 2 (typescript):
```typescript
@Module({
  providers: [LoggingPlugin],
})
export class CommonModule {}
```

Example 3 (typescript):
```typescript
GraphQLModule.forRoot({
  // ...
  plugins: [ApolloServerOperationRegistry({ /* options */})]
}),
```

Example 4 (typescript):
```typescript
GraphQLModule.forRoot({
  driver: MercuriusDriver,
  // ...
  plugins: [
    {
      plugin: cache,
      options: {
        ttl: 10,
        policy: {
          Query: {
            add: true
          }
        }
      },
    }
  ]
}),
```

---

## 

**URL:** https://docs.nestjs.com/techniques/server-sent-events

**Contents:**
  - Server-Sent Events
    - Usage#
    - Example#

Server-Sent Events (SSE) is a server push technology enabling a client to receive automatic updates from a server via HTTP connection. Each notification is sent as a block of text terminated by a pair of newlines (learn more here).

To enable Server-Sent events on a route (route registered within a controller class), annotate the method handler with the @Sse() decorator.

In the example above, we defined a route named sse that will allow us to propagate real-time updates. These events can be listened to using the EventSource API.

The sse method returns an Observable that emits multiple MessageEvent (in this example, it emits a new MessageEvent every second). The MessageEvent object should respect the following interface to match the specification:

With this in place, we can now create an instance of the EventSource class in our client-side application, passing the /sse route (which matches the endpoint we have passed into the @Sse() decorator above) as a constructor argument.

EventSource instance opens a persistent connection to an HTTP server, which sends events in text/event-stream format. The connection remains open until closed by calling EventSource.close().

Once the connection is opened, incoming messages from the server are delivered to your code in the form of events. If there is an event field in the incoming message, the triggered event is the same as the event field value. If no event field is present, then a generic message event is fired (source).

A working example is available here.

**Examples:**

Example 1 (typescript):
```typescript
@Sse('sse')
sse(): Observable<MessageEvent> {
  return interval(1000).pipe(map((_) => ({ data: { hello: 'world' } })));
}
```

Example 2 (typescript):
```typescript
export interface MessageEvent {
  data: string | object;
  id?: string;
  type?: string;
  retry?: number;
}
```

Example 3 (javascript):
```javascript
const eventSource = new EventSource('/sse');
eventSource.onmessage = ({ data }) => {
  console.log('New message', JSON.parse(data));
};
```

---

## 

**URL:** https://docs.nestjs.com/techniques/mvc

**Contents:**
  - Model-View-Controller
    - Template rendering#
    - Dynamic template rendering#
    - Example#
    - Fastify#
    - Example#

Nest, by default, makes use of the Express library under the hood. Hence, every technique for using the MVC (Model-View-Controller) pattern in Express applies to Nest as well.

First, let's scaffold a simple Nest application using the CLI tool:

In order to create an MVC app, we also need a template engine to render our HTML views:

We've used the hbs (Handlebars) engine, though you can use whatever fits your requirements. Once the installation process is complete, we need to configure the express instance using the following code:

We told Express that the public directory will be used for storing static assets, views will contain templates, and the hbs template engine should be used to render HTML output.

Now, let's create a views directory and index.hbs template inside it. In the template, we'll print a message passed from the controller:

Next, open the app.controller file and replace the root() method with the following code:

In this code, we are specifying the template to use in the @Render() decorator, and the return value of the route handler method is passed to the template for rendering. Notice that the return value is an object with a property message, matching the message placeholder we created in the template.

While the application is running, open your browser and navigate to http://localhost:3000. You should see the Hello world! message.

If the application logic must dynamically decide which template to render, then we should use the @Res() decorator, and supply the view name in our route handler, rather than in the @Render() decorator:

A working example is available here.

As mentioned in this chapter, we are able to use any compatible HTTP provider together with Nest. One such library is Fastify. In order to create an MVC application with Fastify, we have to install the following packages:

The next steps cover almost the same process used with Express, with minor differences specific to the platform. Once the installation process is complete, open the main.ts file and update its contents:

The Fastify API has a few differences, but the end result of these method calls is the same. One notable difference is that when using Fastify, the template name you pass into the @Render() decorator must include the file extension.

Here’s how you can set it up:

Alternatively, you can use the @Res() decorator to directly inject the response and specify the view you want to render, as shown below:

While the application is running, open your browser and navigate to http://localhost:3000. You should see the Hello world! message.

A working example is available here.

**Examples:**

Example 1 (bash):
```bash
$ npm i -g @nestjs/cli
$ nest new project
```

Example 2 (bash):
```bash
$ npm install --save hbs
```

Example 3 (typescript):
```typescript
import { NestFactory } from '@nestjs/core';
import { NestExpressApplication } from '@nestjs/platform-express';
import { join } from 'node:path';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create<NestExpressApplication>(
    AppModule,
  );

  app.useStaticAssets(join(__dirname, '..', 'public'));
  app.setBaseViewsDir(join(__dirname, '..', 'views'));
  app.setViewEngine('hbs');

  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();
```

Example 4 (typescript):
```typescript
import { NestFactory } from '@nestjs/core';
import { join } from 'node:path';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(
    AppModule,
  );

  app.useStaticAssets(join(__dirname, '..', 'public'));
  app.setBaseViewsDir(join(__dirname, '..', 'views'));
  app.setViewEngine('hbs');

  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();
```

---

## 

**URL:** https://docs.nestjs.com/techniques/queues

**Contents:**
  - Queues
    - BullMQ installation#
- Official enterprise support
    - Named configurations#
    - Producers#
    - Job options#
    - Consumers#
    - Request-scoped consumers#
    - Event listeners#
    - Queue management#

Queues are a powerful design pattern that help you deal with common application scaling and performance challenges. Some examples of problems that Queues can help you solve are:

Nest provides the @nestjs/bullmq package for BullMQ integration and @nestjs/bull package for Bull integration. Both packages are abstractions/wrappers on top of their respective libraries, which were developed by the same team. Bull is currently in maintenance mode, with the team focusing on fixing bugs, while BullMQ is actively developed, featuring a modern TypeScript implementation and a different set of features. If Bull meets your requirements, it remains a reliable and battle-tested choice. The Nest packages make it easy to integrate both, BullMQ or Bull Queues, into your Nest application in a friendly way.

Both BullMQ and Bull use Redis to persist job data, so you'll need to have Redis installed on your system. Because they are Redis-backed, your Queue architecture can be completely distributed and platform-independent. For example, you can have some Queue producers and consumers and listeners running in Nest on one (or several) nodes, and other producers, consumers and listeners running on other Node.js platforms on other network nodes.

This chapter covers the @nestjs/bullmq and @nestjs/bull packages. We also recommend reading the BullMQ and Bull documentation for more background and specific implementation details.

To begin using BullMQ, we first install the required dependencies.

Once the installation process is complete, we can import the BullModule into the root AppModule.

The forRoot() method is used to register a bullmq package configuration object that will be used by all queues registered in the application (unless specified otherwise). For your reference, the following are a few of the properties within a configuration object:

All the options are optional, providing detailed control over queue behavior. These are passed directly to the BullMQ Queue constructor. Read more about these options and other options here.

To register a queue, import the BullModule.registerQueue() dynamic module, as follows:

The registerQueue() method is used to instantiate and/or register queues. Queues are shared across modules and processes that connect to the same underlying Redis database with the same credentials. Each queue is unique by its name property. A queue name is used as both an injection token (for injecting the queue into controllers/providers), and as an argument to decorators to associate consumer classes and listeners with queues.

You can also override some of the pre-configured options for a specific queue, as follows:

BullMQ also supports parent - child relationships between jobs. This functionality enables the creation of flows where jobs are the node of trees of arbitrary depth. To read more about them check here.

To add a flow, you can do the following:

Since jobs are persisted in Redis, each time a specific named queue is instantiated (e.g., when an app is started/restarted), it attempts to process any old jobs that may exist from a previous unfinished session.

Each queue can have one or many producers, consumers, and listeners. Consumers retrieve jobs from the queue in a specific order: FIFO (the default), LIFO, or according to priorities. Controlling queue processing order is discussed here.

Official enterprise support Providing technical guidance Performing in-depth code reviews Mentoring team members Advising best practices Explore more

If your queues connect to multiple different Redis instances, you can use a technique called named configurations. This feature allows you to register several configurations under specified keys, which then you can refer to in the queue options.

For example, assuming that you have an additional Redis instance (apart from the default one) used by a few queues registered in your application, you can register its configuration as follows:

In the example above, 'alternative-config' is just a configuration key (it can be any arbitrary string).

With this in place, you can now point to this configuration in the registerQueue() options object:

Job producers add jobs to queues. Producers are typically application services (Nest providers). To add jobs to a queue, first inject the queue into the service as follows:

Now, add a job by calling the queue's add() method, passing a user-defined job object. Jobs are represented as serializable JavaScript objects (since that is how they are stored in the Redis database). The shape of the job you pass is arbitrary; use it to represent the semantics of your job object. You also need to give it a name. This allows you to create specialized consumers that will only process jobs with a given name.

Jobs can have additional options associated with them. Pass an options object after the job argument in the Queue.add() method. Some of the job options properties are:

Here are a few examples of customizing jobs with job options.

To delay the start of a job, use the delay configuration property.

To add a job to the right end of the queue (process the job as LIFO (Last In First Out)), set the lifo property of the configuration object to true.

To prioritize a job, use the priority property.

For a full list of options, check the API documentation here and here.

A consumer is a class defining methods that either process jobs added into the queue, or listen for events on the queue, or both. Declare a consumer class using the @Processor() decorator as follows:

Where the decorator's string argument (e.g., 'audio') is the name of the queue to be associated with the class methods.

The process method is called whenever the worker is idle and there are jobs to process in the queue. This handler method receives the job object as its only argument. The value returned by the handler method is stored in the job object and can be accessed later on, for example in a listener for the completed event.

Job objects have multiple methods that allow you to interact with their state. For example, the above code uses the updateProgress() method to update the job's progress. See here for the complete Job object API reference.

In the older version, Bull, you could designate that a job handler method will handle only jobs of a certain type (jobs with a specific name) by passing that name to the @Process() decorator as shown below.

This behavior is not supported in BullMQ due to confusions it generated. Instead, you need switch cases to call different services or logic for each job name:

This is covered in the named processor section of the BullMQ documentation.

When a consumer is flagged as request-scoped (learn more about the injection scopes here), a new instance of the class will be created exclusively for each job. The instance will be garbage-collected after the job has completed.

Since request-scoped consumer classes are instantiated dynamically and scoped to a single job, you can inject a JOB_REF through the constructor using a standard approach.

BullMQ generates a set of useful events when queue and/or job state changes occur. These events can be subscribed to at the Worker level using the @OnWorkerEvent(event) decorator, or at the Queue level with a dedicated listener class and the @OnQueueEvent(event) decorator.

Worker events must be declared within a consumer class (i.e., within a class decorated with the @Processor() decorator). To listen for an event, use the @OnWorkerEvent(event) decorator with the event you want to be handled. For example, to listen to the event emitted when a job enters the active state in the audio queue, use the following construct:

You can see the complete list of events and their arguments as properties of WorkerListener here.

QueueEvent listeners must use the @QueueEventsListener(queue) decorator and extend the QueueEventsHost class provided by @nestjs/bullmq. To listen for an event, use the @OnQueueEvent(event) decorator with the event you want to be handled. For example, to listen to the event emitted when a job enters the active state in the audio queue, use the following construct:

You can see the complete list of events and their arguments as properties of QueueEventsListener here.

Queues have an API that allows you to perform management functions like pausing and resuming, retrieving the count of jobs in various states, and several more. You can find the full queue API here. Invoke any of these methods directly on the Queue object, as shown below with the pause/resume examples.

Pause a queue with the pause() method call. A paused queue will not process new jobs until resumed, but current jobs being processed will continue until they are finalized.

To resume a paused queue, use the resume() method, as follows:

Job handlers can also be run in a separate (forked) process (source). This has several advantages:

You may want to pass bullmq options asynchronously instead of statically. In this case, use the forRootAsync() method which provides several ways to deal with async configuration. Likewise, if you want to pass queue options asynchronously, use the registerQueueAsync() method.

One approach is to use a factory function:

Our factory behaves like any other asynchronous provider (e.g., it can be async and it's able to inject dependencies through inject).

Alternatively, you can use the useClass syntax:

The construction above will instantiate BullConfigService inside BullModule and use it to provide an options object by calling createSharedConfiguration(). Note that this means that the BullConfigService has to implement the SharedBullConfigurationFactory interface, as shown below:

In order to prevent the creation of BullConfigService inside BullModule and use a provider imported from a different module, you can use the useExisting syntax.

This construction works the same as useClass with one critical difference - BullModule will lookup imported modules to reuse an existing ConfigService instead of instantiating a new one.

Likewise, if you want to pass queue options asynchronously, use the registerQueueAsync() method, just keep in mind to specify the name attribute outside the factory function.

By default, BullModule automatically registers BullMQ components (queues, processors, and event listener services) in the onModuleInit lifecycle function. However, in some cases, this behavior may not be ideal. To prevent automatic registration, enable manualRegistration in BullModule like this:

To register these components manually, inject BullRegistrar and call the register function, ideally within OnModuleInit or OnApplicationBootstrap.

Unless you call the BullRegistrar#register function, no BullMQ components will work—meaning no jobs will be processed.

To begin using Bull, we first install the required dependencies.

Once the installation process is complete, we can import the BullModule into the root AppModule.

The forRoot() method is used to register a bull package configuration object that will be used by all queues registered in the application (unless specified otherwise). A configuration object consists of the following properties:

All the options are optional, providing detailed control over queue behavior. These are passed directly to the Bull Queue constructor. Read more about these options here.

To register a queue, import the BullModule.registerQueue() dynamic module, as follows:

The registerQueue() method is used to instantiate and/or register queues. Queues are shared across modules and processes that connect to the same underlying Redis database with the same credentials. Each queue is unique by its name property. A queue name is used as both an injection token (for injecting the queue into controllers/providers), and as an argument to decorators to associate consumer classes and listeners with queues.

You can also override some of the pre-configured options for a specific queue, as follows:

Since jobs are persisted in Redis, each time a specific named queue is instantiated (e.g., when an app is started/restarted), it attempts to process any old jobs that may exist from a previous unfinished session.

Each queue can have one or many producers, consumers, and listeners. Consumers retrieve jobs from the queue in a specific order: FIFO (the default), LIFO, or according to priorities. Controlling queue processing order is discussed here.

Official enterprise support Providing technical guidance Performing in-depth code reviews Mentoring team members Advising best practices Explore more

If your queues connect to multiple Redis instances, you can use a technique called named configurations. This feature allows you to register several configurations under specified keys, which then you can refer to in the queue options.

For example, assuming that you have an additional Redis instance (apart from the default one) used by a few queues registered in your application, you can register its configuration as follows:

In the example above, 'alternative-config' is just a configuration key (it can be any arbitrary string).

With this in place, you can now point to this configuration in the registerQueue() options object:

Job producers add jobs to queues. Producers are typically application services (Nest providers). To add jobs to a queue, first inject the queue into the service as follows:

Now, add a job by calling the queue's add() method, passing a user-defined job object. Jobs are represented as serializable JavaScript objects (since that is how they are stored in the Redis database). The shape of the job you pass is arbitrary; use it to represent the semantics of your job object.

Jobs may have unique names. This allows you to create specialized consumers that will only process jobs with a given name.

Jobs can have additional options associated with them. Pass an options object after the job argument in the Queue.add() method. Job options properties are:

Here are a few examples of customizing jobs with job options.

To delay the start of a job, use the delay configuration property.

To add a job to the right end of the queue (process the job as LIFO (Last In First Out)), set the lifo property of the configuration object to true.

To prioritize a job, use the priority property.

A consumer is a class defining methods that either process jobs added into the queue, or listen for events on the queue, or both. Declare a consumer class using the @Processor() decorator as follows:

Where the decorator's string argument (e.g., 'audio') is the name of the queue to be associated with the class methods.

Within a consumer class, declare job handlers by decorating handler methods with the @Process() decorator.

The decorated method (e.g., transcode()) is called whenever the worker is idle and there are jobs to process in the queue. This handler method receives the job object as its only argument. The value returned by the handler method is stored in the job object and can be accessed later on, for example in a listener for the completed event.

Job objects have multiple methods that allow you to interact with their state. For example, the above code uses the progress() method to update the job's progress. See here for the complete Job object API reference.

You can designate that a job handler method will handle only jobs of a certain type (jobs with a specific name) by passing that name to the @Process() decorator as shown below. You can have multiple @Process() handlers in a given consumer class, corresponding to each job type (name). When you use named jobs, be sure to have a handler corresponding to each name.

When a consumer is flagged as request-scoped (learn more about the injection scopes here), a new instance of the class will be created exclusively for each job. The instance will be garbage-collected after the job has completed.

Since request-scoped consumer classes are instantiated dynamically and scoped to a single job, you can inject a JOB_REF through the constructor using a standard approach.

Bull generates a set of useful events when queue and/or job state changes occur. Nest provides a set of decorators that allow subscribing to a core set of standard events. These are exported from the @nestjs/bull package.

Event listeners must be declared within a consumer class (i.e., within a class decorated with the @Processor() decorator). To listen for an event, use one of the decorators in the table below to declare a handler for the event. For example, to listen to the event emitted when a job enters the active state in the audio queue, use the following construct:

Since Bull operates in a distributed (multi-node) environment, it defines the concept of event locality. This concept recognizes that events may be triggered either entirely within a single process, or on shared queues from different processes. A local event is one that is produced when an action or state change is triggered on a queue in the local process. In other words, when your event producers and consumers are local to a single process, all events happening on queues are local.

When a queue is shared across multiple processes, we encounter the possibility of global events. For a listener in one process to receive an event notification triggered by another process, it must register for a global event.

Event handlers are invoked whenever their corresponding event is emitted. The handler is called with the signature shown in the table below, providing access to information relevant to the event. We discuss one key difference between local and global event handler signatures below.

When listening for global events, the method signatures can be slightly different from their local counterpart. Specifically, any method signature that receives job objects in the local version, instead receives a jobId (number) in the global version. To get a reference to the actual job object in such a case, use the Queue#getJob method. This call should be awaited, and therefore the handler should be declared async. For example:

In addition to the specific event listener decorators, you can also use the generic @OnQueueEvent() decorator in combination with either BullQueueEvents or BullQueueGlobalEvents enums. Read more about events here.

Queue's have an API that allows you to perform management functions like pausing and resuming, retrieving the count of jobs in various states, and several more. You can find the full queue API here. Invoke any of these methods directly on the Queue object, as shown below with the pause/resume examples.

Pause a queue with the pause() method call. A paused queue will not process new jobs until resumed, but current jobs being processed will continue until they are finalized.

To resume a paused queue, use the resume() method, as follows:

Job handlers can also be run in a separate (forked) process (source). This has several advantages:

Please note that because your function is being executed in a forked process, Dependency Injection (and IoC container) won't be available. That means that your processor function will need to contain (or create) all instances of external dependencies it needs.

You may want to pass bull options asynchronously instead of statically. In this case, use the forRootAsync() method which provides several ways to deal with async configuration.

One approach is to use a factory function:

Our factory behaves like any other asynchronous provider (e.g., it can be async and it's able to inject dependencies through inject).

Alternatively, you can use the useClass syntax:

The construction above will instantiate BullConfigService inside BullModule and use it to provide an options object by calling createSharedConfiguration(). Note that this means that the BullConfigService has to implement the SharedBullConfigurationFactory interface, as shown below:

In order to prevent the creation of BullConfigService inside BullModule and use a provider imported from a different module, you can use the useExisting syntax.

This construction works the same as useClass with one critical difference - BullModule will lookup imported modules to reuse an existing ConfigService instead of instantiating a new one.

Likewise, if you want to pass queue options asynchronously, use the registerQueueAsync() method, just keep in mind to specify the name attribute outside the factory function.

A working example is available here.

**Examples:**

Example 1 (bash):
```bash
$ npm install --save @nestjs/bullmq bullmq
```

Example 2 (typescript):
```typescript
import { Module } from '@nestjs/common';
import { BullModule } from '@nestjs/bullmq';

@Module({
  imports: [
    BullModule.forRoot({
      connection: {
        host: 'localhost',
        port: 6379,
      },
    }),
  ],
})
export class AppModule {}
```

Example 3 (typescript):
```typescript
BullModule.registerQueue({
  name: 'audio',
});
```

Example 4 (typescript):
```typescript
BullModule.registerQueue({
  name: 'audio',
  connection: {
    port: 6380,
  },
});
```

---

## 

**URL:** https://docs.nestjs.com/techniques/session

**Contents:**
  - Session
    - Use with Express (default)#
    - Use with Fastify#

HTTP sessions provide a way to store information about the user across multiple requests, which is particularly useful for MVC applications.

First install the required package (and its types for TypeScript users):

Once the installation is complete, apply the express-session middleware as global middleware (for example, in your main.ts file).

The secret is used to sign the session ID cookie. This can be either a string for a single secret, or an array of multiple secrets. If an array of secrets is provided, only the first element will be used to sign the session ID cookie, while all the elements will be considered when verifying the signature in requests. The secret itself should be not easily parsed by a human and would best be a random set of characters.

Enabling the resave option forces the session to be saved back to the session store, even if the session was never modified during the request. The default value is true, but using the default has been deprecated, as the default will change in the future.

Likewise, enabling the saveUninitialized option Forces a session that is "uninitialized" to be saved to the store. A session is uninitialized when it is new but not modified. Choosing false is useful for implementing login sessions, reducing server storage usage, or complying with laws that require permission before setting a cookie. Choosing false will also help with race conditions where a client makes multiple parallel requests without a session (source).

You can pass several other options to the session middleware, read more about them in the API documentation.

With this in place, you can now set and read session values from within the route handlers, as follows:

Alternatively, you can use the @Session() decorator to extract a session object from the request, as follows:

First install the required package:

Once the installation is complete, register the fastify-secure-session plugin:

Read more about the available options in the official repository.

With this in place, you can now set and read session values from within the route handlers, as follows:

Alternatively, you can use the @Session() decorator to extract a session object from the request, as follows:

**Examples:**

Example 1 (shell):
```shell
$ npm i express-session
$ npm i -D @types/express-session
```

Example 2 (typescript):
```typescript
import * as session from 'express-session';
// somewhere in your initialization file
app.use(
  session({
    secret: 'my-secret',
    resave: false,
    saveUninitialized: false,
  }),
);
```

Example 3 (typescript):
```typescript
@Get()
findAll(@Req() request: Request) {
  request.session.visits = request.session.visits ? request.session.visits + 1 : 1;
}
```

Example 4 (typescript):
```typescript
@Get()
findAll(@Session() session: Record<string, any>) {
  session.visits = session.visits ? session.visits + 1 : 1;
}
```

---

## 

**URL:** https://docs.nestjs.com/techniques/logging

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

**URL:** https://docs.nestjs.com/techniques/configuration

**Contents:**
  - Configuration
    - Installation#
    - Getting started#
    - Custom env file path#
    - Disable env variables loading#
    - Use module globally#
    - Custom configuration files#
- Explore your graph with NestJS Devtools
    - Using the ConfigService#
    - Configuration namespaces#

Applications often run in different environments. Depending on the environment, different configuration settings should be used. For example, usually the local environment relies on specific database credentials, valid only for the local DB instance. The production environment would use a separate set of DB credentials. Since configuration variables change, best practice is to store configuration variables in the environment.

Externally defined environment variables are visible inside Node.js through the process.env global. We could try to solve the problem of multiple environments by setting the environment variables separately in each environment. This can quickly get unwieldy, especially in the development and testing environments where these values need to be easily mocked and/or changed.

In Node.js applications, it's common to use .env files, holding key-value pairs where each key represents a particular value, to represent each environment. Running an app in different environments is then just a matter of swapping in the correct .env file.

A good approach for using this technique in Nest is to create a ConfigModule that exposes a ConfigService which loads the appropriate .env file. While you may choose to write such a module yourself, for convenience Nest provides the @nestjs/config package out-of-the box. We'll cover this package in the current chapter.

To begin using it, we first install the required dependency.

Once the installation process is complete, we can import the ConfigModule. Typically, we'll import it into the root AppModule and control its behavior using the .forRoot() static method. During this step, environment variable key/value pairs are parsed and resolved. Later, we'll see several options for accessing the ConfigService class of the ConfigModule in our other feature modules.

The above code will load and parse a .env file from the default location (the project root directory), merge key/value pairs from the .env file with environment variables assigned to process.env, and store the result in a private structure that you can access through the ConfigService. The forRoot() method registers the ConfigService provider, which provides a get() method for reading these parsed/merged configuration variables. Since @nestjs/config relies on dotenv, it uses that package's rules for resolving conflicts in environment variable names. When a key exists both in the runtime environment as an environment variable (e.g., via OS shell exports like export DATABASE_USER=test) and in a .env file, the runtime environment variable takes precedence.

A sample .env file looks something like this:

If you need some env variables to be available even before the ConfigModule is loaded and Nest application is bootstrapped (for example, to pass the microservice configuration to the NestFactory#createMicroservice method), you can use the --env-file option of the Nest CLI. This option allows you to specify the path to the .env file that should be loaded before the application starts. --env-file flag support was introduced in Node v20, see the documentation for more details.

By default, the package looks for a .env file in the root directory of the application. To specify another path for the .env file, set the envFilePath property of an (optional) options object you pass to forRoot(), as follows:

You can also specify multiple paths for .env files like this:

If a variable is found in multiple files, the first one takes precedence.

If you don't want to load the .env file, but instead would like to simply access environment variables from the runtime environment (as with OS shell exports like export DATABASE_USER=test), set the options object's ignoreEnvFile property to true, as follows:

When you want to use ConfigModule in other modules, you'll need to import it (as is standard with any Nest module). Alternatively, declare it as a global module by setting the options object's isGlobal property to true, as shown below. In that case, you will not need to import ConfigModule in other modules once it's been loaded in the root module (e.g., AppModule).

For more complex projects, you may utilize custom configuration files to return nested configuration objects. This allows you to group related configuration settings by function (e.g., database-related settings), and to store related settings in individual files to help manage them independently.

A custom configuration file exports a factory function that returns a configuration object. The configuration object can be any arbitrarily nested plain JavaScript object. The process.env object will contain the fully resolved environment variable key/value pairs (with .env file and externally defined variables resolved and merged as described above). Since you control the returned configuration object, you can add any required logic to cast values to an appropriate type, set default values, etc. For example:

We load this file using the load property of the options object we pass to the ConfigModule.forRoot() method:

With custom configuration files, we can also manage custom files such as YAML files. Here is an example of a configuration using YAML format:

To read and parse YAML files, we can leverage the js-yaml package.

Once the package is installed, we use the yaml#load function to load the YAML file we just created above.

Just a quick note - configuration files aren't automatically validated, even if you're using the validationSchema option in NestJS's ConfigModule. If you need validation or want to apply any transformations, you'll have to handle that within the factory function where you have complete control over the configuration object. This allows you to implement any custom validation logic as needed.

For example, if you want to ensure that port is within a certain range, you can add a validation step to the factory function:

Now, if the port is outside the specified range, the application will throw an error during startup.

Explore your graph with NestJS Devtools Graph visualizer Routes navigator Interactive playground CI/CD integration Sign up

To access configuration values from our ConfigService, we first need to inject ConfigService. As with any provider, we need to import its containing module - the ConfigModule - into the module that will use it (unless you set the isGlobal property in the options object passed to the ConfigModule.forRoot() method to true). Import it into a feature module as shown below.

Then we can inject it using standard constructor injection:

And use it in our class:

As shown above, use the configService.get() method to get a simple environment variable by passing the variable name. You can do TypeScript type hinting by passing the type, as shown above (e.g., get<string>(...)). The get() method can also traverse a nested custom configuration object (created via a Custom configuration file), as shown in the second example above.

You can also get the whole nested custom configuration object using an interface as the type hint:

The get() method also takes an optional second argument defining a default value, which will be returned when the key doesn't exist, as shown below:

ConfigService has two optional generics (type arguments). The first one is to help prevent accessing a config property that does not exist. Use it as shown below:

With the infer property set to true, the ConfigService#get method will automatically infer the property type based on the interface, so for example, typeof port === "number" (if you're not using strictNullChecks flag from TypeScript) since PORT has a number type in the EnvironmentVariables interface.

Also, with the infer feature, you can infer the type of a nested custom configuration object's property, even when using dot notation, as follows:

The second generic relies on the first one, acting as a type assertion to get rid of all undefined types that ConfigService's methods can return when strictNullChecks is on. For instance:

The ConfigModule allows you to define and load multiple custom configuration files, as shown in Custom configuration files above. You can manage complex configuration object hierarchies with nested configuration objects as shown in that section. Alternatively, you can return a "namespaced" configuration object with the registerAs() function as follows:

As with custom configuration files, inside your registerAs() factory function, the process.env object will contain the fully resolved environment variable key/value pairs (with .env file and externally defined variables resolved and merged as described above).

Load a namespaced configuration with the load property of the forRoot() method's options object, in the same way you load a custom configuration file:

Now, to get the host value from the database namespace, use dot notation. Use 'database' as the prefix to the property name, corresponding to the name of the namespace (passed as the first argument to the registerAs() function):

A reasonable alternative is to inject the database namespace directly. This allows us to benefit from strong typing:

To use a namespaced configuration as a configuration object for another module in your application, you can utilize the .asProvider() method of the configuration object. This method converts your namespaced configuration into a provider, which can then be passed to the forRootAsync() (or any equivalent method) of the module you want to use.

To understand how the .asProvider() method functions, let's examine the return value:

This structure allows you to seamlessly integrate namespaced configurations into your modules, ensuring that your application remains organized and modular, without writing boilerplate, repetitive code.

As accessing process.env can be slow, you can set the cache property of the options object passed to ConfigModule.forRoot() to increase the performance of ConfigService#get method when it comes to variables stored in process.env.

Thus far, we've processed configuration files in our root module (e.g., AppModule), with the forRoot() method. Perhaps you have a more complex project structure, with feature-specific configuration files located in multiple different directories. Rather than load all these files in the root module, the @nestjs/config package provides a feature called partial registration, which references only the configuration files associated with each feature module. Use the forFeature() static method within a feature module to perform this partial registration, as follows:

It is standard practice to throw an exception during application startup if required environment variables haven't been provided or if they don't meet certain validation rules. The @nestjs/config package enables two different ways to do this:

To use Joi, we must install Joi package:

Now we can define a Joi validation schema and pass it via the validationSchema property of the forRoot() method's options object, as shown below:

By default, all schema keys are considered optional. Here, we set default values for NODE_ENV and PORT which will be used if we don't provide these variables in the environment (.env file or process environment). Alternatively, we can use the required() validation method to require that a value must be defined in the environment (.env file or process environment). In this case, the validation step will throw an exception if we don't provide the variable in the environment. See Joi validation methods for more on how to construct validation schemas.

By default, unknown environment variables (environment variables whose keys are not present in the schema) are allowed and do not trigger a validation exception. By default, all validation errors are reported. You can alter these behaviors by passing an options object via the validationOptions key of the forRoot() options object. This options object can contain any of the standard validation options properties provided by Joi validation options. For example, to reverse the two settings above, pass options like this:

The @nestjs/config package uses default settings of:

Note that once you decide to pass a validationOptions object, any settings you do not explicitly pass will default to Joi standard defaults (not the @nestjs/config defaults). For example, if you leave allowUnknowns unspecified in your custom validationOptions object, it will have the Joi default value of false. Hence, it is probably safest to specify both of these settings in your custom object.

Alternatively, you can specify a synchronousvalidate function that takes an object containing the environment variables (from env file and process) and returns an object containing validated environment variables so that you can convert/mutate them if needed. If the function throws an error, it will prevent the application from bootstrapping.

In this example, we'll proceed with the class-transformer and class-validator packages. First, we have to define:

With this in place, use the validate function as a configuration option of the ConfigModule, as follows:

ConfigService defines a generic get() method to retrieve a configuration value by key. We may also add getter functions to enable a little more natural coding style:

Now we can use the getter function as follows:

If a module configuration depends on the environment variables, and these variables are loaded from the .env file, you can use the ConfigModule.envVariablesLoaded hook to ensure that the file was loaded before interacting with the process.env object, see the following example:

This construction guarantees that after the ConfigModule.envVariablesLoaded Promise resolves, all configuration variables are loaded up.

There may be times where you want to conditionally load in a module and specify the condition in an env variable. Fortunately, @nestjs/config provides a ConditionalModule that allows you to do just that.

The above module would only load in the FooModule if in the .env file there is not a false value for the env variable USE_FOO. You can also pass a custom condition yourself, a function receiving the process.env reference that should return a boolean for the ConditionalModule to handle:

It is important to be sure that when using the ConditionalModule you also have the ConfigModule loaded in the application, so that the ConfigModule.envVariablesLoaded hook can be properly referenced and utilized. If the hook is not flipped to true within 5 seconds, or a timeout in milliseconds, set by the user in the third options parameter of the registerWhen method, then the ConditionalModule will throw an error and Nest will abort starting the application.

The @nestjs/config package supports environment variable expansion. With this technique, you can create nested environment variables, where one variable is referred to within the definition of another. For example:

With this construction, the variable SUPPORT_EMAIL resolves to 'support@mywebsite.com'. Note the use of the ${...} syntax to trigger resolving the value of the variable APP_URL inside the definition of SUPPORT_EMAIL.

Enable environment variable expansion using the expandVariables property in the options object passed to the forRoot() method of the ConfigModule, as shown below:

While our config is stored in a service, it can still be used in the main.ts file. This way, you can use it to store variables such as the application port or the CORS host.

To access it, you must use the app.get() method, followed by the service reference:

You can then use it as usual, by calling the get method with the configuration key:

**Examples:**

Example 1 (bash):
```bash
$ npm i --save @nestjs/config
```

Example 2 (typescript):
```typescript
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';

@Module({
  imports: [ConfigModule.forRoot()],
})
export class AppModule {}
```

Example 3 (json):
```json
DATABASE_USER=test
DATABASE_PASSWORD=test
```

Example 4 (bash):
```bash
$ nest start --env-file .env
```

---

## 

**URL:** https://docs.nestjs.com/techniques/performance

**Contents:**
  - Performance (Fastify)
    - Installation#
    - Adapter#
    - Platform specific packages#
    - Redirect response#
    - Fastify options#
    - Middleware#
    - Route Config#
    - Route Constraints#
    - Example#

By default, Nest makes use of the Express framework. As mentioned earlier, Nest also provides compatibility with other libraries such as, for example, Fastify. Nest achieves this framework independence by implementing a framework adapter whose primary function is to proxy middleware and handlers to appropriate library-specific implementations.

Fastify provides a good alternative framework for Nest because it solves design issues in a similar manner to Express. However, fastify is much faster than Express, achieving almost two times better benchmarks results. A fair question is why does Nest use Express as the default HTTP provider? The reason is that Express is widely-used, well-known, and has an enormous set of compatible middleware, which is available to Nest users out-of-the-box.

But since Nest provides framework-independence, you can easily migrate between them. Fastify can be a better choice when you place high value on very fast performance. To utilize Fastify, simply choose the built-in FastifyAdapter as shown in this chapter.

First, we need to install the required package:

Once the Fastify platform is installed, we can use the FastifyAdapter.

By default, Fastify listens only on the localhost 127.0.0.1 interface (read more). If you want to accept connections on other hosts, you should specify '0.0.0.0' in the listen() call:

Keep in mind that when you use the FastifyAdapter, Nest uses Fastify as the HTTP provider. This means that each recipe that relies on Express may no longer work. You should, instead, use Fastify equivalent packages.

Fastify handles redirect responses slightly differently than Express. To do a proper redirect with Fastify, return both the status code and the URL, as follows:

You can pass options into the Fastify constructor through the FastifyAdapter constructor. For example:

Middleware functions retrieve the raw req and res objects instead of Fastify's wrappers. This is how the middie package works (that's used under the hood) and fastify - check out this page for more information,

You can use the route config feature of Fastify with the @RouteConfig() decorator.

As of v10.3.0, @nestjs/platform-fastify supports route constraints feature of Fastify with @RouteConstraints decorator.

A working example is available here.

**Examples:**

Example 1 (bash):
```bash
$ npm i --save @nestjs/platform-fastify
```

Example 2 (typescript):
```typescript
import { NestFactory } from '@nestjs/core';
import {
  FastifyAdapter,
  NestFastifyApplication,
} from '@nestjs/platform-fastify';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create<NestFastifyApplication>(
    AppModule,
    new FastifyAdapter()
  );
  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();
```

Example 3 (typescript):
```typescript
async function bootstrap() {
  const app = await NestFactory.create<NestFastifyApplication>(
    AppModule,
    new FastifyAdapter(),
  );
  await app.listen(3000, '0.0.0.0');
}
```

Example 4 (typescript):
```typescript
@Get()
index(@Res() res) {
  res.status(302).redirect('/login');
}
```

---

## 

**URL:** https://docs.nestjs.com/techniques/caching

**Contents:**
  - Caching
    - Installation#
    - In-memory cache#
    - Interacting with the Cache store#
    - Auto-caching responses#
    - Time-to-live (TTL)#
    - Use module globally#
    - Global cache overrides#
    - WebSockets and Microservices#
    - Adjust tracking#

Caching is a powerful and straightforward technique for enhancing your application's performance. By acting as a temporary storage layer, it allows for quicker access to frequently used data, reducing the need to repeatedly fetch or compute the same information. This results in faster response times and improved overall efficiency.

To get started with caching in Nest, you need to install the @nestjs/cache-manager package along with the cache-manager package.

By default, everything is stored in memory; Since cache-manager uses Keyv under the hood, you can easily switch to a more advanced storage solution, such as Redis, by installing the appropriate package. We'll cover this in more detail later.

To enable caching in your application, import the CacheModule and configure it using the register() method:

This setup initializes in-memory caching with default settings, allowing you to start caching data immediately.

To interact with the cache manager instance, inject it to your class using the CACHE_MANAGER token, as follows:

The get method on the Cache instance (from the cache-manager package) is used to retrieve items from the cache. If the item does not exist in the cache, null will be returned.

To add an item to the cache, use the set method:

You can manually specify a TTL (expiration time in milliseconds) for this specific key, as follows:

Where 1000 is the TTL in milliseconds - in this case, the cache item will expire after one second.

To disable expiration of the cache, set the ttl configuration property to 0:

To remove an item from the cache, use the del method:

To clear the entire cache, use the clear method:

To enable auto-caching responses, just tie the CacheInterceptor where you want to cache data.

To reduce the amount of required boilerplate, you can bind CacheInterceptor to all endpoints globally:

The default value for ttl is 0, meaning the cache will never expire. To specify a custom TTL, you can provide the ttl option in the register() method, as demonstrated below:

When you want to use CacheModule in other modules, you'll need to import it (as is standard with any Nest module). Alternatively, declare it as a global module by setting the options object's isGlobal property to true, as shown below. In that case, you will not need to import CacheModule in other modules once it's been loaded in the root module (e.g., AppModule).

While global cache is enabled, cache entries are stored under a CacheKey that is auto-generated based on the route path. You may override certain cache settings (@CacheKey() and @CacheTTL()) on a per-method basis, allowing customized caching strategies for individual controller methods. This may be most relevant while using different cache stores.

You can apply the @CacheTTL() decorator on a per-controller basis to set a caching TTL for the entire controller. In situations where both controller-level and method-level cache TTL settings are defined, the cache TTL settings specified at the method level will take priority over the ones set at the controller level.

The @CacheKey() decorator may be used with or without a corresponding @CacheTTL() decorator and vice versa. One may choose to override only the @CacheKey() or only the @CacheTTL(). Settings that are not overridden with a decorator will use the default values as registered globally (see Customize caching).

You can also apply the CacheInterceptor to WebSocket subscribers as well as Microservice's patterns (regardless of the transport method that is being used).

However, the additional @CacheKey() decorator is required in order to specify a key used to subsequently store and retrieve cached data. Also, please note that you shouldn't cache everything. Actions which perform some business operations rather than simply querying the data should never be cached.

Additionally, you may specify a cache expiration time (TTL) by using the @CacheTTL() decorator, which will override the global default TTL value.

By default, Nest uses the request URL (in an HTTP app) or cache key (in websockets and microservices apps, set through the @CacheKey() decorator) to associate cache records with your endpoints. Nevertheless, sometimes you might want to set up tracking based on different factors, for example, using HTTP headers (e.g. Authorization to properly identify profile endpoints).

In order to accomplish that, create a subclass of CacheInterceptor and override the trackBy() method.

Switching to a different cache store is straightforward. First, install the appropriate package. For example, to use Redis, install the @keyv/redis package:

With this in place, you can register the CacheModule with multiple stores as shown below:

In this example, we've registered two stores: CacheableMemory and KeyvRedis. The CacheableMemory store is a simple in-memory store, while KeyvRedis is a Redis store. The stores array is used to specify the stores you want to use. The first store in the array is the default store, and the rest are fallback stores.

Check out the Keyv documentation for more information on available stores.

You may want to asynchronously pass in module options instead of passing them statically at compile time. In this case, use the registerAsync() method, which provides several ways to deal with async configuration.

One approach is to use a factory function:

Our factory behaves like all other asynchronous module factories (it can be async and is able to inject dependencies through inject).

Alternatively, you can use the useClass method:

The above construction will instantiate CacheConfigService inside CacheModule and will use it to get the options object. The CacheConfigService has to implement the CacheOptionsFactory interface in order to provide the configuration options:

If you wish to use an existing configuration provider imported from a different module, use the useExisting syntax:

This works the same as useClass with one critical difference - CacheModule will lookup imported modules to reuse any already-created ConfigService, instead of instantiating its own.

You can also pass so-called extraProviders to the registerAsync() method. These providers will be merged with the module providers.

This is useful when you want to provide additional dependencies to the factory function or the class constructor.

A working example is available here.

**Examples:**

Example 1 (bash):
```bash
$ npm install @nestjs/cache-manager cache-manager
```

Example 2 (typescript):
```typescript
import { Module } from '@nestjs/common';
import { CacheModule } from '@nestjs/cache-manager';
import { AppController } from './app.controller';

@Module({
  imports: [CacheModule.register()],
  controllers: [AppController],
})
export class AppModule {}
```

Example 3 (typescript):
```typescript
constructor(@Inject(CACHE_MANAGER) private cacheManager: Cache) {}
```

Example 4 (typescript):
```typescript
const value = await this.cacheManager.get('key');
```

---

## 

**URL:** https://docs.nestjs.com/techniques/database

**Contents:**
  - Database
  - TypeORM Integration
    - Repository pattern#
    - Relations#
    - Auto-load entities#
    - Separating entity definition#
    - TypeORM Transactions#
- Explore your graph with NestJS Devtools
    - Subscribers#
    - Migrations#

Nest is database agnostic, allowing you to easily integrate with any SQL or NoSQL database. You have a number of options available to you, depending on your preferences. At the most general level, connecting Nest to a database is simply a matter of loading an appropriate Node.js driver for the database, just as you would with Express or Fastify.

You can also directly use any general purpose Node.js database integration library or ORM, such as MikroORM (see MikroORM recipe), Sequelize (see Sequelize integration), Knex.js (see Knex.js tutorial), TypeORM, and Prisma (see Prisma recipe), to operate at a higher level of abstraction.

For convenience, Nest provides tight integration with TypeORM and Sequelize out-of-the-box with the @nestjs/typeorm and @nestjs/sequelize packages respectively, which we'll cover in the current chapter, and Mongoose with @nestjs/mongoose, which is covered in this chapter. These integrations provide additional NestJS-specific features, such as model/repository injection, testability, and asynchronous configuration to make accessing your chosen database even easier.

For integrating with SQL and NoSQL databases, Nest provides the @nestjs/typeorm package. TypeORM is the most mature Object Relational Mapper (ORM) available for TypeScript. Since it's written in TypeScript, it integrates well with the Nest framework.

To begin using it, we first install the required dependencies. In this chapter, we'll demonstrate using the popular MySQL Relational DBMS, but TypeORM provides support for many relational databases, such as PostgreSQL, Oracle, Microsoft SQL Server, SQLite, and even NoSQL databases like MongoDB. The procedure we walk through in this chapter will be the same for any database supported by TypeORM. You'll simply need to install the associated client API libraries for your selected database.

Once the installation process is complete, we can import the TypeOrmModule into the root AppModule.

The forRoot() method supports all the configuration properties exposed by the DataSource constructor from the TypeORM package. In addition, there are several extra configuration properties described below.

Once this is done, the TypeORM DataSource and EntityManager objects will be available to inject across the entire project (without needing to import any modules), for example:

TypeORM supports the repository design pattern, so each entity has its own repository. These repositories can be obtained from the database data source.

To continue the example, we need at least one entity. Let's define the User entity.

The User entity file sits in the users directory. This directory contains all files related to the UsersModule. You can decide where to keep your model files, however, we recommend creating them near their domain, in the corresponding module directory.

To begin using the User entity, we need to let TypeORM know about it by inserting it into the entities array in the module forRoot() method options (unless you use a static glob path):

Next, let's look at the UsersModule:

This module uses the forFeature() method to define which repositories are registered in the current scope. With that in place, we can inject the UsersRepository into the UsersService using the @InjectRepository() decorator:

If you want to use the repository outside of the module which imports TypeOrmModule.forFeature, you'll need to re-export the providers generated by it. You can do this by exporting the whole module, like this:

Now if we import UsersModule in UserHttpModule, we can use @InjectRepository(User) in the providers of the latter module.

Relations are associations established between two or more tables. Relations are based on common fields from each table, often involving primary and foreign keys.

There are three types of relations:

To define relations in entities, use the corresponding decorators. For example, to define that each User can have multiple photos, use the @OneToMany() decorator.

Manually adding entities to the entities array of the data source options can be tedious. In addition, referencing entities from the root module breaks application domain boundaries and causes leaking implementation details to other parts of the application. To address this issue, an alternative solution is provided. To automatically load entities, set the autoLoadEntities property of the configuration object (passed into the forRoot() method) to true, as shown below:

With that option specified, every entity registered through the forFeature() method will be automatically added to the entities array of the configuration object.

You can define an entity and its columns right in the model, using decorators. But some people prefer to define entities and their columns inside separate files using the "entity schemas".

Nest allows you to use an EntitySchema instance wherever an Entity is expected, for example:

A database transaction symbolizes a unit of work performed within a database management system against a database, and treated in a coherent and reliable way independent of other transactions. A transaction generally represents any change in a database (learn more).

There are many different strategies to handle TypeORM transactions. We recommend using the QueryRunner class because it gives full control over the transaction.

First, we need to inject the DataSource object into a class in the normal way:

Now, we can use this object to create a transaction.

Explore your graph with NestJS Devtools Graph visualizer Routes navigator Interactive playground CI/CD integration Sign up

Alternatively, you can use the callback-style approach with the transaction method of the DataSource object (read more).

With TypeORM subscribers, you can listen to specific entity events.

Now, add the UserSubscriber class to the providers array:

Migrations provide a way to incrementally update the database schema to keep it in sync with the application's data model while preserving existing data in the database. To generate, run, and revert migrations, TypeORM provides a dedicated CLI.

Migration classes are separate from the Nest application source code. Their lifecycle is maintained by the TypeORM CLI. Therefore, you are not able to leverage dependency injection and other Nest specific features with migrations. To learn more about migrations, follow the guide in the TypeORM documentation.

Some projects require multiple database connections. This can also be achieved with this module. To work with multiple connections, first create the connections. In this case, data source naming becomes mandatory.

Suppose you have an Album entity stored in its own database.

See this issue for more details.

At this point, you have User and Album entities registered with their own data source. With this setup, you have to tell the TypeOrmModule.forFeature() method and the @InjectRepository() decorator which data source should be used. If you do not pass any data source name, the default data source is used.

You can also inject the DataSource or EntityManager for a given data source:

It's also possible to inject any DataSource to the providers:

When it comes to unit testing an application, we usually want to avoid making a database connection, keeping our test suites independent and their execution process as fast as possible. But our classes might depend on repositories that are pulled from the data source (connection) instance. How do we handle that? The solution is to create mock repositories. In order to achieve that, we set up custom providers. Each registered repository is automatically represented by an <EntityName>Repository token, where EntityName is the name of your entity class.

The @nestjs/typeorm package exposes the getRepositoryToken() function which returns a prepared token based on a given entity.

Now a substitute mockRepository will be used as the UsersRepository. Whenever any class asks for UsersRepository using an @InjectRepository() decorator, Nest will use the registered mockRepository object.

You may want to pass your repository module options asynchronously instead of statically. In this case, use the forRootAsync() method, which provides several ways to deal with async configuration.

One approach is to use a factory function:

Our factory behaves like any other asynchronous provider (e.g., it can be async and it's able to inject dependencies through inject).

Alternatively, you can use the useClass syntax:

The construction above will instantiate TypeOrmConfigService inside TypeOrmModule and use it to provide an options object by calling createTypeOrmOptions(). Note that this means that the TypeOrmConfigService has to implement the TypeOrmOptionsFactory interface, as shown below:

In order to prevent the creation of TypeOrmConfigService inside TypeOrmModule and use a provider imported from a different module, you can use the useExisting syntax.

This construction works the same as useClass with one critical difference - TypeOrmModule will lookup imported modules to reuse an existing ConfigService instead of instantiating a new one.

In conjunction with async configuration using useFactory, useClass, or useExisting, you can optionally specify a dataSourceFactory function which will allow you to provide your own TypeORM data source rather than allowing TypeOrmModule to create the data source.

dataSourceFactory receives the TypeORM DataSourceOptions configured during async configuration using useFactory, useClass, or useExisting and returns a Promise that resolves a TypeORM DataSource.

A working example is available here.

Official enterprise support Providing technical guidance Performing in-depth code reviews Mentoring team members Advising best practices Explore more

An alternative to using TypeORM is to use the Sequelize ORM with the @nestjs/sequelize package. In addition, we leverage the sequelize-typescript package which provides a set of additional decorators to declaratively define entities.

To begin using it, we first install the required dependencies. In this chapter, we'll demonstrate using the popular MySQL Relational DBMS, but Sequelize provides support for many relational databases, such as PostgreSQL, MySQL, Microsoft SQL Server, SQLite, and MariaDB. The procedure we walk through in this chapter will be the same for any database supported by Sequelize. You'll simply need to install the associated client API libraries for your selected database.

Once the installation process is complete, we can import the SequelizeModule into the root AppModule.

The forRoot() method supports all the configuration properties exposed by the Sequelize constructor (read more). In addition, there are several extra configuration properties described below.

Once this is done, the Sequelize object will be available to inject across the entire project (without needing to import any modules), for example:

Sequelize implements the Active Record pattern. With this pattern, you use model classes directly to interact with the database. To continue the example, we need at least one model. Let's define the User model.

The User model file sits in the users directory. This directory contains all files related to the UsersModule. You can decide where to keep your model files, however, we recommend creating them near their domain, in the corresponding module directory.

To begin using the User model, we need to let Sequelize know about it by inserting it into the models array in the module forRoot() method options:

Next, let's look at the UsersModule:

This module uses the forFeature() method to define which models are registered in the current scope. With that in place, we can inject the UserModel into the UsersService using the @InjectModel() decorator:

If you want to use the model outside of the module which imports SequelizeModule.forFeature, you'll need to re-export the providers generated by it. You can do this by exporting the whole module, like this:

Now if we import UsersModule in UserHttpModule, we can use @InjectModel(User) in the providers of the latter module.

Relations are associations established between two or more tables. Relations are based on common fields from each table, often involving primary and foreign keys.

There are three types of relations:

To define relations in models, use the corresponding decorators. For example, to define that each User can have multiple photos, use the @HasMany() decorator.

Manually adding models to the models array of the connection options can be tedious. In addition, referencing models from the root module breaks application domain boundaries and causes leaking implementation details to other parts of the application. To solve this issue, automatically load models by setting both autoLoadModels and synchronize properties of the configuration object (passed into the forRoot() method) to true, as shown below:

With that option specified, every model registered through the forFeature() method will be automatically added to the models array of the configuration object.

A database transaction symbolizes a unit of work performed within a database management system against a database, and treated in a coherent and reliable way independent of other transactions. A transaction generally represents any change in a database (learn more).

There are many different strategies to handle Sequelize transactions. Below is a sample implementation of a managed transaction (auto-callback).

First, we need to inject the Sequelize object into a class in the normal way:

Now, we can use this object to create a transaction.

Migrations provide a way to incrementally update the database schema to keep it in sync with the application's data model while preserving existing data in the database. To generate, run, and revert migrations, Sequelize provides a dedicated CLI.

Migration classes are separate from the Nest application source code. Their lifecycle is maintained by the Sequelize CLI. Therefore, you are not able to leverage dependency injection and other Nest specific features with migrations. To learn more about migrations, follow the guide in the Sequelize documentation.

Learn the right way! 80+ chapters 5+ hours of videos Official certificate Deep-dive sessions Explore official courses

Some projects require multiple database connections. This can also be achieved with this module. To work with multiple connections, first create the connections. In this case, connection naming becomes mandatory.

Suppose you have an Album entity stored in its own database.

At this point, you have User and Album models registered with their own connection. With this setup, you have to tell the SequelizeModule.forFeature() method and the @InjectModel() decorator which connection should be used. If you do not pass any connection name, the default connection is used.

You can also inject the Sequelize instance for a given connection:

It's also possible to inject any Sequelize instance to the providers:

When it comes to unit testing an application, we usually want to avoid making a database connection, keeping our test suites independent and their execution process as fast as possible. But our classes might depend on models that are pulled from the connection instance. How do we handle that? The solution is to create mock models. In order to achieve that, we set up custom providers. Each registered model is automatically represented by a <ModelName>Model token, where ModelName is the name of your model class.

The @nestjs/sequelize package exposes the getModelToken() function which returns a prepared token based on a given model.

Now a substitute mockModel will be used as the UserModel. Whenever any class asks for UserModel using an @InjectModel() decorator, Nest will use the registered mockModel object.

You may want to pass your SequelizeModule options asynchronously instead of statically. In this case, use the forRootAsync() method, which provides several ways to deal with async configuration.

One approach is to use a factory function:

Our factory behaves like any other asynchronous provider (e.g., it can be async and it's able to inject dependencies through inject).

Alternatively, you can use the useClass syntax:

The construction above will instantiate SequelizeConfigService inside SequelizeModule and use it to provide an options object by calling createSequelizeOptions(). Note that this means that the SequelizeConfigService has to implement the SequelizeOptionsFactory interface, as shown below:

In order to prevent the creation of SequelizeConfigService inside SequelizeModule and use a provider imported from a different module, you can use the useExisting syntax.

This construction works the same as useClass with one critical difference - SequelizeModule will lookup imported modules to reuse an existing ConfigService instead of instantiating a new one.

A working example is available here.

**Examples:**

Example 1 (bash):
```bash
$ npm install --save @nestjs/typeorm typeorm mysql2
```

Example 2 (typescript):
```typescript
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'mysql',
      host: 'localhost',
      port: 3306,
      username: 'root',
      password: 'root',
      database: 'test',
      entities: [],
      synchronize: true,
    }),
  ],
})
export class AppModule {}
```

Example 3 (typescript):
```typescript
import { DataSource } from 'typeorm';

@Module({
  imports: [TypeOrmModule.forRoot(), UsersModule],
})
export class AppModule {
  constructor(private dataSource: DataSource) {}
}
```

Example 4 (typescript):
```typescript
import { DataSource } from 'typeorm';

@Dependencies(DataSource)
@Module({
  imports: [TypeOrmModule.forRoot(), UsersModule],
})
export class AppModule {
  constructor(dataSource) {
    this.dataSource = dataSource;
  }
}
```

---

## 

**URL:** https://docs.nestjs.com/techniques/events

**Contents:**
  - Events
    - Getting started#
    - Dispatching events#
    - Listening to events#
    - Preventing event loss#
    - Example#

Event Emitter package (@nestjs/event-emitter) provides a simple observer implementation, allowing you to subscribe and listen for various events that occur in your application. Events serve as a great way to decouple various aspects of your application, since a single event can have multiple listeners that do not depend on each other.

EventEmitterModule internally uses the eventemitter2 package.

First install the required package:

Once the installation is complete, import the EventEmitterModule into the root AppModule and run the forRoot() static method as shown below:

The .forRoot() call initializes the event emitter and registers any declarative event listeners that exist within your app. Registration occurs when the onApplicationBootstrap lifecycle hook occurs, ensuring that all modules have loaded and declared any scheduled jobs.

To configure the underlying EventEmitter instance, pass the configuration object to the .forRoot() method, as follows:

To dispatch (i.e., fire) an event, first inject EventEmitter2 using standard constructor injection:

Then use it in a class as follows:

To declare an event listener, decorate a method with the @OnEvent() decorator preceding the method definition containing the code to be executed, as follows:

The first argument can be a string or symbol for a simple event emitter and a string | symbol | Array<string | symbol> in a case of a wildcard emitter.

The second argument (optional) is a listener options object as follows:

To use namespaces/wildcards, pass the wildcard option into the EventEmitterModule#forRoot() method. When namespaces/wildcards are enabled, events can either be strings (foo.bar) separated by a delimiter or arrays (['foo', 'bar']). The delimiter is also configurable as a configuration property (delimiter). With namespaces feature enabled, you can subscribe to events using a wildcard:

Note that such a wildcard only applies to one block. The argument order.* will match, for example, the events order.created and order.shipped but not order.delayed.out_of_stock. In order to listen to such events, use the multilevel wildcard pattern (i.e, **), described in the EventEmitter2documentation.

With this pattern, you can, for example, create an event listener that catches all events.

Events triggered before or during the onApplicationBootstrap lifecycle hook—such as those from module constructors or the onModuleInit method—may be missed because the EventSubscribersLoader might not have finished setting up the listeners.

To avoid this issue, you can use the waitUntilReady method of the EventEmitterReadinessWatcher, which returns a promise that resolves once all listeners have been registered. This method can be called in the onApplicationBootstrap lifecycle hook of a module to ensure that all events are properly captured.

A working example is available here.

**Examples:**

Example 1 (shell):
```shell
$ npm i --save @nestjs/event-emitter
```

Example 2 (typescript):
```typescript
import { Module } from '@nestjs/common';
import { EventEmitterModule } from '@nestjs/event-emitter';

@Module({
  imports: [
    EventEmitterModule.forRoot()
  ],
})
export class AppModule {}
```

Example 3 (typescript):
```typescript
EventEmitterModule.forRoot({
  // set this to `true` to use wildcards
  wildcard: false,
  // the delimiter used to segment namespaces
  delimiter: '.',
  // set this to `true` if you want to emit the newListener event
  newListener: false,
  // set this to `true` if you want to emit the removeListener event
  removeListener: false,
  // the maximum amount of listeners that can be assigned to an event
  maxListeners: 10,
  // show event name in memory leak message when more than maximum amount of listeners is assigned
  verboseMemoryLeak: false,
  // disable throwing uncaughtException if an error event is emitted and it has no listeners
  ignoreErrors: false,
});
```

Example 4 (typescript):
```typescript
constructor(private eventEmitter: EventEmitter2) {}
```

---

## 

**URL:** https://docs.nestjs.com/techniques/serialization

**Contents:**
  - Serialization
    - Overview#
    - Exclude properties#
    - Expose properties#
    - Transform#
    - Pass options#
    - Transform plain objects#
    - Example#
    - WebSockets and Microservices#
    - Learn more#

Serialization is a process that happens before objects are returned in a network response. This is an appropriate place to provide rules for transforming and sanitizing the data to be returned to the client. For example, sensitive data like passwords should always be excluded from the response. Or, certain properties might require additional transformation, such as sending only a subset of properties of an entity. Performing these transformations manually can be tedious and error prone, and can leave you uncertain that all cases have been covered.

Nest provides a built-in capability to help ensure that these operations can be performed in a straightforward way. The ClassSerializerInterceptor interceptor uses the powerful class-transformer package to provide a declarative and extensible way of transforming objects. The basic operation it performs is to take the value returned by a method handler and apply the instanceToPlain() function from class-transformer. In doing so, it can apply rules expressed by class-transformer decorators on an entity/DTO class, as described below.

Let's assume that we want to automatically exclude a password property from a user entity. We annotate the entity as follows:

Now consider a controller with a method handler that returns an instance of this class.

When this endpoint is requested, the client receives the following response:

Note that the interceptor can be applied application-wide (as covered here). The combination of the interceptor and the entity class declaration ensures that any method that returns a UserEntity will be sure to remove the password property. This gives you a measure of centralized enforcement of this business rule.

You can use the @Expose() decorator to provide alias names for properties, or to execute a function to calculate a property value (analogous to getter functions), as shown below.

You can perform additional data transformation using the @Transform() decorator. For example, the following construct returns the name property of the RoleEntity instead of returning the whole object.

You may want to modify the default behavior of the transformation functions. To override default settings, pass them in an options object with the @SerializeOptions() decorator.

Options passed via @SerializeOptions() are passed as the second argument of the underlying instanceToPlain() function. In this example, we are automatically excluding all properties that begin with the _ prefix.

You can enforce transformations at the controller level by using the @SerializeOptions decorator. This ensures that all responses are transformed into instances of the specified class, applying any decorators from class-validator or class-transformer, even when plain objects are returned. This approach leads to cleaner code without the need to repeatedly instantiate the class or call plainToInstance.

In the example below, despite returning plain JavaScript objects in both conditional branches, they will be automatically converted into UserEntity instances, with the relevant decorators applied:

A working example is available here.

While this chapter shows examples using HTTP style applications (e.g., Express or Fastify), the ClassSerializerInterceptor works the same for WebSockets and Microservices, regardless of the transport method that is used.

Read more about available decorators and options as provided by the class-transformer package here.

**Examples:**

Example 1 (typescript):
```typescript
import { Exclude } from 'class-transformer';

export class UserEntity {
  id: number;
  firstName: string;
  lastName: string;

  @Exclude()
  password: string;

  constructor(partial: Partial<UserEntity>) {
    Object.assign(this, partial);
  }
}
```

Example 2 (typescript):
```typescript
@UseInterceptors(ClassSerializerInterceptor)
@Get()
findOne(): UserEntity {
  return new UserEntity({
    id: 1,
    firstName: 'John',
    lastName: 'Doe',
    password: 'password',
  });
}
```

Example 3 (json):
```json
{
  "id": 1,
  "firstName": "John",
  "lastName": "Doe"
}
```

Example 4 (typescript):
```typescript
@Expose()
get fullName(): string {
  return `${this.firstName} ${this.lastName}`;
}
```

---

## 

**URL:** https://docs.nestjs.com/techniques/streaming-files

**Contents:**
  - Streaming files
    - Streamable File class#
    - Cross-platform support#
    - Example#

There may be times where you would like to send back a file from your REST API to the client. To do this with Nest, normally you'd do the following:

But in doing so you end up losing access to your post-controller interceptor logic. To handle this, you can return a StreamableFile instance and under the hood, the framework will take care of piping the response.

A StreamableFile is a class that holds onto the stream that is to be returned. To create a new StreamableFile, you can pass either a Buffer or a Stream to the StreamableFile constructor.

Fastify, by default, can support sending files without needing to call stream.pipe(res), so you don't need to use the StreamableFile class at all. However, Nest supports the use of StreamableFile in both platform types, so if you end up switching between Express and Fastify there's no need to worry about compatibility between the two engines.

You can find a simple example of returning the package.json as a file instead of a JSON below, but the idea extends out naturally to images, documents, and any other file type.

The default content type (the value for Content-Type HTTP response header) is application/octet-stream. If you need to customize this value you can use the type option from StreamableFile, or use the res.set method or the @Header() decorator, like this:

**Examples:**

Example 1 (php):
```php
@Controller('file')
export class FileController {
  @Get()
  getFile(@Res() res: Response) {
    const file = createReadStream(join(process.cwd(), 'package.json'));
    file.pipe(res);
  }
}
```

Example 2 (sql):
```sql
import { Controller, Get, StreamableFile } from '@nestjs/common';
import { createReadStream } from 'node:fs';
import { join } from 'node:path';

@Controller('file')
export class FileController {
  @Get()
  getFile(): StreamableFile {
    const file = createReadStream(join(process.cwd(), 'package.json'));
    return new StreamableFile(file);
  }
}
```

Example 3 (sql):
```sql
import { Controller, Get, StreamableFile, Res } from '@nestjs/common';
import { createReadStream } from 'node:fs';
import { join } from 'node:path';
import type { Response } from 'express'; // Assuming that we are using the ExpressJS HTTP Adapter

@Controller('file')
export class FileController {
  @Get()
  getFile(): StreamableFile {
    const file = createReadStream(join(process.cwd(), 'package.json'));
    return new StreamableFile(file, {
      type: 'application/json',
      disposition: 'attachment; filename="package.json"',
      // If you want to define the Content-Length value to another value instead of file's length:
      // length: 123,
    });
  }

  // Or even:
  @Get()
  getFileChangingResponseObjDirectly(@Res({ passthrough: true }) res: Response): StreamableFile {
    const file = createReadStream(join(process.cwd(), 'package.json'));
    res.set({
      'Content-Type': 'application/json',
      'Content-Disposition': 'attachment; filename="package.json"',
    });
    return new StreamableFile(file);
  }

  // Or even:
  @Get()
  @Header('Content-Type', 'application/json')
  @Header('Content-Disposition', 'attachment; filename="package.json"')
  getFileUsingStaticValues(): StreamableFile {
    const file = createReadStream(join(process.cwd(), 'package.json'));
    return new StreamableFile(file);
  }  
}
```

---

## 

**URL:** https://docs.nestjs.com/techniques/http-module

**Contents:**
  - HTTP module
    - Installation#
    - Getting started#
    - Configuration#
    - Async configuration#
    - Using Axios directly#
    - Full example#

Axios is a richly featured HTTP client package that is widely used. Nest wraps Axios and exposes it via the built-in HttpModule. The HttpModule exports the HttpService class, which exposes Axios-based methods to perform HTTP requests. The library also transforms the resulting HTTP responses into Observables.

To begin using it, we first install required dependencies.

Once the installation process is complete, to use the HttpService, first import HttpModule.

Next, inject HttpService using normal constructor injection.

All HttpService methods return an AxiosResponse wrapped in an Observable object.

Axios can be configured with a variety of options to customize the behavior of the HttpService. Read more about them here. To configure the underlying Axios instance, pass an optional options object to the register() method of HttpModule when importing it. This options object will be passed directly to the underlying Axios constructor.

When you need to pass module options asynchronously instead of statically, use the registerAsync() method. As with most dynamic modules, Nest provides several techniques to deal with async configuration.

One technique is to use a factory function:

Like other factory providers, our factory function can be async and can inject dependencies through inject.

Alternatively, you can configure the HttpModule using a class instead of a factory, as shown below.

The construction above instantiates HttpConfigService inside HttpModule, using it to create an options object. Note that in this example, the HttpConfigService has to implement HttpModuleOptionsFactory interface as shown below. The HttpModule will call the createHttpOptions() method on the instantiated object of the supplied class.

If you want to reuse an existing options provider instead of creating a private copy inside the HttpModule, use the useExisting syntax.

You can also pass so-called extraProviders to the registerAsync() method. These providers will be merged with the module providers.

This is useful when you want to provide additional dependencies to the factory function or the class constructor.

If you think that HttpModule.register's options are not enough for you, or if you just want to access the underlying Axios instance created by @nestjs/axios, you can access it via HttpService#axiosRef as follows:

Since the return value of the HttpService methods is an Observable, we can use rxjs - firstValueFrom or lastValueFrom to retrieve the data of the request in the form of a promise.

**Examples:**

Example 1 (bash):
```bash
$ npm i --save @nestjs/axios axios
```

Example 2 (typescript):
```typescript
@Module({
  imports: [HttpModule],
  providers: [CatsService],
})
export class CatsModule {}
```

Example 3 (typescript):
```typescript
@Injectable()
export class CatsService {
  constructor(private readonly httpService: HttpService) {}

  findAll(): Observable<AxiosResponse<Cat[]>> {
    return this.httpService.get('http://localhost:3000/cats');
  }
}
```

Example 4 (typescript):
```typescript
@Injectable()
@Dependencies(HttpService)
export class CatsService {
  constructor(httpService) {
    this.httpService = httpService;
  }

  findAll() {
    return this.httpService.get('http://localhost:3000/cats');
  }
}
```

---

## 

**URL:** https://docs.nestjs.com/recipes/prisma

**Contents:**
  - Prisma
    - Getting started#
    - Create your NestJS project#
    - Set up Prisma#
    - Set the generator output path#
    - Configure the module format#
    - Set the database connection#
    - Create two database tables with Prisma Migrate#
    - Install and generate Prisma Client#
    - Use Prisma Client in your NestJS services#

Prisma is an open-source ORM for Node.js and TypeScript. It is used as an alternative to writing plain SQL, or using another database access tool such as SQL query builders (like knex.js) or ORMs (like TypeORM and Sequelize). Prisma currently supports PostgreSQL, MySQL, SQL Server, SQLite, MongoDB and CockroachDB (Preview).

While Prisma can be used with plain JavaScript, it embraces TypeScript and provides a level to type-safety that goes beyond the guarantees other ORMs in the TypeScript ecosystem. You can find an in-depth comparison of the type-safety guarantees of Prisma and TypeORM here.

In this recipe, you'll learn how to get started with NestJS and Prisma from scratch. You are going to build a sample NestJS application with a REST API that can read and write data in a database.

For the purpose of this guide, you'll use a SQLite database to save the overhead of setting up a database server. Note that you can still follow this guide, even if you're using PostgreSQL or MySQL – you'll get extra instructions for using these databases at the right places.

To get started, install the NestJS CLI and create your app skeleton with the following commands:

See the First steps page to learn more about the project files created by this command. Note also that you can now run npm start to start your application. The REST API running at http://localhost:3000/ currently serves a single route that's implemented in src/app.controller.ts. Over the course of this guide, you'll implement additional routes to store and retrieve data about users and posts.

Start by installing the Prisma CLI as a development dependency in your project:

In the following steps, we'll be utilizing the Prisma CLI. As a best practice, it's recommended to invoke the CLI locally by prefixing it with npx:

If you're using Yarn, then you can install the Prisma CLI as follows:

Once installed, you can invoke it by prefixing it with yarn:

Now create your initial Prisma setup using the init command of the Prisma CLI:

This command creates a new prisma directory with the following contents:

Specify your output path for the generated Prisma client either by passing --output ../src/generated/prisma during prisma init, or directly in your Prisma schema:

Set moduleFormat in the generator to cjs:

Your database connection is configured in the datasource block in your schema.prisma file. By default it's set to postgresql, but since you're using a SQLite database in this guide you need to adjust the provider field of the datasource block to sqlite:

Now, open up .env and adjust the DATABASE_URL environment variable to look as follows:

Make sure you have a ConfigModule configured, otherwise the DATABASE_URL variable will not be picked up from .env.

SQLite databases are simple files; no server is required to use a SQLite database. So instead of configuring a connection URL with a host and port, you can just point it to a local file which in this case is called dev.db. This file will be created in the next step.

With PostgreSQL and MySQL, you need to configure the connection URL to point to the database server. You can learn more about the required connection URL format here.

If you're using PostgreSQL, you have to adjust the schema.prisma and .env files as follows:

Replace the placeholders spelled in all uppercase letters with your database credentials. Note that if you're unsure what to provide for the SCHEMA placeholder, it's most likely the default value public:

If you want to learn how to set up a PostgreSQL database, you can follow this guide on setting up a free PostgreSQL database on Heroku.

If you're using MySQL, you have to adjust the schema.prisma and .env files as follows:

Replace the placeholders spelled in all uppercase letters with your database credentials.

Microsoft SQL Server / Azure SQL Server

If you're using Microsoft SQL Server or Azure SQL Server, you have to adjust the schema.prisma and .env files as follows:

Replace the placeholders spelled in all uppercase letters with your database credentials. Note that if you're unsure what to provide for the encrypt placeholder, it's most likely the default value true:

In this section, you'll create two new tables in your database using Prisma Migrate. Prisma Migrate generates SQL migration files for your declarative data model definition in the Prisma schema. These migration files are fully customizable so that you can configure any additional features of the underlying database or include additional commands, e.g. for seeding.

Add the following two models to your schema.prisma file:

With your Prisma models in place, you can generate your SQL migration files and run them against the database. Run the following commands in your terminal:

This prisma migrate dev command generates SQL files and directly runs them against the database. In this case, the following migration files was created in the existing prisma directory:

The following tables were created in your SQLite database:

Prisma Client is a type-safe database client that's generated from your Prisma model definition. Because of this approach, Prisma Client can expose CRUD operations that are tailored specifically to your models.

To install Prisma Client in your project, run the following command in your terminal:

Once installed, you can run the generate command to generate the types and Client needed for your project. If any changes are made to your schema, you will need to rerun the generate command to keep those types in sync.

In addition to Prisma Client, you also need to a driver adapter for the type of database you are working with. For SQLite, you can install the @prisma/adapter-better-sqlite3 driver.

You're now able to send database queries with Prisma Client. If you want to learn more about building queries with Prisma Client, check out the API documentation.

When setting up your NestJS application, you'll want to abstract away the Prisma Client API for database queries within a service. To get started, you can create a new PrismaService that takes care of instantiating PrismaClient and connecting to your database.

Inside the src directory, create a new file called prisma.service.ts and add the following code to it:

Next, you can write services that you can use to make database calls for the User and Post models from your Prisma schema.

Still inside the src directory, create a new file called user.service.ts and add the following code to it:

Notice how you're using Prisma Client's generated types to ensure that the methods that are exposed by your service are properly typed. You therefore save the boilerplate of typing your models and creating additional interface or DTO files.

Now do the same for the Post model.

Still inside the src directory, create a new file called post.service.ts and add the following code to it:

Your UsersService and PostsService currently wrap the CRUD queries that are available in Prisma Client. In a real world application, the service would also be the place to add business logic to your application. For example, you could have a method called updatePassword inside the UsersService that would be responsible for updating the password of a user.

Remember to register the new services in the app module.

Finally, you'll use the services you created in the previous sections to implement the different routes of your app. For the purpose of this guide, you'll put all your routes into the already existing AppController class.

Replace the contents of the app.controller.ts file with the following code:

This controller implements the following routes:

In this recipe, you learned how to use Prisma along with NestJS to implement a REST API. The controller that implements the routes of the API is calling a PrismaService which in turn uses Prisma Client to send queries to a database to fulfill the data needs of incoming requests.

If you want to learn more about using NestJS with Prisma, be sure to check out the following resources:

**Examples:**

Example 1 (bash):
```bash
$ npm install -g @nestjs/cli
$ nest new hello-prisma
```

Example 2 (bash):
```bash
$ cd hello-prisma
$ npm install prisma --save-dev
```

Example 3 (bash):
```bash
$ npx prisma
```

Example 4 (bash):
```bash
$ yarn add prisma --dev
```

---
