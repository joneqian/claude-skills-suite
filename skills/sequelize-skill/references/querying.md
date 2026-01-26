# Sequelize - Querying

**Pages:** 6

---

## Raw Queries

**URL:** https://sequelize.org/docs/v6/core-concepts/raw-queries/

**Contents:**
- Raw Queries
- "Dotted" attributes and the nest option​
- Replacements​
- Bind Parameter​

As there are often use cases in which it is just easier to execute raw / already prepared SQL queries, you can use the sequelize.query method.

By default the function will return two arguments - a results array, and an object containing metadata (such as amount of affected rows, etc). Note that since this is a raw query, the metadata are dialect specific. Some dialects return the metadata "within" the results object (as properties on an array). However, two arguments will always be returned, but for MSSQL and MySQL it will be two references to the same object.

In cases where you don't need to access the metadata you can pass in a query type to tell sequelize how to format the results. For example, for a simple select query you could do:

Several other query types are available. Peek into the source for details.

A second option is the model. If you pass a model the returned data will be instances of that model.

See more options in the query API reference. Some examples:

If an attribute name of the table contains dots, the resulting objects can become nested objects by setting the nest: true option. This is achieved with dottie.js under the hood. See below:

Replacements in a query can be done in two different ways, either using named parameters (starting with :), or unnamed, represented by a ?. Replacements are passed in the options object.

Array replacements will automatically be handled, the following query searches for projects where the status matches an array of values.

To use the wildcard operator %, append it to your replacement. The following query matches users with names that start with 'ben'.

Bind parameters are like replacements. Except replacements are escaped and inserted into the query by sequelize before the query is sent to the database, while bind parameters are sent to the database outside the SQL query text. A query can have either bind parameters or replacements. Bind parameters are referred to by either $1, $2, ... (numeric) or $key (alpha-numeric). This is independent of the dialect.

The array or object must contain all bound values or Sequelize will throw an exception. This applies even to cases in which the database may ignore the bound parameter.

The database may add further restrictions to this. Bind parameters cannot be SQL keywords, nor table or column names. They are also ignored in quoted text or data. In PostgreSQL it may also be needed to typecast them, if the type cannot be inferred from the context $1::varchar.

**Examples:**

Example 1 (sql):
```sql
const [results, metadata] = await sequelize.query('UPDATE users SET y = 42 WHERE x = 12');// Results will be an empty array and metadata will contain the number of affected rows.
```

Example 2 (sql):
```sql
const { QueryTypes } = require('sequelize');const users = await sequelize.query('SELECT * FROM `users`', {  type: QueryTypes.SELECT,});// We didn't need to destructure the result here - the results were returned directly
```

Example 3 (sql):
```sql
// Callee is the model definition. This allows you to easily map a query to a predefined modelconst projects = await sequelize.query('SELECT * FROM projects', {  model: Projects,  mapToModel: true, // pass true here if you have any mapped fields});// Each element of `projects` is now an instance of Project
```

Example 4 (sql):
```sql
const { QueryTypes } = require('sequelize');await sequelize.query('SELECT 1', {  // A function (or false) for logging your queries  // Will get called for every SQL query that gets sent  // to the server.  logging: console.log,  // If plain is true, then sequelize will only return the first  // record of the result set. In case of false it will return all records.  plain: false,  // Set this to true if you don't have a model definition for your query.  raw: false,  // The type of query you are executing. The query type affects how results are formatted before they are passed back.  type: QueryTypes.SELECT,});// Note the second argument being null!// Even if we declared a callee here, the raw: true would// supersede and return a raw object.console.log(await sequelize.query('SELECT * FROM projects', { raw: true }));
```

---

## Association Scopes

**URL:** https://sequelize.org/docs/v6/advanced-association-concepts/association-scopes/

**Contents:**
- Association Scopes
- Concept​
- Example​
- Achieving the same behavior with standard scopes​

This section concerns association scopes, which are similar but not the same as model scopes.

Association scopes can be placed both on the associated model (the target of the association) and on the through table for Many-to-Many relationships.

Similarly to how a model scope is automatically applied on the model static calls, such as Model.scope('foo').findAll(), an association scope is a rule (more precisely, a set of default attributes and options) that is automatically applied on instance calls from the model. Here, instance calls mean method calls that are called from an instance (rather than from the Model itself). Mixins are the main example of instance methods (instance.getSomething, instance.setSomething, instance.addSomething and instance.createSomething).

