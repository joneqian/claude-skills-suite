# Sqlalchemy - Async

**Pages:** 1

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Asynchronous I/O (asyncio)¶
- Asyncio Platform Installation Notes (Including Apple M1)¶
- Synopsis - Core¶
- Synopsis - ORM¶
  - Using AsyncSession with Concurrent Tasks¶
  - Preventing Implicit IO when Using AsyncSession¶

Home | Download this Documentation

Home | Download this Documentation

Support for Python asyncio. Support for Core and ORM usage is included, using asyncio-compatible dialects.

Added in version 1.4.

Please read Asyncio Platform Installation Notes (Including Apple M1) for important platform installation notes for many platforms, including Apple M1 Architecture.

Asynchronous IO Support for Core and ORM - initial feature announcement

Asyncio Integration - example scripts illustrating working examples of Core and ORM use within the asyncio extension.

The asyncio extension requires Python 3 only. It also depends upon the greenlet library. This dependency is installed by default on common machine platforms including:

For the above platforms, greenlet is known to supply pre-built wheel files. For other platforms, greenlet does not install by default; the current file listing for greenlet can be seen at Greenlet - Download Files. Note that there are many architectures omitted, including Apple M1.

To install SQLAlchemy while ensuring the greenlet dependency is present regardless of what platform is in use, the [asyncio] setuptools extra may be installed as follows, which will include also instruct pip to install greenlet:

Note that installation of greenlet on platforms that do not have a pre-built wheel file means that greenlet will be built from source, which requires that Python’s development libraries also be present.

For Core use, the create_async_engine() function creates an instance of AsyncEngine which then offers an async version of the traditional Engine API. The AsyncEngine delivers an AsyncConnection via its AsyncEngine.connect() and AsyncEngine.begin() methods which both deliver asynchronous context managers. The AsyncConnection can then invoke statements using either the AsyncConnection.execute() method to deliver a buffered Result, or the AsyncConnection.stream() method to deliver a streaming server-side AsyncResult:

Above, the AsyncConnection.run_sync() method may be used to invoke special DDL functions such as MetaData.create_all() that don’t include an awaitable hook.

It’s advisable to invoke the AsyncEngine.dispose() method using await when using the AsyncEngine object in a scope that will go out of context and be garbage collected, as illustrated in the async_main function in the above example. This ensures that any connections held open by the connection pool will be properly disposed within an awaitable context. Unlike when using blocking IO, SQLAlchemy cannot properly dispose of these connections within methods like __del__ or weakref finalizers as there is no opportunity to invoke await. Failing to explicitly dispose of the engine when it falls out of scope may result in warnings emitted to standard out resembling the form RuntimeError: Event loop is closed within garbage collection.

The AsyncConnection also features a “streaming” API via the AsyncConnection.stream() method that returns an AsyncResult object. This result object uses a server-side cursor and provides an async/await API, such as an async iterator:

Using 2.0 style querying, the AsyncSession class provides full ORM functionality.

Within the default mode of use, special care must be taken to avoid lazy loading or other expired-attribute access involving ORM relationships and column attributes; the next section Preventing Implicit IO when Using AsyncSession details this.

A single instance of AsyncSession is not safe for use in multiple, concurrent tasks. See the sections Using AsyncSession with Concurrent Tasks and Is the Session thread-safe? Is AsyncSession safe to share in concurrent tasks? for background.

The example below illustrates a complete example including mapper and session configuration:

In the example above, the AsyncSession is instantiated using the optional async_sessionmaker helper, which provides a factory for new AsyncSession objects with a fixed set of parameters, which here includes associating it with an AsyncEngine against particular database URL. It is then passed to other methods where it may be used in a Python asynchronous context manager (i.e. async with: statement) so that it is automatically closed at the end of the block; this is equivalent to calling the AsyncSession.close() method.

The AsyncSession object is a mutable, stateful object which represents a single, stateful database transaction in progress. Using concurrent tasks with asyncio, with APIs such as asyncio.gather() for example, should use a separate AsyncSession per individual task.

See the section Is the Session thread-safe? Is AsyncSession safe to share in concurrent tasks? for a general description of the Session and AsyncSession with regards to how they should be used with concurrent workloads.

Using traditional asyncio, the application needs to avoid any points at which IO-on-attribute access may occur. Techniques that can be used to help this are below, many of which are illustrated in the preceding example.

Attributes that are lazy-loading relationships, deferred columns or expressions, or are being accessed in expiration scenarios can take advantage of the AsyncAttrs mixin. This mixin, when added to a specific class or more generally to the Declarative Base superclass, provides an accessor AsyncAttrs.awaitable_attrs which delivers any attribute as an awaitable:

Accessing the A.bs collection on newly loaded instances of A when eager loading is not in use will normally use lazy loading, which in order to succeed will usually emit IO to the database, which will fail under asyncio as no implicit IO is allowed. To access this attribute directly under asyncio without any prior loading operations, the attribute can be accessed as an awaitable by indicating the AsyncAttrs.awaitable_attrs prefix:

The AsyncAttrs mixin provides a succinct facade over the internal approach that’s also used by the AsyncSession.run_sync() method.

Added in version 2.0.13.

Collections can be replaced with write only collections that will never emit IO implicitly, by using the Write Only Relationships feature in SQLAlchemy 2.0. Using this feature, collections are never read from, only queried using explicit SQL calls. See the example async_orm_writeonly.py in the Asyncio Integration section for an example of write-only collections used with asyncio.

When using write only collections, the program’s behavior is simple and easy to predict regarding collections. However, the downside is that there is not any built-in system for loading many of these collections all at once, which instead would need to be performed manually. Therefore, many of the bullets below address specific techniques when using traditional lazy-loaded relationships with asyncio, which requires more care.

If not using AsyncAttrs, relationships can be declared with lazy="raise" so that by default they will not attempt to emit SQL. In order to load collections, eager loading would be used instead.

The most useful eager loading strategy is the selectinload() eager loader, which is employed in the previous example in order to eagerly load the A.bs collection within the scope of the await session.execute() call:

When constructing new objects, collections are always assigned a default, empty collection, such as a list in the above example:

This allows the .bs collection on the above A object to be present and readable when the A object is flushed; otherwise, when the A is flushed, .bs would be unloaded and would raise an error on access.

The AsyncSession is configured using Session.expire_on_commit set to False, so that we may access attributes on an object subsequent to a call to AsyncSession.commit(), as in the line at the end where we access an attribute:

Other guidelines include:

Methods like AsyncSession.expire() should be avoided in favor of AsyncSession.refresh(); if expiration is absolutely needed. Expiration should generally not be needed as Session.expire_on_commit should normally be set to False when using asyncio.

A lazy-loaded relationship can be loaded explicitly under asyncio using AsyncSession.refresh(), if the desired attribute name is passed explicitly to Session.refresh.attribute_names, e.g.:

It’s of course preferable to use eager loading up front in order to have collections already set up without the need to lazy-load.

Added in version 2.0.4: Added support for AsyncSession.refresh() and the underlying Session.refresh() method to force lazy-loaded relationships to load, if they are named explicitly in the Session.refresh.attribute_names parameter. In previous versions, the relationship would be silently skipped even if named in the parameter.

Avoid using the all cascade option documented at Cascades in favor of listing out the desired cascade features explicitly. The all cascade option implies among others the refresh-expire setting, which means that the AsyncSession.refresh() method will expire the attributes on related objects, but not necessarily refresh those related objects assuming eager loading is not configured within the relationship(), leaving them in an expired state.

Appropriate loader options should be employed for deferred() columns, if used at all, in addition to that of relationship() constructs as noted above. See Limiting which Columns Load with Column Deferral for background on deferred column loading.

The “dynamic” relationship loader strategy described at Dynamic Relationship Loaders is not compatible by default with the asyncio approach. It can be used directly only if invoked within the AsyncSession.run_sync() method described at Running Synchronous Methods and Functions under asyncio, or by using its .statement attribute to obtain a normal select:

The write only technique, introduced in version 2.0 of SQLAlchemy, is fully compatible with asyncio and should be preferred.

“Dynamic” relationship loaders superseded by “Write Only” - notes on migration to 2.0 style

If using asyncio with a database that does not support RETURNING, such as MySQL 8, server default values such as generated timestamps will not be available on newly flushed objects unless the Mapper.eager_defaults option is used. In SQLAlchemy 2.0, this behavior is applied automatically to backends like PostgreSQL, SQLite and MariaDB which use RETURNING to fetch new values when rows are INSERTed.

This approach is essentially exposing publicly the mechanism by which SQLAlchemy is able to provide the asyncio interface in the first place. While there is no technical issue with doing so, overall the approach can probably be considered “controversial” as it works against some of the central philosophies of the asyncio programming model, which is essentially that any programming statement that can potentially result in IO being invoked must have an await call, lest the program does not make it explicitly clear every line at which IO may occur. This approach does not change that general idea, except that it allows a series of synchronous IO instructions to be exempted from this rule within the scope of a function call, essentially bundled up into a single awaitable.

As an alternative means of integrating traditional SQLAlchemy “lazy loading” within an asyncio event loop, an optional method known as AsyncSession.run_sync() is provided which will run any Python function inside of a greenlet, where traditional synchronous programming concepts will be translated to use await when they reach the database driver. A hypothetical approach here is an asyncio-oriented application can package up database-related methods into functions that are invoked using AsyncSession.run_sync().

Altering the above example, if we didn’t use selectinload() for the A.bs collection, we could accomplish our treatment of these attribute accesses within a separate function:

The above approach of running certain functions within a “sync” runner has some parallels to an application that runs a SQLAlchemy application on top of an event-based programming library such as gevent. The differences are as follows:

unlike when using gevent, we can continue to use the standard Python asyncio event loop, or any custom event loop, without the need to integrate into the gevent event loop.

There is no “monkeypatching” whatsoever. The above example makes use of a real asyncio driver and the underlying SQLAlchemy connection pool is also using the Python built-in asyncio.Queue for pooling connections.

