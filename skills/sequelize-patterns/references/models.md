# Sequelize - Models

**Pages:** 5

---

## Validations & Constraints

**URL:** https://sequelize.org/docs/v6/core-concepts/validations-and-constraints/

**Contents:**
- Validations & Constraints
- Difference between Validations and Constraints​
- Unique Constraint​
- Allowing/disallowing null values​
  - Note about allowNull implementation​
- Validators​
  - Per-attribute validations​
  - allowNull interaction with other validators​
  - Model-wide validations​

In this tutorial you will learn how to setup validations and constraints for your models in Sequelize.

For this tutorial, the following setup will be assumed:

Validations are checks performed in the Sequelize level, in pure JavaScript. They can be arbitrarily complex if you provide a custom validator function, or can be one of the built-in validators offered by Sequelize. If a validation fails, no SQL query will be sent to the database at all.

On the other hand, constraints are rules defined at SQL level. The most basic example of constraint is an Unique Constraint. If a constraint check fails, an error will be thrown by the database and Sequelize will forward this error to JavaScript (in this example, throwing a SequelizeUniqueConstraintError). Note that in this case, the SQL query was performed, unlike the case for validations.

Our code example above defines a unique constraint on the username field:

When this model is synchronized (by calling sequelize.sync for example), the username field will be created in the table as `username` TEXT UNIQUE, and an attempt to insert an username that already exists there will throw a SequelizeUniqueConstraintError.

By default, null is an allowed value for every column of a model. This can be disabled setting the allowNull: false option for a column, as it was done in the username field from our code example:

Without allowNull: false, the call User.create({}) would work.

The allowNull check is the only check in Sequelize that is a mix of a validation and a constraint in the senses described at the beginning of this tutorial. This is because:

Model validators allow you to specify format/content/inheritance validations for each attribute of the model. Validations are automatically run on create, update and save. You can also call validate() to manually validate an instance.

You can define your custom validators or use several built-in validators, implemented by validator.js (10.11.0), as shown below.

Note that where multiple arguments need to be passed to the built-in validation functions, the arguments to be passed must be in an array. But if a single array argument is to be passed, for instance an array of acceptable strings for isIn, this will be interpreted as multiple string arguments instead of one array argument. To work around this pass a single-length array of arguments, such as [['foo', 'bar']] as shown above.

To use a custom error message instead of that provided by validator.js, use an object instead of the plain value or array of arguments, for example a validator which needs no argument can be given a custom message with

or if arguments need to also be passed add an args property:

When using custom validator functions the error message will be whatever message the thrown Error object holds.

See the validator.js project for more details on the built in validation methods.

Hint: You can also define a custom function for the logging part. Just pass a function. The first parameter will be the string that is logged.

If a particular field of a model is set to not allow null (with allowNull: false) and that value has been set to null, all validators will be skipped and a ValidationError will be thrown.

On the other hand, if it is set to allow null (with allowNull: true) and that value has been set to null, only the built-in validators will be skipped, while the custom validators will still run.

This means you can, for instance, have a string field which validates its length to be between 5 and 10 characters, but which also allows null (since the length validator will be skipped automatically when the value is null):

You also can conditionally allow null values, with a custom validator, since it won't be skipped:

You can customize allowNull error message by setting the notNull validator:

Validations can also be defined to check the model after the field-specific validators. Using this you could, for example, ensure either neither of latitude and longitude are set or both, and fail if one but not the other is set.

Model validator methods are called with the model object's context and are deemed to fail if they throw an error, otherwise pass. This is just the same as with custom field-specific validators.

Any error messages collected are put in the validation result object alongside the field validation errors, with keys named after the failed validation method's key in the validate option object. Even though there can only be one error message for each model validation method at any one time, it is presented as a single string error in an array, to maximize consistency with the field errors.

In this simple case an object fails validation if either latitude or longitude is given, but not both. If we try to build one with an out-of-range latitude and no longitude, somePlace.validate() might return:

Such validation could have also been done with a custom validator defined on a single attribute (such as the latitude attribute, by checking (value === null) !== (this.longitude === null)), but the model-wide validation approach is cleaner.

**Examples:**

Example 1 (javascript):
```javascript
const { Sequelize, Op, Model, DataTypes } = require('sequelize');const sequelize = new Sequelize('sqlite::memory:');const User = sequelize.define('user', {  username: {    type: DataTypes.TEXT,    allowNull: false,    unique: true,  },  hashedPassword: {    type: DataTypes.STRING(64),    validate: {      is: /^[0-9a-f]{64}$/i,    },  },});(async () => {  await sequelize.sync({ force: true });  // Code here})();
```

Example 2 (css):
```css
/* ... */ {  username: {    type: DataTypes.TEXT,    allowNull: false,    unique: true  },} /* ... */
```

Example 3 (css):
```css
/* ... */ {  username: {    type: DataTypes.TEXT,    allowNull: false,    unique: true  },} /* ... */
```

Example 4 (sql):
```sql
sequelize.define('foo', {  bar: {    type: DataTypes.STRING,    validate: {      is: /^[a-z]+$/i,          // matches this RegExp      is: ["^[a-z]+$",'i'],     // same as above, but constructing the RegExp from a string      not: /^[a-z]+$/i,         // does not match this RegExp      not: ["^[a-z]+$",'i'],    // same as above, but constructing the RegExp from a string      isEmail: true,            // checks for email format (foo@bar.com)      isUrl: true,              // checks for url format (https://foo.com)      isIP: true,               // checks for IPv4 (129.89.23.1) or IPv6 format      isIPv4: true,             // checks for IPv4 (129.89.23.1)      isIPv6: true,             // checks for IPv6 format      isAlpha: true,            // will only allow letters      isAlphanumeric: true,     // will only allow alphanumeric characters, so "_abc" will fail      isNumeric: true,          // will only allow numbers      isInt: true,              // checks for valid integers      isFloat: true,            // checks for valid floating point numbers      isDecimal: true,          // checks for any numbers      isLowercase: true,        // checks for lowercase      isUppercase: true,        // checks for uppercase      notNull: true,            // won't allow null      isNull: true,             // only allows null      notEmpty: true,           // don't allow empty strings      equals: 'specific value', // only allow a specific value      contains: 'foo',          // force specific substrings      notIn: [['foo', 'bar']],  // check the value is not one of these      isIn: [['foo', 'bar']],   // check the value is one of these      notContains: 'bar',       // don't allow specific substrings      len: [2,10],              // only allow values with length between 2 and 10      isUUID: 4,                // only allow uuids      isDate: true,             // only allow date strings      isAfter: "2011-11-05",    // only allow date strings after a specific date      isBefore: "2011-11-05",   // only allow date strings before a specific date      max: 23,                  // only allow values <= 23      min: 23,                  // only allow values >= 23      isCreditCard: true,       // check for valid credit card numbers      // Examples of custom validators:      isEven(value) {        if (parseInt(value) % 2 !== 0) {          throw new Error('Only even values are allowed!');        }      }      isGreaterThanOtherField(value) {        if (parseInt(value) <= parseInt(this.otherField)) {          throw new Error('Bar must be greater than otherField.');        }      }    }  }});
```

---

## Model Instances

**URL:** https://sequelize.org/docs/v6/core-concepts/model-instances/

**Contents:**
- Model Instances
- Creating an instance​
  - A very useful shortcut: the create method​
- Note: logging instances​
- Default values​
- Updating an instance​
- Deleting an instance​
- Reloading an instance​
- Saving only some fields​
- Change-awareness of save​

As you already know, a model is an ES6 class. An instance of the class represents one object from that model (which maps to one row of the table in the database). This way, model instances are DAOs.

For this guide, the following setup will be assumed:

Although a model is a class, you should not create instances by using the new operator directly. Instead, the build method should be used:

However, the code above does not communicate with the database at all (note that it is not even asynchronous)! This is because the build method only creates an object that represents data that can be mapped to a database. In order to really save (i.e. persist) this instance in the database, the save method should be used:

Note, from the usage of await in the snippet above, that save is an asynchronous method. In fact, almost every Sequelize method is asynchronous; build is one of the very few exceptions.

Sequelize provides the create method, which combines the build and save methods shown above into a single method:

Trying to log a model instance directly to console.log will produce a lot of clutter, since Sequelize instances have a lot of things attached to them. Instead, you can use the .toJSON() method (which, by the way, automatically guarantees the instances to be JSON.stringify-ed well).

Built instances will automatically get default values:

If you change the value of some field of an instance, calling save again will update it accordingly:

You can update several fields at once with the set method:

Note that the save() here will also persist any other changes that have been made on this instance, not just those in the previous set call. If you want to update a specific set of fields, you can use update:

You can delete an instance by calling destroy:

You can reload an instance from the database by calling reload:

The reload call generates a SELECT query to get the up-to-date data from the database.

It is possible to define which attributes should be saved when calling save, by passing an array of column names.

This is useful when you set attributes based on a previously defined object, for example, when you get the values of an object via a form of a web app. Furthermore, this is used internally in the update implementation. This is how it looks like:

The save method is optimized internally to only update fields that really changed. This means that if you don't change anything and call save, Sequelize will know that the save is superfluous and do nothing, i.e., no query will be generated (it will still return a Promise, but it will resolve immediately).

Also, if only a few attributes have changed when you call save, only those fields will be sent in the UPDATE query, to improve performance.

In order to increment/decrement values of an instance without running into concurrency issues, Sequelize provides the increment and decrement instance methods.

You can also increment multiple fields at once:

Decrementing works in the exact same way.

**Examples:**

Example 1 (javascript):
```javascript
const { Sequelize, Model, DataTypes } = require('sequelize');const sequelize = new Sequelize('sqlite::memory:');const User = sequelize.define('user', {  name: DataTypes.TEXT,  favoriteColor: {    type: DataTypes.TEXT,    defaultValue: 'green',  },  age: DataTypes.INTEGER,  cash: DataTypes.INTEGER,});(async () => {  await sequelize.sync({ force: true });  // Code here})();
```

Example 2 (javascript):
```javascript
const jane = User.build({ name: 'Jane' });console.log(jane instanceof User); // trueconsole.log(jane.name); // "Jane"
```

Example 3 (javascript):
```javascript
await jane.save();console.log('Jane was saved to the database!');
```

Example 4 (javascript):
```javascript
const jane = await User.create({ name: 'Jane' });// Jane exists in the database now!console.log(jane instanceof User); // trueconsole.log(jane.name); // "Jane"
```

---

## Model Basics

**URL:** https://sequelize.org/docs/v6/core-concepts/model-basics/

**Contents:**
- Model Basics
- Concept​
- Model Definition​
  - Using sequelize.define:​
  - Extending Model​
    - Caveat with Public Class Fields​
- Table name inference​
  - Enforcing the table name to be equal to the model name​
  - Providing the table name directly​
- Model synchronization​

In this tutorial you will learn what models are in Sequelize and how to use them.

Models are the essence of Sequelize. A model is an abstraction that represents a table in your database. In Sequelize, it is a class that extends Model.

The model tells Sequelize several things about the entity it represents, such as the name of the table in the database and which columns it has (and their data types).

A model in Sequelize has a name. This name does not have to be the same name of the table it represents in the database. Usually, models have singular names (such as User) while tables have pluralized names (such as Users), although this is fully configurable.

Models can be defined in two equivalent ways in Sequelize:

After a model is defined, it is available within sequelize.models by its model name.

To learn with an example, we will consider that we want to create a model to represent users, which have a firstName and a lastName. We want our model to be called User, and the table it represents is called Users in the database.

Both ways to define this model are shown below. After being defined, we can access our model with sequelize.models.User.

