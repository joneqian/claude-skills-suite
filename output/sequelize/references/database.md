# Sequelize - Database

**Pages:** 5

---

## Connection Pool

**URL:** https://sequelize.org/docs/v6/other-topics/connection-pool/

**Contents:**
- Connection Pool

If you're connecting to the database from a single process, you should create only one Sequelize instance. Sequelize will set up a connection pool on initialization. This connection pool can be configured through the constructor's options parameter (using options.pool), as is shown in the following example:

Learn more in the API Reference for the Sequelize constructor. If you're connecting to the database from multiple processes, you'll have to create one instance per process, but each instance should have a maximum connection pool size of such that the total maximum size is respected. For example, if you want a max connection pool size of 90 and you have three processes, the Sequelize instance of each process should have a max connection pool size of 30.

**Examples:**

Example 1 (css):
```css
const sequelize = new Sequelize(/* ... */, {  // ...  pool: {    max: 5,    min: 0,    acquire: 30000,    idle: 10000  }});
```

---

## Dialect-Specific Things

**URL:** https://sequelize.org/docs/v6/other-topics/dialect-specific-things/

**Contents:**
- Dialect-Specific Things
- Underlying Connector Libraries​
  - MySQL​
  - MariaDB​
  - SQLite​
  - PostgreSQL​
  - Redshift​
  - Microsoft SQL Server (MSSQL)​
    - MSSQL Domain Account​
  - Snowflake (Experimental)​

The underlying connector library used by Sequelize for MySQL is the mysql2 npm package (version 1.5.2 or higher).

You can provide custom options to it using the dialectOptions in the Sequelize constructor:

dialectOptions are passed directly to the MySQL connection constructor. A full list of options can be found in the MySQL docs.

The underlying connector library used by Sequelize for MariaDB is the mariadb npm package.

You can provide custom options to it using the dialectOptions in the Sequelize constructor:

dialectOptions are passed directly to the MariaDB connection constructor. A full list of options can be found in the MariaDB docs.

The underlying connector library used by Sequelize for SQLite is the sqlite3 npm package (version 4.0.0 or above). Due to security vulnerabilities with sqlite3@^4 it is recommended to use the @vscode/sqlite3 fork if updating to sqlite3@^5.0.3 is not possible.

You specify the storage file in the Sequelize constructor with the storage option (use :memory: for an in-memory SQLite instance).

You can provide custom options to it using the dialectOptions in the Sequelize constructor:

The following fields may be passed to SQLite dialectOptions:

The underlying connector library used by Sequelize for PostgreSQL is the pg package (for Node 10 & 12, use pg version 7.0.0 or above. For Node 14 and above you need to use pg version 8.2.x or above, as per the pg documentation). The module pg-hstore is also necessary.

You can provide custom options to it using the dialectOptions in the Sequelize constructor:

The following fields may be passed to Postgres dialectOptions:

To connect over a unix domain socket, specify the path to the socket directory in the host option. The socket path must start with /.

The default client_min_messages config in sequelize is WARNING.

Most configuration is same as PostgreSQL above.

Redshift doesn't support client_min_messages, 'ignore' is needed to skip the configuration:

The underlying connector library used by Sequelize for MSSQL is the tedious npm package (version 6.0.0 or above).

You can provide custom options to it using dialectOptions.options in the Sequelize constructor:

A full list of options can be found in the tedious docs.

In order to connect with a domain account, use the following format.

The underlying connector library used by Sequelize for Snowflake is the snowflake-sdk npm package.

In order to connect with an account, use the following format:

NOTE There is no test sandbox provided so the snowflake integration test is not part of the pipeline. Also it is difficult for core team to triage and debug. This dialect needs to be maintained by the snowflake user/community for now.

For running integration test:

The underlying connector library used by Sequelize for Oracle is the node-oracledb package. See Releases to see which versions of Oracle Database & node-oracledb are supported.

