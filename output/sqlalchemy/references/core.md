# Sqlalchemy - Core

**Pages:** 4

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/faq/connections.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - Frequently Asked Questions
    - Project Versions
- Connections / Engines¶
- How do I configure logging?¶
- How do I pool database connections? Are my connections pooled?¶
- How do I pass custom connect arguments to my database API?¶
- “MySQL Server has gone away”¶
- “Commands out of sync; you can’t run this command now” / “This result object does not return rows. It has been closed automatically”¶

Home | Download this Documentation

Home | Download this Documentation

How do I configure logging?

How do I pool database connections? Are my connections pooled?

How do I pass custom connect arguments to my database API?

“MySQL Server has gone away”

“Commands out of sync; you can’t run this command now” / “This result object does not return rows. It has been closed automatically”

How Do I “Retry” a Statement Execution Automatically?

Using DBAPI Autocommit Allows for a Readonly Version of Transparent Reconnect

Why does SQLAlchemy issue so many ROLLBACKs?

I’m on MyISAM - how do I turn it off?

I’m on SQL Server - how do I turn those ROLLBACKs into COMMITs?

I am using multiple connections with a SQLite database (typically to test transaction operation), and my test program is not working!

How do I get at the raw DBAPI connection when using an Engine?

Accessing the underlying connection for an asyncio driver

How do I use engines / connections / sessions with Python multiprocessing, or os.fork()?

See Configuring Logging.

SQLAlchemy performs application-level connection pooling automatically in most cases. For all included dialects (except SQLite when using a “memory” database), a Engine object refers to a QueuePool as a source of connectivity.

For more detail, see Engine Configuration and Connection Pooling.

The create_engine() call accepts additional arguments either directly via the connect_args keyword argument:

Or for basic string and integer arguments, they can usually be specified in the query string of the URL:

Custom DBAPI connect() arguments / on-connect routines

The primary cause of this error is that the MySQL connection has timed out and has been closed by the server. The MySQL server closes connections which have been idle a period of time which defaults to eight hours. To accommodate this, the immediate setting is to enable the create_engine.pool_recycle setting, which will ensure that a connection which is older than a set amount of seconds will be discarded and replaced with a new connection when it is next checked out.

For the more general case of accommodating database restarts and other temporary loss of connectivity due to network issues, connections that are in the pool may be recycled in response to more generalized disconnect detection techniques. The section Dealing with Disconnects provides background on both “pessimistic” (e.g. pre-ping) and “optimistic” (e.g. graceful recovery) techniques. Modern SQLAlchemy tends to favor the “pessimistic” approach.

Dealing with Disconnects

The MySQL drivers have a fairly wide class of failure modes whereby the state of the connection to the server is in an invalid state. Typically, when the connection is used again, one of these two error messages will occur. The reason is because the state of the server has been changed to one in which the client library does not expect, such that when the client library emits a new statement on the connection, the server does not respond as expected.

In SQLAlchemy, because database connections are pooled, the issue of the messaging being out of sync on a connection becomes more important, since when an operation fails, if the connection itself is in an unusable state, if it goes back into the connection pool, it will malfunction when checked out again. The mitigation for this issue is that the connection is invalidated when such a failure mode occurs so that the underlying database connection to MySQL is discarded. This invalidation occurs automatically for many known failure modes and can also be called explicitly via the Connection.invalidate() method.

There is also a second class of failure modes within this category where a context manager such as with session.begin_nested(): wants to “roll back” the transaction when an error occurs; however within some failure modes of the connection, the rollback itself (which can also be a RELEASE SAVEPOINT operation) also fails, causing misleading stack traces.

Originally, the cause of this error used to be fairly simple, it meant that a multithreaded program was invoking commands on a single connection from more than one thread. This applied to the original “MySQLdb” native-C driver that was pretty much the only driver in use. However, with the introduction of pure Python drivers like PyMySQL and MySQL-connector-Python, as well as increased use of tools such as gevent/eventlet, multiprocessing (often with Celery), and others, there is a whole series of factors that has been known to cause this problem, some of which have been improved across SQLAlchemy versions but others which are unavoidable:

Sharing a connection among threads - This is the original reason these kinds of errors occurred. A program used the same connection in two or more threads at the same time, meaning multiple sets of messages got mixed up on the connection, putting the server-side session into a state that the client no longer knows how to interpret. However, other causes are usually more likely today.

Sharing the filehandle for the connection among processes - This usually occurs when a program uses os.fork() to spawn a new process, and a TCP connection that is present in th parent process gets shared into one or more child processes. As multiple processes are now emitting messages to essentially the same filehandle, the server receives interleaved messages and breaks the state of the connection.

This scenario can occur very easily if a program uses Python’s “multiprocessing” module and makes use of an Engine that was created in the parent process. It’s common that “multiprocessing” is in use when using tools like Celery. The correct approach should be either that a new Engine is produced when a child process first starts, discarding any Engine that came down from the parent process; or, the Engine that’s inherited from the parent process can have it’s internal pool of connections disposed by calling Engine.dispose().

Greenlet Monkeypatching w/ Exits - When using a library like gevent or eventlet that monkeypatches the Python networking API, libraries like PyMySQL are now working in an asynchronous mode of operation, even though they are not developed explicitly against this model. A common issue is that a greenthread is interrupted, often due to timeout logic in the application. This results in the GreenletExit exception being raised, and the pure-Python MySQL driver is interrupted from its work, which may have been that it was receiving a response from the server or preparing to otherwise reset the state of the connection. When the exception cuts all that work short, the conversation between client and server is now out of sync and subsequent usage of the connection may fail. SQLAlchemy as of version 1.1.0 knows how to guard against this, as if a database operation is interrupted by a so-called “exit exception”, which includes GreenletExit and any other subclass of Python BaseException that is not also a subclass of Exception, the connection is invalidated.

Rollbacks / SAVEPOINT releases failing - Some classes of error cause the connection to be unusable within the context of a transaction, as well as when operating in a “SAVEPOINT” block. In these cases, the failure on the connection has rendered any SAVEPOINT as no longer existing, yet when SQLAlchemy, or the application, attempts to “roll back” this savepoint, the “RELEASE SAVEPOINT” operation fails, typically with a message like “savepoint does not exist”. In this case, under Python 3 there will be a chain of exceptions output, where the ultimate “cause” of the error will be displayed as well. Under Python 2, there are no “chained” exceptions, however recent versions of SQLAlchemy will attempt to emit a warning illustrating the original failure cause, while still throwing the immediate error which is the failure of the ROLLBACK.

The documentation section Dealing with Disconnects discusses the strategies available for pooled connections that have been disconnected since the last time a particular connection was checked out. The most modern feature in this regard is the create_engine.pre_ping parameter, which allows that a “ping” is emitted on a database connection when it’s retrieved from the pool, reconnecting if the current connection has been disconnected.

It’s important to note that this “ping” is only emitted before the connection is actually used for an operation. Once the connection is delivered to the caller, per the Python DBAPI specification it is now subject to an autobegin operation, which means it will automatically BEGIN a new transaction when it is first used that remains in effect for subsequent statements, until the DBAPI-level connection.commit() or connection.rollback() method is invoked.

In modern use of SQLAlchemy, a series of SQL statements are always invoked within this transactional state, assuming DBAPI autocommit mode is not enabled (more on that in the next section), meaning that no single statement is automatically committed; if an operation fails, the effects of all statements within the current transaction will be lost.

The implication that this has for the notion of “retrying” a statement is that in the default case, when a connection is lost, the entire transaction is lost. There is no useful way that the database can “reconnect and retry” and continue where it left off, since data is already lost. For this reason, SQLAlchemy does not have a transparent “reconnection” feature that works mid-transaction, for the case when the database connection has disconnected while being used. The canonical approach to dealing with mid-operation disconnects is to retry the entire operation from the start of the transaction, often by using a custom Python decorator that will “retry” a particular function several times until it succeeds, or to otherwise architect the application in such a way that it is resilient against transactions that are dropped that then cause operations to fail.

There is also the notion of extensions that can keep track of all of the statements that have proceeded within a transaction and then replay them all in a new transaction in order to approximate a “retry” operation. SQLAlchemy’s event system does allow such a system to be constructed, however this approach is also not generally useful as there is no way to guarantee that those DML statements will be working against the same state, as once a transaction has ended the state of the database in a new transaction may be totally different. Architecting “retry” explicitly into the application at the points at which transactional operations begin and commit remains the better approach since the application-level transactional methods are the ones that know best how to re-run their steps.

Otherwise, if SQLAlchemy were to provide a feature that transparently and silently “reconnected” a connection mid-transaction, the effect would be that data is silently lost. By trying to hide the problem, SQLAlchemy would make the situation much worse.

However, if we are not using transactions, then there are more options available, as the next section describes.

With the rationale for not having a transparent reconnection mechanism stated, the preceding section rests upon the assumption that the application is in fact using DBAPI-level transactions. As most DBAPIs now offer native “autocommit” settings, we can make use of these features to provide a limited form of transparent reconnect for read only, autocommit only operations. A transparent statement retry may be applied to the cursor.execute() method of the DBAPI, however it is still not safe to apply to the cursor.executemany() method of the DBAPI, as the statement may have consumed any portion of the arguments given.

The following recipe should not be used for operations that write data. Users should carefully read and understand how the recipe works and test failure modes very carefully against the specifically targeted DBAPI driver before making production use of this recipe. The retry mechanism does not guarantee prevention of disconnection errors in all cases.

A simple retry mechanism may be applied to the DBAPI level cursor.execute() method by making use of the DialectEvents.do_execute() and DialectEvents.do_execute_no_params() hooks, which will be able to intercept disconnections during statement executions. It will not intercept connection failures during result set fetch operations, for those DBAPIs that don’t fully buffer result sets. The recipe requires that the database support DBAPI level autocommit and is not guaranteed for particular backends. A single function reconnecting_engine() is presented which applies the event hooks to a given Engine object, returning an always-autocommit version that enables DBAPI-level autocommit. A connection will transparently reconnect for single-parameter and no-parameter statement executions:

Given the above recipe, a reconnection mid-transaction may be demonstrated using the following proof of concept script. Once run, it will emit a SELECT 1 statement to the database every five seconds:

Restart the database while the script runs to demonstrate the transparent reconnect operation:

The above recipe is tested for SQLAlchemy 1.4.

SQLAlchemy currently assumes DBAPI connections are in “non-autocommit” mode - this is the default behavior of the Python database API, meaning it must be assumed that a transaction is always in progress. The connection pool issues connection.rollback() when a connection is returned. This is so that any transactional resources remaining on the connection are released. On a database like PostgreSQL or MSSQL where table resources are aggressively locked, this is critical so that rows and tables don’t remain locked within connections that are no longer in use. An application can otherwise hang. It’s not just for locks, however, and is equally critical on any database that has any kind of transaction isolation, including MySQL with InnoDB. Any connection that is still inside an old transaction will return stale data, if that data was already queried on that connection within isolation. For background on why you might see stale data even on MySQL, see https://dev.mysql.com/doc/refman/5.1/en/innodb-transaction-model.html

The behavior of the connection pool’s connection return behavior can be configured using reset_on_return:

reset_on_return accepts the values commit, rollback in addition to True, False, and None. Setting to commit will cause a COMMIT as any connection is returned to the pool:

If using a SQLite :memory: database the default connection pool is the SingletonThreadPool, which maintains exactly one SQLite connection per thread. So two connections in use in the same thread will actually be the same SQLite connection. Make sure you’re not using a :memory: database so that the engine will use QueuePool (the default for non-memory databases in current SQLAlchemy versions).

Threading/Pooling Behavior - info on PySQLite’s behavior.

With a regular SA engine-level Connection, you can get at a pool-proxied version of the DBAPI connection via the Connection.connection attribute on Connection, and for the really-real DBAPI connection you can call the PoolProxiedConnection.dbapi_connection attribute on that. On regular sync drivers there is usually no need to access the non-pool-proxied DBAPI connection, as all methods are proxied through:

Changed in version 1.4.24: Added the PoolProxiedConnection.dbapi_connection attribute, which supersedes the previous PoolProxiedConnection.connection attribute which still remains available; this attribute always provides a pep-249 synchronous style connection object. The PoolProxiedConnection.driver_connection attribute is also added which will always refer to the real driver-level connection regardless of what API it presents.

When an asyncio driver is in use, there are two changes to the above scheme. The first is that when using an AsyncConnection, the PoolProxiedConnection must be accessed using the awaitable method AsyncConnection.get_raw_connection(). The returned PoolProxiedConnection in this case retains a sync-style pep-249 usage pattern, and the PoolProxiedConnection.dbapi_connection attribute refers to a a SQLAlchemy-adapted connection object which adapts the asyncio connection to a sync style pep-249 API, in other words there are two levels of proxying going on when using an asyncio driver. The actual asyncio connection is available from the driver_connection attribute. To restate the previous example in terms of asyncio looks like:

Changed in version 1.4.24: Added the PoolProxiedConnection.dbapi_connection and PoolProxiedConnection.driver_connection attributes to allow access to pep-249 connections, pep-249 adaption layers, and underlying driver connections using a consistent interface.

When using asyncio drivers, the above “DBAPI” connection is actually a SQLAlchemy-adapted form of connection which presents a synchronous-style pep-249 style API. To access the actual asyncio driver connection, which will present the original asyncio API of the driver in use, this can be accessed via the PoolProxiedConnection.driver_connection attribute of PoolProxiedConnection. For a standard pep-249 driver, PoolProxiedConnection.dbapi_connection and PoolProxiedConnection.driver_connection are synonymous.

You must ensure that you revert any isolation level settings or other operation-specific settings on the connection back to normal before returning it to the pool.

As an alternative to reverting settings, you can call the Connection.detach() method on either Connection or the proxied connection, which will de-associate the connection from the pool such that it will be closed and discarded when Connection.close() is called:

This is covered in the section Using Connection Pools with Multiprocessing or os.fork().

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (json):
```json
e = create_engine(
    "mysql+mysqldb://scott:tiger@localhost/test", connect_args={"encoding": "utf8"}
)
```

Example 2 (python):
```python
e = create_engine("mysql+mysqldb://scott:tiger@localhost/test?encoding=utf8")
```

Example 3 (python):
```python
import time

from sqlalchemy import event


def reconnecting_engine(engine, num_retries, retry_interval):
    def _run_with_retries(fn, context, cursor_obj, statement, *arg, **kw):
        for retry in range(num_retries + 1):
            try:
                fn(cursor_obj, statement, context=context, *arg)
            except engine.dialect.dbapi.Error as raw_dbapi_err:
                connection = context.root_connection
                if engine.dialect.is_disconnect(
                    raw_dbapi_err, connection.connection.dbapi_connection, cursor_obj
                ):
                    engine.logger.error(
                        "disconnection error, attempt %d/%d",
                        retry + 1,
                        num_retries + 1,
                        exc_info=True,
                    )
                    connection.invalidate()

                    # use SQLAlchemy 2.0 API if available
                    if hasattr(connection, "rollback"):
                        connection.rollback()
                    else:
                        trans = connection.get_transaction()
                        if trans:
                            trans.rollback()

                    if retry == num_retries:
                        raise

                    time.sleep(retry_interval)
                    context.cursor = cursor_obj = connection.connection.cursor()
                else:
                    raise
            else:
                return True

    e = engine.execution_options(isolation_level="AUTOCOMMIT")

    @event.listens_for(e, "do_execute_no_params")
    def do_execute_no_params(cursor_obj, statement, context):
        return _run_with_retries(
            context.dialect.do_execute_no_params, context, cursor_obj, statement
        )

    @event.listens_for(e, "do_execute")
    def do_execute(cursor_obj, statement, parameters, context):
        return _run_with_retries(
            context.dialect.do_execute, context, cursor_obj, statement, parameters
        )

    return e
```