Association scopes behave just like model scopes, in the sense that both cause an automatic application of things like where clauses to finder calls; the difference being that instead of applying to static finder calls (which is the case for model scopes), the association scopes automatically apply to instance finder calls (such as mixins).

A basic example of an association scope for the One-to-Many association between models Foo and Bar is shown below.

After this setup, calling myFoo.getOpenBars() generates the following SQL:

With this we can see that upon calling the .getOpenBars() mixin, the association scope { status: 'open' } was automatically applied into the WHERE clause of the generated SQL.

We could have achieved the same behavior with standard scopes:

With the above code, myFoo.getOpenBars() yields the same SQL shown above.

**Examples:**

Example 1 (javascript):
```javascript
const Foo = sequelize.define('foo', { name: DataTypes.STRING });const Bar = sequelize.define('bar', { status: DataTypes.STRING });Foo.hasMany(Bar, {  scope: {    status: 'open',  },  as: 'openBars',});await sequelize.sync();const myFoo = await Foo.create({ name: 'My Foo' });
```

Example 2 (sql):
```sql
SELECT    `id`, `status`, `createdAt`, `updatedAt`, `fooId`FROM `bars` AS `bar`WHERE `bar`.`status` = 'open' AND `bar`.`fooId` = 1;
```

Example 3 (css):
```css
// Foo.hasMany(Bar, {//     scope: {//         status: 'open'//     },//     as: 'openBars'// });Bar.addScope('open', {  where: {    status: 'open',  },});Foo.hasMany(Bar);Foo.hasMany(Bar.scope('open'), { as: 'openBars' });
```

---

## Model Querying - Finders

**URL:** https://sequelize.org/docs/v6/core-concepts/model-querying-finders/

**Contents:**
- Model Querying - Finders
- findAll​
- findByPk​
- findOne​
- findOrCreate​
- findAndCountAll​

Finder methods are the ones that generate SELECT queries.

By default, the results of all finder methods are instances of the model class (as opposed to being just plain JavaScript objects). This means that after the database returns the results, Sequelize automatically wraps everything in proper instance objects. In a few cases, when there are too many results, this wrapping can be inefficient. To disable this wrapping and receive a plain response instead, pass { raw: true } as an option to the finder method.

The findAll method is already known from the previous tutorial. It generates a standard SELECT query which will retrieve all entries from the table (unless restricted by something like a where clause, for example).

The findByPk method obtains only a single entry from the table, using the provided primary key.

The findOne method obtains the first entry it finds (that fulfills the optional query options, if provided).

The method findOrCreate will create an entry in the table unless it can find one fulfilling the query options. In both cases, it will return an instance (either the found instance or the created instance) and a boolean indicating whether that instance was created or already existed.

The where option is considered for finding the entry, and the defaults option is used to define what must be created in case nothing was found. If the defaults do not contain values for every column, Sequelize will take the values given to where (if present).

Let's assume we have an empty database with a User model which has a username and a job.

The findAndCountAll method is a convenience method that combines findAll and count. This is useful when dealing with queries related to pagination where you want to retrieve data with a limit and offset but also need to know the total number of records that match the query.

When group is not provided, the findAndCountAll method returns an object with two properties:

When group is provided, the findAndCountAll method returns an object with two properties:

**Examples:**

Example 1 (javascript):
```javascript
const project = await Project.findByPk(123);if (project === null) {  console.log('Not found!');} else {  console.log(project instanceof Project); // true  // Its primary key is 123}
```

Example 2 (javascript):
```javascript
const project = await Project.findOne({ where: { title: 'My Title' } });if (project === null) {  console.log('Not found!');} else {  console.log(project instanceof Project); // true  console.log(project.title); // 'My Title'}
```

Example 3 (javascript):
```javascript
const [user, created] = await User.findOrCreate({  where: { username: 'sdepold' },  defaults: {    job: 'Technical Lead JavaScript',  },});console.log(user.username); // 'sdepold'console.log(user.job); // This may or may not be 'Technical Lead JavaScript'console.log(created); // The boolean indicating whether this instance was just createdif (created) {  console.log(user.job); // This will certainly be 'Technical Lead JavaScript'}
```