Internally, sequelize.define calls Model.init, so both approaches are essentially equivalent.

Adding a Public Class Field with the same name as one of the model's attribute is going to cause issues. Sequelize adds a getter & a setter for each attribute defined through Model.init. Adding a Public Class Field will shadow those getter and setters, blocking access to the model's actual data.

In TypeScript, you can add typing information without adding an actual public class field by using the declare keyword:

Observe that, in both methods above, the table name (Users) was never explicitly defined. However, the model name was given (User).

By default, when the table name is not given, Sequelize automatically pluralizes the model name and uses that as the table name. This pluralization is done under the hood by a library called inflection, so that irregular plurals (such as person -> people) are computed correctly.

Of course, this behavior is easily configurable.

You can stop the auto-pluralization performed by Sequelize using the freezeTableName: true option. This way, Sequelize will infer the table name to be equal to the model name, without any modifications:

The example above will create a model named User pointing to a table also named User.

This behavior can also be defined globally for the sequelize instance, when it is created:

This way, all tables will use the same name as the model name.

You can simply tell Sequelize the name of the table directly as well:

When you define a model, you're telling Sequelize a few things about its table in the database. However, what if the table actually doesn't even exist in the database? What if it exists, but it has different columns, less columns, or any other difference?

This is where model synchronization comes in. A model can be synchronized with the database by calling model.sync(options), an asynchronous function (that returns a Promise). With this call, Sequelize will automatically perform an SQL query to the database. Note that this changes only the table in the database, not the model in the JavaScript side.

You can use sequelize.sync() to automatically synchronize all models. Example:

To drop the table related to a model:

As shown above, the sync and drop operations are destructive. Sequelize accepts a match option as an additional safety check, which receives a RegExp:

As shown above, sync({ force: true }) and sync({ alter: true }) can be destructive operations. Therefore, they are not recommended for production-level software. Instead, synchronization should be done with the advanced concept of Migrations, with the help of the Sequelize CLI.

By default, Sequelize automatically adds the fields createdAt and updatedAt to every model, using the data type DataTypes.DATE. Those fields are automatically managed as well - whenever you use Sequelize to create or update something, those fields will be set correctly. The createdAt field will contain the timestamp representing the moment of creation, and the updatedAt will contain the timestamp of the latest update.

Note: This is done in the Sequelize level (i.e. not done with SQL triggers). This means that direct SQL queries (for example queries performed without Sequelize by any other means) will not cause these fields to be updated automatically.

This behavior can be disabled for a model with the timestamps: false option:

It is also possible to enable only one of createdAt/updatedAt, and to provide a custom name for these columns:

If the only thing being specified about a column is its data type, the syntax can be shortened:

By default, Sequelize assumes that the default value of a column is NULL. This behavior can be changed by passing a specific defaultValue to the column definition:

Some special values, such as DataTypes.NOW, are also accepted:

Every column you define in your model must have a data type. Sequelize provides a lot of built-in data types. To access a built-in data type, you must import DataTypes:

In MySQL and MariaDB, the data types INTEGER, BIGINT, FLOAT and DOUBLE can be set as unsigned or zerofill (or both), as follows:

For UUIDs, use DataTypes.UUID. It becomes the UUID data type for PostgreSQL and SQLite, and CHAR(36) for MySQL. Sequelize can generate UUIDs automatically for these fields, simply use DataTypes.UUIDV1 or DataTypes.UUIDV4 as the default value:

There are other data types, covered in a separate guide.

When defining a column, apart from specifying the type of the column, and the allowNull and defaultValue options mentioned above, there are a lot more options that can be used. Some examples are below.

The Sequelize models are ES6 classes. You can very easily add custom instance or class level methods.

**Examples:**

Example 1 (javascript):
```javascript
const { Sequelize, DataTypes } = require('sequelize');const sequelize = new Sequelize('sqlite::memory:');const User = sequelize.define(  'User',  {    // Model attributes are defined here    firstName: {      type: DataTypes.STRING,      allowNull: false,    },    lastName: {      type: DataTypes.STRING,      // allowNull defaults to true    },  },  {    // Other model options go here  },);// `sequelize.define` also returns the modelconsole.log(User === sequelize.models.User); // true
```

