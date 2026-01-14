# Sqlalchemy - Tutorial

**Pages:** 19

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/tutorial/data.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Unified Tutorial
    - Project Versions
- Working with Data¶

Home | Download this Documentation

Home | Download this Documentation

SQLAlchemy 1.4 / 2.0 Tutorial

This page is part of the SQLAlchemy Unified Tutorial.

Previous: Working with Database Metadata | Next: Using INSERT Statements

In Working with Transactions and the DBAPI, we learned the basics of how to interact with the Python DBAPI and its transactional state. Then, in Working with Database Metadata, we learned how to represent database tables, columns, and constraints within SQLAlchemy using the MetaData and related objects. In this section we will combine both concepts above to create, select and manipulate data within a relational database. Our interaction with the database is always in terms of a transaction, even if we’ve set our database driver to use autocommit behind the scenes.

The components of this section are as follows:

Using INSERT Statements - to get some data into the database, we introduce and demonstrate the Core Insert construct. INSERTs from an ORM perspective are described in the next section Data Manipulation with the ORM.

Using SELECT Statements - this section will describe in detail the Select construct, which is the most commonly used object in SQLAlchemy. The Select construct emits SELECT statements for both Core and ORM centric applications and both use cases will be described here. Additional ORM use cases are also noted in the later section Using Relationships in Queries as well as the ORM Querying Guide.

Using UPDATE and DELETE Statements - Rounding out the INSERT and SELECTion of data, this section will describe from a Core perspective the use of the Update and Delete constructs. ORM-specific UPDATE and DELETE is similarly described in the Data Manipulation with the ORM section.

SQLAlchemy 1.4 / 2.0 Tutorial

Next Tutorial Section: Using INSERT Statements

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Unified Tutorial
    - Project Versions
- Working with ORM Related Objects¶
- Persisting and Loading Relationships¶
  - Cascading Objects into the Session¶
- Loading Relationships¶
- Using Relationships in Queries¶
  - Using Relationships to Join¶

Home | Download this Documentation

Home | Download this Documentation

SQLAlchemy 1.4 / 2.0 Tutorial

This page is part of the SQLAlchemy Unified Tutorial.

Previous: Data Manipulation with the ORM | Next: Further Reading

In this section, we will cover one more essential ORM concept, which is how the ORM interacts with mapped classes that refer to other objects. In the section Declaring Mapped Classes, the mapped class examples made use of a construct called relationship(). This construct defines a linkage between two different mapped classes, or from a mapped class to itself, the latter of which is called a self-referential relationship.

To describe the basic idea of relationship(), first we’ll review the mapping in short form, omitting the mapped_column() mappings and other directives:

Above, the User class now has an attribute User.addresses and the Address class has an attribute Address.user. The relationship() construct, in conjunction with the Mapped construct to indicate typing behavior, will be used to inspect the table relationships between the Table objects that are mapped to the User and Address classes. As the Table object representing the address table has a ForeignKeyConstraint which refers to the user_account table, the relationship() can determine unambiguously that there is a one to many relationship from the User class to the Address class, along the User.addresses relationship; one particular row in the user_account table may be referenced by many rows in the address table.

All one-to-many relationships naturally correspond to a many to one relationship in the other direction, in this case the one noted by Address.user. The relationship.back_populates parameter, seen above configured on both relationship() objects referring to the other name, establishes that each of these two relationship() constructs should be considered to be complimentary to each other; we will see how this plays out in the next section.

We can start by illustrating what relationship() does to instances of objects. If we make a new User object, we can note that there is a Python list when we access the .addresses element:

This object is a SQLAlchemy-specific version of Python list which has the ability to track and respond to changes made to it. The collection also appeared automatically when we accessed the attribute, even though we never assigned it to the object. This is similar to the behavior noted at Inserting Rows using the ORM Unit of Work pattern where it was observed that column-based attributes to which we don’t explicitly assign a value also display as None automatically, rather than raising an AttributeError as would be Python’s usual behavior.

As the u1 object is still transient and the list that we got from u1.addresses has not been mutated (i.e. appended or extended), it’s not actually associated with the object yet, but as we make changes to it, it will become part of the state of the User object.

The collection is specific to the Address class which is the only type of Python object that may be persisted within it. Using the list.append() method we may add an Address object:

At this point, the u1.addresses collection as expected contains the new Address object:

As we associated the Address object with the User.addresses collection of the u1 instance, another behavior also occurred, which is that the User.addresses relationship synchronized itself with the Address.user relationship, such that we can navigate not only from the User object to the Address object, we can also navigate from the Address object back to the “parent” User object:

This synchronization occurred as a result of our use of the relationship.back_populates parameter between the two relationship() objects. This parameter names another relationship() for which complementary attribute assignment / list mutation should occur. It will work equally well in the other direction, which is that if we create another Address object and assign to its Address.user attribute, that Address becomes part of the User.addresses collection on that User object:

We actually made use of the user parameter as a keyword argument in the Address constructor, which is accepted just like any other mapped attribute that was declared on the Address class. It is equivalent to assignment of the Address.user attribute after the fact:

We now have a User and two Address objects that are associated in a bidirectional structure in memory, but as noted previously in Inserting Rows using the ORM Unit of Work pattern , these objects are said to be in the transient state until they are associated with a Session object.

We make use of the Session that’s still ongoing, and note that when we apply the Session.add() method to the lead User object, the related Address object also gets added to that same Session:

The above behavior, where the Session received a User object, and followed along the User.addresses relationship to locate a related Address object, is known as the save-update cascade and is discussed in detail in the ORM reference documentation at Cascades.

The three objects are now in the pending state; this means they are ready to be the subject of an INSERT operation but this has not yet proceeded; all three objects have no primary key assigned yet, and in addition, the a1 and a2 objects have an attribute called user_id which refers to the Column that has a ForeignKeyConstraint referring to the user_account.id column; these are also None as the objects are not yet associated with a real database row:

It’s at this stage that we can see the very great utility that the unit of work process provides; recall in the section INSERT usually generates the “values” clause automatically, rows were inserted into the user_account and address tables using some elaborate syntaxes in order to automatically associate the address.user_id columns with those of the user_account rows. Additionally, it was necessary that we emit INSERT for user_account rows first, before those of address, since rows in address are dependent on their parent row in user_account for a value in their user_id column.

When using the Session, all this tedium is handled for us and even the most die-hard SQL purist can benefit from automation of INSERT, UPDATE and DELETE statements. When we Session.commit() the transaction all steps invoke in the correct order, and furthermore the newly generated primary key of the user_account row is applied to the address.user_id column appropriately:

In the last step, we called Session.commit() which emitted a COMMIT for the transaction, and then per Session.commit.expire_on_commit expired all objects so that they refresh for the next transaction.

When we next access an attribute on these objects, we’ll see the SELECT emitted for the primary attributes of the row, such as when we view the newly generated primary key for the u1 object:

The u1 User object now has a persistent collection User.addresses that we may also access. As this collection consists of an additional set of rows from the address table, when we access this collection as well we again see a lazy load emitted in order to retrieve the objects:

Collections and related attributes in the SQLAlchemy ORM are persistent in memory; once the collection or attribute is populated, SQL is no longer emitted until that collection or attribute is expired. We may access u1.addresses again as well as add or remove items and this will not incur any new SQL calls:

While the loading emitted by lazy loading can quickly become expensive if we don’t take explicit steps to optimize it, the network of lazy loading at least is fairly well optimized to not perform redundant work; as the u1.addresses collection was refreshed, per the identity map these are in fact the same Address instances as the a1 and a2 objects we’ve been dealing with already, so we’re done loading all attributes in this particular object graph:

The issue of how relationships load, or not, is an entire subject onto itself. Some additional introduction to these concepts is later in this section at Loader Strategies.

The previous section introduced the behavior of the relationship() construct when working with instances of a mapped class, above, the u1, a1 and a2 instances of the User and Address classes. In this section, we introduce the behavior of relationship() as it applies to class level behavior of a mapped class, where it serves in several ways to help automate the construction of SQL queries.

The sections Explicit FROM clauses and JOINs and Setting the ON Clause introduced the usage of the Select.join() and Select.join_from() methods to compose SQL JOIN clauses. In order to describe how to join between tables, these methods either infer the ON clause based on the presence of a single unambiguous ForeignKeyConstraint object within the table metadata structure that links the two tables, or otherwise we may provide an explicit SQL Expression construct that indicates a specific ON clause.

When using ORM entities, an additional mechanism is available to help us set up the ON clause of a join, which is to make use of the relationship() objects that we set up in our user mapping, as was demonstrated at Declaring Mapped Classes. The class-bound attribute corresponding to the relationship() may be passed as the single argument to Select.join(), where it serves to indicate both the right side of the join as well as the ON clause at once:

The presence of an ORM relationship() on a mapping is not used by Select.join() or Select.join_from() to infer the ON clause if we don’t specify it. This means, if we join from User to Address without an ON clause, it works because of the ForeignKeyConstraint between the two mapped Table objects, not because of the relationship() objects on the User and Address classes:

See the section Joins in the ORM Querying Guide for many more examples of how to use Select.join() and Select.join_from() with relationship() constructs.

Joins in the ORM Querying Guide

There are some additional varieties of SQL generation helpers that come with relationship() which are typically useful when building up the WHERE clause of a statement. See the section Relationship WHERE Operators in the ORM Querying Guide.

Relationship WHERE Operators in the ORM Querying Guide

In the section Loading Relationships we introduced the concept that when we work with instances of mapped objects, accessing the attributes that are mapped using relationship() in the default case will emit a lazy load when the collection is not populated in order to load the objects that should be present in this collection.

Lazy loading is one of the most famous ORM patterns, and is also the one that is most controversial. When several dozen ORM objects in memory each refer to a handful of unloaded attributes, routine manipulation of these objects can spin off many additional queries that can add up (otherwise known as the N plus one problem), and to make matters worse they are emitted implicitly. These implicit queries may not be noticed, may cause errors when they are attempted after there’s no longer a database transaction available, or when using alternative concurrency patterns such as asyncio, they actually won’t work at all.

At the same time, lazy loading is a vastly popular and useful pattern when it is compatible with the concurrency approach in use and isn’t otherwise causing problems. For these reasons, SQLAlchemy’s ORM places a lot of emphasis on being able to control and optimize this loading behavior.

Above all, the first step in using ORM lazy loading effectively is to test the application, turn on SQL echoing, and watch the SQL that is emitted. If there seem to be lots of redundant SELECT statements that look very much like they could be rolled into one much more efficiently, if there are loads occurring inappropriately for objects that have been detached from their Session, that’s when to look into using loader strategies.

Loader strategies are represented as objects that may be associated with a SELECT statement using the Select.options() method, e.g.:

They may be also configured as defaults for a relationship() using the relationship.lazy option, e.g.:

Each loader strategy object adds some kind of information to the statement that will be used later by the Session when it is deciding how various attributes should be loaded and/or behave when they are accessed.

The sections below will introduce a few of the most prominently used loader strategies.

Two sections in Relationship Loading Techniques:

Configuring Loader Strategies at Mapping Time - details on configuring the strategy on relationship()

Relationship Loading with Loader Options - details on using query-time loader strategies

The most useful loader in modern SQLAlchemy is the selectinload() loader option. This option solves the most common form of the “N plus one” problem which is that of a set of objects that refer to related collections. selectinload() will ensure that a particular collection for a full series of objects are loaded up front using a single query. It does this using a SELECT form that in most cases can be emitted against the related table alone, without the introduction of JOINs or subqueries, and only queries for those parent objects for which the collection isn’t already loaded. Below we illustrate selectinload() by loading all of the User objects and all of their related Address objects; while we invoke Session.execute() only once, given a select() construct, when the database is accessed, there are in fact two SELECT statements emitted, the second one being to fetch the related Address objects:

Select IN loading - in Relationship Loading Techniques

The joinedload() eager load strategy is the oldest eager loader in SQLAlchemy, which augments the SELECT statement that’s being passed to the database with a JOIN (which may be an outer or an inner join depending on options), which can then load in related objects.

The joinedload() strategy is best suited towards loading related many-to-one objects, as this only requires that additional columns are added to a primary entity row that would be fetched in any case. For greater efficiency, it also accepts an option joinedload.innerjoin so that an inner join instead of an outer join may be used for a case such as below where we know that all Address objects have an associated User:

joinedload() also works for collections, meaning one-to-many relationships, however it has the effect of multiplying out primary rows per related item in a recursive way that grows the amount of data sent for a result set by orders of magnitude for nested collections and/or larger collections, so its use vs. another option such as selectinload() should be evaluated on a per-case basis.

It’s important to note that the WHERE and ORDER BY criteria of the enclosing Select statement do not target the table rendered by joinedload(). Above, it can be seen in the SQL that an anonymous alias is applied to the user_account table such that is not directly addressable in the query. This concept is discussed in more detail in the section The Zen of Joined Eager Loading.

It’s important to note that many-to-one eager loads are often not necessary, as the “N plus one” problem is much less prevalent in the common case. When many objects all refer to the same related object, such as many Address objects that each refer to the same User, SQL will be emitted only once for that User object using normal lazy loading. The lazy load routine will look up the related object by primary key in the current Session without emitting any SQL when possible.

Joined Eager Loading - in Relationship Loading Techniques

If we were to load Address rows while joining to the user_account table using a method such as Select.join() to render the JOIN, we could also leverage that JOIN in order to eagerly load the contents of the Address.user attribute on each Address object returned. This is essentially that we are using “joined eager loading” but rendering the JOIN ourselves. This common use case is achieved by using the contains_eager() option. This option is very similar to joinedload(), except that it assumes we have set up the JOIN ourselves, and it instead only indicates that additional columns in the COLUMNS clause should be loaded into related attributes on each returned object, for example:

Above, we both filtered the rows on user_account.name and also loaded rows from user_account into the Address.user attribute of the returned rows. If we had applied joinedload() separately, we would get a SQL query that unnecessarily joins twice:

Two sections in Relationship Loading Techniques:

The Zen of Joined Eager Loading - describes the above problem in detail

Routing Explicit Joins/Statements into Eagerly Loaded Collections - using contains_eager()

One additional loader strategy worth mentioning is raiseload(). This option is used to completely block an application from having the N plus one problem at all by causing what would normally be a lazy load to raise an error instead. It has two variants that are controlled via the raiseload.sql_only option to block either lazy loads that require SQL, versus all “load” operations including those which only need to consult the current Session.

One way to use raiseload() is to configure it on relationship() itself, by setting relationship.lazy to the value "raise_on_sql", so that for a particular mapping, a certain relationship will never try to emit SQL:

Using such a mapping, the application is blocked from lazy loading, indicating that a particular query would need to specify a loader strategy:

The exception would indicate that this collection should be loaded up front instead:

The lazy="raise_on_sql" option tries to be smart about many-to-one relationships as well; above, if the Address.user attribute of an Address object were not loaded, but that User object were locally present in the same Session, the “raiseload” strategy would not raise an error.

Preventing unwanted lazy loads using raiseload - in Relationship Loading Techniques

SQLAlchemy 1.4 / 2.0 Tutorial

Next Tutorial Section: Further Reading

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (typescript):
```typescript
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user_account"

    # ... mapped_column() mappings

    addresses: Mapped[List["Address"]] = relationship(back_populates="user")


class Address(Base):
    __tablename__ = "address"

    # ... mapped_column() mappings

    user: Mapped["User"] = relationship(back_populates="addresses")
```

Example 2 (json):
```json
>>> u1 = User(name="pkrabs", fullname="Pearl Krabs")
>>> u1.addresses
[]
```

Example 3 (python):
```python
>>> a1 = Address(email_address="pearl.krabs@gmail.com")
>>> u1.addresses.append(a1)
```

Example 4 (json):
```json
>>> u1.addresses
[Address(id=None, email_address='pearl.krabs@gmail.com')]
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Unified Tutorial
    - Project Versions
- Working with Transactions and the DBAPI¶
- Getting a Connection¶
- Committing Changes¶
- Basics of Statement Execution¶
  - Fetching Rows¶
  - Sending Parameters¶

Home | Download this Documentation

Home | Download this Documentation

SQLAlchemy 1.4 / 2.0 Tutorial

This page is part of the SQLAlchemy Unified Tutorial.

Previous: Establishing Connectivity - the Engine | Next: Working with Database Metadata

With the Engine object ready to go, we can dive into the basic operation of an Engine and its primary endpoints, the Connection and Result. We’ll also introduce the ORM’s facade for these objects, known as the Session.

When using the ORM, the Engine is managed by the Session. The Session in modern SQLAlchemy emphasizes a transactional and SQL execution pattern that is largely identical to that of the Connection discussed below, so while this subsection is Core-centric, all of the concepts here are relevant to ORM use as well and is recommended for all ORM learners. The execution pattern used by the Connection will be compared to the Session at the end of this section.

As we have yet to introduce the SQLAlchemy Expression Language that is the primary feature of SQLAlchemy, we’ll use a simple construct within this package called the text() construct, to write SQL statements as textual SQL. Rest assured that textual SQL is the exception rather than the rule in day-to-day SQLAlchemy use, but it’s always available.

The purpose of the Engine is to connect to the database by providing a Connection object. When working with the Core directly, the Connection object is how all interaction with the database is done. Because the Connection creates an open resource against the database, we want to limit our use of this object to a specific context. The best way to do that is with a Python context manager, also known as the with statement. Below we use a textual SQL statement to show “Hello World”. Textual SQL is created with a construct called text() which we’ll discuss in more detail later:

In the example above, the context manager creates a database connection and executes the operation in a transaction. The default behavior of the Python DBAPI is that a transaction is always in progress; when the connection is released, a ROLLBACK is emitted to end the transaction. The transaction is not committed automatically; if we want to commit data we need to call Connection.commit() as we’ll see in the next section.

“autocommit” mode is available for special cases. The section Setting Transaction Isolation Levels including DBAPI Autocommit discusses this.

The result of our SELECT was returned in an object called Result that will be discussed later. For the moment we’ll add that it’s best to use this object within the “connect” block, and to not use it outside of the scope of our connection.

We just learned that the DBAPI connection doesn’t commit automatically. What if we want to commit some data? We can change our example above to create a table, insert some data and then commit the transaction using the Connection.commit() method, inside the block where we have the Connection object:

Above, we execute two SQL statements, a “CREATE TABLE” statement [1] and an “INSERT” statement that’s parameterized (we discuss the parameterization syntax later in Sending Multiple Parameters). To commit the work we’ve done in our block, we call the Connection.commit() method which commits the transaction. After this, we can continue to run more SQL statements and call Connection.commit() again for those statements. SQLAlchemy refers to this style as commit as you go.

There’s also another style to commit data. We can declare our “connect” block to be a transaction block up front. To do this, we use the Engine.begin() method to get the connection, rather than the Engine.connect() method. This method will manage the scope of the Connection and also enclose everything inside of a transaction with either a COMMIT at the end if the block was successful, or a ROLLBACK if an exception was raised. This style is known as begin once:

You should mostly prefer the “begin once” style because it’s shorter and shows the intention of the entire block up front. However, in this tutorial we’ll use “commit as you go” style as it’s more flexible for demonstration purposes.

What’s “BEGIN (implicit)”?

You might have noticed the log line “BEGIN (implicit)” at the start of a transaction block. “implicit” here means that SQLAlchemy did not actually send any command to the database; it just considers this to be the start of the DBAPI’s implicit transaction. You can register event hooks to intercept this event, for example.

DDL refers to the subset of SQL that instructs the database to create, modify, or remove schema-level constructs such as tables. DDL such as “CREATE TABLE” should be in a transaction block that ends with COMMIT, as many databases use transactional DDL such that the schema changes don’t take place until the transaction is committed. However, as we’ll see later, we usually let SQLAlchemy run DDL sequences for us as part of a higher level operation where we don’t generally need to worry about the COMMIT.

We have seen a few examples that run SQL statements against a database, making use of a method called Connection.execute(), in conjunction with an object called text(), and returning an object called Result. In this section we’ll illustrate more closely the mechanics and interactions of these components.

Most of the content in this section applies equally well to modern ORM use when using the Session.execute() method, which works very similarly to that of Connection.execute(), including that ORM result rows are delivered using the same Result interface used by Core.

We’ll first illustrate the Result object more closely by making use of the rows we’ve inserted previously, running a textual SELECT statement on the table we’ve created:

Above, the “SELECT” string we executed selected all rows from our table. The object returned is called Result and represents an iterable object of result rows.

Result has lots of methods for fetching and transforming rows, such as the Result.all() method illustrated previously, which returns a list of all Row objects. It also implements the Python iterator interface so that we can iterate over the collection of Row objects directly.

The Row objects themselves are intended to act like Python named tuples. Below we illustrate a variety of ways to access rows.

Tuple Assignment - This is the most Python-idiomatic style, which is to assign variables to each row positionally as they are received:

Integer Index - Tuples are Python sequences, so regular integer access is available too:

Attribute Name - As these are Python named tuples, the tuples have dynamic attribute names matching the names of each column. These names are normally the names that the SQL statement assigns to the columns in each row. While they are usually fairly predictable and can also be controlled by labels, in less defined cases they may be subject to database-specific behaviors:

Mapping Access - To receive rows as Python mapping objects, which is essentially a read-only version of Python’s interface to the common dict object, the Result may be transformed into a MappingResult object using the Result.mappings() modifier; this is a result object that yields dictionary-like RowMapping objects rather than Row objects:

SQL statements are usually accompanied by data that is to be passed with the statement itself, as we saw in the INSERT example previously. The Connection.execute() method therefore also accepts parameters, which are known as bound parameters. A rudimentary example might be if we wanted to limit our SELECT statement only to rows that meet a certain criteria, such as rows where the “y” value were greater than a certain value that is passed in to a function.

In order to achieve this such that the SQL statement can remain fixed and that the driver can properly sanitize the value, we add a WHERE criteria to our statement that names a new parameter called “y”; the text() construct accepts these using a colon format “:y”. The actual value for “:y” is then passed as the second argument to Connection.execute() in the form of a dictionary:

In the logged SQL output, we can see that the bound parameter :y was converted into a question mark when it was sent to the SQLite database. This is because the SQLite database driver uses a format called “qmark parameter style”, which is one of six different formats allowed by the DBAPI specification. SQLAlchemy abstracts these formats into just one, which is the “named” format using a colon.

Always use bound parameters

As mentioned at the beginning of this section, textual SQL is not the usual way we work with SQLAlchemy. However, when using textual SQL, a Python literal value, even non-strings like integers or dates, should never be stringified into SQL string directly; a parameter should always be used. This is most famously known as how to avoid SQL injection attacks when the data is untrusted. However it also allows the SQLAlchemy dialects and/or DBAPI to correctly handle the incoming input for the backend. Outside of plain textual SQL use cases, SQLAlchemy’s Core Expression API otherwise ensures that Python literal values are passed as bound parameters where appropriate.

In the example at Committing Changes, we executed an INSERT statement where it appeared that we were able to INSERT multiple rows into the database at once. For DML statements such as “INSERT”, “UPDATE” and “DELETE”, we can send multiple parameter sets to the Connection.execute() method by passing a list of dictionaries instead of a single dictionary, which indicates that the single SQL statement should be invoked multiple times, once for each parameter set. This style of execution is known as executemany:

The above operation is equivalent to running the given INSERT statement once for each parameter set, except that the operation will be optimized for better performance across many rows.

A key behavioral difference between “execute” and “executemany” is that the latter doesn’t support returning of result rows, even if the statement includes the RETURNING clause. The one exception to this is when using a Core insert() construct, introduced later in this tutorial at Using INSERT Statements, which also indicates RETURNING using the Insert.returning() method. In that case, SQLAlchemy makes use of special logic to reorganize the INSERT statement so that it can be invoked for many rows while still supporting RETURNING.

executemany - in the Glossary, describes the DBAPI-level cursor.executemany() method that’s used for most “executemany” executions.

“Insert Many Values” Behavior for INSERT statements - in Working with Engines and Connections, describes the specialized logic used by Insert.returning() to deliver result sets with “executemany” executions.

As mentioned previously, most of the patterns and examples above apply to use with the ORM as well, so here we will introduce this usage so that as the tutorial proceeds, we will be able to illustrate each pattern in terms of Core and ORM use together.

The fundamental transactional / database interactive object when using the ORM is called the Session. In modern SQLAlchemy, this object is used in a manner very similar to that of the Connection, and in fact as the Session is used, it refers to a Connection internally which it uses to emit SQL.

When the Session is used with non-ORM constructs, it passes through the SQL statements we give it and does not generally do things much differently from how the Connection does directly, so we can illustrate it here in terms of the simple textual SQL operations we’ve already learned.

The Session has a few different creational patterns, but here we will illustrate the most basic one that tracks exactly with how the Connection is used which is to construct it within a context manager:

The example above can be compared to the example in the preceding section in Sending Parameters - we directly replace the call to with engine.connect() as conn with with Session(engine) as session, and then make use of the Session.execute() method just like we do with the Connection.execute() method.

Also, like the Connection, the Session features “commit as you go” behavior using the Session.commit() method, illustrated below using a textual UPDATE statement to alter some of our data:

Above, we invoked an UPDATE statement using the bound-parameter, “executemany” style of execution introduced at Sending Multiple Parameters, ending the block with a “commit as you go” commit.

The Session doesn’t actually hold onto the Connection object after it ends the transaction. It gets a new Connection from the Engine the next time it needs to execute SQL against the database.

The Session obviously has a lot more tricks up its sleeve than that, however understanding that it has a Session.execute() method that’s used the same way as Connection.execute() will get us started with the examples that follow later.

Basics of Using a Session - presents basic creational and usage patterns with the Session object.

SQLAlchemy 1.4 / 2.0 Tutorial

Next Tutorial Section: Working with Database Metadata

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (sql):
```sql
>>> from sqlalchemy import text

>>> with engine.connect() as conn:
...     result = conn.execute(text("select 'hello world'"))
...     print(result.all())
BEGIN (implicit)
select 'hello world'
[...] ()
[('hello world',)]
ROLLBACK
```

Example 2 (sql):
```sql
# "commit as you go"
>>> with engine.connect() as conn:
...     conn.execute(text("CREATE TABLE some_table (x int, y int)"))
...     conn.execute(
...         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
...         [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
...     )
...     conn.commit()
BEGIN (implicit)
CREATE TABLE some_table (x int, y int)
[...] ()
<sqlalchemy.engine.cursor.CursorResult object at 0x...>
INSERT INTO some_table (x, y) VALUES (?, ?)
[...] [(1, 1), (2, 4)]
<sqlalchemy.engine.cursor.CursorResult object at 0x...>
COMMIT
```

Example 3 (json):
```json
# "begin once"
>>> with engine.begin() as conn:
...     conn.execute(
...         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
...         [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
...     )
BEGIN (implicit)
INSERT INTO some_table (x, y) VALUES (?, ?)
[...] [(6, 8), (9, 10)]
<sqlalchemy.engine.cursor.CursorResult object at 0x...>
COMMIT
```

Example 4 (sql):
```sql
>>> with engine.connect() as conn:
...     result = conn.execute(text("SELECT x, y FROM some_table"))
...     for row in result:
...         print(f"x: {row.x}  y: {row.y}")
BEGIN (implicit)
SELECT x, y FROM some_table
[...] ()
x: 1  y: 1
x: 2  y: 4
x: 6  y: 8
x: 9  y: 10
ROLLBACK
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/tutorial/data_select.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Unified Tutorial
    - Project Versions
- Using SELECT Statements¶
- The select() SQL Expression Construct¶
- Setting the COLUMNS and FROM clause¶
  - Selecting ORM Entities and Columns¶
  - Selecting from Labeled SQL Expressions¶
  - Selecting with Textual Column Expressions¶

Home | Download this Documentation

Home | Download this Documentation

SQLAlchemy 1.4 / 2.0 Tutorial

This page is part of the SQLAlchemy Unified Tutorial.

Previous: Using INSERT Statements | Next: Using UPDATE and DELETE Statements

For both Core and ORM, the select() function generates a Select construct which is used for all SELECT queries. Passed to methods like Connection.execute() in Core and Session.execute() in ORM, a SELECT statement is emitted in the current transaction and the result rows available via the returned Result object.

ORM Readers - the content here applies equally well to both Core and ORM use and basic ORM variant use cases are mentioned here. However there are a lot more ORM-specific features available as well; these are documented at ORM Querying Guide.

The select() construct builds up a statement in the same way as that of insert(), using a generative approach where each method builds more state onto the object. Like the other SQL constructs, it can be stringified in place:

Also in the same manner as all other statement-level SQL constructs, to actually run the statement we pass it to an execution method. Since a SELECT statement returns rows we can always iterate the result object to get Row objects back:

When using the ORM, particularly with a select() construct that’s composed against ORM entities, we will want to execute it using the Session.execute() method on the Session; using this approach, we continue to get Row objects from the result, however these rows are now capable of including complete entities, such as instances of the User class, as individual elements within each row:

select() from a Table vs. ORM class

While the SQL generated in these examples looks the same whether we invoke select(user_table) or select(User), in the more general case they do not necessarily render the same thing, as an ORM-mapped class may be mapped to other kinds of “selectables” besides tables. The select() that’s against an ORM entity also indicates that ORM-mapped instances should be returned in a result, which is not the case when SELECTing from a Table object.

The following sections will discuss the SELECT construct in more detail.

The select() function accepts positional elements representing any number of Column and/or Table expressions, as well as a wide range of compatible objects, which are resolved into a list of SQL expressions to be SELECTed from that will be returned as columns in the result set. These elements also serve in simpler cases to create the FROM clause, which is inferred from the columns and table-like expressions passed:

To SELECT from individual columns using a Core approach, Column objects are accessed from the Table.c accessor and can be sent directly; the FROM clause will be inferred as the set of all Table and other FromClause objects that are represented by those columns:

Alternatively, when using the FromClause.c collection of any FromClause such as Table, multiple columns may be specified for a select() by using a tuple of string names:

Added in version 2.0: Added tuple-accessor capability to the FromClause.c collection

ORM entities, such our User class as well as the column-mapped attributes upon it such as User.name, also participate in the SQL Expression Language system representing tables and columns. Below illustrates an example of SELECTing from the User entity, which ultimately renders in the same way as if we had used user_table directly:

When executing a statement like the above using the ORM Session.execute() method, there is an important difference when we select from a full entity such as User, as opposed to user_table, which is that the entity itself is returned as a single element within each row. That is, when we fetch rows from the above statement, as there is only the User entity in the list of things to fetch, we get back Row objects that have only one element, which contain instances of the User class:

The above Row has just one element, representing the User entity:

A highly recommended convenience method of achieving the same result as above is to use the Session.scalars() method to execute the statement directly; this method will return a ScalarResult object that delivers the first “column” of each row at once, in this case, instances of the User class:

Alternatively, we can select individual columns of an ORM entity as distinct elements within result rows, by using the class-bound attributes; when these are passed to a construct such as select(), they are resolved into the Column or other SQL expression represented by each attribute:

When we invoke this statement using Session.execute(), we now receive rows that have individual elements per value, each corresponding to a separate column or other SQL expression:

The approaches can also be mixed, as below where we SELECT the name attribute of the User entity as the first element of the row, and combine it with full Address entities in the second element:

Approaches towards selecting ORM entities and columns as well as common methods for converting rows are discussed further at Selecting ORM Entities and Attributes.

Selecting ORM Entities and Attributes - in the ORM Querying Guide

The ColumnElement.label() method as well as the same-named method available on ORM attributes provides a SQL label of a column or expression, allowing it to have a specific name in a result set. This can be helpful when referring to arbitrary SQL expressions in a result row by name:

Ordering or Grouping by a Label - the label names we create may also be referenced in the ORDER BY or GROUP BY clause of the Select.

When we construct a Select object using the select() function, we are normally passing to it a series of Table and Column objects that were defined using table metadata, or when using the ORM we may be sending ORM-mapped attributes that represent table columns. However, sometimes there is also the need to manufacture arbitrary SQL blocks inside of statements, such as constant string expressions, or just some arbitrary SQL that’s quicker to write literally.

The text() construct introduced at Working with Transactions and the DBAPI can in fact be embedded into a Select construct directly, such as below where we manufacture a hardcoded string literal 'some phrase' and embed it within the SELECT statement:

While the text() construct can be used in most places to inject literal SQL phrases, more often than not we are actually dealing with textual units that each represent an individual column expression. In this common case we can get more functionality out of our textual fragment using the literal_column() construct instead. This object is similar to text() except that instead of representing arbitrary SQL of any form, it explicitly represents a single “column” and can then be labeled and referred towards in subqueries and other expressions:

Note that in both cases, when using text() or literal_column(), we are writing a syntactical SQL expression, and not a literal value. We therefore have to include whatever quoting or syntaxes are necessary for the SQL we want to see rendered.

SQLAlchemy allows us to compose SQL expressions, such as name = 'squidward' or user_id > 10, by making use of standard Python operators in conjunction with Column and similar objects. For boolean expressions, most Python operators such as ==, !=, <, >= etc. generate new SQL Expression objects, rather than plain boolean True/False values:

We can use expressions like these to generate the WHERE clause by passing the resulting objects to the Select.where() method:

To produce multiple expressions joined by AND, the Select.where() method may be invoked any number of times:

A single call to Select.where() also accepts multiple expressions with the same effect:

“AND” and “OR” conjunctions are both available directly using the and_() and or_() functions, illustrated below in terms of ORM entities:

The rendering of parentheses is based on operator precedence rules (there’s no way to detect parentheses from a Python expression at runtime), so if we combine AND and OR in a way that matches the natural precedence of AND, the rendered expression might not have similar looking parentheses as our Python code:

More background on parenthesization is in the Parentheses and Grouping in the Operator Reference.

For simple “equality” comparisons against a single entity, there’s also a popular method known as Select.filter_by() which accepts keyword arguments that match to column keys or ORM attribute names. It will filter against the leftmost FROM clause or the last entity joined:

Operator Reference - descriptions of most SQL operator functions in SQLAlchemy

As mentioned previously, the FROM clause is usually inferred based on the expressions that we are setting in the columns clause as well as other elements of the Select.

If we set a single column from a particular Table in the COLUMNS clause, it puts that Table in the FROM clause as well:

If we were to put columns from two tables, then we get a comma-separated FROM clause:

In order to JOIN these two tables together, we typically use one of two methods on Select. The first is the Select.join_from() method, which allows us to indicate the left and right side of the JOIN explicitly:

The other is the Select.join() method, which indicates only the right side of the JOIN, the left hand-side is inferred:

The ON Clause is inferred

When using Select.join_from() or Select.join(), we may observe that the ON clause of the join is also inferred for us in simple foreign key cases. More on that in the next section.

We also have the option to add elements to the FROM clause explicitly, if it is not inferred the way we want from the columns clause. We use the Select.select_from() method to achieve this, as below where we establish user_table as the first element in the FROM clause and Select.join() to establish address_table as the second:

Another example where we might want to use Select.select_from() is if our columns clause doesn’t have enough information to provide for a FROM clause. For example, to SELECT from the common SQL expression count(*), we use a SQLAlchemy element known as sqlalchemy.sql.expression.func to produce the SQL count() function:

Setting the leftmost FROM clause in a join - in the ORM Querying Guide - contains additional examples and notes regarding the interaction of Select.select_from() and Select.join().

The previous examples of JOIN illustrated that the Select construct can join between two tables and produce the ON clause automatically. This occurs in those examples because the user_table and address_table Table objects include a single ForeignKeyConstraint definition which is used to form this ON clause.

If the left and right targets of the join do not have such a constraint, or there are multiple constraints in place, we need to specify the ON clause directly. Both Select.join() and Select.join_from() accept an additional argument for the ON clause, which is stated using the same SQL Expression mechanics as we saw about in The WHERE clause:

ORM Tip - there’s another way to generate the ON clause when using ORM entities that make use of the relationship() construct, like the mapping set up in the previous section at Declaring Mapped Classes. This is a whole subject onto itself, which is introduced at length at Using Relationships to Join.

Both the Select.join() and Select.join_from() methods accept keyword arguments Select.join.isouter and Select.join.full which will render LEFT OUTER JOIN and FULL OUTER JOIN, respectively:

There is also a method Select.outerjoin() that is equivalent to using .join(..., isouter=True).

SQL also has a “RIGHT OUTER JOIN”. SQLAlchemy doesn’t render this directly; instead, reverse the order of the tables and use “LEFT OUTER JOIN”.

The SELECT SQL statement includes a clause called ORDER BY which is used to return the selected rows within a given ordering.

The GROUP BY clause is constructed similarly to the ORDER BY clause, and has the purpose of sub-dividing the selected rows into specific groups upon which aggregate functions may be invoked. The HAVING clause is usually used with GROUP BY and is of a similar form to the WHERE clause, except that it’s applied to the aggregated functions used within groups.

The ORDER BY clause is constructed in terms of SQL Expression constructs typically based on Column or similar objects. The Select.order_by() method accepts one or more of these expressions positionally:

Ascending / descending is available from the ColumnElement.asc() and ColumnElement.desc() modifiers, which are present from ORM-bound attributes as well:

The above statement will yield rows that are sorted by the user_account.fullname column in descending order.

In SQL, aggregate functions allow column expressions across multiple rows to be aggregated together to produce a single result. Examples include counting, computing averages, as well as locating the maximum or minimum value in a set of values.

SQLAlchemy provides for SQL functions in an open-ended way using a namespace known as func. This is a special constructor object which will create new instances of Function when given the name of a particular SQL function, which can have any name, as well as zero or more arguments to pass to the function, which are, like in all other cases, SQL Expression constructs. For example, to render the SQL COUNT() function against the user_account.id column, we call upon the count() name:

SQL functions are described in more detail later in this tutorial at Working with SQL Functions.

When using aggregate functions in SQL, the GROUP BY clause is essential in that it allows rows to be partitioned into groups where aggregate functions will be applied to each group individually. When requesting non-aggregated columns in the COLUMNS clause of a SELECT statement, SQL requires that these columns all be subject to a GROUP BY clause, either directly or indirectly based on a primary key association. The HAVING clause is then used in a similar manner as the WHERE clause, except that it filters out rows based on aggregated values rather than direct row contents.

SQLAlchemy provides for these two clauses using the Select.group_by() and Select.having() methods. Below we illustrate selecting user name fields as well as count of addresses, for those users that have more than one address:

An important technique, in particular on some database backends, is the ability to ORDER BY or GROUP BY an expression that is already stated in the columns clause, without re-stating the expression in the ORDER BY or GROUP BY clause and instead using the column name or labeled name from the COLUMNS clause. This form is available by passing the string text of the name to the Select.order_by() or Select.group_by() method. The text passed is not rendered directly; instead, the name given to an expression in the columns clause and rendered as that expression name in context, raising an error if no match is found. The unary modifiers asc() and desc() may also be used in this form:

Now that we are selecting from multiple tables and using joins, we quickly run into the case where we need to refer to the same table multiple times in the FROM clause of a statement. We accomplish this using SQL aliases, which are a syntax that supplies an alternative name to a table or subquery from which it can be referenced in the statement.

In the SQLAlchemy Expression Language, these “names” are instead represented by FromClause objects known as the Alias construct, which is constructed in Core using the FromClause.alias() method. An Alias construct is just like a Table construct in that it also has a namespace of Column objects within the Alias.c collection. The SELECT statement below for example returns all unique pairs of user names:

The ORM equivalent of the FromClause.alias() method is the ORM aliased() function, which may be applied to an entity such as User and Address. This produces a Alias object internally that’s against the original mapped Table object, while maintaining ORM functionality. The SELECT below selects from the User entity all objects that include two particular email addresses:

As mentioned in Setting the ON Clause, the ORM provides for another way to join using the relationship() construct. The above example using aliases is demonstrated using relationship() at Using Relationship to join between aliased targets.

A subquery in SQL is a SELECT statement that is rendered within parenthesis and placed within the context of an enclosing statement, typically a SELECT statement but not necessarily.

This section will cover a so-called “non-scalar” subquery, which is typically placed in the FROM clause of an enclosing SELECT. We will also cover the Common Table Expression or CTE, which is used in a similar way as a subquery, but includes additional features.

SQLAlchemy uses the Subquery object to represent a subquery and the CTE to represent a CTE, usually obtained from the Select.subquery() and Select.cte() methods, respectively. Either object can be used as a FROM element inside of a larger select() construct.

We can construct a Subquery that will select an aggregate count of rows from the address table (aggregate functions and GROUP BY were introduced previously at Aggregate functions with GROUP BY / HAVING):

Stringifying the subquery by itself without it being embedded inside of another Select or other statement produces the plain SELECT statement without any enclosing parenthesis:

The Subquery object behaves like any other FROM object such as a Table, notably that it includes a Subquery.c namespace of the columns which it selects. We can use this namespace to refer to both the user_id column as well as our custom labeled count expression:

With a selection of rows contained within the subq object, we can apply the object to a larger Select that will join the data to the user_account table:

In order to join from user_account to address, we made use of the Select.join_from() method. As has been illustrated previously, the ON clause of this join was again inferred based on foreign key constraints. Even though a SQL subquery does not itself have any constraints, SQLAlchemy can act upon constraints represented on the columns by determining that the subq.c.user_id column is derived from the address_table.c.user_id column, which does express a foreign key relationship back to the user_table.c.id column which is then used to generate the ON clause.

Usage of the CTE construct in SQLAlchemy is virtually the same as how the Subquery construct is used. By changing the invocation of the Select.subquery() method to use Select.cte() instead, we can use the resulting object as a FROM element in the same way, but the SQL rendered is the very different common table expression syntax:

The CTE construct also features the ability to be used in a “recursive” style, and may in more elaborate cases be composed from the RETURNING clause of an INSERT, UPDATE or DELETE statement. The docstring for CTE includes details on these additional patterns.

In both cases, the subquery and CTE were named at the SQL level using an “anonymous” name. In the Python code, we don’t need to provide these names at all. The object identity of the Subquery or CTE instances serves as the syntactical identity of the object when rendered. A name that will be rendered in the SQL can be provided by passing it as the first argument of the Select.subquery() or Select.cte() methods.

Select.subquery() - further detail on subqueries

Select.cte() - examples for CTE including how to use RECURSIVE as well as DML-oriented CTEs

In the ORM, the aliased() construct may be used to associate an ORM entity, such as our User or Address class, with any FromClause concept that represents a source of rows. The preceding section ORM Entity Aliases illustrates using aliased() to associate the mapped class with an Alias of its mapped Table. Here we illustrate aliased() doing the same thing against both a Subquery as well as a CTE generated against a Select construct, that ultimately derives from that same mapped Table.

Below is an example of applying aliased() to the Subquery construct, so that ORM entities can be extracted from its rows. The result shows a series of User and Address objects, where the data for each Address object ultimately came from a subquery against the address table rather than that table directly:

Another example follows, which is exactly the same except it makes use of the CTE construct instead:

Selecting Entities from Subqueries - in the ORM Querying Guide

A scalar subquery is a subquery that returns exactly zero or one row and exactly one column. The subquery is then used in the COLUMNS or WHERE clause of an enclosing SELECT statement and is different than a regular subquery in that it is not used in the FROM clause. A correlated subquery is a scalar subquery that refers to a table in the enclosing SELECT statement.

SQLAlchemy represents the scalar subquery using the ScalarSelect construct, which is part of the ColumnElement expression hierarchy, in contrast to the regular subquery which is represented by the Subquery construct, which is in the FromClause hierarchy.

Scalar subqueries are often, but not necessarily, used with aggregate functions, introduced previously at Aggregate functions with GROUP BY / HAVING. A scalar subquery is indicated explicitly by making use of the Select.scalar_subquery() method as below. It’s default string form when stringified by itself renders as an ordinary SELECT statement that is selecting from two tables:

The above subq object now falls within the ColumnElement SQL expression hierarchy, in that it may be used like any other column expression:

Although the scalar subquery by itself renders both user_account and address in its FROM clause when stringified by itself, when embedding it into an enclosing select() construct that deals with the user_account table, the user_account table is automatically correlated, meaning it does not render in the FROM clause of the subquery:

Simple correlated subqueries will usually do the right thing that’s desired. However, in the case where the correlation is ambiguous, SQLAlchemy will let us know that more clarity is needed:

To specify that the user_table is the one we seek to correlate we specify this using the ScalarSelect.correlate() or ScalarSelect.correlate_except() methods:

The statement then can return the data for this column like any other:

LATERAL correlation is a special sub-category of SQL correlation which allows a selectable unit to refer to another selectable unit within a single FROM clause. This is an extremely special use case which, while part of the SQL standard, is only known to be supported by recent versions of PostgreSQL.

Normally, if a SELECT statement refers to table1 JOIN (SELECT ...) AS subquery in its FROM clause, the subquery on the right side may not refer to the “table1” expression from the left side; correlation may only refer to a table that is part of another SELECT that entirely encloses this SELECT. The LATERAL keyword allows us to turn this behavior around and allow correlation from the right side JOIN.

SQLAlchemy supports this feature using the Select.lateral() method, which creates an object known as Lateral. Lateral is in the same family as Subquery and Alias, but also includes correlation behavior when the construct is added to the FROM clause of an enclosing SELECT. The following example illustrates a SQL query that makes use of LATERAL, selecting the “user account / count of email address” data as was discussed in the previous section:

Above, the right side of the JOIN is a subquery that correlates to the user_account table that’s on the left side of the join.

When using Select.lateral(), the behavior of Select.correlate() and Select.correlate_except() methods is applied to the Lateral construct as well.

In SQL, SELECT statements can be merged together using the UNION or UNION ALL SQL operation, which produces the set of all rows produced by one or more statements together. Other set operations such as INTERSECT [ALL] and EXCEPT [ALL] are also possible.

SQLAlchemy’s Select construct supports compositions of this nature using functions like union(), intersect() and except_(), and the “all” counterparts union_all(), intersect_all() and except_all(). These functions all accept an arbitrary number of sub-selectables, which are typically Select constructs but may also be an existing composition.

The construct produced by these functions is the CompoundSelect, which is used in the same manner as the Select construct, except that it has fewer methods. The CompoundSelect produced by union_all() for example may be invoked directly using Connection.execute():

To use a CompoundSelect as a subquery, just like Select it provides a SelectBase.subquery() method which will produce a Subquery object with a FromClause.c collection that may be referenced in an enclosing select():

The preceding examples illustrated how to construct a UNION given two Table objects, to then return database rows. If we wanted to use a UNION or other set operation to select rows that we then receive as ORM objects, there are two approaches that may be used. In both cases, we first construct a select() or CompoundSelect object that represents the SELECT / UNION / etc statement we want to execute; this statement should be composed against the target ORM entities or their underlying mapped Table objects:

For a simple SELECT with UNION that is not already nested inside of a subquery, these can often be used in an ORM object fetching context by using the Select.from_statement() method. With this approach, the UNION statement represents the entire query; no additional criteria can be added after Select.from_statement() is used:

To use a UNION or other set-related construct as an entity-related component in in a more flexible manner, the CompoundSelect construct may be organized into a subquery using CompoundSelect.subquery(), which then links to ORM objects using the aliased() function. This works in the same way introduced at ORM Entity Subqueries/CTEs, to first create an ad-hoc “mapping” of our desired entity to the subquery, then selecting from that new entity as though it were any other mapped class. In the example below, we are able to add additional criteria such as ORDER BY outside of the UNION itself, as we can filter or order by the columns exported by the subquery:

Selecting Entities from UNIONs and other set operations - in the ORM Querying Guide

The SQL EXISTS keyword is an operator that is used with scalar subqueries to return a boolean true or false depending on if the SELECT statement would return a row. SQLAlchemy includes a variant of the ScalarSelect object called Exists, which will generate an EXISTS subquery and is most conveniently generated using the SelectBase.exists() method. Below we produce an EXISTS so that we can return user_account rows that have more than one related row in address:

The EXISTS construct is more often than not used as a negation, e.g. NOT EXISTS, as it provides a SQL-efficient form of locating rows for which a related table has no rows. Below we select user names that have no email addresses; note the binary negation operator (~) used inside the second WHERE clause:

First introduced earlier in this section at Aggregate functions with GROUP BY / HAVING, the func object serves as a factory for creating new Function objects, which when used in a construct like select(), produce a SQL function display, typically consisting of a name, some parenthesis (although not always), and possibly some arguments. Examples of typical SQL functions include:

the count() function, an aggregate function which counts how many rows are returned:

the lower() function, a string function that converts a string to lower case:

the now() function, which provides for the current date and time; as this is a common function, SQLAlchemy knows how to render this differently for each backend, in the case of SQLite using the CURRENT_TIMESTAMP function:

As most database backends feature dozens if not hundreds of different SQL functions, func tries to be as liberal as possible in what it accepts. Any name that is accessed from this namespace is automatically considered to be a SQL function that will render in a generic way:

At the same time, a relatively small set of extremely common SQL functions such as count, now, max, concat include pre-packaged versions of themselves which provide for proper typing information as well as backend-specific SQL generation in some cases. The example below contrasts the SQL generation that occurs for the PostgreSQL dialect compared to the Oracle Database dialect for the now function:

As functions are column expressions, they also have SQL datatypes that describe the data type of a generated SQL expression. We refer to these types here as “SQL return types”, in reference to the type of SQL value that is returned by the function in the context of a database-side SQL expression, as opposed to the “return type” of a Python function.

The SQL return type of any SQL function may be accessed, typically for debugging purposes, by referring to the Function.type attribute; this will be pre-configured for a select few of extremely common SQL functions, but for most SQL functions is the “null” datatype if not otherwise specified:

These SQL return types are significant when making use of the function expression in the context of a larger expression; that is, math operators will work better when the datatype of the expression is something like Integer or Numeric, JSON accessors in order to work need to be using a type such as JSON. Certain classes of functions return entire rows instead of column values, where there is a need to refer to specific columns; such functions are known as table valued functions.

The SQL return type of the function may also be significant when executing a statement and getting rows back, for those cases where SQLAlchemy has to apply result-set processing. A prime example of this are date-related functions on SQLite, where SQLAlchemy’s DateTime and related datatypes take on the role of converting from string values to Python datetime() objects as result rows are received.

To apply a specific type to a function we’re creating, we pass it using the Function.type_ parameter; the type argument may be either a TypeEngine class or an instance. In the example below we pass the JSON class to generate the PostgreSQL json_object() function, noting that the SQL return type will be of type JSON:

By creating our JSON function with the JSON datatype, the SQL expression object takes on JSON-related features, such as that of accessing elements:

For common aggregate functions like count, max, min as well as a very small number of date functions like now and string functions like concat, the SQL return type is set up appropriately, sometimes based on usage. The max function and similar aggregate filtering functions will set up the SQL return type based on the argument given:

Date and time functions typically correspond to SQL expressions described by DateTime, Date or Time:

A known string function such as concat will know that a SQL expression would be of type String:

However, for the vast majority of SQL functions, SQLAlchemy does not have them explicitly present in its very small list of known functions. For example, while there is typically no issue using SQL functions func.lower() and func.upper() to convert the casing of strings, SQLAlchemy doesn’t actually know about these functions, so they have a “null” SQL return type:

For simple functions like upper and lower, the issue is not usually significant, as string values may be received from the database without any special type handling on the SQLAlchemy side, and SQLAlchemy’s type coercion rules can often correctly guess intent as well; the Python + operator for example will be correctly interpreted as the string concatenation operator based on looking at both sides of the expression:

Overall, the scenario where the Function.type_ parameter is likely necessary is:

the function is not already a SQLAlchemy built-in function; this can be evidenced by creating the function and observing the Function.type attribute, that is:

Function-aware expression support is needed; this most typically refers to special operators related to datatypes such as JSON or ARRAY

Result value processing is needed, which may include types such as DateTime, Boolean, Enum, or again special datatypes such as JSON, ARRAY.

The following subsections illustrate more things that can be done with SQL functions. While these techniques are less common and more advanced than basic SQL function use, they nonetheless are extremely popular, largely as a result of PostgreSQL’s emphasis on more complex function forms, including table- and column-valued forms that are popular with JSON data.

A window function is a special use of a SQL aggregate function which calculates the aggregate value over the rows being returned in a group as the individual result rows are processed. Whereas a function like MAX() will give you the highest value of a column within a set of rows, using the same function as a “window function” will given you the highest value for each row, as of that row.

In SQL, window functions allow one to specify the rows over which the function should be applied, a “partition” value which considers the window over different sub-sets of rows, and an “order by” expression which importantly indicates the order in which rows should be applied to the aggregate function.

In SQLAlchemy, all SQL functions generated by the func namespace include a method FunctionElement.over() which grants the window function, or “OVER”, syntax; the construct produced is the Over construct.

A common function used with window functions is the row_number() function which simply counts rows. We may partition this row count against user name to number the email addresses of individual users:

Above, the FunctionElement.over.partition_by parameter is used so that the PARTITION BY clause is rendered within the OVER clause. We also may make use of the ORDER BY clause using FunctionElement.over.order_by:

Further options for window functions include usage of ranges; see over() for more examples.

It’s important to note that the FunctionElement.over() method only applies to those SQL functions which are in fact aggregate functions; while the Over construct will happily render itself for any SQL function given, the database will reject the expression if the function itself is not a SQL aggregate function.

The “WITHIN GROUP” SQL syntax is used in conjunction with an “ordered set” or a “hypothetical set” aggregate function. Common “ordered set” functions include percentile_cont() and rank(). SQLAlchemy includes built in implementations rank, dense_rank, mode, percentile_cont and percentile_disc which include a FunctionElement.within_group() method:

“FILTER” is supported by some backends to limit the range of an aggregate function to a particular subset of rows compared to the total range of rows returned, available using the FunctionElement.filter() method:

Table-valued SQL functions support a scalar representation that contains named sub-elements. Often used for JSON and ARRAY-oriented functions as well as functions like generate_series(), the table-valued function is specified in the FROM clause, and is then referenced as a table, or sometimes even as a column. Functions of this form are prominent within the PostgreSQL database, however some forms of table valued functions are also supported by SQLite, Oracle Database, and SQL Server.

Table values, Table and Column valued functions, Row and Tuple objects - in the PostgreSQL documentation.

While many databases support table valued and other special forms, PostgreSQL tends to be where there is the most demand for these features. See this section for additional examples of PostgreSQL syntaxes as well as additional features.

SQLAlchemy provides the FunctionElement.table_valued() method as the basic “table valued function” construct, which will convert a func object into a FROM clause containing a series of named columns, based on string names passed positionally. This returns a TableValuedAlias object, which is a function-enabled Alias construct that may be used as any other FROM clause as introduced at Using Aliases. Below we illustrate the json_each() function, which while common on PostgreSQL is also supported by modern versions of SQLite:

Above, we used the json_each() JSON function supported by SQLite and PostgreSQL to generate a table valued expression with a single column referred towards as value, and then selected two of its three rows.

Table-Valued Functions - in the PostgreSQL documentation - this section will detail additional syntaxes such as special column derivations and “WITH ORDINALITY” that are known to work with PostgreSQL.

A special syntax supported by PostgreSQL and Oracle Database is that of referring towards a function in the FROM clause, which then delivers itself as a single column in the columns clause of a SELECT statement or other column expression context. PostgreSQL makes great use of this syntax for such functions as json_array_elements(), json_object_keys(), json_each_text(), json_each(), etc.

SQLAlchemy refers to this as a “column valued” function and is available by applying the FunctionElement.column_valued() modifier to a Function construct:

The “column valued” form is also supported by the Oracle Database dialects, where it is usable for custom SQL functions:

Column Valued Functions - in the PostgreSQL documentation.

In SQL, we often need to indicate the datatype of an expression explicitly, either to tell the database what type is expected in an otherwise ambiguous expression, or in some cases when we want to convert the implied datatype of a SQL expression into something else. The SQL CAST keyword is used for this task, which in SQLAlchemy is provided by the cast() function. This function accepts a column expression and a data type object as arguments, as demonstrated below where we produce a SQL expression CAST(user_account.id AS VARCHAR) from the user_table.c.id column object:

The cast() function not only renders the SQL CAST syntax, it also produces a SQLAlchemy column expression that will act as the given datatype on the Python side as well. A string expression that is cast() to JSON will gain JSON subscript and comparison operators, for example:

Sometimes there is the need to have SQLAlchemy know the datatype of an expression, for all the reasons mentioned above, but to not render the CAST expression itself on the SQL side, where it may interfere with a SQL operation that already works without it. For this fairly common use case there is another function type_coerce() which is closely related to cast(), in that it sets up a Python expression as having a specific SQL database type, but does not render the CAST keyword or datatype on the database side. type_coerce() is particularly important when dealing with the JSON datatype, which typically has an intricate relationship with string-oriented datatypes on different platforms and may not even be an explicit datatype, such as on SQLite and MariaDB. Below, we use type_coerce() to deliver a Python structure as a JSON string into one of MySQL’s JSON functions:

Above, MySQL’s JSON_EXTRACT SQL function was invoked because we used type_coerce() to indicate that our Python dictionary should be treated as JSON. The Python __getitem__ operator, ['some_key'] in this case, became available as a result and allowed a JSON_EXTRACT path expression (not shown, however in this case it would ultimately be '$."some_key"') to be rendered.

SQLAlchemy 1.4 / 2.0 Tutorial

Next Tutorial Section: Using UPDATE and DELETE Statements

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (sql):
```sql
>>> from sqlalchemy import select
>>> stmt = select(user_table).where(user_table.c.name == "spongebob")
>>> print(stmt)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = :name_1
```

Example 2 (sql):
```sql
>>> with engine.connect() as conn:
...     for row in conn.execute(stmt):
...         print(row)
BEGIN (implicit)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[...] ('spongebob',)
(1, 'spongebob', 'Spongebob Squarepants')
ROLLBACK
```

Example 3 (sql):
```sql
>>> stmt = select(User).where(User.name == "spongebob")
>>> with Session(engine) as session:
...     for row in session.execute(stmt):
...         print(row)
BEGIN (implicit)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[...] ('spongebob',)
(User(id=1, name='spongebob', fullname='Spongebob Squarepants'),)
ROLLBACK
```

Example 4 (sql):
```sql
>>> print(select(user_table))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Unified Tutorial
    - Project Versions
- Using INSERT Statements¶
- The insert() SQL Expression Construct¶
- Executing the Statement¶
- INSERT usually generates the “values” clause automatically¶
- INSERT…RETURNING¶
- INSERT…FROM SELECT¶

Home | Download this Documentation

Home | Download this Documentation

SQLAlchemy 1.4 / 2.0 Tutorial

This page is part of the SQLAlchemy Unified Tutorial.

Previous: Working with Data | Next: Using SELECT Statements

When using Core as well as when using the ORM for bulk operations, a SQL INSERT statement is generated directly using the insert() function - this function generates a new instance of Insert which represents an INSERT statement in SQL, that adds new data into a table.

This section details the Core means of generating an individual SQL INSERT statement in order to add new rows to a table. When using the ORM, we normally use another tool that rides on top of this called the unit of work, which will automate the production of many INSERT statements at once. However, understanding how the Core handles data creation and manipulation is very useful even when the ORM is running it for us. Additionally, the ORM supports direct use of INSERT using a feature called Bulk / Multi Row INSERT, upsert, UPDATE and DELETE.

To skip directly to how to INSERT rows with the ORM using normal unit of work patterns, see Inserting Rows using the ORM Unit of Work pattern.

A simple example of Insert illustrating the target table and the VALUES clause at once:

The above stmt variable is an instance of Insert. Most SQL expressions can be stringified in place as a means to see the general form of what’s being produced:

The stringified form is created by producing a Compiled form of the object which includes a database-specific string SQL representation of the statement; we can acquire this object directly using the ClauseElement.compile() method:

Our Insert construct is an example of a “parameterized” construct, illustrated previously at Sending Parameters; to view the name and fullname bound parameters, these are available from the Compiled construct as well:

Invoking the statement we can INSERT a row into user_table. The INSERT SQL as well as the bundled parameters can be seen in the SQL logging:

In its simple form above, the INSERT statement does not return any rows, and if only a single row is inserted, it will usually include the ability to return information about column-level default values that were generated during the INSERT of that row, most commonly an integer primary key value. In the above case the first row in a SQLite database will normally return 1 for the first integer primary key value, which we can acquire using the CursorResult.inserted_primary_key accessor:

CursorResult.inserted_primary_key returns a tuple because a primary key may contain multiple columns. This is known as a composite primary key. The CursorResult.inserted_primary_key is intended to always contain the complete primary key of the record just inserted, not just a “cursor.lastrowid” kind of value, and is also intended to be populated regardless of whether or not “autoincrement” were used, hence to express a complete primary key it’s a tuple.

Changed in version 1.4.8: the tuple returned by CursorResult.inserted_primary_key is now a named tuple fulfilled by returning it as a Row object.

The example above made use of the Insert.values() method to explicitly create the VALUES clause of the SQL INSERT statement. If we don’t actually use Insert.values() and just print out an “empty” statement, we get an INSERT for every column in the table:

If we take an Insert construct that has not had Insert.values() called upon it and execute it rather than print it, the statement will be compiled to a string based on the parameters that we passed to the Connection.execute() method, and only include columns relevant to the parameters that were passed. This is actually the usual way that Insert is used to insert rows without having to type out an explicit VALUES clause. The example below illustrates a two-column INSERT statement being executed with a list of parameters at once:

The execution above features “executemany” form first illustrated at Sending Multiple Parameters, however unlike when using the text() construct, we didn’t have to spell out any SQL. By passing a dictionary or list of dictionaries to the Connection.execute() method in conjunction with the Insert construct, the Connection ensures that the column names which are passed will be expressed in the VALUES clause of the Insert construct automatically.

When passing a list of dictionaries to Connection.execute() along with a Core Insert, only the first dictionary in the list determines what columns will be in the VALUES clause. The rest of the dictionaries are not scanned. This is both because within traditional executemany(), the INSERT statement can only have one VALUES clause for all parameters, and additionally SQLAlchemy does not want to add overhead by scanning every parameter dictionary to verify each contains the identical keys as the first one.

Note this behavior is distinctly different from that of an ORM enabled INSERT, introduced later in this tutorial, which performs a full scan of parameter sets in terms of an ORM entity.

Hi, welcome to the first edition of Deep Alchemy. The person on the left is known as The Alchemist, and you’ll note they are not a wizard, as the pointy hat is not sticking upwards. The Alchemist comes around to describe things that are generally more advanced and/or tricky and additionally not usually needed, but for whatever reason they feel you should know about this thing that SQLAlchemy can do.

In this edition, towards the goal of having some interesting data in the address_table as well, below is a more advanced example illustrating how the Insert.values() method may be used explicitly while at the same time including for additional VALUES generated from the parameters. A scalar subquery is constructed, making use of the select() construct introduced in the next section, and the parameters used in the subquery are set up using an explicit bound parameter name, established using the bindparam() construct.

This is some slightly deeper alchemy just so that we can add related rows without fetching the primary key identifiers from the user_table operation into the application. Most Alchemists will simply use the ORM which takes care of things like this for us.

With that, we have some more interesting data in our tables that we will make use of in the upcoming sections.

A true “empty” INSERT that inserts only the “defaults” for a table without including any explicit values at all is generated if we indicate Insert.values() with no arguments; not every database backend supports this, but here’s what SQLite produces:

The RETURNING clause for supported backends is used automatically in order to retrieve the last inserted primary key value as well as the values for server defaults. However the RETURNING clause may also be specified explicitly using the Insert.returning() method; in this case, the Result object that’s returned when the statement is executed has rows which can be fetched:

It can also be combined with Insert.from_select(), as in the example below that builds upon the example stated in INSERT…FROM SELECT:

The RETURNING feature is also supported by UPDATE and DELETE statements, which will be introduced later in this tutorial.

For INSERT statements, the RETURNING feature may be used both for single-row statements as well as for statements that INSERT multiple rows at once. Support for multiple-row INSERT with RETURNING is dialect specific, however is supported for all the dialects that are included in SQLAlchemy which support RETURNING. See the section “Insert Many Values” Behavior for INSERT statements for background on this feature.

Bulk INSERT with or without RETURNING is also supported by the ORM. See ORM Bulk INSERT Statements for reference documentation.

A less used feature of Insert, but here for completeness, the Insert construct can compose an INSERT that gets rows directly from a SELECT using the Insert.from_select() method. This method accepts a select() construct, which is discussed in the next section, along with a list of column names to be targeted in the actual INSERT. In the example below, rows are added to the address table which are derived from rows in the user_account table, giving each user a free email address at aol.com:

This construct is used when one wants to copy data from some other part of the database directly into a new set of rows, without actually fetching and re-sending the data from the client.

Insert - in the SQL Expression API documentation

SQLAlchemy 1.4 / 2.0 Tutorial

Next Tutorial Section: Using SELECT Statements

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
>>> from sqlalchemy import insert
>>> stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants")
```

Example 2 (sql):
```sql
>>> print(stmt)
INSERT INTO user_account (name, fullname) VALUES (:name, :fullname)
```

Example 3 (unknown):
```unknown
>>> compiled = stmt.compile()
```

Example 4 (json):
```json
>>> compiled.params
{'name': 'spongebob', 'fullname': 'Spongebob Squarepants'}
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/core/engines.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Core
    - Project Versions
- Engine Configuration¶
- Supported Databases¶
- Database URLs¶
  - Escaping Special Characters such as @ signs in Passwords¶
  - Creating URLs Programmatically¶
  - Backend-Specific URLs¶

Home | Download this Documentation

Home | Download this Documentation

The Engine is the starting point for any SQLAlchemy application. It’s “home base” for the actual database and its DBAPI, delivered to the SQLAlchemy application through a connection pool and a Dialect, which describes how to talk to a specific kind of database/DBAPI combination.

The general structure can be illustrated as follows:

Where above, an Engine references both a Dialect and a Pool, which together interpret the DBAPI’s module functions as well as the behavior of the database.

Creating an engine is just a matter of issuing a single call, create_engine():

The above engine creates a Dialect object tailored towards PostgreSQL, as well as a Pool object which will establish a DBAPI connection at localhost:5432 when a connection request is first received. Note that the Engine and its underlying Pool do not establish the first actual DBAPI connection until the Engine.connect() or Engine.begin() methods are called. Either of these methods may also be invoked by other SQLAlchemy Engine dependent objects such as the ORM Session object when they first require database connectivity. In this way, Engine and Pool can be said to have a lazy initialization behavior.

The Engine, once created, can either be used directly to interact with the database, or can be passed to a Session object to work with the ORM. This section covers the details of configuring an Engine. The next section, Working with Engines and Connections, will detail the usage API of the Engine and similar, typically for non-ORM applications.

SQLAlchemy includes many Dialect implementations for various backends. Dialects for the most common databases are included with SQLAlchemy; a handful of others require an additional install of a separate dialect.

See the section Dialects for information on the various backends available.

The create_engine() function produces an Engine object based on a URL. The format of the URL generally follows RFC-1738, with some exceptions, including that underscores, not dashes or periods, are accepted within the “scheme” portion. URLs typically include username, password, hostname, database name fields, as well as optional keyword arguments for additional configuration. In some cases a file path is accepted, and in others a “data source name” replaces the “host” and “database” portions. The typical form of a database URL is:

Dialect names include the identifying name of the SQLAlchemy dialect, a name such as sqlite, mysql, postgresql, oracle, or mssql. The drivername is the name of the DBAPI to be used to connect to the database using all lowercase letters. If not specified, a “default” DBAPI will be imported if available - this default is typically the most widely known driver available for that backend.

When constructing a fully formed URL string to pass to create_engine(), special characters such as those that may be used in the user and password need to be URL encoded to be parsed correctly.. This includes the @ sign.

Below is an example of a URL that includes the password "kx@jj5/g", where the “at” sign and slash characters are represented as %40 and %2F, respectively:

The encoding for the above password can be generated using urllib.parse:

The URL may then be passed as a string to create_engine():

As an alternative to escaping special characters in order to create a complete URL string, the object passed to create_engine() may instead be an instance of the URL object, which bypasses the parsing phase and can accommodate for unescaped strings directly. See the next section for an example.

Changed in version 1.4: Support for @ signs in hostnames and database names has been fixed. As a side effect of this fix, @ signs in passwords must be escaped.

The value passed to create_engine() may be an instance of URL, instead of a plain string, which bypasses the need for string parsing to be used, and therefore does not need an escaped URL string to be provided.

The URL object is created using the URL.create() constructor method, passing all fields individually. Special characters such as those within passwords may be passed without any modification:

The constructed URL object may then be passed directly to create_engine() in place of a string argument:

Examples for common connection styles follow below. For a full index of detailed information on all included dialects as well as links to third-party dialects, see Dialects.

The PostgreSQL dialect uses psycopg2 as the default DBAPI. Other PostgreSQL DBAPIs include pg8000 and asyncpg:

More notes on connecting to PostgreSQL at PostgreSQL.

The MySQL dialect uses mysqlclient as the default DBAPI. There are other MySQL DBAPIs available, including PyMySQL:

More notes on connecting to MySQL at MySQL and MariaDB.

The preferred Oracle Database dialect uses the python-oracledb driver as the DBAPI:

For historical reasons, the Oracle dialect uses the obsolete cx_Oracle driver as the default DBAPI:

More notes on connecting to Oracle Database at Oracle.

The SQL Server dialect uses pyodbc as the default DBAPI. pymssql is also available:

More notes on connecting to SQL Server at Microsoft SQL Server.

SQLite connects to file-based databases, using the Python built-in module sqlite3 by default.

As SQLite connects to local files, the URL format is slightly different. The “file” portion of the URL is the filename of the database. For a relative file path, this requires three slashes:

And for an absolute file path, the three slashes are followed by the absolute path:

To use a SQLite :memory: database, specify an empty URL:

More notes on connecting to SQLite at SQLite.

See Dialects, the top-level page for all additional dialect documentation.

create_engine(url, **kwargs)

Create a new Engine instance.

create_mock_engine(url, executor, **kw)

Create a “mock” engine used for echoing DDL.

create_pool_from_url(url, **kwargs)

Create a pool instance from the given url.

engine_from_config(configuration[, prefix], **kwargs)

Create a new Engine instance using a configuration dictionary.

make_url(name_or_url)

Given a string, produce a new URL instance.

Represent the components of a URL used to connect to a database.

Create a new Engine instance.

The standard calling form is to send the URL as the first positional argument, usually a string that indicates database dialect and connection arguments:

Please review Database URLs for general guidelines in composing URL strings. In particular, special characters, such as those often part of passwords, must be URL encoded to be properly parsed.

Additional keyword arguments may then follow it which establish various options on the resulting Engine and its underlying Dialect and Pool constructs:

The string form of the URL is dialect[+driver]://user:password@host/dbname[?key=value..], where dialect is a database name such as mysql, oracle, postgresql, etc., and driver the name of a DBAPI, such as psycopg2, pyodbc, cx_oracle, etc. Alternatively, the URL can be an instance of URL.

**kwargs takes a wide variety of options which are routed towards their appropriate components. Arguments may be specific to the Engine, the underlying Dialect, as well as the Pool. Specific dialects also accept keyword arguments that are unique to that dialect. Here, we describe the parameters that are common to most create_engine() usage.

Once established, the newly resulting Engine will request a connection from the underlying Pool once Engine.connect() is called, or a method which depends on it such as Engine.execute() is invoked. The Pool in turn will establish the first actual DBAPI connection when this request is received. The create_engine() call itself does not establish any actual DBAPI connections directly.

Working with Engines and Connections

connect_args¶ – a dictionary of options which will be passed directly to the DBAPI’s connect() method as additional keyword arguments. See the example at Custom DBAPI connect() arguments / on-connect routines.

a callable which returns a DBAPI connection. This creation function will be passed to the underlying connection pool and will be used to create all new database connections. Usage of this function causes connection parameters specified in the URL argument to be bypassed.

This hook is not as flexible as the newer DialectEvents.do_connect() hook which allows complete control over how a connection is made to the database, given the full set of URL arguments and state beforehand.

DialectEvents.do_connect() - event hook that allows full control over DBAPI connection mechanics.

Custom DBAPI connect() arguments / on-connect routines

if True, the Engine will log all statements as well as a repr() of their parameter lists to the default log handler, which defaults to sys.stdout for output. If set to the string "debug", result rows will be printed to the standard output as well. The echo attribute of Engine can be modified at any time to turn logging on and off; direct control of logging is also available using the standard Python logging module.

Configuring Logging - further detail on how to configure logging.

if True, the connection pool will log informational output such as when connections are invalidated as well as when connections are recycled to the default log handler, which defaults to sys.stdout for output. If set to the string "debug", the logging will include pool checkouts and checkins. Direct control of logging is also available using the standard Python logging module.

Configuring Logging - further detail on how to configure logging.

empty_in_strategy¶ – No longer used; SQLAlchemy now uses “empty set” behavior for IN in all cases.

enable_from_linting¶ –

defaults to True. Will emit a warning if a given SELECT statement is found to have un-linked FROM elements which would cause a cartesian product.

Added in version 1.4.

Built-in FROM linting will warn for any potential cartesian products in a SELECT statement

execution_options¶ – Dictionary execution options which will be applied to all connections. See Connection.execution_options()

Use the 2.0 style Engine and Connection API.

As of SQLAlchemy 2.0, this parameter is present for backwards compatibility only and must remain at its default value of True.

The create_engine.future parameter will be deprecated in a subsequent 2.x release and eventually removed.

Added in version 1.4.

Changed in version 2.0: All Engine objects are “future” style engines and there is no longer a future=False mode of operation.

SQLAlchemy 2.0 - Major Migration Guide

Boolean, when set to True, SQL statement parameters will not be displayed in INFO logging nor will they be formatted into the string representation of StatementError objects.

Added in version 1.3.8.

Configuring Logging - further detail on how to configure logging.

implicit_returning=True¶ – Legacy parameter that may only be set to True. In SQLAlchemy 2.0, this parameter does nothing. In order to disable “implicit returning” for statements invoked by the ORM, configure this on a per-table basis using the Table.implicit_returning parameter.

insertmanyvalues_page_size¶ –

number of rows to format into an INSERT statement when the statement uses “insertmanyvalues” mode, which is a paged form of bulk insert that is used for many backends when using executemany execution typically in conjunction with RETURNING. Defaults to 1000, but may also be subject to dialect-specific limiting factors which may override this value on a per-statement basis.

Added in version 2.0.

“Insert Many Values” Behavior for INSERT statements

Controlling the Batch Size

Connection.execution_options.insertmanyvalues_page_size

optional string name of an isolation level which will be set on all new connections unconditionally. Isolation levels are typically some subset of the string names "SERIALIZABLE", "REPEATABLE READ", "READ COMMITTED", "READ UNCOMMITTED" and "AUTOCOMMIT" based on backend.

The create_engine.isolation_level parameter is in contrast to the Connection.execution_options.isolation_level execution option, which may be set on an individual Connection, as well as the same parameter passed to Engine.execution_options(), where it may be used to create multiple engines with different isolation levels that share a common connection pool and dialect.

Changed in version 2.0: The create_engine.isolation_level parameter has been generalized to work on all dialects which support the concept of isolation level, and is provided as a more succinct, up front configuration switch in contrast to the execution option which is more of an ad-hoc programmatic option.

Setting Transaction Isolation Levels including DBAPI Autocommit

for dialects that support the JSON datatype, this is a Python callable that will convert a JSON string to a Python object. By default, the Python json.loads function is used.

Changed in version 1.3.7: The SQLite dialect renamed this from _json_deserializer.

for dialects that support the JSON datatype, this is a Python callable that will render a given object as JSON. By default, the Python json.dumps function is used.

Changed in version 1.3.7: The SQLite dialect renamed this from _json_serializer.

optional integer value which limits the size of dynamically generated column labels to that many characters. If less than 6, labels are generated as “_(counter)”. If None, the value of dialect.max_identifier_length, which may be affected via the create_engine.max_identifier_length parameter, is used instead. The value of create_engine.label_length may not be larger than that of create_engine.max_identfier_length.

create_engine.max_identifier_length

String identifier which will be used within the “name” field of logging records generated within the “sqlalchemy.engine” logger. Defaults to a hexstring of the object’s id.

Configuring Logging - further detail on how to configure logging.

Connection.execution_options.logging_token

max_identifier_length¶ –

integer; override the max_identifier_length determined by the dialect. if None or zero, has no effect. This is the database’s configured maximum number of characters that may be used in a SQL identifier such as a table name, column name, or label name. All dialects determine this value automatically, however in the case of a new database version for which this value has changed but SQLAlchemy’s dialect has not been adjusted, the value may be passed here.

Added in version 1.3.9.

create_engine.label_length

max_overflow=10¶ – the number of connections to allow in connection pool “overflow”, that is connections that can be opened above and beyond the pool_size setting, which defaults to five. this is only used with QueuePool.

module=None¶ – reference to a Python module object (the module itself, not its string name). Specifies an alternate DBAPI module to be used by the engine’s dialect. Each sub-dialect references a specific DBAPI which will be imported before first connect. This parameter causes the import to be bypassed, and the given module to be used instead. Can be used for testing of DBAPIs as well as to inject “mock” DBAPI implementations into the Engine.

paramstyle=None¶ – The paramstyle to use when rendering bound parameters. This style defaults to the one recommended by the DBAPI itself, which is retrieved from the .paramstyle attribute of the DBAPI. However, most DBAPIs accept more than one paramstyle, and in particular it may be desirable to change a “named” paramstyle into a “positional” one, or vice versa. When this attribute is passed, it should be one of the values "qmark", "numeric", "named", "format" or "pyformat", and should correspond to a parameter style known to be supported by the DBAPI in use.

pool=None¶ – an already-constructed instance of Pool, such as a QueuePool instance. If non-None, this pool will be used directly as the underlying connection pool for the engine, bypassing whatever connection parameters are present in the URL argument. For information on constructing connection pools manually, see Connection Pooling.

poolclass=None¶ – a Pool subclass, which will be used to create a connection pool instance using the connection parameters given in the URL. Note this differs from pool in that you don’t actually instantiate the pool in this case, you just indicate what type of pool to be used.

String identifier which will be used within the “name” field of logging records generated within the “sqlalchemy.pool” logger. Defaults to a hexstring of the object’s id.

Configuring Logging - further detail on how to configure logging.

boolean, if True will enable the connection pool “pre-ping” feature that tests connections for liveness upon each checkout.

Added in version 1.2.

Disconnect Handling - Pessimistic

pool_size=5¶ – the number of connections to keep open inside the connection pool. This used with QueuePool as well as SingletonThreadPool. With QueuePool, a pool_size setting of 0 indicates no limit; to disable pooling, set poolclass to NullPool instead.

this setting causes the pool to recycle connections after the given number of seconds has passed. It defaults to -1, or no timeout. For example, setting to 3600 means connections will be recycled after one hour. Note that MySQL in particular will disconnect automatically if no activity is detected on a connection for eight hours (although this is configurable with the MySQLDB connection itself and the server configuration as well).

pool_reset_on_return='rollback'¶ –

set the Pool.reset_on_return parameter of the underlying Pool object, which can be set to the values "rollback", "commit", or None.

Fully preventing ROLLBACK calls under autocommit - a more modern approach to using connections with no transactional instructions

number of seconds to wait before giving up on getting a connection from the pool. This is only used with QueuePool. This can be a float but is subject to the limitations of Python time functions which may not be reliable in the tens of milliseconds.

pool_use_lifo=False¶ –

use LIFO (last-in-first-out) when retrieving connections from QueuePool instead of FIFO (first-in-first-out). Using LIFO, a server-side timeout scheme can reduce the number of connections used during non- peak periods of use. When planning for server-side timeouts, ensure that a recycle or pre-ping strategy is in use to gracefully handle stale connections.

Added in version 1.3.

Dealing with Disconnects

string list of plugin names to load. See CreateEnginePlugin for background.

Added in version 1.2.3.

size of the cache used to cache the SQL string form of queries. Set to zero to disable caching.

The cache is pruned of its least recently used items when its size reaches N * 1.5. Defaults to 500, meaning the cache will always store at least 500 SQL statements when filled, and will grow up to 750 items at which point it is pruned back down to 500 by removing the 250 least recently used items.

Caching is accomplished on a per-statement basis by generating a cache key that represents the statement’s structure, then generating string SQL for the current dialect only if that key is not present in the cache. All statements support caching, however some features such as an INSERT with a large set of parameters will intentionally bypass the cache. SQL logging will indicate statistics for each statement whether or not it were pull from the cache.

some ORM functions related to unit-of-work persistence as well as some attribute loading strategies will make use of individual per-mapper caches outside of the main cache.

SQL Compilation Caching

Added in version 1.4.

skip_autocommit_rollback¶ –

When True, the dialect will unconditionally skip all calls to the DBAPI connection.rollback() method if the DBAPI connection is confirmed to be in “autocommit” mode. The availability of this feature is dialect specific; if not available, a NotImplementedError is raised by the dialect when rollback occurs.

Fully preventing ROLLBACK calls under autocommit

Added in version 2.0.43.

use_insertmanyvalues¶ –

True by default, use the “insertmanyvalues” execution style for INSERT..RETURNING statements by default.

Added in version 2.0.

“Insert Many Values” Behavior for INSERT statements

Create a new Engine instance using a configuration dictionary.

The dictionary is typically produced from a config file.

The keys of interest to engine_from_config() should be prefixed, e.g. sqlalchemy.url, sqlalchemy.echo, etc. The ‘prefix’ argument indicates the prefix to be searched for. Each matching key (after the prefix is stripped) is treated as though it were the corresponding keyword argument to a create_engine() call.

The only required key is (assuming the default prefix) sqlalchemy.url, which provides the database URL.

A select set of keyword arguments will be “coerced” to their expected type based on string values. The set of arguments is extensible per-dialect using the engine_config_types accessor.

configuration¶ – A dictionary (typically produced from a config file, but this is not a requirement). Items whose keys start with the value of ‘prefix’ will have that prefix stripped, and will then be passed to create_engine().

prefix¶ – Prefix to match and then strip from keys in ‘configuration’.

kwargs¶ – Each keyword argument to engine_from_config() itself overrides the corresponding item taken from the ‘configuration’ dictionary. Keyword arguments should not be prefixed.

Create a “mock” engine used for echoing DDL.

This is a utility function used for debugging or storing the output of DDL sequences as generated by MetaData.create_all() and related methods.

The function accepts a URL which is used only to determine the kind of dialect to be used, as well as an “executor” callable function which will receive a SQL expression object and parameters, which can then be echoed or otherwise printed. The executor’s return value is not handled, nor does the engine allow regular string statements to be invoked, and is therefore only useful for DDL that is sent to the database without receiving any results.

url¶ – A string URL which typically needs to contain only the database backend name.

executor¶ – a callable which receives the arguments sql, *multiparams and **params. The sql parameter is typically an instance of ExecutableDDLElement, which can then be compiled into a string using ExecutableDDLElement.compile().

Added in version 1.4: - the create_mock_engine() function replaces the previous “mock” engine strategy used with create_engine().

How can I get the CREATE TABLE/ DROP TABLE output as a string?

Given a string, produce a new URL instance.

The format of the URL generally follows RFC-1738, with some exceptions, including that underscores, and not dashes or periods, are accepted within the “scheme” portion.

If a URL object is passed, it is returned as is.

Create a pool instance from the given url.

If poolclass is not provided the pool class used is selected using the dialect specified in the URL.

The arguments passed to create_pool_from_url() are identical to the pool argument passed to the create_engine() function.

Added in version 2.0.10.

inherits from builtins.tuple

Represent the components of a URL used to connect to a database.

URLs are typically constructed from a fully formatted URL string, where the make_url() function is used internally by the create_engine() function in order to parse the URL string into its individual components, which are then used to construct a new URL object. When parsing from a formatted URL string, the parsing format generally follows RFC-1738, with some exceptions.

A URL object may also be produced directly, either by using the make_url() function with a fully formed URL string, or by using the URL.create() constructor in order to construct a URL programmatically given individual fields. The resulting URL object may be passed directly to create_engine() in place of a string argument, which will bypass the usage of make_url() within the engine’s creation process.

Changed in version 1.4: The URL object is now an immutable object. To create a URL, use the make_url() or URL.create() function / method. To modify a URL, use methods like URL.set() and URL.update_query_dict() to return a new URL object with modifications. See notes for this change at The URL object is now immutable.

URL contains the following attributes:

URL.drivername: database backend and driver name, such as postgresql+psycopg2

URL.username: username string

URL.password: password string

URL.host: string hostname

URL.port: integer port number

URL.database: string database name

URL.query: an immutable mapping representing the query string. contains strings for keys and either strings or tuples of strings for values.

Create a new URL object.

difference_update_query()

Remove the given names from the URL.query dictionary, returning the new URL.

database backend and driver name, such as postgresql+psycopg2

Return the backend name.

Return the SQLAlchemy Dialect class corresponding to this URL’s driver name.

Return the backend name.

hostname or IP number. May also be a data source name for some drivers.

password, which is normally a string but may also be any object that has a __str__() method.

an immutable mapping representing the query string. contains strings for keys and either strings or tuples of strings for values, e.g.:

Render this URL object as a string.

return a new URL object with modifications.

translate_connect_args()

Translate url attributes into a dictionary of connection arguments.

Return a new URL object with the URL.query parameter dictionary updated by the given dictionary.

Return a new URL object with the URL.query parameter dictionary updated by the given sequence of key/value pairs

update_query_string()

Return a new URL object with the URL.query parameter dictionary updated by the given query string.

Create a new URL object.

drivername¶ – the name of the database backend. This name will correspond to a module in sqlalchemy/databases or a third party plug-in.

username¶ – The user name.

database password. Is typically a string, but may also be an object that can be stringified with str().

The password string should not be URL encoded when passed as an argument to URL.create(); the string should contain the password characters exactly as they would be typed.

A password-producing object will be stringified only once per Engine object. For dynamic password generation per connect, see Generating dynamic authentication tokens.

host¶ – The name of the host.

port¶ – The port number.

database¶ – The database name.

query¶ – A dictionary of string keys to string values to be passed to the dialect and/or the DBAPI upon connect. To specify non-string parameters to a Python DBAPI directly, use the create_engine.connect_args parameter to create_engine(). See also URL.normalized_query for a dictionary that is consistently string->list of string.

Added in version 1.4: The URL object is now an immutable named tuple. In addition, the query dictionary is also immutable. To create a URL, use the make_url() or URL.create() function/ method. To modify a URL, use the URL.set() and URL.update_query() methods.

Remove the given names from the URL.query dictionary, returning the new URL.

Equivalent to using URL.set() as follows:

Added in version 1.4.

URL.update_query_dict()

database backend and driver name, such as postgresql+psycopg2

Return the backend name.

This is the name that corresponds to the database backend in use, and is the portion of the URL.drivername that is to the left of the plus sign.

Return the SQLAlchemy Dialect class corresponding to this URL’s driver name.

Return the backend name.

This is the name that corresponds to the DBAPI driver in use, and is the portion of the URL.drivername that is to the right of the plus sign.

If the URL.drivername does not include a plus sign, then the default Dialect for this URL is imported in order to get the driver name.

hostname or IP number. May also be a data source name for some drivers.

Return the URL.query dictionary with values normalized into sequences.

As the URL.query dictionary may contain either string values or sequences of string values to differentiate between parameters that are specified multiple times in the query string, code that needs to handle multiple parameters generically will wish to use this attribute so that all parameters present are presented as sequences. Inspiration is from Python’s urllib.parse.parse_qs function. E.g.:

password, which is normally a string but may also be any object that has a __str__() method.

an immutable mapping representing the query string. contains strings for keys and either strings or tuples of strings for values, e.g.:

URL.normalized_query - normalizes all values into sequences for consistent processing

Methods for altering the contents of URL.query:

URL.update_query_dict()

URL.update_query_string()

URL.update_query_pairs()

URL.difference_update_query()

Render this URL object as a string.

This method is used when the __str__() or __repr__() methods are used. The method directly includes additional options.

hide_password¶ – Defaults to True. The password is not shown in the string unless this is set to False.

return a new URL object with modifications.

Values are used if they are non-None. To set a value to None explicitly, use the URL._replace() method adapted from namedtuple.

drivername¶ – new drivername

username¶ – new username

password¶ – new password

query¶ – new query parameters, passed a dict of string keys referring to string or sequence of string values. Fully replaces the previous list of arguments.

Added in version 1.4.

URL.update_query_dict()

Translate url attributes into a dictionary of connection arguments.

Returns attributes of this url (host, database, username, password, port) as a plain dictionary. The attribute names are used as the keys by default. Unset or false attributes are omitted from the final dictionary.

**kw¶ – Optional, alternate key names for url attributes.

names¶ – Deprecated. Same purpose as the keyword-based alternate names, but correlates the name to the original positionally.

Return a new URL object with the URL.query parameter dictionary updated by the given dictionary.

The dictionary typically contains string keys and string values. In order to represent a query parameter that is expressed multiple times, pass a sequence of string values.

query_parameters¶ – A dictionary with string keys and values that are either strings, or sequences of strings.

append¶ – if True, parameters in the existing query string will not be removed; new parameters will be in addition to those present. If left at its default of False, keys present in the given query parameters will replace those of the existing query string.

Added in version 1.4.

URL.update_query_string()

URL.update_query_pairs()

URL.difference_update_query()

Return a new URL object with the URL.query parameter dictionary updated by the given sequence of key/value pairs

key_value_pairs¶ – A sequence of tuples containing two strings each.

append¶ – if True, parameters in the existing query string will not be removed; new parameters will be in addition to those present. If left at its default of False, keys present in the given query parameters will replace those of the existing query string.

Added in version 1.4.

URL.difference_update_query()

Return a new URL object with the URL.query parameter dictionary updated by the given query string.

query_string¶ – a URL escaped query string, not including the question mark.

append¶ – if True, parameters in the existing query string will not be removed; new parameters will be in addition to those present. If left at its default of False, keys present in the given query parameters will replace those of the existing query string.

Added in version 1.4.

URL.update_query_dict()

The Engine will ask the connection pool for a connection when the connect() or execute() methods are called. The default connection pool, QueuePool, will open connections to the database on an as-needed basis. As concurrent statements are executed, QueuePool will grow its pool of connections to a default size of five, and will allow a default “overflow” of ten. Since the Engine is essentially “home base” for the connection pool, it follows that you should keep a single Engine per database established within an application, rather than creating a new one for each connection.

QueuePool is not used by default for SQLite engines. See SQLite for details on SQLite connection pool usage.

For more information on connection pooling, see Connection Pooling.

For cases where special connection methods are needed, in the vast majority of cases, it is most appropriate to use one of several hooks at the create_engine() level in order to customize this process. These are described in the following sub-sections.

All Python DBAPIs accept additional arguments beyond the basics of connecting. Common parameters include those to specify character set encodings and timeout values; more complex data includes special DBAPI constants and objects and SSL sub-parameters. There are two rudimentary means of passing these arguments without complexity.

Simple string values, as well as some numeric values and boolean flags, may be often specified in the query string of the URL directly. A common example of this is DBAPIs that accept an argument encoding for character encodings, such as most MySQL DBAPIs:

The advantage of using the query string is that additional DBAPI options may be specified in configuration files in a manner that’s portable to the DBAPI specified in the URL. The specific parameters passed through at this level vary by SQLAlchemy dialect. Some dialects pass all arguments through as strings, while others will parse for specific datatypes and move parameters to different places, such as into driver-level DSNs and connect strings. As per-dialect behavior in this area currently varies, the dialect documentation should be consulted for the specific dialect in use to see if particular parameters are supported at this level.

A general technique to display the exact arguments passed to the DBAPI for a given URL may be performed using the Dialect.create_connect_args() method directly as follows:

The above args, kwargs pair is normally passed to the DBAPI as dbapi.connect(*args, **kwargs).

A more general system of passing any parameter to the dbapi.connect() function that is guaranteed to pass all parameters at all times is the create_engine.connect_args dictionary parameter. This may be used for parameters that are otherwise not handled by the dialect when added to the query string, as well as when special sub-structures or objects must be passed to the DBAPI. Sometimes it’s just that a particular flag must be sent as the True symbol and the SQLAlchemy dialect is not aware of this keyword argument to coerce it from its string form as presented in the URL. Below illustrates the use of a psycopg2 “connection factory” that replaces the underlying implementation the connection:

Another example is the pyodbc “timeout” parameter:

The above example also illustrates that both URL “query string” parameters as well as create_engine.connect_args may be used at the same time; in the case of pyodbc, the “driver” keyword has special meaning within the URL.

Beyond manipulating the parameters passed to connect(), we can further customize how the DBAPI connect() function itself is called using the DialectEvents.do_connect() event hook. This hook is passed the full *args, **kwargs that the dialect would send to connect(). These collections can then be modified in place to alter how they are used:

DialectEvents.do_connect() is also an ideal way to dynamically insert an authentication token that might change over the lifespan of an Engine. For example, if the token gets generated by get_authentication_token() and passed to the DBAPI in a token parameter, this could be implemented as:

Connecting to databases with access tokens - a more concrete example involving SQL Server

For a DBAPI connection that SQLAlchemy creates without issue, but where we would like to modify the completed connection before it’s actually used, such as for setting special flags or running certain commands, the PoolEvents.connect() event hook is the most appropriate hook. This hook is called for every new connection created, before it is used by SQLAlchemy:

Finally, the DialectEvents.do_connect() event hook can also allow us to take over the connection process entirely by establishing the connection and returning it:

The DialectEvents.do_connect() hook supersedes the previous create_engine.creator hook, which remains available. DialectEvents.do_connect() has the distinct advantage that the complete arguments parsed from the URL are also passed to the user-defined function which is not the case with create_engine.creator.

Python’s standard logging module is used to implement informational and debug log output with SQLAlchemy. This allows SQLAlchemy’s logging to integrate in a standard way with other applications and libraries. There are also two parameters create_engine.echo and create_engine.echo_pool present on create_engine() which allow immediate logging to sys.stdout for the purposes of local development; these parameters ultimately interact with the regular Python loggers described below.

This section assumes familiarity with the above linked logging module. All logging performed by SQLAlchemy exists underneath the sqlalchemy namespace, as used by logging.getLogger('sqlalchemy'). When logging has been configured (i.e. such as via logging.basicConfig()), the general namespace of SA loggers that can be turned on is as follows:

sqlalchemy.engine - controls SQL echoing. Set to logging.INFO for SQL query output, logging.DEBUG for query + result set output. These settings are equivalent to echo=True and echo="debug" on create_engine.echo, respectively.

sqlalchemy.pool - controls connection pool logging. Set to logging.INFO to log connection invalidation and recycle events; set to logging.DEBUG to additionally log all pool checkins and checkouts. These settings are equivalent to pool_echo=True and pool_echo="debug" on create_engine.echo_pool, respectively.

sqlalchemy.dialects - controls custom logging for SQL dialects, to the extent that logging is used within specific dialects, which is generally minimal.

sqlalchemy.orm - controls logging of various ORM functions to the extent that logging is used within the ORM, which is generally minimal. Set to logging.INFO to log some top-level information on mapper configurations.

For example, to log SQL queries using Python logging instead of the echo=True flag:

By default, the log level is set to logging.WARN within the entire sqlalchemy namespace so that no log operations occur, even within an application that has logging enabled otherwise.

The SQLAlchemy Engine conserves Python function call overhead by only emitting log statements when the current logging level is detected as logging.INFO or logging.DEBUG. It only checks this level when a new connection is procured from the connection pool. Therefore when changing the logging configuration for an already-running application, any Connection that’s currently active, or more commonly a Session object that’s active in a transaction, won’t log any SQL according to the new configuration until a new Connection is procured (in the case of Session, this is after the current transaction ends and a new one begins).

As mentioned previously, the create_engine.echo and create_engine.echo_pool parameters are a shortcut to immediate logging to sys.stdout:

Use of these flags is roughly equivalent to:

It’s important to note that these two flags work independently of any existing logging configuration, and will make use of logging.basicConfig() unconditionally. This has the effect of being configured in addition to any existing logger configurations. Therefore, when configuring logging explicitly, ensure all echo flags are set to False at all times, to avoid getting duplicate log lines.

The logger name for Engine or Pool is set to be the module-qualified class name of the object. This name can be further qualified with an additional name using the create_engine.logging_name and create_engine.pool_logging_name parameters with sqlalchemy.create_engine(); the name will be appended to existing class-qualified logging name. This use is recommended for applications that make use of multiple global Engine instances simultaneously, so that they may be distinguished in logging:

The create_engine.logging_name and create_engine.pool_logging_name parameters may also be used in conjunction with create_engine.echo and create_engine.echo_pool. However, an unavoidable double logging condition will occur if other engines are created with echo flags set to True and no logging name. This is because a handler will be added automatically for sqlalchemy.engine.Engine which will log messages both for the name-less engine as well as engines with logging names. For example:

The above scenario will double log SELECT 3. To resolve, ensure all engines have a logging_name set, or use explicit logger / handler setup without using create_engine.echo and create_engine.echo_pool.

Added in version 1.4.0b2.

While the logging name is appropriate to establish on an Engine object that is long lived, it’s not flexible enough to accommodate for an arbitrarily large list of names, for the case of tracking individual connections and/or transactions in log messages.

For this use case, the log message itself generated by the Connection and Result objects may be augmented with additional tokens such as transaction or request identifiers. The Connection.execution_options.logging_token parameter accepts a string argument that may be used to establish per-connection tracking tokens:

The Connection.execution_options.logging_token parameter may also be established on engines or sub-engines via create_engine.execution_options or Engine.execution_options(). This may be useful to apply different logging tokens to different components of an application without creating new engines:

The logging emitted by Engine also indicates an excerpt of the SQL parameters that are present for a particular statement. To prevent these parameters from being logged for privacy purposes, enable the create_engine.hide_parameters flag:

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://scott:tiger@localhost:5432/mydatabase")
```

Example 2 (python):
```python
dialect+driver://username:password@host:port/database
```

Example 3 (python):
```python
postgresql+pg8000://dbuser:kx%40jj5%2Fg@pghost10/appdb
```

Example 4 (python):
```python
>>> import urllib.parse
>>> urllib.parse.quote_plus("kx@jj5/g")
'kx%40jj5%2Fg'
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/core/ddl.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Core
    - Project Versions
- Customizing DDL¶
- Custom DDL¶
- Controlling DDL Sequences¶
- Using the built-in DDLElement Classes¶
- Controlling DDL Generation of Constraints and Indexes¶
- DDL Expression Constructs API¶

Home | Download this Documentation

Home | Download this Documentation

In the preceding sections we’ve discussed a variety of schema constructs including Table, ForeignKeyConstraint, CheckConstraint, and Sequence. Throughout, we’ve relied upon the create() and create_all() methods of Table and MetaData in order to issue data definition language (DDL) for all constructs. When issued, a pre-determined order of operations is invoked, and DDL to create each table is created unconditionally including all constraints and other objects associated with it. For more complex scenarios where database-specific DDL is required, SQLAlchemy offers two techniques which can be used to add any DDL based on any condition, either accompanying the standard generation of tables or by itself.

Custom DDL phrases are most easily achieved using the DDL construct. This construct works like all the other DDL elements except it accepts a string which is the text to be emitted:

A more comprehensive method of creating libraries of DDL constructs is to use custom compilation - see Custom SQL Constructs and Compilation Extension for details.

The DDL construct introduced previously also has the ability to be invoked conditionally based on inspection of the database. This feature is available using the ExecutableDDLElement.execute_if() method. For example, if we wanted to create a trigger but only on the PostgreSQL backend, we could invoke this as:

The ExecutableDDLElement.execute_if.dialect keyword also accepts a tuple of string dialect names:

The ExecutableDDLElement.execute_if() method can also work against a callable function that will receive the database connection in use. In the example below, we use this to conditionally create a CHECK constraint, first looking within the PostgreSQL catalogs to see if it exists:

The sqlalchemy.schema package contains SQL expression constructs that provide DDL expressions, all of which extend from the common base ExecutableDDLElement. For example, to produce a CREATE TABLE statement, one can use the CreateTable construct:

Above, the CreateTable construct works like any other expression construct (such as select(), table.insert(), etc.). All of SQLAlchemy’s DDL oriented constructs are subclasses of the ExecutableDDLElement base class; this is the base of all the objects corresponding to CREATE and DROP as well as ALTER, not only in SQLAlchemy but in Alembic Migrations as well. A full reference of available constructs is in DDL Expression Constructs API.

User-defined DDL constructs may also be created as subclasses of ExecutableDDLElement itself. The documentation in Custom SQL Constructs and Compilation Extension has several examples of this.

Added in version 2.0.

While the previously mentioned ExecutableDDLElement.execute_if() method is useful for custom DDL classes which need to invoke conditionally, there is also a common need for elements that are typically related to a particular Table, namely constraints and indexes, to also be subject to “conditional” rules, such as an index that includes features that are specific to a particular backend such as PostgreSQL or SQL Server. For this use case, the Constraint.ddl_if() and Index.ddl_if() methods may be used against constructs such as CheckConstraint, UniqueConstraint and Index, accepting the same arguments as the ExecutableDDLElement.execute_if() method in order to control whether or not their DDL will be emitted in terms of their parent Table object. These methods may be used inline when creating the definition for a Table (or similarly, when using the __table_args__ collection in an ORM declarative mapping), such as:

In the above example, the Table construct refers to both an Index and a CheckConstraint construct, both which indicate .ddl_if(dialect="postgresql"), which indicates that these elements will be included in the CREATE TABLE sequence only against the PostgreSQL dialect. If we run meta.create_all() against the SQLite dialect, for example, neither construct will be included:

However, if we run the same commands against a PostgreSQL database, we will see inline DDL for the CHECK constraint as well as a separate CREATE statement emitted for the index:

The Constraint.ddl_if() and Index.ddl_if() methods create an event hook that may be consulted not just at DDL execution time, as is the behavior with ExecutableDDLElement.execute_if(), but also within the SQL compilation phase of the CreateTable object, which is responsible for rendering the CHECK (num > 5) DDL inline within the CREATE TABLE statement. As such, the event hook that is received by the ddl_if.callable_() parameter has a richer argument set present, including that there is a dialect keyword argument passed, as well as an instance of DDLCompiler via the compiler keyword argument for the “inline rendering” portion of the sequence. The bind argument is not present when the event is triggered within the DDLCompiler sequence, so a modern event hook that wishes to inspect the database versioning information would best use the given Dialect object, such as to test PostgreSQL versioning:

Base class for DDL constructs that represent CREATE and DROP or equivalents.

Represent an ALTER TABLE ADD CONSTRAINT statement.

The root of DDL constructs, including those that are sub-elements within the “create table” and other processes.

Represent a Column as rendered in a CREATE TABLE statement, via the CreateTable construct.

Represent a CREATE INDEX statement.

Represent a CREATE SCHEMA statement.

Represent a CREATE SEQUENCE statement.

Represent a CREATE TABLE statement.

A literal DDL statement.

Represent an ALTER TABLE DROP CONSTRAINT statement.

Represent a DROP INDEX statement.

Represent a DROP SCHEMA statement.

Represent a DROP SEQUENCE statement.

Represent a DROP TABLE statement.

Base class for standalone executable DDL expression constructs.

sort_tables(tables[, skip_fn, extra_dependencies])

Sort a collection of Table objects based on dependency.

sort_tables_and_constraints(tables[, filter_fn, extra_dependencies, _warn_for_cycles])

Sort a collection of Table / ForeignKeyConstraint objects.

Sort a collection of Table objects based on dependency.

This is a dependency-ordered sort which will emit Table objects such that they will follow their dependent Table objects. Tables are dependent on another based on the presence of ForeignKeyConstraint objects as well as explicit dependencies added by Table.add_is_dependent_on().

The sort_tables() function cannot by itself accommodate automatic resolution of dependency cycles between tables, which are usually caused by mutually dependent foreign key constraints. When these cycles are detected, the foreign keys of these tables are omitted from consideration in the sort. A warning is emitted when this condition occurs, which will be an exception raise in a future release. Tables which are not part of the cycle will still be returned in dependency order.

To resolve these cycles, the ForeignKeyConstraint.use_alter parameter may be applied to those constraints which create a cycle. Alternatively, the sort_tables_and_constraints() function will automatically return foreign key constraints in a separate collection when cycles are detected so that they may be applied to a schema separately.

Changed in version 1.3.17: - a warning is emitted when sort_tables() cannot perform a proper sort due to cyclical dependencies. This will be an exception in a future release. Additionally, the sort will continue to return other tables not involved in the cycle in dependency order which was not the case previously.

tables¶ – a sequence of Table objects.

skip_fn¶ – optional callable which will be passed a ForeignKeyConstraint object; if it returns True, this constraint will not be considered as a dependency. Note this is different from the same parameter in sort_tables_and_constraints(), which is instead passed the owning ForeignKeyConstraint object.

extra_dependencies¶ – a sequence of 2-tuples of tables which will also be considered as dependent on each other.

sort_tables_and_constraints()

MetaData.sorted_tables - uses this function to sort

Sort a collection of Table / ForeignKeyConstraint objects.

This is a dependency-ordered sort which will emit tuples of (Table, [ForeignKeyConstraint, ...]) such that each Table follows its dependent Table objects. Remaining ForeignKeyConstraint objects that are separate due to dependency rules not satisfied by the sort are emitted afterwards as (None, [ForeignKeyConstraint ...]).

Tables are dependent on another based on the presence of ForeignKeyConstraint objects, explicit dependencies added by Table.add_is_dependent_on(), as well as dependencies stated here using the sort_tables_and_constraints.skip_fn and/or sort_tables_and_constraints.extra_dependencies parameters.

tables¶ – a sequence of Table objects.

filter_fn¶ – optional callable which will be passed a ForeignKeyConstraint object, and returns a value based on whether this constraint should definitely be included or excluded as an inline constraint, or neither. If it returns False, the constraint will definitely be included as a dependency that cannot be subject to ALTER; if True, it will only be included as an ALTER result at the end. Returning None means the constraint is included in the table-based result unless it is detected as part of a dependency cycle.

extra_dependencies¶ – a sequence of 2-tuples of tables which will also be considered as dependent on each other.

inherits from sqlalchemy.sql.expression.ClauseElement

The root of DDL constructs, including those that are sub-elements within the “create table” and other processes.

Added in version 2.0.

inherits from sqlalchemy.sql.roles.DDLRole, sqlalchemy.sql.expression.Executable, sqlalchemy.schema.BaseDDLElement

Base class for standalone executable DDL expression constructs.

This class is the base for the general purpose DDL class, as well as the various create/drop clause constructs such as CreateTable, DropTable, AddConstraint, etc.

Changed in version 2.0: ExecutableDDLElement is renamed from DDLElement, which still exists for backwards compatibility.

ExecutableDDLElement integrates closely with SQLAlchemy events, introduced in Events. An instance of one is itself an event receiving callable:

Controlling DDL Sequences

Execute the DDL as a ddl_listener.

Return a copy of this ExecutableDDLElement which will include the given target.

Return a callable that will execute this ExecutableDDLElement conditionally within an event handler.

Execute the DDL as a ddl_listener.

Return a copy of this ExecutableDDLElement which will include the given target.

This essentially applies the given item to the .target attribute of the returned ExecutableDDLElement object. This target is then usable by event handlers and compilation routines in order to provide services such as tokenization of a DDL string in terms of a particular Table.

When a ExecutableDDLElement object is established as an event handler for the DDLEvents.before_create() or DDLEvents.after_create() events, and the event then occurs for a given target such as a Constraint or Table, that target is established with a copy of the ExecutableDDLElement object using this method, which then proceeds to the ExecutableDDLElement.execute() method in order to invoke the actual DDL instruction.

target¶ – a SchemaItem that will be the subject of a DDL operation.

a copy of this ExecutableDDLElement with the .target attribute assigned to the given SchemaItem.

DDL - uses tokenization against the “target” when processing the DDL string.

Return a callable that will execute this ExecutableDDLElement conditionally within an event handler.

Used to provide a wrapper for event listening:

May be a string or tuple of strings. If a string, it will be compared to the name of the executing database dialect:

If a tuple, specifies multiple dialect names:

A callable, which will be invoked with three positional arguments as well as optional keyword arguments:

The Table or MetaData object which is the target of this event. May be None if the DDL is executed explicitly.

The Connection being used for DDL execution. May be None if this construct is being created inline within a table, in which case compiler will be present.

Optional keyword argument - a list of Table objects which are to be created/ dropped within a MetaData.create_all() or drop_all() method call.

keyword argument, but always present - the Dialect involved in the operation.

keyword argument. Will be None for an engine level DDL invocation, but will refer to a DDLCompiler if this DDL element is being created inline within a table.

Optional keyword argument - will be the state argument passed to this function.

Keyword argument, will be True if the ‘checkfirst’ flag was set during the call to create(), create_all(), drop(), drop_all().

If the callable returns a True value, the DDL statement will be executed.

state¶ – any value which will be passed to the callable_ as the state keyword argument.

inherits from sqlalchemy.schema.ExecutableDDLElement

A literal DDL statement.

Specifies literal SQL DDL to be executed by the database. DDL objects function as DDL event listeners, and can be subscribed to those events listed in DDLEvents, using either Table or MetaData objects as targets. Basic templating support allows a single DDL instance to handle repetitive tasks for multiple tables.

When operating on Table events, the following statement string substitutions are available:

The DDL’s “context”, if any, will be combined with the standard substitutions noted above. Keys present in the context will override the standard substitutions.

Create a DDL statement.

Create a DDL statement.

A string or unicode string to be executed. Statements will be processed with Python’s string formatting operator using a fixed set of string substitutions, as well as additional substitutions provided by the optional DDL.context parameter.

A literal ‘%’ in a statement must be escaped as ‘%%’.

SQL bind parameters are not available in DDL statements.

context¶ – Optional dictionary, defaults to None. These values will be available for use in string substitutions on the DDL statement.

inherits from sqlalchemy.schema.ExecutableDDLElement, typing.Generic

Base class for DDL constructs that represent CREATE and DROP or equivalents.

The common theme of _CreateDropBase is a single element attribute which refers to the element to be created or dropped.

inherits from sqlalchemy.schema._CreateBase

Represent a CREATE TABLE statement.

Create a CreateTable construct.

Create a CreateTable construct.

element¶ – a Table that’s the subject of the CREATE

on¶ – See the description for ‘on’ in DDL.

include_foreign_key_constraints¶ – optional sequence of ForeignKeyConstraint objects that will be included inline within the CREATE construct; if omitted, all foreign key constraints that do not specify use_alter=True are included.

if True, an IF NOT EXISTS operator will be applied to the construct.

Added in version 1.4.0b2.

inherits from sqlalchemy.schema._DropBase

Represent a DROP TABLE statement.

Create a DropTable construct.

Create a DropTable construct.

element¶ – a Table that’s the subject of the DROP.

on¶ – See the description for ‘on’ in DDL.

if True, an IF EXISTS operator will be applied to the construct.

Added in version 1.4.0b2.

inherits from sqlalchemy.schema.BaseDDLElement

Represent a Column as rendered in a CREATE TABLE statement, via the CreateTable construct.

This is provided to support custom column DDL within the generation of CREATE TABLE statements, by using the compiler extension documented in Custom SQL Constructs and Compilation Extension to extend CreateColumn.

Typical integration is to examine the incoming Column object, and to redirect compilation if a particular flag or condition is found:

The above construct can be applied to a Table as follows:

Above, the directives we’ve added to the Column.info collection will be detected by our custom compilation scheme:

The CreateColumn construct can also be used to skip certain columns when producing a CREATE TABLE. This is accomplished by creating a compilation rule that conditionally returns None. This is essentially how to produce the same effect as using the system=True argument on Column, which marks a column as an implicitly-present “system” column.

For example, suppose we wish to produce a Table which skips rendering of the PostgreSQL xmin column against the PostgreSQL backend, but on other backends does render it, in anticipation of a triggered rule. A conditional compilation rule could skip this name only on PostgreSQL:

Above, a CreateTable construct will generate a CREATE TABLE which only includes the id column in the string; the xmin column will be omitted, but only against the PostgreSQL backend.

inherits from sqlalchemy.schema._CreateBase

Represent a CREATE SEQUENCE statement.

inherits from sqlalchemy.schema._DropBase

Represent a DROP SEQUENCE statement.

inherits from sqlalchemy.schema._CreateBase

Represent a CREATE INDEX statement.

Create a Createindex construct.

Create a Createindex construct.

element¶ – a Index that’s the subject of the CREATE.

if True, an IF NOT EXISTS operator will be applied to the construct.

Added in version 1.4.0b2.

inherits from sqlalchemy.schema._DropBase

Represent a DROP INDEX statement.

Create a DropIndex construct.

Create a DropIndex construct.

element¶ – a Index that’s the subject of the DROP.

if True, an IF EXISTS operator will be applied to the construct.

Added in version 1.4.0b2.

inherits from sqlalchemy.schema._CreateBase

Represent an ALTER TABLE ADD CONSTRAINT statement.

Construct a new AddConstraint construct.

Construct a new AddConstraint construct.

element¶ – a Constraint object

isolate_from_table¶ –

optional boolean, defaults to True. Has the effect of the incoming constraint being isolated from being included in a CREATE TABLE sequence when associated with a Table.

Added in version 2.0.39: - added AddConstraint.isolate_from_table, defaulting to True. Previously, the behavior of this parameter was implicitly turned on in all cases.

inherits from sqlalchemy.schema._DropBase

Represent an ALTER TABLE DROP CONSTRAINT statement.

Construct a new DropConstraint construct.

Construct a new DropConstraint construct.

element¶ – a Constraint object

cascade¶ – optional boolean, indicates backend-specific “CASCADE CONSTRAINT” directive should be rendered if available

if_exists¶ – optional boolean, indicates backend-specific “IF EXISTS” directive should be rendered if available

isolate_from_table¶ –

optional boolean, defaults to True. Has the effect of the incoming constraint being isolated from being included in a CREATE TABLE sequence when associated with a Table.

Added in version 2.0.39: - added DropConstraint.isolate_from_table, defaulting to True. Previously, the behavior of this parameter was implicitly turned on in all cases.

inherits from sqlalchemy.schema._CreateBase

Represent a CREATE SCHEMA statement.

The argument here is the string name of the schema.

Create a new CreateSchema construct.

Create a new CreateSchema construct.

inherits from sqlalchemy.schema._DropBase

Represent a DROP SCHEMA statement.

The argument here is the string name of the schema.

Create a new DropSchema construct.

Create a new DropSchema construct.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (unknown):
```unknown
event.listen(
    metadata,
    "after_create",
    DDL(
        "ALTER TABLE users ADD CONSTRAINT "
        "cst_user_name_length "
        " CHECK (length(user_name) >= 8)"
    ),
)
```

Example 2 (julia):
```julia
mytable = Table(
    "mytable",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("data", String(50)),
)

func = DDL(
    "CREATE FUNCTION my_func() "
    "RETURNS TRIGGER AS $$ "
    "BEGIN "
    "NEW.data := 'ins'; "
    "RETURN NEW; "
    "END; $$ LANGUAGE PLPGSQL"
)

trigger = DDL(
    "CREATE TRIGGER dt_ins BEFORE INSERT ON mytable "
    "FOR EACH ROW EXECUTE PROCEDURE my_func();"
)

event.listen(mytable, "after_create", func.execute_if(dialect="postgresql"))

event.listen(mytable, "after_create", trigger.execute_if(dialect="postgresql"))
```

Example 3 (unknown):
```unknown
event.listen(
    mytable, "after_create", trigger.execute_if(dialect=("postgresql", "mysql"))
)
event.listen(
    mytable, "before_drop", trigger.execute_if(dialect=("postgresql", "mysql"))
)
```

Example 4 (sql):
```sql
def should_create(ddl, target, connection, **kw):
    row = connection.execute(
        "select conname from pg_constraint where conname='%s'" % ddl.element.name
    ).scalar()
    return not bool(row)


def should_drop(ddl, target, connection, **kw):
    return not should_create(ddl, target, connection, **kw)


event.listen(
    users,
    "after_create",
    DDL(
        "ALTER TABLE users ADD CONSTRAINT "
        "cst_user_name_length CHECK (length(user_name) >= 8)"
    ).execute_if(callable_=should_create),
)
event.listen(
    users,
    "before_drop",
    DDL("ALTER TABLE users DROP CONSTRAINT cst_user_name_length").execute_if(
        callable_=should_drop
    ),
)

users.create(engine)
CREATE TABLE users (
    user_id SERIAL NOT NULL,
    user_name VARCHAR(40) NOT NULL,
    PRIMARY KEY (user_id)
)

SELECT conname FROM pg_constraint WHERE conname='cst_user_name_length'
ALTER TABLE users ADD CONSTRAINT cst_user_name_length  CHECK (length(user_name) >= 8)
users.drop(engine)
SELECT conname FROM pg_constraint WHERE conname='cst_user_name_length'
ALTER TABLE users DROP CONSTRAINT cst_user_name_length
DROP TABLE users
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- ORM Mapped Class Overview¶
- ORM Mapping Styles¶
  - Declarative Mapping¶
  - Imperative Mapping¶
- Mapped Class Essential Components¶
  - The class to be mapped¶

Home | Download this Documentation

Home | Download this Documentation

Overview of ORM class mapping configuration.

For readers new to the SQLAlchemy ORM and/or new to Python in general, it’s recommended to browse through the ORM Quick Start and preferably to work through the SQLAlchemy Unified Tutorial, where ORM configuration is first introduced at Using ORM Declarative Forms to Define Table Metadata.

SQLAlchemy features two distinct styles of mapper configuration, which then feature further sub-options for how they are set up. The variability in mapper styles is present to suit a varied list of developer preferences, including the degree of abstraction of a user-defined class from how it is to be mapped to relational schema tables and columns, what kinds of class hierarchies are in use, including whether or not custom metaclass schemes are present, and finally if there are other class-instrumentation approaches present such as if Python dataclasses are in use simultaneously.

In modern SQLAlchemy, the difference between these styles is mostly superficial; when a particular SQLAlchemy configurational style is used to express the intent to map a class, the internal process of mapping the class proceeds in mostly the same way for each, where the end result is always a user-defined class that has a Mapper configured against a selectable unit, typically represented by a Table object, and the class itself has been instrumented to include behaviors linked to relational operations both at the level of the class as well as on instances of that class. As the process is basically the same in all cases, classes mapped from different styles are always fully interoperable with each other. The protocol MappedClassProtocol can be used to indicate a mapped class when using type checkers such as mypy.

The original mapping API is commonly referred to as “classical” style, whereas the more automated style of mapping is known as “declarative” style. SQLAlchemy now refers to these two mapping styles as imperative mapping and declarative mapping.

Regardless of what style of mapping used, all ORM mappings as of SQLAlchemy 1.4 originate from a single object known as registry, which is a registry of mapped classes. Using this registry, a set of mapper configurations can be finalized as a group, and classes within a particular registry may refer to each other by name within the configurational process.

Changed in version 1.4: Declarative and classical mapping are now referred to as “declarative” and “imperative” mapping, and are unified internally, all originating from the registry construct that represents a collection of related mappings.

The Declarative Mapping is the typical way that mappings are constructed in modern SQLAlchemy. The most common pattern is to first construct a base class using the DeclarativeBase superclass. The resulting base class, when subclassed will apply the declarative mapping process to all subclasses that derive from it, relative to a particular registry that is local to the new base by default. The example below illustrates the use of a declarative base which is then used in a declarative table mapping:

Above, the DeclarativeBase class is used to generate a new base class (within SQLAlchemy’s documentation it’s typically referred to as Base, however can have any desired name) from which new classes to be mapped may inherit from, as above a new mapped class User is constructed.

Changed in version 2.0: The DeclarativeBase superclass supersedes the use of the declarative_base() function and registry.generate_base() methods; the superclass approach integrates with PEP 484 tools without the use of plugins. See ORM Declarative Models for migration notes.

The base class refers to a registry object that maintains a collection of related mapped classes. as well as to a MetaData object that retains a collection of Table objects to which the classes are mapped.

The major Declarative mapping styles are further detailed in the following sections:

Using a Declarative Base Class - declarative mapping using a base class.

Declarative Mapping using a Decorator (no declarative base) - declarative mapping using a decorator, rather than a base class.

Within the scope of a Declarative mapped class, there are also two varieties of how the Table metadata may be declared. These include:

Declarative Table with mapped_column() - table columns are declared inline within the mapped class using the mapped_column() directive (or in legacy form, using the Column object directly). The mapped_column() directive may also be optionally combined with type annotations using the Mapped class which can provide some details about the mapped columns directly. The column directives, in combination with the __tablename__ and optional __table_args__ class level directives will allow the Declarative mapping process to construct a Table object to be mapped.

Declarative with Imperative Table (a.k.a. Hybrid Declarative) - Instead of specifying table name and attributes separately, an explicitly constructed Table object is associated with a class that is otherwise mapped declaratively. This style of mapping is a hybrid of “declarative” and “imperative” mapping, and applies to techniques such as mapping classes to reflected Table objects, as well as mapping classes to existing Core constructs such as joins and subqueries.

Documentation for Declarative mapping continues at Mapping Classes with Declarative.

An imperative or classical mapping refers to the configuration of a mapped class using the registry.map_imperatively() method, where the target class does not include any declarative class attributes.

The imperative mapping form is a lesser-used form of mapping that originates from the very first releases of SQLAlchemy in 2006. It’s essentially a means of bypassing the Declarative system to provide a more “barebones” system of mapping, and does not offer modern features such as PEP 484 support. As such, most documentation examples use Declarative forms, and it’s recommended that new users start with Declarative Table configuration.

Changed in version 2.0: The registry.map_imperatively() method is now used to create classical mappings. The sqlalchemy.orm.mapper() standalone function is effectively removed.

In “classical” form, the table metadata is created separately with the Table construct, then associated with the User class via the registry.map_imperatively() method, after establishing a registry instance. Normally, a single instance of registry shared for all mapped classes that are related to each other:

Information about mapped attributes, such as relationships to other classes, are provided via the properties dictionary. The example below illustrates a second Table object, mapped to a class called Address, then linked to User via relationship():

Note that classes which are mapped with the Imperative approach are fully interchangeable with those mapped with the Declarative approach. Both systems ultimately create the same configuration, consisting of a Table, user-defined class, linked together with a Mapper object. When we talk about “the behavior of Mapper”, this includes when using the Declarative system as well - it’s still used, just behind the scenes.

With all mapping forms, the mapping of the class can be configured in many ways by passing construction arguments that ultimately become part of the Mapper object via its constructor. The parameters that are delivered to Mapper originate from the given mapping form, including parameters passed to registry.map_imperatively() for an Imperative mapping, or when using the Declarative system, from a combination of the table columns, SQL expressions and relationships being mapped along with that of attributes such as __mapper_args__.

There are four general classes of configuration information that the Mapper class looks for:

This is a class that we construct in our application. There are generally no restrictions on the structure of this class. [1] When a Python class is mapped, there can only be one Mapper object for the class. [2]

When mapping with the declarative mapping style, the class to be mapped is either a subclass of the declarative base class, or is handled by a decorator or function such as registry.mapped().

When mapping with the imperative style, the class is passed directly as the map_imperatively.class_ argument.

In the vast majority of common cases this is an instance of Table. For more advanced use cases, it may also refer to any kind of FromClause object, the most common alternative objects being the Subquery and Join object.

When mapping with the declarative mapping style, the subject table is either generated by the declarative system based on the __tablename__ attribute and the Column objects presented, or it is established via the __table__ attribute. These two styles of configuration are presented at Declarative Table with mapped_column() and Declarative with Imperative Table (a.k.a. Hybrid Declarative).

When mapping with the imperative style, the subject table is passed positionally as the map_imperatively.local_table argument.

In contrast to the “one mapper per class” requirement of a mapped class, the Table or other FromClause object that is the subject of the mapping may be associated with any number of mappings. The Mapper applies modifications directly to the user-defined class, but does not modify the given Table or other FromClause in any way.

This is a dictionary of all of the attributes that will be associated with the mapped class. By default, the Mapper generates entries for this dictionary derived from the given Table, in the form of ColumnProperty objects which each refer to an individual Column of the mapped table. The properties dictionary will also contain all the other kinds of MapperProperty objects to be configured, most commonly instances generated by the relationship() construct.

When mapping with the declarative mapping style, the properties dictionary is generated by the declarative system by scanning the class to be mapped for appropriate attributes. See the section Defining Mapped Properties with Declarative for notes on this process.

When mapping with the imperative style, the properties dictionary is passed directly as the properties parameter to registry.map_imperatively(), which will pass it along to the Mapper.properties parameter.

When mapping with the declarative mapping style, additional mapper configuration arguments are configured via the __mapper_args__ class attribute. Examples of use are available at Mapper Configuration Options with Declarative.

When mapping with the imperative style, keyword arguments are passed to the to registry.map_imperatively() method which passes them along to the Mapper class.

The full range of parameters accepted are documented at Mapper.

Across all styles of mapping using the registry object, the following behaviors are common:

The registry applies a default constructor, i.e. __init__ method, to all mapped classes that don’t explicitly have their own __init__ method. The behavior of this method is such that it provides a convenient keyword constructor that will accept as optional keyword arguments all the attributes that are named. E.g.:

An object of type User above will have a constructor which allows User objects to be created as:

The Declarative Dataclass Mapping feature provides an alternate means of generating a default __init__() method by using Python dataclasses, and allows for a highly configurable constructor form.

The __init__() method of the class is called only when the object is constructed in Python code, and not when an object is loaded or refreshed from the database. See the next section Maintaining Non-Mapped State Across Loads for a primer on how to invoke special logic when objects are loaded.

A class that includes an explicit __init__() method will maintain that method, and no default constructor will be applied.

To change the default constructor used, a user-defined Python callable may be provided to the registry.constructor parameter which will be used as the default constructor.

The constructor also applies to imperative mappings:

The above class, mapped imperatively as described at Imperative Mapping, will also feature the default constructor associated with the registry.

Added in version 1.4: classical mappings now support a standard configuration-level constructor when they are mapped via the registry.map_imperatively() method.

The __init__() method of the mapped class is invoked when the object is constructed directly in Python code:

However, when an object is loaded using the ORM Session, the __init__() method is not called:

The reason for this is that when loaded from the database, the operation used to construct the object, in the above example the User, is more analogous to deserialization, such as unpickling, rather than initial construction. The majority of the object’s important state is not being assembled for the first time, it’s being re-loaded from database rows.

Therefore to maintain state within the object that is not part of the data that’s stored to the database, such that this state is present when objects are loaded as well as constructed, there are two general approaches detailed below.

Use Python descriptors like @property, rather than state, to dynamically compute attributes as needed.

For simple attributes, this is the simplest approach and the least error prone. For example if an object Point with Point.x and Point.y wanted an attribute with the sum of these attributes:

An advantage of using dynamic descriptors is that the value is computed every time, meaning it maintains the correct value as the underlying attributes (x and y in this case) might change.

Other forms of the above pattern include Python standard library cached_property decorator (which is cached, and not re-computed each time), as well as SQLAlchemy’s hybrid_property decorator which allows for attributes that can work for SQL querying as well.

Establish state on-load using InstanceEvents.load(), and optionally supplemental methods InstanceEvents.refresh() and InstanceEvents.refresh_flush().

These are event hooks that are invoked whenever the object is loaded from the database, or when it is refreshed after being expired. Typically only the InstanceEvents.load() is needed, since non-mapped local object state is not affected by expiration operations. To revise the Point example above looks like:

If using the refresh events as well, the event hooks can be stacked on top of one callable if needed, as:

Above, the attrs attribute will be present for the refresh and refresh_flush events and indicate a list of attribute names that are being refreshed.

A class that is mapped using registry will also feature a few attributes that are common to all mappings:

The __mapper__ attribute will refer to the Mapper that is associated with the class:

This Mapper is also what’s returned when using the inspect() function against the mapped class:

The __table__ attribute will refer to the Table, or more generically to the FromClause object, to which the class is mapped:

This FromClause is also what’s returned when using the Mapper.local_table attribute of the Mapper:

For a single-table inheritance mapping, where the class is a subclass that does not have a table of its own, the Mapper.local_table attribute as well as the .__table__ attribute will be None. To retrieve the “selectable” that is actually selected from during a query for this class, this is available via the Mapper.selectable attribute:

As illustrated in the previous section, the Mapper object is available from any mapped class, regardless of method, using the Runtime Inspection API system. Using the inspect() function, one can acquire the Mapper from a mapped class:

Detailed information is available including Mapper.columns:

This is a namespace that can be viewed in a list format or via individual names:

Other namespaces include Mapper.all_orm_descriptors, which includes all mapped attributes as well as hybrids, association proxies:

As well as Mapper.column_attrs:

The inspect() function also provides information about instances of a mapped class. When applied to an instance of a mapped class, rather than the class itself, the object returned is known as InstanceState, which will provide links to not only the Mapper in use by the class, but also a detailed interface that provides information on the state of individual attributes within the instance including their current value and how this relates to what their database-loaded value is.

Given an instance of the User class loaded from the database:

The inspect() function will return to us an InstanceState object:

With this object we can see elements such as the Mapper:

The Session to which the object is attached, if any:

Information about the current persistence state for the object:

Attribute state information such as attributes that have not been loaded or lazy loaded (assume addresses refers to a relationship() on the mapped class to a related class):

Information regarding the current in-Python status of attributes, such as attributes that have not been modified since the last flush:

as well as specific history on modifications to attributes since the last flush:

When running under Python 2, a Python 2 “old style” class is the only kind of class that isn’t compatible. When running code on Python 2, all classes must extend from the Python object class. Under Python 3 this is always the case.

There is a legacy feature known as a “non primary mapper”, where additional Mapper objects may be associated with a class that’s already mapped, however they don’t apply instrumentation to the class. This feature is deprecated as of SQLAlchemy 1.3.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


# declarative base class
class Base(DeclarativeBase):
    pass


# an example mapping using the base
class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    fullname: Mapped[str] = mapped_column(String(30))
    nickname: Mapped[Optional[str]]
```

Example 2 (python):
```python
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import registry

mapper_registry = registry()

user_table = Table(
    "user",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("fullname", String(50)),
    Column("nickname", String(12)),
)


class User:
    pass


mapper_registry.map_imperatively(User, user_table)
```

Example 3 (json):
```json
address = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("email_address", String(50)),
)

mapper_registry.map_imperatively(
    User,
    user,
    properties={
        "addresses": relationship(Address, backref="user", order_by=address.c.id)
    },
)

mapper_registry.map_imperatively(Address, address)
```

Example 4 (typescript):
```typescript
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    fullname: Mapped[str]
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/core/connections.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Core
    - Project Versions
- Working with Engines and Connections¶
- Basic Usage¶
- Using Transactions¶
  - Commit As You Go¶
  - Begin Once¶
  - Connect and Begin Once from the Engine¶

Home | Download this Documentation

Home | Download this Documentation

This section details direct usage of the Engine, Connection, and related objects. Its important to note that when using the SQLAlchemy ORM, these objects are not generally accessed; instead, the Session object is used as the interface to the database. However, for applications that are built around direct usage of textual SQL statements and/or SQL expression constructs without involvement by the ORM’s higher level management services, the Engine and Connection are king (and queen?) - read on.

Recall from Engine Configuration that an Engine is created via the create_engine() call:

The typical usage of create_engine() is once per particular database URL, held globally for the lifetime of a single application process. A single Engine manages many individual DBAPI connections on behalf of the process and is intended to be called upon in a concurrent fashion. The Engine is not synonymous to the DBAPI connect() function, which represents just one connection resource - the Engine is most efficient when created just once at the module level of an application, not per-object or per-function call.

When using an Engine with multiple Python processes, such as when using os.fork or Python multiprocessing, it’s important that the engine is initialized per process. See Using Connection Pools with Multiprocessing or os.fork() for details.

The most basic function of the Engine is to provide access to a Connection, which can then invoke SQL statements. To emit a textual statement to the database looks like:

Above, the Engine.connect() method returns a Connection object, and by using it in a Python context manager (e.g. the with: statement) the Connection.close() method is automatically invoked at the end of the block. The Connection, is a proxy object for an actual DBAPI connection. The DBAPI connection is retrieved from the connection pool at the point at which Connection is created.

The object returned is known as CursorResult, which references a DBAPI cursor and provides methods for fetching rows similar to that of the DBAPI cursor. The DBAPI cursor will be closed by the CursorResult when all of its result rows (if any) are exhausted. A CursorResult that returns no rows, such as that of an UPDATE statement (without any returned rows), releases cursor resources immediately upon construction.

When the Connection is closed at the end of the with: block, the referenced DBAPI connection is released to the connection pool. From the perspective of the database itself, the connection pool will not actually “close” the connection assuming the pool has room to store this connection for the next use. When the connection is returned to the pool for reuse, the pooling mechanism issues a rollback() call on the DBAPI connection so that any transactional state or locks are removed (this is known as Reset On Return), and the connection is ready for its next use.

Our example above illustrated the execution of a textual SQL string, which should be invoked by using the text() construct to indicate that we’d like to use textual SQL. The Connection.execute() method can of course accommodate more than that; see Working with Data in the SQLAlchemy Unified Tutorial for a tutorial.

This section describes how to use transactions when working directly with Engine and Connection objects. When using the SQLAlchemy ORM, the public API for transaction control is via the Session object, which makes usage of the Transaction object internally. See Managing Transactions for further information.

The Connection object always emits SQL statements within the context of a transaction block. The first time the Connection.execute() method is called to execute a SQL statement, this transaction is begun automatically, using a behavior known as autobegin. The transaction remains in place for the scope of the Connection object until the Connection.commit() or Connection.rollback() methods are called. Subsequent to the transaction ending, the Connection waits for the Connection.execute() method to be called again, at which point it autobegins again.

This calling style is known as commit as you go, and is illustrated in the example below:

the Python DBAPI is where autobegin actually happens

The design of “commit as you go” is intended to be complementary to the design of the DBAPI, which is the underlying database interface that SQLAlchemy interacts with. In the DBAPI, the connection object does not assume changes to the database will be automatically committed, instead requiring in the default case that the connection.commit() method is called in order to commit changes to the database. It should be noted that the DBAPI itself does not have a begin() method at all. All Python DBAPIs implement “autobegin” as the primary means of managing transactions, and handle the job of emitting a statement like BEGIN on the connection when SQL statements are first emitted. SQLAlchemy’s API is basically re-stating this behavior in terms of higher level Python objects.

In “commit as you go” style, we can call upon Connection.commit() and Connection.rollback() methods freely within an ongoing sequence of other statements emitted using Connection.execute(); each time the transaction is ended, and a new statement is emitted, a new transaction begins implicitly:

Added in version 2.0: “commit as you go” style is a new feature of SQLAlchemy 2.0. It is also available in SQLAlchemy 1.4’s “transitional” mode when using a “future” style engine.

The Connection object provides a more explicit transaction management style known as begin once. In contrast to “commit as you go”, “begin once” allows the start point of the transaction to be stated explicitly, and allows that the transaction itself may be framed out as a context manager block so that the end of the transaction is instead implicit. To use “begin once”, the Connection.begin() method is used, which returns a Transaction object which represents the DBAPI transaction. This object also supports explicit management via its own Transaction.commit() and Transaction.rollback() methods, but as a preferred practice also supports the context manager interface, where it will commit itself when the block ends normally and emit a rollback if an exception is raised, before propagating the exception outwards. Below illustrates the form of a “begin once” block:

A convenient shorthand form for the above “begin once” block is to use the Engine.begin() method at the level of the originating Engine object, rather than performing the two separate steps of Engine.connect() and Connection.begin(); the Engine.begin() method returns a special context manager that internally maintains both the context manager for the Connection as well as the context manager for the Transaction normally returned by the Connection.begin() method:

Within the Engine.begin() block, we can call upon the Connection.commit() or Connection.rollback() methods, which will end the transaction normally demarcated by the block ahead of time. However, if we do so, no further SQL operations may be emitted on the Connection until the block ends:

The “commit as you go” and “begin once” styles can be freely mixed within a single Engine.connect() block, provided that the call to Connection.begin() does not conflict with the “autobegin” behavior. To accomplish this, Connection.begin() should only be called either before any SQL statements have been emitted, or directly after a previous call to Connection.commit() or Connection.rollback():

When developing code that uses “begin once”, the library will raise InvalidRequestError if a transaction was already “autobegun”.

Most DBAPIs support the concept of configurable transaction isolation levels. These are traditionally the four levels “READ UNCOMMITTED”, “READ COMMITTED”, “REPEATABLE READ” and “SERIALIZABLE”. These are usually applied to a DBAPI connection before it begins a new transaction, noting that most DBAPIs will begin this transaction implicitly when SQL statements are first emitted.

DBAPIs that support isolation levels also usually support the concept of true “autocommit”, which means that the DBAPI connection itself will be placed into a non-transactional autocommit mode. This usually means that the typical DBAPI behavior of emitting “BEGIN” to the database automatically no longer occurs, but it may also include other directives. SQLAlchemy treats the concept of “autocommit” like any other isolation level; in that it is an isolation level that loses not only “read committed” but also loses atomicity.

It is important to note, as will be discussed further in the section below at Understanding the DBAPI-Level Autocommit Isolation Level, that “autocommit” isolation level like any other isolation level does not affect the “transactional” behavior of the Connection object, which continues to call upon DBAPI .commit() and .rollback() methods (they just have no net effect under autocommit), and for which the .begin() method assumes the DBAPI will start a transaction implicitly (which means that SQLAlchemy’s “begin” does not change autocommit mode).

SQLAlchemy dialects should support these isolation levels as well as autocommit to as great a degree as possible.

For an individual Connection object that’s acquired from Engine.connect(), the isolation level can be set for the duration of that Connection object using the Connection.execution_options() method. The parameter is known as Connection.execution_options.isolation_level and the values are strings which are typically a subset of the following names:

Not every DBAPI supports every value; if an unsupported value is used for a certain backend, an error is raised.

For example, to force REPEATABLE READ on a specific connection, then begin a transaction:

The return value of the Connection.execution_options() method is the same Connection object upon which the method was called, meaning, it modifies the state of the Connection object in place. This is a new behavior as of SQLAlchemy 2.0. This behavior does not apply to the Engine.execution_options() method; that method still returns a copy of the Engine and as described below may be used to construct multiple Engine objects with different execution options, which nonetheless share the same dialect and connection pool.

The Connection.execution_options.isolation_level parameter necessarily does not apply to statement level options, such as that of Executable.execution_options(), and will be rejected if set at this level. This because the option must be set on a DBAPI connection on a per-transaction basis.

The Connection.execution_options.isolation_level option may also be set engine wide, as is often preferable. This may be achieved by passing the create_engine.isolation_level parameter to create_engine():

With the above setting, each new DBAPI connection the moment it’s created will be set to use a "REPEATABLE READ" isolation level setting for all subsequent operations.

Prefer to set frequently used isolation levels engine wide as illustrated above compared to using per-engine or per-connection execution options for maximum performance.

The isolation level may also be set per engine, with a potentially greater level of flexibility but with a small per-connection performance overhead, using either the create_engine.execution_options parameter to create_engine() or the Engine.execution_options() method, the latter of which will create a copy of the Engine that shares the dialect and connection pool of the original engine, but has its own per-connection isolation level setting:

With the above setting, the DBAPI connection will be set to use a "REPEATABLE READ" isolation level setting for each new transaction begun; but the connection as pooled will be reset to the original isolation level that was present when the connection first occurred. At the level of create_engine(), the end effect is not any different from using the create_engine.isolation_level parameter.

However, an application that frequently chooses to run operations within different isolation levels may wish to create multiple “sub-engines” of a lead Engine, each of which will be configured to a different isolation level. One such use case is an application that has operations that break into “transactional” and “read-only” operations, a separate Engine that makes use of "AUTOCOMMIT" may be separated off from the main engine:

Above, the Engine.execution_options() method creates a shallow copy of the original Engine. Both eng and autocommit_engine share the same dialect and connection pool. However, the “AUTOCOMMIT” mode will be set upon connections when they are acquired from the autocommit_engine.

The isolation level setting, regardless of which one it is, is unconditionally reverted when a connection is returned to the connection pool.

The execution options approach, whether used engine wide or per connection, incurs a small performance penalty as isolation level instructions are sent on connection acquire as well as connection release. Consider the engine-wide isolation setting at Setting Isolation Level or DBAPI Autocommit for an Engine so that connections are configured at the target isolation level permanently as they are pooled.

SQLite Transaction Isolation

PostgreSQL Transaction Isolation

MySQL Transaction Isolation

SQL Server Transaction Isolation

Oracle Database Transaction Isolation

Setting Transaction Isolation Levels / DBAPI AUTOCOMMIT - for the ORM

Using DBAPI Autocommit Allows for a Readonly Version of Transparent Reconnect - a recipe that uses DBAPI autocommit to transparently reconnect to the database for read-only operations

In the parent section, we introduced the concept of the Connection.execution_options.isolation_level parameter and how it can be used to set database isolation levels, including DBAPI-level “autocommit” which is treated by SQLAlchemy as another transaction isolation level. In this section we will attempt to clarify the implications of this approach.

If we wanted to check out a Connection object and use it “autocommit” mode, we would proceed as follows:

Above illustrates normal usage of “DBAPI autocommit” mode. There is no need to make use of methods such as Connection.begin() or Connection.commit(), as all statements are committed to the database immediately. When the block ends, the Connection object will revert the “autocommit” isolation level, and the DBAPI connection is released to the connection pool where the DBAPI connection.rollback() method will normally be invoked, but as the above statements were already committed, this rollback has no change on the state of the database.

It is important to note that “autocommit” mode persists even when the Connection.begin() method is called; the DBAPI will not emit any BEGIN to the database. When Connection.commit() is called, the DBAPI may still emit the “COMMIT” instruction, but this is a no-op at the database level. This usage is also not an error scenario, as it is expected that the “autocommit” isolation level may be applied to code that otherwise was written assuming a transactional context; the “isolation level” is, after all, a configurational detail of the transaction itself just like any other isolation level.

In the example below, statements remain autocommitting regardless of SQLAlchemy-level transaction blocks:

When we run a block like the above with logging turned on, the logging will attempt to indicate that while a DBAPI level .commit() is called, it probably will have no effect due to autocommit mode:

At the same time, even though we are using “DBAPI autocommit”, SQLAlchemy’s transactional semantics, that is, the in-Python behavior of Connection.begin() as well as the behavior of “autobegin”, remain in place, even though these don’t impact the DBAPI connection itself. To illustrate, the code below will raise an error, as Connection.begin() is being called after autobegin has already occurred:

The above example also demonstrates the same theme that the “autocommit” isolation level is a configurational detail of the underlying database transaction, and is independent of the begin/commit behavior of the SQLAlchemy Connection object. The “autocommit” mode will not interact with Connection.begin() in any way and the Connection does not consult this status when performing its own state changes with regards to the transaction (with the exception of suggesting within engine logging that these blocks are not actually committing). The rationale for this design is to maintain a completely consistent usage pattern with the Connection where DBAPI-autocommit mode can be changed independently without indicating any code changes elsewhere.

Added in version 2.0.43.

A common use case is to use AUTOCOMMIT isolation mode to improve performance, and this is a particularly common practice on MySQL / MariaDB databases. When seeking this pattern, it should be preferred to set AUTOCOMMIT engine wide using the create_engine.isolation_level so that pooled connections are permanently set in autocommit mode. The SQLAlchemy connection pool as well as the Connection will still seek to invoke the DBAPI .rollback() method upon connection release, as their behavior remains agnostic of the isolation level that’s configured on the connection. As this rollback still incurs a network round trip under most if not all DBAPI drivers, this additional network trip may be disabled using the create_engine.skip_autocommit_rollback parameter, which will apply a rule at the basemost portion of the dialect that invokes DBAPI .rollback() to first check if the connection is configured in autocommit, using a method of detection that does not itself incur network overhead:

When DBAPI connections are returned to the pool by the Connection, whether the Connection or the pool attempts to reset the “transaction”, the underlying DBAPI .rollback() method will be blocked based on a positive test of “autocommit”.

If the dialect in use does not support a no-network means of detecting autocommit, the dialect will raise NotImplementedError when a connection release is attempted.

prefer to use individual Connection objects each with just one isolation level, rather than switching isolation on a single Connection. The code will be easier to read and less error prone.

Isolation level settings, including autocommit mode, are reset automatically when the connection is released back to the connection pool. Therefore it is preferable to avoid trying to switch isolation levels on a single Connection object as this leads to excess verbosity.

To illustrate how to use “autocommit” in an ad-hoc mode within the scope of a single Connection checkout, the Connection.execution_options.isolation_level parameter must be re-applied with the previous isolation level. The previous section illustrated an attempt to call Connection.begin() in order to start a transaction while autocommit was taking place; we can rewrite that example to actually do so by first reverting the isolation level before we call upon Connection.begin():

Above, to manually revert the isolation level we made use of Connection.default_isolation_level to restore the default isolation level (assuming that’s what we want here). However, it’s probably a better idea to work with the architecture of of the Connection which already handles resetting of isolation level automatically upon checkin. The preferred way to write the above is to use two blocks

“DBAPI level autocommit” isolation level is entirely independent of the Connection object’s notion of “begin” and “commit”

use individual Connection checkouts per isolation level. Avoid trying to change back and forth between “autocommit” on a single connection checkout; let the engine do the work of restoring default isolation levels

Some backends feature explicit support for the concept of “server side cursors” versus “client side cursors”. A client side cursor here means that the database driver fully fetches all rows from a result set into memory before returning from a statement execution. Drivers such as those of PostgreSQL and MySQL/MariaDB generally use client side cursors by default. A server side cursor, by contrast, indicates that result rows remain pending within the database server’s state as result rows are consumed by the client. The drivers for Oracle Database generally use a “server side” model, for example, and the SQLite dialect, while not using a real “client / server” architecture, still uses an unbuffered result fetching approach that will leave result rows outside of process memory before they are consumed.

What we really mean is “buffered” vs. “unbuffered” results

Server side cursors also imply a wider set of features with relational databases, such as the ability to “scroll” a cursor forwards and backwards. SQLAlchemy does not include any explicit support for these behaviors; within SQLAlchemy itself, the general term “server side cursors” should be considered to mean “unbuffered results” and “client side cursors” means “result rows are buffered into memory before the first row is returned”. To work with a richer “server side cursor” featureset specific to a certain DBAPI driver, see the section Working with the DBAPI cursor directly.

From this basic architecture it follows that a “server side cursor” is more memory efficient when fetching very large result sets, while at the same time may introduce more complexity in the client/server communication process and be less efficient for small result sets (typically less than 10000 rows).

For those dialects that have conditional support for buffered or unbuffered results, there are usually caveats to the use of the “unbuffered”, or server side cursor mode. When using the psycopg2 dialect for example, an error is raised if a server side cursor is used with any kind of DML or DDL statement. When using MySQL drivers with a server side cursor, the DBAPI connection is in a more fragile state and does not recover as gracefully from error conditions nor will it allow a rollback to proceed until the cursor is fully closed.

For this reason, SQLAlchemy’s dialects will always default to the less error prone version of a cursor, which means for PostgreSQL and MySQL dialects it defaults to a buffered, “client side” cursor where the full set of results is pulled into memory before any fetch methods are called from the cursor. This mode of operation is appropriate in the vast majority of cases; unbuffered cursors are not generally useful except in the uncommon case of an application fetching a very large number of rows in chunks, where the processing of these rows can be complete before more rows are fetched.

For database drivers that provide client and server side cursor options, the Connection.execution_options.stream_results and Connection.execution_options.yield_per execution options provide access to “server side cursors” on a per-Connection or per-statement basis. Similar options exist when using an ORM Session as well.

As individual row-fetch operations with fully unbuffered server side cursors are typically more expensive than fetching batches of rows at once, The Connection.execution_options.yield_per execution option configures a Connection or statement to make use of server-side cursors as are available, while at the same time configuring a fixed-size buffer of rows that will retrieve rows from the server in batches as they are consumed. This parameter may be to a positive integer value using the Connection.execution_options() method on Connection or on a statement using the Executable.execution_options() method.

Added in version 1.4.40: Connection.execution_options.yield_per as a Core-only option is new as of SQLAlchemy 1.4.40; for prior 1.4 versions, use Connection.execution_options.stream_results directly in combination with Result.yield_per().

Using this option is equivalent to manually setting the Connection.execution_options.stream_results option, described in the next section, and then invoking the Result.yield_per() method on the Result object with the given integer value. In both cases, the effect this combination has includes:

server side cursors mode is selected for the given backend, if available and not already the default behavior for that backend

as result rows are fetched, they will be buffered in batches, where the size of each batch up until the last batch will be equal to the integer argument passed to the Connection.execution_options.yield_per option or the Result.yield_per() method; the last batch is then sized against the remaining rows fewer than this size

The default partition size used by the Result.partitions() method, if used, will be made equal to this integer size as well.

These three behaviors are illustrated in the example below:

The above example illustrates the combination of yield_per=100 along with using the Result.partitions() method to run processing on rows in batches that match the size fetched from the server. The use of Result.partitions() is optional, and if the Result is iterated directly, a new batch of rows will be buffered for each 100 rows fetched. Calling a method such as Result.all() should not be used, as this will fully fetch all remaining rows at once and defeat the purpose of using yield_per.

The Result object may be used as a context manager as illustrated above. When iterating with a server-side cursor, this is the best way to ensure the Result object is closed, even if exceptions are raised within the iteration process.

The Connection.execution_options.yield_per option is portable to the ORM as well, used by a Session to fetch ORM objects, where it also limits the amount of ORM objects generated at once. See the section Fetching Large Result Sets with Yield Per - in the ORM Querying Guide for further background on using Connection.execution_options.yield_per with the ORM.

Added in version 1.4.40: Added Connection.execution_options.yield_per as a Core level execution option to conveniently set streaming results, buffer size, and partition size all at once in a manner that is transferable to that of the ORM’s similar use case.

To enable server side cursors without a specific partition size, the Connection.execution_options.stream_results option may be used, which like Connection.execution_options.yield_per may be called on the Connection object or the statement object.

When a Result object delivered using the Connection.execution_options.stream_results option is iterated directly, rows are fetched internally using a default buffering scheme that buffers first a small set of rows, then a larger and larger buffer on each fetch up to a pre-configured limit of 1000 rows. The maximum size of this buffer can be affected using the Connection.execution_options.max_row_buffer execution option:

While the Connection.execution_options.stream_results option may be combined with use of the Result.partitions() method, a specific partition size should be passed to Result.partitions() so that the entire result is not fetched. It is usually more straightforward to use the Connection.execution_options.yield_per option when setting up to use the Result.partitions() method.

Fetching Large Result Sets with Yield Per - in the ORM Querying Guide

To support multi-tenancy applications that distribute common sets of tables into multiple schemas, the Connection.execution_options.schema_translate_map execution option may be used to repurpose a set of Table objects to render under different schema names without any changes.

The “schema” of this Table as defined by the Table.schema attribute is None. The Connection.execution_options.schema_translate_map can specify that all Table objects with a schema of None would instead render the schema as user_schema_one:

The above code will invoke SQL on the database of the form:

That is, the schema name is substituted with our translated name. The map can specify any number of target->destination schemas:

The Connection.execution_options.schema_translate_map parameter affects all DDL and SQL constructs generated from the SQL expression language, as derived from the Table or Sequence objects. It does not impact literal string SQL used via the text() construct nor via plain strings passed to Connection.execute().

The feature takes effect only in those cases where the name of the schema is derived directly from that of a Table or Sequence; it does not impact methods where a string schema name is passed directly. By this pattern, it takes effect within the “can create” / “can drop” checks performed by methods such as MetaData.create_all() or MetaData.drop_all() are called, and it takes effect when using table reflection given a Table object. However it does not affect the operations present on the Inspector object, as the schema name is passed to these methods explicitly.

To use the schema translation feature with the ORM Session, set this option at the level of the Engine, then pass that engine to the Session. The Session uses a new Connection for each transaction:

When using the ORM Session without extensions, the schema translate feature is only supported as a single schema translate map per Session. It will not work if different schema translate maps are given on a per-statement basis, as the ORM Session does not take current schema translate values into account for individual objects.

To use a single Session with multiple schema_translate_map configurations, the Horizontal Sharding extension may be used. See the example at Horizontal Sharding.

Added in version 1.4: SQLAlchemy now has a transparent query caching system that substantially lowers the Python computational overhead involved in converting SQL statement constructs into SQL strings across both Core and ORM. See the introduction at Transparent SQL Compilation Caching added to All DQL, DML Statements in Core, ORM.

SQLAlchemy includes a comprehensive caching system for the SQL compiler as well as its ORM variants. This caching system is transparent within the Engine and provides that the SQL compilation process for a given Core or ORM SQL statement, as well as related computations which assemble result-fetching mechanics for that statement, will only occur once for that statement object and all others with the identical structure, for the duration that the particular structure remains within the engine’s “compiled cache”. By “statement objects that have the identical structure”, this generally corresponds to a SQL statement that is constructed within a function and is built each time that function runs:

The above statement will generate SQL resembling SELECT id, col FROM table WHERE col = :col ORDER BY id, noting that while the value of parameter is a plain Python object such as a string or an integer, the string SQL form of the statement does not include this value as it uses bound parameters. Subsequent invocations of the above run_my_statement() function will use a cached compilation construct within the scope of the connection.execute() call for enhanced performance.

it is important to note that the SQL compilation cache is caching the SQL string that is passed to the database only, and not the data returned by a query. It is in no way a data cache and does not impact the results returned for a particular SQL statement nor does it imply any memory use linked to fetching of result rows.

While SQLAlchemy has had a rudimentary statement cache since the early 1.x series, and additionally has featured the “Baked Query” extension for the ORM, both of these systems required a high degree of special API use in order for the cache to be effective. The new cache as of 1.4 is instead completely automatic and requires no change in programming style to be effective.

The cache is automatically used without any configurational changes and no special steps are needed in order to enable it. The following sections detail the configuration and advanced usage patterns for the cache.

The cache itself is a dictionary-like object called an LRUCache, which is an internal SQLAlchemy dictionary subclass that tracks the usage of particular keys and features a periodic “pruning” step which removes the least recently used items when the size of the cache reaches a certain threshold. The size of this cache defaults to 500 and may be configured using the create_engine.query_cache_size parameter:

The size of the cache can grow to be a factor of 150% of the size given, before it’s pruned back down to the target size. A cache of size 1200 above can therefore grow to be 1800 elements in size at which point it will be pruned to 1200.

The sizing of the cache is based on a single entry per unique SQL statement rendered, per engine. SQL statements generated from both the Core and the ORM are treated equally. DDL statements will usually not be cached. In order to determine what the cache is doing, engine logging will include details about the cache’s behavior, described in the next section.

The above cache size of 1200 is actually fairly large. For small applications, a size of 100 is likely sufficient. To estimate the optimal size of the cache, assuming enough memory is present on the target host, the size of the cache should be based on the number of unique SQL strings that may be rendered for the target engine in use. The most expedient way to see this is to use SQL echoing, which is most directly enabled by using the create_engine.echo flag, or by using Python logging; see the section Configuring Logging for background on logging configuration.

As an example, we will examine the logging produced by the following program:

When run, each SQL statement that’s logged will include a bracketed cache statistics badge to the left of the parameters passed. The four types of message we may see are summarized as follows:

[raw sql] - the driver or the end-user emitted raw SQL using Connection.exec_driver_sql() - caching does not apply

[no key] - the statement object is a DDL statement that is not cached, or the statement object contains uncacheable elements such as user-defined constructs or arbitrarily large VALUES clauses.

[generated in Xs] - the statement was a cache miss and had to be compiled, then stored in the cache. it took X seconds to produce the compiled construct. The number X will be in the small fractional seconds.

[cached since Xs ago] - the statement was a cache hit and did not have to be recompiled. The statement has been stored in the cache since X seconds ago. The number X will be proportional to how long the application has been running and how long the statement has been cached, so for example would be 86400 for a 24 hour period.

Each badge is described in more detail below.

The first statements we see for the above program will be the SQLite dialect checking for the existence of the “a” and “b” tables:

For the above two SQLite PRAGMA statements, the badge reads [raw sql], which indicates the driver is sending a Python string directly to the database using Connection.exec_driver_sql(). Caching does not apply to such statements because they already exist in string form, and there is nothing known about what kinds of result rows will be returned since SQLAlchemy does not parse SQL strings ahead of time.

The next statements we see are the CREATE TABLE statements:

For each of these statements, the badge reads [no key 0.00006s]. This indicates that these two particular statements, caching did not occur because the DDL-oriented CreateTable construct did not produce a cache key. DDL constructs generally do not participate in caching because they are not typically subject to being repeated a second time and DDL is also a database configurational step where performance is not as critical.

The [no key] badge is important for one other reason, as it can be produced for SQL statements that are cacheable except for some particular sub-construct that is not currently cacheable. Examples of this include custom user-defined SQL elements that don’t define caching parameters, as well as some constructs that generate arbitrarily long and non-reproducible SQL strings, the main examples being the Values construct as well as when using “multivalued inserts” with the Insert.values() method.

So far our cache is still empty. The next statements will be cached however, a segment looks like:

Above, we see essentially two unique SQL strings; "INSERT INTO a (data) VALUES (?)" and "INSERT INTO b (a_id, data) VALUES (?, ?)". Since SQLAlchemy uses bound parameters for all literal values, even though these statements are repeated many times for different objects, because the parameters are separate, the actual SQL string stays the same.

the above two statements are generated by the ORM unit of work process, and in fact will be caching these in a separate cache that is local to each mapper. However the mechanics and terminology are the same. The section Disabling or using an alternate dictionary to cache some (or all) statements below will describe how user-facing code can also use an alternate caching container on a per-statement basis.

The caching badge we see for the first occurrence of each of these two statements is [generated in 0.00011s]. This indicates that the statement was not in the cache, was compiled into a String in .00011s and was then cached. When we see the [generated] badge, we know that this means there was a cache miss. This is to be expected for the first occurrence of a particular statement. However, if lots of new [generated] badges are observed for a long-running application that is generally using the same series of SQL statements over and over, this may be a sign that the create_engine.query_cache_size parameter is too small. When a statement that was cached is then evicted from the cache due to the LRU cache pruning lesser used items, it will display the [generated] badge when it is next used.

The caching badge that we then see for the subsequent occurrences of each of these two statements looks like [cached since 0.0003533s ago]. This indicates that the statement was found in the cache, and was originally placed into the cache .0003533 seconds ago. It is important to note that while the [generated] and [cached since] badges refer to a number of seconds, they mean different things; in the case of [generated], the number is a rough timing of how long it took to compile the statement, and will be an extremely small amount of time. In the case of [cached since], this is the total time that a statement has been present in the cache. For an application that’s been running for six hours, this number may read [cached since 21600 seconds ago], and that’s a good thing. Seeing high numbers for “cached since” is an indication that these statements have not been subject to cache misses for a long time. Statements that frequently have a low number of “cached since” even if the application has been running a long time may indicate these statements are too frequently subject to cache misses, and that the create_engine.query_cache_size may need to be increased.

Our example program then performs some SELECTs where we can see the same pattern of “generated” then “cached”, for the SELECT of the “a” table as well as for subsequent lazy loads of the “b” table:

From our above program, a full run shows a total of four distinct SQL strings being cached. Which indicates a cache size of four would be sufficient. This is obviously an extremely small size, and the default size of 500 is fine to be left at its default.

The previous section detailed some techniques to check if the create_engine.query_cache_size needs to be bigger. How do we know if the cache is not too large? The reason we may want to set create_engine.query_cache_size to not be higher than a certain number would be because we have an application that may make use of a very large number of different statements, such as an application that is building queries on the fly from a search UX, and we don’t want our host to run out of memory if for example, a hundred thousand different queries were run in the past 24 hours and they were all cached.

It is extremely difficult to measure how much memory is occupied by Python data structures, however using a process to measure growth in memory via top as a successive series of 250 new statements are added to the cache suggest a moderate Core statement takes up about 12K while a small ORM statement takes about 20K, including result-fetching structures which for the ORM will be much greater.

The internal cache used is known as LRUCache, but this is mostly just a dictionary. Any dictionary may be used as a cache for any series of statements by using the Connection.execution_options.compiled_cache option as an execution option. Execution options may be set on a statement, on an Engine or Connection, as well as when using the ORM Session.execute() method for SQLAlchemy-2.0 style invocations. For example, to run a series of SQL statements and have them cached in a particular dictionary:

The SQLAlchemy ORM uses the above technique to hold onto per-mapper caches within the unit of work “flush” process that are separate from the default cache configured on the Engine, as well as for some relationship loader queries.

The cache can also be disabled with this argument by sending a value of None:

The caching feature requires that the dialect’s compiler produces SQL strings that are safe to reuse for many statement invocations, given a particular cache key that is keyed to that SQL string. This means that any literal values in a statement, such as the LIMIT/OFFSET values for a SELECT, can not be hardcoded in the dialect’s compilation scheme, as the compiled string will not be reusable. SQLAlchemy supports rendered bound parameters using the BindParameter.render_literal_execute() method which can be applied to the existing Select._limit_clause and Select._offset_clause attributes by a custom compiler, which are illustrated later in this section.

As there are many third party dialects, many of which may be generating literal values from SQL statements without the benefit of the newer “literal execute” feature, SQLAlchemy as of version 1.4.5 has added an attribute to dialects known as Dialect.supports_statement_cache. This attribute is checked at runtime for its presence directly on a particular dialect’s class, even if it’s already present on a superclass, so that even a third party dialect that subclasses an existing cacheable SQLAlchemy dialect such as sqlalchemy.dialects.postgresql.PGDialect must still explicitly include this attribute for caching to be enabled. The attribute should only be enabled once the dialect has been altered as needed and tested for reusability of compiled SQL statements with differing parameters.

For all third party dialects that don’t support this attribute, the logging for such a dialect will indicate dialect does not support caching.

When a dialect has been tested against caching, and in particular the SQL compiler has been updated to not render any literal LIMIT / OFFSET within a SQL string directly, dialect authors can apply the attribute as follows:

The flag needs to be applied to all subclasses of the dialect as well:

Added in version 1.4.5: Added the Dialect.supports_statement_cache attribute.

The typical case for dialect modification follows.

As an example, suppose a dialect overrides the SQLCompiler.limit_clause() method, which produces the “LIMIT / OFFSET” clause for a SQL statement, like this:

The above routine renders the Select._limit and Select._offset integer values as literal integers embedded in the SQL statement. This is a common requirement for databases that do not support using a bound parameter within the LIMIT/OFFSET clauses of a SELECT statement. However, rendering the integer value within the initial compilation stage is directly incompatible with caching as the limit and offset integer values of a Select object are not part of the cache key, so that many Select statements with different limit/offset values would not render with the correct value.

The correction for the above code is to move the literal integer into SQLAlchemy’s post-compile facility, which will render the literal integer outside of the initial compilation stage, but instead at execution time before the statement is sent to the DBAPI. This is accessed within the compilation stage using the BindParameter.render_literal_execute() method, in conjunction with using the Select._limit_clause and Select._offset_clause attributes, which represent the LIMIT/OFFSET as a complete SQL expression, as follows:

The approach above will generate a compiled SELECT statement that looks like:

Where above, the __[POSTCOMPILE_param_1] and __[POSTCOMPILE_param_2] indicators will be populated with their corresponding integer values at statement execution time, after the SQL string has been retrieved from the cache.

After changes like the above have been made as appropriate, the Dialect.supports_statement_cache flag should be set to True. It is strongly recommended that third party dialects make use of the dialect third party test suite which will assert that operations like SELECTs with LIMIT/OFFSET are correctly rendered and cached.

Why is my application slow after upgrading to 1.4 and/or 2.x? - in the Frequently Asked Questions section

This technique is generally non-essential except in very performance intensive scenarios, and intended for experienced Python programmers. While fairly straightforward, it involves metaprogramming concepts that are not appropriate for novice Python developers. The lambda approach can be applied to at a later time to existing code with a minimal amount of effort.

Python functions, typically expressed as lambdas, may be used to generate SQL expressions which are cacheable based on the Python code location of the lambda function itself as well as the closure variables within the lambda. The rationale is to allow caching of not only the SQL string-compiled form of a SQL expression construct as is SQLAlchemy’s normal behavior when the lambda system isn’t used, but also the in-Python composition of the SQL expression construct itself, which also has some degree of Python overhead.

The lambda SQL expression feature is available as a performance enhancing feature, and is also optionally used in the with_loader_criteria() ORM option in order to provide a generic SQL fragment.

Lambda statements are constructed using the lambda_stmt() function, which returns an instance of StatementLambdaElement, which is itself an executable statement construct. Additional modifiers and criteria are added to the object using the Python addition operator +, or alternatively the StatementLambdaElement.add_criteria() method which allows for more options.

It is assumed that the lambda_stmt() construct is being invoked within an enclosing function or method that expects to be used many times within an application, so that subsequent executions beyond the first one can take advantage of the compiled SQL being cached. When the lambda is constructed inside of an enclosing function in Python it is then subject to also having closure variables, which are significant to the whole approach:

Above, the three lambda callables that are used to define the structure of a SELECT statement are invoked exactly once, and the resulting SQL string cached in the compilation cache of the engine. From that point forward, the run_my_statement() function may be invoked any number of times and the lambda callables within it will not be called, only used as cache keys to retrieve the already-compiled SQL.

It is important to note that there is already SQL caching in place when the lambda system is not used. The lambda system only adds an additional layer of work reduction per SQL statement invoked by caching the building up of the SQL construct itself and also using a simpler cache key.

Above all, the emphasis within the lambda SQL system is ensuring that there is never a mismatch between the cache key generated for a lambda and the SQL string it will produce. The LambdaElement and related objects will run and analyze the given lambda in order to calculate how it should be cached on each run, trying to detect any potential problems. Basic guidelines include:

Any kind of statement is supported - while it’s expected that select() constructs are the prime use case for lambda_stmt(), DML statements such as insert() and update() are equally usable:

ORM use cases directly supported as well - the lambda_stmt() can accommodate ORM functionality completely and used directly with Session.execute():

Bound parameters are automatically accommodated - in contrast to SQLAlchemy’s previous “baked query” system, the lambda SQL system accommodates for Python literal values which become SQL bound parameters automatically. This means that even though a given lambda runs only once, the values that become bound parameters are extracted from the closure of the lambda on every run:

Above, StatementLambdaElement extracted the values of x and y from the closure of the lambda that is generated each time my_stmt() is invoked; these were substituted into the cached SQL construct as the values of the parameters.

The lambda should ideally produce an identical SQL structure in all cases - Avoid using conditionals or custom callables inside of lambdas that might make it produce different SQL based on inputs; if a function might conditionally use two different SQL fragments, use two separate lambdas:

There are a variety of failures which can occur if the lambda does not produce a consistent SQL construct and some are not trivially detectable right now.

Don’t use functions inside the lambda to produce bound values - the bound value tracking approach requires that the actual value to be used in the SQL statement be locally present in the closure of the lambda. This is not possible if values are generated from other functions, and the LambdaElement should normally raise an error if this is attempted:

Above, the use of get_x() and get_y(), if they are necessary, should occur outside of the lambda and assigned to a local closure variable:

Avoid referring to non-SQL constructs inside of lambdas as they are not cacheable by default - this issue refers to how the LambdaElement creates a cache key from other closure variables within the statement. In order to provide the best guarantee of an accurate cache key, all objects located in the closure of the lambda are considered to be significant, and none will be assumed to be appropriate for a cache key by default. So the following example will also raise a rather detailed error message:

The above error indicates that LambdaElement will not assume that the Foo object passed in will continue to behave the same in all cases. It also won’t assume it can use Foo as part of the cache key by default; if it were to use the Foo object as part of the cache key, if there were many different Foo objects this would fill up the cache with duplicate information, and would also hold long-lasting references to all of these objects.

The best way to resolve the above situation is to not refer to foo inside of the lambda, and refer to it outside instead:

In some situations, if the SQL structure of the lambda is guaranteed to never change based on input, to pass track_closure_variables=False which will disable any tracking of closure variables other than those used for bound parameters:

There is also the option to add objects to the element to explicitly form part of the cache key, using the track_on parameter; using this parameter allows specific values to serve as the cache key and will also prevent other closure variables from being considered. This is useful for cases where part of the SQL being constructed originates from a contextual object of some sort that may have many different values. In the example below, the first segment of the SELECT statement will disable tracking of the foo variable, whereas the second segment will explicitly track self as part of the cache key:

Using track_on means the given objects will be stored long term in the lambda’s internal cache and will have strong references for as long as the cache doesn’t clear out those objects (an LRU scheme of 1000 entries is used by default).

In order to understand some of the options and behaviors which occur with lambda SQL constructs, an understanding of the caching system is helpful.

SQLAlchemy’s caching system normally generates a cache key from a given SQL expression construct by producing a structure that represents all the state within the construct:

The above key is stored in the cache which is essentially a dictionary, and the value is a construct that among other things stores the string form of the SQL statement, in this case the phrase “SELECT q”. We can observe that even for an extremely short query the cache key is pretty verbose as it has to represent everything that may vary about what’s being rendered and potentially executed.

The lambda construction system by contrast creates a different kind of cache key:

Above, we see a cache key that is vastly shorter than that of the non-lambda statement, and additionally that production of the select(column("q")) construct itself was not even necessary; the Python lambda itself contains an attribute called __code__ which refers to a Python code object that within the runtime of the application is immutable and permanent.

When the lambda also includes closure variables, in the normal case that these variables refer to SQL constructs such as column objects, they become part of the cache key, or if they refer to literal values that will be bound parameters, they are placed in a separate element of the cache key:

The above StatementLambdaElement includes two lambdas, both of which refer to the col closure variable, so the cache key will represent both of these segments as well as the column() object:

The second part of the cache key has retrieved the bound parameters that will be used when the statement is invoked:

For a series of examples of “lambda” caching with performance comparisons, see the “short_selects” test suite within the Performance performance example.

Added in version 2.0: see Optimized ORM bulk insert now implemented for all backends other than MySQL for background on the change including sample performance tests

The insertmanyvalues feature is a transparently available performance feature which requires no end-user intervention in order for it to take place as needed. This section describes the architecture of the feature as well as how to measure its performance and tune its behavior in order to optimize the speed of bulk INSERT statements, particularly as used by the ORM.

As more databases have added support for INSERT..RETURNING, SQLAlchemy has undergone a major change in how it approaches the subject of INSERT statements where there’s a need to acquire server-generated values, most importantly server-generated primary key values which allow the new row to be referenced in subsequent operations. In particular, this scenario has long been a significant performance issue in the ORM, which relies on being able to retrieve server-generated primary key values in order to correctly populate the identity map.

With recent support for RETURNING added to SQLite and MariaDB, SQLAlchemy no longer needs to rely upon the single-row-only cursor.lastrowid attribute provided by the DBAPI for most backends; RETURNING may now be used for all SQLAlchemy-included backends with the exception of MySQL. The remaining performance limitation, that the cursor.executemany() DBAPI method does not allow for rows to be fetched, is resolved for most backends by foregoing the use of executemany() and instead restructuring individual INSERT statements to each accommodate a large number of rows in a single statement that is invoked using cursor.execute(). This approach originates from the psycopg2 fast execution helpers feature of the psycopg2 DBAPI, which SQLAlchemy incrementally added more and more support towards in recent release series.

The feature is enabled for all backend included in SQLAlchemy that support RETURNING, with the exception of Oracle Database for which both the python-oracledb and cx_Oracle drivers offer their own equivalent feature. The feature normally takes place when making use of the Insert.returning() method of an Insert construct in conjunction with executemany execution, which occurs when passing a list of dictionaries to the Connection.execute.parameters parameter of the Connection.execute() or Session.execute() methods (as well as equivalent methods under asyncio and shorthand methods like Session.scalars()). It also takes place within the ORM unit of work process when using methods such as Session.add() and Session.add_all() to add rows.

For SQLAlchemy’s included dialects, support or equivalent support is currently as follows:

SQLite - supported for SQLite versions 3.35 and above

PostgreSQL - all supported Postgresql versions (9 and above)

SQL Server - all supported SQL Server versions [1]

MariaDB - supported for MariaDB versions 10.5 and above

MySQL - no support, no RETURNING feature is present

Oracle Database - supports RETURNING with executemany using native python-oracledb / cx_Oracle APIs, for all supported Oracle Database versions 9 and above, using multi-row OUT parameters. This is not the same implementation as “executemanyvalues”, however has the same usage patterns and equivalent performance benefits.

Changed in version 2.0.10:

”insertmanyvalues” support for Microsoft SQL Server is restored, after being temporarily disabled in version 2.0.9.

To disable the “insertmanyvalues” feature for a given backend for an Engine overall, pass the create_engine.use_insertmanyvalues parameter as False to create_engine():

The feature can also be disabled from being used implicitly for a particular Table object by passing the Table.implicit_returning parameter as False:

The reason one might want to disable RETURNING for a specific table is to work around backend-specific limitations.

The feature has two modes of operation, which are selected transparently on a per-dialect, per-Table basis. One is batched mode, which reduces the number of database round trips by rewriting an INSERT statement of the form:

into a “batched” form such as:

where above, the statement is organized against a subset (a “batch”) of the input data, the size of which is determined by the database backend as well as the number of parameters in each batch to correspond to known limits for statement size / number of parameters. The feature then executes the INSERT statement once for each batch of input data until all records are consumed, concatenating the RETURNING results for each batch into a single large rowset that’s available from a single Result object.

This “batched” form allows INSERT of many rows using much fewer database round trips, and has been shown to allow dramatic performance improvements for most backends where it’s supported.

Added in version 2.0.10.

The “batch” mode query illustrated in the previous section does not guarantee the order of records returned would correspond with that of the input data. When used by the SQLAlchemy ORM unit of work process, as well as for applications which correlate returned server-generated values with input data, the Insert.returning() and UpdateBase.return_defaults() methods include an option Insert.returning.sort_by_parameter_order which indicates that “insertmanyvalues” mode should guarantee this correspondence. This is not related to the order in which records are actually INSERTed by the database backend, which is not assumed under any circumstances; only that the returned records should be organized when received back to correspond to the order in which the original input data was passed.

When the Insert.returning.sort_by_parameter_order parameter is present, for tables that use server-generated integer primary key values such as IDENTITY, PostgreSQL SERIAL, MariaDB AUTO_INCREMENT, or SQLite’s ROWID scheme, “batch” mode may instead opt to use a more complex INSERT..RETURNING form, in conjunction with post-execution sorting of rows based on the returned values, or if such a form is not available, the “insertmanyvalues” feature may gracefully degrade to “non-batched” mode which runs individual INSERT statements for each parameter set.

For example, on SQL Server when an auto incrementing IDENTITY column is used as the primary key, the following SQL form is used [2]:

A similar form is used for PostgreSQL as well, when primary key columns use SERIAL or IDENTITY. The above form does not guarantee the order in which rows are inserted. However, it does guarantee that the IDENTITY or SERIAL values will be created in order with each parameter set [3]. The “insertmanyvalues” feature then sorts the returned rows for the above INSERT statement by incrementing integer identity.

For the SQLite database, there is no appropriate INSERT form that can correlate the production of new ROWID values with the order in which the parameter sets are passed. As a result, when using server-generated primary key values, the SQLite backend will degrade to “non-batched” mode when ordered RETURNING is requested. For MariaDB, the default INSERT form used by insertmanyvalues is sufficient, as this database backend will line up the order of AUTO_INCREMENT with the order of input data when using InnoDB [4].

For a client-side generated primary key, such as when using the Python uuid.uuid4() function to generate new values for a Uuid column, the “insertmanyvalues” feature transparently includes this column in the RETURNING records and correlates its value to that of the given input records, thus maintaining correspondence between input records and result rows. From this, it follows that all backends allow for batched, parameter-correlated RETURNING order when client-side-generated primary key values are used.

The subject of how “insertmanyvalues” “batch” mode determines a column or columns to use as a point of correspondence between input parameters and RETURNING rows is known as an insert sentinel, which is a specific column or columns that are used to track such values. The “insert sentinel” is normally selected automatically, however can also be user-configuration for extremely special cases; the section Configuring Sentinel Columns describes this.

For backends that do not offer an appropriate INSERT form that can deliver server-generated values deterministically aligned with input values, or for Table configurations that feature other kinds of server generated primary key values, “insertmanyvalues” mode will make use of non-batched mode when guaranteed RETURNING ordering is requested.

Microsoft SQL Server rationale

“INSERT queries that use SELECT with ORDER BY to populate rows guarantees how identity values are computed but not the order in which the rows are inserted.” https://learn.microsoft.com/en-us/sql/t-sql/statements/insert-transact-sql?view=sql-server-ver16#limitations-and-restrictions

PostgreSQL batched INSERT Discussion

Original description in 2018 https://www.postgresql.org/message-id/29386.1528813619@sss.pgh.pa.us

Follow up in 2023 - https://www.postgresql.org/message-id/be108555-da2a-4abc-a46b-acbe8b55bd25%40app.fastmail.com

MariaDB AUTO_INCREMENT behavior (using the same InnoDB engine as MySQL)

https://dev.mysql.com/doc/refman/8.0/en/innodb-auto-increment-handling.html

https://dba.stackexchange.com/a/72099

For Table configurations that do not have client side primary key values, and offer server-generated primary key values (or no primary key) that the database in question is not able to invoke in a deterministic or sortable way relative to multiple parameter sets, the “insertmanyvalues” feature when tasked with satisfying the Insert.returning.sort_by_parameter_order requirement for an Insert statement may instead opt to use non-batched mode.

In this mode, the original SQL form of INSERT is maintained, and the “insertmanyvalues” feature will instead run the statement as given for each parameter set individually, organizing the returned rows into a full result set. Unlike previous SQLAlchemy versions, it does so in a tight loop that minimizes Python overhead. In some cases, such as on SQLite, “non-batched” mode performs exactly as well as “batched” mode.

For both “batched” and “non-batched” modes, the feature will necessarily invoke multiple INSERT statements using the DBAPI cursor.execute() method, within the scope of single call to the Core-level Connection.execute() method, with each statement containing up to a fixed limit of parameter sets. This limit is configurable as described below at Controlling the Batch Size. The separate calls to cursor.execute() are logged individually and also individually passed along to event listeners such as ConnectionEvents.before_cursor_execute() (see Logging and Events below).

In typical cases, the “insertmanyvalues” feature in order to provide INSERT..RETURNING with deterministic row order will automatically determine a sentinel column from a given table’s primary key, gracefully degrading to “row at a time” mode if one cannot be identified. As a completely optional feature, to get full “insertmanyvalues” bulk performance for tables that have server generated primary keys whose default generator functions aren’t compatible with the “sentinel” use case, other non-primary key columns may be marked as “sentinel” columns assuming they meet certain requirements. A typical example is a non-primary key Uuid column with a client side default such as the Python uuid.uuid4() function. There is also a construct to create simple integer columns with a a client side integer counter oriented towards the “insertmanyvalues” use case.

Sentinel columns may be indicated by adding Column.insert_sentinel to qualifying columns. The most basic “qualifying” column is a not-nullable, unique column with a client side default, such as a UUID column as follows:

When using ORM Declarative models, the same forms are available using the mapped_column construct:

While the values generated by the default generator must be unique, the actual UNIQUE constraint on the above “sentinel” column, indicated by the unique=True parameter, itself is optional and may be omitted if not desired.

There is also a special form of “insert sentinel” that’s a dedicated nullable integer column which makes use of a special default integer counter that’s only used during “insertmanyvalues” operations; as an additional behavior, the column will omit itself from SQL statements and result sets and behave in a mostly transparent manner. It does need to be physically present within the actual database table, however. This style of Column may be constructed using the function insert_sentinel():

When using ORM Declarative, a Declarative-friendly version of insert_sentinel() is available called orm_insert_sentinel(), which has the ability to be used on the Base class or a mixin; if packaged using declared_attr(), the column will apply itself to all table-bound subclasses including within joined inheritance hierarchies:

In the example above, both “my_table” and “sub_table” will have an additional integer column named “_sentinel” that can be used by the “insertmanyvalues” feature to help optimize bulk inserts used by the ORM.

A key characteristic of “insertmanyvalues” is that the size of the INSERT statement is limited on a fixed max number of “values” clauses as well as a dialect-specific fixed total number of bound parameters that may be represented in one INSERT statement at a time. When the number of parameter dictionaries given exceeds a fixed limit, or when the total number of bound parameters to be rendered in a single INSERT statement exceeds a fixed limit (the two fixed limits are separate), multiple INSERT statements will be invoked within the scope of a single Connection.execute() call, each of which accommodate for a portion of the parameter dictionaries, known as a “batch”. The number of parameter dictionaries represented within each “batch” is then known as the “batch size”. For example, a batch size of 500 means that each INSERT statement emitted will INSERT at most 500 rows.

It’s potentially important to be able to adjust the batch size, as a larger batch size may be more performant for an INSERT where the value sets themselves are relatively small, and a smaller batch size may be more appropriate for an INSERT that uses very large value sets, where both the size of the rendered SQL as well as the total data size being passed in one statement may benefit from being limited to a certain size based on backend behavior and memory constraints. For this reason the batch size can be configured on a per-Engine as well as a per-statement basis. The parameter limit on the other hand is fixed based on the known characteristics of the database in use.

The batch size defaults to 1000 for most backends, with an additional per-dialect “max number of parameters” limiting factor that may reduce the batch size further on a per-statement basis. The max number of parameters varies by dialect and server version; the largest size is 32700 (chosen as a healthy distance away from PostgreSQL’s limit of 32767 and SQLite’s modern limit of 32766, while leaving room for additional parameters in the statement as well as for DBAPI quirkiness). Older versions of SQLite (prior to 3.32.0) will set this value to 999. MariaDB has no established limit however 32700 remains as a limiting factor for SQL message size.

The value of the “batch size” can be affected Engine wide via the create_engine.insertmanyvalues_page_size parameter. Such as, to affect INSERT statements to include up to 100 parameter sets in each statement:

The batch size may also be affected on a per statement basis using the Connection.execution_options.insertmanyvalues_page_size execution option, such as per execution:

Or configured on the statement itself:

The “insertmanyvalues” feature integrates fully with SQLAlchemy’s statement logging as well as cursor events such as ConnectionEvents.before_cursor_execute(). When the list of parameters is broken into separate batches, each INSERT statement is logged and passed to event handlers individually. This is a major change compared to how the psycopg2-only feature worked in previous 1.x series of SQLAlchemy, where the production of multiple INSERT statements was hidden from logging and events. Logging display will truncate the long lists of parameters for readability, and will also indicate the specific batch of each statement. The example below illustrates an excerpt of this logging:

When non-batch mode takes place, logging will indicate this along with the insertmanyvalues message:

The PostgreSQL, SQLite, and MariaDB dialects offer backend-specific “upsert” constructs insert(), insert() and insert(), which are each Insert constructs that have an additional method such as on_conflict_do_update()` or ``on_duplicate_key(). These constructs also support “insertmanyvalues” behaviors when they are used with RETURNING, allowing efficient upserts with RETURNING to take place.

The Engine refers to a connection pool, which means under normal circumstances, there are open database connections present while the Engine object is still resident in memory. When an Engine is garbage collected, its connection pool is no longer referred to by that Engine, and assuming none of its connections are still checked out, the pool and its connections will also be garbage collected, which has the effect of closing out the actual database connections as well. But otherwise, the Engine will hold onto open database connections assuming it uses the normally default pool implementation of QueuePool.

The Engine is intended to normally be a permanent fixture established up-front and maintained throughout the lifespan of an application. It is not intended to be created and disposed on a per-connection basis; it is instead a registry that maintains both a pool of connections as well as configurational information about the database and DBAPI in use, as well as some degree of internal caching of per-database resources.

However, there are many cases where it is desirable that all connection resources referred to by the Engine be completely closed out. It’s generally not a good idea to rely on Python garbage collection for this to occur for these cases; instead, the Engine can be explicitly disposed using the Engine.dispose() method. This disposes of the engine’s underlying connection pool and replaces it with a new one that’s empty. Provided that the Engine is discarded at this point and no longer used, all checked-in connections which it refers to will also be fully closed.

Valid use cases for calling Engine.dispose() include:

When a program wants to release any remaining checked-in connections held by the connection pool and expects to no longer be connected to that database at all for any future operations.

When a program uses multiprocessing or fork(), and an Engine object is copied to the child process, Engine.dispose() should be called so that the engine creates brand new database connections local to that fork. Database connections generally do not travel across process boundaries. Use the Engine.dispose.close parameter set to False in this case. See the section Using Connection Pools with Multiprocessing or os.fork() for more background on this use case.

Within test suites or multitenancy scenarios where many ad-hoc, short-lived Engine objects may be created and disposed.

Connections that are checked out are not discarded when the engine is disposed or garbage collected, as these connections are still strongly referenced elsewhere by the application. However, after Engine.dispose() is called, those connections are no longer associated with that Engine; when they are closed, they will be returned to their now-orphaned connection pool which will ultimately be garbage collected, once all connections which refer to it are also no longer referenced anywhere. Since this process is not easy to control, it is strongly recommended that Engine.dispose() is called only after all checked out connections are checked in or otherwise de-associated from their pool.

An alternative for applications that are negatively impacted by the Engine object’s use of connection pooling is to disable pooling entirely. This typically incurs only a modest performance impact upon the use of new connections, and means that when a connection is checked in, it is entirely closed out and is not held in memory. See Switching Pool Implementations for guidelines on how to disable pooling.

Using Connection Pools with Multiprocessing or os.fork()

The introduction on using Connection.execute() made use of the text() construct in order to illustrate how textual SQL statements may be invoked. When working with SQLAlchemy, textual SQL is actually more of the exception rather than the norm, as the Core expression language and the ORM both abstract away the textual representation of SQL. However, the text() construct itself also provides some abstraction of textual SQL in that it normalizes how bound parameters are passed, as well as that it supports datatyping behavior for parameters and result set rows.

For the use case where one wants to invoke textual SQL directly passed to the underlying driver (known as the DBAPI) without any intervention from the text() construct, the Connection.exec_driver_sql() method may be used:

Added in version 1.4: Added the Connection.exec_driver_sql() method.

There are some cases where SQLAlchemy does not provide a genericized way at accessing some DBAPI functions, such as calling stored procedures as well as dealing with multiple result sets. In these cases, it’s just as expedient to deal with the raw DBAPI connection directly.

The most common way to access the raw DBAPI connection is to get it from an already present Connection object directly. It is present using the Connection.connection attribute:

The DBAPI connection here is actually a “proxied” in terms of the originating connection pool, however this is an implementation detail that in most cases can be ignored. As this DBAPI connection is still contained within the scope of an owning Connection object, it is best to make use of the Connection object for most features such as transaction control as well as calling the Connection.close() method; if these operations are performed on the DBAPI connection directly, the owning Connection will not be aware of these changes in state.

To overcome the limitations imposed by the DBAPI connection that is maintained by an owning Connection, a DBAPI connection is also available without the need to procure a Connection first, using the Engine.raw_connection() method of Engine:

This DBAPI connection is again a “proxied” form as was the case before. The purpose of this proxying is now apparent, as when we call the .close() method of this connection, the DBAPI connection is typically not actually closed, but instead released back to the engine’s connection pool:

While SQLAlchemy may in the future add built-in patterns for more DBAPI use cases, there are diminishing returns as these cases tend to be rarely needed and they also vary highly dependent on the type of DBAPI in use, so in any case the direct DBAPI calling pattern is always there for those cases where it is needed.

How do I get at the raw DBAPI connection when using an Engine? - includes additional details about how the DBAPI connection is accessed as well as the “driver” connection when using asyncio drivers.

Some recipes for DBAPI connection use follow.

SQLAlchemy supports calling stored procedures and user defined functions several ways. Please note that all DBAPIs have different practices, so you must consult your underlying DBAPI’s documentation for specifics in relation to your particular usage. The following examples are hypothetical and may not work with your underlying DBAPI.

For stored procedures or functions with special syntactical or parameter concerns, DBAPI-level callproc may potentially be used with your DBAPI. An example of this pattern is:

Not all DBAPIs use callproc and overall usage details will vary. The above example is only an illustration of how it might look to use a particular DBAPI function.

Your DBAPI may not have a callproc requirement or may require a stored procedure or user defined function to be invoked with another pattern, such as normal SQLAlchemy connection usage. One example of this usage pattern is, at the time of this documentation’s writing, executing a stored procedure in the PostgreSQL database with the psycopg2 DBAPI, which should be invoked with normal connection usage:

This above example is hypothetical. The underlying database is not guaranteed to support “CALL” or “SELECT” in these situations, and the keyword may vary dependent on the function being a stored procedure or a user defined function. You should consult your underlying DBAPI and database documentation in these situations to determine the correct syntax and patterns to use.

Multiple result set support is available from a raw DBAPI cursor using the nextset method:

The create_engine() function call locates the given dialect using setuptools entrypoints. These entry points can be established for third party dialects within the setup.py script. For example, to create a new dialect “foodialect://”, the steps are as follows:

Create a package called foodialect.

The package should have a module containing the dialect class, which is typically a subclass of sqlalchemy.engine.default.DefaultDialect. In this example let’s say it’s called FooDialect and its module is accessed via foodialect.dialect.

The entry point can be established in setup.cfg as follows:

If the dialect is providing support for a particular DBAPI on top of an existing SQLAlchemy-supported database, the name can be given including a database-qualification. For example, if FooDialect were in fact a MySQL dialect, the entry point could be established like this:

The above entrypoint would then be accessed as create_engine("mysql+foodialect://").

SQLAlchemy also allows a dialect to be registered within the current process, bypassing the need for separate installation. Use the register() function as follows:

The above will respond to create_engine("mysql+foodialect://") and load the MyMySQLDialect class from the myapp.dialect module.

Provides high-level functionality for a wrapped DB-API connection.

A set of hooks intended to augment the construction of an Engine object based on entrypoint names in a URL.

Connects a Pool and Dialect together to provide a source of database connectivity and behavior.

Encapsulate information about an error condition in progress.

Represent a ‘nested’, or SAVEPOINT transaction.

Represent the “root” transaction on a Connection.

Represent a database transaction in progress.

Represent a two-phase transaction.

inherits from sqlalchemy.engine.interfaces.ConnectionEventsTarget, sqlalchemy.inspection.Inspectable

Provides high-level functionality for a wrapped DB-API connection.

The Connection object is procured by calling the Engine.connect() method of the Engine object, and provides services for execution of SQL statements as well as transaction control.

The Connection object is not thread-safe. While a Connection can be shared among threads using properly synchronized access, it is still possible that the underlying DBAPI connection may not support shared access between threads. Check the DBAPI documentation for details.

The Connection object represents a single DBAPI connection checked out from the connection pool. In this state, the connection pool has no affect upon the connection, including its expiration or timeout state. For the connection pool to properly manage connections, connections should be returned to the connection pool (i.e. connection.close()) whenever the connection is not in use.

Construct a new Connection.

Begin a transaction prior to autobegin occurring.

Begin a nested transaction (i.e. SAVEPOINT) and return a transaction handle that controls the scope of the SAVEPOINT.

Begin a two-phase or XA transaction and return a transaction handle.

Close this Connection.

Commit the transaction that is currently in progress.

Detach the underlying DB-API connection from its connection pool.

Executes a string SQL statement on the DBAPI cursor directly, without any SQL compilation steps.

Executes a SQL statement construct and returns a CursorResult.

Set non-SQL options for the connection which take effect during execution.

get_execution_options()

Get the non-SQL options which will take effect during execution.

get_isolation_level()

Return the current actual isolation level that’s present on the database within the scope of this connection.

get_nested_transaction()

Return the current nested transaction in progress, if any.

Return the current root transaction in progress, if any.

in_nested_transaction()

Return True if a transaction is in progress.

Return True if a transaction is in progress.

Invalidate the underlying DBAPI connection associated with this Connection.

Roll back the transaction that is currently in progress.

Executes a SQL statement construct and returns a scalar object.

Executes and returns a scalar result set, which yields scalar values from the first column of each row.

Return the schema name for the given schema item taking into account current schema translate map.

Construct a new Connection.

Begin a transaction prior to autobegin occurring.

The returned object is an instance of RootTransaction. This object represents the “scope” of the transaction, which completes when either the Transaction.rollback() or Transaction.commit() method is called; the object also works as a context manager as illustrated above.

The Connection.begin() method begins a transaction that normally will be begun in any case when the connection is first used to execute a statement. The reason this method might be used would be to invoke the ConnectionEvents.begin() event at a specific time, or to organize code within the scope of a connection checkout in terms of context managed blocks, such as:

The above code is not fundamentally any different in its behavior than the following code which does not use Connection.begin(); the below style is known as “commit as you go” style:

From a database point of view, the Connection.begin() method does not emit any SQL or change the state of the underlying DBAPI connection in any way; the Python DBAPI does not have any concept of explicit transaction begin.

Working with Transactions and the DBAPI - in the SQLAlchemy Unified Tutorial

Connection.begin_nested() - use a SAVEPOINT

Connection.begin_twophase() - use a two phase /XID transaction

Engine.begin() - context manager available from Engine

Begin a nested transaction (i.e. SAVEPOINT) and return a transaction handle that controls the scope of the SAVEPOINT.

The returned object is an instance of NestedTransaction, which includes transactional methods NestedTransaction.commit() and NestedTransaction.rollback(); for a nested transaction, these methods correspond to the operations “RELEASE SAVEPOINT <name>” and “ROLLBACK TO SAVEPOINT <name>”. The name of the savepoint is local to the NestedTransaction object and is generated automatically. Like any other Transaction, the NestedTransaction may be used as a context manager as illustrated above which will “release” or “rollback” corresponding to if the operation within the block were successful or raised an exception.

Nested transactions require SAVEPOINT support in the underlying database, else the behavior is undefined. SAVEPOINT is commonly used to run operations within a transaction that may fail, while continuing the outer transaction. E.g.:

If Connection.begin_nested() is called without first calling Connection.begin() or Engine.begin(), the Connection object will “autobegin” the outer transaction first. This outer transaction may be committed using “commit-as-you-go” style, e.g.:

Changed in version 2.0: Connection.begin_nested() will now participate in the connection “autobegin” behavior that is new as of 2.0 / “future” style connections in 1.4.

Using SAVEPOINT - ORM support for SAVEPOINT

Begin a two-phase or XA transaction and return a transaction handle.

The returned object is an instance of TwoPhaseTransaction, which in addition to the methods provided by Transaction, also provides a TwoPhaseTransaction.prepare() method.

xid¶ – the two phase transaction id. If not supplied, a random id will be generated.

Connection.begin_twophase()

Close this Connection.

This results in a release of the underlying database resources, that is, the DBAPI connection referenced internally. The DBAPI connection is typically restored back to the connection-holding Pool referenced by the Engine that produced this Connection. Any transactional state present on the DBAPI connection is also unconditionally released via the DBAPI connection’s rollback() method, regardless of any Transaction object that may be outstanding with regards to this Connection.

This has the effect of also calling Connection.rollback() if any transaction is in place.

After Connection.close() is called, the Connection is permanently in a closed state, and will allow no further operations.

Return True if this connection is closed.

Commit the transaction that is currently in progress.

This method commits the current transaction if one has been started. If no transaction was started, the method has no effect, assuming the connection is in a non-invalidated state.

A transaction is begun on a Connection automatically whenever a statement is first executed, or when the Connection.begin() method is called.

The Connection.commit() method only acts upon the primary database transaction that is linked to the Connection object. It does not operate upon a SAVEPOINT that would have been invoked from the Connection.begin_nested() method; for control of a SAVEPOINT, call NestedTransaction.commit() on the NestedTransaction that is returned by the Connection.begin_nested() method itself.

The underlying DB-API connection managed by this Connection.

This is a SQLAlchemy connection-pool proxied connection which then has the attribute _ConnectionFairy.dbapi_connection that refers to the actual driver connection.

Working with Driver SQL and Raw DBAPI Connections

The initial-connection time isolation level associated with the Dialect in use.

This value is independent of the Connection.execution_options.isolation_level and Engine.execution_options.isolation_level execution options, and is determined by the Dialect when the first connection is created, by performing a SQL query against the database for the current isolation level before any additional commands have been emitted.

Calling this accessor does not invoke any new SQL queries.

Connection.get_isolation_level() - view current actual isolation level

create_engine.isolation_level - set per Engine isolation level

Connection.execution_options.isolation_level - set per Connection isolation level

Detach the underlying DB-API connection from its connection pool.

This Connection instance will remain usable. When closed (or exited from a context manager context as above), the DB-API connection will be literally closed and not returned to its originating pool.

This method can be used to insulate the rest of an application from a modified state on a connection (such as a transaction isolation level or similar).

Executes a string SQL statement on the DBAPI cursor directly, without any SQL compilation steps.

This can be used to pass any string directly to the cursor.execute() method of the DBAPI in use.

statement¶ – The statement str to be executed. Bound parameters must use the underlying DBAPI’s paramstyle, such as “qmark”, “pyformat”, “format”, etc.

parameters¶ – represent bound parameter values to be used in the execution. The format is one of: a dictionary of named parameters, a tuple of positional parameters, or a list containing either dictionaries or tuples for multiple-execute support.

E.g. multiple dictionaries:

The Connection.exec_driver_sql() method does not participate in the ConnectionEvents.before_execute() and ConnectionEvents.after_execute() events. To intercept calls to Connection.exec_driver_sql(), use ConnectionEvents.before_cursor_execute() and ConnectionEvents.after_cursor_execute().

Executes a SQL statement construct and returns a CursorResult.

The statement to be executed. This is always an object that is in both the ClauseElement and Executable hierarchies, including:

Insert, Update, Delete

TextClause and TextualSelect

DDL and objects which inherit from ExecutableDDLElement

parameters¶ – parameters which will be bound into the statement. This may be either a dictionary of parameter names to values, or a mutable sequence (e.g. a list) of dictionaries. When a list of dictionaries is passed, the underlying statement execution will make use of the DBAPI cursor.executemany() method. When a single dictionary is passed, the DBAPI cursor.execute() method will be used.

execution_options¶ – optional dictionary of execution options, which will be associated with the statement execution. This dictionary can provide a subset of the options that are accepted by Connection.execution_options().

Set non-SQL options for the connection which take effect during execution.

This method modifies this Connection in-place; the return value is the same Connection object upon which the method is called. Note that this is in contrast to the behavior of the execution_options methods on other objects such as Engine.execution_options() and Executable.execution_options(). The rationale is that many such execution options necessarily modify the state of the base DBAPI connection in any case so there is no feasible means of keeping the effect of such an option localized to a “sub” connection.

Changed in version 2.0: The Connection.execution_options() method, in contrast to other objects with this method, modifies the connection in-place without creating copy of it.

As discussed elsewhere, the Connection.execution_options() method accepts any arbitrary parameters including user defined names. All parameters given are consumable in a number of ways including by using the Connection.get_execution_options() method. See the examples at Executable.execution_options() and Engine.execution_options().

The keywords that are currently recognized by SQLAlchemy itself include all those listed under Executable.execution_options(), as well as others that are specific to Connection.

Available on: Connection, Engine.

A dictionary where Compiled objects will be cached when the Connection compiles a clause expression into a Compiled object. This dictionary will supersede the statement cache that may be configured on the Engine itself. If set to None, caching is disabled, even if the engine has a configured cache size.

Note that the ORM makes use of its own “compiled” caches for some operations, including flush operations. The caching used by the ORM internally supersedes a cache dictionary specified here.

Available on: Connection, Engine, Executable.

Adds the specified string token surrounded by brackets in log messages logged by the connection, i.e. the logging that’s enabled either via the create_engine.echo flag or via the logging.getLogger("sqlalchemy.engine") logger. This allows a per-connection or per-sub-engine token to be available which is useful for debugging concurrent connection scenarios.

Added in version 1.4.0b2.

Setting Per-Connection / Sub-Engine Tokens - usage example

create_engine.logging_name - adds a name to the name used by the Python logger object itself.

Available on: Connection, Engine.

Set the transaction isolation level for the lifespan of this Connection object. Valid values include those string values accepted by the create_engine.isolation_level parameter passed to create_engine(). These levels are semi-database specific; see individual dialect documentation for valid levels.

The isolation level option applies the isolation level by emitting statements on the DBAPI connection, and necessarily affects the original Connection object overall. The isolation level will remain at the given setting until explicitly changed, or when the DBAPI connection itself is released to the connection pool, i.e. the Connection.close() method is called, at which time an event handler will emit additional statements on the DBAPI connection in order to revert the isolation level change.

The isolation_level execution option may only be established before the Connection.begin() method is called, as well as before any SQL statements are emitted which would otherwise trigger “autobegin”, or directly after a call to Connection.commit() or Connection.rollback(). A database cannot change the isolation level on a transaction in progress.

The isolation_level execution option is implicitly reset if the Connection is invalidated, e.g. via the Connection.invalidate() method, or if a disconnection error occurs. The new connection produced after the invalidation will not have the selected isolation level re-applied to it automatically.

Setting Transaction Isolation Levels including DBAPI Autocommit

Connection.get_isolation_level() - view current actual level

Available on: Connection, Executable.

When True, if the final parameter list or dictionary is totally empty, will invoke the statement on the cursor as cursor.execute(statement), not passing the parameter collection at all. Some DBAPIs such as psycopg2 and mysql-python consider percent signs as significant only when parameters are present; this option allows code to generate SQL containing percent signs (and possibly other characters) that is neutral regarding whether it’s executed by the DBAPI or piped into a script that’s later invoked by command line tools.

Available on: Connection, Executable.

Indicate to the dialect that results should be “streamed” and not pre-buffered, if possible. For backends such as PostgreSQL, MySQL and MariaDB, this indicates the use of a “server side cursor” as opposed to a client side cursor. Other backends such as that of Oracle Database may already use server side cursors by default.

The usage of Connection.execution_options.stream_results is usually combined with setting a fixed number of rows to to be fetched in batches, to allow for efficient iteration of database rows while at the same time not loading all result rows into memory at once; this can be configured on a Result object using the Result.yield_per() method, after execution has returned a new Result. If Result.yield_per() is not used, the Connection.execution_options.stream_results mode of operation will instead use a dynamically sized buffer which buffers sets of rows at a time, growing on each batch based on a fixed growth size up until a limit which may be configured using the Connection.execution_options.max_row_buffer parameter.

When using the ORM to fetch ORM mapped objects from a result, Result.yield_per() should always be used with Connection.execution_options.stream_results, so that the ORM does not fetch all rows into new ORM objects at once.

For typical use, the Connection.execution_options.yield_per execution option should be preferred, which sets up both Connection.execution_options.stream_results and Result.yield_per() at once. This option is supported both at a core level by Connection as well as by the ORM Session; the latter is described at Fetching Large Result Sets with Yield Per.

Using Server Side Cursors (a.k.a. stream results) - background on Connection.execution_options.stream_results

Connection.execution_options.max_row_buffer

Connection.execution_options.yield_per

Fetching Large Result Sets with Yield Per - in the ORM Querying Guide describing the ORM version of yield_per

Available on: Connection, Executable. Sets a maximum buffer size to use when the Connection.execution_options.stream_results execution option is used on a backend that supports server side cursors. The default value if not specified is 1000.

Connection.execution_options.stream_results

Using Server Side Cursors (a.k.a. stream results)

Available on: Connection, Executable. Integer value applied which will set the Connection.execution_options.stream_results execution option and invoke Result.yield_per() automatically at once. Allows equivalent functionality as is present when using this parameter with the ORM.

Added in version 1.4.40.

Using Server Side Cursors (a.k.a. stream results) - background and examples on using server side cursors with Core.

Fetching Large Result Sets with Yield Per - in the ORM Querying Guide describing the ORM version of yield_per

insertmanyvalues_page_size¶ –

Available on: Connection, Engine. Number of rows to format into an INSERT statement when the statement uses “insertmanyvalues” mode, which is a paged form of bulk insert that is used for many backends when using executemany execution typically in conjunction with RETURNING. Defaults to 1000. May also be modified on a per-engine basis using the create_engine.insertmanyvalues_page_size parameter.

Added in version 2.0.

“Insert Many Values” Behavior for INSERT statements

schema_translate_map¶ –

Available on: Connection, Engine, Executable.

A dictionary mapping schema names to schema names, that will be applied to the Table.schema element of each Table encountered when SQL or DDL expression elements are compiled into strings; the resulting schema name will be converted based on presence in the map of the original name.

Translation of Schema Names

Boolean; when True, the cursor.rowcount attribute will be unconditionally memoized within the result and made available via the CursorResult.rowcount attribute. Normally, this attribute is only preserved for UPDATE and DELETE statements. Using this option, the DBAPIs rowcount value can be accessed for other kinds of statements such as INSERT and SELECT, to the degree that the DBAPI supports these statements. See CursorResult.rowcount for notes regarding the behavior of this attribute.

Added in version 2.0.28.

Engine.execution_options()

Executable.execution_options()

Connection.get_execution_options()

ORM Execution Options - documentation on all ORM-specific execution options

Get the non-SQL options which will take effect during execution.

Added in version 1.3.

Connection.execution_options()

Return the current actual isolation level that’s present on the database within the scope of this connection.

This attribute will perform a live SQL operation against the database in order to procure the current isolation level, so the value returned is the actual level on the underlying DBAPI connection regardless of how this state was set. This will be one of the four actual isolation modes READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE. It will not include the AUTOCOMMIT isolation level setting. Third party dialects may also feature additional isolation level settings.

This method will not report on the AUTOCOMMIT isolation level, which is a separate dbapi setting that’s independent of actual isolation level. When AUTOCOMMIT is in use, the database connection still has a “traditional” isolation mode in effect, that is typically one of the four values READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE.

Compare to the Connection.default_isolation_level accessor which returns the isolation level that is present on the database at initial connection time.

Connection.default_isolation_level - view default level

create_engine.isolation_level - set per Engine isolation level

Connection.execution_options.isolation_level - set per Connection isolation level

Return the current nested transaction in progress, if any.

Added in version 1.4.

Return the current root transaction in progress, if any.

Added in version 1.4.

Return True if a transaction is in progress.

Return True if a transaction is in progress.

Info dictionary associated with the underlying DBAPI connection referred to by this Connection, allowing user-defined data to be associated with the connection.

The data here will follow along with the DBAPI connection including after it is returned to the connection pool and used again in subsequent instances of Connection.

Invalidate the underlying DBAPI connection associated with this Connection.

An attempt will be made to close the underlying DBAPI connection immediately; however if this operation fails, the error is logged but not raised. The connection is then discarded whether or not close() succeeded.

Upon the next use (where “use” typically means using the Connection.execute() method or similar), this Connection will attempt to procure a new DBAPI connection using the services of the Pool as a source of connectivity (e.g. a “reconnection”).

If a transaction was in progress (e.g. the Connection.begin() method has been called) when Connection.invalidate() method is called, at the DBAPI level all state associated with this transaction is lost, as the DBAPI connection is closed. The Connection will not allow a reconnection to proceed until the Transaction object is ended, by calling the Transaction.rollback() method; until that point, any attempt at continuing to use the Connection will raise an InvalidRequestError. This is to prevent applications from accidentally continuing an ongoing transactional operations despite the fact that the transaction has been lost due to an invalidation.

The Connection.invalidate() method, just like auto-invalidation, will at the connection pool level invoke the PoolEvents.invalidate() event.

exception¶ – an optional Exception instance that’s the reason for the invalidation. is passed along to event handlers and logging functions.

Return True if this connection was invalidated.

This does not indicate whether or not the connection was invalidated at the pool level, however

Roll back the transaction that is currently in progress.

This method rolls back the current transaction if one has been started. If no transaction was started, the method has no effect. If a transaction was started and the connection is in an invalidated state, the transaction is cleared using this method.

A transaction is begun on a Connection automatically whenever a statement is first executed, or when the Connection.begin() method is called.

The Connection.rollback() method only acts upon the primary database transaction that is linked to the Connection object. It does not operate upon a SAVEPOINT that would have been invoked from the Connection.begin_nested() method; for control of a SAVEPOINT, call NestedTransaction.rollback() on the NestedTransaction that is returned by the Connection.begin_nested() method itself.

Executes a SQL statement construct and returns a scalar object.

This method is shorthand for invoking the Result.scalar() method after invoking the Connection.execute() method. Parameters are equivalent.

a scalar Python value representing the first column of the first row returned.

Executes and returns a scalar result set, which yields scalar values from the first column of each row.

This method is equivalent to calling Connection.execute() to receive a Result object, then invoking the Result.scalars() method to produce a ScalarResult instance.

Added in version 1.4.24.

Return the schema name for the given schema item taking into account current schema translate map.

A set of hooks intended to augment the construction of an Engine object based on entrypoint names in a URL.

The purpose of CreateEnginePlugin is to allow third-party systems to apply engine, pool and dialect level event listeners without the need for the target application to be modified; instead, the plugin names can be added to the database URL. Target applications for CreateEnginePlugin include:

connection and SQL performance tools, e.g. which use events to track number of checkouts and/or time spent with statements

connectivity plugins such as proxies

A rudimentary CreateEnginePlugin that attaches a logger to an Engine object might look like:

Plugins are registered using entry points in a similar way as that of dialects:

A plugin that uses the above names would be invoked from a database URL as in:

The plugin URL parameter supports multiple instances, so that a URL may specify multiple plugins; they are loaded in the order stated in the URL:

The plugin names may also be passed directly to create_engine() using the create_engine.plugins argument:

Added in version 1.2.3: plugin names can also be specified to create_engine() as a list

A plugin may consume plugin-specific arguments from the URL object as well as the kwargs dictionary, which is the dictionary of arguments passed to the create_engine() call. “Consuming” these arguments includes that they must be removed when the plugin initializes, so that the arguments are not passed along to the Dialect constructor, where they will raise an ArgumentError because they are not known by the dialect.

As of version 1.4 of SQLAlchemy, arguments should continue to be consumed from the kwargs dictionary directly, by removing the values with a method such as dict.pop. Arguments from the URL object should be consumed by implementing the CreateEnginePlugin.update_url() method, returning a new copy of the URL with plugin-specific parameters removed:

Arguments like those illustrated above would be consumed from a create_engine() call such as:

Changed in version 1.4: The URL object is now immutable; a CreateEnginePlugin that needs to alter the URL should implement the newly added CreateEnginePlugin.update_url() method, which is invoked after the plugin is constructed.

For migration, construct the plugin in the following way, checking for the existence of the CreateEnginePlugin.update_url() method to detect which version is running:

The URL object is now immutable - overview of the URL change which also includes notes regarding CreateEnginePlugin.

When the engine creation process completes and produces the Engine object, it is again passed to the plugin via the CreateEnginePlugin.engine_created() hook. In this hook, additional changes can be made to the engine, most typically involving setup of events (e.g. those defined in Core Events).

Construct a new CreateEnginePlugin.

Receive the Engine object when it is fully constructed.

handle_dialect_kwargs()

parse and modify dialect kwargs

parse and modify pool kwargs

Construct a new CreateEnginePlugin.

The plugin object is instantiated individually for each call to create_engine(). A single Engine will be passed to the CreateEnginePlugin.engine_created() method corresponding to this URL.

the URL object. The plugin may inspect the URL for arguments. Arguments used by the plugin should be removed, by returning an updated URL from the CreateEnginePlugin.update_url() method.

Changed in version 1.4: The URL object is now immutable, so a CreateEnginePlugin that needs to alter the URL object should implement the CreateEnginePlugin.update_url() method.

kwargs¶ – The keyword arguments passed to create_engine().

Receive the Engine object when it is fully constructed.

The plugin may make additional changes to the engine, such as registering engine or connection pool events.

parse and modify dialect kwargs

parse and modify pool kwargs

A new URL should be returned. This method is typically used to consume configuration arguments from the URL which must be removed, as they will not be recognized by the dialect. The URL.difference_update_query() method is available to remove these arguments. See the docstring at CreateEnginePlugin for an example.

Added in version 1.4.

inherits from sqlalchemy.engine.interfaces.ConnectionEventsTarget, sqlalchemy.log.Identified, sqlalchemy.inspection.Inspectable

Connects a Pool and Dialect together to provide a source of database connectivity and behavior.

An Engine object is instantiated publicly using the create_engine() function.

Working with Engines and Connections

Return a context manager delivering a Connection with a Transaction established.

clear_compiled_cache()

Clear the compiled cache associated with the dialect.

Return a new Connection object.

Dispose of the connection pool used by this Engine.

Return a new Engine that will provide Connection objects with the given execution options.

get_execution_options()

Get the non-SQL options which will take effect during execution.

Return a “raw” DBAPI connection from the connection pool.

update_execution_options()

Update the default execution_options dictionary of this Engine.

Return a context manager delivering a Connection with a Transaction established.

Upon successful operation, the Transaction is committed. If an error is raised, the Transaction is rolled back.

Engine.connect() - procure a Connection from an Engine.

Connection.begin() - start a Transaction for a particular Connection.

Clear the compiled cache associated with the dialect.

This applies only to the built-in cache that is established via the create_engine.query_cache_size parameter. It will not impact any dictionary caches that were passed via the Connection.execution_options.compiled_cache parameter.

Added in version 1.4.

Return a new Connection object.

The Connection acts as a Python context manager, so the typical use of this method looks like:

Where above, after the block is completed, the connection is “closed” and its underlying DBAPI resources are returned to the connection pool. This also has the effect of rolling back any transaction that was explicitly begun or was begun via autobegin, and will emit the ConnectionEvents.rollback() event if one was started and is still in progress.

Dispose of the connection pool used by this Engine.

A new connection pool is created immediately after the old one has been disposed. The previous connection pool is disposed either actively, by closing out all currently checked-in connections in that pool, or passively, by losing references to it but otherwise not closing any connections. The latter strategy is more appropriate for an initializer in a forked Python process.

if left at its default of True, has the effect of fully closing all currently checked in database connections. Connections that are still checked out will not be closed, however they will no longer be associated with this Engine, so when they are closed individually, eventually the Pool which they are associated with will be garbage collected and they will be closed out fully, if not already closed on checkin.

If set to False, the previous connection pool is de-referenced, and otherwise not touched in any way.

Added in version 1.4.33: Added the Engine.dispose.close parameter to allow the replacement of a connection pool in a child process without interfering with the connections used by the parent process.

Using Connection Pools with Multiprocessing or os.fork()

Driver name of the Dialect in use by this Engine.

Used for legacy schemes that accept Connection / Engine objects within the same variable.

Return a new Engine that will provide Connection objects with the given execution options.

The returned Engine remains related to the original Engine in that it shares the same connection pool and other state:

The Pool used by the new Engine is the same instance. The Engine.dispose() method will replace the connection pool instance for the parent engine as well as this one.

Event listeners are “cascaded” - meaning, the new Engine inherits the events of the parent, and new events can be associated with the new Engine individually.

The logging configuration and logging_name is copied from the parent Engine.

The intent of the Engine.execution_options() method is to implement schemes where multiple Engine objects refer to the same connection pool, but are differentiated by options that affect some execution-level behavior for each engine. One such example is breaking into separate “reader” and “writer” Engine instances, where one Engine has a lower isolation level setting configured or is even transaction-disabled using “autocommit”. An example of this configuration is at Maintaining Multiple Isolation Levels for a Single Engine.

Another example is one that uses a custom option shard_id which is consumed by an event to change the current schema on a database connection:

The above recipe illustrates two Engine objects that will each serve as factories for Connection objects that have pre-established “shard_id” execution options present. A ConnectionEvents.before_cursor_execute() event handler then interprets this execution option to emit a MySQL use statement to switch databases before a statement execution, while at the same time keeping track of which database we’ve established using the Connection.info dictionary.

Connection.execution_options() - update execution options on a Connection object.

Engine.update_execution_options() - update the execution options for a given Engine in place.

Engine.get_execution_options()

Get the non-SQL options which will take effect during execution.

Engine.execution_options()

String name of the Dialect in use by this Engine.

Return a “raw” DBAPI connection from the connection pool.

The returned object is a proxied version of the DBAPI connection object used by the underlying driver in use. The object will have all the same behavior as the real DBAPI connection, except that its close() method will result in the connection being returned to the pool, rather than being closed for real.

This method provides direct DBAPI connection access for special situations when the API provided by Connection is not needed. When a Connection object is already present, the DBAPI connection is available using the Connection.connection accessor.

Working with Driver SQL and Raw DBAPI Connections

Update the default execution_options dictionary of this Engine.

The given keys/values in **opt are added to the default execution options that will be used for all connections. The initial contents of this dictionary can be sent via the execution_options parameter to create_engine().

Connection.execution_options()

Engine.execution_options()

Encapsulate information about an error condition in progress.

This object exists solely to be passed to the DialectEvents.handle_error() event, supporting an interface that can be extended without backwards-incompatibility.

The exception that was returned by the previous handler in the exception chain, if any.

The Connection in use during the exception.

The DBAPI cursor object.

The Engine in use during the exception.

The ExecutionContext corresponding to the execution operation in progress.

invalidate_pool_on_disconnect

Represent whether all connections in the pool should be invalidated when a “disconnect” condition is in effect.

Represent whether the exception as occurred represents a “disconnect” condition.

Indicates if this error is occurring within the “pre-ping” step performed when create_engine.pool_pre_ping is set to True. In this mode, the ExceptionContext.engine attribute will be None. The dialect in use is accessible via the ExceptionContext.dialect attribute.

The exception object which was caught.

Parameter collection that was emitted directly to the DBAPI.

The sqlalchemy.exc.StatementError which wraps the original, and will be raised if exception handling is not circumvented by the event.

String SQL statement that was emitted directly to the DBAPI.

The exception that was returned by the previous handler in the exception chain, if any.

If present, this exception will be the one ultimately raised by SQLAlchemy unless a subsequent handler replaces it.

The Connection in use during the exception.

This member is present, except in the case of a failure when first connecting.

ExceptionContext.engine

The DBAPI cursor object.

This member is present for all invocations of the event hook.

Added in version 2.0.

The Engine in use during the exception.

This member is present in all cases except for when handling an error within the connection pool “pre-ping” process.

The ExecutionContext corresponding to the execution operation in progress.

This is present for statement execution operations, but not for operations such as transaction begin/end. It also is not present when the exception was raised before the ExecutionContext could be constructed.

Note that the ExceptionContext.statement and ExceptionContext.parameters members may represent a different value than that of the ExecutionContext, potentially in the case where a ConnectionEvents.before_cursor_execute() event or similar modified the statement/parameters to be sent.

Represent whether all connections in the pool should be invalidated when a “disconnect” condition is in effect.

Setting this flag to False within the scope of the DialectEvents.handle_error() event will have the effect such that the full collection of connections in the pool will not be invalidated during a disconnect; only the current connection that is the subject of the error will actually be invalidated.

The purpose of this flag is for custom disconnect-handling schemes where the invalidation of other connections in the pool is to be performed based on other conditions, or even on a per-connection basis.

Represent whether the exception as occurred represents a “disconnect” condition.

This flag will always be True or False within the scope of the DialectEvents.handle_error() handler.

SQLAlchemy will defer to this flag in order to determine whether or not the connection should be invalidated subsequently. That is, by assigning to this flag, a “disconnect” event which then results in a connection and pool invalidation can be invoked or prevented by changing this flag.

The pool “pre_ping” handler enabled using the create_engine.pool_pre_ping parameter does not consult this event before deciding if the “ping” returned false, as opposed to receiving an unhandled error. For this use case, the legacy recipe based on engine_connect() may be used. A future API allow more comprehensive customization of the “disconnect” detection mechanism across all functions.

Indicates if this error is occurring within the “pre-ping” step performed when create_engine.pool_pre_ping is set to True. In this mode, the ExceptionContext.engine attribute will be None. The dialect in use is accessible via the ExceptionContext.dialect attribute.

Added in version 2.0.5.

The exception object which was caught.

This member is always present.

Parameter collection that was emitted directly to the DBAPI.

The sqlalchemy.exc.StatementError which wraps the original, and will be raised if exception handling is not circumvented by the event.

May be None, as not all exception types are wrapped by SQLAlchemy. For DBAPI-level exceptions that subclass the dbapi’s Error class, this field will always be present.

String SQL statement that was emitted directly to the DBAPI.

inherits from sqlalchemy.engine.Transaction

Represent a ‘nested’, or SAVEPOINT transaction.

The NestedTransaction object is created by calling the Connection.begin_nested() method of Connection.

When using NestedTransaction, the semantics of “begin” / “commit” / “rollback” are as follows:

the “begin” operation corresponds to the “BEGIN SAVEPOINT” command, where the savepoint is given an explicit name that is part of the state of this object.

The NestedTransaction.commit() method corresponds to a “RELEASE SAVEPOINT” operation, using the savepoint identifier associated with this NestedTransaction.

The NestedTransaction.rollback() method corresponds to a “ROLLBACK TO SAVEPOINT” operation, using the savepoint identifier associated with this NestedTransaction.

The rationale for mimicking the semantics of an outer transaction in terms of savepoints so that code may deal with a “savepoint” transaction and an “outer” transaction in an agnostic way.

Using SAVEPOINT - ORM version of the SAVEPOINT API.

Close this Transaction.

Commit this Transaction.

Roll back this Transaction.

inherited from the Transaction.close() method of Transaction

Close this Transaction.

If this transaction is the base transaction in a begin/commit nesting, the transaction will rollback(). Otherwise, the method returns.

This is used to cancel a Transaction without affecting the scope of an enclosing transaction.

inherited from the Transaction.commit() method of Transaction

Commit this Transaction.

The implementation of this may vary based on the type of transaction in use:

For a simple database transaction (e.g. RootTransaction), it corresponds to a COMMIT.

For a NestedTransaction, it corresponds to a “RELEASE SAVEPOINT” operation.

For a TwoPhaseTransaction, DBAPI-specific methods for two phase transactions may be used.

inherited from the Transaction.rollback() method of Transaction

Roll back this Transaction.

The implementation of this may vary based on the type of transaction in use:

For a simple database transaction (e.g. RootTransaction), it corresponds to a ROLLBACK.

For a NestedTransaction, it corresponds to a “ROLLBACK TO SAVEPOINT” operation.

For a TwoPhaseTransaction, DBAPI-specific methods for two phase transactions may be used.

inherits from sqlalchemy.engine.Transaction

Represent the “root” transaction on a Connection.

This corresponds to the current “BEGIN/COMMIT/ROLLBACK” that’s occurring for the Connection. The RootTransaction is created by calling upon the Connection.begin() method, and remains associated with the Connection throughout its active span. The current RootTransaction in use is accessible via the Connection.get_transaction method of Connection.

In 2.0 style use, the Connection also employs “autobegin” behavior that will create a new RootTransaction whenever a connection in a non-transactional state is used to emit commands on the DBAPI connection. The scope of the RootTransaction in 2.0 style use can be controlled using the Connection.commit() and Connection.rollback() methods.

Close this Transaction.

Commit this Transaction.

Roll back this Transaction.

inherited from the Transaction.close() method of Transaction

Close this Transaction.

If this transaction is the base transaction in a begin/commit nesting, the transaction will rollback(). Otherwise, the method returns.

This is used to cancel a Transaction without affecting the scope of an enclosing transaction.

inherited from the Transaction.commit() method of Transaction

Commit this Transaction.

The implementation of this may vary based on the type of transaction in use:

For a simple database transaction (e.g. RootTransaction), it corresponds to a COMMIT.

For a NestedTransaction, it corresponds to a “RELEASE SAVEPOINT” operation.

For a TwoPhaseTransaction, DBAPI-specific methods for two phase transactions may be used.

inherited from the Transaction.rollback() method of Transaction

Roll back this Transaction.

The implementation of this may vary based on the type of transaction in use:

For a simple database transaction (e.g. RootTransaction), it corresponds to a ROLLBACK.

For a NestedTransaction, it corresponds to a “ROLLBACK TO SAVEPOINT” operation.

For a TwoPhaseTransaction, DBAPI-specific methods for two phase transactions may be used.

inherits from sqlalchemy.engine.util.TransactionalContext

Represent a database transaction in progress.

The Transaction object is procured by calling the Connection.begin() method of Connection:

The object provides rollback() and commit() methods in order to control transaction boundaries. It also implements a context manager interface so that the Python with statement can be used with the Connection.begin() method:

The Transaction object is not threadsafe.

Connection.begin_twophase()

Connection.begin_nested()

Close this Transaction.

Commit this Transaction.

Roll back this Transaction.

Close this Transaction.

If this transaction is the base transaction in a begin/commit nesting, the transaction will rollback(). Otherwise, the method returns.

This is used to cancel a Transaction without affecting the scope of an enclosing transaction.

Commit this Transaction.

The implementation of this may vary based on the type of transaction in use:

For a simple database transaction (e.g. RootTransaction), it corresponds to a COMMIT.

For a NestedTransaction, it corresponds to a “RELEASE SAVEPOINT” operation.

For a TwoPhaseTransaction, DBAPI-specific methods for two phase transactions may be used.

Roll back this Transaction.

The implementation of this may vary based on the type of transaction in use:

For a simple database transaction (e.g. RootTransaction), it corresponds to a ROLLBACK.

For a NestedTransaction, it corresponds to a “ROLLBACK TO SAVEPOINT” operation.

For a TwoPhaseTransaction, DBAPI-specific methods for two phase transactions may be used.

inherits from sqlalchemy.engine.RootTransaction

Represent a two-phase transaction.

A new TwoPhaseTransaction object may be procured using the Connection.begin_twophase() method.

The interface is the same as that of Transaction with the addition of the prepare() method.

Close this Transaction.

Commit this Transaction.

Prepare this TwoPhaseTransaction.

Roll back this Transaction.

inherited from the Transaction.close() method of Transaction

Close this Transaction.

If this transaction is the base transaction in a begin/commit nesting, the transaction will rollback(). Otherwise, the method returns.

This is used to cancel a Transaction without affecting the scope of an enclosing transaction.

inherited from the Transaction.commit() method of Transaction

Commit this Transaction.

The implementation of this may vary based on the type of transaction in use:

For a simple database transaction (e.g. RootTransaction), it corresponds to a COMMIT.

For a NestedTransaction, it corresponds to a “RELEASE SAVEPOINT” operation.

For a TwoPhaseTransaction, DBAPI-specific methods for two phase transactions may be used.

Prepare this TwoPhaseTransaction.

After a PREPARE, the transaction can be committed.

inherited from the Transaction.rollback() method of Transaction

Roll back this Transaction.

The implementation of this may vary based on the type of transaction in use:

For a simple database transaction (e.g. RootTransaction), it corresponds to a ROLLBACK.

For a NestedTransaction, it corresponds to a “ROLLBACK TO SAVEPOINT” operation.

For a TwoPhaseTransaction, DBAPI-specific methods for two phase transactions may be used.

ChunkedIteratorResult

An IteratorResult that works from an iterator-producing callable.

A Result that is representing state from a DBAPI cursor.

A wrapper for a Result that returns objects other than Row objects, such as dictionaries or scalar objects.

Represents a Result object in a “frozen” state suitable for caching.

A Result that gets data from a Python iterator of Row objects or similar row-like data.

A wrapper for a Result that returns dictionary values rather than Row values.

A Result that is merged from any number of Result objects.

Represent a set of database results.

Represent a single result row.

A Mapping that maps column names and objects to Row values.

A wrapper for a Result that returns scalar values rather than Row values.

A Result that’s typed as returning plain Python tuples instead of rows.

inherits from sqlalchemy.engine.IteratorResult

An IteratorResult that works from an iterator-producing callable.

The given chunks argument is a function that is given a number of rows to return in each chunk, or None for all rows. The function should then return an un-consumed iterator of lists, each list of the requested size.

The function can be called at any time again, in which case it should continue from the same result set but adjust the chunk size as given.

Added in version 1.4.

Configure the row-fetching strategy to fetch num rows at a time.

Configure the row-fetching strategy to fetch num rows at a time.

This impacts the underlying behavior of the result when iterating over the result object, or otherwise making use of methods such as Result.fetchone() that return one row at a time. Data from the underlying cursor or other data source will be buffered up to this many rows in memory, and the buffered collection will then be yielded out one row at a time or as many rows are requested. Each time the buffer clears, it will be refreshed to this many rows or as many rows remain if fewer remain.

The Result.yield_per() method is generally used in conjunction with the Connection.execution_options.stream_results execution option, which will allow the database dialect in use to make use of a server side cursor, if the DBAPI supports a specific “server side cursor” mode separate from its default mode of operation.

Consider using the Connection.execution_options.yield_per execution option, which will simultaneously set Connection.execution_options.stream_results to ensure the use of server side cursors, as well as automatically invoke the Result.yield_per() method to establish a fixed row buffer size at once.

The Connection.execution_options.yield_per execution option is available for ORM operations, with Session-oriented use described at Fetching Large Result Sets with Yield Per. The Core-only version which works with Connection is new as of SQLAlchemy 1.4.40.

Added in version 1.4.

num¶ – number of rows to fetch each time the buffer is refilled. If set to a value below 1, fetches all rows for the next buffer.

Using Server Side Cursors (a.k.a. stream results) - describes Core behavior for Result.yield_per()

Fetching Large Result Sets with Yield Per - in the ORM Querying Guide

inherits from sqlalchemy.engine.Result

A Result that is representing state from a DBAPI cursor.

Changed in version 1.4: The CursorResult` class replaces the previous ResultProxy interface. This classes are based on the Result calling API which provides an updated usage model and calling facade for SQLAlchemy Core and SQLAlchemy ORM.

Returns database rows via the Row class, which provides additional API features and behaviors on top of the raw data returned by the DBAPI. Through the use of filters such as the Result.scalars() method, other kinds of objects may also be returned.

Using SELECT Statements - introductory material for accessing CursorResult and Row objects.

Return all rows in a sequence.

Close this CursorResult.

Establish the columns that should be returned in each row.

A synonym for the Result.all() method.

Fetch the first row or None if no row is present.

Return a callable object that will produce copies of this Result when invoked.

Return an iterable view which yields the string keys that would be represented by each Row.

last_inserted_params()

Return the collection of inserted parameters from this execution.

last_updated_params()

Return the collection of updated parameters from this execution.

lastrow_has_defaults()

Return lastrow_has_defaults() from the underlying ExecutionContext.

Apply a mappings filter to returned rows, returning an instance of MappingResult.

Merge this Result with other compatible result objects.

Return exactly one row or raise an exception.

Return at most one result or raise an exception.

Iterate through sub-lists of rows of the size given.

Return postfetch_cols() from the underlying ExecutionContext.

Return prefetch_cols() from the underlying ExecutionContext.

Return the ‘rowcount’ for this result.

Fetch the first column of the first row, and close the result set.

Return exactly one scalar result or raise an exception.

Return exactly one scalar result or None.

Return a ScalarResult filtering object which will return single elements rather than Row objects.

splice_horizontally()

Return a new CursorResult that “horizontally splices” together the rows of this CursorResult with that of another CursorResult.

Return a new CursorResult that “vertically splices”, i.e. “extends”, the rows of this CursorResult with that of another CursorResult.

supports_sane_multi_rowcount()

Return supports_sane_multi_rowcount from the dialect.

supports_sane_rowcount()

Return supports_sane_rowcount from the dialect.

Apply a “typed tuple” typing filter to returned rows.

Apply unique filtering to the objects returned by this Result.

Configure the row-fetching strategy to fetch num rows at a time.

inherited from the Result.all() method of Result

Return all rows in a sequence.

Closes the result set after invocation. Subsequent invocations will return an empty sequence.

Added in version 1.4.

a sequence of Row objects.

Using Server Side Cursors (a.k.a. stream results) - How to stream a large result set without loading it completely in python.

Close this CursorResult.

This closes out the underlying DBAPI cursor corresponding to the statement execution, if one is still present. Note that the DBAPI cursor is automatically released when the CursorResult exhausts all available rows. CursorResult.close() is generally an optional method except in the case when discarding a CursorResult that still has additional rows pending for fetch.

After this method is called, it is no longer valid to call upon the fetch methods, which will raise a ResourceClosedError on subsequent use.

Working with Engines and Connections

inherited from the Result.columns() method of Result

Establish the columns that should be returned in each row.

This method may be used to limit the columns returned as well as to reorder them. The given list of expressions are normally a series of integers or string key names. They may also be appropriate ColumnElement objects which correspond to a given statement construct.

Changed in version 2.0: Due to a bug in 1.4, the Result.columns() method had an incorrect behavior where calling upon the method with just one index would cause the Result object to yield scalar values rather than Row objects. In version 2.0, this behavior has been corrected such that calling upon Result.columns() with a single index will produce a Result object that continues to yield Row objects, which include only a single column.

Example of using the column objects from the statement itself:

Added in version 1.4.

*col_expressions¶ – indicates columns to be returned. Elements may be integer row indexes, string column names, or appropriate ColumnElement objects corresponding to a select construct.

this Result object with the modifications given.

inherited from the Result.fetchall() method of Result

A synonym for the Result.all() method.

inherited from the Result.fetchmany() method of Result

When all rows are exhausted, returns an empty sequence.

This method is provided for backwards compatibility with SQLAlchemy 1.x.x.

To fetch rows in groups, use the Result.partitions() method.

a sequence of Row objects.

inherited from the Result.fetchone() method of Result

When all rows are exhausted, returns None.

This method is provided for backwards compatibility with SQLAlchemy 1.x.x.

To fetch the first row of a result only, use the Result.first() method. To iterate through all rows, iterate the Result object directly.

a Row object if no filters are applied, or None if no rows remain.

inherited from the Result.first() method of Result

Fetch the first row or None if no row is present.

Closes the result set and discards remaining rows.

This method returns one row, e.g. tuple, by default. To return exactly one single scalar value, that is, the first column of the first row, use the Result.scalar() method, or combine Result.scalars() and Result.first().

Additionally, in contrast to the behavior of the legacy ORM Query.first() method, no limit is applied to the SQL query which was invoked to produce this Result; for a DBAPI driver that buffers results in memory before yielding rows, all rows will be sent to the Python process and all but the first row will be discarded.

ORM Query Unified with Core Select

a Row object, or None if no rows remain.

inherited from the Result.freeze() method of Result

Return a callable object that will produce copies of this Result when invoked.

The callable object returned is an instance of FrozenResult.

This is used for result set caching. The method must be called on the result when it has been unconsumed, and calling the method will consume the result fully. When the FrozenResult is retrieved from a cache, it can be called any number of times where it will produce a new Result object each time against its stored set of rows.

Re-Executing Statements - example usage within the ORM to implement a result-set cache.

Return the primary key for the row just inserted.

The return value is a Row object representing a named tuple of primary key values in the order in which the primary key columns are configured in the source Table.

Changed in version 1.4.8: - the CursorResult.inserted_primary_key value is now a named tuple via the Row class, rather than a plain tuple.

This accessor only applies to single row insert() constructs which did not explicitly specify Insert.returning(). Support for multirow inserts, while not yet available for most backends, would be accessed using the CursorResult.inserted_primary_key_rows accessor.

Note that primary key columns which specify a server_default clause, or otherwise do not qualify as “autoincrement” columns (see the notes at Column), and were generated using the database-side default, will appear in this list as None unless the backend supports “returning” and the insert statement executed with the “implicit returning” enabled.

Raises InvalidRequestError if the executed statement is not a compiled expression construct or is not an insert() construct.

Return the value of CursorResult.inserted_primary_key as a row contained within a list; some dialects may support a multiple row form as well.

As indicated below, in current SQLAlchemy versions this accessor is only useful beyond what’s already supplied by CursorResult.inserted_primary_key when using the psycopg2 dialect. Future versions hope to generalize this feature to more dialects.

This accessor is added to support dialects that offer the feature that is currently implemented by the Psycopg2 Fast Execution Helpers feature, currently only the psycopg2 dialect, which provides for many rows to be INSERTed at once while still retaining the behavior of being able to return server-generated primary key values.

When using the psycopg2 dialect, or other dialects that may support “fast executemany” style inserts in upcoming releases : When invoking an INSERT statement while passing a list of rows as the second argument to Connection.execute(), this accessor will then provide a list of rows, where each row contains the primary key value for each row that was INSERTed.

When using all other dialects / backends that don’t yet support this feature: This accessor is only useful for single row INSERT statements, and returns the same information as that of the CursorResult.inserted_primary_key within a single-element list. When an INSERT statement is executed in conjunction with a list of rows to be INSERTed, the list will contain one row per row inserted in the statement, however it will contain None for any server-generated values.

Future releases of SQLAlchemy will further generalize the “fast execution helper” feature of psycopg2 to suit other dialects, thus allowing this accessor to be of more general use.

Added in version 1.4.

CursorResult.inserted_primary_key

True if this CursorResult is the result of a executing an expression language compiled insert() construct.

When True, this implies that the inserted_primary_key attribute is accessible, assuming the statement did not include a user defined “returning” construct.

inherited from the sqlalchemy.engine._WithKeys.keys method of sqlalchemy.engine._WithKeys

Return an iterable view which yields the string keys that would be represented by each Row.

The keys can represent the labels of the columns returned by a core statement or the names of the orm classes returned by an orm execution.

The view also can be tested for key containment using the Python in operator, which will test both for the string keys represented in the view, as well as for alternate keys such as column objects.

Changed in version 1.4: a key view object is returned rather than a plain list.

Return the collection of inserted parameters from this execution.

Raises InvalidRequestError if the executed statement is not a compiled expression construct or is not an insert() construct.

Return the collection of updated parameters from this execution.

Raises InvalidRequestError if the executed statement is not a compiled expression construct or is not an update() construct.

Return lastrow_has_defaults() from the underlying ExecutionContext.

See ExecutionContext for details.

Return the ‘lastrowid’ accessor on the DBAPI cursor.

This is a DBAPI specific method and is only functional for those backends which support it, for statements where it is appropriate. It’s behavior is not consistent across backends.

Usage of this method is normally unnecessary when using insert() expression constructs; the CursorResult.inserted_primary_key attribute provides a tuple of primary key values for a newly inserted row, regardless of database backend.

inherited from the Result.mappings() method of Result

Apply a mappings filter to returned rows, returning an instance of MappingResult.

When this filter is applied, fetching rows will return RowMapping objects instead of Row objects.

Added in version 1.4.

a new MappingResult filtering object referring to this Result object.

Merge this Result with other compatible result objects.

The object returned is an instance of MergedResult, which will be composed of iterators from the given result objects.

The new result will use the metadata from this result object. The subsequent result objects must be against an identical set of result / cursor metadata, otherwise the behavior is undefined.

inherited from the Result.one() method of Result

Return exactly one row or raise an exception.

Raises NoResultFound if the result returns no rows, or MultipleResultsFound if multiple rows would be returned.

This method returns one row, e.g. tuple, by default. To return exactly one single scalar value, that is, the first column of the first row, use the Result.scalar_one() method, or combine Result.scalars() and Result.one().

Added in version 1.4.

MultipleResultsFound, NoResultFound

inherited from the Result.one_or_none() method of Result

Return at most one result or raise an exception.

Returns None if the result has no rows. Raises MultipleResultsFound if multiple rows are returned.

Added in version 1.4.

The first Row or None if no row is available.

inherited from the Result.partitions() method of Result

Iterate through sub-lists of rows of the size given.

Each list will be of the size given, excluding the last list to be yielded, which may have a small number of rows. No empty lists will be yielded.

The result object is automatically closed when the iterator is fully consumed.

Note that the backend driver will usually buffer the entire result ahead of time unless the Connection.execution_options.stream_results execution option is used indicating that the driver should not pre-buffer results, if possible. Not all drivers support this option and the option is silently ignored for those who do not.

When using the ORM, the Result.partitions() method is typically more effective from a memory perspective when it is combined with use of the yield_per execution option, which instructs both the DBAPI driver to use server side cursors, if available, as well as instructs the ORM loading internals to only build a certain amount of ORM objects from a result at a time before yielding them out.

Added in version 1.4.

size¶ – indicate the maximum number of rows to be present in each list yielded. If None, makes use of the value set by the Result.yield_per(), method, if it were called, or the Connection.execution_options.yield_per execution option, which is equivalent in this regard. If yield_per weren’t set, it makes use of the Result.fetchmany() default, which may be backend specific and not well defined.

Using Server Side Cursors (a.k.a. stream results)

Fetching Large Result Sets with Yield Per - in the ORM Querying Guide

Return postfetch_cols() from the underlying ExecutionContext.

See ExecutionContext for details.

Raises InvalidRequestError if the executed statement is not a compiled expression construct or is not an insert() or update() construct.

Return prefetch_cols() from the underlying ExecutionContext.

See ExecutionContext for details.

Raises InvalidRequestError if the executed statement is not a compiled expression construct or is not an insert() or update() construct.

Return the values of default columns that were fetched using the ValuesBase.return_defaults() feature.

The value is an instance of Row, or None if ValuesBase.return_defaults() was not used or if the backend does not support RETURNING.

ValuesBase.return_defaults()

Return a list of rows each containing the values of default columns that were fetched using the ValuesBase.return_defaults() feature.

The return value is a list of Row objects.

Added in version 1.4.

True if this CursorResult returns zero or more rows.

I.e. if it is legal to call the methods CursorResult.fetchone(), CursorResult.fetchmany() CursorResult.fetchall().

Overall, the value of CursorResult.returns_rows should always be synonymous with whether or not the DBAPI cursor had a .description attribute, indicating the presence of result columns, noting that a cursor that returns zero rows still has a .description if a row-returning statement was emitted.

This attribute should be True for all results that are against SELECT statements, as well as for DML statements INSERT/UPDATE/DELETE that use RETURNING. For INSERT/UPDATE/DELETE statements that were not using RETURNING, the value will usually be False, however there are some dialect-specific exceptions to this, such as when using the MSSQL / pyodbc dialect a SELECT is emitted inline in order to retrieve an inserted primary key value.

Return the ‘rowcount’ for this result.

The primary purpose of ‘rowcount’ is to report the number of rows matched by the WHERE criterion of an UPDATE or DELETE statement executed once (i.e. for a single parameter set), which may then be compared to the number of rows expected to be updated or deleted as a means of asserting data integrity.

This attribute is transferred from the cursor.rowcount attribute of the DBAPI before the cursor is closed, to support DBAPIs that don’t make this value available after cursor close. Some DBAPIs may offer meaningful values for other kinds of statements, such as INSERT and SELECT statements as well. In order to retrieve cursor.rowcount for these statements, set the Connection.execution_options.preserve_rowcount execution option to True, which will cause the cursor.rowcount value to be unconditionally memoized before any results are returned or the cursor is closed, regardless of statement type.

For cases where the DBAPI does not support rowcount for a particular kind of statement and/or execution, the returned value will be -1, which is delivered directly from the DBAPI and is part of PEP 249. All DBAPIs should support rowcount for single-parameter-set UPDATE and DELETE statements, however.

Notes regarding CursorResult.rowcount:

This attribute returns the number of rows matched, which is not necessarily the same as the number of rows that were actually modified. For example, an UPDATE statement may have no net change on a given row if the SET values given are the same as those present in the row already. Such a row would be matched but not modified. On backends that feature both styles, such as MySQL, rowcount is configured to return the match count in all cases.

CursorResult.rowcount in the default case is only useful in conjunction with an UPDATE or DELETE statement, and only with a single set of parameters. For other kinds of statements, SQLAlchemy will not attempt to pre-memoize the value unless the Connection.execution_options.preserve_rowcount execution option is used. Note that contrary to PEP 249, many DBAPIs do not support rowcount values for statements that are not UPDATE or DELETE, particularly when rows are being returned which are not fully pre-buffered. DBAPIs that dont support rowcount for a particular kind of statement should return the value -1 for such statements.

CursorResult.rowcount may not be meaningful when executing a single statement with multiple parameter sets (i.e. an executemany). Most DBAPIs do not sum “rowcount” values across multiple parameter sets and will return -1 when accessed.

SQLAlchemy’s “Insert Many Values” Behavior for INSERT statements feature does support a correct population of CursorResult.rowcount when the Connection.execution_options.preserve_rowcount execution option is set to True.

Statements that use RETURNING may not support rowcount, returning a -1 value instead.

Getting Affected Row Count from UPDATE, DELETE - in the SQLAlchemy Unified Tutorial

Connection.execution_options.preserve_rowcount

inherited from the Result.scalar() method of Result

Fetch the first column of the first row, and close the result set.

Returns None if there are no rows to fetch.

No validation is performed to test if additional rows remain.

After calling this method, the object is fully closed, e.g. the CursorResult.close() method will have been called.

a Python scalar value, or None if no rows remain.

inherited from the Result.scalar_one() method of Result

Return exactly one scalar result or raise an exception.

This is equivalent to calling Result.scalars() and then ScalarResult.one().

inherited from the Result.scalar_one_or_none() method of Result

Return exactly one scalar result or None.

This is equivalent to calling Result.scalars() and then ScalarResult.one_or_none().

ScalarResult.one_or_none()

inherited from the Result.scalars() method of Result

Return a ScalarResult filtering object which will return single elements rather than Row objects.

When results are fetched from the ScalarResult filtering object, the single column-row that would be returned by the Result is instead returned as the column’s value.

Added in version 1.4.

index¶ – integer or row key indicating the column to be fetched from each row, defaults to 0 indicating the first column.

a new ScalarResult filtering object referring to this Result object.

Return a new CursorResult that “horizontally splices” together the rows of this CursorResult with that of another CursorResult.

This method is for the benefit of the SQLAlchemy ORM and is not intended for general use.

“horizontally splices” means that for each row in the first and second result sets, a new row that concatenates the two rows together is produced, which then becomes the new row. The incoming CursorResult must have the identical number of rows. It is typically expected that the two result sets come from the same sort order as well, as the result rows are spliced together based on their position in the result.

The expected use case here is so that multiple INSERT..RETURNING statements (which definitely need to be sorted) against different tables can produce a single result that looks like a JOIN of those two tables.

Added in version 2.0.

CursorResult.splice_vertically()

Return a new CursorResult that “vertically splices”, i.e. “extends”, the rows of this CursorResult with that of another CursorResult.

This method is for the benefit of the SQLAlchemy ORM and is not intended for general use.

“vertically splices” means the rows of the given result are appended to the rows of this cursor result. The incoming CursorResult must have rows that represent the identical list of columns in the identical order as they are in this CursorResult.

Added in version 2.0.

CursorResult.splice_horizontally()

Return supports_sane_multi_rowcount from the dialect.

See CursorResult.rowcount for background.

Return supports_sane_rowcount from the dialect.

See CursorResult.rowcount for background.

Apply a “typed tuple” typing filter to returned rows.

The Result.t attribute is a synonym for calling the Result.tuples() method.

Added in version 2.0.

inherited from the Result.tuples() method of Result

Apply a “typed tuple” typing filter to returned rows.

This method returns the same Result object at runtime, however annotates as returning a TupleResult object that will indicate to PEP 484 typing tools that plain typed Tuple instances are returned rather than rows. This allows tuple unpacking and __getitem__ access of Row objects to by typed, for those cases where the statement invoked itself included typing information.

Added in version 2.0.

the TupleResult type at typing time.

Result.t - shorter synonym

inherited from the Result.unique() method of Result

Apply unique filtering to the objects returned by this Result.

When this filter is applied with no arguments, the rows or objects returned will filtered such that each row is returned uniquely. The algorithm used to determine this uniqueness is by default the Python hashing identity of the whole tuple. In some cases a specialized per-entity hashing scheme may be used, such as when using the ORM, a scheme is applied which works against the primary key identity of returned objects.

The unique filter is applied after all other filters, which means if the columns returned have been refined using a method such as the Result.columns() or Result.scalars() method, the uniquing is applied to only the column or columns returned. This occurs regardless of the order in which these methods have been called upon the Result object.

The unique filter also changes the calculus used for methods like Result.fetchmany() and Result.partitions(). When using Result.unique(), these methods will continue to yield the number of rows or objects requested, after uniquing has been applied. However, this necessarily impacts the buffering behavior of the underlying cursor or datasource, such that multiple underlying calls to cursor.fetchmany() may be necessary in order to accumulate enough objects in order to provide a unique collection of the requested size.

strategy¶ – a callable that will be applied to rows or objects being iterated, which should return an object that represents the unique value of the row. A Python set() is used to store these identities. If not passed, a default uniqueness strategy is used which may have been assembled by the source of this Result object.

Configure the row-fetching strategy to fetch num rows at a time.

This impacts the underlying behavior of the result when iterating over the result object, or otherwise making use of methods such as Result.fetchone() that return one row at a time. Data from the underlying cursor or other data source will be buffered up to this many rows in memory, and the buffered collection will then be yielded out one row at a time or as many rows are requested. Each time the buffer clears, it will be refreshed to this many rows or as many rows remain if fewer remain.

The Result.yield_per() method is generally used in conjunction with the Connection.execution_options.stream_results execution option, which will allow the database dialect in use to make use of a server side cursor, if the DBAPI supports a specific “server side cursor” mode separate from its default mode of operation.

Consider using the Connection.execution_options.yield_per execution option, which will simultaneously set Connection.execution_options.stream_results to ensure the use of server side cursors, as well as automatically invoke the Result.yield_per() method to establish a fixed row buffer size at once.

The Connection.execution_options.yield_per execution option is available for ORM operations, with Session-oriented use described at Fetching Large Result Sets with Yield Per. The Core-only version which works with Connection is new as of SQLAlchemy 1.4.40.

Added in version 1.4.

num¶ – number of rows to fetch each time the buffer is refilled. If set to a value below 1, fetches all rows for the next buffer.

Using Server Side Cursors (a.k.a. stream results) - describes Core behavior for Result.yield_per()

Fetching Large Result Sets with Yield Per - in the ORM Querying Guide

inherits from sqlalchemy.engine.ResultInternal

A wrapper for a Result that returns objects other than Row objects, such as dictionaries or scalar objects.

FilterResult is the common base for additional result APIs including MappingResult, ScalarResult and AsyncResult.

Close this FilterResult.

Configure the row-fetching strategy to fetch num rows at a time.

Close this FilterResult.

Added in version 1.4.43.

Return True if the underlying Result reports closed

Added in version 1.4.43.

Configure the row-fetching strategy to fetch num rows at a time.

The FilterResult.yield_per() method is a pass through to the Result.yield_per() method. See that method’s documentation for usage notes.

Added in version 1.4.40: - added FilterResult.yield_per() so that the method is available on all result set implementations

Using Server Side Cursors (a.k.a. stream results) - describes Core behavior for Result.yield_per()

Fetching Large Result Sets with Yield Per - in the ORM Querying Guide

inherits from typing.Generic

Represents a Result object in a “frozen” state suitable for caching.

The FrozenResult object is returned from the Result.freeze() method of any Result object.

A new iterable Result object is generated from a fixed set of data each time the FrozenResult is invoked as a callable:

Added in version 1.4.

Re-Executing Statements - example usage within the ORM to implement a result-set cache.

merge_frozen_result() - ORM function to merge a frozen result back into a Session.

inherits from sqlalchemy.engine.Result

A Result that gets data from a Python iterator of Row objects or similar row-like data.

Added in version 1.4.

Return True if this IteratorResult has been closed

Added in version 1.4.43.

inherits from sqlalchemy.engine.IteratorResult

A Result that is merged from any number of Result objects.

Returned by the Result.merge() method.

Added in version 1.4.

inherits from sqlalchemy.engine._WithKeys, sqlalchemy.engine.ResultInternal

Represent a set of database results.

Added in version 1.4: The Result object provides a completely updated usage model and calling facade for SQLAlchemy Core and SQLAlchemy ORM. In Core, it forms the basis of the CursorResult object which replaces the previous ResultProxy interface. When using the ORM, a higher level object called ChunkedIteratorResult is normally used.

In SQLAlchemy 1.4 and above, this object is used for ORM results returned by Session.execute(), which can yield instances of ORM mapped objects either individually or within tuple-like rows. Note that the Result object does not deduplicate instances or rows automatically as is the case with the legacy Query object. For in-Python de-duplication of instances or rows, use the Result.unique() modifier method.

Fetching Rows - in the SQLAlchemy Unified Tutorial

Return all rows in a sequence.

Establish the columns that should be returned in each row.

A synonym for the Result.all() method.

Fetch the first row or None if no row is present.

Return a callable object that will produce copies of this Result when invoked.

Return an iterable view which yields the string keys that would be represented by each Row.

Apply a mappings filter to returned rows, returning an instance of MappingResult.

Merge this Result with other compatible result objects.

Return exactly one row or raise an exception.

Return at most one result or raise an exception.

Iterate through sub-lists of rows of the size given.

Fetch the first column of the first row, and close the result set.

Return exactly one scalar result or raise an exception.

Return exactly one scalar result or None.

Return a ScalarResult filtering object which will return single elements rather than Row objects.

Apply a “typed tuple” typing filter to returned rows.

Apply unique filtering to the objects returned by this Result.

Configure the row-fetching strategy to fetch num rows at a time.

Return all rows in a sequence.

Closes the result set after invocation. Subsequent invocations will return an empty sequence.

Added in version 1.4.

a sequence of Row objects.

Using Server Side Cursors (a.k.a. stream results) - How to stream a large result set without loading it completely in python.

The behavior of this method is implementation specific, and is not implemented by default. The method should generally end the resources in use by the result object and also cause any subsequent iteration or row fetching to raise ResourceClosedError.

Added in version 1.4.27: - .close() was previously not generally available for all Result classes, instead only being available on the CursorResult returned for Core statement executions. As most other result objects, namely the ones used by the ORM, are proxying a CursorResult in any case, this allows the underlying cursor result to be closed from the outside facade for the case when the ORM query is using the yield_per execution option where it does not immediately exhaust and autoclose the database cursor.

return True if this Result reports .closed

Added in version 1.4.43.

Establish the columns that should be returned in each row.

This method may be used to limit the columns returned as well as to reorder them. The given list of expressions are normally a series of integers or string key names. They may also be appropriate ColumnElement objects which correspond to a given statement construct.

Changed in version 2.0: Due to a bug in 1.4, the Result.columns() method had an incorrect behavior where calling upon the method with just one index would cause the Result object to yield scalar values rather than Row objects. In version 2.0, this behavior has been corrected such that calling upon Result.columns() with a single index will produce a Result object that continues to yield Row objects, which include only a single column.

Example of using the column objects from the statement itself:

Added in version 1.4.

*col_expressions¶ – indicates columns to be returned. Elements may be integer row indexes, string column names, or appropriate ColumnElement objects corresponding to a select construct.

this Result object with the modifications given.

A synonym for the Result.all() method.

When all rows are exhausted, returns an empty sequence.

This method is provided for backwards compatibility with SQLAlchemy 1.x.x.

To fetch rows in groups, use the Result.partitions() method.

a sequence of Row objects.

When all rows are exhausted, returns None.

This method is provided for backwards compatibility with SQLAlchemy 1.x.x.

To fetch the first row of a result only, use the Result.first() method. To iterate through all rows, iterate the Result object directly.

a Row object if no filters are applied, or None if no rows remain.

Fetch the first row or None if no row is present.

Closes the result set and discards remaining rows.

This method returns one row, e.g. tuple, by default. To return exactly one single scalar value, that is, the first column of the first row, use the Result.scalar() method, or combine Result.scalars() and Result.first().

Additionally, in contrast to the behavior of the legacy ORM Query.first() method, no limit is applied to the SQL query which was invoked to produce this Result; for a DBAPI driver that buffers results in memory before yielding rows, all rows will be sent to the Python process and all but the first row will be discarded.

ORM Query Unified with Core Select

a Row object, or None if no rows remain.

Return a callable object that will produce copies of this Result when invoked.

The callable object returned is an instance of FrozenResult.

This is used for result set caching. The method must be called on the result when it has been unconsumed, and calling the method will consume the result fully. When the FrozenResult is retrieved from a cache, it can be called any number of times where it will produce a new Result object each time against its stored set of rows.

Re-Executing Statements - example usage within the ORM to implement a result-set cache.

inherited from the sqlalchemy.engine._WithKeys.keys method of sqlalchemy.engine._WithKeys

Return an iterable view which yields the string keys that would be represented by each Row.

The keys can represent the labels of the columns returned by a core statement or the names of the orm classes returned by an orm execution.

The view also can be tested for key containment using the Python in operator, which will test both for the string keys represented in the view, as well as for alternate keys such as column objects.

Changed in version 1.4: a key view object is returned rather than a plain list.

Apply a mappings filter to returned rows, returning an instance of MappingResult.

When this filter is applied, fetching rows will return RowMapping objects instead of Row objects.

Added in version 1.4.

a new MappingResult filtering object referring to this Result object.

Merge this Result with other compatible result objects.

The object returned is an instance of MergedResult, which will be composed of iterators from the given result objects.

The new result will use the metadata from this result object. The subsequent result objects must be against an identical set of result / cursor metadata, otherwise the behavior is undefined.

Return exactly one row or raise an exception.

Raises NoResultFound if the result returns no rows, or MultipleResultsFound if multiple rows would be returned.

This method returns one row, e.g. tuple, by default. To return exactly one single scalar value, that is, the first column of the first row, use the Result.scalar_one() method, or combine Result.scalars() and Result.one().

Added in version 1.4.

MultipleResultsFound, NoResultFound

Return at most one result or raise an exception.

Returns None if the result has no rows. Raises MultipleResultsFound if multiple rows are returned.

Added in version 1.4.

The first Row or None if no row is available.

Iterate through sub-lists of rows of the size given.

Each list will be of the size given, excluding the last list to be yielded, which may have a small number of rows. No empty lists will be yielded.

The result object is automatically closed when the iterator is fully consumed.

Note that the backend driver will usually buffer the entire result ahead of time unless the Connection.execution_options.stream_results execution option is used indicating that the driver should not pre-buffer results, if possible. Not all drivers support this option and the option is silently ignored for those who do not.

When using the ORM, the Result.partitions() method is typically more effective from a memory perspective when it is combined with use of the yield_per execution option, which instructs both the DBAPI driver to use server side cursors, if available, as well as instructs the ORM loading internals to only build a certain amount of ORM objects from a result at a time before yielding them out.

Added in version 1.4.

size¶ – indicate the maximum number of rows to be present in each list yielded. If None, makes use of the value set by the Result.yield_per(), method, if it were called, or the Connection.execution_options.yield_per execution option, which is equivalent in this regard. If yield_per weren’t set, it makes use of the Result.fetchmany() default, which may be backend specific and not well defined.

Using Server Side Cursors (a.k.a. stream results)

Fetching Large Result Sets with Yield Per - in the ORM Querying Guide

Fetch the first column of the first row, and close the result set.

Returns None if there are no rows to fetch.

No validation is performed to test if additional rows remain.

After calling this method, the object is fully closed, e.g. the CursorResult.close() method will have been called.

a Python scalar value, or None if no rows remain.

Return exactly one scalar result or raise an exception.

This is equivalent to calling Result.scalars() and then ScalarResult.one().

Return exactly one scalar result or None.

This is equivalent to calling Result.scalars() and then ScalarResult.one_or_none().

ScalarResult.one_or_none()

Return a ScalarResult filtering object which will return single elements rather than Row objects.

When results are fetched from the ScalarResult filtering object, the single column-row that would be returned by the Result is instead returned as the column’s value.

Added in version 1.4.

index¶ – integer or row key indicating the column to be fetched from each row, defaults to 0 indicating the first column.

a new ScalarResult filtering object referring to this Result object.

Apply a “typed tuple” typing filter to returned rows.

The Result.t attribute is a synonym for calling the Result.tuples() method.

Added in version 2.0.

Apply a “typed tuple” typing filter to returned rows.

This method returns the same Result object at runtime, however annotates as returning a TupleResult object that will indicate to PEP 484 typing tools that plain typed Tuple instances are returned rather than rows. This allows tuple unpacking and __getitem__ access of Row objects to by typed, for those cases where the statement invoked itself included typing information.

Added in version 2.0.

the TupleResult type at typing time.

Result.t - shorter synonym

Apply unique filtering to the objects returned by this Result.

When this filter is applied with no arguments, the rows or objects returned will filtered such that each row is returned uniquely. The algorithm used to determine this uniqueness is by default the Python hashing identity of the whole tuple. In some cases a specialized per-entity hashing scheme may be used, such as when using the ORM, a scheme is applied which works against the primary key identity of returned objects.

The unique filter is applied after all other filters, which means if the columns returned have been refined using a method such as the Result.columns() or Result.scalars() method, the uniquing is applied to only the column or columns returned. This occurs regardless of the order in which these methods have been called upon the Result object.

The unique filter also changes the calculus used for methods like Result.fetchmany() and Result.partitions(). When using Result.unique(), these methods will continue to yield the number of rows or objects requested, after uniquing has been applied. However, this necessarily impacts the buffering behavior of the underlying cursor or datasource, such that multiple underlying calls to cursor.fetchmany() may be necessary in order to accumulate enough objects in order to provide a unique collection of the requested size.

strategy¶ – a callable that will be applied to rows or objects being iterated, which should return an object that represents the unique value of the row. A Python set() is used to store these identities. If not passed, a default uniqueness strategy is used which may have been assembled by the source of this Result object.

Configure the row-fetching strategy to fetch num rows at a time.

This impacts the underlying behavior of the result when iterating over the result object, or otherwise making use of methods such as Result.fetchone() that return one row at a time. Data from the underlying cursor or other data source will be buffered up to this many rows in memory, and the buffered collection will then be yielded out one row at a time or as many rows are requested. Each time the buffer clears, it will be refreshed to this many rows or as many rows remain if fewer remain.

The Result.yield_per() method is generally used in conjunction with the Connection.execution_options.stream_results execution option, which will allow the database dialect in use to make use of a server side cursor, if the DBAPI supports a specific “server side cursor” mode separate from its default mode of operation.

Consider using the Connection.execution_options.yield_per execution option, which will simultaneously set Connection.execution_options.stream_results to ensure the use of server side cursors, as well as automatically invoke the Result.yield_per() method to establish a fixed row buffer size at once.

The Connection.execution_options.yield_per execution option is available for ORM operations, with Session-oriented use described at Fetching Large Result Sets with Yield Per. The Core-only version which works with Connection is new as of SQLAlchemy 1.4.40.

Added in version 1.4.

num¶ – number of rows to fetch each time the buffer is refilled. If set to a value below 1, fetches all rows for the next buffer.

Using Server Side Cursors (a.k.a. stream results) - describes Core behavior for Result.yield_per()

Fetching Large Result Sets with Yield Per - in the ORM Querying Guide

inherits from sqlalchemy.engine.FilterResult

A wrapper for a Result that returns scalar values rather than Row values.

The ScalarResult object is acquired by calling the Result.scalars() method.

A special limitation of ScalarResult is that it has no fetchone() method; since the semantics of fetchone() are that the None value indicates no more results, this is not compatible with ScalarResult since there is no way to distinguish between None as a row value versus None as an indicator. Use next(result) to receive values individually.

Return all scalar values in a sequence.

Close this FilterResult.

A synonym for the ScalarResult.all() method.

Fetch the first object or None if no object is present.

Return exactly one object or raise an exception.

Return at most one object or raise an exception.

Iterate through sub-lists of elements of the size given.

Apply unique filtering to the objects returned by this ScalarResult.

Configure the row-fetching strategy to fetch num rows at a time.

Return all scalar values in a sequence.

Equivalent to Result.all() except that scalar values, rather than Row objects, are returned.

inherited from the FilterResult.close() method of FilterResult

Close this FilterResult.

Added in version 1.4.43.

Return True if the underlying Result reports closed

Added in version 1.4.43.

A synonym for the ScalarResult.all() method.

Equivalent to Result.fetchmany() except that scalar values, rather than Row objects, are returned.

Fetch the first object or None if no object is present.

Equivalent to Result.first() except that scalar values, rather than Row objects, are returned.

Return exactly one object or raise an exception.

Equivalent to Result.one() except that scalar values, rather than Row objects, are returned.

Return at most one object or raise an exception.

Equivalent to Result.one_or_none() except that scalar values, rather than Row objects, are returned.

Iterate through sub-lists of elements of the size given.

Equivalent to Result.partitions() except that scalar values, rather than Row objects, are returned.

Apply unique filtering to the objects returned by this ScalarResult.

See Result.unique() for usage details.

inherited from the FilterResult.yield_per() method of FilterResult

Configure the row-fetching strategy to fetch num rows at a time.

The FilterResult.yield_per() method is a pass through to the Result.yield_per() method. See that method’s documentation for usage notes.

Added in version 1.4.40: - added FilterResult.yield_per() so that the method is available on all result set implementations

Using Server Side Cursors (a.k.a. stream results) - describes Core behavior for Result.yield_per()

Fetching Large Result Sets with Yield Per - in the ORM Querying Guide

inherits from sqlalchemy.engine._WithKeys, sqlalchemy.engine.FilterResult

A wrapper for a Result that returns dictionary values rather than Row values.

The MappingResult object is acquired by calling the Result.mappings() method.

Return all scalar values in a sequence.

Close this FilterResult.

Establish the columns that should be returned in each row.

A synonym for the MappingResult.all() method.

Fetch the first object or None if no object is present.

Return an iterable view which yields the string keys that would be represented by each Row.

Return exactly one object or raise an exception.

Return at most one object or raise an exception.

Iterate through sub-lists of elements of the size given.

Apply unique filtering to the objects returned by this MappingResult.

Configure the row-fetching strategy to fetch num rows at a time.

Return all scalar values in a sequence.

Equivalent to Result.all() except that RowMapping values, rather than Row objects, are returned.

inherited from the FilterResult.close() method of FilterResult

Close this FilterResult.

Added in version 1.4.43.

Return True if the underlying Result reports closed

Added in version 1.4.43.

Establish the columns that should be returned in each row.

A synonym for the MappingResult.all() method.

Equivalent to Result.fetchmany() except that RowMapping values, rather than Row objects, are returned.

Equivalent to Result.fetchone() except that RowMapping values, rather than Row objects, are returned.

Fetch the first object or None if no object is present.

Equivalent to Result.first() except that RowMapping values, rather than Row objects, are returned.

inherited from the sqlalchemy.engine._WithKeys.keys method of sqlalchemy.engine._WithKeys

Return an iterable view which yields the string keys that would be represented by each Row.

The keys can represent the labels of the columns returned by a core statement or the names of the orm classes returned by an orm execution.

The view also can be tested for key containment using the Python in operator, which will test both for the string keys represented in the view, as well as for alternate keys such as column objects.

Changed in version 1.4: a key view object is returned rather than a plain list.

Return exactly one object or raise an exception.

Equivalent to Result.one() except that RowMapping values, rather than Row objects, are returned.

Return at most one object or raise an exception.

Equivalent to Result.one_or_none() except that RowMapping values, rather than Row objects, are returned.

Iterate through sub-lists of elements of the size given.

Equivalent to Result.partitions() except that RowMapping values, rather than Row objects, are returned.

Apply unique filtering to the objects returned by this MappingResult.

See Result.unique() for usage details.

inherited from the FilterResult.yield_per() method of FilterResult

Configure the row-fetching strategy to fetch num rows at a time.

The FilterResult.yield_per() method is a pass through to the Result.yield_per() method. See that method’s documentation for usage notes.

Added in version 1.4.40: - added FilterResult.yield_per() so that the method is available on all result set implementations

Using Server Side Cursors (a.k.a. stream results) - describes Core behavior for Result.yield_per()

Fetching Large Result Sets with Yield Per - in the ORM Querying Guide

inherits from sqlalchemy.engine._py_row.BaseRow, collections.abc.Sequence, typing.Generic

Represent a single result row.

The Row object represents a row of a database result. It is typically associated in the 1.x series of SQLAlchemy with the CursorResult object, however is also used by the ORM for tuple-like results as of SQLAlchemy 1.4.

The Row object seeks to act as much like a Python named tuple as possible. For mapping (i.e. dictionary) behavior on a row, such as testing for containment of keys, refer to the Row._mapping attribute.

Using SELECT Statements - includes examples of selecting rows from SELECT statements.

Changed in version 1.4: Renamed RowProxy to Row. Row is no longer a “proxy” object in that it contains the final form of data within it, and now acts mostly like a named tuple. Mapping-like functionality is moved to the Row._mapping attribute. See RowProxy is no longer a “proxy”; is now called Row and behaves like an enhanced named tuple for background on this change.

Return a new dict which maps field names to their corresponding values.

Return a ‘tuple’ form of this Row.

Return a ‘tuple’ form of this Row.

Return a new dict which maps field names to their corresponding values.

This method is analogous to the Python named tuple ._asdict() method, and works by applying the dict() constructor to the Row._mapping attribute.

Added in version 1.4.

Return a tuple of string keys as represented by this Row.

The keys can represent the labels of the columns returned by a core statement or the names of the orm classes returned by an orm execution.

This attribute is analogous to the Python named tuple ._fields attribute.

Added in version 1.4.

Return a RowMapping for this Row.

This object provides a consistent Python mapping (i.e. dictionary) interface for the data contained within the row. The Row by itself behaves like a named tuple.

Added in version 1.4.

A synonym for Row._tuple().

Added in version 2.0.19: - The Row._t attribute supersedes the previous Row.t attribute, which is now underscored to avoid name conflicts with column names in the same way as other named-tuple methods on Row.

Return a ‘tuple’ form of this Row.

At runtime, this method returns “self”; the Row object is already a named tuple. However, at the typing level, if this Row is typed, the “tuple” return type will be a PEP 484 Tuple datatype that contains typing information about individual elements, supporting typed unpacking and attribute access.

Added in version 2.0.19: - The Row._tuple() method supersedes the previous Row.tuple() method, which is now underscored to avoid name conflicts with column names in the same way as other named-tuple methods on Row.

Row._t - shorthand attribute notation

Raises ValueError if the value is not present.

Supporting start and stop arguments is optional, but recommended.

A synonym for Row._tuple().

Deprecated since version 2.0.19: The Row.t attribute is deprecated in favor of Row._t; all Row methods and library-level attributes are intended to be underscored to avoid name conflicts. Please use Row._t.

Added in version 2.0.

Return a ‘tuple’ form of this Row.

Deprecated since version 2.0.19: The Row.tuple() method is deprecated in favor of Row._tuple(); all Row methods and library-level attributes are intended to be underscored to avoid name conflicts. Please use Row._tuple().

Added in version 2.0.

inherits from sqlalchemy.engine._py_row.BaseRow, collections.abc.Mapping, typing.Generic

A Mapping that maps column names and objects to Row values.

The RowMapping is available from a Row via the Row._mapping attribute, as well as from the iterable interface provided by the MappingResult object returned by the Result.mappings() method.

RowMapping supplies Python mapping (i.e. dictionary) access to the contents of the row. This includes support for testing of containment of specific keys (string column names or objects), as well as iteration of keys, values, and items:

Added in version 1.4: The RowMapping object replaces the mapping-like access previously provided by a database result row, which now seeks to behave mostly like a named tuple.

Return a view of key/value tuples for the elements in the underlying Row.

Return a view of ‘keys’ for string column names represented by the underlying Row.

Return a view of values for the values represented in the underlying Row.

Return a view of key/value tuples for the elements in the underlying Row.

Return a view of ‘keys’ for string column names represented by the underlying Row.

Return a view of values for the values represented in the underlying Row.

inherits from sqlalchemy.engine.FilterResult, sqlalchemy.util.langhelpers.TypingOnly

A Result that’s typed as returning plain Python tuples instead of rows.

Since Row acts like a tuple in every way already, this class is a typing only class, regular Result is still used at runtime.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
engine = create_engine("mysql+mysqldb://scott:tiger@localhost/test")
```

Example 2 (sql):
```sql
from sqlalchemy import text

with engine.connect() as connection:
    result = connection.execute(text("select username from users"))
    for row in result:
        print("username:", row.username)
```

Example 3 (json):
```json
with engine.connect() as connection:
    connection.execute(some_table.insert(), {"x": 7, "y": "this is some data"})
    connection.execute(
        some_other_table.insert(), {"q": 8, "p": "this is some more data"}
    )

    connection.commit()  # commit the transaction
```

Example 4 (typescript):
```typescript
with engine.connect() as connection:
    connection.execute(text("<some statement>"))
    connection.commit()  # commits "some statement"

    # new transaction starts
    connection.execute(text("<some other statement>"))
    connection.rollback()  # rolls back "some other statement"

    # new transaction starts
    connection.execute(text("<a third statement>"))
    connection.commit()  # commits "a third statement"
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/tutorial/data_update.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Unified Tutorial
    - Project Versions
- Using UPDATE and DELETE Statements¶
- The update() SQL Expression Construct¶
  - Correlated Updates¶
  - UPDATE..FROM¶
  - Parameter Ordered Updates¶
- The delete() SQL Expression Construct¶

Home | Download this Documentation

Home | Download this Documentation

SQLAlchemy 1.4 / 2.0 Tutorial

This page is part of the SQLAlchemy Unified Tutorial.

Previous: Using SELECT Statements | Next: Data Manipulation with the ORM

So far we’ve covered Insert, so that we can get some data into our database, and then spent a lot of time on Select which handles the broad range of usage patterns used for retrieving data from the database. In this section we will cover the Update and Delete constructs, which are used to modify existing rows as well as delete existing rows. This section will cover these constructs from a Core-centric perspective.

ORM Readers - As was the case mentioned at Using INSERT Statements, the Update and Delete operations when used with the ORM are usually invoked internally from the Session object as part of the unit of work process.

However, unlike Insert, the Update and Delete constructs can also be used directly with the ORM, using a pattern known as “ORM-enabled update and delete”; for this reason, familiarity with these constructs is useful for ORM use. Both styles of use are discussed in the sections Updating ORM Objects using the Unit of Work pattern and Deleting ORM Objects using the Unit of Work pattern.

The update() function generates a new instance of Update which represents an UPDATE statement in SQL, that will update existing data in a table.

Like the insert() construct, there is a “traditional” form of update(), which emits UPDATE against a single table at a time and does not return any rows. However some backends support an UPDATE statement that may modify multiple tables at once, and the UPDATE statement also supports RETURNING such that columns contained in matched rows may be returned in the result set.

A basic UPDATE looks like:

The Update.values() method controls the contents of the SET elements of the UPDATE statement. This is the same method shared by the Insert construct. Parameters can normally be passed using the column names as keyword arguments.

UPDATE supports all the major SQL forms of UPDATE, including updates against expressions, where we can make use of Column expressions:

To support UPDATE in an “executemany” context, where many parameter sets will be invoked against the same statement, the bindparam() construct may be used to set up bound parameters; these replace the places that literal values would normally go:

Other techniques which may be applied to UPDATE include:

An UPDATE statement can make use of rows in other tables by using a correlated subquery. A subquery may be used anywhere a column expression might be placed:

Some databases such as PostgreSQL, MSSQL and MySQL support a syntax UPDATE...FROM where additional tables may be stated directly in a special FROM clause. This syntax will be generated implicitly when additional tables are located in the WHERE clause of the statement:

There is also a MySQL specific syntax that can UPDATE multiple tables. This requires we refer to Table objects in the VALUES clause in order to refer to additional tables:

UPDATE...FROM can also be combined with the Values construct on backends such as PostgreSQL, to create a single UPDATE statement that updates multiple rows at once against the named form of VALUES:

Another MySQL-only behavior is that the order of parameters in the SET clause of an UPDATE actually impacts the evaluation of each expression. For this use case, the Update.ordered_values() method accepts a sequence of tuples so that this order may be controlled [2]:

While Python dictionaries are guaranteed to be insert ordered as of Python 3.7, the Update.ordered_values() method still provides an additional measure of clarity of intent when it is essential that the SET clause of a MySQL UPDATE statement proceed in a specific way.

The delete() function generates a new instance of Delete which represents a DELETE statement in SQL, that will delete rows from a table.

The delete() statement from an API perspective is very similar to that of the update() construct, traditionally returning no rows but allowing for a RETURNING variant on some database backends.

Like Update, Delete supports the use of correlated subqueries in the WHERE clause as well as backend-specific multiple table syntaxes, such as DELETE FROM..USING on MySQL:

Both Update and Delete support the ability to return the number of rows matched after the statement proceeds, for statements that are invoked using Core Connection, i.e. Connection.execute(). Per the caveats mentioned below, this value is available from the CursorResult.rowcount attribute:

The CursorResult class is a subclass of Result which contains additional attributes that are specific to the DBAPI cursor object. An instance of this subclass is returned when a statement is invoked via the Connection.execute() method. When using the ORM, the Session.execute() method will normally not return this type of object, unless the given query uses only Core Table objects directly.

Facts about CursorResult.rowcount:

The value returned is the number of rows matched by the WHERE clause of the statement. It does not matter if the row were actually modified or not.

CursorResult.rowcount is not necessarily available for an UPDATE or DELETE statement that uses RETURNING, or for one that uses an executemany execution. The availability depends on the DBAPI module in use.

In any case where the DBAPI does not determine the rowcount for some type of statement, the returned value will be -1.

SQLAlchemy pre-memoizes the DBAPIs cursor.rowcount value before the cursor is closed, as some DBAPIs don’t support accessing this attribute after the fact. In order to pre-memoize cursor.rowcount for a statement that is not UPDATE or DELETE, such as INSERT or SELECT, the Connection.execution_options.preserve_rowcount execution option may be used.

Some drivers, particularly third party dialects for non-relational databases, may not support CursorResult.rowcount at all. The CursorResult.supports_sane_rowcount cursor attribute will indicate this.

“rowcount” is used by the ORM unit of work process to validate that an UPDATE or DELETE statement matched the expected number of rows, and is also essential for the ORM versioning feature documented at Configuring a Version Counter.

Like the Insert construct, Update and Delete also support the RETURNING clause which is added by using the Update.returning() and Delete.returning() methods. When these methods are used on a backend that supports RETURNING, selected columns from all rows that match the WHERE criteria of the statement will be returned in the Result object as rows that can be iterated:

API documentation for UPDATE / DELETE:

ORM-enabled UPDATE and DELETE:

ORM-Enabled INSERT, UPDATE, and DELETE statements - in the ORM Querying Guide

SQLAlchemy 1.4 / 2.0 Tutorial

Next Tutorial Section: Data Manipulation with the ORM

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (sql):
```sql
>>> from sqlalchemy import update
>>> stmt = (
...     update(user_table)
...     .where(user_table.c.name == "patrick")
...     .values(fullname="Patrick the Star")
... )
>>> print(stmt)
UPDATE user_account SET fullname=:fullname WHERE user_account.name = :name_1
```

Example 2 (sql):
```sql
>>> stmt = update(user_table).values(fullname="Username: " + user_table.c.name)
>>> print(stmt)
UPDATE user_account SET fullname=(:name_1 || user_account.name)
```

Example 3 (sql):
```sql
>>> from sqlalchemy import bindparam
>>> stmt = (
...     update(user_table)
...     .where(user_table.c.name == bindparam("oldname"))
...     .values(name=bindparam("newname"))
... )
>>> with engine.begin() as conn:
...     conn.execute(
...         stmt,
...         [
...             {"oldname": "jack", "newname": "ed"},
...             {"oldname": "wendy", "newname": "mary"},
...             {"oldname": "jim", "newname": "jake"},
...         ],
...     )
BEGIN (implicit)
UPDATE user_account SET name=? WHERE user_account.name = ?
[...] [('ed', 'jack'), ('mary', 'wendy'), ('jake', 'jim')]
<sqlalchemy.engine.cursor.CursorResult object at 0x...>
COMMIT
```

Example 4 (sql):
```sql
>>> scalar_subq = (
...     select(address_table.c.email_address)
...     .where(address_table.c.user_id == user_table.c.id)
...     .order_by(address_table.c.id)
...     .limit(1)
...     .scalar_subquery()
... )
>>> update_stmt = update(user_table).values(fullname=scalar_subq)
>>> print(update_stmt)
UPDATE user_account SET fullname=(SELECT address.email_address
FROM address
WHERE address.user_id = user_account.id ORDER BY address.id
LIMIT :param_1)
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/faq/metadata_schema.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - Frequently Asked Questions
    - Project Versions
- MetaData / Schema¶
- My program is hanging when I say table.drop() / metadata.drop_all()¶
- Does SQLAlchemy support ALTER TABLE, CREATE VIEW, CREATE TRIGGER, Schema Upgrade Functionality?¶
- How can I sort Table objects in order of their dependency?¶
- How can I get the CREATE TABLE/ DROP TABLE output as a string?¶
- How can I subclass Table/Column to provide certain behaviors/configurations?¶

Home | Download this Documentation

Home | Download this Documentation

My program is hanging when I say table.drop() / metadata.drop_all()

Does SQLAlchemy support ALTER TABLE, CREATE VIEW, CREATE TRIGGER, Schema Upgrade Functionality?

How can I sort Table objects in order of their dependency?

How can I get the CREATE TABLE/ DROP TABLE output as a string?

How can I subclass Table/Column to provide certain behaviors/configurations?

This usually corresponds to two conditions: 1. using PostgreSQL, which is really strict about table locks, and 2. you have a connection still open which contains locks on the table and is distinct from the connection being used for the DROP statement. Heres the most minimal version of the pattern:

Above, a connection pool connection is still checked out; furthermore, the result object above also maintains a link to this connection. If “implicit execution” is used, the result will hold this connection opened until the result object is closed or all rows are exhausted.

The call to mytable.drop(engine) attempts to emit DROP TABLE on a second connection procured from the Engine which will lock.

The solution is to close out all connections before emitting DROP TABLE:

General ALTER support isn’t present in SQLAlchemy directly. For special DDL on an ad-hoc basis, the DDL and related constructs can be used. See Customizing DDL for a discussion on this subject.

A more comprehensive option is to use schema migration tools, such as Alembic or SQLAlchemy-Migrate; see Altering Database Objects through Migrations for discussion on this.

This is available via the MetaData.sorted_tables function:

Modern SQLAlchemy has clause constructs which represent DDL operations. These can be rendered to strings like any other SQL expression:

To get the string specific to a certain engine:

There’s also a special form of Engine available via create_mock_engine() that allows one to dump an entire metadata creation sequence as a string, using this recipe:

The Alembic tool also supports an “offline” SQL generation mode that renders database migrations as SQL scripts.

Table and Column are not good targets for direct subclassing. However, there are simple ways to get on-construction behaviors using creation functions, and behaviors related to the linkages between schema objects such as constraint conventions or naming conventions using attachment events. An example of many of these techniques can be seen at Naming Conventions.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (csharp):
```csharp
connection = engine.connect()
result = connection.execute(mytable.select())

mytable.drop(engine)
```

Example 2 (markdown):
```markdown
connection = engine.connect()
result = connection.execute(mytable.select())

# fully read result sets
result.fetchall()

# close connections
connection.close()

# now locks are removed
mytable.drop(engine)
```

Example 3 (markdown):
```markdown
metadata_obj = MetaData()
# ... add Table objects to metadata
ti = metadata_obj.sorted_tables
for t in ti:
    print(t)
```

Example 4 (python):
```python
from sqlalchemy.schema import CreateTable

print(CreateTable(mytable))
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/dataclasses.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Integration with dataclasses and attrs¶
- Declarative Dataclass Mapping¶
  - Class level feature configuration¶
  - Attribute Configuration¶
    - Column Defaults¶
    - Integration with Annotated¶

Home | Download this Documentation

Home | Download this Documentation

SQLAlchemy as of version 2.0 features “native dataclass” integration where an Annotated Declarative Table mapping may be turned into a Python dataclass by adding a single mixin or decorator to mapped classes.

Added in version 2.0: Integrated dataclass creation with ORM Declarative classes

There are also patterns available that allow existing dataclasses to be mapped, as well as to map classes instrumented by the attrs third party integration library.

SQLAlchemy Annotated Declarative Table mappings may be augmented with an additional mixin class or decorator directive, which will add an additional step to the Declarative process after the mapping is complete that will convert the mapped class in-place into a Python dataclass, before completing the mapping process which applies ORM-specific instrumentation to the class. The most prominent behavioral addition this provides is generation of an __init__() method with fine-grained control over positional and keyword arguments with or without defaults, as well as generation of methods like __repr__() and __eq__().

From a PEP 484 typing perspective, the class is recognized as having Dataclass-specific behaviors, most notably by taking advantage of PEP 681 “Dataclass Transforms”, which allows typing tools to consider the class as though it were explicitly decorated using the @dataclasses.dataclass decorator.

Support for PEP 681 in typing tools as of April 4, 2023 is limited and is currently known to be supported by Pyright as well as Mypy as of version 1.2. Note that Mypy 1.1.1 introduced PEP 681 support but did not correctly accommodate Python descriptors which will lead to errors when using SQLAlchemy’s ORM mapping scheme.

https://peps.python.org/pep-0681/#the-dataclass-transform-decorator - background on how libraries like SQLAlchemy enable PEP 681 support

Dataclass conversion may be added to any Declarative class either by adding the MappedAsDataclass mixin to a DeclarativeBase class hierarchy, or for decorator mapping by using the registry.mapped_as_dataclass() class decorator.

The MappedAsDataclass mixin may be applied either to the Declarative Base class or any superclass, as in the example below:

Or may be applied directly to classes that extend from the Declarative base:

When using the decorator form, the registry.mapped_as_dataclass() decorator is supported:

The same method is available in a standalone function form, which may have better compatibility with some versions of the mypy type checker:

Added in version 2.0.44: Added mapped_as_dataclass() after observing mypy compatibility issues with the method form of the same feature

Support for dataclasses features is partial. Currently supported are the init, repr, eq, order and unsafe_hash features, match_args and kw_only are supported on Python 3.10+. Currently not supported are the frozen and slots features.

When using the mixin class form with MappedAsDataclass, class configuration arguments are passed as class-level parameters:

When using the decorator form with registry.mapped_as_dataclass() or mapped_as_dataclass(), class configuration arguments are passed to the decorator directly:

For background on dataclass class options, see the dataclasses documentation at @dataclasses.dataclass.

SQLAlchemy native dataclasses differ from normal dataclasses in that attributes to be mapped are described using the Mapped generic annotation container in all cases. Mappings follow the same forms as those documented at Declarative Table with mapped_column(), and all features of mapped_column() and Mapped are supported.

Additionally, ORM attribute configuration constructs including mapped_column(), relationship() and composite() support per-attribute field options, including init, default, default_factory and repr. The names of these arguments is fixed as specified in PEP 681. Functionality is equivalent to dataclasses:

init, as in mapped_column.init, relationship.init, if False indicates the field should not be part of the __init__() method

default, as in mapped_column.default, relationship.default indicates a default value for the field as given as a keyword argument in the __init__() method.

default_factory, as in mapped_column.default_factory, relationship.default_factory, indicates a callable function that will be invoked to generate a new default value for a parameter if not passed explicitly to the __init__() method.

repr True by default, indicates the field should be part of the generated __repr__() method

Another key difference from dataclasses is that default values for attributes must be configured using the default parameter of the ORM construct, such as mapped_column(default=None). A syntax that resembles dataclass syntax which accepts simple Python values as defaults without using @dataclases.field() is not supported.

As an example using mapped_column(), the mapping below will produce an __init__() method that accepts only the fields name and fullname, where name is required and may be passed positionally, and fullname is optional. The id field, which we expect to be database-generated, is not part of the constructor at all:

In order to accommodate the name overlap of the default argument with the existing Column.default parameter of the Column construct, the mapped_column() construct disambiguates the two names by adding a new parameter mapped_column.insert_default, which will be populated directly into the Column.default parameter of Column, independently of what may be set on mapped_column.default, which is always used for the dataclasses configuration. For example, to configure a datetime column with a Column.default set to the func.utc_timestamp() SQL function, but where the parameter is optional in the constructor:

With the above mapping, an INSERT for a new User object where no parameter for created_at were passed proceeds as:

The approach introduced at Mapping Whole Column Declarations to Python Types illustrates how to use PEP 593 Annotated objects to package whole mapped_column() constructs for reuse. While Annotated objects can be combined with the use of dataclasses, dataclass-specific keyword arguments unfortunately cannot be used within the Annotated construct. This includes PEP 681-specific arguments init, default, repr, and default_factory, which must be present in a mapped_column() or similar construct inline with the class attribute.

Changed in version 2.0.14/2.0.22: the Annotated construct when used with an ORM construct like mapped_column() cannot accommodate dataclass field parameters such as init and repr - this use goes against the design of Python dataclasses and is not supported by PEP 681, and therefore is also rejected by the SQLAlchemy ORM at runtime. A deprecation warning is now emitted and the attribute will be ignored.

As an example, the init=False parameter below will be ignored and additionally emit a deprecation warning:

Instead, mapped_column() must be present on the right side as well with an explicit setting for mapped_column.init; the other arguments can remain within the Annotated construct:

Any mixins or base classes that are used in a MappedAsDataclass mapped class which include Mapped attributes must themselves be part of a MappedAsDataclass hierarchy, such as in the example below using a mixin:

Python type checkers which support PEP 681 will otherwise not consider attributes from non-dataclass mixins to be part of the dataclass.

Deprecated since version 2.0.8: Using mixins and abstract bases within MappedAsDataclass or registry.mapped_as_dataclass() hierarchies which are not themselves dataclasses is deprecated, as these fields are not supported by PEP 681 as belonging to the dataclass. A warning is emitted for this case which will later be an error.

When transforming <cls> to a dataclass, attribute(s) originate from superclass <cls> which is not a dataclass. - background on rationale

The Mapped annotation in combination with relationship() is used in the same way as described at Basic Relationship Patterns. When specifying a collection-based relationship() as an optional keyword argument, the relationship.default_factory parameter must be passed and it must refer to the collection class that’s to be used. Many-to-one and scalar object references may make use of relationship.default if the default value is to be None:

The above mapping will generate an empty list for Parent.children when a new Parent() object is constructed without passing children, and similarly a None value for Child.parent when a new Child() object is constructed without passing parent.

While the relationship.default_factory can be automatically derived from the given collection class of the relationship() itself, this would break compatibility with dataclasses, as the presence of relationship.default_factory or relationship.default is what determines if the parameter is to be required or optional when rendered into the __init__() method.

When using Declarative dataclasses, non-mapped fields may be used on the class as well, which will be part of the dataclass construction process but will not be mapped. Any field that does not use Mapped will be ignored by the mapping process. In the example below, the fields ctrl_one and ctrl_two will be part of the instance-level state of the object, but will not be persisted by the ORM:

Instance of Data above can be created as:

A more real world example might be to make use of the Dataclasses InitVar feature in conjunction with the __post_init__() feature to receive init-only fields that can be used to compose persisted data. In the example below, the User class is declared using id, name and password_hash as mapped features, but makes use of init-only password and repeat_password fields to represent the user creation process (note: to run this example, replace the function your_hash_function_here() with a third party hash function, such as bcrypt or argon2-cffi):

The above object is created with parameters password and repeat_password, which are consumed up front so that the password_hash variable may be generated:

Changed in version 2.0.0rc1: When using registry.mapped_as_dataclass() or MappedAsDataclass, fields that do not include the Mapped annotation may be included, which will be treated as part of the resulting dataclass but not be mapped, without the need to also indicate the __allow_unmapped__ class attribute. Previous 2.0 beta releases would require this attribute to be explicitly present, even though the purpose of this attribute was only to allow legacy ORM typed mappings to continue to function.

The dataclass layer of Pydantic is not fully compatible with SQLAlchemy’s class instrumentation without additional internal changes, and many features such as related collections may not work correctly.

For Pydantic compatibility, please consider the SQLModel ORM which is built with Pydantic on top of SQLAlchemy ORM, which includes special implementation details which explicitly resolve these incompatibilities.

SQLAlchemy’s MappedAsDataclass class and registry.mapped_as_dataclass() method call directly into the Python standard library dataclasses.dataclass class decorator, after the declarative mapping process has been applied to the class. This function call may be swapped out for alternateive dataclasses providers, such as that of Pydantic, using the dataclass_callable parameter accepted by MappedAsDataclass as a class keyword argument as well as by registry.mapped_as_dataclass():

The above User class will be applied as a dataclass, using Pydantic’s pydantic.dataclasses.dataclasses callable. The process is available both for mapped classes as well as mixins that extend from MappedAsDataclass or which have registry.mapped_as_dataclass() applied directly.

Added in version 2.0.4: Added the dataclass_callable class and method parameters for MappedAsDataclass and registry.mapped_as_dataclass(), and adjusted some of the dataclass internals to accommodate more strict dataclass functions such as that of Pydantic.

The approaches described here are superseded by the Declarative Dataclass Mapping feature new in the 2.0 series of SQLAlchemy. This newer version of the feature builds upon the dataclass support first added in version 1.4, which is described in this section.

To map an existing dataclass, SQLAlchemy’s “inline” declarative directives cannot be used directly; ORM directives are assigned using one of three techniques:

Using “Declarative with Imperative Table”, the table / column to be mapped is defined using a Table object assigned to the __table__ attribute of the class; relationships are defined within __mapper_args__ dictionary. The class is mapped using the registry.mapped() decorator. An example is below at Mapping pre-existing dataclasses using Declarative With Imperative Table.

Using full “Declarative”, the Declarative-interpreted directives such as Column, relationship() are added to the .metadata dictionary of the dataclasses.field() construct, where they are consumed by the declarative process. The class is again mapped using the registry.mapped() decorator. See the example below at Mapping pre-existing dataclasses using Declarative-style fields.

An “Imperative” mapping can be applied to an existing dataclass using the registry.map_imperatively() method to produce the mapping in exactly the same way as described at Imperative Mapping. This is illustrated below at Mapping pre-existing dataclasses using Imperative Mapping.

The general process by which SQLAlchemy applies mappings to a dataclass is the same as that of an ordinary class, but also includes that SQLAlchemy will detect class-level attributes that were part of the dataclasses declaration process and replace them at runtime with the usual SQLAlchemy ORM mapped attributes. The __init__ method that would have been generated by dataclasses is left intact, as is the same for all the other methods that dataclasses generates such as __eq__(), __repr__(), etc.

An example of a mapping using @dataclass using Declarative with Imperative Table (a.k.a. Hybrid Declarative) is below. A complete Table object is constructed explicitly and assigned to the __table__ attribute. Instance fields are defined using normal dataclass syntaxes. Additional MapperProperty definitions such as relationship(), are placed in the __mapper_args__ class-level dictionary underneath the properties key, corresponding to the Mapper.properties parameter:

In the above example, the User.id, Address.id, and Address.user_id attributes are defined as field(init=False). This means that parameters for these won’t be added to __init__() methods, but Session will still be able to set them after getting their values during flush from autoincrement or other default value generator. To allow them to be specified in the constructor explicitly, they would instead be given a default value of None.

For a relationship() to be declared separately, it needs to be specified directly within the Mapper.properties dictionary which itself is specified within the __mapper_args__ dictionary, so that it is passed to the constructor for Mapper. An alternative to this approach is in the next example.

Declaring a dataclass field() setting a default together with init=False will not work as would be expected with a totally plain dataclass, since the SQLAlchemy class instrumentation will replace the default value set on the class by the dataclass creation process. Use default_factory instead. This adaptation is done automatically when making use of Declarative Dataclass Mapping.

This approach to Declarative mapping with dataclasses should be considered as legacy. It will remain supported however is unlikely to offer any advantages against the new approach detailed at Declarative Dataclass Mapping.

Note that mapped_column() is not supported with this use; the Column construct should continue to be used to declare table metadata within the metadata field of dataclasses.field().

The fully declarative approach requires that Column objects are declared as class attributes, which when using dataclasses would conflict with the dataclass-level attributes. An approach to combine these together is to make use of the metadata attribute on the dataclass.field object, where SQLAlchemy-specific mapping information may be supplied. Declarative supports extraction of these parameters when the class specifies the attribute __sa_dataclass_metadata_key__. This also provides a more succinct method of indicating the relationship() association:

In the section Composing Mapped Hierarchies with Mixins, Declarative Mixin classes are introduced. One requirement of declarative mixins is that certain constructs that can’t be easily duplicated must be given as callables, using the declared_attr decorator, such as in the example at Mixing in Relationships:

This form is supported within the Dataclasses field() object by using a lambda to indicate the SQLAlchemy construct inside the field(). Using declared_attr() to surround the lambda is optional. If we wanted to produce our User class above where the ORM fields came from a mixin that is itself a dataclass, the form would be:

Added in version 1.4.2: Added support for “declared attr” style mixin attributes, namely relationship() constructs as well as Column objects with foreign key declarations, to be used within “Dataclasses with Declarative Table” style mappings.

As described previously, a class which is set up as a dataclass using the @dataclass decorator can then be further decorated using the registry.mapped() decorator in order to apply declarative-style mapping to the class. As an alternative to using the registry.mapped() decorator, we may also pass the class through the registry.map_imperatively() method instead, so that we may pass all Table and Mapper configuration imperatively to the function rather than having them defined on the class itself as class variables:

The same warning mentioned in Mapping pre-existing dataclasses using Declarative With Imperative Table applies when using this mapping style.

The attrs library is not part of SQLAlchemy’s continuous integration testing, and compatibility with this library may change without notice due to incompatibilities introduced by either side.

The attrs library is a popular third party library that provides similar features as dataclasses, with many additional features provided not found in ordinary dataclasses.

A class augmented with attrs uses the @define decorator. This decorator initiates a process to scan the class for attributes that define the class’ behavior, which are then used to generate methods, documentation, and annotations.

The SQLAlchemy ORM supports mapping an attrs class using Imperative mapping. The general form of this style is equivalent to the Mapping pre-existing dataclasses using Imperative Mapping mapping form used with dataclasses, where the class construction uses attrs alone, with ORM mappings applied after the fact without any class attribute scanning.

The @define decorator of attrs by default replaces the annotated class with a new __slots__ based class, which is not supported. When using the old style annotation @attr.s or using define(slots=False), the class does not get replaced. Furthermore attrs removes its own class-bound attributes after the decorator runs, so that SQLAlchemy’s mapping process takes over these attributes without any issue. Both decorators, @attr.s and @define(slots=False) work with SQLAlchemy.

Changed in version 2.0: SQLAlchemy integration with attrs works only with imperative mapping style, that is, not using Declarative. The introduction of ORM Annotated Declarative style is not cross-compatible with attrs.

The attrs class is built first. The SQLAlchemy ORM mapping can be applied after the fact using registry.map_imperatively():

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (typescript):
```typescript
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import MappedAsDataclass


class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
```

Example 2 (php):
```php
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import MappedAsDataclass


class Base(DeclarativeBase):
    pass


class User(MappedAsDataclass, Base):
    """User class will be converted to a dataclass"""

    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
```

Example 3 (python):
```python
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry


reg = registry()


@reg.mapped_as_dataclass
class User:
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
```

Example 4 (python):
```python
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_as_dataclass
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry


reg = registry()


@mapped_as_dataclass(reg)
class User:
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/tutorial/metadata.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Unified Tutorial
    - Project Versions
- Working with Database Metadata¶
- Setting up MetaData with Table objects¶
  - Components of Table¶
  - Declaring Simple Constraints¶
  - Emitting DDL to the Database¶
- Using ORM Declarative Forms to Define Table Metadata¶

Home | Download this Documentation

Home | Download this Documentation

SQLAlchemy 1.4 / 2.0 Tutorial

This page is part of the SQLAlchemy Unified Tutorial.

Previous: Working with Transactions and the DBAPI | Next: Working with Data

With engines and SQL execution down, we are ready to begin some Alchemy. The central element of both SQLAlchemy Core and ORM is the SQL Expression Language which allows for fluent, composable construction of SQL queries. The foundation for these queries are Python objects that represent database concepts like tables and columns. These objects are known collectively as database metadata.

The most common foundational objects for database metadata in SQLAlchemy are known as MetaData, Table, and Column. The sections below will illustrate how these objects are used in both a Core-oriented style as well as an ORM-oriented style.

ORM readers, stay with us!

As with other sections, Core users can skip the ORM sections, but ORM users would best be familiar with these objects from both perspectives. The Table object discussed here is declared in a more indirect (and also fully Python-typed) way when using the ORM, however there is still a Table object within the ORM’s configuration.

When we work with a relational database, the basic data-holding structure in the database which we query from is known as a table. In SQLAlchemy, the database “table” is ultimately represented by a Python object similarly named Table.

To start using the SQLAlchemy Expression Language, we will want to have Table objects constructed that represent all of the database tables we are interested in working with. The Table is constructed programmatically, either directly by using the Table constructor, or indirectly by using ORM Mapped classes (described later at Using ORM Declarative Forms to Define Table Metadata). There is also the option to load some or all table information from an existing database, called reflection.

Whichever kind of approach is used, we always start out with a collection that will be where we place our tables known as the MetaData object. This object is essentially a facade around a Python dictionary that stores a series of Table objects keyed to their string name. While the ORM provides some options on where to get this collection, we always have the option to simply make one directly, which looks like:

Once we have a MetaData object, we can declare some Table objects. This tutorial will start with the classic SQLAlchemy tutorial model, which has a table called user_account that stores, for example, the users of a website, and a related table address, which stores email addresses associated with rows in the user_account table. When not using ORM Declarative models at all, we construct each Table object directly, typically assigning each to a variable that will be how we will refer to the table in application code:

With the above example, when we wish to write code that refers to the user_account table in the database, we will use the user_table Python variable to refer to it.

When do I make a MetaData object in my program?

Having a single MetaData object for an entire application is the most common case, represented as a module-level variable in a single place in an application, often in a “models” or “dbschema” type of package. It is also very common that the MetaData is accessed via an ORM-centric registry or Declarative Base base class, so that this same MetaData is shared among ORM- and Core-declared Table objects.

There can be multiple MetaData collections as well; Table objects can refer to Table objects in other collections without restrictions. However, for groups of Table objects that are related to each other, it is in practice much more straightforward to have them set up within a single MetaData collection, both from the perspective of declaring them, as well as from the perspective of DDL (i.e. CREATE and DROP) statements being emitted in the correct order.

We can observe that the Table construct as written in Python has a resemblance to a SQL CREATE TABLE statement; starting with the table name, then listing out each column, where each column has a name and a datatype. The objects we use above are:

Table - represents a database table and assigns itself to a MetaData collection.

Column - represents a column in a database table, and assigns itself to a Table object. The Column usually includes a string name and a type object. The collection of Column objects in terms of the parent Table are typically accessed via an associative array located at Table.c:

Integer, String - these classes represent SQL datatypes and can be passed to a Column with or without necessarily being instantiated. Above, we want to give a length of “30” to the “name” column, so we instantiated String(30). But for “id” and “fullname” we did not specify these, so we can send the class itself.

The reference and API documentation for MetaData, Table and Column is at Describing Databases with MetaData. The reference documentation for datatypes is at SQL Datatype Objects.

In an upcoming section, we will illustrate one of the fundamental functions of Table which is to generate DDL on a particular database connection. But first we will declare a second Table.

The first Column in the example user_table includes the Column.primary_key parameter which is a shorthand technique of indicating that this Column should be part of the primary key for this table. The primary key itself is normally declared implicitly and is represented by the PrimaryKeyConstraint construct, which we can see on the Table.primary_key attribute on the Table object:

The constraint that is most typically declared explicitly is the ForeignKeyConstraint object that corresponds to a database foreign key constraint. When we declare tables that are related to each other, SQLAlchemy uses the presence of these foreign key constraint declarations not only so that they are emitted within CREATE statements to the database, but also to assist in constructing SQL expressions.

A ForeignKeyConstraint that involves only a single column on the target table is typically declared using a column-level shorthand notation via the ForeignKey object. Below we declare a second table address that will have a foreign key constraint referring to the user table:

The table above also features a third kind of constraint, which in SQL is the “NOT NULL” constraint, indicated above using the Column.nullable parameter.

When using the ForeignKey object within a Column definition, we can omit the datatype for that Column; it is automatically inferred from that of the related column, in the above example the Integer datatype of the user_account.id column.

In the next section we will emit the completed DDL for the user and address table to see the completed result.

We’ve constructed an object structure that represents two database tables in a database, starting at the root MetaData object, then into two Table objects, each of which hold onto a collection of Column and Constraint objects. This object structure will be at the center of most operations we perform with both Core and ORM going forward.

The first useful thing we can do with this structure will be to emit CREATE TABLE statements, or DDL, to our SQLite database so that we can insert and query data from them. We have already all the tools needed to do so, by invoking the MetaData.create_all() method on our MetaData, sending it the Engine that refers to the target database:

The DDL create process above includes some SQLite-specific PRAGMA statements that test for the existence of each table before emitting a CREATE. The full series of steps are also included within a BEGIN/COMMIT pair to accommodate for transactional DDL.

The create process also takes care of emitting CREATE statements in the correct order; above, the FOREIGN KEY constraint is dependent on the user table existing, so the address table is created second. In more complicated dependency scenarios the FOREIGN KEY constraints may also be applied to tables after the fact using ALTER.

The MetaData object also features a MetaData.drop_all() method that will emit DROP statements in the reverse order as it would emit CREATE in order to drop schema elements.

Migration tools are usually appropriate

Overall, the CREATE / DROP feature of MetaData is useful for test suites, small and/or new applications, and applications that use short-lived databases. For management of an application database schema over the long term however, a schema management tool such as Alembic, which builds upon SQLAlchemy, is likely a better choice, as it can manage and orchestrate the process of incrementally altering a fixed database schema over time as the design of the application changes.

Another way to make Table objects?

The preceding examples illustrated direct use of the Table object, which underlies how SQLAlchemy ultimately refers to database tables when constructing SQL expressions. As mentioned, the SQLAlchemy ORM provides for a facade around the Table declaration process referred towards as Declarative Table. The Declarative Table process accomplishes the same goal as we had in the previous section, that of building Table objects, but also within that process gives us something else called an ORM mapped class, or just “mapped class”. The mapped class is the most common foundational unit of SQL when using the ORM, and in modern SQLAlchemy can also be used quite effectively with Core-centric use as well.

Some benefits of using Declarative Table include:

A more succinct and Pythonic style of setting up column definitions, where Python types may be used to represent SQL types to be used in the database

The resulting mapped class can be used to form SQL expressions that in many cases maintain PEP 484 typing information that’s picked up by static analysis tools such as Mypy and IDE type checkers

Allows declaration of table metadata and the ORM mapped class used in persistence / object loading operations all at once.

This section will illustrate the same Table metadata of the previous section(s) being constructed using Declarative Table.

When using the ORM, the process by which we declare Table metadata is usually combined with the process of declaring mapped classes. The mapped class is any Python class we’d like to create, which will then have attributes on it that will be linked to the columns in a database table. While there are a few varieties of how this is achieved, the most common style is known as declarative, and allows us to declare our user-defined classes and Table metadata at once.

When using the ORM, the MetaData collection remains present, however it itself is associated with an ORM-only construct commonly referred towards as the Declarative Base. The most expedient way to acquire a new Declarative Base is to create a new class that subclasses the SQLAlchemy DeclarativeBase class:

Above, the Base class is what we’ll call the Declarative Base. When we make new classes that are subclasses of Base, combined with appropriate class-level directives, they will each be established as a new ORM mapped class at class creation time, each one typically (but not exclusively) referring to a particular Table object.

The Declarative Base refers to a MetaData collection that is created for us automatically, assuming we didn’t provide one from the outside. This MetaData collection is accessible via the DeclarativeBase.metadata class-level attribute. As we create new mapped classes, they each will reference a Table within this MetaData collection:

The Declarative Base also refers to a collection called registry, which is the central “mapper configuration” unit in the SQLAlchemy ORM. While seldom accessed directly, this object is central to the mapper configuration process, as a set of ORM mapped classes will coordinate with each other via this registry. As was the case with MetaData, our Declarative Base also created a registry for us (again with options to pass our own registry), which we can access via the DeclarativeBase.registry class variable:

Other ways to map with the registry

DeclarativeBase is not the only way to map classes, only the most common. registry also provides other mapper configurational patterns, including decorator-oriented and imperative ways to map classes. There’s also full support for creating Python dataclasses while mapping. The reference documentation at ORM Mapped Class Configuration has it all.

With the Base class established, we can now define ORM mapped classes for the user_account and address tables in terms of new classes User and Address. We illustrate below the most modern form of Declarative, which is driven from PEP 484 type annotations using a special type Mapped, which indicates attributes to be mapped as particular types:

The two classes above, User and Address, are now called as ORM Mapped Classes, and are available for use in ORM persistence and query operations, which will be described later. Details about these classes include:

Each class refers to a Table object that was generated as part of the declarative mapping process, which is named by assigning a string to the DeclarativeBase.__tablename__ attribute. Once the class is created, this generated Table is available from the DeclarativeBase.__table__ attribute.

As mentioned previously, this form is known as Declarative Table Configuration. One of several alternative declaration styles would instead have us build the Table object directly, and assign it directly to DeclarativeBase.__table__. This style is known as Declarative with Imperative Table.

To indicate columns in the Table, we use the mapped_column() construct, in combination with typing annotations based on the Mapped type. This object will generate Column objects that are applied to the construction of the Table.

For columns with simple datatypes and no other options, we can indicate a Mapped type annotation alone, using simple Python types like int and str to mean Integer and String. Customization of how Python types are interpreted within the Declarative mapping process is very open ended; see the sections ORM Annotated Declarative - Complete Guide and Customizing the Type Map for background.

A column can be declared as “nullable” or “not null” based on the presence of the Optional[<typ>] type annotation (or its equivalents, <typ> | None or Union[<typ>, None]). The mapped_column.nullable parameter may also be used explicitly (and does not have to match the annotation’s optionality).

Use of explicit typing annotations is completely optional. We can also use mapped_column() without annotations. When using this form, we would use more explicit type objects like Integer and String as well as nullable=False as needed within each mapped_column() construct.

Two additional attributes, User.addresses and Address.user, define a different kind of attribute called relationship(), which features similar annotation-aware configuration styles as shown. The relationship() construct is discussed more fully at Working with ORM Related Objects.

The classes are automatically given an __init__() method if we don’t declare one of our own. The default form of this method accepts all attribute names as optional keyword arguments:

To automatically generate a full-featured __init__() method which provides for positional arguments as well as arguments with default keyword values, the dataclasses feature introduced at Declarative Dataclass Mapping may be used. It’s of course always an option to use an explicit __init__() method as well.

The __repr__() methods are added so that we get a readable string output; there’s no requirement for these methods to be here. As is the case with __init__(), a __repr__() method can be generated automatically by using the dataclasses feature.

Where’d the old Declarative go?

Users of SQLAlchemy 1.4 or previous will note that the above mapping uses a dramatically different form than before; not only does it use mapped_column() instead of Column in the Declarative mapping, it also uses Python type annotations to derive column information.

To provide context for users of the “old” way, Declarative mappings can still be made using Column objects (as well as using the declarative_base() function to create the base class) as before, and these forms will continue to be supported with no plans to remove support. The reason these two facilities are superseded by new constructs is first and foremost to integrate smoothly with PEP 484 tools, including IDEs such as VSCode and type checkers such as Mypy and Pyright, without the need for plugins. Secondly, deriving the declarations from type annotations is part of SQLAlchemy’s integration with Python dataclasses, which can now be generated natively from mappings.

For users who like the “old” way, but still desire their IDEs to not mistakenly report typing errors for their declarative mappings, the mapped_column() construct is a drop-in replacement for Column in an ORM Declarative mapping (note that mapped_column() is for ORM Declarative mappings only; it can’t be used within a Table construct), and the type annotations are optional. Our mapping above can be written without annotations as:

The above class has an advantage over one that uses Column directly, in that the User class as well as instances of User will indicate the correct typing information to typing tools, without the use of plugins. mapped_column() also allows for additional ORM-specific parameters to configure behaviors such as deferred column loading, which previously needed a separate deferred() function to be used with Column.

There’s also an example of converting an old-style Declarative class to the new style, which can be seen at ORM Declarative Models in the What’s New in SQLAlchemy 2.0? guide.

ORM Mapping Styles - full background on different ORM configurational styles.

Declarative Mapping - overview of Declarative class mapping

Declarative Table with mapped_column() - detail on how to use mapped_column() and Mapped to define the columns within a Table to be mapped when using Declarative.

As our ORM mapped classes refer to Table objects contained within a MetaData collection, emitting DDL given the Declarative Base uses the same process as that described previously at Emitting DDL to the Database. In our case, we have already generated the user and address tables in our SQLite database. If we had not done so already, we would be free to make use of the MetaData associated with our ORM Declarative Base class in order to do so, by accessing the collection from the DeclarativeBase.metadata attribute and then using MetaData.create_all() as before. In this case, PRAGMA statements are run, but no new tables are generated since they are found to be present already:

This section is just a brief introduction to the related subject of table reflection, or how to generate Table objects automatically from an existing database. Tutorial readers who want to get on with writing queries can feel free to skip this section.

To round out the section on working with table metadata, we will illustrate another operation that was mentioned at the beginning of the section, that of table reflection. Table reflection refers to the process of generating Table and related objects by reading the current state of a database. Whereas in the previous sections we’ve been declaring Table objects in Python, where we then have the option to emit DDL to the database to generate such a schema, the reflection process does these two steps in reverse, starting from an existing database and generating in-Python data structures to represent the schemas within that database.

There is no requirement that reflection must be used in order to use SQLAlchemy with a pre-existing database. It is entirely typical that the SQLAlchemy application declares all metadata explicitly in Python, such that its structure corresponds to that the existing database. The metadata structure also need not include tables, columns, or other constraints and constructs in the pre-existing database that are not needed for the local application to function.

As an example of reflection, we will create a new Table object which represents the some_table object we created manually in the earlier sections of this document. There are again some varieties of how this is performed, however the most basic is to construct a Table object, given the name of the table and a MetaData collection to which it will belong, then instead of indicating individual Column and Constraint objects, pass it the target Engine using the Table.autoload_with parameter:

At the end of the process, the some_table object now contains the information about the Column objects present in the table, and the object is usable in exactly the same way as a Table that we declared explicitly:

Read more about table and schema reflection at Reflecting Database Objects.

For ORM-related variants of table reflection, the section Mapping Declaratively with Reflected Tables includes an overview of the available options.

We now have a SQLite database ready to go with two tables present, and Core and ORM table-oriented constructs that we can use to interact with these tables via a Connection and/or ORM Session. In the following sections, we will illustrate how to create, manipulate, and select data using these structures.

SQLAlchemy 1.4 / 2.0 Tutorial

Next Tutorial Section: Working with Data

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
>>> from sqlalchemy import MetaData
>>> metadata_obj = MetaData()
```

Example 2 (python):
```python
>>> from sqlalchemy import Table, Column, Integer, String
>>> user_table = Table(
...     "user_account",
...     metadata_obj,
...     Column("id", Integer, primary_key=True),
...     Column("name", String(30)),
...     Column("fullname", String),
... )
```

Example 3 (json):
```json
>>> user_table.c.name
Column('name', String(length=30), table=<user_account>)

>>> user_table.c.keys()
['id', 'name', 'fullname']
```

Example 4 (typescript):
```typescript
>>> user_table.primary_key
PrimaryKeyConstraint(Column('id', Integer(), table=<user_account>, primary_key=True, nullable=False))
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/core/metadata.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Core
    - Project Versions
- Describing Databases with MetaData¶
- Accessing Tables and Columns¶
- Creating and Dropping Database Tables¶
- Altering Database Objects through Migrations¶
- Specifying the Schema Name¶
  - Specifying a Default Schema Name with MetaData¶

Home | Download this Documentation

Home | Download this Documentation

This section discusses the fundamental Table, Column and MetaData objects.

Working with Database Metadata - tutorial introduction to SQLAlchemy’s database metadata concept in the SQLAlchemy Unified Tutorial

A collection of metadata entities is stored in an object aptly named MetaData:

MetaData is a container object that keeps together many different features of a database (or multiple databases) being described.

To represent a table, use the Table class. Its two primary arguments are the table name, then the MetaData object which it will be associated with. The remaining positional arguments are mostly Column objects describing each column:

Above, a table called user is described, which contains four columns. The primary key of the table consists of the user_id column. Multiple columns may be assigned the primary_key=True flag which denotes a multi-column primary key, known as a composite primary key.

Note also that each column describes its datatype using objects corresponding to genericized types, such as Integer and String. SQLAlchemy features dozens of types of varying levels of specificity as well as the ability to create custom types. Documentation on the type system can be found at SQL Datatype Objects.

The MetaData object contains all of the schema constructs we’ve associated with it. It supports a few methods of accessing these table objects, such as the sorted_tables accessor which returns a list of each Table object in order of foreign key dependency (that is, each table is preceded by all tables which it references):

In most cases, individual Table objects have been explicitly declared, and these objects are typically accessed directly as module-level variables in an application. Once a Table has been defined, it has a full set of accessors which allow inspection of its properties. Given the following Table definition:

Note the ForeignKey object used in this table - this construct defines a reference to a remote table, and is fully described in Defining Foreign Keys. Methods of accessing information about this table include:

The FromClause.c collection, synonymous with the FromClause.columns collection, is an instance of ColumnCollection, which provides a dictionary-like interface to the collection of columns. Names are ordinarily accessed like attribute names, e.g. employees.c.employee_name. However for special names with spaces or those that match the names of dictionary methods such as ColumnCollection.keys() or ColumnCollection.values(), indexed access must be used, such as employees.c['values'] or employees.c["some column"]. See ColumnCollection for further information.

Once you’ve defined some Table objects, assuming you’re working with a brand new database one thing you might want to do is issue CREATE statements for those tables and their related constructs (as an aside, it’s also quite possible that you don’t want to do this, if you already have some preferred methodology such as tools included with your database or an existing scripting system - if that’s the case, feel free to skip this section - SQLAlchemy has no requirement that it be used to create your tables).

The usual way to issue CREATE is to use create_all() on the MetaData object. This method will issue queries that first check for the existence of each individual table, and if not found will issue the CREATE statements:

create_all() creates foreign key constraints between tables usually inline with the table definition itself, and for this reason it also generates the tables in order of their dependency. There are options to change this behavior such that ALTER TABLE is used instead.

Dropping all tables is similarly achieved using the drop_all() method. This method does the exact opposite of create_all() - the presence of each table is checked first, and tables are dropped in reverse order of dependency.

Creating and dropping individual tables can be done via the create() and drop() methods of Table. These methods by default issue the CREATE or DROP regardless of the table being present:

To enable the “check first for the table existing” logic, add the checkfirst=True argument to create() or drop():

While SQLAlchemy directly supports emitting CREATE and DROP statements for schema constructs, the ability to alter those constructs, usually via the ALTER statement as well as other database-specific constructs, is outside of the scope of SQLAlchemy itself. While it’s easy enough to emit ALTER statements and similar by hand, such as by passing a text() construct to Connection.execute() or by using the DDL construct, it’s a common practice to automate the maintenance of database schemas in relation to application code using schema migration tools.

The SQLAlchemy project offers the Alembic migration tool for this purpose. Alembic features a highly customizable environment and a minimalistic usage pattern, supporting such features as transactional DDL, automatic generation of “candidate” migrations, an “offline” mode which generates SQL scripts, and support for branch resolution.

Alembic supersedes the SQLAlchemy-Migrate project, which is the original migration tool for SQLAlchemy and is now considered legacy.

Most databases support the concept of multiple “schemas” - namespaces that refer to alternate sets of tables and other constructs. The server-side geometry of a “schema” takes many forms, including names of “schemas” under the scope of a particular database (e.g. PostgreSQL schemas), named sibling databases (e.g. MySQL / MariaDB access to other databases on the same server), as well as other concepts like tables owned by other usernames (Oracle Database, SQL Server) or even names that refer to alternate database files (SQLite ATTACH) or remote servers (Oracle Database DBLINK with synonyms).

What all of the above approaches have (mostly) in common is that there’s a way of referencing this alternate set of tables using a string name. SQLAlchemy refers to this name as the schema name. Within SQLAlchemy, this is nothing more than a string name which is associated with a Table object, and is then rendered into SQL statements in a manner appropriate to the target database such that the table is referenced in its remote “schema”, whatever mechanism that is on the target database.

The “schema” name may be associated directly with a Table using the Table.schema argument; when using the ORM with declarative table configuration, the parameter is passed using the __table_args__ parameter dictionary.

The “schema” name may also be associated with the MetaData object where it will take effect automatically for all Table objects associated with that MetaData that don’t otherwise specify their own name. Finally, SQLAlchemy also supports a “dynamic” schema name system that is often used for multi-tenant applications such that a single set of Table metadata may refer to a dynamically configured set of schema names on a per-connection or per-statement basis.

SQLAlchemy’s support for database “schema” was designed with first party support for PostgreSQL-style schemas. In this style, there is first a “database” that typically has a single “owner”. Within this database there can be any number of “schemas” which then contain the actual table objects.

A table within a specific schema is referenced explicitly using the syntax “<schemaname>.<tablename>”. Contrast this to an architecture such as that of MySQL, where there are only “databases”, however SQL statements can refer to multiple databases at once, using the same syntax except it is “<database>.<tablename>”. On Oracle Database, this syntax refers to yet another concept, the “owner” of a table. Regardless of which kind of database is in use, SQLAlchemy uses the phrase “schema” to refer to the qualifying identifier within the general syntax of “<qualifier>.<tablename>”.

Explicit Schema Name with Declarative Table - schema name specification when using the ORM declarative table configuration

The most basic example is that of the Table.schema argument using a Core Table object as follows:

SQL that is rendered using this Table, such as the SELECT statement below, will explicitly qualify the table name financial_info with the remote_banks schema name:

When a Table object is declared with an explicit schema name, it is stored in the internal MetaData namespace using the combination of the schema and table name. We can view this in the MetaData.tables collection by searching for the key 'remote_banks.financial_info':

This dotted name is also what must be used when referring to the table for use with the ForeignKey or ForeignKeyConstraint objects, even if the referring table is also in that same schema:

The Table.schema argument may also be used with certain dialects to indicate a multiple-token (e.g. dotted) path to a particular table. This is particularly important on a database such as Microsoft SQL Server where there are often dotted “database/owner” tokens. The tokens may be placed directly in the name at once, such as:

Multipart Schema Names - describes use of dotted schema names with the SQL Server dialect.

Reflecting Tables from Other Schemas

The MetaData object may also set up an explicit default option for all Table.schema parameters by passing the MetaData.schema argument to the top level MetaData construct:

Above, for any Table object (or Sequence object directly associated with the MetaData) which leaves the Table.schema parameter at its default of None will instead act as though the parameter were set to the value "remote_banks". This includes that the Table is cataloged in the MetaData using the schema-qualified name, that is:

When using the ForeignKey or ForeignKeyConstraint objects to refer to this table, either the schema-qualified name or the non-schema-qualified name may be used to refer to the remote_banks.financial_info table:

When using a MetaData object that sets MetaData.schema, a Table that wishes to specify that it should not be schema qualified may use the special symbol BLANK_SCHEMA:

The names used by the Table.schema parameter may also be applied against a lookup that is dynamic on a per-connection or per-execution basis, so that for example in multi-tenant situations, each transaction or statement may be targeted at a specific set of schema names that change. The section Translation of Schema Names describes how this feature is used.

Translation of Schema Names

The above approaches all refer to methods of including an explicit schema-name within SQL statements. Database connections in fact feature the concept of a “default” schema, which is the name of the “schema” (or database, owner, etc.) that takes place if a table name is not explicitly schema-qualified. These names are usually configured at the login level, such as when connecting to a PostgreSQL database, the default “schema” is called “public”.

There are often cases where the default “schema” cannot be set via the login itself and instead would usefully be configured each time a connection is made, using a statement such as “SET SEARCH_PATH” on PostgreSQL or “ALTER SESSION” on Oracle Database. These approaches may be achieved by using the PoolEvents.connect() event, which allows access to the DBAPI connection when it is first created. For example, to set the Oracle Database CURRENT_SCHEMA variable to an alternate name:

Above, the set_current_schema() event handler will take place immediately when the above Engine first connects; as the event is “inserted” into the beginning of the handler list, it will also take place before the dialect’s own event handlers are run, in particular including the one that will determine the “default schema” for the connection.

For other databases, consult the database and/or dialect documentation for specific information regarding how default schemas are configured.

Changed in version 1.4.0b2: The above recipe now works without the need to establish additional event handlers.

Setting Alternate Search Paths on Connect - in the PostgreSQL dialect documentation.

The schema feature of SQLAlchemy interacts with the table reflection feature introduced at Reflecting Database Objects. See the section Reflecting Tables from Other Schemas for additional details on how this works.

Table supports database-specific options. For example, MySQL has different table backend types, including “MyISAM” and “InnoDB”. This can be expressed with Table using mysql_engine:

Other backends may support table-level options as well - these would be described in the individual documentation sections for each dialect.

Represents a column in a database table.

insert_sentinel([name, type_], *, [default, omit_from_statements])

Provides a surrogate Column that will act as a dedicated insert sentinel column, allowing efficient bulk inserts with deterministic RETURNING sorting for tables that don’t otherwise have qualifying primary key configurations.

A collection of Table objects and their associated schema constructs.

Base class for items that define a database schema.

Represent a table in a database.

Refers to SchemaConst.BLANK_SCHEMA.

Refers to SchemaConst.RETAIN_SCHEMA

inherits from sqlalchemy.sql.expression.DialectKWArgs, sqlalchemy.schema.SchemaItem, sqlalchemy.sql.expression.ColumnClause

Represents a column in a database table.

Implement the == operator.

Construct a new Column object.

Implement the <= operator.

Implement the < operator.

Implement the != operator.

Produce an all_() clause against the parent object.

Produce an any_() clause against the parent object.

Add a new kind of dialect-specific keyword argument for this class.

Produce a asc() clause against the parent object.

Produce a between() clause against the parent object, given the lower and upper range.

Produce a bitwise AND operation, typically via the & operator.

Produce a bitwise LSHIFT operation, typically via the << operator.

Produce a bitwise NOT operation, typically via the ~ operator.

Produce a bitwise OR operation, typically via the | operator.

Produce a bitwise RSHIFT operation, typically via the >> operator.

Produce a bitwise XOR operation, typically via the ^ operator, or # for PostgreSQL.

Return a custom boolean operator.

Produce a type cast, i.e. CAST(<expression> AS <type>).

Produce a collate() clause against the parent object, given the collation string.

Compare this ClauseElement to the given ClauseElement.

Compile this SQL expression.

Implement the ‘concat’ operator.

Implement the ‘contains’ operator.

Produce a desc() clause against the parent object.

A collection of keyword arguments specified as dialect-specific options to this construct.

Produce a distinct() clause against the parent object.

Implement the ‘endswith’ operator.

A collection of all ForeignKey marker objects associated with this Column.

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

Implement the icontains operator, e.g. case insensitive version of ColumnOperators.contains().

Implement the iendswith operator, e.g. case insensitive version of ColumnOperators.endswith().

Implement the ilike operator, e.g. case insensitive LIKE.

Implement the in operator.

The value of the Column.index parameter.

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

Implement the IS operator.

Implement the IS DISTINCT FROM operator.

Implement the IS NOT operator.

is_not_distinct_from()

Implement the IS NOT DISTINCT FROM operator.

Implement the IS NOT operator.

isnot_distinct_from()

Implement the IS NOT DISTINCT FROM operator.

Implement the istartswith operator, e.g. case insensitive version of ColumnOperators.startswith().

The ‘key’ that in some circumstances refers to this object in a Python namespace.

Produce a column label, i.e. <columnname> AS <name>.

Implement the like operator.

Implements a database-specific ‘match’ operator.

implement the NOT ILIKE operator.

implement the NOT IN operator.

implement the NOT LIKE operator.

implement the NOT ILIKE operator.

implement the NOT IN operator.

implement the NOT LIKE operator.

Produce a nulls_first() clause against the parent object.

Produce a nulls_last() clause against the parent object.

Produce a nulls_first() clause against the parent object.

Produce a nulls_last() clause against the parent object.

Produce a generic operator function.

Operate on an argument.

Return a copy with bindparam() elements replaced.

set of all columns we are proxying

Return True if this Column references the given column via foreign key.

Implements a database-specific ‘regexp match’ operator.

Implements a database-specific ‘regexp replace’ operator.

Reverse operate on an argument.

Apply a ‘grouping’ to this ClauseElement.

Return True if the given ColumnElement has a common ancestor to this ColumnElement.

Implement the startswith operator.

Hack, allows datetime objects to be compared on the LHS.

The value of the Column.unique parameter.

Return a copy with bindparam() elements replaced.

inherited from the sqlalchemy.sql.expression.ColumnOperators.__eq__ method of ColumnOperators

Implement the == operator.

In a column context, produces the clause a = b. If the target is None, produces a IS NULL.

Construct a new Column object.

The name of this column as represented in the database. This argument may be the first positional argument, or specified via keyword.

Names which contain no upper case characters will be treated as case insensitive names, and will not be quoted unless they are a reserved word. Names with any number of upper case characters will be quoted and sent exactly. Note that this behavior applies even for databases which standardize upper case names as case insensitive such as Oracle Database.

The name field may be omitted at construction time and applied later, at any time before the Column is associated with a Table. This is to support convenient usage within the declarative extension.

The column’s type, indicated using an instance which subclasses TypeEngine. If no arguments are required for the type, the class of the type can be sent as well, e.g.:

The type argument may be the second positional argument or specified by keyword.

If the type is None or is omitted, it will first default to the special type NullType. If and when this Column is made to refer to another column using ForeignKey and/or ForeignKeyConstraint, the type of the remote-referenced column will be copied to this column as well, at the moment that the foreign key is resolved against that remote Column object.

*args¶ – Additional positional arguments include various SchemaItem derived constructs which will be applied as options to the column. These include instances of Constraint, ForeignKey, ColumnDefault, Sequence, Computed Identity. In some cases an equivalent keyword argument is available such as server_default, default and unique.

Set up “auto increment” semantics for an integer primary key column with no foreign key dependencies (see later in this docstring for a more specific definition). This may influence the DDL that will be emitted for this column during a table create, as well as how the column will be considered when INSERT statements are compiled and executed.

The default value is the string "auto", which indicates that a single-column (i.e. non-composite) primary key that is of an INTEGER type with no other client-side or server-side default constructs indicated should receive auto increment semantics automatically. Other values include True (force this column to have auto-increment semantics for a composite primary key as well), False (this column should never have auto-increment semantics), and the string "ignore_fk" (special-case for foreign key columns, see below).

The term “auto increment semantics” refers both to the kind of DDL that will be emitted for the column within a CREATE TABLE statement, when methods such as MetaData.create_all() and Table.create() are invoked, as well as how the column will be considered when an INSERT statement is compiled and emitted to the database:

DDL rendering (i.e. MetaData.create_all(), Table.create()): When used on a Column that has no other default-generating construct associated with it (such as a Sequence or Identity construct), the parameter will imply that database-specific keywords such as PostgreSQL SERIAL, MySQL AUTO_INCREMENT, or IDENTITY on SQL Server should also be rendered. Not every database backend has an “implied” default generator available; for example the Oracle Database backends always needs an explicit construct such as Identity to be included with a Column in order for the DDL rendered to include auto-generating constructs to also be produced in the database.

INSERT semantics (i.e. when a insert() construct is compiled into a SQL string and is then executed on a database using Connection.execute() or equivalent): A single-row INSERT statement will be known to produce a new integer primary key value automatically for this column, which will be accessible after the statement is invoked via the CursorResult.inserted_primary_key attribute upon the Result object. This also applies towards use of the ORM when ORM-mapped objects are persisted to the database, indicating that a new integer primary key will be available to become part of the identity key for that object. This behavior takes place regardless of what DDL constructs are associated with the Column and is independent of the “DDL Rendering” behavior discussed in the previous note above.

The parameter may be set to True to indicate that a column which is part of a composite (i.e. multi-column) primary key should have autoincrement semantics, though note that only one column within a primary key may have this setting. It can also be set to True to indicate autoincrement semantics on a column that has a client-side or server-side default configured, however note that not all dialects can accommodate all styles of default as an “autoincrement”. It can also be set to False on a single-column primary key that has a datatype of INTEGER in order to disable auto increment semantics for that column.

The setting only has an effect for columns which are:

Integer derived (i.e. INT, SMALLINT, BIGINT).

Part of the primary key

Not referring to another column via ForeignKey, unless the value is specified as 'ignore_fk':

It is typically not desirable to have “autoincrement” enabled on a column that refers to another via foreign key, as such a column is required to refer to a value that originates from elsewhere.

The setting has these effects on columns that meet the above criteria:

DDL issued for the column, if the column does not already include a default generating construct supported by the backend such as Identity, will include database-specific keywords intended to signify this column as an “autoincrement” column for specific backends. Behavior for primary SQLAlchemy dialects includes:

AUTO INCREMENT on MySQL and MariaDB

IDENTITY on MS-SQL - this occurs even without the Identity construct as the Column.autoincrement parameter pre-dates this construct.

SQLite - SQLite integer primary key columns are implicitly “auto incrementing” and no additional keywords are rendered; to render the special SQLite keyword AUTOINCREMENT is not included as this is unnecessary and not recommended by the database vendor. See the section SQLite Auto Incrementing Behavior for more background.

Oracle Database - The Oracle Database dialects have no default “autoincrement” feature available at this time, instead the Identity construct is recommended to achieve this (the Sequence construct may also be used).

Third-party dialects - consult those dialects’ documentation for details on their specific behaviors.

When a single-row insert() construct is compiled and executed, which does not set the Insert.inline() modifier, newly generated primary key values for this column will be automatically retrieved upon statement execution using a method specific to the database driver in use:

MySQL, SQLite - calling upon cursor.lastrowid() (see https://www.python.org/dev/peps/pep-0249/#lastrowid)

PostgreSQL, SQL Server, Oracle Database - use RETURNING or an equivalent construct when rendering an INSERT statement, and then retrieving the newly generated primary key values after execution

PostgreSQL, Oracle Database for Table objects that set Table.implicit_returning to False - for a Sequence only, the Sequence is invoked explicitly before the INSERT statement takes place so that the newly generated primary key value is available to the client

SQL Server for Table objects that set Table.implicit_returning to False - the SELECT scope_identity() construct is used after the INSERT statement is invoked to retrieve the newly generated primary key value.

Third-party dialects - consult those dialects’ documentation for details on their specific behaviors.

For multiple-row insert() constructs invoked with a list of parameters (i.e. “executemany” semantics), primary-key retrieving behaviors are generally disabled, however there may be special APIs that may be used to retrieve lists of new primary key values for an “executemany”, such as the psycopg2 “fast insertmany” feature. Such features are very new and may not yet be well covered in documentation.

A scalar, Python callable, or ColumnElement expression representing the default value for this column, which will be invoked upon insert if this column is otherwise not specified in the VALUES clause of the insert. This is a shortcut to using ColumnDefault as a positional argument; see that class for full detail on the structure of the argument.

Contrast this argument to Column.server_default which creates a default generator on the database side.

Column INSERT/UPDATE Defaults

An alias of Column.default for compatibility with mapped_column().

doc¶ – optional String that can be used by the ORM or similar to document attributes on the Python side. This attribute does not render SQL comments; use the Column.comment parameter for this purpose.

key¶ – An optional string identifier which will identify this Column object on the Table. When a key is provided, this is the only identifier referencing the Column within the application, including ORM attribute mapping; the name field is used only when rendering SQL.

When True, indicates that a Index construct will be automatically generated for this Column, which will result in a “CREATE INDEX” statement being emitted for the Table when the DDL create operation is invoked.

Using this flag is equivalent to making use of the Index construct explicitly at the level of the Table construct itself:

To add the Index.unique flag to the Index, set both the Column.unique and Column.index flags to True simultaneously, which will have the effect of rendering the “CREATE UNIQUE INDEX” DDL instruction instead of “CREATE INDEX”.

The name of the index is generated using the default naming convention which for the Index construct is of the form ix_<tablename>_<columnname>.

As this flag is intended only as a convenience for the common case of adding a single-column, default configured index to a table definition, explicit use of the Index construct should be preferred for most use cases, including composite indexes that encompass more than one column, indexes with SQL expressions or ordering, backend-specific index configuration options, and indexes that use a specific name.

the Column.index attribute on Column does not indicate if this column is indexed or not, only if this flag was explicitly set here. To view indexes on a column, view the Table.indexes collection or use Inspector.get_indexes().

Configuring Constraint Naming Conventions

info¶ – Optional data dictionary which will be populated into the SchemaItem.info attribute of this object.

When set to False, will cause the “NOT NULL” phrase to be added when generating DDL for the column. When True, will normally generate nothing (in SQL this defaults to “NULL”), except in some very specific backend-specific edge cases where “NULL” may render explicitly. Defaults to True unless Column.primary_key is also True or the column specifies a Identity, in which case it defaults to False. This parameter is only used when issuing CREATE TABLE statements.

When the column specifies a Identity this parameter is in general ignored by the DDL compiler. The PostgreSQL database allows nullable identity column by setting this parameter to True explicitly.

A scalar, Python callable, or ClauseElement representing a default value to be applied to the column within UPDATE statements, which will be invoked upon update if this column is not present in the SET clause of the update. This is a shortcut to using ColumnDefault as a positional argument with for_update=True.

Column INSERT/UPDATE Defaults - complete discussion of onupdate

primary_key¶ – If True, marks this column as a primary key column. Multiple columns can have this flag set to specify composite primary keys. As an alternative, the primary key of a Table can be specified via an explicit PrimaryKeyConstraint object.

A FetchedValue instance, str, Unicode or text() construct representing the DDL DEFAULT value for the column.

String types will be emitted as-is, surrounded by single quotes:

A text() expression will be rendered as-is, without quotes:

Strings and text() will be converted into a DefaultClause object upon initialization.

This parameter can also accept complex combinations of contextually valid SQLAlchemy expressions or constructs:

The above results in a table created with the following SQL:

Use FetchedValue to indicate that an already-existing column will generate a default value on the database side which will be available to SQLAlchemy for post-fetch after inserts. This construct does not specify any DDL and the implementation is left to the database, such as via a trigger.

Server-invoked DDL-Explicit Default Expressions - complete discussion of server side defaults

A FetchedValue instance representing a database-side default generation function, such as a trigger. This indicates to SQLAlchemy that a newly generated value will be available after updates. This construct does not actually implement any kind of generation function within the database, which instead must be specified separately.

This directive does not currently produce MySQL’s “ON UPDATE CURRENT_TIMESTAMP()” clause. See Rendering ON UPDATE CURRENT TIMESTAMP for MySQL / MariaDB’s explicit_defaults_for_timestamp for background on how to produce this clause.

Marking Implicitly Generated Values, timestamps, and Triggered Columns

quote¶ – Force quoting of this column’s name on or off, corresponding to True or False. When left at its default of None, the column identifier will be quoted according to whether the name is case sensitive (identifiers with at least one upper case character are treated as case sensitive), or if it’s a reserved word. This flag is only needed to force quoting of a reserved word which is not known by the SQLAlchemy dialect.

When True, and the Column.index parameter is left at its default value of False, indicates that a UniqueConstraint construct will be automatically generated for this Column, which will result in a “UNIQUE CONSTRAINT” clause referring to this column being included in the CREATE TABLE statement emitted, when the DDL create operation for the Table object is invoked.

When this flag is True while the Column.index parameter is simultaneously set to True, the effect instead is that a Index construct which includes the Index.unique parameter set to True is generated. See the documentation for Column.index for additional detail.

Using this flag is equivalent to making use of the UniqueConstraint construct explicitly at the level of the Table construct itself:

The UniqueConstraint.name parameter of the unique constraint object is left at its default value of None; in the absence of a naming convention for the enclosing MetaData, the UNIQUE CONSTRAINT construct will be emitted as unnamed, which typically invokes a database-specific naming convention to take place.

As this flag is intended only as a convenience for the common case of adding a single-column, default configured unique constraint to a table definition, explicit use of the UniqueConstraint construct should be preferred for most use cases, including composite constraints that encompass more than one column, backend-specific index configuration options, and constraints that use a specific name.

the Column.unique attribute on Column does not indicate if this column has a unique constraint or not, only if this flag was explicitly set here. To view indexes and unique constraints that may involve this column, view the Table.indexes and/or Table.constraints collections or use Inspector.get_indexes() and/or Inspector.get_unique_constraints()

Configuring Constraint Naming Conventions

When True, indicates this is a “system” column, that is a column which is automatically made available by the database, and should not be included in the columns list for a CREATE TABLE statement.

For more elaborate scenarios where columns should be conditionally rendered differently on different backends, consider custom compilation rules for CreateColumn.

Optional string that will render an SQL comment on table creation.

Added in version 1.2: Added the Column.comment parameter to Column.

Marks this Column as an insert sentinel used for optimizing the performance of the insertmanyvalues feature for tables that don’t otherwise have qualifying primary key configurations.

Added in version 2.0.10.

insert_sentinel() - all in one helper for declaring sentinel columns

“Insert Many Values” Behavior for INSERT statements

Configuring Sentinel Columns

inherited from the sqlalchemy.sql.expression.ColumnOperators.__le__ method of ColumnOperators

Implement the <= operator.

In a column context, produces the clause a <= b.

inherited from the sqlalchemy.sql.expression.ColumnOperators.__lt__ method of ColumnOperators

Implement the < operator.

In a column context, produces the clause a < b.

inherited from the sqlalchemy.sql.expression.ColumnOperators.__ne__ method of ColumnOperators

Implement the != operator.

In a column context, produces the clause a != b. If the target is None, produces a IS NOT NULL.

inherited from the ColumnOperators.all_() method of ColumnOperators

Produce an all_() clause against the parent object.

See the documentation for all_() for examples.

be sure to not confuse the newer ColumnOperators.all_() method with the legacy version of this method, the Comparator.all() method that’s specific to ARRAY, which uses a different calling style.

Deprecated since version 1.4: The ColumnElement.anon_key_label attribute is now private, and the public accessor is deprecated.

Deprecated since version 1.4: The ColumnElement.anon_label attribute is now private, and the public accessor is deprecated.

inherited from the ColumnOperators.any_() method of ColumnOperators

Produce an any_() clause against the parent object.

See the documentation for any_() for examples.

be sure to not confuse the newer ColumnOperators.any_() method with the legacy version of this method, the Comparator.any() method that’s specific to ARRAY, which uses a different calling style.

inherited from the DialectKWArgs.argument_for() method of DialectKWArgs

Add a new kind of dialect-specific keyword argument for this class.

The DialectKWArgs.argument_for() method is a per-argument way adding extra arguments to the DefaultDialect.construct_arguments dictionary. This dictionary provides a list of argument names accepted by various schema-level constructs on behalf of a dialect.

New dialects should typically specify this dictionary all at once as a data member of the dialect class. The use case for ad-hoc addition of argument names is typically for end-user code that is also using a custom compilation scheme which consumes the additional arguments.

dialect_name¶ – name of a dialect. The dialect must be locatable, else a NoSuchModuleError is raised. The dialect must also include an existing DefaultDialect.construct_arguments collection, indicating that it participates in the keyword-argument validation and default system, else ArgumentError is raised. If the dialect does not include this collection, then any keyword argument can be specified on behalf of this dialect already. All dialects packaged within SQLAlchemy include this collection, however for third party dialects, support may vary.

argument_name¶ – name of the parameter.

default¶ – default value of the parameter.

inherited from the ColumnOperators.asc() method of ColumnOperators

Produce a asc() clause against the parent object.

inherited from the ColumnOperators.between() method of ColumnOperators

Produce a between() clause against the parent object, given the lower and upper range.

inherited from the ColumnOperators.bitwise_and() method of ColumnOperators

Produce a bitwise AND operation, typically via the & operator.

Added in version 2.0.2.

inherited from the ColumnOperators.bitwise_lshift() method of ColumnOperators

Produce a bitwise LSHIFT operation, typically via the << operator.

Added in version 2.0.2.

inherited from the ColumnOperators.bitwise_not() method of ColumnOperators

Produce a bitwise NOT operation, typically via the ~ operator.

Added in version 2.0.2.

inherited from the ColumnOperators.bitwise_or() method of ColumnOperators

Produce a bitwise OR operation, typically via the | operator.

Added in version 2.0.2.

inherited from the ColumnOperators.bitwise_rshift() method of ColumnOperators

Produce a bitwise RSHIFT operation, typically via the >> operator.

Added in version 2.0.2.

inherited from the ColumnOperators.bitwise_xor() method of ColumnOperators

Produce a bitwise XOR operation, typically via the ^ operator, or # for PostgreSQL.

Added in version 2.0.2.

inherited from the Operators.bool_op() method of Operators

Return a custom boolean operator.

This method is shorthand for calling Operators.op() and passing the Operators.op.is_comparison flag with True. A key advantage to using Operators.bool_op() is that when using column constructs, the “boolean” nature of the returned expression will be present for PEP 484 purposes.

inherited from the ColumnElement.cast() method of ColumnElement

Produce a type cast, i.e. CAST(<expression> AS <type>).

This is a shortcut to the cast() function.

Data Casts and Type Coercion

inherited from the ColumnOperators.collate() method of ColumnOperators

Produce a collate() clause against the parent object, given the collation string.

inherited from the ClauseElement.compare() method of ClauseElement

Compare this ClauseElement to the given ClauseElement.

Subclasses should override the default behavior, which is a straight identity comparison.

**kw are arguments consumed by subclass compare() methods and may be used to modify the criteria for comparison (see ColumnElement).

inherited from the CompilerElement.compile() method of CompilerElement

Compile this SQL expression.

The return value is a Compiled object. Calling str() or unicode() on the returned value will yield a string representation of the result. The Compiled object also can return a dictionary of bind parameter names and values using the params accessor.

bind¶ – An Connection or Engine which can provide a Dialect in order to generate a Compiled object. If the bind and dialect parameters are both omitted, a default SQL compiler is used.

column_keys¶ – Used for INSERT and UPDATE statements, a list of column names which should be present in the VALUES clause of the compiled statement. If None, all columns from the target table object are rendered.

dialect¶ – A Dialect instance which can generate a Compiled object. This argument takes precedence over the bind argument.

optional dictionary of additional parameters that will be passed through to the compiler within all “visit” methods. This allows any custom flag to be passed through to a custom compilation construct, for example. It is also used for the case of passing the literal_binds flag through:

How do I render SQL expressions as strings, possibly with bound parameters inlined?

inherited from the ColumnOperators.concat() method of ColumnOperators

Implement the ‘concat’ operator.

In a column context, produces the clause a || b, or uses the concat() operator on MySQL.

inherited from the ColumnOperators.contains() method of ColumnOperators

Implement the ‘contains’ operator.

Produces a LIKE expression that tests against a match for the middle of a string value:

Since the operator uses LIKE, wildcard characters "%" and "_" that are present inside the <other> expression will behave like wildcards as well. For literal string values, the ColumnOperators.contains.autoescape flag may be set to True to apply escaping to occurrences of these characters within the string value so that they match as themselves and not as wildcard characters. Alternatively, the ColumnOperators.contains.escape parameter will establish a given character as an escape character which can be of use when the target expression is not a literal string.

other¶ – expression to be compared. This is usually a plain string value, but can also be an arbitrary SQL expression. LIKE wildcard characters % and _ are not escaped by default unless the ColumnOperators.contains.autoescape flag is set to True.

boolean; when True, establishes an escape character within the LIKE expression, then applies it to all occurrences of "%", "_" and the escape character itself within the comparison value, which is assumed to be a literal string and not a SQL expression.

An expression such as:

With the value of :param as "foo/%bar".

a character which when given will render with the ESCAPE keyword to establish that character as the escape character. This character can then be placed preceding occurrences of % and _ to allow them to act as themselves and not wildcard characters.

An expression such as:

The parameter may also be combined with ColumnOperators.contains.autoescape:

Where above, the given literal parameter will be converted to "foo^%bar^^bat" before being passed to the database.

ColumnOperators.startswith()

ColumnOperators.endswith()

ColumnOperators.like()

Deprecated since version 1.4: The Column.copy() method is deprecated and will be removed in a future release.

inherited from the ColumnOperators.desc() method of ColumnOperators

Produce a desc() clause against the parent object.

A collection of keyword arguments specified as dialect-specific options to this construct.

The arguments are present here in their original <dialect>_<kwarg> format. Only arguments that were actually passed are included; unlike the DialectKWArgs.dialect_options collection, which contains all options known by this dialect including defaults.

The collection is also writable; keys are accepted of the form <dialect>_<kwarg> where the value will be assembled into the list of options.

DialectKWArgs.dialect_options - nested dictionary form

inherited from the DialectKWArgs.dialect_options attribute of DialectKWArgs

A collection of keyword arguments specified as dialect-specific options to this construct.

This is a two-level nested registry, keyed to <dialect_name> and <argument_name>. For example, the postgresql_where argument would be locatable as:

Added in version 0.9.2.

DialectKWArgs.dialect_kwargs - flat dictionary form

inherited from the ColumnOperators.distinct() method of ColumnOperators

Produce a distinct() clause against the parent object.

inherited from the ColumnOperators.endswith() method of ColumnOperators

Implement the ‘endswith’ operator.

Produces a LIKE expression that tests against a match for the end of a string value:

Since the operator uses LIKE, wildcard characters "%" and "_" that are present inside the <other> expression will behave like wildcards as well. For literal string values, the ColumnOperators.endswith.autoescape flag may be set to True to apply escaping to occurrences of these characters within the string value so that they match as themselves and not as wildcard characters. Alternatively, the ColumnOperators.endswith.escape parameter will establish a given character as an escape character which can be of use when the target expression is not a literal string.

other¶ – expression to be compared. This is usually a plain string value, but can also be an arbitrary SQL expression. LIKE wildcard characters % and _ are not escaped by default unless the ColumnOperators.endswith.autoescape flag is set to True.

boolean; when True, establishes an escape character within the LIKE expression, then applies it to all occurrences of "%", "_" and the escape character itself within the comparison value, which is assumed to be a literal string and not a SQL expression.

An expression such as:

With the value of :param as "foo/%bar".

a character which when given will render with the ESCAPE keyword to establish that character as the escape character. This character can then be placed preceding occurrences of % and _ to allow them to act as themselves and not wildcard characters.

An expression such as:

The parameter may also be combined with ColumnOperators.endswith.autoescape:

Where above, the given literal parameter will be converted to "foo^%bar^^bat" before being passed to the database.

ColumnOperators.startswith()

ColumnOperators.contains()

ColumnOperators.like()

Return a column expression.

Part of the inspection interface; returns self.

inherited from the ColumnElement.foreign_keys attribute of ColumnElement

A collection of all ForeignKey marker objects associated with this Column.

Each object is a member of a Table-wide ForeignKeyConstraint.

inherited from the ColumnClause.get_children() method of ColumnClause

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

This is used for visit traversal.

**kw may contain flags that change the collection that is returned, for example to return a subset of items in order to cut down on larger traversals, or to return child items from a different context (such as schema-level collections instead of clause-level).

inherited from the ColumnOperators.icontains() method of ColumnOperators

Implement the icontains operator, e.g. case insensitive version of ColumnOperators.contains().

Produces a LIKE expression that tests against an insensitive match for the middle of a string value:

Since the operator uses LIKE, wildcard characters "%" and "_" that are present inside the <other> expression will behave like wildcards as well. For literal string values, the ColumnOperators.icontains.autoescape flag may be set to True to apply escaping to occurrences of these characters within the string value so that they match as themselves and not as wildcard characters. Alternatively, the ColumnOperators.icontains.escape parameter will establish a given character as an escape character which can be of use when the target expression is not a literal string.

other¶ – expression to be compared. This is usually a plain string value, but can also be an arbitrary SQL expression. LIKE wildcard characters % and _ are not escaped by default unless the ColumnOperators.icontains.autoescape flag is set to True.

boolean; when True, establishes an escape character within the LIKE expression, then applies it to all occurrences of "%", "_" and the escape character itself within the comparison value, which is assumed to be a literal string and not a SQL expression.

An expression such as:

With the value of :param as "foo/%bar".

a character which when given will render with the ESCAPE keyword to establish that character as the escape character. This character can then be placed preceding occurrences of % and _ to allow them to act as themselves and not wildcard characters.

An expression such as:

The parameter may also be combined with ColumnOperators.contains.autoescape:

Where above, the given literal parameter will be converted to "foo^%bar^^bat" before being passed to the database.

ColumnOperators.contains()

inherited from the ColumnOperators.iendswith() method of ColumnOperators

Implement the iendswith operator, e.g. case insensitive version of ColumnOperators.endswith().

Produces a LIKE expression that tests against an insensitive match for the end of a string value:

Since the operator uses LIKE, wildcard characters "%" and "_" that are present inside the <other> expression will behave like wildcards as well. For literal string values, the ColumnOperators.iendswith.autoescape flag may be set to True to apply escaping to occurrences of these characters within the string value so that they match as themselves and not as wildcard characters. Alternatively, the ColumnOperators.iendswith.escape parameter will establish a given character as an escape character which can be of use when the target expression is not a literal string.

other¶ – expression to be compared. This is usually a plain string value, but can also be an arbitrary SQL expression. LIKE wildcard characters % and _ are not escaped by default unless the ColumnOperators.iendswith.autoescape flag is set to True.

boolean; when True, establishes an escape character within the LIKE expression, then applies it to all occurrences of "%", "_" and the escape character itself within the comparison value, which is assumed to be a literal string and not a SQL expression.

An expression such as:

With the value of :param as "foo/%bar".

a character which when given will render with the ESCAPE keyword to establish that character as the escape character. This character can then be placed preceding occurrences of % and _ to allow them to act as themselves and not wildcard characters.

An expression such as:

The parameter may also be combined with ColumnOperators.iendswith.autoescape:

Where above, the given literal parameter will be converted to "foo^%bar^^bat" before being passed to the database.

ColumnOperators.endswith()

inherited from the ColumnOperators.ilike() method of ColumnOperators

Implement the ilike operator, e.g. case insensitive LIKE.

In a column context, produces an expression either of the form:

Or on backends that support the ILIKE operator:

other¶ – expression to be compared

optional escape character, renders the ESCAPE keyword, e.g.:

ColumnOperators.like()

inherited from the ColumnOperators.in_() method of ColumnOperators

Implement the in operator.

In a column context, produces the clause column IN <other>.

The given parameter other may be:

A list of literal values, e.g.:

In this calling form, the list of items is converted to a set of bound parameters the same length as the list given:

A list of tuples may be provided if the comparison is against a tuple_() containing multiple expressions:

In this calling form, the expression renders an “empty set” expression. These expressions are tailored to individual backends and are generally trying to get an empty SELECT statement as a subquery. Such as on SQLite, the expression is:

Changed in version 1.4: empty IN expressions now use an execution-time generated SELECT subquery in all cases.

A bound parameter, e.g. bindparam(), may be used if it includes the bindparam.expanding flag:

In this calling form, the expression renders a special non-SQL placeholder expression that looks like:

This placeholder expression is intercepted at statement execution time to be converted into the variable number of bound parameter form illustrated earlier. If the statement were executed as:

The database would be passed a bound parameter for each value:

Added in version 1.2: added “expanding” bound parameters

If an empty list is passed, a special “empty list” expression, which is specific to the database in use, is rendered. On SQLite this would be:

Added in version 1.3: “expanding” bound parameters now support empty lists

a select() construct, which is usually a correlated scalar select:

In this calling form, ColumnOperators.in_() renders as given:

other¶ – a list of literals, a select() construct, or a bindparam() construct that includes the bindparam.expanding flag set to True.

The value of the Column.index parameter.

Does not indicate if this Column is actually indexed or not; use Table.indexes.

inherited from the SchemaItem.info attribute of SchemaItem

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

The dictionary is automatically generated when first accessed. It can also be specified in the constructor of some objects, such as Table and Column.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

inherited from the ColumnOperators.is_() method of ColumnOperators

Implement the IS operator.

Normally, IS is generated automatically when comparing to a value of None, which resolves to NULL. However, explicit usage of IS may be desirable if comparing to boolean values on certain platforms.

ColumnOperators.is_not()

inherited from the ColumnOperators.is_distinct_from() method of ColumnOperators

Implement the IS DISTINCT FROM operator.

Renders “a IS DISTINCT FROM b” on most platforms; on some such as SQLite may render “a IS NOT b”.

inherited from the ColumnOperators.is_not() method of ColumnOperators

Implement the IS NOT operator.

Normally, IS NOT is generated automatically when comparing to a value of None, which resolves to NULL. However, explicit usage of IS NOT may be desirable if comparing to boolean values on certain platforms.

Changed in version 1.4: The is_not() operator is renamed from isnot() in previous releases. The previous name remains available for backwards compatibility.

ColumnOperators.is_()

inherited from the ColumnOperators.is_not_distinct_from() method of ColumnOperators

Implement the IS NOT DISTINCT FROM operator.

Renders “a IS NOT DISTINCT FROM b” on most platforms; on some such as SQLite may render “a IS b”.

Changed in version 1.4: The is_not_distinct_from() operator is renamed from isnot_distinct_from() in previous releases. The previous name remains available for backwards compatibility.

inherited from the ColumnOperators.isnot() method of ColumnOperators

Implement the IS NOT operator.

Normally, IS NOT is generated automatically when comparing to a value of None, which resolves to NULL. However, explicit usage of IS NOT may be desirable if comparing to boolean values on certain platforms.

Changed in version 1.4: The is_not() operator is renamed from isnot() in previous releases. The previous name remains available for backwards compatibility.

ColumnOperators.is_()

inherited from the ColumnOperators.isnot_distinct_from() method of ColumnOperators

Implement the IS NOT DISTINCT FROM operator.

Renders “a IS NOT DISTINCT FROM b” on most platforms; on some such as SQLite may render “a IS b”.

Changed in version 1.4: The is_not_distinct_from() operator is renamed from isnot_distinct_from() in previous releases. The previous name remains available for backwards compatibility.

inherited from the ColumnOperators.istartswith() method of ColumnOperators

Implement the istartswith operator, e.g. case insensitive version of ColumnOperators.startswith().

Produces a LIKE expression that tests against an insensitive match for the start of a string value:

Since the operator uses LIKE, wildcard characters "%" and "_" that are present inside the <other> expression will behave like wildcards as well. For literal string values, the ColumnOperators.istartswith.autoescape flag may be set to True to apply escaping to occurrences of these characters within the string value so that they match as themselves and not as wildcard characters. Alternatively, the ColumnOperators.istartswith.escape parameter will establish a given character as an escape character which can be of use when the target expression is not a literal string.

other¶ – expression to be compared. This is usually a plain string value, but can also be an arbitrary SQL expression. LIKE wildcard characters % and _ are not escaped by default unless the ColumnOperators.istartswith.autoescape flag is set to True.

boolean; when True, establishes an escape character within the LIKE expression, then applies it to all occurrences of "%", "_" and the escape character itself within the comparison value, which is assumed to be a literal string and not a SQL expression.

An expression such as:

With the value of :param as "foo/%bar".

a character which when given will render with the ESCAPE keyword to establish that character as the escape character. This character can then be placed preceding occurrences of % and _ to allow them to act as themselves and not wildcard characters.

An expression such as:

The parameter may also be combined with ColumnOperators.istartswith.autoescape:

Where above, the given literal parameter will be converted to "foo^%bar^^bat" before being passed to the database.

ColumnOperators.startswith()

inherited from the ColumnElement.key attribute of ColumnElement

The ‘key’ that in some circumstances refers to this object in a Python namespace.

This typically refers to the “key” of the column as present in the .c collection of a selectable, e.g. sometable.c["somekey"] would return a Column with a .key of “somekey”.

A synonym for DialectKWArgs.dialect_kwargs.

inherited from the ColumnElement.label() method of ColumnElement

Produce a column label, i.e. <columnname> AS <name>.

This is a shortcut to the label() function.

If ‘name’ is None, an anonymous label name will be generated.

inherited from the ColumnOperators.like() method of ColumnOperators

Implement the like operator.

In a column context, produces the expression:

other¶ – expression to be compared

optional escape character, renders the ESCAPE keyword, e.g.:

ColumnOperators.ilike()

inherited from the ColumnOperators.match() method of ColumnOperators

Implements a database-specific ‘match’ operator.

ColumnOperators.match() attempts to resolve to a MATCH-like function or operator provided by the backend. Examples include:

PostgreSQL - renders x @@ plainto_tsquery(y)

Changed in version 2.0: plainto_tsquery() is used instead of to_tsquery() for PostgreSQL now; for compatibility with other forms, see Full Text Search.

MySQL - renders MATCH (x) AGAINST (y IN BOOLEAN MODE)

match - MySQL specific construct with additional features.

Oracle Database - renders CONTAINS(x, y)

other backends may provide special implementations.

Backends without any special implementation will emit the operator as “MATCH”. This is compatible with SQLite, for example.

inherited from the ColumnOperators.not_ilike() method of ColumnOperators

implement the NOT ILIKE operator.

This is equivalent to using negation with ColumnOperators.ilike(), i.e. ~x.ilike(y).

Changed in version 1.4: The not_ilike() operator is renamed from notilike() in previous releases. The previous name remains available for backwards compatibility.

ColumnOperators.ilike()

inherited from the ColumnOperators.not_in() method of ColumnOperators

implement the NOT IN operator.

This is equivalent to using negation with ColumnOperators.in_(), i.e. ~x.in_(y).

In the case that other is an empty sequence, the compiler produces an “empty not in” expression. This defaults to the expression “1 = 1” to produce true in all cases. The create_engine.empty_in_strategy may be used to alter this behavior.

Changed in version 1.4: The not_in() operator is renamed from notin_() in previous releases. The previous name remains available for backwards compatibility.

Changed in version 1.2: The ColumnOperators.in_() and ColumnOperators.not_in() operators now produce a “static” expression for an empty IN sequence by default.

ColumnOperators.in_()

inherited from the ColumnOperators.not_like() method of ColumnOperators

implement the NOT LIKE operator.

This is equivalent to using negation with ColumnOperators.like(), i.e. ~x.like(y).

Changed in version 1.4: The not_like() operator is renamed from notlike() in previous releases. The previous name remains available for backwards compatibility.

ColumnOperators.like()

inherited from the ColumnOperators.notilike() method of ColumnOperators

implement the NOT ILIKE operator.

This is equivalent to using negation with ColumnOperators.ilike(), i.e. ~x.ilike(y).

Changed in version 1.4: The not_ilike() operator is renamed from notilike() in previous releases. The previous name remains available for backwards compatibility.

ColumnOperators.ilike()

inherited from the ColumnOperators.notin_() method of ColumnOperators

implement the NOT IN operator.

This is equivalent to using negation with ColumnOperators.in_(), i.e. ~x.in_(y).

In the case that other is an empty sequence, the compiler produces an “empty not in” expression. This defaults to the expression “1 = 1” to produce true in all cases. The create_engine.empty_in_strategy may be used to alter this behavior.

Changed in version 1.4: The not_in() operator is renamed from notin_() in previous releases. The previous name remains available for backwards compatibility.

Changed in version 1.2: The ColumnOperators.in_() and ColumnOperators.not_in() operators now produce a “static” expression for an empty IN sequence by default.

ColumnOperators.in_()

inherited from the ColumnOperators.notlike() method of ColumnOperators

implement the NOT LIKE operator.

This is equivalent to using negation with ColumnOperators.like(), i.e. ~x.like(y).

Changed in version 1.4: The not_like() operator is renamed from notlike() in previous releases. The previous name remains available for backwards compatibility.

ColumnOperators.like()

inherited from the ColumnOperators.nulls_first() method of ColumnOperators

Produce a nulls_first() clause against the parent object.

Changed in version 1.4: The nulls_first() operator is renamed from nullsfirst() in previous releases. The previous name remains available for backwards compatibility.

inherited from the ColumnOperators.nulls_last() method of ColumnOperators

Produce a nulls_last() clause against the parent object.

Changed in version 1.4: The nulls_last() operator is renamed from nullslast() in previous releases. The previous name remains available for backwards compatibility.

inherited from the ColumnOperators.nullsfirst() method of ColumnOperators

Produce a nulls_first() clause against the parent object.

Changed in version 1.4: The nulls_first() operator is renamed from nullsfirst() in previous releases. The previous name remains available for backwards compatibility.

inherited from the ColumnOperators.nullslast() method of ColumnOperators

Produce a nulls_last() clause against the parent object.

Changed in version 1.4: The nulls_last() operator is renamed from nullslast() in previous releases. The previous name remains available for backwards compatibility.

inherited from the Operators.op() method of Operators

Produce a generic operator function.

This function can also be used to make bitwise operators explicit. For example:

is a bitwise AND of the value in somecolumn.

opstring¶ – a string which will be output as the infix operator between this element and the expression passed to the generated function.

precedence which the database is expected to apply to the operator in SQL expressions. This integer value acts as a hint for the SQL compiler to know when explicit parenthesis should be rendered around a particular operation. A lower number will cause the expression to be parenthesized when applied against another operator with higher precedence. The default value of 0 is lower than all operators except for the comma (,) and AS operators. A value of 100 will be higher or equal to all operators, and -100 will be lower than or equal to all operators.

I’m using op() to generate a custom operator and my parenthesis are not coming out correctly - detailed description of how the SQLAlchemy SQL compiler renders parenthesis

legacy; if True, the operator will be considered as a “comparison” operator, that is which evaluates to a boolean true/false value, like ==, >, etc. This flag is provided so that ORM relationships can establish that the operator is a comparison operator when used in a custom join condition.

Using the is_comparison parameter is superseded by using the Operators.bool_op() method instead; this more succinct operator sets this parameter automatically, but also provides correct PEP 484 typing support as the returned object will express a “boolean” datatype, i.e. BinaryExpression[bool].

return_type¶ – a TypeEngine class or object that will force the return type of an expression produced by this operator to be of that type. By default, operators that specify Operators.op.is_comparison will resolve to Boolean, and those that do not will be of the same type as the left-hand operand.

an optional Python function that can evaluate two Python values in the same way as this operator works when run on the database server. Useful for in-Python SQL expression evaluation functions, such as for ORM hybrid attributes, and the ORM “evaluator” used to match objects in a session after a multi-row update or delete.

The operator for the above expression will also work for non-SQL left and right objects:

Added in version 2.0.

Redefining and Creating New Operators

Using custom operators in join conditions

inherited from the ColumnElement.operate() method of ColumnElement

Operate on an argument.

This is the lowest level of operation, raises NotImplementedError by default.

Overriding this on a subclass can allow common behavior to be applied to all operations. For example, overriding ColumnOperators to apply func.lower() to the left and right side:

op¶ – Operator callable.

*other¶ – the ‘other’ side of the operation. Will be a single scalar for most operations.

**kwargs¶ – modifiers. These may be passed by special operators such as ColumnOperators.contains().

inherited from the Immutable.params() method of Immutable

Return a copy with bindparam() elements replaced.

Returns a copy of this ClauseElement with bindparam() elements replaced with values taken from the given dictionary:

inherited from the ColumnElement.proxy_set attribute of ColumnElement

set of all columns we are proxying

as of 2.0 this is explicitly deannotated columns. previously it was effectively deannotated columns but wasn’t enforced. annotated columns should basically not go into sets if at all possible because their hashing behavior is very non-performant.

Return True if this Column references the given column via foreign key.

inherited from the ColumnOperators.regexp_match() method of ColumnOperators

Implements a database-specific ‘regexp match’ operator.

ColumnOperators.regexp_match() attempts to resolve to a REGEXP-like function or operator provided by the backend, however the specific regular expression syntax and flags available are not backend agnostic.

PostgreSQL - renders x ~ y or x !~ y when negated.

Oracle Database - renders REGEXP_LIKE(x, y)

SQLite - uses SQLite’s REGEXP placeholder operator and calls into the Python re.match() builtin.

other backends may provide special implementations.

Backends without any special implementation will emit the operator as “REGEXP” or “NOT REGEXP”. This is compatible with SQLite and MySQL, for example.

Regular expression support is currently implemented for Oracle Database, PostgreSQL, MySQL and MariaDB. Partial support is available for SQLite. Support among third-party dialects may vary.

pattern¶ – The regular expression pattern string or column clause.

flags¶ – Any regular expression string flags to apply, passed as plain Python string only. These flags are backend specific. Some backends, like PostgreSQL and MariaDB, may alternatively specify the flags as part of the pattern. When using the ignore case flag ‘i’ in PostgreSQL, the ignore case regexp match operator ~* or !~* will be used.

Added in version 1.4.

Changed in version 1.4.48,: 2.0.18 Note that due to an implementation error, the “flags” parameter previously accepted SQL expression objects such as column expressions in addition to plain Python strings. This implementation did not work correctly with caching and was removed; strings only should be passed for the “flags” parameter, as these flags are rendered as literal inline values within SQL expressions.

ColumnOperators.regexp_replace()

inherited from the ColumnOperators.regexp_replace() method of ColumnOperators

Implements a database-specific ‘regexp replace’ operator.

ColumnOperators.regexp_replace() attempts to resolve to a REGEXP_REPLACE-like function provided by the backend, that usually emit the function REGEXP_REPLACE(). However, the specific regular expression syntax and flags available are not backend agnostic.

Regular expression replacement support is currently implemented for Oracle Database, PostgreSQL, MySQL 8 or greater and MariaDB. Support among third-party dialects may vary.

pattern¶ – The regular expression pattern string or column clause.

pattern¶ – The replacement string or column clause.

flags¶ – Any regular expression string flags to apply, passed as plain Python string only. These flags are backend specific. Some backends, like PostgreSQL and MariaDB, may alternatively specify the flags as part of the pattern.

Added in version 1.4.

Changed in version 1.4.48,: 2.0.18 Note that due to an implementation error, the “flags” parameter previously accepted SQL expression objects such as column expressions in addition to plain Python strings. This implementation did not work correctly with caching and was removed; strings only should be passed for the “flags” parameter, as these flags are rendered as literal inline values within SQL expressions.

ColumnOperators.regexp_match()

inherited from the ColumnElement.reverse_operate() method of ColumnElement

Reverse operate on an argument.

Usage is the same as operate().

inherited from the ColumnElement.self_group() method of ColumnElement

Apply a ‘grouping’ to this ClauseElement.

This method is overridden by subclasses to return a “grouping” construct, i.e. parenthesis. In particular it’s used by “binary” expressions to provide a grouping around themselves when placed into a larger expression, as well as by select() constructs when placed into the FROM clause of another select(). (Note that subqueries should be normally created using the Select.alias() method, as many platforms require nested SELECT statements to be named).

As expressions are composed together, the application of self_group() is automatic - end-user code should never need to use this method directly. Note that SQLAlchemy’s clause constructs take operator precedence into account - so parenthesis might not be needed, for example, in an expression like x OR (y AND z) - AND takes precedence over OR.

The base self_group() method of ClauseElement just returns self.

inherited from the ColumnElement.shares_lineage() method of ColumnElement

Return True if the given ColumnElement has a common ancestor to this ColumnElement.

inherited from the ColumnOperators.startswith() method of ColumnOperators

Implement the startswith operator.

Produces a LIKE expression that tests against a match for the start of a string value:

Since the operator uses LIKE, wildcard characters "%" and "_" that are present inside the <other> expression will behave like wildcards as well. For literal string values, the ColumnOperators.startswith.autoescape flag may be set to True to apply escaping to occurrences of these characters within the string value so that they match as themselves and not as wildcard characters. Alternatively, the ColumnOperators.startswith.escape parameter will establish a given character as an escape character which can be of use when the target expression is not a literal string.

other¶ – expression to be compared. This is usually a plain string value, but can also be an arbitrary SQL expression. LIKE wildcard characters % and _ are not escaped by default unless the ColumnOperators.startswith.autoescape flag is set to True.

boolean; when True, establishes an escape character within the LIKE expression, then applies it to all occurrences of "%", "_" and the escape character itself within the comparison value, which is assumed to be a literal string and not a SQL expression.

An expression such as:

With the value of :param as "foo/%bar".

a character which when given will render with the ESCAPE keyword to establish that character as the escape character. This character can then be placed preceding occurrences of % and _ to allow them to act as themselves and not wildcard characters.

An expression such as:

The parameter may also be combined with ColumnOperators.startswith.autoescape:

Where above, the given literal parameter will be converted to "foo^%bar^^bat" before being passed to the database.

ColumnOperators.endswith()

ColumnOperators.contains()

ColumnOperators.like()

inherited from the ColumnOperators.timetuple attribute of ColumnOperators

Hack, allows datetime objects to be compared on the LHS.

The value of the Column.unique parameter.

Does not indicate if this Column is actually subject to a unique constraint or not; use Table.indexes and Table.constraints.

inherited from the Immutable.unique_params() method of Immutable

Return a copy with bindparam() elements replaced.

Same functionality as ClauseElement.params(), except adds unique=True to affected bind parameters so that multiple statements can be used.

inherits from sqlalchemy.schema.HasSchemaAttr

A collection of Table objects and their associated schema constructs.

Holds a collection of Table objects as well as an optional binding to an Engine or Connection. If bound, the Table objects in the collection and their columns may participate in implicit SQL execution.

The Table objects themselves are stored in the MetaData.tables dictionary.

MetaData is a thread-safe object for read operations. Construction of new tables within a single MetaData object, either explicitly or via reflection, may not be completely thread-safe.

Describing Databases with MetaData - Introduction to database metadata

Create a new MetaData object.

Clear all Table objects from this MetaData.

Create all tables stored in this metadata.

Drop all tables stored in this metadata.

Load all available table definitions from the database.

Remove the given Table object from this MetaData.

A dictionary of Table objects keyed to their name or “table key”.

Create a new MetaData object.

The default schema to use for the Table, Sequence, and potentially other objects associated with this MetaData. Defaults to None.

Specifying a Default Schema Name with MetaData - details on how the MetaData.schema parameter is used.

quote_schema¶ – Sets the quote_schema flag for those Table, Sequence, and other objects which make usage of the local schema name.

info¶ – Optional data dictionary which will be populated into the SchemaItem.info attribute of this object.

a dictionary referring to values which will establish default naming conventions for Constraint and Index objects, for those objects which are not given a name explicitly.

The keys of this dictionary may be:

a constraint or Index class, e.g. the UniqueConstraint, ForeignKeyConstraint class, the Index class

a string mnemonic for one of the known constraint classes; "fk", "pk", "ix", "ck", "uq" for foreign key, primary key, index, check, and unique constraint, respectively.

the string name of a user-defined “token” that can be used to define new naming tokens.

The values associated with each “constraint class” or “constraint mnemonic” key are string naming templates, such as "uq_%(table_name)s_%(column_0_name)s", which describe how the name should be composed. The values associated with user-defined “token” keys should be callables of the form fn(constraint, table), which accepts the constraint/index object and Table as arguments, returning a string result.

The built-in names are as follows, some of which may only be available for certain types of constraint:

%(table_name)s - the name of the Table object associated with the constraint.

%(referred_table_name)s - the name of the Table object associated with the referencing target of a ForeignKeyConstraint.

%(column_0_name)s - the name of the Column at index position “0” within the constraint.

%(column_0N_name)s - the name of all Column objects in order within the constraint, joined without a separator.

%(column_0_N_name)s - the name of all Column objects in order within the constraint, joined with an underscore as a separator.

%(column_0_label)s, %(column_0N_label)s, %(column_0_N_label)s - the label of either the zeroth Column or all Columns, separated with or without an underscore

%(column_0_key)s, %(column_0N_key)s, %(column_0_N_key)s - the key of either the zeroth Column or all Columns, separated with or without an underscore

%(referred_column_0_name)s, %(referred_column_0N_name)s %(referred_column_0_N_name)s, %(referred_column_0_key)s, %(referred_column_0N_key)s, … column tokens which render the names/keys/labels of columns that are referenced by a ForeignKeyConstraint.

%(constraint_name)s - a special key that refers to the existing name given to the constraint. When this key is present, the Constraint object’s existing name will be replaced with one that is composed from template string that uses this token. When this token is present, it is required that the Constraint is given an explicit name ahead of time.

user-defined: any additional token may be implemented by passing it along with a fn(constraint, table) callable to the naming_convention dictionary.

Added in version 1.3.0: - added new %(column_0N_name)s, %(column_0_N_name)s, and related tokens that produce concatenations of names, keys, or labels for all columns referred to by a given constraint.

Configuring Constraint Naming Conventions - for detailed usage examples.

Clear all Table objects from this MetaData.

Create all tables stored in this metadata.

Conditional by default, will not attempt to recreate tables already present in the target database.

bind¶ – A Connection or Engine used to access the database.

tables¶ – Optional list of Table objects, which is a subset of the total tables in the MetaData (others are ignored).

checkfirst¶ – Defaults to True, don’t issue CREATEs for tables already present in the target database.

Drop all tables stored in this metadata.

Conditional by default, will not attempt to drop tables not present in the target database.

bind¶ – A Connection or Engine used to access the database.

tables¶ – Optional list of Table objects, which is a subset of the total tables in the MetaData (others are ignored).

checkfirst¶ – Defaults to True, only issue DROPs for tables confirmed to be present in the target database.

Load all available table definitions from the database.

Automatically creates Table entries in this MetaData for any table available in the database but not yet present in the MetaData. May be called multiple times to pick up tables recently added to the database, however no special action is taken if a table in this MetaData no longer exists in the database.

bind¶ – A Connection or Engine used to access the database.

schema¶ – Optional, query and reflect tables from an alternate schema. If None, the schema associated with this MetaData is used, if any.

views¶ – If True, also reflect views (materialized and plain).

Optional. Load only a sub-set of available named tables. May be specified as a sequence of names or a callable.

If a sequence of names is provided, only those tables will be reflected. An error is raised if a table is requested but not available. Named tables already present in this MetaData are ignored.

If a callable is provided, it will be used as a boolean predicate to filter the list of potential table names. The callable is called with a table name and this MetaData instance as positional arguments and should return a true value for any table to reflect.

extend_existing¶ – Passed along to each Table as Table.extend_existing.

autoload_replace¶ – Passed along to each Table as Table.autoload_replace.

if True, reflect Table objects linked to ForeignKey objects located in each Table. For MetaData.reflect(), this has the effect of reflecting related tables that might otherwise not be in the list of tables being reflected, for example if the referenced table is in a different schema or is omitted via the MetaData.reflect.only parameter. When False, ForeignKey objects are not followed to the Table in which they link, however if the related table is also part of the list of tables that would be reflected in any case, the ForeignKey object will still resolve to its related Table after the MetaData.reflect() operation is complete. Defaults to True.

Added in version 1.3.0.

**dialect_kwargs¶ – Additional keyword arguments not mentioned above are dialect specific, and passed in the form <dialectname>_<argname>. See the documentation regarding an individual dialect at Dialects for detail on documented arguments.

Reflecting Database Objects

DDLEvents.column_reflect() - Event used to customize the reflected columns. Usually used to generalize the types using TypeEngine.as_generic()

Reflecting with Database-Agnostic Types - describes how to reflect tables using general types.

Remove the given Table object from this MetaData.

Returns a list of Table objects sorted in order of foreign key dependency.

The sorting will place Table objects that have dependencies first, before the dependencies themselves, representing the order in which they can be created. To get the order in which the tables would be dropped, use the reversed() Python built-in.

The MetaData.sorted_tables attribute cannot by itself accommodate automatic resolution of dependency cycles between tables, which are usually caused by mutually dependent foreign key constraints. When these cycles are detected, the foreign keys of these tables are omitted from consideration in the sort. A warning is emitted when this condition occurs, which will be an exception raise in a future release. Tables which are not part of the cycle will still be returned in dependency order.

To resolve these cycles, the ForeignKeyConstraint.use_alter parameter may be applied to those constraints which create a cycle. Alternatively, the sort_tables_and_constraints() function will automatically return foreign key constraints in a separate collection when cycles are detected so that they may be applied to a schema separately.

Changed in version 1.3.17: - a warning is emitted when MetaData.sorted_tables cannot perform a proper sort due to cyclical dependencies. This will be an exception in a future release. Additionally, the sort will continue to return other tables not involved in the cycle in dependency order which was not the case previously.

sort_tables_and_constraints()

Inspector.get_table_names()

Inspector.get_sorted_table_and_fkc_names()

A dictionary of Table objects keyed to their name or “table key”.

The exact key is that determined by the Table.key attribute; for a table with no Table.schema attribute, this is the same as Table.name. For a table with a schema, it is typically of the form schemaname.tablename.

MetaData.sorted_tables

inherits from enum.Enum

Symbol indicating that a Table or Sequence should have ‘None’ for its schema, even if the parent MetaData has specified a schema.

Symbol indicating the “nullable” keyword was not passed to a Column.

Symbol indicating that a Table, Sequence or in some cases a ForeignKey object, in situations where the object is being copied for a Table.to_metadata() operation, should retain the schema name that it already has.

Symbol indicating that a Table or Sequence should have ‘None’ for its schema, even if the parent MetaData has specified a schema.

Symbol indicating the “nullable” keyword was not passed to a Column.

This is used to distinguish between the use case of passing nullable=None to a Column, which has special meaning on some backends such as SQL Server.

Symbol indicating that a Table, Sequence or in some cases a ForeignKey object, in situations where the object is being copied for a Table.to_metadata() operation, should retain the schema name that it already has.

inherits from sqlalchemy.sql.expression.SchemaVisitable

Base class for items that define a database schema.

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

The dictionary is automatically generated when first accessed. It can also be specified in the constructor of some objects, such as Table and Column.

Provides a surrogate Column that will act as a dedicated insert sentinel column, allowing efficient bulk inserts with deterministic RETURNING sorting for tables that don’t otherwise have qualifying primary key configurations.

Adding this column to a Table object requires that a corresponding database table actually has this column present, so if adding it to an existing model, existing database tables would need to be migrated (e.g. using ALTER TABLE or similar) to include this column.

For background on how this object is used, see the section Configuring Sentinel Columns as part of the section “Insert Many Values” Behavior for INSERT statements.

The Column returned will be a nullable integer column by default and make use of a sentinel-specific default generator used only in “insertmanyvalues” operations.

orm_insert_sentinel()

Column.insert_sentinel

“Insert Many Values” Behavior for INSERT statements

Configuring Sentinel Columns

Added in version 2.0.10.

inherits from sqlalchemy.sql.expression.DialectKWArgs, sqlalchemy.schema.HasSchemaAttr, sqlalchemy.sql.expression.TableClause, sqlalchemy.inspection.Inspectable

Represent a table in a database.

The Table object constructs a unique instance of itself based on its name and optional schema name within the given MetaData object. Calling the Table constructor with the same name and same MetaData argument a second time will return the same Table object - in this way the Table constructor acts as a registry function.

Describing Databases with MetaData - Introduction to database metadata

Constructor for Table.

add_is_dependent_on()

Add a ‘dependency’ for this Table.

Return an alias of this FromClause.

Append a Column to this Table.

Append a Constraint to this Table.

Add a new kind of dialect-specific keyword argument for this class.

A synonym for FromClause.columns

A named-based collection of ColumnElement objects maintained by this FromClause.

Compare this ClauseElement to the given ClauseElement.

Compile this SQL expression.

A collection of all Constraint objects associated with this Table.

corresponding_column()

Given a ColumnElement, return the exported ColumnElement object from the Selectable.exported_columns collection of this Selectable which corresponds to that original ColumnElement via a common ancestor column.

Issue a CREATE statement for this Table, using the given Connection or Engine for connectivity.

Generate a delete() construct against this TableClause.

A collection of keyword arguments specified as dialect-specific options to this construct.

Issue a DROP statement for this Table, using the given Connection or Engine for connectivity.

Return a namespace used for name-based access in SQL expressions.

A ColumnCollection that represents the “exported” columns of this Selectable.

Return the collection of ForeignKey marker objects which this FromClause references.

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

TableClause doesn’t support having a primary key or column -level defaults, so implicit returning doesn’t apply.

A collection of all Index objects associated with this Table.

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

Generate an Insert construct against this TableClause.

Return True if this FromClause is ‘derived’ from the given FromClause.

Return a Join from this FromClause to another FromClause.

Return a LATERAL alias of this Selectable.

Return a Join from this FromClause to another FromClause, with the “isouter” flag set to True.

Return a copy with bindparam() elements replaced.

Return the iterable collection of Column objects which comprise the primary key of this _selectable.FromClause.

Replace all occurrences of FromClause ‘old’ with the given Alias object, returning a copy of this FromClause.

Define the ‘schema’ attribute for this FromClause.

Return a SELECT of this FromClause.

Apply a ‘grouping’ to this ClauseElement.

Return a TableValuedColumn object for this FromClause.

Return a TABLESAMPLE alias of this FromClause.

Return a copy of this Table associated with a different MetaData.

Return a copy of this Table associated with a different MetaData.

Return a copy with bindparam() elements replaced.

Generate an update() construct against this TableClause.

Constructor for Table.

The name of this table as represented in the database.

The table name, along with the value of the schema parameter, forms a key which uniquely identifies this Table within the owning MetaData collection. Additional calls to Table with the same name, metadata, and schema name will return the same Table object.

Names which contain no upper case characters will be treated as case insensitive names, and will not be quoted unless they are a reserved word or contain special characters. A name with any number of upper case characters is considered to be case sensitive, and will be sent as quoted.

To enable unconditional quoting for the table name, specify the flag quote=True to the constructor, or use the quoted_name construct to specify the name.

metadata¶ – a MetaData object which will contain this table. The metadata is used as a point of association of this table with other tables which are referenced via foreign key. It also may be used to associate this table with a particular Connection or Engine.

*args¶ – Additional positional arguments are used primarily to add the list of Column objects contained within this table. Similar to the style of a CREATE TABLE statement, other SchemaItem constructs may be added here, including PrimaryKeyConstraint, and ForeignKeyConstraint.

Defaults to True; when using Table.autoload_with in conjunction with Table.extend_existing, indicates that Column objects present in the already-existing Table object should be replaced with columns of the same name retrieved from the autoload process. When False, columns already present under existing names will be omitted from the reflection process.

Note that this setting does not impact Column objects specified programmatically within the call to Table that also is autoloading; those Column objects will always replace existing columns of the same name when Table.extend_existing is True.

Table.extend_existing

An Engine or Connection object, or a Inspector object as returned by inspect() against one, with which this Table object will be reflected. When set to a non-None value, the autoload process will take place for this table against the given engine or connection.

Reflecting Database Objects

DDLEvents.column_reflect()

Reflecting with Database-Agnostic Types

When True, indicates that if this Table is already present in the given MetaData, apply further arguments within the constructor to the existing Table.

If Table.extend_existing or Table.keep_existing are not set, and the given name of the new Table refers to a Table that is already present in the target MetaData collection, and this Table specifies additional columns or other constructs or flags that modify the table’s state, an error is raised. The purpose of these two mutually-exclusive flags is to specify what action should be taken when a Table is specified that matches an existing Table, yet specifies additional constructs.

Table.extend_existing will also work in conjunction with Table.autoload_with to run a new reflection operation against the database, even if a Table of the same name is already present in the target MetaData; newly reflected Column objects and other options will be added into the state of the Table, potentially overwriting existing columns and options of the same name.

As is always the case with Table.autoload_with, Column objects can be specified in the same Table constructor, which will take precedence. Below, the existing table mytable will be augmented with Column objects both reflected from the database, as well as the given Column named “y”:

Table.autoload_replace

implicit_returning¶ –

True by default - indicates that RETURNING can be used, typically by the ORM, in order to fetch server-generated values such as primary key values and server side defaults, on those backends which support RETURNING.

In modern SQLAlchemy there is generally no reason to alter this setting, except for some backend specific cases (see Triggers in the SQL Server dialect documentation for one such example).

include_columns¶ – A list of strings indicating a subset of columns to be loaded via the autoload operation; table columns who aren’t present in this list will not be represented on the resulting Table object. Defaults to None which indicates all columns should be reflected.

Whether or not to reflect Table objects related to this one via ForeignKey objects, when Table.autoload_with is specified. Defaults to True. Set to False to disable reflection of related tables as ForeignKey objects are encountered; may be used either to save on SQL calls or to avoid issues with related tables that can’t be accessed. Note that if a related table is already present in the MetaData collection, or becomes present later, a ForeignKey object associated with this Table will resolve to that table normally.

Added in version 1.3.

MetaData.reflect.resolve_fks

info¶ – Optional data dictionary which will be populated into the SchemaItem.info attribute of this object.

When True, indicates that if this Table is already present in the given MetaData, ignore further arguments within the constructor to the existing Table, and return the Table object as originally created. This is to allow a function that wishes to define a new Table on first call, but on subsequent calls will return the same Table, without any of the declarations (particularly constraints) being applied a second time.

If Table.extend_existing or Table.keep_existing are not set, and the given name of the new Table refers to a Table that is already present in the target MetaData collection, and this Table specifies additional columns or other constructs or flags that modify the table’s state, an error is raised. The purpose of these two mutually-exclusive flags is to specify what action should be taken when a Table is specified that matches an existing Table, yet specifies additional constructs.

Table.extend_existing

A list of tuples of the form (<eventname>, <fn>) which will be passed to listen() upon construction. This alternate hook to listen() allows the establishment of a listener function specific to this Table before the “autoload” process begins. Historically this has been intended for use with the DDLEvents.column_reflect() event, however note that this event hook may now be associated with the MetaData object directly:

DDLEvents.column_reflect()

must_exist¶ – When True, indicates that this Table must already be present in the given MetaData collection, else an exception is raised.

prefixes¶ – A list of strings to insert after CREATE in the CREATE TABLE statement. They will be separated by spaces.

Force quoting of this table’s name on or off, corresponding to True or False. When left at its default of None, the column identifier will be quoted according to whether the name is case sensitive (identifiers with at least one upper case character are treated as case sensitive), or if it’s a reserved word. This flag is only needed to force quoting of a reserved word which is not known by the SQLAlchemy dialect.

setting this flag to False will not provide case-insensitive behavior for table reflection; table reflection will always search for a mixed-case name in a case sensitive fashion. Case insensitive names are specified in SQLAlchemy only by stating the name with all lower case characters.

quote_schema¶ – same as ‘quote’ but applies to the schema identifier.

The schema name for this table, which is required if the table resides in a schema other than the default selected schema for the engine’s database connection. Defaults to None.

If the owning MetaData of this Table specifies its own MetaData.schema parameter, then that schema name will be applied to this Table if the schema parameter here is set to None. To set a blank schema name on a Table that would otherwise use the schema set on the owning MetaData, specify the special symbol BLANK_SCHEMA.

The quoting rules for the schema name are the same as those for the name parameter, in that quoting is applied for reserved words or case-sensitive names; to enable unconditional quoting for the schema name, specify the flag quote_schema=True to the constructor, or use the quoted_name construct to specify the name.

Optional string that will render an SQL comment on table creation.

Added in version 1.2: Added the Table.comment parameter to Table.

**kw¶ – Additional keyword arguments not mentioned above are dialect specific, and passed in the form <dialectname>_<argname>. See the documentation regarding an individual dialect at Dialects for detail on documented arguments.

Add a ‘dependency’ for this Table.

This is another Table object which must be created first before this one can, or dropped after this one.

Usually, dependencies between tables are determined via ForeignKey objects. However, for other situations that create dependencies outside of foreign keys (rules, inheriting), this method can manually establish such a link.

inherited from the FromClause.alias() method of FromClause

Return an alias of this FromClause.

The above code creates an Alias object which can be used as a FROM clause in any SELECT statement.

Append a Column to this Table.

The “key” of the newly added Column, i.e. the value of its .key attribute, will then be available in the .c collection of this Table, and the column definition will be included in any CREATE TABLE, SELECT, UPDATE, etc. statements generated from this Table construct.

Note that this does not change the definition of the table as it exists within any underlying database, assuming that table has already been created in the database. Relational databases support the addition of columns to existing tables using the SQL ALTER command, which would need to be emitted for an already-existing table that doesn’t contain the newly added column.

When True, allows replacing existing columns. When False, the default, an warning will be raised if a column with the same .key already exists. A future version of sqlalchemy will instead rise a warning.

Added in version 1.4.0.

Append a Constraint to this Table.

This has the effect of the constraint being included in any future CREATE TABLE statement, assuming specific DDL creation events have not been associated with the given Constraint object.

Note that this does not produce the constraint within the relational database automatically, for a table that already exists in the database. To add a constraint to an existing relational database table, the SQL ALTER command must be used. SQLAlchemy also provides the AddConstraint construct which can produce this SQL when invoked as an executable clause.

inherited from the DialectKWArgs.argument_for() method of DialectKWArgs

Add a new kind of dialect-specific keyword argument for this class.

The DialectKWArgs.argument_for() method is a per-argument way adding extra arguments to the DefaultDialect.construct_arguments dictionary. This dictionary provides a list of argument names accepted by various schema-level constructs on behalf of a dialect.

New dialects should typically specify this dictionary all at once as a data member of the dialect class. The use case for ad-hoc addition of argument names is typically for end-user code that is also using a custom compilation scheme which consumes the additional arguments.

dialect_name¶ – name of a dialect. The dialect must be locatable, else a NoSuchModuleError is raised. The dialect must also include an existing DefaultDialect.construct_arguments collection, indicating that it participates in the keyword-argument validation and default system, else ArgumentError is raised. If the dialect does not include this collection, then any keyword argument can be specified on behalf of this dialect already. All dialects packaged within SQLAlchemy include this collection, however for third party dialects, support may vary.

argument_name¶ – name of the parameter.

default¶ – default value of the parameter.

Returns the Column object which currently represents the “auto increment” column, if any, else returns None.

This is based on the rules for Column as defined by the Column.autoincrement parameter, which generally means the column within a single integer column primary key constraint that is not constrained by a foreign key. If the table does not have such a primary key constraint, then there’s no “autoincrement” column. A Table may have only one column defined as the “autoincrement” column.

Added in version 2.0.4.

inherited from the FromClause.c attribute of FromClause

A synonym for FromClause.columns

inherited from the FromClause.columns attribute of FromClause

A named-based collection of ColumnElement objects maintained by this FromClause.

The columns, or c collection, is the gateway to the construction of SQL expressions using table-bound or other selectable-bound columns:

a ColumnCollection object.

inherited from the ClauseElement.compare() method of ClauseElement

Compare this ClauseElement to the given ClauseElement.

Subclasses should override the default behavior, which is a straight identity comparison.

**kw are arguments consumed by subclass compare() methods and may be used to modify the criteria for comparison (see ColumnElement).

inherited from the CompilerElement.compile() method of CompilerElement

Compile this SQL expression.

The return value is a Compiled object. Calling str() or unicode() on the returned value will yield a string representation of the result. The Compiled object also can return a dictionary of bind parameter names and values using the params accessor.

bind¶ – An Connection or Engine which can provide a Dialect in order to generate a Compiled object. If the bind and dialect parameters are both omitted, a default SQL compiler is used.

column_keys¶ – Used for INSERT and UPDATE statements, a list of column names which should be present in the VALUES clause of the compiled statement. If None, all columns from the target table object are rendered.

dialect¶ – A Dialect instance which can generate a Compiled object. This argument takes precedence over the bind argument.

optional dictionary of additional parameters that will be passed through to the compiler within all “visit” methods. This allows any custom flag to be passed through to a custom compilation construct, for example. It is also used for the case of passing the literal_binds flag through:

How do I render SQL expressions as strings, possibly with bound parameters inlined?

A collection of all Constraint objects associated with this Table.

Includes PrimaryKeyConstraint, ForeignKeyConstraint, UniqueConstraint, CheckConstraint. A separate collection Table.foreign_key_constraints refers to the collection of all ForeignKeyConstraint objects, and the Table.primary_key attribute refers to the single PrimaryKeyConstraint associated with the Table.

Table.foreign_key_constraints

inherited from the Selectable.corresponding_column() method of Selectable

Given a ColumnElement, return the exported ColumnElement object from the Selectable.exported_columns collection of this Selectable which corresponds to that original ColumnElement via a common ancestor column.

column¶ – the target ColumnElement to be matched.

require_embedded¶ – only return corresponding columns for the given ColumnElement, if the given ColumnElement is actually present within a sub-element of this Selectable. Normally the column will match if it merely shares a common ancestor with one of the exported columns of this Selectable.

Selectable.exported_columns - the ColumnCollection that is used for the operation.

ColumnCollection.corresponding_column() - implementation method.

Issue a CREATE statement for this Table, using the given Connection or Engine for connectivity.

MetaData.create_all().

inherited from the TableClause.delete() method of TableClause

Generate a delete() construct against this TableClause.

See delete() for argument and usage information.

inherited from the TableClause.description attribute of TableClause

A collection of keyword arguments specified as dialect-specific options to this construct.

The arguments are present here in their original <dialect>_<kwarg> format. Only arguments that were actually passed are included; unlike the DialectKWArgs.dialect_options collection, which contains all options known by this dialect including defaults.

The collection is also writable; keys are accepted of the form <dialect>_<kwarg> where the value will be assembled into the list of options.

DialectKWArgs.dialect_options - nested dictionary form

inherited from the DialectKWArgs.dialect_options attribute of DialectKWArgs

A collection of keyword arguments specified as dialect-specific options to this construct.

This is a two-level nested registry, keyed to <dialect_name> and <argument_name>. For example, the postgresql_where argument would be locatable as:

Added in version 0.9.2.

DialectKWArgs.dialect_kwargs - flat dictionary form

Issue a DROP statement for this Table, using the given Connection or Engine for connectivity.

inherited from the FromClause.entity_namespace attribute of FromClause

Return a namespace used for name-based access in SQL expressions.

This is the namespace that is used to resolve “filter_by()” type expressions, such as:

It defaults to the .c collection, however internally it can be overridden using the “entity_namespace” annotation to deliver alternative results.

inherited from the FromClause.exported_columns attribute of FromClause

A ColumnCollection that represents the “exported” columns of this Selectable.

The “exported” columns for a FromClause object are synonymous with the FromClause.columns collection.

Added in version 1.4.

Selectable.exported_columns

SelectBase.exported_columns

ForeignKeyConstraint objects referred to by this Table.

This list is produced from the collection of ForeignKey objects currently associated.

inherited from the FromClause.foreign_keys attribute of FromClause

Return the collection of ForeignKey marker objects which this FromClause references.

Each ForeignKey is a member of a Table-wide ForeignKeyConstraint.

Table.foreign_key_constraints

inherited from the HasTraverseInternals.get_children() method of HasTraverseInternals

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

This is used for visit traversal.

**kw may contain flags that change the collection that is returned, for example to return a subset of items in order to cut down on larger traversals, or to return child items from a different context (such as schema-level collections instead of clause-level).

inherited from the TableClause.implicit_returning attribute of TableClause

TableClause doesn’t support having a primary key or column -level defaults, so implicit returning doesn’t apply.

A collection of all Index objects associated with this Table.

Inspector.get_indexes()

inherited from the SchemaItem.info attribute of SchemaItem

Info dictionary associated with the object, allowing user-defined data to be associated with this SchemaItem.

The dictionary is automatically generated when first accessed. It can also be specified in the constructor of some objects, such as Table and Column.

inherited from the HasCacheKey.inherit_cache attribute of HasCacheKey

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

inherited from the TableClause.insert() method of TableClause

Generate an Insert construct against this TableClause.

See insert() for argument and usage information.

inherited from the FromClause.is_derived_from() method of FromClause

Return True if this FromClause is ‘derived’ from the given FromClause.

An example would be an Alias of a Table is derived from that Table.

inherited from the FromClause.join() method of FromClause

Return a Join from this FromClause to another FromClause.

would emit SQL along the lines of:

right¶ – the right side of the join; this is any FromClause object such as a Table object, and may also be a selectable-compatible object such as an ORM-mapped class.

onclause¶ – a SQL expression representing the ON clause of the join. If left at None, FromClause.join() will attempt to join the two tables based on a foreign key relationship.

isouter¶ – if True, render a LEFT OUTER JOIN, instead of JOIN.

full¶ – if True, render a FULL OUTER JOIN, instead of LEFT OUTER JOIN. Implies FromClause.join.isouter.

join() - standalone function

Join - the type of object produced

Return the ‘key’ for this Table.

This value is used as the dictionary key within the MetaData.tables collection. It is typically the same as that of Table.name for a table with no Table.schema set; otherwise it is typically of the form schemaname.tablename.

A synonym for DialectKWArgs.dialect_kwargs.

inherited from the Selectable.lateral() method of Selectable

Return a LATERAL alias of this Selectable.

The return value is the Lateral construct also provided by the top-level lateral() function.

LATERAL correlation - overview of usage.

inherited from the FromClause.outerjoin() method of FromClause

Return a Join from this FromClause to another FromClause, with the “isouter” flag set to True.

The above is equivalent to:

right¶ – the right side of the join; this is any FromClause object such as a Table object, and may also be a selectable-compatible object such as an ORM-mapped class.

onclause¶ – a SQL expression representing the ON clause of the join. If left at None, FromClause.join() will attempt to join the two tables based on a foreign key relationship.

full¶ – if True, render a FULL OUTER JOIN, instead of LEFT OUTER JOIN.

inherited from the Immutable.params() method of Immutable

Return a copy with bindparam() elements replaced.

Returns a copy of this ClauseElement with bindparam() elements replaced with values taken from the given dictionary:

inherited from the FromClause.primary_key attribute of FromClause

Return the iterable collection of Column objects which comprise the primary key of this _selectable.FromClause.

For a Table object, this collection is represented by the PrimaryKeyConstraint which itself is an iterable collection of Column objects.

inherited from the Selectable.replace_selectable() method of Selectable

Replace all occurrences of FromClause ‘old’ with the given Alias object, returning a copy of this FromClause.

Deprecated since version 1.4: The Selectable.replace_selectable() method is deprecated, and will be removed in a future release. Similar functionality is available via the sqlalchemy.sql.visitors module.

inherited from the FromClause.schema attribute of FromClause

Define the ‘schema’ attribute for this FromClause.

This is typically None for most objects except that of Table, where it is taken as the value of the Table.schema argument.

inherited from the FromClause.select() method of FromClause

Return a SELECT of this FromClause.

select() - general purpose method which allows for arbitrary column lists.

inherited from the ClauseElement.self_group() method of ClauseElement

Apply a ‘grouping’ to this ClauseElement.

This method is overridden by subclasses to return a “grouping” construct, i.e. parenthesis. In particular it’s used by “binary” expressions to provide a grouping around themselves when placed into a larger expression, as well as by select() constructs when placed into the FROM clause of another select(). (Note that subqueries should be normally created using the Select.alias() method, as many platforms require nested SELECT statements to be named).

As expressions are composed together, the application of self_group() is automatic - end-user code should never need to use this method directly. Note that SQLAlchemy’s clause constructs take operator precedence into account - so parenthesis might not be needed, for example, in an expression like x OR (y AND z) - AND takes precedence over OR.

The base self_group() method of ClauseElement just returns self.

inherited from the NamedFromClause.table_valued() method of NamedFromClause

Return a TableValuedColumn object for this FromClause.

A TableValuedColumn is a ColumnElement that represents a complete row in a table. Support for this construct is backend dependent, and is supported in various forms by backends such as PostgreSQL, Oracle Database and SQL Server.

Added in version 1.4.0b2.

Working with SQL Functions - in the SQLAlchemy Unified Tutorial

inherited from the FromClause.tablesample() method of FromClause

Return a TABLESAMPLE alias of this FromClause.

The return value is the TableSample construct also provided by the top-level tablesample() function.

tablesample() - usage guidelines and parameters

Return a copy of this Table associated with a different MetaData.

Changed in version 1.4: The Table.to_metadata() function was renamed from Table.tometadata().

metadata¶ – Target MetaData object, into which the new Table object will be created.

optional string name indicating the target schema. Defaults to the special symbol RETAIN_SCHEMA which indicates that no change to the schema name should be made in the new Table. If set to a string name, the new Table will have this new name as the .schema. If set to None, the schema will be set to that of the schema set on the target MetaData, which is typically None as well, unless set explicitly:

referred_schema_fn¶ –

optional callable which can be supplied in order to provide for the schema name that should be assigned to the referenced table of a ForeignKeyConstraint. The callable accepts this parent Table, the target schema that we are changing to, the ForeignKeyConstraint object, and the existing “target schema” of that constraint. The function should return the string schema name that should be applied. To reset the schema to “none”, return the symbol BLANK_SCHEMA. To effect no change, return None or RETAIN_SCHEMA.

Changed in version 1.4.33: The referred_schema_fn function may return the BLANK_SCHEMA or RETAIN_SCHEMA symbols.

name¶ – optional string name indicating the target table name. If not specified or None, the table name is retained. This allows a Table to be copied to the same MetaData target with a new name.

Return a copy of this Table associated with a different MetaData.

Deprecated since version 1.4: Table.tometadata() is renamed to Table.to_metadata()

See Table.to_metadata() for a full description.

inherited from the Immutable.unique_params() method of Immutable

Return a copy with bindparam() elements replaced.

Same functionality as ClauseElement.params(), except adds unique=True to affected bind parameters so that multiple statements can be used.

inherited from the TableClause.update() method of TableClause

Generate an update() construct against this TableClause.

See update() for argument and usage information.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from sqlalchemy import MetaData

metadata_obj = MetaData()
```

Example 2 (python):
```python
from sqlalchemy import Table, Column, Integer, String

user = Table(
    "user",
    metadata_obj,
    Column("user_id", Integer, primary_key=True),
    Column("user_name", String(16), nullable=False),
    Column("email_address", String(60)),
    Column("nickname", String(50), nullable=False),
)
```

Example 3 (python):
```python
>>> for t in metadata_obj.sorted_tables:
...     print(t.name)
user
user_preference
invoice
invoice_item
```

Example 4 (unknown):
```unknown
employees = Table(
    "employees",
    metadata_obj,
    Column("employee_id", Integer, primary_key=True),
    Column("employee_name", String(60), nullable=False),
    Column("employee_dept", Integer, ForeignKey("departments.department_id")),
)
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/mapper_config.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- ORM Mapped Class Configuration¶

Home | Download this Documentation

Home | Download this Documentation

Detailed reference for ORM configuration, not including relationships, which are detailed at Relationship Configuration.

For a quick look at a typical ORM configuration, start with ORM Quick Start.

For an introduction to the concept of object relational mapping as implemented in SQLAlchemy, it’s first introduced in the SQLAlchemy Unified Tutorial at Using ORM Declarative Forms to Define Table Metadata.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Unified Tutorial
    - Project Versions
- Data Manipulation with the ORM¶
- Inserting Rows using the ORM Unit of Work pattern¶
  - Instances of Classes represent Rows¶
  - Adding objects to a Session¶
  - Flushing¶
  - Autogenerated primary key attributes¶

Home | Download this Documentation

Home | Download this Documentation

SQLAlchemy 1.4 / 2.0 Tutorial

This page is part of the SQLAlchemy Unified Tutorial.

Previous: Working with Data | Next: Working with ORM Related Objects

The previous section Working with Data remained focused on the SQL Expression Language from a Core perspective, in order to provide continuity across the major SQL statement constructs. This section will then build out the lifecycle of the Session and how it interacts with these constructs.

Prerequisite Sections - the ORM focused part of the tutorial builds upon two previous ORM-centric sections in this document:

Executing with an ORM Session - introduces how to make an ORM Session object

Using ORM Declarative Forms to Define Table Metadata - where we set up our ORM mappings of the User and Address entities

Selecting ORM Entities and Columns - a few examples on how to run SELECT statements for entities like User

When using the ORM, the Session object is responsible for constructing Insert constructs and emitting them as INSERT statements within the ongoing transaction. The way we instruct the Session to do so is by adding object entries to it; the Session then makes sure these new entries will be emitted to the database when they are needed, using a process known as a flush. The overall process used by the Session to persist objects is known as the unit of work pattern.

Whereas in the previous example we emitted an INSERT using Python dictionaries to indicate the data we wanted to add, with the ORM we make direct use of the custom Python classes we defined, back at Using ORM Declarative Forms to Define Table Metadata. At the class level, the User and Address classes served as a place to define what the corresponding database tables should look like. These classes also serve as extensible data objects that we use to create and manipulate rows within a transaction as well. Below we will create two User objects each representing a potential database row to be INSERTed:

We are able to construct these objects using the names of the mapped columns as keyword arguments in the constructor. This is possible as the User class includes an automatically generated __init__() constructor that was provided by the ORM mapping so that we could create each object using column names as keys in the constructor.

In a similar manner as in our Core examples of Insert, we did not include a primary key (i.e. an entry for the id column), since we would like to make use of the auto-incrementing primary key feature of the database, SQLite in this case, which the ORM also integrates with. The value of the id attribute on the above objects, if we were to view it, displays itself as None:

The None value is provided by SQLAlchemy to indicate that the attribute has no value as of yet. SQLAlchemy-mapped attributes always return a value in Python and don’t raise AttributeError if they’re missing, when dealing with a new object that has not had a value assigned.

At the moment, our two objects above are said to be in a state called transient - they are not associated with any database state and are yet to be associated with a Session object that can generate INSERT statements for them.

To illustrate the addition process step by step, we will create a Session without using a context manager (and hence we must make sure we close it later!):

The objects are then added to the Session using the Session.add() method. When this is called, the objects are in a state known as pending and have not been inserted yet:

When we have pending objects, we can see this state by looking at a collection on the Session called Session.new:

The above view is using a collection called IdentitySet that is essentially a Python set that hashes on object identity in all cases (i.e., using Python built-in id() function, rather than the Python hash() function).

The Session makes use of a pattern known as unit of work. This generally means it accumulates changes one at a time, but does not actually communicate them to the database until needed. This allows it to make better decisions about how SQL DML should be emitted in the transaction based on a given set of pending changes. When it does emit SQL to the database to push out the current set of changes, the process is known as a flush.

We can illustrate the flush process manually by calling the Session.flush() method:

Above we observe the Session was first called upon to emit SQL, so it created a new transaction and emitted the appropriate INSERT statements for the two objects. The transaction now remains open until we call any of the Session.commit(), Session.rollback(), or Session.close() methods of Session.

While Session.flush() may be used to manually push out pending changes to the current transaction, it is usually unnecessary as the Session features a behavior known as autoflush, which we will illustrate later. It also flushes out changes whenever Session.commit() is called.

Once the rows are inserted, the two Python objects we’ve created are in a state known as persistent, where they are associated with the Session object in which they were added or loaded, and feature lots of other behaviors that will be covered later.

Another effect of the INSERT that occurred was that the ORM has retrieved the new primary key identifiers for each new object; internally it normally uses the same CursorResult.inserted_primary_key accessor we introduced previously. The squidward and krabs objects now have these new primary key identifiers associated with them and we can view them by accessing the id attribute:

Why did the ORM emit two separate INSERT statements when it could have used executemany? As we’ll see in the next section, the Session when flushing objects always needs to know the primary key of newly inserted objects. If a feature such as SQLite’s autoincrement is used (other examples include PostgreSQL IDENTITY or SERIAL, using sequences, etc.), the CursorResult.inserted_primary_key feature usually requires that each INSERT is emitted one row at a time. If we had provided values for the primary keys ahead of time, the ORM would have been able to optimize the operation better. Some database backends such as psycopg2 can also INSERT many rows at once while still being able to retrieve the primary key values.

The primary key identity of the objects are significant to the Session, as the objects are now linked to this identity in memory using a feature known as the identity map. The identity map is an in-memory store that links all objects currently loaded in memory to their primary key identity. We can observe this by retrieving one of the above objects using the Session.get() method, which will return an entry from the identity map if locally present, otherwise emitting a SELECT:

The important thing to note about the identity map is that it maintains a unique instance of a particular Python object per a particular database identity, within the scope of a particular Session object. We may observe that the some_squidward refers to the same object as that of squidward previously:

The identity map is a critical feature that allows complex sets of objects to be manipulated within a transaction without things getting out of sync.

There’s much more to say about how the Session works which will be discussed further. For now we will commit the transaction so that we can build up knowledge on how to SELECT rows before examining more ORM behaviors and features:

The above operation will commit the transaction that was in progress. The objects which we’ve dealt with are still attached to the Session, which is a state they stay in until the Session is closed (which is introduced at Closing a Session).

An important thing to note is that attributes on the objects that we just worked with have been expired, meaning, when we next access any attributes on them, the Session will start a new transaction and re-load their state. This option is sometimes problematic for both performance reasons, or if one wishes to use the objects after closing the Session (which is known as the detached state), as they will not have any state and will have no Session with which to load that state, leading to “detached instance” errors. The behavior is controllable using a parameter called Session.expire_on_commit. More on this is at Closing a Session.

In the preceding section Using UPDATE and DELETE Statements, we introduced the Update construct that represents a SQL UPDATE statement. When using the ORM, there are two ways in which this construct is used. The primary way is that it is emitted automatically as part of the unit of work process used by the Session, where an UPDATE statement is emitted on a per-primary key basis corresponding to individual objects that have changes on them.

Supposing we loaded the User object for the username sandy into a transaction (also showing off the Select.filter_by() method as well as the Result.scalar_one() method):

The Python object sandy as mentioned before acts as a proxy for the row in the database, more specifically the database row in terms of the current transaction, that has the primary key identity of 2:

If we alter the attributes of this object, the Session tracks this change:

The object appears in a collection called Session.dirty, indicating the object is “dirty”:

When the Session next emits a flush, an UPDATE will be emitted that updates this value in the database. As mentioned previously, a flush occurs automatically before we emit any SELECT, using a behavior known as autoflush. We can query directly for the User.fullname column from this row and we will get our updated value back:

We can see above that we requested that the Session execute a single select() statement. However the SQL emitted shows that an UPDATE were emitted as well, which was the flush process pushing out pending changes. The sandy Python object is now no longer considered dirty:

However note we are still in a transaction and our changes have not been pushed to the database’s permanent storage. Since Sandy’s last name is in fact “Cheeks” not “Squirrel”, we will repair this mistake later when we roll back the transaction. But first we’ll make some more data changes.

Flushing- details the flush process as well as information about the Session.autoflush setting.

To round out the basic persistence operations, an individual ORM object may be marked for deletion within the unit of work process by using the Session.delete() method. Let’s load up patrick from the database:

If we mark patrick for deletion, as is the case with other operations, nothing actually happens yet until a flush proceeds:

Current ORM behavior is that patrick stays in the Session until the flush proceeds, which as mentioned before occurs if we emit a query:

Above, the SELECT we asked to emit was preceded by a DELETE, which indicated the pending deletion for patrick proceeded. There was also a SELECT against the address table, which was prompted by the ORM looking for rows in this table which may be related to the target row; this behavior is part of a behavior known as cascade, and can be tailored to work more efficiently by allowing the database to handle related rows in address automatically; the section delete has all the detail on this.

delete - describes how to tune the behavior of Session.delete() in terms of how related rows in other tables should be handled.

Beyond that, the patrick object instance now being deleted is no longer considered to be persistent within the Session, as is shown by the containment check:

However just like the UPDATEs we made to the sandy object, every change we’ve made here is local to an ongoing transaction, which won’t become permanent if we don’t commit it. As rolling the transaction back is actually more interesting at the moment, we will do that in the next section.

The unit of work techniques discussed in this section are intended to integrate dml, or INSERT/UPDATE/DELETE statements, with Python object mechanics, often involving complex graphs of inter-related objects. Once objects are added to a Session using Session.add(), the unit of work process transparently emits INSERT/UPDATE/DELETE on our behalf as attributes on our objects are created and modified.

However, the ORM Session also has the ability to process commands that allow it to emit INSERT, UPDATE and DELETE statements directly without being passed any ORM-persisted objects, instead being passed lists of values to be INSERTed, UPDATEd, or upserted, or WHERE criteria so that an UPDATE or DELETE statement that matches many rows at once can be invoked. This mode of use is of particular importance when large numbers of rows must be affected without the need to construct and manipulate mapped objects, which may be cumbersome and unnecessary for simplistic, performance-intensive tasks such as large bulk inserts.

The Bulk / Multi row features of the ORM Session make use of the insert(), update() and delete() constructs directly, and their usage resembles how they are used with SQLAlchemy Core (first introduced in this tutorial at Using INSERT Statements and Using UPDATE and DELETE Statements). When using these constructs with the ORM Session instead of a plain Connection, their construction, execution and result handling is fully integrated with the ORM.

For background and examples on using these features, see the section ORM-Enabled INSERT, UPDATE, and DELETE statements in the ORM Querying Guide.

ORM-Enabled INSERT, UPDATE, and DELETE statements - in the ORM Querying Guide

The Session has a Session.rollback() method that as expected emits a ROLLBACK on the SQL connection in progress. However, it also has an effect on the objects that are currently associated with the Session, in our previous example the Python object sandy. While we changed the .fullname of the sandy object to read "Sandy Squirrel", we want to roll back this change. Calling Session.rollback() will not only roll back the transaction but also expire all objects currently associated with this Session, which will have the effect that they will refresh themselves when next accessed using a process known as lazy loading:

To view the “expiration” process more closely, we may observe that the Python object sandy has no state left within its Python __dict__, with the exception of a special SQLAlchemy internal state object:

This is the “expired” state; accessing the attribute again will autobegin a new transaction and refresh sandy with the current database row:

We may now observe that the full database row was also populated into the __dict__ of the sandy object:

For deleted objects, when we earlier noted that patrick was no longer in the session, that object’s identity is also restored:

and of course the database data is present again as well:

Within the above sections we used a Session object outside of a Python context manager, that is, we didn’t use the with statement. That’s fine, however if we are doing things this way, it’s best that we explicitly close out the Session when we are done with it:

Closing the Session, which is what happens when we use it in a context manager as well, accomplishes the following things:

It releases all connection resources to the connection pool, cancelling out (e.g. rolling back) any transactions that were in progress.

This means that when we make use of a session to perform some read-only tasks and then close it, we don’t need to explicitly call upon Session.rollback() to make sure the transaction is rolled back; the connection pool handles this.

It expunges all objects from the Session.

This means that all the Python objects we had loaded for this Session, like sandy, patrick and squidward, are now in a state known as detached. In particular, we will note that objects that were still in an expired state, for example due to the call to Session.commit(), are now non-functional, as they don’t contain the state of a current row and are no longer associated with any database transaction in which to be refreshed:

The detached objects can be re-associated with the same, or a new Session using the Session.add() method, which will re-establish their relationship with their particular database row:

Try to avoid using objects in their detached state, if possible. When the Session is closed, clean up references to all the previously attached objects as well. For cases where detached objects are necessary, typically the immediate display of just-committed objects for a web application where the Session is closed before the view is rendered, set the Session.expire_on_commit flag to False.

SQLAlchemy 1.4 / 2.0 Tutorial

Next Tutorial Section: Working with ORM Related Objects

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (unknown):
```unknown
>>> squidward = User(name="squidward", fullname="Squidward Tentacles")
>>> krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")
```

Example 2 (rust):
```rust
>>> squidward
User(id=None, name='squidward', fullname='Squidward Tentacles')
```

Example 3 (unknown):
```unknown
>>> session = Session(engine)
```

Example 4 (unknown):
```unknown
>>> session.add(squidward)
>>> session.add(krabs)
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/core/reflection.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Core
    - Project Versions
- Reflecting Database Objects¶
- Overriding Reflected Columns¶
- Reflecting Views¶
- Reflecting All Tables at Once¶
- Reflecting Tables from Other Schemas¶
  - Interaction of Schema-qualified Reflection with the Default Schema¶

Home | Download this Documentation

Home | Download this Documentation

A Table object can be instructed to load information about itself from the corresponding database schema object already existing within the database. This process is called reflection. In the most simple case you need only specify the table name, a MetaData object, and the autoload_with argument:

The above operation will use the given engine to query the database for information about the messages table, and will then generate Column, ForeignKey, and other objects corresponding to this information as though the Table object were hand-constructed in Python.

When tables are reflected, if a given table references another one via foreign key, a second Table object is created within the MetaData object representing the connection. Below, assume the table shopping_cart_items references a table named shopping_carts. Reflecting the shopping_cart_items table has the effect such that the shopping_carts table will also be loaded:

The MetaData has an interesting “singleton-like” behavior such that if you requested both tables individually, MetaData will ensure that exactly one Table object is created for each distinct table name. The Table constructor actually returns to you the already-existing Table object if one already exists with the given name. Such as below, we can access the already generated shopping_carts table just by naming it:

Of course, it’s a good idea to use autoload_with=engine with the above table regardless. This is so that the table’s attributes will be loaded if they have not been already. The autoload operation only occurs for the table if it hasn’t already been loaded; once loaded, new calls to Table with the same name will not re-issue any reflection queries.

Individual columns can be overridden with explicit values when reflecting tables; this is handy for specifying custom datatypes, constraints such as primary keys that may not be configured within the database, etc.:

Working with Custom Types and Reflection - illustrates how the above column override technique applies to the use of custom datatypes with table reflection.

The reflection system can also reflect views. Basic usage is the same as that of a table:

Above, my_view is a Table object with Column objects representing the names and types of each column within the view “some_view”.

Usually, it’s desired to have at least a primary key constraint when reflecting a view, if not foreign keys as well. View reflection doesn’t extrapolate these constraints.

Use the “override” technique for this, specifying explicitly those columns which are part of the primary key or have foreign key constraints:

The MetaData object can also get a listing of tables and reflect the full set. This is achieved by using the reflect() method. After calling it, all located tables are present within the MetaData object’s dictionary of tables:

metadata.reflect() also provides a handy way to clear or delete all the rows in a database:

The section Specifying the Schema Name introduces the concept of table schemas, which are namespaces within a database that contain tables and other objects, and which can be specified explicitly. The “schema” for a Table object, as well as for other objects like views, indexes and sequences, can be set up using the Table.schema parameter, and also as the default schema for a MetaData object using the MetaData.schema parameter.

The use of this schema parameter directly affects where the table reflection feature will look when it is asked to reflect objects. For example, given a MetaData object configured with a default schema name “project” via its MetaData.schema parameter:

The MetaData.reflect() will then utilize that configured .schema for reflection:

The end result is that Table objects from the “project” schema will be reflected, and they will be populated as schema-qualified with that name:

Similarly, an individual Table object that includes the Table.schema parameter will also be reflected from that database schema, overriding any default schema that may have been configured on the owning MetaData collection:

Finally, the MetaData.reflect() method itself also allows a MetaData.reflect.schema parameter to be passed, so we could also load tables from the “project” schema for a default configured MetaData object:

We can call MetaData.reflect() any number of times with different MetaData.schema arguments (or none at all) to continue populating the MetaData object with more objects:

Section Best Practices Summarized

In this section, we discuss SQLAlchemy’s reflection behavior regarding tables that are visible in the “default schema” of a database session, and how these interact with SQLAlchemy directives that include the schema explicitly. As a best practice, ensure the “default” schema for a database is just a single name, and not a list of names; for tables that are part of this “default” schema and can be named without schema qualification in DDL and SQL, leave corresponding Table.schema and similar schema parameters set to their default of None.

As described at Specifying a Default Schema Name with MetaData, databases that have the concept of schemas usually also include the concept of a “default” schema. The reason for this is naturally that when one refers to table objects without a schema as is common, a schema-capable database will still consider that table to be in a “schema” somewhere. Some databases such as PostgreSQL take this concept further into the notion of a schema search path where multiple schema names can be considered in a particular database session to be “implicit”; referring to a table name that it’s any of those schemas will not require that the schema name be present (while at the same time it’s also perfectly fine if the schema name is present).

Since most relational databases therefore have the concept of a particular table object which can be referenced both in a schema-qualified way, as well as an “implicit” way where no schema is present, this presents a complexity for SQLAlchemy’s reflection feature. Reflecting a table in a schema-qualified manner will always populate its Table.schema attribute and additionally affect how this Table is organized into the MetaData.tables collection, that is, in a schema qualified manner. Conversely, reflecting the same table in a non-schema qualified manner will organize it into the MetaData.tables collection without being schema qualified. The end result is that there would be two separate Table objects in the single MetaData collection representing the same table in the actual database.

To illustrate the ramifications of this issue, consider tables from the “project” schema in the previous example, and suppose also that the “project” schema is the default schema of our database connection, or if using a database such as PostgreSQL suppose the “project” schema is set up in the PostgreSQL search_path. This would mean that the database accepts the following two SQL statements as equivalent:

This is not a problem as the table can be found in both ways. However in SQLAlchemy, it’s the identity of the Table object that determines its semantic role within a SQL statement. Based on the current decisions within SQLAlchemy, this means that if we reflect the same “messages” table in both a schema-qualified as well as a non-schema qualified manner, we get two Table objects that will not be treated as semantically equivalent:

The above issue becomes more complicated when the tables being reflected contain foreign key references to other tables. Suppose “messages” has a “project_id” column which refers to rows in another schema-local table “projects”, meaning there is a ForeignKeyConstraint object that is part of the definition of the “messages” table.

We can find ourselves in a situation where one MetaData collection may contain as many as four Table objects representing these two database tables, where one or two of the additional tables were generated by the reflection process; this is because when the reflection process encounters a foreign key constraint on a table being reflected, it branches out to reflect that referenced table as well. The decision making it uses to assign the schema to this referenced table is that SQLAlchemy will omit a default schema from the reflected ForeignKeyConstraint object if the owning Table also omits its schema name and also that these two objects are in the same schema, but will include it if it were not omitted.

The common scenario is when the reflection of a table in a schema qualified fashion then loads a related table that will also be performed in a schema qualified fashion:

The above messages_table_1 will refer to projects also in a schema qualified fashion. This “projects” table will be reflected automatically by the fact that “messages” refers to it:

if some other part of the code reflects “projects” in a non-schema qualified fashion, there are now two projects tables that are not the same:

The above confusion can cause problems within applications that use table reflection to load up application-level Table objects, as well as within migration scenarios, in particular such as when using Alembic Migrations to detect new tables and foreign key constraints.

The above behavior can be remedied by sticking to one simple practice:

Don’t include the Table.schema parameter for any Table that expects to be located in the default schema of the database.

For PostgreSQL and other databases that support a “search” path for schemas, add the following additional practice:

Keep the “search path” narrowed down to one schema only, which is the default schema.

Remote-Schema Table Introspection and PostgreSQL search_path - additional details of this behavior as regards the PostgreSQL database.

A low level interface which provides a backend-agnostic system of loading lists of schema, table, column, and constraint descriptions from a given database is also available. This is known as the “Inspector”:

Performs database schema inspection.

ReflectedCheckConstraint

Dictionary representing the reflected elements corresponding to CheckConstraint.

Dictionary representing the reflected elements corresponding to a Column object.

Represent the reflected elements of a computed column, corresponding to the Computed construct.

ReflectedForeignKeyConstraint

Dictionary representing the reflected elements corresponding to ForeignKeyConstraint.

represent the reflected IDENTITY structure of a column, corresponding to the Identity construct.

Dictionary representing the reflected elements corresponding to Index.

ReflectedPrimaryKeyConstraint

Dictionary representing the reflected elements corresponding to PrimaryKeyConstraint.

ReflectedTableComment

Dictionary representing the reflected comment corresponding to the Table.comment attribute.

ReflectedUniqueConstraint

Dictionary representing the reflected elements corresponding to UniqueConstraint.

inherits from sqlalchemy.inspection.Inspectable

Performs database schema inspection.

The Inspector acts as a proxy to the reflection methods of the Dialect, providing a consistent interface as well as caching support for previously fetched metadata.

A Inspector object is usually created via the inspect() function, which may be passed an Engine or a Connection:

Where above, the Dialect associated with the engine may opt to return an Inspector subclass that provides additional methods specific to the dialect’s target database.

Initialize a new Inspector.

reset the cache for this Inspector.

Construct a new dialect-specific Inspector object from the given engine or connection.

get_check_constraints()

Return information about check constraints in table_name.

Return information about columns in table_name.

Return information about foreign_keys in table_name.

Return information about indexes in table_name.

get_materialized_view_names()

Return all materialized view names in schema.

get_multi_check_constraints()

Return information about check constraints in all tables in the given schema.

Return information about columns in all objects in the given schema.

get_multi_foreign_keys()

Return information about foreign_keys in all tables in the given schema.

Return information about indexes in in all objects in the given schema.

get_multi_pk_constraint()

Return information about primary key constraints in all tables in the given schema.

get_multi_table_comment()

Return information about the table comment in all objects in the given schema.

get_multi_table_options()

Return a dictionary of options specified when the tables in the given schema were created.

get_multi_unique_constraints()

Return information about unique constraints in all tables in the given schema.

Return information about primary key constraint in table_name.

Return all schema names.

Return all sequence names in schema.

get_sorted_table_and_fkc_names()

Return dependency-sorted table and foreign key constraint names in referred to within a particular schema.

Return information about the table comment for table_name.

Return all table names within a particular schema.

Return a dictionary of options specified when the table of the given name was created.

get_temp_table_names()

Return a list of temporary table names for the current bind.

get_temp_view_names()

Return a list of temporary view names for the current bind.

get_unique_constraints()

Return information about unique constraints in table_name.

get_view_definition()

Return definition for the plain or materialized view called view_name.

Return all non-materialized view names in schema.

Check the existence of a particular index name in the database.

Return True if the backend has a schema with the given name.

Return True if the backend has a sequence with the given name.

Return True if the backend has a table, view, or temporary table of the given name.

Given a Table object, load its internal constructs based on introspection.

sort_tables_on_foreign_key_dependency()

Return dependency-sorted table and foreign key constraint names referred to within multiple schemas.

Initialize a new Inspector.

Deprecated since version 1.4: The __init__() method on Inspector is deprecated and will be removed in a future release. Please use the inspect() function on an Engine or Connection in order to acquire an Inspector.

bind¶ – a Connection, which is typically an instance of Engine or Connection.

For a dialect-specific instance of Inspector, see Inspector.from_engine()

reset the cache for this Inspector.

Inspection methods that have data cached will emit SQL queries when next called to get new data.

Added in version 2.0.

Return the default schema name presented by the dialect for the current engine’s database user.

E.g. this is typically public for PostgreSQL and dbo for SQL Server.

Construct a new dialect-specific Inspector object from the given engine or connection.

Deprecated since version 1.4: The from_engine() method on Inspector is deprecated and will be removed in a future release. Please use the inspect() function on an Engine or Connection in order to acquire an Inspector.

bind¶ – a Connection or Engine.

This method differs from direct a direct constructor call of Inspector in that the Dialect is given a chance to provide a dialect-specific Inspector instance, which may provide additional methods.

See the example at Inspector.

Return information about check constraints in table_name.

Given a string table_name and an optional string schema, return check constraint information as a list of ReflectedCheckConstraint.

table_name¶ – string name of the table. For special quoting, use quoted_name.

schema¶ – string schema name; if omitted, uses the default schema of the database connection. For special quoting, use quoted_name.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

a list of dictionaries, each representing the definition of a check constraints.

Inspector.get_multi_check_constraints()

Return information about columns in table_name.

Given a string table_name and an optional string schema, return column information as a list of ReflectedColumn.

table_name¶ – string name of the table. For special quoting, use quoted_name.

schema¶ – string schema name; if omitted, uses the default schema of the database connection. For special quoting, use quoted_name.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

list of dictionaries, each representing the definition of a database column.

Inspector.get_multi_columns().

Return information about foreign_keys in table_name.

Given a string table_name, and an optional string schema, return foreign key information as a list of ReflectedForeignKeyConstraint.

table_name¶ – string name of the table. For special quoting, use quoted_name.

schema¶ – string schema name; if omitted, uses the default schema of the database connection. For special quoting, use quoted_name.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

a list of dictionaries, each representing the a foreign key definition.

Inspector.get_multi_foreign_keys()

Return information about indexes in table_name.

Given a string table_name and an optional string schema, return index information as a list of ReflectedIndex.

table_name¶ – string name of the table. For special quoting, use quoted_name.

schema¶ – string schema name; if omitted, uses the default schema of the database connection. For special quoting, use quoted_name.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

a list of dictionaries, each representing the definition of an index.

Inspector.get_multi_indexes()

Return all materialized view names in schema.

schema¶ – Optional, retrieve names from a non-default schema. For special quoting, use quoted_name.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

Added in version 2.0.

Inspector.get_view_names()

Return information about check constraints in all tables in the given schema.

The tables can be filtered by passing the names to use to filter_names.

For each table the value is a list of ReflectedCheckConstraint.

schema¶ – string schema name; if omitted, uses the default schema of the database connection. For special quoting, use quoted_name.

filter_names¶ – optionally return information only for the objects listed here.

kind¶ – a ObjectKind that specifies the type of objects to reflect. Defaults to ObjectKind.TABLE.

scope¶ – a ObjectScope that specifies if constraints of default, temporary or any tables should be reflected. Defaults to ObjectScope.DEFAULT.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

a dictionary where the keys are two-tuple schema,table-name and the values are list of dictionaries, each representing the definition of a check constraints. The schema is None if no schema is provided.

Added in version 2.0.

Inspector.get_check_constraints()

Return information about columns in all objects in the given schema.

The objects can be filtered by passing the names to use to filter_names.

For each table the value is a list of ReflectedColumn.

schema¶ – string schema name; if omitted, uses the default schema of the database connection. For special quoting, use quoted_name.

filter_names¶ – optionally return information only for the objects listed here.

kind¶ – a ObjectKind that specifies the type of objects to reflect. Defaults to ObjectKind.TABLE.

scope¶ – a ObjectScope that specifies if columns of default, temporary or any tables should be reflected. Defaults to ObjectScope.DEFAULT.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

a dictionary where the keys are two-tuple schema,table-name and the values are list of dictionaries, each representing the definition of a database column. The schema is None if no schema is provided.

Added in version 2.0.

Inspector.get_columns()

Return information about foreign_keys in all tables in the given schema.

The tables can be filtered by passing the names to use to filter_names.

For each table the value is a list of ReflectedForeignKeyConstraint.

schema¶ – string schema name; if omitted, uses the default schema of the database connection. For special quoting, use quoted_name.

filter_names¶ – optionally return information only for the objects listed here.

kind¶ – a ObjectKind that specifies the type of objects to reflect. Defaults to ObjectKind.TABLE.

scope¶ – a ObjectScope that specifies if foreign keys of default, temporary or any tables should be reflected. Defaults to ObjectScope.DEFAULT.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

a dictionary where the keys are two-tuple schema,table-name and the values are list of dictionaries, each representing a foreign key definition. The schema is None if no schema is provided.

Added in version 2.0.

Inspector.get_foreign_keys()

Return information about indexes in in all objects in the given schema.

The objects can be filtered by passing the names to use to filter_names.

For each table the value is a list of ReflectedIndex.

schema¶ – string schema name; if omitted, uses the default schema of the database connection. For special quoting, use quoted_name.

filter_names¶ – optionally return information only for the objects listed here.

kind¶ – a ObjectKind that specifies the type of objects to reflect. Defaults to ObjectKind.TABLE.

scope¶ – a ObjectScope that specifies if indexes of default, temporary or any tables should be reflected. Defaults to ObjectScope.DEFAULT.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

a dictionary where the keys are two-tuple schema,table-name and the values are list of dictionaries, each representing the definition of an index. The schema is None if no schema is provided.

Added in version 2.0.

Inspector.get_indexes()

Return information about primary key constraints in all tables in the given schema.

The tables can be filtered by passing the names to use to filter_names.

For each table the value is a ReflectedPrimaryKeyConstraint.

schema¶ – string schema name; if omitted, uses the default schema of the database connection. For special quoting, use quoted_name.

filter_names¶ – optionally return information only for the objects listed here.

kind¶ – a ObjectKind that specifies the type of objects to reflect. Defaults to ObjectKind.TABLE.

scope¶ – a ObjectScope that specifies if primary keys of default, temporary or any tables should be reflected. Defaults to ObjectScope.DEFAULT.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

a dictionary where the keys are two-tuple schema,table-name and the values are dictionaries, each representing the definition of a primary key constraint. The schema is None if no schema is provided.

Added in version 2.0.

Inspector.get_pk_constraint()

Return information about the table comment in all objects in the given schema.

The objects can be filtered by passing the names to use to filter_names.

For each table the value is a ReflectedTableComment.

Raises NotImplementedError for a dialect that does not support comments.

schema¶ – string schema name; if omitted, uses the default schema of the database connection. For special quoting, use quoted_name.

filter_names¶ – optionally return information only for the objects listed here.

kind¶ – a ObjectKind that specifies the type of objects to reflect. Defaults to ObjectKind.TABLE.

scope¶ – a ObjectScope that specifies if comments of default, temporary or any tables should be reflected. Defaults to ObjectScope.DEFAULT.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

a dictionary where the keys are two-tuple schema,table-name and the values are dictionaries, representing the table comments. The schema is None if no schema is provided.

Added in version 2.0.

Inspector.get_table_comment()

Return a dictionary of options specified when the tables in the given schema were created.

The tables can be filtered by passing the names to use to filter_names.

This currently includes some options that apply to MySQL and Oracle tables.

schema¶ – string schema name; if omitted, uses the default schema of the database connection. For special quoting, use quoted_name.

filter_names¶ – optionally return information only for the objects listed here.

kind¶ – a ObjectKind that specifies the type of objects to reflect. Defaults to ObjectKind.TABLE.

scope¶ – a ObjectScope that specifies if options of default, temporary or any tables should be reflected. Defaults to ObjectScope.DEFAULT.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

a dictionary where the keys are two-tuple schema,table-name and the values are dictionaries with the table options. The returned keys in each dict depend on the dialect in use. Each one is prefixed with the dialect name. The schema is None if no schema is provided.

Added in version 2.0.

Inspector.get_table_options()

Return information about unique constraints in all tables in the given schema.

The tables can be filtered by passing the names to use to filter_names.

For each table the value is a list of ReflectedUniqueConstraint.

schema¶ – string schema name; if omitted, uses the default schema of the database connection. For special quoting, use quoted_name.

filter_names¶ – optionally return information only for the objects listed here.

kind¶ – a ObjectKind that specifies the type of objects to reflect. Defaults to ObjectKind.TABLE.

scope¶ – a ObjectScope that specifies if constraints of default, temporary or any tables should be reflected. Defaults to ObjectScope.DEFAULT.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

a dictionary where the keys are two-tuple schema,table-name and the values are list of dictionaries, each representing the definition of an unique constraint. The schema is None if no schema is provided.

Added in version 2.0.

Inspector.get_unique_constraints()

Return information about primary key constraint in table_name.

Given a string table_name, and an optional string schema, return primary key information as a ReflectedPrimaryKeyConstraint.

table_name¶ – string name of the table. For special quoting, use quoted_name.

schema¶ – string schema name; if omitted, uses the default schema of the database connection. For special quoting, use quoted_name.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

a dictionary representing the definition of a primary key constraint.

Inspector.get_multi_pk_constraint()

Return all schema names.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

Return all sequence names in schema.

schema¶ – Optional, retrieve names from a non-default schema. For special quoting, use quoted_name.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

Return dependency-sorted table and foreign key constraint names in referred to within a particular schema.

This will yield 2-tuples of (tablename, [(tname, fkname), (tname, fkname), ...]) consisting of table names in CREATE order grouped with the foreign key constraint names that are not detected as belonging to a cycle. The final element will be (None, [(tname, fkname), (tname, fkname), ..]) which will consist of remaining foreign key constraint names that would require a separate CREATE step after-the-fact, based on dependencies between tables.

schema¶ – schema name to query, if not the default schema.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

Inspector.get_table_names()

sort_tables_and_constraints() - similar method which works with an already-given MetaData.

Return information about the table comment for table_name.

Given a string table_name and an optional string schema, return table comment information as a ReflectedTableComment.

Raises NotImplementedError for a dialect that does not support comments.

table_name¶ – string name of the table. For special quoting, use quoted_name.

schema¶ – string schema name; if omitted, uses the default schema of the database connection. For special quoting, use quoted_name.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

a dictionary, with the table comment.

Added in version 1.2.

Inspector.get_multi_table_comment()

Return all table names within a particular schema.

The names are expected to be real tables only, not views. Views are instead returned using the Inspector.get_view_names() and/or Inspector.get_materialized_view_names() methods.

schema¶ – Schema name. If schema is left at None, the database’s default schema is used, else the named schema is searched. If the database does not support named schemas, behavior is undefined if schema is not passed as None. For special quoting, use quoted_name.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

Inspector.get_sorted_table_and_fkc_names()

MetaData.sorted_tables

Return a dictionary of options specified when the table of the given name was created.

This currently includes some options that apply to MySQL and Oracle Database tables.

table_name¶ – string name of the table. For special quoting, use quoted_name.

schema¶ – string schema name; if omitted, uses the default schema of the database connection. For special quoting, use quoted_name.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

a dict with the table options. The returned keys depend on the dialect in use. Each one is prefixed with the dialect name.

Inspector.get_multi_table_options()

Return a list of temporary table names for the current bind.

This method is unsupported by most dialects; currently only Oracle Database, PostgreSQL and SQLite implements it.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

Return a list of temporary view names for the current bind.

This method is unsupported by most dialects; currently only PostgreSQL and SQLite implements it.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

Return information about unique constraints in table_name.

Given a string table_name and an optional string schema, return unique constraint information as a list of ReflectedUniqueConstraint.

table_name¶ – string name of the table. For special quoting, use quoted_name.

schema¶ – string schema name; if omitted, uses the default schema of the database connection. For special quoting, use quoted_name.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

a list of dictionaries, each representing the definition of an unique constraint.

Inspector.get_multi_unique_constraints()

Return definition for the plain or materialized view called view_name.

view_name¶ – Name of the view.

schema¶ – Optional, retrieve names from a non-default schema. For special quoting, use quoted_name.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

Return all non-materialized view names in schema.

schema¶ – Optional, retrieve names from a non-default schema. For special quoting, use quoted_name.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

Changed in version 2.0: For those dialects that previously included the names of materialized views in this list (currently PostgreSQL), this method no longer returns the names of materialized views. the Inspector.get_materialized_view_names() method should be used instead.

Inspector.get_materialized_view_names()

Check the existence of a particular index name in the database.

table_name¶ – the name of the table the index belongs to

index_name¶ – the name of the index to check

schema¶ – schema name to query, if not the default schema.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

Added in version 2.0.

Return True if the backend has a schema with the given name.

schema_name¶ – name of the schema to check

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

Added in version 2.0.

Return True if the backend has a sequence with the given name.

sequence_name¶ – name of the sequence to check

schema¶ – schema name to query, if not the default schema.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

Added in version 1.4.

Return True if the backend has a table, view, or temporary table of the given name.

table_name¶ – name of the table to check

schema¶ – schema name to query, if not the default schema.

**kw¶ – Additional keyword argument to pass to the dialect specific implementation. See the documentation of the dialect in use for more information.

Added in version 1.4: - the Inspector.has_table() method replaces the Engine.has_table() method.

Changed in version 2.0::: Inspector.has_table() now formally supports checking for additional table-like objects:

any type of views (plain or materialized)

temporary tables of any kind

Previously, these two checks were not formally specified and different dialects would vary in their behavior. The dialect testing suite now includes tests for all of these object types and should be supported by all SQLAlchemy-included dialects. Support among third party dialects may be lagging, however.

Given a Table object, load its internal constructs based on introspection.

This is the underlying method used by most dialects to produce table reflection. Direct usage is like:

Changed in version 1.4: Renamed from reflecttable to reflect_table

table¶ – a Table instance.

include_columns¶ – a list of string column names to include in the reflection process. If None, all columns are reflected.

Return dependency-sorted table and foreign key constraint names referred to within multiple schemas.

This method may be compared to Inspector.get_sorted_table_and_fkc_names(), which works on one schema at a time; here, the method is a generalization that will consider multiple schemas at once including that it will resolve for cross-schema foreign keys.

Added in version 2.0.

inherits from builtins.dict

Dictionary representing the reflected elements corresponding to a Column object.

The ReflectedColumn structure is returned by the get_columns method.

database-dependent autoincrement flag.

comment for the column, if present. Only some dialects return this key

indicates that this column is computed by the database. Only some dialects return this key.

column default expression as a SQL string

Additional dialect-specific options detected for this reflected object

indicates this column is an IDENTITY column. Only some dialects return this key.

boolean flag if the column is NULL or NOT NULL

column type represented as a TypeEngine instance.

database-dependent autoincrement flag.

This flag indicates if the column has a database-side “autoincrement” flag of some kind. Within SQLAlchemy, other kinds of columns may also act as an “autoincrement” column without necessarily having such a flag on them.

See Column.autoincrement for more background on “autoincrement”.

comment for the column, if present. Only some dialects return this key

indicates that this column is computed by the database. Only some dialects return this key.

Added in version 1.3.16: - added support for computed reflection.

column default expression as a SQL string

Additional dialect-specific options detected for this reflected object

indicates this column is an IDENTITY column. Only some dialects return this key.

Added in version 1.4: - added support for identity column reflection.

boolean flag if the column is NULL or NOT NULL

column type represented as a TypeEngine instance.

inherits from builtins.dict

Represent the reflected elements of a computed column, corresponding to the Computed construct.

The ReflectedComputed structure is part of the ReflectedColumn structure, which is returned by the Inspector.get_columns() method.

indicates if the value is stored in the table or computed on demand

the expression used to generate this column returned as a string SQL expression

indicates if the value is stored in the table or computed on demand

the expression used to generate this column returned as a string SQL expression

inherits from builtins.dict

Dictionary representing the reflected elements corresponding to CheckConstraint.

The ReflectedCheckConstraint structure is returned by the Inspector.get_check_constraints() method.

Additional dialect-specific options detected for this check constraint

the check constraint’s SQL expression

Additional dialect-specific options detected for this check constraint

Added in version 1.3.8.

the check constraint’s SQL expression

inherits from builtins.dict

Dictionary representing the reflected elements corresponding to ForeignKeyConstraint.

The ReflectedForeignKeyConstraint structure is returned by the Inspector.get_foreign_keys() method.

local column names which comprise the foreign key

Additional options detected for this foreign key constraint

referred column names that correspond to constrained_columns

schema name of the table being referred

name of the table being referred

local column names which comprise the foreign key

Additional options detected for this foreign key constraint

referred column names that correspond to constrained_columns

schema name of the table being referred

name of the table being referred

inherits from builtins.dict

represent the reflected IDENTITY structure of a column, corresponding to the Identity construct.

The ReflectedIdentity structure is part of the ReflectedColumn structure, which is returned by the Inspector.get_columns() method.

type of identity column

number of future values in the sequence which are calculated in advance.

allows the sequence to wrap around when the maxvalue or minvalue has been reached.

increment value of the sequence

the maximum value of the sequence.

the minimum value of the sequence.

no maximum value of the sequence.

no minimum value of the sequence.

if true, renders the ORDER keyword.

starting index of the sequence

type of identity column

number of future values in the sequence which are calculated in advance.

allows the sequence to wrap around when the maxvalue or minvalue has been reached.

increment value of the sequence

the maximum value of the sequence.

the minimum value of the sequence.

no maximum value of the sequence.

no minimum value of the sequence.

if true, renders the ORDER keyword.

starting index of the sequence

inherits from builtins.dict

Dictionary representing the reflected elements corresponding to Index.

The ReflectedIndex structure is returned by the Inspector.get_indexes() method.

column names which the index references. An element of this list is None if it’s an expression and is returned in the expressions list.

optional dict mapping column names or expressions to tuple of sort keywords, which may include asc, desc, nulls_first, nulls_last.

Additional dialect-specific options detected for this index

duplicates_constraint

Indicates if this index mirrors a constraint with this name

Expressions that compose the index. This list, when present, contains both plain column names (that are also in column_names) and expressions (that are None in column_names).

columns to include in the INCLUDE clause for supporting databases.

whether or not the index has a unique flag

column names which the index references. An element of this list is None if it’s an expression and is returned in the expressions list.

optional dict mapping column names or expressions to tuple of sort keywords, which may include asc, desc, nulls_first, nulls_last.

Added in version 1.3.5.

Additional dialect-specific options detected for this index

Indicates if this index mirrors a constraint with this name

Expressions that compose the index. This list, when present, contains both plain column names (that are also in column_names) and expressions (that are None in column_names).

columns to include in the INCLUDE clause for supporting databases.

Deprecated since version 2.0: Legacy value, will be replaced with index_dict["dialect_options"]["<dialect name>_include"]

whether or not the index has a unique flag

inherits from builtins.dict

Dictionary representing the reflected elements corresponding to PrimaryKeyConstraint.

The ReflectedPrimaryKeyConstraint structure is returned by the Inspector.get_pk_constraint() method.

column names which comprise the primary key

Additional dialect-specific options detected for this primary key

column names which comprise the primary key

Additional dialect-specific options detected for this primary key

inherits from builtins.dict

Dictionary representing the reflected elements corresponding to UniqueConstraint.

The ReflectedUniqueConstraint structure is returned by the Inspector.get_unique_constraints() method.

column names which comprise the unique constraint

Additional dialect-specific options detected for this unique constraint

Indicates if this unique constraint duplicates an index with this name

column names which comprise the unique constraint

Additional dialect-specific options detected for this unique constraint

Indicates if this unique constraint duplicates an index with this name

inherits from builtins.dict

Dictionary representing the reflected comment corresponding to the Table.comment attribute.

The ReflectedTableComment structure is returned by the Inspector.get_table_comment() method.

When the columns of a table are reflected, using either the Table.autoload_with parameter of Table or the Inspector.get_columns() method of Inspector, the datatypes will be as specific as possible to the target database. This means that if an “integer” datatype is reflected from a MySQL database, the type will be represented by the sqlalchemy.dialects.mysql.INTEGER class, which includes MySQL-specific attributes such as “display_width”. Or on PostgreSQL, a PostgreSQL-specific datatype such as sqlalchemy.dialects.postgresql.INTERVAL or sqlalchemy.dialects.postgresql.ENUM may be returned.

There is a use case for reflection which is that a given Table is to be transferred to a different vendor database. To suit this use case, there is a technique by which these vendor-specific datatypes can be converted on the fly to be instance of SQLAlchemy backend-agnostic datatypes, for the examples above types such as Integer, Interval and Enum. This may be achieved by intercepting the column reflection using the DDLEvents.column_reflect() event in conjunction with the TypeEngine.as_generic() method.

Given a table in MySQL (chosen because MySQL has a lot of vendor-specific datatypes and options):

The above table includes MySQL-only integer types MEDIUMINT and TINYINT as well as a VARCHAR that includes the MySQL-only CHARACTER SET option. If we reflect this table normally, it produces a Table object that will contain those MySQL-specific datatypes and options:

The above example reflects the above table schema into a new Table object. We can then, for demonstration purposes, print out the MySQL-specific “CREATE TABLE” statement using the CreateTable construct:

Above, the MySQL-specific datatypes and options were maintained. If we wanted a Table that we could instead transfer cleanly to another database vendor, replacing the special datatypes sqlalchemy.dialects.mysql.MEDIUMINT and sqlalchemy.dialects.mysql.TINYINT with Integer, we can choose instead to “genericize” the datatypes on this table, or otherwise change them in any way we’d like, by establishing a handler using the DDLEvents.column_reflect() event. The custom handler will make use of the TypeEngine.as_generic() method to convert the above MySQL-specific type objects into generic ones, by replacing the "type" entry within the column dictionary entry that is passed to the event handler. The format of this dictionary is described at Inspector.get_columns():

We now get a new Table that is generic and uses Integer for those datatypes. We can now emit a “CREATE TABLE” statement for example on a PostgreSQL database:

Noting above also that SQLAlchemy will usually make a decent guess for other behaviors, such as that the MySQL AUTO_INCREMENT directive is represented in PostgreSQL most closely using the SERIAL auto-incrementing datatype.

Added in version 1.4: Added the TypeEngine.as_generic() method and additionally improved the use of the DDLEvents.column_reflect() event such that it may be applied to a MetaData object for convenience.

It’s important to note that the reflection process recreates Table metadata using only information which is represented in the relational database. This process by definition cannot restore aspects of a schema that aren’t actually stored in the database. State which is not available from reflection includes but is not limited to:

Client side defaults, either Python functions or SQL expressions defined using the default keyword of Column (note this is separate from server_default, which specifically is what’s available via reflection).

Column information, e.g. data that might have been placed into the Column.info dictionary

The value of the .quote setting for Column or Table

The association of a particular Sequence with a given Column

The relational database also in many cases reports on table metadata in a different format than what was specified in SQLAlchemy. The Table objects returned from reflection cannot be always relied upon to produce the identical DDL as the original Python-defined Table objects. Areas where this occurs includes server defaults, column-associated sequences and various idiosyncrasies regarding constraints and datatypes. Server side defaults may be returned with cast directives (typically PostgreSQL will include a ::<type> cast) or different quoting patterns than originally specified.

Another category of limitation includes schema structures for which reflection is only partially or not yet defined. Recent improvements to reflection allow things like views, indexes and foreign key options to be reflected. As of this writing, structures like CHECK constraints, table comments, and triggers are not reflected.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (json):
```json
>>> messages = Table("messages", metadata_obj, autoload_with=engine)
>>> [c.name for c in messages.columns]
['message_id', 'message_name', 'date']
```

Example 2 (unknown):
```unknown
>>> shopping_cart_items = Table("shopping_cart_items", metadata_obj, autoload_with=engine)
>>> "shopping_carts" in metadata_obj.tables
True
```

Example 3 (unknown):
```unknown
shopping_carts = Table("shopping_carts", metadata_obj)
```

Example 4 (unknown):
```unknown
>>> mytable = Table(
...     "mytable",
...     metadata_obj,
...     Column(
...         "id", Integer, primary_key=True
...     ),  # override reflected 'id' to have primary key
...     Column("mydata", Unicode(50)),  # override reflected 'mydata' to be Unicode
...     # additional Column objects which require no change are reflected normally
...     autoload_with=some_engine,
... )
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/core/type_basics.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Core
    - Project Versions
- The Type Hierarchy¶
- The “CamelCase” datatypes¶
- The “UPPERCASE” datatypes¶
- Backend-specific “UPPERCASE” datatypes¶
- Using “UPPERCASE” and Backend-specific types for multiple backends¶
- Generic “CamelCase” Types¶

Home | Download this Documentation

Home | Download this Documentation

SQLAlchemy provides abstractions for most common database data types, as well as several techniques for customization of datatypes.

Database types are represented using Python classes, all of which ultimately extend from the base type class known as TypeEngine. There are two general categories of datatypes, each of which express themselves within the typing hierarchy in different ways. The category used by an individual datatype class can be identified based on the use of two different naming conventions, which are “CamelCase” and “UPPERCASE”.

Setting up MetaData with Table objects - in the SQLAlchemy Unified Tutorial. Illustrates the most rudimental use of TypeEngine type objects to define Table metadata and introduces the concept of type objects in tutorial form.

The rudimental types have “CamelCase” names such as String, Numeric, Integer, and DateTime. All of the immediate subclasses of TypeEngine are “CamelCase” types. The “CamelCase” types are to the greatest degree possible database agnostic, meaning they can all be used on any database backend where they will behave in such a way as appropriate to that backend in order to produce the desired behavior.

An example of a straightforward “CamelCase” datatype is String. On most backends, using this datatype in a table specification will correspond to the VARCHAR database type being used on the target backend, delivering string values to and from the database, as in the example below:

When using a particular TypeEngine class in a Table definition or in any SQL expression overall, if no arguments are required it may be passed as the class itself, that is, without instantiating it with (). If arguments are needed, such as the length argument of 60 in the "email_address" column above, the type may be instantiated.

Another “CamelCase” datatype that expresses more backend-specific behavior is the Boolean datatype. Unlike String, which represents a string datatype that all databases have, not every backend has a real “boolean” datatype; some make use of integers or BIT values 0 and 1, some have boolean literal constants true and false while others dont. For this datatype, Boolean may render BOOLEAN on a backend such as PostgreSQL, BIT on the MySQL backend and SMALLINT on Oracle Database. As data is sent and received from the database using this type, based on the dialect in use it may be interpreting Python numeric or boolean values.

The typical SQLAlchemy application will likely wish to use primarily “CamelCase” types in the general case, as they will generally provide the best basic behavior and be automatically portable to all backends.

Reference for the general set of “CamelCase” datatypes is below at Generic “CamelCase” Types.

In contrast to the “CamelCase” types are the “UPPERCASE” datatypes. These datatypes are always inherited from a particular “CamelCase” datatype, and always represent an exact datatype. When using an “UPPERCASE” datatype, the name of the type is always rendered exactly as given, without regard for whether or not the current backend supports it. Therefore the use of “UPPERCASE” types in a SQLAlchemy application indicates that specific datatypes are required, which then implies that the application would normally, without additional steps taken, be limited to those backends which use the type exactly as given. Examples of UPPERCASE types include VARCHAR, NUMERIC, INTEGER, and TIMESTAMP, which inherit directly from the previously mentioned “CamelCase” types String, Numeric, Integer, and DateTime, respectively.

The “UPPERCASE” datatypes that are part of sqlalchemy.types are common SQL types that typically expect to be available on at least two backends if not more.

Reference for the general set of “UPPERCASE” datatypes is below at SQL Standard and Multiple Vendor “UPPERCASE” Types.

Most databases also have their own datatypes that are either fully specific to those databases, or add additional arguments that are specific to those databases. For these datatypes, specific SQLAlchemy dialects provide backend-specific “UPPERCASE” datatypes, for a SQL type that has no analogue on other backends. Examples of backend-specific uppercase datatypes include PostgreSQL’s JSONB, SQL Server’s IMAGE and MySQL’s TINYTEXT.

Specific backends may also include “UPPERCASE” datatypes that extend the arguments available from that same “UPPERCASE” datatype as found in the sqlalchemy.types module. An example is when creating a MySQL string datatype, one might want to specify MySQL-specific arguments such as charset or national, which are available from the MySQL version of VARCHAR as the MySQL-only parameters VARCHAR.charset and VARCHAR.national.

API documentation for backend-specific types are in the dialect-specific documentation, listed at Dialects.

Reviewing the presence of “UPPERCASE” and “CamelCase” types leads to the natural use case of how to make use of “UPPERCASE” datatypes for backend-specific options, but only when that backend is in use. To tie together the database-agnostic “CamelCase” and backend-specific “UPPERCASE” systems, one makes use of the TypeEngine.with_variant() method in order to compose types together to work with specific behaviors on specific backends.

Such as, to use the String datatype, but when running on MySQL to make use of the VARCHAR.charset parameter of VARCHAR when the table is created on MySQL or MariaDB, TypeEngine.with_variant() may be used as below:

In the above table definition, the "bio" column will have string-behaviors on all backends. On most backends it will render in DDL as VARCHAR. However on MySQL and MariaDB (indicated by database URLs that start with mysql or mariadb), it will render as VARCHAR(255) CHARACTER SET utf8.

TypeEngine.with_variant() - additional usage examples and notes

Generic types specify a column that can read, write and store a particular type of Python data. SQLAlchemy will choose the best database column type available on the target database when issuing a CREATE TABLE statement. For complete control over which column type is emitted in CREATE TABLE, such as VARCHAR see SQL Standard and Multiple Vendor “UPPERCASE” Types and the other sections of this chapter.

A type for bigger int integers.

A type for datetime.date() objects.

A type for datetime.datetime() objects.

A type for double FLOAT floating point types.

Type representing floating point types, such as FLOAT or REAL.

A type for int integers.

A type for datetime.timedelta() objects.

A type for large binary byte data.

Refers to the return type of the MATCH operator.

Base for non-integer numeric types, such as NUMERIC, FLOAT, DECIMAL, and other variants.

Holds Python objects, which are serialized using pickle.

Add capabilities to a type which allow for schema-level DDL to be associated with a type.

A type for smaller int integers.

The base for all string and character types.

A variably sized string type.

A type for datetime.time() objects.

A variable length Unicode string type.

An unbounded-length Unicode string type.

Represent a database agnostic UUID datatype.

inherits from sqlalchemy.types.Integer

A type for bigger int integers.

Typically generates a BIGINT in DDL, and otherwise acts like a normal Integer on the Python side.

inherits from sqlalchemy.types.SchemaType, sqlalchemy.types.Emulated, sqlalchemy.types.TypeEngine

Boolean typically uses BOOLEAN or SMALLINT on the DDL side, and on the Python side deals in True or False.

The Boolean datatype currently has two levels of assertion that the values persisted are simple true/false values. For all backends, only the Python values None, True, False, 1 or 0 are accepted as parameter values. For those backends that don’t support a “native boolean” datatype, an option exists to also create a CHECK constraint on the target column

Changed in version 1.2: the Boolean datatype now asserts that incoming Python values are already in pure boolean form.

Return a conversion function for processing bind values.

Return a conversion function for processing literal values that are to be rendered directly without using binds.

Return a conversion function for processing result row values.

defaults to False. If the boolean is generated as an int/smallint, also create a CHECK constraint on the table that ensures 1 or 0 as a value.

it is strongly recommended that the CHECK constraint have an explicit name in order to support schema-management concerns. This can be established either by setting the Boolean.name parameter or by setting up an appropriate naming convention; see Configuring Constraint Naming Conventions for background.

Changed in version 1.4: - this flag now defaults to False, meaning no CHECK constraint is generated for a non-native enumerated type.

name¶ – if a CHECK constraint is generated, specify the name of the constraint.

Return a conversion function for processing bind values.

Returns a callable which will receive a bind parameter value as the sole positional argument and will return a value to send to the DB-API.

If processing is not necessary, the method should return None.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.bind_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.bind_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_bind_param().

Augmenting Existing Types

dialect¶ – Dialect instance in use.

Return a conversion function for processing literal values that are to be rendered directly without using binds.

This function is used when the compiler makes use of the “literal_binds” flag, typically used in DDL generation as well as in certain scenarios where backends don’t accept bound parameters.

Returns a callable which will receive a literal Python value as the sole positional argument and will return a string representation to be rendered in a SQL statement.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.literal_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.literal_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_literal_param().

Augmenting Existing Types

Return the Python type object expected to be returned by instances of this type, if known.

Basically, for those types which enforce a return type, or are known across the board to do such for all common DBAPIs (like int for example), will return that type.

If a return type is not defined, raises NotImplementedError.

Note that any type also accommodates NULL in SQL which means you can also get back None from any type in practice.

Return a conversion function for processing result row values.

Returns a callable which will receive a result row column value as the sole positional argument and will return a value to return to the user.

If processing is not necessary, the method should return None.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.result_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.result_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_result_value().

Augmenting Existing Types

dialect¶ – Dialect instance in use.

coltype¶ – DBAPI coltype argument received in cursor.description.

inherits from sqlalchemy.types._RenderISO8601NoT, sqlalchemy.types.HasExpressionLookup, sqlalchemy.types.TypeEngine

A type for datetime.date() objects.

Return the corresponding type object from the underlying DB-API, if any.

Return a conversion function for processing literal values that are to be rendered directly without using binds.

Return the corresponding type object from the underlying DB-API, if any.

This can be useful for calling setinputsizes(), for example.

Return a conversion function for processing literal values that are to be rendered directly without using binds.

This function is used when the compiler makes use of the “literal_binds” flag, typically used in DDL generation as well as in certain scenarios where backends don’t accept bound parameters.

Returns a callable which will receive a literal Python value as the sole positional argument and will return a string representation to be rendered in a SQL statement.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.literal_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.literal_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_literal_param().

Augmenting Existing Types

Return the Python type object expected to be returned by instances of this type, if known.

Basically, for those types which enforce a return type, or are known across the board to do such for all common DBAPIs (like int for example), will return that type.

If a return type is not defined, raises NotImplementedError.

Note that any type also accommodates NULL in SQL which means you can also get back None from any type in practice.

inherits from sqlalchemy.types._RenderISO8601NoT, sqlalchemy.types.HasExpressionLookup, sqlalchemy.types.TypeEngine

A type for datetime.datetime() objects.

Date and time types return objects from the Python datetime module. Most DBAPIs have built in support for the datetime module, with the noted exception of SQLite. In the case of SQLite, date and time types are stored as strings which are then converted back to datetime objects when rows are returned.

For the time representation within the datetime type, some backends include additional options, such as timezone support and fractional seconds support. For fractional seconds, use the dialect-specific datatype, such as TIME. For timezone support, use at least the TIMESTAMP datatype, if not the dialect-specific datatype object.

Construct a new DateTime.

Return the corresponding type object from the underlying DB-API, if any.

Return a conversion function for processing literal values that are to be rendered directly without using binds.

Construct a new DateTime.

timezone¶ – boolean. Indicates that the datetime type should enable timezone support, if available on the base date/time-holding type only. It is recommended to make use of the TIMESTAMP datatype directly when using this flag, as some databases include separate generic date/time-holding types distinct from the timezone-capable TIMESTAMP datatype, such as Oracle Database.

Return the corresponding type object from the underlying DB-API, if any.

This can be useful for calling setinputsizes(), for example.

Return a conversion function for processing literal values that are to be rendered directly without using binds.

This function is used when the compiler makes use of the “literal_binds” flag, typically used in DDL generation as well as in certain scenarios where backends don’t accept bound parameters.

Returns a callable which will receive a literal Python value as the sole positional argument and will return a string representation to be rendered in a SQL statement.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.literal_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.literal_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_literal_param().

Augmenting Existing Types

Return the Python type object expected to be returned by instances of this type, if known.

Basically, for those types which enforce a return type, or are known across the board to do such for all common DBAPIs (like int for example), will return that type.

If a return type is not defined, raises NotImplementedError.

Note that any type also accommodates NULL in SQL which means you can also get back None from any type in practice.

inherits from sqlalchemy.types.String, sqlalchemy.types.SchemaType, sqlalchemy.types.Emulated, sqlalchemy.types.TypeEngine

The Enum type provides a set of possible string values which the column is constrained towards.

The Enum type will make use of the backend’s native “ENUM” type if one is available; otherwise, it uses a VARCHAR datatype. An option also exists to automatically produce a CHECK constraint when the VARCHAR (so called “non-native”) variant is produced; see the Enum.create_constraint flag.

The Enum type also provides in-Python validation of string values during both read and write operations. When reading a value from the database in a result set, the string value is always checked against the list of possible values and a LookupError is raised if no match is found. When passing a value to the database as a plain string within a SQL statement, if the Enum.validate_strings parameter is set to True, a LookupError is raised for any string value that’s not located in the given list of possible values; note that this impacts usage of LIKE expressions with enumerated values (an unusual use case).

The source of enumerated values may be a list of string values, or alternatively a PEP-435-compliant enumerated class. For the purposes of the Enum datatype, this class need only provide a __members__ method.

When using an enumerated class, the enumerated objects are used both for input and output, rather than strings as is the case with a plain-string enumerated type:

Above, the string names of each element, e.g. “one”, “two”, “three”, are persisted to the database; the values of the Python Enum, here indicated as integers, are not used; the value of each enum can therefore be any kind of Python object whether or not it is persistable.

In order to persist the values and not the names, the Enum.values_callable parameter may be used. The value of this parameter is a user-supplied callable, which is intended to be used with a PEP-435-compliant enumerated class and returns a list of string values to be persisted. For a simple enumeration that uses string values, a callable such as lambda x: [e.value for e in x] is sufficient.

Using Python Enum or pep-586 Literal types in the type map - background on using the Enum datatype with the ORM’s ORM Annotated Declarative feature.

ENUM - PostgreSQL-specific type, which has additional functionality.

ENUM - MySQL-specific type

Issue CREATE DDL for this type, if applicable.

Issue DROP DDL for this type, if applicable.

Keyword arguments which don’t apply to a specific backend are ignored by that backend.

*enums¶ – either exactly one PEP-435 compliant enumerated type or one or more string labels.

defaults to False. When creating a non-native enumerated type, also build a CHECK constraint on the database against the valid values.

it is strongly recommended that the CHECK constraint have an explicit name in order to support schema-management concerns. This can be established either by setting the Enum.name parameter or by setting up an appropriate naming convention; see Configuring Constraint Naming Conventions for background.

Changed in version 1.4: - this flag now defaults to False, meaning no CHECK constraint is generated for a non-native enumerated type.

Associate this type directly with a MetaData object. For types that exist on the target database as an independent schema construct (PostgreSQL), this type will be created and dropped within create_all() and drop_all() operations. If the type is not associated with any MetaData object, it will associate itself with each Table in which it is used, and will be created when any of those individual tables are created, after a check is performed for its existence. The type is only dropped when drop_all() is called for that Table object’s metadata, however.

The value of the MetaData.schema parameter of the MetaData object, if set, will be used as the default value of the Enum.schema on this object if an explicit value is not otherwise supplied.

Changed in version 1.4.12: Enum inherits the MetaData.schema parameter of the MetaData object if present, when passed using the Enum.metadata parameter.

name¶ – The name of this type. This is required for PostgreSQL and any future supported database which requires an explicitly named type, or an explicitly named constraint in order to generate the type and/or a table that uses it. If a PEP-435 enumerated class was used, its name (converted to lower case) is used by default.

native_enum¶ – Use the database’s native ENUM type when available. Defaults to True. When False, uses VARCHAR + check constraint for all backends. When False, the VARCHAR length can be controlled with Enum.length; currently “length” is ignored if native_enum=True.

Allows specifying a custom length for the VARCHAR when a non-native enumeration datatype is used. By default it uses the length of the longest value.

Changed in version 2.0.0: The Enum.length parameter is used unconditionally for VARCHAR rendering regardless of the Enum.native_enum parameter, for those backends where VARCHAR is used for enumerated datatypes.

Schema name of this type. For types that exist on the target database as an independent schema construct (PostgreSQL), this parameter specifies the named schema in which the type is present.

If not present, the schema name will be taken from the MetaData collection if passed as Enum.metadata, for a MetaData that includes the MetaData.schema parameter.

Changed in version 1.4.12: Enum inherits the MetaData.schema parameter of the MetaData object if present, when passed using the Enum.metadata parameter.

Otherwise, if the Enum.inherit_schema flag is set to True, the schema will be inherited from the associated Table object if any; when Enum.inherit_schema is at its default of False, the owning table’s schema is not used.

quote¶ – Set explicit quoting preferences for the type’s name.

inherit_schema¶ – When True, the “schema” from the owning Table will be copied to the “schema” attribute of this Enum, replacing whatever value was passed for the schema attribute. This also takes effect when using the Table.to_metadata() operation.

validate_strings¶ – when True, string values that are being passed to the database in a SQL statement will be checked for validity against the list of enumerated values. Unrecognized values will result in a LookupError being raised.

A callable which will be passed the PEP-435 compliant enumerated type, which should then return a list of string values to be persisted. This allows for alternate usages such as using the string value of an enum to be persisted to the database instead of its name. The callable must return the values to be persisted in the same order as iterating through the Enum’s __member__ attribute. For example lambda x: [i.value for i in x].

Added in version 1.2.3.

a Python callable which may be used as the “key” argument in the Python sorted() built-in. The SQLAlchemy ORM requires that primary key columns which are mapped must be sortable in some way. When using an unsortable enumeration object such as a Python 3 Enum object, this parameter may be used to set a default sort key function for the objects. By default, the database value of the enumeration is used as the sorting function.

Added in version 1.3.8.

A boolean that when true will remove aliases from pep 435 enums. defaults to True.

Changed in version 2.0: This parameter now defaults to True.

inherited from the SchemaType.create() method of SchemaType

Issue CREATE DDL for this type, if applicable.

inherited from the SchemaType.drop() method of SchemaType

Issue DROP DDL for this type, if applicable.

inherits from sqlalchemy.types.Float

A type for double FLOAT floating point types.

Typically generates a DOUBLE or DOUBLE_PRECISION in DDL, and otherwise acts like a normal Float on the Python side.

Added in version 2.0.

inherits from sqlalchemy.types.Numeric

Type representing floating point types, such as FLOAT or REAL.

This type returns Python float objects by default, unless the Float.asdecimal flag is set to True, in which case they are coerced to decimal.Decimal objects.

When a Float.precision is not provided in a Float type some backend may compile this type as an 8 bytes / 64 bit float datatype. To use a 4 bytes / 32 bit float datatype a precision <= 24 can usually be provided or the REAL type can be used. This is known to be the case in the PostgreSQL and MSSQL dialects that render the type as FLOAT that’s in both an alias of DOUBLE PRECISION. Other third party dialects may have similar behavior.

Return a conversion function for processing result row values.

the numeric precision for use in DDL CREATE TABLE. Backends should attempt to ensure this precision indicates a number of digits for the generic Float datatype.

For the Oracle Database backend, the Float.precision parameter is not accepted when rendering DDL, as Oracle Database does not support float precision specified as a number of decimal places. Instead, use the Oracle Database-specific FLOAT datatype and specify the FLOAT.binary_precision parameter. This is new in version 2.0 of SQLAlchemy.

To create a database agnostic Float that separately specifies binary precision for Oracle Database, use TypeEngine.with_variant() as follows:

asdecimal¶ – the same flag as that of Numeric, but defaults to False. Note that setting this flag to True results in floating point conversion.

decimal_return_scale¶ – Default scale to use when converting from floats to Python decimals. Floating point values will typically be much longer due to decimal inaccuracy, and most floating point database types don’t have a notion of “scale”, so by default the float type looks for the first ten decimal places when converting. Specifying this value will override that length. Note that the MySQL float types, which do include “scale”, will use “scale” as the default for decimal_return_scale, if not otherwise specified.

Return a conversion function for processing result row values.

Returns a callable which will receive a result row column value as the sole positional argument and will return a value to return to the user.

If processing is not necessary, the method should return None.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.result_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.result_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_result_value().

Augmenting Existing Types

dialect¶ – Dialect instance in use.

coltype¶ – DBAPI coltype argument received in cursor.description.

inherits from sqlalchemy.types.HasExpressionLookup, sqlalchemy.types.TypeEngine

A type for int integers.

Return the corresponding type object from the underlying DB-API, if any.

Return a conversion function for processing literal values that are to be rendered directly without using binds.

Return the corresponding type object from the underlying DB-API, if any.

This can be useful for calling setinputsizes(), for example.

Return a conversion function for processing literal values that are to be rendered directly without using binds.

This function is used when the compiler makes use of the “literal_binds” flag, typically used in DDL generation as well as in certain scenarios where backends don’t accept bound parameters.

Returns a callable which will receive a literal Python value as the sole positional argument and will return a string representation to be rendered in a SQL statement.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.literal_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.literal_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_literal_param().

Augmenting Existing Types

Return the Python type object expected to be returned by instances of this type, if known.

Basically, for those types which enforce a return type, or are known across the board to do such for all common DBAPIs (like int for example), will return that type.

If a return type is not defined, raises NotImplementedError.

Note that any type also accommodates NULL in SQL which means you can also get back None from any type in practice.

inherits from sqlalchemy.types.Emulated, sqlalchemy.types._AbstractInterval, sqlalchemy.types.TypeDecorator

A type for datetime.timedelta() objects.

The Interval type deals with datetime.timedelta objects. In PostgreSQL and Oracle Database, the native INTERVAL type is used; for others, the value is stored as a date which is relative to the “epoch” (Jan. 1, 1970).

Note that the Interval type does not currently provide date arithmetic operations on platforms which do not support interval types natively. Such operations usually require transformation of both sides of the expression (such as, conversion of both sides into integer epoch values first) which currently is a manual procedure (such as via expression.func).

Construct an Interval object.

Given an impl class, adapt this type to the impl assuming “emulated”.

Return a conversion function for processing bind values.

Indicate if statements using this ExternalType are “safe to cache”.

coerce_compared_value()

Suggest a type for a ‘coerced’ Python value in an expression.

Return a conversion function for processing result row values.

inherits from sqlalchemy.types.Comparator, sqlalchemy.types.Comparator

Construct an Interval object.

native¶ – when True, use the actual INTERVAL type provided by the database, if supported (currently PostgreSQL, Oracle Database). Otherwise, represent the interval data as an epoch value regardless.

second_precision¶ – For native interval types which support a “fractional seconds precision” parameter, i.e. Oracle Database and PostgreSQL

day_precision¶ – for native interval types which support a “day precision” parameter, i.e. Oracle Database.

Given an impl class, adapt this type to the impl assuming “emulated”.

The impl should also be an “emulated” version of this type, most likely the same class as this type itself.

e.g.: sqltypes.Enum adapts to the Enum class.

Return a conversion function for processing bind values.

Returns a callable which will receive a bind parameter value as the sole positional argument and will return a value to send to the DB-API.

If processing is not necessary, the method should return None.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.bind_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.bind_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_bind_param().

Augmenting Existing Types

dialect¶ – Dialect instance in use.

Indicate if statements using this ExternalType are “safe to cache”.

The default value None will emit a warning and then not allow caching of a statement which includes this type. Set to False to disable statements using this type from being cached at all without a warning. When set to True, the object’s class and selected elements from its state will be used as part of the cache key. For example, using a TypeDecorator:

The cache key for the above type would be equivalent to:

The caching scheme will extract attributes from the type that correspond to the names of parameters in the __init__() method. Above, the “choices” attribute becomes part of the cache key but “internal_only” does not, because there is no parameter named “internal_only”.

The requirements for cacheable elements is that they are hashable and also that they indicate the same SQL rendered for expressions using this type every time for a given cache value.

To accommodate for datatypes that refer to unhashable structures such as dictionaries, sets and lists, these objects can be made “cacheable” by assigning hashable structures to the attributes whose names correspond with the names of the arguments. For example, a datatype which accepts a dictionary of lookup values may publish this as a sorted series of tuples. Given a previously un-cacheable type as:

Where “lookup” is a dictionary. The type will not be able to generate a cache key:

If we did set up such a cache key, it wouldn’t be usable. We would get a tuple structure that contains a dictionary inside of it, which cannot itself be used as a key in a “cache dictionary” such as SQLAlchemy’s statement cache, since Python dictionaries aren’t hashable:

The type may be made cacheable by assigning a sorted tuple of tuples to the “.lookup” attribute:

Where above, the cache key for LookupType({"a": 10, "b": 20}) will be:

Added in version 1.4.14: - added the cache_ok flag to allow some configurability of caching for TypeDecorator classes.

Added in version 1.4.28: - added the ExternalType mixin which generalizes the cache_ok flag to both the TypeDecorator and UserDefinedType classes.

SQL Compilation Caching

Suggest a type for a ‘coerced’ Python value in an expression.

Given an operator and value, gives the type a chance to return a type which the value should be coerced into.

The default behavior here is conservative; if the right-hand side is already coerced into a SQL type based on its Python type, it is usually left alone.

End-user functionality extension here should generally be via TypeDecorator, which provides more liberal behavior in that it defaults to coercing the other side of the expression into this type, thus applying special Python conversions above and beyond those needed by the DBAPI to both ides. It also provides the public method TypeDecorator.coerce_compared_value() which is intended for end-user customization of this behavior.

Return the Python type object expected to be returned by instances of this type, if known.

Basically, for those types which enforce a return type, or are known across the board to do such for all common DBAPIs (like int for example), will return that type.

If a return type is not defined, raises NotImplementedError.

Note that any type also accommodates NULL in SQL which means you can also get back None from any type in practice.

Return a conversion function for processing result row values.

Returns a callable which will receive a result row column value as the sole positional argument and will return a value to return to the user.

If processing is not necessary, the method should return None.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.result_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.result_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_result_value().

Augmenting Existing Types

dialect¶ – Dialect instance in use.

coltype¶ – DBAPI coltype argument received in cursor.description.

inherits from sqlalchemy.types._Binary

A type for large binary byte data.

The LargeBinary type corresponds to a large and/or unlengthed binary type for the target platform, such as BLOB on MySQL and BYTEA for PostgreSQL. It also handles the necessary conversions for the DBAPI.

Construct a LargeBinary type.

Construct a LargeBinary type.

length¶ – optional, a length for the column for use in DDL statements, for those binary types that accept a length, such as the MySQL BLOB type.

inherits from sqlalchemy.types.Boolean

Refers to the return type of the MATCH operator.

As the ColumnOperators.match() is probably the most open-ended operator in generic SQLAlchemy Core, we can’t assume the return type at SQL evaluation time, as MySQL returns a floating point, not a boolean, and other backends might do something different. So this type acts as a placeholder, currently subclassing Boolean. The type allows dialects to inject result-processing functionality if needed, and on MySQL will return floating-point values.

inherits from sqlalchemy.types.HasExpressionLookup, sqlalchemy.types.TypeEngine

Base for non-integer numeric types, such as NUMERIC, FLOAT, DECIMAL, and other variants.

The Numeric datatype when used directly will render DDL corresponding to precision numerics if available, such as NUMERIC(precision, scale). The Float subclass will attempt to render a floating-point datatype such as FLOAT(precision).

Numeric returns Python decimal.Decimal objects by default, based on the default value of True for the Numeric.asdecimal parameter. If this parameter is set to False, returned values are coerced to Python float objects.

The Float subtype, being more specific to floating point, defaults the Float.asdecimal flag to False so that the default Python datatype is float.

When using a Numeric datatype against a database type that returns Python floating point values to the driver, the accuracy of the decimal conversion indicated by Numeric.asdecimal may be limited. The behavior of specific numeric/floating point datatypes is a product of the SQL datatype in use, the Python DBAPI in use, as well as strategies that may be present within the SQLAlchemy dialect in use. Users requiring specific precision/ scale are encouraged to experiment with the available datatypes in order to determine the best results.

Return a conversion function for processing bind values.

Return the corresponding type object from the underlying DB-API, if any.

Return a conversion function for processing literal values that are to be rendered directly without using binds.

Return a conversion function for processing result row values.

precision¶ – the numeric precision for use in DDL CREATE TABLE.

scale¶ – the numeric scale for use in DDL CREATE TABLE.

asdecimal¶ – default True. Return whether or not values should be sent as Python Decimal objects, or as floats. Different DBAPIs send one or the other based on datatypes - the Numeric type will ensure that return values are one or the other across DBAPIs consistently.

decimal_return_scale¶ – Default scale to use when converting from floats to Python decimals. Floating point values will typically be much longer due to decimal inaccuracy, and most floating point database types don’t have a notion of “scale”, so by default the float type looks for the first ten decimal places when converting. Specifying this value will override that length. Types which do include an explicit “.scale” value, such as the base Numeric as well as the MySQL float types, will use the value of “.scale” as the default for decimal_return_scale, if not otherwise specified.

When using the Numeric type, care should be taken to ensure that the asdecimal setting is appropriate for the DBAPI in use - when Numeric applies a conversion from Decimal->float or float-> Decimal, this conversion incurs an additional performance overhead for all result columns received.

DBAPIs that return Decimal natively (e.g. psycopg2) will have better accuracy and higher performance with a setting of True, as the native translation to Decimal reduces the amount of floating- point issues at play, and the Numeric type itself doesn’t need to apply any further conversions. However, another DBAPI which returns floats natively will incur an additional conversion overhead, and is still subject to floating point data loss - in which case asdecimal=False will at least remove the extra conversion overhead.

Return a conversion function for processing bind values.

Returns a callable which will receive a bind parameter value as the sole positional argument and will return a value to send to the DB-API.

If processing is not necessary, the method should return None.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.bind_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.bind_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_bind_param().

Augmenting Existing Types

dialect¶ – Dialect instance in use.

Return the corresponding type object from the underlying DB-API, if any.

This can be useful for calling setinputsizes(), for example.

Return a conversion function for processing literal values that are to be rendered directly without using binds.

This function is used when the compiler makes use of the “literal_binds” flag, typically used in DDL generation as well as in certain scenarios where backends don’t accept bound parameters.

Returns a callable which will receive a literal Python value as the sole positional argument and will return a string representation to be rendered in a SQL statement.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.literal_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.literal_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_literal_param().

Augmenting Existing Types

Return the Python type object expected to be returned by instances of this type, if known.

Basically, for those types which enforce a return type, or are known across the board to do such for all common DBAPIs (like int for example), will return that type.

If a return type is not defined, raises NotImplementedError.

Note that any type also accommodates NULL in SQL which means you can also get back None from any type in practice.

Return a conversion function for processing result row values.

Returns a callable which will receive a result row column value as the sole positional argument and will return a value to return to the user.

If processing is not necessary, the method should return None.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.result_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.result_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_result_value().

Augmenting Existing Types

dialect¶ – Dialect instance in use.

coltype¶ – DBAPI coltype argument received in cursor.description.

inherits from sqlalchemy.types.TypeDecorator

Holds Python objects, which are serialized using pickle.

PickleType builds upon the Binary type to apply Python’s pickle.dumps() to incoming objects, and pickle.loads() on the way out, allowing any pickleable Python object to be stored as a serialized binary field.

To allow ORM change events to propagate for elements associated with PickleType, see Mutation Tracking.

Construct a PickleType.

Provide a bound value processing function for the given Dialect.

Indicate if statements using this ExternalType are “safe to cache”.

Given two values, compare them for equality.

Provide a result value processing function for the given Dialect.

Construct a PickleType.

protocol¶ – defaults to pickle.HIGHEST_PROTOCOL.

pickler¶ – defaults to pickle. May be any object with pickle-compatible dumps and loads methods.

comparator¶ – a 2-arg callable predicate used to compare values of this type. If left as None, the Python “equals” operator is used to compare values.

A binary-storing TypeEngine class or instance to use in place of the default LargeBinary. For example the :class: _mysql.LONGBLOB class may be more effective when using MySQL.

Added in version 1.4.20.

Provide a bound value processing function for the given Dialect.

This is the method that fulfills the TypeEngine contract for bound value conversion which normally occurs via the TypeEngine.bind_processor() method.

User-defined subclasses of TypeDecorator should not implement this method, and should instead implement TypeDecorator.process_bind_param() so that the “inner” processing provided by the implementing type is maintained.

dialect¶ – Dialect instance in use.

Indicate if statements using this ExternalType are “safe to cache”.

The default value None will emit a warning and then not allow caching of a statement which includes this type. Set to False to disable statements using this type from being cached at all without a warning. When set to True, the object’s class and selected elements from its state will be used as part of the cache key. For example, using a TypeDecorator:

The cache key for the above type would be equivalent to:

The caching scheme will extract attributes from the type that correspond to the names of parameters in the __init__() method. Above, the “choices” attribute becomes part of the cache key but “internal_only” does not, because there is no parameter named “internal_only”.

The requirements for cacheable elements is that they are hashable and also that they indicate the same SQL rendered for expressions using this type every time for a given cache value.

To accommodate for datatypes that refer to unhashable structures such as dictionaries, sets and lists, these objects can be made “cacheable” by assigning hashable structures to the attributes whose names correspond with the names of the arguments. For example, a datatype which accepts a dictionary of lookup values may publish this as a sorted series of tuples. Given a previously un-cacheable type as:

Where “lookup” is a dictionary. The type will not be able to generate a cache key:

If we did set up such a cache key, it wouldn’t be usable. We would get a tuple structure that contains a dictionary inside of it, which cannot itself be used as a key in a “cache dictionary” such as SQLAlchemy’s statement cache, since Python dictionaries aren’t hashable:

The type may be made cacheable by assigning a sorted tuple of tuples to the “.lookup” attribute:

Where above, the cache key for LookupType({"a": 10, "b": 20}) will be:

Added in version 1.4.14: - added the cache_ok flag to allow some configurability of caching for TypeDecorator classes.

Added in version 1.4.28: - added the ExternalType mixin which generalizes the cache_ok flag to both the TypeDecorator and UserDefinedType classes.

SQL Compilation Caching

Given two values, compare them for equality.

By default this calls upon TypeEngine.compare_values() of the underlying “impl”, which in turn usually uses the Python equals operator ==.

This function is used by the ORM to compare an original-loaded value with an intercepted “changed” value, to determine if a net change has occurred.

Provide a result value processing function for the given Dialect.

This is the method that fulfills the TypeEngine contract for bound value conversion which normally occurs via the TypeEngine.result_processor() method.

User-defined subclasses of TypeDecorator should not implement this method, and should instead implement TypeDecorator.process_result_value() so that the “inner” processing provided by the implementing type is maintained.

dialect¶ – Dialect instance in use.

coltype¶ – A SQLAlchemy data type

inherits from sqlalchemy.sql.expression.SchemaEventTarget, sqlalchemy.types.TypeEngineMixin

Add capabilities to a type which allow for schema-level DDL to be associated with a type.

Supports types that must be explicitly created/dropped (i.e. PG ENUM type) as well as types that are complimented by table or schema level constraints, triggers, and other rules.

SchemaType classes can also be targets for the DDLEvents.before_parent_attach() and DDLEvents.after_parent_attach() events, where the events fire off surrounding the association of the type object with a parent Column.

Issue CREATE DDL for this type, if applicable.

Issue DROP DDL for this type, if applicable.

Issue CREATE DDL for this type, if applicable.

Issue DROP DDL for this type, if applicable.

inherits from sqlalchemy.types.Integer

A type for smaller int integers.

Typically generates a SMALLINT in DDL, and otherwise acts like a normal Integer on the Python side.

inherits from sqlalchemy.types.Concatenable, sqlalchemy.types.TypeEngine

The base for all string and character types.

In SQL, corresponds to VARCHAR.

The length field is usually required when the String type is used within a CREATE TABLE statement, as VARCHAR requires a length on most databases.

Create a string-holding type.

Return a conversion function for processing bind values.

Return the corresponding type object from the underlying DB-API, if any.

Return a conversion function for processing literal values that are to be rendered directly without using binds.

Return a conversion function for processing result row values.

Create a string-holding type.

length¶ – optional, a length for the column for use in DDL and CAST expressions. May be safely omitted if no CREATE TABLE will be issued. Certain databases may require a length for use in DDL, and will raise an exception when the CREATE TABLE DDL is issued if a VARCHAR with no length is included. Whether the value is interpreted as bytes or characters is database specific.

Optional, a column-level collation for use in DDL and CAST expressions. Renders using the COLLATE keyword supported by SQLite, MySQL, and PostgreSQL. E.g.:

In most cases, the Unicode or UnicodeText datatypes should be used for a Column that expects to store non-ascii data. These datatypes will ensure that the correct types are used on the database.

Return a conversion function for processing bind values.

Returns a callable which will receive a bind parameter value as the sole positional argument and will return a value to send to the DB-API.

If processing is not necessary, the method should return None.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.bind_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.bind_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_bind_param().

Augmenting Existing Types

dialect¶ – Dialect instance in use.

Return the corresponding type object from the underlying DB-API, if any.

This can be useful for calling setinputsizes(), for example.

Return a conversion function for processing literal values that are to be rendered directly without using binds.

This function is used when the compiler makes use of the “literal_binds” flag, typically used in DDL generation as well as in certain scenarios where backends don’t accept bound parameters.

Returns a callable which will receive a literal Python value as the sole positional argument and will return a string representation to be rendered in a SQL statement.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.literal_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.literal_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_literal_param().

Augmenting Existing Types

Return the Python type object expected to be returned by instances of this type, if known.

Basically, for those types which enforce a return type, or are known across the board to do such for all common DBAPIs (like int for example), will return that type.

If a return type is not defined, raises NotImplementedError.

Note that any type also accommodates NULL in SQL which means you can also get back None from any type in practice.

Return a conversion function for processing result row values.

Returns a callable which will receive a result row column value as the sole positional argument and will return a value to return to the user.

If processing is not necessary, the method should return None.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.result_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.result_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_result_value().

Augmenting Existing Types

dialect¶ – Dialect instance in use.

coltype¶ – DBAPI coltype argument received in cursor.description.

inherits from sqlalchemy.types.String

A variably sized string type.

In SQL, usually corresponds to CLOB or TEXT. In general, TEXT objects do not have a length; while some databases will accept a length argument here, it will be rejected by others.

inherits from sqlalchemy.types._RenderISO8601NoT, sqlalchemy.types.HasExpressionLookup, sqlalchemy.types.TypeEngine

A type for datetime.time() objects.

Return the corresponding type object from the underlying DB-API, if any.

Return a conversion function for processing literal values that are to be rendered directly without using binds.

Return the corresponding type object from the underlying DB-API, if any.

This can be useful for calling setinputsizes(), for example.

Return a conversion function for processing literal values that are to be rendered directly without using binds.

This function is used when the compiler makes use of the “literal_binds” flag, typically used in DDL generation as well as in certain scenarios where backends don’t accept bound parameters.

Returns a callable which will receive a literal Python value as the sole positional argument and will return a string representation to be rendered in a SQL statement.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.literal_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.literal_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_literal_param().

Augmenting Existing Types

Return the Python type object expected to be returned by instances of this type, if known.

Basically, for those types which enforce a return type, or are known across the board to do such for all common DBAPIs (like int for example), will return that type.

If a return type is not defined, raises NotImplementedError.

Note that any type also accommodates NULL in SQL which means you can also get back None from any type in practice.

inherits from sqlalchemy.types.String

A variable length Unicode string type.

The Unicode type is a String subclass that assumes input and output strings that may contain non-ASCII characters, and for some backends implies an underlying column type that is explicitly supporting of non-ASCII data, such as NVARCHAR on Oracle Database and SQL Server. This will impact the output of CREATE TABLE statements and CAST functions at the dialect level.

The character encoding used by the Unicode type that is used to transmit and receive data to the database is usually determined by the DBAPI itself. All modern DBAPIs accommodate non-ASCII strings but may have different methods of managing database encodings; if necessary, this encoding should be configured as detailed in the notes for the target DBAPI in the Dialects section.

In modern SQLAlchemy, use of the Unicode datatype does not imply any encoding/decoding behavior within SQLAlchemy itself. In Python 3, all string objects are inherently Unicode capable, and SQLAlchemy does not produce bytestring objects nor does it accommodate a DBAPI that does not return Python Unicode objects in result sets for string values.

Some database backends, particularly SQL Server with pyodbc, are known to have undesirable behaviors regarding data that is noted as being of NVARCHAR type as opposed to VARCHAR, including datatype mismatch errors and non-use of indexes. See the section on DialectEvents.do_setinputsizes() for background on working around unicode character issues for backends like SQL Server with pyodbc as well as cx_Oracle.

UnicodeText - unlengthed textual counterpart to Unicode.

DialectEvents.do_setinputsizes()

inherits from sqlalchemy.types.Text

An unbounded-length Unicode string type.

See Unicode for details on the unicode behavior of this object.

Like Unicode, usage the UnicodeText type implies a unicode-capable type being used on the backend, such as NCLOB, NTEXT.

inherits from sqlalchemy.types.Emulated, sqlalchemy.types.TypeEngine

Represent a database agnostic UUID datatype.

For backends that have no “native” UUID datatype, the value will make use of CHAR(32) and store the UUID as a 32-character alphanumeric hex string.

For backends which are known to support UUID directly or a similar uuid-storing datatype such as SQL Server’s UNIQUEIDENTIFIER, a “native” mode enabled by default allows these types will be used on those backends.

In its default mode of use, the Uuid datatype expects Python uuid objects, from the Python uuid module:

To have the Uuid datatype work with string-based Uuids (e.g. 32 character hexadecimal strings), pass the Uuid.as_uuid parameter with the value False.

Added in version 2.0.

UUID - represents exactly the UUID datatype without any backend-agnostic behaviors.

Construct a Uuid type.

Return a conversion function for processing bind values.

coerce_compared_value()

See TypeEngine.coerce_compared_value() for a description.

Return a conversion function for processing literal values that are to be rendered directly without using binds.

Return a conversion function for processing result row values.

Construct a Uuid type.

if True, values will be interpreted as Python uuid objects, converting to/from string via the DBAPI.

native_uuid=True¶ – if True, backends that support either the UUID datatype directly, or a UUID-storing value (such as SQL Server’s UNIQUEIDENTIFIER will be used by those backends. If False, a CHAR(32) datatype will be used for all backends regardless of native support.

Return a conversion function for processing bind values.

Returns a callable which will receive a bind parameter value as the sole positional argument and will return a value to send to the DB-API.

If processing is not necessary, the method should return None.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.bind_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.bind_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_bind_param().

Augmenting Existing Types

dialect¶ – Dialect instance in use.

See TypeEngine.coerce_compared_value() for a description.

Return a conversion function for processing literal values that are to be rendered directly without using binds.

This function is used when the compiler makes use of the “literal_binds” flag, typically used in DDL generation as well as in certain scenarios where backends don’t accept bound parameters.

Returns a callable which will receive a literal Python value as the sole positional argument and will return a string representation to be rendered in a SQL statement.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.literal_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.literal_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_literal_param().

Augmenting Existing Types

Return the Python type object expected to be returned by instances of this type, if known.

Basically, for those types which enforce a return type, or are known across the board to do such for all common DBAPIs (like int for example), will return that type.

If a return type is not defined, raises NotImplementedError.

Note that any type also accommodates NULL in SQL which means you can also get back None from any type in practice.

Return a conversion function for processing result row values.

Returns a callable which will receive a result row column value as the sole positional argument and will return a value to return to the user.

If processing is not necessary, the method should return None.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.result_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.result_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_result_value().

Augmenting Existing Types

dialect¶ – Dialect instance in use.

coltype¶ – DBAPI coltype argument received in cursor.description.

This category of types refers to types that are either part of the SQL standard, or are potentially found within a subset of database backends. Unlike the “generic” types, the SQL standard/multi-vendor types have no guarantee of working on all backends, and will only work on those backends that explicitly support them by name. That is, the type will always emit its exact name in DDL with CREATE TABLE is issued.

Represent a SQL Array type.

The SQL BOOLEAN type.

The SQL DATETIME type.

The SQL DECIMAL type.

The SQL DOUBLE PRECISION type.

The SQL INT or INTEGER type.

Represent a SQL JSON type.

The SQL NUMERIC type.

The SQL NVARCHAR type.

The SQL SMALLINT type.

The SQL TIMESTAMP type.

Represent the SQL UUID type.

The SQL VARBINARY type.

The SQL VARCHAR type.

inherits from sqlalchemy.sql.expression.SchemaEventTarget, sqlalchemy.types.Indexable, sqlalchemy.types.Concatenable, sqlalchemy.types.TypeEngine

Represent a SQL Array type.

This type serves as the basis for all ARRAY operations. However, currently only the PostgreSQL backend has support for SQL arrays in SQLAlchemy. It is recommended to use the PostgreSQL-specific sqlalchemy.dialects.postgresql.ARRAY type directly when using ARRAY types with PostgreSQL, as it provides additional operators specific to that backend.

ARRAY is part of the Core in support of various SQL standard functions such as array_agg which explicitly involve arrays; however, with the exception of the PostgreSQL backend and possibly some third-party dialects, no other SQLAlchemy built-in dialect has support for this type.

An ARRAY type is constructed given the “type” of element:

The above type represents an N-dimensional array, meaning a supporting backend such as PostgreSQL will interpret values with any number of dimensions automatically. To produce an INSERT construct that passes in a 1-dimensional array of integers:

The ARRAY type can be constructed given a fixed number of dimensions:

Sending a number of dimensions is optional, but recommended if the datatype is to represent arrays of more than one dimension. This number is used:

When emitting the type declaration itself to the database, e.g. INTEGER[][]

When translating Python values to database values, and vice versa, e.g. an ARRAY of Unicode objects uses this number to efficiently access the string values inside of array structures without resorting to per-row type inspection

When used with the Python getitem accessor, the number of dimensions serves to define the kind of type that the [] operator should return, e.g. for an ARRAY of INTEGER with two dimensions:

For 1-dimensional arrays, an ARRAY instance with no dimension parameter will generally assume single-dimensional behaviors.

SQL expressions of type ARRAY have support for “index” and “slice” behavior. The [] operator produces expression constructs which will produce the appropriate SQL, both for SELECT statements:

as well as UPDATE statements when the Update.values() method is used:

Indexed access is one-based by default; for zero-based index conversion, set ARRAY.zero_indexes.

The ARRAY type also provides for the operators Comparator.any() and Comparator.all(). The PostgreSQL-specific version of ARRAY also provides additional operators.

Detecting Changes in ARRAY columns when using the ORM

The ARRAY type, when used with the SQLAlchemy ORM, does not detect in-place mutations to the array. In order to detect these, the sqlalchemy.ext.mutable extension must be used, using the MutableList class:

This extension will allow “in-place” changes such to the array such as .append() to produce events which will be detected by the unit of work. Note that changes to elements inside the array, including subarrays that are mutated in place, are not detected.

Alternatively, assigning a new array value to an ORM element that replaces the old one will always trigger a change event.

sqlalchemy.dialects.postgresql.ARRAY

ARRAY.contains() not implemented for the base ARRAY type. Use the dialect-specific ARRAY type.

Return other operator ANY (array) clause.

Return other operator ALL (array) clause.

item_type¶ – The data type of items of this array. Note that dimensionality is irrelevant here, so multi-dimensional arrays like INTEGER[][], are constructed as ARRAY(Integer), not as ARRAY(ARRAY(Integer)) or such.

as_tuple=False¶ – Specify whether return results should be converted to tuples from lists. This parameter is not generally needed as a Python list corresponds well to a SQL array.

dimensions¶ – if non-None, the ARRAY will assume a fixed number of dimensions. This impacts how the array is declared on the database, how it goes about interpreting Python and result values, as well as how expression behavior in conjunction with the “getitem” operator works. See the description at ARRAY for additional detail.

zero_indexes=False¶ – when True, index values will be converted between Python zero-based and SQL one-based indexes, e.g. a value of one will be added to all index values before passing to the database.

inherits from sqlalchemy.types.Comparator, sqlalchemy.types.Comparator

Define comparison operations for ARRAY.

More operators are available on the dialect-specific form of this type. See Comparator.

ARRAY.contains() not implemented for the base ARRAY type. Use the dialect-specific ARRAY type.

ARRAY - PostgreSQL specific version.

Return other operator ANY (array) clause.

This method is an ARRAY - specific construct that is now superseded by the any_() function, which features a different calling style. The any_() function is also mirrored at the method level via the ColumnOperators.any_() method.

Usage of array-specific Comparator.any() is as follows:

other¶ – expression to be compared

operator¶ – an operator object from the sqlalchemy.sql.operators package, defaults to eq().

Return other operator ALL (array) clause.

This method is an ARRAY - specific construct that is now superseded by the all_() function, which features a different calling style. The all_() function is also mirrored at the method level via the ColumnOperators.all_() method.

Usage of array-specific Comparator.all() is as follows:

other¶ – expression to be compared

operator¶ – an operator object from the sqlalchemy.sql.operators package, defaults to eq().

inherits from sqlalchemy.types.BigInteger

BigInteger - documentation for the base type.

inherits from sqlalchemy.types._Binary

inherits from sqlalchemy.types.LargeBinary

Construct a LargeBinary type.

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

inherits from sqlalchemy.types.String

Create a string-holding type.

inherited from the sqlalchemy.types.String.__init__ method of String

Create a string-holding type.

length¶ – optional, a length for the column for use in DDL and CAST expressions. May be safely omitted if no CREATE TABLE will be issued. Certain databases may require a length for use in DDL, and will raise an exception when the CREATE TABLE DDL is issued if a VARCHAR with no length is included. Whether the value is interpreted as bytes or characters is database specific.

Optional, a column-level collation for use in DDL and CAST expressions. Renders using the COLLATE keyword supported by SQLite, MySQL, and PostgreSQL. E.g.:

In most cases, the Unicode or UnicodeText datatypes should be used for a Column that expects to store non-ascii data. These datatypes will ensure that the correct types are used on the database.

inherits from sqlalchemy.types.Text

This type is found in Oracle Database and Informix.

Create a string-holding type.

inherited from the sqlalchemy.types.String.__init__ method of String

Create a string-holding type.

length¶ – optional, a length for the column for use in DDL and CAST expressions. May be safely omitted if no CREATE TABLE will be issued. Certain databases may require a length for use in DDL, and will raise an exception when the CREATE TABLE DDL is issued if a VARCHAR with no length is included. Whether the value is interpreted as bytes or characters is database specific.

Optional, a column-level collation for use in DDL and CAST expressions. Renders using the COLLATE keyword supported by SQLite, MySQL, and PostgreSQL. E.g.:

In most cases, the Unicode or UnicodeText datatypes should be used for a Column that expects to store non-ascii data. These datatypes will ensure that the correct types are used on the database.

inherits from sqlalchemy.types.Date

inherits from sqlalchemy.types.DateTime

The SQL DATETIME type.

Construct a new DateTime.

inherited from the sqlalchemy.types.DateTime.__init__ method of DateTime

Construct a new DateTime.

timezone¶ – boolean. Indicates that the datetime type should enable timezone support, if available on the base date/time-holding type only. It is recommended to make use of the TIMESTAMP datatype directly when using this flag, as some databases include separate generic date/time-holding types distinct from the timezone-capable TIMESTAMP datatype, such as Oracle Database.

inherits from sqlalchemy.types.Numeric

The SQL DECIMAL type.

Numeric - documentation for the base type.

inherited from the sqlalchemy.types.Numeric.__init__ method of Numeric

precision¶ – the numeric precision for use in DDL CREATE TABLE.

scale¶ – the numeric scale for use in DDL CREATE TABLE.

asdecimal¶ – default True. Return whether or not values should be sent as Python Decimal objects, or as floats. Different DBAPIs send one or the other based on datatypes - the Numeric type will ensure that return values are one or the other across DBAPIs consistently.

decimal_return_scale¶ – Default scale to use when converting from floats to Python decimals. Floating point values will typically be much longer due to decimal inaccuracy, and most floating point database types don’t have a notion of “scale”, so by default the float type looks for the first ten decimal places when converting. Specifying this value will override that length. Types which do include an explicit “.scale” value, such as the base Numeric as well as the MySQL float types, will use the value of “.scale” as the default for decimal_return_scale, if not otherwise specified.

When using the Numeric type, care should be taken to ensure that the asdecimal setting is appropriate for the DBAPI in use - when Numeric applies a conversion from Decimal->float or float-> Decimal, this conversion incurs an additional performance overhead for all result columns received.

DBAPIs that return Decimal natively (e.g. psycopg2) will have better accuracy and higher performance with a setting of True, as the native translation to Decimal reduces the amount of floating- point issues at play, and the Numeric type itself doesn’t need to apply any further conversions. However, another DBAPI which returns floats natively will incur an additional conversion overhead, and is still subject to floating point data loss - in which case asdecimal=False will at least remove the extra conversion overhead.

inherits from sqlalchemy.types.Double

Added in version 2.0.

Double - documentation for the base type.

inherited from the sqlalchemy.types.Float.__init__ method of Float

the numeric precision for use in DDL CREATE TABLE. Backends should attempt to ensure this precision indicates a number of digits for the generic Float datatype.

For the Oracle Database backend, the Float.precision parameter is not accepted when rendering DDL, as Oracle Database does not support float precision specified as a number of decimal places. Instead, use the Oracle Database-specific FLOAT datatype and specify the FLOAT.binary_precision parameter. This is new in version 2.0 of SQLAlchemy.

To create a database agnostic Float that separately specifies binary precision for Oracle Database, use TypeEngine.with_variant() as follows:

asdecimal¶ – the same flag as that of Numeric, but defaults to False. Note that setting this flag to True results in floating point conversion.

decimal_return_scale¶ – Default scale to use when converting from floats to Python decimals. Floating point values will typically be much longer due to decimal inaccuracy, and most floating point database types don’t have a notion of “scale”, so by default the float type looks for the first ten decimal places when converting. Specifying this value will override that length. Note that the MySQL float types, which do include “scale”, will use “scale” as the default for decimal_return_scale, if not otherwise specified.

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

inherits from sqlalchemy.types.Float

Float - documentation for the base type.

inherited from the sqlalchemy.types.Float.__init__ method of Float

the numeric precision for use in DDL CREATE TABLE. Backends should attempt to ensure this precision indicates a number of digits for the generic Float datatype.

For the Oracle Database backend, the Float.precision parameter is not accepted when rendering DDL, as Oracle Database does not support float precision specified as a number of decimal places. Instead, use the Oracle Database-specific FLOAT datatype and specify the FLOAT.binary_precision parameter. This is new in version 2.0 of SQLAlchemy.

To create a database agnostic Float that separately specifies binary precision for Oracle Database, use TypeEngine.with_variant() as follows:

asdecimal¶ – the same flag as that of Numeric, but defaults to False. Note that setting this flag to True results in floating point conversion.

decimal_return_scale¶ – Default scale to use when converting from floats to Python decimals. Floating point values will typically be much longer due to decimal inaccuracy, and most floating point database types don’t have a notion of “scale”, so by default the float type looks for the first ten decimal places when converting. Specifying this value will override that length. Note that the MySQL float types, which do include “scale”, will use “scale” as the default for decimal_return_scale, if not otherwise specified.

inherits from sqlalchemy.types.Indexable, sqlalchemy.types.TypeEngine

Represent a SQL JSON type.

JSON is provided as a facade for vendor-specific JSON types. Since it supports JSON SQL operations, it only works on backends that have an actual JSON type, currently:

PostgreSQL - see sqlalchemy.dialects.postgresql.JSON and sqlalchemy.dialects.postgresql.JSONB for backend-specific notes

MySQL - see sqlalchemy.dialects.mysql.JSON for backend-specific notes

SQLite as of version 3.9 - see sqlalchemy.dialects.sqlite.JSON for backend-specific notes

Microsoft SQL Server 2016 and later - see sqlalchemy.dialects.mssql.JSON for backend-specific notes

JSON is part of the Core in support of the growing popularity of native JSON datatypes.

The JSON type stores arbitrary JSON format data, e.g.:

JSON-Specific Expression Operators

The JSON datatype provides these additional SQL operations:

Keyed index operations:

Integer index operations:

Path index operations:

Data casters for specific JSON element types, subsequent to an index or path operation being invoked:

Added in version 1.3.11.

Additional operations may be available from the dialect-specific versions of JSON, such as sqlalchemy.dialects.postgresql.JSON and sqlalchemy.dialects.postgresql.JSONB which both offer additional PostgreSQL-specific operations.

Casting JSON Elements to Other Types

Index operations, i.e. those invoked by calling upon the expression using the Python bracket operator as in some_column['some key'], return an expression object whose type defaults to JSON by default, so that further JSON-oriented instructions may be called upon the result type. However, it is likely more common that an index operation is expected to return a specific scalar element, such as a string or integer. In order to provide access to these elements in a backend-agnostic way, a series of data casters are provided:

Comparator.as_string() - return the element as a string

Comparator.as_boolean() - return the element as a boolean

Comparator.as_float() - return the element as a float

Comparator.as_integer() - return the element as an integer

These data casters are implemented by supporting dialects in order to assure that comparisons to the above types will work as expected, such as:

Added in version 1.3.11: Added type-specific casters for the basic JSON data element types.

The data caster functions are new in version 1.3.11, and supersede the previous documented approaches of using CAST; for reference, this looked like:

The above case now works directly as:

For details on the previous comparison approach within the 1.3.x series, see the documentation for SQLAlchemy 1.2 or the included HTML files in the doc/ directory of the version’s distribution.

Detecting Changes in JSON columns when using the ORM

The JSON type, when used with the SQLAlchemy ORM, does not detect in-place mutations to the structure. In order to detect these, the sqlalchemy.ext.mutable extension must be used, most typically using the MutableDict class. This extension will allow “in-place” changes to the datastructure to produce events which will be detected by the unit of work. See the example at HSTORE for a simple example involving a dictionary.

Alternatively, assigning a JSON structure to an ORM element that replaces the old one will always trigger a change event.

Support for JSON null vs. SQL NULL

When working with NULL values, the JSON type recommends the use of two specific constants in order to differentiate between a column that evaluates to SQL NULL, e.g. no value, vs. the JSON-encoded string of "null". To insert or select against a value that is SQL NULL, use the constant null(). This symbol may be passed as a parameter value specifically when using the JSON datatype, which contains special logic that interprets this symbol to mean that the column value should be SQL NULL as opposed to JSON "null":

To insert or select against a value that is JSON "null", use the constant JSON.NULL:

The JSON type supports a flag JSON.none_as_null which when set to True will result in the Python constant None evaluating to the value of SQL NULL, and when set to False results in the Python constant None evaluating to the value of JSON "null". The Python value None may be used in conjunction with either JSON.NULL and null() in order to indicate NULL values, but care must be taken as to the value of the JSON.none_as_null in these cases.

Customizing the JSON Serializer

The JSON serializer and deserializer used by JSON defaults to Python’s json.dumps and json.loads functions; in the case of the psycopg2 dialect, psycopg2 may be using its own custom loader function.

In order to affect the serializer / deserializer, they are currently configurable at the create_engine() level via the create_engine.json_serializer and create_engine.json_deserializer parameters. For example, to turn off ensure_ascii:

Changed in version 1.3.7: SQLite dialect’s json_serializer and json_deserializer parameters renamed from _json_serializer and _json_deserializer.

sqlalchemy.dialects.postgresql.JSON

sqlalchemy.dialects.postgresql.JSONB

sqlalchemy.dialects.mysql.JSON

sqlalchemy.dialects.sqlite.JSON

Consider an indexed value as boolean.

Consider an indexed value as float.

Consider an indexed value as integer.

Consider an indexed value as JSON.

Consider an indexed value as numeric/decimal.

Consider an indexed value as string.

Return a conversion function for processing bind values.

Return a conversion function for processing literal values that are to be rendered directly without using binds.

Describe the json value of NULL.

Construct a JSON type.

Return a conversion function for processing bind values.

Flag, if False, means values from this type aren’t hashable.

Return a conversion function for processing result row values.

inherits from sqlalchemy.types.Comparator, sqlalchemy.types.Comparator

Define comparison operations for JSON.

Consider an indexed value as boolean.

This is similar to using type_coerce, and will usually not apply a CAST().

Added in version 1.3.11.

Consider an indexed value as float.

This is similar to using type_coerce, and will usually not apply a CAST().

Added in version 1.3.11.

Consider an indexed value as integer.

This is similar to using type_coerce, and will usually not apply a CAST().

Added in version 1.3.11.

Consider an indexed value as JSON.

This is similar to using type_coerce, and will usually not apply a CAST().

This is typically the default behavior of indexed elements in any case.

Note that comparison of full JSON structures may not be supported by all backends.

Added in version 1.3.11.

Consider an indexed value as numeric/decimal.

This is similar to using type_coerce, and will usually not apply a CAST().

Added in version 1.4.0b2.

Consider an indexed value as string.

This is similar to using type_coerce, and will usually not apply a CAST().

Added in version 1.3.11.

inherits from sqlalchemy.types.TypeEngine

Common function for index / path elements in a JSON expression.

Return a conversion function for processing bind values.

Returns a callable which will receive a bind parameter value as the sole positional argument and will return a value to send to the DB-API.

If processing is not necessary, the method should return None.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.bind_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.bind_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_bind_param().

Augmenting Existing Types

dialect¶ – Dialect instance in use.

Return a conversion function for processing literal values that are to be rendered directly without using binds.

This function is used when the compiler makes use of the “literal_binds” flag, typically used in DDL generation as well as in certain scenarios where backends don’t accept bound parameters.

Returns a callable which will receive a literal Python value as the sole positional argument and will return a string representation to be rendered in a SQL statement.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.literal_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.literal_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_literal_param().

Augmenting Existing Types

inherits from sqlalchemy.types.JSONElementType

Placeholder for the datatype of a JSON index value.

This allows execution-time processing of JSON index values for special syntaxes.

inherits from sqlalchemy.types.JSONIndexType

Placeholder for the datatype of a JSON index value.

This allows execution-time processing of JSON index values for special syntaxes.

inherits from sqlalchemy.types.JSONElementType

Placeholder type for JSON path operations.

This allows execution-time processing of a path-based index value into a specific SQL syntax.

inherits from sqlalchemy.types.JSONIndexType

Placeholder for the datatype of a JSON index value.

This allows execution-time processing of JSON index values for special syntaxes.

Describe the json value of NULL.

This value is used to force the JSON value of "null" to be used as the value. A value of Python None will be recognized either as SQL NULL or JSON "null", based on the setting of the JSON.none_as_null flag; the JSON.NULL constant can be used to always resolve to JSON "null" regardless of this setting. This is in contrast to the null() construct, which always resolves to SQL NULL. E.g.:

In order to set JSON NULL as a default value for a column, the most transparent method is to use text():

While it is possible to use JSON.NULL in this context, the JSON.NULL value will be returned as the value of the column, which in the context of the ORM or other repurposing of the default value, may not be desirable. Using a SQL expression means the value will be re-fetched from the database within the context of retrieving generated defaults.

Construct a JSON type.

none_as_null=False¶ –

if True, persist the value None as a SQL NULL value, not the JSON encoding of null. Note that when this flag is False, the null() construct can still be used to persist a NULL value, which may be passed directly as a parameter value that is specially interpreted by the JSON type as SQL NULL:

JSON.none_as_null does not apply to the values passed to Column.default and Column.server_default; a value of None passed for these parameters means “no default present”.

Additionally, when used in SQL comparison expressions, the Python value None continues to refer to SQL null, and not JSON NULL. The JSON.none_as_null flag refers explicitly to the persistence of the value within an INSERT or UPDATE statement. The JSON.NULL value should be used for SQL expressions that wish to compare to JSON null.

Return a conversion function for processing bind values.

Returns a callable which will receive a bind parameter value as the sole positional argument and will return a value to send to the DB-API.

If processing is not necessary, the method should return None.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.bind_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.bind_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_bind_param().

Augmenting Existing Types

dialect¶ – Dialect instance in use.

Flag, if False, means values from this type aren’t hashable.

Used by the ORM when uniquing result lists.

Return the Python type object expected to be returned by instances of this type, if known.

Basically, for those types which enforce a return type, or are known across the board to do such for all common DBAPIs (like int for example), will return that type.

If a return type is not defined, raises NotImplementedError.

Note that any type also accommodates NULL in SQL which means you can also get back None from any type in practice.

Return a conversion function for processing result row values.

Returns a callable which will receive a result row column value as the sole positional argument and will return a value to return to the user.

If processing is not necessary, the method should return None.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.result_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.result_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_result_value().

Augmenting Existing Types

dialect¶ – Dialect instance in use.

coltype¶ – DBAPI coltype argument received in cursor.description.

Alias of JSON.none_as_null

inherits from sqlalchemy.types.Integer

The SQL INT or INTEGER type.

Integer - documentation for the base type.

inherits from sqlalchemy.types.Unicode

Create a string-holding type.

inherited from the sqlalchemy.types.String.__init__ method of String

Create a string-holding type.

length¶ – optional, a length for the column for use in DDL and CAST expressions. May be safely omitted if no CREATE TABLE will be issued. Certain databases may require a length for use in DDL, and will raise an exception when the CREATE TABLE DDL is issued if a VARCHAR with no length is included. Whether the value is interpreted as bytes or characters is database specific.

Optional, a column-level collation for use in DDL and CAST expressions. Renders using the COLLATE keyword supported by SQLite, MySQL, and PostgreSQL. E.g.:

In most cases, the Unicode or UnicodeText datatypes should be used for a Column that expects to store non-ascii data. These datatypes will ensure that the correct types are used on the database.

inherits from sqlalchemy.types.Unicode

The SQL NVARCHAR type.

Create a string-holding type.

inherited from the sqlalchemy.types.String.__init__ method of String

Create a string-holding type.

length¶ – optional, a length for the column for use in DDL and CAST expressions. May be safely omitted if no CREATE TABLE will be issued. Certain databases may require a length for use in DDL, and will raise an exception when the CREATE TABLE DDL is issued if a VARCHAR with no length is included. Whether the value is interpreted as bytes or characters is database specific.

Optional, a column-level collation for use in DDL and CAST expressions. Renders using the COLLATE keyword supported by SQLite, MySQL, and PostgreSQL. E.g.:

In most cases, the Unicode or UnicodeText datatypes should be used for a Column that expects to store non-ascii data. These datatypes will ensure that the correct types are used on the database.

inherits from sqlalchemy.types.Numeric

The SQL NUMERIC type.

Numeric - documentation for the base type.

inherited from the sqlalchemy.types.Numeric.__init__ method of Numeric

precision¶ – the numeric precision for use in DDL CREATE TABLE.

scale¶ – the numeric scale for use in DDL CREATE TABLE.

asdecimal¶ – default True. Return whether or not values should be sent as Python Decimal objects, or as floats. Different DBAPIs send one or the other based on datatypes - the Numeric type will ensure that return values are one or the other across DBAPIs consistently.

decimal_return_scale¶ – Default scale to use when converting from floats to Python decimals. Floating point values will typically be much longer due to decimal inaccuracy, and most floating point database types don’t have a notion of “scale”, so by default the float type looks for the first ten decimal places when converting. Specifying this value will override that length. Types which do include an explicit “.scale” value, such as the base Numeric as well as the MySQL float types, will use the value of “.scale” as the default for decimal_return_scale, if not otherwise specified.

When using the Numeric type, care should be taken to ensure that the asdecimal setting is appropriate for the DBAPI in use - when Numeric applies a conversion from Decimal->float or float-> Decimal, this conversion incurs an additional performance overhead for all result columns received.

DBAPIs that return Decimal natively (e.g. psycopg2) will have better accuracy and higher performance with a setting of True, as the native translation to Decimal reduces the amount of floating- point issues at play, and the Numeric type itself doesn’t need to apply any further conversions. However, another DBAPI which returns floats natively will incur an additional conversion overhead, and is still subject to floating point data loss - in which case asdecimal=False will at least remove the extra conversion overhead.

inherits from sqlalchemy.types.Float

Float - documentation for the base type.

inherited from the sqlalchemy.types.Float.__init__ method of Float

the numeric precision for use in DDL CREATE TABLE. Backends should attempt to ensure this precision indicates a number of digits for the generic Float datatype.

For the Oracle Database backend, the Float.precision parameter is not accepted when rendering DDL, as Oracle Database does not support float precision specified as a number of decimal places. Instead, use the Oracle Database-specific FLOAT datatype and specify the FLOAT.binary_precision parameter. This is new in version 2.0 of SQLAlchemy.

To create a database agnostic Float that separately specifies binary precision for Oracle Database, use TypeEngine.with_variant() as follows:

asdecimal¶ – the same flag as that of Numeric, but defaults to False. Note that setting this flag to True results in floating point conversion.

decimal_return_scale¶ – Default scale to use when converting from floats to Python decimals. Floating point values will typically be much longer due to decimal inaccuracy, and most floating point database types don’t have a notion of “scale”, so by default the float type looks for the first ten decimal places when converting. Specifying this value will override that length. Note that the MySQL float types, which do include “scale”, will use “scale” as the default for decimal_return_scale, if not otherwise specified.

inherits from sqlalchemy.types.SmallInteger

The SQL SMALLINT type.

SmallInteger - documentation for the base type.

inherits from sqlalchemy.types.Text

Create a string-holding type.

inherited from the sqlalchemy.types.String.__init__ method of String

Create a string-holding type.

length¶ – optional, a length for the column for use in DDL and CAST expressions. May be safely omitted if no CREATE TABLE will be issued. Certain databases may require a length for use in DDL, and will raise an exception when the CREATE TABLE DDL is issued if a VARCHAR with no length is included. Whether the value is interpreted as bytes or characters is database specific.

Optional, a column-level collation for use in DDL and CAST expressions. Renders using the COLLATE keyword supported by SQLite, MySQL, and PostgreSQL. E.g.:

In most cases, the Unicode or UnicodeText datatypes should be used for a Column that expects to store non-ascii data. These datatypes will ensure that the correct types are used on the database.

inherits from sqlalchemy.types.Time

inherits from sqlalchemy.types.DateTime

The SQL TIMESTAMP type.

TIMESTAMP datatypes have support for timezone storage on some backends, such as PostgreSQL and Oracle Database. Use the TIMESTAMP.timezone argument in order to enable “TIMESTAMP WITH TIMEZONE” for these backends.

Construct a new TIMESTAMP.

Return the corresponding type object from the underlying DB-API, if any.

Construct a new TIMESTAMP.

timezone¶ – boolean. Indicates that the TIMESTAMP type should enable timezone support, if available on the target database. On a per-dialect basis is similar to “TIMESTAMP WITH TIMEZONE”. If the target database does not support timezones, this flag is ignored.

Return the corresponding type object from the underlying DB-API, if any.

This can be useful for calling setinputsizes(), for example.

inherits from sqlalchemy.types.Uuid, sqlalchemy.types.NativeForEmulated

Represent the SQL UUID type.

This is the SQL-native form of the Uuid database agnostic datatype, and is backwards compatible with the previous PostgreSQL-only version of UUID.

The UUID datatype only works on databases that have a SQL datatype named UUID. It will not function for backends which don’t have this exact-named type, including SQL Server. For backend-agnostic UUID values with native support, including for SQL Server’s UNIQUEIDENTIFIER datatype, use the Uuid datatype.

Added in version 2.0.

Construct a UUID type.

Construct a UUID type.

if True, values will be interpreted as Python uuid objects, converting to/from string via the DBAPI.

inherits from sqlalchemy.types._Binary

The SQL VARBINARY type.

inherits from sqlalchemy.types.String

The SQL VARCHAR type.

Create a string-holding type.

inherited from the sqlalchemy.types.String.__init__ method of String

Create a string-holding type.

length¶ – optional, a length for the column for use in DDL and CAST expressions. May be safely omitted if no CREATE TABLE will be issued. Certain databases may require a length for use in DDL, and will raise an exception when the CREATE TABLE DDL is issued if a VARCHAR with no length is included. Whether the value is interpreted as bytes or characters is database specific.

Optional, a column-level collation for use in DDL and CAST expressions. Renders using the COLLATE keyword supported by SQLite, MySQL, and PostgreSQL. E.g.:

In most cases, the Unicode or UnicodeText datatypes should be used for a Column that expects to store non-ascii data. These datatypes will ensure that the correct types are used on the database.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String

metadata_obj = MetaData()

user = Table(
    "user",
    metadata_obj,
    Column("user_name", String, primary_key=True),
    Column("email_address", String(60)),
)
```

Example 2 (python):
```python
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.dialects.mysql import VARCHAR

metadata_obj = MetaData()

user = Table(
    "user",
    metadata_obj,
    Column("user_name", String(100), primary_key=True),
    Column(
        "bio",
        String(255).with_variant(VARCHAR(255, charset="utf8"), "mysql", "mariadb"),
    ),
)
```

Example 3 (python):
```python
import enum
from sqlalchemy import Enum


class MyEnum(enum.Enum):
    one = 1
    two = 2
    three = 3


t = Table("data", MetaData(), Column("value", Enum(MyEnum)))

connection.execute(t.insert(), {"value": MyEnum.two})
assert connection.scalar(t.select()) is MyEnum.two
```

Example 4 (python):
```python
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy.dialects import oracle

Column(
    "float_data",
    Float(5).with_variant(oracle.FLOAT(binary_precision=16), "oracle"),
)
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/tutorial/engine.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Unified Tutorial
    - Project Versions
- Establishing Connectivity - the Engine¶

Home | Download this Documentation

Home | Download this Documentation

SQLAlchemy 1.4 / 2.0 Tutorial

This page is part of the SQLAlchemy Unified Tutorial.

Previous: SQLAlchemy Unified Tutorial | Next: Working with Transactions and the DBAPI

Welcome ORM and Core readers alike!

Every SQLAlchemy application that connects to a database needs to use an Engine. This short section is for everyone.

The start of any SQLAlchemy application is an object called the Engine. This object acts as a central source of connections to a particular database, providing both a factory as well as a holding space called a connection pool for these database connections. The engine is typically a global object created just once for a particular database server, and is configured using a URL string which will describe how it should connect to the database host or backend.

For this tutorial we will use an in-memory-only SQLite database. This is an easy way to test things without needing to have an actual pre-existing database set up. The Engine is created by using the create_engine() function:

The main argument to create_engine is a string URL, above passed as the string "sqlite+pysqlite:///:memory:". This string indicates to the Engine three important facts:

What kind of database are we communicating with? This is the sqlite portion above, which links in SQLAlchemy to an object known as the dialect.

What DBAPI are we using? The Python DBAPI is a third party driver that SQLAlchemy uses to interact with a particular database. In this case, we’re using the name pysqlite, which in modern Python use is the sqlite3 standard library interface for SQLite. If omitted, SQLAlchemy will use a default DBAPI for the particular database selected.

How do we locate the database? In this case, our URL includes the phrase /:memory:, which is an indicator to the sqlite3 module that we will be using an in-memory-only database. This kind of database is perfect for experimenting as it does not require any server nor does it need to create new files.

The Engine, when first returned by create_engine(), has not actually tried to connect to the database yet; that happens only the first time it is asked to perform a task against the database. This is a software design pattern known as lazy initialization.

We have also specified a parameter create_engine.echo, which will instruct the Engine to log all of the SQL it emits to a Python logger that will write to standard out. This flag is a shorthand way of setting up Python logging more formally and is useful for experimentation in scripts. Many of the SQL examples will include this SQL logging output beneath a [SQL] link that when clicked, will reveal the full SQL interaction.

SQLAlchemy 1.4 / 2.0 Tutorial

Next Tutorial Section: Working with Transactions and the DBAPI

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
>>> from sqlalchemy import create_engine
>>> engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
```

---
