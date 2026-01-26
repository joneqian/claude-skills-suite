# Sqlalchemy - Other

**Pages:** 11

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/core/defaults.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Core
    - Project Versions
- Column INSERT/UPDATE Defaults¶
- Scalar Defaults¶
- Python-Executed Functions¶
  - Context-Sensitive Default Functions¶
- Client-Invoked SQL Expressions¶
- Server-invoked DDL-Explicit Default Expressions¶

Home | Download this Documentation

Home | Download this Documentation

Column INSERT and UPDATE defaults refer to functions that create a default value for a particular column in a row as an INSERT or UPDATE statement is proceeding against that row, in the case where no value was provided to the INSERT or UPDATE statement for that column. That is, if a table has a column called “timestamp”, and an INSERT statement proceeds which does not include a value for this column, an INSERT default would create a new value, such as the current time, that is used as the value to be INSERTed into the “timestamp” column. If the statement does include a value for this column, then the default does not take place.

Column defaults can be server-side functions or constant values which are defined in the database along with the schema in DDL, or as SQL expressions which are rendered directly within an INSERT or UPDATE statement emitted by SQLAlchemy; they may also be client-side Python functions or constant values which are invoked by SQLAlchemy before data is passed to the database.

A column default handler should not be confused with a construct that intercepts and modifies incoming values for INSERT and UPDATE statements which are provided to the statement as it is invoked. This is known as data marshalling, where a column value is modified in some way by the application before being sent to the database. SQLAlchemy provides a few means of achieving this which include using custom datatypes, SQL execution events and in the ORM custom validators as well as attribute events. Column defaults are only invoked when there is no value present for a column in a SQL DML statement.

SQLAlchemy provides an array of features regarding default generation functions which take place for non-present values during INSERT and UPDATE statements. Options include:

Scalar values used as defaults during INSERT and UPDATE operations

Python functions which execute upon INSERT and UPDATE operations

SQL expressions which are embedded in INSERT statements (or in some cases execute beforehand)

SQL expressions which are embedded in UPDATE statements

Server side default values used during INSERT

Markers for server-side triggers used during UPDATE

The general rule for all insert/update defaults is that they only take effect if no value for a particular column is passed as an execute() parameter; otherwise, the given value is used.

The simplest kind of default is a scalar value used as the default value of a column:

Above, the value “12” will be bound as the column value during an INSERT if no other value is supplied.

A scalar value may also be associated with an UPDATE statement, though this is not very common (as UPDATE statements are usually looking for dynamic defaults):

The Column.default and Column.onupdate keyword arguments also accept Python functions. These functions are invoked at the time of insert or update if no other value for that column is supplied, and the value returned is used for the column’s value. Below illustrates a crude “sequence” that assigns an incrementing counter to a primary key column:

It should be noted that for real “incrementing sequence” behavior, the built-in capabilities of the database should normally be used, which may include sequence objects or other autoincrementing capabilities. For primary key columns, SQLAlchemy will in most cases use these capabilities automatically. See the API documentation for Column including the Column.autoincrement flag, as well as the section on Sequence later in this chapter for background on standard primary key generation techniques.

To illustrate onupdate, we assign the Python datetime function now to the Column.onupdate attribute:

When an update statement executes and no value is passed for last_updated, the datetime.datetime.now() Python function is executed and its return value used as the value for last_updated. Notice that we provide now as the function itself without calling it (i.e. there are no parenthesis following) - SQLAlchemy will execute the function at the time the statement executes.

The Python functions used by Column.default and Column.onupdate may also make use of the current statement’s context in order to determine a value. The context of a statement is an internal SQLAlchemy object which contains all information about the statement being executed, including its source expression, the parameters associated with it and the cursor. The typical use case for this context with regards to default generation is to have access to the other values being inserted or updated on the row. To access the context, provide a function that accepts a single context argument:

The above default generation function is applied so that it will execute for all INSERT and UPDATE statements where a value for counter_plus_twelve was otherwise not provided, and the value will be that of whatever value is present in the execution for the counter column, plus the number 12.

For a single statement that is being executed using “executemany” style, e.g. with multiple parameter sets passed to Connection.execute(), the user-defined function is called once for each set of parameters. For the use case of a multi-valued Insert construct (e.g. with more than one VALUES clause set up via the Insert.values() method), the user-defined function is also called once for each set of parameters.

When the function is invoked, the special method DefaultExecutionContext.get_current_parameters() is available from the context object (an subclass of DefaultExecutionContext). This method returns a dictionary of column-key to values that represents the full set of values for the INSERT or UPDATE statement. In the case of a multi-valued INSERT construct, the subset of parameters that corresponds to the individual VALUES clause is isolated from the full parameter dictionary and returned alone.

Added in version 1.2: Added DefaultExecutionContext.get_current_parameters() method, which improves upon the still-present DefaultExecutionContext.current_parameters attribute by offering the service of organizing multiple VALUES clauses into individual parameter dictionaries.

The Column.default and Column.onupdate keywords may also be passed SQL expressions, which are in most cases rendered inline within the INSERT or UPDATE statement:

Above, the create_date column will be populated with the result of the now() SQL function (which, depending on backend, compiles into NOW() or CURRENT_TIMESTAMP in most cases) during an INSERT statement, and the key column with the result of a SELECT subquery from another table. The last_modified column will be populated with the value of the SQL UTC_TIMESTAMP() MySQL function when an UPDATE statement is emitted for this table.

When using SQL functions with the func construct, we “call” the named function, e.g. with parenthesis as in func.now(). This differs from when we specify a Python callable as a default such as datetime.datetime, where we pass the function itself, but we don’t invoke it ourselves. In the case of a SQL function, invoking func.now() returns the SQL expression object that will render the “NOW” function into the SQL being emitted.

Default and update SQL expressions specified by Column.default and Column.onupdate are invoked explicitly by SQLAlchemy when an INSERT or UPDATE statement occurs, typically rendered inline within the DML statement except in certain cases listed below. This is different than a “server side” default, which is part of the table’s DDL definition, e.g. as part of the “CREATE TABLE” statement, which are likely more common. For server side defaults, see the next section Server-invoked DDL-Explicit Default Expressions.

When a SQL expression indicated by Column.default is used with primary key columns, there are some cases where SQLAlchemy must “pre-execute” the default generation SQL function, meaning it is invoked in a separate SELECT statement, and the resulting value is passed as a parameter to the INSERT. This only occurs for primary key columns for an INSERT statement that is being asked to return this primary key value, where RETURNING or cursor.lastrowid may not be used. An Insert construct that specifies the insert.inline flag will always render default expressions inline.

When the statement is executed with a single set of parameters (that is, it is not an “executemany” style execution), the returned CursorResult will contain a collection accessible via CursorResult.postfetch_cols() which contains a list of all Column objects which had an inline-executed default. Similarly, all parameters which were bound to the statement, including all Python and SQL expressions which were pre-executed, are present in the CursorResult.last_inserted_params() or CursorResult.last_updated_params() collections on CursorResult. The CursorResult.inserted_primary_key collection contains a list of primary key values for the row inserted (a list so that single-column and composite-column primary keys are represented in the same format).

A variant on the SQL expression default is the Column.server_default, which gets placed in the CREATE TABLE statement during a Table.create() operation:

A create call for the above table will produce:

The above example illustrates the two typical use cases for Column.server_default, that of the SQL function (SYSDATE in the above example) as well as a server-side constant value (the integer “0” in the above example). It is advisable to use the text() construct for any literal SQL values as opposed to passing the raw value, as SQLAlchemy does not typically perform any quoting or escaping on these values.

Like client-generated expressions, Column.server_default can accommodate SQL expressions in general, however it is expected that these will usually be simple functions and expressions, and not the more complex cases like an embedded SELECT.

Columns which generate a new value on INSERT or UPDATE based on other server-side database mechanisms, such as database-specific auto-generating behaviors such as seen with TIMESTAMP columns on some platforms, as well as custom triggers that invoke upon INSERT or UPDATE to generate a new value, may be called out using FetchedValue as a marker:

The FetchedValue indicator does not affect the rendered DDL for the CREATE TABLE. Instead, it marks the column as one that will have a new value populated by the database during the process of an INSERT or UPDATE statement, and for supporting databases may be used to indicate that the column should be part of a RETURNING or OUTPUT clause for the statement. Tools such as the SQLAlchemy ORM then make use of this marker in order to know how to get at the value of the column after such an operation. In particular, the ValuesBase.return_defaults() method can be used with an Insert or Update construct to indicate that these values should be returned.

For details on using FetchedValue with the ORM, see Fetching Server-Generated Defaults.

The Column.server_onupdate directive does not currently produce MySQL’s “ON UPDATE CURRENT_TIMESTAMP()” clause. See Rendering ON UPDATE CURRENT TIMESTAMP for MySQL / MariaDB’s explicit_defaults_for_timestamp for background on how to produce this clause.

Fetching Server-Generated Defaults

SQLAlchemy represents database sequences using the Sequence object, which is considered to be a special case of “column default”. It only has an effect on databases which have explicit support for sequences, which among SQLAlchemy’s included dialects includes PostgreSQL, Oracle Database, MS SQL Server, and MariaDB. The Sequence object is otherwise ignored.

In newer database engines, the Identity construct should likely be preferred vs. Sequence for generation of integer primary key values. See the section Identity Columns (GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY) for background on this construct.

The Sequence may be placed on any column as a “default” generator to be used during INSERT operations, and can also be configured to fire off during UPDATE operations if desired. It is most commonly used in conjunction with a single integer primary key column:

Where above, the table cartitems is associated with a sequence named cart_id_seq. Emitting MetaData.create_all() for the above table will include:

When using tables with explicit schema names (detailed at Specifying the Schema Name), the configured schema of the Table is not automatically shared by an embedded Sequence, instead, specify Sequence.schema:

The Sequence may also be made to automatically make use of the MetaData.schema setting on the MetaData in use; see Associating a Sequence with the MetaData for background.

When Insert DML constructs are invoked against the cartitems table, without an explicit value passed for the cart_id column, the cart_id_seq sequence will be used to generate a value on participating backends. Typically, the sequence function is embedded in the INSERT statement, which is combined with RETURNING so that the newly generated value can be returned to the Python process:

When using Connection.execute() to invoke an Insert construct, newly generated primary key identifiers, including but not limited to those generated using Sequence, are available from the CursorResult construct using the CursorResult.inserted_primary_key attribute.

When the Sequence is associated with a Column as its Python-side default generator, the Sequence will also be subject to “CREATE SEQUENCE” and “DROP SEQUENCE” DDL when similar DDL is emitted for the owning Table, such as when using MetaData.create_all() to generate DDL for a series of tables.

The Sequence may also be associated with a MetaData construct directly. This allows the Sequence to be used in more than one Table at a time and also allows the MetaData.schema parameter to be inherited. See the section Associating a Sequence with the MetaData for background.

PostgreSQL’s SERIAL datatype is an auto-incrementing type that implies the implicit creation of a PostgreSQL sequence when CREATE TABLE is emitted. The Sequence construct, when indicated for a Column, may indicate that it should not be used in this specific case by specifying a value of True for the Sequence.optional parameter. This allows the given Sequence to be used for backends that have no alternative primary key generation system but to ignore it for backends such as PostgreSQL which will automatically generate a sequence for a particular column:

In the above example, CREATE TABLE for PostgreSQL will make use of the SERIAL datatype for the cart_id column, and the cart_id_seq sequence will be ignored. However on Oracle Database, the cart_id_seq sequence will be created explicitly.

This particular interaction of SERIAL and SEQUENCE is fairly legacy, and as in other cases, using Identity instead will simplify the operation to simply use IDENTITY on all supported backends.

A SEQUENCE is a first class schema object in SQL and can be used to generate values independently in the database. If you have a Sequence object, it can be invoked with its “next value” instruction by passing it directly to a SQL execution method:

In order to embed the “next value” function of a Sequence inside of a SQL statement like a SELECT or INSERT, use the Sequence.next_value() method, which will render at statement compilation time a SQL function that is appropriate for the target backend:

For a Sequence that is to be associated with arbitrary Table objects, the Sequence may be associated with a particular MetaData, using the Sequence.metadata parameter:

Such a sequence can then be associated with columns in the usual way:

In the above example, the Sequence object is treated as an independent schema construct that can exist on its own or be shared among tables.

Explicitly associating the Sequence with MetaData allows for the following behaviors:

The Sequence will inherit the MetaData.schema parameter specified to the target MetaData, which affects the production of CREATE / DROP DDL as well as how the Sequence.next_value() function is rendered in SQL statements.

The MetaData.create_all() and MetaData.drop_all() methods will emit CREATE / DROP for this Sequence, even if the Sequence is not associated with any Table / Column that’s a member of this MetaData.

The following technique is known to work only with the PostgreSQL database. It does not work with Oracle Database.

The preceding sections illustrate how to associate a Sequence with a Column as the Python side default generator:

In the above case, the Sequence will automatically be subject to CREATE SEQUENCE / DROP SEQUENCE DDL when the related Table is subject to CREATE / DROP. However, the sequence will not be present as the server-side default for the column when CREATE TABLE is emitted.

If we want the sequence to be used as a server-side default, meaning it takes place even if we emit INSERT commands to the table from the SQL command line, we can use the Column.server_default parameter in conjunction with the value-generation function of the sequence, available from the Sequence.next_value() method. Below we illustrate the same Sequence being associated with the Column both as the Python-side default generator as well as the server-side default generator:

When the “CREATE TABLE” statement is emitted, on PostgreSQL it would be emitted as:

