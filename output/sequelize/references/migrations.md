# Sequelize - Migrations

**Pages:** 2

---

## Working with Legacy Tables

**URL:** https://sequelize.org/docs/v6/other-topics/legacy/

**Contents:**
- Working with Legacy Tables
- Tables​
- Fields​
- Primary keys​
- Foreign keys​

While out of the box Sequelize will seem a bit opinionated it's easy to work legacy tables and forward proof your application by defining (otherwise generated) table and field names.

Sequelize will assume your table has a id primary key property by default.

To define your own primary key:

And if your model has no primary key at all you can use Model.removeAttribute('id');

Instances without primary keys can still be retrieved using Model.findOne and Model.findAll. While it's currently possible to use their instance methods (instance.save, instance.update, etc…), doing this will lead to subtle bugs, and is planned for removal in a future major update.

If your model has no primary keys, you need to use the static equivalent of the following instance methods, and provide your own where parameter:

**Examples:**

Example 1 (gdscript):
```gdscript
class User extends Model {}User.init(  {    // ...  },  {    modelName: 'user',    tableName: 'users',    sequelize,  },);
```

Example 2 (gdscript):
```gdscript
class MyModel extends Model {}MyModel.init(  {    userId: {      type: DataTypes.INTEGER,      field: 'user_id',    },  },  { sequelize },);
```

Example 3 (gdscript):
```gdscript
class Collection extends Model {}Collection.init(  {    uid: {      type: DataTypes.INTEGER,      primaryKey: true,      autoIncrement: true, // Automatically gets converted to SERIAL for postgres    },  },  { sequelize },);class Collection extends Model {}Collection.init(  {    uuid: {      type: DataTypes.UUID,      primaryKey: true,    },  },  { sequelize },);
```

Example 4 (css):
```css
// 1:1Organization.belongsTo(User, { foreignKey: 'owner_id' });User.hasOne(Organization, { foreignKey: 'owner_id' });// 1:MProject.hasMany(Task, { foreignKey: 'tasks_pk' });Task.belongsTo(Project, { foreignKey: 'tasks_pk' });// N:MUser.belongsToMany(Role, {  through: 'user_has_roles',  foreignKey: 'user_role_user_id',});Role.belongsToMany(User, {  through: 'user_has_roles',  foreignKey: 'roles_identifier',});
```

---

## Migrations

**URL:** https://sequelize.org/docs/v6/other-topics/migrations/

**Contents:**
- Migrations
- Installing the CLI​
- Project bootstrapping​
  - Configuration​
- Creating the first Model (and Migration)​
- Running Migrations​
- Undoing Migrations​
- Creating the first Seed​
- Running Seeds​
- Undoing Seeds​

Just like you use version control systems such as Git to manage changes in your source code, you can use migrations to keep track of changes to the database. With migrations you can transfer your existing database into another state and vice versa: Those state transitions are saved in migration files, which describe how to get to the new state and how to revert the changes in order to get back to the old state.

You will need the Sequelize Command-Line Interface (CLI). The CLI ships support for migrations and project bootstrapping.

A Migration in Sequelize is a javascript file which exports two functions, up and down, that dictates how to perform the migration and undo it. You define those functions manually, but you don't call them manually; they will be called automatically by the CLI. In these functions, you should simply perform whatever queries you need, with the help of sequelize.query and whichever other methods Sequelize provides to you. There is no extra magic beyond that.

To install the Sequelize CLI:

For details see the CLI GitHub repository.

To create an empty project you will need to execute init command

This will create following folders

Before continuing further we will need to tell the CLI how to connect to the database. To do that let's open default config file config/config.json. It looks something like this:

Note that the Sequelize CLI assumes mysql by default. If you're using another dialect, you need to change the content of the "dialect" option.

Now edit this file and set correct database credentials and dialect. The keys of the objects (e.g. "development") are used on model/index.js for matching process.env.NODE_ENV (When undefined, "development" is a default value).

Sequelize will use the default connection port for each dialect (for example, for postgres, it is port 5432). If you need to specify a different port, use the "port" field (it is not present by default in config/config.js but you can simply add it).

Note: If your database doesn't exist yet, you can just call db:create command. With proper access it will create that database for you.

Once you have properly configured CLI config file you are ready to create your first migration. It's as simple as executing a simple command.

We will use model:generate command. This command requires two options:

Let's create a model named User.

Note: Sequelize will only use Model files, it's the table representation. On the other hand, the migration file is a change in that model or more specifically that table, used by CLI. Treat migrations like a commit or a log for some change in database.

Until this step, we haven't inserted anything into the database. We have just created the required model and migration files for our first model, User. Now to actually create that table in the database you need to run db:migrate command.

This command will execute these steps:

Now our table has been created and saved in the database. With migration you can revert to old state by just running a command.

You can use db:migrate:undo, this command will revert the most recent migration.

You can revert back to the initial state by undoing all migrations with the db:migrate:undo:all command. You can also revert back to a specific migration by passing its name with the --to option.