Example 4 (python):
```python
from sqlalchemy import create_engine
from sqlalchemy import select

if __name__ == "__main__":
    engine = create_engine("mysql+mysqldb://scott:tiger@localhost/test", echo_pool=True)

    def do_a_thing(engine):
        with engine.begin() as conn:
            while True:
                print("ping: %s" % conn.execute(select([1])).scalar())
                time.sleep(5)

    e = reconnecting_engine(
        create_engine("mysql+mysqldb://scott:tiger@localhost/test", echo_pool=True),
        num_retries=5,
        retry_interval=2,
    )

    do_a_thing(e)
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/core/constraints.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Core
    - Project Versions
- Defining Constraints and Indexes¶
- Defining Foreign Keys¶
  - Creating/Dropping Foreign Key Constraints via ALTER¶
  - ON UPDATE and ON DELETE¶
- UNIQUE Constraint¶
- CHECK Constraint¶

Home | Download this Documentation

Home | Download this Documentation

This section will discuss SQL constraints and indexes. In SQLAlchemy the key classes include ForeignKeyConstraint and Index.

A foreign key in SQL is a table-level construct that constrains one or more columns in that table to only allow values that are present in a different set of columns, typically but not always located on a different table. We call the columns which are constrained the foreign key columns and the columns which they are constrained towards the referenced columns. The referenced columns almost always define the primary key for their owning table, though there are exceptions to this. The foreign key is the “joint” that connects together pairs of rows which have a relationship with each other, and SQLAlchemy assigns very deep importance to this concept in virtually every area of its operation.

In SQLAlchemy as well as in DDL, foreign key constraints can be defined as additional attributes within the table clause, or for single-column foreign keys they may optionally be specified within the definition of a single column. The single column foreign key is more common, and at the column level is specified by constructing a ForeignKey object as an argument to a Column object:

Above, we define a new table user_preference for which each row must contain a value in the user_id column that also exists in the user table’s user_id column.

The argument to ForeignKey is most commonly a string of the form <tablename>.<columnname>, or for a table in a remote schema or “owner” of the form <schemaname>.<tablename>.<columnname>. It may also be an actual Column object, which as we’ll see later is accessed from an existing Table object via its c collection:

The advantage to using a string is that the in-python linkage between user and user_preference is resolved only when first needed, so that table objects can be easily spread across multiple modules and defined in any order.

Foreign keys may also be defined at the table level, using the ForeignKeyConstraint object. This object can describe a single- or multi-column foreign key. A multi-column foreign key is known as a composite foreign key, and almost always references a table that has a composite primary key. Below we define a table invoice which has a composite primary key:

And then a table invoice_item with a composite foreign key referencing invoice:

It’s important to note that the ForeignKeyConstraint is the only way to define a composite foreign key. While we could also have placed individual ForeignKey objects on both the invoice_item.invoice_id and invoice_item.ref_num columns, SQLAlchemy would not be aware that these two values should be paired together - it would be two individual foreign key constraints instead of a single composite foreign key referencing two columns.

The behavior we’ve seen in tutorials and elsewhere involving foreign keys with DDL illustrates that the constraints are typically rendered “inline” within the CREATE TABLE statement, such as:

The CONSTRAINT .. FOREIGN KEY directive is used to create the constraint in an “inline” fashion within the CREATE TABLE definition. The MetaData.create_all() and MetaData.drop_all() methods do this by default, using a topological sort of all the Table objects involved such that tables are created and dropped in order of their foreign key dependency (this sort is also available via the MetaData.sorted_tables accessor).

This approach can’t work when two or more foreign key constraints are involved in a “dependency cycle”, where a set of tables are mutually dependent on each other, assuming the backend enforces foreign keys (always the case except on SQLite, MySQL/MyISAM). The methods will therefore break out constraints in such a cycle into separate ALTER statements, on all backends other than SQLite which does not support most forms of ALTER. Given a schema like:

When we call upon MetaData.create_all() on a backend such as the PostgreSQL backend, the cycle between these two tables is resolved and the constraints are created separately:

In order to emit DROP for these tables, the same logic applies, however note here that in SQL, to emit DROP CONSTRAINT requires that the constraint has a name. In the case of the 'node' table above, we haven’t named this constraint; the system will therefore attempt to emit DROP for only those constraints that are named:

In the case where the cycle cannot be resolved, such as if we hadn’t applied a name to either constraint here, we will receive the following error:

This error only applies to the DROP case as we can emit “ADD CONSTRAINT” in the CREATE case without a name; the database typically assigns one automatically.

The ForeignKeyConstraint.use_alter and ForeignKey.use_alter keyword arguments can be used to manually resolve dependency cycles. We can add this flag only to the 'element' table as follows:

in our CREATE DDL we will see the ALTER statement only for this constraint, and not the other one:

ForeignKeyConstraint.use_alter and ForeignKey.use_alter, when used in conjunction with a drop operation, will require that the constraint is named, else an error like the following is generated:

Configuring Constraint Naming Conventions

sort_tables_and_constraints()

Most databases support cascading of foreign key values, that is the when a parent row is updated the new value is placed in child rows, or when the parent row is deleted all corresponding child rows are set to null or deleted. In data definition language these are specified using phrases like “ON UPDATE CASCADE”, “ON DELETE CASCADE”, and “ON DELETE SET NULL”, corresponding to foreign key constraints. The phrase after “ON UPDATE” or “ON DELETE” may also allow other phrases that are specific to the database in use. The ForeignKey and ForeignKeyConstraint objects support the generation of this clause via the onupdate and ondelete keyword arguments. The value is any string which will be output after the appropriate “ON UPDATE” or “ON DELETE” phrase:

Note that some backends have special requirements for cascades to function:

MySQL / MariaDB - the InnoDB storage engine should be used (this is typically the default in modern databases)

SQLite - constraints are not enabled by default. See Foreign Key Support

For background on integration of ON DELETE CASCADE with ORM relationship() constructs, see the following sections:

Using foreign key ON DELETE cascade with ORM relationships

Using foreign key ON DELETE with many-to-many relationships

PostgreSQL Constraint Options - indicates additional options available for foreign key cascades such as column lists

Foreign Key Support - background on enabling foreign key support with SQLite

Unique constraints can be created anonymously on a single column using the unique keyword on Column. Explicitly named unique constraints and/or those with multiple columns are created via the UniqueConstraint table-level construct.

Check constraints can be named or unnamed and can be created at the Column or Table level, using the CheckConstraint construct. The text of the check constraint is passed directly through to the database, so there is limited “database independent” behavior. Column level check constraints generally should only refer to the column to which they are placed, while table level constraints can refer to any columns in the table.

Note that some databases do not actively support check constraints such as older versions of MySQL (prior to 8.0.16).

The primary key constraint of any Table object is implicitly present, based on the Column objects that are marked with the Column.primary_key flag. The PrimaryKeyConstraint object provides explicit access to this constraint, which includes the option of being configured directly:

PrimaryKeyConstraint - detailed API documentation.

The Table is the SQLAlchemy Core construct that allows one to define table metadata, which among other things can be used by the SQLAlchemy ORM as a target to map a class. The Declarative extension allows the Table object to be created automatically, given the contents of the table primarily as a mapping of Column objects.

To apply table-level constraint objects such as ForeignKeyConstraint to a table defined using Declarative, use the __table_args__ attribute, described at Table Configuration.

Relational databases typically assign explicit names to all constraints and indexes. In the common case that a table is created using CREATE TABLE where constraints such as CHECK, UNIQUE, and PRIMARY KEY constraints are produced inline with the table definition, the database usually has a system in place in which names are automatically assigned to these constraints, if a name is not otherwise specified. When an existing database table is altered in a database using a command such as ALTER TABLE, this command typically needs to specify explicit names for new constraints as well as be able to specify the name of an existing constraint that is to be dropped or modified.

Constraints can be named explicitly using the Constraint.name parameter, and for indexes the Index.name parameter. However, in the case of constraints this parameter is optional. There are also the use cases of using the Column.unique and Column.index parameters which create UniqueConstraint and Index objects without an explicit name being specified.

The use case of alteration of existing tables and constraints can be handled by schema migration tools such as Alembic. However, neither Alembic nor SQLAlchemy currently create names for constraint objects where the name is otherwise unspecified, leading to the case where being able to alter existing constraints means that one must reverse-engineer the naming system used by the relational database to auto-assign names, or that care must be taken to ensure that all constraints are named.

In contrast to having to assign explicit names to all Constraint and Index objects, automated naming schemes can be constructed using events. This approach has the advantage that constraints will get a consistent naming scheme without the need for explicit name parameters throughout the code, and also that the convention takes place just as well for those constraints and indexes produced by the Column.unique and Column.index parameters. As of SQLAlchemy 0.9.2 this event-based approach is included, and can be configured using the argument MetaData.naming_convention.

MetaData.naming_convention refers to a dictionary which accepts the Index class or individual Constraint classes as keys, and Python string templates as values. It also accepts a series of string-codes as alternative keys, "fk", "pk", "ix", "ck", "uq" for foreign key, primary key, index, check, and unique constraint, respectively. The string templates in this dictionary are used whenever a constraint or index is associated with this MetaData object that does not have an existing name given (including one exception case where an existing name can be further embellished).

An example naming convention that suits basic cases is as follows:

The above convention will establish names for all constraints within the target MetaData collection. For example, we can observe the name produced when we create an unnamed UniqueConstraint:

This same feature takes effect even if we just use the Column.unique flag:

A key advantage to the naming convention approach is that the names are established at Python construction time, rather than at DDL emit time. The effect this has when using Alembic’s --autogenerate feature is that the naming convention will be explicit when a new migration script is generated:

The above "uq_user_name" string was copied from the UniqueConstraint object that --autogenerate located in our metadata.

The tokens available include %(table_name)s, %(referred_table_name)s, %(column_0_name)s, %(column_0_label)s, %(column_0_key)s, %(referred_column_0_name)s, and %(constraint_name)s, as well as multiple-column versions of each including %(column_0N_name)s, %(column_0_N_name)s, %(referred_column_0_N_name)s which render all column names separated with or without an underscore. The documentation for MetaData.naming_convention has further detail on each of these conventions.

The default value for MetaData.naming_convention handles the long-standing SQLAlchemy behavior of assigning a name to a Index object that is created using the Column.index parameter:

When a generated name, particularly those that use the multiple-column tokens, is too long for the identifier length limit of the target database (for example, PostgreSQL has a limit of 63 characters), the name will be deterministically truncated using a 4-character suffix based on the md5 hash of the long name. For example, the naming convention below will generate very long names given the column names in use:

On the PostgreSQL dialect, names longer than 63 characters will be truncated as in the following example:

The above suffix a79e is based on the md5 hash of the long name and will generate the same value every time to produce consistent names for a given schema.

New tokens can also be added, by specifying an additional token and a callable within the naming_convention dictionary. For example, if we wanted to name our foreign key constraints using a GUID scheme, we could do that as follows:

Above, when we create a new ForeignKeyConstraint, we will get a name as follows:

MetaData.naming_convention - for additional usage details as well as a listing of all available naming components.

The Importance of Naming Constraints - in the Alembic documentation.

Added in version 1.3.0: added multi-column naming tokens such as %(column_0_N_name)s. Generated names that go beyond the character limit for the target database will be deterministically truncated.

The CheckConstraint object is configured against an arbitrary SQL expression, which can have any number of columns present, and additionally is often configured using a raw SQL string. Therefore a common convention to use with CheckConstraint is one where we expect the object to have a name already, and we then enhance it with other convention elements. A typical convention is "ck_%(table_name)s_%(constraint_name)s":

The above table will produce the name ck_foo_value_gt_5:

CheckConstraint also supports the %(columns_0_name)s token; we can make use of this by ensuring we use a Column or column() element within the constraint’s expression, either by declaring the constraint separate from the table:

or by using a column() inline:

Both will produce the name ck_foo_value:

The determination of the name of “column zero” is performed by scanning the given expression for column objects. If the expression has more than one column present, the scan does use a deterministic search, however the structure of the expression will determine which column is noted as “column zero”.

The SchemaType class refers to type objects such as Boolean and Enum which generate a CHECK constraint accompanying the type. The name for the constraint here is most directly set up by sending the “name” parameter, e.g. Boolean.name:

The naming convention feature may be combined with these types as well, normally by using a convention which includes %(constraint_name)s and then applying a name to the type:

The above table will produce the constraint name ck_foo_flag_bool:

The SchemaType classes use special internal symbols so that the naming convention is only determined at DDL compile time. On PostgreSQL, there’s a native BOOLEAN type, so the CHECK constraint of Boolean is not needed; we are safe to set up a Boolean type without a name, even though a naming convention is in place for check constraints. This convention will only be consulted for the CHECK constraint if we run against a database without a native BOOLEAN type like SQLite or MySQL.

The CHECK constraint may also make use of the column_0_name token, which works nicely with SchemaType since these constraints have only one column:

The above schema will produce:

When using the naming convention feature with ORM Declarative Mixins, individual constraint objects must exist for each actual table-mapped subclass. See the section Creating Indexes and Constraints with Naming Conventions on Mixins for background and examples.

A table- or column-level CHECK constraint.

ColumnCollectionConstraint

A constraint that proxies a ColumnCollection.

ColumnCollectionMixin

A ColumnCollection of Column objects.

A table-level SQL constraint.

Mark a string indicating that a name has already been converted by a naming convention.

Defines a dependency between two columns.

A table-level FOREIGN KEY constraint.

define a class that includes the HasConditionalDDL.ddl_if() method, allowing for conditional rendering of DDL.

A table-level PRIMARY KEY constraint.

A table-level UNIQUE constraint.

inherits from sqlalchemy.sql.expression.DialectKWArgs, sqlalchemy.schema.HasConditionalDDL, sqlalchemy.schema.SchemaItem

A table-level SQL constraint.

Constraint serves as the base class for the series of constraint objects that can be associated with Table objects, including PrimaryKeyConstraint, ForeignKeyConstraint UniqueConstraint, and CheckConstraint.

Create a SQL constraint.

Add a new kind of dialect-specific keyword argument for this class.

apply a conditional DDL rule to this schema item.

A collection of keyword arguments specified as dialect-specific options to this construct.

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

Create a SQL constraint.

name¶ – Optional, the in-database name of this Constraint.

deferrable¶ – Optional bool. If set, emit DEFERRABLE or NOT DEFERRABLE when issuing DDL for this constraint.

initially¶ – Optional string. If set, emit INITIALLY <value> when issuing DDL for this constraint.

info¶ – Optional data dictionary which will be populated into the SchemaItem.info attribute of this object.

Optional string that will render an SQL comment on foreign key constraint creation.

Added in version 2.0.

**dialect_kw¶ – Additional keyword arguments are dialect specific, and passed in the form <dialectname>_<argname>. See the documentation regarding an individual dialect at Dialects for detail on documented arguments.

_create_rule¶ – used internally by some datatypes that also create constraints.

_type_bound¶ – used internally to indicate that this constraint is associated with a specific datatype.

inherited from the DialectKWArgs.argument_for() method of DialectKWArgs

Add a new kind of dialect-specific keyword argument for this class.

The DialectKWArgs.argument_for() method is a per-argument way adding extra arguments to the DefaultDialect.construct_arguments dictionary. This dictionary provides a list of argument names accepted by various schema-level constructs on behalf of a dialect.

New dialects should typically specify this dictionary all at once as a data member of the dialect class. The use case for ad-hoc addition of argument names is typically for end-user code that is also using a custom compilation scheme which consumes the additional arguments.

dialect_name¶ – name of a dialect. The dialect must be locatable, else a NoSuchModuleError is raised. The dialect must also include an existing DefaultDialect.construct_arguments collection, indicating that it participates in the keyword-argument validation and default system, else ArgumentError is raised. If the dialect does not include this collection, then any keyword argument can be specified on behalf of this dialect already. All dialects packaged within SQLAlchemy include this collection, however for third party dialects, support may vary.

argument_name¶ – name of the parameter.

default¶ – default value of the parameter.

Deprecated since version 1.4: The Constraint.copy() method is deprecated and will be removed in a future release.

inherited from the HasConditionalDDL.ddl_if() method of HasConditionalDDL

apply a conditional DDL rule to this schema item.

These rules work in a similar manner to the ExecutableDDLElement.execute_if() callable, with the added feature that the criteria may be checked within the DDL compilation phase for a construct such as CreateTable. HasConditionalDDL.ddl_if() currently applies towards the Index construct as well as all Constraint constructs.

dialect¶ – string name of a dialect, or a tuple of string names to indicate multiple dialect types.

callable_¶ – a callable that is constructed using the same form as that described in ExecutableDDLElement.execute_if.callable_.

state¶ – any arbitrary object that will be passed to the callable, if present.

Added in version 2.0.

Controlling DDL Generation of Constraints and Indexes - background and usage examples

A collection of keyword arguments specified as dialect-specific options to this construct.

The arguments are present here in their original <dialect>_<kwarg> format. Only arguments that were actually passed are included; unlike the DialectKWArgs.dialect_options collection, which contains all options known by this dialect including defaults.

The collection is also writable; keys are accepted of the form <dialect>_<kwarg> where the value will be assembled into the list of options.

DialectKWArgs.dialect_options - nested dictionary form

inherited from the DialectKWArgs.dialect_options attribute of DialectKWArgs

A collection of keyword arguments specified as dialect-specific options to this construct.

This is a two-level nested registry, keyed to <dialect_name> and <argument_name>. For example, the postgresql_where argument would be locatable as:

Added in version 0.9.2.

DialectKWArgs.dialect_kwargs - flat dictionary form

inherited from the SchemaItem.info attribute of SchemaItem

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

The dictionary is automatically generated when first accessed. It can also be specified in the constructor of some objects, such as Table and Column.

A synonym for DialectKWArgs.dialect_kwargs.

A ColumnCollection of Column objects.

This collection represents the columns which are referred to by this object.

inherits from sqlalchemy.schema.ColumnCollectionMixin, sqlalchemy.schema.Constraint

A constraint that proxies a ColumnCollection.

Add a new kind of dialect-specific keyword argument for this class.

A ColumnCollection representing the set of columns for this constraint.

Return True if this constraint contains the given column.

apply a conditional DDL rule to this schema item.

A collection of keyword arguments specified as dialect-specific options to this construct.

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

*columns¶ – A sequence of column names or Column objects.

name¶ – Optional, the in-database name of this constraint.

deferrable¶ – Optional bool. If set, emit DEFERRABLE or NOT DEFERRABLE when issuing DDL for this constraint.

initially¶ – Optional string. If set, emit INITIALLY <value> when issuing DDL for this constraint.

**dialect_kw¶ – other keyword arguments including dialect-specific arguments are propagated to the Constraint superclass.

inherited from the DialectKWArgs.argument_for() method of DialectKWArgs

Add a new kind of dialect-specific keyword argument for this class.

The DialectKWArgs.argument_for() method is a per-argument way adding extra arguments to the DefaultDialect.construct_arguments dictionary. This dictionary provides a list of argument names accepted by various schema-level constructs on behalf of a dialect.

New dialects should typically specify this dictionary all at once as a data member of the dialect class. The use case for ad-hoc addition of argument names is typically for end-user code that is also using a custom compilation scheme which consumes the additional arguments.

dialect_name¶ – name of a dialect. The dialect must be locatable, else a NoSuchModuleError is raised. The dialect must also include an existing DefaultDialect.construct_arguments collection, indicating that it participates in the keyword-argument validation and default system, else ArgumentError is raised. If the dialect does not include this collection, then any keyword argument can be specified on behalf of this dialect already. All dialects packaged within SQLAlchemy include this collection, however for third party dialects, support may vary.

argument_name¶ – name of the parameter.

default¶ – default value of the parameter.

inherited from the ColumnCollectionMixin.columns attribute of ColumnCollectionMixin

A ColumnCollection representing the set of columns for this constraint.

Return True if this constraint contains the given column.

Note that this object also contains an attribute .columns which is a ColumnCollection of Column objects.

Deprecated since version 1.4: The ColumnCollectionConstraint.copy() method is deprecated and will be removed in a future release.

inherited from the HasConditionalDDL.ddl_if() method of HasConditionalDDL

apply a conditional DDL rule to this schema item.

These rules work in a similar manner to the ExecutableDDLElement.execute_if() callable, with the added feature that the criteria may be checked within the DDL compilation phase for a construct such as CreateTable. HasConditionalDDL.ddl_if() currently applies towards the Index construct as well as all Constraint constructs.

dialect¶ – string name of a dialect, or a tuple of string names to indicate multiple dialect types.

callable_¶ – a callable that is constructed using the same form as that described in ExecutableDDLElement.execute_if.callable_.

state¶ – any arbitrary object that will be passed to the callable, if present.

Added in version 2.0.

Controlling DDL Generation of Constraints and Indexes - background and usage examples

A collection of keyword arguments specified as dialect-specific options to this construct.

The arguments are present here in their original <dialect>_<kwarg> format. Only arguments that were actually passed are included; unlike the DialectKWArgs.dialect_options collection, which contains all options known by this dialect including defaults.

The collection is also writable; keys are accepted of the form <dialect>_<kwarg> where the value will be assembled into the list of options.

DialectKWArgs.dialect_options - nested dictionary form

inherited from the DialectKWArgs.dialect_options attribute of DialectKWArgs

A collection of keyword arguments specified as dialect-specific options to this construct.

This is a two-level nested registry, keyed to <dialect_name> and <argument_name>. For example, the postgresql_where argument would be locatable as:

Added in version 0.9.2.

DialectKWArgs.dialect_kwargs - flat dictionary form

inherited from the SchemaItem.info attribute of SchemaItem

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

The dictionary is automatically generated when first accessed. It can also be specified in the constructor of some objects, such as Table and Column.

A synonym for DialectKWArgs.dialect_kwargs.

inherits from sqlalchemy.schema.ColumnCollectionConstraint

A table- or column-level CHECK constraint.

Can be included in the definition of a Table or Column.

Construct a CHECK constraint.

Add a new kind of dialect-specific keyword argument for this class.

A ColumnCollection representing the set of columns for this constraint.

Return True if this constraint contains the given column.

apply a conditional DDL rule to this schema item.

A collection of keyword arguments specified as dialect-specific options to this construct.

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

Construct a CHECK constraint.

A string containing the constraint definition, which will be used verbatim, or a SQL expression construct. If given as a string, the object is converted to a text() object. If the textual string includes a colon character, escape this using a backslash:

name¶ – Optional, the in-database name of the constraint.

deferrable¶ – Optional bool. If set, emit DEFERRABLE or NOT DEFERRABLE when issuing DDL for this constraint.

initially¶ – Optional string. If set, emit INITIALLY <value> when issuing DDL for this constraint.

info¶ – Optional data dictionary which will be populated into the SchemaItem.info attribute of this object.

inherited from the DialectKWArgs.argument_for() method of DialectKWArgs

Add a new kind of dialect-specific keyword argument for this class.

The DialectKWArgs.argument_for() method is a per-argument way adding extra arguments to the DefaultDialect.construct_arguments dictionary. This dictionary provides a list of argument names accepted by various schema-level constructs on behalf of a dialect.

New dialects should typically specify this dictionary all at once as a data member of the dialect class. The use case for ad-hoc addition of argument names is typically for end-user code that is also using a custom compilation scheme which consumes the additional arguments.

dialect_name¶ – name of a dialect. The dialect must be locatable, else a NoSuchModuleError is raised. The dialect must also include an existing DefaultDialect.construct_arguments collection, indicating that it participates in the keyword-argument validation and default system, else ArgumentError is raised. If the dialect does not include this collection, then any keyword argument can be specified on behalf of this dialect already. All dialects packaged within SQLAlchemy include this collection, however for third party dialects, support may vary.

argument_name¶ – name of the parameter.

default¶ – default value of the parameter.

inherited from the ColumnCollectionMixin.columns attribute of ColumnCollectionMixin

A ColumnCollection representing the set of columns for this constraint.

inherited from the ColumnCollectionConstraint.contains_column() method of ColumnCollectionConstraint

Return True if this constraint contains the given column.

Note that this object also contains an attribute .columns which is a ColumnCollection of Column objects.

Deprecated since version 1.4: The CheckConstraint.copy() method is deprecated and will be removed in a future release.

inherited from the HasConditionalDDL.ddl_if() method of HasConditionalDDL

apply a conditional DDL rule to this schema item.

These rules work in a similar manner to the ExecutableDDLElement.execute_if() callable, with the added feature that the criteria may be checked within the DDL compilation phase for a construct such as CreateTable. HasConditionalDDL.ddl_if() currently applies towards the Index construct as well as all Constraint constructs.

dialect¶ – string name of a dialect, or a tuple of string names to indicate multiple dialect types.

callable_¶ – a callable that is constructed using the same form as that described in ExecutableDDLElement.execute_if.callable_.

state¶ – any arbitrary object that will be passed to the callable, if present.

Added in version 2.0.

Controlling DDL Generation of Constraints and Indexes - background and usage examples

A collection of keyword arguments specified as dialect-specific options to this construct.

The arguments are present here in their original <dialect>_<kwarg> format. Only arguments that were actually passed are included; unlike the DialectKWArgs.dialect_options collection, which contains all options known by this dialect including defaults.

The collection is also writable; keys are accepted of the form <dialect>_<kwarg> where the value will be assembled into the list of options.

DialectKWArgs.dialect_options - nested dictionary form

inherited from the DialectKWArgs.dialect_options attribute of DialectKWArgs

A collection of keyword arguments specified as dialect-specific options to this construct.

This is a two-level nested registry, keyed to <dialect_name> and <argument_name>. For example, the postgresql_where argument would be locatable as:

Added in version 0.9.2.

DialectKWArgs.dialect_kwargs - flat dictionary form

inherited from the SchemaItem.info attribute of SchemaItem

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

The dictionary is automatically generated when first accessed. It can also be specified in the constructor of some objects, such as Table and Column.

A synonym for DialectKWArgs.dialect_kwargs.

inherits from sqlalchemy.sql.expression.DialectKWArgs, sqlalchemy.schema.SchemaItem

Defines a dependency between two columns.

ForeignKey is specified as an argument to a Column object, e.g.:

Note that ForeignKey is only a marker object that defines a dependency between two columns. The actual constraint is in all cases represented by the ForeignKeyConstraint object. This object will be generated automatically when a ForeignKey is associated with a Column which in turn is associated with a Table. Conversely, when ForeignKeyConstraint is applied to a Table, ForeignKey markers are automatically generated to be present on each associated Column, which are also associated with the constraint object.

Note that you cannot define a “composite” foreign key constraint, that is a constraint between a grouping of multiple parent/child columns, using ForeignKey objects. To define this grouping, the ForeignKeyConstraint object must be used, and applied to the Table. The associated ForeignKey objects are created automatically.

The ForeignKey objects associated with an individual Column object are available in the foreign_keys collection of that column.

Further examples of foreign key configuration are in Defining Foreign Keys.

Construct a column-level FOREIGN KEY.

Add a new kind of dialect-specific keyword argument for this class.

Return the target Column referenced by this ForeignKey.

A collection of keyword arguments specified as dialect-specific options to this construct.

Return the Column in the given Table (or any FromClause) referenced by this ForeignKey.

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

Return True if the given Table is referenced by this ForeignKey.

Construct a column-level FOREIGN KEY.

The ForeignKey object when constructed generates a ForeignKeyConstraint which is associated with the parent Table object’s collection of constraints.

column¶ – A single target column for the key relationship. A Column object or a column name as a string: tablename.columnkey or schema.tablename.columnkey. columnkey is the key which has been assigned to the column (defaults to the column name itself), unless link_to_name is True in which case the rendered name of the column is used.

name¶ – Optional string. An in-database name for the key if constraint is not provided.

Optional string. If set, emit ON UPDATE <value> when issuing DDL for this constraint. Typical values include CASCADE, DELETE and RESTRICT.

ON UPDATE and ON DELETE

Optional string. If set, emit ON DELETE <value> when issuing DDL for this constraint. Typical values include CASCADE, SET NULL and RESTRICT. Some dialects may allow for additional syntaxes.

ON UPDATE and ON DELETE

deferrable¶ – Optional bool. If set, emit DEFERRABLE or NOT DEFERRABLE when issuing DDL for this constraint.

initially¶ – Optional string. If set, emit INITIALLY <value> when issuing DDL for this constraint.

link_to_name¶ – if True, the string name given in column is the rendered name of the referenced column, not its locally assigned key.

passed to the underlying ForeignKeyConstraint to indicate the constraint should be generated/dropped externally from the CREATE TABLE/ DROP TABLE statement. See ForeignKeyConstraint.use_alter for further description.

ForeignKeyConstraint.use_alter

Creating/Dropping Foreign Key Constraints via ALTER

match¶ – Optional string. If set, emit MATCH <value> when issuing DDL for this constraint. Typical values include SIMPLE, PARTIAL and FULL.

info¶ – Optional data dictionary which will be populated into the SchemaItem.info attribute of this object.

Optional string that will render an SQL comment on foreign key constraint creation.

Added in version 2.0.

**dialect_kw¶ – Additional keyword arguments are dialect specific, and passed in the form <dialectname>_<argname>. The arguments are ultimately handled by a corresponding ForeignKeyConstraint. See the documentation regarding an individual dialect at Dialects for detail on documented arguments.

inherited from the DialectKWArgs.argument_for() method of DialectKWArgs

Add a new kind of dialect-specific keyword argument for this class.

The DialectKWArgs.argument_for() method is a per-argument way adding extra arguments to the DefaultDialect.construct_arguments dictionary. This dictionary provides a list of argument names accepted by various schema-level constructs on behalf of a dialect.

New dialects should typically specify this dictionary all at once as a data member of the dialect class. The use case for ad-hoc addition of argument names is typically for end-user code that is also using a custom compilation scheme which consumes the additional arguments.

dialect_name¶ – name of a dialect. The dialect must be locatable, else a NoSuchModuleError is raised. The dialect must also include an existing DefaultDialect.construct_arguments collection, indicating that it participates in the keyword-argument validation and default system, else ArgumentError is raised. If the dialect does not include this collection, then any keyword argument can be specified on behalf of this dialect already. All dialects packaged within SQLAlchemy include this collection, however for third party dialects, support may vary.

argument_name¶ – name of the parameter.

default¶ – default value of the parameter.

Return the target Column referenced by this ForeignKey.

If no target column has been established, an exception is raised.

Deprecated since version 1.4: The ForeignKey.copy() method is deprecated and will be removed in a future release.

A collection of keyword arguments specified as dialect-specific options to this construct.

The arguments are present here in their original <dialect>_<kwarg> format. Only arguments that were actually passed are included; unlike the DialectKWArgs.dialect_options collection, which contains all options known by this dialect including defaults.

The collection is also writable; keys are accepted of the form <dialect>_<kwarg> where the value will be assembled into the list of options.

DialectKWArgs.dialect_options - nested dictionary form

inherited from the DialectKWArgs.dialect_options attribute of DialectKWArgs

A collection of keyword arguments specified as dialect-specific options to this construct.

This is a two-level nested registry, keyed to <dialect_name> and <argument_name>. For example, the postgresql_where argument would be locatable as:

Added in version 0.9.2.

DialectKWArgs.dialect_kwargs - flat dictionary form

Return the Column in the given Table (or any FromClause) referenced by this ForeignKey.

Returns None if this ForeignKey does not reference the given Table.

inherited from the SchemaItem.info attribute of SchemaItem

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

The dictionary is automatically generated when first accessed. It can also be specified in the constructor of some objects, such as Table and Column.

A synonym for DialectKWArgs.dialect_kwargs.

Return True if the given Table is referenced by this ForeignKey.

Return a string based ‘column specification’ for this ForeignKey.

This is usually the equivalent of the string-based “tablename.colname” argument first passed to the object’s constructor.

inherits from sqlalchemy.schema.ColumnCollectionConstraint

A table-level FOREIGN KEY constraint.

Defines a single column or composite FOREIGN KEY … REFERENCES constraint. For a no-frills, single column foreign key, adding a ForeignKey to the definition of a Column is a shorthand equivalent for an unnamed, single column ForeignKeyConstraint.

Examples of foreign key configuration are in Defining Foreign Keys.

Construct a composite-capable FOREIGN KEY.

Add a new kind of dialect-specific keyword argument for this class.

A ColumnCollection representing the set of columns for this constraint.

Return True if this constraint contains the given column.

apply a conditional DDL rule to this schema item.

A collection of keyword arguments specified as dialect-specific options to this construct.

A sequence of ForeignKey objects.

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

Construct a composite-capable FOREIGN KEY.

columns¶ – A sequence of local column names. The named columns must be defined and present in the parent Table. The names should match the key given to each column (defaults to the name) unless link_to_name is True.

refcolumns¶ – A sequence of foreign column names or Column objects. The columns must all be located within the same Table.

name¶ – Optional, the in-database name of the key.

Optional string. If set, emit ON UPDATE <value> when issuing DDL for this constraint. Typical values include CASCADE, DELETE and RESTRICT.

ON UPDATE and ON DELETE

Optional string. If set, emit ON DELETE <value> when issuing DDL for this constraint. Typical values include CASCADE, SET NULL and RESTRICT. Some dialects may allow for additional syntaxes.

ON UPDATE and ON DELETE

deferrable¶ – Optional bool. If set, emit DEFERRABLE or NOT DEFERRABLE when issuing DDL for this constraint.

initially¶ – Optional string. If set, emit INITIALLY <value> when issuing DDL for this constraint.

link_to_name¶ – if True, the string name given in column is the rendered name of the referenced column, not its locally assigned key.

If True, do not emit the DDL for this constraint as part of the CREATE TABLE definition. Instead, generate it via an ALTER TABLE statement issued after the full collection of tables have been created, and drop it via an ALTER TABLE statement before the full collection of tables are dropped.

The use of ForeignKeyConstraint.use_alter is particularly geared towards the case where two or more tables are established within a mutually-dependent foreign key constraint relationship; however, the MetaData.create_all() and MetaData.drop_all() methods will perform this resolution automatically, so the flag is normally not needed.

Creating/Dropping Foreign Key Constraints via ALTER

match¶ – Optional string. If set, emit MATCH <value> when issuing DDL for this constraint. Typical values include SIMPLE, PARTIAL and FULL.

info¶ – Optional data dictionary which will be populated into the SchemaItem.info attribute of this object.

Optional string that will render an SQL comment on foreign key constraint creation.

Added in version 2.0.

**dialect_kw¶ – Additional keyword arguments are dialect specific, and passed in the form <dialectname>_<argname>. See the documentation regarding an individual dialect at Dialects for detail on documented arguments.

inherited from the DialectKWArgs.argument_for() method of DialectKWArgs

Add a new kind of dialect-specific keyword argument for this class.

The DialectKWArgs.argument_for() method is a per-argument way adding extra arguments to the DefaultDialect.construct_arguments dictionary. This dictionary provides a list of argument names accepted by various schema-level constructs on behalf of a dialect.

New dialects should typically specify this dictionary all at once as a data member of the dialect class. The use case for ad-hoc addition of argument names is typically for end-user code that is also using a custom compilation scheme which consumes the additional arguments.

dialect_name¶ – name of a dialect. The dialect must be locatable, else a NoSuchModuleError is raised. The dialect must also include an existing DefaultDialect.construct_arguments collection, indicating that it participates in the keyword-argument validation and default system, else ArgumentError is raised. If the dialect does not include this collection, then any keyword argument can be specified on behalf of this dialect already. All dialects packaged within SQLAlchemy include this collection, however for third party dialects, support may vary.

argument_name¶ – name of the parameter.

default¶ – default value of the parameter.

Return a list of string keys representing the local columns in this ForeignKeyConstraint.

This list is either the original string arguments sent to the constructor of the ForeignKeyConstraint, or if the constraint has been initialized with Column objects, is the string .key of each element.

inherited from the ColumnCollectionMixin.columns attribute of ColumnCollectionMixin

A ColumnCollection representing the set of columns for this constraint.

inherited from the ColumnCollectionConstraint.contains_column() method of ColumnCollectionConstraint

Return True if this constraint contains the given column.

Note that this object also contains an attribute .columns which is a ColumnCollection of Column objects.

Deprecated since version 1.4: The ForeignKeyConstraint.copy() method is deprecated and will be removed in a future release.

inherited from the HasConditionalDDL.ddl_if() method of HasConditionalDDL

apply a conditional DDL rule to this schema item.

These rules work in a similar manner to the ExecutableDDLElement.execute_if() callable, with the added feature that the criteria may be checked within the DDL compilation phase for a construct such as CreateTable. HasConditionalDDL.ddl_if() currently applies towards the Index construct as well as all Constraint constructs.

dialect¶ – string name of a dialect, or a tuple of string names to indicate multiple dialect types.

callable_¶ – a callable that is constructed using the same form as that described in ExecutableDDLElement.execute_if.callable_.

state¶ – any arbitrary object that will be passed to the callable, if present.

Added in version 2.0.

Controlling DDL Generation of Constraints and Indexes - background and usage examples

A collection of keyword arguments specified as dialect-specific options to this construct.

The arguments are present here in their original <dialect>_<kwarg> format. Only arguments that were actually passed are included; unlike the DialectKWArgs.dialect_options collection, which contains all options known by this dialect including defaults.

The collection is also writable; keys are accepted of the form <dialect>_<kwarg> where the value will be assembled into the list of options.

DialectKWArgs.dialect_options - nested dictionary form

inherited from the DialectKWArgs.dialect_options attribute of DialectKWArgs

A collection of keyword arguments specified as dialect-specific options to this construct.

This is a two-level nested registry, keyed to <dialect_name> and <argument_name>. For example, the postgresql_where argument would be locatable as:

Added in version 0.9.2.

DialectKWArgs.dialect_kwargs - flat dictionary form

A sequence of ForeignKey objects.

Each ForeignKey represents a single referring column/referred column pair.

This collection is intended to be read-only.

inherited from the SchemaItem.info attribute of SchemaItem

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

The dictionary is automatically generated when first accessed. It can also be specified in the constructor of some objects, such as Table and Column.

A synonym for DialectKWArgs.dialect_kwargs.

The Table object to which this ForeignKeyConstraint references.

This is a dynamically calculated attribute which may not be available if the constraint and/or parent table is not yet associated with a metadata collection that contains the referred table.

define a class that includes the HasConditionalDDL.ddl_if() method, allowing for conditional rendering of DDL.

Currently applies to constraints and indexes.

Added in version 2.0.

apply a conditional DDL rule to this schema item.

apply a conditional DDL rule to this schema item.

These rules work in a similar manner to the ExecutableDDLElement.execute_if() callable, with the added feature that the criteria may be checked within the DDL compilation phase for a construct such as CreateTable. HasConditionalDDL.ddl_if() currently applies towards the Index construct as well as all Constraint constructs.

dialect¶ – string name of a dialect, or a tuple of string names to indicate multiple dialect types.

callable_¶ – a callable that is constructed using the same form as that described in ExecutableDDLElement.execute_if.callable_.

state¶ – any arbitrary object that will be passed to the callable, if present.

Added in version 2.0.

Controlling DDL Generation of Constraints and Indexes - background and usage examples

inherits from sqlalchemy.schema.ColumnCollectionConstraint

A table-level PRIMARY KEY constraint.

The PrimaryKeyConstraint object is present automatically on any Table object; it is assigned a set of Column objects corresponding to those marked with the Column.primary_key flag:

The primary key of a Table can also be specified by using a PrimaryKeyConstraint object explicitly; in this mode of usage, the “name” of the constraint can also be specified, as well as other options which may be recognized by dialects:

The two styles of column-specification should generally not be mixed. An warning is emitted if the columns present in the PrimaryKeyConstraint don’t match the columns that were marked as primary_key=True, if both are present; in this case, the columns are taken strictly from the PrimaryKeyConstraint declaration, and those columns otherwise marked as primary_key=True are ignored. This behavior is intended to be backwards compatible with previous behavior.

For the use case where specific options are to be specified on the PrimaryKeyConstraint, but the usual style of using primary_key=True flags is still desirable, an empty PrimaryKeyConstraint may be specified, which will take on the primary key column collection from the Table based on the flags:

Add a new kind of dialect-specific keyword argument for this class.

A ColumnCollection representing the set of columns for this constraint.

Return True if this constraint contains the given column.

apply a conditional DDL rule to this schema item.

A collection of keyword arguments specified as dialect-specific options to this construct.

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

inherited from the DialectKWArgs.argument_for() method of DialectKWArgs

Add a new kind of dialect-specific keyword argument for this class.

The DialectKWArgs.argument_for() method is a per-argument way adding extra arguments to the DefaultDialect.construct_arguments dictionary. This dictionary provides a list of argument names accepted by various schema-level constructs on behalf of a dialect.

New dialects should typically specify this dictionary all at once as a data member of the dialect class. The use case for ad-hoc addition of argument names is typically for end-user code that is also using a custom compilation scheme which consumes the additional arguments.

dialect_name¶ – name of a dialect. The dialect must be locatable, else a NoSuchModuleError is raised. The dialect must also include an existing DefaultDialect.construct_arguments collection, indicating that it participates in the keyword-argument validation and default system, else ArgumentError is raised. If the dialect does not include this collection, then any keyword argument can be specified on behalf of this dialect already. All dialects packaged within SQLAlchemy include this collection, however for third party dialects, support may vary.

argument_name¶ – name of the parameter.

default¶ – default value of the parameter.

inherited from the ColumnCollectionMixin.columns attribute of ColumnCollectionMixin

A ColumnCollection representing the set of columns for this constraint.

inherited from the ColumnCollectionConstraint.contains_column() method of ColumnCollectionConstraint

Return True if this constraint contains the given column.

Note that this object also contains an attribute .columns which is a ColumnCollection of Column objects.

inherited from the ColumnCollectionConstraint.copy() method of ColumnCollectionConstraint

Deprecated since version 1.4: The ColumnCollectionConstraint.copy() method is deprecated and will be removed in a future release.

inherited from the HasConditionalDDL.ddl_if() method of HasConditionalDDL

apply a conditional DDL rule to this schema item.

These rules work in a similar manner to the ExecutableDDLElement.execute_if() callable, with the added feature that the criteria may be checked within the DDL compilation phase for a construct such as CreateTable. HasConditionalDDL.ddl_if() currently applies towards the Index construct as well as all Constraint constructs.

dialect¶ – string name of a dialect, or a tuple of string names to indicate multiple dialect types.

callable_¶ – a callable that is constructed using the same form as that described in ExecutableDDLElement.execute_if.callable_.

state¶ – any arbitrary object that will be passed to the callable, if present.

Added in version 2.0.

Controlling DDL Generation of Constraints and Indexes - background and usage examples

A collection of keyword arguments specified as dialect-specific options to this construct.

The arguments are present here in their original <dialect>_<kwarg> format. Only arguments that were actually passed are included; unlike the DialectKWArgs.dialect_options collection, which contains all options known by this dialect including defaults.

The collection is also writable; keys are accepted of the form <dialect>_<kwarg> where the value will be assembled into the list of options.

DialectKWArgs.dialect_options - nested dictionary form

inherited from the DialectKWArgs.dialect_options attribute of DialectKWArgs

A collection of keyword arguments specified as dialect-specific options to this construct.

This is a two-level nested registry, keyed to <dialect_name> and <argument_name>. For example, the postgresql_where argument would be locatable as:

Added in version 0.9.2.

DialectKWArgs.dialect_kwargs - flat dictionary form

inherited from the SchemaItem.info attribute of SchemaItem

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

The dictionary is automatically generated when first accessed. It can also be specified in the constructor of some objects, such as Table and Column.

A synonym for DialectKWArgs.dialect_kwargs.

inherits from sqlalchemy.schema.ColumnCollectionConstraint

A table-level UNIQUE constraint.

Defines a single column or composite UNIQUE constraint. For a no-frills, single column constraint, adding unique=True to the Column definition is a shorthand equivalent for an unnamed, single column UniqueConstraint.

Add a new kind of dialect-specific keyword argument for this class.

A ColumnCollection representing the set of columns for this constraint.

Return True if this constraint contains the given column.

apply a conditional DDL rule to this schema item.

A collection of keyword arguments specified as dialect-specific options to this construct.

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

inherited from the sqlalchemy.schema.ColumnCollectionConstraint.__init__ method of ColumnCollectionConstraint

*columns¶ – A sequence of column names or Column objects.

name¶ – Optional, the in-database name of this constraint.

deferrable¶ – Optional bool. If set, emit DEFERRABLE or NOT DEFERRABLE when issuing DDL for this constraint.

initially¶ – Optional string. If set, emit INITIALLY <value> when issuing DDL for this constraint.

**dialect_kw¶ – other keyword arguments including dialect-specific arguments are propagated to the Constraint superclass.

inherited from the DialectKWArgs.argument_for() method of DialectKWArgs

Add a new kind of dialect-specific keyword argument for this class.

The DialectKWArgs.argument_for() method is a per-argument way adding extra arguments to the DefaultDialect.construct_arguments dictionary. This dictionary provides a list of argument names accepted by various schema-level constructs on behalf of a dialect.

New dialects should typically specify this dictionary all at once as a data member of the dialect class. The use case for ad-hoc addition of argument names is typically for end-user code that is also using a custom compilation scheme which consumes the additional arguments.

dialect_name¶ – name of a dialect. The dialect must be locatable, else a NoSuchModuleError is raised. The dialect must also include an existing DefaultDialect.construct_arguments collection, indicating that it participates in the keyword-argument validation and default system, else ArgumentError is raised. If the dialect does not include this collection, then any keyword argument can be specified on behalf of this dialect already. All dialects packaged within SQLAlchemy include this collection, however for third party dialects, support may vary.

argument_name¶ – name of the parameter.

default¶ – default value of the parameter.

inherited from the ColumnCollectionMixin.columns attribute of ColumnCollectionMixin

A ColumnCollection representing the set of columns for this constraint.

inherited from the ColumnCollectionConstraint.contains_column() method of ColumnCollectionConstraint

Return True if this constraint contains the given column.

Note that this object also contains an attribute .columns which is a ColumnCollection of Column objects.

inherited from the ColumnCollectionConstraint.copy() method of ColumnCollectionConstraint

Deprecated since version 1.4: The ColumnCollectionConstraint.copy() method is deprecated and will be removed in a future release.

inherited from the HasConditionalDDL.ddl_if() method of HasConditionalDDL

apply a conditional DDL rule to this schema item.

These rules work in a similar manner to the ExecutableDDLElement.execute_if() callable, with the added feature that the criteria may be checked within the DDL compilation phase for a construct such as CreateTable. HasConditionalDDL.ddl_if() currently applies towards the Index construct as well as all Constraint constructs.

dialect¶ – string name of a dialect, or a tuple of string names to indicate multiple dialect types.

callable_¶ – a callable that is constructed using the same form as that described in ExecutableDDLElement.execute_if.callable_.

state¶ – any arbitrary object that will be passed to the callable, if present.

Added in version 2.0.

Controlling DDL Generation of Constraints and Indexes - background and usage examples

A collection of keyword arguments specified as dialect-specific options to this construct.

The arguments are present here in their original <dialect>_<kwarg> format. Only arguments that were actually passed are included; unlike the DialectKWArgs.dialect_options collection, which contains all options known by this dialect including defaults.

The collection is also writable; keys are accepted of the form <dialect>_<kwarg> where the value will be assembled into the list of options.

DialectKWArgs.dialect_options - nested dictionary form

inherited from the DialectKWArgs.dialect_options attribute of DialectKWArgs

A collection of keyword arguments specified as dialect-specific options to this construct.

This is a two-level nested registry, keyed to <dialect_name> and <argument_name>. For example, the postgresql_where argument would be locatable as:

Added in version 0.9.2.

DialectKWArgs.dialect_kwargs - flat dictionary form

inherited from the SchemaItem.info attribute of SchemaItem

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

The dictionary is automatically generated when first accessed. It can also be specified in the constructor of some objects, such as Table and Column.

A synonym for DialectKWArgs.dialect_kwargs.

Mark a string indicating that a name has already been converted by a naming convention.

This is a string subclass that indicates a name that should not be subject to any further naming conventions.

E.g. when we create a Constraint using a naming convention as follows:

The name of the above constraint will be rendered as "ck_t_x5". That is, the existing name x5 is used in the naming convention as the constraint_name token.

In some situations, such as in migration scripts, we may be rendering the above CheckConstraint with a name that’s already been converted. In order to make sure the name isn’t double-modified, the new name is applied using the conv() marker. We can use this explicitly as follows:

Where above, the conv() marker indicates that the constraint name here is final, and the name will render as "ck_t_x5" and not "ck_t_ck_t_x5"

Configuring Constraint Naming Conventions

Indexes can be created anonymously (using an auto-generated name ix_<column label>) for a single column using the inline index keyword on Column, which also modifies the usage of unique to apply the uniqueness to the index itself, instead of adding a separate UNIQUE constraint. For indexes with specific names or which encompass more than one column, use the Index construct, which requires a name.

Below we illustrate a Table with several Index objects associated. The DDL for “CREATE INDEX” is issued right after the create statements for the table:

Note in the example above, the Index construct is created externally to the table which it corresponds, using Column objects directly. Index also supports “inline” definition inside the Table, using string names to identify columns:

The Index object also supports its own create() method:

Index supports SQL and function expressions, as supported by the target backend. To create an index against a column using a descending value, the ColumnElement.desc() modifier may be used:

Or with a backend that supports functional indexes such as PostgreSQL, a “case insensitive” index can be created using the lower() function:

inherits from sqlalchemy.sql.expression.DialectKWArgs, sqlalchemy.schema.ColumnCollectionMixin, sqlalchemy.schema.HasConditionalDDL, sqlalchemy.schema.SchemaItem

Defines a composite (one or more column) INDEX.

For a no-frills, single column index, adding Column also supports index=True:

For a composite index, multiple columns can be specified:

Functional indexes are supported as well, typically by using the func construct in conjunction with table-bound Column objects:

An Index can also be manually associated with a Table, either through inline declaration or using Table.append_constraint(). When this approach is used, the names of the indexed columns can be specified as strings:

To support functional or expression-based indexes in this form, the text() construct may be used:

Indexes - General information on Index.

PostgreSQL-Specific Index Options - PostgreSQL-specific options available for the Index construct.

MySQL / MariaDB- Specific Index Options - MySQL-specific options available for the Index construct.

Clustered Index Support - MSSQL-specific options available for the Index construct.

Construct an index object.

Add a new kind of dialect-specific keyword argument for this class.

Issue a CREATE statement for this Index, using the given Connection or Engine` for connectivity.

