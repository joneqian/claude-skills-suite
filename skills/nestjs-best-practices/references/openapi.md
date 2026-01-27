# Nestjs - Openapi

**Pages:** 8

---

## 

**URL:** https://docs.nestjs.com/openapi/operations

**Contents:**
  - Operations
    - Tags#
    - Headers#
    - Responses#
    - File upload#
    - Extensions#
    - Advanced: Generic ApiResponse#

In OpenAPI terms, paths are endpoints (resources), such as /users or /reports/summary, that your API exposes, and operations are the HTTP methods used to manipulate these paths, such as GET, POST or DELETE.

To attach a controller to a specific tag, use the @ApiTags(...tags) decorator.

To define custom headers that are expected as part of the request, use @ApiHeader().

To define a custom HTTP response, use the @ApiResponse() decorator.

Nest provides a set of short-hand API response decorators that inherit from the @ApiResponse decorator:

To specify a return model for a request, we must create a class and annotate all properties with the @ApiProperty() decorator.

Then the Cat model can be used in combination with the type property of the response decorator.

Let's open the browser and verify the generated Cat model:

Instead of defining responses for each endpoint or controller individually, you can define a global response for all endpoints using the DocumentBuilder class. This approach is useful when you want to define a global response for all endpoints in your application (e.g., for errors like 401 Unauthorized or 500 Internal Server Error).

You can enable file upload for a specific method with the @ApiBody decorator together with @ApiConsumes(). Here's a full example using the File Upload technique:

Where FileUploadDto is defined as follows:

To handle multiple files uploading, you can define FilesUploadDto as follows:

To add an Extension to a request use the @ApiExtension() decorator. The extension name must be prefixed with x-.

With the ability to provide Raw Definitions, we can define Generic schema for Swagger UI. Assume we have the following DTO:

We skip decorating results as we will be providing a raw definition for it later. Now, let's define another DTO and name it, for example, CatDto, as follows:

With this in place, we can define a PaginatedDto<CatDto> response, as follows:

In this example, we specify that the response will have allOf PaginatedDto and the results property will be of type Array<CatDto>.

Lastly, since PaginatedDto is not directly referenced by any controller, the SwaggerModule will not be able to generate a corresponding model definition just yet. In this case, we must add it as an Extra Model. For example, we can use the @ApiExtraModels() decorator on the controller level, as follows:

If you run Swagger now, the generated swagger.json for this specific endpoint should have the following response defined:

To make it reusable, we can create a custom decorator for PaginatedDto, as follows:

To ensure that SwaggerModule will generate a definition for our model, we must add it as an extra model, like we did earlier with the PaginatedDto in the controller.

With this in place, we can use the custom @ApiPaginatedResponse() decorator on our endpoint:

For client generation tools, this approach poses an ambiguity in how the PaginatedResponse<TModel> is being generated for the client. The following snippet is an example of a client generator result for the above GET / endpoint.

As you can see, the Return Type here is ambiguous. To workaround this issue, you can add a title property to the schema for ApiPaginatedResponse:

Now the result of the client generator tool will become:

**Examples:**

Example 1 (typescript):
```typescript
@ApiTags('cats')
@Controller('cats')
export class CatsController {}
```

Example 2 (typescript):
```typescript
@ApiHeader({
  name: 'X-MyHeader',
  description: 'Custom header',
})
@Controller('cats')
export class CatsController {}
```

Example 3 (typescript):
```typescript
@Post()
@ApiResponse({ status: 201, description: 'The record has been successfully created.'})
@ApiResponse({ status: 403, description: 'Forbidden.'})
async create(@Body() createCatDto: CreateCatDto) {
  this.catsService.create(createCatDto);
}
```

Example 4 (typescript):
```typescript
@Post()
@ApiCreatedResponse({ description: 'The record has been successfully created.'})
@ApiForbiddenResponse({ description: 'Forbidden.'})
async create(@Body() createCatDto: CreateCatDto) {
  this.catsService.create(createCatDto);
}
```

