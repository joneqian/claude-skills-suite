# Sqlalchemy - Dialects

**Pages:** 5

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/dialects/sqlite.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - Dialects
    - Project Versions
- SQLite¶
- DBAPI Support¶
- Date and Time Types¶
  - Ensuring Text affinity¶
- SQLite Auto Incrementing Behavior¶
  - Using the AUTOINCREMENT Keyword¶

Home | Download this Documentation

Home | Download this Documentation

Support for the SQLite database.

The following table summarizes current support levels for database release versions.

The following dialect/DBAPI options are available. Please refer to individual DBAPI sections for connect information.

SQLite does not have built-in DATE, TIME, or DATETIME types, and pysqlite does not provide out of the box functionality for translating values between Python datetime objects and a SQLite-supported format. SQLAlchemy’s own DateTime and related types provide date formatting and parsing functionality when SQLite is used. The implementation classes are DATETIME, DATE and TIME. These types represent dates and times as ISO formatted strings, which also nicely support ordering. There’s no reliance on typical “libc” internals for these functions so historical dates are fully supported.

The DDL rendered for these types is the standard DATE, TIME and DATETIME indicators. However, custom storage formats can also be applied to these types. When the storage format is detected as containing no alpha characters, the DDL for these types is rendered as DATE_CHAR, TIME_CHAR, and DATETIME_CHAR, so that the column continues to have textual affinity.

Type Affinity - in the SQLite documentation

Background on SQLite’s autoincrement is at: https://sqlite.org/autoinc.html

SQLite has an implicit “auto increment” feature that takes place for any non-composite primary-key column that is specifically created using “INTEGER PRIMARY KEY” for the type + primary key.

SQLite also has an explicit “AUTOINCREMENT” keyword, that is not equivalent to the implicit autoincrement feature; this keyword is not recommended for general use. SQLAlchemy does not render this keyword unless a special SQLite-specific directive is used (see below). However, it still requires that the column’s type is named “INTEGER”.

To specifically render the AUTOINCREMENT keyword on the primary key column when rendering DDL, add the flag sqlite_autoincrement=True to the Table construct:

SQLite’s typing model is based on naming conventions. Among other things, this means that any type name which contains the substring "INT" will be determined to be of “integer affinity”. A type named "BIGINT", "SPECIAL_INT" or even "XYZINTQPR", will be considered by SQLite to be of “integer” affinity. However, the SQLite autoincrement feature, whether implicitly or explicitly enabled, requires that the name of the column’s type is exactly the string “INTEGER”. Therefore, if an application uses a type like BigInteger for a primary key, on SQLite this type will need to be rendered as the name "INTEGER" when emitting the initial CREATE TABLE statement in order for the autoincrement behavior to be available.

One approach to achieve this is to use Integer on SQLite only using TypeEngine.with_variant():

Another is to use a subclass of BigInteger that overrides its DDL name to be INTEGER when compiled against SQLite:

TypeEngine.with_variant()

Custom SQL Constructs and Compilation Extension

Datatypes In SQLite Version 3

As a file-based database, SQLite’s approach to transactions differs from traditional databases in many ways. Additionally, the sqlite3 driver standard with Python (as well as the async version aiosqlite which builds on top of it) has several quirks, workarounds, and API features in the area of transaction control, all of which generally need to be addressed when constructing a SQLAlchemy application that uses SQLite.

The most important aspect of transaction handling with the sqlite3 driver is that it defaults (which will continue through Python 3.15 before being removed in Python 3.16) to legacy transactional behavior which does not strictly follow PEP 249. The way in which the driver diverges from the PEP is that it does not “begin” a transaction automatically as dictated by PEP 249 except in the case of DML statements, e.g. INSERT, UPDATE, and DELETE. Normally, PEP 249 dictates that a BEGIN must be emitted upon the first SQL statement of any kind, so that all subsequent operations will be established within a transaction until connection.commit() has been called. The sqlite3 driver, in an effort to be easier to use in highly concurrent environments, skips this step for DQL (e.g. SELECT) statements, and also skips it for DDL (e.g. CREATE TABLE etc.) statements for more legacy reasons. Statements such as SAVEPOINT are also skipped.

In modern versions of the sqlite3 driver as of Python 3.12, this legacy mode of operation is referred to as “legacy transaction control”, and is in effect by default due to the Connection.autocommit parameter being set to the constant sqlite3.LEGACY_TRANSACTION_CONTROL. Prior to Python 3.12, the Connection.autocommit attribute did not exist.

The implications of legacy transaction mode include:

Incorrect support for transactional DDL - statements like CREATE TABLE, ALTER TABLE, CREATE INDEX etc. will not automatically BEGIN a transaction if one were not started already, leading to the changes by each statement being “autocommitted” immediately unless BEGIN were otherwise emitted first. Very old (pre Python 3.6) versions of SQLite would also force a COMMIT for these operations even if a transaction were present, however this is no longer the case.

SERIALIZABLE behavior not fully functional - SQLite’s transaction isolation behavior is normally consistent with SERIALIZABLE isolation, as it is a file- based system that locks the database file entirely for write operations, preventing COMMIT until all reader transactions (and associated file locks) have completed. However, sqlite3’s legacy transaction mode fails to emit BEGIN for SELECT statements, which causes these SELECT statements to no longer be “repeatable”, failing one of the consistency guarantees of SERIALIZABLE.

Incorrect behavior for SAVEPOINT - as the SAVEPOINT statement does not imply a BEGIN, a new SAVEPOINT emitted before a BEGIN will function on its own but fails to participate in the enclosing transaction, meaning a ROLLBACK of the transaction will not rollback elements that were part of a released savepoint.

Legacy transaction mode first existed in order to facilitate working around SQLite’s file locks. Because SQLite relies upon whole-file locks, it is easy to get “database is locked” errors, particularly when newer features like “write ahead logging” are disabled. This is a key reason why sqlite3’s legacy transaction mode is still the default mode of operation; disabling it will produce behavior that is more susceptible to locked database errors. However note that legacy transaction mode will no longer be the default in a future Python version (3.16 as of this writing).

Current SQLAlchemy support allows either for setting the .Connection.autocommit attribute, most directly by using a create_engine() parameter, or if on an older version of Python where the attribute is not available, using event hooks to control the behavior of BEGIN.

Enabling modern sqlite3 transaction control via the autocommit connect parameter (Python 3.12 and above)

To use SQLite in the mode described at Transaction control via the autocommit attribute, the most straightforward approach is to set the attribute to its recommended value of False at the connect level using create_engine.connect_args`:

This parameter is also passed through when using the aiosqlite driver:

The parameter can also be set at the attribute level using the PoolEvents.connect() event hook, however this will only work for sqlite3, as aiosqlite does not yet expose this attribute on its Connection object:

Using SQLAlchemy to emit BEGIN in lieu of SQLite’s transaction control (all Python versions, sqlite3 and aiosqlite)

For older versions of sqlite3 or for cross-compatiblity with older and newer versions, SQLAlchemy can also take over the job of transaction control. This is achieved by using the ConnectionEvents.begin() hook to emit the “BEGIN” command directly, while also disabling SQLite’s control of this command using the PoolEvents.connect() event hook to set the Connection.isolation_level attribute to None:

When using the asyncio variant aiosqlite, refer to engine.sync_engine as in the example below:

SQLAlchemy has a comprehensive database isolation feature with optional autocommit support that is introduced in the section Setting Transaction Isolation Levels including DBAPI Autocommit.

For the sqlite3 and aiosqlite drivers, SQLAlchemy only includes built-in support for “AUTOCOMMIT”. Note that this mode is currently incompatible with the non-legacy isolation mode hooks documented in the previous section at Enabling Non-Legacy SQLite Transactional Modes with the sqlite3 or aiosqlite driver.

To use the sqlite3 driver with SQLAlchemy driver-level autocommit, create an engine setting the create_engine.isolation_level parameter to “AUTOCOMMIT”:

When using the above mode, any event hooks that set the sqlite3 Connection.autocommit parameter away from its default of sqlite3.LEGACY_TRANSACTION_CONTROL as well as hooks that emit BEGIN should be disabled.

Links with important information on SQLite, the sqlite3 driver, as well as long historical conversations on how things got to their current state:

Isolation in SQLite - on the SQLite website

Transaction control - describes the sqlite3 autocommit attribute as well as the legacy isolation_level attribute.

sqlite3 SELECT does not BEGIN a transaction, but should according to spec - imported Python standard library issue on github

sqlite3 module breaks transactions and potentially corrupts data - imported Python standard library issue on github

The SQLite dialect supports SQLite 3.35’s INSERT|UPDATE|DELETE..RETURNING syntax. INSERT..RETURNING may be used automatically in some cases in order to fetch newly generated identifiers in place of the traditional approach of using cursor.lastrowid, however cursor.lastrowid is currently still preferred for simple single-statement cases for its better performance.

To specify an explicit RETURNING clause, use the _UpdateBase.returning() method on a per-statement basis:

Added in version 2.0: Added support for SQLite RETURNING

SQLite supports FOREIGN KEY syntax when emitting CREATE statements for tables, however by default these constraints have no effect on the operation of the table.

Constraint checking on SQLite has three prerequisites:

At least version 3.6.19 of SQLite must be in use

The SQLite library must be compiled without the SQLITE_OMIT_FOREIGN_KEY or SQLITE_OMIT_TRIGGER symbols enabled.

The PRAGMA foreign_keys = ON statement must be emitted on all connections before use – including the initial call to MetaData.create_all().

SQLAlchemy allows for the PRAGMA statement to be emitted automatically for new connections through the usage of events:

When SQLite foreign keys are enabled, it is not possible to emit CREATE or DROP statements for tables that contain mutually-dependent foreign key constraints; to emit the DDL for these tables requires that ALTER TABLE be used to create or drop these constraints separately, for which SQLite has no support.

SQLite Foreign Key Support - on the SQLite web site.

Events - SQLAlchemy event API.

mutually-dependent foreign key constraints.

This section describes the DDL version of “ON CONFLICT” for SQLite, which occurs within a CREATE TABLE statement. For “ON CONFLICT” as applied to an INSERT statement, see INSERT…ON CONFLICT (Upsert).

SQLite supports a non-standard DDL clause known as ON CONFLICT which can be applied to primary key, unique, check, and not null constraints. In DDL, it is rendered either within the “CONSTRAINT” clause or within the column definition itself depending on the location of the target constraint. To render this clause within DDL, the extension parameter sqlite_on_conflict can be specified with a string conflict resolution algorithm within the PrimaryKeyConstraint, UniqueConstraint, CheckConstraint objects. Within the Column object, there are individual parameters sqlite_on_conflict_not_null, sqlite_on_conflict_primary_key, sqlite_on_conflict_unique which each correspond to the three types of relevant constraint types that can be indicated from a Column object.

ON CONFLICT - in the SQLite documentation

Added in version 1.3.

The sqlite_on_conflict parameters accept a string argument which is just the resolution name to be chosen, which on SQLite can be one of ROLLBACK, ABORT, FAIL, IGNORE, and REPLACE. For example, to add a UNIQUE constraint that specifies the IGNORE algorithm:

The above renders CREATE TABLE DDL as:

When using the Column.unique flag to add a UNIQUE constraint to a single column, the sqlite_on_conflict_unique parameter can be added to the Column as well, which will be added to the UNIQUE constraint in the DDL:

To apply the FAIL algorithm for a NOT NULL constraint, sqlite_on_conflict_not_null is used:

this renders the column inline ON CONFLICT phrase:

Similarly, for an inline primary key, use sqlite_on_conflict_primary_key:

SQLAlchemy renders the PRIMARY KEY constraint separately, so the conflict resolution algorithm is applied to the constraint itself:

This section describes the DML version of “ON CONFLICT” for SQLite, which occurs within an INSERT statement. For “ON CONFLICT” as applied to a CREATE TABLE statement, see ON CONFLICT support for constraints.

From version 3.24.0 onwards, SQLite supports “upserts” (update or insert) of rows into a table via the ON CONFLICT clause of the INSERT statement. A candidate row will only be inserted if that row does not violate any unique or primary key constraints. In the case of a unique constraint violation, a secondary action can occur which can be either “DO UPDATE”, indicating that the data in the target row should be updated, or “DO NOTHING”, which indicates to silently skip this row.

Conflicts are determined using columns that are part of existing unique constraints and indexes. These constraints are identified by stating the columns and conditions that comprise the indexes.

SQLAlchemy provides ON CONFLICT support via the SQLite-specific insert() function, which provides the generative methods Insert.on_conflict_do_update() and Insert.on_conflict_do_nothing():

Added in version 1.4.

Upsert - in the SQLite documentation.

Both methods supply the “target” of the conflict using column inference:

The Insert.on_conflict_do_update.index_elements argument specifies a sequence containing string column names, Column objects, and/or SQL expression elements, which would identify a unique index or unique constraint.

When using Insert.on_conflict_do_update.index_elements to infer an index, a partial index can be inferred by also specifying the Insert.on_conflict_do_update.index_where parameter:

ON CONFLICT...DO UPDATE is used to perform an update of the already existing row, using any combination of new values as well as values from the proposed insertion. These values are specified using the Insert.on_conflict_do_update.set_ parameter. This parameter accepts a dictionary which consists of direct values for UPDATE:

The Insert.on_conflict_do_update() method does not take into account Python-side default UPDATE values or generation functions, e.g. those specified using Column.onupdate. These values will not be exercised for an ON CONFLICT style of UPDATE, unless they are manually specified in the Insert.on_conflict_do_update.set_ dictionary.

In order to refer to the proposed insertion row, the special alias Insert.excluded is available as an attribute on the Insert object; this object creates an “excluded.” prefix on a column, that informs the DO UPDATE to update the row with the value that would have been inserted had the constraint not failed:

The Insert.on_conflict_do_update() method also accepts a WHERE clause using the Insert.on_conflict_do_update.where parameter, which will limit those rows which receive an UPDATE:

ON CONFLICT may be used to skip inserting a row entirely if any conflict with a unique constraint occurs; below this is illustrated using the Insert.on_conflict_do_nothing() method:

If DO NOTHING is used without specifying any columns or constraint, it has the effect of skipping the INSERT for any unique violation which occurs:

SQLite types are unlike those of most other database backends, in that the string name of the type usually does not correspond to a “type” in a one-to-one fashion. Instead, SQLite links per-column typing behavior to one of five so-called “type affinities” based on a string matching pattern for the type.

SQLAlchemy’s reflection process, when inspecting types, uses a simple lookup table to link the keywords returned to provided SQLAlchemy types. This lookup table is present within the SQLite dialect as it is for all other dialects. However, the SQLite dialect has a different “fallback” routine for when a particular type name is not located in the lookup map; it instead implements the SQLite “type affinity” scheme located at https://www.sqlite.org/datatype3.html section 2.1.

The provided typemap will make direct associations from an exact string name match for the following types:

BIGINT, BLOB, BOOLEAN, BOOLEAN, CHAR, DATE, DATETIME, FLOAT, DECIMAL, FLOAT, INTEGER, INTEGER, NUMERIC, REAL, SMALLINT, TEXT, TIME, TIMESTAMP, VARCHAR, NVARCHAR, NCHAR

When a type name does not match one of the above types, the “type affinity” lookup is used instead:

INTEGER is returned if the type name includes the string INT

TEXT is returned if the type name includes the string CHAR, CLOB or TEXT

NullType is returned if the type name includes the string BLOB

REAL is returned if the type name includes the string REAL, FLOA or DOUB.

Otherwise, the NUMERIC type is used.

A partial index, e.g. one which uses a WHERE clause, can be specified with the DDL system using the argument sqlite_where:

The index will be rendered at create time as:

Using table or column names that explicitly have periods in them is not recommended. While this is generally a bad idea for relational databases in general, as the dot is a syntactically significant character, the SQLite driver up until version 3.10.0 of SQLite has a bug which requires that SQLAlchemy filter out these dots in result sets.

The bug, entirely outside of SQLAlchemy, can be illustrated thusly:

The second assertion fails:

Where above, the driver incorrectly reports the names of the columns including the name of the table, which is entirely inconsistent vs. when the UNION is not present.

SQLAlchemy relies upon column names being predictable in how they match to the original statement, so the SQLAlchemy dialect has no choice but to filter these out:

Note that above, even though SQLAlchemy filters out the dots, both names are still addressable:

Therefore, the workaround applied by SQLAlchemy only impacts CursorResult.keys() and Row.keys() in the public API. In the very specific case where an application is forced to use column names that contain dots, and the functionality of CursorResult.keys() and Row.keys() is required to return these dotted names unmodified, the sqlite_raw_colnames execution option may be provided, either on a per-Connection basis:

or on a per-Engine basis:

When using the per-Engine execution option, note that Core and ORM queries that use UNION may not function properly.

One option for CREATE TABLE is supported directly by the SQLite dialect in conjunction with the Table construct:

Added in version 2.0.37.

SQLite CREATE TABLE options

Reflection methods that return lists of tables will omit so-called “SQLite internal schema object” names, which are considered by SQLite as any object name that is prefixed with sqlite_. An example of such an object is the sqlite_sequence table that’s generated when the AUTOINCREMENT column parameter is used. In order to return these objects, the parameter sqlite_include_internal=True may be passed to methods such as MetaData.reflect() or Inspector.get_table_names().

Added in version 2.0: Added the sqlite_include_internal=True parameter. Previously, these tables were not ignored by SQLAlchemy reflection methods.

The sqlite_include_internal parameter does not refer to the “system” tables that are present in schemas such as sqlite_master.

SQLite Internal Schema Objects - in the SQLite documentation.

As with all SQLAlchemy dialects, all UPPERCASE types that are known to be valid with SQLite are importable from the top level dialect, whether they originate from sqlalchemy.types or from the local dialect:

Represent a Python date object in SQLite using a string.

Represent a Python datetime object in SQLite using a string.

Represent a Python time object in SQLite using a string.

inherits from sqlalchemy.dialects.sqlite.base._DateTimeMixin, sqlalchemy.types.DateTime

Represent a Python datetime object in SQLite using a string.

The default string storage format is:

The incoming storage format is by default parsed using the Python datetime.fromisoformat() function.

Changed in version 2.0: datetime.fromisoformat() is used for default datetime string parsing.

The storage format can be customized to some degree using the storage_format and regexp parameters, such as:

truncate_microseconds¶ – when True microseconds will be truncated from the datetime. Can’t be specified together with storage_format or regexp.

storage_format¶ – format string which will be applied to the dict with keys year, month, day, hour, minute, second, and microsecond.

regexp¶ – regular expression which will be applied to incoming result rows, replacing the use of datetime.fromisoformat() to parse incoming strings. If the regexp contains named groups, the resulting match dict is applied to the Python datetime() constructor as keyword arguments. Otherwise, if positional groups are used, the datetime() constructor is called with positional arguments via *map(int, match_obj.groups(0)).

inherits from sqlalchemy.dialects.sqlite.base._DateTimeMixin, sqlalchemy.types.Date

Represent a Python date object in SQLite using a string.

The default string storage format is:

The incoming storage format is by default parsed using the Python date.fromisoformat() function.

Changed in version 2.0: date.fromisoformat() is used for default date string parsing.

The storage format can be customized to some degree using the storage_format and regexp parameters, such as:

storage_format¶ – format string which will be applied to the dict with keys year, month, and day.

regexp¶ – regular expression which will be applied to incoming result rows, replacing the use of date.fromisoformat() to parse incoming strings. If the regexp contains named groups, the resulting match dict is applied to the Python date() constructor as keyword arguments. Otherwise, if positional groups are used, the date() constructor is called with positional arguments via *map(int, match_obj.groups(0)).

inherits from sqlalchemy.types.JSON

SQLite supports JSON as of version 3.9 through its JSON1 extension. Note that JSON1 is a loadable extension and as such may not be available, or may require run-time loading.

JSON is used automatically whenever the base JSON datatype is used against a SQLite backend.

JSON - main documentation for the generic cross-platform JSON datatype.

The JSON type supports persistence of JSON values as well as the core index operations provided by JSON datatype, by adapting the operations to render the JSON_EXTRACT function wrapped in the JSON_QUOTE function at the database level. Extracted values are quoted in order to ensure that the results are always JSON string values.

Added in version 1.3.

Construct a JSON type.

inherited from the sqlalchemy.types.JSON.__init__ method of JSON

Construct a JSON type.

none_as_null=False¶ –

if True, persist the value None as a SQL NULL value, not the JSON encoding of null. Note that when this flag is False, the null() construct can still be used to persist a NULL value, which may be passed directly as a parameter value that is specially interpreted by the JSON type as SQL NULL:

JSON.none_as_null does not apply to the values passed to Column.default and Column.server_default; a value of None passed for these parameters means “no default present”.

Additionally, when used in SQL comparison expressions, the Python value None continues to refer to SQL null, and not JSON NULL. The JSON.none_as_null flag refers explicitly to the persistence of the value within an INSERT or UPDATE statement. The JSON.NULL value should be used for SQL expressions that wish to compare to JSON null.

inherits from sqlalchemy.dialects.sqlite.base._DateTimeMixin, sqlalchemy.types.Time

Represent a Python time object in SQLite using a string.

The default string storage format is:

The incoming storage format is by default parsed using the Python time.fromisoformat() function.

Changed in version 2.0: time.fromisoformat() is used for default time string parsing.

The storage format can be customized to some degree using the storage_format and regexp parameters, such as:

truncate_microseconds¶ – when True microseconds will be truncated from the time. Can’t be specified together with storage_format or regexp.

storage_format¶ – format string which will be applied to the dict with keys hour, minute, second, and microsecond.

regexp¶ – regular expression which will be applied to incoming result rows, replacing the use of datetime.fromisoformat() to parse incoming strings. If the regexp contains named groups, the resulting match dict is applied to the Python time() constructor as keyword arguments. Otherwise, if positional groups are used, the time() constructor is called with positional arguments via *map(int, match_obj.groups(0)).

Construct a sqlite-specific variant Insert construct.

SQLite-specific implementation of INSERT.

Construct a sqlite-specific variant Insert construct.

The sqlalchemy.dialects.sqlite.insert() function creates a sqlalchemy.dialects.sqlite.Insert. This class is based on the dialect-agnostic Insert construct which may be constructed using the insert() function in SQLAlchemy Core.

The Insert construct includes additional methods Insert.on_conflict_do_update(), Insert.on_conflict_do_nothing().

inherits from sqlalchemy.sql.expression.Insert

SQLite-specific implementation of INSERT.

Adds methods for SQLite-specific syntaxes such as ON CONFLICT.

The Insert object is created using the sqlalchemy.dialects.sqlite.insert() function.

Added in version 1.4.

INSERT…ON CONFLICT (Upsert)

Provide the excluded namespace for an ON CONFLICT statement

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

on_conflict_do_nothing()

Specifies a DO NOTHING action for ON CONFLICT clause.

on_conflict_do_update()

Specifies a DO UPDATE SET action for ON CONFLICT clause.

Provide the excluded namespace for an ON CONFLICT statement

SQLite’s ON CONFLICT clause allows reference to the row that would be inserted, known as excluded. This attribute provides all columns in this row to be referenceable.

The Insert.excluded attribute is an instance of ColumnCollection, which provides an interface the same as that of the Table.c collection described at Accessing Tables and Columns. With this collection, ordinary names are accessible like attributes (e.g. stmt.excluded.some_column), but special names and dictionary method names should be accessed using indexed access, such as stmt.excluded["column name"] or stmt.excluded["values"]. See the docstring for ColumnCollection for further examples.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

Specifies a DO NOTHING action for ON CONFLICT clause.

index_elements¶ – A sequence consisting of string column names, Column objects, or other column expression objects that will be used to infer a target index or unique constraint.

index_where¶ – Additional WHERE criterion that can be used to infer a conditional target index.

Specifies a DO UPDATE SET action for ON CONFLICT clause.

index_elements¶ – A sequence consisting of string column names, Column objects, or other column expression objects that will be used to infer a target index or unique constraint.

index_where¶ – Additional WHERE criterion that can be used to infer a conditional target index.

A dictionary or other mapping object where the keys are either names of columns in the target table, or Column objects or other ORM-mapped columns matching that of the target table, and expressions or literals as values, specifying the SET actions to take.

Added in version 1.4: The Insert.on_conflict_do_update.set_ parameter supports Column objects from the target Table as keys.

This dictionary does not take into account Python-specified default UPDATE values or generation functions, e.g. those specified using Column.onupdate. These values will not be exercised for an ON CONFLICT style of UPDATE, unless they are manually specified in the Insert.on_conflict_do_update.set_ dictionary.

where¶ – Optional argument. An expression object representing a WHERE clause that restricts the rows affected by DO UPDATE SET. Rows not meeting the WHERE condition will not be updated (effectively a DO NOTHING for those rows).

Support for the SQLite database via the pysqlite driver.

Note that pysqlite is the same driver as the sqlite3 module included with the Python distribution.

Documentation and download information (if applicable) for pysqlite is available at: https://docs.python.org/library/sqlite3.html

The sqlite3 Python DBAPI is standard on all modern Python versions; for cPython and Pypy, no additional installation is necessary.

The file specification for the SQLite database is taken as the “database” portion of the URL. Note that the format of a SQLAlchemy url is:

This means that the actual filename to be used starts with the characters to the right of the third slash. So connecting to a relative filepath looks like:

An absolute path, which is denoted by starting with a slash, means you need four slashes:

To use a Windows path, regular drive specifications and backslashes can be used. Double backslashes are probably needed:

To use sqlite :memory: database specify it as the filename using sqlite:///:memory:. It’s also the default if no filepath is present, specifying only sqlite:// and nothing else:

Modern versions of SQLite support an alternative system of connecting using a driver level URI, which has the advantage that additional driver-level arguments can be passed including options such as “read only”. The Python sqlite3 driver supports this mode under modern Python 3 versions. The SQLAlchemy pysqlite driver supports this mode of use by specifying “uri=true” in the URL query string. The SQLite-level “URI” is kept as the “database” portion of the SQLAlchemy url (that is, following a slash):

The “uri=true” parameter must appear in the query string of the URL. It will not currently work as expected if it is only present in the create_engine.connect_args parameter dictionary.

The logic reconciles the simultaneous presence of SQLAlchemy’s query string and SQLite’s query string by separating out the parameters that belong to the Python sqlite3 driver vs. those that belong to the SQLite URI. This is achieved through the use of a fixed list of parameters known to be accepted by the Python side of the driver. For example, to include a URL that indicates the Python sqlite3 “timeout” and “check_same_thread” parameters, along with the SQLite “mode” and “nolock” parameters, they can all be passed together on the query string:

Above, the pysqlite / sqlite3 DBAPI would be passed arguments as:

Regarding future parameters added to either the Python or native drivers. new parameter names added to the SQLite URI scheme should be automatically accommodated by this scheme. New parameter names added to the Python driver side can be accommodated by specifying them in the create_engine.connect_args dictionary, until dialect support is added by SQLAlchemy. For the less likely case that the native SQLite driver adds a new parameter name that overlaps with one of the existing, known Python driver parameters (such as “timeout” perhaps), SQLAlchemy’s dialect would require adjustment for the URL scheme to continue to support this.

As is always the case for all SQLAlchemy dialects, the entire “URL” process can be bypassed in create_engine() through the use of the create_engine.creator parameter which allows for a custom callable that creates a Python sqlite3 driver level connection directly.

Added in version 1.3.9.

Uniform Resource Identifiers - in the SQLite documentation

Added in version 1.4.

Support for the ColumnOperators.regexp_match() operator is provided using Python’s re.search function. SQLite itself does not include a working regular expression operator; instead, it includes a non-implemented placeholder operator REGEXP that calls a user-defined function that must be provided.

SQLAlchemy’s implementation makes use of the pysqlite create_function hook as follows:

There is currently no support for regular expression flags as a separate argument, as these are not supported by SQLite’s REGEXP operator, however these may be included inline within the regular expression string. See Python regular expressions for details.

Python regular expressions: Documentation for Python’s regular expression syntax.

The pysqlite driver includes the sqlite3.PARSE_DECLTYPES and sqlite3.PARSE_COLNAMES options, which have the effect of any column or expression explicitly cast as “date” or “timestamp” will be converted to a Python date or datetime object. The date and datetime types provided with the pysqlite dialect are not currently compatible with these options, since they render the ISO date/datetime including microseconds, which pysqlite’s driver does not. Additionally, SQLAlchemy does not at this time automatically render the “cast” syntax required for the freestanding functions “current_timestamp” and “current_date” to return datetime/date types natively. Unfortunately, pysqlite does not provide the standard DBAPI types in cursor.description, leaving SQLAlchemy with no way to detect these types on the fly without expensive per-row type checks.

Keeping in mind that pysqlite’s parsing option is not recommended, nor should be necessary, for use with SQLAlchemy, usage of PARSE_DECLTYPES can be forced if one configures “native_datetime=True” on create_engine():

With this flag enabled, the DATE and TIMESTAMP types (but note - not the DATETIME or TIME types…confused yet ?) will not perform any bind parameter or result processing. Execution of “func.current_date()” will return a string. “func.current_timestamp()” is registered as returning a DATETIME type in SQLAlchemy, so this function still receives SQLAlchemy-level result processing.

The sqlite3 DBAPI by default prohibits the use of a particular connection in a thread which is not the one in which it was created. As SQLite has matured, it’s behavior under multiple threads has improved, and even includes options for memory only databases to be used in multiple threads.

The thread prohibition is known as “check same thread” and may be controlled using the sqlite3 parameter check_same_thread, which will disable or enable this check. SQLAlchemy’s default behavior here is to set check_same_thread to False automatically whenever a file-based database is in use, to establish compatibility with the default pool class QueuePool.

The SQLAlchemy pysqlite DBAPI establishes the connection pool differently based on the kind of SQLite database that’s requested:

When a :memory: SQLite database is specified, the dialect by default will use SingletonThreadPool. This pool maintains a single connection per thread, so that all access to the engine within the current thread use the same :memory: database - other threads would access a different :memory: database. The check_same_thread parameter defaults to True.

When a file-based database is specified, the dialect will use QueuePool as the source of connections. at the same time, the check_same_thread flag is set to False by default unless overridden.

Changed in version 2.0: SQLite file database engines now use QueuePool by default. Previously, NullPool were used. The NullPool class may be used by specifying it via the create_engine.poolclass parameter.

Pooling may be disabled for a file based database by specifying the NullPool implementation for the poolclass() parameter:

It’s been observed that the NullPool implementation incurs an extremely small performance overhead for repeated checkouts due to the lack of connection reuse implemented by QueuePool. However, it still may be beneficial to use this class if the application is experiencing issues with files being locked.

To use a :memory: database in a multithreaded scenario, the same connection object must be shared among threads, since the database exists only within the scope of that connection. The StaticPool implementation will maintain a single connection globally, and the check_same_thread flag can be passed to Pysqlite as False:

Note that using a :memory: database in multiple threads requires a recent version of SQLite.

Due to the way SQLite deals with temporary tables, if you wish to use a temporary table in a file-based SQLite database across multiple checkouts from the connection pool, such as when using an ORM Session where the temporary table should continue to remain after Session.commit() or Session.rollback() is called, a pool which maintains a single connection must be used. Use SingletonThreadPool if the scope is only needed within the current thread, or StaticPool is scope is needed within multiple threads for this case:

Note that SingletonThreadPool should be configured for the number of threads that are to be used; beyond that number, connections will be closed out in a non deterministic way.

The SQLite database is weakly typed, and as such it is possible when using binary values, which in Python are represented as b'some string', that a particular SQLite database can have data values within different rows where some of them will be returned as a b'' value by the Pysqlite driver, and others will be returned as Python strings, e.g. '' values. This situation is not known to occur if the SQLAlchemy LargeBinary datatype is used consistently, however if a particular SQLite database has data that was inserted using the Pysqlite driver directly, or when using the SQLAlchemy String type which was later changed to LargeBinary, the table will not be consistently readable because SQLAlchemy’s LargeBinary datatype does not handle strings so it has no way of “encoding” a value that is in string format.

To deal with a SQLite table that has mixed string / binary data in the same column, use a custom type that will check each row individually:

Then use the above MixedBinary datatype in the place where LargeBinary would normally be used.

A newly revised version of this important section is now available at the top level of the SQLAlchemy SQLite documentation, in the section Transactions with SQLite and the sqlite3 driver.

pysqlite supports a create_function() method that allows us to create our own user-defined functions (UDFs) in Python and use them directly in SQLite queries. These functions are registered with a specific DBAPI Connection.

SQLAlchemy uses connection pooling with file-based SQLite databases, so we need to ensure that the UDF is attached to the connection when it is created. That is accomplished with an event listener:

Support for the SQLite database via the aiosqlite driver.

Documentation and download information (if applicable) for aiosqlite is available at: https://pypi.org/project/aiosqlite/

The aiosqlite dialect provides support for the SQLAlchemy asyncio interface running on top of pysqlite.

aiosqlite is a wrapper around pysqlite that uses a background thread for each connection. It does not actually use non-blocking IO, as SQLite databases are not socket-based. However it does provide a working asyncio interface that’s useful for testing and prototyping purposes.

Using a special asyncio mediation layer, the aiosqlite dialect is usable as the backend for the SQLAlchemy asyncio extension package.

This dialect should normally be used only with the create_async_engine() engine creation function:

The URL passes through all arguments to the pysqlite driver, so all connection arguments are the same as they are for that of Pysqlite.

aiosqlite extends pysqlite to support async, so we can create our own user-defined functions (UDFs) in Python and use them directly in SQLite queries as described here: User-Defined Functions.

A newly revised version of this important section is now available at the top level of the SQLAlchemy SQLite documentation, in the section Transactions with SQLite and the sqlite3 driver.

The SQLAlchemy aiosqlite DBAPI establishes the connection pool differently based on the kind of SQLite database that’s requested:

When a :memory: SQLite database is specified, the dialect by default will use StaticPool. This pool maintains a single connection, so that all access to the engine use the same :memory: database.

When a file-based database is specified, the dialect will use AsyncAdaptedQueuePool as the source of connections.

Changed in version 2.0.38: SQLite file database engines now use AsyncAdaptedQueuePool by default. Previously, NullPool were used. The NullPool class may be used by specifying it via the create_engine.poolclass parameter.

Support for the SQLite database via the pysqlcipher driver.

Dialect for support of DBAPIs that make use of the SQLCipher backend.

Current dialect selection logic is:

If the create_engine.module parameter supplies a DBAPI module, that module is used.

Otherwise for Python 3, choose https://pypi.org/project/sqlcipher3/

If not available, fall back to https://pypi.org/project/pysqlcipher3/

For Python 2, https://pypi.org/project/pysqlcipher/ is used.

The pysqlcipher3 and pysqlcipher DBAPI drivers are no longer maintained; the sqlcipher3 driver as of this writing appears to be current. For future compatibility, any pysqlcipher-compatible DBAPI may be used as follows:

These drivers make use of the SQLCipher engine. This system essentially introduces new PRAGMA commands to SQLite which allows the setting of a passphrase and other encryption parameters, allowing the database file to be encrypted.

The format of the connect string is in every way the same as that of the pysqlite driver, except that the “password” field is now accepted, which should contain a passphrase:

For an absolute file path, two leading slashes should be used for the database name:

A selection of additional encryption-related pragmas supported by SQLCipher as documented at https://www.zetetic.net/sqlcipher/sqlcipher-api/ can be passed in the query string, and will result in that PRAGMA being called for each new connection. Currently, cipher, kdf_iter cipher_page_size and cipher_use_hmac are supported:

Previous versions of sqlalchemy did not take into consideration the encryption-related pragmas passed in the url string, that were silently ignored. This may cause errors when opening files saved by a previous sqlalchemy version if the encryption options do not match.

The driver makes a change to the default pool behavior of pysqlite as described in Threading/Pooling Behavior. The pysqlcipher driver has been observed to be significantly slower on connection than the pysqlite driver, most likely due to the encryption overhead, so the dialect here defaults to using the SingletonThreadPool implementation, instead of the NullPool pool used by pysqlite. As always, the pool implementation is entirely configurable using the create_engine.poolclass parameter; the StaticPool may be more feasible for single-threaded use, or NullPool may be used to prevent unencrypted connections from being held open for long periods of time, at the expense of slower startup time for new connections.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (unknown):
```unknown
Table(
    "sometable",
    metadata,
    Column("id", Integer, primary_key=True),
    sqlite_autoincrement=True,
)
```

Example 2 (unknown):
```unknown
table = Table(
    "my_table",
    metadata,
    Column(
        "id",
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
    ),
)
```

Example 3 (python):
```python
from sqlalchemy import BigInteger
from sqlalchemy.ext.compiler import compiles