apply a conditional DDL rule to this schema item.

A collection of keyword arguments specified as dialect-specific options to this construct.

Issue a DROP statement for this Index, using the given Connection or Engine for connectivity.

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

Construct an index object.

name¶ – The name of the index

*expressions¶ – Column expressions to include in the index. The expressions are normally instances of Column, but may also be arbitrary SQL expressions which ultimately refer to a Column.

unique=False¶ – Keyword only argument; if True, create a unique index.

quote=None¶ – Keyword only argument; whether to apply quoting to the name of the index. Works in the same manner as that of Column.quote.

info=None¶ – Optional data dictionary which will be populated into the SchemaItem.info attribute of this object.

**dialect_kw¶ – Additional keyword arguments not mentioned above are dialect specific, and passed in the form <dialectname>_<argname>. See the documentation regarding an individual dialect at Dialects for detail on documented arguments.

inherited from the DialectKWArgs.argument_for() method of DialectKWArgs

Add a new kind of dialect-specific keyword argument for this class.

The DialectKWArgs.argument_for() method is a per-argument way adding extra arguments to the DefaultDialect.construct_arguments dictionary. This dictionary provides a list of argument names accepted by various schema-level constructs on behalf of a dialect.

New dialects should typically specify this dictionary all at once as a data member of the dialect class. The use case for ad-hoc addition of argument names is typically for end-user code that is also using a custom compilation scheme which consumes the additional arguments.