The program can freely switch between async/await code and contained functions that use sync code with virtually no performance penalty. There is no “thread executor” or any additional waiters or synchronization in use.

The underlying network drivers are also using pure Python asyncio concepts, no third party networking libraries as gevent and eventlet provides are in use.

The SQLAlchemy event system is not directly exposed by the asyncio extension, meaning there is not yet an “async” version of a SQLAlchemy event handler.

However, as the asyncio extension surrounds the usual synchronous SQLAlchemy API, regular “synchronous” style event handlers are freely available as they would be if asyncio were not used.

As detailed below, there are two current strategies to register events given asyncio-facing APIs:

Events can be registered at the instance level (e.g. a specific AsyncEngine instance) by associating the event with the sync attribute that refers to the proxied object. For example to register the PoolEvents.connect() event against an AsyncEngine instance, use its AsyncEngine.sync_engine attribute as target. Targets include:

AsyncEngine.sync_engine

AsyncConnection.sync_connection

AsyncConnection.sync_engine

AsyncSession.sync_session

To register an event at the class level, targeting all instances of the same type (e.g. all AsyncSession instances), use the corresponding sync-style class. For example to register the SessionEvents.before_commit() event against the AsyncSession class, use the Session class as the target.

To register at the sessionmaker level, combine an explicit sessionmaker with an async_sessionmaker using async_sessionmaker.sync_session_class, and associate events with the sessionmaker.

When working within an event handler that is within an asyncio context, objects like the Connection continue to work in their usual “synchronous” way without requiring await or async usage; when messages are ultimately received by the asyncio database adapter, the calling style is transparently adapted back into the asyncio calling style. For events that are passed a DBAPI level connection, such as PoolEvents.connect(), the object is a pep-249 compliant “connection” object which will adapt sync-style calls into the asyncio driver.

Some examples of sync style event handlers associated with async-facing API constructs are illustrated below:

Core Events on AsyncEngine

In this example, we access the AsyncEngine.sync_engine attribute of AsyncEngine as the target for ConnectionEvents and PoolEvents:

ORM Events on AsyncSession

In this example, we access AsyncSession.sync_session as the target for SessionEvents:

ORM Events on async_sessionmaker

For this use case, we make a sessionmaker as the event target, then assign it to the async_sessionmaker using the async_sessionmaker.sync_session_class parameter:

asyncio and events, two opposites

SQLAlchemy events by their nature take place within the interior of a particular SQLAlchemy process; that is, an event always occurs after some particular SQLAlchemy API has been invoked by end-user code, and before some other internal aspect of that API occurs.

Contrast this to the architecture of the asyncio extension, which takes place on the exterior of SQLAlchemy’s usual flow from end-user API to DBAPI function.

The flow of messaging may be visualized as follows:

Where above, an API call always starts as asyncio, flows through the synchronous API, and ends as asyncio, before results are propagated through this same chain in the opposite direction. In between, the message is adapted first into sync-style API use, and then back out to async style. Event hooks then by their nature occur in the middle of the “sync-style API use”. From this it follows that the API presented within event hooks occurs inside the process by which asyncio API requests have been adapted to sync, and outgoing messages to the database API will be converted to asyncio transparently.

As discussed in the above section, event handlers such as those oriented around the PoolEvents event handlers receive a sync-style “DBAPI” connection, which is a wrapper object supplied by SQLAlchemy asyncio dialects to adapt the underlying asyncio “driver” connection into one that can be used by SQLAlchemy’s internals. A special use case arises when the user-defined implementation for such an event handler needs to make use of the ultimate “driver” connection directly, using awaitable only methods on that driver connection. One such example is the .set_type_codec() method supplied by the asyncpg driver.

To accommodate this use case, SQLAlchemy’s AdaptedConnection class provides a method AdaptedConnection.run_async() that allows an awaitable function to be invoked within the “synchronous” context of an event handler or other SQLAlchemy internal. This method is directly analogous to the AsyncConnection.run_sync() method that allows a sync-style method to run under async.

AdaptedConnection.run_async() should be passed a function that will accept the innermost “driver” connection as a single argument, and return an awaitable that will be invoked by the AdaptedConnection.run_async() method. The given function itself does not need to be declared as async; it’s perfectly fine for it to be a Python lambda:, as the return awaitable value will be invoked after being returned:

Above, the object passed to the register_custom_types event handler is an instance of AdaptedConnection, which provides a DBAPI-like interface to an underlying async-only driver-level connection object. The AdaptedConnection.run_async() method then provides access to an awaitable environment where the underlying driver level connection may be acted upon.

Added in version 1.4.30.

An application that makes use of multiple event loops, for example in the uncommon case of combining asyncio with multithreading, should not share the same AsyncEngine with different event loops when using the default pool implementation.

If an AsyncEngine is be passed from one event loop to another, the method AsyncEngine.dispose() should be called before it’s reused on a new event loop. Failing to do so may lead to a RuntimeError along the lines of Task <Task pending ...> got Future attached to a different loop

If the same engine must be shared between different loop, it should be configured to disable pooling using NullPool, preventing the Engine from using any connection more than once:

The “scoped session” pattern used in threaded SQLAlchemy with the scoped_session object is also available in asyncio, using an adapted version called async_scoped_session.

SQLAlchemy generally does not recommend the “scoped” pattern for new development as it relies upon mutable global state that must also be explicitly torn down when work within the thread or task is complete. Particularly when using asyncio, it’s likely a better idea to pass the AsyncSession directly to the awaitable functions that need it.

When using async_scoped_session, as there’s no “thread-local” concept in the asyncio context, the “scopefunc” parameter must be provided to the constructor. The example below illustrates using the asyncio.current_task() function for this purpose:

The “scopefunc” used by async_scoped_session is invoked an arbitrary number of times within a task, once for each time the underlying AsyncSession is accessed. The function should therefore be idempotent and lightweight, and should not attempt to create or mutate any state, such as establishing callbacks, etc.

Using current_task() for the “key” in the scope requires that the async_scoped_session.remove() method is called from within the outermost awaitable, to ensure the key is removed from the registry when the task is complete, otherwise the task handle as well as the AsyncSession will remain in memory, essentially creating a memory leak. See the following example which illustrates the correct use of async_scoped_session.remove().

async_scoped_session includes proxy behavior similar to that of scoped_session, which means it can be treated as a AsyncSession directly, keeping in mind that the usual await keywords are necessary, including for the async_scoped_session.remove() method:

Added in version 1.4.19.

SQLAlchemy does not yet offer an asyncio version of the Inspector (introduced at Fine Grained Reflection with Inspector), however the existing interface may be used in an asyncio context by leveraging the AsyncConnection.run_sync() method of AsyncConnection:

Reflecting Database Objects

Runtime Inspection API

async_engine_from_config(configuration[, prefix], **kwargs)

Create a new AsyncEngine instance using a configuration dictionary.

An asyncio proxy for a Connection.

An asyncio proxy for a Engine.

An asyncio proxy for a Transaction.

create_async_engine(url, **kw)

Create a new async engine instance.

create_async_pool_from_url(url, **kwargs)

Create a new async engine instance.

Create a new async engine instance.

Arguments passed to create_async_engine() are mostly identical to those passed to the create_engine() function. The specified dialect must be an asyncio-compatible dialect such as asyncpg.

Added in version 1.4.

an async callable which returns a driver-level asyncio connection. If given, the function should take no arguments, and return a new asyncio connection from the underlying asyncio database driver; the connection will be wrapped in the appropriate structures to be used with the AsyncEngine. Note that the parameters specified in the URL are not applied here, and the creator function should use its own connection parameters.

This parameter is the asyncio equivalent of the create_engine.creator parameter of the create_engine() function.

Added in version 2.0.16.

Create a new AsyncEngine instance using a configuration dictionary.

This function is analogous to the engine_from_config() function in SQLAlchemy Core, except that the requested dialect must be an asyncio-compatible dialect such as asyncpg. The argument signature of the function is identical to that of engine_from_config().

Added in version 1.4.29.

Create a new async engine instance.

Arguments passed to create_async_pool_from_url() are mostly identical to those passed to the create_pool_from_url() function. The specified dialect must be an asyncio-compatible dialect such as asyncpg.

Added in version 2.0.10.

inherits from sqlalchemy.ext.asyncio.base.ProxyComparable, sqlalchemy.ext.asyncio.AsyncConnectable

An asyncio proxy for a Engine.

AsyncEngine is acquired using the create_async_engine() function:

Added in version 1.4.

Return a context manager which when entered will deliver an AsyncConnection with an AsyncTransaction established.

clear_compiled_cache()

Clear the compiled cache associated with the dialect.

Return an AsyncConnection object.

Dispose of the connection pool used by this AsyncEngine.

Return a new AsyncEngine that will provide AsyncConnection objects with the given execution options.

get_execution_options()

Get the non-SQL options which will take effect during execution.

Return a “raw” DBAPI connection from the connection pool.

Reference to the sync-style Engine this AsyncEngine proxies requests towards.

update_execution_options()

Update the default execution_options dictionary of this Engine.

Return a context manager which when entered will deliver an AsyncConnection with an AsyncTransaction established.

Clear the compiled cache associated with the dialect.

Proxied for the Engine class on behalf of the AsyncEngine class.

This applies only to the built-in cache that is established via the create_engine.query_cache_size parameter. It will not impact any dictionary caches that were passed via the Connection.execution_options.compiled_cache parameter.

Added in version 1.4.

Return an AsyncConnection object.

The AsyncConnection will procure a database connection from the underlying connection pool when it is entered as an async context manager:

The AsyncConnection may also be started outside of a context manager by invoking its AsyncConnection.start() method.

Proxy for the Engine.dialect attribute on behalf of the AsyncEngine class.

Dispose of the connection pool used by this AsyncEngine.

if left at its default of True, has the effect of fully closing all currently checked in database connections. Connections that are still checked out will not be closed, however they will no longer be associated with this Engine, so when they are closed individually, eventually the Pool which they are associated with will be garbage collected and they will be closed out fully, if not already closed on checkin.