Placement of the Sequence in both the Python-side and server-side default generation contexts ensures that the “primary key fetch” logic works in all cases. Typically, sequence-enabled databases also support RETURNING for INSERT statements, which is used automatically by SQLAlchemy when emitting this statement. However if RETURNING is not used for a particular insert, then SQLAlchemy would prefer to “pre-execute” the sequence outside of the INSERT statement itself, which only works if the sequence is included as the Python-side default generator function.

The example also associates the Sequence with the enclosing MetaData directly, which again ensures that the Sequence is fully associated with the parameters of the MetaData collection including the default schema, if any.

Sequences/SERIAL/IDENTITY - in the PostgreSQL dialect documentation

RETURNING Support - in the Oracle Database dialect documentation

Added in version 1.3.11.

The Computed construct allows a Column to be declared in DDL as a “GENERATED ALWAYS AS” column, that is, one which has a value that is computed by the database server. The construct accepts a SQL expression typically declared textually using a string or the text() construct, in a similar manner as that of CheckConstraint. The SQL expression is then interpreted by the database server in order to determine the value for the column within a row.

The DDL for the square table when run on a PostgreSQL 12 backend will look like:

Whether the value is persisted upon INSERT and UPDATE, or if it is calculated on fetch, is an implementation detail of the database; the former is known as “stored” and the latter is known as “virtual”. Some database implementations support both, but some only support one or the other. The optional Computed.persisted flag may be specified as True or False to indicate if the “STORED” or “VIRTUAL” keyword should be rendered in DDL, however this will raise an error if the keyword is not supported by the target backend; leaving it unset will use a working default for the target backend.

The Computed construct is a subclass of the FetchedValue object, and will set itself up as both the “server default” and “server onupdate” generator for the target Column, meaning it will be treated as a default generating column when INSERT and UPDATE statements are generated, as well as that it will be fetched as a generating column when using the ORM. This includes that it will be part of the RETURNING clause of the database for databases which support RETURNING and the generated values are to be eagerly fetched.

A Column that is defined with the Computed construct may not store any value outside of that which the server applies to it; SQLAlchemy’s behavior when a value is passed for such a column to be written in INSERT or UPDATE is currently that the value will be ignored.

“GENERATED ALWAYS AS” is currently known to be supported by:

MySQL version 5.7 and onwards

MariaDB 10.x series and onwards

PostgreSQL as of version 12

Oracle Database - with the caveat that RETURNING does not work correctly with UPDATE (a warning will be emitted to this effect when the UPDATE..RETURNING that includes a computed column is rendered)

SQLite as of version 3.31

When Computed is used with an unsupported backend, if the target dialect does not support it, a CompileError is raised when attempting to render the construct. Otherwise, if the dialect supports it but the particular database server version in use does not, then a subclass of DBAPIError, usually OperationalError, is raised when the DDL is emitted to the database.

Added in version 1.4.

The Identity construct allows a Column to be declared as an identity column and rendered in DDL as “GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY”. An identity column has its value automatically generated by the database server using an incrementing (or decrementing) sequence. The construct shares most of its option to control the database behaviour with Sequence.

The DDL for the data table when run on a PostgreSQL 12 backend will look like:

The database will generate a value for the id column upon insert, starting from 42, if the statement did not already contain a value for the id column. An identity column can also require that the database generates the value of the column, ignoring the value passed with the statement or raising an error, depending on the backend. To activate this mode, set the parameter Identity.always to True in the Identity construct. Updating the previous example to include this parameter will generate the following DDL:

The Identity construct is a subclass of the FetchedValue object, and will set itself up as the “server default” generator for the target Column, meaning it will be treated as a default generating column when INSERT statements are generated, as well as that it will be fetched as a generating column when using the ORM. This includes that it will be part of the RETURNING clause of the database for databases which support RETURNING and the generated values are to be eagerly fetched.

The Identity construct is currently known to be supported by:

PostgreSQL as of version 10.

Oracle Database as of version 12. It also supports passing always=None to enable the default generated mode and the parameter on_null=True to specify “ON NULL” in conjunction with a “BY DEFAULT” identity column.

Microsoft SQL Server. MSSQL uses a custom syntax that only supports the start and increment parameters, and ignores all other.

When Identity is used with an unsupported backend, it is ignored, and the default SQLAlchemy logic for autoincrementing columns is used.

An error is raised when a Column specifies both an Identity and also sets Column.autoincrement to False.

A plain default value on a column.

Defines a generated column, i.e. “GENERATED ALWAYS AS” syntax.

A DDL-specified DEFAULT column value.

Base class for column default values.

A marker for a transparent database-side default.

Defines an identity column, i.e. “GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY” syntax.

Represents a named database sequence.

inherits from sqlalchemy.schema.FetchedValue, sqlalchemy.schema.SchemaItem

Defines a generated column, i.e. “GENERATED ALWAYS AS” syntax.

The Computed construct is an inline construct added to the argument list of a Column object:

See the linked documentation below for complete details.

Added in version 1.3.11.

Computed Columns (GENERATED ALWAYS AS)

Construct a GENERATED ALWAYS AS DDL construct to accompany a Column.

Construct a GENERATED ALWAYS AS DDL construct to accompany a Column.

sqltext¶ – A string containing the column generation expression, which will be used verbatim, or a SQL expression construct, such as a text() object. If given as a string, the object is converted to a text() object.

Optional, controls how this column should be persisted by the database. Possible values are:

None, the default, it will use the default persistence defined by the database.

True, will render GENERATED ALWAYS AS ... STORED, or the equivalent for the target database if supported.

False, will render GENERATED ALWAYS AS ... VIRTUAL, or the equivalent for the target database if supported.

Specifying True or False may raise an error when the DDL is emitted to the target database if the database does not support that persistence option. Leaving this parameter at its default of None is guaranteed to succeed for all databases that support GENERATED ALWAYS AS.

Deprecated since version 1.4: The Computed.copy() method is deprecated and will be removed in a future release.

inherits from sqlalchemy.schema.DefaultGenerator, abc.ABC

A plain default value on a column.

This could correspond to a constant, a callable function, or a SQL clause.

ColumnDefault is generated automatically whenever the default, onupdate arguments of Column are used. A ColumnDefault can be passed positionally as well.

For example, the following:

inherits from sqlalchemy.schema.FetchedValue

A DDL-specified DEFAULT column value.

DefaultClause is a FetchedValue that also generates a “DEFAULT” clause when “CREATE TABLE” is emitted.

DefaultClause is generated automatically whenever the server_default, server_onupdate arguments of Column are used. A DefaultClause can be passed positionally as well.

For example, the following:

inherits from sqlalchemy.sql.expression.Executable, sqlalchemy.schema.SchemaItem

Base class for column default values.

This object is only present on column.default or column.onupdate. It’s not valid as a server default.

inherits from sqlalchemy.sql.expression.SchemaEventTarget

A marker for a transparent database-side default.

Use FetchedValue when the database is configured to provide some automatic default for a column.

Would indicate that some trigger or default generator will create a new value for the foo column during an INSERT.

Marking Implicitly Generated Values, timestamps, and Triggered Columns

inherits from sqlalchemy.schema.HasSchemaAttr, sqlalchemy.schema.IdentityOptions, sqlalchemy.schema.DefaultGenerator

Represents a named database sequence.

The Sequence object represents the name and configurational parameters of a database sequence. It also represents a construct that can be “executed” by a SQLAlchemy Engine or Connection, rendering the appropriate “next value” function for the target database and returning a result.

The Sequence is typically associated with a primary key column:

When CREATE TABLE is emitted for the above Table, if the target platform supports sequences, a CREATE SEQUENCE statement will be emitted as well. For platforms that don’t support sequences, the Sequence construct is ignored.

Construct a Sequence object.

Creates this sequence in the database.

Drops this sequence from the database.

Return a next_value function element which will render the appropriate increment function for this Sequence within any SQL expression.

Construct a Sequence object.

name¶ – the name of the sequence.

the starting index of the sequence. This value is used when the CREATE SEQUENCE command is emitted to the database as the value of the “START WITH” clause. If None, the clause is omitted, which on most platforms indicates a starting value of 1.

Changed in version 2.0: The Sequence.start parameter is required in order to have DDL emit “START WITH”. This is a reversal of a change made in version 1.4 which would implicitly render “START WITH 1” if the Sequence.start were not included. See The Sequence construct reverts to not having any explicit default “start” value; impacts MS SQL Server for more detail.

increment¶ – the increment value of the sequence. This value is used when the CREATE SEQUENCE command is emitted to the database as the value of the “INCREMENT BY” clause. If None, the clause is omitted, which on most platforms indicates an increment of 1.

minvalue¶ – the minimum value of the sequence. This value is used when the CREATE SEQUENCE command is emitted to the database as the value of the “MINVALUE” clause. If None, the clause is omitted, which on most platforms indicates a minvalue of 1 and -2^63-1 for ascending and descending sequences, respectively.

maxvalue¶ – the maximum value of the sequence. This value is used when the CREATE SEQUENCE command is emitted to the database as the value of the “MAXVALUE” clause. If None, the clause is omitted, which on most platforms indicates a maxvalue of 2^63-1 and -1 for ascending and descending sequences, respectively.

nominvalue¶ – no minimum value of the sequence. This value is used when the CREATE SEQUENCE command is emitted to the database as the value of the “NO MINVALUE” clause. If None, the clause is omitted, which on most platforms indicates a minvalue of 1 and -2^63-1 for ascending and descending sequences, respectively.

nomaxvalue¶ – no maximum value of the sequence. This value is used when the CREATE SEQUENCE command is emitted to the database as the value of the “NO MAXVALUE” clause. If None, the clause is omitted, which on most platforms indicates a maxvalue of 2^63-1 and -1 for ascending and descending sequences, respectively.

cycle¶ – allows the sequence to wrap around when the maxvalue or minvalue has been reached by an ascending or descending sequence respectively. This value is used when the CREATE SEQUENCE command is emitted to the database as the “CYCLE” clause. If the limit is reached, the next number generated will be the minvalue or maxvalue, respectively. If cycle=False (the default) any calls to nextval after the sequence has reached its maximum value will return an error.

schema¶ – optional schema name for the sequence, if located in a schema other than the default. The rules for selecting the schema name when a MetaData is also present are the same as that of Table.schema.

cache¶ – optional integer value; number of future values in the sequence which are calculated in advance. Renders the CACHE keyword understood by Oracle Database and PostgreSQL.

order¶ – optional boolean value; if True, renders the ORDER keyword, understood by Oracle Database, indicating the sequence is definitively ordered. May be necessary to provide deterministic ordering using Oracle RAC.

The type to be returned by the sequence, for dialects that allow us to choose between INTEGER, BIGINT, etc. (e.g., mssql).

Added in version 1.4.0.

optional¶ – boolean value, when True, indicates that this Sequence object only needs to be explicitly generated on backends that don’t provide another way to generate primary key identifiers. Currently, it essentially means, “don’t create this sequence on the PostgreSQL backend, where the SERIAL keyword creates a sequence for us automatically”.

quote¶ – boolean value, when True or False, explicitly forces quoting of the Sequence.name on or off. When left at its default of None, normal quoting rules based on casing and reserved words take place.

quote_schema¶ – Set the quoting preferences for the schema name.

optional MetaData object which this Sequence will be associated with. A Sequence that is associated with a MetaData gains the following capabilities:

The Sequence will inherit the MetaData.schema parameter specified to the target MetaData, which affects the production of CREATE / DROP DDL, if any.

The Sequence.create() and Sequence.drop() methods automatically use the engine bound to the MetaData object, if any.

The MetaData.create_all() and MetaData.drop_all() methods will emit CREATE / DROP for this Sequence, even if the Sequence is not associated with any Table / Column that’s a member of this MetaData.

The above behaviors can only occur if the Sequence is explicitly associated with the MetaData via this parameter.

Associating a Sequence with the MetaData - full discussion of the Sequence.metadata parameter.

for_update¶ – Indicates this Sequence, when associated with a Column, should be invoked for UPDATE statements on that column’s table, rather than for INSERT statements, when no value is otherwise present for that column in the statement.

Creates this sequence in the database.

Drops this sequence from the database.

Return a next_value function element which will render the appropriate increment function for this Sequence within any SQL expression.

inherits from sqlalchemy.schema.IdentityOptions, sqlalchemy.schema.FetchedValue, sqlalchemy.schema.SchemaItem

Defines an identity column, i.e. “GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY” syntax.

The Identity construct is an inline construct added to the argument list of a Column object:

See the linked documentation below for complete details.

Added in version 1.4.

Identity Columns (GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY)

Construct a GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY DDL construct to accompany a Column.

Construct a GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY DDL construct to accompany a Column.

See the Sequence documentation for a complete description of most parameters.

MSSQL supports this construct as the preferred alternative to generate an IDENTITY on a column, but it uses non standard syntax that only support Identity.start and Identity.increment. All other parameters are ignored.

always¶ – A boolean, that indicates the type of identity column. If False is specified, the default, then the user-specified value takes precedence. If True is specified, a user-specified value is not accepted ( on some backends, like PostgreSQL, OVERRIDING SYSTEM VALUE, or similar, may be specified in an INSERT to override the sequence value). Some backends also have a default value for this parameter, None can be used to omit rendering this part in the DDL. It will be treated as False if a backend does not have a default value.

on_null¶ – Set to True to specify ON NULL in conjunction with a always=False identity column. This option is only supported on some backends, like Oracle Database.

start¶ – the starting index of the sequence.

increment¶ – the increment value of the sequence.

minvalue¶ – the minimum value of the sequence.

