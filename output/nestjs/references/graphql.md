# Nestjs - Graphql

**Pages:** 15

---

## 

**URL:** https://docs.nestjs.com/openapi/cli-plugin

**Contents:**
  - CLI Plugin
    - Overview#
    - Comments introspection#
    - Using the CLI plugin#
    - SWC builder#
    - Integration with ts-jest (e2e tests)#
    - Troubleshooting jest (e2e tests)#

TypeScript's metadata reflection system has several limitations which make it impossible to, for instance, determine what properties a class consists of or recognize whether a given property is optional or required. However, some of these constraints can be addressed at compilation time. Nest provides a plugin that enhances the TypeScript compilation process to reduce the amount of boilerplate code required.

The Swagger plugin will automatically:

Please, note that your filenames must have one of the following suffixes: ['.dto.ts', '.entity.ts'] (e.g., create-user.dto.ts) in order to be analysed by the plugin.

If you are using a different suffix, you can adjust the plugin's behavior by specifying the dtoFileNameSuffix option (see below).

Previously, if you wanted to provide an interactive experience with the Swagger UI, you had to duplicate a lot of code to let the package know how your models/components should be declared in the specification. For example, you could define a simple CreateUserDto class as follows:

While not a significant issue with medium-sized projects, it becomes verbose & hard to maintain once you have a large set of classes.

By enabling the Swagger plugin, the above class definition can be declared simply:

Hence, if you intend to rely on automatic annotations for generating documentations and still wish for runtime validations, then the class-validator decorators are still necessary.

The plugin adds appropriate decorators on the fly based on the Abstract Syntax Tree. Thus you won't have to struggle with @ApiProperty decorators scattered throughout the code.

With the comments introspection feature enabled, CLI plugin will generate descriptions and example values for properties based on comments.

For example, given an example roles property:

You must duplicate both description and example values. With introspectComments enabled, the CLI plugin can extract these comments and automatically provide descriptions (and examples, if defined) for properties. Now, the above property can be declared simply as follows:

There are dtoKeyOfComment and controllerKeyOfComment plugin options available for customizing how the plugin assigns values to the ApiProperty and ApiOperation decorators, respectively. See the example below:

This is equivalent to the following instruction:

For controllers, you can provide not only a summary but also a description (remarks), tags (such as @deprecated), and response examples, like this:

To enable the plugin, open nest-cli.json (if you use Nest CLI) and add the following plugins configuration:

You can use the options property to customize the behavior of the plugin.

The options property has to fulfill the following interface:

Make sure to delete the /dist folder and rebuild your application whenever plugin options are updated. If you don't use the CLI but instead have a custom webpack configuration, you can use this plugin in combination with ts-loader:

For standard setups (non-monorepo), to use CLI Plugins with the SWC builder, you need to enable type checking, as described here.

For monorepo setups, follow the instructions here.

Now, the serialized metadata file must be loaded by the SwaggerModule#loadPluginMetadata method, as shown below:

To run e2e tests, ts-jest compiles your source code files on the fly, in memory. This means, it doesn't use Nest CLI compiler and does not apply any plugins or perform AST transformations.

To enable the plugin, create the following file in your e2e tests directory:

With this in place, import AST transformer within your jest configuration file. By default (in the starter application), e2e tests configuration file is located under the test folder and is named jest-e2e.json.

If you use jest@<29, then use the snippet below.

If you use jest@^29, then use the snippet below, as the previous approach got deprecated.

In case jest does not seem to pick up your configuration changes, it's possible that Jest has already cached the build result. To apply the new configuration, you need to clear Jest's cache directory.

To clear the cache directory, run the following command in your NestJS project folder:

In case the automatic cache clearance fails, you can still manually remove the cache folder with the following commands:

**Examples:**

Example 1 (typescript):
```typescript
export class CreateUserDto {
  @ApiProperty()
  email: string;

  @ApiProperty()
  password: string;

  @ApiProperty({ enum: RoleEnum, default: [], isArray: true })
  roles: RoleEnum[] = [];

  @ApiProperty({ required: false, default: true })
  isEnabled?: boolean = true;
}
```

Example 2 (typescript):
```typescript
export class CreateUserDto {
  email: string;
  password: string;
  roles: RoleEnum[] = [];
  isEnabled?: boolean = true;
}
```

Example 3 (typescript):
```typescript
/**
 * A list of user's roles
 * @example ['admin']
 */
@ApiProperty({
  description: `A list of user's roles`,
  example: ['admin'],
})
roles: RoleEnum[] = [];
```

Example 4 (typescript):
```typescript
/**
 * A list of user's roles
 * @example ['admin']
 */
roles: RoleEnum[] = [];
```

---

## 

**URL:** https://docs.nestjs.com/graphql/complexity

**Contents:**
  - Complexity
    - Installation#
    - Getting started#
    - Field-level complexity#
    - Query/Mutation-level complexity#

Query complexity allows you to define how complex certain fields are, and to restrict queries with a maximum complexity. The idea is to define how complex each field is by using a simple number. A common default is to give each field a complexity of 1. In addition, the complexity calculation of a GraphQL query can be customized with so-called complexity estimators. A complexity estimator is a simple function that calculates the complexity for a field. You can add any number of complexity estimators to the rule, which are then executed one after another. The first estimator that returns a numeric complexity value determines the complexity for that field.

The @nestjs/graphql package integrates very well with tools like graphql-query-complexity that provides a cost analysis-based solution. With this library, you can reject queries to your GraphQL server that are deemed too costly to execute.

To begin using it, we first install the required dependency.

Once the installation process is complete, we can define the ComplexityPlugin class:

For demonstration purposes, we specified the maximum allowed complexity as 20. In the example above, we used 2 estimators, the simpleEstimator and the fieldExtensionsEstimator.

With this plugin in place, we can now define the complexity for any field by specifying the complexity property in the options object passed into the @Field() decorator, as follows:

Alternatively, you can define the estimator function:

In addition, @Query() and @Mutation() decorators may have a complexity property specified like so:

**Examples:**

Example 1 (bash):
```bash
$ npm install --save graphql-query-complexity
```

Example 2 (typescript):
```typescript
import { GraphQLSchemaHost } from '@nestjs/graphql';
import { Plugin } from '@nestjs/apollo';
import {
  ApolloServerPlugin,
  BaseContext,
  GraphQLRequestListener,
} from '@apollo/server';
import { GraphQLError } from 'graphql';
import {
  fieldExtensionsEstimator,
  getComplexity,
  simpleEstimator,
} from 'graphql-query-complexity';

@Plugin()
export class ComplexityPlugin implements ApolloServerPlugin {
  constructor(private gqlSchemaHost: GraphQLSchemaHost) {}

