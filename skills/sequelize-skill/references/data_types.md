# Sequelize - Data Types

**Pages:** 2

---

## Other Data Types

**URL:** https://sequelize.org/docs/v6/other-topics/other-data-types/

**Contents:**
- Other Data Types
- Ranges (PostgreSQL only)​
  - Special Cases​
- Network Addresses​
- Arrays (PostgreSQL only)​
- BLOBs​
- ENUMs​
- JSON (SQLite, MySQL, MariaDB, Oracle and PostgreSQL only)​
  - Note for PostgreSQL​
  - JSONB (PostgreSQL only)​

Apart from the most common data types mentioned in the Model Basics guide, Sequelize provides several other data types.

Since range types have extra information for their bound inclusion/exclusion it's not very straightforward to just use a tuple to represent them in javascript.

When supplying ranges as values you can choose from the following APIs:

However, retrieved range values always come in the form of an array of objects. For example, if the stored value is ("2016-01-01 00:00:00+00:00", "2016-02-01 00:00:00+00:00"], after a finder query you will get:

You will need to call reload() after updating an instance with a range type or use the returning: true option.

The blob datatype allows you to insert data both as strings and as buffers. However, when a blob is retrieved from database with Sequelize, it will always be retrieved as a buffer.

The ENUM is a data type that accepts only a few values, specified as a list.

ENUMs can also be specified with the values field of the column definition, as follows:

The DataTypes.JSON data type is only supported for SQLite, MySQL, MariaDB, Oracle and PostgreSQL. However, there is a minimum support for MSSQL (see below).

The JSON data type in PostgreSQL stores the value as plain text, as opposed to binary representation. If you simply want to store and retrieve a JSON representation, using JSON will take less disk space and less time to build from its input representation. However, if you want to do any operations on the JSON value, you should prefer the JSONB data type described below.

PostgreSQL also supports a JSONB data type: DataTypes.JSONB. It can be queried in three different ways:

MSSQL does not have a JSON data type, however it does provide some support for JSON stored as strings through certain functions since SQL Server 2016. Using these functions, you will be able to query the JSON stored in the string, but any returned values will need to be parsed separately.

In Postgres, the GEOMETRY and GEOGRAPHY types are implemented by the PostGIS extension.

In Postgres, You must install the pg-hstore package if you use DataTypes.HSTORE

**Examples:**

Example 1 (unknown):
```unknown
DataTypes.RANGE(DataTypes.INTEGER); // int4rangeDataTypes.RANGE(DataTypes.BIGINT); // int8rangeDataTypes.RANGE(DataTypes.DATE); // tstzrangeDataTypes.RANGE(DataTypes.DATEONLY); // daterangeDataTypes.RANGE(DataTypes.DECIMAL); // numrange
```

Example 2 (javascript):
```javascript
// defaults to inclusive lower bound, exclusive upper boundconst range = [new Date(Date.UTC(2016, 0, 1)), new Date(Date.UTC(2016, 1, 1))];// '["2016-01-01 00:00:00+00:00", "2016-02-01 00:00:00+00:00")'// control inclusionconst range = [  { value: new Date(Date.UTC(2016, 0, 1)), inclusive: false },  { value: new Date(Date.UTC(2016, 1, 1)), inclusive: true },];// '("2016-01-01 00:00:00+00:00", "2016-02-01 00:00:00+00:00"]'// composite formconst range = [  { value: new Date(Date.UTC(2016, 0, 1)), inclusive: false },  new Date(Date.UTC(2016, 1, 1)),];// '("2016-01-01 00:00:00+00:00", "2016-02-01 00:00:00+00:00")'const Timeline = sequelize.define('Timeline', {  range: DataTypes.RANGE(DataTypes.DATE),});await Timeline.create({ range });
```

Example 3 (css):
```css
[  { value: Date, inclusive: false },  { value: Date, inclusive: true },];
```

Example 4 (css):
```css
// empty range:Timeline.create({ range: [] }); // range = 'empty'// Unbounded range:Timeline.create({ range: [null, null] }); // range = '[,)'// range = '[,"2016-01-01 00:00:00+00:00")'Timeline.create({ range: [null, new Date(Date.UTC(2016, 0, 1))] });// Infinite range:// range = '[-infinity,"2016-01-01 00:00:00+00:00")'Timeline.create({ range: [-Infinity, new Date(Date.UTC(2016, 0, 1))] });
```

