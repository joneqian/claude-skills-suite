# Sequelize - Advanced

**Pages:** 5

---

## Hooks

**URL:** https://sequelize.org/docs/v6/other-topics/hooks/

**Contents:**
- Hooks
- Available hooks​
- Hooks firing order​
- Declaring Hooks​
- Removing hooks​
- Global / universal hooks​
  - Default Hooks (on Sequelize constructor options)​
  - Permanent Hooks (with sequelize.addHook)​
  - Connection Hooks​
- Instance hooks​

Hooks (also known as lifecycle events), are functions which are called before and after calls in sequelize are executed. For example, if you want to always set a value on a model before saving it, you can add a beforeUpdate hook.

Note: You can't use hooks with instances. Hooks are used with models.

Sequelize provides a lot of hooks. The full list can be found in directly in the source code - src/hooks.js.

The diagram below shows the firing order for the most common hooks.

Note: this list is not exhaustive.

Arguments to hooks are passed by reference. This means, that you can change the values, and this will be reflected in the insert / update statement. A hook may contain async actions - in this case the hook function should return a promise.

There are currently three ways to programmatically add hooks:

Only a hook with name param can be removed.

You can have many hooks with same name. Calling .removeHook() will remove all of them.

Global hooks are hooks that are run for all models. They are especially useful for plugins and can define behaviours that you want for all your models, for example to allow customization on timestamps using sequelize.define on your models:

They can be defined in many ways, which have slightly different semantics:

This adds a default hook to all models, which is run if the model does not define its own beforeCreate hook:

This hook is always run, whether or not the model specifies its own beforeCreate hook. Local hooks are always run before global hooks:

Permanent hooks may also be defined in the options passed to the Sequelize constructor:

Note that the above is not the same as the Default Hooks mentioned above. That one uses the define option of the constructor. This one does not.

Sequelize provides four hooks that are executed immediately before and after a database connection is obtained or released:

These hooks can be useful if you need to asynchronously obtain database credentials, or need to directly access the low-level database connection after it has been created.

For example, we can asynchronously obtain a database password from a rotating token store, and mutate Sequelize's configuration object with the new credentials:

You can also use two hooks that are executed immediately before and after a pool connection is acquired:

These hooks may only be declared as a permanent global hook, as the connection pool is shared by all models.

The following hooks will emit whenever you're editing a single object:

The following example will throw an error:

The following example will be successful:

Sometimes you'll be editing more than one record at a time by using methods like bulkCreate, update and destroy. The following hooks will emit whenever you're using one of those methods:

Note: methods like bulkCreate do not emit individual hooks by default - only the bulk hooks. However, if you want individual hooks to be emitted as well, you can pass the { individualHooks: true } option to the query call. However, this can drastically impact performance, depending on the number of records involved (since, among other things, all instances will be loaded into memory). Examples:

If you use Model.bulkCreate(...) with the updateOnDuplicate option, changes made in the hook to fields that aren't given in the updateOnDuplicate array will not be persisted to the database. However it is possible to change the updateOnDuplicate option inside the hook if this is what you want.

Only Model methods trigger hooks. This means there are a number of cases where Sequelize will interact with the database without triggering hooks. These include but are not limited to:

If you need to react to these events, consider using your database's native triggers and notification system instead.

As indicated in Exceptions, Sequelize will not trigger hooks when instances are deleted by the database because of an ON DELETE CASCADE constraint.

However, if you set the hooks option to true when defining your association, Sequelize will trigger the beforeDestroy and afterDestroy hooks for the deleted instances.

Using this option is discouraged for the following reasons:

This option is considered legacy. We highly recommend using your database's triggers and notification system if you need to be notified of database changes.

Here is an example of how to use this option:

For the most part hooks will work the same for instances when being associated.

When using add mixin methods for belongsToMany relationships (that will add one or more records to the junction table) the beforeBulkCreate and afterBulkCreate hooks in the junction model will run.

When using remove mixin methods for belongsToMany relationships (that will remove one or more records to the junction table) the beforeBulkDestroy and afterBulkDestroy hooks in the junction model will run.