class SLBigInteger(BigInteger):
    pass


@compiles(SLBigInteger, "sqlite")
def bi_c(element, compiler, **kw):
    return "INTEGER"


@compiles(SLBigInteger)
def bi_c(element, compiler, **kw):
    return compiler.visit_BIGINT(element, **kw)


table = Table(
    "my_table", metadata, Column("id", SLBigInteger(), primary_key=True)
)
```

Example 4 (python):
```python
from sqlalchemy import create_engine

engine = create_engine(
    "sqlite:///myfile.db", connect_args={"autocommit": False}
)
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/dialects/oracle.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - Dialects
    - Project Versions
- Oracle¶
- DBAPI Support¶
- Auto Increment Behavior¶
  - Specifying GENERATED AS IDENTITY (Oracle Database 12 and above)¶
  - Using a SEQUENCE (all Oracle Database versions)¶
- Transaction Isolation Level / Autocommit¶

Home | Download this Documentation

Home | Download this Documentation

Support for the Oracle Database database.

The following table summarizes current support levels for database release versions.

The following dialect/DBAPI options are available. Please refer to individual DBAPI sections for connect information.

SQLAlchemy Table objects which include integer primary keys are usually assumed to have “autoincrementing” behavior, meaning they can generate their own primary key values upon INSERT. For use within Oracle Database, two options are available, which are the use of IDENTITY columns (Oracle Database 12 and above only) or the association of a SEQUENCE with the column.

Starting from version 12, Oracle Database can make use of identity columns using the Identity to specify the autoincrementing behavior:

The CREATE TABLE for the above Table object would be:

The Identity object support many options to control the “autoincrementing” behavior of the column, like the starting value, the incrementing value, etc. In addition to the standard options, Oracle Database supports setting Identity.always to None to use the default generated mode, rendering GENERATED AS IDENTITY in the DDL. It also supports setting Identity.on_null to True to specify ON NULL in conjunction with a ‘BY DEFAULT’ identity column.

Older version of Oracle Database had no “autoincrement” feature: SQLAlchemy relies upon sequences to produce these values. With the older Oracle Database versions, a sequence must always be explicitly specified to enable autoincrement. This is divergent with the majority of documentation examples which assume the usage of an autoincrement-capable database. To specify sequences, use the sqlalchemy.schema.Sequence object which is passed to a Column construct:

This step is also required when using table reflection, i.e. autoload_with=engine:

Changed in version 1.4: Added Identity construct in a Column to specify the option of an autoincrementing column.

Oracle Database supports “READ COMMITTED” and “SERIALIZABLE” modes of isolation. The AUTOCOMMIT isolation level is also supported by the python-oracledb and cx_Oracle dialects.

To set using per-connection execution options:

For READ COMMITTED and SERIALIZABLE, the Oracle Database dialects sets the level at the session level using ALTER SESSION, which is reverted back to its default setting when the connection is returned to the connection pool.

Valid values for isolation_level include:

The implementation for the Connection.get_isolation_level() method as implemented by the Oracle Database dialects necessarily force the start of a transaction using the Oracle Database DBMS_TRANSACTION.LOCAL_TRANSACTION_ID function; otherwise no level is normally readable.

Additionally, the Connection.get_isolation_level() method will raise an exception if the v$transaction view is not available due to permissions or other reasons, which is a common occurrence in Oracle Database installations.

The python-oracledb and cx_Oracle dialects attempt to call the Connection.get_isolation_level() method when the dialect makes its first connection to the database in order to acquire the “default”isolation level. This default level is necessary so that the level can be reset on a connection after it has been temporarily modified using Connection.execution_options() method. In the common event that the Connection.get_isolation_level() method raises an exception due to v$transaction not being readable as well as any other database-related failure, the level is assumed to be “READ COMMITTED”. No warning is emitted for this initial first-connect condition as it is expected to be a common restriction on Oracle databases.

Added in version 1.3.16: added support for AUTOCOMMIT to the cx_Oracle dialect as well as the notion of a default isolation level

Added in version 1.3.21: Added support for SERIALIZABLE as well as live reading of the isolation level.

Changed in version 1.3.22: In the event that the default isolation level cannot be read due to permissions on the v$transaction view as is common in Oracle installations, the default isolation level is hardcoded to “READ COMMITTED” which was the behavior prior to 1.3.21.

Setting Transaction Isolation Levels including DBAPI Autocommit

In Oracle Database, the data dictionary represents all case insensitive identifier names using UPPERCASE text. This is in contradiction to the expectations of SQLAlchemy, which assume a case insensitive name is represented as lowercase text.

As an example of case insensitive identifier names, consider the following table:

If you were to ask Oracle Database for information about this table, the table name would be reported as MYTABLE and the column name would be reported as IDENTIFIER. Compare to most other databases such as PostgreSQL and MySQL which would report these names as mytable and identifier. The names are not quoted, therefore are case insensitive. The special casing of MyTable and Identifier would only be maintained if they were quoted in the table definition:

When constructing a SQLAlchemy Table object, an all lowercase name is considered to be case insensitive. So the following table assumes case insensitive names:

Whereas when mixed case or UPPERCASE names are used, case sensitivity is assumed:

A similar situation occurs at the database driver level when emitting a textual SQL SELECT statement and looking at column names in the DBAPI cursor.description attribute. A database like PostgreSQL will normalize case insensitive names to be lowercase:

Whereas Oracle normalizes them to UPPERCASE:

In order to achieve cross-database parity for the two cases of a. table reflection and b. textual-only SQL statement round trips, SQLAlchemy performs a step called name normalization when using the Oracle dialect. This process may also apply to other third party dialects that have similar UPPERCASE handling of case insensitive names.

When using name normalization, SQLAlchemy attempts to detect if a name is case insensitive by checking if all characters are UPPERCASE letters only; if so, then it assumes this is a case insensitive name and is delivered as a lowercase name.

For table reflection, a tablename that is seen represented as all UPPERCASE in Oracle Database’s catalog tables will be assumed to have a case insensitive name. This is what allows the Table definition to use lower case names and be equally compatible from a reflection point of view on Oracle Database and all other databases such as PostgreSQL and MySQL:

Above, the all lowercase name "mytable" is case insensitive; it will match a table reported by PostgreSQL as "mytable" and a table reported by Oracle as "MYTABLE". If name normalization were not present, it would not be possible for the above Table definition to be introspectable in a cross-database way, since we are dealing with a case insensitive name that is not reported by each database in the same way.

Case sensitivity can be forced on in this case, such as if we wanted to represent the quoted tablename "MYTABLE" with that exact casing, most simply by using that casing directly, which will be seen as a case sensitive name:

For the unusual case of a quoted all-lowercase name, the quoted_name construct may be used:

Name normalization also takes place when handling result sets from purely textual SQL strings, that have no other Table or Column metadata associated with them. This includes SQL strings executed using Connection.exec_driver_sql() and SQL strings executed using the text() construct which do not include Column metadata.

Returning to the Oracle Database SELECT statement, we see that even though cursor.description reports the column name as SOMENAME, SQLAlchemy name normalizes this to somename:

The single scenario where the above behavior produces inaccurate results is when using an all-uppercase, quoted name. SQLAlchemy has no way to determine that a particular name in cursor.description was quoted, and is therefore case sensitive, or was not quoted, and should be name normalized:

For this case, a new feature will be available in SQLAlchemy 2.1 to disable the name normalization behavior in specific cases.

SQLAlchemy is sensitive to the maximum identifier length supported by Oracle Database. This affects generated SQL label names as well as the generation of constraint names, particularly in the case where the constraint naming convention feature described at Configuring Constraint Naming Conventions is being used.

Oracle Database 12.2 increased the default maximum identifier length from 30 to 128. As of SQLAlchemy 1.4, the default maximum identifier length for the Oracle dialects is 128 characters. Upon first connection, the maximum length actually supported by the database is obtained. In all cases, setting the create_engine.max_identifier_length parameter will bypass this change and the value given will be used as is:

If create_engine.max_identifier_length is not set, the oracledb dialect internally uses the max_identifier_length attribute available on driver connections since python-oracledb version 2.5. When using an older driver version, or using the cx_Oracle dialect, SQLAlchemy will instead attempt to use the query SELECT value FROM v$parameter WHERE name = 'compatible' upon first connect in order to determine the effective compatibility version of the database. The “compatibility” version is a version number that is independent of the actual database version. It is used to assist database migration. It is configured by an Oracle Database initialization parameter. The compatibility version then determines the maximum allowed identifier length for the database. If the V$ view is not available, the database version information is used instead.

The maximum identifier length comes into play both when generating anonymized SQL labels in SELECT statements, but more crucially when generating constraint names from a naming convention. It is this area that has created the need for SQLAlchemy to change this default conservatively. For example, the following naming convention produces two very different constraint names based on the identifier length:

With an identifier length of 30, the above CREATE INDEX looks like:

However with length of 128, it becomes:

CREATE INDEX ix_some_column_name_1some_column_name_2some_column_name_3 ON t (some_column_name_1, some_column_name_2, some_column_name_3)

Applications which have run versions of SQLAlchemy prior to 1.4 on Oracle Database version 12.2 or greater are therefore subject to the scenario of a database migration that wishes to “DROP CONSTRAINT” on a name that was previously generated with the shorter length. This migration will fail when the identifier length is changed without the name of the index or constraint first being adjusted. Such applications are strongly advised to make use of create_engine.max_identifier_length in order to maintain control of the generation of truncated names, and to fully review and test all database migrations in a staging environment when changing this value to ensure that the impact of this change has been mitigated.

Changed in version 1.4: the default max_identifier_length for Oracle Database is 128 characters, which is adjusted down to 30 upon first connect if the Oracle Database, or its compatibility setting, are lower than version 12.2.

Methods like Select.limit() and Select.offset() make use of FETCH FIRST N ROW / OFFSET N ROWS syntax assuming Oracle Database 12c or above, and assuming the SELECT statement is not embedded within a compound statement like UNION. This syntax is also available directly by using the Select.fetch() method.

Changed in version 2.0: the Oracle Database dialects now use FETCH FIRST N ROW / OFFSET N ROWS for all Select.limit() and Select.offset() usage including within the ORM and legacy Query. To force the legacy behavior using window functions, specify the enable_offset_fetch=False dialect parameter to create_engine().

The use of FETCH FIRST / OFFSET may be disabled on any Oracle Database version by passing enable_offset_fetch=False to create_engine(), which will force the use of “legacy” mode that makes use of window functions. This mode is also selected automatically when using a version of Oracle Database prior to 12c.

When using legacy mode, or when a Select statement with limit/offset is embedded in a compound statement, an emulated approach for LIMIT / OFFSET based on window functions is used, which involves creation of a subquery using ROW_NUMBER that is prone to performance issues as well as SQL construction issues for complex statements. However, this approach is supported by all Oracle Database versions. See notes below.

If using Select.limit() and Select.offset(), or with the ORM the Query.limit() and Query.offset() methods on an Oracle Database version prior to 12c, the following notes apply:

SQLAlchemy currently makes use of ROWNUM to achieve LIMIT/OFFSET; the exact methodology is taken from https://blogs.oracle.com/oraclemagazine/on-rownum-and-limiting-results .

the “FIRST_ROWS()” optimization keyword is not used by default. To enable the usage of this optimization directive, specify optimize_limits=True to create_engine().

Changed in version 1.4: The Oracle Database dialect renders limit/offset integer values using a “post compile” scheme which renders the integer directly before passing the statement to the cursor for execution. The use_binds_for_limits flag no longer has an effect.

New “post compile” bound parameters used for LIMIT/OFFSET in Oracle, SQL Server.

Oracle Database supports RETURNING fully for INSERT, UPDATE and DELETE statements that are invoked with a single collection of bound parameters (that is, a cursor.execute() style statement; SQLAlchemy does not generally support RETURNING with executemany statements). Multiple rows may be returned as well.

Changed in version 2.0: the Oracle Database backend has full support for RETURNING on parity with other backends.

Oracle Database doesn’t have native ON UPDATE CASCADE functionality. A trigger based solution is available at https://web.archive.org/web/20090317041251/https://asktom.oracle.com/tkyte/update_cascade/index.html

When using the SQLAlchemy ORM, the ORM has limited ability to manually issue cascading updates - specify ForeignKey objects using the “deferrable=True, initially=’deferred’” keyword arguments, and specify “passive_updates=False” on each relationship().

The status of Oracle Database 8 compatibility is not known for SQLAlchemy 2.0.

When Oracle Database 8 is detected, the dialect internally configures itself to the following behaviors:

the use_ansi flag is set to False. This has the effect of converting all JOIN phrases into the WHERE clause, and in the case of LEFT OUTER JOIN makes use of Oracle’s (+) operator.

the NVARCHAR2 and NCLOB datatypes are no longer generated as DDL when the Unicode is used - VARCHAR2 and CLOB are issued instead. This because these types don’t seem to work correctly on Oracle 8 even though they are available. The NVARCHAR and NCLOB types will always generate NVARCHAR2 and NCLOB.

When using reflection with Table objects, the dialect can optionally search for tables indicated by synonyms, either in local or remote schemas or accessed over DBLINK, by passing the flag oracle_resolve_synonyms=True as a keyword argument to the Table construct:

When this flag is set, the given name (such as some_table above) will be searched not just in the ALL_TABLES view, but also within the ALL_SYNONYMS view to see if this name is actually a synonym to another name. If the synonym is located and refers to a DBLINK, the Oracle Database dialects know how to locate the table’s information using DBLINK syntax(e.g. @dblink).

oracle_resolve_synonyms is accepted wherever reflection arguments are accepted, including methods such as MetaData.reflect() and Inspector.get_columns().

If synonyms are not in use, this flag should be left disabled.

The Oracle Database dialects can return information about foreign key, unique, and CHECK constraints, as well as indexes on tables.

Raw information regarding these constraints can be acquired using Inspector.get_foreign_keys(), Inspector.get_unique_constraints(), Inspector.get_check_constraints(), and Inspector.get_indexes().

Changed in version 1.2: The Oracle Database dialect can now reflect UNIQUE and CHECK constraints.

When using reflection at the Table level, the Table will also include these constraints.

Note the following caveats:

When using the Inspector.get_check_constraints() method, Oracle Database builds a special “IS NOT NULL” constraint for columns that specify “NOT NULL”. This constraint is not returned by default; to include the “IS NOT NULL” constraints, pass the flag include_all=True:

in most cases, when reflecting a Table, a UNIQUE constraint will not be available as a UniqueConstraint object, as Oracle Database mirrors unique constraints with a UNIQUE index in most cases (the exception seems to be when two or more unique constraints represent the same columns); the Table will instead represent these using Index with the unique=True flag set.

Oracle Database creates an implicit index for the primary key of a table; this index is excluded from all index results.

the list of columns reflected for an index will not include column names that start with SYS_NC.

The Inspector.get_table_names() and Inspector.get_temp_table_names() methods each return a list of table names for the current engine. These methods are also part of the reflection which occurs within an operation such as MetaData.reflect(). By default, these operations exclude the SYSTEM and SYSAUX tablespaces from the operation. In order to change this, the default list of tablespaces excluded can be changed at the engine level using the exclude_tablespaces parameter:

The SQLAlchemy Float and Double datatypes are generic datatypes that resolve to the “least surprising” datatype for a given backend. For Oracle Database, this means they resolve to the FLOAT and DOUBLE types:

Oracle’s FLOAT / DOUBLE datatypes are aliases for NUMBER. Oracle Database stores NUMBER values with full precision, not floating point precision, which means that FLOAT / DOUBLE do not actually behave like native FP values. Oracle Database instead offers special datatypes BINARY_FLOAT and BINARY_DOUBLE to deliver real 4- and 8- byte FP values.

SQLAlchemy supports these datatypes directly using BINARY_FLOAT and BINARY_DOUBLE. To use the Float or Double datatypes in a database agnostic way, while allowing Oracle backends to utilize one of these types, use the TypeEngine.with_variant() method to set up a variant:

E.g. to use this datatype in a Table definition:

Oracle Database has no datatype known as DATETIME, it instead has only DATE, which can actually store a date and time value. For this reason, the Oracle Database dialects provide a type DATE which is a subclass of DateTime. This type has no special behavior, and is only present as a “marker” for this type; additionally, when a database column is reflected and the type is reported as DATE, the time-supporting DATE type is used.

The CREATE TABLE phrase supports the following options with Oracle Database dialects in conjunction with the Table construct:

The oracle_compress parameter accepts either an integer compression level, or True to use the default compression level.

The oracle_tablespace parameter specifies the tablespace in which the table is to be created. This is useful when you want to create a table in a tablespace other than the default tablespace of the user.

Added in version 2.0.37.

You can specify the oracle_bitmap parameter to create a bitmap index instead of a B-tree index:

Bitmap indexes cannot be unique and cannot be compressed. SQLAlchemy will not check for such limitations, only the database will.

Oracle Database has a more efficient storage mode for indexes containing lots of repeated values. Use the oracle_compress parameter to turn on key compression:

The oracle_compress parameter accepts either an integer specifying the number of prefix columns to compress, or True to use the default (all columns for non-unique indexes, all but the last column for unique indexes).

Oracle Database 23ai introduced a new VECTOR datatype for artificial intelligence and machine learning search operations. The VECTOR datatype is a homogeneous array of 8-bit signed integers, 8-bit unsigned integers (binary), 32-bit floating-point numbers, or 64-bit floating-point numbers.

A vector’s storage type can be either DENSE or SPARSE. A dense vector contains meaningful values in most or all of its dimensions. In contrast, a sparse vector has non-zero values in only a few dimensions, with the majority being zero.

Sparse vectors are represented by the total number of vector dimensions, an array of indices, and an array of values where each value’s location in the vector is indicated by the corresponding indices array position. All other vector values are treated as zero.

The storage formats that can be used with sparse vectors are float32, float64, and int8. Note that the binary storage format cannot be used with sparse vectors.

Sparse vectors are supported when you are using Oracle Database 23.7 or later.

Using VECTOR Data - in the documentation for the python-oracledb driver.

Added in version 2.0.41: - Added VECTOR datatype

Added in version 2.0.43: - Added DENSE/SPARSE support

With the VECTOR datatype, you can specify the number of dimensions, the storage format, and the storage type for the data. Valid values for the storage format are enum members of VectorStorageFormat. Valid values for the storage type are enum members of VectorStorageType. If storage type is not specified, a DENSE vector is created by default.

To create a table that includes a VECTOR column:

Vectors can also be defined with an arbitrary number of dimensions and formats. This allows you to specify vectors of different dimensions with the various storage formats mentioned below.

In this case, the storage format is flexible, allowing any vector type data to be inserted, such as INT8 or BINARY etc:

The dimension is flexible in this case, meaning that any dimension vector can be used:

Both the dimensions and the storage format are flexible. It creates a DENSE vector:

To create a SPARSE vector with both dimensions and the storage format as flexible, use the VectorStorageType.SPARSE storage type:

VECTOR data can be inserted using Python list or Python array.array() objects. Python arrays of type FLOAT (32-bit), DOUBLE (64-bit), INT (8-bit signed integers), or BINARY (8-bit unsigned integers) are used as bind values when inserting VECTOR columns:

Data can be inserted into a sparse vector using the SparseVector class, creating an object consisting of the number of dimensions, an array of indices, and a corresponding array of values:

The VECTOR feature supports an Oracle-specific parameter oracle_vector on the Index construct, which allows the construction of VECTOR indexes.

SPARSE vectors cannot be used in the creation of vector indexes.

To utilize VECTOR indexing, set the oracle_vector parameter to True to use the default values provided by Oracle. HNSW is the default indexing method:

The full range of parameters for vector indexes are available by using the VectorIndexConfig dataclass in place of a boolean; this dataclass allows full configuration of the index:

For complete explanation of these parameters, see the Oracle documentation linked below.

CREATE VECTOR INDEX - in the Oracle documentation

When using the VECTOR datatype with a Column or similar ORM mapped construct, additional comparison functions are available, including:

Approximate vector search can only be performed when all syntax and semantic rules are satisfied, the corresponding vector index is available, and the query optimizer determines to perform it. If any of these conditions are unmet, then an approximate search is not performed. In this case the query returns exact results.

To enable approximate searching during similarity searches on VECTORS, the oracle_fetch_approximate parameter may be used with the Select.fetch() clause to add FETCH APPROX to the SELECT statement:

As with all SQLAlchemy dialects, all UPPERCASE types that are known to be valid with Oracle Database are importable from the top level dialect, whether they originate from sqlalchemy.types or from the local dialect:

Added in version 1.2.19: Added NCHAR to the list of datatypes exported by the Oracle dialect.

Types which are specific to Oracle Database, or have Oracle-specific construction arguments, are as follows:

Implement the Oracle BINARY_DOUBLE datatype.

Implement the Oracle BINARY_FLOAT datatype.

Provide the Oracle Database DATE type.

Oracle Database FLOAT.

Oracle Database ROWID type.

Lightweight SQLAlchemy-side version of SparseVector. This mimics oracledb.SparseVector.

Oracle Database implementation of TIMESTAMP, which supports additional Oracle Database-specific modes

Oracle VECTOR datatype.

Enum representing different types of vector distance metrics.

Define the configuration for Oracle VECTOR Index.

Enum representing different types of VECTOR index structures.

Enum representing the data format used to store vector components.

Enum representing the vector type,

inherits from sqlalchemy.types.LargeBinary

Construct a LargeBinary type.

inherited from the sqlalchemy.types.LargeBinary.__init__ method of LargeBinary

Construct a LargeBinary type.

length¶ – optional, a length for the column for use in DDL statements, for those binary types that accept a length, such as the MySQL BLOB type.

inherits from sqlalchemy.types.Double

Implement the Oracle BINARY_DOUBLE datatype.

This datatype differs from the Oracle DOUBLE datatype in that it delivers a true 8-byte FP value. The datatype may be combined with a generic Double datatype using TypeEngine.with_variant().

FLOAT / DOUBLE Support and Behaviors

inherited from the sqlalchemy.types.Float.__init__ method of Float

the numeric precision for use in DDL CREATE TABLE. Backends should attempt to ensure this precision indicates a number of digits for the generic Float datatype.

For the Oracle Database backend, the Float.precision parameter is not accepted when rendering DDL, as Oracle Database does not support float precision specified as a number of decimal places. Instead, use the Oracle Database-specific FLOAT datatype and specify the FLOAT.binary_precision parameter. This is new in version 2.0 of SQLAlchemy.

To create a database agnostic Float that separately specifies binary precision for Oracle Database, use TypeEngine.with_variant() as follows:

asdecimal¶ – the same flag as that of Numeric, but defaults to False. Note that setting this flag to True results in floating point conversion.

decimal_return_scale¶ – Default scale to use when converting from floats to Python decimals. Floating point values will typically be much longer due to decimal inaccuracy, and most floating point database types don’t have a notion of “scale”, so by default the float type looks for the first ten decimal places when converting. Specifying this value will override that length. Note that the MySQL float types, which do include “scale”, will use “scale” as the default for decimal_return_scale, if not otherwise specified.

inherits from sqlalchemy.types.Float

Implement the Oracle BINARY_FLOAT datatype.

This datatype differs from the Oracle FLOAT datatype in that it delivers a true 4-byte FP value. The datatype may be combined with a generic Float datatype using TypeEngine.with_variant().

FLOAT / DOUBLE Support and Behaviors

inherited from the sqlalchemy.types.Float.__init__ method of Float

the numeric precision for use in DDL CREATE TABLE. Backends should attempt to ensure this precision indicates a number of digits for the generic Float datatype.

For the Oracle Database backend, the Float.precision parameter is not accepted when rendering DDL, as Oracle Database does not support float precision specified as a number of decimal places. Instead, use the Oracle Database-specific FLOAT datatype and specify the FLOAT.binary_precision parameter. This is new in version 2.0 of SQLAlchemy.

To create a database agnostic Float that separately specifies binary precision for Oracle Database, use TypeEngine.with_variant() as follows:

asdecimal¶ – the same flag as that of Numeric, but defaults to False. Note that setting this flag to True results in floating point conversion.

decimal_return_scale¶ – Default scale to use when converting from floats to Python decimals. Floating point values will typically be much longer due to decimal inaccuracy, and most floating point database types don’t have a notion of “scale”, so by default the float type looks for the first ten decimal places when converting. Specifying this value will override that length. Note that the MySQL float types, which do include “scale”, will use “scale” as the default for decimal_return_scale, if not otherwise specified.

inherits from sqlalchemy.dialects.oracle.types._OracleDateLiteralRender, sqlalchemy.types.DateTime

Provide the Oracle Database DATE type.

This type has no special Python behavior, except that it subclasses DateTime; this is to suit the fact that the Oracle Database DATE type supports a time value.

Construct a new DateTime.

inherited from the sqlalchemy.types.DateTime.__init__ method of DateTime

Construct a new DateTime.

timezone¶ – boolean. Indicates that the datetime type should enable timezone support, if available on the base date/time-holding type only. It is recommended to make use of the TIMESTAMP datatype directly when using this flag, as some databases include separate generic date/time-holding types distinct from the timezone-capable TIMESTAMP datatype, such as Oracle Database.

inherits from sqlalchemy.types.FLOAT

Oracle Database FLOAT.

This is the same as FLOAT except that an Oracle Database -specific FLOAT.binary_precision parameter is accepted, and the Float.precision parameter is not accepted.

Oracle Database FLOAT types indicate precision in terms of “binary precision”, which defaults to 126. For a REAL type, the value is 63. This parameter does not cleanly map to a specific number of decimal places but is roughly equivalent to the desired number of decimal places divided by 0.3103.

Added in version 2.0.

binary_precision¶ – Oracle Database binary precision value to be rendered in DDL. This may be approximated to the number of decimal characters using the formula “decimal precision = 0.30103 * binary precision”. The default value used by Oracle Database for FLOAT / DOUBLE PRECISION is 126.

asdecimal¶ – See Float.asdecimal

decimal_return_scale¶ – See Float.decimal_return_scale

inherits from sqlalchemy.types.NativeForEmulated, sqlalchemy.types._AbstractInterval

Construct an INTERVAL.

Construct an INTERVAL.

Note that only DAY TO SECOND intervals are currently supported. This is due to a lack of support for YEAR TO MONTH intervals within available DBAPIs.

day_precision¶ – the day precision value. this is the number of digits to store for the day field. Defaults to “2”

second_precision¶ – the second precision value. this is the number of digits to store for the fractional seconds field. Defaults to “6”.

inherits from sqlalchemy.types.Text

Create a string-holding type.

inherited from the sqlalchemy.types.String.__init__ method of String

Create a string-holding type.

length¶ – optional, a length for the column for use in DDL and CAST expressions. May be safely omitted if no CREATE TABLE will be issued. Certain databases may require a length for use in DDL, and will raise an exception when the CREATE TABLE DDL is issued if a VARCHAR with no length is included. Whether the value is interpreted as bytes or characters is database specific.

Optional, a column-level collation for use in DDL and CAST expressions. Renders using the COLLATE keyword supported by SQLite, MySQL, and PostgreSQL. E.g.:

In most cases, the Unicode or UnicodeText datatypes should be used for a Column that expects to store non-ascii data. These datatypes will ensure that the correct types are used on the database.

inherits from sqlalchemy.types.Numeric, sqlalchemy.types.Integer

inherits from sqlalchemy.types.Text

Create a string-holding type.

inherited from the sqlalchemy.types.String.__init__ method of String

Create a string-holding type.

length¶ – optional, a length for the column for use in DDL and CAST expressions. May be safely omitted if no CREATE TABLE will be issued. Certain databases may require a length for use in DDL, and will raise an exception when the CREATE TABLE DDL is issued if a VARCHAR with no length is included. Whether the value is interpreted as bytes or characters is database specific.

Optional, a column-level collation for use in DDL and CAST expressions. Renders using the COLLATE keyword supported by SQLite, MySQL, and PostgreSQL. E.g.:

In most cases, the Unicode or UnicodeText datatypes should be used for a Column that expects to store non-ascii data. These datatypes will ensure that the correct types are used on the database.

inherits from sqlalchemy.types._Binary

inherits from sqlalchemy.types.TypeEngine

Oracle Database ROWID type.

When used in a cast() or similar, generates ROWID.

inherits from sqlalchemy.types.TIMESTAMP

Oracle Database implementation of TIMESTAMP, which supports additional Oracle Database-specific modes

Added in version 2.0.

Construct a new TIMESTAMP.

Construct a new TIMESTAMP.

timezone¶ – boolean. Indicates that the TIMESTAMP type should use Oracle Database’s TIMESTAMP WITH TIME ZONE datatype.

local_timezone¶ – boolean. Indicates that the TIMESTAMP type should use Oracle Database’s TIMESTAMP WITH LOCAL TIME ZONE datatype.

inherits from sqlalchemy.types.TypeEngine

Oracle VECTOR datatype.

For complete background on using this type, see VECTOR Datatype.

Added in version 2.0.41.

dim¶ – integer. The dimension of the VECTOR datatype. This should be an integer value.

storage_format¶ – VectorStorageFormat. The VECTOR storage type format. This should be Enum values form VectorStorageFormat INT8, BINARY, FLOAT32, or FLOAT64.

storage_type¶ – VectorStorageType. The Vector storage type. This should be Enum values from VectorStorageType SPARSE or DENSE.

inherits from enum.Enum

Enum representing different types of VECTOR index structures.

See VECTOR Datatype for background.

Added in version 2.0.41.

The HNSW (Hierarchical Navigable Small World) index type.

The IVF (Inverted File Index) index type

The HNSW (Hierarchical Navigable Small World) index type.

The IVF (Inverted File Index) index type

Define the configuration for Oracle VECTOR Index.

See VECTOR Datatype for background.

Added in version 2.0.41.

index_type¶ – Enum value from VectorIndexType Specifies the indexing method. For HNSW, this must be VectorIndexType.HNSW.

distance¶ – Enum value from VectorDistanceType specifies the metric for calculating distance between VECTORS.

accuracy¶ – integer. Should be in the range 0 to 100 Specifies the accuracy of the nearest neighbor search during query execution.

parallel¶ – integer. Specifies degree of parallelism.

hnsw_neighbors¶ – integer. Should be in the range 0 to 2048. Specifies the number of nearest neighbors considered during the search. The attribute VectorIndexConfig.hnsw_neighbors is HNSW index specific.

hnsw_efconstruction¶ – integer. Should be in the range 0 to 65535. Controls the trade-off between indexing speed and recall quality during index construction. The attribute VectorIndexConfig.hnsw_efconstruction is HNSW index specific.

ivf_neighbor_partitions¶ – integer. Should be in the range 0 to 10,000,000. Specifies the number of partitions used to divide the dataset. The attribute VectorIndexConfig.ivf_neighbor_partitions is IVF index specific.

ivf_sample_per_partition¶ – integer. Should be between 1 and num_vectors / neighbor partitions. Specifies the number of samples used per partition. The attribute VectorIndexConfig.ivf_sample_per_partition is IVF index specific.

ivf_min_vectors_per_partition¶ – integer. From 0 (no trimming) to the total number of vectors (results in 1 partition). Specifies the minimum number of vectors per partition. The attribute VectorIndexConfig.ivf_min_vectors_per_partition is IVF index specific.