maxvalue¶ – the maximum value of the sequence.

nominvalue¶ – no minimum value of the sequence.

nomaxvalue¶ – no maximum value of the sequence.

cycle¶ – allows the sequence to wrap around when the maxvalue or minvalue has been reached.

cache¶ – optional integer value; number of future values in the sequence which are calculated in advance.

order¶ – optional boolean value; if true, renders the ORDER keyword.

Deprecated since version 1.4: The Identity.copy() method is deprecated and will be removed in a future release.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (unknown):
```unknown
Table("mytable", metadata_obj, Column("somecolumn", Integer, default=12))
```

Example 2 (unknown):
```unknown
Table("mytable", metadata_obj, Column("somecolumn", Integer, onupdate=25))
```

Example 3 (python):
```python
# a function which counts upwards
i = 0


def mydefault():
    global i
    i += 1
    return i


t = Table(
    "mytable",
    metadata_obj,
    Column("id", Integer, primary_key=True, default=mydefault),
)
```

Example 4 (python):
```python
import datetime

t = Table(
    "mytable",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    # define 'last_updated' to be populated with datetime.now()
    Column("last_updated", DateTime, onupdate=datetime.datetime.now),
)
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/faq/ormconfiguration.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - Frequently Asked Questions
    - Project Versions
- ORM Configuration¶
- How do I map a table that has no primary key?¶
- How do I configure a Column that is a Python reserved word or similar?¶
- How do I get a list of all columns, relationships, mapped attributes, etc. given a mapped class?¶
- I’m getting a warning or error about “Implicitly combining column X under attribute Y”¶
- I’m using Declarative and setting primaryjoin/secondaryjoin using an and_() or or_(), and I am getting an error message about foreign keys.¶

Home | Download this Documentation

Home | Download this Documentation

How do I map a table that has no primary key?

How do I configure a Column that is a Python reserved word or similar?

How do I get a list of all columns, relationships, mapped attributes, etc. given a mapped class?

I’m getting a warning or error about “Implicitly combining column X under attribute Y”

I’m using Declarative and setting primaryjoin/secondaryjoin using an and_() or or_(), and I am getting an error message about foreign keys.

Why is ORDER BY recommended with LIMIT (especially with subqueryload())?

What are default, default_factory and insert_default and what should I use?

Part One - Classic SQLAlchemy that is not using dataclasses

Part Two - Using Dataclasses support with MappedAsDataclass

The SQLAlchemy ORM, in order to map to a particular table, needs there to be at least one column denoted as a primary key column; multiple-column, i.e. composite, primary keys are of course entirely feasible as well. These columns do not need to be actually known to the database as primary key columns, though it’s a good idea that they are. It’s only necessary that the columns behave as a primary key does, e.g. as a unique and not nullable identifier for a row.

Most ORMs require that objects have some kind of primary key defined because the object in memory must correspond to a uniquely identifiable row in the database table; at the very least, this allows the object can be targeted for UPDATE and DELETE statements which will affect only that object’s row and no other. However, the importance of the primary key goes far beyond that. In SQLAlchemy, all ORM-mapped objects are at all times linked uniquely within a Session to their specific database row using a pattern called the identity map, a pattern that’s central to the unit of work system employed by SQLAlchemy, and is also key to the most common (and not-so-common) patterns of ORM usage.

It’s important to note that we’re only talking about the SQLAlchemy ORM; an application which builds on Core and deals only with Table objects, select() constructs and the like, does not need any primary key to be present on or associated with a table in any way (though again, in SQL, all tables should really have some kind of primary key, lest you need to actually update or delete specific rows).

In almost all cases, a table does have a so-called candidate key, which is a column or series of columns that uniquely identify a row. If a table truly doesn’t have this, and has actual fully duplicate rows, the table is not corresponding to first normal form and cannot be mapped. Otherwise, whatever columns comprise the best candidate key can be applied directly to the mapper:

Better yet is when using fully declared table metadata, use the primary_key=True flag on those columns:

All tables in a relational database should have primary keys. Even a many-to-many association table - the primary key would be the composite of the two association columns:

Column-based attributes can be given any name desired in the mapping. See Naming Declarative Mapped Columns Explicitly.

This information is all available from the Mapper object.

To get at the Mapper for a particular mapped class, call the inspect() function on it:

From there, all information about the class can be accessed through properties such as:

Mapper.attrs - a namespace of all mapped attributes. The attributes themselves are instances of MapperProperty, which contain additional attributes that can lead to the mapped SQL expression or column, if applicable.

Mapper.column_attrs - the mapped attribute namespace limited to column and SQL expression attributes. You might want to use Mapper.columns to get at the Column objects directly.

Mapper.relationships - namespace of all RelationshipProperty attributes.

Mapper.all_orm_descriptors - namespace of all mapped attributes, plus user-defined attributes defined using systems such as hybrid_property, AssociationProxy and others.

Mapper.columns - A namespace of Column objects and other named SQL expressions associated with the mapping.

Mapper.mapped_table - The Table or other selectable to which this mapper is mapped.

Mapper.local_table - The Table that is “local” to this mapper; this differs from Mapper.mapped_table in the case of a mapper mapped using inheritance to a composed selectable.

This condition refers to when a mapping contains two columns that are being mapped under the same attribute name due to their name, but there’s no indication that this is intentional. A mapped class needs to have explicit names for every attribute that is to store an independent value; when two columns have the same name and aren’t disambiguated, they fall under the same attribute and the effect is that the value from one column is copied into the other, based on which column was assigned to the attribute first.

This behavior is often desirable and is allowed without warning in the case where the two columns are linked together via a foreign key relationship within an inheritance mapping. When the warning or exception occurs, the issue can be resolved by either assigning the columns to differently-named attributes, or if combining them together is desired, by using column_property() to make this explicit.

Given the example as follows:

As of SQLAlchemy version 0.9.5, the above condition is detected, and will warn that the id column of A and B is being combined under the same-named attribute id, which above is a serious issue since it means that a B object’s primary key will always mirror that of its A.

A mapping which resolves this is as follows:

Suppose we did want A.id and B.id to be mirrors of each other, despite the fact that B.a_id is where A.id is related. We could combine them together using column_property():

That’s an and_() of two string expressions, which SQLAlchemy cannot apply any mapping towards. Declarative allows relationship() arguments to be specified as strings, which are converted into expression objects using eval(). But this doesn’t occur inside of an and_() expression - it’s a special operation declarative applies only to the entirety of what’s passed to primaryjoin or other arguments as a string:

Or if the objects you need are already available, skip the strings:

The same idea applies to all the other arguments, such as foreign_keys:

When ORDER BY is not used for a SELECT statement that returns rows, the relational database is free to returned matched rows in any arbitrary order. While this ordering very often corresponds to the natural order of rows within a table, this is not the case for all databases and all queries. The consequence of this is that any query that limits rows using LIMIT or OFFSET, or which merely selects the first row of the result, discarding the rest, will not be deterministic in terms of what result row is returned, assuming there’s more than one row that matches the query’s criteria.

While we may not notice this for simple queries on databases that usually returns rows in their natural order, it becomes more of an issue if we also use subqueryload() to load related collections, and we may not be loading the collections as intended.

SQLAlchemy implements subqueryload() by issuing a separate query, the results of which are matched up to the results from the first query. We see two queries emitted like this:

The second query embeds the first query as a source of rows. When the inner query uses OFFSET and/or LIMIT without ordering, the two queries may not see the same results:

Depending on database specifics, there is a chance we may get a result like the following for the two queries:

Above, we receive two addresses rows for user.id of 2, and none for 1. We’ve wasted two rows and failed to actually load the collection. This is an insidious error because without looking at the SQL and the results, the ORM will not show that there’s any issue; if we access the addresses for the User we have, it will emit a lazy load for the collection and we won’t see that anything actually went wrong.

The solution to this problem is to always specify a deterministic sort order, so that the main query always returns the same set of rows. This generally means that you should Select.order_by() on a unique column on the table. The primary key is a good choice for this:

Note that the joinedload() eager loader strategy does not suffer from the same problem because only one query is ever issued, so the load query cannot be different from the main query. Similarly, the selectinload() eager loader strategy also does not have this issue as it links its collection loads directly to primary key values just loaded.

Subquery Eager Loading

There’s a bit of a clash in SQLAlchemy’s API here due to the addition of PEP-681 dataclass transforms, which is strict about its naming conventions. PEP-681 comes into play if you are using MappedAsDataclass as shown in Declarative Dataclass Mapping. If you are not using MappedAsDataclass, then it does not apply.

When not using MappedAsDataclass, as has been the case for many years in SQLAlchemy, the mapped_column() (and Column) construct supports a parameter mapped_column.default. This indicates a Python-side default (as opposed to a server side default that would be part of your database’s schema definition) that will take place when an INSERT statement is emitted. This default can be any of a static Python value like a string, or a Python callable function, or a SQLAlchemy SQL construct. Full documentation for mapped_column.default is at Client-Invoked SQL Expressions.

When using mapped_column.default with an ORM mapping that is not using MappedAsDataclass, this default value /callable does not show up on your object when you first construct it. It only takes place when SQLAlchemy works up an INSERT statement for your object.

A very important thing to note is that when using mapped_column() (and Column), the classic mapped_column.default parameter is also available under a new name, called mapped_column.insert_default. If you build a mapped_column() and you are not using MappedAsDataclass, the mapped_column.default and mapped_column.insert_default parameters are synonymous.

When you are using MappedAsDataclass, that is, the specific form of mapping used at Declarative Dataclass Mapping, the meaning of the mapped_column.default keyword changes. We recognize that it’s not ideal that this name changes its behavior, however there was no alternative as PEP-681 requires mapped_column.default to take on this meaning.

When dataclasses are used, the mapped_column.default parameter must be used the way it’s described at Python Dataclasses - it refers to a constant value like a string or a number, and is applied to your object immediately when constructed. It is also at the moment also applied to the mapped_column.default parameter of Column where it would be used in an INSERT statement automatically even if not present on the object. If you instead want to use a callable for your dataclass, which will be applied to the object when constructed, you would use mapped_column.default_factory.

The value used for mapped_column.default is also applied to the Column.default parameter of Column. This is so that the value used as the dataclass default is also applied in an ORM INSERT statement for a mapped object where the value was not explicitly passed. Using this parameter is mutually exclusive against the Column.insert_default parameter, meaning that both cannot be used at the same time.

For the specific case of using a callable to generate defaults, the situation changes a bit; the mapped_column.default_factory parameter is a dataclass only parameter that may be used to generate new default values for instances of the class, but only takes place when the object is constructed. That is, it is not equivalent to mapped_column.insert_default with a callable as it will not take effect for a plain insert() statement that does not actually construct the object; it only is useful for objects that are inserted using unit of work patterns, i.e. using Session.add() with Session.flush() / Session.commit(). For defaults that should apply to INSERT statements regardless of how they are invoked, use mapped_column.insert_default instead.

Works with dataclasses?

Works without dataclasses?

Available on object immediately?

Used in INSERT statements?

mapped_column.default

Only if no dataclasses

mapped_column.insert_default

mapped_column.default_factory

✖ (unit of work only)

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (json):
```json
class SomeClass(Base):
    __table__ = some_table_with_no_pk
    __mapper_args__ = {
        "primary_key": [some_table_with_no_pk.c.uid, some_table_with_no_pk.c.bar]
    }
```

Example 2 (typescript):
```typescript
class SomeClass(Base):
    __tablename__ = "some_table_with_no_pk"

    uid = Column(Integer, primary_key=True)
    bar = Column(String, primary_key=True)
```

Example 3 (sql):
```sql
CREATE TABLE my_association (
  user_id INTEGER REFERENCES user(id),
  account_id INTEGER REFERENCES account(id),
  PRIMARY KEY (user_id, account_id)
)
```

Example 4 (python):
```python
from sqlalchemy import inspect

mapper = inspect(MyClass)
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/faq/performance.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - Frequently Asked Questions
    - Project Versions
- Performance¶
- Why is my application slow after upgrading to 1.4 and/or 2.x?¶
  - Step one - turn on SQL logging and confirm whether or not caching is working¶
  - Step two - identify what constructs are blocking caching from being enabled¶
  - Step three - enable caching for the given objects and/or seek alternatives¶
- How can I profile a SQLAlchemy powered application?¶

Home | Download this Documentation

Home | Download this Documentation

Why is my application slow after upgrading to 1.4 and/or 2.x?

Step one - turn on SQL logging and confirm whether or not caching is working

Step two - identify what constructs are blocking caching from being enabled

Step three - enable caching for the given objects and/or seek alternatives

How can I profile a SQLAlchemy powered application?

Result Fetching Slowness - Core

Result Fetching Slowness - ORM

I’m inserting 400,000 rows with the ORM and it’s really slow!

SQLAlchemy as of version 1.4 includes a SQL compilation caching facility which will allow Core and ORM SQL constructs to cache their stringified form, along with other structural information used to fetch results from the statement, allowing the relatively expensive string compilation process to be skipped when another structurally equivalent construct is next used. This system relies upon functionality that is implemented for all SQL constructs, including objects such as Column, select(), and TypeEngine objects, to produce a cache key which fully represents their state to the degree that it affects the SQL compilation process.

The caching system allows SQLAlchemy 1.4 and above to be more performant than SQLAlchemy 1.3 with regards to the time spent converting SQL constructs into strings repeatedly. However, this only works if caching is enabled for the dialect and SQL constructs in use; if not, string compilation is usually similar to that of SQLAlchemy 1.3, with a slight decrease in speed in some cases.