Example 2 (javascript):
```javascript
const { Sequelize, DataTypes, Model } = require('sequelize');const sequelize = new Sequelize('sqlite::memory:');class User extends Model {}User.init(  {    // Model attributes are defined here    firstName: {      type: DataTypes.STRING,      allowNull: false,    },    lastName: {      type: DataTypes.STRING,      // allowNull defaults to true    },  },  {    // Other model options go here    sequelize, // We need to pass the connection instance    modelName: 'User', // We need to choose the model name  },);// the defined model is the class itselfconsole.log(User === sequelize.models.User); // true
```

Example 3 (typescript):
```typescript
// Invalidclass User extends Model {  id; // this field will shadow sequelize's getter & setter. It should be removed.  otherPublicField; // this field does not shadow anything. It is fine.}User.init(  {    id: {      type: DataTypes.INTEGER,      autoIncrement: true,      primaryKey: true,    },  },  { sequelize },);const user = new User({ id: 1 });user.id; // undefined
```

Example 4 (typescript):
```typescript
// Validclass User extends Model {  otherPublicField;}User.init(  {    id: {      type: DataTypes.INTEGER,      autoIncrement: true,      primaryKey: true,    },  },  { sequelize },);const user = new User({ id: 1 });user.id; // 1
```

---

## Paranoid

**URL:** https://sequelize.org/docs/v6/core-concepts/paranoid/

**Contents:**
- Paranoid
- Defining a model as paranoid​
- Deleting​
- Restoring​
- Behavior with other queries​

Sequelize supports the concept of paranoid tables. A paranoid table is one that, when told to delete a record, it will not truly delete it. Instead, a special column called deletedAt will have its value set to the timestamp of that deletion request.

This means that paranoid tables perform a soft-deletion of records, instead of a hard-deletion.