ivf_min_vectors_per_partition

ivf_neighbor_partitions

ivf_sample_per_partition

inherits from enum.Enum

Enum representing the data format used to store vector components.

See VECTOR Datatype for background.

Added in version 2.0.41.

32-bit floating-point format.

64-bit floating-point format.

8-bit integer format.

32-bit floating-point format.

64-bit floating-point format.

8-bit integer format.

inherits from enum.Enum

Enum representing different types of vector distance metrics.

See VECTOR Datatype for background.

Added in version 2.0.41.

Dot product similarity.

Euclidean distance (L2 norm).

Manhattan distance (L1 norm).

Measures the cosine of the angle between two vectors.

Dot product similarity.

Measures the algebraic similarity between two vectors.

Euclidean distance (L2 norm).

Measures the straight-line distance between two vectors in space.

Manhattan distance (L1 norm).

Calculates the sum of absolute differences across dimensions.

inherits from enum.Enum

Enum representing the vector type,

See VECTOR Datatype for background.

Added in version 2.0.43.

A Dense vector is a vector where most, if not all, elements hold meaningful values.

A Sparse vector is a vector which has zero value for most of its dimensions.

A Dense vector is a vector where most, if not all, elements hold meaningful values.

A Sparse vector is a vector which has zero value for most of its dimensions.

Lightweight SQLAlchemy-side version of SparseVector. This mimics oracledb.SparseVector.

Added in version 2.0.43.

Support for the Oracle Database database via the python-oracledb driver.

Documentation and download information (if applicable) for python-oracledb is available at: https://oracle.github.io/python-oracledb/

Python-oracledb is the Oracle Database driver for Python. It features a default “thin” client mode that requires no dependencies, and an optional “thick” mode that uses Oracle Client libraries. It supports SQLAlchemy features including two phase transactions and Asyncio.

Python-oracle is the renamed, updated cx_Oracle driver. Oracle is no longer doing any releases in the cx_Oracle namespace.

The SQLAlchemy oracledb dialect provides both a sync and an async implementation under the same dialect name. The proper version is selected depending on how the engine is created:

calling create_engine() with oracle+oracledb://... will automatically select the sync version:

calling create_async_engine() with oracle+oracledb://... will automatically select the async version:

The asyncio version of the dialect may also be specified explicitly using the oracledb_async suffix:

Added in version 2.0.25: added support for the async version of oracledb.

By default, the python-oracledb driver runs in a “thin” mode that does not require Oracle Client libraries to be installed. The driver also supports a “thick” mode that uses Oracle Client libraries to get functionality such as Oracle Application Continuity.

To enable thick mode, call oracledb.init_oracle_client() explicitly, or pass the parameter thick_mode=True to create_engine(). To pass custom arguments to init_oracle_client(), like the lib_dir path, a dict may be passed, for example:

Note that passing a lib_dir path should only be done on macOS or Windows. On Linux it does not behave as you might expect.

python-oracledb documentation Enabling python-oracledb Thick mode

python-oracledb provides several methods of indicating the target database. The dialect translates from a series of different URL forms.

Given the hostname, port and service name of the target database, you can connect in SQLAlchemy using the service_name query string parameter:

You can pass any valid python-oracledb connection string as the dsn key value in a create_engine.connect_args dictionary. See python-oracledb documentation Oracle Net Services Connection Strings.

For example to use an Easy Connect string with a timeout to prevent connection establishment from hanging if the network transport to the database cannot be established in 30 seconds, and also setting a keep-alive time of 60 seconds to stop idle network connections from being terminated by a firewall:

The Easy Connect syntax has been enhanced during the life of Oracle Database. Review the documentation for your database version. The current documentation is at Understanding the Easy Connect Naming Method.

The general syntax is similar to:

Note that although the SQLAlchemy URL syntax hostname:port/dbname looks like Oracle’s Easy Connect syntax, it is different. SQLAlchemy’s URL requires a system identifier (SID) for the dbname component:

Easy Connect syntax does not support SIDs. It uses services names, which are the preferred choice for connecting to Oracle Database.

Other python-oracledb driver connection options can be passed in connect_args. For example:

If no port, database name, or service name is provided, the dialect will use an Oracle Database DSN “connection string”. This takes the “hostname” portion of the URL as the data source name. For example, if the tnsnames.ora file contains a TNS Alias of myalias as below:

The python-oracledb dialect connects to this database service when myalias is the hostname portion of the URL, without specifying a port, database name or service_name:

Users of Oracle Autonomous Database should use either use the TNS Alias URL shown above, or pass the TNS Alias as the dsn key value in a create_engine.connect_args dictionary.

If Oracle Autonomous Database is configured for mutual TLS (“mTLS”) connections, then additional configuration is required as shown in Connecting to Oracle Cloud Autonomous Databases. In summary, Thick mode users should configure file locations and set the wallet path in sqlnet.ora appropriately:

Thin mode users of mTLS should pass the appropriate directories and PEM wallet password when creating the engine, similar to:

Typically config_dir and wallet_location are the same directory, which is where the Oracle Autonomous Database wallet zip file was extracted. Note this directory should be protected.

The python-oracledb driver provides its own connection pool implementation that may be used in place of SQLAlchemy’s pooling functionality. The driver pool gives support for high availability features such as dead connection detection, connection draining for planned database downtime, support for Oracle Application Continuity and Transparent Application Continuity, and gives support for Database Resident Connection Pooling (DRCP).

To take advantage of python-oracledb’s pool, use the create_engine.creator parameter to provide a function that returns a new connection, along with setting create_engine.pool_class to NullPool to disable SQLAlchemy’s pooling:

The above engine may then be used normally. Internally, python-oracledb handles connection pooling:

Refer to the python-oracledb documentation for oracledb.create_pool() for the arguments that can be used when creating a connection pool.

When using Oracle Database’s Database Resident Connection Pooling (DRCP), the best practice is to specify a connection class and “purity”. Refer to the python-oracledb documentation on DRCP. For example:

The above engine may then be used normally where python-oracledb handles application connection pooling and Oracle Database additionally uses DRCP:

If you wish to use different connection classes or purities for different connections, then wrap pool.acquire():

There are also options that are consumed by the SQLAlchemy oracledb dialect itself. These options are always passed directly to create_engine(), such as:

The parameters accepted by the oracledb dialect are as follows:

arraysize - set the driver cursor.arraysize value. It defaults to None, indicating that the driver default value of 100 should be used. This setting controls how many rows are buffered when fetching rows, and can have a significant effect on performance if increased for queries that return large numbers of rows.

Changed in version 2.0.26: - changed the default value from 50 to None, to use the default value of the driver itself.

auto_convert_lobs - defaults to True; See LOB Datatypes.

coerce_to_decimal - see Precision Numerics for detail.

encoding_errors - see Encoding Errors for detail.

As is the case for all DBAPIs under Python 3, all strings are inherently Unicode strings.

In python-oracledb, the encoding used for all character data is “UTF-8”.

The Core expression language handles unicode data by use of the Unicode and UnicodeText datatypes. These types correspond to the VARCHAR2 and CLOB Oracle Database datatypes by default. When using these datatypes with Unicode data, it is expected that the database is configured with a Unicode-aware character set so that the VARCHAR2 and CLOB datatypes can accommodate the data.

In the case that Oracle Database is not configured with a Unicode character set, the two options are to use the NCHAR and NCLOB datatypes explicitly, or to pass the flag use_nchar_for_unicode=True to create_engine(), which will cause the SQLAlchemy dialect to use NCHAR/NCLOB for the Unicode / UnicodeText datatypes instead of VARCHAR/CLOB.

Changed in version 1.3: The Unicode and UnicodeText datatypes now correspond to the VARCHAR2 and CLOB Oracle Database datatypes unless the use_nchar_for_unicode=True is passed to the dialect when create_engine() is called.

For the unusual case that data in Oracle Database is present with a broken encoding, the dialect accepts a parameter encoding_errors which will be passed to Unicode decoding functions in order to affect how decoding errors are handled. The value is ultimately consumed by the Python decode function, and is passed both via python-oracledb’s encodingErrors parameter consumed by Cursor.var(), as well as SQLAlchemy’s own decoding function, as the python-oracledb dialect makes use of both under different circumstances.

Added in version 1.3.11.

The python-oracle DBAPI has a deep and fundamental reliance upon the usage of the DBAPI setinputsizes() call. The purpose of this call is to establish the datatypes that are bound to a SQL statement for Python values being passed as parameters. While virtually no other DBAPI assigns any use to the setinputsizes() call, the python-oracledb DBAPI relies upon it heavily in its interactions with the Oracle Database, and in some scenarios it is not possible for SQLAlchemy to know exactly how data should be bound, as some settings can cause profoundly different performance characteristics, while altering the type coercion behavior at the same time.

Users of the oracledb dialect are strongly encouraged to read through python-oracledb’s list of built-in datatype symbols at Database Types Note that in some cases, significant performance degradation can occur when using these types vs. not.

On the SQLAlchemy side, the DialectEvents.do_setinputsizes() event can be used both for runtime visibility (e.g. logging) of the setinputsizes step as well as to fully control how setinputsizes() is used on a per-statement basis.

Added in version 1.2.9: Added DialectEvents.setinputsizes()

The following example illustrates how to log the intermediary values from a SQLAlchemy perspective before they are converted to the raw setinputsizes() parameter dictionary. The keys of the dictionary are BindParameter objects which have a .key and a .type attribute:

For performance, fetching LOB datatypes from Oracle Database is set by default for the Text type within SQLAlchemy. This setting can be modified as follows:

LOB datatypes refer to the “large object” datatypes such as CLOB, NCLOB and BLOB. Oracle Database can efficiently return these datatypes as a single buffer. SQLAlchemy makes use of type handlers to do this by default.

To disable the use of the type handlers and deliver LOB objects as classic buffered objects with a read() method, the parameter auto_convert_lobs=False may be passed to create_engine().

The oracledb dialect implements RETURNING using OUT parameters. The dialect supports RETURNING fully.

Two phase transactions are fully supported with python-oracledb. (Thin mode requires python-oracledb 2.3). APIs for two phase transactions are provided at the Core level via Connection.begin_twophase() and Session.twophase for transparent ORM use.

Changed in version 2.0.32: added support for two phase transactions

SQLAlchemy’s numeric types can handle receiving and returning values as Python Decimal objects or float objects. When a Numeric object, or a subclass such as Float, DOUBLE_PRECISION etc. is in use, the Numeric.asdecimal flag determines if values should be coerced to Decimal upon return, or returned as float objects. To make matters more complicated under Oracle Database, the NUMBER type can also represent integer values if the “scale” is zero, so the Oracle Database-specific NUMBER type takes this into account as well.

The oracledb dialect makes extensive use of connection- and cursor-level “outputtypehandler” callables in order to coerce numeric values as requested. These callables are specific to the specific flavor of Numeric in use, as well as if no SQLAlchemy typing objects are present. There are observed scenarios where Oracle Database may send incomplete or ambiguous information about the numeric types being returned, such as a query where the numeric types are buried under multiple levels of subquery. The type handlers do their best to make the right decision in all cases, deferring to the underlying python-oracledb DBAPI for all those cases where the driver can make the best decision.

When no typing objects are present, as when executing plain SQL strings, a default “outputtypehandler” is present which will generally return numeric values which specify precision and scale as Python Decimal objects. To disable this coercion to decimal for performance reasons, pass the flag coerce_to_decimal=False to create_engine():

The coerce_to_decimal flag only impacts the results of plain string SQL statements that are not otherwise associated with a Numeric SQLAlchemy type (or a subclass of such).

Changed in version 1.2: The numeric handling system for the oracle dialects has been reworked to take advantage of newer driver features as well as better integration of outputtypehandlers.

Added in version 2.0.0: added support for the python-oracledb driver.

Support for the Oracle Database database via the cx-Oracle driver.

Documentation and download information (if applicable) for cx-Oracle is available at: https://oracle.github.io/python-cx_Oracle/

cx_Oracle was the original driver for Oracle Database. It was superseded by python-oracledb which should be used instead.

cx_Oracle provides several methods of indicating the target database. The dialect translates from a series of different URL forms.

Given a hostname, port and service name of the target database, for example from Oracle Database’s Easy Connect syntax then connect in SQLAlchemy using the service_name query string parameter:

Note that the default driver value for encoding and nencoding was changed to “UTF-8” in cx_Oracle 8.0 so these parameters can be omitted when using that version, or later.

To use a full Easy Connect string, pass it as the dsn key value in a create_engine.connect_args dictionary:

Alternatively, if no port, database name, or service name is provided, the dialect will use an Oracle Database DSN “connection string”. This takes the “hostname” portion of the URL as the data source name. For example, if the tnsnames.ora file contains a TNS Alias of myalias as below:

The cx_Oracle dialect connects to this database service when myalias is the hostname portion of the URL, without specifying a port, database name or service_name:

Users of Oracle Autonomous Database should use this syntax. If the database is configured for mutural TLS (“mTLS”), then you must also configure the cloud wallet as shown in cx_Oracle documentation Connecting to Autononmous Databases.

To use Oracle Database’s obsolete System Identifier connection syntax, the SID can be passed in a “database name” portion of the URL:

Above, the DSN passed to cx_Oracle is created by cx_Oracle.makedsn() as follows:

Note that although the SQLAlchemy syntax hostname:port/dbname looks like Oracle’s Easy Connect syntax it is different. It uses a SID in place of the service name required by Easy Connect. The Easy Connect syntax does not support SIDs.

Additional connection arguments can usually be passed via the URL query string; particular symbols like SYSDBA are intercepted and converted to the correct symbol:

Changed in version 1.3: the cx_Oracle dialect now accepts all argument names within the URL string itself, to be passed to the cx_Oracle DBAPI. As was the case earlier but not correctly documented, the create_engine.connect_args parameter also accepts all cx_Oracle DBAPI connect arguments.

To pass arguments directly to .connect() without using the query string, use the create_engine.connect_args dictionary. Any cx_Oracle parameter value and/or constant may be passed, such as:

Note that the default driver value for encoding and nencoding was changed to “UTF-8” in cx_Oracle 8.0 so these parameters can be omitted when using that version, or later.

There are also options that are consumed by the SQLAlchemy cx_oracle dialect itself. These options are always passed directly to create_engine() , such as:

The parameters accepted by the cx_oracle dialect are as follows:

arraysize - set the cx_oracle.arraysize value on cursors; defaults to None, indicating that the driver default should be used (typically the value is 100). This setting controls how many rows are buffered when fetching rows, and can have a significant effect on performance when modified.

Changed in version 2.0.26: - changed the default value from 50 to None, to use the default value of the driver itself.

auto_convert_lobs - defaults to True; See LOB Datatypes.

coerce_to_decimal - see Precision Numerics for detail.

encoding_errors - see Encoding Errors for detail.

The cx_Oracle driver provides its own connection pool implementation that may be used in place of SQLAlchemy’s pooling functionality. The driver pool supports Oracle Database features such dead connection detection, connection draining for planned database downtime, support for Oracle Application Continuity and Transparent Application Continuity, and gives support for Database Resident Connection Pooling (DRCP).

Using the driver pool can be achieved by using the create_engine.creator parameter to provide a function that returns a new connection, along with setting create_engine.pool_class to NullPool to disable SQLAlchemy’s pooling:

The above engine may then be used normally where cx_Oracle’s pool handles connection pooling:

As well as providing a scalable solution for multi-user applications, the cx_Oracle session pool supports some Oracle features such as DRCP and Application Continuity.

Note that the pool creation parameters threaded, encoding and nencoding were deprecated in later cx_Oracle releases.

When using Oracle Database’s DRCP, the best practice is to pass a connection class and “purity” when acquiring a connection from the SessionPool. Refer to the cx_Oracle DRCP documentation.

This can be achieved by wrapping pool.acquire():

The above engine may then be used normally where cx_Oracle handles session pooling and Oracle Database additionally uses DRCP:

As is the case for all DBAPIs under Python 3, all strings are inherently Unicode strings. In all cases however, the driver requires an explicit encoding configuration.

The long accepted standard for establishing client encoding for nearly all Oracle Database related software is via the NLS_LANG environment variable. Older versions of cx_Oracle use this environment variable as the source of its encoding configuration. The format of this variable is Territory_Country.CharacterSet; a typical value would be AMERICAN_AMERICA.AL32UTF8. cx_Oracle version 8 and later use the character set “UTF-8” by default, and ignore the character set component of NLS_LANG.

The cx_Oracle driver also supported a programmatic alternative which is to pass the encoding and nencoding parameters directly to its .connect() function. These can be present in the URL as follows:

For the meaning of the encoding and nencoding parameters, please consult Characters Sets and National Language Support (NLS).

Characters Sets and National Language Support (NLS) - in the cx_Oracle documentation.

The Core expression language handles unicode data by use of the Unicode and UnicodeText datatypes. These types correspond to the VARCHAR2 and CLOB Oracle Database datatypes by default. When using these datatypes with Unicode data, it is expected that the database is configured with a Unicode-aware character set, as well as that the NLS_LANG environment variable is set appropriately (this applies to older versions of cx_Oracle), so that the VARCHAR2 and CLOB datatypes can accommodate the data.

In the case that Oracle Database is not configured with a Unicode character set, the two options are to use the NCHAR and NCLOB datatypes explicitly, or to pass the flag use_nchar_for_unicode=True to create_engine(), which will cause the SQLAlchemy dialect to use NCHAR/NCLOB for the Unicode / UnicodeText datatypes instead of VARCHAR/CLOB.

Changed in version 1.3: The Unicode and UnicodeText datatypes now correspond to the VARCHAR2 and CLOB Oracle Database datatypes unless the use_nchar_for_unicode=True is passed to the dialect when create_engine() is called.

For the unusual case that data in Oracle Database is present with a broken encoding, the dialect accepts a parameter encoding_errors which will be passed to Unicode decoding functions in order to affect how decoding errors are handled. The value is ultimately consumed by the Python decode function, and is passed both via cx_Oracle’s encodingErrors parameter consumed by Cursor.var(), as well as SQLAlchemy’s own decoding function, as the cx_Oracle dialect makes use of both under different circumstances.

Added in version 1.3.11.

The cx_Oracle DBAPI has a deep and fundamental reliance upon the usage of the DBAPI setinputsizes() call. The purpose of this call is to establish the datatypes that are bound to a SQL statement for Python values being passed as parameters. While virtually no other DBAPI assigns any use to the setinputsizes() call, the cx_Oracle DBAPI relies upon it heavily in its interactions with the Oracle Database client interface, and in some scenarios it is not possible for SQLAlchemy to know exactly how data should be bound, as some settings can cause profoundly different performance characteristics, while altering the type coercion behavior at the same time.

Users of the cx_Oracle dialect are strongly encouraged to read through cx_Oracle’s list of built-in datatype symbols at https://cx-oracle.readthedocs.io/en/latest/api_manual/module.html#database-types. Note that in some cases, significant performance degradation can occur when using these types vs. not, in particular when specifying cx_Oracle.CLOB.

On the SQLAlchemy side, the DialectEvents.do_setinputsizes() event can be used both for runtime visibility (e.g. logging) of the setinputsizes step as well as to fully control how setinputsizes() is used on a per-statement basis.

Added in version 1.2.9: Added DialectEvents.setinputsizes()

The following example illustrates how to log the intermediary values from a SQLAlchemy perspective before they are converted to the raw setinputsizes() parameter dictionary. The keys of the dictionary are BindParameter objects which have a .key and a .type attribute:

The CLOB datatype in cx_Oracle incurs a significant performance overhead, however is set by default for the Text type within the SQLAlchemy 1.2 series. This setting can be modified as follows:

LOB datatypes refer to the “large object” datatypes such as CLOB, NCLOB and BLOB. Modern versions of cx_Oracle is optimized for these datatypes to be delivered as a single buffer. As such, SQLAlchemy makes use of these newer type handlers by default.

To disable the use of newer type handlers and deliver LOB objects as classic buffered objects with a read() method, the parameter auto_convert_lobs=False may be passed to create_engine(), which takes place only engine-wide.

The cx_Oracle dialect implements RETURNING using OUT parameters. The dialect supports RETURNING fully.

Two phase transactions are not supported under cx_Oracle due to poor driver support. The newer python-oracledb dialect however does support two phase transactions.

SQLAlchemy’s numeric types can handle receiving and returning values as Python Decimal objects or float objects. When a Numeric object, or a subclass such as Float, DOUBLE_PRECISION etc. is in use, the Numeric.asdecimal flag determines if values should be coerced to Decimal upon return, or returned as float objects. To make matters more complicated under Oracle Database, the NUMBER type can also represent integer values if the “scale” is zero, so the Oracle Database-specific NUMBER type takes this into account as well.

The cx_Oracle dialect makes extensive use of connection- and cursor-level “outputtypehandler” callables in order to coerce numeric values as requested. These callables are specific to the specific flavor of Numeric in use, as well as if no SQLAlchemy typing objects are present. There are observed scenarios where Oracle Database may send incomplete or ambiguous information about the numeric types being returned, such as a query where the numeric types are buried under multiple levels of subquery. The type handlers do their best to make the right decision in all cases, deferring to the underlying cx_Oracle DBAPI for all those cases where the driver can make the best decision.

When no typing objects are present, as when executing plain SQL strings, a default “outputtypehandler” is present which will generally return numeric values which specify precision and scale as Python Decimal objects. To disable this coercion to decimal for performance reasons, pass the flag coerce_to_decimal=False to create_engine():

The coerce_to_decimal flag only impacts the results of plain string SQL statements that are not otherwise associated with a Numeric SQLAlchemy type (or a subclass of such).

Changed in version 1.2: The numeric handling system for cx_Oracle has been reworked to take advantage of newer cx_Oracle features as well as better integration of outputtypehandlers.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (unknown):
```unknown
t = Table(
    "mytable",
    metadata,
    Column("id", Integer, Identity(start=3), primary_key=True),
    Column(...),
    ...,
)
```

Example 2 (sql):
```sql
CREATE TABLE mytable (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY (START WITH 3),
    ...,
    PRIMARY KEY (id)
)
```

Example 3 (unknown):
```unknown
t = Table(
    "mytable",
    metadata,
    Column("id", Integer, Sequence("id_seq", start=1), primary_key=True),
    Column(...),
    ...,
)
```