dialect_name¶ – name of a dialect. The dialect must be locatable, else a NoSuchModuleError is raised. The dialect must also include an existing DefaultDialect.construct_arguments collection, indicating that it participates in the keyword-argument validation and default system, else ArgumentError is raised. If the dialect does not include this collection, then any keyword argument can be specified on behalf of this dialect already. All dialects packaged within SQLAlchemy include this collection, however for third party dialects, support may vary.

argument_name¶ – name of the parameter.

default¶ – default value of the parameter.

Issue a CREATE statement for this Index, using the given Connection or Engine` for connectivity.

MetaData.create_all().

inherited from the HasConditionalDDL.ddl_if() method of HasConditionalDDL

apply a conditional DDL rule to this schema item.

These rules work in a similar manner to the ExecutableDDLElement.execute_if() callable, with the added feature that the criteria may be checked within the DDL compilation phase for a construct such as CreateTable. HasConditionalDDL.ddl_if() currently applies towards the Index construct as well as all Constraint constructs.

dialect¶ – string name of a dialect, or a tuple of string names to indicate multiple dialect types.

callable_¶ – a callable that is constructed using the same form as that described in ExecutableDDLElement.execute_if.callable_.

state¶ – any arbitrary object that will be passed to the callable, if present.

Added in version 2.0.

Controlling DDL Generation of Constraints and Indexes - background and usage examples

A collection of keyword arguments specified as dialect-specific options to this construct.

The arguments are present here in their original <dialect>_<kwarg> format. Only arguments that were actually passed are included; unlike the DialectKWArgs.dialect_options collection, which contains all options known by this dialect including defaults.

The collection is also writable; keys are accepted of the form <dialect>_<kwarg> where the value will be assembled into the list of options.

DialectKWArgs.dialect_options - nested dictionary form

inherited from the DialectKWArgs.dialect_options attribute of DialectKWArgs

A collection of keyword arguments specified as dialect-specific options to this construct.

This is a two-level nested registry, keyed to <dialect_name> and <argument_name>. For example, the postgresql_where argument would be locatable as:

Added in version 0.9.2.

DialectKWArgs.dialect_kwargs - flat dictionary form

Issue a DROP statement for this Index, using the given Connection or Engine for connectivity.

inherited from the SchemaItem.info attribute of SchemaItem

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

The dictionary is automatically generated when first accessed. It can also be specified in the constructor of some objects, such as Table and Column.

A synonym for DialectKWArgs.dialect_kwargs.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (unknown):
```unknown
user_preference = Table(
    "user_preference",
    metadata_obj,
    Column("pref_id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.user_id"), nullable=False),
    Column("pref_name", String(40), nullable=False),
    Column("pref_value", String(100)),
)
```

Example 2 (unknown):
```unknown
ForeignKey(user.c.user_id)
```

Example 3 (unknown):
```unknown
invoice = Table(
    "invoice",
    metadata_obj,
    Column("invoice_id", Integer, primary_key=True),
    Column("ref_num", Integer, primary_key=True),
    Column("description", String(60), nullable=False),
)
```

Example 4 (json):
```json
invoice_item = Table(
    "invoice_item",
    metadata_obj,
    Column("item_id", Integer, primary_key=True),
    Column("item_name", String(60), nullable=False),
    Column("invoice_id", Integer, nullable=False),
    Column("ref_num", Integer, nullable=False),
    ForeignKeyConstraint(
        ["invoice_id", "ref_num"], ["invoice.invoice_id", "invoice.ref_num"]
    ),
)
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/tutorial/further_reading.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Unified Tutorial
    - Project Versions