Suppose we want to insert some data into a few tables by default. If we follow up on the previous example we can consider creating a demo user for the User table.

To manage all data migrations you can use seeders. Seed files are some change in data that can be used to populate database tables with sample or test data.

Let's create a seed file which will add a demo user to our User table.

This command will create a seed file in seeders folder. File name will look something like XXXXXXXXXXXXXX-demo-user.js. It follows the same up / down semantics as the migration files.

Now we should edit this file to insert demo user to User table.

In last step you created a seed file; however, it has not been committed to the database. To do that we run a simple command.

This will execute that seed file and a demo user will be inserted into the User table.

Note: Seeder execution history is not stored anywhere, unlike migrations, which use the SequelizeMeta table. If you wish to change this behavior, please read the Storage section.

Seeders can be undone if they are using any storage. There are two commands available for that:

If you wish to undo the most recent seed:

If you wish to undo a specific seed:

If you wish to undo all seeds:

The following skeleton shows a typical migration file.

We can generate this file using migration:generate. This will create xxx-migration-skeleton.js in your migration folder.

The passed queryInterface object can be used to modify the database. The Sequelize object stores the available data types such as STRING or INTEGER. Function up or down should return a Promise. Let's look at an example:

The following is an example of a migration that performs two changes in the database, using an automatically-managed transaction to ensure that all instructions are successfully executed or rolled back in case of failure:

The next example is of a migration that has a foreign key. You can use references to specify a foreign key:

The next example is of a migration that uses async/await where you create an unique index on a new column, with a manually-managed transaction:

The next example is of a migration that creates an unique index composed of multiple fields with a condition, which allows a relation to exist multiple times but only one can satisfy the condition:

This is a special configuration file. It lets you specify the following options that you would usually pass as arguments to CLI:

Some scenarios where you can use it:

And a whole lot more. Let's see how you can use this file for custom configuration.

To begin, let's create the .sequelizerc file in the root directory of your project, with the following content:

With this config you are telling the CLI to:

The configuration file is by default a JSON file called config.json. But sometimes you need a dynamic configuration, for example to access environment variables or execute some other code to determine the configuration.

Thankfully, the Sequelize CLI can read from both .json and .js files. This can be setup with .sequelizerc file. You just have to provide the path to your .js file as the config option of your exported object:

Now the Sequelize CLI will load config/config.js for getting configuration options.

An example of config/config.js file:

The example above also shows how to add custom dialect options to the configuration.

To enable more modern constructions in your migrations and seeders, you can simply install babel-register and require it at the beginning of .sequelizerc:

Of course, the outcome will depend upon your babel configuration (such as in a .babelrc file). Learn more at babeljs.io.

Use environment variables for config settings. This is because secrets such as passwords should never be part of the source code (and especially not committed to version control).

There are three types of storage that you can use: sequelize, json, and none.

By default the CLI will create a table in your database called SequelizeMeta containing an entry for each executed migration. To change this behavior, there are three options you can add to the configuration file. Using migrationStorage, you can choose the type of storage to be used for migrations. If you choose json, you can specify the path of the file using migrationStoragePath or the CLI will write to the file sequelize-meta.json. If you want to keep the information in the database, using sequelize, but want to use a different table, you can change the table name using migrationStorageTableName. Also you can define a different schema for the SequelizeMeta table by providing the migrationStorageTableSchema property.

Note: The none storage is not recommended as a migration storage. If you decide to use it, be aware of the implications of having no record of what migrations did or didn't run.

By default the CLI will not save any seed that is executed. If you choose to change this behavior (!), you can use seederStorage in the configuration file to change the storage type. If you choose json, you can specify the path of the file using seederStoragePath or the CLI will write to the file sequelize-data.json. If you want to keep the information in the database, using sequelize, you can specify the table name using seederStorageTableName, or it will default to SequelizeData.

As an alternative to the --config option with configuration files defining your database, you can use the --url option to pass in a connection string. For example:

If utilizing package.json scripts with npm, make sure to use the extra -- in your command when using flags. For example:

Use the command like so: npm run migrate:up -- --url <url>

Sequelize has a sister library called umzug for programmatically handling execution and logging of migration tasks.

**Examples:**

Example 1 (unknown):
```unknown
npm install --save-dev sequelize-cli
```

Example 2 (unknown):
```unknown
npx sequelize-cli init
```

Example 3 (json):
```json
{  "development": {    "username": "root",    "password": null,    "database": "database_development",    "host": "127.0.0.1",    "dialect": "mysql"  },  "test": {    "username": "root",    "password": null,    "database": "database_test",    "host": "127.0.0.1",    "dialect": "mysql"  },  "production": {    "username": "root",    "password": null,    "database": "database_production",    "host": "127.0.0.1",    "dialect": "mysql"  }}
```

Example 4 (unknown):
```unknown
npx sequelize-cli model:generate --name User --attributes firstName:string,lastName:string,email:string
```

---