Example 4 (unknown):
```unknown
t = Table(
    "mytable",
    metadata,
    Column("id", Integer, Sequence("id_seq", start=1), primary_key=True),
    autoload_with=engine,
)
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/dialects/postgresql.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - Dialects
    - Project Versions
- PostgreSQL¶
- DBAPI Support¶
- Sequences/SERIAL/IDENTITY¶
  - PostgreSQL 10 and above IDENTITY columns¶
- Server Side Cursors¶
- Transaction Isolation Level¶

Home | Download this Documentation

Home | Download this Documentation

Support for the PostgreSQL database.

The following table summarizes current support levels for database release versions.

The following dialect/DBAPI options are available. Please refer to individual DBAPI sections for connect information.

psycopg (a.k.a. psycopg 3)

PostgreSQL supports sequences, and SQLAlchemy uses these as the default means of creating new primary key values for integer-based primary key columns. When creating tables, SQLAlchemy will issue the SERIAL datatype for integer-based primary key columns, which generates a sequence and server side default corresponding to the column.

To specify a specific named sequence to be used for primary key generation, use the Sequence() construct:

When SQLAlchemy issues a single INSERT statement, to fulfill the contract of having the “last insert identifier” available, a RETURNING clause is added to the INSERT statement which specifies the primary key columns should be returned after the statement completes. The RETURNING functionality only takes place if PostgreSQL 8.2 or later is in use. As a fallback approach, the sequence, whether specified explicitly or implicitly via SERIAL, is executed independently beforehand, the returned value to be used in the subsequent insert. Note that when an insert() construct is executed using “executemany” semantics, the “last inserted identifier” functionality does not apply; no RETURNING clause is emitted nor is the sequence pre-executed in this case.

PostgreSQL 10 and above have a new IDENTITY feature that supersedes the use of SERIAL. The Identity construct in a Column can be used to control its behavior:

The CREATE TABLE for the above Table object would be:

Changed in version 1.4: Added Identity construct in a Column to specify the option of an autoincrementing column.

Previous versions of SQLAlchemy did not have built-in support for rendering of IDENTITY, and could use the following compilation hook to replace occurrences of SERIAL with IDENTITY:

Using the above, a table such as:

Will generate on the backing database as:

Server-side cursor support is available for the psycopg2, asyncpg dialects and may also be available in others.

Server side cursors are enabled on a per-statement basis by using the Connection.execution_options.stream_results connection execution option:

Note that some kinds of SQL statements may not be supported with server side cursors; generally, only SQL statements that return rows should be used with this option.

Deprecated since version 1.4: The dialect-level server_side_cursors flag is deprecated and will be removed in a future release. Please use the Connection.stream_results execution option for unbuffered cursor support.

Using Server Side Cursors (a.k.a. stream results)

Most SQLAlchemy dialects support setting of transaction isolation level using the create_engine.isolation_level parameter at the create_engine() level, and at the Connection level via the Connection.execution_options.isolation_level parameter.

For PostgreSQL dialects, this feature works either by making use of the DBAPI-specific features, such as psycopg2’s isolation level flags which will embed the isolation level setting inline with the "BEGIN" statement, or for DBAPIs with no direct support by emitting SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL <level> ahead of the "BEGIN" statement emitted by the DBAPI. For the special AUTOCOMMIT isolation level, DBAPI-specific techniques are used which is typically an .autocommit flag on the DBAPI connection object.

To set isolation level using create_engine():

To set using per-connection execution options:

There are also more options for isolation level configurations, such as “sub-engine” objects linked to a main Engine which each apply different isolation level settings. See the discussion at Setting Transaction Isolation Levels including DBAPI Autocommit for background.

Valid values for isolation_level on most PostgreSQL dialects include:

Setting Transaction Isolation Levels including DBAPI Autocommit

Setting READ ONLY / DEFERRABLE

Psycopg2 Transaction Isolation Level

pg8000 Transaction Isolation Level

Most PostgreSQL dialects support setting the “READ ONLY” and “DEFERRABLE” characteristics of the transaction, which is in addition to the isolation level setting. These two attributes can be established either in conjunction with or independently of the isolation level by passing the postgresql_readonly and postgresql_deferrable flags with Connection.execution_options(). The example below illustrates passing the "SERIALIZABLE" isolation level at the same time as setting “READ ONLY” and “DEFERRABLE”:

Note that some DBAPIs such as asyncpg only support “readonly” with SERIALIZABLE isolation.

Added in version 1.4: added support for the postgresql_readonly and postgresql_deferrable execution options.

The QueuePool connection pool implementation used by the SQLAlchemy Engine object includes reset on return behavior that will invoke the DBAPI .rollback() method when connections are returned to the pool. While this rollback will clear out the immediate state used by the previous transaction, it does not cover a wider range of session-level state, including temporary tables as well as other server state such as prepared statement handles and statement caches. The PostgreSQL database includes a variety of commands which may be used to reset this state, including DISCARD, RESET, DEALLOCATE, and UNLISTEN.

To install one or more of these commands as the means of performing reset-on-return, the PoolEvents.reset() event hook may be used, as demonstrated in the example below. The implementation will end transactions in progress as well as discard temporary tables using the CLOSE, RESET and DISCARD commands; see the PostgreSQL documentation for background on what each of these statements do.

The create_engine.pool_reset_on_return parameter is set to None so that the custom scheme can replace the default behavior completely. The custom hook implementation calls .rollback() in any case, as it’s usually important that the DBAPI’s own tracking of commit/rollback will remain consistent with the state of the transaction:

Changed in version 2.0.0b3: Added additional state arguments to the PoolEvents.reset() event and additionally ensured the event is invoked for all “reset” occurrences, so that it’s appropriate as a place for custom “reset” handlers. Previous schemes which use the PoolEvents.checkin() handler remain usable as well.

Reset On Return - in the Connection Pooling documentation

The PostgreSQL search_path variable refers to the list of schema names that will be implicitly referenced when a particular table or other object is referenced in a SQL statement. As detailed in the next section Remote-Schema Table Introspection and PostgreSQL search_path, SQLAlchemy is generally organized around the concept of keeping this variable at its default value of public, however, in order to have it set to any arbitrary name or names when connections are used automatically, the “SET SESSION search_path” command may be invoked for all connections in a pool using the following event handler, as discussed at Setting a Default Schema for New Connections:

The reason the recipe is complicated by use of the .autocommit DBAPI attribute is so that when the SET SESSION search_path directive is invoked, it is invoked outside of the scope of any transaction and therefore will not be reverted when the DBAPI connection has a rollback.

Setting a Default Schema for New Connections - in the Describing Databases with MetaData documentation

Section Best Practices Summarized

keep the search_path variable set to its default of public, without any other schema names. Ensure the username used to connect does not match remote schemas, or ensure the "$user" token is removed from search_path. For other schema names, name these explicitly within Table definitions. Alternatively, the postgresql_ignore_search_path option will cause all reflected Table objects to have a Table.schema attribute set up.

The PostgreSQL dialect can reflect tables from any schema, as outlined in Reflecting Tables from Other Schemas.

In all cases, the first thing SQLAlchemy does when reflecting tables is to determine the default schema for the current database connection. It does this using the PostgreSQL current_schema() function, illustated below using a PostgreSQL client session (i.e. using the psql tool):

Above we see that on a plain install of PostgreSQL, the default schema name is the name public.

However, if your database username matches the name of a schema, PostgreSQL’s default is to then use that name as the default schema. Below, we log in using the username scott. When we create a schema named scott, it implicitly changes the default schema:

The behavior of current_schema() is derived from the PostgreSQL search path variable search_path, which in modern PostgreSQL versions defaults to this:

Where above, the "$user" variable will inject the current username as the default schema, if one exists. Otherwise, public is used.

When a Table object is reflected, if it is present in the schema indicated by the current_schema() function, the schema name assigned to the “.schema” attribute of the Table is the Python “None” value. Otherwise, the “.schema” attribute will be assigned the string name of that schema.

With regards to tables which these Table objects refer to via foreign key constraint, a decision must be made as to how the .schema is represented in those remote tables, in the case where that remote schema name is also a member of the current search_path.

By default, the PostgreSQL dialect mimics the behavior encouraged by PostgreSQL’s own pg_get_constraintdef() builtin procedure. This function returns a sample definition for a particular foreign key constraint, omitting the referenced schema name from that definition when the name is also in the PostgreSQL schema search path. The interaction below illustrates this behavior:

Above, we created a table referred as a member of the remote schema test_schema, however when we added test_schema to the PG search_path and then asked pg_get_constraintdef() for the FOREIGN KEY syntax, test_schema was not included in the output of the function.

On the other hand, if we set the search path back to the typical default of public:

The same query against pg_get_constraintdef() now returns the fully schema-qualified name for us:

SQLAlchemy will by default use the return value of pg_get_constraintdef() in order to determine the remote schema name. That is, if our search_path were set to include test_schema, and we invoked a table reflection process as follows:

The above process would deliver to the MetaData.tables collection referred table named without the schema:

To alter the behavior of reflection such that the referred schema is maintained regardless of the search_path setting, use the postgresql_ignore_search_path option, which can be specified as a dialect-specific argument to both Table as well as MetaData.reflect():

We will now have test_schema.referred stored as schema-qualified:

Best Practices for PostgreSQL Schema reflection

The description of PostgreSQL schema reflection behavior is complex, and is the product of many years of dealing with widely varied use cases and user preferences. But in fact, there’s no need to understand any of it if you just stick to the simplest use pattern: leave the search_path set to its default of public only, never refer to the name public as an explicit schema name otherwise, and refer to all other schema names explicitly when building up a Table object. The options described here are only for those users who can’t, or prefer not to, stay within these guidelines.

Interaction of Schema-qualified Reflection with the Default Schema - discussion of the issue from a backend-agnostic perspective

The Schema Search Path - on the PostgreSQL website.

The dialect supports PG 8.2’s INSERT..RETURNING, UPDATE..RETURNING and DELETE..RETURNING syntaxes. INSERT..RETURNING is used by default for single-row INSERT statements in order to fetch newly generated primary key identifiers. To specify an explicit RETURNING clause, use the _UpdateBase.returning() method on a per-statement basis:

Starting with version 9.5, PostgreSQL allows “upserts” (update or insert) of rows into a table via the ON CONFLICT clause of the INSERT statement. A candidate row will only be inserted if that row does not violate any unique constraints. In the case of a unique constraint violation, a secondary action can occur which can be either “DO UPDATE”, indicating that the data in the target row should be updated, or “DO NOTHING”, which indicates to silently skip this row.

Conflicts are determined using existing unique constraints and indexes. These constraints may be identified either using their name as stated in DDL, or they may be inferred by stating the columns and conditions that comprise the indexes.

SQLAlchemy provides ON CONFLICT support via the PostgreSQL-specific insert() function, which provides the generative methods Insert.on_conflict_do_update() and Insert.on_conflict_do_nothing():

INSERT .. ON CONFLICT - in the PostgreSQL documentation.

Both methods supply the “target” of the conflict using either the named constraint or by column inference:

The Insert.on_conflict_do_update.index_elements argument specifies a sequence containing string column names, Column objects, and/or SQL expression elements, which would identify a unique index:

When using Insert.on_conflict_do_update.index_elements to infer an index, a partial index can be inferred by also specifying the use the Insert.on_conflict_do_update.index_where parameter:

The Insert.on_conflict_do_update.constraint argument is used to specify an index directly rather than inferring it. This can be the name of a UNIQUE constraint, a PRIMARY KEY constraint, or an INDEX:

The Insert.on_conflict_do_update.constraint argument may also refer to a SQLAlchemy construct representing a constraint, e.g. UniqueConstraint, PrimaryKeyConstraint, Index, or ExcludeConstraint. In this use, if the constraint has a name, it is used directly. Otherwise, if the constraint is unnamed, then inference will be used, where the expressions and optional WHERE clause of the constraint will be spelled out in the construct. This use is especially convenient to refer to the named or unnamed primary key of a Table using the Table.primary_key attribute:

ON CONFLICT...DO UPDATE is used to perform an update of the already existing row, using any combination of new values as well as values from the proposed insertion. These values are specified using the Insert.on_conflict_do_update.set_ parameter. This parameter accepts a dictionary which consists of direct values for UPDATE:

The Insert.on_conflict_do_update() method does not take into account Python-side default UPDATE values or generation functions, e.g. those specified using Column.onupdate. These values will not be exercised for an ON CONFLICT style of UPDATE, unless they are manually specified in the Insert.on_conflict_do_update.set_ dictionary.

In order to refer to the proposed insertion row, the special alias Insert.excluded is available as an attribute on the Insert object; this object is a ColumnCollection which alias contains all columns of the target table:

The Insert.on_conflict_do_update() method also accepts a WHERE clause using the Insert.on_conflict_do_update.where parameter, which will limit those rows which receive an UPDATE:

ON CONFLICT may be used to skip inserting a row entirely if any conflict with a unique or exclusion constraint occurs; below this is illustrated using the Insert.on_conflict_do_nothing() method:

If DO NOTHING is used without specifying any columns or constraint, it has the effect of skipping the INSERT for any unique or exclusion constraint violation which occurs:

PostgreSQL’s full text search system is available through the use of the func namespace, combined with the use of custom operators via the Operators.bool_op() method. For simple cases with some degree of cross-backend compatibility, the Operators.match() operator may also be used.

The Operators.match() operator provides for cross-compatible simple text matching. For the PostgreSQL backend, it’s hardcoded to generate an expression using the @@ operator in conjunction with the plainto_tsquery() PostgreSQL function.

On the PostgreSQL dialect, an expression like the following:

would emit to the database:

Above, passing a plain string to Operators.match() will automatically make use of plainto_tsquery() to specify the type of tsquery. This establishes basic database cross-compatibility for Operators.match() with other backends.

Changed in version 2.0: The default tsquery generation function used by the PostgreSQL dialect with Operators.match() is plainto_tsquery().

To render exactly what was rendered in 1.4, use the following form:

Text search operations beyond the simple use of Operators.match() may make use of the func namespace to generate PostgreSQL full-text functions, in combination with Operators.bool_op() to generate any boolean operator.

For example, the query:

The TSVECTOR type can provide for explicit CAST:

produces a statement equivalent to:

The func namespace is augmented by the PostgreSQL dialect to set up correct argument and return types for most full text search functions. These functions are used automatically by the sqlalchemy.sql.expression.func namespace assuming the sqlalchemy.dialects.postgresql package has been imported, or create_engine() has been invoked using a postgresql dialect. These functions are documented at:

PostgreSQL’s plainto_tsquery() function accepts an optional “regconfig” argument that is used to instruct PostgreSQL to use a particular pre-computed GIN or GiST index in order to perform the search. When using Operators.match(), this additional parameter may be specified using the postgresql_regconfig parameter, such as:

When using other PostgreSQL search functions with func, the “regconfig” parameter may be passed directly as the initial argument:

produces a statement equivalent to:

It is recommended that you use the EXPLAIN ANALYZE... tool from PostgreSQL to ensure that you are generating queries with SQLAlchemy that take full advantage of any indexes you may have created for full text search.

Full Text Search - in the PostgreSQL documentation

The dialect supports PostgreSQL’s ONLY keyword for targeting only a particular table in an inheritance hierarchy. This can be used to produce the SELECT ... FROM ONLY, UPDATE ONLY ..., and DELETE FROM ONLY ... syntaxes. It uses SQLAlchemy’s hints mechanism:

Several extensions to the Index construct are available, specific to the PostgreSQL dialect.

A covering index includes additional columns that are not part of the index key but are stored in the index, allowing PostgreSQL to satisfy queries using only the index without accessing the table (an “index-only scan”). This is indicated on the index using the INCLUDE clause. The postgresql_include option for Index (as well as UniqueConstraint) renders INCLUDE(colname) for the given string names:

would render the index as CREATE INDEX my_index ON table (x) INCLUDE (y)

Note that this feature requires PostgreSQL 11 or later.

INCLUDE - the same feature implemented for UniqueConstraint

Added in version 1.4: - support for covering indexes with Index. support for UniqueConstraint was in 2.0.41

Partial indexes add criterion to the index definition so that the index is applied to a subset of rows. These can be specified on Index using the postgresql_where keyword argument:

PostgreSQL allows the specification of an operator class for each column of an index (see https://www.postgresql.org/docs/current/interactive/indexes-opclass.html). The Index construct allows these to be specified via the postgresql_ops keyword argument:

Note that the keys in the postgresql_ops dictionaries are the “key” name of the Column, i.e. the name used to access it from the .c collection of Table, which can be configured to be different than the actual name of the column as expressed in the database.

If postgresql_ops is to be used against a complex SQL expression such as a function call, then to apply to the column it must be given a label that is identified in the dictionary by name, e.g.:

Operator classes are also supported by the ExcludeConstraint construct using the ExcludeConstraint.ops parameter. See that parameter for details.

Added in version 1.3.21: added support for operator classes with ExcludeConstraint.

PostgreSQL provides several index types: B-Tree, Hash, GiST, and GIN, as well as the ability for users to create their own (see https://www.postgresql.org/docs/current/static/indexes-types.html). These can be specified on Index using the postgresql_using keyword argument:

The value passed to the keyword argument will be simply passed through to the underlying CREATE INDEX command, so it must be a valid index type for your version of PostgreSQL.

PostgreSQL allows storage parameters to be set on indexes. The storage parameters available depend on the index method used by the index. Storage parameters can be specified on Index using the postgresql_with keyword argument:

PostgreSQL allows to define the tablespace in which to create the index. The tablespace can be specified on Index using the postgresql_tablespace keyword argument:

Note that the same option is available on Table as well.

The PostgreSQL index option CONCURRENTLY is supported by passing the flag postgresql_concurrently to the Index construct:

The above index construct will render DDL for CREATE INDEX, assuming PostgreSQL 8.2 or higher is detected or for a connection-less dialect, as:

For DROP INDEX, assuming PostgreSQL 9.2 or higher is detected or for a connection-less dialect, it will emit:

When using CONCURRENTLY, the PostgreSQL database requires that the statement be invoked outside of a transaction block. The Python DBAPI enforces that even for a single statement, a transaction is present, so to use this construct, the DBAPI’s “autocommit” mode must be used:

Transaction Isolation Level

The PostgreSQL database creates a UNIQUE INDEX implicitly whenever the UNIQUE CONSTRAINT construct is used. When inspecting a table using Inspector, the Inspector.get_indexes() and the Inspector.get_unique_constraints() will report on these two constructs distinctly; in the case of the index, the key duplicates_constraint will be present in the index entry if it is detected as mirroring a constraint. When performing reflection using Table(..., autoload_with=engine), the UNIQUE INDEX is not returned in Table.indexes when it is detected as mirroring a UniqueConstraint in the Table.constraints collection .

The Inspector used for the PostgreSQL backend is an instance of PGInspector, which offers additional methods:

inherits from sqlalchemy.engine.reflection.Inspector

Return a list of DOMAIN objects.

Return a list of ENUM objects.

get_foreign_table_names()

Return a list of FOREIGN TABLE names.

Return the OID for the given table name.

Return if the database has the specified type in the provided schema.

Return a list of DOMAIN objects.

Each member is a dictionary containing these fields:

name - name of the domain

schema - the schema name for the domain.

visible - boolean, whether or not this domain is visible in the default search path.

type - the type defined by this domain.

nullable - Indicates if this domain can be NULL.

default - The default value of the domain or None if the domain has no default.

constraints - A list of dict with the constraint defined by this domain. Each element contains two keys: name of the constraint and check with the constraint text.

schema¶ – schema name. If None, the default schema (typically ‘public’) is used. May also be set to '*' to indicate load domains for all schemas.

Added in version 2.0.

Return a list of ENUM objects.

Each member is a dictionary containing these fields:

name - name of the enum

schema - the schema name for the enum.

visible - boolean, whether or not this enum is visible in the default search path.

labels - a list of string labels that apply to the enum.

schema¶ – schema name. If None, the default schema (typically ‘public’) is used. May also be set to '*' to indicate load enums for all schemas.

Return a list of FOREIGN TABLE names.

Behavior is similar to that of Inspector.get_table_names(), except that the list is limited to those tables that report a relkind value of f.

Return the OID for the given table name.

table_name¶ – string name of the table. For special quoting, use quoted_name.

schema¶ – string schema name; if omitted, uses the default schema of the database connection. For special quoting, use quoted_name.

Return if the database has the specified type in the provided schema.

type_name¶ – the type to check.

schema¶ – schema name. If None, the default schema (typically ‘public’) is used. May also be set to '*' to check in all schemas.

Added in version 2.0.

Several options for CREATE TABLE are supported directly by the PostgreSQL dialect in conjunction with the Table construct, listed in the following sections.

PostgreSQL CREATE TABLE options - in the PostgreSQL documentation.

Specifies one or more parent tables from which this table inherits columns and constraints, enabling table inheritance hierarchies in PostgreSQL.

Controls the behavior of temporary tables at transaction commit, with options to preserve rows, delete rows, or drop the table.

Declares the table as a partitioned table using the specified partitioning strategy (RANGE, LIST, or HASH) on the given column(s).

Specifies the tablespace where the table will be stored, allowing control over the physical location of table data on disk.

The above option is also available on the Index construct.

Specifies the table access method to use for storing table data, such as heap (the default) or other custom access methods.

Added in version 2.0.26.

Enables the legacy OID (object identifier) system column for the table, which assigns a unique identifier to each row.

Explicitly disables the OID system column for the table (the default behavior in modern PostgreSQL versions).

The following sections indicate options which are supported by the PostgreSQL dialect in conjunction with selected constraint constructs.

Allows a constraint to be added without validating existing rows, improving performance when adding constraints to large tables. This option applies towards CHECK and FOREIGN KEY constraints when the constraint is being added to an existing table via ALTER TABLE, and has the effect that existing rows are not scanned during the ALTER operation against the constraint being added.

When using a SQL migration tool such as Alembic that renders ALTER TABLE constructs, the postgresql_not_valid argument may be specified as an additional keyword argument within the operation that creates the constraint, as in the following Alembic example:

The keyword is ultimately accepted directly by the CheckConstraint, ForeignKeyConstraint and ForeignKey constructs; when using a tool like Alembic, dialect-specific keyword arguments are passed through to these constructs from the migration operation directives:

Added in version 1.4.32.

PostgreSQL ALTER TABLE options - in the PostgreSQL documentation.

This keyword is applicable to both a UNIQUE constraint as well as an INDEX. The postgresql_include option available for UniqueConstraint as well as Index creates a covering index by including additional columns in the underlying index without making them part of the key constraint. This option adds one or more columns as a “payload” to the index created automatically by PostgreSQL for the constraint. For example, the following table definition:

would produce the DDL statement

Note that this feature requires PostgreSQL 11 or later.

Added in version 2.0.41: - added support for postgresql_include to UniqueConstraint, to complement the existing feature in Index.

Covering Indexes - background on postgresql_include for the Index construct.

Allows selective column updates when a foreign key action is triggered, limiting which columns are set to NULL or DEFAULT upon deletion of a referenced row. This applies to ForeignKey and ForeignKeyConstraint, the ForeignKey.ondelete parameter will accept on the PostgreSQL backend only a string list of column names inside parenthesis, following the SET NULL or SET DEFAULT phrases, which will limit the set of columns that are subject to the action:

Added in version 2.0.40.

PostgreSQL makes great use of modern SQL forms such as table-valued functions, tables and rows as values. These constructs are commonly used as part of PostgreSQL’s support for complex datatypes such as JSON, ARRAY, and other datatypes. SQLAlchemy’s SQL expression language has native support for most table-valued and row-valued forms.

Many PostgreSQL built-in functions are intended to be used in the FROM clause of a SELECT statement, and are capable of returning table rows or sets of table rows. A large portion of PostgreSQL’s JSON functions for example such as json_array_elements(), json_object_keys(), json_each_text(), json_each(), json_to_record(), json_populate_recordset() use such forms. These classes of SQL function calling forms in SQLAlchemy are available using the FunctionElement.table_valued() method in conjunction with Function objects generated from the func namespace.

Examples from PostgreSQL’s reference documentation follow below:

json_populate_record():

json_to_record() - this form uses a PostgreSQL specific form of derived columns in the alias, where we may make use of column() elements with types to produce them. The FunctionElement.table_valued() method produces a TableValuedAlias construct, and the method TableValuedAlias.render_derived() method sets up the derived columns specification:

WITH ORDINALITY - part of the SQL standard, WITH ORDINALITY adds an ordinal counter to the output of a function and is accepted by a limited set of PostgreSQL functions including unnest() and generate_series(). The FunctionElement.table_valued() method accepts a keyword parameter with_ordinality for this purpose, which accepts the string name that will be applied to the “ordinality” column:

Added in version 1.4.0b2.

Table-Valued Functions - in the SQLAlchemy Unified Tutorial

Similar to the table valued function, a column valued function is present in the FROM clause, but delivers itself to the columns clause as a single scalar value. PostgreSQL functions such as json_array_elements(), unnest() and generate_series() may use this form. Column valued functions are available using the FunctionElement.column_valued() method of FunctionElement:

json_array_elements():

unnest() - in order to generate a PostgreSQL ARRAY literal, the array() construct may be used:

The function can of course be used against an existing table-bound column that’s of type ARRAY:

Column Valued Functions - Table Valued Function as a Scalar Column - in the SQLAlchemy Unified Tutorial

Built-in support for rendering a ROW may be approximated using func.ROW with the sqlalchemy.func namespace, or by using the tuple_() construct:

PostgreSQL Row Constructors

PostgreSQL Row Constructor Comparison

PostgreSQL supports passing a table as an argument to a function, which is known as a “record” type. SQLAlchemy FromClause objects such as Table support this special form using the FromClause.table_valued() method, which is comparable to the FunctionElement.table_valued() method except that the collection of columns is already established by that of the FromClause itself:

Added in version 1.4.0b2.

The PostgreSQL dialect supports arrays, both as multidimensional column types as well as array literals:

ARRAY - ARRAY datatype

array - array literal

array_agg() - ARRAY_AGG SQL function

aggregate_order_by - helper for PG’s ORDER BY aggregate function syntax.

The PostgreSQL dialect supports both JSON and JSONB datatypes, including psycopg2’s native support and support for all of PostgreSQL’s special operators:

The PostgreSQL HSTORE type as well as hstore literals are supported:

HSTORE - HSTORE datatype

hstore - hstore literal

PostgreSQL has an independently creatable TYPE structure which is used to implement an enumerated type. This approach introduces significant complexity on the SQLAlchemy side in terms of when this type should be CREATED and DROPPED. The type object is also an independently reflectable entity. The following sections should be consulted:

ENUM - DDL and typing support for ENUM.

PGInspector.get_enums() - retrieve a listing of current ENUM types

ENUM.create() , ENUM.drop() - individual CREATE and DROP commands for ENUM.

The combination of ENUM and ARRAY is not directly supported by backend DBAPIs at this time. Prior to SQLAlchemy 1.3.17, a special workaround was needed in order to allow this combination to work, described below.

Changed in version 1.3.17: The combination of ENUM and ARRAY is now directly handled by SQLAlchemy’s implementation without any workarounds needed.

This type is not included as a built-in type as it would be incompatible with a DBAPI that suddenly decides to support ARRAY of ENUM directly in a new version.

Similar to using ENUM, prior to SQLAlchemy 1.3.17, for an ARRAY of JSON/JSONB we need to render the appropriate CAST. Current psycopg2 drivers accommodate the result set correctly without any special steps.

Changed in version 1.3.17: The combination of JSON/JSONB and ARRAY is now directly handled by SQLAlchemy’s implementation without any workarounds needed.

PostgreSQL range and multirange types are supported for the psycopg, pg8000 and asyncpg dialects; the psycopg2 dialect supports the range types only.

Added in version 2.0.17: Added range and multirange support for the pg8000 dialect. pg8000 1.29.8 or greater is required.

Data values being passed to the database may be passed as string values or by using the Range data object.

Added in version 2.0: Added the backend-agnostic Range object used to indicate ranges. The psycopg2-specific range classes are no longer exposed and are only used internally by that particular dialect.

E.g. an example of a fully typed model using the TSRANGE datatype:

To represent data for the during column above, the Range type is a simple dataclass that will represent the bounds of the range. Below illustrates an INSERT of a row into the above room_booking table:

Selecting from any range column will also return Range objects as indicated:

The available range datatypes are as follows:

Represent a PostgreSQL range.

inherits from typing.Generic

Represent a PostgreSQL range.

The calling style is similar to that of psycopg and psycopg2, in part to allow easier migration from previous SQLAlchemy versions that used these objects directly.

lower¶ – Lower bound value, or None

upper¶ – Upper bound value, or None

bounds¶ – keyword-only, optional string value that is one of "()", "[)", "(]", "[]". Defaults to "[)".

empty¶ – keyword-only, optional bool indicating this is an “empty” range

Added in version 2.0.

Compare this range to the other taking into account bounds inclusivity, returning True if they are equal.

Determine whether this range is adjacent to the other.

Determine whether this range is a contained by other.

Determine whether this range contains value.

Compute the difference between this range and the other.

Compute the intersection of this range with the other.

Determine whether this does not extend to the left of other.

not_extend_right_of()

Determine whether this does not extend to the right of other.

Determine whether this range overlaps with other.

Determine whether this range is completely to the left of other.

Determine whether this range is completely to the right of other.

Compute the union of this range with the other.

Compare this range to the other taking into account bounds inclusivity, returning True if they are equal.

Determine whether this range is adjacent to the other.

Determine whether this range is a contained by other.

Determine whether this range contains value.

Compute the difference between this range and the other.

This raises a ValueError exception if the two ranges are “disjunct”, that is neither adjacent nor overlapping.

Compute the intersection of this range with the other.

Added in version 2.0.10.

A synonym for the ‘empty’ attribute.

A synonym for the ‘empty’ attribute.

Return True if the lower bound is inclusive.

Return True if this range is non-empty and lower bound is infinite.

Determine whether this does not extend to the left of other.

Determine whether this does not extend to the right of other.

Determine whether this range overlaps with other.

Determine whether this range is completely to the left of other.

Determine whether this range is completely to the right of other.

Compute the union of this range with the other.

This raises a ValueError exception if the two ranges are “disjunct”, that is neither adjacent nor overlapping.

Return True if the upper bound is inclusive.

Return True if this range is non-empty and the upper bound is infinite.

Multiranges are supported by PostgreSQL 14 and above. SQLAlchemy’s multirange datatypes deal in lists of Range types.

Multiranges are supported on the psycopg, asyncpg, and pg8000 dialects only. The psycopg2 dialect, which is SQLAlchemy’s default postgresql dialect, does not support multirange datatypes.

Added in version 2.0: Added support for MULTIRANGE datatypes. SQLAlchemy represents a multirange value as a list of Range objects.

Added in version 2.0.17: Added multirange support for the pg8000 dialect. pg8000 1.29.8 or greater is required.

Added in version 2.0.26: MultiRange sequence added.

The example below illustrates use of the TSMULTIRANGE datatype:

Illustrating insertion and selecting of a record:

In the above example, the list of Range types as handled by the ORM will not automatically detect in-place changes to a particular list value; to update list values with the ORM, either re-assign a new list to the attribute, or use the MutableList type modifier. See the section Mutation Tracking for background.

When using a multirange as a literal without specifying the type the utility MultiRange sequence can be used:

Using a simple list instead of MultiRange would require manually setting the type of the literal value to the appropriate multirange type.

Added in version 2.0.26: MultiRange sequence added.

The available multirange datatypes are as follows:

The included networking datatypes are INET, CIDR, MACADDR.

For INET and CIDR datatypes, conditional support is available for these datatypes to send and retrieve Python ipaddress objects including ipaddress.IPv4Network, ipaddress.IPv6Network, ipaddress.IPv4Address, ipaddress.IPv6Address. This support is currently the default behavior of the DBAPI itself, and varies per DBAPI. SQLAlchemy does not yet implement its own network address conversion logic.

The psycopg and asyncpg support these datatypes fully; objects from the ipaddress family are returned in rows by default.

The psycopg2 dialect only sends and receives strings.

The pg8000 dialect supports ipaddress.IPv4Address and ipaddress.IPv6Address objects for the INET datatype, but uses strings for CIDR types.

To normalize all the above DBAPIs to only return strings, use the native_inet_types parameter, passing a value of False:

With the above parameter, the psycopg, asyncpg and pg8000 dialects will disable the DBAPI’s adaptation of these types and will return only strings, matching the behavior of the older psycopg2 dialect.

The parameter may also be set to True, where it will have the effect of raising NotImplementedError for those backends that don’t support, or don’t yet fully support, conversion of rows to Python ipaddress datatypes (currently psycopg2 and pg8000).

Added in version 2.0.18: - added the native_inet_types parameter.

As with all SQLAlchemy dialects, all UPPERCASE types that are known to be valid with PostgreSQL are importable from the top level dialect, whether they originate from sqlalchemy.types or from the local dialect:

Types which are specific to PostgreSQL, or have PostgreSQL-specific construction arguments, are as follows:

Base for PostgreSQL MULTIRANGE types.

Base class for single and multi Range SQL types.

Base for PostgreSQL RANGE types.

PostgreSQL ARRAY type.

Provide the PostgreSQL CITEXT type.

Represent the PostgreSQL DATEMULTIRANGE type.

Represent the PostgreSQL DATERANGE type.

Represent the DOMAIN PostgreSQL type.

PostgreSQL ENUM type.

Represent the PostgreSQL HSTORE type.

Represent the PostgreSQL INT4MULTIRANGE type.

Represent the PostgreSQL INT4RANGE type.

Represent the PostgreSQL INT8MULTIRANGE type.

Represent the PostgreSQL INT8RANGE type.

PostgreSQL INTERVAL type.

Represent the PostgreSQL JSON type.

Represent the PostgreSQL JSONB type.

Provide the PostgreSQL MONEY type.

Represents a multirange sequence.

Represent the PostgreSQL NUMMULTIRANGE type.

Represent the PostgreSQL NUMRANGE type.

Provide the PostgreSQL OID type.

Provide the PostgreSQL REGCLASS type.

Provide the PostgreSQL REGCONFIG type.

PostgreSQL TIME type.

Provide the PostgreSQL TIMESTAMP type.

Represent the PostgreSQL TSRANGE type.

Provide the PostgreSQL TSQUERY type.

Represent the PostgreSQL TSRANGE type.

Represent the PostgreSQL TSTZRANGE type.

Represent the PostgreSQL TSTZRANGE type.

The TSVECTOR type implements the PostgreSQL text search type TSVECTOR.

inherits from sqlalchemy.types.TypeEngine

Base class for single and multi Range SQL types.

Boolean expression. Returns true if the range in the column is adjacent to the range in the operand.

Boolean expression. Returns true if the column is contained within the right hand operand.

Boolean expression. Returns true if the right hand operand, which can be an element or a range, is contained within the column.

Range expression. Returns the union of the two ranges. Will raise an exception if the resulting range is not contiguous.

Range expression. Returns the intersection of the two ranges. Will raise an exception if the resulting range is not contiguous.

Boolean expression. Returns true if the range in the column does not extend left of the range in the operand.

not_extend_right_of()

Boolean expression. Returns true if the range in the column does not extend right of the range in the operand.

Boolean expression. Returns true if the column overlaps (has points in common with) the right hand operand.

Boolean expression. Returns true if the column is strictly left of the right hand operand.

Boolean expression. Returns true if the column is strictly right of the right hand operand.

Range expression. Returns the union of the two ranges. Will raise an exception if the resulting range is not contiguous.

inherits from sqlalchemy.types.Comparator

Define comparison operations for range types.

Boolean expression. Returns true if the range in the column is adjacent to the range in the operand.

Boolean expression. Returns true if the column is contained within the right hand operand.

Boolean expression. Returns true if the right hand operand, which can be an element or a range, is contained within the column.

kwargs may be ignored by this operator but are required for API conformance.

Range expression. Returns the union of the two ranges. Will raise an exception if the resulting range is not contiguous.

Range expression. Returns the intersection of the two ranges. Will raise an exception if the resulting range is not contiguous.

Boolean expression. Returns true if the range in the column does not extend left of the range in the operand.

Boolean expression. Returns true if the range in the column does not extend right of the range in the operand.

Boolean expression. Returns true if the column overlaps (has points in common with) the right hand operand.

Boolean expression. Returns true if the column is strictly left of the right hand operand.

Boolean expression. Returns true if the column is strictly right of the right hand operand.

Range expression. Returns the union of the two ranges. Will raise an exception if the resulting range is not contiguous.

inherits from sqlalchemy.dialects.postgresql.ranges.AbstractRange

Base for PostgreSQL RANGE types.

These are types that return a single Range object.

PostgreSQL range functions

inherits from sqlalchemy.dialects.postgresql.ranges.AbstractRange

Base for PostgreSQL MULTIRANGE types.

these are types that return a sequence of Range objects.

inherits from sqlalchemy.types.ARRAY

PostgreSQL ARRAY type.

The ARRAY type is constructed in the same way as the core ARRAY type; a member type is required, and a number of dimensions is recommended if the type is to be used for more than one dimension:

The ARRAY type provides all operations defined on the core ARRAY type, including support for “dimensions”, indexed access, and simple matching such as Comparator.any() and Comparator.all(). ARRAY class also provides PostgreSQL-specific methods for containment operations, including Comparator.contains() Comparator.contained_by(), and Comparator.overlap(), e.g.:

Indexed access is one-based by default, to match that of PostgreSQL; for zero-based indexed access, set ARRAY.zero_indexes.

Additionally, the ARRAY type does not work directly in conjunction with the ENUM type. For a workaround, see the special type at Using ENUM with ARRAY.

Detecting Changes in ARRAY columns when using the ORM

The ARRAY type, when used with the SQLAlchemy ORM, does not detect in-place mutations to the array. In order to detect these, the sqlalchemy.ext.mutable extension must be used, using the MutableList class:

This extension will allow “in-place” changes such to the array such as .append() to produce events which will be detected by the unit of work. Note that changes to elements inside the array, including subarrays that are mutated in place, are not detected.

Alternatively, assigning a new array value to an ORM element that replaces the old one will always trigger a change event.

ARRAY - base array type

array - produces a literal array value.

Boolean expression. Test if elements are a superset of the elements of the argument array expression.

Boolean expression. Test if elements are a proper subset of the elements of the argument array expression.

Boolean expression. Test if array has elements in common with an argument array expression.

item_type¶ – The data type of items of this array. Note that dimensionality is irrelevant here, so multi-dimensional arrays like INTEGER[][], are constructed as ARRAY(Integer), not as ARRAY(ARRAY(Integer)) or such.

as_tuple=False¶ – Specify whether return results should be converted to tuples from lists. DBAPIs such as psycopg2 return lists by default. When tuples are returned, the results are hashable.

dimensions¶ – if non-None, the ARRAY will assume a fixed number of dimensions. This will cause the DDL emitted for this ARRAY to include the exact number of bracket clauses [], and will also optimize the performance of the type overall. Note that PG arrays are always implicitly “non-dimensioned”, meaning they can store any number of dimensions no matter how they were declared.

zero_indexes=False¶ – when True, index values will be converted between Python zero-based and PostgreSQL one-based indexes, e.g. a value of one will be added to all index values before passing to the database.

inherits from sqlalchemy.types.Comparator

Define comparison operations for ARRAY.

Note that these operations are in addition to those provided by the base Comparator class, including Comparator.any() and Comparator.all().

Boolean expression. Test if elements are a superset of the elements of the argument array expression.

kwargs may be ignored by this operator but are required for API conformance.

Boolean expression. Test if elements are a proper subset of the elements of the argument array expression.

Boolean expression. Test if array has elements in common with an argument array expression.

inherits from sqlalchemy.types.TypeEngine

inherits from sqlalchemy.types.LargeBinary

Construct a LargeBinary type.

inherited from the sqlalchemy.types.LargeBinary.__init__ method of LargeBinary

Construct a LargeBinary type.

length¶ – optional, a length for the column for use in DDL statements, for those binary types that accept a length, such as the MySQL BLOB type.

inherits from sqlalchemy.dialects.postgresql.types._NetworkAddressTypeMixin, sqlalchemy.types.TypeEngine

inherits from sqlalchemy.types.TEXT

Provide the PostgreSQL CITEXT type.

Added in version 2.0.7.

Create a string-holding type.

inherited from the sqlalchemy.types.String.__init__ method of String

Create a string-holding type.

length¶ – optional, a length for the column for use in DDL and CAST expressions. May be safely omitted if no CREATE TABLE will be issued. Certain databases may require a length for use in DDL, and will raise an exception when the CREATE TABLE DDL is issued if a VARCHAR with no length is included. Whether the value is interpreted as bytes or characters is database specific.

Optional, a column-level collation for use in DDL and CAST expressions. Renders using the COLLATE keyword supported by SQLite, MySQL, and PostgreSQL. E.g.:

In most cases, the Unicode or UnicodeText datatypes should be used for a Column that expects to store non-ascii data. These datatypes will ensure that the correct types are used on the database.

inherits from sqlalchemy.dialects.postgresql.named_types.NamedType, sqlalchemy.types.SchemaType

Represent the DOMAIN PostgreSQL type.

A domain is essentially a data type with optional constraints that restrict the allowed set of values. E.g.:

See the PostgreSQL documentation for additional details

Added in version 2.0.

Emit CREATE DDL for this type.

Emit DROP DDL for this type.

name¶ – the name of the domain

data_type¶ – The underlying data type of the domain. This can include array specifiers.

collation¶ – An optional collation for the domain. If no collation is specified, the underlying data type’s default collation is used. The underlying type must be collatable if collation is specified.

default¶ – The DEFAULT clause specifies a default value for columns of the domain data type. The default should be a string or a text() value. If no default value is specified, then the default value is the null value.

constraint_name¶ – An optional name for a constraint. If not specified, the backend generates a name.

not_null¶ – Values of this domain are prevented from being null. By default domain are allowed to be null. If not specified no nullability clause will be emitted.

check¶ – CHECK clause specify integrity constraint or test which values of the domain must satisfy. A constraint must be an expression producing a Boolean result that can use the key word VALUE to refer to the value being tested. Differently from PostgreSQL, only a single check clause is currently allowed in SQLAlchemy.

schema¶ – optional schema name

metadata¶ – optional MetaData object which this DOMAIN will be directly associated

create_type¶ – Defaults to True. Indicates that CREATE TYPE should be emitted, after optionally checking for the presence of the type, when the parent table is being created; and additionally that DROP TYPE is called when the table is dropped.

inherited from the NamedType.create() method of NamedType

Emit CREATE DDL for this type.

bind¶ – a connectable Engine, Connection, or similar object to emit SQL.

checkfirst¶ – if True, a query against the PG catalog will be first performed to see if the type does not exist already before creating.

inherited from the NamedType.drop() method of NamedType

Emit DROP DDL for this type.

bind¶ – a connectable Engine, Connection, or similar object to emit SQL.

checkfirst¶ – if True, a query against the PG catalog will be first performed to see if the type actually exists before dropping.

inherits from sqlalchemy.types.Double

The SQL DOUBLE PRECISION type.

Added in version 2.0.

Double - documentation for the base type.

inherited from the sqlalchemy.types.Float.__init__ method of Float

the numeric precision for use in DDL CREATE TABLE. Backends should attempt to ensure this precision indicates a number of digits for the generic Float datatype.

For the Oracle Database backend, the Float.precision parameter is not accepted when rendering DDL, as Oracle Database does not support float precision specified as a number of decimal places. Instead, use the Oracle Database-specific FLOAT datatype and specify the FLOAT.binary_precision parameter. This is new in version 2.0 of SQLAlchemy.

To create a database agnostic Float that separately specifies binary precision for Oracle Database, use TypeEngine.with_variant() as follows:

asdecimal¶ – the same flag as that of Numeric, but defaults to False. Note that setting this flag to True results in floating point conversion.

decimal_return_scale¶ – Default scale to use when converting from floats to Python decimals. Floating point values will typically be much longer due to decimal inaccuracy, and most floating point database types don’t have a notion of “scale”, so by default the float type looks for the first ten decimal places when converting. Specifying this value will override that length. Note that the MySQL float types, which do include “scale”, will use “scale” as the default for decimal_return_scale, if not otherwise specified.

inherits from sqlalchemy.dialects.postgresql.named_types.NamedType, sqlalchemy.types.NativeForEmulated, sqlalchemy.types.Enum

PostgreSQL ENUM type.

This is a subclass of Enum which includes support for PG’s CREATE TYPE and DROP TYPE.

When the builtin type Enum is used and the Enum.native_enum flag is left at its default of True, the PostgreSQL backend will use a ENUM type as the implementation, so the special create/drop rules will be used.

The create/drop behavior of ENUM is necessarily intricate, due to the awkward relationship the ENUM type has in relationship to the parent table, in that it may be “owned” by just a single table, or may be shared among many tables.

When using Enum or ENUM in an “inline” fashion, the CREATE TYPE and DROP TYPE is emitted corresponding to when the Table.create() and Table.drop() methods are called:

To use a common enumerated type between multiple tables, the best practice is to declare the Enum or ENUM independently, and associate it with the MetaData object itself:

When this pattern is used, care must still be taken at the level of individual table creates. Emitting CREATE TABLE without also specifying checkfirst=True will still cause issues:

If we specify checkfirst=True, the individual table-level create operation will check for the ENUM and create if not exists:

When using a metadata-level ENUM type, the type will always be created and dropped if either the metadata-wide create/drop is called:

The type can also be created and dropped directly:

Emit CREATE TYPE for this ENUM.

Emit DROP TYPE for this ENUM.

Arguments are the same as that of Enum, but also including the following parameters.

create_type¶ – Defaults to True. Indicates that CREATE TYPE should be emitted, after optionally checking for the presence of the type, when the parent table is being created; and additionally that DROP TYPE is called when the table is dropped. When False, no check will be performed and no CREATE TYPE or DROP TYPE is emitted, unless ENUM.create() or ENUM.drop() are called directly. Setting to False is helpful when invoking a creation scheme to a SQL file without access to the actual database - the ENUM.create() and ENUM.drop() methods can be used to emit SQL to a target bind.

Emit CREATE TYPE for this ENUM.

If the underlying dialect does not support PostgreSQL CREATE TYPE, no action is taken.

bind¶ – a connectable Engine, Connection, or similar object to emit SQL.

checkfirst¶ – if True, a query against the PG catalog will be first performed to see if the type does not exist already before creating.

Emit DROP TYPE for this ENUM.

If the underlying dialect does not support PostgreSQL DROP TYPE, no action is taken.

bind¶ – a connectable Engine, Connection, or similar object to emit SQL.

checkfirst¶ – if True, a query against the PG catalog will be first performed to see if the type actually exists before dropping.

inherits from sqlalchemy.types.Indexable, sqlalchemy.types.Concatenable, sqlalchemy.types.TypeEngine

Represent the PostgreSQL HSTORE type.

The HSTORE type stores dictionaries containing strings, e.g.:

HSTORE provides for a wide range of operations, including:

Containment operations:

For a full list of special methods see comparator_factory.

Detecting Changes in HSTORE columns when using the ORM

For usage with the SQLAlchemy ORM, it may be desirable to combine the usage of HSTORE with MutableDict dictionary now part of the sqlalchemy.ext.mutable extension. This extension will allow “in-place” changes to the dictionary, e.g. addition of new keys or replacement/removal of existing keys to/from the current dictionary, to produce events which will be detected by the unit of work:

When the sqlalchemy.ext.mutable extension is not used, the ORM will not be alerted to any changes to the contents of an existing dictionary, unless that dictionary value is re-assigned to the HSTORE-attribute itself, thus generating a change event.

hstore - render the PostgreSQL hstore() function.

Text array expression. Returns array of alternating keys and values.

Boolean expression. Test if keys are a proper subset of the keys of the argument jsonb expression.

Boolean expression. Test if keys (or array) are a superset of/contained the keys of the argument jsonb expression.

Boolean expression. Test for presence of a non-NULL value for the key. Note that the key may be a SQLA expression.

HStore expression. Returns the contents of this hstore with the given key deleted. Note that the key may be a SQLA expression.

Boolean expression. Test for presence of all keys in jsonb

Boolean expression. Test for presence of any key in jsonb

Boolean expression. Test for presence of a key. Note that the key may be a SQLA expression.

Text array expression. Returns array of keys.

Text array expression. Returns array of [key, value] pairs.

HStore expression. Returns a subset of an hstore defined by array of keys.

Text array expression. Returns array of values.

Construct a new HSTORE.

Return a conversion function for processing bind values.

Flag, if False, means values from this type aren’t hashable.

Return a conversion function for processing result row values.

inherits from sqlalchemy.types.Comparator, sqlalchemy.types.Comparator

Define comparison operations for HSTORE.

Text array expression. Returns array of alternating keys and values.

Boolean expression. Test if keys are a proper subset of the keys of the argument jsonb expression.

Boolean expression. Test if keys (or array) are a superset of/contained the keys of the argument jsonb expression.

kwargs may be ignored by this operator but are required for API conformance.

Boolean expression. Test for presence of a non-NULL value for the key. Note that the key may be a SQLA expression.

HStore expression. Returns the contents of this hstore with the given key deleted. Note that the key may be a SQLA expression.

Boolean expression. Test for presence of all keys in jsonb

Boolean expression. Test for presence of any key in jsonb

Boolean expression. Test for presence of a key. Note that the key may be a SQLA expression.

Text array expression. Returns array of keys.

Text array expression. Returns array of [key, value] pairs.

HStore expression. Returns a subset of an hstore defined by array of keys.

Text array expression. Returns array of values.

Construct a new HSTORE.

text_type¶ – the type that should be used for indexed values. Defaults to Text.

Return a conversion function for processing bind values.

Returns a callable which will receive a bind parameter value as the sole positional argument and will return a value to send to the DB-API.

If processing is not necessary, the method should return None.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.bind_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.bind_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_bind_param().

Augmenting Existing Types

dialect¶ – Dialect instance in use.

Flag, if False, means values from this type aren’t hashable.

Used by the ORM when uniquing result lists.

Return a conversion function for processing result row values.

Returns a callable which will receive a result row column value as the sole positional argument and will return a value to return to the user.

If processing is not necessary, the method should return None.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.result_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.result_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_result_value().

Augmenting Existing Types

dialect¶ – Dialect instance in use.

coltype¶ – DBAPI coltype argument received in cursor.description.

inherits from sqlalchemy.dialects.postgresql.types._NetworkAddressTypeMixin, sqlalchemy.types.TypeEngine

inherits from sqlalchemy.types.NativeForEmulated, sqlalchemy.types._AbstractInterval

PostgreSQL INTERVAL type.

Construct an INTERVAL.

Construct an INTERVAL.

precision¶ – optional integer precision value

string fields specifier. allows storage of fields to be limited, such as "YEAR", "MONTH", "DAY TO HOUR", etc.

Added in version 1.2.

inherits from sqlalchemy.types.JSON

Represent the PostgreSQL JSON type.

JSON is used automatically whenever the base JSON datatype is used against a PostgreSQL backend, however base JSON datatype does not provide Python accessors for PostgreSQL-specific comparison methods such as Comparator.astext(); additionally, to use PostgreSQL JSONB, the JSONB datatype should be used explicitly.

JSON - main documentation for the generic cross-platform JSON datatype.

The operators provided by the PostgreSQL version of JSON include:

Index operations (the -> operator):

Index operations returning text (the ->> operator):

Note that equivalent functionality is available via the Comparator.as_string accessor.

Index operations with CAST (equivalent to CAST(col ->> ['some key'] AS <type>)):

Note that equivalent functionality is available via the Comparator.as_integer and similar accessors.

Path index operations (the #> operator):

Path index operations returning text (the #>> operator):

Index operations return an expression object whose type defaults to JSON by default, so that further JSON-oriented instructions may be called upon the result type.

Custom serializers and deserializers are specified at the dialect level, that is using create_engine(). The reason for this is that when using psycopg2, the DBAPI only allows serializers at the per-cursor or per-connection level. E.g.:

When using the psycopg2 dialect, the json_deserializer is registered against the database using psycopg2.extras.register_default_json.

JSON - Core level JSON type

Construct a JSON type.

Render bind casts for BindTyping.RENDER_CASTS mode.

inherits from sqlalchemy.types.Comparator

Define comparison operations for JSON.

On an indexed expression, use the “astext” (e.g. “->>”) conversion when rendered in SQL.

Construct a JSON type.

if True, persist the value None as a SQL NULL value, not the JSON encoding of null. Note that when this flag is False, the null() construct can still be used to persist a NULL value:

astext_type¶ – the type to use for the Comparator.astext accessor on indexed attributes. Defaults to Text.

Render bind casts for BindTyping.RENDER_CASTS mode.

If True, this type (usually a dialect level impl type) signals to the compiler that a cast should be rendered around a bound parameter for this type.

Added in version 2.0.

inherits from sqlalchemy.dialects.postgresql.json.JSON

Represent the PostgreSQL JSONB type.

The JSONB type stores arbitrary JSONB format data, e.g.:

The JSONB type includes all operations provided by JSON, including the same behaviors for indexing operations. It also adds additional operators specific to JSONB, including Comparator.has_key(), Comparator.has_all(), Comparator.has_any(), Comparator.contains(), Comparator.contained_by(), Comparator.delete_path(), Comparator.path_exists() and Comparator.path_match().

Like the JSON type, the JSONB type does not detect in-place changes when used with the ORM, unless the sqlalchemy.ext.mutable extension is used.

Custom serializers and deserializers are shared with the JSON class, using the json_serializer and json_deserializer keyword arguments. These must be specified at the dialect level using create_engine(). When using psycopg2, the serializers are associated with the jsonb type using psycopg2.extras.register_default_jsonb on a per-connection basis, in the same way that psycopg2.extras.register_default_json is used to register these handlers with the json type.

For applications that have indexes against JSONB subscript expressions

SQLAlchemy 2.0.42 made a change in how the subscript operation for JSONB is rendered, from -> 'element' to ['element'], for PostgreSQL versions greater than 14. This change caused an unintended side effect for indexes that were created against expressions that use subscript notation, e.g. Index("ix_entity_json_ab_text", data["a"]["b"].astext). If these indexes were generated with the older syntax e.g. ((entity.data -> 'a') ->> 'b'), they will not be used by the PostgreSQL query planner when a query is made using SQLAlchemy 2.0.42 or higher on PostgreSQL versions 14 or higher. This occurs because the new text will resemble (entity.data['a'] ->> 'b') which will fail to produce the exact textual syntax match required by the PostgreSQL query planner. Therefore, for users upgrading to SQLAlchemy 2.0.42 or higher, existing indexes that were created against JSONB expressions that use subscripting would need to be dropped and re-created in order for them to work with the new query syntax, e.g. an expression like ((entity.data -> 'a') ->> 'b') would become (entity.data['a'] ->> 'b').

#12868 - discussion of this issue

Boolean expression. Test if keys are a proper subset of the keys of the argument jsonb expression (equivalent of the <@ operator).

Boolean expression. Test if keys (or array) are a superset of/contained the keys of the argument jsonb expression (equivalent of the @> operator).

JSONB expression. Deletes field or array element specified in the argument array (equivalent of the #- operator).

Boolean expression. Test for presence of all keys in jsonb (equivalent of the ?& operator)

Boolean expression. Test for presence of any key in jsonb (equivalent of the ?| operator)

Boolean expression. Test for presence of a key (equivalent of the ? operator). Note that the key may be a SQLA expression.

Boolean expression. Test for presence of item given by the argument JSONPath expression (equivalent of the @? operator).

Boolean expression. Test if JSONPath predicate given by the argument JSONPath expression matches (equivalent of the @@ operator).

coerce_compared_value()

Suggest a type for a ‘coerced’ Python value in an expression.

inherits from sqlalchemy.dialects.postgresql.json.Comparator

Define comparison operations for JSON.

Boolean expression. Test if keys are a proper subset of the keys of the argument jsonb expression (equivalent of the <@ operator).

Boolean expression. Test if keys (or array) are a superset of/contained the keys of the argument jsonb expression (equivalent of the @> operator).

kwargs may be ignored by this operator but are required for API conformance.

JSONB expression. Deletes field or array element specified in the argument array (equivalent of the #- operator).

The input may be a list of strings that will be coerced to an ARRAY or an instance of _postgres.array().

Added in version 2.0.

Boolean expression. Test for presence of all keys in jsonb (equivalent of the ?& operator)

Boolean expression. Test for presence of any key in jsonb (equivalent of the ?| operator)

Boolean expression. Test for presence of a key (equivalent of the ? operator). Note that the key may be a SQLA expression.

Boolean expression. Test for presence of item given by the argument JSONPath expression (equivalent of the @? operator).

Added in version 2.0.

Boolean expression. Test if JSONPath predicate given by the argument JSONPath expression matches (equivalent of the @@ operator).

Only the first item of the result is taken into account.

Added in version 2.0.

Suggest a type for a ‘coerced’ Python value in an expression.

Given an operator and value, gives the type a chance to return a type which the value should be coerced into.

The default behavior here is conservative; if the right-hand side is already coerced into a SQL type based on its Python type, it is usually left alone.

End-user functionality extension here should generally be via TypeDecorator, which provides more liberal behavior in that it defaults to coercing the other side of the expression into this type, thus applying special Python conversions above and beyond those needed by the DBAPI to both ides. It also provides the public method TypeDecorator.coerce_compared_value() which is intended for end-user customization of this behavior.

inherits from sqlalchemy.dialects.postgresql.json.JSONPathType

This is usually required to cast literal values to json path when using json search like function, such as jsonb_path_query_array or jsonb_path_exists:

inherits from sqlalchemy.dialects.postgresql.types._NetworkAddressTypeMixin, sqlalchemy.types.TypeEngine

inherits from sqlalchemy.dialects.postgresql.types._NetworkAddressTypeMixin, sqlalchemy.types.TypeEngine

inherits from sqlalchemy.types.TypeEngine

Provide the PostgreSQL MONEY type.

Depending on driver, result rows using this type may return a string value which includes currency symbols.

For this reason, it may be preferable to provide conversion to a numerically-based currency datatype using TypeDecorator:

Alternatively, the conversion may be applied as a CAST using the TypeDecorator.column_expression() method as follows:

Added in version 1.2.

inherits from sqlalchemy.types.TypeEngine

Provide the PostgreSQL OID type.

inherits from sqlalchemy.types.Float

Float - documentation for the base type.

inherited from the sqlalchemy.types.Float.__init__ method of Float

the numeric precision for use in DDL CREATE TABLE. Backends should attempt to ensure this precision indicates a number of digits for the generic Float datatype.

For the Oracle Database backend, the Float.precision parameter is not accepted when rendering DDL, as Oracle Database does not support float precision specified as a number of decimal places. Instead, use the Oracle Database-specific FLOAT datatype and specify the FLOAT.binary_precision parameter. This is new in version 2.0 of SQLAlchemy.

To create a database agnostic Float that separately specifies binary precision for Oracle Database, use TypeEngine.with_variant() as follows:

asdecimal¶ – the same flag as that of Numeric, but defaults to False. Note that setting this flag to True results in floating point conversion.

decimal_return_scale¶ – Default scale to use when converting from floats to Python decimals. Floating point values will typically be much longer due to decimal inaccuracy, and most floating point database types don’t have a notion of “scale”, so by default the float type looks for the first ten decimal places when converting. Specifying this value will override that length. Note that the MySQL float types, which do include “scale”, will use “scale” as the default for decimal_return_scale, if not otherwise specified.

inherits from sqlalchemy.types.TypeEngine

Provide the PostgreSQL REGCONFIG type.

Added in version 2.0.0rc1.

inherits from sqlalchemy.types.TypeEngine

Provide the PostgreSQL REGCLASS type.

Added in version 1.2.7.

inherits from sqlalchemy.types.TIMESTAMP

Provide the PostgreSQL TIMESTAMP type.

Construct a TIMESTAMP.

Construct a TIMESTAMP.

timezone¶ – boolean value if timezone present, default False

optional integer precision value

Added in version 1.4.

inherits from sqlalchemy.types.TIME

PostgreSQL TIME type.

timezone¶ – boolean value if timezone present, default False

optional integer precision value

Added in version 1.4.

inherits from sqlalchemy.types.TypeEngine

Provide the PostgreSQL TSQUERY type.

Added in version 2.0.0rc1.

inherits from sqlalchemy.types.TypeEngine

The TSVECTOR type implements the PostgreSQL text search type TSVECTOR.

It can be used to do full text queries on natural language documents.

inherits from sqlalchemy.types.Uuid, sqlalchemy.types.NativeForEmulated

Represent the SQL UUID type.

This is the SQL-native form of the Uuid database agnostic datatype, and is backwards compatible with the previous PostgreSQL-only version of UUID.

The UUID datatype only works on databases that have a SQL datatype named UUID. It will not function for backends which don’t have this exact-named type, including SQL Server. For backend-agnostic UUID values with native support, including for SQL Server’s UNIQUEIDENTIFIER datatype, use the Uuid datatype.

Added in version 2.0.

Construct a UUID type.

if True, values will be interpreted as Python uuid objects, converting to/from string via the DBAPI.

inherits from sqlalchemy.dialects.postgresql.ranges.AbstractSingleRange

Represent the PostgreSQL INT4RANGE type.

inherits from sqlalchemy.dialects.postgresql.ranges.AbstractSingleRange

Represent the PostgreSQL INT8RANGE type.

inherits from sqlalchemy.dialects.postgresql.ranges.AbstractSingleRange

Represent the PostgreSQL NUMRANGE type.

inherits from sqlalchemy.dialects.postgresql.ranges.AbstractSingleRange

Represent the PostgreSQL DATERANGE type.

inherits from sqlalchemy.dialects.postgresql.ranges.AbstractSingleRange

Represent the PostgreSQL TSRANGE type.

inherits from sqlalchemy.dialects.postgresql.ranges.AbstractSingleRange

Represent the PostgreSQL TSTZRANGE type.

inherits from sqlalchemy.dialects.postgresql.ranges.AbstractMultiRange

Represent the PostgreSQL INT4MULTIRANGE type.

inherits from sqlalchemy.dialects.postgresql.ranges.AbstractMultiRange

Represent the PostgreSQL INT8MULTIRANGE type.

inherits from sqlalchemy.dialects.postgresql.ranges.AbstractMultiRange

Represent the PostgreSQL NUMMULTIRANGE type.

inherits from sqlalchemy.dialects.postgresql.ranges.AbstractMultiRange

Represent the PostgreSQL DATEMULTIRANGE type.

inherits from sqlalchemy.dialects.postgresql.ranges.AbstractMultiRange

Represent the PostgreSQL TSRANGE type.

inherits from sqlalchemy.dialects.postgresql.ranges.AbstractMultiRange

Represent the PostgreSQL TSTZRANGE type.

inherits from builtins.list, typing.Generic

Represents a multirange sequence.

This list subclass is an utility to allow automatic type inference of the proper multi-range SQL type depending on the single range values. This is useful when operating on literal multi-ranges:

Added in version 2.0.26.

Use of a MultiRange sequence to infer the multirange type.

Represent a PostgreSQL aggregate order by expression.

All(other, arrexpr[, operator])

A synonym for the ARRAY-level Comparator.all() method. See that method for details.

Any(other, arrexpr[, operator])

A synonym for the ARRAY-level Comparator.any() method. See that method for details.

A PostgreSQL ARRAY literal.

array_agg(*arg, **kw)

PostgreSQL-specific form of array_agg, ensures return type is ARRAY and not the plain ARRAY, unless an explicit type_ is passed.

Construct an hstore value within a SQL expression using the PostgreSQL hstore() function.

The PostgreSQL phraseto_tsquery SQL function.

The PostgreSQL plainto_tsquery SQL function.

The PostgreSQL to_tsquery SQL function.

The PostgreSQL to_tsvector SQL function.

The PostgreSQL ts_headline SQL function.

The PostgreSQL websearch_to_tsquery SQL function.

inherits from sqlalchemy.sql.expression.ColumnElement

Represent a PostgreSQL aggregate order by expression.

would represent the expression:

Changed in version 1.2.13: - the ORDER BY argument may be multiple terms

inherits from sqlalchemy.sql.expression.ExpressionClauseList

A PostgreSQL ARRAY literal.

This is used to produce ARRAY literals in SQL expressions, e.g.:

An instance of array will always have the datatype ARRAY. The “inner” type of the array is inferred from the values present, unless the array.type_ keyword argument is passed:

When constructing an empty array, the array.type_ argument is particularly important as PostgreSQL server typically requires a cast to be rendered for the inner type in order to render an empty array. SQLAlchemy’s compilation for the empty array will produce this cast so that:

As required by PostgreSQL for empty arrays.

Added in version 2.0.40: added support to render empty PostgreSQL array literals with a required cast.

Multidimensional arrays are produced by nesting array constructs. The dimensionality of the final ARRAY type is calculated by recursively adding the dimensions of the inner ARRAY type:

Added in version 1.3.6: added support for multidimensional array literals

Construct an ARRAY literal.

Construct an ARRAY literal.

clauses¶ – iterable, such as a list, containing elements to be rendered in the array

type_¶ – optional type. If omitted, the type is inferred from the contents of the array.

PostgreSQL-specific form of array_agg, ensures return type is ARRAY and not the plain ARRAY, unless an explicit type_ is passed.

A synonym for the ARRAY-level Comparator.any() method. See that method for details.

A synonym for the ARRAY-level Comparator.all() method. See that method for details.

inherits from sqlalchemy.sql.functions.GenericFunction

Construct an hstore value within a SQL expression using the PostgreSQL hstore() function.

The hstore function accepts one or two arguments as described in the PostgreSQL documentation.

HSTORE - the PostgreSQL HSTORE datatype.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

inherits from sqlalchemy.dialects.postgresql.ext._regconfig_fn

The PostgreSQL to_tsvector SQL function.

This function applies automatic casting of the REGCONFIG argument to use the REGCONFIG datatype automatically, and applies a return type of TSVECTOR.

Assuming the PostgreSQL dialect has been imported, either by invoking from sqlalchemy.dialects import postgresql, or by creating a PostgreSQL engine using create_engine("postgresql..."), to_tsvector will be used automatically when invoking sqlalchemy.func.to_tsvector(), ensuring the correct argument and return type handlers are used at compile and execution time.

Added in version 2.0.0rc1.

inherits from sqlalchemy.dialects.postgresql.ext._regconfig_fn

The PostgreSQL to_tsquery SQL function.

This function applies automatic casting of the REGCONFIG argument to use the REGCONFIG datatype automatically, and applies a return type of TSQUERY.

Assuming the PostgreSQL dialect has been imported, either by invoking from sqlalchemy.dialects import postgresql, or by creating a PostgreSQL engine using create_engine("postgresql..."), to_tsquery will be used automatically when invoking sqlalchemy.func.to_tsquery(), ensuring the correct argument and return type handlers are used at compile and execution time.

Added in version 2.0.0rc1.

inherits from sqlalchemy.dialects.postgresql.ext._regconfig_fn

The PostgreSQL plainto_tsquery SQL function.

This function applies automatic casting of the REGCONFIG argument to use the REGCONFIG datatype automatically, and applies a return type of TSQUERY.

Assuming the PostgreSQL dialect has been imported, either by invoking from sqlalchemy.dialects import postgresql, or by creating a PostgreSQL engine using create_engine("postgresql..."), plainto_tsquery will be used automatically when invoking sqlalchemy.func.plainto_tsquery(), ensuring the correct argument and return type handlers are used at compile and execution time.

Added in version 2.0.0rc1.

inherits from sqlalchemy.dialects.postgresql.ext._regconfig_fn

The PostgreSQL phraseto_tsquery SQL function.

This function applies automatic casting of the REGCONFIG argument to use the REGCONFIG datatype automatically, and applies a return type of TSQUERY.

Assuming the PostgreSQL dialect has been imported, either by invoking from sqlalchemy.dialects import postgresql, or by creating a PostgreSQL engine using create_engine("postgresql..."), phraseto_tsquery will be used automatically when invoking sqlalchemy.func.phraseto_tsquery(), ensuring the correct argument and return type handlers are used at compile and execution time.

Added in version 2.0.0rc1.

inherits from sqlalchemy.dialects.postgresql.ext._regconfig_fn

The PostgreSQL websearch_to_tsquery SQL function.

This function applies automatic casting of the REGCONFIG argument to use the REGCONFIG datatype automatically, and applies a return type of TSQUERY.

Assuming the PostgreSQL dialect has been imported, either by invoking from sqlalchemy.dialects import postgresql, or by creating a PostgreSQL engine using create_engine("postgresql..."), websearch_to_tsquery will be used automatically when invoking sqlalchemy.func.websearch_to_tsquery(), ensuring the correct argument and return type handlers are used at compile and execution time.

Added in version 2.0.0rc1.

inherits from sqlalchemy.dialects.postgresql.ext._regconfig_fn

The PostgreSQL ts_headline SQL function.

This function applies automatic casting of the REGCONFIG argument to use the REGCONFIG datatype automatically, and applies a return type of TEXT.

Assuming the PostgreSQL dialect has been imported, either by invoking from sqlalchemy.dialects import postgresql, or by creating a PostgreSQL engine using create_engine("postgresql..."), ts_headline will be used automatically when invoking sqlalchemy.func.ts_headline(), ensuring the correct argument and return type handlers are used at compile and execution time.

Added in version 2.0.0rc1.

SQLAlchemy supports PostgreSQL EXCLUDE constraints via the ExcludeConstraint class:

A table-level EXCLUDE constraint.

inherits from sqlalchemy.schema.ColumnCollectionConstraint

A table-level EXCLUDE constraint.

Defines an EXCLUDE constraint as described in the PostgreSQL documentation.

Create an ExcludeConstraint object.

Create an ExcludeConstraint object.

The constraint is normally embedded into the Table construct directly, or added later using append_constraint():

The exclude constraint defined in this example requires the btree_gist extension, that can be created using the command CREATE EXTENSION btree_gist;.

A sequence of two tuples of the form (column, operator) where “column” is either a Column object, or a SQL expression element (e.g. func.int8range(table.from, table.to)) or the name of a column as string, and “operator” is a string containing the operator to use (e.g. “&&” or “=”).

In order to specify a column name when a Column object is not available, while ensuring that any necessary quoting rules take effect, an ad-hoc Column or column() object should be used. The column may also be a string SQL expression when passed as literal_column() or text()

name¶ – Optional, the in-database name of this constraint.

deferrable¶ – Optional bool. If set, emit DEFERRABLE or NOT DEFERRABLE when issuing DDL for this constraint.

initially¶ – Optional string. If set, emit INITIALLY <value> when issuing DDL for this constraint.

using¶ – Optional string. If set, emit USING <index_method> when issuing DDL for this constraint. Defaults to ‘gist’.

where¶ – Optional SQL expression construct or literal SQL string. If set, emit WHERE <predicate> when issuing DDL for this constraint.

Optional dictionary. Used to define operator classes for the elements; works the same way as that of the postgresql_ops parameter specified to the Index construct.

Added in version 1.3.21.

Operator Classes - general description of how PostgreSQL operator classes are specified.

Construct a PostgreSQL-specific variant Insert construct.

PostgreSQL-specific implementation of INSERT.

Construct a PostgreSQL-specific variant Insert construct.

The sqlalchemy.dialects.postgresql.insert() function creates a sqlalchemy.dialects.postgresql.Insert. This class is based on the dialect-agnostic Insert construct which may be constructed using the insert() function in SQLAlchemy Core.

The Insert construct includes additional methods Insert.on_conflict_do_update(), Insert.on_conflict_do_nothing().

inherits from sqlalchemy.sql.expression.Insert

PostgreSQL-specific implementation of INSERT.

Adds methods for PG-specific syntaxes such as ON CONFLICT.

The Insert object is created using the sqlalchemy.dialects.postgresql.insert() function.

Provide the excluded namespace for an ON CONFLICT statement

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

on_conflict_do_nothing()

Specifies a DO NOTHING action for ON CONFLICT clause.

on_conflict_do_update()

Specifies a DO UPDATE SET action for ON CONFLICT clause.

Provide the excluded namespace for an ON CONFLICT statement

PG’s ON CONFLICT clause allows reference to the row that would be inserted, known as excluded. This attribute provides all columns in this row to be referenceable.

The Insert.excluded attribute is an instance of ColumnCollection, which provides an interface the same as that of the Table.c collection described at Accessing Tables and Columns. With this collection, ordinary names are accessible like attributes (e.g. stmt.excluded.some_column), but special names and dictionary method names should be accessed using indexed access, such as stmt.excluded["column name"] or stmt.excluded["values"]. See the docstring for ColumnCollection for further examples.

INSERT…ON CONFLICT (Upsert) - example of how to use Insert.excluded

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

Specifies a DO NOTHING action for ON CONFLICT clause.

The constraint and index_elements arguments are optional, but only one of these can be specified.

constraint¶ – The name of a unique or exclusion constraint on the table, or the constraint object itself if it has a .name attribute.

index_elements¶ – A sequence consisting of string column names, Column objects, or other column expression objects that will be used to infer a target index.

index_where¶ – Additional WHERE criterion that can be used to infer a conditional target index.

INSERT…ON CONFLICT (Upsert)

Specifies a DO UPDATE SET action for ON CONFLICT clause.

Either the constraint or index_elements argument is required, but only one of these can be specified.

constraint¶ – The name of a unique or exclusion constraint on the table, or the constraint object itself if it has a .name attribute.

index_elements¶ – A sequence consisting of string column names, Column objects, or other column expression objects that will be used to infer a target index.

index_where¶ – Additional WHERE criterion that can be used to infer a conditional target index.

A dictionary or other mapping object where the keys are either names of columns in the target table, or Column objects or other ORM-mapped columns matching that of the target table, and expressions or literals as values, specifying the SET actions to take.

Added in version 1.4: The Insert.on_conflict_do_update.set_ parameter supports Column objects from the target Table as keys.

This dictionary does not take into account Python-specified default UPDATE values or generation functions, e.g. those specified using Column.onupdate. These values will not be exercised for an ON CONFLICT style of UPDATE, unless they are manually specified in the Insert.on_conflict_do_update.set_ dictionary.

where¶ – Optional argument. An expression object representing a WHERE clause that restricts the rows affected by DO UPDATE SET. Rows not meeting the WHERE condition will not be updated (effectively a DO NOTHING for those rows).

INSERT…ON CONFLICT (Upsert)

Support for the PostgreSQL database via the psycopg2 driver.

Documentation and download information (if applicable) for psycopg2 is available at: https://pypi.org/project/psycopg2/

Keyword arguments that are specific to the SQLAlchemy psycopg2 dialect may be passed to create_engine(), and include the following:

isolation_level: This option, available for all PostgreSQL dialects, includes the AUTOCOMMIT isolation level when using the psycopg2 dialect. This option sets the default isolation level for the connection that is set immediately upon connection to the database before the connection is pooled. This option is generally superseded by the more modern Connection.execution_options.isolation_level execution option, detailed at Setting Transaction Isolation Levels including DBAPI Autocommit.

Psycopg2 Transaction Isolation Level

Setting Transaction Isolation Levels including DBAPI Autocommit

client_encoding: sets the client encoding in a libpq-agnostic way, using psycopg2’s set_client_encoding() method.

Unicode with Psycopg2

executemany_mode, executemany_batch_page_size, executemany_values_page_size: Allows use of psycopg2 extensions for optimizing “executemany”-style queries. See the referenced section below for details.

Psycopg2 Fast Execution Helpers

The above keyword arguments are dialect keyword arguments, meaning that they are passed as explicit keyword arguments to create_engine():

These should not be confused with DBAPI connect arguments, which are passed as part of the create_engine.connect_args dictionary and/or are passed in the URL query string, as detailed in the section Custom DBAPI connect() arguments / on-connect routines.

The psycopg2 module has a connection argument named sslmode for controlling its behavior regarding secure (SSL) connections. The default is sslmode=prefer; it will attempt an SSL connection and if that fails it will fall back to an unencrypted connection. sslmode=require may be used to ensure that only secure connections are established. Consult the psycopg2 / libpq documentation for further options that are available.

Note that sslmode is specific to psycopg2 so it is included in the connection URI:

psycopg2 supports connecting via Unix domain connections. When the host portion of the URL is omitted, SQLAlchemy passes None to psycopg2, which specifies Unix-domain communication rather than TCP/IP communication:

By default, the socket file used is to connect to a Unix-domain socket in /tmp, or whatever socket directory was specified when PostgreSQL was built. This value can be overridden by passing a pathname to psycopg2, using host as an additional keyword argument:

The format accepted here allows for a hostname in the main URL in addition to the “host” query string argument. When using this URL format, the initial host is silently ignored. That is, this URL:

Above, the hostname myhost1 is silently ignored and discarded. The host which is connected is the myhost2 host.

This is to maintain some degree of compatibility with PostgreSQL’s own URL format which has been tested to behave the same way and for which tools like PifPaf hardcode two hostnames.

psycopg2 supports multiple connection points in the connection string. When the host parameter is used multiple times in the query section of the URL, SQLAlchemy will create a single string of the host and port information provided to make the connections. Tokens may consist of host::port or just host; in the latter case, the default port is selected by libpq. In the example below, three host connections are specified, for HostA::PortA, HostB connecting to the default port, and HostC::PortC:

As an alternative, libpq query string format also may be used; this specifies host and port as single query string arguments with comma-separated lists - the default port can be chosen by indicating an empty value in the comma separated list:

With either URL style, connections to each host is attempted based on a configurable strategy, which may be configured using the libpq target_session_attrs parameter. Per libpq this defaults to any which indicates a connection to each host is then attempted until a connection is successful. Other strategies include primary, prefer-standby, etc. The complete list is documented by PostgreSQL at libpq connection strings.

For example, to indicate two hosts using the primary strategy:

Changed in version 1.4.40: Port specification in psycopg2 multiple host format is repaired, previously ports were not correctly interpreted in this context. libpq comma-separated format is also now supported.

Added in version 1.3.20: Support for multiple hosts in PostgreSQL connection string.

libpq connection strings - please refer to this section in the libpq documentation for complete background on multiple host support.

The psycopg2 DBAPI can connect to PostgreSQL by passing an empty DSN to the libpq client library, which by default indicates to connect to a localhost PostgreSQL database that is open for “trust” connections. This behavior can be further tailored using a particular set of environment variables which are prefixed with PG_..., which are consumed by libpq to take the place of any or all elements of the connection string.

For this form, the URL can be passed without any elements other than the initial scheme:

In the above form, a blank “dsn” string is passed to the psycopg2.connect() function which in turn represents an empty DSN passed to libpq.

Added in version 1.3.2: support for parameter-less connections with psycopg2.

Environment Variables - PostgreSQL documentation on how to use PG_... environment variables for connections.

The following DBAPI-specific options are respected when used with Connection.execution_options(), Executable.execution_options(), Query.execution_options(), in addition to those not specific to DBAPIs:

isolation_level - Set the transaction isolation level for the lifespan of a Connection (can only be set on a connection, not a statement or query). See Psycopg2 Transaction Isolation Level.

stream_results - Enable or disable usage of psycopg2 server side cursors - this feature makes use of “named” cursors in combination with special result handling methods so that result rows are not fully buffered. Defaults to False, meaning cursors are buffered by default.

max_row_buffer - when using stream_results, an integer value that specifies the maximum number of rows to buffer at a time. This is interpreted by the BufferedRowCursorResult, and if omitted the buffer will grow to ultimately store 1000 rows at a time.

Changed in version 1.4: The max_row_buffer size can now be greater than 1000, and the buffer will grow to that size.

Modern versions of psycopg2 include a feature known as Fast Execution Helpers , which have been shown in benchmarking to improve psycopg2’s executemany() performance, primarily with INSERT statements, by at least an order of magnitude.

SQLAlchemy implements a native form of the “insert many values” handler that will rewrite a single-row INSERT statement to accommodate for many values at once within an extended VALUES clause; this handler is equivalent to psycopg2’s execute_values() handler; an overview of this feature and its configuration are at “Insert Many Values” Behavior for INSERT statements.

Added in version 2.0: Replaced psycopg2’s execute_values() fast execution helper with a native SQLAlchemy mechanism known as insertmanyvalues.

The psycopg2 dialect retains the ability to use the psycopg2-specific execute_batch() feature, although it is not expected that this is a widely used feature. The use of this extension may be enabled using the executemany_mode flag which may be passed to create_engine():

Possible options for executemany_mode include:

values_only - this is the default value. SQLAlchemy’s native insertmanyvalues handler is used for qualifying INSERT statements, assuming create_engine.use_insertmanyvalues is left at its default value of True. This handler rewrites simple INSERT statements to include multiple VALUES clauses so that many parameter sets can be inserted with one statement.

'values_plus_batch'- SQLAlchemy’s native insertmanyvalues handler is used for qualifying INSERT statements, assuming create_engine.use_insertmanyvalues is left at its default value of True. Then, psycopg2’s execute_batch() handler is used for qualifying UPDATE and DELETE statements when executed with multiple parameter sets. When using this mode, the CursorResult.rowcount attribute will not contain a value for executemany-style executions against UPDATE and DELETE statements.

Changed in version 2.0: Removed the 'batch' and 'None' options from psycopg2 executemany_mode. Control over batching for INSERT statements is now configured via the create_engine.use_insertmanyvalues engine-level parameter.

The term “qualifying statements” refers to the statement being executed being a Core insert(), update() or delete() construct, and not a plain textual SQL string or one constructed using text(). It also may not be a special “extension” statement such as an “ON CONFLICT” “upsert” statement. When using the ORM, all insert/update/delete statements used by the ORM flush process are qualifying.

The “page size” for the psycopg2 “batch” strategy can be affected by using the executemany_batch_page_size parameter, which defaults to 100.

For the “insertmanyvalues” feature, the page size can be controlled using the create_engine.insertmanyvalues_page_size parameter, which defaults to 1000. An example of modifying both parameters is below:

“Insert Many Values” Behavior for INSERT statements - background on “insertmanyvalues”

Sending Multiple Parameters - General information on using the Connection object to execute statements in such a way as to make use of the DBAPI .executemany() method.

The psycopg2 DBAPI driver supports Unicode data transparently.

The client character encoding can be controlled for the psycopg2 dialect in the following ways:

For PostgreSQL 9.1 and above, the client_encoding parameter may be passed in the database URL; this parameter is consumed by the underlying libpq PostgreSQL client library:

Alternatively, the above client_encoding value may be passed using create_engine.connect_args for programmatic establishment with libpq:

For all PostgreSQL versions, psycopg2 supports a client-side encoding value that will be passed to database connections when they are first established. The SQLAlchemy psycopg2 dialect supports this using the client_encoding parameter passed to create_engine():

The above client_encoding parameter admittedly is very similar in appearance to usage of the parameter within the create_engine.connect_args dictionary; the difference above is that the parameter is consumed by psycopg2 and is passed to the database connection using SET client_encoding TO 'utf8'; in the previously mentioned style, the parameter is instead passed through psycopg2 and consumed by the libpq library.

A common way to set up client encoding with PostgreSQL databases is to ensure it is configured within the server-side postgresql.conf file; this is the recommended way to set encoding for a server that is consistently of one encoding in all databases:

The psycopg2 dialect fully supports SAVEPOINT and two-phase commit operations.

As discussed in Transaction Isolation Level, all PostgreSQL dialects support setting of transaction isolation level both via the isolation_level parameter passed to create_engine() , as well as the isolation_level argument used by Connection.execution_options(). When using the psycopg2 dialect , these options make use of psycopg2’s set_isolation_level() connection method, rather than emitting a PostgreSQL directive; this is because psycopg2’s API-level setting is always emitted at the start of each transaction in any case.

The psycopg2 dialect supports these constants for isolation level:

Transaction Isolation Level

pg8000 Transaction Isolation Level

The psycopg2 dialect will log PostgreSQL NOTICE messages via the sqlalchemy.dialects.postgresql logger. When this logger is set to the logging.INFO level, notice messages will be logged:

Above, it is assumed that logging is configured externally. If this is not the case, configuration such as logging.basicConfig() must be utilized:

Logging HOWTO - on the python.org website

The psycopg2 DBAPI includes an extension to natively handle marshalling of the HSTORE type. The SQLAlchemy psycopg2 dialect will enable this extension by default when psycopg2 version 2.4 or greater is used, and it is detected that the target database has the HSTORE type set up for use. In other words, when the dialect makes the first connection, a sequence like the following is performed:

Request the available HSTORE oids using psycopg2.extras.HstoreAdapter.get_oids(). If this function returns a list of HSTORE identifiers, we then determine that the HSTORE extension is present. This function is skipped if the version of psycopg2 installed is less than version 2.4.

If the use_native_hstore flag is at its default of True, and we’ve detected that HSTORE oids are available, the psycopg2.extensions.register_hstore() extension is invoked for all connections.

The register_hstore() extension has the effect of all Python dictionaries being accepted as parameters regardless of the type of target column in SQL. The dictionaries are converted by this extension into a textual HSTORE expression. If this behavior is not desired, disable the use of the hstore extension by setting use_native_hstore to False as follows:

The HSTORE type is still supported when the psycopg2.extensions.register_hstore() extension is not used. It merely means that the coercion between Python dictionaries and the HSTORE string format, on both the parameter side and the result side, will take place within SQLAlchemy’s own marshalling logic, and not that of psycopg2 which may be more performant.

Support for the PostgreSQL database via the psycopg (a.k.a. psycopg 3) driver.

Documentation and download information (if applicable) for psycopg (a.k.a. psycopg 3) is available at: https://pypi.org/project/psycopg/

psycopg is the package and module name for version 3 of the psycopg database driver, formerly known as psycopg2. This driver is different enough from its psycopg2 predecessor that SQLAlchemy supports it via a totally separate dialect; support for psycopg2 is expected to remain for as long as that package continues to function for modern Python versions, and also remains the default dialect for the postgresql:// dialect series.

The SQLAlchemy psycopg dialect provides both a sync and an async implementation under the same dialect name. The proper version is selected depending on how the engine is created:

calling create_engine() with postgresql+psycopg://... will automatically select the sync version, e.g.:

calling create_async_engine() with postgresql+psycopg://... will automatically select the async version, e.g.:

The asyncio version of the dialect may also be specified explicitly using the psycopg_async suffix, as:

psycopg2 - The SQLAlchemy psycopg dialect shares most of its behavior with the psycopg2 dialect. Further documentation is available there.

The psycopg driver provides its own connection pool implementation that may be used in place of SQLAlchemy’s pooling functionality. This pool implementation provides support for fixed and dynamic pool sizes (including automatic downsizing for unused connections), connection health pre-checks, and support for both synchronous and asynchronous code environments.

Here is an example that uses the sync version of the pool, using psycopg_pool >= 3.3 that introduces support for close_returns=True:

Similarly an the async example:

The resulting engine may then be used normally. Internally, Psycopg 3 handles connection pooling:

Connection pools - the Psycopg 3 documentation for psycopg_pool.ConnectionPool.

Example for older version of psycopg_pool - An example about using the psycopg_pool<3.3 that did not have the close_returns` parameter.