If your association is Many-to-Many, you may be interested in firing hooks on the through model when using the remove call. Internally, sequelize is using Model.destroy resulting in calling the bulkDestroy instead of the before/afterDestroy hooks on each through instance.

Many model operations in Sequelize allow you to specify a transaction in the options parameter of the method. If a transaction is specified in the original call, it will be present in the options parameter passed to the hook function. For example, consider the following snippet:

If we had not included the transaction option in our call to User.update in the preceding code, no change would have occurred, since our newly created user does not exist in the database until the pending transaction has been committed.

It is very important to recognize that sequelize may make use of transactions internally for certain operations such as Model.findOrCreate. If your hook functions execute read or write operations that rely on the object's presence in the database, or modify the object's stored values like the example in the preceding section, you should always specify { transaction: options.transaction }:

This way your hooks will always behave correctly.

**Examples:**

Example 1 (markdown):
```markdown
(1)  beforeBulkCreate(instances, options)  beforeBulkDestroy(options)  beforeBulkUpdate(options)(2)  beforeValidate(instance, options)[... validation happens ...](3)  afterValidate(instance, options)  validationFailed(instance, options, error)(4)  beforeCreate(instance, options)  beforeDestroy(instance, options)  beforeUpdate(instance, options)  beforeSave(instance, options)  beforeUpsert(values, options)[... creation/update/destruction happens ...](5)  afterCreate(instance, options)  afterDestroy(instance, options)  afterUpdate(instance, options)  afterSave(instance, options)  afterUpsert(created, options)(6)  afterBulkCreate(instances, options)  afterBulkDestroy(options)  afterBulkUpdate(options)
```

Example 2 (javascript):
```javascript
// Method 1 via the .init() methodclass User extends Model {}User.init(  {    username: DataTypes.STRING,    mood: {      type: DataTypes.ENUM,      values: ['happy', 'sad', 'neutral'],    },  },  {    hooks: {      beforeValidate: (user, options) => {        user.mood = 'happy';      },      afterValidate: (user, options) => {        user.username = 'Toni';      },    },    sequelize,  },);// Method 2 via the .addHook() methodUser.addHook('beforeValidate', (user, options) => {  user.mood = 'happy';});User.addHook('afterValidate', 'someCustomName', (user, options) => {  return Promise.reject(new Error("I'm afraid I can't let you do that!"));});// Method 3 via the direct methodUser.beforeCreate(async (user, options) => {  const hashedPassword = await hashPassword(user.password);  user.password = hashedPassword;});User.afterValidate('myHookAfter', (user, options) => {  user.username = 'Toni';});
```

Example 3 (gdscript):
```gdscript
class Book extends Model {}Book.init(  {    title: DataTypes.STRING,  },  { sequelize },);Book.addHook('afterCreate', 'notifyUsers', (book, options) => {  // ...});Book.removeHook('afterCreate', 'notifyUsers');
```

Example 4 (javascript):
```javascript
const User = sequelize.define(  'User',  {},  {    tableName: 'users',    hooks: {      beforeCreate: (record, options) => {        record.dataValues.createdAt = new Date()          .toISOString()          .replace(/T/, ' ')          .replace(/\..+/g, '');        record.dataValues.updatedAt = new Date()          .toISOString()          .replace(/T/, ' ')          .replace(/\..+/g, '');      },      beforeUpdate: (record, options) => {        record.dataValues.updatedAt = new Date()          .toISOString()          .replace(/T/, ' ')          .replace(/\..+/g, '');      },    },  },);
```

---

## Naming Strategies

**URL:** https://sequelize.org/docs/v6/other-topics/naming-strategies/

**Contents:**
- Naming Strategies
- The underscored option​
- Singular vs. Plural​
  - When defining models​
  - When defining a reference key in a model​
  - When retrieving data from eager loading​
  - Overriding singulars and plurals when defining aliases​

Sequelize provides the underscored option for a model. When true, this option will set the field option on all attributes to the snake_case version of its name. This also applies to foreign keys automatically generated by associations and other automatically generated fields. Example:

Above we have the models User and Task, both using the underscored option. We also have a One-to-Many relationship between them. Also, recall that since timestamps is true by default, we should expect the createdAt and updatedAt fields to be automatically created as well.

Without the underscored option, Sequelize would automatically define:

With the underscored option enabled, Sequelize will instead define:

Note that in both cases the fields are still camelCase in the JavaScript side; this option only changes how these fields are mapped to the database itself. The field option of every attribute is set to their snake_case version, but the attribute itself remains camelCase.

This way, calling sync() on the above code will generate the following:

At a first glance, it can be confusing whether the singular form or plural form of a name shall be used around in Sequelize. This section aims at clarifying that a bit.

Recall that Sequelize uses a library called inflection under the hood, so that irregular plurals (such as person -> people) are computed correctly. However, if you're working in another language, you may want to define the singular and plural forms of names directly; sequelize allows you to do this with some options.

Models should be defined with the singular form of a word. Example:

Above, the model name is foo (singular), and the respective table name is foos, since Sequelize automatically gets the plural for the table name.

In the above example we are manually defining a key that references another model. It's not usual to do this, but if you have to, you should use the table name there. This is because the reference is created upon the referenced table name. In the example above, the plural form was used (bars), assuming that the bar model was created with the default settings (making its underlying table automatically pluralized).

When you perform an include in a query, the included data will be added to an extra field in the returned objects, according to the following rules:

In short, the name of the field will take the most logical form in each situation.

When defining an alias for an association, instead of using simply { as: 'myAlias' }, you can pass an object to specify the singular and plural forms:

If you know that a model will always use the same alias in associations, you can provide the singular and plural forms directly to the model itself:

The mixins added to the user instances will use the correct forms. For example, instead of project.addUser(), Sequelize will provide project.getLíder(). Also, instead of project.setUsers(), Sequelize will provide project.setLíderes().

Note: recall that using as to change the name of the association will also change the name of the foreign key. Therefore it is recommended to also specify the foreign key(s) involved directly in this case.

The first call above will establish a foreign key called theSubscriptionId on Invoice. However, the second call will also establish a foreign key on Invoice (since as we know, hasMany calls places foreign keys in the target model) - however, it will be named subscriptionId. This way you will have both subscriptionId and theSubscriptionId columns.

The best approach is to choose a name for the foreign key and place it explicitly in both calls. For example, if subscription_id was chosen:

**Examples:**

Example 1 (css):
```css
const User = sequelize.define(  'user',  { username: Sequelize.STRING },  {    underscored: true,  },);const Task = sequelize.define(  'task',  { title: Sequelize.STRING },  {    underscored: true,  },);User.hasMany(Task);Task.belongsTo(User);
```

Example 2 (sql):
```sql
CREATE TABLE IF NOT EXISTS "users" (  "id" SERIAL,  "username" VARCHAR(255),  "created_at" TIMESTAMP WITH TIME ZONE NOT NULL,  "updated_at" TIMESTAMP WITH TIME ZONE NOT NULL,  PRIMARY KEY ("id"));CREATE TABLE IF NOT EXISTS "tasks" (  "id" SERIAL,  "title" VARCHAR(255),  "created_at" TIMESTAMP WITH TIME ZONE NOT NULL,  "updated_at" TIMESTAMP WITH TIME ZONE NOT NULL,  "user_id" INTEGER REFERENCES "users" ("id") ON DELETE SET NULL ON UPDATE CASCADE,  PRIMARY KEY ("id"));
```

Example 3 (css):
```css
sequelize.define('foo', { name: DataTypes.STRING });
```

Example 4 (css):
```css
sequelize.define('foo', {  name: DataTypes.STRING,  barId: {    type: DataTypes.INTEGER,    allowNull: false,    references: {      model: 'bars',      key: 'id',    },    onDelete: 'CASCADE',  },});
```

---

## Query Interface

**URL:** https://sequelize.org/docs/v6/other-topics/query-interface/