There is one case however where if SQLAlchemy’s new caching system has been disabled (for reasons below), performance for the ORM may be in fact significantly poorer than that of 1.3 or other prior releases which is due to the lack of caching within ORM lazy loaders and object refresh queries, which in the 1.3 and earlier releases used the now-legacy BakedQuery system. If an application is seeing significant (30% or higher) degradations in performance (measured in time for operations to complete) when switching to 1.4, this is the likely cause of the issue, with steps to mitigate below.

SQL Compilation Caching - overview of the caching system

Object will not produce a cache key, Performance Implications - additional information regarding the warnings generated for elements that don’t enable caching.

Here, we want to use the technique described at engine logging, looking for statements with the [no key] indicator or even [dialect does not support caching]. The indicators we would see for SQL statements that are successfully participating in the caching system would be indicating [generated in Xs] when statements are invoked for the first time and then [cached since Xs ago] for the vast majority of statements subsequent. If [no key] is prevalent in particular for SELECT statements, or if caching is disabled entirely due to [dialect does not support caching], this can be the cause of significant performance degradation.

Estimating Cache Performance Using Logging

Assuming statements are not being cached, there should be warnings emitted early in the application’s log (SQLAlchemy 1.4.28 and above only) indicating dialects, TypeEngine objects, and SQL constructs that are not participating in caching.

For user defined datatypes such as those which extend TypeDecorator and UserDefinedType, the warnings will look like:

For custom and third party SQL elements, such as those constructed using the techniques described at Custom SQL Constructs and Compilation Extension, these warnings will look like:

For custom and third party dialects which make use of the Dialect class hierarchy, the warnings will look like:

Steps to mitigate the lack of caching include:

Review and set ExternalType.cache_ok to True for all custom types which extend from TypeDecorator, UserDefinedType, as well as subclasses of these such as PickleType. Set this only if the custom type does not include any additional state attributes which affect how it renders SQL:

If the types in use are from a third-party library, consult with the maintainers of that library so that it may be adjusted and released.

ExternalType.cache_ok - background on requirements to enable caching for custom datatypes.

Make sure third party dialects set Dialect.supports_statement_cache to True. What this indicates is that the maintainers of a third party dialect have made sure their dialect works with SQLAlchemy 1.4 or greater, and that their dialect doesn’t include any compilation features which may get in the way of caching. As there are some common compilation patterns which can in fact interfere with caching, it’s important that dialect maintainers check and test this carefully, adjusting for any of the legacy patterns which won’t work with caching.

Caching for Third Party Dialects - background and examples for third-party dialects to participate in SQL statement caching.

Custom SQL classes, including all DQL / DML constructs one might create using the Custom SQL Constructs and Compilation Extension, as well as ad-hoc subclasses of objects such as Column or Table. The HasCacheKey.inherit_cache attribute may be set to True for trivial subclasses, which do not contain any subclass-specific state information which affects the SQL compilation.

Enabling Caching Support for Custom Constructs - guidelines for applying the HasCacheKey.inherit_cache attribute.

SQL Compilation Caching - caching system overview

Object will not produce a cache key, Performance Implications - background on warnings emitted when caching is not enabled for specific constructs and/or dialects.

Looking for performance issues typically involves two strategies. One is query profiling, and the other is code profiling.

Sometimes just plain SQL logging (enabled via python’s logging module or via the echo=True argument on create_engine()) can give an idea how long things are taking. For example, if you log something right after a SQL operation, you’d see something like this in your log:

if you logged myapp.somemessage right after the operation, you know it took 334ms to complete the SQL part of things.

Logging SQL will also illustrate if dozens/hundreds of queries are being issued which could be better organized into much fewer queries. When using the SQLAlchemy ORM, the “eager loading” feature is provided to partially (contains_eager()) or fully (joinedload(), subqueryload()) automate this activity, but without the ORM “eager loading” typically means to use joins so that results across multiple tables can be loaded in one result set instead of multiplying numbers of queries as more depth is added (i.e. r + r*r2 + r*r2*r3 …)

For more long-term profiling of queries, or to implement an application-side “slow query” monitor, events can be used to intercept cursor executions, using a recipe like the following:

Above, we use the ConnectionEvents.before_cursor_execute() and ConnectionEvents.after_cursor_execute() events to establish an interception point around when a statement is executed. We attach a timer onto the connection using the info dictionary; we use a stack here for the occasional case where the cursor execute events may be nested.

If logging reveals that individual queries are taking too long, you’d need a breakdown of how much time was spent within the database processing the query, sending results over the network, being handled by the DBAPI, and finally being received by SQLAlchemy’s result set and/or ORM layer. Each of these stages can present their own individual bottlenecks, depending on specifics.

For that you need to use the Python Profiling Module. Below is a simple recipe which works profiling into a context manager:

To profile a section of code:

The output of profiling can be used to give an idea where time is being spent. A section of profiling output looks like this:

Above, we can see that the instances() SQLAlchemy function was called 222 times (recursively, and 21 times from the outside), taking a total of .011 seconds for all calls combined.

The specifics of these calls can tell us where the time is being spent. If for example, you see time being spent within cursor.execute(), e.g. against the DBAPI:

this would indicate that the database is taking a long time to start returning results, and it means your query should be optimized, either by adding indexes or restructuring the query and/or underlying schema. For that task, analysis of the query plan is warranted, using a system such as EXPLAIN, SHOW PLAN, etc. as is provided by the database backend.

If on the other hand you see many thousands of calls related to fetching rows, or very long calls to fetchall(), it may mean your query is returning more rows than expected, or that the fetching of rows itself is slow. The ORM itself typically uses fetchall() to fetch rows (or fetchmany() if the Query.yield_per() option is used).

An inordinately large number of rows would be indicated by a very slow call to fetchall() at the DBAPI level:

An unexpectedly large number of rows, even if the ultimate result doesn’t seem to have many rows, can be the result of a cartesian product - when multiple sets of rows are combined together without appropriately joining the tables together. It’s often easy to produce this behavior with SQLAlchemy Core or ORM query if the wrong Column objects are used in a complex query, pulling in additional FROM clauses that are unexpected.

On the other hand, a fast call to fetchall() at the DBAPI level, but then slowness when SQLAlchemy’s CursorResult is asked to do a fetchall(), may indicate slowness in processing of datatypes, such as unicode conversions and similar:

In some cases, a backend might be doing type-level processing that isn’t needed. More specifically, seeing calls within the type API that are slow are better indicators - below is what it looks like when we use a type like this:

the profiling output of this intentionally slow operation can be seen like this:

that is, we see many expensive calls within the type_api system, and the actual time consuming thing is the time.sleep() call.

Make sure to check the Dialect documentation for notes on known performance tuning suggestions at this level, especially for databases like Oracle. There may be systems related to ensuring numeric accuracy or string processing that may not be needed in all cases.

There also may be even more low-level points at which row-fetching performance is suffering; for example, if time spent seems to focus on a call like socket.receive(), that could indicate that everything is fast except for the actual network connection, and too much time is spent with data moving over the network.

To detect slowness in ORM fetching of rows (which is the most common area of performance concern), calls like populate_state() and _instance() will illustrate individual ORM object populations:

The ORM’s slowness in turning rows into ORM-mapped objects is a product of the complexity of this operation combined with the overhead of cPython. Common strategies to mitigate this include:

fetch individual columns instead of full entities, that is:

Use Bundle objects to organize column-based results:

Use result caching - see Dogpile Caching for an in-depth example of this.

Consider a faster interpreter like that of PyPy.

The output of a profile can be a little daunting but after some practice they are very easy to read.

Performance - a suite of performance demonstrations with bundled profiling capabilities.

The nature of ORM inserts has changed, as most included drivers use RETURNING with insertmanyvalues support as of SQLAlchemy 2.0. See the section Optimized ORM bulk insert now implemented for all backends other than MySQL for details.

Overall, SQLAlchemy built-in drivers other than that of MySQL should now offer very fast ORM bulk insert performance.

Third party drivers can opt in to the new bulk infrastructure as well with some small code changes assuming their backends support the necessary syntaxes. SQLAlchemy developers would encourage users of third party dialects to post issues with these drivers, so that they may contact SQLAlchemy developers for assistance.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (unknown):
```unknown
sqlalchemy.ext.SAWarning: MyType will not produce a cache key because the
``cache_ok`` attribute is not set to True. This can have significant
performance implications including some performance degradations in
comparison to prior SQLAlchemy versions. Set this attribute to True if this
type object's state is safe to use in a cache key, or False to disable this
warning.
```

Example 2 (php):
```php
sqlalchemy.exc.SAWarning: Class MyClass will not make use of SQL
compilation caching as it does not set the 'inherit_cache' attribute to
``True``. This can have significant performance implications including some
performance degradations in comparison to prior SQLAlchemy versions. Set
this attribute to True if this object can make use of the cache key
generated by the superclass. Alternatively, this attribute may be set to
False which will disable this warning.
```

Example 3 (typescript):
```typescript
sqlalchemy.exc.SAWarning: Dialect database:driver will not make use of SQL
compilation caching as it does not set the 'supports_statement_cache'
attribute to ``True``. This can have significant performance implications
including some performance degradations in comparison to prior SQLAlchemy
versions. Dialect maintainers should seek to set this attribute to True
after appropriate development and testing for SQLAlchemy 1.4 caching
support. Alternatively, this attribute may be set to False which will
disable this warning.
```