---

## Extending Data Types

**URL:** https://sequelize.org/docs/v6/other-topics/extending-data-types/

**Contents:**
- Extending Data Types
- Example​
- PostgreSQL​
  - Ranges​

Most likely the type you are trying to implement is already included in DataTypes. If a new datatype is not included, this manual will show how to write it yourself.

Sequelize doesn't create new datatypes in the database. This tutorial explains how to make Sequelize recognize new datatypes and assumes that those new datatypes are already created in the database.

To extend Sequelize datatypes, do it before any Sequelize instance is created.

In this example, we will create a type called SOMETYPE that replicates the built-in datatype DataTypes.INTEGER(11).ZEROFILL.UNSIGNED.

After creating this new datatype, you need to map this datatype in each database dialect and make some adjustments.

Let's say the name of the new datatype is pg_new_type in the postgres database. That name has to be mapped to DataTypes.SOMETYPE. Additionally, it is required to create a child postgres-specific datatype.

After a new range type has been defined in postgres, it is trivial to add it to Sequelize.

In this example the name of the postgres range type is SOMETYPE_range and the name of the underlying postgres datatype is pg_new_type. The key of subtypes and castTypes is the key of the Sequelize datatype DataTypes.SOMETYPE.key, in lower case.

The new range can be used in model definitions as DataTypes.RANGE(DataTypes.SOMETYPE) or DataTypes.RANGE(DataTypes.SOMETYPE).

**Examples:**

Example 1 (javascript):
```javascript
const { Sequelize, DataTypes, Utils } = require('Sequelize');createTheNewDataType();const sequelize = new Sequelize('sqlite::memory:');function createTheNewDataType() {  class SOMETYPE extends DataTypes.ABSTRACT {    // Mandatory: complete definition of the new type in the database    toSql() {      return 'INTEGER(11) UNSIGNED ZEROFILL';    }    // Optional: validator function    validate(value, options) {      return typeof value === 'number' && !Number.isNaN(value);    }    // Optional: sanitizer    _sanitize(value) {      // Force all numbers to be positive      return value < 0 ? 0 : Math.round(value);    }    // Optional: value stringifier before sending to database    _stringify(value) {      return value.toString();    }    // Optional: parser for values received from the database    static parse(value) {      return Number.parseInt(value);    }  }  // Mandatory: set the type key  SOMETYPE.prototype.key = SOMETYPE.key = 'SOMETYPE';  // Mandatory: add the new type to DataTypes. Optionally wrap it on `Utils.classToInvokable` to  // be able to use this datatype directly without having to call `new` on it.  DataTypes.SOMETYPE = Utils.classToInvokable(SOMETYPE);  // Optional: disable escaping after stringifier. Do this at your own risk, since this opens opportunity for SQL injections.  // DataTypes.SOMETYPE.escape = false;}
```

Example 2 (javascript):
```javascript
function createTheNewDataType() {  // [...]  const PgTypes = DataTypes.postgres;  // Mandatory: map postgres datatype name  DataTypes.SOMETYPE.types.postgres = ['pg_new_type'];  // Mandatory: create a postgres-specific child datatype with its own parse  // method. The parser will be dynamically mapped to the OID of pg_new_type.  PgTypes.SOMETYPE = function SOMETYPE() {    if (!(this instanceof PgTypes.SOMETYPE)) {      return new PgTypes.SOMETYPE();    }    DataTypes.SOMETYPE.apply(this, arguments);  }  const util = require('util'); // Built-in Node package  util.inherits(PgTypes.SOMETYPE, DataTypes.SOMETYPE);  // Mandatory: create, override or reassign a postgres-specific parser  // PgTypes.SOMETYPE.parse = value => value;  PgTypes.SOMETYPE.parse = DataTypes.SOMETYPE.parse || x => x;  // Optional: add or override methods of the postgres-specific datatype  // like toSql, escape, validate, _stringify, _sanitize...}
```

Example 3 (javascript):
```javascript
function createTheNewDataType() {  // [...]  // Add postgresql range, SOMETYPE comes from DataType.SOMETYPE.key in lower case  DataTypes.RANGE.types.postgres.subtypes.SOMETYPE = 'SOMETYPE_range';  DataTypes.RANGE.types.postgres.castTypes.SOMETYPE = 'pg_new_type';}
```

---