Example 4 (javascript):
```javascript
const { count, rows } = await Project.findAndCountAll({  where: {    title: {      [Op.like]: 'foo%',    },  },  offset: 10,  limit: 2,});console.log(count);console.log(rows);
```

---

## Scopes

**URL:** https://sequelize.org/docs/v6/other-topics/scopes/

**Contents:**
- Scopes
- Definition​
- Usage​
- Merging​
  - Merging includes​

Scopes are used to help you reuse code. You can define commonly used queries, specifying options such as where, include, limit, etc.

This guide concerns model scopes. You might also be interested in the guide for association scopes, which are similar but not the same thing.

Scopes are defined in the model definition and can be finder objects, or functions returning finder objects - except for the default scope, which can only be an object:

You can also add scopes after a model has been defined by calling YourModel.addScope. This is especially useful for scopes with includes, where the model in the include might not be defined at the time the other model is being defined.

The default scope is always applied. This means, that with the model definition above, Project.findAll() will create the following query:

The default scope can be removed by calling .unscoped(), .scope(null), or by invoking another scope:

It is also possible to include scoped models in a scope definition. This allows you to avoid duplicating include, attributes or where definitions. Using the above example, and invoking the active scope on the included User model (rather than specifying the condition directly in that include object):

Scopes are applied by calling .scope on the model definition, passing the name of one or more scopes. .scope returns a fully functional model instance with all the regular methods: .findAll, .update, .count, .destroy etc. You can save this model instance and reuse it later:

Scopes apply to .find, .findAll, .count, .update, .increment and .destroy.

Scopes which are functions can be invoked in two ways. If the scope does not take any arguments it can be invoked as normally. If the scope takes arguments, pass an object:

Several scopes can be applied simultaneously by passing an array of scopes to .scope, or by passing the scopes as consecutive arguments.

If you want to apply another scope alongside the default scope, pass the key defaultScope to .scope:

When invoking several scopes, keys from subsequent scopes will overwrite previous ones (similarly to Object.assign), except for where and include, which will be merged. Consider two scopes:

Using .scope('scope1', 'scope2') will yield the following WHERE clause:

Note how limit and age are overwritten by scope2, while firstName is preserved. The limit, offset, order, paranoid, lock and raw fields are overwritten, while where is by default shallowly merged (meaning that identical keys will be overwritten). If the flag whereMergeStrategy is set to and (on the model or on the sequelize instance), where fields will be merged using the and operator.

For instance, if YourModel was initialized as such:

Using .scope('scope1', 'scope2') will yield the following WHERE clause:

Note that attributes keys of multiple applied scopes are merged in such a way that attributes.exclude are always preserved. This allows merging several scopes and never leaking sensitive fields in final scope.

The same merge logic applies when passing a find object directly to findAll (and similar finders) on a scoped model:

Generated where clause:

Here the deleted scope is merged with the finder. If we were to pass where: { firstName: 'john', deleted: false } to the finder, the deleted scope would be overwritten.

Includes are merged recursively based on the models being included. This is a very powerful merge, added on v5, and is better understood with an example.

Consider the models Foo, Bar, Baz and Qux, with One-to-Many associations as follows:

Now, consider the following four scopes defined on Foo:

These four scopes can be deeply merged easily, for example by calling Foo.scope('includeEverything', 'limitedBars', 'limitedBazs', 'excludeBazName').findAll(), which would be entirely equivalent to calling the following:

Observe how the four scopes were merged into one. The includes of scopes are merged based on the model being included. If one scope includes model A and another includes model B, the merged result will include both models A and B. On the other hand, if both scopes include the same model A, but with different options (such as nested includes or other attributes), those will be merged recursively, as shown above.

The merge illustrated above works in the exact same way regardless of the order applied to the scopes. The order would only make a difference if a certain option was set by two different scopes - which is not the case of the above example, since each scope does a different thing.

This merge strategy also works in the exact same way with options passed to .findAll, .findOne and the like.

**Examples:**

Example 1 (gdscript):
```gdscript
class Project extends Model {}Project.init(  {    // Attributes  },  {    defaultScope: {      where: {        active: true,      },    },    scopes: {      deleted: {        where: {          deleted: true,        },      },      activeUsers: {        include: [{ model: User, where: { active: true } }],      },      random() {        return {          where: {            someNumber: Math.random(),          },        };      },      accessLevel(value) {        return {          where: {            accessLevel: {              [Op.gte]: value,            },          },        };      },      sequelize,      modelName: 'project',    },  },);
```