Example 4 (typescript):
```typescript
class MyCustomType(TypeDecorator):
    cache_ok = True
    impl = String
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/tutorial/index.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
    - Project Versions
- SQLAlchemy Unified Tutorial¶
- Tutorial Overview¶
  - Version Check¶

Home | Download this Documentation

Home | Download this Documentation

The SQLAlchemy Unified Tutorial is integrated between the Core and ORM components of SQLAlchemy and serves as a unified introduction to SQLAlchemy as a whole. For users of SQLAlchemy within the 1.x series, in the 2.0 style of working, the ORM uses Core-style querying with the select() construct, and transactional semantics between Core connections and ORM sessions are equivalent. Take note of the blue border styles for each section, that will tell you how “ORM-ish” a particular topic is!

Users who are already familiar with SQLAlchemy, and especially those looking to migrate existing applications to work under the SQLAlchemy 2.0 series within the 1.4 transitional phase should check out the SQLAlchemy 2.0 - Major Migration Guide document as well.

For the newcomer, this document has a lot of detail, however by the end they will be considered an Alchemist.

SQLAlchemy is presented as two distinct APIs, one building on top of the other. These APIs are known as Core and ORM.

SQLAlchemy Core is the foundational architecture for SQLAlchemy as a “database toolkit”. The library provides tools for managing connectivity to a database, interacting with database queries and results, and programmatic construction of SQL statements.

Sections that are primarily Core-only will not refer to the ORM. SQLAlchemy constructs used in these sections will be imported from the sqlalchemy namespace. As an additional indicator of subject classification, they will also include a dark blue border on the right. When using the ORM, these concepts are still in play but are less often explicit in user code. ORM users should read these sections, but not expect to be using these APIs directly for ORM-centric code.

SQLAlchemy ORM builds upon the Core to provide optional object relational mapping capabilities. The ORM provides an additional configuration layer allowing user-defined Python classes to be mapped to database tables and other constructs, as well as an object persistence mechanism known as the Session. It then extends the Core-level SQL Expression Language to allow SQL queries to be composed and invoked in terms of user-defined objects.

Sections that are primarily ORM-only should be titled to include the phrase “ORM”, so that it’s clear this is an ORM related topic. SQLAlchemy constructs used in these sections will be imported from the sqlalchemy.orm namespace. Finally, as an additional indicator of subject classification, they will also include a light blue border on the left. Core-only users can skip these.

Most sections in this tutorial discuss Core concepts that are also used explicitly with the ORM. SQLAlchemy 2.0 in particular features a much greater level of integration of Core API use within the ORM.

For each of these sections, there will be introductory text discussing the degree to which ORM users should expect to be using these programming patterns. SQLAlchemy constructs in these sections will be imported from the sqlalchemy namespace with some potential use of sqlalchemy.orm constructs at the same time. As an additional indicator of subject classification, these sections will also include both a thinner light border on the left, and a thicker dark border on the right. Core and ORM users should familiarize with concepts in these sections equally.

The tutorial will present both concepts in the natural order that they should be learned, first with a mostly-Core-centric approach and then spanning out into more ORM-centric concepts.

The major sections of this tutorial are as follows:

Establishing Connectivity - the Engine - all SQLAlchemy applications start with an Engine object; here’s how to create one.

Working with Transactions and the DBAPI - the usage API of the Engine and its related objects Connection and Result are presented here. This content is Core-centric however ORM users will want to be familiar with at least the Result object.

Working with Database Metadata - SQLAlchemy’s SQL abstractions as well as the ORM rely upon a system of defining database schema constructs as Python objects. This section introduces how to do that from both a Core and an ORM perspective.

Working with Data - here we learn how to create, select, update and delete data in the database. The so-called CRUD operations here are given in terms of SQLAlchemy Core with links out towards their ORM counterparts. The SELECT operation that is introduced in detail at Using SELECT Statements applies equally well to Core and ORM.

Data Manipulation with the ORM covers the persistence framework of the ORM; basically the ORM-centric ways to insert, update and delete, as well as how to handle transactions.

Working with ORM Related Objects introduces the concept of the relationship() construct and provides a brief overview of how it’s used, with links to deeper documentation.

Further Reading lists a series of major top-level documentation sections which fully document the concepts introduced in this tutorial.

This tutorial is written using a system called doctest. All of the code excerpts written with a >>> are actually run as part of SQLAlchemy’s test suite, and the reader is invited to work with the code examples given in real time with their own Python interpreter.

If running the examples, it is advised that the reader performs a quick check to verify that we are on version 2.0 of SQLAlchemy:

SQLAlchemy Unified Tutorial

Next Section: Establishing Connectivity - the Engine

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
>>> import sqlalchemy
>>> sqlalchemy.__version__  
2.0.0
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/versioning.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Configuring a Version Counter¶
- Simple Version Counting¶
- Custom Version Counters / Types¶
- Server Side Version Counters¶
- Programmatic or Conditional Version Counters¶

Home | Download this Documentation

Home | Download this Documentation

The Mapper supports management of a version id column, which is a single table column that increments or otherwise updates its value each time an UPDATE to the mapped table occurs. This value is checked each time the ORM emits an UPDATE or DELETE against the row to ensure that the value held in memory matches the database value.

Because the versioning feature relies upon comparison of the in memory record of an object, the feature only applies to the Session.flush() process, where the ORM flushes individual in-memory rows to the database. It does not take effect when performing a multirow UPDATE or DELETE using Query.update() or Query.delete() methods, as these methods only emit an UPDATE or DELETE statement but otherwise do not have direct access to the contents of those rows being affected.

The purpose of this feature is to detect when two concurrent transactions are modifying the same row at roughly the same time, or alternatively to provide a guard against the usage of a “stale” row in a system that might be reusing data from a previous transaction without refreshing (e.g. if one sets expire_on_commit=False with a Session, it is possible to reuse the data from a previous transaction).

Concurrent transaction updates

When detecting concurrent updates within transactions, it is typically the case that the database’s transaction isolation level is below the level of repeatable read; otherwise, the transaction will not be exposed to a new row value created by a concurrent update which conflicts with the locally updated value. In this case, the SQLAlchemy versioning feature will typically not be useful for in-transaction conflict detection, though it still can be used for cross-transaction staleness detection.

The database that enforces repeatable reads will typically either have locked the target row against a concurrent update, or is employing some form of multi version concurrency control such that it will emit an error when the transaction is committed. SQLAlchemy’s version_id_col is an alternative which allows version tracking to occur for specific tables within a transaction that otherwise might not have this isolation level set.

Repeatable Read Isolation Level - PostgreSQL’s implementation of repeatable read, including a description of the error condition.

The most straightforward way to track versions is to add an integer column to the mapped table, then establish it as the version_id_col within the mapper options:

It is strongly recommended that the version_id column be made NOT NULL. The versioning feature does not support a NULL value in the versioning column.

Above, the User mapping tracks integer versions using the column version_id. When an object of type User is first flushed, the version_id column will be given a value of “1”. Then, an UPDATE of the table later on will always be emitted in a manner similar to the following:

The above UPDATE statement is updating the row that not only matches user.id = 1, it also is requiring that user.version_id = 1, where “1” is the last version identifier we’ve been known to use on this object. If a transaction elsewhere has modified the row independently, this version id will no longer match, and the UPDATE statement will report that no rows matched; this is the condition that SQLAlchemy tests, that exactly one row matched our UPDATE (or DELETE) statement. If zero rows match, that indicates our version of the data is stale, and a StaleDataError is raised.

Other kinds of values or counters can be used for versioning. Common types include dates and GUIDs. When using an alternate type or counter scheme, SQLAlchemy provides a hook for this scheme using the version_id_generator argument, which accepts a version generation callable. This callable is passed the value of the current known version, and is expected to return the subsequent version.

For example, if we wanted to track the versioning of our User class using a randomly generated GUID, we could do this (note that some backends support a native GUID type, but we illustrate here using a simple string):

The persistence engine will call upon uuid.uuid4() each time a User object is subject to an INSERT or an UPDATE. In this case, our version generation function can disregard the incoming value of version, as the uuid4() function generates identifiers without any prerequisite value. If we were using a sequential versioning scheme such as numeric or a special character system, we could make use of the given version in order to help determine the subsequent value.

Backend-agnostic GUID Type

The version_id_generator can also be configured to rely upon a value that is generated by the database. In this case, the database would need some means of generating new identifiers when a row is subject to an INSERT as well as with an UPDATE. For the UPDATE case, typically an update trigger is needed, unless the database in question supports some other native version identifier. The PostgreSQL database in particular supports a system column called xmin which provides UPDATE versioning. We can make use of the PostgreSQL xmin column to version our User class as follows:

With the above mapping, the ORM will rely upon the xmin column for automatically providing the new value of the version id counter.

creating tables that refer to system columns

In the above scenario, as xmin is a system column provided by PostgreSQL, we use the system=True argument to mark it as a system-provided column, omitted from the CREATE TABLE statement. The datatype of this column is an internal PostgreSQL type called xid which acts mostly like a string, so we use the String datatype.

The ORM typically does not actively fetch the values of database-generated values when it emits an INSERT or UPDATE, instead leaving these columns as “expired” and to be fetched when they are next accessed, unless the eager_defaults Mapper flag is set. However, when a server side version column is used, the ORM needs to actively fetch the newly generated value. This is so that the version counter is set up before any concurrent transaction may update it again. This fetching is also best done simultaneously within the INSERT or UPDATE statement using RETURNING, otherwise if emitting a SELECT statement afterwards, there is still a potential race condition where the version counter may change before it can be fetched.

When the target database supports RETURNING, an INSERT statement for our User class will look like this:

Where above, the ORM can acquire any newly generated primary key values along with server-generated version identifiers in one statement. When the backend does not support RETURNING, an additional SELECT must be emitted for every INSERT and UPDATE, which is much less efficient, and also introduces the possibility of missed version counters:

It is strongly recommended that server side version counters only be used when absolutely necessary and only on backends that support RETURNING, currently PostgreSQL, Oracle Database, MariaDB 10.5, SQLite 3.35, and SQL Server.

When version_id_generator is set to False, we can also programmatically (and conditionally) set the version identifier on our object in the same way we assign any other mapped attribute. Such as if we used our UUID example, but set version_id_generator to False, we can set the version identifier at our choosing:

We can update our User object without incrementing the version counter as well; the value of the counter will remain unchanged, and the UPDATE statement will still check against the previous value. This may be useful for schemes where only certain classes of UPDATE are sensitive to concurrency issues:

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (typescript):
```typescript
class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    version_id = mapped_column(Integer, nullable=False)
    name = mapped_column(String(50), nullable=False)

    __mapper_args__ = {"version_id_col": version_id}
```

Example 2 (sql):
```sql
UPDATE user SET version_id=:version_id, name=:name
WHERE user.id = :user_id AND user.version_id = :user_version_id
-- {"name": "new name", "version_id": 2, "user_id": 1, "user_version_id": 1}
```

Example 3 (typescript):
```typescript
import uuid


class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    version_uuid = mapped_column(String(32), nullable=False)
    name = mapped_column(String(50), nullable=False)

    __mapper_args__ = {
        "version_id_col": version_uuid,
        "version_id_generator": lambda version: uuid.uuid4().hex,
    }
```

Example 4 (python):
```python
from sqlalchemy import FetchedValue


class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50), nullable=False)
    xmin = mapped_column("xmin", String, system=True, server_default=FetchedValue())

    __mapper_args__ = {"version_id_col": xmin, "version_id_generator": False}
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/index.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
    - Project Versions
- SQLAlchemy ORM¶

Home | Download this Documentation

Home | Download this Documentation

Here, the Object Relational Mapper is introduced and fully described. If you want to work with higher-level SQL which is constructed automatically for you, as well as automated persistence of Python objects, proceed first to the tutorial.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/errors.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
    - Project Versions
- Error Messages¶
- Connections and Transactions¶
  - QueuePool limit of size <x> overflow <y> reached, connection timed out, timeout <z>¶
  - Pool class cannot be used with asyncio engine (or vice versa)¶
  - Can’t reconnect until invalid transaction is rolled back. Please rollback() fully before proceeding¶
- DBAPI Errors¶

Home | Download this Documentation

Home | Download this Documentation

This section lists descriptions and background for common error messages and warnings raised or emitted by SQLAlchemy.

SQLAlchemy normally raises errors within the context of a SQLAlchemy-specific exception class. For details on these classes, see Core Exceptions and ORM Exceptions.

SQLAlchemy errors can roughly be separated into two categories, the programming-time error and the runtime error. Programming-time errors are raised as a result of functions or methods being called with incorrect arguments, or from other configuration-oriented methods such as mapper configurations that can’t be resolved. The programming-time error is typically immediate and deterministic. The runtime error on the other hand represents a failure that occurs as a program runs in response to some condition that occurs arbitrarily, such as database connections being exhausted or some data-related issue occurring. Runtime errors are more likely to be seen in the logs of a running application as the program encounters these states in response to load and data being encountered.

Since runtime errors are not as easy to reproduce and often occur in response to some arbitrary condition as the program runs, they are more difficult to debug and also affect programs that have already been put into production.

Within this section, the goal is to try to provide background on some of the most common runtime errors as well as programming time errors.

This is possibly the most common runtime error experienced, as it directly involves the work load of the application surpassing a configured limit, one which typically applies to nearly all SQLAlchemy applications.

The following points summarize what this error means, beginning with the most fundamental points that most SQLAlchemy users should already be familiar with.

The SQLAlchemy Engine object uses a pool of connections by default - What this means is that when one makes use of a SQL database connection resource of an Engine object, and then releases that resource, the database connection itself remains connected to the database and is returned to an internal queue where it can be used again. Even though the code may appear to be ending its conversation with the database, in many cases the application will still maintain a fixed number of database connections that persist until the application ends or the pool is explicitly disposed.

Because of the pool, when an application makes use of a SQL database connection, most typically from either making use of Engine.connect() or when making queries using an ORM Session, this activity does not necessarily establish a new connection to the database at the moment the connection object is acquired; it instead consults the connection pool for a connection, which will often retrieve an existing connection from the pool to be reused. If no connections are available, the pool will create a new database connection, but only if the pool has not surpassed a configured capacity.

The default pool used in most cases is called QueuePool. When you ask this pool to give you a connection and none are available, it will create a new connection if the total number of connections in play are less than a configured value. This value is equal to the pool size plus the max overflow. That means if you have configured your engine as:

The above Engine will allow at most 30 connections to be in play at any time, not including connections that were detached from the engine or invalidated. If a request for a new connection arrives and 30 connections are already in use by other parts of the application, the connection pool will block for a fixed period of time, before timing out and raising this error message.

In order to allow for a higher number of connections be in use at once, the pool can be adjusted using the create_engine.pool_size and create_engine.max_overflow parameters as passed to the create_engine() function. The timeout to wait for a connection to be available is configured using the create_engine.pool_timeout parameter.

The pool can be configured to have unlimited overflow by setting create_engine.max_overflow to the value “-1”. With this setting, the pool will still maintain a fixed pool of connections, however it will never block upon a new connection being requested; it will instead unconditionally make a new connection if none are available.

However, when running in this way, if the application has an issue where it is using up all available connectivity resources, it will eventually hit the configured limit of available connections on the database itself, which will again return an error. More seriously, when the application exhausts the database of connections, it usually will have caused a great amount of resources to be used up before failing, and can also interfere with other applications and database status mechanisms that rely upon being able to connect to the database.

Given the above, the connection pool can be looked at as a safety valve for connection use, providing a critical layer of protection against a rogue application causing the entire database to become unavailable to all other applications. When receiving this error message, it is vastly preferable to repair the issue using up too many connections and/or configure the limits appropriately, rather than allowing for unlimited overflow which does not actually solve the underlying issue.

What causes an application to use up all the connections that it has available?

The application is fielding too many concurrent requests to do work based on the configured value for the pool - This is the most straightforward cause. If you have an application that runs in a thread pool that allows for 30 concurrent threads, with one connection in use per thread, if your pool is not configured to allow at least 30 connections checked out at once, you will get this error once your application receives enough concurrent requests. Solution is to raise the limits on the pool or lower the number of concurrent threads.

The application is not returning connections to the pool - This is the next most common reason, which is that the application is making use of the connection pool, but the program is failing to release these connections and is instead leaving them open. The connection pool as well as the ORM Session do have logic such that when the session and/or connection object is garbage collected, it results in the underlying connection resources being released, however this behavior cannot be relied upon to release resources in a timely manner.

A common reason this can occur is that the application uses ORM sessions and does not call Session.close() upon them once the work involving that session is complete. Solution is to make sure ORM sessions if using the ORM, or engine-bound Connection objects if using Core, are explicitly closed at the end of the work being done, either via the appropriate .close() method, or by using one of the available context managers (e.g. “with:” statement) to properly release the resource.

The application is attempting to run long-running transactions - A database transaction is a very expensive resource, and should never be left idle waiting for some event to occur. If an application is waiting for a user to push a button, or a result to come off of a long running job queue, or is holding a persistent connection open to a browser, don’t keep a database transaction open for the whole time. As the application needs to work with the database and interact with an event, open a short-lived transaction at that point and then close it.

The application is deadlocking - Also a common cause of this error and more difficult to grasp, if an application is not able to complete its use of a connection either due to an application-side or database-side deadlock, the application can use up all the available connections which then leads to additional requests receiving this error. Reasons for deadlocks include:

Using an implicit async system such as gevent or eventlet without properly monkeypatching all socket libraries and drivers, or which has bugs in not fully covering for all monkeypatched driver methods, or less commonly when the async system is being used against CPU-bound workloads and greenlets making use of database resources are simply waiting too long to attend to them. Neither implicit nor explicit async programming frameworks are typically necessary or appropriate for the vast majority of relational database operations; if an application must use an async system for some area of functionality, it’s best that database-oriented business methods run within traditional threads that pass messages to the async part of the application.