If set to False, the previous connection pool is de-referenced, and otherwise not touched in any way.

Driver name of the Dialect in use by this Engine.

Proxied for the Engine class on behalf of the AsyncEngine class.

When True, enable log output for this element.

Proxied for the Engine class on behalf of the AsyncEngine class.

This has the effect of setting the Python logging level for the namespace of this element’s class and object reference. A value of boolean True indicates that the loglevel logging.INFO will be set for the logger, whereas the string value debug will set the loglevel to logging.DEBUG.

Proxied for the Engine class on behalf of the AsyncEngine class.

Used for legacy schemes that accept Connection / Engine objects within the same variable.

Return a new AsyncEngine that will provide AsyncConnection objects with the given execution options.

Proxied from Engine.execution_options(). See that method for details.

Get the non-SQL options which will take effect during execution.

Proxied for the Engine class on behalf of the AsyncEngine class.

Engine.execution_options()

String name of the Dialect in use by this Engine.

Proxied for the Engine class on behalf of the AsyncEngine class.

Proxy for the Engine.pool attribute on behalf of the AsyncEngine class.

Return a “raw” DBAPI connection from the connection pool.

Working with Driver SQL and Raw DBAPI Connections

Reference to the sync-style Engine this AsyncEngine proxies requests towards.

This instance can be used as an event target.

Using events with the asyncio extension

Update the default execution_options dictionary of this Engine.

Proxied for the Engine class on behalf of the AsyncEngine class.

The given keys/values in **opt are added to the default execution options that will be used for all connections. The initial contents of this dictionary can be sent via the execution_options parameter to create_engine().

Connection.execution_options()

Engine.execution_options()

Proxy for the Engine.url attribute on behalf of the AsyncEngine class.

inherits from sqlalchemy.ext.asyncio.base.ProxyComparable, sqlalchemy.ext.asyncio.base.StartableContext, sqlalchemy.ext.asyncio.AsyncConnectable

An asyncio proxy for a Connection.

AsyncConnection is acquired using the AsyncEngine.connect() method of AsyncEngine:

Added in version 1.4.

A synonym for AsyncConnection.close().

Begin a transaction prior to autobegin occurring.

Begin a nested transaction and return a transaction handle.

Close this AsyncConnection.

Commit the transaction that is currently in progress.

Executes a driver-level SQL string and return buffered Result.

Executes a SQL statement construct and return a buffered Result.

Set non-SQL options for the connection which take effect during execution.

get_nested_transaction()

Return an AsyncTransaction representing the current nested (savepoint) transaction, if any.

Return the pooled DBAPI-level connection in use by this AsyncConnection.

Return an AsyncTransaction representing the current transaction, if any.

in_nested_transaction()

Return True if a transaction is in progress.

Return True if a transaction is in progress.

Return the Connection.info dictionary of the underlying Connection.

Invalidate the underlying DBAPI connection associated with this Connection.

Roll back the transaction that is currently in progress.

Invoke the given synchronous (i.e. not async) callable, passing a synchronous-style Connection as the first argument.

Executes a SQL statement construct and returns a scalar object.

Executes a SQL statement construct and returns a scalar objects.

Start this AsyncConnection object’s context outside of using a Python with: block.

Execute a statement and return an awaitable yielding a AsyncResult object.

Execute a statement and return an awaitable yielding a AsyncScalarResult object.

Reference to the sync-style Connection this AsyncConnection proxies requests towards.

Reference to the sync-style Engine this AsyncConnection is associated with via its underlying Connection.

A synonym for AsyncConnection.close().

The AsyncConnection.aclose() name is specifically to support the Python standard library @contextlib.aclosing context manager function.

Added in version 2.0.20.

Begin a transaction prior to autobegin occurring.

Begin a nested transaction and return a transaction handle.

Close this AsyncConnection.

This has the effect of also rolling back the transaction if one is in place.

Return True if this connection is closed.

Proxied for the Connection class on behalf of the AsyncConnection class.

Commit the transaction that is currently in progress.

This method commits the current transaction if one has been started. If no transaction was started, the method has no effect, assuming the connection is in a non-invalidated state.

A transaction is begun on a Connection automatically whenever a statement is first executed, or when the Connection.begin() method is called.

Not implemented for async; call AsyncConnection.get_raw_connection().

The initial-connection time isolation level associated with the Dialect in use.

Proxied for the Connection class on behalf of the AsyncConnection class.

This value is independent of the Connection.execution_options.isolation_level and Engine.execution_options.isolation_level execution options, and is determined by the Dialect when the first connection is created, by performing a SQL query against the database for the current isolation level before any additional commands have been emitted.

Calling this accessor does not invoke any new SQL queries.

Connection.get_isolation_level() - view current actual isolation level

create_engine.isolation_level - set per Engine isolation level

Connection.execution_options.isolation_level - set per Connection isolation level

Proxy for the Connection.dialect attribute on behalf of the AsyncConnection class.

Executes a driver-level SQL string and return buffered Result.

Executes a SQL statement construct and return a buffered Result.

The statement to be executed. This is always an object that is in both the ClauseElement and Executable hierarchies, including:

Insert, Update, Delete

TextClause and TextualSelect

DDL and objects which inherit from ExecutableDDLElement

parameters¶ – parameters which will be bound into the statement. This may be either a dictionary of parameter names to values, or a mutable sequence (e.g. a list) of dictionaries. When a list of dictionaries is passed, the underlying statement execution will make use of the DBAPI cursor.executemany() method. When a single dictionary is passed, the DBAPI cursor.execute() method will be used.

execution_options¶ – optional dictionary of execution options, which will be associated with the statement execution. This dictionary can provide a subset of the options that are accepted by Connection.execution_options().

Set non-SQL options for the connection which take effect during execution.

This returns this AsyncConnection object with the new options added.

See Connection.execution_options() for full details on this method.

Return an AsyncTransaction representing the current nested (savepoint) transaction, if any.

This makes use of the underlying synchronous connection’s Connection.get_nested_transaction() method to get the current Transaction, which is then proxied in a new AsyncTransaction object.

Added in version 1.4.0b2.

Return the pooled DBAPI-level connection in use by this AsyncConnection.

This is a SQLAlchemy connection-pool proxied connection which then has the attribute _ConnectionFairy.driver_connection that refers to the actual driver connection. Its _ConnectionFairy.dbapi_connection refers instead to an AdaptedConnection instance that adapts the driver connection to the DBAPI protocol.

Return an AsyncTransaction representing the current transaction, if any.

This makes use of the underlying synchronous connection’s Connection.get_transaction() method to get the current Transaction, which is then proxied in a new AsyncTransaction object.

Added in version 1.4.0b2.

Return True if a transaction is in progress.

Added in version 1.4.0b2.

Return True if a transaction is in progress.

Return the Connection.info dictionary of the underlying Connection.

This dictionary is freely writable for user-defined state to be associated with the database connection.

This attribute is only available if the AsyncConnection is currently connected. If the AsyncConnection.closed attribute is True, then accessing this attribute will raise ResourceClosedError.

Added in version 1.4.0b2.

Invalidate the underlying DBAPI connection associated with this Connection.

See the method Connection.invalidate() for full detail on this method.

Return True if this connection was invalidated.

Proxied for the Connection class on behalf of the AsyncConnection class.

This does not indicate whether or not the connection was invalidated at the pool level, however

Roll back the transaction that is currently in progress.

This method rolls back the current transaction if one has been started. If no transaction was started, the method has no effect. If a transaction was started and the connection is in an invalidated state, the transaction is cleared using this method.

A transaction is begun on a Connection automatically whenever a statement is first executed, or when the Connection.begin() method is called.

Invoke the given synchronous (i.e. not async) callable, passing a synchronous-style Connection as the first argument.

This method allows traditional synchronous SQLAlchemy functions to run within the context of an asyncio application.

This method maintains the asyncio event loop all the way through to the database connection by running the given callable in a specially instrumented greenlet.

The most rudimentary use of AsyncConnection.run_sync() is to invoke methods such as MetaData.create_all(), given an AsyncConnection that needs to be provided to MetaData.create_all() as a Connection object:

The provided callable is invoked inline within the asyncio event loop, and will block on traditional IO calls. IO within this callable should only call into SQLAlchemy’s asyncio database APIs which will be properly adapted to the greenlet context.

AsyncSession.run_sync()

Running Synchronous Methods and Functions under asyncio

Executes a SQL statement construct and returns a scalar object.

This method is shorthand for invoking the Result.scalar() method after invoking the Connection.execute() method. Parameters are equivalent.

a scalar Python value representing the first column of the first row returned.

Executes a SQL statement construct and returns a scalar objects.

This method is shorthand for invoking the Result.scalars() method after invoking the Connection.execute() method. Parameters are equivalent.

a ScalarResult object.

Added in version 1.4.24.

Start this AsyncConnection object’s context outside of using a Python with: block.

Execute a statement and return an awaitable yielding a AsyncResult object.

The AsyncConnection.stream() method supports optional context manager use against the AsyncResult object, as in:

In the above pattern, the AsyncResult.close() method is invoked unconditionally, even if the iterator is interrupted by an exception throw. Context manager use remains optional, however, and the function may be called in either an async with fn(): or await fn() style.

Added in version 2.0.0b3: added context manager support

an awaitable object that will yield an AsyncResult object.

AsyncConnection.stream_scalars()

Execute a statement and return an awaitable yielding a AsyncScalarResult object.

This method is shorthand for invoking the AsyncResult.scalars() method after invoking the Connection.stream() method. Parameters are equivalent.

The AsyncConnection.stream_scalars() method supports optional context manager use against the AsyncScalarResult object, as in:

In the above pattern, the AsyncScalarResult.close() method is invoked unconditionally, even if the iterator is interrupted by an exception throw. Context manager use remains optional, however, and the function may be called in either an async with fn(): or await fn() style.

Added in version 2.0.0b3: added context manager support