To make a model paranoid, you must pass the paranoid: true option to the model definition. Paranoid requires timestamps to work (i.e. it won't work if you also pass timestamps: false).

You can also change the default column name (which is deletedAt) to something else.

When you call the destroy method, a soft-deletion will happen:

If you really want a hard-deletion and your model is paranoid, you can force it using the force: true option:

The above examples used the static destroy method as an example (Post.destroy), but everything works in the same way with the instance method:

To restore soft-deleted records, you can use the restore method, which comes both in the static version as well as in the instance version:

Every query performed by Sequelize will automatically ignore soft-deleted records (except raw queries, of course).

This means that, for example, the findAll method will not see the soft-deleted records, fetching only the ones that were not deleted.

Even if you simply call findByPk providing the primary key of a soft-deleted record, the result will be null as if that record didn't exist.

If you really want to let the query see the soft-deleted records, you can pass the paranoid: false option to the query method. For example:

**Examples:**

Example 1 (gdscript):
```gdscript
class Post extends Model {}Post.init(  {    /* attributes here */  },  {    sequelize,    paranoid: true,    // If you want to give a custom name to the deletedAt column    deletedAt: 'destroyTime',  },);
```

Example 2 (sql):
```sql
await Post.destroy({  where: {    id: 1,  },});// UPDATE "posts" SET "deletedAt"=[timestamp] WHERE "deletedAt" IS NULL AND "id" = 1
```

Example 3 (sql):
```sql
await Post.destroy({  where: {    id: 1,  },  force: true,});// DELETE FROM "posts" WHERE "id" = 1
```

Example 4 (javascript):
```javascript
const post = await Post.create({ title: 'test' });console.log(post instanceof Post); // trueawait post.destroy(); // Would just set the `deletedAt` flagawait post.destroy({ force: true }); // Would really delete the record
```

---

## Getters, Setters & Virtuals

**URL:** https://sequelize.org/docs/v6/core-concepts/getters-setters-virtuals/

**Contents:**
- Getters, Setters & Virtuals
- Getters​
- Setters​
- Combining getters and setters​
- Virtual fields​
- Deprecated: getterMethods and setterMethods​

Sequelize allows you to define custom getters and setters for the attributes of your models.

Sequelize also allows you to specify the so-called virtual attributes, which are attributes on the Sequelize Model that doesn't really exist in the underlying SQL table, but instead are populated automatically by Sequelize. They are very useful to create custom attributes which also could simplify your code, for example.

A getter is a get() function defined for one column in the model definition:

This getter, just like a standard JavaScript getter, is called automatically when the field value is read:

Note that, although SUPERUSER123 was logged above, the value truly stored in the database is still SuperUser123. We used this.getDataValue('username') to obtain this value, and converted it to uppercase.

Had we tried to use this.username in the getter instead, we would have gotten an infinite loop! This is why Sequelize provides the getDataValue method.

A setter is a set() function defined for one column in the model definition. It receives the value being set:

Observe that Sequelize called the setter automatically, before even sending data to the database. The only data the database ever saw was the already hashed value.

If we wanted to involve another field from our model instance in the computation, that is possible and very easy!

Note: The above examples involving password handling, although much better than simply storing the password in plaintext, are far from perfect security. Handling passwords properly is hard, everything here is just for the sake of an example to show Sequelize functionality. We suggest involving a cybersecurity expert and/or reading OWASP documents and/or visiting the InfoSec StackExchange.

Getters and setters can be both defined in the same field.

For the sake of an example, let's say we are modeling a Post, whose content is a text of unlimited length. To improve memory usage, let's say we want to store a gzipped version of the content.

Note: modern databases should do some compression automatically in these cases. Please note that this is just for the sake of an example.

With the above setup, whenever we try to interact with the content field of our Post model, Sequelize will automatically handle the custom getter and setter. For example:

Virtual fields are fields that Sequelize populates under the hood, but in reality they don't even exist in the database.

For example, let's say we have the firstName and lastName attributes for a User.

Again, this is only for the sake of an example.

It would be nice to have a simple way to obtain the full name directly! We can combine the idea of getters with the special data type Sequelize provides for this kind of situation: DataTypes.VIRTUAL:

The VIRTUAL field does not cause a column in the table to exist. In other words, the model above will not have a fullName column. However, it will appear to have it!

This feature has been removed in Sequelize 7. You should consider using either VIRTUAL attributes or native class getter & setters instead.

Sequelize also provides the getterMethods and setterMethods options in the model definition to specify things that look like, but aren't exactly the same as, virtual attributes.

**Examples:**

Example 1 (css):
```css
const User = sequelize.define('user', {  // Let's say we wanted to see every username in uppercase, even  // though they are not necessarily uppercase in the database itself  username: {    type: DataTypes.STRING,    get() {      const rawValue = this.getDataValue('username');      return rawValue ? rawValue.toUpperCase() : null;    },  },});
```

Example 2 (javascript):
```javascript
const user = User.build({ username: 'SuperUser123' });console.log(user.username); // 'SUPERUSER123'console.log(user.getDataValue('username')); // 'SuperUser123'
```

Example 3 (css):
```css
const User = sequelize.define('user', {  username: DataTypes.STRING,  password: {    type: DataTypes.STRING,    set(value) {      // Storing passwords in plaintext in the database is terrible.      // Hashing the value with an appropriate cryptographic hash function is better.      this.setDataValue('password', hash(value));    },  },});
```

Example 4 (javascript):
```javascript
const user = User.build({  username: 'someone',  password: 'NotSo§tr0ngP4$SW0RD!',});console.log(user.password); // '7cfc84b8ea898bb72462e78b4643cfccd77e9f05678ec2ce78754147ba947acc'console.log(user.getDataValue('password')); // '7cfc84b8ea898bb72462e78b4643cfccd77e9f05678ec2ce78754147ba947acc'
```

---