A database side deadlock, e.g. rows are mutually deadlocked

Threading errors, such as mutexes in a mutual deadlock, or calling upon an already locked mutex in the same thread

Keep in mind an alternative to using pooling is to turn off pooling entirely. See the section Switching Pool Implementations for background on this. However, note that when this error message is occurring, it is always due to a bigger problem in the application itself; the pool just helps to reveal the problem sooner.

Working with Engines and Connections

The QueuePool pool class uses a thread.Lock object internally and is not compatible with asyncio. If using the create_async_engine() function to create an AsyncEngine, the appropriate queue pool class is AsyncAdaptedQueuePool, which is used automatically and does not need to be specified.

In addition to AsyncAdaptedQueuePool, the NullPool and StaticPool pool classes do not use locks and are also suitable for use with async engines.

This error is also raised in reverse in the unlikely case that the AsyncAdaptedQueuePool pool class is indicated explicitly with the create_engine() function.

This error condition refers to the case where a Connection was invalidated, either due to a database disconnect detection or due to an explicit call to Connection.invalidate(), but there is still a transaction present that was initiated either explicitly by the Connection.begin() method, or due to the connection automatically beginning a transaction as occurs in the 2.x series of SQLAlchemy when any SQL statements are emitted. When a connection is invalidated, any Transaction that was in progress is now in an invalid state, and must be explicitly rolled back in order to remove it from the Connection.

The Python database API, or DBAPI, is a specification for database drivers which can be located at Pep-249. This API specifies a set of exception classes that accommodate the full range of failure modes of the database.

SQLAlchemy does not generate these exceptions directly. Instead, they are intercepted from the database driver and wrapped by the SQLAlchemy-provided exception DBAPIError, however the messaging within the exception is generated by the driver, not SQLAlchemy.

Exception raised for errors that are related to the database interface rather than the database itself.

This error is a DBAPI Error and originates from the database driver (DBAPI), not SQLAlchemy itself.

The InterfaceError is sometimes raised by drivers in the context of the database connection being dropped, or not being able to connect to the database. For tips on how to deal with this, see the section Dealing with Disconnects.

Exception raised for errors that are related to the database itself, and not the interface or data being passed.

This error is a DBAPI Error and originates from the database driver (DBAPI), not SQLAlchemy itself.

Exception raised for errors that are due to problems with the processed data like division by zero, numeric value out of range, etc.

This error is a DBAPI Error and originates from the database driver (DBAPI), not SQLAlchemy itself.

Exception raised for errors that are related to the database’s operation and not necessarily under the control of the programmer, e.g. an unexpected disconnect occurs, the data source name is not found, a transaction could not be processed, a memory allocation error occurred during processing, etc.

This error is a DBAPI Error and originates from the database driver (DBAPI), not SQLAlchemy itself.

The OperationalError is the most common (but not the only) error class used by drivers in the context of the database connection being dropped, or not being able to connect to the database. For tips on how to deal with this, see the section Dealing with Disconnects.

Exception raised when the relational integrity of the database is affected, e.g. a foreign key check fails.

This error is a DBAPI Error and originates from the database driver (DBAPI), not SQLAlchemy itself.

Exception raised when the database encounters an internal error, e.g. the cursor is not valid anymore, the transaction is out of sync, etc.

This error is a DBAPI Error and originates from the database driver (DBAPI), not SQLAlchemy itself.

The InternalError is sometimes raised by drivers in the context of the database connection being dropped, or not being able to connect to the database. For tips on how to deal with this, see the section Dealing with Disconnects.

Exception raised for programming errors, e.g. table not found or already exists, syntax error in the SQL statement, wrong number of parameters specified, etc.

This error is a DBAPI Error and originates from the database driver (DBAPI), not SQLAlchemy itself.

The ProgrammingError is sometimes raised by drivers in the context of the database connection being dropped, or not being able to connect to the database. For tips on how to deal with this, see the section Dealing with Disconnects.

Exception raised in case a method or database API was used which is not supported by the database, e.g. requesting a .rollback() on a connection that does not support transaction or has transactions turned off.

This error is a DBAPI Error and originates from the database driver (DBAPI), not SQLAlchemy itself.

SQLAlchemy as of version 1.4 includes a SQL compilation caching facility which will allow Core and ORM SQL constructs to cache their stringified form, along with other structural information used to fetch results from the statement, allowing the relatively expensive string compilation process to be skipped when another structurally equivalent construct is next used. This system relies upon functionality that is implemented for all SQL constructs, including objects such as Column, select(), and TypeEngine objects, to produce a cache key which fully represents their state to the degree that it affects the SQL compilation process.

If the warnings in question refer to widely used objects such as Column objects, and are shown to be affecting the majority of SQL constructs being emitted (using the estimation techniques described at Estimating Cache Performance Using Logging) such that caching is generally not enabled for an application, this will negatively impact performance and can in some cases effectively produce a performance degradation compared to prior SQLAlchemy versions. The FAQ at Why is my application slow after upgrading to 1.4 and/or 2.x? covers this in additional detail.

Caching relies on being able to generate a cache key that accurately represents the complete structure of a statement in a consistent fashion. If a particular SQL construct (or type) does not have the appropriate directives in place which allow it to generate a proper cache key, then caching cannot be safely enabled:

The cache key must represent the complete structure: If the usage of two separate instances of that construct may result in different SQL being rendered, caching the SQL against the first instance of the element using a cache key that does not capture the distinct differences between the first and second elements will result in incorrect SQL being cached and rendered for the second instance.

The cache key must be consistent: If a construct represents state that changes every time, such as a literal value, producing unique SQL for every instance of it, this construct is also not safe to cache, as repeated use of the construct will quickly fill up the statement cache with unique SQL strings that will likely not be used again, defeating the purpose of the cache.

For the above two reasons, SQLAlchemy’s caching system is extremely conservative about deciding to cache the SQL corresponding to an object.

The warning is emitted based on the criteria below. For further detail on each, see the section Why is my application slow after upgrading to 1.4 and/or 2.x?.