an awaitable object that will yield an AsyncScalarResult object.

Added in version 1.4.24.

AsyncConnection.stream()

Reference to the sync-style Connection this AsyncConnection proxies requests towards.

This instance can be used as an event target.

Using events with the asyncio extension

Reference to the sync-style Engine this AsyncConnection is associated with via its underlying Connection.

This instance can be used as an event target.

Using events with the asyncio extension

inherits from sqlalchemy.ext.asyncio.base.ProxyComparable, sqlalchemy.ext.asyncio.base.StartableContext

An asyncio proxy for a Transaction.

Close this AsyncTransaction.

Commit this AsyncTransaction.

Roll back this AsyncTransaction.

Start this AsyncTransaction object’s context outside of using a Python with: block.

Close this AsyncTransaction.

If this transaction is the base transaction in a begin/commit nesting, the transaction will rollback(). Otherwise, the method returns.

This is used to cancel a Transaction without affecting the scope of an enclosing transaction.

Commit this AsyncTransaction.

Roll back this AsyncTransaction.

Start this AsyncTransaction object’s context outside of using a Python with: block.

The AsyncResult object is an async-adapted version of the Result object. It is only returned when using the AsyncConnection.stream() or AsyncSession.stream() methods, which return a result object that is on top of an active database cursor.

A wrapper for a AsyncResult that returns dictionary values rather than Row values.

An asyncio wrapper around a Result object.

A wrapper for a AsyncResult that returns scalar values rather than Row values.

A AsyncResult that’s typed as returning plain Python tuples instead of rows.

inherits from sqlalchemy.engine._WithKeys, sqlalchemy.ext.asyncio.AsyncCommon

An asyncio wrapper around a Result object.

The AsyncResult only applies to statement executions that use a server-side cursor. It is returned only from the AsyncConnection.stream() and AsyncSession.stream() methods.

As is the case with Result, this object is used for ORM results returned by AsyncSession.execute(), which can yield instances of ORM mapped objects either individually or within tuple-like rows. Note that these result objects do not deduplicate instances or rows automatically as is the case with the legacy Query object. For in-Python de-duplication of instances or rows, use the AsyncResult.unique() modifier method.

Added in version 1.4.

Return all rows in a list.

Establish the columns that should be returned in each row.

A synonym for the AsyncResult.all() method.

Fetch the first row or None if no row is present.

Return a callable object that will produce copies of this AsyncResult when invoked.

Return an iterable view which yields the string keys that would be represented by each Row.

Apply a mappings filter to returned rows, returning an instance of AsyncMappingResult.

Return exactly one row or raise an exception.

Return at most one result or raise an exception.

Iterate through sub-lists of rows of the size given.

Fetch the first column of the first row, and close the result set.

Return exactly one scalar result or raise an exception.

Return exactly one scalar result or None.

Return an AsyncScalarResult filtering object which will return single elements rather than Row objects.

Apply a “typed tuple” typing filter to returned rows.

Apply unique filtering to the objects returned by this AsyncResult.

Configure the row-fetching strategy to fetch num rows at a time.

Return all rows in a list.

Closes the result set after invocation. Subsequent invocations will return an empty list.

a list of Row objects.

inherited from the AsyncCommon.close() method of AsyncCommon

proxies the .closed attribute of the underlying result object, if any, else raises AttributeError.

Added in version 2.0.0b3.

Establish the columns that should be returned in each row.

Refer to Result.columns() in the synchronous SQLAlchemy API for a complete behavioral description.

A synonym for the AsyncResult.all() method.

Added in version 2.0.

When all rows are exhausted, returns an empty list.

This method is provided for backwards compatibility with SQLAlchemy 1.x.x.

To fetch rows in groups, use the AsyncResult.partitions() method.

a list of Row objects.

AsyncResult.partitions()

When all rows are exhausted, returns None.

This method is provided for backwards compatibility with SQLAlchemy 1.x.x.

To fetch the first row of a result only, use the AsyncResult.first() method. To iterate through all rows, iterate the AsyncResult object directly.

a Row object if no filters are applied, or None if no rows remain.

Fetch the first row or None if no row is present.

Closes the result set and discards remaining rows.

This method returns one row, e.g. tuple, by default. To return exactly one single scalar value, that is, the first column of the first row, use the AsyncResult.scalar() method, or combine AsyncResult.scalars() and AsyncResult.first().

Additionally, in contrast to the behavior of the legacy ORM Query.first() method, no limit is applied to the SQL query which was invoked to produce this AsyncResult; for a DBAPI driver that buffers results in memory before yielding rows, all rows will be sent to the Python process and all but the first row will be discarded.

ORM Query Unified with Core Select

a Row object, or None if no rows remain.

Return a callable object that will produce copies of this AsyncResult when invoked.

The callable object returned is an instance of FrozenResult.

This is used for result set caching. The method must be called on the result when it has been unconsumed, and calling the method will consume the result fully. When the FrozenResult is retrieved from a cache, it can be called any number of times where it will produce a new Result object each time against its stored set of rows.

Re-Executing Statements - example usage within the ORM to implement a result-set cache.

inherited from the sqlalchemy.engine._WithKeys.keys method of sqlalchemy.engine._WithKeys

Return an iterable view which yields the string keys that would be represented by each Row.

The keys can represent the labels of the columns returned by a core statement or the names of the orm classes returned by an orm execution.

The view also can be tested for key containment using the Python in operator, which will test both for the string keys represented in the view, as well as for alternate keys such as column objects.

Changed in version 1.4: a key view object is returned rather than a plain list.

Apply a mappings filter to returned rows, returning an instance of AsyncMappingResult.

When this filter is applied, fetching rows will return RowMapping objects instead of Row objects.

a new AsyncMappingResult filtering object referring to the underlying Result object.

Return exactly one row or raise an exception.

Raises NoResultFound if the result returns no rows, or MultipleResultsFound if multiple rows would be returned.

This method returns one row, e.g. tuple, by default. To return exactly one single scalar value, that is, the first column of the first row, use the AsyncResult.scalar_one() method, or combine AsyncResult.scalars() and AsyncResult.one().

Added in version 1.4.

MultipleResultsFound, NoResultFound

AsyncResult.one_or_none()

AsyncResult.scalar_one()

Return at most one result or raise an exception.

Returns None if the result has no rows. Raises MultipleResultsFound if multiple rows are returned.

Added in version 1.4.

The first Row or None if no row is available.

Iterate through sub-lists of rows of the size given.

An async iterator is returned:

Refer to Result.partitions() in the synchronous SQLAlchemy API for a complete behavioral description.

Fetch the first column of the first row, and close the result set.

Returns None if there are no rows to fetch.

No validation is performed to test if additional rows remain.

After calling this method, the object is fully closed, e.g. the CursorResult.close() method will have been called.

a Python scalar value, or None if no rows remain.

Return exactly one scalar result or raise an exception.

This is equivalent to calling AsyncResult.scalars() and then AsyncScalarResult.one().

AsyncScalarResult.one()

AsyncResult.scalars()

Return exactly one scalar result or None.

This is equivalent to calling AsyncResult.scalars() and then AsyncScalarResult.one_or_none().

AsyncScalarResult.one_or_none()

AsyncResult.scalars()

Return an AsyncScalarResult filtering object which will return single elements rather than Row objects.

Refer to Result.scalars() in the synchronous SQLAlchemy API for a complete behavioral description.

index¶ – integer or row key indicating the column to be fetched from each row, defaults to 0 indicating the first column.

a new AsyncScalarResult filtering object referring to this AsyncResult object.

Apply a “typed tuple” typing filter to returned rows.

The AsyncResult.t attribute is a synonym for calling the AsyncResult.tuples() method.

Added in version 2.0.

Apply a “typed tuple” typing filter to returned rows.

This method returns the same AsyncResult object at runtime, however annotates as returning a AsyncTupleResult object that will indicate to PEP 484 typing tools that plain typed Tuple instances are returned rather than rows. This allows tuple unpacking and __getitem__ access of Row objects to by typed, for those cases where the statement invoked itself included typing information.

Added in version 2.0.

the AsyncTupleResult type at typing time.

AsyncResult.t - shorter synonym

Apply unique filtering to the objects returned by this AsyncResult.

Refer to Result.unique() in the synchronous SQLAlchemy API for a complete behavioral description.

inherited from the FilterResult.yield_per() method of FilterResult

Configure the row-fetching strategy to fetch num rows at a time.

The FilterResult.yield_per() method is a pass through to the Result.yield_per() method. See that method’s documentation for usage notes.

Added in version 1.4.40: - added FilterResult.yield_per() so that the method is available on all result set implementations

Using Server Side Cursors (a.k.a. stream results) - describes Core behavior for Result.yield_per()

Fetching Large Result Sets with Yield Per - in the ORM Querying Guide

inherits from sqlalchemy.ext.asyncio.AsyncCommon

A wrapper for a AsyncResult that returns scalar values rather than Row values.

The AsyncScalarResult object is acquired by calling the AsyncResult.scalars() method.

Refer to the ScalarResult object in the synchronous SQLAlchemy API for a complete behavioral description.

Added in version 1.4.

Return all scalar values in a list.

A synonym for the AsyncScalarResult.all() method.

Fetch the first object or None if no object is present.

Return exactly one object or raise an exception.

Return at most one object or raise an exception.

Iterate through sub-lists of elements of the size given.

Apply unique filtering to the objects returned by this AsyncScalarResult.

Configure the row-fetching strategy to fetch num rows at a time.

Return all scalar values in a list.

Equivalent to AsyncResult.all() except that scalar values, rather than Row objects, are returned.

inherited from the AsyncCommon.close() method of AsyncCommon

proxies the .closed attribute of the underlying result object, if any, else raises AttributeError.

Added in version 2.0.0b3.

A synonym for the AsyncScalarResult.all() method.

Equivalent to AsyncResult.fetchmany() except that scalar values, rather than Row objects, are returned.

Fetch the first object or None if no object is present.