One of the differences between psycopg and the older psycopg2 is how bound parameters are handled: psycopg2 would bind them client side, while psycopg by default will bind them server side.

It’s possible to configure psycopg to do client side binding by specifying the cursor_factory to be ClientCursor when creating the engine:

Similarly when using an async engine the AsyncClientCursor can be specified:

Client-side-binding cursors

Support for the PostgreSQL database via the pg8000 driver.

Documentation and download information (if applicable) for pg8000 is available at: https://pypi.org/project/pg8000/

Changed in version 1.4: The pg8000 dialect has been updated for version 1.16.6 and higher, and is again part of SQLAlchemy’s continuous integration with full feature support.

pg8000 will encode / decode string values between it and the server using the PostgreSQL client_encoding parameter; by default this is the value in the postgresql.conf file, which often defaults to SQL_ASCII. Typically, this can be changed to utf-8, as a more useful default:

The client_encoding can be overridden for a session by executing the SQL:

SQLAlchemy will execute this SQL on all new connections based on the value passed to create_engine() using the client_encoding parameter:

pg8000 accepts a Python SSLContext object which may be specified using the create_engine.connect_args dictionary:

If the server uses an automatically-generated certificate that is self-signed or does not match the host name (as seen from the client), it may also be necessary to disable hostname checking:

The pg8000 dialect offers the same isolation level settings as that of the psycopg2 dialect:

Transaction Isolation Level

Psycopg2 Transaction Isolation Level

Support for the PostgreSQL database via the asyncpg driver.

Documentation and download information (if applicable) for asyncpg is available at: https://magicstack.github.io/asyncpg/

The asyncpg dialect is SQLAlchemy’s first Python asyncio dialect.

Using a special asyncio mediation layer, the asyncpg dialect is usable as the backend for the SQLAlchemy asyncio extension package.

This dialect should normally be used only with the create_async_engine() engine creation function:

Added in version 1.4.

By default asyncpg does not decode the json and jsonb types and returns them as strings. SQLAlchemy sets default type decoder for json and jsonb types using the python builtin json.loads function. The json implementation used can be changed by setting the attribute json_deserializer when creating the engine with create_engine() or create_async_engine().

The asyncpg dialect features support for multiple fallback hosts in the same way as that of the psycopg2 and psycopg dialects. The syntax is the same, using host=<host>:<port> combinations as additional query string arguments; however, there is no default port, so all hosts must have a complete port number present, otherwise an exception is raised:

For complete background on this syntax, see Specifying multiple fallback hosts.

Added in version 2.0.18.

Specifying multiple fallback hosts

The asyncpg SQLAlchemy dialect makes use of asyncpg.connection.prepare() for all statements. The prepared statement objects are cached after construction which appears to grant a 10% or more performance improvement for statement invocation. The cache is on a per-DBAPI connection basis, which means that the primary storage for prepared statements is within DBAPI connections pooled within the connection pool. The size of this cache defaults to 100 statements per DBAPI connection and may be adjusted using the prepared_statement_cache_size DBAPI argument (note that while this argument is implemented by SQLAlchemy, it is part of the DBAPI emulation portion of the asyncpg dialect, therefore is handled as a DBAPI argument, not a dialect argument):

To disable the prepared statement cache, use a value of zero:

Added in version 1.4.0b2: Added prepared_statement_cache_size for asyncpg.

The asyncpg database driver necessarily uses caches for PostgreSQL type OIDs, which become stale when custom PostgreSQL datatypes such as ENUM objects are changed via DDL operations. Additionally, prepared statements themselves which are optionally cached by SQLAlchemy’s driver as described above may also become “stale” when DDL has been emitted to the PostgreSQL database which modifies the tables or other objects involved in a particular prepared statement.

The SQLAlchemy asyncpg dialect will invalidate these caches within its local process when statements that represent DDL are emitted on a local connection, but this is only controllable within a single Python process / database engine. If DDL changes are made from other database engines and/or processes, a running application may encounter asyncpg exceptions InvalidCachedStatementError and/or InternalServerError("cache lookup failed for type <oid>") if it refers to pooled database connections which operated upon the previous structures. The SQLAlchemy asyncpg dialect will recover from these error cases when the driver raises these exceptions by clearing its internal caches as well as those of the asyncpg driver in response to them, but cannot prevent them from being raised in the first place if the cached prepared statement or asyncpg type caches have gone stale, nor can it retry the statement as the PostgreSQL transaction is invalidated when these errors occur.

By default, asyncpg enumerates prepared statements in numeric order, which can lead to errors if a name has already been taken for another prepared statement. This issue can arise if your application uses database proxies such as PgBouncer to handle connections. One possible workaround is to use dynamic prepared statement names, which asyncpg now supports through an optional name value for the statement name. This allows you to generate your own unique names that won’t conflict with existing ones. To achieve this, you can provide a function that will be called every time a prepared statement is prepared:

https://github.com/MagicStack/asyncpg/issues/837

https://github.com/sqlalchemy/sqlalchemy/issues/6467

When using PGBouncer, to prevent a buildup of useless prepared statements in your application, it’s important to use the NullPool pool class, and to configure PgBouncer to use DISCARD when returning connections. The DISCARD command is used to release resources held by the db connection, including prepared statements. Without proper setup, prepared statements can accumulate quickly and cause performance issues.

Asyncpg has an issue when using PostgreSQL ENUM datatypes, where upon the creation of new database connections, an expensive query may be emitted in order to retrieve metadata regarding custom types which has been shown to negatively affect performance. To mitigate this issue, the PostgreSQL “jit” setting may be disabled from the client using this setting passed to create_async_engine():

https://github.com/MagicStack/asyncpg/issues/727

Support for the PostgreSQL database via the psycopg2cffi driver.

Documentation and download information (if applicable) for psycopg2cffi is available at: https://pypi.org/project/psycopg2cffi/

psycopg2cffi is an adaptation of psycopg2, using CFFI for the C layer. This makes it suitable for use in e.g. PyPy. Documentation is as per psycopg2.

sqlalchemy.dialects.postgresql.psycopg2

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (unknown):
```unknown
Table(
    "sometable",
    metadata,
    Column(
        "id", Integer, Sequence("some_id_seq", start=1), primary_key=True
    ),
)
```

Example 2 (python):
```python
from sqlalchemy import Table, Column, MetaData, Integer, Computed

metadata = MetaData()

data = Table(
    "data",
    metadata,
    Column(
        "id", Integer, Identity(start=42, cycle=True), primary_key=True
    ),
    Column("data", String),
)
```

Example 3 (sql):
```sql
CREATE TABLE data (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY (START WITH 42 CYCLE),
    data VARCHAR,
    PRIMARY KEY (id)
)
```

