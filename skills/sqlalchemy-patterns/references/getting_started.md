# Sqlalchemy - Getting Started

**Pages:** 2

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/intro.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
    - Project Versions
- Overview¶
- Documentation Overview¶
- Code Examples¶
- Installation Guide¶
  - Supported Platforms¶
  - AsyncIO Support¶

Home | Download this Documentation

Home | Download this Documentation

The SQLAlchemy SQL Toolkit and Object Relational Mapper is a comprehensive set of tools for working with databases and Python. It has several distinct areas of functionality which can be used individually or combined together. Its major components are illustrated below, with component dependencies organized into layers:

Above, the two most significant front-facing portions of SQLAlchemy are the Object Relational Mapper (ORM) and the Core.

Core contains the breadth of SQLAlchemy’s SQL and database integration and description services, the most prominent part of this being the SQL Expression Language.

The SQL Expression Language is a toolkit on its own, independent of the ORM package, which provides a system of constructing SQL expressions represented by composable objects, which can then be “executed” against a target database within the scope of a specific transaction, returning a result set. Inserts, updates and deletes (i.e. DML) are achieved by passing SQL expression objects representing these statements along with dictionaries that represent parameters to be used with each statement.

The ORM builds upon Core to provide a means of working with a domain object model mapped to a database schema. When using the ORM, SQL statements are constructed in mostly the same way as when using Core, however the task of DML, which here refers to the persistence of business objects in a database, is automated using a pattern called unit of work, which translates changes in state against mutable objects into INSERT, UPDATE and DELETE constructs which are then invoked in terms of those objects. SELECT statements are also augmented by ORM-specific automations and object-centric querying capabilities.

Whereas working with Core and the SQL Expression language presents a schema-centric view of the database, along with a programming paradigm that is oriented around immutability, the ORM builds on top of this a domain-centric view of the database with a programming paradigm that is more explicitly object-oriented and reliant upon mutability. Since a relational database is itself a mutable service, the difference is that Core/SQL Expression language is command oriented whereas the ORM is state oriented.

The documentation is separated into four sections:

SQLAlchemy Unified Tutorial - this all-new tutorial for the 1.4/2.0 series of SQLAlchemy introduces the entire library holistically, starting from a description of Core and working more and more towards ORM-specific concepts. New users, as well as users coming from the 1.x series of SQLAlchemy, should start here.

SQLAlchemy ORM - In this section, reference documentation for the ORM is presented.

SQLAlchemy Core - Here, reference documentation for everything else within Core is presented. SQLAlchemy engine, connection, and pooling services are also described here.

Dialects - Provides reference documentation for all dialect implementations, including DBAPI specifics.

Working code examples, mostly regarding the ORM, are included in the SQLAlchemy distribution. A description of all the included example applications is at ORM Examples.

There is also a wide variety of examples involving both core SQLAlchemy constructs as well as the ORM on the wiki. See Theatrum Chemicum.

SQLAlchemy supports the following platforms:

cPython 3.7 and higher

Python-3 compatible versions of PyPy

Changed in version 2.0: SQLAlchemy now targets Python 3.7 and above.

SQLAlchemy’s asyncio support depends upon the greenlet project. This dependency will be installed by default on common machine platforms, however is not supported on every architecture and also may not install by default on less common architectures. See the section Asyncio Platform Installation Notes (Including Apple M1) for additional details on ensuring asyncio support is present.

SQLAlchemy installation is via standard Python methodologies that are based on setuptools, either by referring to setup.py directly or by using pip or other setuptools-compatible approaches.

When pip is available, the distribution can be downloaded from PyPI and installed in one step:

This command will download the latest released version of SQLAlchemy from the Python Cheese Shop and install it to your system. For most common platforms, a Python Wheel file will be downloaded which provides native Cython / C extensions prebuilt.

In order to install the latest prerelease version, such as 2.0.0b1, pip requires that the --pre flag be used:

Where above, if the most recent version is a prerelease, it will be installed instead of the latest released version.

When not installing from pip, the source distribution may be installed using the setup.py script:

The source install is platform agnostic and will install on any platform regardless of whether or not Cython / C build tools are installed. As the next section Building the Cython Extensions details, setup.py will attempt to build using Cython / C if possible but will fall back to a pure Python installation otherwise.

SQLAlchemy includes Cython extensions which provide an extra speed boost within various areas, with a current emphasis on the speed of Core result sets.

Changed in version 2.0: The SQLAlchemy C extensions have been rewritten using Cython.