Equivalent to AsyncResult.first() except that scalar values, rather than Row objects, are returned.

Return exactly one object or raise an exception.

Equivalent to AsyncResult.one() except that scalar values, rather than Row objects, are returned.

Return at most one object or raise an exception.

Equivalent to AsyncResult.one_or_none() except that scalar values, rather than Row objects, are returned.

Iterate through sub-lists of elements of the size given.

Equivalent to AsyncResult.partitions() except that scalar values, rather than Row objects, are returned.

Apply unique filtering to the objects returned by this AsyncScalarResult.

See AsyncResult.unique() for usage details.

inherited from the FilterResult.yield_per() method of FilterResult

Configure the row-fetching strategy to fetch num rows at a time.

The FilterResult.yield_per() method is a pass through to the Result.yield_per() method. See that method’s documentation for usage notes.

Added in version 1.4.40: - added FilterResult.yield_per() so that the method is available on all result set implementations

Using Server Side Cursors (a.k.a. stream results) - describes Core behavior for Result.yield_per()

Fetching Large Result Sets with Yield Per - in the ORM Querying Guide

inherits from sqlalchemy.engine._WithKeys, sqlalchemy.ext.asyncio.AsyncCommon

A wrapper for a AsyncResult that returns dictionary values rather than Row values.

The AsyncMappingResult object is acquired by calling the AsyncResult.mappings() method.

Refer to the MappingResult object in the synchronous SQLAlchemy API for a complete behavioral description.

Added in version 1.4.

Return all rows in a list.

Establish the columns that should be returned in each row.

A synonym for the AsyncMappingResult.all() method.

Fetch the first object or None if no object is present.

Return an iterable view which yields the string keys that would be represented by each Row.

Return exactly one object or raise an exception.

Return at most one object or raise an exception.

Iterate through sub-lists of elements of the size given.

Apply unique filtering to the objects returned by this AsyncMappingResult.

Configure the row-fetching strategy to fetch num rows at a time.

Return all rows in a list.

Equivalent to AsyncResult.all() except that RowMapping values, rather than Row objects, are returned.

inherited from the AsyncCommon.close() method of AsyncCommon

proxies the .closed attribute of the underlying result object, if any, else raises AttributeError.

Added in version 2.0.0b3.

Establish the columns that should be returned in each row.

A synonym for the AsyncMappingResult.all() method.

Equivalent to AsyncResult.fetchmany() except that RowMapping values, rather than Row objects, are returned.

Equivalent to AsyncResult.fetchone() except that RowMapping values, rather than Row objects, are returned.

Fetch the first object or None if no object is present.

Equivalent to AsyncResult.first() except that RowMapping values, rather than Row objects, are returned.

inherited from the sqlalchemy.engine._WithKeys.keys method of sqlalchemy.engine._WithKeys

Return an iterable view which yields the string keys that would be represented by each Row.

The keys can represent the labels of the columns returned by a core statement or the names of the orm classes returned by an orm execution.

The view also can be tested for key containment using the Python in operator, which will test both for the string keys represented in the view, as well as for alternate keys such as column objects.

Changed in version 1.4: a key view object is returned rather than a plain list.

Return exactly one object or raise an exception.

Equivalent to AsyncResult.one() except that RowMapping values, rather than Row objects, are returned.

Return at most one object or raise an exception.

Equivalent to AsyncResult.one_or_none() except that RowMapping values, rather than Row objects, are returned.

Iterate through sub-lists of elements of the size given.

Equivalent to AsyncResult.partitions() except that RowMapping values, rather than Row objects, are returned.

Apply unique filtering to the objects returned by this AsyncMappingResult.

See AsyncResult.unique() for usage details.

inherited from the FilterResult.yield_per() method of FilterResult

Configure the row-fetching strategy to fetch num rows at a time.

The FilterResult.yield_per() method is a pass through to the Result.yield_per() method. See that method’s documentation for usage notes.

Added in version 1.4.40: - added FilterResult.yield_per() so that the method is available on all result set implementations

Using Server Side Cursors (a.k.a. stream results) - describes Core behavior for Result.yield_per()

Fetching Large Result Sets with Yield Per - in the ORM Querying Guide

inherits from sqlalchemy.ext.asyncio.AsyncCommon, sqlalchemy.util.langhelpers.TypingOnly

A AsyncResult that’s typed as returning plain Python tuples instead of rows.

Since Row acts like a tuple in every way already, this class is a typing only class, regular AsyncResult is still used at runtime.

async_object_session(instance)

Return the AsyncSession to which the given instance belongs.

Provides scoped management of AsyncSession objects.

async_session(session)

Return the AsyncSession which is proxying the given Session object, if any.

A configurable AsyncSession factory.

Mixin class which provides an awaitable accessor for all attributes.

Asyncio version of Session.

AsyncSessionTransaction

A wrapper for the ORM SessionTransaction object.

Close all AsyncSession sessions.

Return the AsyncSession to which the given instance belongs.

This function makes use of the sync-API function object_session to retrieve the Session which refers to the given instance, and from there links it to the original AsyncSession.

If the AsyncSession has been garbage collected, the return value is None.

This functionality is also available from the InstanceState.async_session accessor.

instance¶ – an ORM mapped instance

an AsyncSession object, or None.

Added in version 1.4.18.

Return the AsyncSession which is proxying the given Session object, if any.

session¶ – a Session instance.

a AsyncSession instance, or None.

Added in version 1.4.18.

Close all AsyncSession sessions.

Added in version 2.0.23.

inherits from typing.Generic

A configurable AsyncSession factory.

The async_sessionmaker factory works in the same way as the sessionmaker factory, to generate new AsyncSession objects when called, creating them given the configurational arguments established here.

The async_sessionmaker is useful so that different parts of a program can create new AsyncSession objects with a fixed configuration established up front. Note that AsyncSession objects may also be instantiated directly when not using async_sessionmaker.

Added in version 2.0: async_sessionmaker provides a sessionmaker class that’s dedicated to the AsyncSession object, including pep-484 typing support.

Synopsis - ORM - shows example use

sessionmaker architecture

Opening and Closing a Session - introductory text on creating sessions using sessionmaker.

Produce a new AsyncSession object using the configuration established in this async_sessionmaker.

Construct a new async_sessionmaker.

Produce a context manager that both provides a new AsyncSession as well as a transaction that commits.

(Re)configure the arguments for this async_sessionmaker.

Produce a new AsyncSession object using the configuration established in this async_sessionmaker.

In Python, the __call__ method is invoked on an object when it is “called” in the same way as a function:

Construct a new async_sessionmaker.

All arguments here except for class_ correspond to arguments accepted by Session directly. See the AsyncSession.__init__() docstring for more details on parameters.

Produce a context manager that both provides a new AsyncSession as well as a transaction that commits.

(Re)configure the arguments for this async_sessionmaker.

inherits from typing.Generic

Provides scoped management of AsyncSession objects.

See the section Using asyncio scoped session for usage details.

Added in version 1.4.19.

Return the current AsyncSession, creating it using the scoped_session.session_factory if not present.

Construct a new async_scoped_session.

A synonym for AsyncSession.close().

Place an object into this Session.

Add the given collection of instances to this Session.

Return an AsyncSessionTransaction object.

Return an AsyncSessionTransaction object which will begin a “nested” transaction, e.g. SAVEPOINT.

Close out the transactional resources and ORM objects used by this AsyncSession.

Close all AsyncSession sessions.

Commit the current transaction in progress.

reconfigure the sessionmaker used by this scoped_session.

Return a AsyncConnection object corresponding to this Session object’s transactional state.

Mark an instance as deleted.

Execute a statement and return a buffered Result object.

Expire the attributes on an instance.

Expires all persistent instances within this Session.

Remove the instance from this Session.

Remove all object instances from this Session.

Flush all the object changes to the database.

Return an instance based on the given primary key identifier, or None if not found.

Return a “bind” to which the synchronous proxied Session is bound.

Return an instance based on the given primary key identifier, or raise an exception if not found.

Return an identity key.

Close this Session, using connection invalidation.

Return True if the given instance has locally modified attributes.

Copy the state of a given instance into a corresponding instance within this AsyncSession.

Return the Session to which an object belongs.

Expire and refresh the attributes on the given instance.

Dispose of the current AsyncSession, if present.

Close out the transactional resources and ORM objects used by this Session, resetting the session to its initial state.

Rollback the current transaction in progress.

Execute a statement and return a scalar result.

Execute a statement and return scalar results.

The session_factory provided to __init__ is stored in this attribute and may be accessed at a later time. This can be useful when a new non-scoped AsyncSession is needed.

Execute a statement and return a streaming AsyncResult object.

Execute a statement and return a stream of scalar results.

Return the current AsyncSession, creating it using the scoped_session.session_factory if not present.

**kw¶ – Keyword arguments will be passed to the scoped_session.session_factory callable, if an existing AsyncSession is not present. If the AsyncSession is present and keyword arguments have been passed, InvalidRequestError is raised.

Construct a new async_scoped_session.

session_factory¶ – a factory to create new AsyncSession instances. This is usually, but not necessarily, an instance of async_sessionmaker.

scopefunc¶ – function which defines the current scope. A function such as asyncio.current_task may be useful here.

A synonym for AsyncSession.close().

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

The AsyncSession.aclose() name is specifically to support the Python standard library @contextlib.aclosing context manager function.

Added in version 2.0.20.

Place an object into this Session.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Proxied for the Session class on behalf of the AsyncSession class.

Objects that are in the transient state when passed to the Session.add() method will move to the pending state, until the next flush, at which point they will move to the persistent state.

Objects that are in the detached state when passed to the Session.add() method will move to the persistent state directly.

If the transaction used by the Session is rolled back, objects which were transient when they were passed to Session.add() will be moved back to the transient state, and will no longer be present within this Session.

Adding New or Existing Items - at Basics of Using a Session

Add the given collection of instances to this Session.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Proxied for the Session class on behalf of the AsyncSession class.

See the documentation for Session.add() for a general behavioral description.