Example 4 (python):
```python
from sqlalchemy.schema import CreateColumn
from sqlalchemy.ext.compiler import compiles


@compiles(CreateColumn, "postgresql")
def use_identity(element, compiler, **kw):
    text = compiler.visit_create_column(element, **kw)
    text = text.replace("SERIAL", "INT GENERATED BY DEFAULT AS IDENTITY")
    return text
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/dialects/mysql.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - Dialects
    - Project Versions
- MySQL and MariaDB¶
- DBAPI Support¶
- Supported Versions and Features¶
  - MariaDB Support¶
  - MariaDB-Only Mode¶
- Connection Timeouts and Disconnects¶

Home | Download this Documentation

Home | Download this Documentation

Support for the MySQL / MariaDB database.

The following table summarizes current support levels for database release versions.

The following dialect/DBAPI options are available. Please refer to individual DBAPI sections for connect information.

mysqlclient (maintained fork of MySQL-Python)

MariaDB Connector/Python

MySQL Connector/Python

SQLAlchemy supports MySQL starting with version 5.0.2 through modern releases, as well as all modern versions of MariaDB. See the official MySQL documentation for detailed information about features supported in any given server release.

Changed in version 1.4: minimum MySQL version supported is now 5.0.2.

The MariaDB variant of MySQL retains fundamental compatibility with MySQL’s protocols however the development of these two products continues to diverge. Within the realm of SQLAlchemy, the two databases have a small number of syntactical and behavioral differences that SQLAlchemy accommodates automatically. To connect to a MariaDB database, no changes to the database URL are required:

Upon first connect, the SQLAlchemy dialect employs a server version detection scheme that determines if the backing database reports as MariaDB. Based on this flag, the dialect can make different choices in those of areas where its behavior must be different.

The dialect also supports an optional “MariaDB-only” mode of connection, which may be useful for the case where an application makes use of MariaDB-specific features and is not compatible with a MySQL database. To use this mode of operation, replace the “mysql” token in the above URL with “mariadb”:

The above engine, upon first connect, will raise an error if the server version detection detects that the backing database is not MariaDB.

When using an engine with "mariadb" as the dialect name, all mysql-specific options that include the name “mysql” in them are now named with “mariadb”. This means options like mysql_engine should be named mariadb_engine, etc. Both “mysql” and “mariadb” options can be used simultaneously for applications that use URLs with both “mysql” and “mariadb” dialects:

Similar behavior will occur when the above structures are reflected, i.e. the “mariadb” prefix will be present in the option names when the database URL is based on the “mariadb” name.

Added in version 1.4: Added “mariadb” dialect name supporting “MariaDB-only mode” for the MySQL dialect.

MySQL / MariaDB feature an automatic connection close behavior, for connections that have been idle for a fixed period of time, defaulting to eight hours. To circumvent having this issue, use the create_engine.pool_recycle option which ensures that a connection will be discarded and replaced with a new one if it has been present in the pool for a fixed number of seconds:

For more comprehensive disconnect detection of pooled connections, including accommodation of server restarts and network issues, a pre-ping approach may be employed. See Dealing with Disconnects for current approaches.

Dealing with Disconnects - Background on several techniques for dealing with timed out connections as well as database restarts.

Both MySQL’s and MariaDB’s CREATE TABLE syntax includes a wide array of special options, including ENGINE, CHARSET, MAX_ROWS, ROW_FORMAT, INSERT_METHOD, and many more. To accommodate the rendering of these arguments, specify the form mysql_argument_name="value". For example, to specify a table with ENGINE of InnoDB, CHARSET of utf8mb4, and KEY_BLOCK_SIZE of 1024:

When supporting MariaDB-Only Mode mode, similar keys against the “mariadb” prefix must be included as well. The values can of course vary independently so that different settings on MySQL vs. MariaDB may be maintained:

The MySQL / MariaDB dialects will normally transfer any keyword specified as mysql_keyword_name to be rendered as KEYWORD_NAME in the CREATE TABLE statement. A handful of these names will render with a space instead of an underscore; to support this, the MySQL dialect has awareness of these particular names, which include DATA DIRECTORY (e.g. mysql_data_directory), CHARACTER SET (e.g. mysql_character_set) and INDEX DIRECTORY (e.g. mysql_index_directory).

The most common argument is mysql_engine, which refers to the storage engine for the table. Historically, MySQL server installations would default to MyISAM for this value, although newer versions may be defaulting to InnoDB. The InnoDB engine is typically preferred for its support of transactions and foreign keys.

A Table that is created in a MySQL / MariaDB database with a storage engine of MyISAM will be essentially non-transactional, meaning any INSERT/UPDATE/DELETE statement referring to this table will be invoked as autocommit. It also will have no support for foreign key constraints; while the CREATE TABLE statement accepts foreign key options, when using the MyISAM storage engine these arguments are discarded. Reflecting such a table will also produce no foreign key constraint information.

For fully atomic transactions as well as support for foreign key constraints, all participating CREATE TABLE statements must specify a transactional engine, which in the vast majority of cases is InnoDB.

Partitioning can similarly be specified using similar options. In the example below the create table will specify PARTITION_BY, PARTITIONS, SUBPARTITIONS and SUBPARTITION_BY:

Both MySQL and MariaDB have inconsistent support for case-sensitive identifier names, basing support on specific details of the underlying operating system. However, it has been observed that no matter what case sensitivity behavior is present, the names of tables in foreign key declarations are always received from the database as all-lower case, making it impossible to accurately reflect a schema where inter-related tables use mixed-case identifier names.

Therefore it is strongly advised that table names be declared as all lower case both within SQLAlchemy as well as on the MySQL / MariaDB database itself, especially if database reflection features are to be used.

All MySQL / MariaDB dialects support setting of transaction isolation level both via a dialect-specific parameter create_engine.isolation_level accepted by create_engine(), as well as the Connection.execution_options.isolation_level argument as passed to Connection.execution_options(). This feature works by issuing the command SET SESSION TRANSACTION ISOLATION LEVEL <level> for each new connection. For the special AUTOCOMMIT isolation level, DBAPI-specific techniques are used.

To set isolation level using create_engine():

To set using per-connection execution options:

Valid values for isolation_level include:

The special AUTOCOMMIT value makes use of the various “autocommit” attributes provided by specific DBAPIs, and is currently supported by MySQLdb, MySQL-Client, MySQL-Connector Python, and PyMySQL. Using it, the database connection will return true for the value of SELECT @@autocommit;.

There are also more options for isolation level configurations, such as “sub-engine” objects linked to a main Engine which each apply different isolation level settings. See the discussion at Setting Transaction Isolation Levels including DBAPI Autocommit for background.

Setting Transaction Isolation Levels including DBAPI Autocommit

When creating tables, SQLAlchemy will automatically set AUTO_INCREMENT on the first Integer primary key column which is not marked as a foreign key:

You can disable this behavior by passing False to the Column.autoincrement argument of Column. This flag can also be used to enable auto-increment on a secondary column in a multi-column key for some storage engines:

Server-side cursor support is available for the mysqlclient, PyMySQL, mariadbconnector dialects and may also be available in others. This makes use of either the “buffered=True/False” flag if available or by using a class such as MySQLdb.cursors.SSCursor or pymysql.cursors.SSCursor internally.

Server side cursors are enabled on a per-statement basis by using the Connection.execution_options.stream_results connection execution option:

Note that some kinds of SQL statements may not be supported with server side cursors; generally, only SQL statements that return rows should be used with this option.

Deprecated since version 1.4: The dialect-level server_side_cursors flag is deprecated and will be removed in a future release. Please use the Connection.stream_results execution option for unbuffered cursor support.

Using Server Side Cursors (a.k.a. stream results)

Most MySQL / MariaDB DBAPIs offer the option to set the client character set for a connection. This is typically delivered using the charset parameter in the URL, such as:

This charset is the client character set for the connection. Some MySQL DBAPIs will default this to a value such as latin1, and some will make use of the default-character-set setting in the my.cnf file as well. Documentation for the DBAPI in use should be consulted for specific behavior.

The encoding used for Unicode has traditionally been 'utf8'. However, for MySQL versions 5.5.3 and MariaDB 5.5 on forward, a new MySQL-specific encoding 'utf8mb4' has been introduced, and as of MySQL 8.0 a warning is emitted by the server if plain utf8 is specified within any server-side directives, replaced with utf8mb3. The rationale for this new encoding is due to the fact that MySQL’s legacy utf-8 encoding only supports codepoints up to three bytes instead of four. Therefore, when communicating with a MySQL or MariaDB database that includes codepoints more than three bytes in size, this new charset is preferred, if supported by both the database as well as the client DBAPI, as in:

All modern DBAPIs should support the utf8mb4 charset.

In order to use utf8mb4 encoding for a schema that was created with legacy utf8, changes to the MySQL/MariaDB schema and/or server configuration may be required.

The utf8mb4 Character Set - in the MySQL documentation

MySQL versions 5.6, 5.7 and later (not MariaDB at the time of this writing) now emit a warning when attempting to pass binary data to the database, while a character set encoding is also in place, when the binary data itself is not valid for that encoding:

This warning is due to the fact that the MySQL client library is attempting to interpret the binary string as a unicode object even if a datatype such as LargeBinary is in use. To resolve this, the SQL statement requires a binary “character set introducer” be present before any non-NULL value that renders like this:

These character set introducers are provided by the DBAPI driver, assuming the use of mysqlclient or PyMySQL (both of which are recommended). Add the query string parameter binary_prefix=true to the URL to repair this warning:

The binary_prefix flag may or may not be supported by other MySQL drivers.

SQLAlchemy itself cannot render this _binary prefix reliably, as it does not work with the NULL value, which is valid to be sent as a bound parameter. As the MySQL driver renders parameters directly into the SQL string, it’s the most efficient place for this additional keyword to be passed.

Character set introducers - on the MySQL website

MySQL / MariaDB feature two varieties of identifier “quoting style”, one using backticks and the other using quotes, e.g. `some_identifier` vs. "some_identifier". All MySQL dialects detect which version is in use by checking the value of sql_mode when a connection is first established with a particular Engine. This quoting style comes into play when rendering table and column names as well as when reflecting existing database structures. The detection is entirely automatic and no special configuration is needed to use either quoting style.

MySQL supports operating in multiple Server SQL Modes for both Servers and Clients. To change the sql_mode for a given application, a developer can leverage SQLAlchemy’s Events system.

In the following example, the event system is used to set the sql_mode on the first_connect and connect events:

In the example illustrated above, the “connect” event will invoke the “SET” statement on the connection at the moment a particular DBAPI connection is first created for a given Pool, before the connection is made available to the connection pool. Additionally, because the function was registered with insert=True, it will be prepended to the internal list of registered functions.

Many of the MySQL / MariaDB SQL extensions are handled through SQLAlchemy’s generic function and operator support:

And of course any valid SQL statement can be executed as a string as well.

Some limited direct support for MySQL / MariaDB extensions to SQL is currently available.

INSERT..ON DUPLICATE KEY UPDATE: See INSERT…ON DUPLICATE KEY UPDATE (Upsert)

SELECT pragma, use Select.prefix_with() and Query.prefix_with():

Added in version 2.0.37: Added delete with limit

optimizer hints, use Select.prefix_with() and Query.prefix_with():

index hints, use Select.with_hint() and Query.with_hint():

MATCH operator support:

The MariaDB dialect supports 10.5+’s INSERT..RETURNING and DELETE..RETURNING (10.0+) syntaxes. INSERT..RETURNING may be used automatically in some cases in order to fetch newly generated identifiers in place of the traditional approach of using cursor.lastrowid, however cursor.lastrowid is currently still preferred for simple single-statement cases for its better performance.

To specify an explicit RETURNING clause, use the _UpdateBase.returning() method on a per-statement basis:

Added in version 2.0: Added support for MariaDB RETURNING

MySQL / MariaDB allow “upserts” (update or insert) of rows into a table via the ON DUPLICATE KEY UPDATE clause of the INSERT statement. A candidate row will only be inserted if that row does not match an existing primary or unique key in the table; otherwise, an UPDATE will be performed. The statement allows for separate specification of the values to INSERT versus the values for UPDATE.

SQLAlchemy provides ON DUPLICATE KEY UPDATE support via the MySQL-specific insert() function, which provides the generative method Insert.on_duplicate_key_update():

Unlike PostgreSQL’s “ON CONFLICT” phrase, the “ON DUPLICATE KEY UPDATE” phrase will always match on any primary key or unique key, and will always perform an UPDATE if there’s a match; there are no options for it to raise an error or to skip performing an UPDATE.

ON DUPLICATE KEY UPDATE is used to perform an update of the already existing row, using any combination of new values as well as values from the proposed insertion. These values are normally specified using keyword arguments passed to the Insert.on_duplicate_key_update() given column key values (usually the name of the column, unless it specifies Column.key ) as keys and literal or SQL expressions as values:

In a manner similar to that of UpdateBase.values(), other parameter forms are accepted, including a single dictionary:

as well as a list of 2-tuples, which will automatically provide a parameter-ordered UPDATE statement in a manner similar to that described at Parameter Ordered Updates. Unlike the Update object, no special flag is needed to specify the intent since the argument form is this context is unambiguous:

Changed in version 1.3: support for parameter-ordered UPDATE clause within MySQL ON DUPLICATE KEY UPDATE

The Insert.on_duplicate_key_update() method does not take into account Python-side default UPDATE values or generation functions, e.g. e.g. those specified using Column.onupdate. These values will not be exercised for an ON DUPLICATE KEY style of UPDATE, unless they are manually specified explicitly in the parameters.

In order to refer to the proposed insertion row, the special alias Insert.inserted is available as an attribute on the Insert object; this object is a ColumnCollection which contains all columns of the target table:

When rendered, the “inserted” namespace will produce the expression VALUES(<columnname>).

Added in version 1.2: Added support for MySQL ON DUPLICATE KEY UPDATE clause

SQLAlchemy standardizes the DBAPI cursor.rowcount attribute to be the usual definition of “number of rows matched by an UPDATE or DELETE” statement. This is in contradiction to the default setting on most MySQL DBAPI drivers, which is “number of rows actually modified/deleted”. For this reason, the SQLAlchemy MySQL dialects always add the constants.CLIENT.FOUND_ROWS flag, or whatever is equivalent for the target dialect, upon connection. This setting is currently hardcoded.

CursorResult.rowcount

MySQL and MariaDB-specific extensions to the Index construct are available.

MySQL and MariaDB both provide an option to create index entries with a certain length, where “length” refers to the number of characters or bytes in each value which will become part of the index. SQLAlchemy provides this feature via the mysql_length and/or mariadb_length parameters:

Prefix lengths are given in characters for nonbinary string types and in bytes for binary string types. The value passed to the keyword argument must be either an integer (and, thus, specify the same prefix length value for all columns of the index) or a dict in which keys are column names and values are prefix length values for corresponding columns. MySQL and MariaDB only allow a length for a column of an index if it is for a CHAR, VARCHAR, TEXT, BINARY, VARBINARY and BLOB.

MySQL storage engines permit you to specify an index prefix when creating an index. SQLAlchemy provides this feature via the mysql_prefix parameter on Index:

The value passed to the keyword argument will be simply passed through to the underlying CREATE INDEX, so it must be a valid index prefix for your MySQL storage engine.

CREATE INDEX - MySQL documentation

Some MySQL storage engines permit you to specify an index type when creating an index or primary key constraint. SQLAlchemy provides this feature via the mysql_using parameter on Index:

As well as the mysql_using parameter on PrimaryKeyConstraint:

The value passed to the keyword argument will be simply passed through to the underlying CREATE INDEX or PRIMARY KEY clause, so it must be a valid index type for your MySQL storage engine.

More information can be found at:

https://dev.mysql.com/doc/refman/5.0/en/create-index.html

https://dev.mysql.com/doc/refman/5.0/en/create-table.html

CREATE FULLTEXT INDEX in MySQL also supports a “WITH PARSER” option. This is available using the keyword argument mysql_with_parser:

Added in version 1.3.

MySQL and MariaDB’s behavior regarding foreign keys has some important caveats.

Neither MySQL nor MariaDB support the foreign key arguments “DEFERRABLE”, “INITIALLY”, or “MATCH”. Using the deferrable or initially keyword argument with ForeignKeyConstraint or ForeignKey will have the effect of these keywords being rendered in a DDL expression, which will then raise an error on MySQL or MariaDB. In order to use these keywords on a foreign key while having them ignored on a MySQL / MariaDB backend, use a custom compile rule:

The “MATCH” keyword is in fact more insidious, and is explicitly disallowed by SQLAlchemy in conjunction with the MySQL or MariaDB backends. This argument is silently ignored by MySQL / MariaDB, but in addition has the effect of ON UPDATE and ON DELETE options also being ignored by the backend. Therefore MATCH should never be used with the MySQL / MariaDB backends; as is the case with DEFERRABLE and INITIALLY, custom compilation rules can be used to correct a ForeignKeyConstraint at DDL definition time.

Not all MySQL / MariaDB storage engines support foreign keys. When using the very common MyISAM MySQL storage engine, the information loaded by table reflection will not include foreign keys. For these tables, you may supply a ForeignKeyConstraint at reflection time:

CREATE TABLE arguments including Storage Engines

SQLAlchemy supports both the Index construct with the flag unique=True, indicating a UNIQUE index, as well as the UniqueConstraint construct, representing a UNIQUE constraint. Both objects/syntaxes are supported by MySQL / MariaDB when emitting DDL to create these constraints. However, MySQL / MariaDB does not have a unique constraint construct that is separate from a unique index; that is, the “UNIQUE” constraint on MySQL / MariaDB is equivalent to creating a “UNIQUE INDEX”.

When reflecting these constructs, the Inspector.get_indexes() and the Inspector.get_unique_constraints() methods will both return an entry for a UNIQUE index in MySQL / MariaDB. However, when performing full table reflection using Table(..., autoload_with=engine), the UniqueConstraint construct is not part of the fully reflected Table construct under any circumstances; this construct is always represented by a Index with the unique=True setting present in the Table.indexes collection.

MySQL / MariaDB have historically expanded the DDL for the TIMESTAMP datatype into the phrase “TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP”, which includes non-standard SQL that automatically updates the column with the current timestamp when an UPDATE occurs, eliminating the usual need to use a trigger in such a case where server-side update changes are desired.

MySQL 5.6 introduced a new flag explicit_defaults_for_timestamp which disables the above behavior, and in MySQL 8 this flag defaults to true, meaning in order to get a MySQL “on update timestamp” without changing this flag, the above DDL must be rendered explicitly. Additionally, the same DDL is valid for use of the DATETIME datatype as well.

SQLAlchemy’s MySQL dialect does not yet have an option to generate MySQL’s “ON UPDATE CURRENT_TIMESTAMP” clause, noting that this is not a general purpose “ON UPDATE” as there is no such syntax in standard SQL. SQLAlchemy’s Column.server_onupdate parameter is currently not related to this special MySQL behavior.

To generate this DDL, make use of the Column.server_default parameter and pass a textual clause that also includes the ON UPDATE clause:

The same instructions apply to use of the DateTime and DATETIME datatypes:

Even though the Column.server_onupdate feature does not generate this DDL, it still may be desirable to signal to the ORM that this updated value should be fetched. This syntax looks like the following:

MySQL historically enforces that a column which specifies the TIMESTAMP datatype implicitly includes a default value of CURRENT_TIMESTAMP, even though this is not stated, and additionally sets the column as NOT NULL, the opposite behavior vs. that of all other datatypes:

Above, we see that an INTEGER column defaults to NULL, unless it is specified with NOT NULL. But when the column is of type TIMESTAMP, an implicit default of CURRENT_TIMESTAMP is generated which also coerces the column to be a NOT NULL, even though we did not specify it as such.

This behavior of MySQL can be changed on the MySQL side using the explicit_defaults_for_timestamp configuration flag introduced in MySQL 5.6. With this server setting enabled, TIMESTAMP columns behave like any other datatype on the MySQL side with regards to defaults and nullability.

However, to accommodate the vast majority of MySQL databases that do not specify this new flag, SQLAlchemy emits the “NULL” specifier explicitly with any TIMESTAMP column that does not specify nullable=False. In order to accommodate newer databases that specify explicit_defaults_for_timestamp, SQLAlchemy also emits NOT NULL for TIMESTAMP columns that do specify nullable=False. The following example illustrates:

Produce a MATCH (X, Y) AGAINST ('TEXT') clause.

inherits from sqlalchemy.sql.expression.Generative, sqlalchemy.sql.expression.BinaryExpression

Produce a MATCH (X, Y) AGAINST ('TEXT') clause.

Would produce SQL resembling:

The match() function is a standalone version of the ColumnElement.match() method available on all SQL expressions, as when ColumnElement.match() is used, but allows to pass multiple columns

cols¶ – column expressions to match against

against¶ – expression to be compared towards

in_boolean_mode¶ – boolean, set “boolean mode” to true

in_natural_language_mode¶ – boolean , set “natural language” to true

with_query_expansion¶ – boolean, set “query expansion” to true

Added in version 1.4.19.

ColumnElement.match()

Apply the “IN BOOLEAN MODE” modifier to the MATCH expression.

in_natural_language_mode()

Apply the “IN NATURAL LANGUAGE MODE” modifier to the MATCH expression.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

with_query_expansion()

Apply the “WITH QUERY EXPANSION” modifier to the MATCH expression.

Apply the “IN BOOLEAN MODE” modifier to the MATCH expression.

a new match instance with modifications applied.

Apply the “IN NATURAL LANGUAGE MODE” modifier to the MATCH expression.

a new match instance with modifications applied.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

Apply the “WITH QUERY EXPANSION” modifier to the MATCH expression.

a new match instance with modifications applied.

As with all SQLAlchemy dialects, all UPPERCASE types that are known to be valid with MySQL are importable from the top level dialect:

In addition to the above types, MariaDB also supports the following:

Types which are specific to MySQL or MariaDB, or have specific construction arguments, are as follows:

MySQL BIGINTEGER type.

MySQL CHAR type, for fixed-length character data.

INET4 column type for MariaDB

INET6 column type for MariaDB

MySQL LONGBLOB type, for binary data up to 2^32 bytes.

MySQL LONGTEXT type, for character storage encoded up to 2^32 bytes.

MySQL MEDIUMBLOB type, for binary data up to 2^24 bytes.

MySQL MEDIUMINTEGER type.

MySQL MEDIUMTEXT type, for character storage encoded up to 2^24 bytes.

MySQL SMALLINTEGER type.

MySQL TIMESTAMP type.

MySQL TINYBLOB type, for binary data up to 2^8 bytes.

MySQL TINYTEXT type, for character storage encoded up to 2^8 bytes.

MySQL VARCHAR type, for variable-length character data.

MySQL YEAR type, for single byte storage of years 1901-2155.

inherits from sqlalchemy.dialects.mysql.types._IntegerType, sqlalchemy.types.BIGINT

MySQL BIGINTEGER type.

Construct a BIGINTEGER.

Construct a BIGINTEGER.

display_width¶ – Optional, maximum display width for this number.

unsigned¶ – a boolean, optional.

zerofill¶ – Optional. If true, values will be stored as strings left-padded with zeros. Note that this does not effect the values returned by the underlying database API, which continue to be numeric.

inherits from sqlalchemy.types._Binary

inherits from sqlalchemy.types.TypeEngine

This type is for MySQL 5.0.3 or greater for MyISAM, and 5.0.5 or greater for MyISAM, MEMORY, InnoDB and BDB. For older versions, use a MSTinyInteger() type.

length¶ – Optional, number of bits.

inherits from sqlalchemy.types.LargeBinary

inherited from the sqlalchemy.types.LargeBinary.__init__ method of LargeBinary

Construct a LargeBinary type.

length¶ – optional, a length for the column for use in DDL statements, for those binary types that accept a length, such as the MySQL BLOB type.

inherits from sqlalchemy.types.Boolean

The SQL BOOLEAN type.

inherited from the sqlalchemy.types.Boolean.__init__ method of Boolean

defaults to False. If the boolean is generated as an int/smallint, also create a CHECK constraint on the table that ensures 1 or 0 as a value.

it is strongly recommended that the CHECK constraint have an explicit name in order to support schema-management concerns. This can be established either by setting the Boolean.name parameter or by setting up an appropriate naming convention; see Configuring Constraint Naming Conventions for background.

Changed in version 1.4: - this flag now defaults to False, meaning no CHECK constraint is generated for a non-native enumerated type.

name¶ – if a CHECK constraint is generated, specify the name of the constraint.

inherits from sqlalchemy.dialects.mysql.types._StringType, sqlalchemy.types.CHAR

MySQL CHAR type, for fixed-length character data.

length¶ – Maximum data length, in characters.

binary¶ – Optional, use the default binary collation for the national character set. This does not affect the type of data stored, use a BINARY type for binary data.

collation¶ – Optional, request a particular collation. Must be compatible with the national character set.

inherits from sqlalchemy.types.Date

inherits from sqlalchemy.types.DATETIME

Construct a MySQL DATETIME type.

Construct a MySQL DATETIME type.

timezone¶ – not used by the MySQL dialect.

fractional seconds precision value. MySQL 5.6.4 supports storage of fractional seconds; this parameter will be used when emitting DDL for the DATETIME type.

DBAPI driver support for fractional seconds may be limited; current support includes MySQL Connector/Python.

inherits from sqlalchemy.dialects.mysql.types._NumericType, sqlalchemy.types.DECIMAL

precision¶ – Total digits in this number. If scale and precision are both None, values are stored to limits allowed by the server.

scale¶ – The number of digits after the decimal point.

unsigned¶ – a boolean, optional.

zerofill¶ – Optional. If true, values will be stored as strings left-padded with zeros. Note that this does not effect the values returned by the underlying database API, which continue to be numeric.

inherits from sqlalchemy.dialects.mysql.types._FloatType, sqlalchemy.types.DOUBLE

The DOUBLE type by default converts from float to Decimal, using a truncation that defaults to 10 digits. Specify either scale=n or decimal_return_scale=n in order to change this scale, or asdecimal=False to return values directly as Python floating points.

precision¶ – Total digits in this number. If scale and precision are both None, values are stored to limits allowed by the server.

scale¶ – The number of digits after the decimal point.

unsigned¶ – a boolean, optional.

zerofill¶ – Optional. If true, values will be stored as strings left-padded with zeros. Note that this does not effect the values returned by the underlying database API, which continue to be numeric.

inherits from sqlalchemy.types.NativeForEmulated, sqlalchemy.types.Enum, sqlalchemy.dialects.mysql.types._StringType

The range of valid values for this ENUM. Values in enums are not quoted, they will be escaped and surrounded by single quotes when generating the schema. This object may also be a PEP-435-compliant enumerated type.

This flag has no effect.

Changed in version The: MySQL ENUM type as well as the base Enum type now validates all Python data values.

charset¶ – Optional, a column-level character set for this string value. Takes precedence to ‘ascii’ or ‘unicode’ short-hand.

collation¶ – Optional, a column-level collation for this string value. Takes precedence to ‘binary’ short-hand.

ascii¶ – Defaults to False: short-hand for the latin1 character set, generates ASCII in schema.

unicode¶ – Defaults to False: short-hand for the ucs2 character set, generates UNICODE in schema.

binary¶ – Defaults to False: short-hand, pick the binary collation type that matches the column’s character set. Generates BINARY in schema. This does not affect the type of data stored, only the collation of character data.

inherits from sqlalchemy.dialects.mysql.types._FloatType, sqlalchemy.types.FLOAT

precision¶ – Total digits in this number. If scale and precision are both None, values are stored to limits allowed by the server.

scale¶ – The number of digits after the decimal point.

unsigned¶ – a boolean, optional.

zerofill¶ – Optional. If true, values will be stored as strings left-padded with zeros. Note that this does not effect the values returned by the underlying database API, which continue to be numeric.

inherits from sqlalchemy.types.TypeEngine

INET4 column type for MariaDB

Added in version 2.0.37.

inherits from sqlalchemy.types.TypeEngine

INET6 column type for MariaDB

Added in version 2.0.37.

inherits from sqlalchemy.dialects.mysql.types._IntegerType, sqlalchemy.types.INTEGER

Construct an INTEGER.

Construct an INTEGER.

display_width¶ – Optional, maximum display width for this number.

unsigned¶ – a boolean, optional.

zerofill¶ – Optional. If true, values will be stored as strings left-padded with zeros. Note that this does not effect the values returned by the underlying database API, which continue to be numeric.

inherits from sqlalchemy.types.JSON

MySQL supports JSON as of version 5.7. MariaDB supports JSON (as an alias for LONGTEXT) as of version 10.2.

JSON is used automatically whenever the base JSON datatype is used against a MySQL or MariaDB backend.

JSON - main documentation for the generic cross-platform JSON datatype.

The JSON type supports persistence of JSON values as well as the core index operations provided by JSON datatype, by adapting the operations to render the JSON_EXTRACT function at the database level.

inherits from sqlalchemy.types._Binary

MySQL LONGBLOB type, for binary data up to 2^32 bytes.

inherits from sqlalchemy.dialects.mysql.types._StringType

MySQL LONGTEXT type, for character storage encoded up to 2^32 bytes.

Construct a LONGTEXT.

Construct a LONGTEXT.

charset¶ – Optional, a column-level character set for this string value. Takes precedence to ‘ascii’ or ‘unicode’ short-hand.

collation¶ – Optional, a column-level collation for this string value. Takes precedence to ‘binary’ short-hand.

ascii¶ – Defaults to False: short-hand for the latin1 character set, generates ASCII in schema.

unicode¶ – Defaults to False: short-hand for the ucs2 character set, generates UNICODE in schema.

national¶ – Optional. If true, use the server’s configured national character set.

binary¶ – Defaults to False: short-hand, pick the binary collation type that matches the column’s character set. Generates BINARY in schema. This does not affect the type of data stored, only the collation of character data.

inherits from sqlalchemy.types._Binary

MySQL MEDIUMBLOB type, for binary data up to 2^24 bytes.

inherits from sqlalchemy.dialects.mysql.types._IntegerType

MySQL MEDIUMINTEGER type.

Construct a MEDIUMINTEGER

Construct a MEDIUMINTEGER

display_width¶ – Optional, maximum display width for this number.

unsigned¶ – a boolean, optional.

zerofill¶ – Optional. If true, values will be stored as strings left-padded with zeros. Note that this does not effect the values returned by the underlying database API, which continue to be numeric.

inherits from sqlalchemy.dialects.mysql.types._StringType

MySQL MEDIUMTEXT type, for character storage encoded up to 2^24 bytes.

Construct a MEDIUMTEXT.

Construct a MEDIUMTEXT.

charset¶ – Optional, a column-level character set for this string value. Takes precedence to ‘ascii’ or ‘unicode’ short-hand.

collation¶ – Optional, a column-level collation for this string value. Takes precedence to ‘binary’ short-hand.

ascii¶ – Defaults to False: short-hand for the latin1 character set, generates ASCII in schema.

unicode¶ – Defaults to False: short-hand for the ucs2 character set, generates UNICODE in schema.

national¶ – Optional. If true, use the server’s configured national character set.

binary¶ – Defaults to False: short-hand, pick the binary collation type that matches the column’s character set. Generates BINARY in schema. This does not affect the type of data stored, only the collation of character data.

inherits from sqlalchemy.dialects.mysql.types._StringType, sqlalchemy.types.NCHAR

For fixed-length character data in the server’s configured national character set.

length¶ – Maximum data length, in characters.

binary¶ – Optional, use the default binary collation for the national character set. This does not affect the type of data stored, use a BINARY type for binary data.

collation¶ – Optional, request a particular collation. Must be compatible with the national character set.

inherits from sqlalchemy.dialects.mysql.types._NumericType, sqlalchemy.types.NUMERIC

precision¶ – Total digits in this number. If scale and precision are both None, values are stored to limits allowed by the server.

scale¶ – The number of digits after the decimal point.

unsigned¶ – a boolean, optional.

zerofill¶ – Optional. If true, values will be stored as strings left-padded with zeros. Note that this does not effect the values returned by the underlying database API, which continue to be numeric.

inherits from sqlalchemy.dialects.mysql.types._StringType, sqlalchemy.types.NVARCHAR

For variable-length character data in the server’s configured national character set.

Construct an NVARCHAR.

Construct an NVARCHAR.

length¶ – Maximum data length, in characters.

binary¶ – Optional, use the default binary collation for the national character set. This does not affect the type of data stored, use a BINARY type for binary data.

collation¶ – Optional, request a particular collation. Must be compatible with the national character set.

inherits from sqlalchemy.dialects.mysql.types._FloatType, sqlalchemy.types.REAL

The REAL type by default converts from float to Decimal, using a truncation that defaults to 10 digits. Specify either scale=n or decimal_return_scale=n in order to change this scale, or asdecimal=False to return values directly as Python floating points.

precision¶ – Total digits in this number. If scale and precision are both None, values are stored to limits allowed by the server.

scale¶ – The number of digits after the decimal point.

unsigned¶ – a boolean, optional.

zerofill¶ – Optional. If true, values will be stored as strings left-padded with zeros. Note that this does not effect the values returned by the underlying database API, which continue to be numeric.

inherits from sqlalchemy.dialects.mysql.types._StringType

The list of potential values is required in the case that this set will be used to generate DDL for a table, or if the SET.retrieve_as_bitwise flag is set to True.

values¶ – The range of valid values for this SET. The values are not quoted, they will be escaped and surrounded by single quotes when generating the schema.

convert_unicode¶ – Same flag as that of String.convert_unicode.

collation¶ – same as that of String.collation

charset¶ – same as that of VARCHAR.charset.

ascii¶ – same as that of VARCHAR.ascii.

unicode¶ – same as that of VARCHAR.unicode.

binary¶ – same as that of VARCHAR.binary.

retrieve_as_bitwise¶ –

if True, the data for the set type will be persisted and selected using an integer value, where a set is coerced into a bitwise mask for persistence. MySQL allows this mode which has the advantage of being able to store values unambiguously, such as the blank string ''. The datatype will appear as the expression col + 0 in a SELECT statement, so that the value is coerced into an integer value in result sets. This flag is required if one wishes to persist a set that can store the blank string '' as a value.

When using SET.retrieve_as_bitwise, it is essential that the list of set values is expressed in the exact same order as exists on the MySQL database.

inherits from sqlalchemy.dialects.mysql.types._IntegerType, sqlalchemy.types.SMALLINT

MySQL SMALLINTEGER type.

Construct a SMALLINTEGER.

Construct a SMALLINTEGER.

display_width¶ – Optional, maximum display width for this number.

unsigned¶ – a boolean, optional.

zerofill¶ – Optional. If true, values will be stored as strings left-padded with zeros. Note that this does not effect the values returned by the underlying database API, which continue to be numeric.

inherits from sqlalchemy.dialects.mysql.types._StringType, sqlalchemy.types.TEXT

MySQL TEXT type, for character storage encoded up to 2^16 bytes.

length¶ – Optional, if provided the server may optimize storage by substituting the smallest TEXT type sufficient to store length bytes of characters.

charset¶ – Optional, a column-level character set for this string value. Takes precedence to ‘ascii’ or ‘unicode’ short-hand.

collation¶ – Optional, a column-level collation for this string value. Takes precedence to ‘binary’ short-hand.

ascii¶ – Defaults to False: short-hand for the latin1 character set, generates ASCII in schema.

unicode¶ – Defaults to False: short-hand for the ucs2 character set, generates UNICODE in schema.

national¶ – Optional. If true, use the server’s configured national character set.

binary¶ – Defaults to False: short-hand, pick the binary collation type that matches the column’s character set. Generates BINARY in schema. This does not affect the type of data stored, only the collation of character data.

inherits from sqlalchemy.types.TIME

Construct a MySQL TIME type.

Construct a MySQL TIME type.

timezone¶ – not used by the MySQL dialect.

fractional seconds precision value. MySQL 5.6 supports storage of fractional seconds; this parameter will be used when emitting DDL for the TIME type.

DBAPI driver support for fractional seconds may be limited; current support includes MySQL Connector/Python.

inherits from sqlalchemy.types.TIMESTAMP

MySQL TIMESTAMP type.

Construct a MySQL TIMESTAMP type.

Construct a MySQL TIMESTAMP type.

timezone¶ – not used by the MySQL dialect.

fractional seconds precision value. MySQL 5.6.4 supports storage of fractional seconds; this parameter will be used when emitting DDL for the TIMESTAMP type.

DBAPI driver support for fractional seconds may be limited; current support includes MySQL Connector/Python.

inherits from sqlalchemy.types._Binary

MySQL TINYBLOB type, for binary data up to 2^8 bytes.

inherits from sqlalchemy.dialects.mysql.types._IntegerType

display_width¶ – Optional, maximum display width for this number.

unsigned¶ – a boolean, optional.

zerofill¶ – Optional. If true, values will be stored as strings left-padded with zeros. Note that this does not effect the values returned by the underlying database API, which continue to be numeric.

inherits from sqlalchemy.dialects.mysql.types._StringType

MySQL TINYTEXT type, for character storage encoded up to 2^8 bytes.

Construct a TINYTEXT.

Construct a TINYTEXT.

charset¶ – Optional, a column-level character set for this string value. Takes precedence to ‘ascii’ or ‘unicode’ short-hand.

collation¶ – Optional, a column-level collation for this string value. Takes precedence to ‘binary’ short-hand.

ascii¶ – Defaults to False: short-hand for the latin1 character set, generates ASCII in schema.

unicode¶ – Defaults to False: short-hand for the ucs2 character set, generates UNICODE in schema.

national¶ – Optional. If true, use the server’s configured national character set.

binary¶ – Defaults to False: short-hand, pick the binary collation type that matches the column’s character set. Generates BINARY in schema. This does not affect the type of data stored, only the collation of character data.

inherits from sqlalchemy.types._Binary

The SQL VARBINARY type.

inherits from sqlalchemy.dialects.mysql.types._StringType, sqlalchemy.types.VARCHAR

MySQL VARCHAR type, for variable-length character data.

charset¶ – Optional, a column-level character set for this string value. Takes precedence to ‘ascii’ or ‘unicode’ short-hand.

collation¶ – Optional, a column-level collation for this string value. Takes precedence to ‘binary’ short-hand.

ascii¶ – Defaults to False: short-hand for the latin1 character set, generates ASCII in schema.

unicode¶ – Defaults to False: short-hand for the ucs2 character set, generates UNICODE in schema.

national¶ – Optional. If true, use the server’s configured national character set.

binary¶ – Defaults to False: short-hand, pick the binary collation type that matches the column’s character set. Generates BINARY in schema. This does not affect the type of data stored, only the collation of character data.

inherits from sqlalchemy.types.TypeEngine

MySQL YEAR type, for single byte storage of years 1901-2155.

Construct a MySQL/MariaDB-specific variant Insert construct.

MySQL-specific implementation of INSERT.

Construct a MySQL/MariaDB-specific variant Insert construct.

The sqlalchemy.dialects.mysql.insert() function creates a sqlalchemy.dialects.mysql.Insert. This class is based on the dialect-agnostic Insert construct which may be constructed using the insert() function in SQLAlchemy Core.

The Insert construct includes additional methods Insert.on_duplicate_key_update().

inherits from sqlalchemy.sql.expression.Insert

MySQL-specific implementation of INSERT.

Adds methods for MySQL-specific syntaxes such as ON DUPLICATE KEY UPDATE.

The Insert object is created using the sqlalchemy.dialects.mysql.insert() function.

Added in version 1.2.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

on_duplicate_key_update()

Specifies the ON DUPLICATE KEY UPDATE clause.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

Provide the “inserted” namespace for an ON DUPLICATE KEY UPDATE statement

MySQL’s ON DUPLICATE KEY UPDATE clause allows reference to the row that would be inserted, via a special function called VALUES(). This attribute provides all columns in this row to be referenceable such that they will render within a VALUES() function inside the ON DUPLICATE KEY UPDATE clause. The attribute is named .inserted so as not to conflict with the existing Insert.values() method.

The Insert.inserted attribute is an instance of ColumnCollection, which provides an interface the same as that of the Table.c collection described at Accessing Tables and Columns. With this collection, ordinary names are accessible like attributes (e.g. stmt.inserted.some_column), but special names and dictionary method names should be accessed using indexed access, such as stmt.inserted["column name"] or stmt.inserted["values"]. See the docstring for ColumnCollection for further examples.

INSERT…ON DUPLICATE KEY UPDATE (Upsert) - example of how to use Insert.inserted

Specifies the ON DUPLICATE KEY UPDATE clause.

**kw¶ – Column keys linked to UPDATE values. The values may be any SQL expression or supported literal Python values.

This dictionary does not take into account Python-specified default UPDATE values or generation functions, e.g. those specified using Column.onupdate. These values will not be exercised for an ON DUPLICATE KEY UPDATE style of UPDATE, unless values are manually specified here.

As an alternative to passing key/value parameters, a dictionary or list of 2-tuples can be passed as a single positional argument.

Passing a single dictionary is equivalent to the keyword argument form:

Passing a list of 2-tuples indicates that the parameter assignments in the UPDATE clause should be ordered as sent, in a manner similar to that described for the Update construct overall in Parameter Ordered Updates:

Changed in version 1.3: parameters can be specified as a dictionary or list of 2-tuples; the latter form provides for parameter ordering.

Added in version 1.2.

INSERT…ON DUPLICATE KEY UPDATE (Upsert)

Support for the MySQL / MariaDB database via the mysqlclient (maintained fork of MySQL-Python) driver.

Documentation and download information (if applicable) for mysqlclient (maintained fork of MySQL-Python) is available at: https://pypi.org/project/mysqlclient/

The mysqlclient DBAPI is a maintained fork of the MySQL-Python DBAPI that is no longer maintained. mysqlclient supports Python 2 and Python 3 and is very stable.

Please see Unicode for current recommendations on unicode handling.

The mysqlclient and PyMySQL DBAPIs accept an additional dictionary under the key “ssl”, which may be specified using the create_engine.connect_args dictionary:

For convenience, the following keys may also be specified inline within the URL where they will be interpreted into the “ssl” dictionary automatically: “ssl_ca”, “ssl_cert”, “ssl_key”, “ssl_capath”, “ssl_cipher”, “ssl_check_hostname”. An example is as follows:

SSL Connections in the PyMySQL dialect

Google Cloud SQL now recommends use of the MySQLdb dialect. Connect using a URL like the following:

The mysqldb dialect supports server-side cursors. See Server Side Cursors.

Support for the MySQL / MariaDB database via the PyMySQL driver.

Documentation and download information (if applicable) for PyMySQL is available at: https://pymysql.readthedocs.io/

Please see Unicode for current recommendations on unicode handling.

The PyMySQL DBAPI accepts the same SSL arguments as that of MySQLdb, described at SSL Connections. See that section for additional examples.

If the server uses an automatically-generated certificate that is self-signed or does not match the host name (as seen from the client), it may also be necessary to indicate ssl_check_hostname=false in PyMySQL:

The pymysql DBAPI is a pure Python port of the MySQL-python (MySQLdb) driver, and targets 100% compatibility. Most behavioral notes for MySQL-python apply to the pymysql driver as well.

Support for the MySQL / MariaDB database via the MariaDB Connector/Python driver.

Documentation and download information (if applicable) for MariaDB Connector/Python is available at: https://pypi.org/project/mariadb/

MariaDB Connector/Python enables Python programs to access MariaDB and MySQL databases using an API which is compliant with the Python DB API 2.0 (PEP-249). It is written in C and uses MariaDB Connector/C client library for client server communication.

Note that the default driver for a mariadb:// connection URI continues to be mysqldb. mariadb+mariadbconnector:// is required to use this driver.

Support for the MySQL / MariaDB database via the MySQL Connector/Python driver.

Documentation and download information (if applicable) for MySQL Connector/Python is available at: https://pypi.org/project/mysql-connector-python/

MySQL Connector/Python is supported as of SQLAlchemy 2.0.39 to the degree which the driver is functional. There are still ongoing issues with features such as server side cursors which remain disabled until upstream issues are repaired.

The MySQL Connector/Python driver published by Oracle is subject to frequent, major regressions of essential functionality such as being able to correctly persist simple binary strings which indicate it is not well tested. The SQLAlchemy project is not able to maintain this dialect fully as regressions in the driver prevent it from being included in continuous integration.

Changed in version 2.0.39: The MySQL Connector/Python dialect has been updated to support the latest version of this DBAPI. Previously, MySQL Connector/Python was not fully supported. However, support remains limited due to ongoing regressions introduced in this driver.

MySQL Connector/Python may attempt to pass an incompatible collation to the database when connecting to MariaDB. Experimentation has shown that using ?charset=utf8mb4&collation=utfmb4_general_ci or similar MariaDB-compatible charset/collation will allow connectivity.

Support for the MySQL / MariaDB database via the asyncmy driver.

Documentation and download information (if applicable) for asyncmy is available at: https://github.com/long2ice/asyncmy

Using a special asyncio mediation layer, the asyncmy dialect is usable as the backend for the SQLAlchemy asyncio extension package.

This dialect should normally be used only with the create_async_engine() engine creation function:

Support for the MySQL / MariaDB database via the aiomysql driver.

Documentation and download information (if applicable) for aiomysql is available at: https://github.com/aio-libs/aiomysql

The aiomysql dialect is SQLAlchemy’s second Python asyncio dialect.

Using a special asyncio mediation layer, the aiomysql dialect is usable as the backend for the SQLAlchemy asyncio extension package.

This dialect should normally be used only with the create_async_engine() engine creation function:

Support for the MySQL / MariaDB database via the CyMySQL driver.

Documentation and download information (if applicable) for CyMySQL is available at: https://github.com/nakagami/CyMySQL

The CyMySQL dialect is not tested as part of SQLAlchemy’s continuous integration and may have unresolved issues. The recommended MySQL dialects are mysqlclient and PyMySQL.

Support for the MySQL / MariaDB database via the PyODBC driver.

Documentation and download information (if applicable) for PyODBC is available at: https://pypi.org/project/pyodbc/

The PyODBC for MySQL dialect is not tested as part of SQLAlchemy’s continuous integration. The recommended MySQL dialects are mysqlclient and PyMySQL. However, if you want to use the mysql+pyodbc dialect and require full support for utf8mb4 characters (including supplementary characters like emoji) be sure to use a current release of MySQL Connector/ODBC and specify the “ANSI” (not “Unicode”) version of the driver in your DSN or connection string.

Pass through exact pyodbc connection string:

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
engine = create_engine(
    "mysql+pymysql://user:pass@some_mariadb/dbname?charset=utf8mb4"
)
```

Example 2 (python):
```python
engine = create_engine(
    "mariadb+pymysql://user:pass@some_mariadb/dbname?charset=utf8mb4"
)
```

Example 3 (unknown):
```unknown
my_table = Table(
    "mytable",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("textdata", String(50)),
    mariadb_engine="InnoDB",
    mysql_engine="InnoDB",
)

Index(
    "textdata_ix",
    my_table.c.textdata,
    mysql_prefix="FULLTEXT",
    mariadb_prefix="FULLTEXT",
)
```