setup.py will automatically build the extensions if an appropriate platform is detected, assuming the Cython package is installed. A complete manual build looks like:

Source builds may also be performed using PEP 517 techniques, such as using build:

If the build of the Cython extensions fails due to Cython not being installed, a missing compiler or other issue, the setup process will output a warning message and re-run the build without the Cython extensions upon completion, reporting final status.

To run the build/install without even attempting to compile the Cython extensions, the DISABLE_SQLALCHEMY_CEXT environment variable may be specified. The use case for this is either for special testing circumstances, or in the rare case of compatibility/build issues not overcome by the usual “rebuild” mechanism:

SQLAlchemy is designed to operate with a DBAPI implementation built for a particular database, and includes support for the most popular databases. The individual database sections in Dialects enumerate the available DBAPIs for each database, including external links.

This documentation covers SQLAlchemy version 2.0. If you’re working on a system that already has SQLAlchemy installed, check the version from your Python prompt like this:

With SQLAlchemy installed, new and old users alike can Proceed to the SQLAlchemy Tutorial.

Notes on the new API released in SQLAlchemy 2.0 is available here at SQLAlchemy 2.0 - Major Migration Guide.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (unknown):
```unknown
pip install SQLAlchemy
```

Example 2 (unknown):
```unknown
pip install --pre SQLAlchemy
```

Example 3 (unknown):
```unknown
python setup.py install
```