- Further Reading¶

Home | Download this Documentation

Home | Download this Documentation

SQLAlchemy 1.4 / 2.0 Tutorial

This page is part of the SQLAlchemy Unified Tutorial.

Previous: Working with ORM Related Objects

The sections below are the major top-level sections that discuss the concepts in this tutorial in much more detail, as well as describe many more features of each subsystem.

Core Essential Reference

Working with Engines and Connections

Schema Definition Language

SQL Statements and Expressions API

ORM Essential Reference

ORM Mapped Class Configuration

Relationship Configuration

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/core/pooling.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Core
    - Project Versions
- Connection Pooling¶
- Connection Pool Configuration¶
- Switching Pool Implementations¶
- Using a Custom Connection Function¶
- Constructing a Pool¶
- Reset On Return¶

Home | Download this Documentation

Home | Download this Documentation

A connection pool is a standard technique used to maintain long running connections in memory for efficient reuse, as well as to provide management for the total number of connections an application might use simultaneously.

Particularly for server-side web applications, a connection pool is the standard way to maintain a “pool” of active database connections in memory which are reused across requests.

SQLAlchemy includes several connection pool implementations which integrate with the Engine. They can also be used directly for applications that want to add pooling to an otherwise plain DBAPI approach.

The Engine returned by the create_engine() function in most cases has a QueuePool integrated, pre-configured with reasonable pooling defaults. If you’re reading this section only to learn how to enable pooling - congratulations! You’re already done.

The most common QueuePool tuning parameters can be passed directly to create_engine() as keyword arguments: pool_size, max_overflow, pool_recycle and pool_timeout. For example:

All SQLAlchemy pool implementations have in common that none of them “pre create” connections - all implementations wait until first use before creating a connection. At that point, if no additional concurrent checkout requests for more connections are made, no additional connections are created. This is why it’s perfectly fine for create_engine() to default to using a QueuePool of size five without regard to whether or not the application really needs five connections queued up - the pool would only grow to that size if the application actually used five connections concurrently, in which case the usage of a small pool is an entirely appropriate default behavior.

The QueuePool class is not compatible with asyncio. When using create_async_engine to create an instance of AsyncEngine, the AsyncAdaptedQueuePool class, which makes use of an asyncio-compatible queue implementation, is used instead.

The usual way to use a different kind of pool with create_engine() is to use the poolclass argument. This argument accepts a class imported from the sqlalchemy.pool module, and handles the details of building the pool for you. A common use case here is when connection pooling is to be disabled, which can be achieved by using the NullPool implementation:

See the section Custom DBAPI connect() arguments / on-connect routines for a rundown of the various connection customization routines.

To use a Pool by itself, the creator function is the only argument that’s required and is passed first, followed by any additional options:

DBAPI connections can then be procured from the pool using the Pool.connect() function. The return value of this method is a DBAPI connection that’s contained within a transparent proxy:

The purpose of the transparent proxy is to intercept the close() call, such that instead of the DBAPI connection being closed, it is returned to the pool:

The proxy also returns its contained DBAPI connection to the pool when it is garbage collected, though it’s not deterministic in Python that this occurs immediately (though it is typical with cPython). This usage is not recommended however and in particular is not supported with asyncio DBAPI drivers.

The pool includes “reset on return” behavior which will call the rollback() method of the DBAPI connection when the connection is returned to the pool. This is so that any existing transactional state is removed from the connection, which includes not just uncommitted data but table and row locks as well. For most DBAPIs, the call to rollback() is relatively inexpensive.

The “reset on return” feature takes place when a connection is released back to the connection pool. In modern SQLAlchemy, this reset on return behavior is shared between the Connection and the Pool, where the Connection itself, if it releases its transaction upon close, considers .rollback() to have been called, and instructs the pool to skip this step.

For very specific cases where this rollback() is not useful, such as when using a connection that is configured for autocommit or when using a database that has no ACID capabilities such as the MyISAM engine of MySQL, the reset-on-return behavior can be disabled, which is typically done for performance reasons.

As of SQLAlchemy 2.0.43, the create_engine.skip_autocommit_rollback parameter of create_engine() provides the most complete means of preventing ROLLBACK from being emitted while under autocommit mode, as it blocks the DBAPI .rollback() method from being called by the dialect completely:

Detail on this pattern is at Fully preventing ROLLBACK calls under autocommit.

The Pool itself also has a parameter that can control its “reset on return” behavior, noting that in modern SQLAlchemy this is not the only path by which the DBAPI transaction is released, which is the Pool.reset_on_return parameter of Pool, which is also available from create_engine() as create_engine.pool_reset_on_return, passing a value of None. This pattern looks as below:

The above pattern will still see ROLLBACKs occur however as the Connection object implicitly starts transaction blocks in the SQLAlchemy 2.0 series, which still emit ROLLBACK independently of the pool’s reset sequence.

“reset on return” consisting of a single rollback() may not be sufficient for some use cases; in particular, applications which make use of temporary tables may wish for these tables to be automatically removed on connection checkin. Some (but notably not all) backends include features that can “reset” such tables within the scope of a database connection, which may be a desirable behavior for connection pool reset. Other server resources such as prepared statement handles and server-side statement caches may persist beyond the checkin process, which may or may not be desirable, depending on specifics. Again, some (but again not all) backends may provide for a means of resetting this state. The two SQLAlchemy included dialects which are known to have such reset schemes include Microsoft SQL Server, where an undocumented but widely known stored procedure called sp_reset_connection is often used, and PostgreSQL, which has a well-documented series of commands including DISCARD RESET, DEALLOCATE, and UNLISTEN.

The following example illustrates how to replace reset on return with the Microsoft SQL Server sp_reset_connection stored procedure, using the PoolEvents.reset() event hook. The create_engine.pool_reset_on_return parameter is set to None so that the custom scheme can replace the default behavior completely. The custom hook implementation calls .rollback() in any case, as it’s usually important that the DBAPI’s own tracking of commit/rollback will remain consistent with the state of the transaction:

Changed in version 2.0.0b3: Added additional state arguments to the PoolEvents.reset() event and additionally ensured the event is invoked for all “reset” occurrences, so that it’s appropriate as a place for custom “reset” handlers. Previous schemes which use the PoolEvents.checkin() handler remain usable as well.

Temporary Table / Resource Reset for Connection Pooling - in the Microsoft SQL Server documentation

Temporary Table / Resource Reset for Connection Pooling in the PostgreSQL documentation

Logging for pool events including reset on return can be set logging.DEBUG log level along with the sqlalchemy.pool logger, or by setting create_engine.echo_pool to "debug" when using create_engine():

The above pool will show verbose logging including reset on return:

Connection pools support an event interface that allows hooks to execute upon first connect, upon each new connection, and upon checkout and checkin of connections. See PoolEvents for details.

The connection pool has the ability to refresh individual connections as well as its entire set of connections, setting the previously pooled connections as “invalid”. A common use case is allow the connection pool to gracefully recover when the database server has been restarted, and all previously established connections are no longer functional. There are two approaches to this.

The pessimistic approach refers to emitting a test statement on the SQL connection at the start of each connection pool checkout, to test that the database connection is still viable. The implementation is dialect-specific, and makes use of either a DBAPI-specific ping method, or by using a simple SQL statement like “SELECT 1”, in order to test the connection for liveness.

The approach adds a small bit of overhead to the connection checkout process, however is otherwise the most simple and reliable approach to completely eliminating database errors due to stale pooled connections. The calling application does not need to be concerned about organizing operations to be able to recover from stale connections checked out from the pool.

Pessimistic testing of connections upon checkout is achievable by using the Pool.pre_ping argument, available from create_engine() via the create_engine.pool_pre_ping argument:

The “pre ping” feature operates on a per-dialect basis either by invoking a DBAPI-specific “ping” method, or if not available will emit SQL equivalent to “SELECT 1”, catching any errors and detecting the error as a “disconnect” situation. If the ping / error check determines that the connection is not usable, the connection will be immediately recycled, and all other pooled connections older than the current time are invalidated, so that the next time they are checked out, they will also be recycled before use.

If the database is still not available when “pre ping” runs, then the initial connect will fail and the error for failure to connect will be propagated normally. In the uncommon situation that the database is available for connections, but is not able to respond to a “ping”, the “pre_ping” will try up to three times before giving up, propagating the database error last received.

It is critical to note that the pre-ping approach does not accommodate for connections dropped in the middle of transactions or other SQL operations. If the database becomes unavailable while a transaction is in progress, the transaction will be lost and the database error will be raised. While the Connection object will detect a “disconnect” situation and recycle the connection as well as invalidate the rest of the connection pool when this condition occurs, the individual operation where the exception was raised will be lost, and it’s up to the application to either abandon the operation, or retry the whole transaction again. If the engine is configured using DBAPI-level autocommit connections, as described at Setting Transaction Isolation Levels including DBAPI Autocommit, a connection may be reconnected transparently mid-operation using events. See the section How Do I “Retry” a Statement Execution Automatically? for an example.

For dialects that make use of “SELECT 1” and catch errors in order to detect disconnects, the disconnection test may be augmented for new backend-specific error messages using the DialectEvents.handle_error() hook.

Before create_engine.pool_pre_ping was added, the “pre-ping” approach historically has been performed manually using the ConnectionEvents.engine_connect() engine event. The most common recipe for this is below, for reference purposes in case an application is already using such a recipe, or special behaviors are needed:

The above recipe has the advantage that we are making use of SQLAlchemy’s facilities for detecting those DBAPI exceptions that are known to indicate a “disconnect” situation, as well as the Engine object’s ability to correctly invalidate the current connection pool when this condition occurs and allowing the current Connection to re-validate onto a new DBAPI connection.

When pessimistic handling is not employed, as well as when the database is shutdown and/or restarted in the middle of a connection’s period of use within a transaction, the other approach to dealing with stale / closed connections is to let SQLAlchemy handle disconnects as they occur, at which point all connections in the pool are invalidated, meaning they are assumed to be stale and will be refreshed upon next checkout. This behavior assumes the Pool is used in conjunction with a Engine. The Engine has logic which can detect disconnection events and refresh the pool automatically.

When the Connection attempts to use a DBAPI connection, and an exception is raised that corresponds to a “disconnect” event, the connection is invalidated. The Connection then calls the Pool.recreate() method, effectively invalidating all connections not currently checked out so that they are replaced with new ones upon next checkout. This flow is illustrated by the code example below:

The above example illustrates that no special intervention is needed to refresh the pool, which continues normally after a disconnection event is detected. However, one database exception is raised, per each connection that is in use while the database unavailability event occurred. In a typical web application using an ORM Session, the above condition would correspond to a single request failing with a 500 error, then the web application continuing normally beyond that. Hence the approach is “optimistic” in that frequent database restarts are not anticipated.

An additional setting that can augment the “optimistic” approach is to set the pool recycle parameter. This parameter prevents the pool from using a particular connection that has passed a certain age, and is appropriate for database backends such as MySQL that automatically close connections that have been stale after a particular period of time:

Above, any DBAPI connection that has been open for more than one hour will be invalidated and replaced, upon next checkout. Note that the invalidation only occurs during checkout - not on any connections that are held in a checked out state. pool_recycle is a function of the Pool itself, independent of whether or not an Engine is in use.