Example 4 (unknown):
```unknown
engine = create_engine("mysql+mysqldb://...", pool_recycle=3600)
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/dialects/mssql.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - Dialects
    - Project Versions
- Microsoft SQL Server¶
- DBAPI Support¶
- External Dialects¶
- Auto Increment Behavior / IDENTITY Columns¶
  - Controlling “Start” and “Increment”¶
  - Using IDENTITY with Non-Integer numeric types¶

Home | Download this Documentation

Home | Download this Documentation

Support for the Microsoft SQL Server database.

The following table summarizes current support levels for database release versions.

The following dialect/DBAPI options are available. Please refer to individual DBAPI sections for connect information.

In addition to the above DBAPI layers with native SQLAlchemy support, there are third-party dialects for other DBAPI layers that are compatible with SQL Server. See the “External Dialects” list on the Dialects page.

SQL Server provides so-called “auto incrementing” behavior using the IDENTITY construct, which can be placed on any single integer column in a table. SQLAlchemy considers IDENTITY within its default “autoincrement” behavior for an integer primary key column, described at Column.autoincrement. This means that by default, the first integer primary key column in a Table will be considered to be the identity column - unless it is associated with a Sequence - and will generate DDL as such:

The above example will generate DDL as:

For the case where this default generation of IDENTITY is not desired, specify False for the Column.autoincrement flag, on the first integer primary key column:

To add the IDENTITY keyword to a non-primary key column, specify True for the Column.autoincrement flag on the desired Column object, and ensure that Column.autoincrement is set to False on any integer primary key column:

Changed in version 1.4: Added Identity construct in a Column to specify the start and increment parameters of an IDENTITY. These replace the use of the Sequence object in order to specify these values.

Deprecated since version 1.4: The mssql_identity_start and mssql_identity_increment parameters to Column are deprecated and should we replaced by an Identity object. Specifying both ways of configuring an IDENTITY will result in a compile error. These options are also no longer returned as part of the dialect_options key in Inspector.get_columns(). Use the information in the identity key instead.

Deprecated since version 1.3: The use of Sequence to specify IDENTITY characteristics is deprecated and will be removed in a future release. Please use the Identity object parameters Identity.start and Identity.increment.

Changed in version 1.4: Removed the ability to use a Sequence object to modify IDENTITY characteristics. Sequence objects now only manipulate true T-SQL SEQUENCE types.

There can only be one IDENTITY column on the table. When using autoincrement=True to enable the IDENTITY keyword, SQLAlchemy does not guard against multiple columns specifying the option simultaneously. The SQL Server database will instead reject the CREATE TABLE statement.

An INSERT statement which attempts to provide a value for a column that is marked with IDENTITY will be rejected by SQL Server. In order for the value to be accepted, a session-level option “SET IDENTITY_INSERT” must be enabled. The SQLAlchemy SQL Server dialect will perform this operation automatically when using a core Insert construct; if the execution specifies a value for the IDENTITY column, the “IDENTITY_INSERT” option will be enabled for the span of that statement’s invocation.However, this scenario is not high performing and should not be relied upon for normal use. If a table doesn’t actually require IDENTITY behavior in its integer primary key column, the keyword should be disabled when creating the table by ensuring that autoincrement=False is set.

Specific control over the “start” and “increment” values for the IDENTITY generator are provided using the Identity.start and Identity.increment parameters passed to the Identity object:

The CREATE TABLE for the above Table object would be:

The Identity object supports many other parameter in addition to start and increment. These are not supported by SQL Server and will be ignored when generating the CREATE TABLE ddl.

Changed in version 1.3.19: The Identity object is now used to affect the IDENTITY generator for a Column under SQL Server. Previously, the Sequence object was used. As SQL Server now supports real sequences as a separate construct, Sequence will be functional in the normal way starting from SQLAlchemy version 1.4.

SQL Server also allows IDENTITY to be used with NUMERIC columns. To implement this pattern smoothly in SQLAlchemy, the primary datatype of the column should remain as Integer, however the underlying implementation type deployed to the SQL Server database can be specified as Numeric using TypeEngine.with_variant():

In the above example, Integer().with_variant() provides clear usage information that accurately describes the intent of the code. The general restriction that autoincrement only applies to Integer is established at the metadata level and not at the per-dialect level.

When using the above pattern, the primary key identifier that comes back from the insertion of a row, which is also the value that would be assigned to an ORM object such as TestTable above, will be an instance of Decimal() and not int when using SQL Server. The numeric return type of the Numeric type can be changed to return floats by passing False to Numeric.asdecimal. To normalize the return type of the above Numeric(10, 0) to return Python ints (which also support “long” integer values in Python 3), use TypeDecorator as follows:

Handling of the IDENTITY column at INSERT time involves two key techniques. The most common is being able to fetch the “last inserted value” for a given IDENTITY column, a process which SQLAlchemy performs implicitly in many cases, most importantly within the ORM.

The process for fetching this value has several variants:

In the vast majority of cases, RETURNING is used in conjunction with INSERT statements on SQL Server in order to get newly generated primary key values:

As of SQLAlchemy 2.0, the “Insert Many Values” Behavior for INSERT statements feature is also used by default to optimize many-row INSERT statements; for SQL Server the feature takes place for both RETURNING and-non RETURNING INSERT statements.

Changed in version 2.0.10: The “Insert Many Values” Behavior for INSERT statements feature for SQL Server was temporarily disabled for SQLAlchemy version 2.0.9 due to issues with row ordering. As of 2.0.10 the feature is re-enabled, with special case handling for the unit of work’s requirement for RETURNING to be ordered.

When RETURNING is not available or has been disabled via implicit_returning=False, either the scope_identity() function or the @@identity variable is used; behavior varies by backend:

when using PyODBC, the phrase ; select scope_identity() will be appended to the end of the INSERT statement; a second result set will be fetched in order to receive the value. Given a table as:

an INSERT will look like:

Other dialects such as pymssql will call upon SELECT scope_identity() AS lastrowid subsequent to an INSERT statement. If the flag use_scope_identity=False is passed to create_engine(), the statement SELECT @@identity AS lastrowid is used instead.

A table that contains an IDENTITY column will prohibit an INSERT statement that refers to the identity column explicitly. The SQLAlchemy dialect will detect when an INSERT construct, created using a core insert() construct (not a plain string SQL), refers to the identity column, and in this case will emit SET IDENTITY_INSERT ON prior to the insert statement proceeding, and SET IDENTITY_INSERT OFF subsequent to the execution. Given this example:

The above column will be created with IDENTITY, however the INSERT statement we emit is specifying explicit values. In the echo output we can see how SQLAlchemy handles this:

This is an auxiliary use case suitable for testing and bulk insert scenarios.

The Sequence object creates “real” sequences, i.e., CREATE SEQUENCE:

For integer primary key generation, SQL Server’s IDENTITY construct should generally be preferred vs. sequence.

The default start value for T-SQL is -2**63 instead of 1 as in most other SQL databases. Users should explicitly set the Sequence.start to 1 if that’s the expected default:

Added in version 1.4: added SQL Server support for Sequence

Changed in version 2.0: The SQL Server dialect will no longer implicitly render “START WITH 1” for CREATE SEQUENCE, which was the behavior first implemented in version 1.4.

SQL Server supports the special string “MAX” within the VARCHAR and NVARCHAR datatypes, to indicate “maximum length possible”. The dialect currently handles this as a length of “None” in the base type, rather than supplying a dialect-specific version of these types, so that a base type specified such as VARCHAR(None) can assume “unlengthed” behavior on more than one backend without using dialect-specific types.

To build a SQL Server VARCHAR or NVARCHAR with MAX length, use None:

Character collations are supported by the base string types, specified by the string argument “collation”:

When such a column is associated with a Table, the CREATE TABLE statement for this column will yield:

MSSQL has added support for LIMIT / OFFSET as of SQL Server 2012, via the “OFFSET n ROWS” and “FETCH NEXT n ROWS” clauses. SQLAlchemy supports these syntaxes automatically if SQL Server 2012 or greater is detected.

Changed in version 1.4: support added for SQL Server “OFFSET n ROWS” and “FETCH NEXT n ROWS” syntax.

For statements that specify only LIMIT and no OFFSET, all versions of SQL Server support the TOP keyword. This syntax is used for all SQL Server versions when no OFFSET clause is present. A statement such as:

will render similarly to:

For versions of SQL Server prior to SQL Server 2012, a statement that uses LIMIT and OFFSET, or just OFFSET alone, will be rendered using the ROW_NUMBER() window function. A statement such as:

will render similarly to:

Note that when using LIMIT and/or OFFSET, whether using the older or newer SQL Server syntaxes, the statement must have an ORDER BY as well, else a CompileError is raised.

Comment support, which includes DDL rendering for attributes such as Table.comment and Column.comment, as well as the ability to reflect these comments, is supported assuming a supported version of SQL Server is in use. If a non-supported version such as Azure Synapse is detected at first-connect time (based on the presence of the fn_listextendedproperty SQL function), comment support including rendering and table-comment reflection is disabled, as both features rely upon SQL Server stored procedures and functions that are not available on all backend types.

To force comment support to be on or off, bypassing autodetection, set the parameter supports_comments within create_engine():

Added in version 2.0: Added support for table and column comments for the SQL Server dialect, including DDL generation and reflection.

All SQL Server dialects support setting of transaction isolation level both via a dialect-specific parameter create_engine.isolation_level accepted by create_engine(), as well as the Connection.execution_options.isolation_level argument as passed to Connection.execution_options(). This feature works by issuing the command SET TRANSACTION ISOLATION LEVEL <level> for each new connection.

To set isolation level using create_engine():

To set using per-connection execution options:

Valid values for isolation_level include:

AUTOCOMMIT - pyodbc / pymssql-specific

SNAPSHOT - specific to SQL Server

There are also more options for isolation level configurations, such as “sub-engine” objects linked to a main Engine which each apply different isolation level settings. See the discussion at Setting Transaction Isolation Levels including DBAPI Autocommit for background.

Setting Transaction Isolation Levels including DBAPI Autocommit

The QueuePool connection pool implementation used by the SQLAlchemy Engine object includes reset on return behavior that will invoke the DBAPI .rollback() method when connections are returned to the pool. While this rollback will clear out the immediate state used by the previous transaction, it does not cover a wider range of session-level state, including temporary tables as well as other server state such as prepared statement handles and statement caches. An undocumented SQL Server procedure known as sp_reset_connection is known to be a workaround for this issue which will reset most of the session state that builds up on a connection, including temporary tables.

To install sp_reset_connection as the means of performing reset-on-return, the PoolEvents.reset() event hook may be used, as demonstrated in the example below. The create_engine.pool_reset_on_return parameter is set to None so that the custom scheme can replace the default behavior completely. The custom hook implementation calls .rollback() in any case, as it’s usually important that the DBAPI’s own tracking of commit/rollback will remain consistent with the state of the transaction:

Changed in version 2.0.0b3: Added additional state arguments to the PoolEvents.reset() event and additionally ensured the event is invoked for all “reset” occurrences, so that it’s appropriate as a place for custom “reset” handlers. Previous schemes which use the PoolEvents.checkin() handler remain usable as well.

Reset On Return - in the Connection Pooling documentation

MSSQL has support for three levels of column nullability. The default nullability allows nulls and is explicit in the CREATE TABLE construct:

If nullable=None is specified then no specification is made. In other words the database’s configured default is used. This will render:

If nullable is True or False then the column will be NULL or NOT NULL respectively.

DATE and TIME are supported. Bind parameters are converted to datetime.datetime() objects as required by most MSSQL drivers, and results are processed from strings if needed. The DATE and TIME types are not available for MSSQL 2005 and previous - if a server version below 2008 is detected, DDL for these types will be issued as DATETIME.

Per SQL Server 2012/2014 Documentation, the NTEXT, TEXT and IMAGE datatypes are to be removed from SQL Server in a future release. SQLAlchemy normally relates these types to the UnicodeText, TextClause and LargeBinary datatypes.

In order to accommodate this change, a new flag deprecate_large_types is added to the dialect, which will be automatically set based on detection of the server version in use, if not otherwise set by the user. The behavior of this flag is as follows:

When this flag is True, the UnicodeText, TextClause and LargeBinary datatypes, when used to render DDL, will render the types NVARCHAR(max), VARCHAR(max), and VARBINARY(max), respectively. This is a new behavior as of the addition of this flag.

When this flag is False, the UnicodeText, TextClause and LargeBinary datatypes, when used to render DDL, will render the types NTEXT, TEXT, and IMAGE, respectively. This is the long-standing behavior of these types.

The flag begins with the value None, before a database connection is established. If the dialect is used to render DDL without the flag being set, it is interpreted the same as False.

On first connection, the dialect detects if SQL Server version 2012 or greater is in use; if the flag is still at None, it sets it to True or False based on whether 2012 or greater is detected.

The flag can be set to either True or False when the dialect is created, typically via create_engine():

Complete control over whether the “old” or “new” types are rendered is available in all SQLAlchemy versions by using the UPPERCASE type objects instead: NVARCHAR, VARCHAR, VARBINARY, TEXT, NTEXT, IMAGE will always remain fixed and always output exactly that type.

SQL Server schemas sometimes require multiple parts to their “schema” qualifier, that is, including the database name and owner name as separate tokens, such as mydatabase.dbo.some_table. These multipart names can be set at once using the Table.schema argument of Table:

When performing operations such as table or component reflection, a schema argument that contains a dot will be split into separate “database” and “owner” components in order to correctly query the SQL Server information schema tables, as these two values are stored separately. Additionally, when rendering the schema name for DDL or SQL, the two components will be quoted separately for case sensitive names and other special characters. Given an argument as below:

The above schema would be rendered as [MyDataBase].dbo, and also in reflection, would be reflected using “dbo” as the owner and “MyDataBase” as the database name.

To control how the schema name is broken into database / owner, specify brackets (which in SQL Server are quoting characters) in the name. Below, the “owner” will be considered as MyDataBase.dbo and the “database” will be None:

To individually specify both database and owner name with special characters or embedded dots, use two sets of brackets:

Changed in version 1.2: the SQL Server dialect now treats brackets as identifier delimiters splitting the schema into separate database and owner tokens, to allow dots within either name itself.

Very old versions of the MSSQL dialect introduced the behavior such that a schema-qualified table would be auto-aliased when used in a SELECT statement; given a table:

this legacy mode of rendering would assume that “customer_schema.account” would not be accepted by all parts of the SQL statement, as illustrated below:

This mode of behavior is now off by default, as it appears to have served no purpose; however in the case that legacy applications rely upon it, it is available using the legacy_schema_aliasing argument to create_engine() as illustrated above.

Deprecated since version 1.4: The legacy_schema_aliasing flag is now deprecated and will be removed in a future release.

The MSSQL dialect supports clustered indexes (and primary keys) via the mssql_clustered option. This option is available to Index, UniqueConstraint. and PrimaryKeyConstraint. For indexes this option can be combined with the mssql_columnstore one to create a clustered columnstore index.

To generate a clustered index:

which renders the index as CREATE CLUSTERED INDEX my_index ON table (x).

To generate a clustered primary key use:

which will render the table, for example, as:

Similarly, we can generate a clustered unique constraint using:

To explicitly request a non-clustered primary key (for example, when a separate clustered index is desired), use:

which will render the table, for example, as:

The MSSQL dialect supports columnstore indexes via the mssql_columnstore option. This option is available to Index. It be combined with the mssql_clustered option to create a clustered columnstore index.

To generate a columnstore index:

which renders the index as CREATE COLUMNSTORE INDEX my_index ON table (x).

To generate a clustered columnstore index provide no columns:

the above renders the index as CREATE CLUSTERED COLUMNSTORE INDEX my_index ON table.

Added in version 2.0.18.

In addition to clustering, the MSSQL dialect supports other special options for Index.

The mssql_include option renders INCLUDE(colname) for the given string names:

would render the index as CREATE INDEX my_index ON table (x) INCLUDE (y)

The mssql_where option renders WHERE(condition) for the given string names:

would render the index as CREATE INDEX my_index ON table (x) WHERE x > 10.

Added in version 1.3.4.

Index ordering is available via functional expressions, such as:

would render the index as CREATE INDEX my_index ON table (x DESC)

MSSQL supports the notion of setting compatibility levels at the database level. This allows, for instance, to run a database that is compatible with SQL2000 while running on a SQL2005 database server. server_version_info will always return the database server version information (in this case SQL2005) and not the compatibility level information. Because of this, if running under a backwards compatibility mode SQLAlchemy may attempt to use T-SQL statements that are unable to be parsed by the database server.

SQLAlchemy by default uses OUTPUT INSERTED to get at newly generated primary key values via IDENTITY columns or other server side defaults. MS-SQL does not allow the usage of OUTPUT INSERTED on tables that have triggers. To disable the usage of OUTPUT INSERTED on a per-table basis, specify implicit_returning=False for each Table which has triggers:

The SQL Server drivers may have limited ability to return the number of rows updated from an UPDATE or DELETE statement.

As of this writing, the PyODBC driver is not able to return a rowcount when OUTPUT INSERTED is used. Previous versions of SQLAlchemy therefore had limitations for features such as the “ORM Versioning” feature that relies upon accurate rowcounts in order to match version numbers with matched rows.

SQLAlchemy 2.0 now retrieves the “rowcount” manually for these particular use cases based on counting the rows that arrived back within RETURNING; so while the driver still has this limitation, the ORM Versioning feature is no longer impacted by it. As of SQLAlchemy 2.0.5, ORM versioning has been fully re-enabled for the pyodbc driver.

Changed in version 2.0.5: ORM versioning support is restored for the pyodbc driver. Previously, a warning would be emitted during ORM flush that versioning was not supported.

SQL Server has a default transaction isolation mode that locks entire tables, and causes even mildly concurrent applications to have long held locks and frequent deadlocks. Enabling snapshot isolation for the database as a whole is recommended for modern levels of concurrency support. This is accomplished via the following ALTER DATABASE commands executed at the SQL prompt:

Background on SQL Server snapshot isolation is available at https://msdn.microsoft.com/en-us/library/ms175095.aspx.

try_cast(expression, type_)

Produce a TRY_CAST expression for backends which support it; this is a CAST which returns NULL for un-castable conversions.

Produce a TRY_CAST expression for backends which support it; this is a CAST which returns NULL for un-castable conversions.

In SQLAlchemy, this construct is supported only by the SQL Server dialect, and will raise a CompileError if used on other included backends. However, third party backends may also support this construct.

As try_cast() originates from the SQL Server dialect, it’s importable both from sqlalchemy. as well as from sqlalchemy.dialects.mssql.

try_cast() returns an instance of TryCast and generally behaves similarly to the Cast construct; at the SQL level, the difference between CAST and TRY_CAST is that TRY_CAST returns NULL for an un-castable expression, such as attempting to cast a string "hi" to an integer value.

The above would render on Microsoft SQL Server as:

Added in version 2.0.14: try_cast() has been generalized from the SQL Server dialect into a general use construct that may be supported by additional dialects.

As with all SQLAlchemy dialects, all UPPERCASE types that are known to be valid with SQL server are importable from the top level dialect, whether they originate from sqlalchemy.types or from the local dialect:

Types which are specific to SQL Server, or have SQL Server-specific construction arguments, are as follows:

the SQL Server DOUBLE PRECISION datatype.

MSSQL NTEXT type, for variable-length unicode text up to 2^30 characters.

the SQL Server REAL datatype.

Implement the SQL Server ROWVERSION type.

Implement the SQL Server TIMESTAMP type.

inherits from sqlalchemy.types.Boolean

Both pyodbc and pymssql return values from BIT columns as Python <class ‘bool’> so just subclass Boolean.

inherited from the sqlalchemy.types.Boolean.__init__ method of Boolean

defaults to False. If the boolean is generated as an int/smallint, also create a CHECK constraint on the table that ensures 1 or 0 as a value.

it is strongly recommended that the CHECK constraint have an explicit name in order to support schema-management concerns. This can be established either by setting the Boolean.name parameter or by setting up an appropriate naming convention; see Configuring Constraint Naming Conventions for background.

Changed in version 1.4: - this flag now defaults to False, meaning no CHECK constraint is generated for a non-native enumerated type.

name¶ – if a CHECK constraint is generated, specify the name of the constraint.

inherits from sqlalchemy.types.String

inherited from the sqlalchemy.types.String.__init__ method of String

Create a string-holding type.

length¶ – optional, a length for the column for use in DDL and CAST expressions. May be safely omitted if no CREATE TABLE will be issued. Certain databases may require a length for use in DDL, and will raise an exception when the CREATE TABLE DDL is issued if a VARCHAR with no length is included. Whether the value is interpreted as bytes or characters is database specific.

Optional, a column-level collation for use in DDL and CAST expressions. Renders using the COLLATE keyword supported by SQLite, MySQL, and PostgreSQL. E.g.:

In most cases, the Unicode or UnicodeText datatypes should be used for a Column that expects to store non-ascii data. These datatypes will ensure that the correct types are used on the database.

inherits from sqlalchemy.dialects.mssql.base._DateTimeBase, sqlalchemy.types.DateTime

inherits from sqlalchemy.dialects.mssql.base._DateTimeBase, sqlalchemy.types.DateTime

inherits from sqlalchemy.types.DOUBLE_PRECISION

the SQL Server DOUBLE PRECISION datatype.

Added in version 2.0.11.

inherits from sqlalchemy.types.LargeBinary

Construct a LargeBinary type.

inherited from the sqlalchemy.types.LargeBinary.__init__ method of LargeBinary

Construct a LargeBinary type.

length¶ – optional, a length for the column for use in DDL statements, for those binary types that accept a length, such as the MySQL BLOB type.

inherits from sqlalchemy.types.JSON

MSSQL supports JSON-formatted data as of SQL Server 2016.

The JSON datatype at the DDL level will represent the datatype as NVARCHAR(max), but provides for JSON-level comparison functions as well as Python coercion behavior.

JSON is used automatically whenever the base JSON datatype is used against a SQL Server backend.

JSON - main documentation for the generic cross-platform JSON datatype.

The JSON type supports persistence of JSON values as well as the core index operations provided by JSON datatype, by adapting the operations to render the JSON_VALUE or JSON_QUERY functions at the database level.

The SQL Server JSON type necessarily makes use of the JSON_QUERY and JSON_VALUE functions when querying for elements of a JSON object. These two functions have a major restriction in that they are mutually exclusive based on the type of object to be returned. The JSON_QUERY function only returns a JSON dictionary or list, but not an individual string, numeric, or boolean element; the JSON_VALUE function only returns an individual string, numeric, or boolean element. both functions either return NULL or raise an error if they are not used against the correct expected value.

To handle this awkward requirement, indexed access rules are as follows:

When extracting a sub element from a JSON that is itself a JSON dictionary or list, the Comparator.as_json() accessor should be used:

When extracting a sub element from a JSON that is a plain boolean, string, integer, or float, use the appropriate method among Comparator.as_boolean(), Comparator.as_string(), Comparator.as_integer(), Comparator.as_float():

Added in version 1.4.

Construct a JSON type.

inherited from the sqlalchemy.types.JSON.__init__ method of JSON

Construct a JSON type.

none_as_null=False¶ –

if True, persist the value None as a SQL NULL value, not the JSON encoding of null. Note that when this flag is False, the null() construct can still be used to persist a NULL value, which may be passed directly as a parameter value that is specially interpreted by the JSON type as SQL NULL:

JSON.none_as_null does not apply to the values passed to Column.default and Column.server_default; a value of None passed for these parameters means “no default present”.

Additionally, when used in SQL comparison expressions, the Python value None continues to refer to SQL null, and not JSON NULL. The JSON.none_as_null flag refers explicitly to the persistence of the value within an INSERT or UPDATE statement. The JSON.NULL value should be used for SQL expressions that wish to compare to JSON null.

inherits from sqlalchemy.types.TypeEngine

inherits from sqlalchemy.types.Unicode

inherited from the sqlalchemy.types.String.__init__ method of String

Create a string-holding type.

length¶ – optional, a length for the column for use in DDL and CAST expressions. May be safely omitted if no CREATE TABLE will be issued. Certain databases may require a length for use in DDL, and will raise an exception when the CREATE TABLE DDL is issued if a VARCHAR with no length is included. Whether the value is interpreted as bytes or characters is database specific.

Optional, a column-level collation for use in DDL and CAST expressions. Renders using the COLLATE keyword supported by SQLite, MySQL, and PostgreSQL. E.g.:

In most cases, the Unicode or UnicodeText datatypes should be used for a Column that expects to store non-ascii data. These datatypes will ensure that the correct types are used on the database.

inherits from sqlalchemy.types.UnicodeText

MSSQL NTEXT type, for variable-length unicode text up to 2^30 characters.

Create a string-holding type.

inherited from the sqlalchemy.types.String.__init__ method of String

Create a string-holding type.

length¶ – optional, a length for the column for use in DDL and CAST expressions. May be safely omitted if no CREATE TABLE will be issued. Certain databases may require a length for use in DDL, and will raise an exception when the CREATE TABLE DDL is issued if a VARCHAR with no length is included. Whether the value is interpreted as bytes or characters is database specific.

Optional, a column-level collation for use in DDL and CAST expressions. Renders using the COLLATE keyword supported by SQLite, MySQL, and PostgreSQL. E.g.:

In most cases, the Unicode or UnicodeText datatypes should be used for a Column that expects to store non-ascii data. These datatypes will ensure that the correct types are used on the database.

inherits from sqlalchemy.types.Unicode

The SQL NVARCHAR type.

inherited from the sqlalchemy.types.String.__init__ method of String

Create a string-holding type.

length¶ – optional, a length for the column for use in DDL and CAST expressions. May be safely omitted if no CREATE TABLE will be issued. Certain databases may require a length for use in DDL, and will raise an exception when the CREATE TABLE DDL is issued if a VARCHAR with no length is included. Whether the value is interpreted as bytes or characters is database specific.

Optional, a column-level collation for use in DDL and CAST expressions. Renders using the COLLATE keyword supported by SQLite, MySQL, and PostgreSQL. E.g.:

In most cases, the Unicode or UnicodeText datatypes should be used for a Column that expects to store non-ascii data. These datatypes will ensure that the correct types are used on the database.

inherits from sqlalchemy.types.REAL

the SQL Server REAL datatype.

inherits from sqlalchemy.dialects.mssql.base.TIMESTAMP

Implement the SQL Server ROWVERSION type.

The ROWVERSION datatype is a SQL Server synonym for the TIMESTAMP datatype, however current SQL Server documentation suggests using ROWVERSION for new datatypes going forward.

The ROWVERSION datatype does not reflect (e.g. introspect) from the database as itself; the returned datatype will be TIMESTAMP.

This is a read-only datatype that does not support INSERT of values.

Added in version 1.2.

Construct a TIMESTAMP or ROWVERSION type.

inherited from the sqlalchemy.dialects.mssql.base.TIMESTAMP.__init__ method of TIMESTAMP

Construct a TIMESTAMP or ROWVERSION type.

convert_int¶ – if True, binary integer values will be converted to integers on read.

Added in version 1.2.

inherits from sqlalchemy.dialects.mssql.base._DateTimeBase, sqlalchemy.types.DateTime

Construct a new DateTime.

inherited from the sqlalchemy.types.DateTime.__init__ method of DateTime

Construct a new DateTime.

timezone¶ – boolean. Indicates that the datetime type should enable timezone support, if available on the base date/time-holding type only. It is recommended to make use of the TIMESTAMP datatype directly when using this flag, as some databases include separate generic date/time-holding types distinct from the timezone-capable TIMESTAMP datatype, such as Oracle Database.

inherits from sqlalchemy.types.TypeEngine

inherits from sqlalchemy.types.TypeEngine

inherits from sqlalchemy.types.Text

inherited from the sqlalchemy.types.String.__init__ method of String

Create a string-holding type.

length¶ – optional, a length for the column for use in DDL and CAST expressions. May be safely omitted if no CREATE TABLE will be issued. Certain databases may require a length for use in DDL, and will raise an exception when the CREATE TABLE DDL is issued if a VARCHAR with no length is included. Whether the value is interpreted as bytes or characters is database specific.

Optional, a column-level collation for use in DDL and CAST expressions. Renders using the COLLATE keyword supported by SQLite, MySQL, and PostgreSQL. E.g.:

In most cases, the Unicode or UnicodeText datatypes should be used for a Column that expects to store non-ascii data. These datatypes will ensure that the correct types are used on the database.

inherits from sqlalchemy.types.TIME

inherits from sqlalchemy.types._Binary

Implement the SQL Server TIMESTAMP type.

Note this is completely different than the SQL Standard TIMESTAMP type, which is not supported by SQL Server. It is a read-only datatype that does not support INSERT of values.

Added in version 1.2.

Construct a TIMESTAMP or ROWVERSION type.

Construct a TIMESTAMP or ROWVERSION type.

convert_int¶ – if True, binary integer values will be converted to integers on read.

Added in version 1.2.

inherits from sqlalchemy.types.Integer

inherits from sqlalchemy.types.Uuid

Construct a UNIQUEIDENTIFIER type.

Construct a UNIQUEIDENTIFIER type.

if True, values will be interpreted as Python uuid objects, converting to/from string via the DBAPI.

inherits from sqlalchemy.types.VARBINARY, sqlalchemy.types.LargeBinary

The MSSQL VARBINARY type.

This type adds additional features to the core VARBINARY type, including “deprecate_large_types” mode where either VARBINARY(max) or IMAGE is rendered, as well as the SQL Server FILESTREAM option.

Large Text/Binary Type Deprecation

Construct a VARBINARY type.

length¶ – optional, a length for the column for use in DDL statements, for those binary types that accept a length, such as the MySQL BLOB type.

if True, renders the FILESTREAM keyword in the table definition. In this case length must be None or 'max'.

Added in version 1.4.31.

inherits from sqlalchemy.types.String

The SQL VARCHAR type.

inherited from the sqlalchemy.types.String.__init__ method of String

Create a string-holding type.

length¶ – optional, a length for the column for use in DDL and CAST expressions. May be safely omitted if no CREATE TABLE will be issued. Certain databases may require a length for use in DDL, and will raise an exception when the CREATE TABLE DDL is issued if a VARCHAR with no length is included. Whether the value is interpreted as bytes or characters is database specific.

Optional, a column-level collation for use in DDL and CAST expressions. Renders using the COLLATE keyword supported by SQLite, MySQL, and PostgreSQL. E.g.:

In most cases, the Unicode or UnicodeText datatypes should be used for a Column that expects to store non-ascii data. These datatypes will ensure that the correct types are used on the database.

inherits from sqlalchemy.types.Text

This is a placeholder type for reflection purposes that does not include any Python-side datatype support. It also does not currently support additional arguments, such as “CONTENT”, “DOCUMENT”, “xml_schema_collection”.

Create a string-holding type.

inherited from the sqlalchemy.types.String.__init__ method of String

Create a string-holding type.

length¶ – optional, a length for the column for use in DDL and CAST expressions. May be safely omitted if no CREATE TABLE will be issued. Certain databases may require a length for use in DDL, and will raise an exception when the CREATE TABLE DDL is issued if a VARCHAR with no length is included. Whether the value is interpreted as bytes or characters is database specific.

Optional, a column-level collation for use in DDL and CAST expressions. Renders using the COLLATE keyword supported by SQLite, MySQL, and PostgreSQL. E.g.:

In most cases, the Unicode or UnicodeText datatypes should be used for a Column that expects to store non-ascii data. These datatypes will ensure that the correct types are used on the database.

Support for the Microsoft SQL Server database via the PyODBC driver.

Documentation and download information (if applicable) for PyODBC is available at: https://pypi.org/project/pyodbc/

The URL here is to be translated to PyODBC connection strings, as detailed in ConnectionStrings.

A DSN connection in ODBC means that a pre-existing ODBC datasource is configured on the client machine. The application then specifies the name of this datasource, which encompasses details such as the specific ODBC driver in use as well as the network address of the database. Assuming a datasource is configured on the client, a basic DSN-based connection looks like:

Which above, will pass the following connection string to PyODBC:

If the username and password are omitted, the DSN form will also add the Trusted_Connection=yes directive to the ODBC string.

Hostname-based connections are also supported by pyodbc. These are often easier to use than a DSN and have the additional advantage that the specific database name to connect towards may be specified locally in the URL, rather than it being fixed as part of a datasource configuration.

When using a hostname connection, the driver name must also be specified in the query parameters of the URL. As these names usually have spaces in them, the name must be URL encoded which means using plus signs for spaces:

The driver keyword is significant to the pyodbc dialect and must be specified in lowercase.

Any other names passed in the query string are passed through in the pyodbc connect string, such as authentication, TrustServerCertificate, etc. Multiple keyword arguments must be separated by an ampersand (&); these will be translated to semicolons when the pyodbc connect string is generated internally:

The equivalent URL can be constructed using URL:

A PyODBC connection string can also be sent in pyodbc’s format directly, as specified in the PyODBC documentation, using the parameter odbc_connect. A URL object can help make this easier:

Some database servers are set up to only accept access tokens for login. For example, SQL Server allows the use of Azure Active Directory tokens to connect to databases. This requires creating a credential object using the azure-identity library. More information about the authentication step can be found in Microsoft’s documentation.

After getting an engine, the credentials need to be sent to pyodbc.connect each time a connection is requested. One way to do this is to set up an event listener on the engine that adds the credential token to the dialect’s connect call. This is discussed more generally in Generating dynamic authentication tokens. For SQL Server in particular, this is passed as an ODBC connection attribute with a data structure described by Microsoft.

The following code snippet will create an engine that connects to an Azure SQL database using Azure credentials:

The Trusted_Connection token is currently added by the SQLAlchemy pyodbc dialect when no username or password is present. This needs to be removed per Microsoft’s documentation for Azure access tokens, stating that a connection string when using an access token must not contain UID, PWD, Authentication or Trusted_Connection parameters.

Azure Synapse Analytics has a significant difference in its transaction handling compared to plain SQL Server; in some cases an error within a Synapse transaction can cause it to be arbitrarily terminated on the server side, which then causes the DBAPI .rollback() method (as well as .commit()) to fail. The issue prevents the usual DBAPI contract of allowing .rollback() to pass silently if no transaction is present as the driver does not expect this condition. The symptom of this failure is an exception with a message resembling ‘No corresponding transaction found. (111214)’ when attempting to emit a .rollback() after an operation had a failure of some kind.

This specific case can be handled by passing ignore_no_transaction_on_rollback=True to the SQL Server dialect via the create_engine() function as follows:

Using the above parameter, the dialect will catch ProgrammingError exceptions raised during connection.rollback() and emit a warning if the error message contains code 111214, however will not raise an exception.

Added in version 1.4.40: Added the ignore_no_transaction_on_rollback=True parameter.

Azure SQL Data Warehouse does not support transactions, and that can cause problems with SQLAlchemy’s “autobegin” (and implicit commit/rollback) behavior. We can avoid these problems by enabling autocommit at both the pyodbc and engine levels:

By default, for historical reasons, Microsoft’s ODBC drivers for SQL Server send long string parameters (greater than 4000 SBCS characters or 2000 Unicode characters) as TEXT/NTEXT values. TEXT and NTEXT have been deprecated for many years and are starting to cause compatibility issues with newer versions of SQL_Server/Azure. For example, see this issue.

Starting with ODBC Driver 18 for SQL Server we can override the legacy behavior and pass long strings as varchar(max)/nvarchar(max) using the LongAsMax=Yes connection string parameter:

PyODBC uses internal pooling by default, which means connections will be longer lived than they are within SQLAlchemy itself. As SQLAlchemy has its own pooling behavior, it is often preferable to disable this behavior. This behavior can only be disabled globally at the PyODBC module level, before any connections are made:

If this variable is left at its default value of True, the application will continue to maintain active database connections, even when the SQLAlchemy engine itself fully discards a connection or if the engine is disposed.

pooling - in the PyODBC documentation.

PyODBC works best with Microsoft ODBC drivers, particularly in the area of Unicode support on both Python 2 and Python 3.

Using the FreeTDS ODBC drivers on Linux or OSX with PyODBC is not recommended; there have been historically many Unicode-related issues in this area, including before Microsoft offered ODBC drivers for Linux and OSX. Now that Microsoft offers drivers for all platforms, for PyODBC support these are recommended. FreeTDS remains relevant for non-ODBC drivers such as pymssql where it works very well.

Previous limitations with the SQLAlchemy ORM’s “versioned rows” feature with Pyodbc have been resolved as of SQLAlchemy 2.0.5. See the notes at Rowcount Support / ORM Versioning.

The PyODBC driver includes support for a “fast executemany” mode of execution which greatly reduces round trips for a DBAPI executemany() call when using Microsoft ODBC drivers, for limited size batches that fit in memory. The feature is enabled by setting the attribute .fast_executemany on the DBAPI cursor when an executemany call is to be used. The SQLAlchemy PyODBC SQL Server dialect supports this parameter by passing the fast_executemany parameter to create_engine() , when using the Microsoft ODBC driver only:

Changed in version 2.0.9: - the fast_executemany parameter now has its intended effect of this PyODBC feature taking effect for all INSERT statements that are executed with multiple parameter sets, which don’t include RETURNING. Previously, SQLAlchemy 2.0’s insertmanyvalues feature would cause fast_executemany to not be used in most cases even if specified.

Added in version 1.3.

fast executemany - on github

As of version 2.0, the pyodbc cursor.setinputsizes() method is used for all statement executions, except for cursor.executemany() calls when fast_executemany=True where it is not supported (assuming insertmanyvalues is kept enabled, “fastexecutemany” will not take place for INSERT statements in any case).

The use of cursor.setinputsizes() can be disabled by passing use_setinputsizes=False to create_engine().

When use_setinputsizes is left at its default of True, the specific per-type symbols passed to cursor.setinputsizes() can be programmatically customized using the DialectEvents.do_setinputsizes() hook. See that method for usage examples.

Changed in version 2.0: The mssql+pyodbc dialect now defaults to using use_setinputsizes=True for all statement executions with the exception of cursor.executemany() calls when fast_executemany=True. The behavior can be turned off by passing use_setinputsizes=False to create_engine().

Support for the Microsoft SQL Server database via the pymssql driver.

pymssql is a Python module that provides a Python DBAPI interface around FreeTDS.

Changed in version 2.0.5: pymssql was restored to SQLAlchemy’s continuous integration testing

Support for the Microsoft SQL Server database via the aioodbc driver.

Documentation and download information (if applicable) for aioodbc is available at: https://pypi.org/project/aioodbc/

Support for the SQL Server database in asyncio style, using the aioodbc driver which itself is a thread-wrapper around pyodbc.

Added in version 2.0.23: Added the mssql+aioodbc dialect which builds on top of the pyodbc and general aio* dialect architecture.

Using a special asyncio mediation layer, the aioodbc dialect is usable as the backend for the SQLAlchemy asyncio extension package.

Most behaviors and caveats for this driver are the same as that of the pyodbc dialect used on SQL Server; see PyODBC for general background.

This dialect should normally be used only with the create_async_engine() engine creation function; connection styles are otherwise equivalent to those documented in the pyodbc section:

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from sqlalchemy import Table, MetaData, Column, Integer

m = MetaData()
t = Table(
    "t",
    m,
    Column("id", Integer, primary_key=True),
    Column("x", Integer),
)
m.create_all(engine)
```

Example 2 (sql):
```sql
CREATE TABLE t (
    id INTEGER NOT NULL IDENTITY,
    x INTEGER NULL,
    PRIMARY KEY (id)
)
```

Example 3 (unknown):
```unknown
m = MetaData()
t = Table(
    "t",
    m,
    Column("id", Integer, primary_key=True, autoincrement=False),
    Column("x", Integer),
)
m.create_all(engine)
```

Example 4 (unknown):
```unknown
m = MetaData()
t = Table(
    "t",
    m,
    Column("id", Integer, primary_key=True, autoincrement=False),
    Column("x", Integer, autoincrement=True),
)
m.create_all(engine)
```

---