Adding New or Existing Items - at Basics of Using a Session

Proxy for the Session.autoflush attribute on behalf of the AsyncSession class.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Return an AsyncSessionTransaction object.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

The underlying Session will perform the “begin” action when the AsyncSessionTransaction object is entered:

Note that database IO will not normally occur when the session-level transaction is begun, as database transactions begin on an on-demand basis. However, the begin block is async to accommodate for a SessionEvents.after_transaction_create() event hook that may perform IO.

For a general description of ORM begin, see Session.begin().

Return an AsyncSessionTransaction object which will begin a “nested” transaction, e.g. SAVEPOINT.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Behavior is the same as that of AsyncSession.begin().

For a general description of ORM begin nested, see Session.begin_nested().

Serializable isolation / Savepoints / Transactional DDL (asyncio version) - special workarounds required with the SQLite asyncio driver in order for SAVEPOINT to work correctly.

Proxy for the AsyncSession.bind attribute on behalf of the async_scoped_session class.

Close out the transactional resources and ORM objects used by this AsyncSession.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Session.close() - main documentation for “close”

Closing - detail on the semantics of AsyncSession.close() and AsyncSession.reset().

Close all AsyncSession sessions.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Deprecated since version 2.0: The AsyncSession.close_all() method is deprecated and will be removed in a future release. Please refer to close_all_sessions().

Commit the current transaction in progress.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Session.commit() - main documentation for “commit”

reconfigure the sessionmaker used by this scoped_session.

See sessionmaker.configure().

Return a AsyncConnection object corresponding to this Session object’s transactional state.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

This method may also be used to establish execution options for the database connection used by the current transaction.

Added in version 1.4.24: Added **kw arguments which are passed through to the underlying Session.connection() method.

Session.connection() - main documentation for “connection”

Mark an instance as deleted.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

The database delete operation occurs upon flush().

As this operation may need to cascade along unloaded relationships, it is awaitable to allow for those queries to take place.

Session.delete() - main documentation for delete

The set of all instances marked as ‘deleted’ within this Session

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Proxied for the Session class on behalf of the AsyncSession class.

The set of all persistent instances considered dirty.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Proxied for the Session class on behalf of the AsyncSession class.

Instances are considered dirty when they were modified but not deleted.

Note that this ‘dirty’ calculation is ‘optimistic’; most attribute-setting or collection modification operations will mark an instance as ‘dirty’ and place it in this set, even if there is no net change to the attribute’s value. At flush time, the value of each attribute is compared to its previously saved value, and if there’s no net change, no SQL operation will occur (this is a more expensive operation so it’s only done at flush time).

To check if an instance has actionable net changes to its attributes, use the Session.is_modified() method.

Execute a statement and return a buffered Result object.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Session.execute() - main documentation for execute

Expire the attributes on an instance.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Proxied for the Session class on behalf of the AsyncSession class.

Marks the attributes of an instance as out of date. When an expired attribute is next accessed, a query will be issued to the Session object’s current transactional context in order to load all expired attributes for the given instance. Note that a highly isolated transaction will return the same values as were previously read in that same transaction, regardless of changes in database state outside of that transaction.

To expire all objects in the Session simultaneously, use Session.expire_all().

The Session object’s default behavior is to expire all state whenever the Session.rollback() or Session.commit() methods are called, so that new state can be loaded for the new transaction. For this reason, calling Session.expire() only makes sense for the specific case that a non-ORM SQL statement was emitted in the current transaction.

instance¶ – The instance to be refreshed.

attribute_names¶ – optional list of string attribute names indicating a subset of attributes to be expired.

Refreshing / Expiring - introductory material

Query.populate_existing()

Expires all persistent instances within this Session.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Proxied for the Session class on behalf of the AsyncSession class.

When any attributes on a persistent instance is next accessed, a query will be issued using the Session object’s current transactional context in order to load all expired attributes for the given instance. Note that a highly isolated transaction will return the same values as were previously read in that same transaction, regardless of changes in database state outside of that transaction.

To expire individual objects and individual attributes on those objects, use Session.expire().

The Session object’s default behavior is to expire all state whenever the Session.rollback() or Session.commit() methods are called, so that new state can be loaded for the new transaction. For this reason, calling Session.expire_all() is not usually needed, assuming the transaction is isolated.

Refreshing / Expiring - introductory material

Query.populate_existing()

Remove the instance from this Session.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Proxied for the Session class on behalf of the AsyncSession class.

This will free all internal references to the instance. Cascading will be applied according to the expunge cascade rule.

Remove all object instances from this Session.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Proxied for the Session class on behalf of the AsyncSession class.

This is equivalent to calling expunge(obj) on all objects in this Session.

Flush all the object changes to the database.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Session.flush() - main documentation for flush

Return an instance based on the given primary key identifier, or None if not found.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Session.get() - main documentation for get

Return a “bind” to which the synchronous proxied Session is bound.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Unlike the Session.get_bind() method, this method is currently not used by this AsyncSession in any way in order to resolve engines for requests.

This method proxies directly to the Session.get_bind() method, however is currently not useful as an override target, in contrast to that of the Session.get_bind() method. The example below illustrates how to implement custom Session.get_bind() schemes that work with AsyncSession and AsyncEngine.

The pattern introduced at Custom Vertical Partitioning illustrates how to apply a custom bind-lookup scheme to a Session given a set of Engine objects. To apply a corresponding Session.get_bind() implementation for use with a AsyncSession and AsyncEngine objects, continue to subclass Session and apply it to AsyncSession using AsyncSession.sync_session_class. The inner method must continue to return Engine instances, which can be acquired from a AsyncEngine using the AsyncEngine.sync_engine attribute:

The Session.get_bind() method is called in a non-asyncio, implicitly non-blocking context in the same manner as ORM event hooks and functions that are invoked via AsyncSession.run_sync(), so routines that wish to run SQL commands inside of Session.get_bind() can continue to do so using blocking-style code, which will be translated to implicitly async calls at the point of invoking IO on the database drivers.

Return an instance based on the given primary key identifier, or raise an exception if not found.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Raises NoResultFound if the query selects no rows.

..versionadded: 2.0.22

Session.get_one() - main documentation for get_one

Return an identity key.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Proxied for the Session class on behalf of the AsyncSession class.

This is an alias of identity_key().

Proxy for the Session.identity_map attribute on behalf of the AsyncSession class.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

A user-modifiable dictionary.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Proxied for the Session class on behalf of the AsyncSession class.

The initial value of this dictionary can be populated using the info argument to the Session constructor or sessionmaker constructor or factory methods. The dictionary here is always local to this Session and can be modified independently of all other Session objects.

Close this Session, using connection invalidation.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

For a complete description, see Session.invalidate().

True if this Session not in “partial rollback” state.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Proxied for the Session class on behalf of the AsyncSession class.

Changed in version 1.4: The Session no longer begins a new transaction immediately, so this attribute will be False when the Session is first instantiated.

“partial rollback” state typically indicates that the flush process of the Session has failed, and that the Session.rollback() method must be emitted in order to fully roll back the transaction.

If this Session is not in a transaction at all, the Session will autobegin when it is first used, so in this case Session.is_active will return True.

Otherwise, if this Session is within a transaction, and that transaction has not been rolled back internally, the Session.is_active will also return True.

“This Session’s transaction has been rolled back due to a previous exception during flush.” (or similar)

Session.in_transaction()

Return True if the given instance has locally modified attributes.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Proxied for the Session class on behalf of the AsyncSession class.

This method retrieves the history for each instrumented attribute on the instance and performs a comparison of the current value to its previously flushed or committed value, if any.

It is in effect a more expensive and accurate version of checking for the given instance in the Session.dirty collection; a full test for each attribute’s net “dirty” status is performed.

A few caveats to this method apply:

Instances present in the Session.dirty collection may report False when tested with this method. This is because the object may have received change events via attribute mutation, thus placing it in Session.dirty, but ultimately the state is the same as that loaded from the database, resulting in no net change here.

Scalar attributes may not have recorded the previously set value when a new value was applied, if the attribute was not loaded, or was expired, at the time the new value was received - in these cases, the attribute is assumed to have a change, even if there is ultimately no net change against its database value. SQLAlchemy in most cases does not need the “old” value when a set event occurs, so it skips the expense of a SQL call if the old value isn’t present, based on the assumption that an UPDATE of the scalar value is usually needed, and in those few cases where it isn’t, is less expensive on average than issuing a defensive SELECT.

The “old” value is fetched unconditionally upon set only if the attribute container has the active_history flag set to True. This flag is set typically for primary key attributes and scalar object references that are not a simple many-to-one. To set this flag for any arbitrary mapped column, use the active_history argument with column_property().

instance¶ – mapped instance to be tested for pending changes.

include_collections¶ – Indicates if multivalued collections should be included in the operation. Setting this to False is a way to detect only local-column based properties (i.e. scalar columns or many-to-one foreign keys) that would result in an UPDATE for this instance upon flush.

Copy the state of a given instance into a corresponding instance within this AsyncSession.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Session.merge() - main documentation for merge

The set of all instances marked as ‘new’ within this Session.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Proxied for the Session class on behalf of the AsyncSession class.

Return a context manager that disables autoflush.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Proxied for the Session class on behalf of the AsyncSession class.

Operations that proceed within the with: block will not be subject to flushes occurring upon query access. This is useful when initializing a series of objects which involve existing database queries, where the uncompleted object should not yet be flushed.

Return the Session to which an object belongs.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Proxied for the Session class on behalf of the AsyncSession class.

This is an alias of object_session().

Expire and refresh the attributes on the given instance.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

A query will be issued to the database and all attributes will be refreshed with their current database value.

This is the async version of the Session.refresh() method. See that method for a complete description of all options.

Session.refresh() - main documentation for refresh

Dispose of the current AsyncSession, if present.

Different from scoped_session’s remove method, this method would use await to wait for the close method of AsyncSession.

Close out the transactional resources and ORM objects used by this Session, resetting the session to its initial state.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Added in version 2.0.22.