Example 2 (sql):
```sql
SELECT * FROM projects WHERE active = true
```

Example 3 (csharp):
```csharp
await Project.scope('deleted').findAll(); // Removes the default scope
```

Example 4 (sql):
```sql
SELECT * FROM projects WHERE deleted = true
```

---

## Sub Queries

**URL:** https://sequelize.org/docs/v6/other-topics/sub-queries/

**Contents:**
- Sub Queries
- Using sub-queries for complex ordering​

Consider you have two models, Post and Reaction, with a One-to-Many relationship set up, so that one post has many reactions:

Note: we have disabled timestamps just to have shorter queries for the next examples.

Let's fill our tables with some data:

Now, we are ready for examples of the power of subqueries.

Let's say we wanted to compute via SQL a laughReactionsCount for each post. We can achieve that with a sub-query, such as the following:

If we run the above raw SQL query through Sequelize, we get:

So how can we achieve that with more help from Sequelize, without having to write the whole raw query by hand?

The answer: by combining the attributes option of the finder methods (such as findAll) with the sequelize.literal utility function, that allows you to directly insert arbitrary content into the query without any automatic escaping.

This means that Sequelize will help you with the main, larger query, but you will still have to write that sub-query by yourself:

Important Note: Since sequelize.literal inserts arbitrary content without escaping to the query, it deserves very special attention since it may be a source of (major) security vulnerabilities. It should not be used on user-generated content. However, here, we are using sequelize.literal with a fixed string, carefully written by us (the coders). This is ok, since we know what we are doing.

The above gives the following output:

This idea can be used to enable complex ordering, such as ordering posts by the number of laugh reactions they have:

**Examples:**

Example 1 (css):
```css
const Post = sequelize.define(  'post',  {    content: DataTypes.STRING,  },  { timestamps: false },);const Reaction = sequelize.define(  'reaction',  {    type: DataTypes.STRING,  },  { timestamps: false },);Post.hasMany(Reaction);Reaction.belongsTo(Post);
```

Example 2 (javascript):
```javascript
async function makePostWithReactions(content, reactionTypes) {  const post = await Post.create({ content });  await Reaction.bulkCreate(reactionTypes.map(type => ({ type, postId: post.id })));  return post;}await makePostWithReactions('Hello World', [  'Like',  'Angry',  'Laugh',  'Like',  'Like',  'Angry',  'Sad',  'Like',]);await makePostWithReactions('My Second Post', ['Laugh', 'Laugh', 'Like', 'Laugh']);
```

Example 3 (sql):
```sql
SELECT    *,    (        SELECT COUNT(*)        FROM reactions AS reaction        WHERE            reaction.postId = post.id            AND            reaction.type = "Laugh"    ) AS laughReactionsCountFROM posts AS post
```

Example 4 (json):
```json
[  {    "id": 1,    "content": "Hello World",    "laughReactionsCount": 1  },  {    "id": 2,    "content": "My Second Post",    "laughReactionsCount": 3  }]
```

---

## Model Querying - Basics

**URL:** https://sequelize.org/docs/v6/core-concepts/model-querying-basics/

**Contents:**
- Model Querying - Basics
- Simple INSERT queries​
- Simple SELECT queries​
- Specifying attributes for SELECT queries​
- Applying WHERE clauses​
  - The basics​
  - Operators​
    - Shorthand syntax for Op.in​
  - Logical combinations with operators​
    - Examples with Op.and and Op.or​

Sequelize provides various methods to assist querying your database for data.

Important notice: to perform production-ready queries with Sequelize, make sure you have read the Transactions guide as well. Transactions are important to ensure data integrity and to provide other benefits.

This guide will show how to make the standard CRUD queries.

First, a simple example:

The Model.create() method is a shorthand for building an unsaved instance with Model.build() and saving the instance with instance.save().

It is also possible to define which attributes can be set in the create method. This can be especially useful if you create database entries based on a form which can be filled by a user. Using that would, for example, allow you to restrict the User model to set only a username but not an admin flag (i.e., isAdmin):

You can read the whole table from the database with the findAll method:

To select only some attributes, you can use the attributes option:

Attributes can be renamed using a nested array:

You can use sequelize.fn to do aggregations:

When using aggregation function, you must give it an alias to be able to access it from the model. In the example above you can get the number of hats with instance.n_hats.

Sometimes it may be tiresome to list all the attributes of the model if you only want to add an aggregation:

Similarly, it's also possible to remove a selected few attributes:

The where option is used to filter the query. There are lots of operators to use for the where clause, available as Symbols from Op.

Observe that no operator (from Op) was explicitly passed, so Sequelize assumed an equality comparison by default. The above code is equivalent to:

Multiple checks can be passed:

Just like Sequelize inferred the Op.eq operator in the first example, here Sequelize inferred that the caller wanted an AND for the two checks. The code above is equivalent to:

An OR can be easily performed in a similar way:

Since the above was an OR involving the same field, Sequelize allows you to use a slightly different structure which is more readable and generates the same behavior:

Sequelize provides several operators.

Passing an array directly to the where option will implicitly use the IN operator:

The operators Op.and, Op.or and Op.not can be used to create arbitrarily complex nested logical comparisons.

The above will generate:

What if you wanted to obtain something like WHERE char_length("content") = 7?

Note the usage of the sequelize.fn and sequelize.col methods, which should be used to specify an SQL function call and a table column, respectively. These methods should be used instead of passing a plain string (such as char_length(content)) because Sequelize needs to treat this situation differently (for example, using other symbol escaping approaches).

What if you need something even more complex?

The above generates the following SQL:

Range types can be queried with all supported operators.

Keep in mind, the provided range value can define the bound inclusion/exclusion as well.

In Sequelize v4, it was possible to specify strings to refer to operators, instead of using Symbols. This is now deprecated and heavily discouraged, and will probably be removed in the next major version. If you really need it, you can pass the operatorAliases option in the Sequelize constructor.

Update queries also accept the where option, just like the read queries shown above.

Delete queries also accept the where option, just like the read queries shown above.

To destroy everything the TRUNCATE SQL can be used:

Sequelize provides the Model.bulkCreate method to allow creating multiple records at once, with only one query.

The usage of Model.bulkCreate is very similar to Model.create, by receiving an array of objects instead of a single object.

However, by default, bulkCreate does not run validations on each object that is going to be created (which create does). To make bulkCreate run these validations as well, you must pass the validate: true option. This will decrease performance. Usage example:

If you are accepting values directly from the user, it might be beneficial to limit the columns that you want to actually insert. To support this, bulkCreate() accepts a fields option, an array defining which fields must be considered (the rest will be ignored).

Sequelize provides the order and group options to work with ORDER BY and GROUP BY.

The order option takes an array of items to order the query by or a sequelize method. These items are themselves arrays in the form [column, direction]. The column will be escaped correctly and the direction will be checked in a whitelist of valid directions (such as ASC, DESC, NULLS FIRST, etc).

To recap, the elements of the order array can be the following:

The syntax for grouping and ordering are equal, except that grouping does not accept a direction as last argument of the array (there is no ASC, DESC, NULLS FIRST, etc).

You can also pass a string directly to group, which will be included directly (verbatim) into the generated SQL. Use with caution and don't use with user generated content.

The limit and offset options allow you to work with limiting / pagination:

Usually these are used alongside the order option.

Sequelize also provides a few utility methods.

The count method simply counts the occurrences of elements in the database.

Sequelize also provides the max, min and sum convenience methods.

Let's assume we have three users, whose ages are 10, 5, and 40.

Sequelize also provides the increment convenience method.

Let's assume we have a user, whose age is 10.

**Examples:**

Example 1 (javascript):
```javascript
// Create a new userconst jane = await User.create({ firstName: 'Jane', lastName: 'Doe' });console.log("Jane's auto-generated ID:", jane.id);
```

Example 2 (javascript):
```javascript
const user = await User.create(  {    username: 'alice123',    isAdmin: true,  },  { fields: ['username'] },);// let's assume the default of isAdmin is falseconsole.log(user.username); // 'alice123'console.log(user.isAdmin); // false
```

Example 3 (javascript):
```javascript
// Find all usersconst users = await User.findAll();console.log(users.every(user => user instanceof User)); // trueconsole.log('All users:', JSON.stringify(users, null, 2));
```

Example 4 (sql):
```sql
SELECT * FROM ...
```

---