  async requestDidStart(): Promise<GraphQLRequestListener<BaseContext>> {
    const maxComplexity = 20;
    const { schema } = this.gqlSchemaHost;

    return {
      async didResolveOperation({ request, document }) {
        const complexity = getComplexity({
          schema,
          operationName: request.operationName,
          query: document,
          variables: request.variables,
          estimators: [
            fieldExtensionsEstimator(),
            simpleEstimator({ defaultComplexity: 1 }),
          ],
        });
        if (complexity > maxComplexity) {
          throw new GraphQLError(
            `Query is too complex: ${complexity}. Maximum allowed complexity: ${maxComplexity}`,
          );
        }
        console.log('Query Complexity:', complexity);
      },
    };
  }
}
```

Example 3 (typescript):
```typescript
@Field({ complexity: 3 })
title: string;
```

Example 4 (typescript):
```typescript
@Field({ complexity: (options: ComplexityEstimatorArgs) => ... })
title: string;
```

---

## 

**URL:** https://docs.nestjs.com/graphql/mapped-types

**Contents:**
  - Mapped types
    - Partial#
    - Pick#
    - Omit#
    - Intersection#
    - Composition#

As you build out features like CRUD (Create/Read/Update/Delete) it's often useful to construct variants on a base entity type. Nest provides several utility functions that perform type transformations to make this task more convenient.

When building input validation types (also called Data Transfer Objects or DTOs), it's often useful to build create and update variations on the same type. For example, the create variant may require all fields, while the update variant may make all fields optional.

Nest provides the PartialType() utility function to make this task easier and minimize boilerplate.

The PartialType() function returns a type (class) with all the properties of the input type set to optional. For example, suppose we have a create type as follows:

By default, all of these fields are required. To create a type with the same fields, but with each one optional, use PartialType() passing the class reference (CreateUserInput) as an argument:

The PartialType() function takes an optional second argument that is a reference to a decorator factory. This argument can be used to change the decorator function applied to the resulting (child) class. If not specified, the child class effectively uses the same decorator as the parent class (the class referenced in the first argument). In the example above, we are extending CreateUserInput which is annotated with the @InputType() decorator. Since we want UpdateUserInput to also be treated as if it were decorated with @InputType(), we didn't need to pass InputType as the second argument. If the parent and child types are different, (e.g., the parent is decorated with @ObjectType), we would pass InputType as the second argument. For example:

The PickType() function constructs a new type (class) by picking a set of properties from an input type. For example, suppose we start with a type like:

We can pick a set of properties from this class using the PickType() utility function:

The OmitType() function constructs a type by picking all properties from an input type and then removing a particular set of keys. For example, suppose we start with a type like:

We can generate a derived type that has every property exceptemail as shown below. In this construct, the second argument to OmitType is an array of property names.

The IntersectionType() function combines two types into one new type (class). For example, suppose we start with two types like:

We can generate a new type that combines all properties in both types.

The type mapping utility functions are composable. For example, the following will produce a type (class) that has all of the properties of the CreateUserInput type except for email, and those properties will be set to optional:

**Examples:**

Example 1 (typescript):
```typescript
@InputType()
class CreateUserInput {
  @Field()
  email: string;

  @Field()
  password: string;

  @Field()
  firstName: string;
}
```

Example 2 (typescript):
```typescript
@InputType()
export class UpdateUserInput extends PartialType(CreateUserInput) {}
```

Example 3 (typescript):
```typescript
@InputType()
export class UpdateUserInput extends PartialType(User, InputType) {}
```

Example 4 (typescript):
```typescript
@InputType()
class CreateUserInput {
  @Field()
  email: string;

  @Field()
  password: string;

  @Field()
  firstName: string;
}
```

---

## 

**URL:** https://docs.nestjs.com/graphql/scalars

**Contents:**
  - Scalars
    - Code first#
    - Override a default scalar#
    - Import a custom scalar#
    - Create a custom scalar#
    - Schema first#

A GraphQL object type has a name and fields, but at some point those fields have to resolve to some concrete data. That's where the scalar types come in: they represent the leaves of the query (read more here). GraphQL includes the following default types: Int, Float, String, Boolean and ID. In addition to these built-in types, you may need to support custom atomic data types (e.g., Date).

The code-first approach ships with five scalars in which three of them are simple aliases for the existing GraphQL types.

The GraphQLISODateTime (e.g. 2019-12-03T09:54:33Z) is used by default to represent the Date type. To use the GraphQLTimestamp instead, set the dateScalarMode of the buildSchemaOptions object to 'timestamp' as follows:

Likewise, the GraphQLFloat is used by default to represent the number type. To use the GraphQLInt instead, set the numberScalarMode of the buildSchemaOptions object to 'integer' as follows:

In addition, you can create custom scalars.

To create a custom implementation for the Date scalar, simply create a new class.

With this in place, register DateScalar as a provider.

Now we can use the Date type in our classes.

To use a custom scalar, import and register it as a resolver. We’ll use the graphql-type-json package for demonstration purposes. This npm package defines a JSON GraphQL scalar type.

Start by installing the package:

Once the package is installed, we pass a custom resolver to the forRoot() method:

Now we can use the JSON type in our classes.

For a suite of useful scalars, take a look at the graphql-scalars package.

To define a custom scalar, create a new GraphQLScalarType instance. We'll create a custom UUID scalar.

We pass a custom resolver to the forRoot() method:

Now we can use the UUID type in our classes.

To define a custom scalar (read more about scalars here), create a type definition and a dedicated resolver. Here (as in the official documentation), we’ll use the graphql-type-json package for demonstration purposes. This npm package defines a JSON GraphQL scalar type.

Start by installing the package:

Once the package is installed, we pass a custom resolver to the forRoot() method:

Now we can use the JSON scalar in our type definitions:

Another method to define a scalar type is to create a simple class. Assume we want to enhance our schema with the Date type.

With this in place, register DateScalar as a provider.

Now we can use the Date scalar in type definitions.

By default, the generated TypeScript definition for all scalars is any - which isn't particularly typesafe. But, you can configure how Nest generates typings for your custom scalars when you specify how to generate types:

Now, given the following GraphQL custom scalar types:

We will now see the following generated TypeScript definitions in src/graphql.ts:

Here, we've used the customScalarTypeMapping property to supply a map of the types we wish to declare for our custom scalars. We've also provided an additionalHeader property so that we can add any imports required for these type definitions. Lastly, we've added a defaultScalarType of 'unknown', so that any custom scalars not specified in customScalarTypeMapping will be aliased to unknown instead of any (which TypeScript recommends using since 3.0 for added type safety).

**Examples:**

Example 1 (typescript):
```typescript
GraphQLModule.forRoot({
  buildSchemaOptions: {
    dateScalarMode: 'timestamp',
  }
}),
```

Example 2 (typescript):
```typescript
GraphQLModule.forRoot({
  buildSchemaOptions: {
    numberScalarMode: 'integer',
  }
}),
```

Example 3 (typescript):
```typescript
import { Scalar, CustomScalar } from '@nestjs/graphql';
import { Kind, ValueNode } from 'graphql';

@Scalar('Date', () => Date)
export class DateScalar implements CustomScalar<number, Date> {
  description = 'Date custom scalar type';

  parseValue(value: number): Date {
    return new Date(value); // value from the client
  }

  serialize(value: Date): number {
    return value.getTime(); // value sent to the client
  }