The Pool provides “connection invalidation” services which allow both explicit invalidation of a connection as well as automatic invalidation in response to conditions that are determined to render a connection unusable.

“Invalidation” means that a particular DBAPI connection is removed from the pool and discarded. The .close() method is called on this connection if it is not clear that the connection itself might not be closed, however if this method fails, the exception is logged but the operation still proceeds.

When using a Engine, the Connection.invalidate() method is the usual entrypoint to explicit invalidation. Other conditions by which a DBAPI connection might be invalidated include:

a DBAPI exception such as OperationalError, raised when a method like connection.execute() is called, is detected as indicating a so-called “disconnect” condition. As the Python DBAPI provides no standard system for determining the nature of an exception, all SQLAlchemy dialects include a system called is_disconnect() which will examine the contents of an exception object, including the string message and any potential error codes included with it, in order to determine if this exception indicates that the connection is no longer usable. If this is the case, the _ConnectionFairy.invalidate() method is called and the DBAPI connection is then discarded.

When the connection is returned to the pool, and calling the connection.rollback() or connection.commit() methods, as dictated by the pool’s “reset on return” behavior, throws an exception. A final attempt at calling .close() on the connection will be made, and it is then discarded.

When a listener implementing PoolEvents.checkout() raises the DisconnectionError exception, indicating that the connection won’t be usable and a new connection attempt needs to be made.

All invalidations which occur will invoke the PoolEvents.invalidate() event.

SQLAlchemy dialects each include a routine called is_disconnect() that is invoked whenever a DBAPI exception is encountered. The DBAPI exception object is passed to this method, where dialect-specific heuristics will then determine if the error code received indicates that the database connection has been “disconnected”, or is in an otherwise unusable state which indicates it should be recycled. The heuristics applied here may be customized using the DialectEvents.handle_error() event hook, which is typically established via the owning Engine object. Using this hook, all errors which occur are delivered passing along a contextual object known as ExceptionContext. Custom event hooks may control whether or not a particular error should be considered a “disconnect” situation or not, as well as if this disconnect should cause the entire connection pool to be invalidated or not.

For example, to add support to consider the Oracle Database driver error codes DPY-1001 and DPY-4011 to be handled as disconnect codes, apply an event handler to the engine after creation:

The above error processing function will be invoked for all Oracle Database errors raised, including those caught when using the pool pre ping feature for those backends that rely upon disconnect error handling (new in 2.0).

DialectEvents.handle_error()

The QueuePool class features a flag called QueuePool.use_lifo, which can also be accessed from create_engine() via the flag create_engine.pool_use_lifo. Setting this flag to True causes the pool’s “queue” behavior to instead be that of a “stack”, e.g. the last connection to be returned to the pool is the first one to be used on the next request. In contrast to the pool’s long- standing behavior of first-in-first-out, which produces a round-robin effect of using each connection in the pool in series, lifo mode allows excess connections to remain idle in the pool, allowing server-side timeout schemes to close these connections out. The difference between FIFO and LIFO is basically whether or not its desirable for the pool to keep a full set of connections ready to go even during idle periods:

Above, we also make use of the create_engine.pool_pre_ping flag so that connections which are closed from the server side are gracefully handled by the connection pool and replaced with a new connection.

Note that the flag only applies to QueuePool use.

Added in version 1.3.

Dealing with Disconnects

It’s critical that when using a connection pool, and by extension when using an Engine created via create_engine(), that the pooled connections are not shared to a forked process. TCP connections are represented as file descriptors, which usually work across process boundaries, meaning this will cause concurrent access to the file descriptor on behalf of two or more entirely independent Python interpreter states.

Depending on specifics of the driver and OS, the issues that arise here range from non-working connections to socket connections that are used by multiple processes concurrently, leading to broken messaging (the latter case is typically the most common).

The SQLAlchemy Engine object refers to a connection pool of existing database connections. So when this object is replicated to a child process, the goal is to ensure that no database connections are carried over. There are four general approaches to this:

Disable pooling using NullPool. This is the most simplistic, one shot system that prevents the Engine from using any connection more than once:

Call Engine.dispose() on any given Engine, passing the Engine.dispose.close parameter with a value of False, within the initialize phase of the child process. This is so that the new process will not touch any of the parent process’ connections and will instead start with new connections. This is the recommended approach:

Added in version 1.4.33: Added the Engine.dispose.close parameter to allow the replacement of a connection pool in a child process without interfering with the connections used by the parent process.

Call Engine.dispose() directly before the child process is created. This will also cause the child process to start with a new connection pool, while ensuring the parent connections are not transferred to the child process:

An event handler can be applied to the connection pool that tests for connections being shared across process boundaries, and invalidates them:

Above, we use an approach similar to that described in Disconnect Handling - Pessimistic to treat a DBAPI connection that originated in a different parent process as an “invalid” connection, coercing the pool to recycle the connection record to make a new connection.

The above strategies will accommodate the case of an Engine being shared among processes. The above steps alone are not sufficient for the case of sharing a specific Connection over a process boundary; prefer to keep the scope of a particular Connection local to a single process (and thread). It’s additionally not supported to share any kind of ongoing transactional state directly across a process boundary, such as an ORM Session object that’s begun a transaction and references active Connection instances; again prefer to create new Session objects in new processes.

A pool implementation can be used directly without an engine. This could be used in applications that just wish to use the pool behavior without all other SQLAlchemy features. In the example below the default pool for the MySQLdb dialect is obtained using create_pool_from_url():

If the type of pool to create is not specified, the default one for the dialect will be used. To specify it directly the poolclass argument can be used, like in the following example:

Proxies a DBAPI connection and provides return-on-dereference support.

Maintains a position in a connection pool which references a pooled connection.

A Pool that allows at most one checked out connection at any given time.

AsyncAdaptedQueuePool

An asyncio-compatible version of QueuePool.

Interface for the object that maintains an individual database connection on behalf of a Pool instance.

Common base for the two connection-management interfaces PoolProxiedConnection and ConnectionPoolEntry.

A Pool which does not pool connections.

Abstract base class for connection pools.

PoolProxiedConnection

A connection-like adapter for a PEP 249 DBAPI connection, which includes additional methods specific to the Pool implementation.

A Pool that imposes a limit on the number of open connections.

A Pool that maintains one connection per thread.

A Pool of exactly one connection, used for all requests.

inherits from sqlalchemy.log.Identified, sqlalchemy.event.registry.EventTarget

Abstract base class for connection pools.

Return a DBAPI connection from the pool.

Dispose of this pool.

Return a new Pool, of the same class as this one and configured with identical creation arguments.

Returns a brief description of the state of this pool.

creator¶ – a callable function that returns a DB-API connection object. The function will be called with parameters.

recycle¶ – If set to a value other than -1, number of seconds between connection recycling, which means upon checkout, if this timeout is surpassed the connection will be closed and replaced with a newly opened connection. Defaults to -1.

logging_name¶ – String identifier which will be used within the “name” field of logging records generated within the “sqlalchemy.pool” logger. Defaults to a hexstring of the object’s id.

if True, the connection pool will log informational output such as when connections are invalidated as well as when connections are recycled to the default log handler, which defaults to sys.stdout for output.. If set to the string "debug", the logging will include pool checkouts and checkins.

The Pool.echo parameter can also be set from the create_engine() call by using the create_engine.echo_pool parameter.

Configuring Logging - further detail on how to configure logging.

Determine steps to take on connections as they are returned to the pool, which were not otherwise handled by a Connection. Available from create_engine() via the create_engine.pool_reset_on_return parameter.

Pool.reset_on_return can have any of these values:

"rollback" - call rollback() on the connection, to release locks and transaction resources. This is the default value. The vast majority of use cases should leave this value set.

"commit" - call commit() on the connection, to release locks and transaction resources. A commit here may be desirable for databases that cache query plans if a commit is emitted, such as Microsoft SQL Server. However, this value is more dangerous than ‘rollback’ because any data changes present on the transaction are committed unconditionally.

None - don’t do anything on the connection. This setting may be appropriate if the database / DBAPI works in pure “autocommit” mode at all times, or if a custom reset handler is established using the PoolEvents.reset() event handler.

True - same as ‘rollback’, this is here for backwards compatibility.

False - same as None, this is here for backwards compatibility.

For further customization of reset on return, the PoolEvents.reset() event hook may be used which can perform any connection activity desired on reset.

events¶ – a list of 2-tuples, each of the form (callable, target) which will be passed to listen() upon construction. Provided here so that event listeners can be assigned via create_engine() before dialect-level listeners are applied.

dialect¶ – a Dialect that will handle the job of calling rollback(), close(), or commit() on DBAPI connections. If omitted, a built-in “stub” dialect is used. Applications that make use of create_engine() should not use this parameter as it is handled by the engine creation strategy.

if True, the pool will emit a “ping” (typically “SELECT 1”, but is dialect-specific) on the connection upon checkout, to test if the connection is alive or not. If not, the connection is transparently re-connected and upon success, all other pooled connections established prior to that timestamp are invalidated. Requires that a dialect is passed as well to interpret the disconnection error.

Added in version 1.2.

Return a DBAPI connection from the pool.

The connection is instrumented such that when its close() method is called, the connection will be returned to the pool.

Dispose of this pool.

This method leaves the possibility of checked-out connections remaining open, as it only affects connections that are idle in the pool.

Return a new Pool, of the same class as this one and configured with identical creation arguments.

This method is used in conjunction with dispose() to close out an entire Pool and create a new one in its place.

Returns a brief description of the state of this pool.

inherits from sqlalchemy.pool.base.Pool

A Pool that imposes a limit on the number of open connections.

QueuePool is the default pooling implementation used for all Engine objects other than SQLite with a :memory: database.

The QueuePool class is not compatible with asyncio and create_async_engine(). The AsyncAdaptedQueuePool class is used automatically when using create_async_engine(), if no other kind of pool is specified.

AsyncAdaptedQueuePool

Construct a QueuePool.

Dispose of this pool.

Return a new Pool, of the same class as this one and configured with identical creation arguments.

Returns a brief description of the state of this pool.

Construct a QueuePool.

creator¶ – a callable function that returns a DB-API connection object, same as that of Pool.creator.

pool_size¶ – The size of the pool to be maintained, defaults to 5. This is the largest number of connections that will be kept persistently in the pool. Note that the pool begins with no connections; once this number of connections is requested, that number of connections will remain. pool_size can be set to 0 to indicate no size limit; to disable pooling, use a NullPool instead.

max_overflow¶ – The maximum overflow size of the pool. When the number of checked-out connections reaches the size set in pool_size, additional connections will be returned up to this limit. When those additional connections are returned to the pool, they are disconnected and discarded. It follows then that the total number of simultaneous connections the pool will allow is pool_size + max_overflow, and the total number of “sleeping” connections the pool will allow is pool_size. max_overflow can be set to -1 to indicate no overflow limit; no limit will be placed on the total number of concurrent connections. Defaults to 10.

timeout¶ – The number of seconds to wait before giving up on returning a connection. Defaults to 30.0. This can be a float but is subject to the limitations of Python time functions which may not be reliable in the tens of milliseconds.

use LIFO (last-in-first-out) when retrieving connections instead of FIFO (first-in-first-out). Using LIFO, a server-side timeout scheme can reduce the number of connections used during non-peak periods of use. When planning for server-side timeouts, ensure that a recycle or pre-ping strategy is in use to gracefully handle stale connections.

Added in version 1.3.

Dealing with Disconnects

**kw¶ – Other keyword arguments including Pool.recycle, Pool.echo, Pool.reset_on_return and others are passed to the Pool constructor.

Dispose of this pool.

This method leaves the possibility of checked-out connections remaining open, as it only affects connections that are idle in the pool.

Return a new Pool, of the same class as this one and configured with identical creation arguments.

This method is used in conjunction with dispose() to close out an entire Pool and create a new one in its place.

Returns a brief description of the state of this pool.

inherits from sqlalchemy.pool.impl.QueuePool

An asyncio-compatible version of QueuePool.

This pool is used by default when using AsyncEngine engines that were generated from create_async_engine(). It uses an asyncio-compatible queue implementation that does not use threading.Lock.

The arguments and operation of AsyncAdaptedQueuePool are otherwise identical to that of QueuePool.

inherits from sqlalchemy.pool.base.Pool

A Pool that maintains one connection per thread.

Maintains one connection per each thread, never moving a connection to a thread other than the one which it was created in.

the SingletonThreadPool will call .close() on arbitrary connections that exist beyond the size setting of pool_size, e.g. if more unique thread identities than what pool_size states are used. This cleanup is non-deterministic and not sensitive to whether or not the connections linked to those thread identities are currently in use.

SingletonThreadPool may be improved in a future release, however in its current status it is generally used only for test scenarios using a SQLite :memory: database and is not recommended for production use.

The SingletonThreadPool class is not compatible with asyncio and create_async_engine().

Options are the same as those of Pool, as well as:

pool_size¶ – The number of threads in which to maintain connections at once. Defaults to five.

SingletonThreadPool is used by the SQLite dialect automatically when a memory-based database is used. See SQLite.

Return a DBAPI connection from the pool.

Dispose of this pool.

Return a new Pool, of the same class as this one and configured with identical creation arguments.

Returns a brief description of the state of this pool.

Return a DBAPI connection from the pool.

The connection is instrumented such that when its close() method is called, the connection will be returned to the pool.

Dispose of this pool.

Return a new Pool, of the same class as this one and configured with identical creation arguments.

This method is used in conjunction with dispose() to close out an entire Pool and create a new one in its place.

Returns a brief description of the state of this pool.

inherits from sqlalchemy.pool.base.Pool

A Pool that allows at most one checked out connection at any given time.

This will raise an exception if more than one connection is checked out at a time. Useful for debugging code that is using more connections than desired.

The AssertionPool class is compatible with asyncio and create_async_engine().

Dispose of this pool.

Return a new Pool, of the same class as this one and configured with identical creation arguments.

