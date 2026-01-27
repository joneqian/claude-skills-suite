# Sequelize - Getting Started

**Pages:** 1

---

## Getting Started

**URL:** https://sequelize.org/docs/v6/getting-started/

**Contents:**
- Getting Started
- Installing​
- Connecting to a database​
  - Testing the connection​
  - Closing the connection​
- Terminology convention​
- Tip for reading the docs​
- New databases versus existing databases​
- Logging​
- Promises and async/await​

In this tutorial, you will learn to make a simple setup of Sequelize.

Sequelize is available via npm (or yarn).

You'll also have to manually install the driver for your database of choice:

To connect to the database, you must create a Sequelize instance. This can be done by either passing the connection parameters separately to the Sequelize constructor or by passing a single connection URI:

The Sequelize constructor accepts a lot of options. They are documented in the API Reference.

You can use the .authenticate() function to test if the connection is OK:

Sequelize will keep the connection open by default, and use the same connection for all queries. If you need to close the connection, call sequelize.close() (which is asynchronous and returns a Promise).

Once sequelize.close() has been called, it's impossible to open a new connection. You will need to create a new Sequelize instance to access your database again.

Observe that, in the examples above, Sequelize refers to the library itself while sequelize refers to an instance of Sequelize, which represents a connection to one database. This is the recommended convention and it will be followed throughout the documentation.

You are encouraged to run code examples locally while reading the Sequelize docs. This will help you learn faster. The easiest way to do this is using the SQLite dialect:

To experiment with the other dialects, which are harder to set up locally, you can use the Sequelize SSCCE GitHub repository, which allows you to run code on all supported dialects directly from GitHub, for free, without any setup!

If you are starting a project from scratch, and your database is still empty, Sequelize can be used from the beginning in order to automate the creation of every table in your database.

Also, if you want to use Sequelize to connect to a database that is already filled with tables and data, that works as well! Sequelize has got you covered in both cases.

By default, Sequelize will log into the console for every SQL query it performs. The options.logging option can be used to customize this behavior, by defining the function that gets executed every time Sequelize logs something. The default value is console.log and when using that only the first log parameter of a log function call is displayed. For example, for query logging the first parameter is the raw query and the second (hidden by default) is the Sequelize object.

Common useful values for options.logging:

Most of the methods provided by Sequelize are asynchronous and therefore return Promises. They are all Promises, so you can use the Promise API (for example, using then, catch, finally) out of the box.

Of course, using async and await works fine as well.

**Examples:**

Example 1 (unknown):
```unknown
npm install --save sequelize
```

Example 2 (markdown):
```markdown
# One of the following:$ npm install --save pg pg-hstore # Postgres$ npm install --save mysql2$ npm install --save mariadb$ npm install --save sqlite3$ npm install --save tedious # Microsoft SQL Server$ npm install --save oracledb # Oracle Database
```

Example 3 (javascript):
```javascript
const { Sequelize } = require('sequelize');// Option 1: Passing a connection URIconst sequelize = new Sequelize('sqlite::memory:') // Example for sqliteconst sequelize = new Sequelize('postgres://user:pass@example.com:5432/dbname') // Example for postgres// Option 2: Passing parameters separately (sqlite)const sequelize = new Sequelize({  dialect: 'sqlite',  storage: 'path/to/database.sqlite'});// Option 3: Passing parameters separately (other dialects)const sequelize = new Sequelize('database', 'username', 'password', {  host: 'localhost',  dialect: /* one of 'mysql' | 'postgres' | 'sqlite' | 'mariadb' | 'mssql' | 'db2' | 'snowflake' | 'oracle' */});
```

Example 4 (javascript):
```javascript
try {  await sequelize.authenticate();  console.log('Connection has been established successfully.');} catch (error) {  console.error('Unable to connect to the database:', error);}
```

---