  parseLiteral(ast: ValueNode): Date {
    if (ast.kind === Kind.INT) {
      return new Date(ast.value);
    }
    return null;
  }
}
```

Example 4 (typescript):
```typescript
@Module({
  providers: [DateScalar],
})
export class CommonModule {}
```

---

## 

**URL:** https://docs.nestjs.com/graphql/federation

**Contents:**
  - Federation
    - Federation with Apollo#
    - Schema first#
    - Code first#
    - Federated example: Posts#
    - Schema first#
    - Code first#
    - Federated example: Gateway#
    - Federation with Mercurius#
    - Schema first#

Federation offers a means of splitting your monolithic GraphQL server into independent microservices. It consists of two components: a gateway and one or more federated microservices. Each microservice holds part of the schema and the gateway merges the schemas into a single schema that can be consumed by the client.

To quote the Apollo docs, Federation is designed with these core principles:

In the following sections, we'll set up a demo application that consists of a gateway and two federated endpoints: Users service and Posts service.

Start by installing the required dependencies:

The "User service" provides a simple schema. Note the @key directive: it instructs the Apollo query planner that a particular instance of User can be fetched if you specify its id. Also, note that we extend the Query type.

Resolver provides one additional method named resolveReference(). This method is triggered by the Apollo Gateway whenever a related resource requires a User instance. We'll see an example of this in the Posts service later. Please note that the method must be annotated with the @ResolveReference() decorator.

Finally, we hook everything up by registering the GraphQLModule passing the ApolloFederationDriver driver in the configuration object:

Start by adding some extra decorators to the User entity.

Resolver provides one additional method named resolveReference(). This method is triggered by the Apollo Gateway whenever a related resource requires a User instance. We'll see an example of this in the Posts service later. Please note that the method must be annotated with the @ResolveReference() decorator.

Finally, we hook everything up by registering the GraphQLModule passing the ApolloFederationDriver driver in the configuration object:

A working example is available here in code first mode and here in schema first mode.

Post service is supposed to serve aggregated posts through the getPosts query, but also extend our User type with the user.posts field.

"Posts service" references the User type in its schema by marking it with the extend keyword. It also declares one additional property on the User type (posts). Note the @key directive used for matching instances of User, and the @external directive indicating that the id field is managed elsewhere.

In the following example, the PostsResolver provides the getUser() method that returns a reference containing __typename and some additional properties your application may need to resolve the reference, in this case id. __typename is used by the GraphQL Gateway to pinpoint the microservice responsible for the User type and retrieve the corresponding instance. The "Users service" described above will be requested upon execution of the resolveReference() method.

Lastly, we must register the GraphQLModule, similarly to what we did in the "Users service" section.

First, we will have to declare a class representing the User entity. Although the entity itself lives in another service, we will be using it (extending its definition) here. Note the @extends and @external directives.

Now let's create the corresponding resolver for our extension on the User entity, as follows:

We also have to define the Post entity class:

And finally, tie it together in a module. Note the schema build options, where we specify that User is an orphaned (external) type.

A working example is available here for the code first mode and here for the schema first mode.

Start by installing the required dependency:

The gateway requires a list of endpoints to be specified and it will auto-discover the corresponding schemas. Therefore the implementation of the gateway service will remain the same for both code and schema first approaches.

A working example is available here for the code first mode and here for the schema first mode.

Start by installing the required dependencies:

The "User service" provides a simple schema. Note the @key directive: it instructs the Mercurius query planner that a particular instance of User can be fetched if you specify its id. Also, note that we extend the Query type.

Resolver provides one additional method named resolveReference(). This method is triggered by the Mercurius Gateway whenever a related resource requires a User instance. We'll see an example of this in the Posts service later. Please note that the method must be annotated with the @ResolveReference() decorator.

Finally, we hook everything up by registering the GraphQLModule passing the MercuriusFederationDriver driver in the configuration object:

Start by adding some extra decorators to the User entity.

Resolver provides one additional method named resolveReference(). This method is triggered by the Mercurius Gateway whenever a related resource requires a User instance. We'll see an example of this in the Posts service later. Please note that the method must be annotated with the @ResolveReference() decorator.

Finally, we hook everything up by registering the GraphQLModule passing the MercuriusFederationDriver driver in the configuration object:

Post service is supposed to serve aggregated posts through the getPosts query, but also extend our User type with the user.posts field.

"Posts service" references the User type in its schema by marking it with the extend keyword. It also declares one additional property on the User type (posts). Note the @key directive used for matching instances of User, and the @external directive indicating that the id field is managed elsewhere.

In the following example, the PostsResolver provides the getUser() method that returns a reference containing __typename and some additional properties your application may need to resolve the reference, in this case id. __typename is used by the GraphQL Gateway to pinpoint the microservice responsible for the User type and retrieve the corresponding instance. The "Users service" described above will be requested upon execution of the resolveReference() method.

Lastly, we must register the GraphQLModule, similarly to what we did in the "Users service" section.

First, we will have to declare a class representing the User entity. Although the entity itself lives in another service, we will be using it (extending its definition) here. Note the @extends and @external directives.

Now let's create the corresponding resolver for our extension on the User entity, as follows:

We also have to define the Post entity class:

And finally, tie it together in a module. Note the schema build options, where we specify that User is an orphaned (external) type.

The gateway requires a list of endpoints to be specified and it will auto-discover the corresponding schemas. Therefore the implementation of the gateway service will remain the same for both code and schema first approaches.

To quote the Apollo docs, Federation 2 improves developer experience from the original Apollo Federation (called Federation 1 in this doc), which is backward compatible with most original supergraphs.

In the following sections, we'll upgrade the previous example to Federation 2.

One change in Federation 2 is that entities have no originating subgraph, so we don't need to extend Query anymore. For more detail please refer to the entities topic in Apollo Federation 2 docs.

We can simply remove extend keyword from the schema.

To use Federation 2, we need to specify the federation version in autoSchemaFile option.

With the same reason as above, we don't need to extend User and Query anymore.

We can simply remove extend and external directives from the schema

Since we don't extend User entity anymore, we can simply remove extends and external directives from User.

Also, similarly to the User service, we need to specify in the GraphQLModule to use Federation 2.

**Examples:**

Example 1 (bash):
```bash
$ npm install --save @apollo/subgraph
```

Example 2 (css):
```css
type User @key(fields: "id") {
  id: ID!
  name: String!
}

extend type Query {
  getUser(id: ID!): User
}
```

Example 3 (typescript):
```typescript
import { Args, Query, Resolver, ResolveReference } from '@nestjs/graphql';
import { UsersService } from './users.service';

@Resolver('User')
export class UsersResolver {
  constructor(private usersService: UsersService) {}

  @Query()
  getUser(@Args('id') id: string) {
    return this.usersService.findById(id);
  }

  @ResolveReference()
  resolveReference(reference: { __typename: string; id: string }) {
    return this.usersService.findById(reference.id);
  }
}
```

Example 4 (typescript):
```typescript
import {
  ApolloFederationDriver,
  ApolloFederationDriverConfig,
} from '@nestjs/apollo';
import { Module } from '@nestjs/common';
import { GraphQLModule } from '@nestjs/graphql';
import { UsersResolver } from './users.resolver';