node-oracledb needs Oracle Instant Client to work. You can use the node-oracledb quick start link for installations.

Below is a Sequelize constructor with parameters related to Oracle Database.

The default port number for Oracle database is 1521.

Sequelize also lets you pass credentials in URL format:

You can pass an Easy Connect String, a Net Service Name, or a Connect Descriptor to the Sequelize constructor using dialectOptions.connectString:

Note that the database, host and port will be overriden and the values in connectString will be used for authentication.

Please refer to Connect String for more about connect strings.

If you are working with the PostgreSQL TIMESTAMP WITHOUT TIME ZONE and you need to parse it to a different timezone, please use the pg library's own parser:

Array(Enum) type requireS special treatment. Whenever Sequelize will talk to the database, it has to typecast array values with ENUM name.

So this enum name must follow this pattern enum_<table_name>_<col_name>. If you are using sync then correct name will automatically be generated.

The tableHint option can be used to define a table hint. The hint must be a value from TableHints and should only be used when absolutely necessary. Only a single table hint is currently supported per query.

Table hints override the default behavior of MSSQL query optimizer by specifying certain options. They only affect the table or view referenced in that clause.

The indexHints option can be used to define index hints. The hint type must be a value from IndexHints and the values should reference existing indexes.

Index hints override the default behavior of the MySQL query optimizer.

The above will generate a MySQL query that looks like this:

Sequelize.IndexHints includes USE, FORCE, and IGNORE.

See Issue #9421 for the original API proposal.

The default engine for a model is InnoDB.

You can change the engine for a model with the engine option (e.g., to MyISAM):

Like every option for the definition of a model, this setting can also be changed globally with the define option of the Sequelize constructor:

You can specify a comment for a table when defining the model:

The comment will be set when calling sync().

**Examples:**

Example 1 (css):
```css
const sequelize = new Sequelize('database', 'username', 'password', {  dialect: 'mysql',  dialectOptions: {    // Your mysql2 options here  },});
```

Example 2 (css):
```css
const sequelize = new Sequelize('database', 'username', 'password', {  dialect: 'mariadb',  dialectOptions: {    // Your mariadb options here    // connectTimeout: 1000  },});
```

Example 3 (sql):
```sql
import { Sequelize } from 'sequelize';import SQLite from 'sqlite3';const sequelize = new Sequelize('database', 'username', 'password', {  dialect: 'sqlite',  storage: 'path/to/database.sqlite', // or ':memory:'  dialectOptions: {    // Your sqlite3 options here    // for instance, this is how you can configure the database opening mode:    mode: SQLite.OPEN_READWRITE | SQLite.OPEN_CREATE | SQLite.OPEN_FULLMUTEX,  },});
```

Example 4 (css):
```css
const sequelize = new Sequelize('database', 'username', 'password', {  dialect: 'postgres',  dialectOptions: {    // Your pg options here  },});
```

---

## Indexes

**URL:** https://sequelize.org/docs/v6/other-topics/indexes/

**Contents:**
- Indexes

Sequelize supports adding indexes to the model definition which will be created on sequelize.sync().

**Examples:**

Example 1 (css):
```css
const User = sequelize.define(  'User',  {    /* attributes */  },  {    indexes: [      // Create a unique index on email      {        unique: true,        fields: ['email'],      },      // Creates a gin index on data with the jsonb_path_ops operator      {        fields: ['data'],        using: 'gin',        operator: 'jsonb_path_ops',      },      // By default index name will be [table]_[fields]      // Creates a multi column partial index      {        name: 'public_by_author',        fields: ['author', 'status'],        where: {          status: 'public',        },      },      // A BTREE index with an ordered field      {        name: 'title_index',        using: 'BTREE',        fields: [          'author',          {            name: 'title',            collate: 'en_US',            order: 'DESC',            length: 5,          },        ],      },    ],  },);
```

---

## Constraints & Circularities

**URL:** https://sequelize.org/docs/v6/other-topics/constraints-and-circularities/