Example 4 (markdown):
```markdown
# cd into SQLAlchemy source distribution
cd path/to/sqlalchemy

# install cython
pip install cython

# optionally build Cython extensions ahead of install
python setup.py build_ext

# run the install
python setup.py install
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/quickstart.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- ORM Quick Start¶
- Declare Models¶
- Create an Engine¶
- Emit CREATE TABLE DDL¶
- Create Objects and Persist¶
- Simple SELECT¶

Home | Download this Documentation

Home | Download this Documentation

For new users who want to quickly see what basic ORM use looks like, here’s an abbreviated form of the mappings and examples used in the SQLAlchemy Unified Tutorial. The code here is fully runnable from a clean command line.

As the descriptions in this section are intentionally very short, please proceed to the full SQLAlchemy Unified Tutorial for a much more in-depth description of each of the concepts being illustrated here.

Changed in version 2.0: The ORM Quickstart is updated for the latest PEP 484-aware features using new constructs including mapped_column(). See the section ORM Declarative Models for migration information.

Here, we define module-level constructs that will form the structures which we will be querying from the database. This structure, known as a Declarative Mapping, defines at once both a Python object model, as well as database metadata that describes real SQL tables that exist, or will exist, in a particular database:

The mapping starts with a base class, which above is called Base, and is created by making a simple subclass against the DeclarativeBase class.

Individual mapped classes are then created by making subclasses of Base. A mapped class typically refers to a single particular database table, the name of which is indicated by using the __tablename__ class-level attribute.

Next, columns that are part of the table are declared, by adding attributes that include a special typing annotation called Mapped. The name of each attribute corresponds to the column that is to be part of the database table. The datatype of each column is taken first from the Python datatype that’s associated with each Mapped annotation; int for INTEGER, str for VARCHAR, etc. Nullability derives from whether or not the Optional[] (or its equivalent) type modifier is used. More specific typing information may be indicated using SQLAlchemy type objects in the right side mapped_column() directive, such as the String datatype used above in the User.name column. The association between Python types and SQL types can be customized using the type annotation map.

The mapped_column() directive is used for all column-based attributes that require more specific customization. Besides typing information, this directive accepts a wide variety of arguments that indicate specific details about a database column, including server defaults and constraint information, such as membership within the primary key and foreign keys. The mapped_column() directive accepts a superset of arguments that are accepted by the SQLAlchemy Column class, which is used by SQLAlchemy Core to represent database columns.

All ORM mapped classes require at least one column be declared as part of the primary key, typically by using the Column.primary_key parameter on those mapped_column() objects that should be part of the key. In the above example, the User.id and Address.id columns are marked as primary key.

Taken together, the combination of a string table name as well as a list of column declarations is known in SQLAlchemy as table metadata. Setting up table metadata using both Core and ORM approaches is introduced in the SQLAlchemy Unified Tutorial at Working with Database Metadata. The above mapping is an example of what’s known as Annotated Declarative Table configuration.

Other variants of Mapped are available, most commonly the relationship() construct indicated above. In contrast to the column-based attributes, relationship() denotes a linkage between two ORM classes. In the above example, User.addresses links User to Address, and Address.user links Address to User. The relationship() construct is introduced in the SQLAlchemy Unified Tutorial at Working with ORM Related Objects.

Finally, the above example classes include a __repr__() method, which is not required but is useful for debugging. Mapped classes can be created with methods such as __repr__() generated automatically, using dataclasses. More on dataclass mapping at Declarative Dataclass Mapping.

The Engine is a factory that can create new database connections for us, which also holds onto connections inside of a Connection Pool for fast reuse. For learning purposes, we normally use a SQLite memory-only database for convenience:

The echo=True parameter indicates that SQL emitted by connections will be logged to standard out.

A full intro to the Engine starts at Establishing Connectivity - the Engine.

Using our table metadata and our engine, we can generate our schema at once in our target SQLite database, using a method called MetaData.create_all():

A lot just happened from that bit of Python code we wrote. For a complete overview of what’s going on on with Table metadata, proceed in the Tutorial at Working with Database Metadata.

We are now ready to insert data in the database. We accomplish this by creating instances of User and Address classes, which have an __init__() method already as established automatically by the declarative mapping process. We then pass them to the database using an object called a Session, which makes use of the Engine to interact with the database. The Session.add_all() method is used here to add multiple objects at once, and the Session.commit() method will be used to flush any pending changes to the database and then commit the current database transaction, which is always in progress whenever the Session is used:

It’s recommended that the Session be used in context manager style as above, that is, using the Python with: statement. The Session object represents active database resources so it’s good to make sure it’s closed out when a series of operations are completed. In the next section, we’ll keep a Session opened just for illustration purposes.

Basics on creating a Session are at Executing with an ORM Session and more at Basics of Using a Session.

Then, some varieties of basic persistence operations are introduced at Inserting Rows using the ORM Unit of Work pattern.

With some rows in the database, here’s the simplest form of emitting a SELECT statement to load some objects. To create SELECT statements, we use the select() function to create a new Select object, which we then invoke using a Session. The method that is often useful when querying for ORM objects is the Session.scalars() method, which will return a ScalarResult object that will iterate through the ORM objects we’ve selected:

The above query also made use of the Select.where() method to add WHERE criteria, and also used the ColumnOperators.in_() method that’s part of all SQLAlchemy column-like constructs to use the SQL IN operator.

More detail on how to select objects and individual columns is at Selecting ORM Entities and Columns.

It’s very common to query amongst multiple tables at once, and in SQL the JOIN keyword is the primary way this happens. The Select construct creates joins using the Select.join() method:

The above query illustrates multiple WHERE criteria which are automatically chained together using AND, as well as how to use SQLAlchemy column-like objects to create “equality” comparisons, which uses the overridden Python method ColumnOperators.__eq__() to produce a SQL criteria object.

Some more background on the concepts above are at The WHERE clause and Explicit FROM clauses and JOINs.

The Session object, in conjunction with our ORM-mapped classes User and Address, automatically track changes to the objects as they are made, which result in SQL statements that will be emitted the next time the Session flushes. Below, we change one email address associated with “sandy”, and also add a new email address to “patrick”, after emitting a SELECT to retrieve the row for “patrick”:

Notice when we accessed patrick.addresses, a SELECT was emitted. This is called a lazy load. Background on different ways to access related items using more or less SQL is introduced at Loader Strategies.

A detailed walkthrough on ORM data manipulation starts at Data Manipulation with the ORM.

All things must come to an end, as is the case for some of our database rows - here’s a quick demonstration of two different forms of deletion, both of which are important based on the specific use case.

First we will remove one of the Address objects from the “sandy” user. When the Session next flushes, this will result in the row being deleted. This behavior is something that we configured in our mapping called the delete cascade. We can get a handle to the sandy object by primary key using Session.get(), then work with the object:

The last SELECT above was the lazy load operation proceeding so that the sandy.addresses collection could be loaded, so that we could remove the sandy_address member. There are other ways to go about this series of operations that won’t emit as much SQL.

We can choose to emit the DELETE SQL for what’s set to be changed so far, without committing the transaction, using the Session.flush() method:

Next, we will delete the “patrick” user entirely. For a top-level delete of an object by itself, we use the Session.delete() method; this method doesn’t actually perform the deletion, but sets up the object to be deleted on the next flush. The operation will also cascade to related objects based on the cascade options that we configured, in this case, onto the related Address objects:

The Session.delete() method in this particular case emitted two SELECT statements, even though it didn’t emit a DELETE, which might seem surprising. This is because when the method went to inspect the object, it turns out the patrick object was expired, which happened when we last called upon Session.commit(), and the SQL emitted was to re-load the rows from the new transaction. This expiration is optional, and in normal use we will often be turning it off for situations where it doesn’t apply well.

To illustrate the rows being deleted, here’s the commit:

The Tutorial discusses ORM deletion at Deleting ORM Objects using the Unit of Work pattern. Background on object expiration is at Expiring / Refreshing; cascades are discussed in depth at Cascades.

For a new user, the above sections were likely a whirlwind tour. There’s a lot of important concepts in each step above that weren’t covered. With a quick overview of what things look like, it’s recommended to work through the SQLAlchemy Unified Tutorial to gain a solid working knowledge of what’s really going on above. Good luck!

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
>>> from typing import List
>>> from typing import Optional
>>> from sqlalchemy import ForeignKey
>>> from sqlalchemy import String
>>> from sqlalchemy.orm import DeclarativeBase
>>> from sqlalchemy.orm import Mapped
>>> from sqlalchemy.orm import mapped_column
>>> from sqlalchemy.orm import relationship

>>> class Base(DeclarativeBase):
...     pass

>>> class User(Base):
...     __tablename__ = "user_account"
...
...     id: Mapped[int] = mapped_column(primary_key=True)
...     name: Mapped[str] = mapped_column(String(30))
...     fullname: Mapped[Optional[str]]
...
...     addresses: Mapped[List["Address"]] = relationship(
...         back_populates="user", cascade="all, delete-orphan"
...     )
...
...     def __repr__(self) -> str:
...         return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

>>> class Address(Base):
...     __tablename__ = "address"
...
...     id: Mapped[int] = mapped_column(primary_key=True)
...     email_address: Mapped[str]
...     user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
...
...     user: Mapped["User"] = relationship(back_populates="addresses")
...
...     def __repr__(self) -> str:
...         return f"Address(id={self.id!r}, email_address={self.email_address!r})"
```