Returns a brief description of the state of this pool.

Dispose of this pool.

This method leaves the possibility of checked-out connections remaining open, as it only affects connections that are idle in the pool.

Return a new Pool, of the same class as this one and configured with identical creation arguments.

This method is used in conjunction with dispose() to close out an entire Pool and create a new one in its place.

Returns a brief description of the state of this pool.

inherits from sqlalchemy.pool.base.Pool

A Pool which does not pool connections.

Instead it literally opens and closes the underlying DB-API connection per each connection open/close.

Reconnect-related functions such as recycle and connection invalidation are not supported by this Pool implementation, since no connections are held persistently.

The NullPool class is compatible with asyncio and create_async_engine().

Dispose of this pool.

Return a new Pool, of the same class as this one and configured with identical creation arguments.

Returns a brief description of the state of this pool.

Dispose of this pool.

This method leaves the possibility of checked-out connections remaining open, as it only affects connections that are idle in the pool.

Return a new Pool, of the same class as this one and configured with identical creation arguments.

This method is used in conjunction with dispose() to close out an entire Pool and create a new one in its place.

Returns a brief description of the state of this pool.

inherits from sqlalchemy.pool.base.Pool

A Pool of exactly one connection, used for all requests.

Reconnect-related functions such as recycle and connection invalidation (which is also used to support auto-reconnect) are only partially supported right now and may not yield good results.

The StaticPool class is compatible with asyncio and create_async_engine().

Dispose of this pool.

Return a new Pool, of the same class as this one and configured with identical creation arguments.

Returns a brief description of the state of this pool.

Dispose of this pool.

This method leaves the possibility of checked-out connections remaining open, as it only affects connections that are idle in the pool.

Return a new Pool, of the same class as this one and configured with identical creation arguments.

This method is used in conjunction with dispose() to close out an entire Pool and create a new one in its place.

Returns a brief description of the state of this pool.

Common base for the two connection-management interfaces PoolProxiedConnection and ConnectionPoolEntry.

These two objects are typically exposed in the public facing API via the connection pool event hooks, documented at PoolEvents.

Added in version 2.0.

A reference to the actual DBAPI connection being tracked.

The “driver level” connection object as used by the Python DBAPI or database driver.

Info dictionary associated with the underlying DBAPI connection referred to by this ManagesConnection instance, allowing user-defined data to be associated with the connection.

Mark the managed connection as invalidated.

Persistent info dictionary associated with this ManagesConnection.

A reference to the actual DBAPI connection being tracked.

This is a PEP 249-compliant object that for traditional sync-style dialects is provided by the third-party DBAPI implementation in use. For asyncio dialects, the implementation is typically an adapter object provided by the SQLAlchemy dialect itself; the underlying asyncio object is available via the ManagesConnection.driver_connection attribute.

SQLAlchemy’s interface for the DBAPI connection is based on the DBAPIConnection protocol object

ManagesConnection.driver_connection

How do I get at the raw DBAPI connection when using an Engine?

The “driver level” connection object as used by the Python DBAPI or database driver.

For traditional PEP 249 DBAPI implementations, this object will be the same object as that of ManagesConnection.dbapi_connection. For an asyncio database driver, this will be the ultimate “connection” object used by that driver, such as the asyncpg.Connection object which will not have standard pep-249 methods.

Added in version 1.4.24.

ManagesConnection.dbapi_connection

How do I get at the raw DBAPI connection when using an Engine?

Info dictionary associated with the underlying DBAPI connection referred to by this ManagesConnection instance, allowing user-defined data to be associated with the connection.

The data in this dictionary is persistent for the lifespan of the DBAPI connection itself, including across pool checkins and checkouts. When the connection is invalidated and replaced with a new one, this dictionary is cleared.

For a PoolProxiedConnection instance that’s not associated with a ConnectionPoolEntry, such as if it were detached, the attribute returns a dictionary that is local to that ConnectionPoolEntry. Therefore the ManagesConnection.info attribute will always provide a Python dictionary.

ManagesConnection.record_info

Mark the managed connection as invalidated.

e¶ – an exception object indicating a reason for the invalidation.

soft¶ – if True, the connection isn’t closed; instead, this connection will be recycled on next checkout.

Persistent info dictionary associated with this ManagesConnection.

Unlike the ManagesConnection.info dictionary, the lifespan of this dictionary is that of the ConnectionPoolEntry which owns it; therefore this dictionary will persist across reconnects and connection invalidation for a particular entry in the connection pool.

For a PoolProxiedConnection instance that’s not associated with a ConnectionPoolEntry, such as if it were detached, the attribute returns None. Contrast to the ManagesConnection.info dictionary which is never None.

ManagesConnection.info

inherits from sqlalchemy.pool.base.ManagesConnection

Interface for the object that maintains an individual database connection on behalf of a Pool instance.

The ConnectionPoolEntry object represents the long term maintenance of a particular connection for a pool, including expiring or invalidating that connection to have it replaced with a new one, which will continue to be maintained by that same ConnectionPoolEntry instance. Compared to PoolProxiedConnection, which is the short-term, per-checkout connection manager, this object lasts for the lifespan of a particular “slot” within a connection pool.

The ConnectionPoolEntry object is mostly visible to public-facing API code when it is delivered to connection pool event hooks, such as PoolEvents.connect() and PoolEvents.checkout().

Added in version 2.0: ConnectionPoolEntry provides the public facing interface for the _ConnectionRecord internal class.

Close the DBAPI connection managed by this connection pool entry.

A reference to the actual DBAPI connection being tracked.

The “driver level” connection object as used by the Python DBAPI or database driver.

Info dictionary associated with the underlying DBAPI connection referred to by this ManagesConnection instance, allowing user-defined data to be associated with the connection.

Mark the managed connection as invalidated.

Persistent info dictionary associated with this ManagesConnection.

Close the DBAPI connection managed by this connection pool entry.

A reference to the actual DBAPI connection being tracked.

This is a PEP 249-compliant object that for traditional sync-style dialects is provided by the third-party DBAPI implementation in use. For asyncio dialects, the implementation is typically an adapter object provided by the SQLAlchemy dialect itself; the underlying asyncio object is available via the ManagesConnection.driver_connection attribute.

SQLAlchemy’s interface for the DBAPI connection is based on the DBAPIConnection protocol object

ManagesConnection.driver_connection

How do I get at the raw DBAPI connection when using an Engine?

The “driver level” connection object as used by the Python DBAPI or database driver.

For traditional PEP 249 DBAPI implementations, this object will be the same object as that of ManagesConnection.dbapi_connection. For an asyncio database driver, this will be the ultimate “connection” object used by that driver, such as the asyncpg.Connection object which will not have standard pep-249 methods.

Added in version 1.4.24.

ManagesConnection.dbapi_connection

How do I get at the raw DBAPI connection when using an Engine?

Return True the connection is currently checked out

inherited from the ManagesConnection.info attribute of ManagesConnection

Info dictionary associated with the underlying DBAPI connection referred to by this ManagesConnection instance, allowing user-defined data to be associated with the connection.

The data in this dictionary is persistent for the lifespan of the DBAPI connection itself, including across pool checkins and checkouts. When the connection is invalidated and replaced with a new one, this dictionary is cleared.

For a PoolProxiedConnection instance that’s not associated with a ConnectionPoolEntry, such as if it were detached, the attribute returns a dictionary that is local to that ConnectionPoolEntry. Therefore the ManagesConnection.info attribute will always provide a Python dictionary.

ManagesConnection.record_info

inherited from the ManagesConnection.invalidate() method of ManagesConnection

Mark the managed connection as invalidated.

e¶ – an exception object indicating a reason for the invalidation.

soft¶ – if True, the connection isn’t closed; instead, this connection will be recycled on next checkout.

inherited from the ManagesConnection.record_info attribute of ManagesConnection

Persistent info dictionary associated with this ManagesConnection.

Unlike the ManagesConnection.info dictionary, the lifespan of this dictionary is that of the ConnectionPoolEntry which owns it; therefore this dictionary will persist across reconnects and connection invalidation for a particular entry in the connection pool.

For a PoolProxiedConnection instance that’s not associated with a ConnectionPoolEntry, such as if it were detached, the attribute returns None. Contrast to the ManagesConnection.info dictionary which is never None.

ManagesConnection.info

inherits from sqlalchemy.pool.base.ManagesConnection

A connection-like adapter for a PEP 249 DBAPI connection, which includes additional methods specific to the Pool implementation.

PoolProxiedConnection is the public-facing interface for the internal _ConnectionFairy implementation object; users familiar with _ConnectionFairy can consider this object to be equivalent.

Added in version 2.0: PoolProxiedConnection provides the public- facing interface for the _ConnectionFairy internal class.

Release this connection back to the pool.

A reference to the actual DBAPI connection being tracked.

Separate this connection from its Pool.

The “driver level” connection object as used by the Python DBAPI or database driver.

Info dictionary associated with the underlying DBAPI connection referred to by this ManagesConnection instance, allowing user-defined data to be associated with the connection.

Mark the managed connection as invalidated.

Persistent info dictionary associated with this ManagesConnection.

Release this connection back to the pool.

The PoolProxiedConnection.close() method shadows the PEP 249 .close() method, altering its behavior to instead release the proxied connection back to the connection pool.

Upon release to the pool, whether the connection stays “opened” and pooled in the Python process, versus actually closed out and removed from the Python process, is based on the pool implementation in use and its configuration and current state.

A reference to the actual DBAPI connection being tracked.

This is a PEP 249-compliant object that for traditional sync-style dialects is provided by the third-party DBAPI implementation in use. For asyncio dialects, the implementation is typically an adapter object provided by the SQLAlchemy dialect itself; the underlying asyncio object is available via the ManagesConnection.driver_connection attribute.

SQLAlchemy’s interface for the DBAPI connection is based on the DBAPIConnection protocol object

ManagesConnection.driver_connection

How do I get at the raw DBAPI connection when using an Engine?

Separate this connection from its Pool.

This means that the connection will no longer be returned to the pool when closed, and will instead be literally closed. The associated ConnectionPoolEntry is de-associated from this DBAPI connection.

Note that any overall connection limiting constraints imposed by a Pool implementation may be violated after a detach, as the detached connection is removed from the pool’s knowledge and control.

The “driver level” connection object as used by the Python DBAPI or database driver.

For traditional PEP 249 DBAPI implementations, this object will be the same object as that of ManagesConnection.dbapi_connection. For an asyncio database driver, this will be the ultimate “connection” object used by that driver, such as the asyncpg.Connection object which will not have standard pep-249 methods.

Added in version 1.4.24.

ManagesConnection.dbapi_connection

How do I get at the raw DBAPI connection when using an Engine?

inherited from the ManagesConnection.info attribute of ManagesConnection

Info dictionary associated with the underlying DBAPI connection referred to by this ManagesConnection instance, allowing user-defined data to be associated with the connection.

The data in this dictionary is persistent for the lifespan of the DBAPI connection itself, including across pool checkins and checkouts. When the connection is invalidated and replaced with a new one, this dictionary is cleared.

For a PoolProxiedConnection instance that’s not associated with a ConnectionPoolEntry, such as if it were detached, the attribute returns a dictionary that is local to that ConnectionPoolEntry. Therefore the ManagesConnection.info attribute will always provide a Python dictionary.

ManagesConnection.record_info

inherited from the ManagesConnection.invalidate() method of ManagesConnection

Mark the managed connection as invalidated.

e¶ – an exception object indicating a reason for the invalidation.

soft¶ – if True, the connection isn’t closed; instead, this connection will be recycled on next checkout.

Return True if this PoolProxiedConnection is detached from its pool.

Return True if this PoolProxiedConnection still refers to an active DBAPI connection.

inherited from the ManagesConnection.record_info attribute of ManagesConnection

Persistent info dictionary associated with this ManagesConnection.

Unlike the ManagesConnection.info dictionary, the lifespan of this dictionary is that of the ConnectionPoolEntry which owns it; therefore this dictionary will persist across reconnects and connection invalidation for a particular entry in the connection pool.

For a PoolProxiedConnection instance that’s not associated with a ConnectionPoolEntry, such as if it were detached, the attribute returns None. Contrast to the ManagesConnection.info dictionary which is never None.

ManagesConnection.info

inherits from sqlalchemy.pool.base.PoolProxiedConnection

Proxies a DBAPI connection and provides return-on-dereference support.

This is an internal object used by the Pool implementation to provide context management to a DBAPI connection delivered by that Pool. The public facing interface for this class is described by the PoolProxiedConnection class. See that class for public API details.

The name “fairy” is inspired by the fact that the _ConnectionFairy object’s lifespan is transitory, as it lasts only for the length of a specific DBAPI connection being checked out from the pool, and additionally that as a transparent proxy, it is mostly invisible.

PoolProxiedConnection

inherits from sqlalchemy.pool.base.ConnectionPoolEntry

Maintains a position in a connection pool which references a pooled connection.

This is an internal object used by the Pool implementation to provide context management to a DBAPI connection maintained by that Pool. The public facing interface for this class is described by the ConnectionPoolEntry class. See that class for public API details.

PoolProxiedConnection

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
engine = create_engine(
    "postgresql+psycopg2://me@localhost/mydb", pool_size=20, max_overflow=0
)
```

Example 2 (python):
```python
from sqlalchemy.pool import NullPool

engine = create_engine(
    "postgresql+psycopg2://scott:tiger@localhost/test", poolclass=NullPool
)
```

Example 3 (python):
```python
import sqlalchemy.pool as pool
import psycopg2


def getconn():
    c = psycopg2.connect(user="ed", host="127.0.0.1", dbname="test")
    return c


mypool = pool.QueuePool(getconn, max_overflow=10, pool_size=5)
```

Example 4 (sql):
```sql
# get a connection
conn = mypool.connect()

# use it
cursor_obj = conn.cursor()
cursor_obj.execute("select foo")
```

---