@Module({
  imports: [
    GraphQLModule.forRoot<ApolloFederationDriverConfig>({
      driver: ApolloFederationDriver,
      typePaths: ['**/*.graphql'],
    }),
  ],
  providers: [UsersResolver],
})
export class AppModule {}
```

---

## 

**URL:** https://docs.nestjs.com/graphql/generating-sdl

**Contents:**
  - Generating SDL
    - Usage#

To manually generate a GraphQL SDL schema (i.e., without running an application, connecting to the database, hooking up resolvers, etc.), use the GraphQLSchemaBuilderModule.

The gqlSchemaFactory.create() method takes an array of resolver class references. For example:

It also takes a second optional argument with an array of scalar classes:

Lastly, you can pass an options object:

**Examples:**

Example 1 (typescript):
```typescript
async function generateSchema() {
  const app = await NestFactory.create(GraphQLSchemaBuilderModule);
  await app.init();

  const gqlSchemaFactory = app.get(GraphQLSchemaFactory);
  const schema = await gqlSchemaFactory.create([RecipesResolver]);
  console.log(printSchema(schema));
}
```

Example 2 (typescript):
```typescript
const schema = await gqlSchemaFactory.create([
  RecipesResolver,
  AuthorsResolver,
  PostsResolvers,
]);
```

Example 3 (typescript):
```typescript
const schema = await gqlSchemaFactory.create(
  [RecipesResolver, AuthorsResolver, PostsResolvers],
  [DurationScalar, DateScalar],
);
```

Example 4 (typescript):
```typescript
const schema = await gqlSchemaFactory.create([RecipesResolver], {
  skipCheck: true,
  orphanedTypes: [],
});
```

---

## 

**URL:** https://docs.nestjs.com/graphql/mutations

**Contents:**
  - Mutations
    - Code first#
    - Schema first#

Most discussions of GraphQL focus on data fetching, but any complete data platform needs a way to modify server-side data as well. In REST, any request could end up causing side-effects on the server, but best practice suggests we should not modify data in GET requests. GraphQL is similar - technically any query could be implemented to cause a data write. However, like REST, it's recommended to observe the convention that any operations that cause writes should be sent explicitly via a mutation (read more here).

The official Apollo documentation uses an upvotePost() mutation example. This mutation implements a method to increase a post's votes property value. To create an equivalent mutation in Nest, we'll make use of the @Mutation() decorator.

Let's add another method to the AuthorResolver used in the previous section (see resolvers).

This will result in generating the following part of the GraphQL schema in SDL:

The upvotePost() method takes postId (Int) as an argument and returns an updated Post entity. For the reasons explained in the resolvers section, we have to explicitly set the expected type.

If the mutation needs to take an object as an argument, we can create an input type. The input type is a special kind of object type that can be passed in as an argument (read more here). To declare an input type, use the @InputType() decorator.

We can then use this type in the resolver class:

Let's extend our AuthorResolver used in the previous section (see resolvers).

Note that we assumed above that the business logic has been moved to the PostsService (querying the post and incrementing its votes property). The logic inside the PostsService class can be as simple or sophisticated as needed. The main point of this example is to show how resolvers can interact with other providers.

The last step is to add our mutation to the existing types definition.

The upvotePost(postId: Int!): Post mutation is now available to be called as part of our application's GraphQL API.

**Examples:**

Example 1 (typescript):
```typescript
@Mutation(() => Post)
async upvotePost(@Args({ name: 'postId', type: () => Int }) postId: number) {
  return this.postsService.upvoteById({ id: postId });
}
```

Example 2 (unknown):
```unknown
type Mutation {
  upvotePost(postId: Int!): Post
}
```

Example 3 (typescript):
```typescript
import { InputType, Field } from '@nestjs/graphql';

@InputType()
export class UpvotePostInput {
  @Field()
  postId: number;
}
```

Example 4 (typescript):
```typescript
@Mutation(() => Post)
async upvotePost(
  @Args('upvotePostData') upvotePostData: UpvotePostInput,
) {}
```

---

## 

**URL:** https://docs.nestjs.com/graphql/interfaces

**Contents:**
  - Interfaces
    - Code first#
    - Interface resolvers#
    - Schema first#

Like many type systems, GraphQL supports interfaces. An Interface is an abstract type that includes a certain set of fields that a type must include to implement the interface (read more here).

When using the code first approach, you define a GraphQL interface by creating an abstract class annotated with the @InterfaceType() decorator exported from the @nestjs/graphql.

This will result in generating the following part of the GraphQL schema in SDL:

Now, to implement the Character interface, use the implements key:

The default resolveType() function generated by the library extracts the type based on the value returned from the resolver method. This means that you must return class instances (you cannot return literal JavaScript objects).

To provide a customized resolveType() function, pass the resolveType property to the options object passed into the @InterfaceType() decorator, as follows:

So far, using interfaces, you could only share field definitions with your objects. If you also want to share the actual field resolvers implementation, you can create a dedicated interface resolver, as follows:

Now the friends field resolver is auto-registered for all object types that implement the Character interface.

To define an interface in the schema first approach, simply create a GraphQL interface with SDL.

Then, you can use the typings generation feature (as shown in the quick start chapter) to generate corresponding TypeScript definitions:

Interfaces require an extra __resolveType field in the resolver map to determine which type the interface should resolve to. Let's create a CharactersResolver class and define the __resolveType method:

**Examples:**

Example 1 (typescript):
```typescript
import { Field, ID, InterfaceType } from '@nestjs/graphql';

@InterfaceType()
export abstract class Character {
  @Field(() => ID)
  id: string;

  @Field()
  name: string;
}
```

Example 2 (typescript):
```typescript
interface Character {
  id: ID!
  name: String!
}
```

Example 3 (typescript):
```typescript
@ObjectType({
  implements: () => [Character],
})
export class Human implements Character {
  id: string;
  name: string;
}
```

Example 4 (typescript):
```typescript
@InterfaceType({
  resolveType(book) {
    if (book.colors) {
      return ColoringBook;
    }
    return TextBook;
  },
})
export abstract class Book {
  @Field(() => ID)
  id: string;