---

## 

**URL:** https://docs.nestjs.com/recipes/sql-sequelize

**Contents:**
  - SQL (Sequelize)
      - This chapter applies only to TypeScript
    - Getting started#
    - Model injection#

Sequelize is a popular Object Relational Mapper (ORM) written in a vanilla JavaScript, but there is a sequelize-typescript TypeScript wrapper which provides a set of decorators and other extras for the base sequelize.

To start the adventure with this library we have to install the following dependencies:

The first step we need to do is create a Sequelize instance with an options object passed into the constructor. Also, we need to add all models (the alternative is to use modelPaths property) and sync() our database tables.

Then, we need to export these providers to make them accessible for the rest part of the application.

Now we can inject the Sequelize object using @Inject() decorator. Each class that would depend on the Sequelize async provider will wait until a Promise is resolved.

In Sequelize the Model defines a table in the database. Instances of this class represent a database row. Firstly, we need at least one entity:

The Cat entity belongs to the cats directory. This directory represents the CatsModule. Now it's time to create a Repository provider:

In Sequelize, we use static methods to manipulate the data, and thus we created an alias here.

Now we can inject the CATS_REPOSITORY to the CatsService using the @Inject() decorator:

The database connection is asynchronous, but Nest makes this process completely invisible for the end-user. The CATS_REPOSITORY provider is waiting for the db connection, and the CatsService is delayed until repository is ready to use. The entire application can start when each class is instantiated.

Here is a final CatsModule:

**Examples:**

Example 1 (bash):
```bash
$ npm install --save sequelize sequelize-typescript mysql2
$ npm install --save-dev @types/sequelize
```

Example 2 (typescript):
```typescript
import { Sequelize } from 'sequelize-typescript';
import { Cat } from '../cats/cat.entity';

export const databaseProviders = [
  {
    provide: 'SEQUELIZE',
    useFactory: async () => {
      const sequelize = new Sequelize({
        dialect: 'mysql',
        host: 'localhost',
        port: 3306,
        username: 'root',
        password: 'password',
        database: 'nest',
      });
      sequelize.addModels([Cat]);
      await sequelize.sync();
      return sequelize;
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
import { Table, Column, Model } from 'sequelize-typescript';

@Table
export class Cat extends Model {
  @Column
  name: string;

  @Column
  age: number;

  @Column
  breed: string;
}
```

---

## 

**URL:** https://docs.nestjs.com/openapi/introduction

**Contents:**
  - Introduction
    - Installation#
    - Bootstrap#
    - Document options#
    - Setup options#
    - Example#

The OpenAPI specification is a language-agnostic definition format used to describe RESTful APIs. Nest provides a dedicated module which allows generating such a specification by leveraging decorators.

To begin using it, we first install the required dependency.

Once the installation process is complete, open the main.ts file and initialize Swagger using the SwaggerModule class:

The DocumentBuilder helps to structure a base document that conforms to the OpenAPI Specification. It provides several methods that allow setting such properties as title, description, version, etc. In order to create a full document (with all HTTP routes defined) we use the createDocument() method of the SwaggerModule class. This method takes two arguments, an application instance and a Swagger options object. Alternatively, we can provide a third argument, which should be of type SwaggerDocumentOptions. More on this in the Document options section.

Once we create a document, we can call the setup() method. It accepts:

Now you can run the following command to start the HTTP server:

While the application is running, open your browser and navigate to http://localhost:3000/api. You should see the Swagger UI.

As you can see, the SwaggerModule automatically reflects all of your endpoints.

Which would expose it at http://localhost:3000/swagger/json

When creating a document, it is possible to provide some extra options to fine tune the library's behavior. These options should be of type SwaggerDocumentOptions, which can be the following:

For example, if you want to make sure that the library generates operation names like createUser instead of UsersController_createUser, you can set the following:

You can configure Swagger UI by passing the options object which fulfills the SwaggerCustomOptions interface as a fourth argument of the SwaggerModule#setup method.

For example, the following configuration will disable the Swagger UI but still allow access to API definitions:

In this case, http://localhost:3000/api-json will still be accessible, but http://localhost:3000/api (Swagger UI) will not.

A working example is available here.

**Examples:**

Example 1 (bash):
```bash
$ npm install --save @nestjs/swagger
```

Example 2 (typescript):
```typescript
import { NestFactory } from '@nestjs/core';
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  const config = new DocumentBuilder()
    .setTitle('Cats example')
    .setDescription('The cats API description')
    .setVersion('1.0')
    .addTag('cats')
    .build();
  const documentFactory = () => SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api', app, documentFactory);

  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();
```

Example 3 (bash):
```bash
$ npm run start
```

Example 4 (typescript):
```typescript
SwaggerModule.setup('swagger', app, documentFactory, {
  jsonDocumentUrl: 'swagger/json',
});
```

---

## 

**URL:** https://docs.nestjs.com/openapi/decorators

**Contents:**
  - Decorators

All of the available OpenAPI decorators have an Api prefix to distinguish them from the core decorators. Below is a full list of the exported decorators along with a designation of the level at which the decorator may be applied.

---

## 

**URL:** https://docs.nestjs.com/openapi/security

**Contents:**
  - Security
    - Basic authentication#
    - Bearer authentication#
    - OAuth2 authentication#
    - Cookie authentication#

To define which security mechanisms should be used for a specific operation, use the @ApiSecurity() decorator.

Before you run your application, remember to add the security definition to your base document using DocumentBuilder:

Some of the most popular authentication techniques are built-in (e.g., basic and bearer) and therefore you don't have to define security mechanisms manually as shown above.

To enable basic authentication, use @ApiBasicAuth().

Before you run your application, remember to add the security definition to your base document using DocumentBuilder:

To enable bearer authentication, use @ApiBearerAuth().

Before you run your application, remember to add the security definition to your base document using DocumentBuilder:

To enable OAuth2, use @ApiOAuth2().

Before you run your application, remember to add the security definition to your base document using DocumentBuilder:

To enable cookie authentication, use @ApiCookieAuth().

Before you run your application, remember to add the security definition to your base document using DocumentBuilder:

**Examples:**

Example 1 (typescript):
```typescript
@ApiSecurity('basic')
@Controller('cats')
export class CatsController {}
```

Example 2 (typescript):
```typescript
const options = new DocumentBuilder().addSecurity('basic', {
  type: 'http',
  scheme: 'basic',
});
```

Example 3 (typescript):
```typescript
@ApiBasicAuth()
@Controller('cats')
export class CatsController {}
```

Example 4 (typescript):
```typescript
const options = new DocumentBuilder().addBasicAuth();
```

---

## 

**URL:** https://docs.nestjs.com/openapi/other-features

**Contents:**
  - Other features
    - Global prefix#
    - Global parameters#
    - Global responses#
    - Multiple specifications#
    - Dropdown in the explorer bar#

This page lists all the other available features that you may find useful.

To ignore a global prefix for routes set through setGlobalPrefix(), use ignoreGlobalPrefix:

You can define parameters for all routes using DocumentBuilder, as shown below:

You can define global responses for all routes using DocumentBuilder. This is useful for setting up consistent responses across all endpoints in your application, such as error codes like 401 Unauthorized or 500 Internal Server Error.

The SwaggerModule provides a way to support multiple specifications. In other words, you can serve different documentation, with different UIs, on different endpoints.

To support multiple specifications, your application must be written with a modular approach. The createDocument() method takes a 3rd argument, extraOptions, which is an object with a property named include. The include property takes a value which is an array of modules.

You can setup multiple specifications support as shown below:

Now you can start your server with the following command:

Navigate to http://localhost:3000/api/cats to see the Swagger UI for cats:

In turn, http://localhost:3000/api/dogs will expose the Swagger UI for dogs:

To enable support for multiple specifications in the dropdown menu of the explorer bar, you'll need to set explorer: true and configure swaggerOptions.urls in your SwaggerCustomOptions.

Here’s how to set up multiple specifications from a dropdown in the explorer bar:

In this example, we set up a main API along with separate specifications for Cats and Dogs, each accessible from the dropdown in the explorer bar.

**Examples:**

Example 1 (typescript):
```typescript
const document = SwaggerModule.createDocument(app, options, {
  ignoreGlobalPrefix: true,
});
```

Example 2 (typescript):
```typescript
const config = new DocumentBuilder()
  .addGlobalParameters({
    name: 'tenantId',
    in: 'header',
  })
  // other configurations
  .build();
```

Example 3 (typescript):
```typescript
const config = new DocumentBuilder()
  .addGlobalResponse({
    status: 500,
    description: 'Internal server error',
  })
  // other configurations
  .build();
```

Example 4 (typescript):
```typescript
import { NestFactory } from '@nestjs/core';
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';
import { AppModule } from './app.module';
import { CatsModule } from './cats/cats.module';
import { DogsModule } from './dogs/dogs.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  /**
   * createDocument(application, configurationOptions, extraOptions);
   *
   * createDocument method takes an optional 3rd argument "extraOptions"
   * which is an object with "include" property where you can pass an Array
   * of Modules that you want to include in that Swagger Specification
   * E.g: CatsModule and DogsModule will have two separate Swagger Specifications which
   * will be exposed on two different SwaggerUI with two different endpoints.
   */

  const options = new DocumentBuilder()
    .setTitle('Cats example')
    .setDescription('The cats API description')
    .setVersion('1.0')
    .addTag('cats')
    .build();

  const catDocumentFactory = () =>
    SwaggerModule.createDocument(app, options, {
      include: [CatsModule],
    });
  SwaggerModule.setup('api/cats', app, catDocumentFactory);

  const secondOptions = new DocumentBuilder()
    .setTitle('Dogs example')
    .setDescription('The dogs API description')
    .setVersion('1.0')
    .addTag('dogs')
    .build();

  const dogDocumentFactory = () =>
    SwaggerModule.createDocument(app, secondOptions, {
      include: [DogsModule],
    });
  SwaggerModule.setup('api/dogs', app, dogDocumentFactory);

  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();
```

---

## 

**URL:** https://docs.nestjs.com/openapi/types-and-parameters

**Contents:**
  - Types and parameters
    - Arrays#
- Official enterprise support
    - Circular dependencies#
    - Generics and interfaces#
    - Enums#
    - Enums schema#
    - Property value examples#
    - Raw definitions#
    - Extra models#

The SwaggerModule searches for all @Body(), @Query(), and @Param() decorators in route handlers to generate the API document. It also creates corresponding model definitions by taking advantage of reflection. Consider the following code:

Based on the CreateCatDto, the following model definition Swagger UI will be created:

As you can see, the definition is empty although the class has a few declared properties. In order to make the class properties visible to the SwaggerModule, we have to either annotate them with the @ApiProperty() decorator or use the CLI plugin (read more in the Plugin section) which will do it automatically:

Let's open the browser and verify the generated CreateCatDto model:

In addition, the @ApiProperty() decorator allows setting various Schema Object properties:

In order to explicitly set the type of the property, use the type key:

When the property is an array, we must manually indicate the array type as shown below:

Either include the type as the first element of an array (as shown above) or set the isArray property to true.

Official enterprise support Providing technical guidance Performing in-depth code reviews Mentoring team members Advising best practices Explore more

When you have circular dependencies between classes, use a lazy function to provide the SwaggerModule with type information:

Since TypeScript does not store metadata about generics or interfaces, when you use them in your DTOs, SwaggerModule may not be able to properly generate model definitions at runtime. For instance, the following code won't be correctly inspected by the Swagger module:

In order to overcome this limitation, you can set the type explicitly:

To identify an enum, we must manually set the enum property on the @ApiProperty with an array of values.

Alternatively, define an actual TypeScript enum as follows:

You can then use the enum directly with the @Query() parameter decorator in combination with the @ApiQuery() decorator.

With isArray set to true, the enum can be selected as a multi-select:

By default, the enum property will add a raw definition of Enum on the parameter.

The above specification works fine for most cases. However, if you are utilizing a tool that takes the specification as input and generates client-side code, you might run into a problem with the generated code containing duplicated enums. Consider the following code snippet:

You can see that now you have two enums that are exactly the same. To address this issue, you can pass an enumName along with the enum property in your decorator.

The enumName property enables @nestjs/swagger to turn CatBreed into its own schema which in turns makes CatBreed enum reusable. The specification will look like the following:

You can set a single example for a property by using the example key, like this:

If you want to provide multiple examples, you can use the examples key by passing in an object structured like this:

In certain cases, such as deeply nested arrays or matrices, you may need to manually define your type:

You can also specify raw object schemas, like this:

To manually define input/output content in controller classes, use the schema property:

To define additional models that are not directly referenced in your controllers but should be inspected by the Swagger module, use the @ApiExtraModels() decorator:

Alternatively, you can pass an options object with the extraModels property specified to the SwaggerModule.createDocument() method, as follows:

To get a reference ($ref) to your model, use the getSchemaPath(ExtraModel) function:

To combine schemas, you can use the oneOf, anyOf or allOf keywords (read more).

If you want to define a polymorphic array (i.e., an array whose members span multiple schemas), you should use a raw definition (see above) to define your type by hand.

Both Cat and Dog must be defined as extra models using the @ApiExtraModels() decorator (at the class-level).

As you may have noticed, the name of the generated schema is based on the name of the original model class (for example, the CreateCatDto model generates a CreateCatDto schema). If you'd like to change the schema name, you can use the @ApiSchema() decorator.

The model above will be translated into the CreateCatRequest schema.

By default, no description is added to the generated schema. You can add one using the description attribute:

That way, the description will be included in the schema, as follows:

**Examples:**

Example 1 (typescript):
```typescript
@Post()
async create(@Body() createCatDto: CreateCatDto) {
  this.catsService.create(createCatDto);
}
```

Example 2 (typescript):
```typescript
import { ApiProperty } from '@nestjs/swagger';

export class CreateCatDto {
  @ApiProperty()
  name: string;

  @ApiProperty()
  age: number;

  @ApiProperty()
  breed: string;
}
```

Example 3 (typescript):
```typescript
@ApiProperty({
  description: 'The age of a cat',
  minimum: 1,
  default: 1,
})
age: number;
```

Example 4 (typescript):
```typescript
@ApiProperty({
  type: Number,
})
age: number;
```

---

## 

**URL:** https://docs.nestjs.com/graphql/sharing-models

**Contents:**
  - Sharing models
    - Using the model shim#

One of the biggest advantages of using Typescript for the backend of your project is the ability to reuse the same models in a Typescript-based frontend application, by using a common Typescript package.

But there's a problem: the models created using the code first approach are heavily decorated with GraphQL related decorators. Those decorators are irrelevant in the frontend, negatively impacting performance.

To solve this issue, NestJS provides a "shim" which allows you to replace the original decorators with inert code by using a webpack (or similar) configuration. To use this shim, configure an alias between the @nestjs/graphql package and the shim.

For example, for webpack this is resolved this way:

**Examples:**

Example 1 (typescript):
```typescript
resolve: { // see: https://webpack.js.org/configuration/resolve/
  alias: {
      "@nestjs/graphql": path.resolve(__dirname, "../node_modules/@nestjs/graphql/dist/extra/graphql-model-shim")
  }
}
```

---