Session.reset() - main documentation for “reset”

Closing - detail on the semantics of AsyncSession.close() and AsyncSession.reset().

Rollback the current transaction in progress.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Session.rollback() - main documentation for “rollback”

Execute a statement and return a scalar result.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Session.scalar() - main documentation for scalar

Execute a statement and return scalar results.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

a ScalarResult object

Added in version 1.4.24: Added AsyncSession.scalars()

Added in version 1.4.26: Added async_scoped_session.scalars()

Session.scalars() - main documentation for scalars

AsyncSession.stream_scalars() - streaming version

The session_factory provided to __init__ is stored in this attribute and may be accessed at a later time. This can be useful when a new non-scoped AsyncSession is needed.

Execute a statement and return a streaming AsyncResult object.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

Execute a statement and return a stream of scalar results.

Proxied for the AsyncSession class on behalf of the async_scoped_session class.

an AsyncScalarResult object

Added in version 1.4.24.

Session.scalars() - main documentation for scalars

AsyncSession.scalars() - non streaming version

Mixin class which provides an awaitable accessor for all attributes.

In the above example, the AsyncAttrs mixin is applied to the declarative Base class where it takes effect for all subclasses. This mixin adds a single new attribute AsyncAttrs.awaitable_attrs to all classes, which will yield the value of any attribute as an awaitable. This allows attributes which may be subject to lazy loading or deferred / unexpiry loading to be accessed such that IO can still be emitted:

The AsyncAttrs.awaitable_attrs performs a call against the attribute that is approximately equivalent to using the AsyncSession.run_sync() method, e.g.:

Added in version 2.0.13.

Preventing Implicit IO when Using AsyncSession

provide a namespace of all attributes on this object wrapped as awaitables.

inherits from sqlalchemy.ext.asyncio.base.ReversibleProxy

Asyncio version of Session.

The AsyncSession is a proxy for a traditional Session instance.

The AsyncSession is not safe for use in concurrent tasks.. See Is the Session thread-safe? Is AsyncSession safe to share in concurrent tasks? for background.

Added in version 1.4.

To use an AsyncSession with custom Session implementations, see the AsyncSession.sync_session_class parameter.

Construct a new AsyncSession.

A synonym for AsyncSession.close().

Place an object into this Session.

Add the given collection of instances to this Session.

Return an AsyncSessionTransaction object.

Return an AsyncSessionTransaction object which will begin a “nested” transaction, e.g. SAVEPOINT.

Close out the transactional resources and ORM objects used by this AsyncSession.

Close all AsyncSession sessions.

Commit the current transaction in progress.

Return a AsyncConnection object corresponding to this Session object’s transactional state.

Mark an instance as deleted.

Execute a statement and return a buffered Result object.

Expire the attributes on an instance.

Expires all persistent instances within this Session.

Remove the instance from this Session.

Remove all object instances from this Session.

Flush all the object changes to the database.

Return an instance based on the given primary key identifier, or None if not found.

Return a “bind” to which the synchronous proxied Session is bound.

get_nested_transaction()

Return the current nested transaction in progress, if any.

Return an instance based on the given primary key identifier, or raise an exception if not found.

Return the current root transaction in progress, if any.

Return an identity key.

in_nested_transaction()

Return True if this Session has begun a nested transaction, e.g. SAVEPOINT.

Return True if this Session has begun a transaction.

Close this Session, using connection invalidation.

Return True if the given instance has locally modified attributes.

Copy the state of a given instance into a corresponding instance within this AsyncSession.

Return the Session to which an object belongs.

Expire and refresh the attributes on the given instance.

Close out the transactional resources and ORM objects used by this Session, resetting the session to its initial state.

Rollback the current transaction in progress.

Invoke the given synchronous (i.e. not async) callable, passing a synchronous-style Session as the first argument.

Execute a statement and return a scalar result.

Execute a statement and return scalar results.

Execute a statement and return a streaming AsyncResult object.

Execute a statement and return a stream of scalar results.

Reference to the underlying Session this AsyncSession proxies requests towards.

The class or callable that provides the underlying Session instance for a particular AsyncSession.

Construct a new AsyncSession.

All parameters other than sync_session_class are passed to the sync_session_class callable directly to instantiate a new Session. Refer to Session.__init__() for parameter documentation.

sync_session_class¶ –

A Session subclass or other callable which will be used to construct the Session which will be proxied. This parameter may be used to provide custom Session subclasses. Defaults to the AsyncSession.sync_session_class class-level attribute.

Added in version 1.4.24.

A synonym for AsyncSession.close().

The AsyncSession.aclose() name is specifically to support the Python standard library @contextlib.aclosing context manager function.

Added in version 2.0.20.

Place an object into this Session.

Proxied for the Session class on behalf of the AsyncSession class.

Objects that are in the transient state when passed to the Session.add() method will move to the pending state, until the next flush, at which point they will move to the persistent state.

Objects that are in the detached state when passed to the Session.add() method will move to the persistent state directly.

If the transaction used by the Session is rolled back, objects which were transient when they were passed to Session.add() will be moved back to the transient state, and will no longer be present within this Session.

Adding New or Existing Items - at Basics of Using a Session

Add the given collection of instances to this Session.

Proxied for the Session class on behalf of the AsyncSession class.

See the documentation for Session.add() for a general behavioral description.

Adding New or Existing Items - at Basics of Using a Session

Proxy for the Session.autoflush attribute on behalf of the AsyncSession class.

Return an AsyncSessionTransaction object.

The underlying Session will perform the “begin” action when the AsyncSessionTransaction object is entered:

Note that database IO will not normally occur when the session-level transaction is begun, as database transactions begin on an on-demand basis. However, the begin block is async to accommodate for a SessionEvents.after_transaction_create() event hook that may perform IO.

For a general description of ORM begin, see Session.begin().

Return an AsyncSessionTransaction object which will begin a “nested” transaction, e.g. SAVEPOINT.

Behavior is the same as that of AsyncSession.begin().

For a general description of ORM begin nested, see Session.begin_nested().

Serializable isolation / Savepoints / Transactional DDL (asyncio version) - special workarounds required with the SQLite asyncio driver in order for SAVEPOINT to work correctly.

Close out the transactional resources and ORM objects used by this AsyncSession.

Session.close() - main documentation for “close”

Closing - detail on the semantics of AsyncSession.close() and AsyncSession.reset().

Close all AsyncSession sessions.

Deprecated since version 2.0: The AsyncSession.close_all() method is deprecated and will be removed in a future release. Please refer to close_all_sessions().

Commit the current transaction in progress.

Session.commit() - main documentation for “commit”

Return a AsyncConnection object corresponding to this Session object’s transactional state.

This method may also be used to establish execution options for the database connection used by the current transaction.

Added in version 1.4.24: Added **kw arguments which are passed through to the underlying Session.connection() method.

Session.connection() - main documentation for “connection”

Mark an instance as deleted.

The database delete operation occurs upon flush().

As this operation may need to cascade along unloaded relationships, it is awaitable to allow for those queries to take place.

Session.delete() - main documentation for delete

The set of all instances marked as ‘deleted’ within this Session

Proxied for the Session class on behalf of the AsyncSession class.

The set of all persistent instances considered dirty.

Proxied for the Session class on behalf of the AsyncSession class.

Instances are considered dirty when they were modified but not deleted.

Note that this ‘dirty’ calculation is ‘optimistic’; most attribute-setting or collection modification operations will mark an instance as ‘dirty’ and place it in this set, even if there is no net change to the attribute’s value. At flush time, the value of each attribute is compared to its previously saved value, and if there’s no net change, no SQL operation will occur (this is a more expensive operation so it’s only done at flush time).

To check if an instance has actionable net changes to its attributes, use the Session.is_modified() method.

Execute a statement and return a buffered Result object.

Session.execute() - main documentation for execute

Expire the attributes on an instance.

Proxied for the Session class on behalf of the AsyncSession class.

Marks the attributes of an instance as out of date. When an expired attribute is next accessed, a query will be issued to the Session object’s current transactional context in order to load all expired attributes for the given instance. Note that a highly isolated transaction will return the same values as were previously read in that same transaction, regardless of changes in database state outside of that transaction.

To expire all objects in the Session simultaneously, use Session.expire_all().

The Session object’s default behavior is to expire all state whenever the Session.rollback() or Session.commit() methods are called, so that new state can be loaded for the new transaction. For this reason, calling Session.expire() only makes sense for the specific case that a non-ORM SQL statement was emitted in the current transaction.

instance¶ – The instance to be refreshed.

attribute_names¶ – optional list of string attribute names indicating a subset of attributes to be expired.

Refreshing / Expiring - introductory material

Query.populate_existing()

Expires all persistent instances within this Session.

Proxied for the Session class on behalf of the AsyncSession class.

When any attributes on a persistent instance is next accessed, a query will be issued using the Session object’s current transactional context in order to load all expired attributes for the given instance. Note that a highly isolated transaction will return the same values as were previously read in that same transaction, regardless of changes in database state outside of that transaction.

To expire individual objects and individual attributes on those objects, use Session.expire().

The Session object’s default behavior is to expire all state whenever the Session.rollback() or Session.commit() methods are called, so that new state can be loaded for the new transaction. For this reason, calling Session.expire_all() is not usually needed, assuming the transaction is isolated.

Refreshing / Expiring - introductory material

Query.populate_existing()

Remove the instance from this Session.

Proxied for the Session class on behalf of the AsyncSession class.

This will free all internal references to the instance. Cascading will be applied according to the expunge cascade rule.

Remove all object instances from this Session.

Proxied for the Session class on behalf of the AsyncSession class.

This is equivalent to calling expunge(obj) on all objects in this Session.

Flush all the object changes to the database.

Session.flush() - main documentation for flush

Return an instance based on the given primary key identifier, or None if not found.

Session.get() - main documentation for get

Return a “bind” to which the synchronous proxied Session is bound.