Example 2 (python):
```python
>>> from sqlalchemy import create_engine
>>> engine = create_engine("sqlite://", echo=True)
```

Example 3 (sql):
```sql
>>> Base.metadata.create_all(engine)
BEGIN (implicit)
PRAGMA main.table_...info("user_account")
...
PRAGMA main.table_...info("address")
...
CREATE TABLE user_account (
    id INTEGER NOT NULL,
    name VARCHAR(30) NOT NULL,
    fullname VARCHAR,
    PRIMARY KEY (id)
)
...
CREATE TABLE address (
    id INTEGER NOT NULL,
    email_address VARCHAR NOT NULL,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES user_account (id)
)
...
COMMIT
```

Example 4 (sql):
```sql
>>> from sqlalchemy.orm import Session

>>> with Session(engine) as session:
...     spongebob = User(
...         name="spongebob",
...         fullname="Spongebob Squarepants",
...         addresses=[Address(email_address="spongebob@sqlalchemy.org")],
...     )
...     sandy = User(
...         name="sandy",
...         fullname="Sandy Cheeks",
...         addresses=[
...             Address(email_address="sandy@sqlalchemy.org"),
...             Address(email_address="sandy@squirrelpower.org"),
...         ],
...     )
...     patrick = User(name="patrick", fullname="Patrick Star")
...
...     session.add_all([spongebob, sandy, patrick])
...
...     session.commit()
BEGIN (implicit)
INSERT INTO user_account (name, fullname) VALUES (?, ?) RETURNING id
[...] ('spongebob', 'Spongebob Squarepants')
INSERT INTO user_account (name, fullname) VALUES (?, ?) RETURNING id
[...] ('sandy', 'Sandy Cheeks')
INSERT INTO user_account (name, fullname) VALUES (?, ?) RETURNING id
[...] ('patrick', 'Patrick Star')
INSERT INTO address (email_address, user_id) VALUES (?, ?) RETURNING id
[...] ('spongebob@sqlalchemy.org', 1)
INSERT INTO address (email_address, user_id) VALUES (?, ?) RETURNING id
[...] ('sandy@sqlalchemy.org', 2)
INSERT INTO address (email_address, user_id) VALUES (?, ?) RETURNING id
[...] ('sandy@squirrelpower.org', 2)
COMMIT
```

---
