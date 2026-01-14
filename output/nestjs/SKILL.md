---
name: nestjs
description: NestJS progressive Node.js framework. Use for building scalable server-side applications, TypeScript backend development, dependency injection, modules, controllers, providers, middleware, guards, interceptors, pipes, and microservices architecture.
---

# Nestjs Skill

Nestjs progressive node.js framework. use for building scalable server-side applications, typescript backend development, dependency injection, modules, controllers, providers, middleware, guards, interceptors, pipes, and microservices architecture., generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with nestjs
- Asking about nestjs features or APIs
- Implementing nestjs solutions
- Debugging nestjs code
- Learning nestjs best practices

## Quick Reference

### Common Patterns

**Pattern 1:** Alternatively, the @Prop() decorator accepts an options object argument (read more about the available options). With this, you can indicate whether a property is required or not, specify a default value, or mark it as immutable. For example:

```
@Prop()
```

**Pattern 2:** Alternatively, if you prefer not using decorators, you can define a schema manually. For example:

```
export const CatSchema = new mongoose.Schema({
  name: String,
  age: Number,
  breed: String,
});
```

**Pattern 3:** To make this easier, the @nestjs/mongoose package exposes a getModelToken() function that returns a prepared injection token based on a token name. Using this token, you can easily provide a mock implementation using any of the standard custom provider techniques, including useClass, useValue, and useFactory. For example:

```
@nestjs/mongoose
```

**Pattern 4:** That said, routes that previously worked in Express v4 may not work in Express v5. For example:

```
@Get('users/*')
findAll() {
  // In NestJS 11, this will be automatically converted to a valid Express v5 route.
  // While it may still work, it's no longer advisable to use this wildcard syntax in Express v5.
  return 'This route should not work in Express v5';
}
```

**Pattern 5:** Any standard Passport customization options can be passed the same way, using the register() method. The available options depend on the strategy being implemented. For example:

```
register()
```

**Pattern 6:** The PartialType() function takes an optional second argument that is a reference to a decorator factory. This argument can be used to change the decorator function applied to the resulting (child) class. If not specified, the child class effectively uses the same decorator as the parent class (the class referenced in the first argument). In the example above, we are extending CreateUserInput which is annotated with the @InputType() decorator. Since we want UpdateUserInput to also be treated as if it were decorated with @InputType(), we didn't need to pass InputType as the second argument. If the parent and child types are different, (e.g., the parent is decorated with @ObjectType), we would pass InputType as the second argument. For example:

```
PartialType()
```

**Pattern 7:** To understand how these can be used in conjunction with the aforementioned FileParsePipe, we'll use an altered snippet of the last presented example:

```
FileParsePipe
```

**Pattern 8:** Now let's review and refine our requirements for this example:

```
article.authorId === userId
```

### Example Code Patterns

**Example 1** (typescript):
```typescript
const user = req.user;
```

**Example 2** (typescript):
```typescript
@ObjectType()
export class Recipe {
  @Field({ middleware: [loggerMiddleware] })
  title: string;
}
```

**Example 3** (typescript):
```typescript
import { Injectable, Scope } from '@nestjs/common';

@Injectable({ scope: Scope.REQUEST })
export class CatsService {}
```

**Example 4** (typescript):
```typescript
{
  provide: 'CACHE_MANAGER',
  useClass: CacheManager,
  scope: Scope.TRANSIENT,
}
```

**Example 5** (bash):
```bash
$ npm i --save-dev @nestjs/testing
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **cli.md** - Cli documentation
- **fundamentals.md** - Fundamentals documentation
- **graphql.md** - Graphql documentation
- **microservices.md** - Microservices documentation
- **openapi.md** - Openapi documentation
- **other.md** - Other documentation
- **overview.md** - Overview documentation
- **recipes.md** - Recipes documentation
- **security.md** - Security documentation
- **techniques.md** - Techniques documentation
- **websockets.md** - Websockets documentation

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with the getting_started or tutorials reference files for foundational concepts.

### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