Unlike the Session.get_bind() method, this method is currently not used by this AsyncSession in any way in order to resolve engines for requests.

This method proxies directly to the Session.get_bind() method, however is currently not useful as an override target, in contrast to that of the Session.get_bind() method. The example below illustrates how to implement custom Session.get_bind() schemes that work with AsyncSession and AsyncEngine.

The pattern introduced at Custom Vertical Partitioning illustrates how to apply a custom bind-lookup scheme to a Session given a set of Engine objects. To apply a corresponding Session.get_bind() implementation for use with a AsyncSession and AsyncEngine objects, continue to subclass Session and apply it to AsyncSession using AsyncSession.sync_session_class. The inner method must continue to return Engine instances, which can be acquired from a AsyncEngine using the AsyncEngine.sync_engine attribute:

The Session.get_bind() method is called in a non-asyncio, implicitly non-blocking context in the same manner as ORM event hooks and functions that are invoked via AsyncSession.run_sync(), so routines that wish to run SQL commands inside of Session.get_bind() can continue to do so using blocking-style code, which will be translated to implicitly async calls at the point of invoking IO on the database drivers.

Return the current nested transaction in progress, if any.

an AsyncSessionTransaction object, or None.

Added in version 1.4.18.

Return an instance based on the given primary key identifier, or raise an exception if not found.

Raises NoResultFound if the query selects no rows.

..versionadded: 2.0.22

Session.get_one() - main documentation for get_one

Return the current root transaction in progress, if any.

an AsyncSessionTransaction object, or None.

Added in version 1.4.18.

Return an identity key.

Proxied for the Session class on behalf of the AsyncSession class.

This is an alias of identity_key().

Proxy for the Session.identity_map attribute on behalf of the AsyncSession class.

Return True if this Session has begun a nested transaction, e.g. SAVEPOINT.

Proxied for the Session class on behalf of the AsyncSession class.

Added in version 1.4.

Return True if this Session has begun a transaction.

Proxied for the Session class on behalf of the AsyncSession class.

Added in version 1.4.

A user-modifiable dictionary.

Proxied for the Session class on behalf of the AsyncSession class.

The initial value of this dictionary can be populated using the info argument to the Session constructor or sessionmaker constructor or factory methods. The dictionary here is always local to this Session and can be modified independently of all other Session objects.

Close this Session, using connection invalidation.

For a complete description, see Session.invalidate().

True if this Session not in “partial rollback” state.

Proxied for the Session class on behalf of the AsyncSession class.

Changed in version 1.4: The Session no longer begins a new transaction immediately, so this attribute will be False when the Session is first instantiated.

“partial rollback” state typically indicates that the flush process of the Session has failed, and that the Session.rollback() method must be emitted in order to fully roll back the transaction.

If this Session is not in a transaction at all, the Session will autobegin when it is first used, so in this case Session.is_active will return True.

Otherwise, if this Session is within a transaction, and that transaction has not been rolled back internally, the Session.is_active will also return True.

“This Session’s transaction has been rolled back due to a previous exception during flush.” (or similar)

Session.in_transaction()

Return True if the given instance has locally modified attributes.

Proxied for the Session class on behalf of the AsyncSession class.

This method retrieves the history for each instrumented attribute on the instance and performs a comparison of the current value to its previously flushed or committed value, if any.

It is in effect a more expensive and accurate version of checking for the given instance in the Session.dirty collection; a full test for each attribute’s net “dirty” status is performed.

A few caveats to this method apply:

Instances present in the Session.dirty collection may report False when tested with this method. This is because the object may have received change events via attribute mutation, thus placing it in Session.dirty, but ultimately the state is the same as that loaded from the database, resulting in no net change here.

Scalar attributes may not have recorded the previously set value when a new value was applied, if the attribute was not loaded, or was expired, at the time the new value was received - in these cases, the attribute is assumed to have a change, even if there is ultimately no net change against its database value. SQLAlchemy in most cases does not need the “old” value when a set event occurs, so it skips the expense of a SQL call if the old value isn’t present, based on the assumption that an UPDATE of the scalar value is usually needed, and in those few cases where it isn’t, is less expensive on average than issuing a defensive SELECT.

The “old” value is fetched unconditionally upon set only if the attribute container has the active_history flag set to True. This flag is set typically for primary key attributes and scalar object references that are not a simple many-to-one. To set this flag for any arbitrary mapped column, use the active_history argument with column_property().

instance¶ – mapped instance to be tested for pending changes.

include_collections¶ – Indicates if multivalued collections should be included in the operation. Setting this to False is a way to detect only local-column based properties (i.e. scalar columns or many-to-one foreign keys) that would result in an UPDATE for this instance upon flush.

Copy the state of a given instance into a corresponding instance within this AsyncSession.

Session.merge() - main documentation for merge

The set of all instances marked as ‘new’ within this Session.

Proxied for the Session class on behalf of the AsyncSession class.

Return a context manager that disables autoflush.

Proxied for the Session class on behalf of the AsyncSession class.

Operations that proceed within the with: block will not be subject to flushes occurring upon query access. This is useful when initializing a series of objects which involve existing database queries, where the uncompleted object should not yet be flushed.

Return the Session to which an object belongs.

Proxied for the Session class on behalf of the AsyncSession class.

This is an alias of object_session().

Expire and refresh the attributes on the given instance.

A query will be issued to the database and all attributes will be refreshed with their current database value.

This is the async version of the Session.refresh() method. See that method for a complete description of all options.

Session.refresh() - main documentation for refresh

Close out the transactional resources and ORM objects used by this Session, resetting the session to its initial state.

Added in version 2.0.22.

Session.reset() - main documentation for “reset”

Closing - detail on the semantics of AsyncSession.close() and AsyncSession.reset().

Rollback the current transaction in progress.

Session.rollback() - main documentation for “rollback”

Invoke the given synchronous (i.e. not async) callable, passing a synchronous-style Session as the first argument.

This method allows traditional synchronous SQLAlchemy functions to run within the context of an asyncio application.

This method maintains the asyncio event loop all the way through to the database connection by running the given callable in a specially instrumented greenlet.

The provided callable is invoked inline within the asyncio event loop, and will block on traditional IO calls. IO within this callable should only call into SQLAlchemy’s asyncio database APIs which will be properly adapted to the greenlet context.

AsyncAttrs - a mixin for ORM mapped classes that provides a similar feature more succinctly on a per-attribute basis

AsyncConnection.run_sync()

Running Synchronous Methods and Functions under asyncio

Execute a statement and return a scalar result.

Session.scalar() - main documentation for scalar

Execute a statement and return scalar results.

a ScalarResult object

Added in version 1.4.24: Added AsyncSession.scalars()

Added in version 1.4.26: Added async_scoped_session.scalars()

Session.scalars() - main documentation for scalars

AsyncSession.stream_scalars() - streaming version

Execute a statement and return a streaming AsyncResult object.

Execute a statement and return a stream of scalar results.

an AsyncScalarResult object

Added in version 1.4.24.

Session.scalars() - main documentation for scalars

AsyncSession.scalars() - non streaming version

Reference to the underlying Session this AsyncSession proxies requests towards.

This instance can be used as an event target.

Using events with the asyncio extension

The class or callable that provides the underlying Session instance for a particular AsyncSession.

At the class level, this attribute is the default value for the AsyncSession.sync_session_class parameter. Custom subclasses of AsyncSession can override this.

At the instance level, this attribute indicates the current class or callable that was used to provide the Session instance for this AsyncSession instance.

Added in version 1.4.24.

inherits from sqlalchemy.ext.asyncio.base.ReversibleProxy, sqlalchemy.ext.asyncio.base.StartableContext

A wrapper for the ORM SessionTransaction object.

This object is provided so that a transaction-holding object for the AsyncSession.begin() may be returned.

The object supports both explicit calls to AsyncSessionTransaction.commit() and AsyncSessionTransaction.rollback(), as well as use as an async context manager.

Added in version 1.4.

Commit this AsyncTransaction.

Roll back this AsyncTransaction.

Commit this AsyncTransaction.

Roll back this AsyncTransaction.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (unknown):
```unknown
x86_64 aarch64 ppc64le amd64 win32
```

Example 2 (unknown):
```unknown
pip install sqlalchemy[asyncio]
```

Example 3 (python):
```python
>>> import asyncio

>>> from sqlalchemy import Column
>>> from sqlalchemy import MetaData
>>> from sqlalchemy import select
>>> from sqlalchemy import String
>>> from sqlalchemy import Table
>>> from sqlalchemy.ext.asyncio import create_async_engine

>>> meta = MetaData()
>>> t1 = Table("t1", meta, Column("name", String(50), primary_key=True))


>>> async def async_main() -> None:
...     engine = create_async_engine("sqlite+aiosqlite://", echo=True)
...
...     async with engine.begin() as conn:
...         await conn.run_sync(meta.drop_all)
...         await conn.run_sync(meta.create_all)
...
...         await conn.execute(
...             t1.insert(), [{"name": "some name 1"}, {"name": "some name 2"}]
...         )
...
...     async with engine.connect() as conn:
...         # select a Result, which will be delivered with buffered
...         # results
...         result = await conn.execute(select(t1).where(t1.c.name == "some name 1"))
...
...         print(result.fetchall())
...
...     # for AsyncEngine created in function scope, close and
...     # clean-up pooled connections
...     await engine.dispose()


>>> asyncio.run(async_main())
BEGIN (implicit)
...
CREATE TABLE t1 (
    name VARCHAR(50) NOT NULL,
    PRIMARY KEY (name)
)
...
INSERT INTO t1 (name) VALUES (?)
[...] [('some name 1',), ('some name 2',)]
COMMIT
BEGIN (implicit)
SELECT t1.name
FROM t1
WHERE t1.name = ?
[...] ('some name 1',)
[('some name 1',)]
ROLLBACK
```

Example 4 (typescript):
```typescript
async with engine.connect() as conn:
    async_result = await conn.stream(select(t1))

    async for row in async_result:
        print("row: %s" % (row,))
```

---