  @Field()
  title: string;
}
```

---

## 

**URL:** https://docs.nestjs.com/graphql/cli-plugin

**Contents:**
  - CLI Plugin
    - Overview#
    - Comments introspection#
    - Using the CLI plugin#
    - SWC builder#
    - Integration with ts-jest (e2e tests)#

TypeScript's metadata reflection system has several limitations which make it impossible to, for instance, determine what properties a class consists of or recognize whether a given property is optional or required. However, some of these constraints can be addressed at compilation time. Nest provides a plugin that enhances the TypeScript compilation process to reduce the amount of boilerplate code required.

The GraphQL plugin will automatically:

Please, note that your filenames must have one of the following suffixes in order to be analyzed by the plugin: ['.input.ts', '.args.ts', '.entity.ts', '.model.ts'] (e.g., author.entity.ts). If you are using a different suffix, you can adjust the plugin's behavior by specifying the typeFileNameSuffix option (see below).

With what we've learned so far, you have to duplicate a lot of code to let the package know how your type should be declared in GraphQL. For example, you could define a simple Author class as follows:

While not a significant issue with medium-sized projects, it becomes verbose & hard to maintain once you have a large set of classes.

By enabling the GraphQL plugin, the above class definition can be declared simply:

The plugin adds appropriate decorators on-the-fly based on the Abstract Syntax Tree. Thus, you won't have to struggle with @Field decorators scattered throughout the code.

With the comments introspection feature enabled, CLI plugin will generate descriptions for fields based on comments.

For example, given an example roles property:

You must duplicate description values. With introspectComments enabled, the CLI plugin can extract these comments and automatically provide descriptions for properties. Now, the above field can be declared simply as follows:

To enable the plugin, open nest-cli.json (if you use Nest CLI) and add the following plugins configuration:

You can use the options property to customize the behavior of the plugin.

The options property has to fulfill the following interface:

If you don't use the CLI but instead have a custom webpack configuration, you can use this plugin in combination with ts-loader:

For standard setups (non-monorepo), to use CLI Plugins with the SWC builder, you need to enable type checking, as described here.

For monorepo setups, follow the instructions here.

Now, the serialized metadata file must be loaded by the GraphQLModule method, as shown below:

When running e2e tests with this plugin enabled, you may run into issues with compiling schema. For example, one of the most common errors is:

This happens because jest configuration does not import @nestjs/graphql/plugin plugin anywhere.

To fix this, create the following file in your e2e tests directory:

With this in place, import AST transformer within your jest configuration file. By default (in the starter application), e2e tests configuration file is located under the test folder and is named jest-e2e.json.

If you use jest@^29, then use the snippet below, as the previous approach got deprecated.

**Examples:**

Example 1 (typescript):
```typescript
@ObjectType()
export class Author {
  @Field(type => ID)
  id: number;

  @Field({ nullable: true })
  firstName?: string;

  @Field({ nullable: true })
  lastName?: string;

  @Field(type => [Post])
  posts: Post[];
}
```

Example 2 (typescript):
```typescript
@ObjectType()
export class Author {
  @Field(type => ID)
  id: number;
  firstName?: string;
  lastName?: string;
  posts: Post[];
}
```

Example 3 (typescript):
```typescript
/**
 * A list of user's roles
 */
@Field(() => [String], {
  description: `A list of user's roles`
})
roles: string[];
```

Example 4 (typescript):
```typescript
/**
 * A list of user's roles
 */
roles: string[];
```

---

## 

**URL:** https://docs.nestjs.com/openapi/mapped-types

**Contents:**
  - Mapped types
    - Partial#
    - Pick#
    - Omit#
    - Intersection#
    - Composition#

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

**Examples:**

Example 1 (typescript):
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

Example 2 (typescript):
```typescript
export class UpdateCatDto extends PartialType(CreateCatDto) {}
```

Example 3 (typescript):
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

Example 4 (typescript):
```typescript
export class UpdateCatAgeDto extends PickType(CreateCatDto, ['age'] as const) {}
```

---

## 

**URL:** https://docs.nestjs.com/graphql/extensions

**Contents:**
  - Extensions
    - Adding custom metadata#
    - Using custom metadata#

Extensions is an advanced, low-level feature that lets you define arbitrary data in the types configuration. Attaching custom metadata to certain fields allows you to create more sophisticated, generic solutions. For example, with extensions, you can define field-level roles required to access particular fields. Such roles can be reflected at runtime to determine whether the caller has sufficient permissions to retrieve a specific field.

To attach custom metadata for a field, use the @Extensions() decorator exported from the @nestjs/graphql package.

In the example above, we assigned the role metadata property the value of Role.ADMIN. Role is a simple TypeScript enum that groups all the user roles available in our system.

Note, in addition to setting metadata on fields, you can use the @Extensions() decorator at the class level and method level (e.g., on the query handler).

Logic that leverages the custom metadata can be as complex as needed. For example, you can create a simple interceptor that stores/logs events per method invocation, or a field middleware that matches roles required to retrieve a field with the caller permissions (field-level permissions system).

For illustration purposes, let's define a checkRoleMiddleware that compares a user's role (hardcoded here) with a role required to access a target field:

With this in place, we can register a middleware for the password field, as follows:

**Examples:**

Example 1 (typescript):
```typescript
@Field()
@Extensions({ role: Role.ADMIN })
password: string;
```

Example 2 (typescript):
```typescript
export const checkRoleMiddleware: FieldMiddleware = async (
  ctx: MiddlewareContext,
  next: NextFn,
) => {
  const { info } = ctx;
  const { extensions } = info.parentType.getFields()[info.fieldName];

  /**
   * In a real-world application, the "userRole" variable
   * should represent the caller's (user) role (for example, "ctx.user.role").
   */
  const userRole = Role.USER;
  if (userRole === extensions.role) {
    // or just "return null" to ignore
    throw new ForbiddenException(
      `User does not have sufficient permissions to access "${info.fieldName}" field.`,
    );
  }
  return next();
};
```

Example 3 (typescript):
```typescript
@Field({ middleware: [checkRoleMiddleware] })
@Extensions({ role: Role.ADMIN })
password: string;
```

---

## 

**URL:** https://docs.nestjs.com/graphql/directives

**Contents:**
  - Directives
    - Custom directives#
    - Code first#
    - Schema first#

A directive can be attached to a field or fragment inclusion, and can affect execution of the query in any way the server desires (read more here). The GraphQL specification provides several default directives:

A directive is an identifier preceded by a @ character, optionally followed by a list of named arguments, which can appear after almost any element in the GraphQL query and schema languages.

To instruct what should happen when Apollo/Mercurius encounters your directive, you can create a transformer function. This function uses the mapSchema function to iterate through locations in your schema (field definitions, type definitions, etc.) and perform corresponding transformations.

Now, apply the upperDirectiveTransformer transformation function in the GraphQLModule#forRoot method using the transformSchema function:

Once registered, the @upper directive can be used in our schema. However, the way you apply the directive will vary depending on the approach you use (code first or schema first).

In the code first approach, use the @Directive() decorator to apply the directive.

Directives can be applied on fields, field resolvers, input and object types, as well as queries, mutations, and subscriptions. Here's an example of the directive applied on the query handler level:

Lastly, make sure to declare directives in the GraphQLModule, as follows:

In the schema first approach, apply directives directly in SDL.

**Examples:**

Example 1 (typescript):
```typescript
import { getDirective, MapperKind, mapSchema } from '@graphql-tools/utils';
import { defaultFieldResolver, GraphQLSchema } from 'graphql';