The Dialect itself (i.e. the module that is specified by the first part of the URL we pass to create_engine(), like postgresql+psycopg2://), must indicate it has been reviewed and tested to support caching correctly, which is indicated by the Dialect.supports_statement_cache attribute being set to True. When using third party dialects, consult with the maintainers of the dialect so that they may follow the steps to ensure caching may be enabled in their dialect and publish a new release.

Third party or user defined types that inherit from either TypeDecorator or UserDefinedType must include the ExternalType.cache_ok attribute in their definition, including for all derived subclasses, following the guidelines described in the docstring for ExternalType.cache_ok. As before, if these datatypes are imported from third party libraries, consult with the maintainers of that library so that they may provide the necessary changes to their library and publish a new release.

Third party or user defined SQL constructs that subclass from classes such as ClauseElement, Column, Insert etc, including simple subclasses as well as those which are designed to work with the Custom SQL Constructs and Compilation Extension, should normally include the HasCacheKey.inherit_cache attribute set to True or False based on the design of the construct, following the guidelines described at Enabling Caching Support for Custom Constructs.

Estimating Cache Performance Using Logging - background on observing cache behavior and efficiency

Why is my application slow after upgrading to 1.4 and/or 2.x? - in the Frequently Asked Questions section

This error usually occurs when attempting to stringify a SQL expression construct that includes elements which are not part of the default compilation; in this case, the error will be against the StrSQLCompiler class. In less common cases, it can also occur when the wrong kind of SQL expression is used with a particular type of database backend; in those cases, other kinds of SQL compiler classes will be named, such as SQLCompiler or sqlalchemy.dialects.postgresql.PGCompiler. The guidance below is more specific to the “stringification” use case but describes the general background as well.

Normally, a Core SQL construct or ORM Query object can be stringified directly, such as when we use print():

When the above SQL expression is stringified, the StrSQLCompiler compiler class is used, which is a special statement compiler that is invoked when a construct is stringified without any dialect-specific information.

However, there are many constructs that are specific to some particular kind of database dialect, for which the StrSQLCompiler doesn’t know how to turn into a string, such as the PostgreSQL INSERT…ON CONFLICT (Upsert) construct:

In order to stringify constructs that are specific to particular backend, the ClauseElement.compile() method must be used, passing either an Engine or a Dialect object which will invoke the correct compiler. Below we use a PostgreSQL dialect:

For an ORM Query object, the statement can be accessed using the Query.statement accessor:

See the FAQ link below for additional detail on direct stringification / compilation of SQL elements.

How do I render SQL expressions as strings, possibly with bound parameters inlined?

This often occurs when attempting to use a column_property() or deferred() object in the context of a SQL expression, usually within declarative such as:

Above, the cprop attribute is used inline before it has been mapped, however this cprop attribute is not a Column, it’s a ColumnProperty, which is an interim object and therefore does not have the full functionality of either the Column object or the InstrumentedAttribute object that will be mapped onto the Bar class once the declarative process is complete.

While the ColumnProperty does have a __clause_element__() method, which allows it to work in some column-oriented contexts, it can’t work in an open-ended comparison context as illustrated above, since it has no Python __eq__() method that would allow it to interpret the comparison to the number “5” as a SQL expression and not a regular Python comparison.

The solution is to access the Column directly using the ColumnProperty.expression attribute:

This error occurs when a statement makes use of bindparam() either implicitly or explicitly and does not provide a value when the statement is executed:

Above, no value has been provided for the parameter “my_param”. The correct approach is to provide a value:

When the message takes the form “a value is required for bind parameter <x> in parameter group <y>”, the message is referring to the “executemany” style of execution. In this case, the statement is typically an INSERT, UPDATE, or DELETE and a list of parameters is being passed. In this format, the statement may be generated dynamically to include parameter positions for every parameter given in the argument list, where it will use the first set of parameters to determine what these should be.

For example, the statement below is calculated based on the first parameter set to require the parameters, “a”, “b”, and “c” - these names determine the final string format of the statement which will be used for each set of parameters in the list. As the second entry does not contain “b”, this error is generated:

Since “b” is required, pass it as None so that the INSERT may proceed:

This refers to a change made as of SQLAlchemy 1.4 where a SELECT statement as generated by a function such as select(), but also including things like unions and textual SELECT expressions are no longer considered to be FromClause objects and can’t be placed directly in the FROM clause of another SELECT statement without them being wrapped in a Subquery first. This is a major conceptual change in the Core and the full rationale is discussed at A SELECT statement is no longer implicitly considered to be a FROM clause.

Above, stmt represents a SELECT statement. The error is produced when we want to use stmt directly as a FROM clause in another SELECT, such as if we attempted to select from it:

Or if we wanted to use it in a FROM clause such as in a JOIN:

In previous versions of SQLAlchemy, using a SELECT inside of another SELECT would produce a parenthesized, unnamed subquery. In most cases, this form of SQL is not very useful as databases like MySQL and PostgreSQL require that subqueries in FROM clauses have named aliases, which means using the SelectBase.alias() method or as of 1.4 using the SelectBase.subquery() method to produce this. On other databases, it is still much clearer for the subquery to have a name to resolve any ambiguity on future references to column names inside the subquery.

Beyond the above practical reasons, there are a lot of other SQLAlchemy-oriented reasons the change is being made. The correct form of the above two statements therefore requires that SelectBase.subquery() is used:

A SELECT statement is no longer implicitly considered to be a FROM clause

Added in version 1.4.26.

This deprecation warning refers to a very old and likely not well known pattern that applies to the legacy Query.join() method as well as the 2.0 style Select.join() method, where a join can be stated in terms of a relationship() but the target is the Table or other Core selectable to which the class is mapped, rather than an ORM entity such as a mapped class or aliased() construct:

The above pattern also allows an arbitrary selectable, such as a Core Join or Alias object, however there is no automatic adaptation of this element, meaning the Core element would need to be referenced directly:

The correct way to specify a join target is always by using the mapped class itself or an aliased object, in the latter case using the PropComparator.of_type() modifier to set up an alias:

Added in version 1.4.26.

This warning is typically generated when querying using the Select.join() method or the legacy Query.join() method with mappings that involve joined table inheritance. The issue is that when joining between two joined inheritance models that share a common base table, a proper SQL JOIN between the two entities cannot be formed without applying an alias to one side or the other; SQLAlchemy applies an alias to the right side of the join. For example given a joined inheritance mapping as:

The above mapping includes a relationship between the Employee and Manager classes. Since both classes make use of the “employee” database table, from a SQL perspective this is a self referential relationship. If we wanted to query from both the Employee and Manager models using a join, at the SQL level the “employee” table needs to be included twice in the query, which means it must be aliased. When we create such a join using the SQLAlchemy ORM, we get SQL that looks like the following:

Above, the SQL selects FROM the employee table, representing the Employee entity in the query. It then joins to a right-nested join of employee AS employee_1 JOIN manager AS manager_1, where the employee table is stated again, except as an anonymous alias employee_1. This is the ‘automatic generation of an alias’ to which the warning message refers.

When SQLAlchemy loads ORM rows that each contain an Employee and a Manager object, the ORM must adapt rows from what above is the employee_1 and manager_1 table aliases into those of the un-aliased Manager class. This process is internally complex and does not accommodate for all API features, notably when trying to use eager loading features such as contains_eager() with more deeply nested queries than are shown here. As the pattern is unreliable for more complex scenarios and involves implicit decisionmaking that is difficult to anticipate and follow, the warning is emitted and this pattern may be considered a legacy feature. The better way to write this query is to use the same patterns that apply to any other self-referential relationship, which is to use the aliased() construct explicitly. For joined-inheritance and other join-oriented mappings, it is usually desirable to add the use of the aliased.flat parameter, which will allow a JOIN of two or more tables to be aliased by applying an alias to the individual tables within the join, rather than embedding the join into a new subquery:

If we then wanted to use contains_eager() to populate the reports_to attribute, we refer to the alias:

Without using the explicit aliased() object, in some more nested cases the contains_eager() option does not have enough context to know where to get its data from, in the case that the ORM is “auto-aliasing” in a very nested context. Therefore it’s best not to rely on this feature and instead keep the SQL construction as explicit as possible.

SQLAlchemy 2.0 introduced a new system described at Session raises proactively when illegal concurrent or reentrant access is detected, which proactively detects concurrent methods being invoked on an individual instance of the Session object and by extension the AsyncSession proxy object. These concurrent access calls typically, though not exclusively, would occur when a single instance of Session is shared among multiple concurrent threads without such access being synchronized, or similarly when a single instance of AsyncSession is shared among multiple concurrent tasks (such as when using a function like asyncio.gather()). These use patterns are not the appropriate use of these objects, where without the proactive warning system SQLAlchemy implements would still otherwise produce invalid state within the objects, producing hard-to-debug errors including driver-level errors on the database connections themselves.

Instances of Session and AsyncSession are mutable, stateful objects with no built-in synchronization of method calls, and represent a single, ongoing database transaction upon a single database connection at a time for a particular Engine or AsyncEngine to which the object is bound (note that these objects both support being bound to multiple engines at once, however in this case there will still be only one connection per engine in play within the scope of a transaction). A single database transaction is not an appropriate target for concurrent SQL commands; instead, an application that runs concurrent database operations should use concurrent transactions. For these objects then it follows that the appropriate pattern is Session per thread, or AsyncSession per task.

For more background on concurrency see the section Is the Session thread-safe? Is AsyncSession safe to share in concurrent tasks?.

This is likely the most common error message when dealing with the ORM, and it occurs as a result of the nature of a technique the ORM makes wide use of known as lazy loading. Lazy loading is a common object-relational pattern whereby an object that’s persisted by the ORM maintains a proxy to the database itself, such that when various attributes upon the object are accessed, their value may be retrieved from the database lazily. The advantage to this approach is that objects can be retrieved from the database without having to load all of their attributes or related data at once, and instead only that data which is requested can be delivered at that time. The major disadvantage is basically a mirror image of the advantage, which is that if lots of objects are being loaded which are known to require a certain set of data in all cases, it is wasteful to load that additional data piecemeal.

Another caveat of lazy loading beyond the usual efficiency concerns is that in order for lazy loading to proceed, the object has to remain associated with a Session in order to be able to retrieve its state. This error message means that an object has become de-associated with its Session and is being asked to lazy load data from the database.

The most common reason that objects become detached from their Session is that the session itself was closed, typically via the Session.close() method. The objects will then live on to be accessed further, very often within web applications where they are delivered to a server-side templating engine and are asked for further attributes which they cannot load.

Mitigation of this error is via these techniques:

Try not to have detached objects; don’t close the session prematurely - Often, applications will close out a transaction before passing off related objects to some other system which then fails due to this error. Sometimes the transaction doesn’t need to be closed so soon; an example is the web application closes out the transaction before the view is rendered. This is often done in the name of “correctness”, but may be seen as a mis-application of “encapsulation”, as this term refers to code organization, not actual actions. The template that uses an ORM object is making use of the proxy pattern which keeps database logic encapsulated from the caller. If the Session can be held open until the lifespan of the objects are done, this is the best approach.

Otherwise, load everything that’s needed up front - It is very often impossible to keep the transaction open, especially in more complex applications that need to pass objects off to other systems that can’t run in the same context even though they’re in the same process. In this case, the application should prepare to deal with detached objects, and should try to make appropriate use of eager loading to ensure that objects have what they need up front.

And importantly, set expire_on_commit to False - When using detached objects, the most common reason objects need to re-load data is because they were expired from the last call to Session.commit(). This expiration should not be used when dealing with detached objects; so the Session.expire_on_commit parameter be set to False. By preventing the objects from becoming expired outside of the transaction, the data which was loaded will remain present and will not incur additional lazy loads when that data is accessed.

Note also that Session.rollback() method unconditionally expires all contents in the Session and should also be avoided in non-error scenarios.

Relationship Loading Techniques - detailed documentation on eager loading and other relationship-oriented loading techniques

Committing - background on session commit

Refreshing / Expiring - background on attribute expiry

The flush process of the Session, described at Flushing, will roll back the database transaction if an error is encountered, in order to maintain internal consistency. However, once this occurs, the session’s transaction is now “inactive” and must be explicitly rolled back by the calling application, in the same way that it would otherwise need to be explicitly committed if a failure had not occurred.

This is a common error when using the ORM and typically applies to an application that doesn’t yet have correct “framing” around its Session operations. Further detail is described in the FAQ at “This Session’s transaction has been rolled back due to a previous exception during flush.” (or similar).

This error arises when the “delete-orphan” cascade is set on a many-to-one or many-to-many relationship, such as:

Above, the “delete-orphan” setting on B.a indicates the intent that when every B object that refers to a particular A is deleted, that the A should then be deleted as well. That is, it expresses that the “orphan” which is being deleted would be an A object, and it becomes an “orphan” when every B that refers to it is deleted.

The “delete-orphan” cascade model does not support this functionality. The “orphan” consideration is only made in terms of the deletion of a single object which would then refer to zero or more objects that are now “orphaned” by this single deletion, which would result in those objects being deleted as well. In other words, it is designed only to track the creation of “orphans” based on the removal of one and only one “parent” object per orphan, which is the natural case in a one-to-many relationship where a deletion of the object on the “one” side results in the subsequent deletion of the related items on the “many” side.

The above mapping in support of this functionality would instead place the cascade setting on the one-to-many side, which looks like:

Where the intent is expressed that when an A is deleted, all of the B objects to which it refers are also deleted.

The error message then goes on to suggest the usage of the relationship.single_parent flag. This flag may be used to enforce that a relationship which is capable of having many objects refer to a particular object will in fact have only one object referring to it at a time. It is used for legacy or other less ideal database schemas where the foreign key relationships suggest a “many” collection, however in practice only one object would actually refer to a given target object at at time. This uncommon scenario can be demonstrated in terms of the above example as follows:

The above configuration will then install a validator which will enforce that only one B may be associated with an A at at time, within the scope of the B.a relationship:

Note that this validator is of limited scope and will not prevent multiple “parents” from being created via the other direction. For example, it will not detect the same setting in terms of A.bs:

However, things will not go as expected later on, as the “delete-orphan” cascade will continue to work in terms of a single lead object, meaning if we delete either of the B objects, the A is deleted. The other B stays around, where the ORM will usually be smart enough to set the foreign key attribute to NULL, but this is usually not what’s desired:

For all the above examples, similar logic applies to the calculus of a many-to-many relationship; if a many-to-many relationship sets single_parent=True on one side, that side can use the “delete-orphan” cascade, however this is very unlikely to be what someone actually wants as the point of a many-to-many relationship is so that there can be many objects referring to an object in either direction.

Overall, “delete-orphan” cascade is usually applied on the “one” side of a one-to-many relationship so that it deletes objects in the “many” side, and not the other way around.

Changed in version 1.3.18: The text of the “delete-orphan” error message when used on a many-to-one or many-to-many relationship has been updated to be more descriptive.

Instance <instance> is already associated with an instance of <instance> via its <attribute> attribute, and is only allowed a single parent.

This error is emitted when the relationship.single_parent flag is used, and more than one object is assigned as the “parent” of an object at once.

Given the following mapping:

The intent indicates that no more than a single B object may refer to a particular A object at once:

When this error occurs unexpectedly, it is usually because the relationship.single_parent flag was applied in response to the error message described at For relationship <relationship>, delete-orphan cascade is normally configured only on the “one” side of a one-to-many relationship, and not on the “many” side of a many-to-one or many-to-many relationship., and the issue is in fact a misunderstanding of the “delete-orphan” cascade setting. See that message for details.

For relationship <relationship>, delete-orphan cascade is normally configured only on the “one” side of a one-to-many relationship, and not on the “many” side of a many-to-one or many-to-many relationship.

This warning refers to the case when two or more relationships will write data to the same columns on flush, but the ORM does not have any means of coordinating these relationships together. Depending on specifics, the solution may be that two relationships need to be referenced by one another using relationship.back_populates, or that one or more of the relationships should be configured with relationship.viewonly to prevent conflicting writes, or sometimes that the configuration is fully intentional and should configure relationship.overlaps to silence each warning.

For the typical example that’s missing relationship.back_populates, given the following mapping:

The above mapping will generate warnings:

The relationships Child.parent and Parent.children appear to be in conflict. The solution is to apply relationship.back_populates:

For more customized relationships where an “overlap” situation may be intentional and cannot be resolved, the relationship.overlaps parameter may specify the names of relationships for which the warning should not take effect. This typically occurs for two or more relationships to the same underlying table that include custom relationship.primaryjoin conditions that limit the related items in each case:

Above, the ORM will know that the overlap between Parent.c1, Parent.c2 and Child.parent is intentional.

Added in version 1.4.26.

This message was added to accommodate for the case where a Result object that would yield ORM objects is iterated after the originating Session has been closed, or otherwise had its Session.expunge_all() method called. When a Session expunges all objects at once, the internal identity map used by that Session is replaced with a new one, and the original one discarded. An unconsumed and unbuffered Result object will internally maintain a reference to that now-discarded identity map. Therefore, when the Result is consumed, the objects that would be yielded cannot be associated with that Session. This arrangement is by design as it is generally not recommended to iterate an unbuffered Result object outside of the transactional context in which it was created:

The above situation typically will not occur when using the asyncio ORM extension, as when AsyncSession returns a sync-style Result, the results have been pre-buffered when the statement was executed. This is to allow secondary eager loaders to invoke without needing an additional await call.

To pre-buffer results in the above situation using the regular Session in the same way that the asyncio extension does it, the prebuffer_rows execution option may be used as follows:

Above, the selected ORM objects are fully generated within the session_obj block, associated with session_obj and buffered within the Result object for iteration. Outside the block, session_obj is closed and expunges these ORM objects. Iterating the Result object will yield those ORM objects, however as their originating Session has expunged them, they will be delivered in the detached state.

The above reference to a “pre-buffered” vs. “un-buffered” Result object refers to the process by which the ORM converts incoming raw database rows from the DBAPI into ORM objects. It does not imply whether or not the underlying cursor object itself, which represents pending results from the DBAPI, is itself buffered or unbuffered, as this is essentially a lower layer of buffering. For background on buffering of the cursor results itself, see the section Using Server Side Cursors (a.k.a. stream results).

SQLAlchemy 2.0 introduces a new Annotated Declarative Table declarative system which derives ORM mapped attribute information from PEP 484 annotations within class definitions at runtime. A requirement of this form is that all ORM annotations must make use of a generic container called Mapped to be properly annotated. Legacy SQLAlchemy mappings which include explicit PEP 484 typing annotations, such as those which use the legacy Mypy extension for typing support, may include directives such as those for relationship() that don’t include this generic.

To resolve, the classes may be marked with the __allow_unmapped__ boolean attribute until they can be fully migrated to the 2.0 syntax. See the migration notes at Migration to 2.0 Step Six - Add __allow_unmapped__ to explicitly typed ORM models for an example.

Migration to 2.0 Step Six - Add __allow_unmapped__ to explicitly typed ORM models - in the SQLAlchemy 2.0 - Major Migration Guide document

This warning occurs when using the SQLAlchemy ORM Mapped Dataclasses feature described at Declarative Dataclass Mapping in conjunction with any mixin class or abstract base that is not itself declared as a dataclass, such as in the example below:

Above, since Mixin does not itself extend from MappedAsDataclass, the following warning is generated:

The fix is to add MappedAsDataclass to the signature of Mixin as well:

Python’s PEP 681 specification does not accommodate for attributes declared on superclasses of dataclasses that are not themselves dataclasses; per the behavior of Python dataclasses, such fields are ignored, as in the following example:

Above, the User class will not include create_user in its constructor nor will it attempt to interpret update_user as a dataclass attribute. This is because Mixin is not a dataclass.

SQLAlchemy’s dataclasses feature within the 2.0 series does not honor this behavior correctly; instead, attributes on non-dataclass mixins and superclasses are treated as part of the final dataclass configuration. However type checkers such as Pyright and Mypy will not consider these fields as part of the dataclass constructor as they are to be ignored per PEP 681. Since their presence is ambiguous otherwise, SQLAlchemy 2.1 will require that mixin classes which have SQLAlchemy mapped attributes within a dataclass hierarchy have to themselves be dataclasses.

When using the MappedAsDataclass mixin class or registry.mapped_as_dataclass() decorator, SQLAlchemy makes use of the actual Python dataclasses module that’s in the Python standard library in order to apply dataclass behaviors to the target class. This API has its own error scenarios, most of which involve the construction of an __init__() method on the user defined class; the order of attributes declared on the class, as well as on superclasses, determines how the __init__() method will be constructed and there are specific rules in how the attributes are organized as well as how they should make use of parameters such as init=False, kw_only=True, etc. SQLAlchemy does not control or implement these rules. Therefore, for errors of this nature, consult the Python dataclasses documentation, with special attention to the rules applied to inheritance.

Declarative Dataclass Mapping - SQLAlchemy dataclasses documentation

Python dataclasses - on the python.org website

inheritance - on the python.org website

This error occurs when making use of the ORM Bulk UPDATE by Primary Key feature without supplying primary key values in the given records, such as:

Above, the presence of a list of parameter dictionaries combined with usage of the Session to execute an ORM-enabled UPDATE statement will automatically make use of ORM Bulk Update by Primary Key, which expects parameter dictionaries to include primary key values, e.g.:

To invoke the UPDATE statement without supplying per-record primary key values, use Session.connection() to acquire the current Connection, then invoke with that:

ORM Bulk UPDATE by Primary Key

Disabling Bulk ORM Update by Primary Key for an UPDATE statement with multiple parameter sets

The SQLAlchemy async mode requires an async driver to be used to connect to the db. This error is usually raised when trying to use the async version of SQLAlchemy with a non compatible DBAPI.

Asynchronous I/O (asyncio)

A call to the async DBAPI was initiated outside the greenlet spawn context usually setup by the SQLAlchemy AsyncIO proxy classes. Usually this error happens when an IO was attempted in an unexpected place, using a calling pattern that does not directly provide for use of the await keyword. When using the ORM this is nearly always due to the use of lazy loading, which is not directly supported under asyncio without additional steps and/or alternate loader patterns in order to use successfully.

Preventing Implicit IO when Using AsyncSession - covers most ORM scenarios where this problem can occur and how to mitigate, including specific patterns to use with lazy load scenarios.

Using the inspect() function directly on an AsyncConnection or AsyncEngine object is not currently supported, as there is not yet an awaitable form of the Inspector object available. Instead, the object is used by acquiring it using the inspect() function in such a way that it refers to the underlying AsyncConnection.sync_connection attribute of the AsyncConnection object; the Inspector is then used in a “synchronous” calling style by using the AsyncConnection.run_sync() method along with a custom function that performs the desired operations:

Using the Inspector to inspect schema objects - additional examples of using inspect() with the asyncio extension.

See Core Exceptions for Core exception classes.

See ORM Exceptions for ORM exception classes.

Exceptions in this section are not generated by current SQLAlchemy versions, however are provided here to suit exception message hyperlinks.

SQLAlchemy 2.0 represents a major shift for a wide variety of key SQLAlchemy usage patterns in both the Core and ORM components. The goal of the 2.0 release is to make a slight readjustment in some of the most fundamental assumptions of SQLAlchemy since its early beginnings, and to deliver a newly streamlined usage model that is hoped to be significantly more minimalist and consistent between the Core and ORM components, as well as more capable.

Introduced at SQLAlchemy 2.0 - Major Migration Guide, the SQLAlchemy 2.0 project includes a comprehensive future compatibility system that’s integrated into the 1.4 series of SQLAlchemy, such that applications will have a clear, unambiguous, and incremental upgrade path in order to migrate applications to being fully 2.0 compatible. The RemovedIn20Warning deprecation warning is at the base of this system to provide guidance on what behaviors in an existing codebase will need to be modified. An overview of how to enable this warning is at SQLAlchemy 2.0 Deprecations Mode.

SQLAlchemy 2.0 - Major Migration Guide - An overview of the upgrade process from the 1.x series, as well as the current goals and progress of SQLAlchemy 2.0.

SQLAlchemy 2.0 Deprecations Mode - specific guidelines on how to use “2.0 deprecations mode” in SQLAlchemy 1.4.

This message refers to the “backref cascade” behavior of SQLAlchemy, removed in version 2.0. This refers to the action of an object being added into a Session as a result of another object that’s already present in that session being associated with it. As this behavior has been shown to be more confusing than helpful, the relationship.cascade_backrefs and backref.cascade_backrefs parameters were added, which can be set to False to disable it, and in SQLAlchemy 2.0 the “cascade backrefs” behavior has been removed entirely.

For older SQLAlchemy versions, to set relationship.cascade_backrefs to False on a backref that is currently configured using the relationship.backref string parameter, the backref must be declared using the backref() function first so that the backref.cascade_backrefs parameter may be passed.

Alternatively, the entire “cascade backrefs” behavior can be turned off across the board by using the Session in “future” mode, by passing True for the Session.future parameter.

cascade_backrefs behavior deprecated for removal in 2.0 - background on the change for SQLAlchemy 2.0.

The select() construct has been updated as of SQLAlchemy 1.4 to support the newer calling style that is standard in SQLAlchemy 2.0. For backwards compatibility within the 1.4 series, the construct accepts arguments in both the “legacy” style as well as the “new” style.

The “new” style features that column and table expressions are passed positionally to the select() construct only; any other modifiers to the object must be passed using subsequent method chaining:

For comparison, a select() in legacy forms of SQLAlchemy, before methods like Select.where() were even added, would like:

Or even that the “whereclause” would be passed positionally:

For some years now, the additional “whereclause” and other arguments that are accepted have been removed from most narrative documentation, leading to a calling style that is most familiar as the list of column arguments passed as a list, but no further arguments:

The document at select() no longer accepts varied constructor arguments, columns are passed positionally describes this change in terms of 2.0 Migration.

select() no longer accepts varied constructor arguments, columns are passed positionally

SQLAlchemy 2.0 - Major Migration Guide

The concept of “bound metadata” is present up until SQLAlchemy 1.4; as of SQLAlchemy 2.0 it’s been removed.

This error refers to the MetaData.bind parameter on the MetaData object that in turn allows objects like the ORM Session to associate a particular mapped class with an Engine. In SQLAlchemy 2.0, the Session must be linked to each Engine directly. That is, instead of instantiating the Session or sessionmaker without any arguments, and associating the Engine with the MetaData:

The Engine must instead be associated directly with the sessionmaker or Session. The MetaData object should no longer be associated with any engine:

In SQLAlchemy 1.4, this 2.0 style behavior is enabled when the Session.future flag is set on sessionmaker or Session.

This error refers to the concept of “bound metadata”, which is a legacy SQLAlchemy pattern present only in 1.x versions. The issue occurs when one invokes the Executable.execute() method directly off of a Core expression object that is not associated with any Engine:

What the logic is expecting is that the MetaData object has been bound to a Engine:

Where above, any statement that derives from a Table which in turn derives from that MetaData will implicitly make use of the given Engine in order to invoke the statement.

Note that the concept of bound metadata is not present in SQLAlchemy 2.0. The correct way to invoke statements is via the Connection.execute() method of a Connection:

When using the ORM, a similar facility is available via the Session:

Basics of Statement Execution

This error condition was added to SQLAlchemy as of version 1.4, and does not apply to SQLAlchemy 2.0. The error refers to the state where a Connection is placed into a transaction using a method like Connection.begin(), and then a further “marker” transaction is created within that scope; the “marker” transaction is then rolled back using Transaction.rollback() or closed using Transaction.close(), however the outer transaction is still present in an “inactive” state and must be rolled back.

The pattern looks like:

Above, transaction2 is a “marker” transaction, which indicates a logical nesting of transactions within an outer one; while the inner transaction can roll back the whole transaction via its rollback() method, its commit() method has no effect except to close the scope of the “marker” transaction itself. The call to transaction2.rollback() has the effect of deactivating transaction1 which means it is essentially rolled back at the database level, however is still present in order to accommodate a consistent nesting pattern of transactions.

The correct resolution is to ensure the outer transaction is also rolled back:

This pattern is not commonly used in Core. Within the ORM, a similar issue can occur which is the product of the ORM’s “logical” transaction structure; this is described in the FAQ entry at “This Session’s transaction has been rolled back due to a previous exception during flush.” (or similar).

The “subtransaction” pattern is removed in SQLAlchemy 2.0 so that this particular programming pattern is no longer be available, preventing this error message.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
engine = create_engine("mysql+mysqldb://u:p@host/db", pool_size=10, max_overflow=20)
```

Example 2 (python):
```python
>>> from sqlalchemy import column
>>> print(column("x") == 5)
x = :x_1
```

Example 3 (python):
```python
>>> from sqlalchemy.dialects.postgresql import insert
>>> from sqlalchemy import table, column
>>> my_table = table("my_table", column("x"), column("y"))
>>> insert_stmt = insert(my_table).values(x="foo")
>>> insert_stmt = insert_stmt.on_conflict_do_nothing(index_elements=["y"])
>>> print(insert_stmt)
Traceback (most recent call last):

...

sqlalchemy.exc.UnsupportedCompilationError:
Compiler <sqlalchemy.sql.compiler.StrSQLCompiler object at 0x7f04fc17e320>
can't render element of type
<class 'sqlalchemy.dialects.postgresql.dml.OnConflictDoNothing'>
```

Example 4 (sql):
```sql
>>> from sqlalchemy.dialects import postgresql
>>> print(insert_stmt.compile(dialect=postgresql.dialect()))
INSERT INTO my_table (x) VALUES (%(x)s) ON CONFLICT (y) DO NOTHING
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/core/index.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
    - Project Versions
- SQLAlchemy Core¶

Home | Download this Documentation

Home | Download this Documentation

The breadth of SQLAlchemy’s SQL rendering engine, DBAPI integration, transaction integration, and schema description services are documented here. In contrast to the ORM’s domain-centric mode of usage, the SQL Expression Language provides a schema-centric usage paradigm.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/

**Contents:**
- SQLAlchemy 2.0 Documentation
- SQLAlchemy Documentation¶

Contents | Index | Download this Documentation

Home | Download this Documentation

New to SQLAlchemy? Start here:

For Python Beginners: Installation Guide - basic guidance on installing with pip and similar

For Python Veterans: SQLAlchemy Overview - brief architectural overview

New users of SQLAlchemy, as well as veterans of older SQLAlchemy release series, should start with the SQLAlchemy Unified Tutorial, which covers everything an Alchemist needs to know when using the ORM or just Core.

For a quick glance: ORM Quick Start - a glimpse at what working with the ORM looks like

For all users: SQLAlchemy Unified Tutorial - In depth tutorial for Core and ORM

Users coming from older versions of SQLAlchemy, especially those transitioning from the 1.x style of working, will want to review this documentation.

Migrating to SQLAlchemy 2.0 - Complete background on migrating from 1.3 or 1.4 to 2.0

What’s New in SQLAlchemy 2.0? - New 2.0 features and behaviors beyond the 1.x migration

Changelog catalog - Detailed changelogs for all SQLAlchemy Versions

SQLAlchemy ORM - Detailed guides and API reference for using the ORM

Mapping Classes: Mapping Python Classes | Relationship Configuration

Using the ORM: Using the ORM Session | ORM Querying Guide | Using AsyncIO

Configuration Extensions: Association Proxy | Hybrid Attributes | Mutable Scalars | Automap | All extensions

Extending the ORM: ORM Events and Internals

Other: Introduction to Examples

SQLAlchemy Core - Detailed guides and API reference for working with Core

Engines, Connections, Pools: Engine Configuration | Connections, Transactions, Results | AsyncIO Support | Connection Pooling

Schema Definition: Overview | Tables and Columns | Database Introspection (Reflection) | Insert/Update Defaults | Constraints and Indexes | Using Data Definition Language (DDL)

SQL Statements: SQL Expression Elements | Operator Reference | SELECT and related constructs | INSERT, UPDATE, DELETE | SQL Functions | Table of Contents

Datatypes: Overview | Building Custom Types | Type API Reference

Core Basics: Overview | Runtime Inspection API | Event System | Core Event Interfaces | Creating Custom SQL Constructs

Dialect Documentation

The dialect is the system SQLAlchemy uses to communicate with various types of DBAPIs and databases. This section describes notes, options, and usage patterns regarding individual dialects.

PostgreSQL | MySQL and MariaDB | SQLite | Oracle Database | Microsoft SQL Server

Frequently Asked Questions - A collection of common problems and solutions

Glossary - Definitions of terms used in SQLAlchemy documentation

Error Message Guide - Explanations of many SQLAlchemy errors

Complete table of of contents - Full list of available documentation

Index - Index for easy lookup of documentation topics

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/faq/index.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
    - Project Versions
- Frequently Asked Questions¶

Home | Download this Documentation

Home | Download this Documentation

The Frequently Asked Questions section is a growing collection of commonly observed questions to well-known issues.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/dialects/index.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
    - Project Versions
- Dialects¶
- Included Dialects¶
  - Supported versions for Included Dialects¶
  - Support Definitions¶
- External Dialects¶

Home | Download this Documentation

Home | Download this Documentation

The dialect is the system SQLAlchemy uses to communicate with various types of DBAPI implementations and databases. The sections that follow contain reference documentation and notes specific to the usage of each backend, as well as notes for the various DBAPIs.

All dialects require that an appropriate DBAPI driver is installed.

The following table summarizes the support level for each included dialect.

Supported version indicates that most SQLAlchemy features should work for the mentioned database version. Since not all database versions may be tested in the ci there may be some not working edge cases.

Best effort indicates that SQLAlchemy tries to support basic features on these versions, but most likely there will be unsupported features or errors in some use cases. Pull requests with associated issues may be accepted to continue supporting older versions, which are reviewed on a case-by-case basis.

Currently maintained external dialect projects for SQLAlchemy include:

Actian Data Platform, Vector, Actian X, Ingres

aurora-dsql-sqlalchemy

Amazon Redshift (via psycopg2)

Apache Hive and Presto

clickhouse-sqlalchemy

sqlalchemy-cockroachdb

Elasticsearch (readonly)

IBM Netezza Performance Server [1]

Microsoft Access (via pyodbc)

Microsoft SQL Server (via python-tds)

Microsoft SQL Server (via turbodbc)

SAP ASE (fork of former Sybase dialect)

SAP Sybase SQL Anywhere

sqlalchemy-yugabytedb

Supports version 1.3.x only at the moment.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

---