**Contents:**
- Query Interface
- Obtaining the query interface​
- Creating a table​
- Adding a column to a table​
- Changing the datatype of a column​
- Removing a column​
- Changing and removing columns in SQLite​
- Other​

An instance of Sequelize uses something called Query Interface to communicate to the database in a dialect-agnostic way. Most of the methods you've learned in this manual are implemented with the help of several methods from the query interface.

The methods from the query interface are therefore lower-level methods; you should use them only if you do not find another way to do it with higher-level APIs from Sequelize. They are, of course, still higher-level than running raw queries directly (i.e., writing SQL by hand).

This guide shows a few examples, but for the full list of what it can do, and for detailed usage of each method, check the QueryInterface API.

From now on, we will call queryInterface the singleton instance of the QueryInterface class, which is available on your Sequelize instance:

Generated SQL (using SQLite):

Note: Consider defining a Model instead and calling YourModel.sync() instead, which is a higher-level approach.

Generated SQL (using SQLite):

Generated SQL (using MySQL):

Generated SQL (using PostgreSQL):

SQLite does not support directly altering and removing columns. However, Sequelize will try to work around this by recreating the whole table with the help of a backup table, inspired by these instructions.

The following SQL calls are generated for SQLite:

As mentioned in the beginning of this guide, there is a lot more to the Query Interface available in Sequelize! Check the QueryInterface API for a full list of what can be done.

**Examples:**

Example 1 (javascript):
```javascript
const { Sequelize, DataTypes } = require('sequelize');const sequelize = new Sequelize(/* ... */);const queryInterface = sequelize.getQueryInterface();
```

Example 2 (css):
```css
queryInterface.createTable('Person', {  name: DataTypes.STRING,  isBetaMember: {    type: DataTypes.BOOLEAN,    defaultValue: false,    allowNull: false,  },});
```

Example 3 (sql):
```sql
CREATE TABLE IF NOT EXISTS `Person` (  `name` VARCHAR(255),  `isBetaMember` TINYINT(1) NOT NULL DEFAULT 0);
```

Example 4 (css):
```css
queryInterface.addColumn('Person', 'petName', { type: DataTypes.STRING });
```

---

## Transactions

**URL:** https://sequelize.org/docs/v6/other-topics/transactions/

**Contents:**
- Transactions
- Unmanaged transactions​
- Managed transactions​
  - Throw errors to rollback​
  - Automatically pass transactions to all queries​
- Concurrent/Partial transactions​
  - With CLS enabled​
- Passing options​
- Isolation levels​
- Usage with other sequelize methods​

Sequelize does not use transactions by default. However, for production-ready usage of Sequelize, you should definitely configure Sequelize to use transactions.

Sequelize supports two ways of using transactions:

Unmanaged transactions: Committing and rolling back the transaction should be done manually by the user (by calling the appropriate Sequelize methods).

Managed transactions: Sequelize will automatically rollback the transaction if any error is thrown, or commit the transaction otherwise. Also, if CLS (Continuation Local Storage) is enabled, all queries within the transaction callback will automatically receive the transaction object.

Let's start with an example:

As shown above, the unmanaged transaction approach requires that you commit and rollback the transaction manually, when necessary.

Managed transactions handle committing or rolling back the transaction automatically. You start a managed transaction by passing a callback to sequelize.transaction. This callback can be async (and usually is).

The following will happen in this case:

Note that t.commit() and t.rollback() were not called directly (which is correct).

When using the managed transaction you should never commit or rollback the transaction manually. If all queries are successful (in the sense of not throwing any error), but you still want to rollback the transaction, you should throw an error yourself:

In the examples above, the transaction is still manually passed, by passing { transaction: t } as the second argument. To automatically pass the transaction to all queries you must install the cls-hooked (CLS) module and instantiate a namespace in your own code:

To enable CLS you must tell sequelize which namespace to use by using a static method of the sequelize constructor:

Notice, that the useCLS() method is on the constructor, not on an instance of sequelize. This means that all instances will share the same namespace, and that CLS is all-or-nothing - you cannot enable it only for some instances.