export function upperDirectiveTransformer(
  schema: GraphQLSchema,
  directiveName: string,
) {
  return mapSchema(schema, {
    [MapperKind.OBJECT_FIELD]: (fieldConfig) => {
      const upperDirective = getDirective(
        schema,
        fieldConfig,
        directiveName,
      )?.[0];

      if (upperDirective) {
        const { resolve = defaultFieldResolver } = fieldConfig;

        // Replace the original resolver with a function that *first* calls
        // the original resolver, then converts its result to upper case
        fieldConfig.resolve = async function (source, args, context, info) {
          const result = await resolve(source, args, context, info);
          if (typeof result === 'string') {
            return result.toUpperCase();
          }
          return result;
        };
        return fieldConfig;
      }
    },
  });
}
```

Example 2 (typescript):
```typescript
GraphQLModule.forRoot({
  // ...
  transformSchema: (schema) => upperDirectiveTransformer(schema, 'upper'),
});
```

Example 3 (typescript):
```typescript
@Directive('@upper')
@Field()
title: string;
```

Example 4 (typescript):
```typescript
@Directive('@deprecated(reason: "This query will be removed in the next version")')
@Query(() => Author, { name: 'author' })
async getAuthor(@Args({ name: 'id', type: () => Int }) id: number) {
  return this.authorsService.findOneById(id);
}
```

---

## 

**URL:** https://docs.nestjs.com/graphql/unions-and-enums

**Contents:**
  - Unions
    - Code first#
    - Schema first#
  - Enums
    - Code first#
    - Schema first#

Union types are very similar to interfaces, but they don't get to specify any common fields between the types (read more here). Unions are useful for returning disjoint data types from a single field.

To define a GraphQL union type, we must define classes that this union will be composed of. Following the example from the Apollo documentation, we'll create two classes. First, Book:

With this in place, register the ResultUnion union using the createUnionType function exported from the @nestjs/graphql package:

Now, we can reference the ResultUnion in our query:

This will result in generating the following part of the GraphQL schema in SDL:

The default resolveType() function generated by the library will extract the type based on the value returned from the resolver method. That means returning class instances instead of literal JavaScript object is obligatory.

To provide a customized resolveType() function, pass the resolveType property to the options object passed into the createUnionType() function, as follows:

To define a union in the schema first approach, simply create a GraphQL union with SDL.

Then, you can use the typings generation feature (as shown in the quick start chapter) to generate corresponding TypeScript definitions:

Unions require an extra __resolveType field in the resolver map to determine which type the union should resolve to. Also, note that the ResultUnionResolver class has to be registered as a provider in any module. Let's create a ResultUnionResolver class and define the __resolveType method.

Enumeration types are a special kind of scalar that is restricted to a particular set of allowed values (read more here). This allows you to:

When using the code first approach, you define a GraphQL enum type by simply creating a TypeScript enum.

With this in place, register the AllowedColor enum using the registerEnumType function exported from the @nestjs/graphql package:

Now you can reference the AllowedColor in our types:

This will result in generating the following part of the GraphQL schema in SDL:

To provide a description for the enum, pass the description property into the registerEnumType() function.

To provide a description for the enum values, or to mark a value as deprecated, pass the valuesMap property, as follows:

This will generate the following GraphQL schema in SDL:

To define an enumerator in the schema first approach, simply create a GraphQL enum with SDL.

Then you can use the typings generation feature (as shown in the quick start chapter) to generate corresponding TypeScript definitions:

Sometimes a backend forces a different value for an enum internally than in the public API. In this example the API contains RED, however in resolvers we may use #f00 instead (read more here). To accomplish this, declare a resolver object for the AllowedColor enum:

Then use this resolver object together with the resolvers property of the GraphQLModule#forRoot() method, as follows:

**Examples:**

Example 1 (typescript):
```typescript
import { Field, ObjectType } from '@nestjs/graphql';

@ObjectType()
export class Book {
  @Field()
  title: string;
}
```

Example 2 (typescript):
```typescript
import { Field, ObjectType } from '@nestjs/graphql';

@ObjectType()
export class Author {
  @Field()
  name: string;
}
```

Example 3 (typescript):
```typescript
export const ResultUnion = createUnionType({
  name: 'ResultUnion',
  types: () => [Author, Book] as const,
});
```

Example 4 (typescript):
```typescript
@Query(() => [ResultUnion])
search(): Array<typeof ResultUnion> {
  return [new Author(), new Book()];
}
```

---

## 

**URL:** https://docs.nestjs.com/graphql/subscriptions

**Contents:**
  - Subscriptions
    - Enable subscriptions with Apollo driver#
    - Code first#
    - Publishing#
    - Filtering subscriptions#
    - Mutating subscription payloads#
    - Schema first#
    - PubSub#
    - Customize subscriptions server#
    - Authentication over WebSockets#

In addition to fetching data using queries and modifying data using mutations, the GraphQL spec supports a third operation type, called subscription. GraphQL subscriptions are a way to push data from the server to the clients that choose to listen to real time messages from the server. Subscriptions are similar to queries in that they specify a set of fields to be delivered to the client, but instead of immediately returning a single answer, a channel is opened and a result is sent to the client every time a particular event happens on the server.

A common use case for subscriptions is notifying the client side about particular events, for example the creation of a new object, updated fields and so on (read more here).

To enable subscriptions, set the installSubscriptionHandlers property to true.

To switch to use the graphql-ws package instead, use the following configuration:

To create a subscription using the code first approach, we use the @Subscription() decorator (exported from the @nestjs/graphql package) and the PubSub class from the graphql-subscriptions package, which provides a simple publish/subscribe API.

The following subscription handler takes care of subscribing to an event by calling PubSub#asyncIterableIterator. This method takes a single argument, the triggerName, which corresponds to an event topic name.

This will result in generating the following part of the GraphQL schema in SDL:

Note that subscriptions, by definition, return an object with a single top level property whose key is the name of the subscription. This name is either inherited from the name of the subscription handler method (i.e., commentAdded above), or is provided explicitly by passing an option with the key name as the second argument to the @Subscription() decorator, as shown below.

This construct produces the same SDL as the previous code sample, but allows us to decouple the method name from the subscription.

Now, to publish the event, we use the PubSub#publish method. This is often used within a mutation to trigger a client-side update when a part of the object graph has changed. For example:

The PubSub#publish method takes a triggerName (again, think of this as an event topic name) as the first parameter, and an event payload as the second parameter. As mentioned, the subscription, by definition, returns a value and that value has a shape. Look again at the generated SDL for our commentAdded subscription:

This tells us that the subscription must return an object with a top-level property name of commentAdded that has a value which is a Comment object. The important point to note is that the shape of the event payload emitted by the PubSub#publish method must correspond to the shape of the value expected to return from the subscription. So, in our example above, the pubSub.publish('commentAdded', { commentAdded: newComment }) statement publishes a commentAdded event with the appropriately shaped payload. If these shapes don't match, your subscription will fail during the GraphQL validation phase.

To filter out specific events, set the filter property to a filter function. This function acts similar to the function passed to an array filter. It takes two arguments: payload containing the event payload (as sent by the event publisher), and variables taking any arguments passed in during the subscription request. It returns a boolean determining whether this event should be published to client listeners.

To mutate the published event payload, set the resolve property to a function. The function receives the event payload (as sent by the event publisher) and returns the appropriate value.

If you need to access injected providers (e.g., use an external service to validate the data), use the following construction.

The same construction works with filters:

To create an equivalent subscription in Nest, we'll make use of the @Subscription() decorator.

To filter out specific events based on context and arguments, set the filter property.

To mutate the published payload, we can use a resolve function.

If you need to access injected providers (e.g., use an external service to validate the data), use the following construction:

The same construction works with filters:

The last step is to update the type definitions file.

With this, we've created a single commentAdded(title: String!): Comment subscription. You can find a full sample implementation here.

We instantiated a local PubSub instance above. The preferred approach is to define PubSub as a provider and inject it through the constructor (using the @Inject() decorator). This allows us to re-use the instance across the whole application. For example, define a provider as follows, then inject 'PUB_SUB' where needed.

To customize the subscriptions server (e.g., change the path), use the subscriptions options property.

If you're using the graphql-ws package for subscriptions, replace the subscriptions-transport-ws key with graphql-ws, as follows:

Checking whether the user is authenticated can be done inside the onConnect callback function that you can specify in the subscriptions options.

The onConnect will receive as a first argument the connectionParams passed to the SubscriptionClient (read more).

The authToken in this example is only sent once by the client, when the connection is first established. All subscriptions made with this connection will have the same authToken, and thus the same user info.

If you're using the graphql-ws package, the signature of the onConnect callback will be slightly different:

To enable subscriptions, set the subscription property to true.

To create a subscription using the code first approach, we use the @Subscription() decorator (exported from the @nestjs/graphql package) and the PubSub class from the mercurius package, which provides a simple publish/subscribe API.

The following subscription handler takes care of subscribing to an event by calling PubSub#asyncIterableIterator. This method takes a single argument, the triggerName, which corresponds to an event topic name.

This will result in generating the following part of the GraphQL schema in SDL:

Note that subscriptions, by definition, return an object with a single top level property whose key is the name of the subscription. This name is either inherited from the name of the subscription handler method (i.e., commentAdded above), or is provided explicitly by passing an option with the key name as the second argument to the @Subscription() decorator, as shown below.

This construct produces the same SDL as the previous code sample, but allows us to decouple the method name from the subscription.

Now, to publish the event, we use the PubSub#publish method. This is often used within a mutation to trigger a client-side update when a part of the object graph has changed. For example:

As mentioned, the subscription, by definition, returns a value and that value has a shape. Look again at the generated SDL for our commentAdded subscription:

This tells us that the subscription must return an object with a top-level property name of commentAdded that has a value which is a Comment object. The important point to note is that the shape of the event payload emitted by the PubSub#publish method must correspond to the shape of the value expected to return from the subscription. So, in our example above, the pubSub.publish({ topic: 'commentAdded', payload: { commentAdded: newComment } }) statement publishes a commentAdded event with the appropriately shaped payload. If these shapes don't match, your subscription will fail during the GraphQL validation phase.

To filter out specific events, set the filter property to a filter function. This function acts similar to the function passed to an array filter. It takes two arguments: payload containing the event payload (as sent by the event publisher), and variables taking any arguments passed in during the subscription request. It returns a boolean determining whether this event should be published to client listeners.

If you need to access injected providers (e.g., use an external service to validate the data), use the following construction.

To create an equivalent subscription in Nest, we'll make use of the @Subscription() decorator.

To filter out specific events based on context and arguments, set the filter property.

If you need to access injected providers (e.g., use an external service to validate the data), use the following construction:

The last step is to update the type definitions file.

With this, we've created a single commentAdded(title: String!): Comment subscription.

In the examples above, we used the default PubSub emitter (mqemitter) The preferred approach (for production) is to use mqemitter-redis. Alternatively, a custom PubSub implementation can be provided (read more here)

Checking whether the user is authenticated can be done inside the verifyClient callback function that you can specify in the subscription options.

The verifyClient will receive the info object as a first argument which you can use to retrieve the request's headers.

**Examples:**

Example 1 (typescript):
```typescript
GraphQLModule.forRoot<ApolloDriverConfig>({
  driver: ApolloDriver,
  installSubscriptionHandlers: true,
}),
```

Example 2 (typescript):
```typescript
GraphQLModule.forRoot<ApolloDriverConfig>({
  driver: ApolloDriver,
  subscriptions: {
    'graphql-ws': true
  },
}),
```

Example 3 (typescript):
```typescript
const pubSub = new PubSub();