**Contents:**
- Constraints & Circularities
- Enforcing a foreign key reference without constraints​

Adding constraints between tables means that tables must be created in the database in a certain order, when using sequelize.sync. If Task has a reference to User, the User table must be created before the Task table can be created. This can sometimes lead to circular references, where Sequelize cannot find an order in which to sync. Imagine a scenario of documents and versions. A document can have multiple versions, and for convenience, a document has a reference to its current version.

However, unfortunately the code above will result in the following error:

In order to alleviate that, we can pass constraints: false to one of the associations:

Which will allow us to sync the tables correctly:

Sometimes you may want to reference another table, without adding any constraints, or associations. In that case you can manually add the reference attributes to your schema definition, and mark the relations between them.

**Examples:**

Example 1 (gdscript):
```gdscript
const { Sequelize, Model, DataTypes } = require('sequelize');class Document extends Model {}Document.init(  {    author: DataTypes.STRING,  },  { sequelize, modelName: 'document' },);class Version extends Model {}Version.init(  {    timestamp: DataTypes.DATE,  },  { sequelize, modelName: 'version' },);Document.hasMany(Version); // This adds documentId attribute to versionDocument.belongsTo(Version, {  as: 'Current',  foreignKey: 'currentVersionId',}); // This adds currentVersionId attribute to document
```

Example 2 (javascript):
```javascript
Cyclic dependency found. documents is dependent of itself. Dependency chain: documents -> versions => documents
```

Example 3 (css):
```css
Document.hasMany(Version);Document.belongsTo(Version, {  as: 'Current',  foreignKey: 'currentVersionId',  constraints: false,});
```

Example 4 (sql):
```sql
CREATE TABLE IF NOT EXISTS "documents" (  "id" SERIAL,  "author" VARCHAR(255),  "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL,  "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL,  "currentVersionId" INTEGER,  PRIMARY KEY ("id"));CREATE TABLE IF NOT EXISTS "versions" (  "id" SERIAL,  "timestamp" TIMESTAMP WITH TIME ZONE,  "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL,  "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL,  "documentId" INTEGER REFERENCES "documents" ("id") ON DELETE  SET    NULL ON UPDATE CASCADE,    PRIMARY KEY ("id"));
```

---

## Read Replication

**URL:** https://sequelize.org/docs/v6/other-topics/read-replication/

**Contents:**
- Read Replication

Sequelize supports read replication, i.e. having multiple servers that you can connect to when you want to do a SELECT query. When you do read replication, you specify one or more servers to act as read replicas, and one server to act as the main writer, which handles all writes and updates and propagates them to the replicas (note that the actual replication process is not handled by Sequelize, but should be set up by database backend).

If you have any general settings that apply to all replicas you do not need to provide them for each instance. In the code above, database name and port is propagated to all replicas. The same will happen for user and password, if you leave them out for any of the replicas. Each replica has the following options:host,port,username,password,database.

Sequelize uses a pool to manage connections to your replicas. Internally Sequelize will maintain two pools created using pool configuration.

If you want to modify these, you can pass pool as an options when instantiating Sequelize, as shown above.

Each write or useMaster: true query will use write pool. For SELECT read pool will be used. Read replica are switched using a basic round robin scheduling.

**Examples:**

Example 1 (css):
```css
const sequelize = new Sequelize('database', null, null, {  dialect: 'mysql',  port: 3306,  replication: {    read: [      {        host: '8.8.8.8',        username: 'read-1-username',        password: process.env.READ_DB_1_PW,      },      {        host: '9.9.9.9',        username: 'read-2-username',        password: process.env.READ_DB_2_PW,      },    ],    write: {      host: '1.1.1.1',      username: 'write-username',      password: process.env.WRITE_DB_PW,    },  },  pool: {    // If you want to override the options used for the read/write pool you can do so here    max: 20,    idle: 30000,  },});
```

---