CLS works like a thread-local storage for callbacks. What this means in practice is that different callback chains can access local variables by using the CLS namespace. When CLS is enabled sequelize will set the transaction property on the namespace when a new transaction is created. Since variables set within a callback chain are private to that chain several concurrent transactions can exist at the same time:

In most case you won't need to access namespace.get('transaction') directly, since all queries will automatically look for a transaction on the namespace:

You can have concurrent transactions within a sequence of queries or have some of them excluded from any transactions. Use the transaction option to control which transaction a query belongs to:

Note: SQLite does not support more than one transaction at the same time.

The sequelize.transaction method accepts options.

For unmanaged transactions, just use sequelize.transaction(options).

For managed transactions, use sequelize.transaction(options, callback).

The possible isolations levels to use when starting a transaction:

By default, sequelize uses the isolation level of the database. If you want to use a different isolation level, pass in the desired level as the first argument:

You can also overwrite the isolationLevel setting globally with an option in the Sequelize constructor:

Note for MSSQL: The SET ISOLATION LEVEL queries are not logged since the specified isolationLevel is passed directly to tedious.

The transaction option goes with most other options, which are usually the first argument of a method.

For methods that take values, like .create, .update(), etc. transaction should be passed to the option in the second argument.

If unsure, refer to the API documentation for the method you are using to be sure of the signature.

A transaction object allows tracking if and when it is committed.

An afterCommit hook can be added to both managed and unmanaged transaction objects:

The callback passed to afterCommit can be async. In this case:

You can use the afterCommit hook in conjunction with model hooks to know when a instance is saved and available outside of a transaction

Queries within a transaction can be performed with locks:

Queries within a transaction can skip locked rows:

**Examples:**

Example 1 (javascript):
```javascript
// First, we start a transaction from your connection and save it into a variableconst t = await sequelize.transaction();try {  // Then, we do some calls passing this transaction as an option:  const user = await User.create(    {      firstName: 'Bart',      lastName: 'Simpson',    },    { transaction: t },  );  await user.addSibling(    {      firstName: 'Lisa',      lastName: 'Simpson',    },    { transaction: t },  );  // If the execution reaches this line, no errors were thrown.  // We commit the transaction.  await t.commit();} catch (error) {  // If the execution reaches this line, an error was thrown.  // We rollback the transaction.  await t.rollback();}
```

Example 2 (javascript):
```javascript
try {  const result = await sequelize.transaction(async t => {    const user = await User.create(      {        firstName: 'Abraham',        lastName: 'Lincoln',      },      { transaction: t },    );    await user.setShooter(      {        firstName: 'John',        lastName: 'Boothe',      },      { transaction: t },    );    return user;  });  // If the execution reaches this line, the transaction has been committed successfully  // `result` is whatever was returned from the transaction callback (the `user`, in this case)} catch (error) {  // If the execution reaches this line, an error occurred.  // The transaction has already been rolled back automatically by Sequelize!}
```

Example 3 (javascript):
```javascript
await sequelize.transaction(async t => {  const user = await User.create(    {      firstName: 'Abraham',      lastName: 'Lincoln',    },    { transaction: t },  );  // Woops, the query was successful but we still want to roll back!  // We throw an error manually, so that Sequelize handles everything automatically.  throw new Error();});
```

Example 4 (javascript):
```javascript
const cls = require('cls-hooked');const namespace = cls.createNamespace('my-very-own-namespace');
```

---

## Optimistic Locking

**URL:** https://sequelize.org/docs/v6/other-topics/optimistic-locking/

**Contents:**
- Optimistic Locking

Sequelize has built-in support for optimistic locking through a model instance version count.

Optimistic locking is disabled by default and can be enabled by setting the version property to true in a specific model definition or global model configuration. See model configuration for more details.

Optimistic locking allows concurrent access to model records for edits and prevents conflicts from overwriting data. It does this by checking whether another process has made changes to a record since it was read and throws an OptimisticLockError when a conflict is detected.

---