@Resolver(() => Author)
export class AuthorResolver {
  // ...
  @Subscription(() => Comment)
  commentAdded() {
    return pubSub.asyncIterableIterator('commentAdded');
  }
}
```

Example 4 (unknown):
```unknown
type Subscription {
  commentAdded(): Comment!
}
```

---

## 

**URL:** https://docs.nestjs.com/graphql/resolvers

**Contents:**
  - Resolvers
    - Code first#
    - Object types#
    - Code first resolver#
    - Query type names#
    - Query decorator options#
    - Args decorator options#
    - Dedicated arguments class#
    - Class inheritance#
    - Generics#

Resolvers provide the instructions for turning a GraphQL operation (a query, mutation, or subscription) into data. They return the same shape of data we specify in our schema -- either synchronously or as a promise that resolves to a result of that shape. Typically, you create a resolver map manually. The @nestjs/graphql package, on the other hand, generates a resolver map automatically using the metadata provided by decorators you use to annotate classes. To demonstrate the process of using the package features to create a GraphQL API, we'll create a simple authors API.

In the code first approach, we don't follow the typical process of creating our GraphQL schema by writing GraphQL SDL by hand. Instead, we use TypeScript decorators to generate the SDL from TypeScript class definitions. The @nestjs/graphql package reads the metadata defined through the decorators and automatically generates the schema for you.

Most of the definitions in a GraphQL schema are object types. Each object type you define should represent a domain object that an application client might need to interact with. For example, our sample API needs to be able to fetch a list of authors and their posts, so we should define the Author type and Post type to support this functionality.

If we were using the schema first approach, we'd define such a schema with SDL like this:

In this case, using the code first approach, we define schemas using TypeScript classes and using TypeScript decorators to annotate the fields of those classes. The equivalent of the above SDL in the code first approach is:

The Author object type, like any class, is made of a collection of fields, with each field declaring a type. A field's type corresponds to a GraphQL type. A field's GraphQL type can be either another object type or a scalar type. A GraphQL scalar type is a primitive (like ID, String, Boolean, or Int) that resolves to a single value.

The above Author object type definition will cause Nest to generate the SDL we showed above:

The @Field() decorator accepts an optional type function (e.g., type => Int), and optionally an options object.

The type function is required when there's the potential for ambiguity between the TypeScript type system and the GraphQL type system. Specifically: it is not required for string and boolean types; it is required for number (which must be mapped to either a GraphQL Int or Float). The type function should simply return the desired GraphQL type (as shown in various examples in these chapters).

The options object can have any of the following key/value pairs:

When the field is an array, we must manually indicate the array type in the Field() decorator's type function, as shown below:

To declare that an array's items (not the array itself) are nullable, set the nullable property to 'items' as shown below:

Now that the Author object type is created, let's define the Post object type.

The Post object type will result in generating the following part of the GraphQL schema in SDL:

At this point, we've defined the objects (type definitions) that can exist in our data graph, but clients don't yet have a way to interact with those objects. To address that, we need to create a resolver class. In the code first method, a resolver class both defines resolver functions and generates the Query type. This will be clear as we work through the example below:

You can define multiple resolver classes. Nest will combine these at run time. See the module section below for more on code organization.

In the example above, we created the AuthorsResolver which defines one query resolver function and one field resolver function. To create a resolver, we create a class with resolver functions as methods, and annotate the class with the @Resolver() decorator.

In this example, we defined a query handler to get the author object based on the id sent in the request. To specify that the method is a query handler, use the @Query() decorator.

The argument passed to the @Resolver() decorator is optional, but comes into play when our graph becomes non-trivial. It's used to supply a parent object used by field resolver functions as they traverse down through an object graph.

In our example, since the class includes a field resolver function (for the posts property of the Author object type), we must supply the @Resolver() decorator with a value to indicate which class is the parent type (i.e., the corresponding ObjectType class name) for all field resolvers defined within this class. As should be clear from the example, when writing a field resolver function, it's necessary to access the parent object (the object the field being resolved is a member of). In this example, we populate an author's posts array with a field resolver that calls a service which takes the author's id as an argument. Hence the need to identify the parent object in the @Resolver() decorator. Note the corresponding use of the @Parent() method parameter decorator to then extract a reference to that parent object in the field resolver.

We can define multiple @Query() resolver functions (both within this class, and in any other resolver class), and they will be aggregated into a single Query type definition in the generated SDL along with the appropriate entries in the resolver map. This allows you to define queries close to the models and services that they use, and to keep them well organized in modules.

In the above examples, the @Query() decorator generates a GraphQL schema query type name based on the method name. For example, consider the following construction from the example above:

This generates the following entry for the author query in our schema (the query type uses the same name as the method name):

Conventionally, we prefer to decouple these names; for example, we prefer to use a name like getAuthor() for our query handler method, but still use author for our query type name. The same applies to our field resolvers. We can easily do this by passing the mapping names as arguments of the @Query() and @ResolveField() decorators, as shown below:

The getAuthor handler method above will result in generating the following part of the GraphQL schema in SDL:

The @Query() decorator's options object (where we pass {name: 'author'} above) accepts a number of key/value pairs:

Use the @Args() decorator to extract arguments from a request for use in the method handler. This works in a very similar fashion to REST route parameter argument extraction.

Usually your @Args() decorator will be simple, and not require an object argument as seen with the getAuthor() method above. For example, if the type of an identifier is string, the following construction is sufficient, and simply plucks the named field from the inbound GraphQL request for use as a method argument.

In the getAuthor() case, the number type is used, which presents a challenge. The number TypeScript type doesn't give us enough information about the expected GraphQL representation (e.g., Int vs. Float). Thus we have to explicitly pass the type reference. We do that by passing a second argument to the Args() decorator, containing argument options, as shown below:

The options object allows us to specify the following optional key value pairs:

Query handler methods can take multiple arguments. Let's imagine that we want to fetch an author based on its firstName and lastName. In this case, we can call @Args twice:

With inline @Args() calls, code like the example above becomes bloated. Instead, you can create a dedicated GetAuthorArgs arguments class and access it in the handler method as follows:

Create the GetAuthorArgs class using @ArgsType() as shown below:

This will result in generating the following part of the GraphQL schema in SDL:

You can use standard TypeScript class inheritance to create base classes with generic utility type features (fields and field properties, validations, etc.) that can be extended. For example, you may have a set of pagination related arguments that always include the standard offset and limit fields, but also other index fields that are type-specific. You can set up a class hierarchy as shown below.

Base @ArgsType() class:

Type specific sub-class of the base @ArgsType() class:

The same approach can be taken with @ObjectType() objects. Define generic properties on the base class:

Add type-specific properties on sub-classes:

You can use inheritance with a resolver as well. You can ensure type safety by combining inheritance and TypeScript generics. For example, to create a base class with a generic findAll query, use a construction like this:

Here's how you could generate a concrete sub-class of the BaseResolver:

This construct would generated the following SDL:

We saw one use of generics above. This powerful TypeScript feature can be used to create useful abstractions. For example, here's a sample cursor-based pagination implementation based on this documentation:

With the above base class defined, we can now easily create specialized types that inherit this behavior. For example:

As mentioned in the previous chapter, in the schema first approach we start by manually defining schema types in SDL (read more). Consider the following SDL type definitions.

The schema above exposes a single query - author(id: Int!): Author.

Let's now create an AuthorsResolver class that resolves author queries:

The @Resolver() decorator is required. It takes an optional string argument with the name of a class. This class name is required whenever the class includes @ResolveField() decorators to inform Nest that the decorated method is associated with a parent type (the Author type in our current example). Alternatively, instead of setting @Resolver() at the top of the class, this can be done for each method:

In this case (@Resolver() decorator at the method level), if you have multiple @ResolveField() decorators inside a class, you must add @Resolver() to all of them. This is not considered the best practice (as it creates extra overhead).

In the above examples, the @Query() and @ResolveField() decorators are associated with GraphQL schema types based on the method name. For example, consider the following construction from the example above:

This generates the following entry for the author query in our schema (the query type uses the same name as the method name):

Conventionally, we would prefer to decouple these, using names like getAuthor() or getPosts() for our resolver methods. We can easily do this by passing the mapping name as an argument to the decorator, as shown below:

Assuming that we use the schema first approach and have enabled the typings generation feature (with outputAs: 'class' as shown in the previous chapter), once you run the application it will generate the following file (in the location you specified in the GraphQLModule.forRoot() method). For example, in src/graphql.ts:

By generating classes (instead of the default technique of generating interfaces), you can use declarative validation decorators in combination with the schema first approach, which is an extremely useful technique (read more). For example, you could add class-validator decorators to the generated CreatePostInput class as shown below to enforce minimum and maximum string lengths on the title field:

However, if you add decorators directly to the automatically generated file, they will be overwritten each time the file is generated. Instead, create a separate file and simply extend the generated class.

We can access the standard GraphQL resolver arguments using dedicated decorators. Below is a comparison of the Nest decorators and the plain Apollo parameters they represent.

These arguments have the following meanings:

Explore your graph with NestJS Devtools Graph visualizer Routes navigator Interactive playground CI/CD integration Sign up

Once we're done with the above steps, we have declaratively specified all the information needed by the GraphQLModule to generate a resolver map. The GraphQLModule uses reflection to introspect the meta data provided via the decorators, and transforms classes into the correct resolver map automatically.

The only other thing you need to take care of is to provide (i.e., list as a provider in some module) the resolver class(es) (AuthorsResolver), and importing the module (AuthorsModule) somewhere, so Nest will be able to utilize it.

For example, we can do this in an AuthorsModule, which can also provide other services needed in this context. Be sure to import AuthorsModule somewhere (e.g., in the root module, or some other module imported by the root module).

**Examples:**

Example 1 (css):
```css
type Author {
  id: Int!
  firstName: String
  lastName: String
  posts: [Post!]!
}
```

Example 2 (typescript):
```typescript
import { Field, Int, ObjectType } from '@nestjs/graphql';
import { Post } from './post';

@ObjectType()
export class Author {
  @Field(type => Int)
  id: number;

  @Field({ nullable: true })
  firstName?: string;

  @Field({ nullable: true })
  lastName?: string;

  @Field(type => [Post])
  posts: Post[];
}
```

Example 3 (css):
```css
type Author {
  id: Int!
  firstName: String
  lastName: String
  posts: [Post!]!
}
```

Example 4 (typescript):
```typescript
@Field({ description: `Book title`, deprecationReason: 'Not useful in v2 schema' })
title: string;
```

---
