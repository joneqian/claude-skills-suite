# Sqlalchemy - Querying

**Pages:** 8

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/nonstandard_mappings.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Non-Traditional Mappings¶
- Mapping a Class against Multiple Tables¶
- Mapping a Class against Arbitrary Subqueries¶
- Multiple Mappers for One Class¶

Home | Download this Documentation

Home | Download this Documentation

Mappers can be constructed against arbitrary relational units (called selectables) in addition to plain tables. For example, the join() function creates a selectable unit comprised of multiple tables, complete with its own composite primary key, which can be mapped in the same way as a Table:

In the example above, the join expresses columns for both the user and the address table. The user.id and address.user_id columns are equated by foreign key, so in the mapping they are defined as one attribute, AddressUser.id, using column_property() to indicate a specialized column mapping. Based on this part of the configuration, the mapping will copy new primary key values from user.id into the address.user_id column when a flush occurs.

Additionally, the address.id column is mapped explicitly to an attribute named address_id. This is to disambiguate the mapping of the address.id column from the same-named AddressUser.id attribute, which here has been assigned to refer to the user table combined with the address.user_id foreign key.

The natural primary key of the above mapping is the composite of (user.id, address.id), as these are the primary key columns of the user and address table combined together. The identity of an AddressUser object will be in terms of these two values, and is represented from an AddressUser object as (AddressUser.id, AddressUser.address_id).

When referring to the AddressUser.id column, most SQL expressions will make use of only the first column in the list of columns mapped, as the two columns are synonymous. However, for the special use case such as a GROUP BY expression where both columns must be referenced at the same time while making use of the proper context, that is, accommodating for aliases and similar, the accessor Comparator.expressions may be used:

Added in version 1.3.17: Added the Comparator.expressions accessor.

A mapping against multiple tables as illustrated above supports persistence, that is, INSERT, UPDATE and DELETE of rows within the targeted tables. However, it does not support an operation that would UPDATE one table and perform INSERT or DELETE on others at the same time for one record. That is, if a record PtoQ is mapped to tables “p” and “q”, where it has a row based on a LEFT OUTER JOIN of “p” and “q”, if an UPDATE proceeds that is to alter data in the “q” table in an existing record, the row in “q” must exist; it won’t emit an INSERT if the primary key identity is already present. If the row does not exist, for most DBAPI drivers which support reporting the number of rows affected by an UPDATE, the ORM will fail to detect an updated row and raise an error; otherwise, the data would be silently ignored.

A recipe to allow for an on-the-fly “insert” of the related row might make use of the .MapperEvents.before_update event and look like:

where above, a row is INSERTed into the q_table table by creating an INSERT construct with Table.insert(), then executing it using the given Connection which is the same one being used to emit other SQL for the flush process. The user-supplied logic would have to detect that the LEFT OUTER JOIN from “p” to “q” does not have an entry for the “q” side.

Similar to mapping against a join, a plain select() object can be used with a mapper as well. The example fragment below illustrates mapping a class called Customer to a select() which includes a join to a subquery:

Above, the full row represented by customer_select will be all the columns of the customers table, in addition to those columns exposed by the subq subquery, which are order_count, highest_order, and customer_id. Mapping the Customer class to this selectable then creates a class which will contain those attributes.

When the ORM persists new instances of Customer, only the customers table will actually receive an INSERT. This is because the primary key of the orders table is not represented in the mapping; the ORM will only emit an INSERT into a table for which it has mapped the primary key.

The practice of mapping to arbitrary SELECT statements, especially complex ones as above, is almost never needed; it necessarily tends to produce complex queries which are often less efficient than that which would be produced by direct query construction. The practice is to some degree based on the very early history of SQLAlchemy where the Mapper construct was meant to represent the primary querying interface; in modern usage, the Query object can be used to construct virtually any SELECT statement, including complex composites, and should be favored over the “map-to-selectable” approach.

In modern SQLAlchemy, a particular class is mapped by only one so-called primary mapper at a time. This mapper is involved in three main areas of functionality: querying, persistence, and instrumentation of the mapped class. The rationale of the primary mapper relates to the fact that the Mapper modifies the class itself, not only persisting it towards a particular Table, but also instrumenting attributes upon the class which are structured specifically according to the table metadata. It’s not possible for more than one mapper to be associated with a class in equal measure, since only one mapper can actually instrument the class.

The concept of a “non-primary” mapper had existed for many versions of SQLAlchemy however as of version 1.3 this feature is deprecated. The one case where such a non-primary mapper is useful is when constructing a relationship to a class against an alternative selectable. This use case is now suited using the aliased construct and is described at Relationship to Aliased Class.

As far as the use case of a class that can actually be fully persisted to different tables under different scenarios, very early versions of SQLAlchemy offered a feature for this adapted from Hibernate, known as the “entity name” feature. However, this use case became infeasible within SQLAlchemy once the mapped class itself became the source of SQL expression construction; that is, the class’ attributes themselves link directly to mapped table columns. The feature was removed and replaced with a simple recipe-oriented approach to accomplishing this task without any ambiguity of instrumentation - to create new subclasses, each mapped individually. This pattern is now available as a recipe at Entity Name.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (sql):
```sql
from sqlalchemy import Table, Column, Integer, String, MetaData, join, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import column_property

metadata_obj = MetaData()

# define two Table objects
user_table = Table(
    "user",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String),
)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("email_address", String),
)

# define a join between them.  This
# takes place across the user.id and address.user_id
# columns.
user_address_join = join(user_table, address_table)


class Base(DeclarativeBase):
    metadata = metadata_obj


# map to it
class AddressUser(Base):
    __table__ = user_address_join

    id = column_property(user_table.c.id, address_table.c.user_id)
    address_id = address_table.c.id
```

Example 2 (unknown):
```unknown
stmt = select(AddressUser).group_by(*AddressUser.id.expressions)
```

Example 3 (python):
```python
from sqlalchemy import event


@event.listens_for(PtoQ, "before_update")
def receive_before_update(mapper, connection, target):
    if target.some_required_attr_on_q is None:
        connection.execute(q_table.insert(), {"id": target.id})
```

Example 4 (python):
```python
from sqlalchemy import select, func

subq = (
    select(
        func.count(orders.c.id).label("order_count"),
        func.max(orders.c.price).label("highest_order"),
        orders.c.customer_id,
    )
    .group_by(orders.c.customer_id)
    .subquery()
)

customer_select = (
    select(customers, subq)
    .join_from(customers, subq, customers.c.id == subq.c.customer_id)
    .subquery()
)


class Customer(Base):
    __table__ = customer_select
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/core/selectable.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Core
    - Project Versions
- SELECT and Related Constructs¶
- Selectable Foundational Constructors¶
- Selectable Modifier Constructors¶
- Selectable Class Documentation¶
- Label Style Constants¶

Home | Download this Documentation

Home | Download this Documentation

The term “selectable” refers to any object that represents database rows. In SQLAlchemy, these objects descend from Selectable, the most prominent being Select, which represents a SQL SELECT statement. A subset of Selectable is FromClause, which represents objects that can be within the FROM clause of a Select statement. A distinguishing feature of FromClause is the FromClause.c attribute, which is a namespace of all the columns contained within the FROM clause (these elements are themselves ColumnElement subclasses).

Top level “FROM clause” and “SELECT” constructors.

Return an EXCEPT of multiple selectables.

Return an EXCEPT ALL of multiple selectables.

Construct a new Exists construct.

Return an INTERSECT of multiple selectables.

intersect_all(*selects)

Return an INTERSECT ALL of multiple selectables.

select(*entities, **__kw)

Construct a new Select.

table(name, *columns, **kw)

Produce a new TableClause.

Return a UNION of multiple selectables.

Return a UNION ALL of multiple selectables.

values(*columns, [name, literal_binds])

Construct a Values construct representing the SQL VALUES clause.

Return an EXCEPT of multiple selectables.

The returned object is an instance of CompoundSelect.

*selects¶ – a list of Select instances.

Return an EXCEPT ALL of multiple selectables.

The returned object is an instance of CompoundSelect.

*selects¶ – a list of Select instances.

Construct a new Exists construct.

The exists() can be invoked by itself to produce an Exists construct, which will accept simple WHERE criteria:

However, for greater flexibility in constructing the SELECT, an existing Select construct may be converted to an Exists, most conveniently by making use of the SelectBase.exists() method:

The EXISTS criteria is then used inside of an enclosing SELECT:

The above statement will then be of the form:

EXISTS subqueries - in the 2.0 style tutorial.

SelectBase.exists() - method to transform a SELECT to an EXISTS clause.

Return an INTERSECT of multiple selectables.

The returned object is an instance of CompoundSelect.

*selects¶ – a list of Select instances.

Return an INTERSECT ALL of multiple selectables.

The returned object is an instance of CompoundSelect.

*selects¶ – a list of Select instances.

Construct a new Select.

Added in version 1.4: - The select() function now accepts column arguments positionally. The top-level select() function will automatically use the 1.x or 2.x style API based on the incoming arguments; using select() from the sqlalchemy.future module will enforce that only the 2.x style constructor is used.

Similar functionality is also available via the FromClause.select() method on any FromClause.

Using SELECT Statements - in the SQLAlchemy Unified Tutorial

Entities to SELECT from. For Core usage, this is typically a series of ColumnElement and / or FromClause objects which will form the columns clause of the resulting statement. For those objects that are instances of FromClause (typically Table or Alias objects), the FromClause.c collection is extracted to form a collection of ColumnElement objects.

This parameter will also accept TextClause constructs as given, as well as ORM-mapped classes.

Produce a new TableClause.

The object returned is an instance of TableClause, which represents the “syntactical” portion of the schema-level Table object. It may be used to construct lightweight table constructs.

name¶ – Name of the table.

columns¶ – A collection of column() constructs.

The schema name for this table.

Added in version 1.3.18: table() can now accept a schema argument.

Return a UNION of multiple selectables.

The returned object is an instance of CompoundSelect.

A similar union() method is available on all FromClause subclasses.

*selects¶ – a list of Select instances.

**kwargs¶ – available keyword arguments are the same as those of select().

Return a UNION ALL of multiple selectables.

The returned object is an instance of CompoundSelect.

A similar union_all() method is available on all FromClause subclasses.

*selects¶ – a list of Select instances.

Construct a Values construct representing the SQL VALUES clause.

The column expressions and the actual data for Values are given in two separate steps. The constructor receives the column expressions typically as column() constructs, and the data is then passed via the Values.data() method as a list, which can be called multiple times to add more data, e.g.:

Would represent a SQL fragment like:

The values construct has an optional values.name field; when using this field, the PostgreSQL-specific “named VALUES” clause may be generated:

When selecting from the above construct, the name and column names will be listed out using a PostgreSQL-specific syntax:

For a more database-agnostic means of SELECTing named columns from a VALUES expression, the Values.cte() method may be used, which produces a named CTE with explicit column names against the VALUES construct within; this syntax works on PostgreSQL, SQLite, and MariaDB:

Added in version 2.0.42: Added the Values.cte() method to Values

*columns¶ – column expressions, typically composed using column() objects.

name¶ – the name for this VALUES construct. If omitted, the VALUES construct will be unnamed in a SQL expression. Different backends may have different requirements here.

literal_binds¶ – Defaults to False. Whether or not to render the data values inline in the SQL output, rather than using bound parameters.

Functions listed here are more commonly available as methods from FromClause and Selectable elements, for example, the alias() function is usually invoked via the FromClause.alias() method.

alias(selectable[, name, flat])

Return a named alias of the given FromClause.

cte(selectable[, name, recursive])

Return a new CTE, or Common Table Expression instance.

join(left, right[, onclause, isouter, ...])

Produce a Join object, given two FromClause expressions.

lateral(selectable[, name])

Return a Lateral object.

outerjoin(left, right[, onclause, full])

Return an OUTER JOIN clause element.

tablesample(selectable, sampling[, name, seed])

Return a TableSample object.

Return a named alias of the given FromClause.

For Table and Join objects, the return type is the Alias object. Other kinds of NamedFromClause objects may be returned for other kinds of FromClause objects.

The named alias represents any FromClause with an alternate name assigned within SQL, typically using the AS clause when generated, e.g. SELECT * FROM table AS aliasname.

Equivalent functionality is available via the FromClause.alias() method available on all FromClause objects.

selectable¶ – any FromClause subclass, such as a table, select statement, etc.

name¶ – string name to be assigned as the alias. If None, a name will be deterministically generated at compile time. Deterministic means the name is guaranteed to be unique against other constructs used in the same statement, and will also be the same name for each successive compilation of the same statement object.

flat¶ – Will be passed through to if the given selectable is an instance of Join - see Join.alias() for details.

Return a new CTE, or Common Table Expression instance.

Please see HasCTE.cte() for detail on CTE usage.

Produce a Join object, given two FromClause expressions.

would emit SQL along the lines of:

Similar functionality is available given any FromClause object (e.g. such as a Table) using the FromClause.join() method.

left¶ – The left side of the join.

right¶ – the right side of the join; this is any FromClause object such as a Table object, and may also be a selectable-compatible object such as an ORM-mapped class.

onclause¶ – a SQL expression representing the ON clause of the join. If left at None, FromClause.join() will attempt to join the two tables based on a foreign key relationship.

isouter¶ – if True, render a LEFT OUTER JOIN, instead of JOIN.

full¶ – if True, render a FULL OUTER JOIN, instead of JOIN.

FromClause.join() - method form, based on a given left side.

Join - the type of object produced.

Return a Lateral object.

Lateral is an Alias subclass that represents a subquery with the LATERAL keyword applied to it.

The special behavior of a LATERAL subquery is that it appears in the FROM clause of an enclosing SELECT, but may correlate to other FROM clauses of that SELECT. It is a special case of subquery only supported by a small number of backends, currently more recent PostgreSQL versions.

LATERAL correlation - overview of usage.

Return an OUTER JOIN clause element.

The returned object is an instance of Join.

Similar functionality is also available via the FromClause.outerjoin() method on any FromClause.

left¶ – The left side of the join.

right¶ – The right side of the join.

onclause¶ – Optional criterion for the ON clause, is derived from foreign key relationships established between left and right otherwise.

To chain joins together, use the FromClause.join() or FromClause.outerjoin() methods on the resulting Join object.

Return a TableSample object.

TableSample is an Alias subclass that represents a table with the TABLESAMPLE clause applied to it. tablesample() is also available from the FromClause class via the FromClause.tablesample() method.

The TABLESAMPLE clause allows selecting a randomly selected approximate percentage of rows from a table. It supports multiple sampling methods, most commonly BERNOULLI and SYSTEM.

Assuming people with a column people_id, the above statement would render as:

sampling¶ – a float percentage between 0 and 100 or Function.

name¶ – optional alias name

seed¶ – any real-valued SQL expression. When specified, the REPEATABLE sub-clause is also rendered.

The classes here are generated using the constructors listed at Selectable Foundational Constructors and Selectable Modifier Constructors.

Represents an table or selectable alias (AS).

Base class of aliases against tables, subqueries, and other selectables.

Forms the basis of UNION, UNION ALL, and other SELECT-based set operations.

Represent a Common Table Expression.

Mark a ClauseElement as supporting execution.

Represent an EXISTS clause.

Represent an element that can be used within the FROM clause of a SELECT statement.

Base class for SELECT statements where additional elements can be added.

Mixin that declares a class to include CTE support.

Represent a JOIN construct between two FromClause elements.

Represent a LATERAL subquery.

The base-most class for Core constructs that have some concept of columns that can represent rows.

Represent a scalar subquery.

Represent a scalar VALUES construct that can be used as a COLUMN element in a statement.

Represents a SELECT statement.

Mark a class as being selectable.

Base class for SELECT statements.

Represent a subquery of a SELECT.

Represents a minimal “table” construct.

Represent a TABLESAMPLE clause.

An alias against a “table valued” SQL function.

Wrap a TextClause construct within a SelectBase interface.

Represent a VALUES construct that can be used as a FROM element in a statement.

inherits from sqlalchemy.sql.roles.DMLTableRole, sqlalchemy.sql.expression.FromClauseAlias

Represents an table or selectable alias (AS).

Represents an alias, as typically applied to any table or sub-select within a SQL statement using the AS keyword (or without the keyword on certain databases such as Oracle Database).

This object is constructed from the alias() module level function as well as the FromClause.alias() method available on all FromClause subclasses.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

inherits from sqlalchemy.sql.expression.NoInit, sqlalchemy.sql.expression.NamedFromClause

Base class of aliases against tables, subqueries, and other selectables.

Return True if this FromClause is ‘derived’ from the given FromClause.

Return True if this FromClause is ‘derived’ from the given FromClause.

An example would be an Alias of a Table is derived from that Table.

Legacy for dialects that are referring to Alias.original.

inherits from sqlalchemy.sql.expression.HasCompileState, sqlalchemy.sql.expression.GenerativeSelect, sqlalchemy.sql.expression.TypedReturnsRows

Forms the basis of UNION, UNION ALL, and other SELECT-based set operations.

Add one or more CTE constructs to this statement.

Return a named subquery against this SelectBase.

Add a new kind of dialect-specific keyword argument for this class.

Compile this SQL expression.

corresponding_column()

Given a ColumnElement, return the exported ColumnElement object from the Selectable.exported_columns collection of this Selectable which corresponds to that original ColumnElement via a common ancestor column.

Return a new CTE, or Common Table Expression instance.

A collection of keyword arguments specified as dialect-specific options to this construct.

Set non-SQL options for the statement which take effect during execution.

Return an Exists representation of this selectable, which can be used as a column expression.

Return a new selectable with the given FETCH FIRST criterion applied.

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

get_execution_options()

Get the non-SQL options which will take effect during execution.

Retrieve the current label style.

Return a new selectable with the given list of GROUP BY criterion applied.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

Return True if this ReturnsRows is ‘derived’ from the given FromClause.

Return a ‘scalar’ representation of this selectable, embedded as a subquery with a label.

Return a LATERAL alias of this Selectable.

Return a new selectable with the given LIMIT criterion applied.

indicates if this HasCTE as contained within a CTE should compel the CTE to render the column names of this object in the WITH clause.

Return a new selectable with the given OFFSET criterion applied.

Apply options to this statement.

Return a new selectable with the given list of ORDER BY criteria applied.

Replace all occurrences of FromClause ‘old’ with the given Alias object, returning a copy of this FromClause.

Return a ‘scalar’ representation of this selectable, which can be used as a column expression.

A ColumnCollection representing the columns that this SELECT statement or similar construct returns in its result set, not including TextClause constructs.

Apply a ‘grouping’ to this ClauseElement.

Return a new selectable with the specified label style.

Apply LIMIT / OFFSET to this statement based on a slice.

Return a subquery of this SelectBase.

Specify a FOR UPDATE clause for this GenerativeSelect.

inherited from the HasCTE.add_cte() method of HasCTE

Add one or more CTE constructs to this statement.

This method will associate the given CTE constructs with the parent statement such that they will each be unconditionally rendered in the WITH clause of the final statement, even if not referenced elsewhere within the statement or any sub-selects.

The optional HasCTE.add_cte.nest_here parameter when set to True will have the effect that each given CTE will render in a WITH clause rendered directly along with this statement, rather than being moved to the top of the ultimate rendered statement, even if this statement is rendered as a subquery within a larger statement.

This method has two general uses. One is to embed CTE statements that serve some purpose without being referenced explicitly, such as the use case of embedding a DML statement such as an INSERT or UPDATE as a CTE inline with a primary statement that may draw from its results indirectly. The other is to provide control over the exact placement of a particular series of CTE constructs that should remain rendered directly in terms of a particular statement that may be nested in a larger statement.

Above, the “anon_1” CTE is not referenced in the SELECT statement, however still accomplishes the task of running an INSERT statement.

Similarly in a DML-related context, using the PostgreSQL Insert construct to generate an “upsert”:

The above statement renders as:

Added in version 1.4.21.

zero or more CTE constructs.

Changed in version 2.0: Multiple CTE instances are accepted

if True, the given CTE or CTEs will be rendered as though they specified the HasCTE.cte.nesting flag to True when they were added to this HasCTE. Assuming the given CTEs are not referenced in an outer-enclosing statement as well, the CTEs given should render at the level of this statement when this flag is given.

Added in version 2.0.

inherited from the SelectBase.alias() method of SelectBase

Return a named subquery against this SelectBase.

For a SelectBase (as opposed to a FromClause), this returns a Subquery object which behaves mostly the same as the Alias object that is used with a FromClause.

Changed in version 1.4: The SelectBase.alias() method is now a synonym for the SelectBase.subquery() method.

inherited from the DialectKWArgs.argument_for() method of DialectKWArgs

Add a new kind of dialect-specific keyword argument for this class.

The DialectKWArgs.argument_for() method is a per-argument way adding extra arguments to the DefaultDialect.construct_arguments dictionary. This dictionary provides a list of argument names accepted by various schema-level constructs on behalf of a dialect.

New dialects should typically specify this dictionary all at once as a data member of the dialect class. The use case for ad-hoc addition of argument names is typically for end-user code that is also using a custom compilation scheme which consumes the additional arguments.

dialect_name¶ – name of a dialect. The dialect must be locatable, else a NoSuchModuleError is raised. The dialect must also include an existing DefaultDialect.construct_arguments collection, indicating that it participates in the keyword-argument validation and default system, else ArgumentError is raised. If the dialect does not include this collection, then any keyword argument can be specified on behalf of this dialect already. All dialects packaged within SQLAlchemy include this collection, however for third party dialects, support may vary.

argument_name¶ – name of the parameter.

default¶ – default value of the parameter.

inherited from the SelectBase.as_scalar() method of SelectBase

Deprecated since version 1.4: The SelectBase.as_scalar() method is deprecated and will be removed in a future release. Please refer to SelectBase.scalar_subquery().

Deprecated since version 1.4: The SelectBase.c and SelectBase.columns attributes are deprecated and will be removed in a future release; these attributes implicitly create a subquery that should be explicit. Please call SelectBase.subquery() first in order to create a subquery, which then contains this attribute. To access the columns that this SELECT object SELECTs from, use the SelectBase.selected_columns attribute.

inherited from the CompilerElement.compile() method of CompilerElement

Compile this SQL expression.

The return value is a Compiled object. Calling str() or unicode() on the returned value will yield a string representation of the result. The Compiled object also can return a dictionary of bind parameter names and values using the params accessor.

bind¶ – An Connection or Engine which can provide a Dialect in order to generate a Compiled object. If the bind and dialect parameters are both omitted, a default SQL compiler is used.

column_keys¶ – Used for INSERT and UPDATE statements, a list of column names which should be present in the VALUES clause of the compiled statement. If None, all columns from the target table object are rendered.

dialect¶ – A Dialect instance which can generate a Compiled object. This argument takes precedence over the bind argument.

optional dictionary of additional parameters that will be passed through to the compiler within all “visit” methods. This allows any custom flag to be passed through to a custom compilation construct, for example. It is also used for the case of passing the literal_binds flag through:

How do I render SQL expressions as strings, possibly with bound parameters inlined?

inherited from the Selectable.corresponding_column() method of Selectable

Given a ColumnElement, return the exported ColumnElement object from the Selectable.exported_columns collection of this Selectable which corresponds to that original ColumnElement via a common ancestor column.

column¶ – the target ColumnElement to be matched.

require_embedded¶ – only return corresponding columns for the given ColumnElement, if the given ColumnElement is actually present within a sub-element of this Selectable. Normally the column will match if it merely shares a common ancestor with one of the exported columns of this Selectable.

Selectable.exported_columns - the ColumnCollection that is used for the operation.

ColumnCollection.corresponding_column() - implementation method.

inherited from the HasCTE.cte() method of HasCTE

Return a new CTE, or Common Table Expression instance.

Common table expressions are a SQL standard whereby SELECT statements can draw upon secondary statements specified along with the primary statement, using a clause called “WITH”. Special semantics regarding UNION can also be employed to allow “recursive” queries, where a SELECT statement can draw upon the set of rows that have previously been selected.

CTEs can also be applied to DML constructs UPDATE, INSERT and DELETE on some databases, both as a source of CTE rows when combined with RETURNING, as well as a consumer of CTE rows.

SQLAlchemy detects CTE objects, which are treated similarly to Alias objects, as special elements to be delivered to the FROM clause of the statement as well as to a WITH clause at the top of the statement.

For special prefixes such as PostgreSQL “MATERIALIZED” and “NOT MATERIALIZED”, the CTE.prefix_with() method may be used to establish these.

Changed in version 1.3.13: Added support for prefixes. In particular - MATERIALIZED and NOT MATERIALIZED.

name¶ – name given to the common table expression. Like FromClause.alias(), the name can be left as None in which case an anonymous symbol will be used at query compile time.

recursive¶ – if True, will render WITH RECURSIVE. A recursive common table expression is intended to be used in conjunction with UNION ALL in order to derive rows from those already selected.

if True, will render the CTE locally to the statement in which it is referenced. For more complex scenarios, the HasCTE.add_cte() method using the HasCTE.add_cte.nest_here parameter may also be used to more carefully control the exact placement of a particular CTE.

Added in version 1.4.24.

The following examples include two from PostgreSQL’s documentation at https://www.postgresql.org/docs/current/static/queries-with.html, as well as additional examples.

Example 1, non recursive:

Example 2, WITH RECURSIVE:

Example 3, an upsert using UPDATE and INSERT with CTEs:

Example 4, Nesting CTE (SQLAlchemy 1.4.24 and above):

The above query will render the second CTE nested inside the first, shown with inline parameters below as:

The same CTE can be set up using the HasCTE.add_cte() method as follows (SQLAlchemy 2.0 and above):

Example 5, Non-Linear CTE (SQLAlchemy 1.4.28 and above):

The above query will render 2 UNIONs inside the recursive CTE:

Query.cte() - ORM version of HasCTE.cte().

A collection of keyword arguments specified as dialect-specific options to this construct.

The arguments are present here in their original <dialect>_<kwarg> format. Only arguments that were actually passed are included; unlike the DialectKWArgs.dialect_options collection, which contains all options known by this dialect including defaults.

The collection is also writable; keys are accepted of the form <dialect>_<kwarg> where the value will be assembled into the list of options.

DialectKWArgs.dialect_options - nested dictionary form

inherited from the DialectKWArgs.dialect_options attribute of DialectKWArgs

A collection of keyword arguments specified as dialect-specific options to this construct.

This is a two-level nested registry, keyed to <dialect_name> and <argument_name>. For example, the postgresql_where argument would be locatable as:

Added in version 0.9.2.

DialectKWArgs.dialect_kwargs - flat dictionary form

inherited from the Executable.execution_options() method of Executable

Set non-SQL options for the statement which take effect during execution.

Execution options can be set at many scopes, including per-statement, per-connection, or per execution, using methods such as Connection.execution_options() and parameters which accept a dictionary of options such as Connection.execute.execution_options and Session.execute.execution_options.

The primary characteristic of an execution option, as opposed to other kinds of options such as ORM loader options, is that execution options never affect the compiled SQL of a query, only things that affect how the SQL statement itself is invoked or how results are fetched. That is, execution options are not part of what’s accommodated by SQL compilation nor are they considered part of the cached state of a statement.

The Executable.execution_options() method is generative, as is the case for the method as applied to the Engine and Query objects, which means when the method is called, a copy of the object is returned, which applies the given parameters to that new copy, but leaves the original unchanged:

An exception to this behavior is the Connection object, where the Connection.execution_options() method is explicitly not generative.

The kinds of options that may be passed to Executable.execution_options() and other related methods and parameter dictionaries include parameters that are explicitly consumed by SQLAlchemy Core or ORM, as well as arbitrary keyword arguments not defined by SQLAlchemy, which means the methods and/or parameter dictionaries may be used for user-defined parameters that interact with custom code, which may access the parameters using methods such as Executable.get_execution_options() and Connection.get_execution_options(), or within selected event hooks using a dedicated execution_options event parameter such as ConnectionEvents.before_execute.execution_options or ORMExecuteState.execution_options, e.g.:

Within the scope of options that are explicitly recognized by SQLAlchemy, most apply to specific classes of objects and not others. The most common execution options include:

Connection.execution_options.isolation_level - sets the isolation level for a connection or a class of connections via an Engine. This option is accepted only by Connection or Engine.

Connection.execution_options.stream_results - indicates results should be fetched using a server side cursor; this option is accepted by Connection, by the Connection.execute.execution_options parameter on Connection.execute(), and additionally by Executable.execution_options() on a SQL statement object, as well as by ORM constructs like Session.execute().

Connection.execution_options.compiled_cache - indicates a dictionary that will serve as the SQL compilation cache for a Connection or Engine, as well as for ORM methods like Session.execute(). Can be passed as None to disable caching for statements. This option is not accepted by Executable.execution_options() as it is inadvisable to carry along a compilation cache within a statement object.

Connection.execution_options.schema_translate_map - a mapping of schema names used by the Schema Translate Map feature, accepted by Connection, Engine, Executable, as well as by ORM constructs like Session.execute().

Connection.execution_options()

Connection.execute.execution_options

Session.execute.execution_options

ORM Execution Options - documentation on all ORM-specific execution options

inherited from the SelectBase.exists() method of SelectBase

Return an Exists representation of this selectable, which can be used as a column expression.

The returned object is an instance of Exists.

EXISTS subqueries - in the 2.0 style tutorial.

Added in version 1.4.

A ColumnCollection that represents the “exported” columns of this Selectable, not including TextClause constructs.

The “exported” columns for a SelectBase object are synonymous with the SelectBase.selected_columns collection.

Added in version 1.4.

Select.exported_columns

Selectable.exported_columns

FromClause.exported_columns

inherited from the GenerativeSelect.fetch() method of GenerativeSelect

Return a new selectable with the given FETCH FIRST criterion applied.

This is a numeric value which usually renders as FETCH {FIRST | NEXT} [ count ] {ROW | ROWS} {ONLY | WITH TIES} expression in the resulting select. This functionality is is currently implemented for Oracle Database, PostgreSQL, MSSQL.

Use GenerativeSelect.offset() to specify the offset.

The GenerativeSelect.fetch() method will replace any clause applied with GenerativeSelect.limit().

Added in version 1.4.

count¶ – an integer COUNT parameter, or a SQL expression that provides an integer result. When percent=True this will represent the percentage of rows to return, not the absolute value. Pass None to reset it.

with_ties¶ – When True, the WITH TIES option is used to return any additional rows that tie for the last place in the result set according to the ORDER BY clause. The ORDER BY may be mandatory in this case. Defaults to False

percent¶ – When True, count represents the percentage of the total number of selected rows to return. Defaults to False

Additional dialect-specific keyword arguments may be accepted by dialects.

Added in version 2.0.41.

GenerativeSelect.limit()

GenerativeSelect.offset()

inherited from the HasTraverseInternals.get_children() method of HasTraverseInternals

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

This is used for visit traversal.

**kw may contain flags that change the collection that is returned, for example to return a subset of items in order to cut down on larger traversals, or to return child items from a different context (such as schema-level collections instead of clause-level).

inherited from the Executable.get_execution_options() method of Executable

Get the non-SQL options which will take effect during execution.

Added in version 1.3.

Executable.execution_options()

inherited from the GenerativeSelect.get_label_style() method of GenerativeSelect

Retrieve the current label style.

Added in version 1.4.

inherited from the GenerativeSelect.group_by() method of GenerativeSelect

Return a new selectable with the given list of GROUP BY criterion applied.

All existing GROUP BY settings can be suppressed by passing None.

a series of ColumnElement constructs which will be used to generate an GROUP BY clause.

Alternatively, an individual entry may also be the string name of a label located elsewhere in the columns clause of the statement which will be matched and rendered in a backend-specific way based on context; see Ordering or Grouping by a Label for background on string label matching in ORDER BY and GROUP BY expressions.

Aggregate functions with GROUP BY / HAVING - in the SQLAlchemy Unified Tutorial

Ordering or Grouping by a Label - in the SQLAlchemy Unified Tutorial

inherited from the HasCacheKey.inherit_cache attribute of HasCacheKey

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

Return True if this ReturnsRows is ‘derived’ from the given FromClause.

An example would be an Alias of a Table is derived from that Table.

A synonym for DialectKWArgs.dialect_kwargs.

inherited from the SelectBase.label() method of SelectBase

Return a ‘scalar’ representation of this selectable, embedded as a subquery with a label.

SelectBase.scalar_subquery().

inherited from the SelectBase.lateral() method of SelectBase

Return a LATERAL alias of this Selectable.

The return value is the Lateral construct also provided by the top-level lateral() function.

LATERAL correlation - overview of usage.

inherited from the GenerativeSelect.limit() method of GenerativeSelect

Return a new selectable with the given LIMIT criterion applied.

This is a numerical value which usually renders as a LIMIT expression in the resulting select. Backends that don’t support LIMIT will attempt to provide similar functionality.

The GenerativeSelect.limit() method will replace any clause applied with GenerativeSelect.fetch().

limit¶ – an integer LIMIT parameter, or a SQL expression that provides an integer result. Pass None to reset it.

GenerativeSelect.fetch()

GenerativeSelect.offset()

inherited from the HasCTE.name_cte_columns attribute of HasCTE

indicates if this HasCTE as contained within a CTE should compel the CTE to render the column names of this object in the WITH clause.

Added in version 2.0.42.

inherited from the GenerativeSelect.offset() method of GenerativeSelect

Return a new selectable with the given OFFSET criterion applied.

This is a numeric value which usually renders as an OFFSET expression in the resulting select. Backends that don’t support OFFSET will attempt to provide similar functionality.

offset¶ – an integer OFFSET parameter, or a SQL expression that provides an integer result. Pass None to reset it.

GenerativeSelect.limit()

GenerativeSelect.fetch()

inherited from the Executable.options() method of Executable

Apply options to this statement.

In the general sense, options are any kind of Python object that can be interpreted by the SQL compiler for the statement. These options can be consumed by specific dialects or specific kinds of compilers.

The most commonly known kind of option are the ORM level options that apply “eager load” and other loading behaviors to an ORM query. However, options can theoretically be used for many other purposes.

For background on specific kinds of options for specific kinds of statements, refer to the documentation for those option objects.

Changed in version 1.4: - added Executable.options() to Core statement objects towards the goal of allowing unified Core / ORM querying capabilities.

Column Loading Options - refers to options specific to the usage of ORM queries

Relationship Loading with Loader Options - refers to options specific to the usage of ORM queries

inherited from the GenerativeSelect.order_by() method of GenerativeSelect

Return a new selectable with the given list of ORDER BY criteria applied.

Calling this method multiple times is equivalent to calling it once with all the clauses concatenated. All existing ORDER BY criteria may be cancelled by passing None by itself. New ORDER BY criteria may then be added by invoking Query.order_by() again, e.g.:

a series of ColumnElement constructs which will be used to generate an ORDER BY clause.

Alternatively, an individual entry may also be the string name of a label located elsewhere in the columns clause of the statement which will be matched and rendered in a backend-specific way based on context; see Ordering or Grouping by a Label for background on string label matching in ORDER BY and GROUP BY expressions.

ORDER BY - in the SQLAlchemy Unified Tutorial

Ordering or Grouping by a Label - in the SQLAlchemy Unified Tutorial

inherited from the Selectable.replace_selectable() method of Selectable

Replace all occurrences of FromClause ‘old’ with the given Alias object, returning a copy of this FromClause.

Deprecated since version 1.4: The Selectable.replace_selectable() method is deprecated, and will be removed in a future release. Similar functionality is available via the sqlalchemy.sql.visitors module.

inherited from the SelectBase.scalar_subquery() method of SelectBase

Return a ‘scalar’ representation of this selectable, which can be used as a column expression.

The returned object is an instance of ScalarSelect.

Typically, a select statement which has only one column in its columns clause is eligible to be used as a scalar expression. The scalar subquery can then be used in the WHERE clause or columns clause of an enclosing SELECT.

Note that the scalar subquery differentiates from the FROM-level subquery that can be produced using the SelectBase.subquery() method.

Scalar and Correlated Subqueries - in the 2.0 tutorial

inherited from the SelectBase.select() method of SelectBase

Deprecated since version 1.4: The SelectBase.select() method is deprecated and will be removed in a future release; this method implicitly creates a subquery that should be explicit. Please call SelectBase.subquery() first in order to create a subquery, which then can be selected.

A ColumnCollection representing the columns that this SELECT statement or similar construct returns in its result set, not including TextClause constructs.

For a CompoundSelect, the CompoundSelect.selected_columns attribute returns the selected columns of the first SELECT statement contained within the series of statements within the set operation.

Select.selected_columns

Added in version 1.4.

Apply a ‘grouping’ to this ClauseElement.

This method is overridden by subclasses to return a “grouping” construct, i.e. parenthesis. In particular it’s used by “binary” expressions to provide a grouping around themselves when placed into a larger expression, as well as by select() constructs when placed into the FROM clause of another select(). (Note that subqueries should be normally created using the Select.alias() method, as many platforms require nested SELECT statements to be named).

As expressions are composed together, the application of self_group() is automatic - end-user code should never need to use this method directly. Note that SQLAlchemy’s clause constructs take operator precedence into account - so parenthesis might not be needed, for example, in an expression like x OR (y AND z) - AND takes precedence over OR.

The base self_group() method of ClauseElement just returns self.

Return a new selectable with the specified label style.

There are three “label styles” available, SelectLabelStyle.LABEL_STYLE_DISAMBIGUATE_ONLY, SelectLabelStyle.LABEL_STYLE_TABLENAME_PLUS_COL, and SelectLabelStyle.LABEL_STYLE_NONE. The default style is SelectLabelStyle.LABEL_STYLE_DISAMBIGUATE_ONLY.

In modern SQLAlchemy, there is not generally a need to change the labeling style, as per-expression labels are more effectively used by making use of the ColumnElement.label() method. In past versions, LABEL_STYLE_TABLENAME_PLUS_COL was used to disambiguate same-named columns from different tables, aliases, or subqueries; the newer LABEL_STYLE_DISAMBIGUATE_ONLY now applies labels only to names that conflict with an existing name so that the impact of this labeling is minimal.

The rationale for disambiguation is mostly so that all column expressions are available from a given FromClause.c collection when a subquery is created.

Added in version 1.4: - the GenerativeSelect.set_label_style() method replaces the previous combination of .apply_labels(), .with_labels() and use_labels=True methods and/or parameters.

LABEL_STYLE_DISAMBIGUATE_ONLY

LABEL_STYLE_TABLENAME_PLUS_COL

inherited from the GenerativeSelect.slice() method of GenerativeSelect

Apply LIMIT / OFFSET to this statement based on a slice.

The start and stop indices behave like the argument to Python’s built-in range() function. This method provides an alternative to using LIMIT/OFFSET to get a slice of the query.

The GenerativeSelect.slice() method will replace any clause applied with GenerativeSelect.fetch().

Added in version 1.4: Added the GenerativeSelect.slice() method generalized from the ORM.

GenerativeSelect.limit()

GenerativeSelect.offset()

GenerativeSelect.fetch()

inherited from the SelectBase.subquery() method of SelectBase

Return a subquery of this SelectBase.

A subquery is from a SQL perspective a parenthesized, named construct that can be placed in the FROM clause of another SELECT statement.

Given a SELECT statement such as:

The above statement might look like:

The subquery form by itself renders the same way, however when embedded into the FROM clause of another SELECT statement, it becomes a named sub-element:

The above renders as:

Historically, SelectBase.subquery() is equivalent to calling the FromClause.alias() method on a FROM object; however, as a SelectBase object is not directly FROM object, the SelectBase.subquery() method provides clearer semantics.

Added in version 1.4.

inherited from the GenerativeSelect.with_for_update() method of GenerativeSelect

Specify a FOR UPDATE clause for this GenerativeSelect.

On a database like PostgreSQL or Oracle Database, the above would render a statement like:

on other backends, the nowait option is ignored and instead would produce:

When called with no arguments, the statement will render with the suffix FOR UPDATE. Additional arguments can then be provided which allow for common database-specific variants.

nowait¶ – boolean; will render FOR UPDATE NOWAIT on Oracle Database and PostgreSQL dialects.

read¶ – boolean; will render LOCK IN SHARE MODE on MySQL, FOR SHARE on PostgreSQL. On PostgreSQL, when combined with nowait, will render FOR SHARE NOWAIT.

of¶ – SQL expression or list of SQL expression elements, (typically Column objects or a compatible expression, for some backends may also be a table expression) which will render into a FOR UPDATE OF clause; supported by PostgreSQL, Oracle Database, some MySQL versions and possibly others. May render as a table or as a column depending on backend.

skip_locked¶ – boolean, will render FOR UPDATE SKIP LOCKED on Oracle Database and PostgreSQL dialects or FOR SHARE SKIP LOCKED if read=True is also specified.

key_share¶ – boolean, will render FOR NO KEY UPDATE, or if combined with read=True will render FOR KEY SHARE, on the PostgreSQL dialect.

inherits from sqlalchemy.sql.roles.DMLTableRole, sqlalchemy.sql.roles.IsCTERole, sqlalchemy.sql.expression.Generative, sqlalchemy.sql.expression.HasPrefixes, sqlalchemy.sql.expression.HasSuffixes, sqlalchemy.sql.expression.AliasedReturnsRows

Represent a Common Table Expression.

The CTE object is obtained using the SelectBase.cte() method from any SELECT statement. A less often available syntax also allows use of the HasCTE.cte() method present on DML constructs such as Insert, Update and Delete. See the HasCTE.cte() method for usage details on CTEs.

Subqueries and CTEs - in the 2.0 tutorial

HasCTE.cte() - examples of calling styles

Return an Alias of this CTE.

Return a new CTE with a SQL UNION of the original CTE against the given selectables provided as positional arguments.

Return a new CTE with a SQL UNION ALL of the original CTE against the given selectables provided as positional arguments.

Return an Alias of this CTE.

This method is a CTE-specific specialization of the FromClause.alias() method.

Return a new CTE with a SQL UNION of the original CTE against the given selectables provided as positional arguments.

one or more elements with which to create a UNION.

Changed in version 1.4.28: multiple elements are now accepted.

HasCTE.cte() - examples of calling styles

Return a new CTE with a SQL UNION ALL of the original CTE against the given selectables provided as positional arguments.

one or more elements with which to create a UNION.

Changed in version 1.4.28: multiple elements are now accepted.

HasCTE.cte() - examples of calling styles

inherits from sqlalchemy.sql.roles.StatementRole

Mark a ClauseElement as supporting execution.

Executable is a superclass for all “statement” types of objects, including select(), delete(), update(), insert(), text().

Set non-SQL options for the statement which take effect during execution.

get_execution_options()

Get the non-SQL options which will take effect during execution.

Apply options to this statement.

Set non-SQL options for the statement which take effect during execution.

Execution options can be set at many scopes, including per-statement, per-connection, or per execution, using methods such as Connection.execution_options() and parameters which accept a dictionary of options such as Connection.execute.execution_options and Session.execute.execution_options.

The primary characteristic of an execution option, as opposed to other kinds of options such as ORM loader options, is that execution options never affect the compiled SQL of a query, only things that affect how the SQL statement itself is invoked or how results are fetched. That is, execution options are not part of what’s accommodated by SQL compilation nor are they considered part of the cached state of a statement.

The Executable.execution_options() method is generative, as is the case for the method as applied to the Engine and Query objects, which means when the method is called, a copy of the object is returned, which applies the given parameters to that new copy, but leaves the original unchanged:

An exception to this behavior is the Connection object, where the Connection.execution_options() method is explicitly not generative.

The kinds of options that may be passed to Executable.execution_options() and other related methods and parameter dictionaries include parameters that are explicitly consumed by SQLAlchemy Core or ORM, as well as arbitrary keyword arguments not defined by SQLAlchemy, which means the methods and/or parameter dictionaries may be used for user-defined parameters that interact with custom code, which may access the parameters using methods such as Executable.get_execution_options() and Connection.get_execution_options(), or within selected event hooks using a dedicated execution_options event parameter such as ConnectionEvents.before_execute.execution_options or ORMExecuteState.execution_options, e.g.:

Within the scope of options that are explicitly recognized by SQLAlchemy, most apply to specific classes of objects and not others. The most common execution options include:

Connection.execution_options.isolation_level - sets the isolation level for a connection or a class of connections via an Engine. This option is accepted only by Connection or Engine.

Connection.execution_options.stream_results - indicates results should be fetched using a server side cursor; this option is accepted by Connection, by the Connection.execute.execution_options parameter on Connection.execute(), and additionally by Executable.execution_options() on a SQL statement object, as well as by ORM constructs like Session.execute().

Connection.execution_options.compiled_cache - indicates a dictionary that will serve as the SQL compilation cache for a Connection or Engine, as well as for ORM methods like Session.execute(). Can be passed as None to disable caching for statements. This option is not accepted by Executable.execution_options() as it is inadvisable to carry along a compilation cache within a statement object.

Connection.execution_options.schema_translate_map - a mapping of schema names used by the Schema Translate Map feature, accepted by Connection, Engine, Executable, as well as by ORM constructs like Session.execute().

Connection.execution_options()

Connection.execute.execution_options

Session.execute.execution_options

ORM Execution Options - documentation on all ORM-specific execution options

Get the non-SQL options which will take effect during execution.

Added in version 1.3.

Executable.execution_options()

Apply options to this statement.

In the general sense, options are any kind of Python object that can be interpreted by the SQL compiler for the statement. These options can be consumed by specific dialects or specific kinds of compilers.

The most commonly known kind of option are the ORM level options that apply “eager load” and other loading behaviors to an ORM query. However, options can theoretically be used for many other purposes.

For background on specific kinds of options for specific kinds of statements, refer to the documentation for those option objects.

Changed in version 1.4: - added Executable.options() to Core statement objects towards the goal of allowing unified Core / ORM querying capabilities.

Column Loading Options - refers to options specific to the usage of ORM queries

Relationship Loading with Loader Options - refers to options specific to the usage of ORM queries

inherits from sqlalchemy.sql.expression.UnaryExpression

Represent an EXISTS clause.

See exists() for a description of usage.

An EXISTS clause can also be constructed from a select() instance by calling SelectBase.exists().

Apply correlation to the subquery noted by this Exists.

Apply correlation to the subquery noted by this Exists.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

Return a SELECT of this Exists.

Return a new Exists construct, applying the given expression to the Select.select_from() method of the select statement contained.

Return a new exists() construct with the given expression added to its WHERE clause, joined to the existing clause via AND, if any.

Apply correlation to the subquery noted by this Exists.

ScalarSelect.correlate()

Apply correlation to the subquery noted by this Exists.

ScalarSelect.correlate_except()

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

Return a SELECT of this Exists.

This will produce a statement resembling:

select() - general purpose method which allows for arbitrary column lists.

Return a new Exists construct, applying the given expression to the Select.select_from() method of the select statement contained.

it is typically preferable to build a Select statement first, including the desired WHERE clause, then use the SelectBase.exists() method to produce an Exists object at once.

Return a new exists() construct with the given expression added to its WHERE clause, joined to the existing clause via AND, if any.

it is typically preferable to build a Select statement first, including the desired WHERE clause, then use the SelectBase.exists() method to produce an Exists object at once.

inherits from sqlalchemy.sql.roles.AnonymizedFromClauseRole, sqlalchemy.sql.expression.Selectable

Represent an element that can be used within the FROM clause of a SELECT statement.

The most common forms of FromClause are the Table and the select() constructs. Key features common to all FromClause objects include:

a c collection, which provides per-name access to a collection of ColumnElement objects.

a primary_key attribute, which is a collection of all those ColumnElement objects that indicate the primary_key flag.

Methods to generate various derivations of a “from” clause, including FromClause.alias(), FromClause.join(), FromClause.select().

Return an alias of this FromClause.

A synonym for FromClause.columns

A named-based collection of ColumnElement objects maintained by this FromClause.

A brief description of this FromClause.

Return a namespace used for name-based access in SQL expressions.

A ColumnCollection that represents the “exported” columns of this Selectable.

Return the collection of ForeignKey marker objects which this FromClause references.

Return True if this FromClause is ‘derived’ from the given FromClause.

Return a Join from this FromClause to another FromClause.

Return a Join from this FromClause to another FromClause, with the “isouter” flag set to True.

Return the iterable collection of Column objects which comprise the primary key of this _selectable.FromClause.

Define the ‘schema’ attribute for this FromClause.

Return a SELECT of this FromClause.

Return a TABLESAMPLE alias of this FromClause.

Return an alias of this FromClause.

The above code creates an Alias object which can be used as a FROM clause in any SELECT statement.

A synonym for FromClause.columns

A named-based collection of ColumnElement objects maintained by this FromClause.

The columns, or c collection, is the gateway to the construction of SQL expressions using table-bound or other selectable-bound columns:

a ColumnCollection object.

A brief description of this FromClause.

Used primarily for error message formatting.

Return a namespace used for name-based access in SQL expressions.

This is the namespace that is used to resolve “filter_by()” type expressions, such as:

It defaults to the .c collection, however internally it can be overridden using the “entity_namespace” annotation to deliver alternative results.

A ColumnCollection that represents the “exported” columns of this Selectable.

The “exported” columns for a FromClause object are synonymous with the FromClause.columns collection.

Added in version 1.4.

Selectable.exported_columns

SelectBase.exported_columns

Return the collection of ForeignKey marker objects which this FromClause references.

Each ForeignKey is a member of a Table-wide ForeignKeyConstraint.

Table.foreign_key_constraints

Return True if this FromClause is ‘derived’ from the given FromClause.

An example would be an Alias of a Table is derived from that Table.

Return a Join from this FromClause to another FromClause.

would emit SQL along the lines of:

right¶ – the right side of the join; this is any FromClause object such as a Table object, and may also be a selectable-compatible object such as an ORM-mapped class.

onclause¶ – a SQL expression representing the ON clause of the join. If left at None, FromClause.join() will attempt to join the two tables based on a foreign key relationship.

isouter¶ – if True, render a LEFT OUTER JOIN, instead of JOIN.

full¶ – if True, render a FULL OUTER JOIN, instead of LEFT OUTER JOIN. Implies FromClause.join.isouter.

join() - standalone function

Join - the type of object produced

Return a Join from this FromClause to another FromClause, with the “isouter” flag set to True.

The above is equivalent to:

right¶ – the right side of the join; this is any FromClause object such as a Table object, and may also be a selectable-compatible object such as an ORM-mapped class.

onclause¶ – a SQL expression representing the ON clause of the join. If left at None, FromClause.join() will attempt to join the two tables based on a foreign key relationship.

full¶ – if True, render a FULL OUTER JOIN, instead of LEFT OUTER JOIN.

Return the iterable collection of Column objects which comprise the primary key of this _selectable.FromClause.

For a Table object, this collection is represented by the PrimaryKeyConstraint which itself is an iterable collection of Column objects.

Define the ‘schema’ attribute for this FromClause.

This is typically None for most objects except that of Table, where it is taken as the value of the Table.schema argument.

Return a SELECT of this FromClause.

select() - general purpose method which allows for arbitrary column lists.

Return a TABLESAMPLE alias of this FromClause.

The return value is the TableSample construct also provided by the top-level tablesample() function.

tablesample() - usage guidelines and parameters

inherits from sqlalchemy.sql.expression.DialectKWArgs, sqlalchemy.sql.expression.SelectBase, sqlalchemy.sql.expression.Generative

Base class for SELECT statements where additional elements can be added.

This serves as the base for Select and CompoundSelect where elements such as ORDER BY, GROUP BY can be added and column rendering can be controlled. Compare to TextualSelect, which, while it subclasses SelectBase and is also a SELECT construct, represents a fixed textual string which cannot be altered at this level, only wrapped as a subquery.

Return a new selectable with the given FETCH FIRST criterion applied.

Retrieve the current label style.

Return a new selectable with the given list of GROUP BY criterion applied.

Return a new selectable with the given LIMIT criterion applied.

Return a new selectable with the given OFFSET criterion applied.

Return a new selectable with the given list of ORDER BY criteria applied.

Return a new selectable with the specified label style.

Apply LIMIT / OFFSET to this statement based on a slice.

Specify a FOR UPDATE clause for this GenerativeSelect.

Return a new selectable with the given FETCH FIRST criterion applied.

This is a numeric value which usually renders as FETCH {FIRST | NEXT} [ count ] {ROW | ROWS} {ONLY | WITH TIES} expression in the resulting select. This functionality is is currently implemented for Oracle Database, PostgreSQL, MSSQL.

Use GenerativeSelect.offset() to specify the offset.

The GenerativeSelect.fetch() method will replace any clause applied with GenerativeSelect.limit().

Added in version 1.4.

count¶ – an integer COUNT parameter, or a SQL expression that provides an integer result. When percent=True this will represent the percentage of rows to return, not the absolute value. Pass None to reset it.

with_ties¶ – When True, the WITH TIES option is used to return any additional rows that tie for the last place in the result set according to the ORDER BY clause. The ORDER BY may be mandatory in this case. Defaults to False

percent¶ – When True, count represents the percentage of the total number of selected rows to return. Defaults to False

Additional dialect-specific keyword arguments may be accepted by dialects.

Added in version 2.0.41.

GenerativeSelect.limit()

GenerativeSelect.offset()

Retrieve the current label style.

Added in version 1.4.

Return a new selectable with the given list of GROUP BY criterion applied.

All existing GROUP BY settings can be suppressed by passing None.

a series of ColumnElement constructs which will be used to generate an GROUP BY clause.

Alternatively, an individual entry may also be the string name of a label located elsewhere in the columns clause of the statement which will be matched and rendered in a backend-specific way based on context; see Ordering or Grouping by a Label for background on string label matching in ORDER BY and GROUP BY expressions.

Aggregate functions with GROUP BY / HAVING - in the SQLAlchemy Unified Tutorial

Ordering or Grouping by a Label - in the SQLAlchemy Unified Tutorial

Return a new selectable with the given LIMIT criterion applied.

This is a numerical value which usually renders as a LIMIT expression in the resulting select. Backends that don’t support LIMIT will attempt to provide similar functionality.

The GenerativeSelect.limit() method will replace any clause applied with GenerativeSelect.fetch().

limit¶ – an integer LIMIT parameter, or a SQL expression that provides an integer result. Pass None to reset it.

GenerativeSelect.fetch()

GenerativeSelect.offset()

Return a new selectable with the given OFFSET criterion applied.

This is a numeric value which usually renders as an OFFSET expression in the resulting select. Backends that don’t support OFFSET will attempt to provide similar functionality.

offset¶ – an integer OFFSET parameter, or a SQL expression that provides an integer result. Pass None to reset it.

GenerativeSelect.limit()

GenerativeSelect.fetch()

Return a new selectable with the given list of ORDER BY criteria applied.

Calling this method multiple times is equivalent to calling it once with all the clauses concatenated. All existing ORDER BY criteria may be cancelled by passing None by itself. New ORDER BY criteria may then be added by invoking Query.order_by() again, e.g.:

a series of ColumnElement constructs which will be used to generate an ORDER BY clause.

Alternatively, an individual entry may also be the string name of a label located elsewhere in the columns clause of the statement which will be matched and rendered in a backend-specific way based on context; see Ordering or Grouping by a Label for background on string label matching in ORDER BY and GROUP BY expressions.

ORDER BY - in the SQLAlchemy Unified Tutorial

Ordering or Grouping by a Label - in the SQLAlchemy Unified Tutorial

Return a new selectable with the specified label style.

There are three “label styles” available, SelectLabelStyle.LABEL_STYLE_DISAMBIGUATE_ONLY, SelectLabelStyle.LABEL_STYLE_TABLENAME_PLUS_COL, and SelectLabelStyle.LABEL_STYLE_NONE. The default style is SelectLabelStyle.LABEL_STYLE_DISAMBIGUATE_ONLY.

In modern SQLAlchemy, there is not generally a need to change the labeling style, as per-expression labels are more effectively used by making use of the ColumnElement.label() method. In past versions, LABEL_STYLE_TABLENAME_PLUS_COL was used to disambiguate same-named columns from different tables, aliases, or subqueries; the newer LABEL_STYLE_DISAMBIGUATE_ONLY now applies labels only to names that conflict with an existing name so that the impact of this labeling is minimal.

The rationale for disambiguation is mostly so that all column expressions are available from a given FromClause.c collection when a subquery is created.

Added in version 1.4: - the GenerativeSelect.set_label_style() method replaces the previous combination of .apply_labels(), .with_labels() and use_labels=True methods and/or parameters.

LABEL_STYLE_DISAMBIGUATE_ONLY

LABEL_STYLE_TABLENAME_PLUS_COL

Apply LIMIT / OFFSET to this statement based on a slice.

The start and stop indices behave like the argument to Python’s built-in range() function. This method provides an alternative to using LIMIT/OFFSET to get a slice of the query.

The GenerativeSelect.slice() method will replace any clause applied with GenerativeSelect.fetch().

Added in version 1.4: Added the GenerativeSelect.slice() method generalized from the ORM.

GenerativeSelect.limit()

GenerativeSelect.offset()

GenerativeSelect.fetch()

Specify a FOR UPDATE clause for this GenerativeSelect.

On a database like PostgreSQL or Oracle Database, the above would render a statement like:

on other backends, the nowait option is ignored and instead would produce:

When called with no arguments, the statement will render with the suffix FOR UPDATE. Additional arguments can then be provided which allow for common database-specific variants.

nowait¶ – boolean; will render FOR UPDATE NOWAIT on Oracle Database and PostgreSQL dialects.

read¶ – boolean; will render LOCK IN SHARE MODE on MySQL, FOR SHARE on PostgreSQL. On PostgreSQL, when combined with nowait, will render FOR SHARE NOWAIT.

of¶ – SQL expression or list of SQL expression elements, (typically Column objects or a compatible expression, for some backends may also be a table expression) which will render into a FOR UPDATE OF clause; supported by PostgreSQL, Oracle Database, some MySQL versions and possibly others. May render as a table or as a column depending on backend.

skip_locked¶ – boolean, will render FOR UPDATE SKIP LOCKED on Oracle Database and PostgreSQL dialects or FOR SHARE SKIP LOCKED if read=True is also specified.

key_share¶ – boolean, will render FOR NO KEY UPDATE, or if combined with read=True will render FOR KEY SHARE, on the PostgreSQL dialect.

inherits from sqlalchemy.sql.roles.HasCTERole, sqlalchemy.sql.expression.SelectsRows

Mixin that declares a class to include CTE support.

Add one or more CTE constructs to this statement.

Return a new CTE, or Common Table Expression instance.

indicates if this HasCTE as contained within a CTE should compel the CTE to render the column names of this object in the WITH clause.

Add one or more CTE constructs to this statement.

This method will associate the given CTE constructs with the parent statement such that they will each be unconditionally rendered in the WITH clause of the final statement, even if not referenced elsewhere within the statement or any sub-selects.

The optional HasCTE.add_cte.nest_here parameter when set to True will have the effect that each given CTE will render in a WITH clause rendered directly along with this statement, rather than being moved to the top of the ultimate rendered statement, even if this statement is rendered as a subquery within a larger statement.

This method has two general uses. One is to embed CTE statements that serve some purpose without being referenced explicitly, such as the use case of embedding a DML statement such as an INSERT or UPDATE as a CTE inline with a primary statement that may draw from its results indirectly. The other is to provide control over the exact placement of a particular series of CTE constructs that should remain rendered directly in terms of a particular statement that may be nested in a larger statement.

Above, the “anon_1” CTE is not referenced in the SELECT statement, however still accomplishes the task of running an INSERT statement.

Similarly in a DML-related context, using the PostgreSQL Insert construct to generate an “upsert”:

The above statement renders as:

Added in version 1.4.21.

zero or more CTE constructs.

Changed in version 2.0: Multiple CTE instances are accepted

if True, the given CTE or CTEs will be rendered as though they specified the HasCTE.cte.nesting flag to True when they were added to this HasCTE. Assuming the given CTEs are not referenced in an outer-enclosing statement as well, the CTEs given should render at the level of this statement when this flag is given.

Added in version 2.0.

Return a new CTE, or Common Table Expression instance.

Common table expressions are a SQL standard whereby SELECT statements can draw upon secondary statements specified along with the primary statement, using a clause called “WITH”. Special semantics regarding UNION can also be employed to allow “recursive” queries, where a SELECT statement can draw upon the set of rows that have previously been selected.

CTEs can also be applied to DML constructs UPDATE, INSERT and DELETE on some databases, both as a source of CTE rows when combined with RETURNING, as well as a consumer of CTE rows.

SQLAlchemy detects CTE objects, which are treated similarly to Alias objects, as special elements to be delivered to the FROM clause of the statement as well as to a WITH clause at the top of the statement.

For special prefixes such as PostgreSQL “MATERIALIZED” and “NOT MATERIALIZED”, the CTE.prefix_with() method may be used to establish these.

Changed in version 1.3.13: Added support for prefixes. In particular - MATERIALIZED and NOT MATERIALIZED.

name¶ – name given to the common table expression. Like FromClause.alias(), the name can be left as None in which case an anonymous symbol will be used at query compile time.

recursive¶ – if True, will render WITH RECURSIVE. A recursive common table expression is intended to be used in conjunction with UNION ALL in order to derive rows from those already selected.

if True, will render the CTE locally to the statement in which it is referenced. For more complex scenarios, the HasCTE.add_cte() method using the HasCTE.add_cte.nest_here parameter may also be used to more carefully control the exact placement of a particular CTE.

Added in version 1.4.24.

The following examples include two from PostgreSQL’s documentation at https://www.postgresql.org/docs/current/static/queries-with.html, as well as additional examples.

Example 1, non recursive:

Example 2, WITH RECURSIVE:

Example 3, an upsert using UPDATE and INSERT with CTEs:

Example 4, Nesting CTE (SQLAlchemy 1.4.24 and above):

The above query will render the second CTE nested inside the first, shown with inline parameters below as:

The same CTE can be set up using the HasCTE.add_cte() method as follows (SQLAlchemy 2.0 and above):

Example 5, Non-Linear CTE (SQLAlchemy 1.4.28 and above):

The above query will render 2 UNIONs inside the recursive CTE:

Query.cte() - ORM version of HasCTE.cte().

indicates if this HasCTE as contained within a CTE should compel the CTE to render the column names of this object in the WITH clause.

Added in version 2.0.42.

Add one or more expressions following the statement keyword, i.e. SELECT, INSERT, UPDATE, or DELETE. Generative.

Add one or more expressions following the statement keyword, i.e. SELECT, INSERT, UPDATE, or DELETE. Generative.

This is used to support backend-specific prefix keywords such as those provided by MySQL.

Multiple prefixes can be specified by multiple calls to HasPrefixes.prefix_with().

*prefixes¶ – textual or ClauseElement construct which will be rendered following the INSERT, UPDATE, or DELETE keyword.

dialect¶ – optional string dialect name which will limit rendering of this prefix to only that dialect.

Add one or more expressions following the statement as a whole.

Add one or more expressions following the statement as a whole.

This is used to support backend-specific suffix keywords on certain constructs.

Multiple suffixes can be specified by multiple calls to HasSuffixes.suffix_with().

*suffixes¶ – textual or ClauseElement construct which will be rendered following the target clause.

dialect¶ – Optional string dialect name which will limit rendering of this suffix to only that dialect.

inherits from sqlalchemy.sql.roles.DMLTableRole, sqlalchemy.sql.expression.FromClause

Represent a JOIN construct between two FromClause elements.

The public constructor function for Join is the module-level join() function, as well as the FromClause.join() method of any FromClause (e.g. such as Table).

Construct a new Join.

Return True if this FromClause is ‘derived’ from the given FromClause.

Create a Select from this Join.

Apply a ‘grouping’ to this ClauseElement.

Construct a new Join.

The usual entrypoint here is the join() function or the FromClause.join() method of any FromClause object.

Return True if this FromClause is ‘derived’ from the given FromClause.

An example would be an Alias of a Table is derived from that Table.

Create a Select from this Join.

The above will produce a SQL string resembling:

Apply a ‘grouping’ to this ClauseElement.

This method is overridden by subclasses to return a “grouping” construct, i.e. parenthesis. In particular it’s used by “binary” expressions to provide a grouping around themselves when placed into a larger expression, as well as by select() constructs when placed into the FROM clause of another select(). (Note that subqueries should be normally created using the Select.alias() method, as many platforms require nested SELECT statements to be named).

As expressions are composed together, the application of self_group() is automatic - end-user code should never need to use this method directly. Note that SQLAlchemy’s clause constructs take operator precedence into account - so parenthesis might not be needed, for example, in an expression like x OR (y AND z) - AND takes precedence over OR.

The base self_group() method of ClauseElement just returns self.

inherits from sqlalchemy.sql.expression.FromClauseAlias, sqlalchemy.sql.expression.LateralFromClause

Represent a LATERAL subquery.

This object is constructed from the lateral() module level function as well as the FromClause.lateral() method available on all FromClause subclasses.

While LATERAL is part of the SQL standard, currently only more recent PostgreSQL versions provide support for this keyword.

LATERAL correlation - overview of usage.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

inherits from sqlalchemy.sql.roles.ReturnsRowsRole, sqlalchemy.sql.expression.DQLDMLClauseElement

The base-most class for Core constructs that have some concept of columns that can represent rows.

While the SELECT statement and TABLE are the primary things we think of in this category, DML like INSERT, UPDATE and DELETE can also specify RETURNING which means they can be used in CTEs and other forms, and PostgreSQL has functions that return rows also.

Added in version 1.4.

Compile this SQL expression.

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

Return True if this ReturnsRows is ‘derived’ from the given FromClause.

inherited from the CompilerElement.compile() method of CompilerElement

Compile this SQL expression.

The return value is a Compiled object. Calling str() or unicode() on the returned value will yield a string representation of the result. The Compiled object also can return a dictionary of bind parameter names and values using the params accessor.

bind¶ – An Connection or Engine which can provide a Dialect in order to generate a Compiled object. If the bind and dialect parameters are both omitted, a default SQL compiler is used.

column_keys¶ – Used for INSERT and UPDATE statements, a list of column names which should be present in the VALUES clause of the compiled statement. If None, all columns from the target table object are rendered.

dialect¶ – A Dialect instance which can generate a Compiled object. This argument takes precedence over the bind argument.

optional dictionary of additional parameters that will be passed through to the compiler within all “visit” methods. This allows any custom flag to be passed through to a custom compilation construct, for example. It is also used for the case of passing the literal_binds flag through:

How do I render SQL expressions as strings, possibly with bound parameters inlined?

A ColumnCollection that represents the “exported” columns of this ReturnsRows.

The “exported” columns represent the collection of ColumnElement expressions that are rendered by this SQL construct. There are primary varieties which are the “FROM clause columns” of a FROM clause, such as a table, join, or subquery, the “SELECTed columns”, which are the columns in the “columns clause” of a SELECT statement, and the RETURNING columns in a DML statement..

Added in version 1.4.

FromClause.exported_columns

SelectBase.exported_columns

inherited from the HasTraverseInternals.get_children() method of HasTraverseInternals

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

This is used for visit traversal.

**kw may contain flags that change the collection that is returned, for example to return a subset of items in order to cut down on larger traversals, or to return child items from a different context (such as schema-level collections instead of clause-level).

inherited from the HasCacheKey.inherit_cache attribute of HasCacheKey

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

Return True if this ReturnsRows is ‘derived’ from the given FromClause.

An example would be an Alias of a Table is derived from that Table.

inherits from sqlalchemy.sql.roles.InElementRole, sqlalchemy.sql.expression.Generative, sqlalchemy.sql.expression.GroupedElement, sqlalchemy.sql.expression.ColumnElement

Represent a scalar subquery.

A ScalarSelect is created by invoking the SelectBase.scalar_subquery() method. The object then participates in other SQL expressions as a SQL column expression within the ColumnElement hierarchy.

SelectBase.scalar_subquery()

Scalar and Correlated Subqueries - in the 2.0 tutorial

Return a new ScalarSelect which will correlate the given FROM clauses to that of an enclosing Select.

Return a new ScalarSelect which will omit the given FROM clauses from the auto-correlation process.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

Apply a ‘grouping’ to this ClauseElement.

Apply a WHERE clause to the SELECT statement referred to by this ScalarSelect.

Return a new ScalarSelect which will correlate the given FROM clauses to that of an enclosing Select.

This method is mirrored from the Select.correlate() method of the underlying Select. The method applies the :meth:_sql.Select.correlate` method, then returns a new ScalarSelect against that statement.

Added in version 1.4: Previously, the ScalarSelect.correlate() method was only available from Select.

*fromclauses¶ – a list of one or more FromClause constructs, or other compatible constructs (i.e. ORM-mapped classes) to become part of the correlate collection.

ScalarSelect.correlate_except()

Scalar and Correlated Subqueries - in the 2.0 tutorial

Return a new ScalarSelect which will omit the given FROM clauses from the auto-correlation process.

This method is mirrored from the Select.correlate_except() method of the underlying Select. The method applies the :meth:_sql.Select.correlate_except` method, then returns a new ScalarSelect against that statement.

Added in version 1.4: Previously, the ScalarSelect.correlate_except() method was only available from Select.

*fromclauses¶ – a list of one or more FromClause constructs, or other compatible constructs (i.e. ORM-mapped classes) to become part of the correlate-exception collection.

ScalarSelect.correlate()

Scalar and Correlated Subqueries - in the 2.0 tutorial

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

Apply a ‘grouping’ to this ClauseElement.

This method is overridden by subclasses to return a “grouping” construct, i.e. parenthesis. In particular it’s used by “binary” expressions to provide a grouping around themselves when placed into a larger expression, as well as by select() constructs when placed into the FROM clause of another select(). (Note that subqueries should be normally created using the Select.alias() method, as many platforms require nested SELECT statements to be named).

As expressions are composed together, the application of self_group() is automatic - end-user code should never need to use this method directly. Note that SQLAlchemy’s clause constructs take operator precedence into account - so parenthesis might not be needed, for example, in an expression like x OR (y AND z) - AND takes precedence over OR.

The base self_group() method of ClauseElement just returns self.

Apply a WHERE clause to the SELECT statement referred to by this ScalarSelect.

inherits from sqlalchemy.sql.expression.HasPrefixes, sqlalchemy.sql.expression.HasSuffixes, sqlalchemy.sql.expression.HasHints, sqlalchemy.sql.expression.HasCompileState, sqlalchemy.sql.expression._SelectFromElements, sqlalchemy.sql.expression.GenerativeSelect, sqlalchemy.sql.expression.TypedReturnsRows

Represents a SELECT statement.

The Select object is normally constructed using the select() function. See that function for details.

Using SELECT Statements - in the 2.0 tutorial

Construct a new Select.

Return a new select() construct with the given entities appended to its columns clause.

Add one or more CTE constructs to this statement.

Return a named subquery against this SelectBase.

Add a new kind of dialect-specific keyword argument for this class.

Return a new select() construct with the given column expression added to its columns clause.

Compile this SQL expression.

Return a new Select which will correlate the given FROM clauses to that of an enclosing Select.

Return a new Select which will omit the given FROM clauses from the auto-correlation process.

corresponding_column()

Given a ColumnElement, return the exported ColumnElement object from the Selectable.exported_columns collection of this Selectable which corresponds to that original ColumnElement via a common ancestor column.

Return a new CTE, or Common Table Expression instance.

A collection of keyword arguments specified as dialect-specific options to this construct.

Return a new select() construct which will apply DISTINCT to the SELECT statement overall.

Return a SQL EXCEPT of this select() construct against the given selectable provided as positional arguments.

Return a SQL EXCEPT ALL of this select() construct against the given selectables provided as positional arguments.

Set non-SQL options for the statement which take effect during execution.

Return an Exists representation of this selectable, which can be used as a column expression.

Return a new selectable with the given FETCH FIRST criterion applied.

A synonym for the Select.where() method.

apply the given filtering criterion as a WHERE clause to this select.

Apply the columns which this Select would select onto another statement.

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

get_execution_options()

Get the non-SQL options which will take effect during execution.

Compute the final displayed list of FromClause elements.

Retrieve the current label style.

Return a new selectable with the given list of GROUP BY criterion applied.

Return a new select() construct with the given expression added to its HAVING clause, joined to the existing clause via AND, if any.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

Return a SQL INTERSECT of this select() construct against the given selectables provided as positional arguments.

Return a SQL INTERSECT ALL of this select() construct against the given selectables provided as positional arguments.

Return True if this ReturnsRows is ‘derived’ from the given FromClause.

Create a SQL JOIN against this Select object’s criterion and apply generatively, returning the newly resulting Select.

Create a SQL JOIN against this Select object’s criterion and apply generatively, returning the newly resulting Select.

Return a ‘scalar’ representation of this selectable, embedded as a subquery with a label.

Return a LATERAL alias of this Selectable.

Return a new selectable with the given LIMIT criterion applied.

indicates if this HasCTE as contained within a CTE should compel the CTE to render the column names of this object in the WITH clause.

Return a new selectable with the given OFFSET criterion applied.

Apply options to this statement.

Return a new selectable with the given list of ORDER BY criteria applied.

Create a left outer join.

Create a SQL LEFT OUTER JOIN against this Select object’s criterion and apply generatively, returning the newly resulting Select.

Add one or more expressions following the statement keyword, i.e. SELECT, INSERT, UPDATE, or DELETE. Generative.

Return a new select() construct with redundantly named, equivalently-valued columns removed from the columns clause.

Replace all occurrences of FromClause ‘old’ with the given Alias object, returning a copy of this FromClause.

Return a ‘scalar’ representation of this selectable, which can be used as a column expression.

Return a new select() construct with the given FROM expression(s) merged into its list of FROM objects.

A ColumnCollection representing the columns that this SELECT statement or similar construct returns in its result set, not including TextClause constructs.

Return a ‘grouping’ construct as per the ClauseElement specification.

Return a new selectable with the specified label style.

Apply LIMIT / OFFSET to this statement based on a slice.

Return a subquery of this SelectBase.

Add one or more expressions following the statement as a whole.

Return a SQL UNION of this select() construct against the given selectables provided as positional arguments.

Return a SQL UNION ALL of this select() construct against the given selectables provided as positional arguments.

Return a new select() construct with the given expression added to its WHERE clause, joined to the existing clause via AND, if any.

Specify a FOR UPDATE clause for this GenerativeSelect.

Add an indexing or other executional context hint for the given selectable to this Select or other selectable object.

Return a new select() construct with its columns clause replaced with the given entities.

with_statement_hint()

Add a statement hint to this Select or other selectable object.

Construct a new Select.

The public constructor for Select is the select() function.

Return a new select() construct with the given entities appended to its columns clause.

The original expressions in the columns clause remain in place. To replace the original expressions with new ones, see the method Select.with_only_columns().

*entities¶ – column, table, or other entity expressions to be added to the columns clause

Select.with_only_columns() - replaces existing expressions rather than appending.

Selecting Multiple ORM Entities Simultaneously - ORM-centric example

inherited from the HasCTE.add_cte() method of HasCTE

Add one or more CTE constructs to this statement.

This method will associate the given CTE constructs with the parent statement such that they will each be unconditionally rendered in the WITH clause of the final statement, even if not referenced elsewhere within the statement or any sub-selects.

The optional HasCTE.add_cte.nest_here parameter when set to True will have the effect that each given CTE will render in a WITH clause rendered directly along with this statement, rather than being moved to the top of the ultimate rendered statement, even if this statement is rendered as a subquery within a larger statement.

This method has two general uses. One is to embed CTE statements that serve some purpose without being referenced explicitly, such as the use case of embedding a DML statement such as an INSERT or UPDATE as a CTE inline with a primary statement that may draw from its results indirectly. The other is to provide control over the exact placement of a particular series of CTE constructs that should remain rendered directly in terms of a particular statement that may be nested in a larger statement.

Above, the “anon_1” CTE is not referenced in the SELECT statement, however still accomplishes the task of running an INSERT statement.

Similarly in a DML-related context, using the PostgreSQL Insert construct to generate an “upsert”:

The above statement renders as:

Added in version 1.4.21.

zero or more CTE constructs.

Changed in version 2.0: Multiple CTE instances are accepted

if True, the given CTE or CTEs will be rendered as though they specified the HasCTE.cte.nesting flag to True when they were added to this HasCTE. Assuming the given CTEs are not referenced in an outer-enclosing statement as well, the CTEs given should render at the level of this statement when this flag is given.

Added in version 2.0.

inherited from the SelectBase.alias() method of SelectBase

Return a named subquery against this SelectBase.

For a SelectBase (as opposed to a FromClause), this returns a Subquery object which behaves mostly the same as the Alias object that is used with a FromClause.

Changed in version 1.4: The SelectBase.alias() method is now a synonym for the SelectBase.subquery() method.

inherited from the DialectKWArgs.argument_for() method of DialectKWArgs

Add a new kind of dialect-specific keyword argument for this class.

The DialectKWArgs.argument_for() method is a per-argument way adding extra arguments to the DefaultDialect.construct_arguments dictionary. This dictionary provides a list of argument names accepted by various schema-level constructs on behalf of a dialect.

New dialects should typically specify this dictionary all at once as a data member of the dialect class. The use case for ad-hoc addition of argument names is typically for end-user code that is also using a custom compilation scheme which consumes the additional arguments.

dialect_name¶ – name of a dialect. The dialect must be locatable, else a NoSuchModuleError is raised. The dialect must also include an existing DefaultDialect.construct_arguments collection, indicating that it participates in the keyword-argument validation and default system, else ArgumentError is raised. If the dialect does not include this collection, then any keyword argument can be specified on behalf of this dialect already. All dialects packaged within SQLAlchemy include this collection, however for third party dialects, support may vary.

argument_name¶ – name of the parameter.

default¶ – default value of the parameter.

inherited from the SelectBase.as_scalar() method of SelectBase

Deprecated since version 1.4: The SelectBase.as_scalar() method is deprecated and will be removed in a future release. Please refer to SelectBase.scalar_subquery().

Deprecated since version 1.4: The SelectBase.c and SelectBase.columns attributes are deprecated and will be removed in a future release; these attributes implicitly create a subquery that should be explicit. Please call SelectBase.subquery() first in order to create a subquery, which then contains this attribute. To access the columns that this SELECT object SELECTs from, use the SelectBase.selected_columns attribute.

Return a new select() construct with the given column expression added to its columns clause.

Deprecated since version 1.4: The Select.column() method is deprecated and will be removed in a future release. Please use Select.add_columns()

See the documentation for Select.with_only_columns() for guidelines on adding /replacing the columns of a Select object.

Return a plugin-enabled ‘column descriptions’ structure referring to the columns which are SELECTed by this statement.

This attribute is generally useful when using the ORM, as an extended structure which includes information about mapped entities is returned. The section Inspecting entities and columns from ORM-enabled SELECT and DML statements contains more background.

For a Core-only statement, the structure returned by this accessor is derived from the same objects that are returned by the Select.selected_columns accessor, formatted as a list of dictionaries which contain the keys name, type and expr, which indicate the column expressions to be selected:

Changed in version 1.4.33: The Select.column_descriptions attribute returns a structure for a Core-only set of entities, not just ORM-only entities.

UpdateBase.entity_description - entity information for an insert(), update(), or delete()

Inspecting entities and columns from ORM-enabled SELECT and DML statements - ORM background

Return the set of FromClause objects implied by the columns clause of this SELECT statement.

Added in version 1.4.23.

Select.froms - “final” FROM list taking the full statement into account

Select.with_only_columns() - makes use of this collection to set up a new FROM list

inherited from the CompilerElement.compile() method of CompilerElement

Compile this SQL expression.

The return value is a Compiled object. Calling str() or unicode() on the returned value will yield a string representation of the result. The Compiled object also can return a dictionary of bind parameter names and values using the params accessor.

bind¶ – An Connection or Engine which can provide a Dialect in order to generate a Compiled object. If the bind and dialect parameters are both omitted, a default SQL compiler is used.

column_keys¶ – Used for INSERT and UPDATE statements, a list of column names which should be present in the VALUES clause of the compiled statement. If None, all columns from the target table object are rendered.

dialect¶ – A Dialect instance which can generate a Compiled object. This argument takes precedence over the bind argument.

optional dictionary of additional parameters that will be passed through to the compiler within all “visit” methods. This allows any custom flag to be passed through to a custom compilation construct, for example. It is also used for the case of passing the literal_binds flag through:

How do I render SQL expressions as strings, possibly with bound parameters inlined?

Return a new Select which will correlate the given FROM clauses to that of an enclosing Select.

Calling this method turns off the Select object’s default behavior of “auto-correlation”. Normally, FROM elements which appear in a Select that encloses this one via its WHERE clause, ORDER BY, HAVING or columns clause will be omitted from this Select object’s FROM clause. Setting an explicit correlation collection using the Select.correlate() method provides a fixed list of FROM objects that can potentially take place in this process.

When Select.correlate() is used to apply specific FROM clauses for correlation, the FROM elements become candidates for correlation regardless of how deeply nested this Select object is, relative to an enclosing Select which refers to the same FROM object. This is in contrast to the behavior of “auto-correlation” which only correlates to an immediate enclosing Select. Multi-level correlation ensures that the link between enclosed and enclosing Select is always via at least one WHERE/ORDER BY/HAVING/columns clause in order for correlation to take place.

If None is passed, the Select object will correlate none of its FROM entries, and all will render unconditionally in the local FROM clause.

*fromclauses¶ – one or more FromClause or other FROM-compatible construct such as an ORM mapped entity to become part of the correlate collection; alternatively pass a single value None to remove all existing correlations.

Select.correlate_except()

Scalar and Correlated Subqueries

Return a new Select which will omit the given FROM clauses from the auto-correlation process.

Calling Select.correlate_except() turns off the Select object’s default behavior of “auto-correlation” for the given FROM elements. An element specified here will unconditionally appear in the FROM list, while all other FROM elements remain subject to normal auto-correlation behaviors.

If None is passed, or no arguments are passed, the Select object will correlate all of its FROM entries.

*fromclauses¶ – a list of one or more FromClause constructs, or other compatible constructs (i.e. ORM-mapped classes) to become part of the correlate-exception collection.

Scalar and Correlated Subqueries

inherited from the Selectable.corresponding_column() method of Selectable

Given a ColumnElement, return the exported ColumnElement object from the Selectable.exported_columns collection of this Selectable which corresponds to that original ColumnElement via a common ancestor column.

column¶ – the target ColumnElement to be matched.

require_embedded¶ – only return corresponding columns for the given ColumnElement, if the given ColumnElement is actually present within a sub-element of this Selectable. Normally the column will match if it merely shares a common ancestor with one of the exported columns of this Selectable.

Selectable.exported_columns - the ColumnCollection that is used for the operation.

ColumnCollection.corresponding_column() - implementation method.

inherited from the HasCTE.cte() method of HasCTE

Return a new CTE, or Common Table Expression instance.

Common table expressions are a SQL standard whereby SELECT statements can draw upon secondary statements specified along with the primary statement, using a clause called “WITH”. Special semantics regarding UNION can also be employed to allow “recursive” queries, where a SELECT statement can draw upon the set of rows that have previously been selected.

CTEs can also be applied to DML constructs UPDATE, INSERT and DELETE on some databases, both as a source of CTE rows when combined with RETURNING, as well as a consumer of CTE rows.

SQLAlchemy detects CTE objects, which are treated similarly to Alias objects, as special elements to be delivered to the FROM clause of the statement as well as to a WITH clause at the top of the statement.

For special prefixes such as PostgreSQL “MATERIALIZED” and “NOT MATERIALIZED”, the CTE.prefix_with() method may be used to establish these.

Changed in version 1.3.13: Added support for prefixes. In particular - MATERIALIZED and NOT MATERIALIZED.

name¶ – name given to the common table expression. Like FromClause.alias(), the name can be left as None in which case an anonymous symbol will be used at query compile time.

recursive¶ – if True, will render WITH RECURSIVE. A recursive common table expression is intended to be used in conjunction with UNION ALL in order to derive rows from those already selected.

if True, will render the CTE locally to the statement in which it is referenced. For more complex scenarios, the HasCTE.add_cte() method using the HasCTE.add_cte.nest_here parameter may also be used to more carefully control the exact placement of a particular CTE.

Added in version 1.4.24.

The following examples include two from PostgreSQL’s documentation at https://www.postgresql.org/docs/current/static/queries-with.html, as well as additional examples.

Example 1, non recursive:

Example 2, WITH RECURSIVE:

Example 3, an upsert using UPDATE and INSERT with CTEs:

Example 4, Nesting CTE (SQLAlchemy 1.4.24 and above):

The above query will render the second CTE nested inside the first, shown with inline parameters below as:

The same CTE can be set up using the HasCTE.add_cte() method as follows (SQLAlchemy 2.0 and above):

Example 5, Non-Linear CTE (SQLAlchemy 1.4.28 and above):

The above query will render 2 UNIONs inside the recursive CTE:

Query.cte() - ORM version of HasCTE.cte().

A collection of keyword arguments specified as dialect-specific options to this construct.

The arguments are present here in their original <dialect>_<kwarg> format. Only arguments that were actually passed are included; unlike the DialectKWArgs.dialect_options collection, which contains all options known by this dialect including defaults.

The collection is also writable; keys are accepted of the form <dialect>_<kwarg> where the value will be assembled into the list of options.

DialectKWArgs.dialect_options - nested dictionary form

inherited from the DialectKWArgs.dialect_options attribute of DialectKWArgs

A collection of keyword arguments specified as dialect-specific options to this construct.

This is a two-level nested registry, keyed to <dialect_name> and <argument_name>. For example, the postgresql_where argument would be locatable as:

Added in version 0.9.2.

DialectKWArgs.dialect_kwargs - flat dictionary form

Return a new select() construct which will apply DISTINCT to the SELECT statement overall.

The above would produce an statement resembling:

The method also accepts an *expr parameter which produces the PostgreSQL dialect-specific DISTINCT ON expression. Using this parameter on other backends which don’t support this syntax will raise an error.

optional column expressions. When present, the PostgreSQL dialect will render a DISTINCT ON (<expressions>) construct. A deprecation warning and/or CompileError will be raised on other backends.

Deprecated since version 1.4: Using *expr in other dialects is deprecated and will raise CompileError in a future version.

Return a SQL EXCEPT of this select() construct against the given selectable provided as positional arguments.

one or more elements with which to create a UNION.

Changed in version 1.4.28: multiple elements are now accepted.

Return a SQL EXCEPT ALL of this select() construct against the given selectables provided as positional arguments.

one or more elements with which to create a UNION.

Changed in version 1.4.28: multiple elements are now accepted.

inherited from the Executable.execution_options() method of Executable

Set non-SQL options for the statement which take effect during execution.

Execution options can be set at many scopes, including per-statement, per-connection, or per execution, using methods such as Connection.execution_options() and parameters which accept a dictionary of options such as Connection.execute.execution_options and Session.execute.execution_options.

The primary characteristic of an execution option, as opposed to other kinds of options such as ORM loader options, is that execution options never affect the compiled SQL of a query, only things that affect how the SQL statement itself is invoked or how results are fetched. That is, execution options are not part of what’s accommodated by SQL compilation nor are they considered part of the cached state of a statement.

The Executable.execution_options() method is generative, as is the case for the method as applied to the Engine and Query objects, which means when the method is called, a copy of the object is returned, which applies the given parameters to that new copy, but leaves the original unchanged:

An exception to this behavior is the Connection object, where the Connection.execution_options() method is explicitly not generative.

The kinds of options that may be passed to Executable.execution_options() and other related methods and parameter dictionaries include parameters that are explicitly consumed by SQLAlchemy Core or ORM, as well as arbitrary keyword arguments not defined by SQLAlchemy, which means the methods and/or parameter dictionaries may be used for user-defined parameters that interact with custom code, which may access the parameters using methods such as Executable.get_execution_options() and Connection.get_execution_options(), or within selected event hooks using a dedicated execution_options event parameter such as ConnectionEvents.before_execute.execution_options or ORMExecuteState.execution_options, e.g.:

Within the scope of options that are explicitly recognized by SQLAlchemy, most apply to specific classes of objects and not others. The most common execution options include:

Connection.execution_options.isolation_level - sets the isolation level for a connection or a class of connections via an Engine. This option is accepted only by Connection or Engine.

Connection.execution_options.stream_results - indicates results should be fetched using a server side cursor; this option is accepted by Connection, by the Connection.execute.execution_options parameter on Connection.execute(), and additionally by Executable.execution_options() on a SQL statement object, as well as by ORM constructs like Session.execute().

Connection.execution_options.compiled_cache - indicates a dictionary that will serve as the SQL compilation cache for a Connection or Engine, as well as for ORM methods like Session.execute(). Can be passed as None to disable caching for statements. This option is not accepted by Executable.execution_options() as it is inadvisable to carry along a compilation cache within a statement object.

Connection.execution_options.schema_translate_map - a mapping of schema names used by the Schema Translate Map feature, accepted by Connection, Engine, Executable, as well as by ORM constructs like Session.execute().

Connection.execution_options()

Connection.execute.execution_options

Session.execute.execution_options

ORM Execution Options - documentation on all ORM-specific execution options

inherited from the SelectBase.exists() method of SelectBase

Return an Exists representation of this selectable, which can be used as a column expression.

The returned object is an instance of Exists.

EXISTS subqueries - in the 2.0 style tutorial.

Added in version 1.4.

A ColumnCollection that represents the “exported” columns of this Selectable, not including TextClause constructs.

The “exported” columns for a SelectBase object are synonymous with the SelectBase.selected_columns collection.

Added in version 1.4.

Select.exported_columns

Selectable.exported_columns

FromClause.exported_columns

inherited from the GenerativeSelect.fetch() method of GenerativeSelect

Return a new selectable with the given FETCH FIRST criterion applied.

This is a numeric value which usually renders as FETCH {FIRST | NEXT} [ count ] {ROW | ROWS} {ONLY | WITH TIES} expression in the resulting select. This functionality is is currently implemented for Oracle Database, PostgreSQL, MSSQL.

Use GenerativeSelect.offset() to specify the offset.

The GenerativeSelect.fetch() method will replace any clause applied with GenerativeSelect.limit().

Added in version 1.4.

count¶ – an integer COUNT parameter, or a SQL expression that provides an integer result. When percent=True this will represent the percentage of rows to return, not the absolute value. Pass None to reset it.

with_ties¶ – When True, the WITH TIES option is used to return any additional rows that tie for the last place in the result set according to the ORDER BY clause. The ORDER BY may be mandatory in this case. Defaults to False

percent¶ – When True, count represents the percentage of the total number of selected rows to return. Defaults to False

Additional dialect-specific keyword arguments may be accepted by dialects.

Added in version 2.0.41.

GenerativeSelect.limit()

GenerativeSelect.offset()

A synonym for the Select.where() method.

apply the given filtering criterion as a WHERE clause to this select.

Apply the columns which this Select would select onto another statement.

This operation is plugin-specific and will raise a not supported exception if this Select does not select from plugin-enabled entities.

The statement is typically either a text() or select() construct, and should return the set of columns appropriate to the entities represented by this Select.

Getting ORM Results from Textual Statements - usage examples in the ORM Querying Guide

Return the displayed list of FromClause elements.

Deprecated since version 1.4.23: The Select.froms attribute is moved to the Select.get_final_froms() method.

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

This is used for visit traversal.

**kw may contain flags that change the collection that is returned, for example to return a subset of items in order to cut down on larger traversals, or to return child items from a different context (such as schema-level collections instead of clause-level).

inherited from the Executable.get_execution_options() method of Executable

Get the non-SQL options which will take effect during execution.

Added in version 1.3.

Executable.execution_options()

Compute the final displayed list of FromClause elements.

This method will run through the full computation required to determine what FROM elements will be displayed in the resulting SELECT statement, including shadowing individual tables with JOIN objects, as well as full computation for ORM use cases including eager loading clauses.

For ORM use, this accessor returns the post compilation list of FROM objects; this collection will include elements such as eagerly loaded tables and joins. The objects will not be ORM enabled and not work as a replacement for the Select.select_froms() collection; additionally, the method is not well performing for an ORM enabled statement as it will incur the full ORM construction process.

To retrieve the FROM list that’s implied by the “columns” collection passed to the Select originally, use the Select.columns_clause_froms accessor.

To select from an alternative set of columns while maintaining the FROM list, use the Select.with_only_columns() method and pass the Select.with_only_columns.maintain_column_froms parameter.

Added in version 1.4.23: - the Select.get_final_froms() method replaces the previous Select.froms accessor, which is deprecated.

Select.columns_clause_froms

inherited from the GenerativeSelect.get_label_style() method of GenerativeSelect

Retrieve the current label style.

Added in version 1.4.

inherited from the GenerativeSelect.group_by() method of GenerativeSelect

Return a new selectable with the given list of GROUP BY criterion applied.

All existing GROUP BY settings can be suppressed by passing None.

a series of ColumnElement constructs which will be used to generate an GROUP BY clause.

Alternatively, an individual entry may also be the string name of a label located elsewhere in the columns clause of the statement which will be matched and rendered in a backend-specific way based on context; see Ordering or Grouping by a Label for background on string label matching in ORDER BY and GROUP BY expressions.

Aggregate functions with GROUP BY / HAVING - in the SQLAlchemy Unified Tutorial

Ordering or Grouping by a Label - in the SQLAlchemy Unified Tutorial

Return a new select() construct with the given expression added to its HAVING clause, joined to the existing clause via AND, if any.

inherited from the HasCacheKey.inherit_cache attribute of HasCacheKey

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

An iterator of all ColumnElement expressions which would be rendered into the columns clause of the resulting SELECT statement.

This method is legacy as of 1.4 and is superseded by the Select.exported_columns collection.

Return a SQL INTERSECT of this select() construct against the given selectables provided as positional arguments.

one or more elements with which to create a UNION.

Changed in version 1.4.28: multiple elements are now accepted.

**kwargs¶ – keyword arguments are forwarded to the constructor for the newly created CompoundSelect object.

Return a SQL INTERSECT ALL of this select() construct against the given selectables provided as positional arguments.

one or more elements with which to create a UNION.

Changed in version 1.4.28: multiple elements are now accepted.

**kwargs¶ – keyword arguments are forwarded to the constructor for the newly created CompoundSelect object.

Return True if this ReturnsRows is ‘derived’ from the given FromClause.

An example would be an Alias of a Table is derived from that Table.

Create a SQL JOIN against this Select object’s criterion and apply generatively, returning the newly resulting Select.

The above statement generates SQL similar to:

Changed in version 1.4: Select.join() now creates a Join object between a FromClause source that is within the FROM clause of the existing SELECT, and a given target FromClause, and then adds this Join to the FROM clause of the newly generated SELECT statement. This is completely reworked from the behavior in 1.3, which would instead create a subquery of the entire Select and then join that subquery to the target.

This is a backwards incompatible change as the previous behavior was mostly useless, producing an unnamed subquery rejected by most databases in any case. The new behavior is modeled after that of the very successful Query.join() method in the ORM, in order to support the functionality of Query being available by using a Select object with an Session.

See the notes for this change at select().join() and outerjoin() add JOIN criteria to the current query, rather than creating a subquery.

target¶ – target table to join towards

onclause¶ – ON clause of the join. If omitted, an ON clause is generated automatically based on the ForeignKey linkages between the two tables, if one can be unambiguously determined, otherwise an error is raised.

isouter¶ – if True, generate LEFT OUTER join. Same as Select.outerjoin().

full¶ – if True, generate FULL OUTER join.

Explicit FROM clauses and JOINs - in the SQLAlchemy Unified Tutorial

Joins - in the ORM Querying Guide

Create a SQL JOIN against this Select object’s criterion and apply generatively, returning the newly resulting Select.

The above statement generates SQL similar to:

Added in version 1.4.

from_¶ – the left side of the join, will be rendered in the FROM clause and is roughly equivalent to using the Select.select_from() method.

target¶ – target table to join towards

onclause¶ – ON clause of the join.

isouter¶ – if True, generate LEFT OUTER join. Same as Select.outerjoin().

full¶ – if True, generate FULL OUTER join.

Explicit FROM clauses and JOINs - in the SQLAlchemy Unified Tutorial

Joins - in the ORM Querying Guide

A synonym for DialectKWArgs.dialect_kwargs.

inherited from the SelectBase.label() method of SelectBase

Return a ‘scalar’ representation of this selectable, embedded as a subquery with a label.

SelectBase.scalar_subquery().

inherited from the SelectBase.lateral() method of SelectBase

Return a LATERAL alias of this Selectable.

The return value is the Lateral construct also provided by the top-level lateral() function.

LATERAL correlation - overview of usage.

inherited from the GenerativeSelect.limit() method of GenerativeSelect

Return a new selectable with the given LIMIT criterion applied.

This is a numerical value which usually renders as a LIMIT expression in the resulting select. Backends that don’t support LIMIT will attempt to provide similar functionality.

The GenerativeSelect.limit() method will replace any clause applied with GenerativeSelect.fetch().

limit¶ – an integer LIMIT parameter, or a SQL expression that provides an integer result. Pass None to reset it.

GenerativeSelect.fetch()

GenerativeSelect.offset()

inherited from the HasCTE.name_cte_columns attribute of HasCTE

indicates if this HasCTE as contained within a CTE should compel the CTE to render the column names of this object in the WITH clause.

Added in version 2.0.42.

inherited from the GenerativeSelect.offset() method of GenerativeSelect

Return a new selectable with the given OFFSET criterion applied.

This is a numeric value which usually renders as an OFFSET expression in the resulting select. Backends that don’t support OFFSET will attempt to provide similar functionality.

offset¶ – an integer OFFSET parameter, or a SQL expression that provides an integer result. Pass None to reset it.

GenerativeSelect.limit()

GenerativeSelect.fetch()

inherited from the Executable.options() method of Executable

Apply options to this statement.

In the general sense, options are any kind of Python object that can be interpreted by the SQL compiler for the statement. These options can be consumed by specific dialects or specific kinds of compilers.

The most commonly known kind of option are the ORM level options that apply “eager load” and other loading behaviors to an ORM query. However, options can theoretically be used for many other purposes.

For background on specific kinds of options for specific kinds of statements, refer to the documentation for those option objects.

Changed in version 1.4: - added Executable.options() to Core statement objects towards the goal of allowing unified Core / ORM querying capabilities.

Column Loading Options - refers to options specific to the usage of ORM queries

Relationship Loading with Loader Options - refers to options specific to the usage of ORM queries

inherited from the GenerativeSelect.order_by() method of GenerativeSelect

Return a new selectable with the given list of ORDER BY criteria applied.

Calling this method multiple times is equivalent to calling it once with all the clauses concatenated. All existing ORDER BY criteria may be cancelled by passing None by itself. New ORDER BY criteria may then be added by invoking Query.order_by() again, e.g.:

a series of ColumnElement constructs which will be used to generate an ORDER BY clause.

Alternatively, an individual entry may also be the string name of a label located elsewhere in the columns clause of the statement which will be matched and rendered in a backend-specific way based on context; see Ordering or Grouping by a Label for background on string label matching in ORDER BY and GROUP BY expressions.

ORDER BY - in the SQLAlchemy Unified Tutorial

Ordering or Grouping by a Label - in the SQLAlchemy Unified Tutorial

Create a left outer join.

Parameters are the same as that of Select.join().

Changed in version 1.4: Select.outerjoin() now creates a Join object between a FromClause source that is within the FROM clause of the existing SELECT, and a given target FromClause, and then adds this Join to the FROM clause of the newly generated SELECT statement. This is completely reworked from the behavior in 1.3, which would instead create a subquery of the entire Select and then join that subquery to the target.

This is a backwards incompatible change as the previous behavior was mostly useless, producing an unnamed subquery rejected by most databases in any case. The new behavior is modeled after that of the very successful Query.join() method in the ORM, in order to support the functionality of Query being available by using a Select object with an Session.

See the notes for this change at select().join() and outerjoin() add JOIN criteria to the current query, rather than creating a subquery.

Explicit FROM clauses and JOINs - in the SQLAlchemy Unified Tutorial

Joins - in the ORM Querying Guide

Create a SQL LEFT OUTER JOIN against this Select object’s criterion and apply generatively, returning the newly resulting Select.

Usage is the same as that of Select.join_from().

inherited from the HasPrefixes.prefix_with() method of HasPrefixes

Add one or more expressions following the statement keyword, i.e. SELECT, INSERT, UPDATE, or DELETE. Generative.

This is used to support backend-specific prefix keywords such as those provided by MySQL.

Multiple prefixes can be specified by multiple calls to HasPrefixes.prefix_with().

*prefixes¶ – textual or ClauseElement construct which will be rendered following the INSERT, UPDATE, or DELETE keyword.

dialect¶ – optional string dialect name which will limit rendering of this prefix to only that dialect.

Return a new select() construct with redundantly named, equivalently-valued columns removed from the columns clause.

“Redundant” here means two columns where one refers to the other either based on foreign key, or via a simple equality comparison in the WHERE clause of the statement. The primary purpose of this method is to automatically construct a select statement with all uniquely-named columns, without the need to use table-qualified labels as Select.set_label_style() does.

When columns are omitted based on foreign key, the referred-to column is the one that’s kept. When columns are omitted based on WHERE equivalence, the first column in the columns clause is the one that’s kept.

only_synonyms¶ – when True, limit the removal of columns to those which have the same name as the equivalent. Otherwise, all columns that are equivalent to another are removed.

inherited from the Selectable.replace_selectable() method of Selectable

Replace all occurrences of FromClause ‘old’ with the given Alias object, returning a copy of this FromClause.

Deprecated since version 1.4: The Selectable.replace_selectable() method is deprecated, and will be removed in a future release. Similar functionality is available via the sqlalchemy.sql.visitors module.

inherited from the SelectBase.scalar_subquery() method of SelectBase

Return a ‘scalar’ representation of this selectable, which can be used as a column expression.

The returned object is an instance of ScalarSelect.

Typically, a select statement which has only one column in its columns clause is eligible to be used as a scalar expression. The scalar subquery can then be used in the WHERE clause or columns clause of an enclosing SELECT.

Note that the scalar subquery differentiates from the FROM-level subquery that can be produced using the SelectBase.subquery() method.

Scalar and Correlated Subqueries - in the 2.0 tutorial

inherited from the SelectBase.select() method of SelectBase

Deprecated since version 1.4: The SelectBase.select() method is deprecated and will be removed in a future release; this method implicitly creates a subquery that should be explicit. Please call SelectBase.subquery() first in order to create a subquery, which then can be selected.

Return a new select() construct with the given FROM expression(s) merged into its list of FROM objects.

The “from” list is a unique set on the identity of each element, so adding an already present Table or other selectable will have no effect. Passing a Join that refers to an already present Table or other selectable will have the effect of concealing the presence of that selectable as an individual element in the rendered FROM list, instead rendering it into a JOIN clause.

While the typical purpose of Select.select_from() is to replace the default, derived FROM clause with a join, it can also be called with individual table elements, multiple times if desired, in the case that the FROM clause cannot be fully derived from the columns clause:

A ColumnCollection representing the columns that this SELECT statement or similar construct returns in its result set, not including TextClause constructs.

This collection differs from the FromClause.columns collection of a FromClause in that the columns within this collection cannot be directly nested inside another SELECT statement; a subquery must be applied first which provides for the necessary parenthesization required by SQL.

For a select() construct, the collection here is exactly what would be rendered inside the “SELECT” statement, and the ColumnElement objects are directly present as they were given, e.g.:

Above, stmt.selected_columns would be a collection that contains the col1 and col2 objects directly. For a statement that is against a Table or other FromClause, the collection will use the ColumnElement objects that are in the FromClause.c collection of the from element.

A use case for the Select.selected_columns collection is to allow the existing columns to be referenced when adding additional criteria, e.g.:

The Select.selected_columns collection does not include expressions established in the columns clause using the text() construct; these are silently omitted from the collection. To use plain textual column expressions inside of a Select construct, use the literal_column() construct.

Added in version 1.4.

Return a ‘grouping’ construct as per the ClauseElement specification.

This produces an element that can be embedded in an expression. Note that this method is called automatically as needed when constructing expressions and should not require explicit use.

inherited from the GenerativeSelect.set_label_style() method of GenerativeSelect

Return a new selectable with the specified label style.

There are three “label styles” available, SelectLabelStyle.LABEL_STYLE_DISAMBIGUATE_ONLY, SelectLabelStyle.LABEL_STYLE_TABLENAME_PLUS_COL, and SelectLabelStyle.LABEL_STYLE_NONE. The default style is SelectLabelStyle.LABEL_STYLE_DISAMBIGUATE_ONLY.

In modern SQLAlchemy, there is not generally a need to change the labeling style, as per-expression labels are more effectively used by making use of the ColumnElement.label() method. In past versions, LABEL_STYLE_TABLENAME_PLUS_COL was used to disambiguate same-named columns from different tables, aliases, or subqueries; the newer LABEL_STYLE_DISAMBIGUATE_ONLY now applies labels only to names that conflict with an existing name so that the impact of this labeling is minimal.

The rationale for disambiguation is mostly so that all column expressions are available from a given FromClause.c collection when a subquery is created.

Added in version 1.4: - the GenerativeSelect.set_label_style() method replaces the previous combination of .apply_labels(), .with_labels() and use_labels=True methods and/or parameters.

LABEL_STYLE_DISAMBIGUATE_ONLY

LABEL_STYLE_TABLENAME_PLUS_COL

inherited from the GenerativeSelect.slice() method of GenerativeSelect

Apply LIMIT / OFFSET to this statement based on a slice.

The start and stop indices behave like the argument to Python’s built-in range() function. This method provides an alternative to using LIMIT/OFFSET to get a slice of the query.

The GenerativeSelect.slice() method will replace any clause applied with GenerativeSelect.fetch().

Added in version 1.4: Added the GenerativeSelect.slice() method generalized from the ORM.

GenerativeSelect.limit()

GenerativeSelect.offset()

GenerativeSelect.fetch()

inherited from the SelectBase.subquery() method of SelectBase

Return a subquery of this SelectBase.

A subquery is from a SQL perspective a parenthesized, named construct that can be placed in the FROM clause of another SELECT statement.

Given a SELECT statement such as:

The above statement might look like:

The subquery form by itself renders the same way, however when embedded into the FROM clause of another SELECT statement, it becomes a named sub-element:

The above renders as:

Historically, SelectBase.subquery() is equivalent to calling the FromClause.alias() method on a FROM object; however, as a SelectBase object is not directly FROM object, the SelectBase.subquery() method provides clearer semantics.

Added in version 1.4.

inherited from the HasSuffixes.suffix_with() method of HasSuffixes

Add one or more expressions following the statement as a whole.

This is used to support backend-specific suffix keywords on certain constructs.

Multiple suffixes can be specified by multiple calls to HasSuffixes.suffix_with().

*suffixes¶ – textual or ClauseElement construct which will be rendered following the target clause.

dialect¶ – Optional string dialect name which will limit rendering of this suffix to only that dialect.

Return a SQL UNION of this select() construct against the given selectables provided as positional arguments.

one or more elements with which to create a UNION.

Changed in version 1.4.28: multiple elements are now accepted.

**kwargs¶ – keyword arguments are forwarded to the constructor for the newly created CompoundSelect object.

Return a SQL UNION ALL of this select() construct against the given selectables provided as positional arguments.

one or more elements with which to create a UNION.

Changed in version 1.4.28: multiple elements are now accepted.

**kwargs¶ – keyword arguments are forwarded to the constructor for the newly created CompoundSelect object.

Return a new select() construct with the given expression added to its WHERE clause, joined to the existing clause via AND, if any.

Return the completed WHERE clause for this Select statement.

This assembles the current collection of WHERE criteria into a single BooleanClauseList construct.

Added in version 1.4.

inherited from the GenerativeSelect.with_for_update() method of GenerativeSelect

Specify a FOR UPDATE clause for this GenerativeSelect.

On a database like PostgreSQL or Oracle Database, the above would render a statement like:

on other backends, the nowait option is ignored and instead would produce:

When called with no arguments, the statement will render with the suffix FOR UPDATE. Additional arguments can then be provided which allow for common database-specific variants.

nowait¶ – boolean; will render FOR UPDATE NOWAIT on Oracle Database and PostgreSQL dialects.

read¶ – boolean; will render LOCK IN SHARE MODE on MySQL, FOR SHARE on PostgreSQL. On PostgreSQL, when combined with nowait, will render FOR SHARE NOWAIT.

of¶ – SQL expression or list of SQL expression elements, (typically Column objects or a compatible expression, for some backends may also be a table expression) which will render into a FOR UPDATE OF clause; supported by PostgreSQL, Oracle Database, some MySQL versions and possibly others. May render as a table or as a column depending on backend.

skip_locked¶ – boolean, will render FOR UPDATE SKIP LOCKED on Oracle Database and PostgreSQL dialects or FOR SHARE SKIP LOCKED if read=True is also specified.

key_share¶ – boolean, will render FOR NO KEY UPDATE, or if combined with read=True will render FOR KEY SHARE, on the PostgreSQL dialect.

inherited from the HasHints.with_hint() method of HasHints

Add an indexing or other executional context hint for the given selectable to this Select or other selectable object.

The Select.with_hint() method adds hints that are specific to a single table to a statement, in a location that is dialect-specific. To add generic optimizer hints to the beginning of a statement ahead of the SELECT keyword such as for MySQL or Oracle Database, use the Select.prefix_with() method. To add optimizer hints to the end of a statement such as for PostgreSQL, use the Select.with_statement_hint() method.

The text of the hint is rendered in the appropriate location for the database backend in use, relative to the given Table or Alias passed as the selectable argument. The dialect implementation typically uses Python string substitution syntax with the token %(name)s to render the name of the table or alias. E.g. when using Oracle Database, the following:

The dialect_name option will limit the rendering of a particular hint to a particular backend. Such as, to add hints for both Oracle Database and MSSql simultaneously:

Select.with_statement_hint()

Select.prefix_with() - generic SELECT prefixing which also can suit some database-specific HINT syntaxes such as MySQL or Oracle Database optimizer hints

Return a new select() construct with its columns clause replaced with the given entities.

By default, this method is exactly equivalent to as if the original select() had been called with the given entities. E.g. a statement:

should be exactly equivalent to:

In this mode of operation, Select.with_only_columns() will also dynamically alter the FROM clause of the statement if it is not explicitly stated. To maintain the existing set of FROMs including those implied by the current columns clause, add the Select.with_only_columns.maintain_column_froms parameter:

The above parameter performs a transfer of the effective FROMs in the columns collection to the Select.select_from() method, as though the following were invoked:

The Select.with_only_columns.maintain_column_froms parameter makes use of the Select.columns_clause_froms collection and performs an operation equivalent to the following:

*entities¶ – column expressions to be used.

maintain_column_froms¶ –

boolean parameter that will ensure the FROM list implied from the current columns clause will be transferred to the Select.select_from() method first.

Added in version 1.4.23.

inherited from the HasHints.with_statement_hint() method of HasHints

Add a statement hint to this Select or other selectable object.

Select.with_statement_hint() generally adds hints at the trailing end of a SELECT statement. To place dialect-specific hints such as optimizer hints at the front of the SELECT statement after the SELECT keyword, use the Select.prefix_with() method for an open-ended space, or for table-specific hints the Select.with_hint() may be used, which places hints in a dialect-specific location.

This method is similar to Select.with_hint() except that it does not require an individual table, and instead applies to the statement as a whole.

Hints here are specific to the backend database and may include directives such as isolation levels, file directives, fetch directives, etc.

Select.prefix_with() - generic SELECT prefixing which also can suit some database-specific HINT syntaxes such as MySQL or Oracle Database optimizer hints

inherits from sqlalchemy.sql.expression.ReturnsRows

Mark a class as being selectable.

Compile this SQL expression.

corresponding_column()

Given a ColumnElement, return the exported ColumnElement object from the Selectable.exported_columns collection of this Selectable which corresponds to that original ColumnElement via a common ancestor column.

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

Return True if this ReturnsRows is ‘derived’ from the given FromClause.

Return a LATERAL alias of this Selectable.

Replace all occurrences of FromClause ‘old’ with the given Alias object, returning a copy of this FromClause.

inherited from the CompilerElement.compile() method of CompilerElement

Compile this SQL expression.

The return value is a Compiled object. Calling str() or unicode() on the returned value will yield a string representation of the result. The Compiled object also can return a dictionary of bind parameter names and values using the params accessor.

bind¶ – An Connection or Engine which can provide a Dialect in order to generate a Compiled object. If the bind and dialect parameters are both omitted, a default SQL compiler is used.

column_keys¶ – Used for INSERT and UPDATE statements, a list of column names which should be present in the VALUES clause of the compiled statement. If None, all columns from the target table object are rendered.

dialect¶ – A Dialect instance which can generate a Compiled object. This argument takes precedence over the bind argument.

optional dictionary of additional parameters that will be passed through to the compiler within all “visit” methods. This allows any custom flag to be passed through to a custom compilation construct, for example. It is also used for the case of passing the literal_binds flag through:

How do I render SQL expressions as strings, possibly with bound parameters inlined?

Given a ColumnElement, return the exported ColumnElement object from the Selectable.exported_columns collection of this Selectable which corresponds to that original ColumnElement via a common ancestor column.

column¶ – the target ColumnElement to be matched.

require_embedded¶ – only return corresponding columns for the given ColumnElement, if the given ColumnElement is actually present within a sub-element of this Selectable. Normally the column will match if it merely shares a common ancestor with one of the exported columns of this Selectable.

Selectable.exported_columns - the ColumnCollection that is used for the operation.

ColumnCollection.corresponding_column() - implementation method.

A ColumnCollection that represents the “exported” columns of this ReturnsRows.

The “exported” columns represent the collection of ColumnElement expressions that are rendered by this SQL construct. There are primary varieties which are the “FROM clause columns” of a FROM clause, such as a table, join, or subquery, the “SELECTed columns”, which are the columns in the “columns clause” of a SELECT statement, and the RETURNING columns in a DML statement..

Added in version 1.4.

FromClause.exported_columns

SelectBase.exported_columns

inherited from the HasTraverseInternals.get_children() method of HasTraverseInternals

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

This is used for visit traversal.

**kw may contain flags that change the collection that is returned, for example to return a subset of items in order to cut down on larger traversals, or to return child items from a different context (such as schema-level collections instead of clause-level).

inherited from the HasCacheKey.inherit_cache attribute of HasCacheKey

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

inherited from the ReturnsRows.is_derived_from() method of ReturnsRows

Return True if this ReturnsRows is ‘derived’ from the given FromClause.

An example would be an Alias of a Table is derived from that Table.

Return a LATERAL alias of this Selectable.

The return value is the Lateral construct also provided by the top-level lateral() function.

LATERAL correlation - overview of usage.

Replace all occurrences of FromClause ‘old’ with the given Alias object, returning a copy of this FromClause.

Deprecated since version 1.4: The Selectable.replace_selectable() method is deprecated, and will be removed in a future release. Similar functionality is available via the sqlalchemy.sql.visitors module.

inherits from sqlalchemy.sql.roles.SelectStatementRole, sqlalchemy.sql.roles.DMLSelectRole, sqlalchemy.sql.roles.CompoundElementRole, sqlalchemy.sql.roles.InElementRole, sqlalchemy.sql.expression.HasCTE, sqlalchemy.sql.annotation.SupportsCloneAnnotations, sqlalchemy.sql.expression.Selectable

Base class for SELECT statements.

This includes Select, CompoundSelect and TextualSelect.

Add one or more CTE constructs to this statement.

Return a named subquery against this SelectBase.

Compile this SQL expression.

corresponding_column()

Given a ColumnElement, return the exported ColumnElement object from the Selectable.exported_columns collection of this Selectable which corresponds to that original ColumnElement via a common ancestor column.

Return a new CTE, or Common Table Expression instance.

Return an Exists representation of this selectable, which can be used as a column expression.

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

Retrieve the current label style.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

Return True if this ReturnsRows is ‘derived’ from the given FromClause.

Return a ‘scalar’ representation of this selectable, embedded as a subquery with a label.

Return a LATERAL alias of this Selectable.

indicates if this HasCTE as contained within a CTE should compel the CTE to render the column names of this object in the WITH clause.

Replace all occurrences of FromClause ‘old’ with the given Alias object, returning a copy of this FromClause.

Return a ‘scalar’ representation of this selectable, which can be used as a column expression.

A ColumnCollection representing the columns that this SELECT statement or similar construct returns in its result set.

Return a new selectable with the specified label style.

Return a subquery of this SelectBase.

inherited from the HasCTE.add_cte() method of HasCTE

Add one or more CTE constructs to this statement.

This method will associate the given CTE constructs with the parent statement such that they will each be unconditionally rendered in the WITH clause of the final statement, even if not referenced elsewhere within the statement or any sub-selects.

The optional HasCTE.add_cte.nest_here parameter when set to True will have the effect that each given CTE will render in a WITH clause rendered directly along with this statement, rather than being moved to the top of the ultimate rendered statement, even if this statement is rendered as a subquery within a larger statement.

This method has two general uses. One is to embed CTE statements that serve some purpose without being referenced explicitly, such as the use case of embedding a DML statement such as an INSERT or UPDATE as a CTE inline with a primary statement that may draw from its results indirectly. The other is to provide control over the exact placement of a particular series of CTE constructs that should remain rendered directly in terms of a particular statement that may be nested in a larger statement.

Above, the “anon_1” CTE is not referenced in the SELECT statement, however still accomplishes the task of running an INSERT statement.

Similarly in a DML-related context, using the PostgreSQL Insert construct to generate an “upsert”:

The above statement renders as:

Added in version 1.4.21.

zero or more CTE constructs.

Changed in version 2.0: Multiple CTE instances are accepted

if True, the given CTE or CTEs will be rendered as though they specified the HasCTE.cte.nesting flag to True when they were added to this HasCTE. Assuming the given CTEs are not referenced in an outer-enclosing statement as well, the CTEs given should render at the level of this statement when this flag is given.

Added in version 2.0.

Return a named subquery against this SelectBase.

For a SelectBase (as opposed to a FromClause), this returns a Subquery object which behaves mostly the same as the Alias object that is used with a FromClause.

Changed in version 1.4: The SelectBase.alias() method is now a synonym for the SelectBase.subquery() method.

Deprecated since version 1.4: The SelectBase.as_scalar() method is deprecated and will be removed in a future release. Please refer to SelectBase.scalar_subquery().

Deprecated since version 1.4: The SelectBase.c and SelectBase.columns attributes are deprecated and will be removed in a future release; these attributes implicitly create a subquery that should be explicit. Please call SelectBase.subquery() first in order to create a subquery, which then contains this attribute. To access the columns that this SELECT object SELECTs from, use the SelectBase.selected_columns attribute.

inherited from the CompilerElement.compile() method of CompilerElement

Compile this SQL expression.

The return value is a Compiled object. Calling str() or unicode() on the returned value will yield a string representation of the result. The Compiled object also can return a dictionary of bind parameter names and values using the params accessor.

bind¶ – An Connection or Engine which can provide a Dialect in order to generate a Compiled object. If the bind and dialect parameters are both omitted, a default SQL compiler is used.

column_keys¶ – Used for INSERT and UPDATE statements, a list of column names which should be present in the VALUES clause of the compiled statement. If None, all columns from the target table object are rendered.

dialect¶ – A Dialect instance which can generate a Compiled object. This argument takes precedence over the bind argument.

optional dictionary of additional parameters that will be passed through to the compiler within all “visit” methods. This allows any custom flag to be passed through to a custom compilation construct, for example. It is also used for the case of passing the literal_binds flag through:

How do I render SQL expressions as strings, possibly with bound parameters inlined?

inherited from the Selectable.corresponding_column() method of Selectable

Given a ColumnElement, return the exported ColumnElement object from the Selectable.exported_columns collection of this Selectable which corresponds to that original ColumnElement via a common ancestor column.

column¶ – the target ColumnElement to be matched.

require_embedded¶ – only return corresponding columns for the given ColumnElement, if the given ColumnElement is actually present within a sub-element of this Selectable. Normally the column will match if it merely shares a common ancestor with one of the exported columns of this Selectable.

Selectable.exported_columns - the ColumnCollection that is used for the operation.

ColumnCollection.corresponding_column() - implementation method.

inherited from the HasCTE.cte() method of HasCTE

Return a new CTE, or Common Table Expression instance.

Common table expressions are a SQL standard whereby SELECT statements can draw upon secondary statements specified along with the primary statement, using a clause called “WITH”. Special semantics regarding UNION can also be employed to allow “recursive” queries, where a SELECT statement can draw upon the set of rows that have previously been selected.

CTEs can also be applied to DML constructs UPDATE, INSERT and DELETE on some databases, both as a source of CTE rows when combined with RETURNING, as well as a consumer of CTE rows.

SQLAlchemy detects CTE objects, which are treated similarly to Alias objects, as special elements to be delivered to the FROM clause of the statement as well as to a WITH clause at the top of the statement.

For special prefixes such as PostgreSQL “MATERIALIZED” and “NOT MATERIALIZED”, the CTE.prefix_with() method may be used to establish these.

Changed in version 1.3.13: Added support for prefixes. In particular - MATERIALIZED and NOT MATERIALIZED.

name¶ – name given to the common table expression. Like FromClause.alias(), the name can be left as None in which case an anonymous symbol will be used at query compile time.

recursive¶ – if True, will render WITH RECURSIVE. A recursive common table expression is intended to be used in conjunction with UNION ALL in order to derive rows from those already selected.

if True, will render the CTE locally to the statement in which it is referenced. For more complex scenarios, the HasCTE.add_cte() method using the HasCTE.add_cte.nest_here parameter may also be used to more carefully control the exact placement of a particular CTE.

Added in version 1.4.24.

The following examples include two from PostgreSQL’s documentation at https://www.postgresql.org/docs/current/static/queries-with.html, as well as additional examples.

Example 1, non recursive:

Example 2, WITH RECURSIVE:

Example 3, an upsert using UPDATE and INSERT with CTEs:

Example 4, Nesting CTE (SQLAlchemy 1.4.24 and above):

The above query will render the second CTE nested inside the first, shown with inline parameters below as:

The same CTE can be set up using the HasCTE.add_cte() method as follows (SQLAlchemy 2.0 and above):

Example 5, Non-Linear CTE (SQLAlchemy 1.4.28 and above):

The above query will render 2 UNIONs inside the recursive CTE:

Query.cte() - ORM version of HasCTE.cte().

Return an Exists representation of this selectable, which can be used as a column expression.

The returned object is an instance of Exists.

EXISTS subqueries - in the 2.0 style tutorial.

Added in version 1.4.

A ColumnCollection that represents the “exported” columns of this Selectable, not including TextClause constructs.

The “exported” columns for a SelectBase object are synonymous with the SelectBase.selected_columns collection.

Added in version 1.4.

Select.exported_columns

Selectable.exported_columns

FromClause.exported_columns

inherited from the HasTraverseInternals.get_children() method of HasTraverseInternals

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

This is used for visit traversal.

**kw may contain flags that change the collection that is returned, for example to return a subset of items in order to cut down on larger traversals, or to return child items from a different context (such as schema-level collections instead of clause-level).

Retrieve the current label style.

Implemented by subclasses.

inherited from the HasCacheKey.inherit_cache attribute of HasCacheKey

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

inherited from the ReturnsRows.is_derived_from() method of ReturnsRows

Return True if this ReturnsRows is ‘derived’ from the given FromClause.

An example would be an Alias of a Table is derived from that Table.

Return a ‘scalar’ representation of this selectable, embedded as a subquery with a label.

SelectBase.scalar_subquery().

Return a LATERAL alias of this Selectable.

The return value is the Lateral construct also provided by the top-level lateral() function.

LATERAL correlation - overview of usage.

inherited from the HasCTE.name_cte_columns attribute of HasCTE

indicates if this HasCTE as contained within a CTE should compel the CTE to render the column names of this object in the WITH clause.

Added in version 2.0.42.

inherited from the Selectable.replace_selectable() method of Selectable

Replace all occurrences of FromClause ‘old’ with the given Alias object, returning a copy of this FromClause.

Deprecated since version 1.4: The Selectable.replace_selectable() method is deprecated, and will be removed in a future release. Similar functionality is available via the sqlalchemy.sql.visitors module.

Return a ‘scalar’ representation of this selectable, which can be used as a column expression.

The returned object is an instance of ScalarSelect.

Typically, a select statement which has only one column in its columns clause is eligible to be used as a scalar expression. The scalar subquery can then be used in the WHERE clause or columns clause of an enclosing SELECT.

Note that the scalar subquery differentiates from the FROM-level subquery that can be produced using the SelectBase.subquery() method.

Scalar and Correlated Subqueries - in the 2.0 tutorial

Deprecated since version 1.4: The SelectBase.select() method is deprecated and will be removed in a future release; this method implicitly creates a subquery that should be explicit. Please call SelectBase.subquery() first in order to create a subquery, which then can be selected.

A ColumnCollection representing the columns that this SELECT statement or similar construct returns in its result set.

This collection differs from the FromClause.columns collection of a FromClause in that the columns within this collection cannot be directly nested inside another SELECT statement; a subquery must be applied first which provides for the necessary parenthesization required by SQL.

The SelectBase.selected_columns collection does not include expressions established in the columns clause using the text() construct; these are silently omitted from the collection. To use plain textual column expressions inside of a Select construct, use the literal_column() construct.

Select.selected_columns

Added in version 1.4.

Return a new selectable with the specified label style.

Implemented by subclasses.

Return a subquery of this SelectBase.

A subquery is from a SQL perspective a parenthesized, named construct that can be placed in the FROM clause of another SELECT statement.

Given a SELECT statement such as:

The above statement might look like:

The subquery form by itself renders the same way, however when embedded into the FROM clause of another SELECT statement, it becomes a named sub-element:

The above renders as:

Historically, SelectBase.subquery() is equivalent to calling the FromClause.alias() method on a FROM object; however, as a SelectBase object is not directly FROM object, the SelectBase.subquery() method provides clearer semantics.

Added in version 1.4.

inherits from sqlalchemy.sql.expression.AliasedReturnsRows

Represent a subquery of a SELECT.

A Subquery is created by invoking the SelectBase.subquery() method, or for convenience the SelectBase.alias() method, on any SelectBase subclass which includes Select, CompoundSelect, and TextualSelect. As rendered in a FROM clause, it represents the body of the SELECT statement inside of parenthesis, followed by the usual “AS <somename>” that defines all “alias” objects.

The Subquery object is very similar to the Alias object and can be used in an equivalent way. The difference between Alias and Subquery is that Alias always contains a FromClause object whereas Subquery always contains a SelectBase object.

Added in version 1.4: The Subquery class was added which now serves the purpose of providing an aliased version of a SELECT statement.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

Deprecated since version 1.4: The Subquery.as_scalar() method, which was previously Alias.as_scalar() prior to version 1.4, is deprecated and will be removed in a future release; Please use the Select.scalar_subquery() method of the select() construct before constructing a subquery object, or with the ORM use the Query.scalar_subquery() method.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

inherits from sqlalchemy.sql.roles.DMLTableRole, sqlalchemy.sql.expression.Immutable, sqlalchemy.sql.expression.NamedFromClause

Represents a minimal “table” construct.

This is a lightweight table object that has only a name, a collection of columns, which are typically produced by the column() function, and a schema:

The TableClause construct serves as the base for the more commonly used Table object, providing the usual set of FromClause services including the .c. collection and statement generation methods.

It does not provide all the additional schema-level services of Table, including constraints, references to other tables, or support for MetaData-level services. It’s useful on its own as an ad-hoc construct used to generate quick SQL statements when a more fully fledged Table is not on hand.

Return an alias of this FromClause.

A synonym for FromClause.columns

A named-based collection of ColumnElement objects maintained by this FromClause.

Compare this ClauseElement to the given ClauseElement.

Compile this SQL expression.

corresponding_column()

Given a ColumnElement, return the exported ColumnElement object from the Selectable.exported_columns collection of this Selectable which corresponds to that original ColumnElement via a common ancestor column.

Generate a delete() construct against this TableClause.

Return a namespace used for name-based access in SQL expressions.

A ColumnCollection that represents the “exported” columns of this Selectable.

Return the collection of ForeignKey marker objects which this FromClause references.

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

TableClause doesn’t support having a primary key or column -level defaults, so implicit returning doesn’t apply.

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

Return a copy with bindparam() elements replaced.

Generate an update() construct against this TableClause.

inherited from the FromClause.alias() method of FromClause

Return an alias of this FromClause.

The above code creates an Alias object which can be used as a FROM clause in any SELECT statement.

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

inherited from the Selectable.corresponding_column() method of Selectable

Given a ColumnElement, return the exported ColumnElement object from the Selectable.exported_columns collection of this Selectable which corresponds to that original ColumnElement via a common ancestor column.

column¶ – the target ColumnElement to be matched.

require_embedded¶ – only return corresponding columns for the given ColumnElement, if the given ColumnElement is actually present within a sub-element of this Selectable. Normally the column will match if it merely shares a common ancestor with one of the exported columns of this Selectable.

Selectable.exported_columns - the ColumnCollection that is used for the operation.

ColumnCollection.corresponding_column() - implementation method.

Generate a delete() construct against this TableClause.

See delete() for argument and usage information.

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

inherited from the FromClause.foreign_keys attribute of FromClause

Return the collection of ForeignKey marker objects which this FromClause references.

Each ForeignKey is a member of a Table-wide ForeignKeyConstraint.

Table.foreign_key_constraints

inherited from the HasTraverseInternals.get_children() method of HasTraverseInternals

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

This is used for visit traversal.

**kw may contain flags that change the collection that is returned, for example to return a subset of items in order to cut down on larger traversals, or to return child items from a different context (such as schema-level collections instead of clause-level).

TableClause doesn’t support having a primary key or column -level defaults, so implicit returning doesn’t apply.

inherited from the HasCacheKey.inherit_cache attribute of HasCacheKey

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

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

inherited from the Immutable.unique_params() method of Immutable

Return a copy with bindparam() elements replaced.

Same functionality as ClauseElement.params(), except adds unique=True to affected bind parameters so that multiple statements can be used.

Generate an update() construct against this TableClause.

See update() for argument and usage information.

inherits from sqlalchemy.sql.expression.FromClauseAlias

Represent a TABLESAMPLE clause.

This object is constructed from the tablesample() module level function as well as the FromClause.tablesample() method available on all FromClause subclasses.

inherits from sqlalchemy.sql.expression.LateralFromClause, sqlalchemy.sql.expression.Alias

An alias against a “table valued” SQL function.

This construct provides for a SQL function that returns columns to be used in the FROM clause of a SELECT statement. The object is generated using the FunctionElement.table_valued() method, e.g.:

Added in version 1.4.0b2.

Table-Valued Functions - in the SQLAlchemy Unified Tutorial

Return a new alias of this TableValuedAlias.

Return a column expression representing this TableValuedAlias.

Return a new TableValuedAlias with the lateral flag set, so that it renders as LATERAL.

Apply “render derived” to this TableValuedAlias.

Return a new alias of this TableValuedAlias.

This creates a distinct FROM object that will be distinguished from the original one when used in a SQL statement.

Return a column expression representing this TableValuedAlias.

This accessor is used to implement the FunctionElement.column_valued() method. See that method for further details.

FunctionElement.column_valued()

Return a new TableValuedAlias with the lateral flag set, so that it renders as LATERAL.

Apply “render derived” to this TableValuedAlias.

This has the effect of the individual column names listed out after the alias name in the “AS” sequence, e.g.:

The with_types keyword will render column types inline within the alias expression (this syntax currently applies to the PostgreSQL database):

name¶ – optional string name that will be applied to the alias generated. If left as None, a unique anonymizing name will be used.

with_types¶ – if True, the derived columns will include the datatype specification with each column. This is a special syntax currently known to be required by PostgreSQL for some SQL functions.

inherits from sqlalchemy.sql.expression.SelectBase, sqlalchemy.sql.expression.ExecutableReturnsRows, sqlalchemy.sql.expression.Generative

Wrap a TextClause construct within a SelectBase interface.

This allows the TextClause object to gain a .c collection and other FROM-like capabilities such as FromClause.alias(), SelectBase.cte(), etc.

The TextualSelect construct is produced via the TextClause.columns() method - see that method for details.

Changed in version 1.4: the TextualSelect class was renamed from TextAsFrom, to more correctly suit its role as a SELECT-oriented object and not a FROM clause.

TextClause.columns() - primary creation interface.

Add one or more CTE constructs to this statement.

Return a named subquery against this SelectBase.

Compare this ClauseElement to the given ClauseElement.

Compile this SQL expression.

corresponding_column()

Given a ColumnElement, return the exported ColumnElement object from the Selectable.exported_columns collection of this Selectable which corresponds to that original ColumnElement via a common ancestor column.

Return a new CTE, or Common Table Expression instance.

Set non-SQL options for the statement which take effect during execution.

Return an Exists representation of this selectable, which can be used as a column expression.

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

get_execution_options()

Get the non-SQL options which will take effect during execution.

Retrieve the current label style.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

Return True if this ReturnsRows is ‘derived’ from the given FromClause.

Return a ‘scalar’ representation of this selectable, embedded as a subquery with a label.

Return a LATERAL alias of this Selectable.

indicates if this HasCTE as contained within a CTE should compel the CTE to render the column names of this object in the WITH clause.

Apply options to this statement.

Return a copy with bindparam() elements replaced.

Replace all occurrences of FromClause ‘old’ with the given Alias object, returning a copy of this FromClause.

Return a ‘scalar’ representation of this selectable, which can be used as a column expression.

A ColumnCollection representing the columns that this SELECT statement or similar construct returns in its result set, not including TextClause constructs.

Apply a ‘grouping’ to this ClauseElement.

Return a new selectable with the specified label style.

Return a subquery of this SelectBase.

Return a copy with bindparam() elements replaced.

inherited from the HasCTE.add_cte() method of HasCTE

Add one or more CTE constructs to this statement.

This method will associate the given CTE constructs with the parent statement such that they will each be unconditionally rendered in the WITH clause of the final statement, even if not referenced elsewhere within the statement or any sub-selects.

The optional HasCTE.add_cte.nest_here parameter when set to True will have the effect that each given CTE will render in a WITH clause rendered directly along with this statement, rather than being moved to the top of the ultimate rendered statement, even if this statement is rendered as a subquery within a larger statement.

This method has two general uses. One is to embed CTE statements that serve some purpose without being referenced explicitly, such as the use case of embedding a DML statement such as an INSERT or UPDATE as a CTE inline with a primary statement that may draw from its results indirectly. The other is to provide control over the exact placement of a particular series of CTE constructs that should remain rendered directly in terms of a particular statement that may be nested in a larger statement.

Above, the “anon_1” CTE is not referenced in the SELECT statement, however still accomplishes the task of running an INSERT statement.

Similarly in a DML-related context, using the PostgreSQL Insert construct to generate an “upsert”:

The above statement renders as:

Added in version 1.4.21.

zero or more CTE constructs.

Changed in version 2.0: Multiple CTE instances are accepted

if True, the given CTE or CTEs will be rendered as though they specified the HasCTE.cte.nesting flag to True when they were added to this HasCTE. Assuming the given CTEs are not referenced in an outer-enclosing statement as well, the CTEs given should render at the level of this statement when this flag is given.

Added in version 2.0.

inherited from the SelectBase.alias() method of SelectBase

Return a named subquery against this SelectBase.

For a SelectBase (as opposed to a FromClause), this returns a Subquery object which behaves mostly the same as the Alias object that is used with a FromClause.

Changed in version 1.4: The SelectBase.alias() method is now a synonym for the SelectBase.subquery() method.

inherited from the SelectBase.as_scalar() method of SelectBase

Deprecated since version 1.4: The SelectBase.as_scalar() method is deprecated and will be removed in a future release. Please refer to SelectBase.scalar_subquery().

Deprecated since version 1.4: The SelectBase.c and SelectBase.columns attributes are deprecated and will be removed in a future release; these attributes implicitly create a subquery that should be explicit. Please call SelectBase.subquery() first in order to create a subquery, which then contains this attribute. To access the columns that this SELECT object SELECTs from, use the SelectBase.selected_columns attribute.

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

inherited from the Selectable.corresponding_column() method of Selectable

Given a ColumnElement, return the exported ColumnElement object from the Selectable.exported_columns collection of this Selectable which corresponds to that original ColumnElement via a common ancestor column.

column¶ – the target ColumnElement to be matched.

require_embedded¶ – only return corresponding columns for the given ColumnElement, if the given ColumnElement is actually present within a sub-element of this Selectable. Normally the column will match if it merely shares a common ancestor with one of the exported columns of this Selectable.

Selectable.exported_columns - the ColumnCollection that is used for the operation.

ColumnCollection.corresponding_column() - implementation method.

inherited from the HasCTE.cte() method of HasCTE

Return a new CTE, or Common Table Expression instance.

Common table expressions are a SQL standard whereby SELECT statements can draw upon secondary statements specified along with the primary statement, using a clause called “WITH”. Special semantics regarding UNION can also be employed to allow “recursive” queries, where a SELECT statement can draw upon the set of rows that have previously been selected.

CTEs can also be applied to DML constructs UPDATE, INSERT and DELETE on some databases, both as a source of CTE rows when combined with RETURNING, as well as a consumer of CTE rows.

SQLAlchemy detects CTE objects, which are treated similarly to Alias objects, as special elements to be delivered to the FROM clause of the statement as well as to a WITH clause at the top of the statement.

For special prefixes such as PostgreSQL “MATERIALIZED” and “NOT MATERIALIZED”, the CTE.prefix_with() method may be used to establish these.

Changed in version 1.3.13: Added support for prefixes. In particular - MATERIALIZED and NOT MATERIALIZED.

name¶ – name given to the common table expression. Like FromClause.alias(), the name can be left as None in which case an anonymous symbol will be used at query compile time.

recursive¶ – if True, will render WITH RECURSIVE. A recursive common table expression is intended to be used in conjunction with UNION ALL in order to derive rows from those already selected.

if True, will render the CTE locally to the statement in which it is referenced. For more complex scenarios, the HasCTE.add_cte() method using the HasCTE.add_cte.nest_here parameter may also be used to more carefully control the exact placement of a particular CTE.

Added in version 1.4.24.

The following examples include two from PostgreSQL’s documentation at https://www.postgresql.org/docs/current/static/queries-with.html, as well as additional examples.

Example 1, non recursive:

Example 2, WITH RECURSIVE:

Example 3, an upsert using UPDATE and INSERT with CTEs:

Example 4, Nesting CTE (SQLAlchemy 1.4.24 and above):

The above query will render the second CTE nested inside the first, shown with inline parameters below as:

The same CTE can be set up using the HasCTE.add_cte() method as follows (SQLAlchemy 2.0 and above):

Example 5, Non-Linear CTE (SQLAlchemy 1.4.28 and above):

The above query will render 2 UNIONs inside the recursive CTE:

Query.cte() - ORM version of HasCTE.cte().

inherited from the Executable.execution_options() method of Executable

Set non-SQL options for the statement which take effect during execution.

Execution options can be set at many scopes, including per-statement, per-connection, or per execution, using methods such as Connection.execution_options() and parameters which accept a dictionary of options such as Connection.execute.execution_options and Session.execute.execution_options.

The primary characteristic of an execution option, as opposed to other kinds of options such as ORM loader options, is that execution options never affect the compiled SQL of a query, only things that affect how the SQL statement itself is invoked or how results are fetched. That is, execution options are not part of what’s accommodated by SQL compilation nor are they considered part of the cached state of a statement.

The Executable.execution_options() method is generative, as is the case for the method as applied to the Engine and Query objects, which means when the method is called, a copy of the object is returned, which applies the given parameters to that new copy, but leaves the original unchanged:

An exception to this behavior is the Connection object, where the Connection.execution_options() method is explicitly not generative.

The kinds of options that may be passed to Executable.execution_options() and other related methods and parameter dictionaries include parameters that are explicitly consumed by SQLAlchemy Core or ORM, as well as arbitrary keyword arguments not defined by SQLAlchemy, which means the methods and/or parameter dictionaries may be used for user-defined parameters that interact with custom code, which may access the parameters using methods such as Executable.get_execution_options() and Connection.get_execution_options(), or within selected event hooks using a dedicated execution_options event parameter such as ConnectionEvents.before_execute.execution_options or ORMExecuteState.execution_options, e.g.:

Within the scope of options that are explicitly recognized by SQLAlchemy, most apply to specific classes of objects and not others. The most common execution options include:

Connection.execution_options.isolation_level - sets the isolation level for a connection or a class of connections via an Engine. This option is accepted only by Connection or Engine.

Connection.execution_options.stream_results - indicates results should be fetched using a server side cursor; this option is accepted by Connection, by the Connection.execute.execution_options parameter on Connection.execute(), and additionally by Executable.execution_options() on a SQL statement object, as well as by ORM constructs like Session.execute().

Connection.execution_options.compiled_cache - indicates a dictionary that will serve as the SQL compilation cache for a Connection or Engine, as well as for ORM methods like Session.execute(). Can be passed as None to disable caching for statements. This option is not accepted by Executable.execution_options() as it is inadvisable to carry along a compilation cache within a statement object.

Connection.execution_options.schema_translate_map - a mapping of schema names used by the Schema Translate Map feature, accepted by Connection, Engine, Executable, as well as by ORM constructs like Session.execute().

Connection.execution_options()

Connection.execute.execution_options

Session.execute.execution_options

ORM Execution Options - documentation on all ORM-specific execution options

inherited from the SelectBase.exists() method of SelectBase

Return an Exists representation of this selectable, which can be used as a column expression.

The returned object is an instance of Exists.

EXISTS subqueries - in the 2.0 style tutorial.

Added in version 1.4.

A ColumnCollection that represents the “exported” columns of this Selectable, not including TextClause constructs.

The “exported” columns for a SelectBase object are synonymous with the SelectBase.selected_columns collection.

Added in version 1.4.

Select.exported_columns

Selectable.exported_columns

FromClause.exported_columns

inherited from the HasTraverseInternals.get_children() method of HasTraverseInternals

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

This is used for visit traversal.

**kw may contain flags that change the collection that is returned, for example to return a subset of items in order to cut down on larger traversals, or to return child items from a different context (such as schema-level collections instead of clause-level).

inherited from the Executable.get_execution_options() method of Executable

Get the non-SQL options which will take effect during execution.

Added in version 1.3.

Executable.execution_options()

inherited from the SelectBase.get_label_style() method of SelectBase

Retrieve the current label style.

Implemented by subclasses.

inherited from the HasCacheKey.inherit_cache attribute of HasCacheKey

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

inherited from the ReturnsRows.is_derived_from() method of ReturnsRows

Return True if this ReturnsRows is ‘derived’ from the given FromClause.

An example would be an Alias of a Table is derived from that Table.

inherited from the SelectBase.label() method of SelectBase

Return a ‘scalar’ representation of this selectable, embedded as a subquery with a label.

SelectBase.scalar_subquery().

inherited from the SelectBase.lateral() method of SelectBase

Return a LATERAL alias of this Selectable.

The return value is the Lateral construct also provided by the top-level lateral() function.

LATERAL correlation - overview of usage.

inherited from the HasCTE.name_cte_columns attribute of HasCTE

indicates if this HasCTE as contained within a CTE should compel the CTE to render the column names of this object in the WITH clause.

Added in version 2.0.42.

inherited from the Executable.options() method of Executable

Apply options to this statement.

In the general sense, options are any kind of Python object that can be interpreted by the SQL compiler for the statement. These options can be consumed by specific dialects or specific kinds of compilers.

The most commonly known kind of option are the ORM level options that apply “eager load” and other loading behaviors to an ORM query. However, options can theoretically be used for many other purposes.

For background on specific kinds of options for specific kinds of statements, refer to the documentation for those option objects.

Changed in version 1.4: - added Executable.options() to Core statement objects towards the goal of allowing unified Core / ORM querying capabilities.

Column Loading Options - refers to options specific to the usage of ORM queries

Relationship Loading with Loader Options - refers to options specific to the usage of ORM queries

inherited from the ClauseElement.params() method of ClauseElement

Return a copy with bindparam() elements replaced.

Returns a copy of this ClauseElement with bindparam() elements replaced with values taken from the given dictionary:

inherited from the Selectable.replace_selectable() method of Selectable

Replace all occurrences of FromClause ‘old’ with the given Alias object, returning a copy of this FromClause.

Deprecated since version 1.4: The Selectable.replace_selectable() method is deprecated, and will be removed in a future release. Similar functionality is available via the sqlalchemy.sql.visitors module.

inherited from the SelectBase.scalar_subquery() method of SelectBase

Return a ‘scalar’ representation of this selectable, which can be used as a column expression.

The returned object is an instance of ScalarSelect.

Typically, a select statement which has only one column in its columns clause is eligible to be used as a scalar expression. The scalar subquery can then be used in the WHERE clause or columns clause of an enclosing SELECT.

Note that the scalar subquery differentiates from the FROM-level subquery that can be produced using the SelectBase.subquery() method.

Scalar and Correlated Subqueries - in the 2.0 tutorial

inherited from the SelectBase.select() method of SelectBase

Deprecated since version 1.4: The SelectBase.select() method is deprecated and will be removed in a future release; this method implicitly creates a subquery that should be explicit. Please call SelectBase.subquery() first in order to create a subquery, which then can be selected.

A ColumnCollection representing the columns that this SELECT statement or similar construct returns in its result set, not including TextClause constructs.

This collection differs from the FromClause.columns collection of a FromClause in that the columns within this collection cannot be directly nested inside another SELECT statement; a subquery must be applied first which provides for the necessary parenthesization required by SQL.

For a TextualSelect construct, the collection contains the ColumnElement objects that were passed to the constructor, typically via the TextClause.columns() method.

Added in version 1.4.

inherited from the ClauseElement.self_group() method of ClauseElement

Apply a ‘grouping’ to this ClauseElement.

This method is overridden by subclasses to return a “grouping” construct, i.e. parenthesis. In particular it’s used by “binary” expressions to provide a grouping around themselves when placed into a larger expression, as well as by select() constructs when placed into the FROM clause of another select(). (Note that subqueries should be normally created using the Select.alias() method, as many platforms require nested SELECT statements to be named).

As expressions are composed together, the application of self_group() is automatic - end-user code should never need to use this method directly. Note that SQLAlchemy’s clause constructs take operator precedence into account - so parenthesis might not be needed, for example, in an expression like x OR (y AND z) - AND takes precedence over OR.

The base self_group() method of ClauseElement just returns self.

Return a new selectable with the specified label style.

Implemented by subclasses.

inherited from the SelectBase.subquery() method of SelectBase

Return a subquery of this SelectBase.

A subquery is from a SQL perspective a parenthesized, named construct that can be placed in the FROM clause of another SELECT statement.

Given a SELECT statement such as:

The above statement might look like:

The subquery form by itself renders the same way, however when embedded into the FROM clause of another SELECT statement, it becomes a named sub-element:

The above renders as:

Historically, SelectBase.subquery() is equivalent to calling the FromClause.alias() method on a FROM object; however, as a SelectBase object is not directly FROM object, the SelectBase.subquery() method provides clearer semantics.

Added in version 1.4.

inherited from the ClauseElement.unique_params() method of ClauseElement

Return a copy with bindparam() elements replaced.

Same functionality as ClauseElement.params(), except adds unique=True to affected bind parameters so that multiple statements can be used.

inherits from sqlalchemy.sql.roles.InElementRole, sqlalchemy.sql.expression.HasCTE, sqlalchemy.sql.expression.Generative, sqlalchemy.sql.expression.LateralFromClause

Represent a VALUES construct that can be used as a FROM element in a statement.

The Values object is created from the values() function.

Added in version 1.4.

Add one or more CTE constructs to this statement.

Return a new Values construct that is a copy of this one with the given name.

Compile this SQL expression.

Return a new CTE, or Common Table Expression instance.

Return a new Values construct, adding the given data to the data list.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

Return a new Values with the lateral flag set, so that it renders as LATERAL.

indicates if this HasCTE as contained within a CTE should compel the CTE to render the column names of this object in the WITH clause.

Returns a scalar VALUES construct that can be used as a COLUMN element in a statement.

Return a TableValuedColumn object for this FromClause.

inherited from the HasCTE.add_cte() method of HasCTE

Add one or more CTE constructs to this statement.

This method will associate the given CTE constructs with the parent statement such that they will each be unconditionally rendered in the WITH clause of the final statement, even if not referenced elsewhere within the statement or any sub-selects.

The optional HasCTE.add_cte.nest_here parameter when set to True will have the effect that each given CTE will render in a WITH clause rendered directly along with this statement, rather than being moved to the top of the ultimate rendered statement, even if this statement is rendered as a subquery within a larger statement.

This method has two general uses. One is to embed CTE statements that serve some purpose without being referenced explicitly, such as the use case of embedding a DML statement such as an INSERT or UPDATE as a CTE inline with a primary statement that may draw from its results indirectly. The other is to provide control over the exact placement of a particular series of CTE constructs that should remain rendered directly in terms of a particular statement that may be nested in a larger statement.

Above, the “anon_1” CTE is not referenced in the SELECT statement, however still accomplishes the task of running an INSERT statement.

Similarly in a DML-related context, using the PostgreSQL Insert construct to generate an “upsert”:

The above statement renders as:

Added in version 1.4.21.

zero or more CTE constructs.

Changed in version 2.0: Multiple CTE instances are accepted

if True, the given CTE or CTEs will be rendered as though they specified the HasCTE.cte.nesting flag to True when they were added to this HasCTE. Assuming the given CTEs are not referenced in an outer-enclosing statement as well, the CTEs given should render at the level of this statement when this flag is given.

Added in version 2.0.

Return a new Values construct that is a copy of this one with the given name.

This method is a VALUES-specific specialization of the FromClause.alias() method.

inherited from the CompilerElement.compile() method of CompilerElement

Compile this SQL expression.

The return value is a Compiled object. Calling str() or unicode() on the returned value will yield a string representation of the result. The Compiled object also can return a dictionary of bind parameter names and values using the params accessor.

bind¶ – An Connection or Engine which can provide a Dialect in order to generate a Compiled object. If the bind and dialect parameters are both omitted, a default SQL compiler is used.

column_keys¶ – Used for INSERT and UPDATE statements, a list of column names which should be present in the VALUES clause of the compiled statement. If None, all columns from the target table object are rendered.

dialect¶ – A Dialect instance which can generate a Compiled object. This argument takes precedence over the bind argument.

optional dictionary of additional parameters that will be passed through to the compiler within all “visit” methods. This allows any custom flag to be passed through to a custom compilation construct, for example. It is also used for the case of passing the literal_binds flag through:

How do I render SQL expressions as strings, possibly with bound parameters inlined?

inherited from the HasCTE.cte() method of HasCTE

Return a new CTE, or Common Table Expression instance.

Common table expressions are a SQL standard whereby SELECT statements can draw upon secondary statements specified along with the primary statement, using a clause called “WITH”. Special semantics regarding UNION can also be employed to allow “recursive” queries, where a SELECT statement can draw upon the set of rows that have previously been selected.

CTEs can also be applied to DML constructs UPDATE, INSERT and DELETE on some databases, both as a source of CTE rows when combined with RETURNING, as well as a consumer of CTE rows.

SQLAlchemy detects CTE objects, which are treated similarly to Alias objects, as special elements to be delivered to the FROM clause of the statement as well as to a WITH clause at the top of the statement.

For special prefixes such as PostgreSQL “MATERIALIZED” and “NOT MATERIALIZED”, the CTE.prefix_with() method may be used to establish these.

Changed in version 1.3.13: Added support for prefixes. In particular - MATERIALIZED and NOT MATERIALIZED.

name¶ – name given to the common table expression. Like FromClause.alias(), the name can be left as None in which case an anonymous symbol will be used at query compile time.

recursive¶ – if True, will render WITH RECURSIVE. A recursive common table expression is intended to be used in conjunction with UNION ALL in order to derive rows from those already selected.

if True, will render the CTE locally to the statement in which it is referenced. For more complex scenarios, the HasCTE.add_cte() method using the HasCTE.add_cte.nest_here parameter may also be used to more carefully control the exact placement of a particular CTE.

Added in version 1.4.24.

The following examples include two from PostgreSQL’s documentation at https://www.postgresql.org/docs/current/static/queries-with.html, as well as additional examples.

Example 1, non recursive:

Example 2, WITH RECURSIVE:

Example 3, an upsert using UPDATE and INSERT with CTEs:

Example 4, Nesting CTE (SQLAlchemy 1.4.24 and above):

The above query will render the second CTE nested inside the first, shown with inline parameters below as:

The same CTE can be set up using the HasCTE.add_cte() method as follows (SQLAlchemy 2.0 and above):

Example 5, Non-Linear CTE (SQLAlchemy 1.4.28 and above):

The above query will render 2 UNIONs inside the recursive CTE:

Query.cte() - ORM version of HasCTE.cte().

Return a new Values construct, adding the given data to the data list.

values¶ – a sequence (i.e. list) of tuples that map to the column expressions given in the Values constructor.

inherited from the HasCacheKey.inherit_cache attribute of HasCacheKey

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

Return a new Values with the lateral flag set, so that it renders as LATERAL.

indicates if this HasCTE as contained within a CTE should compel the CTE to render the column names of this object in the WITH clause.

Added in version 2.0.42.

Returns a scalar VALUES construct that can be used as a COLUMN element in a statement.

Added in version 2.0.0b4.

inherited from the NamedFromClause.table_valued() method of NamedFromClause

Return a TableValuedColumn object for this FromClause.

A TableValuedColumn is a ColumnElement that represents a complete row in a table. Support for this construct is backend dependent, and is supported in various forms by backends such as PostgreSQL, Oracle Database and SQL Server.

Added in version 1.4.0b2.

Working with SQL Functions - in the SQLAlchemy Unified Tutorial

inherits from sqlalchemy.sql.roles.InElementRole, sqlalchemy.sql.expression.GroupedElement, sqlalchemy.sql.expression.ColumnElement

Represent a scalar VALUES construct that can be used as a COLUMN element in a statement.

The ScalarValues object is created from the Values.scalar_values() method. It’s also automatically generated when a Values is used in an IN or NOT IN condition.

Added in version 2.0.0b4.

Constants used with the GenerativeSelect.set_label_style() method.

Label style constants that may be passed to Select.set_label_style().

inherits from enum.Enum

Label style constants that may be passed to Select.set_label_style().

The default label style, refers to LABEL_STYLE_DISAMBIGUATE_ONLY.

LABEL_STYLE_DISAMBIGUATE_ONLY

Label style indicating that columns with a name that conflicts with an existing name should be labeled with a semi-anonymizing label when generating the columns clause of a SELECT statement.

Label style indicating no automatic labeling should be applied to the columns clause of a SELECT statement.

LABEL_STYLE_TABLENAME_PLUS_COL

Label style indicating all columns should be labeled as <tablename>_<columnname> when generating the columns clause of a SELECT statement, to disambiguate same-named columns referenced from different tables, aliases, or subqueries.

The default label style, refers to LABEL_STYLE_DISAMBIGUATE_ONLY.

Added in version 1.4.

Label style indicating that columns with a name that conflicts with an existing name should be labeled with a semi-anonymizing label when generating the columns clause of a SELECT statement.

Below, most column names are left unaffected, except for the second occurrence of the name columna, which is labeled using the label columna_1 to disambiguate it from that of tablea.columna:

Used with the GenerativeSelect.set_label_style() method, LABEL_STYLE_DISAMBIGUATE_ONLY is the default labeling style for all SELECT statements outside of 1.x style ORM queries.

Added in version 1.4.

Label style indicating no automatic labeling should be applied to the columns clause of a SELECT statement.

Below, the columns named columna are both rendered as is, meaning that the name columna can only refer to the first occurrence of this name within a result set, as well as if the statement were used as a subquery:

Used with the Select.set_label_style() method.

Added in version 1.4.

Label style indicating all columns should be labeled as <tablename>_<columnname> when generating the columns clause of a SELECT statement, to disambiguate same-named columns referenced from different tables, aliases, or subqueries.

Below, all column names are given a label so that the two same-named columns columna are disambiguated as table1_columna and table2_columna:

Used with the GenerativeSelect.set_label_style() method. Equivalent to the legacy method Select.apply_labels(); LABEL_STYLE_TABLENAME_PLUS_COL is SQLAlchemy’s legacy auto-labeling style. LABEL_STYLE_DISAMBIGUATE_ONLY provides a less intrusive approach to disambiguation of same-named column expressions.

Added in version 1.4.

Select.set_label_style()

Select.get_label_style()

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (csharp):
```csharp
exists_criteria = exists().where(table1.c.col1 == table2.c.col2)
```

Example 2 (csharp):
```csharp
exists_criteria = (
    select(table2.c.col2).where(table1.c.col1 == table2.c.col2).exists()
)
```

Example 3 (csharp):
```csharp
stmt = select(table1.c.col1).where(exists_criteria)
```

Example 4 (sql):
```sql
SELECT col1 FROM table1 WHERE EXISTS
(SELECT table2.col2 FROM table2 WHERE table2.col2 = table1.col1)
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Writing SELECT statements for ORM Mapped Classes¶
- Selecting ORM Entities and Attributes¶
  - Selecting ORM Entities¶
  - Selecting Multiple ORM Entities Simultaneously¶
  - Selecting Individual Attributes¶
  - Grouping Selected Attributes with Bundles¶

Home | Download this Documentation

Home | Download this Documentation

This page is part of the ORM Querying Guide.

Previous: ORM Querying Guide | Next: Writing SELECT statements for Inheritance Mappings

This section makes use of ORM mappings first illustrated in the SQLAlchemy Unified Tutorial, shown in the section Declaring Mapped Classes.

View the ORM setup for this page.

SELECT statements are produced by the select() function which returns a Select object. The entities and/or SQL expressions to return (i.e. the “columns” clause) are passed positionally to the function. From there, additional methods are used to generate the complete statement, such as the Select.where() method illustrated below:

Given a completed Select object, in order to execute it within the ORM to get rows back, the object is passed to Session.execute(), where a Result object is then returned:

The select() construct accepts ORM entities, including mapped classes as well as class-level attributes representing mapped columns, which are converted into ORM-annotated FromClause and ColumnElement elements at construction time.

A Select object that contains ORM-annotated entities is normally executed using a Session object, and not a Connection object, so that ORM-related features may take effect, including that instances of ORM-mapped objects may be returned. When using the Connection directly, result rows will only contain column-level data.

Below we select from the User entity, producing a Select that selects from the mapped Table to which User is mapped:

When selecting from ORM entities, the entity itself is returned in the result as a row with a single element, as opposed to a series of individual columns; for example above, the Result returns Row objects that have just a single element per row, that element holding onto a User object:

When selecting a list of single-element rows containing ORM entities, it is typical to skip the generation of Row objects and instead receive ORM entities directly. This is most easily achieved by using the Session.scalars() method to execute, rather than the Session.execute() method, so that a ScalarResult object which yields single elements rather than rows is returned:

Calling the Session.scalars() method is the equivalent to calling upon Session.execute() to receive a Result object, then calling upon Result.scalars() to receive a ScalarResult object.

The select() function accepts any number of ORM classes and/or column expressions at once, including that multiple ORM classes may be requested. When SELECTing from multiple ORM classes, they are named in each result row based on their class name. In the example below, the result rows for a SELECT against User and Address will refer to them under the names User and Address:

If we wanted to assign different names to these entities in the rows, we would use the aliased() construct using the aliased.name parameter to alias them with an explicit name:

The aliased form above is discussed further at Using Relationship to join between aliased targets.

An existing Select construct may also have ORM classes and/or column expressions added to its columns clause using the Select.add_columns() method. We can produce the same statement as above using this form as well:

The attributes on a mapped class, such as User.name and Address.email_address, can be used just like Column or other SQL expression objects when passed to select(). Creating a select() that is against specific columns will return Row objects, and not entities like User or Address objects. Each Row will have each column represented individually:

The above statement returns Row objects with name and email_address columns, as illustrated in the runtime demonstration below:

The Bundle construct is an extensible ORM-only construct that allows sets of column expressions to be grouped in result rows:

The Bundle is potentially useful for creating lightweight views and custom column groupings. Bundle may also be subclassed in order to return alternate data structures; see Bundle.create_row_processor() for an example.

Bundle.create_row_processor()

As discussed in the tutorial at Using Aliases, to create a SQL alias of an ORM entity is achieved using the aliased() construct against a mapped class:

As is the case when using Table.alias(), the SQL alias is anonymously named. For the case of selecting the entity from a row with an explicit name, the aliased.name parameter may be passed as well:

The aliased construct is central for several use cases, including:

making use of subqueries with the ORM; the sections Selecting Entities from Subqueries and Joining to Subqueries discuss this further.

Controlling the name of an entity in a result set; see Selecting Multiple ORM Entities Simultaneously for an example

Joining to the same ORM entity multiple times; see Using Relationship to join between aliased targets for an example.

The ORM supports loading of entities from SELECT statements that come from other sources. The typical use case is that of a textual SELECT statement, which in SQLAlchemy is represented using the text() construct. A text() construct can be augmented with information about the ORM-mapped columns that the statement would load; this can then be associated with the ORM entity itself so that ORM objects can be loaded based on this statement.

Given a textual SQL statement we’d like to load from:

We can add column information to the statement by using the TextClause.columns() method; when this method is invoked, the TextClause object is converted into a TextualSelect object, which takes on a role that is comparable to the Select construct. The TextClause.columns() method is typically passed Column objects or equivalent, and in this case we can make use of the ORM-mapped attributes on the User class directly:

We now have an ORM-configured SQL construct that as given, can load the “id”, “name” and “fullname” columns separately. To use this SELECT statement as a source of complete User entities instead, we can link these columns to a regular ORM-enabled Select construct using the Select.from_statement() method:

The same TextualSelect object can also be converted into a subquery using the TextualSelect.subquery() method, and linked to the User entity to it using the aliased() construct, in a similar manner as discussed below in Selecting Entities from Subqueries:

The difference between using the TextualSelect directly with Select.from_statement() versus making use of aliased() is that in the former case, no subquery is produced in the resulting SQL. This can in some scenarios be advantageous from a performance or complexity perspective.

The aliased() construct discussed in the previous section can be used with any Subquery construct that comes from a method such as Select.subquery() to link ORM entities to the columns returned by that subquery; by default, there must be a column correspondence relationship between the columns delivered by the subquery and the columns to which the entity is mapped, meaning, the subquery needs to be ultimately derived from those entities, such as in the example below:

Alternatively, an aliased subquery can be matched to the entity based on name by applying the aliased.adapt_on_names parameter:

ORM Entity Subqueries/CTEs - in the SQLAlchemy Unified Tutorial

Joining to Subqueries

The union() and union_all() functions are the most common set operations, which along with other set operations such as except_(), intersect() and others deliver an object known as a CompoundSelect, which is composed of multiple Select constructs joined by a set-operation keyword. ORM entities may be selected from simple compound selects using the Select.from_statement() method illustrated previously at Getting ORM Results from Textual Statements. In this method, the UNION statement is the complete statement that will be rendered, no additional criteria can be added after Select.from_statement() is used:

A CompoundSelect construct can be more flexibly used within a query that can be further modified by organizing it into a subquery and linking it to an ORM entity using aliased(), as illustrated previously at Selecting Entities from Subqueries. In the example below, we first use CompoundSelect.subquery() to create a subquery of the UNION ALL statement, we then package that into the aliased() construct where it can be used like any other mapped entity in a select() construct, including that we can add filtering and order by criteria based on its exported columns:

Selecting ORM Entities from Unions - in the SQLAlchemy Unified Tutorial

The Select.join() and Select.join_from() methods are used to construct SQL JOINs against a SELECT statement.

This section will detail ORM use cases for these methods. For a general overview of their use from a Core perspective, see Explicit FROM clauses and JOINs in the SQLAlchemy Unified Tutorial.

The usage of Select.join() in an ORM context for 2.0 style queries is mostly equivalent, minus legacy use cases, to the usage of the Query.join() method in 1.x style queries.

Consider a mapping between two classes User and Address, with a relationship User.addresses representing a collection of Address objects associated with each User. The most common usage of Select.join() is to create a JOIN along this relationship, using the User.addresses attribute as an indicator for how this should occur:

Where above, the call to Select.join() along User.addresses will result in SQL approximately equivalent to:

In the above example we refer to User.addresses as passed to Select.join() as the “on clause”, that is, it indicates how the “ON” portion of the JOIN should be constructed.

Note that using Select.join() to JOIN from one entity to another affects the FROM clause of the SELECT statement, but not the columns clause; the SELECT statement in this example will continue to return rows from only the User entity. To SELECT columns / entities from both User and Address at the same time, the Address entity must also be named in the select() function, or added to the Select construct afterwards using the Select.add_columns() method. See the section Selecting Multiple ORM Entities Simultaneously for examples of both of these forms.

To construct a chain of joins, multiple Select.join() calls may be used. The relationship-bound attribute implies both the left and right side of the join at once. Consider additional entities Order and Item, where the User.orders relationship refers to the Order entity, and the Order.items relationship refers to the Item entity, via an association table order_items. Two Select.join() calls will result in a JOIN first from User to Order, and a second from Order to Item. However, since Order.items is a many to many relationship, it results in two separate JOIN elements, for a total of three JOIN elements in the resulting SQL:

The order in which each call to the Select.join() method is significant only to the degree that the “left” side of what we would like to join from needs to be present in the list of FROMs before we indicate a new target. Select.join() would not, for example, know how to join correctly if we were to specify select(User).join(Order.items).join(User.orders), and would raise an error. In correct practice, the Select.join() method is invoked in such a way that lines up with how we would want the JOIN clauses in SQL to be rendered, and each call should represent a clear link from what precedes it.

All of the elements that we target in the FROM clause remain available as potential points to continue joining FROM. We can continue to add other elements to join FROM the User entity above, for example adding on the User.addresses relationship to our chain of joins:

A second form of Select.join() allows any mapped entity or core selectable construct as a target. In this usage, Select.join() will attempt to infer the ON clause for the JOIN, using the natural foreign key relationship between two entities:

In the above calling form, Select.join() is called upon to infer the “on clause” automatically. This calling form will ultimately raise an error if either there are no ForeignKeyConstraint setup between the two mapped Table constructs, or if there are multiple ForeignKeyConstraint linkages between them such that the appropriate constraint to use is ambiguous.

When making use of Select.join() or Select.join_from() without indicating an ON clause, ORM configured relationship() constructs are not taken into account. Only the configured ForeignKeyConstraint relationships between the entities at the level of the mapped Table objects are consulted when an attempt is made to infer an ON clause for the JOIN.

The third calling form allows both the target entity as well as the ON clause to be passed explicitly. A example that includes a SQL expression as the ON clause is as follows:

The expression-based ON clause may also be a relationship()-bound attribute, in the same way it’s used in Simple Relationship Joins:

The above example seems redundant in that it indicates the target of Address in two different ways; however, the utility of this form becomes apparent when joining to aliased entities; see the section Using Relationship to join between aliased targets for an example.

The ON clause generated by the relationship() construct may be augmented with additional criteria. This is useful both for quick ways to limit the scope of a particular join over a relationship path, as well as for cases like configuring loader strategies such as joinedload() and selectinload(). The PropComparator.and_() method accepts a series of SQL expressions positionally that will be joined to the ON clause of the JOIN via AND. For example if we wanted to JOIN from User to Address but also limit the ON criteria to only certain email addresses:

The PropComparator.and_() method also works with loader strategies such as joinedload() and selectinload(). See the section Adding Criteria to loader options.

When constructing joins using relationship()-bound attributes to indicate the ON clause, the two-argument syntax illustrated in Joins to a Target with an ON Clause can be expanded to work with the aliased() construct, to indicate a SQL alias as the target of a join while still making use of the relationship()-bound attribute to indicate the ON clause, as in the example below, where the User entity is joined twice to two different aliased() constructs against the Address entity:

The same pattern may be expressed more succinctly using the modifier PropComparator.of_type(), which may be applied to the relationship()-bound attribute, passing along the target entity in order to indicate the target in one step. The example below uses PropComparator.of_type() to produce the same SQL statement as the one just illustrated:

To make use of a relationship() to construct a join from an aliased entity, the attribute is available from the aliased() construct directly:

The target of a join may be any “selectable” entity which includes subqueries. When using the ORM, it is typical that these targets are stated in terms of an aliased() construct, but this is not strictly required, particularly if the joined entity is not being returned in the results. For example, to join from the User entity to the Address entity, where the Address entity is represented as a row limited subquery, we first construct a Subquery object using Select.subquery(), which may then be used as the target of the Select.join() method:

The above SELECT statement when invoked via Session.execute() will return rows that contain User entities, but not Address entities. In order to include Address entities to the set of entities that would be returned in result sets, we construct an aliased() object against the Address entity and Subquery object. We also may wish to apply a name to the aliased() construct, such as "address" used below, so that we can refer to it by name in the result row:

The subquery form illustrated in the previous section may be expressed with more specificity using a relationship()-bound attribute using one of the forms indicated at Using Relationship to join between aliased targets. For example, to create the same join while ensuring the join is along that of a particular relationship(), we may use the PropComparator.of_type() method, passing the aliased() construct containing the Subquery object that’s the target of the join:

A subquery that contains columns spanning more than one ORM entity may be applied to more than one aliased() construct at once, and used in the same Select construct in terms of each entity separately. The rendered SQL will continue to treat all such aliased() constructs as the same subquery, however from the ORM / Python perspective the different return values and object attributes can be referenced by using the appropriate aliased() construct.

Given for example a subquery that refers to both User and Address:

We can create aliased() constructs against both User and Address that each refer to the same object:

A Select construct selecting from both entities will render the subquery once, but in a result-row context can return objects of both User and Address classes at the same time:

In cases where the left side of the current state of Select is not in line with what we want to join from, the Select.join_from() method may be used:

The Select.join_from() method accepts two or three arguments, either in the form (<join from>, <onclause>), or (<join from>, <join to>, [<onclause>]):

To set up the initial FROM clause for a SELECT such that Select.join() can be used subsequent, the Select.select_from() method may also be used:

The Select.select_from() method does not actually have the final say on the order of tables in the FROM clause. If the statement also refers to a Join construct that refers to existing tables in a different order, the Join construct takes precedence. When we use methods like Select.join() and Select.join_from(), these methods are ultimately creating such a Join object. Therefore we can see the contents of Select.select_from() being overridden in a case like this:

Where above, we see that the FROM clause is address JOIN user_account, even though we stated select_from(User) first. Because of the .join(Address.user) method call, the statement is ultimately equivalent to the following:

The Join construct above is added as another entry in the Select.select_from() list which supersedes the previous entry.

Besides the use of relationship() constructs within the Select.join() and Select.join_from() methods, relationship() also plays a role in helping to construct SQL expressions that are typically for use in the WHERE clause, using the Select.where() method.

The Exists construct was first introduced in the SQLAlchemy Unified Tutorial in the section EXISTS subqueries. This object is used to render the SQL EXISTS keyword in conjunction with a scalar subquery. The relationship() construct provides for some helper methods that may be used to generate some common EXISTS styles of queries in terms of the relationship.

For a one-to-many relationship such as User.addresses, an EXISTS against the address table that correlates back to the user_account table can be produced using PropComparator.any(). This method accepts an optional WHERE criteria to limit the rows matched by the subquery:

As EXISTS tends to be more efficient for negative lookups, a common query is to locate entities where there are no related entities present. This is succinct using a phrase such as ~User.addresses.any(), to select for User entities that have no related Address rows:

The PropComparator.has() method works in mostly the same way as PropComparator.any(), except that it’s used for many-to-one relationships, such as if we wanted to locate all Address objects which belonged to “sandy”:

The relationship()-bound attribute also offers a few SQL construction implementations that are geared towards filtering a relationship()-bound attribute in terms of a specific instance of a related object, which can unpack the appropriate attribute values from a given persistent (or less commonly a detached) object instance and construct WHERE criteria in terms of the target relationship().

many to one equals comparison - a specific object instance can be compared to many-to-one relationship, to select rows where the foreign key of the target entity matches the primary key value of the object given:

many to one not equals comparison - the not equals operator may also be used:

object is contained in a one-to-many collection - this is essentially the one-to-many version of the “equals” comparison, select rows where the primary key equals the value of the foreign key in a related object:

An object has a particular parent from a one-to-many perspective - the with_parent() function produces a comparison that returns rows which are referenced by a given parent, this is essentially the same as using the == operator with the many-to-one side:

Next Query Guide Section: Writing SELECT statements for Inheritance Mappings

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (sql):
```sql
>>> from sqlalchemy import select
>>> stmt = select(User).where(User.name == "spongebob")
```

Example 2 (sql):
```sql
>>> result = session.execute(stmt)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[...] ('spongebob',)
>>> for user_obj in result.scalars():
...     print(f"{user_obj.name} {user_obj.fullname}")
spongebob Spongebob Squarepants
```

Example 3 (sql):
```sql
>>> result = session.execute(select(User).order_by(User.id))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account ORDER BY user_account.id
[...] ()
```

Example 4 (json):
```json
>>> result.all()
[(User(id=1, name='spongebob', fullname='Spongebob Squarepants'),),
 (User(id=2, name='sandy', fullname='Sandy Cheeks'),),
 (User(id=3, name='patrick', fullname='Patrick Star'),),
 (User(id=4, name='squidward', fullname='Squidward Tentacles'),),
 (User(id=5, name='ehkrabs', fullname='Eugene H. Krabs'),)]
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Column Loading Options¶
- Limiting which Columns Load with Column Deferral¶
  - Using load_only() to reduce loaded columns¶
    - Using load_only() with multiple entities¶
    - Using load_only() on related objects and collections¶
  - Using defer() to omit specific columns¶

Home | Download this Documentation

Home | Download this Documentation

This page is part of the ORM Querying Guide.

Previous: ORM-Enabled INSERT, UPDATE, and DELETE statements | Next: Relationship Loading Techniques

This section presents additional options regarding the loading of columns. The mappings used include columns that would store large string values for which we may want to limit when they are loaded.

View the ORM setup for this page. Some of the examples below will redefine the Book mapper to modify some of the column definitions.

Column deferral refers to ORM mapped columns that are omitted from a SELECT statement when objects of that type are queried. The general rationale here is performance, in cases where tables have seldom-used columns with potentially large data values, as fully loading these columns on every query may be time and/or memory intensive. SQLAlchemy ORM offers a variety of ways to control the loading of columns when entities are loaded.

Most examples in this section are illustrating ORM loader options. These are small constructs that are passed to the Select.options() method of the Select object, which are then consumed by the ORM when the object is compiled into a SQL string.

The load_only() loader option is the most expedient option to use when loading objects where it is known that only a small handful of columns will be accessed. This option accepts a variable number of class-bound attribute objects indicating those column-mapped attributes that should be loaded, where all other column-mapped attributes outside of the primary key will not be part of the columns fetched . In the example below, the Book class contains columns .title, .summary and .cover_photo. Using load_only() we can instruct the ORM to only load the .title and .summary columns up front:

Above, the SELECT statement has omitted the .cover_photo column and included only .title and .summary, as well as the primary key column .id; the ORM will typically always fetch the primary key columns as these are required to establish the identity for the row.

Once loaded, the object will normally have lazy loading behavior applied to the remaining unloaded attributes, meaning that when any are first accessed, a SQL statement will be emitted within the current transaction in order to load the value. Below, accessing .cover_photo emits a SELECT statement to load its value:

Lazy loads are always emitted using the Session to which the object is in the persistent state. If the object is detached from any Session, the operation fails, raising an exception.

As an alternative to lazy loading on access, deferred columns may also be configured to raise an informative exception when accessed, regardless of their attachment state. When using the load_only() construct, this may be indicated using the load_only.raiseload parameter. See the section Using raiseload to prevent deferred column loads for background and examples.

as noted elsewhere, lazy loading is not available when using Asynchronous I/O (asyncio).

load_only() limits itself to the single entity that is referred towards in its list of attributes (passing a list of attributes that span more than a single entity is currently disallowed). In the example below, the given load_only() option applies only to the Book entity. The User entity that’s also selected is not affected; within the resulting SELECT statement, all columns for user_account are present, whereas only book.id and book.title are present for the book table:

If we wanted to apply load_only() options to both User and Book, we would make use of two separate options:

When using relationship loaders to control the loading of related objects, the Load.load_only() method of any relationship loader may be used to apply load_only() rules to columns on the sub-entity. In the example below, selectinload() is used to load the related books collection on each User object. By applying Load.load_only() to the resulting option object, when objects are loaded for the relationship, the SELECT emitted will only refer to the title column in addition to primary key column:

load_only() may also be applied to sub-entities without needing to state the style of loading to use for the relationship itself. If we didn’t want to change the default loading style of User.books but still apply load only rules to Book, we would link using the defaultload() option, which in this case will retain the default relationship loading style of "lazy", and applying our custom load_only() rule to the SELECT statement emitted for each User.books collection:

The defer() loader option is a more fine grained alternative to load_only(), which allows a single specific column to be marked as “dont load”. In the example below, defer() is applied directly to the .cover_photo column, leaving the behavior of all other columns unchanged:

As is the case with load_only(), unloaded columns by default will load themselves when accessed using lazy loading:

Multiple defer() options may be used in one statement in order to mark several columns as deferred.

As is the case with load_only(), the defer() option also includes the ability to have a deferred attribute raise an exception on access rather than lazy loading. This is illustrated in the section Using raiseload to prevent deferred column loads.

When using the load_only() or defer() loader options, attributes marked as deferred on an object have the default behavior that when first accessed, a SELECT statement will be emitted within the current transaction in order to load their value. It is often necessary to prevent this load from occurring, and instead raise an exception when the attribute is accessed, indicating that the need to query the database for this column was not expected. A typical scenario is an operation where objects are loaded with all the columns that are known to be required for the operation to proceed, which are then passed onto a view layer. Any further SQL operations that emit within the view layer should be caught, so that the up-front loading operation can be adjusted to accommodate for that additional data up front, rather than incurring additional lazy loading.

For this use case the defer() and load_only() options include a boolean parameter defer.raiseload, which when set to True will cause the affected attributes to raise on access. In the example below, the deferred column .cover_photo will disallow attribute access:

When using load_only() to name a specific set of non-deferred columns, raiseload behavior may be applied to the remaining columns using the load_only.raiseload parameter, which will be applied to all deferred attributes:

It is not yet possible to mix load_only() and defer() options which refer to the same entity together in one statement in order to change the raiseload behavior of certain attributes; currently, doing so will produce undefined loading behavior of attributes.

The defer.raiseload feature is the column-level version of the same “raiseload” feature that’s available for relationships. For “raiseload” with relationships, see Preventing unwanted lazy loads using raiseload in the Relationship Loading Techniques section of this guide.

The functionality of defer() is available as a default behavior for mapped columns, as may be appropriate for columns that should not be loaded unconditionally on every query. To configure, use the mapped_column.deferred parameter of mapped_column(). The example below illustrates a mapping for Book which applies default column deferral to the summary and cover_photo columns:

Using the above mapping, queries against Book will automatically not include the summary and cover_photo columns:

As is the case with all deferral, the default behavior when deferred attributes on the loaded object are first accessed is that they will lazy load their value:

As is the case with the defer() and load_only() loader options, mapper level deferral also includes an option for raiseload behavior to occur, rather than lazy loading, when no other options are present in a statement. This allows a mapping where certain columns will not load by default and will also never load lazily without explicit directives used in a statement. See the section Configuring mapper-level “raiseload” behavior for background on how to configure and use this behavior.

The deferred() function is the earlier, more general purpose “deferred column” mapping directive that precedes the introduction of the mapped_column() construct in SQLAlchemy.

deferred() is used when configuring ORM mappers, and accepts arbitrary SQL expressions or Column objects. As such it’s suitable to be used with non-declarative imperative mappings, passing it to the map_imperatively.properties dictionary:

deferred() may also be used in place of column_property() when mapped SQL expressions should be loaded on a deferred basis:

Using column_property - in the section SQL Expressions as Mapped Attributes

Applying Load, Persistence and Mapping Options for Imperative Table Columns - in the section Table Configuration with Declarative

With columns configured on mappings to defer by default, the undefer() option will cause any column that is normally deferred to be undeferred, that is, to load up front with all the other columns of the mapping. For example we may apply undefer() to the Book.summary column, which is indicated in the previous mapping as deferred:

The Book.summary column was now eagerly loaded, and may be accessed without additional SQL being emitted:

Normally when a column is mapped with mapped_column(deferred=True), when the deferred attribute is accessed on an object, SQL will be emitted to load only that specific column and no others, even if the mapping has other columns that are also marked as deferred. In the common case that the deferred attribute is part of a group of attributes that should all load at once, rather than emitting SQL for each attribute individually, the mapped_column.deferred_group parameter may be used, which accepts an arbitrary string which will define a common group of columns to be undeferred:

Using the above mapping, accessing either summary or cover_photo will load both columns at once using just one SELECT statement:

If deferred columns are configured with mapped_column.deferred_group as introduced in the preceding section, the entire group may be indicated to load eagerly using the undefer_group() option, passing the string name of the group to be eagerly loaded:

Both summary and cover_photo are available without additional loads:

Most ORM loader options accept a wildcard expression, indicated by "*", which indicates that the option should be applied to all relevant attributes. If a mapping has a series of deferred columns, all such columns can be undeferred at once, without using a group name, by indicating a wildcard:

The “raiseload” behavior first introduced at Using raiseload to prevent deferred column loads may also be applied as a default mapper-level behavior, using the mapped_column.deferred_raiseload parameter of mapped_column(). When using this parameter, the affected columns will raise on access in all cases unless explicitly “undeferred” using undefer() or load_only() at query time:

Using the above mapping, the .summary and .cover_photo columns are by default not loadable:

Only by overriding their behavior at query time, typically using undefer() or undefer_group(), or less commonly defer(), may the attributes be loaded. The example below applies undefer('*') to undefer all attributes, also making use of Populate Existing to refresh the already-loaded object’s loader options:

As discussed Selecting ORM Entities and Attributes and elsewhere, the select() construct may be used to load arbitrary SQL expressions in a result set. Such as if we wanted to issue a query that loads User objects, but also includes a count of how many books each User owned, we could use func.count(Book.id) to add a “count” column to a query which includes a JOIN to Book as well as a GROUP BY owner id. This will yield Row objects that each contain two entries, one for User and one for func.count(Book.id):

In the above example, the User entity and the “book count” SQL expression are returned separately. However, a popular use case is to produce a query that will yield User objects alone, which can be iterated for example using Session.scalars(), where the result of the func.count(Book.id) SQL expression is applied dynamically to each User entity. The end result would be similar to the case where an arbitrary SQL expression were mapped to the class using column_property(), except that the SQL expression can be modified at query time. For this use case SQLAlchemy provides the with_expression() loader option, which when combined with the mapper level query_expression() directive may produce this result.

To apply with_expression() to a query, the mapped class must have pre-configured an ORM mapped attribute using the query_expression() directive; this directive will produce an attribute on the mapped class that is suitable for receiving query-time SQL expressions. Below we add a new attribute User.book_count to User. This ORM mapped attribute is read-only and has no default value; accessing it on a loaded instance will normally produce None:

With the User.book_count attribute configured in our mapping, we may populate it with data from a SQL expression using the with_expression() loader option to apply a custom SQL expression to each User object as it’s loaded:

Above, we moved our func.count(Book.id) expression out of the columns argument of the select() construct and into the with_expression() loader option. The ORM then considers this to be a special column load option that’s applied dynamically to the statement.

The query_expression() mapping has these caveats:

On an object where with_expression() were not used to populate the attribute, the attribute on an object instance will have the value None, unless on the mapping the query_expression.default_expr parameter is set to a default SQL expression.

The with_expression() value does not populate on an object that is already loaded, unless Populate Existing is used. The example below will not work, as the A object is already loaded:

To ensure the attribute is re-loaded on an existing object, use the Populate Existing execution option to ensure all columns are re-populated:

The with_expression() SQL expression is lost when the object is expired. Once the object is expired, either via Session.expire() or via the expire_on_commit behavior of Session.commit(), the SQL expression and its value is no longer associated with the attribute and will return None on subsequent access.

with_expression(), as an object loading option, only takes effect on the outermost part of a query and only for a query against a full entity, and not for arbitrary column selects, within subqueries, or the elements of a compound statement such as a UNION. See the next section Using with_expression() with UNIONs, other subqueries for an example.

The mapped attribute cannot be applied to other parts of the query, such as the WHERE clause, the ORDER BY clause, and make use of the ad-hoc expression; that is, this won’t work:

The A.expr expression will resolve to NULL in the above WHERE clause and ORDER BY clause. To use the expression throughout the query, assign to a variable and use that:

The with_expression() option is a special option used to apply SQL expressions to mapped classes dynamically at query time. For ordinary fixed SQL expressions configured on mappers, see the section SQL Expressions as Mapped Attributes.

The with_expression() construct is an ORM loader option, and as such may only be applied to the outermost level of a SELECT statement which is to load a particular ORM entity. It does not have any effect if used inside of a select() that will then be used as a subquery or as an element within a compound statement such as a UNION.

In order to use arbitrary SQL expressions in subqueries, normal Core-style means of adding expressions should be used. To assemble a subquery-derived expression onto the ORM entity’s query_expression() attributes, with_expression() is used at the top layer of ORM object loading, referencing the SQL expression within the subquery.

In the example below, two select() constructs are used against the ORM entity A with an additional SQL expression labeled in expr, and combined using union_all(). Then, at the topmost layer, the A entity is SELECTed from this UNION, using the querying technique described at Selecting Entities from UNIONs and other set operations, adding an option with with_expression() to extract this SQL expression onto newly loaded instances of A:

defer(key, *addl_attrs, [raiseload])

Indicate that the given column-oriented attribute should be deferred, e.g. not loaded until accessed.

deferred(column, *additional_columns, [group, raiseload, comparator_factory, init, repr, default, default_factory, compare, kw_only, hash, active_history, expire_on_flush, info, doc, dataclass_metadata])

Indicate a column-based mapped attribute that by default will not load unless accessed.

load_only(*attrs, [raiseload])

Indicate that for a particular entity, only the given list of column-based attribute names should be loaded; all others will be deferred.

query_expression([default_expr], *, [repr, compare, expire_on_flush, info, doc])

Indicate an attribute that populates from a query-time SQL expression.

undefer(key, *addl_attrs)

Indicate that the given column-oriented attribute should be undeferred, e.g. specified within the SELECT statement of the entity as a whole.

Indicate that columns within the given deferred group name should be undeferred.

with_expression(key, expression)

Apply an ad-hoc SQL expression to a “deferred expression” attribute.

Indicate that the given column-oriented attribute should be deferred, e.g. not loaded until accessed.

This function is part of the Load interface and supports both method-chained and standalone operation.

To specify a deferred load of an attribute on a related class, the path can be specified one token at a time, specifying the loading style for each link along the chain. To leave the loading style for a link unchanged, use defaultload():

Multiple deferral options related to a relationship can be bundled at once using Load.options():

key¶ – Attribute to be deferred.

raiseload¶ – raise InvalidRequestError rather than lazy loading a value when the deferred attribute is accessed. Used to prevent unwanted SQL from being emitted.

Added in version 1.4.

Limiting which Columns Load with Column Deferral - in the ORM Querying Guide

Indicate a column-based mapped attribute that by default will not load unless accessed.

When using mapped_column(), the same functionality as that of deferred() construct is provided by using the mapped_column.deferred parameter.

*columns¶ – columns to be mapped. This is typically a single Column object, however a collection is supported in order to support multiple columns mapped under the same attribute.

boolean, if True, indicates an exception should be raised if the load operation is to take place.

Added in version 1.4.

Additional arguments are the same as that of column_property().

Using deferred() for imperative mappers, mapped SQL expressions

Indicate an attribute that populates from a query-time SQL expression.

default_expr¶ – Optional SQL expression object that will be used in all cases if not assigned later with with_expression().

Added in version 1.2.

Loading Arbitrary SQL Expressions onto Objects - background and usage examples

Indicate that for a particular entity, only the given list of column-based attribute names should be loaded; all others will be deferred.

This function is part of the Load interface and supports both method-chained and standalone operation.

Example - given a class User, load only the name and fullname attributes:

Example - given a relationship User.addresses -> Address, specify subquery loading for the User.addresses collection, but on each Address object load only the email_address attribute:

For a statement that has multiple entities, the lead entity can be specifically referred to using the Load constructor:

When used together with the populate_existing execution option only the attributes listed will be refreshed.

*attrs¶ – Attributes to be loaded, all others will be deferred.

raise InvalidRequestError rather than lazy loading a value when a deferred attribute is accessed. Used to prevent unwanted SQL from being emitted.

Added in version 2.0.

Limiting which Columns Load with Column Deferral - in the ORM Querying Guide

*attrs¶ – Attributes to be loaded, all others will be deferred.

raise InvalidRequestError rather than lazy loading a value when a deferred attribute is accessed. Used to prevent unwanted SQL from being emitted.

Added in version 2.0.

Indicate that the given column-oriented attribute should be undeferred, e.g. specified within the SELECT statement of the entity as a whole.

The column being undeferred is typically set up on the mapping as a deferred() attribute.

This function is part of the Load interface and supports both method-chained and standalone operation.

key¶ – Attribute to be undeferred.

Limiting which Columns Load with Column Deferral - in the ORM Querying Guide

Indicate that columns within the given deferred group name should be undeferred.

The columns being undeferred are set up on the mapping as deferred() attributes and include a “group” name.

To undefer a group of attributes on a related entity, the path can be spelled out using relationship loader options, such as defaultload():

Limiting which Columns Load with Column Deferral - in the ORM Querying Guide

Apply an ad-hoc SQL expression to a “deferred expression” attribute.

This option is used in conjunction with the query_expression() mapper-level construct that indicates an attribute which should be the target of an ad-hoc SQL expression.

Added in version 1.2.

key¶ – Attribute to be populated

expr¶ – SQL expression to be applied to the attribute.

Loading Arbitrary SQL Expressions onto Objects - background and usage examples

Next Query Guide Section: Relationship Loading Techniques

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (sql):
```sql
>>> from sqlalchemy import select
>>> from sqlalchemy.orm import load_only
>>> stmt = select(Book).options(load_only(Book.title, Book.summary))
>>> books = session.scalars(stmt).all()
SELECT book.id, book.title, book.summary
FROM book
[...] ()
>>> for book in books:
...     print(f"{book.title}  {book.summary}")
100 Years of Krabby Patties  some long summary
Sea Catch 22  another long summary
The Sea Grapes of Wrath  yet another summary
A Nut Like No Other  some long summary
Geodesic Domes: A Retrospective  another long summary
Rocketry for Squirrels  yet another summary
```

Example 2 (sql):
```sql
>>> img_data = books[0].cover_photo
SELECT book.cover_photo AS book_cover_photo
FROM book
WHERE book.id = ?
[...] (1,)
```

Example 3 (sql):
```sql
>>> stmt = select(User, Book).join_from(User, Book).options(load_only(Book.title))
>>> print(stmt)
SELECT user_account.id, user_account.name, user_account.fullname,
book.id AS id_1, book.title
FROM user_account JOIN book ON user_account.id = book.owner_id
```

Example 4 (sql):
```sql
>>> stmt = (
...     select(User, Book)
...     .join_from(User, Book)
...     .options(load_only(User.name), load_only(Book.title))
... )
>>> print(stmt)
SELECT user_account.id, user_account.name, book.id AS id_1, book.title
FROM user_account JOIN book ON user_account.id = book.owner_id
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- ORM-Enabled INSERT, UPDATE, and DELETE statements¶
- ORM Bulk INSERT Statements¶
  - Getting new objects with RETURNING¶
    - Correlating RETURNING records with input data order¶
  - Using Heterogeneous Parameter Dictionaries¶
  - Sending NULL values in ORM bulk INSERT statements¶

Home | Download this Documentation

Home | Download this Documentation

This page is part of the ORM Querying Guide.

Previous: Writing SELECT statements for Inheritance Mappings | Next: Column Loading Options

This section makes use of ORM mappings first illustrated in the SQLAlchemy Unified Tutorial, shown in the section Declaring Mapped Classes, as well as inheritance mappings shown in the section Mapping Class Inheritance Hierarchies.

View the ORM setup for this page.

The Session.execute() method, in addition to handling ORM-enabled Select objects, can also accommodate ORM-enabled Insert, Update and Delete objects, in various ways which are each used to INSERT, UPDATE, or DELETE many database rows at once. There is also dialect-specific support for ORM-enabled “upserts”, which are INSERT statements that automatically make use of UPDATE for rows that already exist.

The following table summarizes the calling forms that are discussed in this document:

Data is passed using …

Supports Multi-Table Mappings?

ORM Bulk INSERT Statements

List of dictionaries to Session.execute.params

ORM Bulk Insert with SQL Expressions

Session.execute.params with Insert.values()

ORM Bulk Insert with Per Row SQL Expressions

List of dictionaries to Insert.values()

ORM “upsert” Statements

List of dictionaries to Insert.values()

ORM Bulk UPDATE by Primary Key

List of dictionaries to Session.execute.params

ORM UPDATE and DELETE with Custom WHERE Criteria

keywords to Update.values()

partial, with manual steps

A insert() construct can be constructed in terms of an ORM class and passed to the Session.execute() method. A list of parameter dictionaries sent to the Session.execute.params parameter, separate from the Insert object itself, will invoke bulk INSERT mode for the statement, which essentially means the operation will optimize as much as possible for many rows:

The parameter dictionaries contain key/value pairs which may correspond to ORM mapped attributes that line up with mapped Column or mapped_column() declarations, as well as with composite declarations. The keys should match the ORM mapped attribute name and not the actual database column name, if these two names happen to be different.

ORM bulk INSERT allows each dictionary to have different keys. The operation will emit multiple INSERT statements with different VALUES clauses for each set of keys. This is distinctly different from a Core Insert operation, which as introduced at INSERT usually generates the “values” clause automatically only uses the first dictionary in the list to determine a single VALUES clause for all parameter sets.

Changed in version 2.0: Passing an Insert construct to the Session.execute() method now invokes a “bulk insert”, which makes use of the same functionality as the legacy Session.bulk_insert_mappings() method. This is a behavior change compared to the 1.x series where the Insert would be interpreted in a Core-centric way, using column names for value keys; ORM attribute keys are now accepted. Core-style functionality is available by passing the execution option {"dml_strategy": "raw"} to the Session.execution_options parameter of Session.execute().

The bulk ORM insert feature supports INSERT..RETURNING for selected backends, which can return a Result object that may yield individual columns back as well as fully constructed ORM objects corresponding to the newly generated records. INSERT..RETURNING requires the use of a backend that supports SQL RETURNING syntax as well as support for executemany with RETURNING; this feature is available with all SQLAlchemy-included backends with the exception of MySQL (MariaDB is included).

As an example, we can run the same statement as before, adding use of the UpdateBase.returning() method, passing the full User entity as what we’d like to return. Session.scalars() is used to allow iteration of User objects:

In the above example, the rendered SQL takes on the form used by the insertmanyvalues feature as requested by the SQLite backend, where individual parameter dictionaries are inlined into a single INSERT statement so that RETURNING may be used.

Changed in version 2.0: The ORM Session now interprets RETURNING clauses from Insert, Update, and even Delete constructs in an ORM context, meaning a mixture of column expressions and ORM mapped entities may be passed to the Insert.returning() method which will then be delivered in the way that ORM results are delivered from constructs such as Select, including that mapped entities will be delivered in the result as ORM mapped objects. Limited support for ORM loader options such as load_only() and selectinload() is also present.

When using bulk INSERT with RETURNING, it’s important to note that most database backends provide no formal guarantee of the order in which the records from RETURNING are returned, including that there is no guarantee that their order will correspond to that of the input records. For applications that need to ensure RETURNING records can be correlated with input data, the additional parameter Insert.returning.sort_by_parameter_order may be specified, which depending on backend may use special INSERT forms that maintain a token which is used to reorder the returned rows appropriately, or in some cases, such as in the example below using the SQLite backend, the operation will INSERT one row at a time:

Added in version 2.0.10: Added Insert.returning.sort_by_parameter_order which is implemented within the insertmanyvalues architecture.

Correlating RETURNING rows to parameter sets - background on approaches taken to guarantee correspondence between input data and result rows without significant loss of performance

The ORM bulk insert feature supports lists of parameter dictionaries that are “heterogeneous”, which basically means “individual dictionaries can have different keys”. When this condition is detected, the ORM will break up the parameter dictionaries into groups corresponding to each set of keys and batch accordingly into separate INSERT statements:

In the above example, the five parameter dictionaries passed translated into three INSERT statements, grouped along the specific sets of keys in each dictionary while still maintaining row order, i.e. ("name", "fullname", "species"), ("name", "species"), ("name","fullname", "species").

The bulk ORM insert feature draws upon a behavior that is also present in the legacy “bulk” insert behavior, as well as in the ORM unit of work overall, which is that rows which contain NULL values are INSERTed using a statement that does not refer to those columns; the rationale here is so that backends and schemas which contain server-side INSERT defaults that may be sensitive to the presence of a NULL value vs. no value present will produce a server side value as expected. This default behavior has the effect of breaking up the bulk inserted batches into more batches of fewer rows:

Above, the bulk INSERT of four rows is broken into three separate statements, the second statement reformatted to not refer to the NULL column for the single parameter dictionary that contains a None value. This default behavior may be undesirable when many rows in the dataset contain random NULL values, as it causes the “executemany” operation to be broken into a larger number of smaller operations; particularly when relying upon insertmanyvalues to reduce the overall number of statements, this can have a bigger performance impact.

To disable the handling of None values in the parameters into separate batches, pass the execution option render_nulls=True; this will cause all parameter dictionaries to be treated equivalently, assuming the same set of keys in each dictionary:

Above, all parameter dictionaries are sent in a single INSERT batch, including the None value present in the third parameter dictionary.

Added in version 2.0.23: Added the render_nulls execution option which mirrors the behavior of the legacy Session.bulk_insert_mappings.render_nulls parameter.

ORM bulk insert builds upon the internal system that is used by the traditional unit of work system in order to emit INSERT statements. This means that for an ORM entity that is mapped to multiple tables, typically one which is mapped using joined table inheritance, the bulk INSERT operation will emit an INSERT statement for each table represented by the mapping, correctly transferring server-generated primary key values to the table rows that depend upon them. The RETURNING feature is also supported here, where the ORM will receive Result objects for each INSERT statement executed, and will then “horizontally splice” them together so that the returned rows include values for all columns inserted:

Bulk INSERT of joined inheritance mappings requires that the ORM make use of the Insert.returning.sort_by_parameter_order parameter internally, so that it can correlate primary key values from RETURNING rows from the base table into the parameter sets being used to INSERT into the “sub” table, which is why the SQLite backend illustrated above transparently degrades to using non-batched statements. Background on this feature is at Correlating RETURNING rows to parameter sets.

The ORM bulk insert feature supports the addition of a fixed set of parameters which may include SQL expressions to be applied to every target row. To achieve this, combine the use of the Insert.values() method, passing a dictionary of parameters that will be applied to all rows, with the usual bulk calling form by including a list of parameter dictionaries that contain individual row values when invoking Session.execute().

As an example, given an ORM mapping that includes a “timestamp” column:

If we wanted to INSERT a series of LogRecord elements, each with a unique message field, however we would like to apply the SQL function now() to all rows, we can pass timestamp within Insert.values() and then pass the additional records using “bulk” mode:

The Insert.values() method itself accommodates a list of parameter dictionaries directly. When using the Insert construct in this way, without passing any list of parameter dictionaries to the Session.execute.params parameter, bulk ORM insert mode is not used, and instead the INSERT statement is rendered exactly as given and invoked exactly once. This mode of operation may be useful both for the case of passing SQL expressions on a per-row basis, and is also used when using “upsert” statements with the ORM, documented later in this chapter at ORM “upsert” Statements.

A contrived example of an INSERT that embeds per-row SQL expressions, and also demonstrates Insert.returning() in this form, is below:

Because bulk ORM insert mode is not used above, the following features are not present:

Joined table inheritance or other multi-table mappings are not supported, since that would require multiple INSERT statements.

Heterogeneous parameter sets are not supported - each element in the VALUES set must have the same columns.

Core-level scale optimizations such as the batching provided by insertmanyvalues are not available; statements will need to ensure the total number of parameters does not exceed limits imposed by the backing database.

For the above reasons, it is generally not recommended to use multiple parameter sets with Insert.values() with ORM INSERT statements unless there is a clear rationale, which is either that “upsert” is being used or there is a need to embed per-row SQL expressions in each parameter set.

ORM “upsert” Statements

The Session includes legacy methods for performing “bulk” INSERT and UPDATE statements. These methods share implementations with the SQLAlchemy 2.0 versions of these features, described at ORM Bulk INSERT Statements and ORM Bulk UPDATE by Primary Key, however lack many features, namely RETURNING support as well as support for session-synchronization.

Code which makes use of Session.bulk_insert_mappings() for example can port code as follows, starting with this mappings example:

The above is expressed using the new API as:

Legacy Session Bulk UPDATE Methods

Selected backends with SQLAlchemy may include dialect-specific Insert constructs which additionally have the ability to perform “upserts”, or INSERTs where an existing row in the parameter set is turned into an approximation of an UPDATE statement instead. By “existing row” , this may mean rows which share the same primary key value, or may refer to other indexed columns within the row that are considered to be unique; this is dependent on the capabilities of the backend in use.

The dialects included with SQLAlchemy that include dialect-specific “upsert” API features are:

SQLite - using Insert documented at INSERT…ON CONFLICT (Upsert)

PostgreSQL - using Insert documented at INSERT…ON CONFLICT (Upsert)

MySQL/MariaDB - using Insert documented at INSERT…ON DUPLICATE KEY UPDATE (Upsert)

Users should review the above sections for background on proper construction of these objects; in particular, the “upsert” method typically needs to refer back to the original statement, so the statement is usually constructed in two separate steps.

Third party backends such as those mentioned at External Dialects may also feature similar constructs.

While SQLAlchemy does not yet have a backend-agnostic upsert construct, the above Insert variants are nonetheless ORM compatible in that they may be used in the same way as the Insert construct itself as documented at ORM Bulk Insert with Per Row SQL Expressions, that is, by embedding the desired rows to INSERT within the Insert.values() method. In the example below, the SQLite insert() function is used to generate an Insert construct that includes “ON CONFLICT DO UPDATE” support. The statement is then passed to Session.execute() where it proceeds normally, with the additional characteristic that the parameter dictionaries passed to Insert.values() are interpreted as ORM mapped attribute keys, rather than column names:

From the SQLAlchemy ORM’s point of view, upsert statements look like regular Insert constructs, which includes that Insert.returning() works with upsert statements in the same way as was demonstrated at ORM Bulk Insert with Per Row SQL Expressions, so that any column expression or relevant ORM entity class may be passed. Continuing from the example in the previous section:

The example above uses RETURNING to return ORM objects for each row inserted or upserted by the statement. The example also adds use of the Populate Existing execution option. This option indicates that User objects which are already present in the Session for rows that already exist should be refreshed with the data from the new row. For a pure Insert statement, this option is not significant, because every row produced is a brand new primary key identity. However when the Insert also includes “upsert” options, it may also be yielding results from rows that already exist and therefore may already have a primary key identity represented in the Session object’s identity map.

The Update construct may be used with Session.execute() in a similar way as the Insert statement is used as described at ORM Bulk INSERT Statements, passing a list of many parameter dictionaries, each dictionary representing an individual row that corresponds to a single primary key value. This use should not be confused with a more common way to use Update statements with the ORM, using an explicit WHERE clause, which is documented at ORM UPDATE and DELETE with Custom WHERE Criteria.

For the “bulk” version of UPDATE, a update() construct is made in terms of an ORM class and passed to the Session.execute() method; the resulting Update object should have no values and typically no WHERE criteria, that is, the Update.values() method is not used, and the Update.where() is usually not used, but may be used in the unusual case that additional filtering criteria would be added.

Passing the Update construct along with a list of parameter dictionaries which each include a full primary key value will invoke bulk UPDATE by primary key mode for the statement, generating the appropriate WHERE criteria to match each row by primary key, and using executemany to run each parameter set against the UPDATE statement:

Note that each parameter dictionary must include a full primary key for each record, else an error is raised.

Like the bulk INSERT feature, heterogeneous parameter lists are supported here as well, where the parameters will be grouped into sub-batches of UPDATE runs.

Changed in version 2.0.11: Additional WHERE criteria can be combined with ORM Bulk UPDATE by Primary Key by using the Update.where() method to add additional criteria. However this criteria is always in addition to the WHERE criteria that’s already made present which includes primary key values.

The RETURNING feature is not available when using the “bulk UPDATE by primary key” feature; the list of multiple parameter dictionaries necessarily makes use of DBAPI executemany, which in its usual form does not typically support result rows.

Changed in version 2.0: Passing an Update construct to the Session.execute() method along with a list of parameter dictionaries now invokes a “bulk update”, which makes use of the same functionality as the legacy Session.bulk_update_mappings() method. This is a behavior change compared to the 1.x series where the Update would only be supported with explicit WHERE criteria and inline VALUES.

The ORM Bulk Update by Primary Key feature, which runs an UPDATE statement per record which includes WHERE criteria for each primary key value, is automatically used when:

the UPDATE statement given is against an ORM entity

the Session is used to execute the statement, and not a Core Connection

The parameters passed are a list of dictionaries.

In order to invoke an UPDATE statement without using “ORM Bulk Update by Primary Key”, invoke the statement against the Connection directly using the Session.connection() method to acquire the current Connection for the transaction:

per-row ORM Bulk Update by Primary Key requires that records contain primary key values

ORM bulk update has similar behavior to ORM bulk insert when using mappings with joined table inheritance; as described at Bulk INSERT for Joined Table Inheritance, the bulk UPDATE operation will emit an UPDATE statement for each table represented in the mapping, for which the given parameters include values to be updated (non-affected tables are skipped).

As discussed at Legacy Session Bulk INSERT Methods, the Session.bulk_update_mappings() method of Session is the legacy form of bulk update, which the ORM makes use of internally when interpreting a update() statement with primary key parameters given; however, when using the legacy version, features such as support for session-synchronization are not included.

Is expressed using the new API as:

Legacy Session Bulk INSERT Methods

The Update and Delete constructs, when constructed with custom WHERE criteria (that is, using the Update.where() and Delete.where() methods), may be invoked in an ORM context by passing them to Session.execute(), without using the Session.execute.params parameter. For Update, the values to be updated should be passed using Update.values().

This mode of use differs from the feature described previously at ORM Bulk UPDATE by Primary Key in that the ORM uses the given WHERE clause as is, rather than fixing the WHERE clause to be by primary key. This means that the single UPDATE or DELETE statement can affect many rows at once.

As an example, below an UPDATE is emitted that affects the “fullname” field of multiple rows

For a DELETE, an example of deleting rows based on criteria:

Please read the following section Important Notes and Caveats for ORM-Enabled Update and Delete for important notes regarding how the functionality of ORM-Enabled UPDATE and DELETE diverges from that of ORM unit of work features, such as using the Session.delete() method to delete individual objects.

The ORM-enabled UPDATE and DELETE features bypass ORM unit of work automation in favor of being able to emit a single UPDATE or DELETE statement that matches multiple rows at once without complexity.

The operations do not offer in-Python cascading of relationships - it is assumed that ON UPDATE CASCADE and/or ON DELETE CASCADE is configured for any foreign key references which require it, otherwise the database may emit an integrity violation if foreign key references are being enforced. See the notes at Using foreign key ON DELETE cascade with ORM relationships for some examples.

After the UPDATE or DELETE, dependent objects in the Session which were impacted by an ON UPDATE CASCADE or ON DELETE CASCADE on related tables, particularly objects that refer to rows that have now been deleted, may still reference those objects. This issue is resolved once the Session is expired, which normally occurs upon Session.commit() or can be forced by using Session.expire_all().

ORM-enabled UPDATEs and DELETEs do not handle joined table inheritance automatically. See the section UPDATE/DELETE with Custom WHERE Criteria for Joined Table Inheritance for notes on how to work with joined-inheritance mappings.

The WHERE criteria needed in order to limit the polymorphic identity to specific subclasses for single-table-inheritance mappings is included automatically . This only applies to a subclass mapper that has no table of its own.

The with_loader_criteria() option is supported by ORM update and delete operations; criteria here will be added to that of the UPDATE or DELETE statement being emitted, as well as taken into account during the “synchronize” process.

In order to intercept ORM-enabled UPDATE and DELETE operations with event handlers, use the SessionEvents.do_orm_execute() event.

When making use of update() or delete() in conjunction with ORM-enabled execution using Session.execute(), additional ORM-specific functionality is present which will synchronize the state being changed by the statement with that of the objects that are currently present within the identity map of the Session. By “synchronize” we mean that UPDATEd attributes will be refreshed with the new value, or at the very least expired so that they will re-populate with their new value on next access, and DELETEd objects will be moved into the deleted state.

This synchronization is controllable as the “synchronization strategy”, which is passed as an string ORM execution option, typically by using the Session.execute.execution_options dictionary:

The execution option may also be bundled with the statement itself using the Executable.execution_options() method:

The following values for synchronize_session are supported:

'auto' - this is the default. The 'fetch' strategy will be used on backends that support RETURNING, which includes all SQLAlchemy-native drivers except for MySQL. If RETURNING is not supported, the 'evaluate' strategy will be used instead.

'fetch' - Retrieves the primary key identity of affected rows by either performing a SELECT before the UPDATE or DELETE, or by using RETURNING if the database supports it, so that in-memory objects which are affected by the operation can be refreshed with new values (updates) or expunged from the Session (deletes). This synchronization strategy may be used even if the given update() or delete() construct explicitly specifies entities or columns using UpdateBase.returning().

Changed in version 2.0: Explicit UpdateBase.returning() may be combined with the 'fetch' synchronization strategy when using ORM-enabled UPDATE and DELETE with WHERE criteria. The actual statement will contain the union of columns between that which the 'fetch' strategy requires and those which were requested.

'evaluate' - This indicates to evaluate the WHERE criteria given in the UPDATE or DELETE statement in Python, to locate matching objects within the Session. This approach does not add any SQL round trips to the operation, and in the absence of RETURNING support, may be more efficient. For UPDATE or DELETE statements with complex criteria, the 'evaluate' strategy may not be able to evaluate the expression in Python and will raise an error. If this occurs, use the 'fetch' strategy for the operation instead.

If a SQL expression makes use of custom operators using the Operators.op() or custom_op feature, the Operators.op.python_impl parameter may be used to indicate a Python function that will be used by the "evaluate" synchronization strategy.

Added in version 2.0.

The "evaluate" strategy should be avoided if an UPDATE operation is to run on a Session that has many objects which have been expired, because it will necessarily need to refresh objects in order to test them against the given WHERE criteria, which will emit a SELECT for each one. In this case, and particularly if the backend supports RETURNING, the "fetch" strategy should be preferred.

False - don’t synchronize the session. This option may be useful for backends that don’t support RETURNING where the "evaluate" strategy is not able to be used. In this case, the state of objects in the Session is unchanged and will not automatically correspond to the UPDATE or DELETE statement that was emitted, if such objects that would normally correspond to the rows matched are present.

The UpdateBase.returning() method is fully compatible with ORM-enabled UPDATE and DELETE with WHERE criteria. Full ORM objects and/or columns may be indicated for RETURNING:

The support for RETURNING is also compatible with the fetch synchronization strategy, which also uses RETURNING. The ORM will organize the columns in RETURNING appropriately so that the synchronization proceeds as well as that the returned Result will contain the requested entities and SQL columns in their requested order.

Added in version 2.0: UpdateBase.returning() may be used for ORM enabled UPDATE and DELETE while still retaining full compatibility with the fetch synchronization strategy.

The UPDATE/DELETE with WHERE criteria feature, unlike the ORM Bulk UPDATE by Primary Key, only emits a single UPDATE or DELETE statement per call to Session.execute(). This means that when running an update() or delete() statement against a multi-table mapping, such as a subclass in a joined-table inheritance mapping, the statement must conform to the backend’s current capabilities, which may include that the backend does not support an UPDATE or DELETE statement that refers to multiple tables, or may have only limited support for this. This means that for mappings such as joined inheritance subclasses, the ORM version of the UPDATE/DELETE with WHERE criteria feature can only be used to a limited extent or not at all, depending on specifics.

The most straightforward way to emit a multi-row UPDATE statement for a joined-table subclass is to refer to the sub-table alone. This means the Update() construct should only refer to attributes that are local to the subclass table, as in the example below:

With the above form, a rudimentary way to refer to the base table in order to locate rows which will work on any SQL backend is so use a subquery:

For backends that support UPDATE…FROM, the subquery may be stated instead as additional plain WHERE criteria, however the criteria between the two tables must be stated explicitly in some way:

For a DELETE, it’s expected that rows in both the base table and the sub-table would be DELETEd at the same time. To DELETE many rows of joined inheritance objects without using cascading foreign keys, emit DELETE for each table individually:

Overall, normal unit of work processes should be preferred for updating and deleting rows for joined inheritance and other multi-table mappings, unless there is a performance rationale for using custom WHERE criteria.

The ORM enabled UPDATE/DELETE with WHERE feature was originally part of the now-legacy Query object, in the Query.update() and Query.delete() methods. These methods remain available and provide a subset of the same functionality as that described at ORM UPDATE and DELETE with Custom WHERE Criteria. The primary difference is that the legacy methods don’t provide for explicit RETURNING support.

Next Query Guide Section: Column Loading Options

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (json):
```json
>>> from sqlalchemy import insert
>>> session.execute(
...     insert(User),
...     [
...         {"name": "spongebob", "fullname": "Spongebob Squarepants"},
...         {"name": "sandy", "fullname": "Sandy Cheeks"},
...         {"name": "patrick", "fullname": "Patrick Star"},
...         {"name": "squidward", "fullname": "Squidward Tentacles"},
...         {"name": "ehkrabs", "fullname": "Eugene H. Krabs"},
...     ],
... )
INSERT INTO user_account (name, fullname) VALUES (?, ?)
[...] [('spongebob', 'Spongebob Squarepants'), ('sandy', 'Sandy Cheeks'), ('patrick', 'Patrick Star'),
('squidward', 'Squidward Tentacles'), ('ehkrabs', 'Eugene H. Krabs')]
<...>
```

Example 2 (json):
```json
>>> users = session.scalars(
...     insert(User).returning(User),
...     [
...         {"name": "spongebob", "fullname": "Spongebob Squarepants"},
...         {"name": "sandy", "fullname": "Sandy Cheeks"},
...         {"name": "patrick", "fullname": "Patrick Star"},
...         {"name": "squidward", "fullname": "Squidward Tentacles"},
...         {"name": "ehkrabs", "fullname": "Eugene H. Krabs"},
...     ],
... )
INSERT INTO user_account (name, fullname)
VALUES (?, ?), (?, ?), (?, ?), (?, ?), (?, ?)
RETURNING id, name, fullname, species
[...] ('spongebob', 'Spongebob Squarepants', 'sandy', 'Sandy Cheeks',
'patrick', 'Patrick Star', 'squidward', 'Squidward Tentacles',
'ehkrabs', 'Eugene H. Krabs')
>>> print(users.all())
[User(name='spongebob', fullname='Spongebob Squarepants'),
 User(name='sandy', fullname='Sandy Cheeks'),
 User(name='patrick', fullname='Patrick Star'),
 User(name='squidward', fullname='Squidward Tentacles'),
 User(name='ehkrabs', fullname='Eugene H. Krabs')]
```

Example 3 (json):
```json
>>> data = [
...     {"name": "pearl", "fullname": "Pearl Krabs"},
...     {"name": "plankton", "fullname": "Plankton"},
...     {"name": "gary", "fullname": "Gary"},
... ]
>>> user_ids = session.scalars(
...     insert(User).returning(User.id, sort_by_parameter_order=True), data
... )
INSERT INTO user_account (name, fullname) VALUES (?, ?) RETURNING id
[... (insertmanyvalues) 1/3 (ordered; batch not supported)] ('pearl', 'Pearl Krabs')
INSERT INTO user_account (name, fullname) VALUES (?, ?) RETURNING id
[insertmanyvalues 2/3 (ordered; batch not supported)] ('plankton', 'Plankton')
INSERT INTO user_account (name, fullname) VALUES (?, ?) RETURNING id
[insertmanyvalues 3/3 (ordered; batch not supported)] ('gary', 'Gary')
>>> for user_id, input_record in zip(user_ids, data):
...     input_record["id"] = user_id
>>> print(data)
[{'name': 'pearl', 'fullname': 'Pearl Krabs', 'id': 6},
{'name': 'plankton', 'fullname': 'Plankton', 'id': 7},
{'name': 'gary', 'fullname': 'Gary', 'id': 8}]
```

Example 4 (json):
```json
>>> users = session.scalars(
...     insert(User).returning(User),
...     [
...         {
...             "name": "spongebob",
...             "fullname": "Spongebob Squarepants",
...             "species": "Sea Sponge",
...         },
...         {"name": "sandy", "fullname": "Sandy Cheeks", "species": "Squirrel"},
...         {"name": "patrick", "species": "Starfish"},
...         {
...             "name": "squidward",
...             "fullname": "Squidward Tentacles",
...             "species": "Squid",
...         },
...         {"name": "ehkrabs", "fullname": "Eugene H. Krabs", "species": "Crab"},
...     ],
... )
INSERT INTO user_account (name, fullname, species)
VALUES (?, ?, ?), (?, ?, ?) RETURNING id, name, fullname, species
[... (insertmanyvalues) 1/1 (unordered)] ('spongebob', 'Spongebob Squarepants', 'Sea Sponge',
'sandy', 'Sandy Cheeks', 'Squirrel')
INSERT INTO user_account (name, species)
VALUES (?, ?) RETURNING id, name, fullname, species
[...] ('patrick', 'Starfish')
INSERT INTO user_account (name, fullname, species)
VALUES (?, ?, ?), (?, ?, ?) RETURNING id, name, fullname, species
[... (insertmanyvalues) 1/1 (unordered)] ('squidward', 'Squidward Tentacles',
'Squid', 'ehkrabs', 'Eugene H. Krabs', 'Crab')
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/core/dml.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Core
    - Project Versions
- Insert, Updates, Deletes¶
- DML Foundational Constructors¶
- DML Class Documentation Constructors¶

Home | Download this Documentation

Home | Download this Documentation

INSERT, UPDATE and DELETE statements build on a hierarchy starting with UpdateBase. The Insert and Update constructs build on the intermediary ValuesBase.

Top level “INSERT”, “UPDATE”, “DELETE” constructors.

Construct Delete object.

Construct an Insert object.

Construct an Update object.

Construct Delete object.

Similar functionality is available via the TableClause.delete() method on Table.

table¶ – The table to delete rows from.

Using UPDATE and DELETE Statements - in the SQLAlchemy Unified Tutorial

Construct an Insert object.

Similar functionality is available via the TableClause.insert() method on Table.

Using INSERT Statements - in the SQLAlchemy Unified Tutorial

table¶ – TableClause which is the subject of the insert.

values¶ – collection of values to be inserted; see Insert.values() for a description of allowed formats here. Can be omitted entirely; a Insert construct will also dynamically render the VALUES clause at execution time based on the parameters passed to Connection.execute().

inline¶ – if True, no attempt will be made to retrieve the SQL-generated default values to be provided within the statement; in particular, this allows SQL expressions to be rendered ‘inline’ within the statement without the need to pre-execute them beforehand; for backends that support “returning”, this turns off the “implicit returning” feature for the statement.

If both insert.values and compile-time bind parameters are present, the compile-time bind parameters override the information specified within insert.values on a per-key basis.

The keys within Insert.values can be either Column objects or their string identifiers. Each key may reference one of:

a literal data value (i.e. string, number, etc.);

If a SELECT statement is specified which references this INSERT statement’s table, the statement will be correlated against the INSERT statement.

Using INSERT Statements - in the SQLAlchemy Unified Tutorial

Construct an Update object.

Similar functionality is available via the TableClause.update() method on Table.

table¶ – A Table object representing the database table to be updated.

Using UPDATE and DELETE Statements - in the SQLAlchemy Unified Tutorial

Class documentation for the constructors listed at DML Foundational Constructors.

Represent a DELETE construct.

Represent an INSERT construct.

Represent an Update construct.

Form the base for INSERT, UPDATE, and DELETE statements.

Supplies support for ValuesBase.values() to INSERT and UPDATE constructs.

inherits from sqlalchemy.sql.expression.DMLWhereBase, sqlalchemy.sql.expression.UpdateBase

Represent a DELETE construct.

The Delete object is created using the delete() function.

Return a new construct with the given expression(s) added to its WHERE clause, joined to the existing clause via AND, if any.

with_dialect_options()

Add dialect options to this INSERT/UPDATE/DELETE object.

Add a RETURNING or equivalent clause to this statement.

inherited from the DMLWhereBase.where() method of DMLWhereBase

Return a new construct with the given expression(s) added to its WHERE clause, joined to the existing clause via AND, if any.

Both Update.where() and Delete.where() support multiple-table forms, including database-specific UPDATE...FROM as well as DELETE..USING. For backends that don’t have multiple-table support, a backend agnostic approach to using multiple tables is to make use of correlated subqueries. See the linked tutorial sections below for examples.

Multiple Table Deletes

inherited from the UpdateBase.with_dialect_options() method of UpdateBase

Add dialect options to this INSERT/UPDATE/DELETE object.

inherited from the UpdateBase.returning() method of UpdateBase

Add a RETURNING or equivalent clause to this statement.

The method may be invoked multiple times to add new entries to the list of expressions to be returned.

Added in version 1.4.0b2: The method may be invoked multiple times to add new entries to the list of expressions to be returned.

The given collection of column expressions should be derived from the table that is the target of the INSERT, UPDATE, or DELETE. While Column objects are typical, the elements can also be expressions:

Upon compilation, a RETURNING clause, or database equivalent, will be rendered within the statement. For INSERT and UPDATE, the values are the newly inserted/updated values. For DELETE, the values are those of the rows which were deleted.

Upon execution, the values of the columns to be returned are made available via the result set and can be iterated using CursorResult.fetchone() and similar. For DBAPIs which do not natively support returning values (i.e. cx_oracle), SQLAlchemy will approximate this behavior at the result level so that a reasonable amount of behavioral neutrality is provided.

Note that not all databases/DBAPIs support RETURNING. For those backends with no support, an exception is raised upon compilation and/or execution. For those who do support it, the functionality across backends varies greatly, including restrictions on executemany() and other statements which return multiple rows. Please read the documentation notes for the database in use in order to determine the availability of RETURNING.

*cols¶ – series of columns, SQL expressions, or whole tables entities to be returned.

sort_by_parameter_order¶ –

for a batch INSERT that is being executed against multiple parameter sets, organize the results of RETURNING so that the returned rows correspond to the order of parameter sets passed in. This applies only to an executemany execution for supporting dialects and typically makes use of the insertmanyvalues feature.

Added in version 2.0.10.

Correlating RETURNING rows to parameter sets - background on sorting of RETURNING rows for bulk INSERT (Core level discussion)

Correlating RETURNING records with input data order - example of use with ORM Bulk INSERT Statements (ORM level discussion)

UpdateBase.return_defaults() - an alternative method tailored towards efficient fetching of server-side defaults and triggers for single-row INSERTs or UPDATEs.

INSERT…RETURNING - in the SQLAlchemy Unified Tutorial

inherits from sqlalchemy.sql.expression.ValuesBase

Represent an INSERT construct.

The Insert object is created using the insert() function.

with_dialect_options()

Add dialect options to this INSERT/UPDATE/DELETE object.

Specify a fixed VALUES clause for an INSERT statement, or the SET clause for an UPDATE.

Add a RETURNING or equivalent clause to this statement.

Return a new Insert construct which represents an INSERT...FROM SELECT statement.

Make this Insert construct “inline” .

SELECT statement for INSERT .. FROM SELECT

inherited from the UpdateBase.with_dialect_options() method of UpdateBase

Add dialect options to this INSERT/UPDATE/DELETE object.

inherited from the ValuesBase.values() method of ValuesBase

Specify a fixed VALUES clause for an INSERT statement, or the SET clause for an UPDATE.

Note that the Insert and Update constructs support per-execution time formatting of the VALUES and/or SET clauses, based on the arguments passed to Connection.execute(). However, the ValuesBase.values() method can be used to “fix” a particular set of parameters into the statement.

Multiple calls to ValuesBase.values() will produce a new construct, each one with the parameter list modified to include the new parameters sent. In the typical case of a single dictionary of parameters, the newly passed keys will replace the same keys in the previous construct. In the case of a list-based “multiple values” construct, each new list of values is extended onto the existing list of values.

key value pairs representing the string key of a Column mapped to the value to be rendered into the VALUES or SET clause:

As an alternative to passing key/value parameters, a dictionary, tuple, or list of dictionaries or tuples can be passed as a single positional argument in order to form the VALUES or SET clause of the statement. The forms that are accepted vary based on whether this is an Insert or an Update construct.

For either an Insert or Update construct, a single dictionary can be passed, which works the same as that of the kwargs form:

Also for either form but more typically for the Insert construct, a tuple that contains an entry for every column in the table is also accepted:

The Insert construct also supports being passed a list of dictionaries or full-table-tuples, which on the server will render the less common SQL syntax of “multiple values” - this syntax is supported on backends such as SQLite, PostgreSQL, MySQL, but not necessarily others:

The above form would render a multiple VALUES statement similar to:

It is essential to note that passing multiple values is NOT the same as using traditional executemany() form. The above syntax is a special syntax not typically used. To emit an INSERT statement against multiple rows, the normal method is to pass a multiple values list to the Connection.execute() method, which is supported by all database backends and is generally more efficient for a very large number of parameters.

Sending Multiple Parameters - an introduction to the traditional Core method of multiple parameter set invocation for INSERTs and other statements.

The UPDATE construct also supports rendering the SET parameters in a specific order. For this feature refer to the Update.ordered_values() method.

Update.ordered_values()

inherited from the UpdateBase.returning() method of UpdateBase

Add a RETURNING or equivalent clause to this statement.

The method may be invoked multiple times to add new entries to the list of expressions to be returned.

Added in version 1.4.0b2: The method may be invoked multiple times to add new entries to the list of expressions to be returned.

The given collection of column expressions should be derived from the table that is the target of the INSERT, UPDATE, or DELETE. While Column objects are typical, the elements can also be expressions:

Upon compilation, a RETURNING clause, or database equivalent, will be rendered within the statement. For INSERT and UPDATE, the values are the newly inserted/updated values. For DELETE, the values are those of the rows which were deleted.

Upon execution, the values of the columns to be returned are made available via the result set and can be iterated using CursorResult.fetchone() and similar. For DBAPIs which do not natively support returning values (i.e. cx_oracle), SQLAlchemy will approximate this behavior at the result level so that a reasonable amount of behavioral neutrality is provided.

Note that not all databases/DBAPIs support RETURNING. For those backends with no support, an exception is raised upon compilation and/or execution. For those who do support it, the functionality across backends varies greatly, including restrictions on executemany() and other statements which return multiple rows. Please read the documentation notes for the database in use in order to determine the availability of RETURNING.

*cols¶ – series of columns, SQL expressions, or whole tables entities to be returned.

sort_by_parameter_order¶ –

for a batch INSERT that is being executed against multiple parameter sets, organize the results of RETURNING so that the returned rows correspond to the order of parameter sets passed in. This applies only to an executemany execution for supporting dialects and typically makes use of the insertmanyvalues feature.

Added in version 2.0.10.

Correlating RETURNING rows to parameter sets - background on sorting of RETURNING rows for bulk INSERT (Core level discussion)

Correlating RETURNING records with input data order - example of use with ORM Bulk INSERT Statements (ORM level discussion)

UpdateBase.return_defaults() - an alternative method tailored towards efficient fetching of server-side defaults and triggers for single-row INSERTs or UPDATEs.

INSERT…RETURNING - in the SQLAlchemy Unified Tutorial

Return a new Insert construct which represents an INSERT...FROM SELECT statement.

names¶ – a sequence of string column names or Column objects representing the target columns.

select¶ – a select() construct, FromClause or other construct which resolves into a FromClause, such as an ORM Query object, etc. The order of columns returned from this FROM clause should correspond to the order of columns sent as the names parameter; while this is not checked before passing along to the database, the database would normally raise an exception if these column lists don’t correspond.

if True, non-server default values and SQL expressions as specified on Column objects (as documented in Column INSERT/UPDATE Defaults) not otherwise specified in the list of names will be rendered into the INSERT and SELECT statements, so that these values are also included in the data to be inserted.

A Python-side default that uses a Python callable function will only be invoked once for the whole statement, and not per row.

Make this Insert construct “inline” .

When set, no attempt will be made to retrieve the SQL-generated default values to be provided within the statement; in particular, this allows SQL expressions to be rendered ‘inline’ within the statement without the need to pre-execute them beforehand; for backends that support “returning”, this turns off the “implicit returning” feature for the statement.

Changed in version 1.4: the Insert.inline parameter is now superseded by the Insert.inline() method.

SELECT statement for INSERT .. FROM SELECT

inherits from sqlalchemy.sql.expression.DMLWhereBase, sqlalchemy.sql.expression.ValuesBase

Represent an Update construct.

The Update object is created using the update() function.

Add a RETURNING or equivalent clause to this statement.

Return a new construct with the given expression(s) added to its WHERE clause, joined to the existing clause via AND, if any.

with_dialect_options()

Add dialect options to this INSERT/UPDATE/DELETE object.

Specify a fixed VALUES clause for an INSERT statement, or the SET clause for an UPDATE.

Make this Update construct “inline” .

Specify the VALUES clause of this UPDATE statement with an explicit parameter ordering that will be maintained in the SET clause of the resulting UPDATE statement.

inherited from the UpdateBase.returning() method of UpdateBase

Add a RETURNING or equivalent clause to this statement.

The method may be invoked multiple times to add new entries to the list of expressions to be returned.

Added in version 1.4.0b2: The method may be invoked multiple times to add new entries to the list of expressions to be returned.

The given collection of column expressions should be derived from the table that is the target of the INSERT, UPDATE, or DELETE. While Column objects are typical, the elements can also be expressions:

Upon compilation, a RETURNING clause, or database equivalent, will be rendered within the statement. For INSERT and UPDATE, the values are the newly inserted/updated values. For DELETE, the values are those of the rows which were deleted.

Upon execution, the values of the columns to be returned are made available via the result set and can be iterated using CursorResult.fetchone() and similar. For DBAPIs which do not natively support returning values (i.e. cx_oracle), SQLAlchemy will approximate this behavior at the result level so that a reasonable amount of behavioral neutrality is provided.

Note that not all databases/DBAPIs support RETURNING. For those backends with no support, an exception is raised upon compilation and/or execution. For those who do support it, the functionality across backends varies greatly, including restrictions on executemany() and other statements which return multiple rows. Please read the documentation notes for the database in use in order to determine the availability of RETURNING.

*cols¶ – series of columns, SQL expressions, or whole tables entities to be returned.

sort_by_parameter_order¶ –

for a batch INSERT that is being executed against multiple parameter sets, organize the results of RETURNING so that the returned rows correspond to the order of parameter sets passed in. This applies only to an executemany execution for supporting dialects and typically makes use of the insertmanyvalues feature.

Added in version 2.0.10.

Correlating RETURNING rows to parameter sets - background on sorting of RETURNING rows for bulk INSERT (Core level discussion)

Correlating RETURNING records with input data order - example of use with ORM Bulk INSERT Statements (ORM level discussion)

UpdateBase.return_defaults() - an alternative method tailored towards efficient fetching of server-side defaults and triggers for single-row INSERTs or UPDATEs.

INSERT…RETURNING - in the SQLAlchemy Unified Tutorial

inherited from the DMLWhereBase.where() method of DMLWhereBase

Return a new construct with the given expression(s) added to its WHERE clause, joined to the existing clause via AND, if any.

Both Update.where() and Delete.where() support multiple-table forms, including database-specific UPDATE...FROM as well as DELETE..USING. For backends that don’t have multiple-table support, a backend agnostic approach to using multiple tables is to make use of correlated subqueries. See the linked tutorial sections below for examples.

Multiple Table Deletes

inherited from the UpdateBase.with_dialect_options() method of UpdateBase

Add dialect options to this INSERT/UPDATE/DELETE object.

inherited from the ValuesBase.values() method of ValuesBase

Specify a fixed VALUES clause for an INSERT statement, or the SET clause for an UPDATE.

Note that the Insert and Update constructs support per-execution time formatting of the VALUES and/or SET clauses, based on the arguments passed to Connection.execute(). However, the ValuesBase.values() method can be used to “fix” a particular set of parameters into the statement.

Multiple calls to ValuesBase.values() will produce a new construct, each one with the parameter list modified to include the new parameters sent. In the typical case of a single dictionary of parameters, the newly passed keys will replace the same keys in the previous construct. In the case of a list-based “multiple values” construct, each new list of values is extended onto the existing list of values.

key value pairs representing the string key of a Column mapped to the value to be rendered into the VALUES or SET clause:

As an alternative to passing key/value parameters, a dictionary, tuple, or list of dictionaries or tuples can be passed as a single positional argument in order to form the VALUES or SET clause of the statement. The forms that are accepted vary based on whether this is an Insert or an Update construct.

For either an Insert or Update construct, a single dictionary can be passed, which works the same as that of the kwargs form:

Also for either form but more typically for the Insert construct, a tuple that contains an entry for every column in the table is also accepted:

The Insert construct also supports being passed a list of dictionaries or full-table-tuples, which on the server will render the less common SQL syntax of “multiple values” - this syntax is supported on backends such as SQLite, PostgreSQL, MySQL, but not necessarily others:

The above form would render a multiple VALUES statement similar to:

It is essential to note that passing multiple values is NOT the same as using traditional executemany() form. The above syntax is a special syntax not typically used. To emit an INSERT statement against multiple rows, the normal method is to pass a multiple values list to the Connection.execute() method, which is supported by all database backends and is generally more efficient for a very large number of parameters.

Sending Multiple Parameters - an introduction to the traditional Core method of multiple parameter set invocation for INSERTs and other statements.

The UPDATE construct also supports rendering the SET parameters in a specific order. For this feature refer to the Update.ordered_values() method.

Update.ordered_values()

Make this Update construct “inline” .

When set, SQL defaults present on Column objects via the default keyword will be compiled ‘inline’ into the statement and not pre-executed. This means that their values will not be available in the dictionary returned from CursorResult.last_updated_params().

Changed in version 1.4: the update.inline parameter is now superseded by the Update.inline() method.

Specify the VALUES clause of this UPDATE statement with an explicit parameter ordering that will be maintained in the SET clause of the resulting UPDATE statement.

Parameter Ordered Updates - full example of the Update.ordered_values() method.

Changed in version 1.4: The Update.ordered_values() method supersedes the update.preserve_parameter_order parameter, which will be removed in SQLAlchemy 2.0.

inherits from sqlalchemy.sql.roles.DMLRole, sqlalchemy.sql.expression.HasCTE, sqlalchemy.sql.expression.HasCompileState, sqlalchemy.sql.expression.DialectKWArgs, sqlalchemy.sql.expression.HasPrefixes, sqlalchemy.sql.expression.Generative, sqlalchemy.sql.expression.ExecutableReturnsRows, sqlalchemy.sql.expression.ClauseElement

Form the base for INSERT, UPDATE, and DELETE statements.

Return the RETURNING columns as a column collection for this statement.

Return True if this ReturnsRows is ‘derived’ from the given FromClause.

Set the parameters for the statement.

Make use of a RETURNING clause for the purpose of fetching server-side expressions and defaults, for supporting backends only.

Add a RETURNING or equivalent clause to this statement.

with_dialect_options()

Add dialect options to this INSERT/UPDATE/DELETE object.

Add a table hint for a single table to this INSERT/UPDATE/DELETE statement.

Return a plugin-enabled description of the table and/or entity which this DML construct is operating against.

This attribute is generally useful when using the ORM, as an extended structure which includes information about mapped entities is returned. The section Inspecting entities and columns from ORM-enabled SELECT and DML statements contains more background.

For a Core statement, the structure returned by this accessor is derived from the UpdateBase.table attribute, and refers to the Table being inserted, updated, or deleted:

Added in version 1.4.33.

UpdateBase.returning_column_descriptions

Select.column_descriptions - entity information for a select() construct

Inspecting entities and columns from ORM-enabled SELECT and DML statements - ORM background

Return the RETURNING columns as a column collection for this statement.

Added in version 1.4.

Return True if this ReturnsRows is ‘derived’ from the given FromClause.

Since these are DMLs, we dont want such statements ever being adapted so we return False for derives.

Set the parameters for the statement.

This method raises NotImplementedError on the base class, and is overridden by ValuesBase to provide the SET/VALUES clause of UPDATE and INSERT.

Make use of a RETURNING clause for the purpose of fetching server-side expressions and defaults, for supporting backends only.

The UpdateBase.return_defaults() method is used by the ORM for its internal work in fetching newly generated primary key and server default values, in particular to provide the underlying implementation of the Mapper.eager_defaults ORM feature as well as to allow RETURNING support with bulk ORM inserts. Its behavior is fairly idiosyncratic and is not really intended for general use. End users should stick with using UpdateBase.returning() in order to add RETURNING clauses to their INSERT, UPDATE and DELETE statements.

Normally, a single row INSERT statement will automatically populate the CursorResult.inserted_primary_key attribute when executed, which stores the primary key of the row that was just inserted in the form of a Row object with column names as named tuple keys (and the Row._mapping view fully populated as well). The dialect in use chooses the strategy to use in order to populate this data; if it was generated using server-side defaults and / or SQL expressions, dialect-specific approaches such as cursor.lastrowid or RETURNING are typically used to acquire the new primary key value.

However, when the statement is modified by calling UpdateBase.return_defaults() before executing the statement, additional behaviors take place only for backends that support RETURNING and for Table objects that maintain the Table.implicit_returning parameter at its default value of True. In these cases, when the CursorResult is returned from the statement’s execution, not only will CursorResult.inserted_primary_key be populated as always, the CursorResult.returned_defaults attribute will also be populated with a Row named-tuple representing the full range of server generated values from that single row, including values for any columns that specify Column.server_default or which make use of Column.default using a SQL expression.

When invoking INSERT statements with multiple rows using insertmanyvalues, the UpdateBase.return_defaults() modifier will have the effect of the CursorResult.inserted_primary_key_rows and CursorResult.returned_defaults_rows attributes being fully populated with lists of Row objects representing newly inserted primary key values as well as newly inserted server generated values for each row inserted. The CursorResult.inserted_primary_key and CursorResult.returned_defaults attributes will also continue to be populated with the first row of these two collections.

If the backend does not support RETURNING or the Table in use has disabled Table.implicit_returning, then no RETURNING clause is added and no additional data is fetched, however the INSERT, UPDATE or DELETE statement proceeds normally.

When used against an UPDATE statement UpdateBase.return_defaults() instead looks for columns that include Column.onupdate or Column.server_onupdate parameters assigned, when constructing the columns that will be included in the RETURNING clause by default if explicit columns were not specified. When used against a DELETE statement, no columns are included in RETURNING by default, they instead must be specified explicitly as there are no columns that normally change values when a DELETE statement proceeds.

Added in version 2.0: UpdateBase.return_defaults() is supported for DELETE statements also and has been moved from ValuesBase to UpdateBase.

The UpdateBase.return_defaults() method is mutually exclusive against the UpdateBase.returning() method and errors will be raised during the SQL compilation process if both are used at the same time on one statement. The RETURNING clause of the INSERT, UPDATE or DELETE statement is therefore controlled by only one of these methods at a time.

The UpdateBase.return_defaults() method differs from UpdateBase.returning() in these ways:

UpdateBase.return_defaults() method causes the CursorResult.returned_defaults collection to be populated with the first row from the RETURNING result. This attribute is not populated when using UpdateBase.returning().

UpdateBase.return_defaults() is compatible with existing logic used to fetch auto-generated primary key values that are then populated into the CursorResult.inserted_primary_key attribute. By contrast, using UpdateBase.returning() will have the effect of the CursorResult.inserted_primary_key attribute being left unpopulated.

UpdateBase.return_defaults() can be called against any backend. Backends that don’t support RETURNING will skip the usage of the feature, rather than raising an exception, unless supplemental_cols is passed. The return value of CursorResult.returned_defaults will be None for backends that don’t support RETURNING or for which the target Table sets Table.implicit_returning to False.

An INSERT statement invoked with executemany() is supported if the backend database driver supports the insertmanyvalues feature which is now supported by most SQLAlchemy-included backends. When executemany is used, the CursorResult.returned_defaults_rows and CursorResult.inserted_primary_key_rows accessors will return the inserted defaults and primary keys.

Added in version 1.4: Added CursorResult.returned_defaults_rows and CursorResult.inserted_primary_key_rows accessors. In version 2.0, the underlying implementation which fetches and populates the data for these attributes was generalized to be supported by most backends, whereas in 1.4 they were only supported by the psycopg2 driver.

cols¶ – optional list of column key names or Column that acts as a filter for those columns that will be fetched.

optional list of RETURNING expressions, in the same form as one would pass to the UpdateBase.returning() method. When present, the additional columns will be included in the RETURNING clause, and the CursorResult object will be “rewound” when returned, so that methods like CursorResult.all() will return new rows mostly as though the statement used UpdateBase.returning() directly. However, unlike when using UpdateBase.returning() directly, the order of the columns is undefined, so can only be targeted using names or Row._mapping keys; they cannot reliably be targeted positionally.

Added in version 2.0.

sort_by_parameter_order¶ –

for a batch INSERT that is being executed against multiple parameter sets, organize the results of RETURNING so that the returned rows correspond to the order of parameter sets passed in. This applies only to an executemany execution for supporting dialects and typically makes use of the insertmanyvalues feature.

Added in version 2.0.10.

Correlating RETURNING rows to parameter sets - background on sorting of RETURNING rows for bulk INSERT

UpdateBase.returning()

CursorResult.returned_defaults

CursorResult.returned_defaults_rows

CursorResult.inserted_primary_key

CursorResult.inserted_primary_key_rows

Add a RETURNING or equivalent clause to this statement.

The method may be invoked multiple times to add new entries to the list of expressions to be returned.

Added in version 1.4.0b2: The method may be invoked multiple times to add new entries to the list of expressions to be returned.

The given collection of column expressions should be derived from the table that is the target of the INSERT, UPDATE, or DELETE. While Column objects are typical, the elements can also be expressions:

Upon compilation, a RETURNING clause, or database equivalent, will be rendered within the statement. For INSERT and UPDATE, the values are the newly inserted/updated values. For DELETE, the values are those of the rows which were deleted.

Upon execution, the values of the columns to be returned are made available via the result set and can be iterated using CursorResult.fetchone() and similar. For DBAPIs which do not natively support returning values (i.e. cx_oracle), SQLAlchemy will approximate this behavior at the result level so that a reasonable amount of behavioral neutrality is provided.

Note that not all databases/DBAPIs support RETURNING. For those backends with no support, an exception is raised upon compilation and/or execution. For those who do support it, the functionality across backends varies greatly, including restrictions on executemany() and other statements which return multiple rows. Please read the documentation notes for the database in use in order to determine the availability of RETURNING.

*cols¶ – series of columns, SQL expressions, or whole tables entities to be returned.

sort_by_parameter_order¶ –

for a batch INSERT that is being executed against multiple parameter sets, organize the results of RETURNING so that the returned rows correspond to the order of parameter sets passed in. This applies only to an executemany execution for supporting dialects and typically makes use of the insertmanyvalues feature.

Added in version 2.0.10.

Correlating RETURNING rows to parameter sets - background on sorting of RETURNING rows for bulk INSERT (Core level discussion)

Correlating RETURNING records with input data order - example of use with ORM Bulk INSERT Statements (ORM level discussion)

UpdateBase.return_defaults() - an alternative method tailored towards efficient fetching of server-side defaults and triggers for single-row INSERTs or UPDATEs.

INSERT…RETURNING - in the SQLAlchemy Unified Tutorial

Return a plugin-enabled description of the columns which this DML construct is RETURNING against, in other words the expressions established as part of UpdateBase.returning().

This attribute is generally useful when using the ORM, as an extended structure which includes information about mapped entities is returned. The section Inspecting entities and columns from ORM-enabled SELECT and DML statements contains more background.

For a Core statement, the structure returned by this accessor is derived from the same objects that are returned by the UpdateBase.exported_columns accessor:

Added in version 1.4.33.

UpdateBase.entity_description

Select.column_descriptions - entity information for a select() construct

Inspecting entities and columns from ORM-enabled SELECT and DML statements - ORM background

Add dialect options to this INSERT/UPDATE/DELETE object.

Add a table hint for a single table to this INSERT/UPDATE/DELETE statement.

UpdateBase.with_hint() currently applies only to Microsoft SQL Server. For MySQL INSERT/UPDATE/DELETE hints, use UpdateBase.prefix_with().

The text of the hint is rendered in the appropriate location for the database backend in use, relative to the Table that is the subject of this statement, or optionally to that of the given Table passed as the selectable argument.

The dialect_name option will limit the rendering of a particular hint to a particular backend. Such as, to add a hint that only takes effect for SQL Server:

text¶ – Text of the hint.

selectable¶ – optional Table that specifies an element of the FROM clause within an UPDATE or DELETE to be the subject of the hint - applies only to certain backends.

dialect_name¶ – defaults to *, if specified as the name of a particular dialect, will apply these hints only when that dialect is in use.

inherits from sqlalchemy.sql.expression.UpdateBase

Supplies support for ValuesBase.values() to INSERT and UPDATE constructs.

SELECT statement for INSERT .. FROM SELECT

Specify a fixed VALUES clause for an INSERT statement, or the SET clause for an UPDATE.

SELECT statement for INSERT .. FROM SELECT

Specify a fixed VALUES clause for an INSERT statement, or the SET clause for an UPDATE.

Note that the Insert and Update constructs support per-execution time formatting of the VALUES and/or SET clauses, based on the arguments passed to Connection.execute(). However, the ValuesBase.values() method can be used to “fix” a particular set of parameters into the statement.

Multiple calls to ValuesBase.values() will produce a new construct, each one with the parameter list modified to include the new parameters sent. In the typical case of a single dictionary of parameters, the newly passed keys will replace the same keys in the previous construct. In the case of a list-based “multiple values” construct, each new list of values is extended onto the existing list of values.

key value pairs representing the string key of a Column mapped to the value to be rendered into the VALUES or SET clause:

As an alternative to passing key/value parameters, a dictionary, tuple, or list of dictionaries or tuples can be passed as a single positional argument in order to form the VALUES or SET clause of the statement. The forms that are accepted vary based on whether this is an Insert or an Update construct.

For either an Insert or Update construct, a single dictionary can be passed, which works the same as that of the kwargs form:

Also for either form but more typically for the Insert construct, a tuple that contains an entry for every column in the table is also accepted:

The Insert construct also supports being passed a list of dictionaries or full-table-tuples, which on the server will render the less common SQL syntax of “multiple values” - this syntax is supported on backends such as SQLite, PostgreSQL, MySQL, but not necessarily others:

The above form would render a multiple VALUES statement similar to:

It is essential to note that passing multiple values is NOT the same as using traditional executemany() form. The above syntax is a special syntax not typically used. To emit an INSERT statement against multiple rows, the normal method is to pass a multiple values list to the Connection.execute() method, which is supported by all database backends and is generally more efficient for a very large number of parameters.

Sending Multiple Parameters - an introduction to the traditional Core method of multiple parameter set invocation for INSERTs and other statements.

The UPDATE construct also supports rendering the SET parameters in a specific order. For this feature refer to the Update.ordered_values() method.

Update.ordered_values()

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from sqlalchemy import delete

stmt = delete(user_table).where(user_table.c.id == 5)
```

Example 2 (python):
```python
from sqlalchemy import insert

stmt = insert(user_table).values(name="username", fullname="Full Username")
```

Example 3 (sql):
```sql
from sqlalchemy import update

stmt = (
    update(user_table).where(user_table.c.id == 5).values(name="user #5")
)
```

Example 4 (unknown):
```unknown
upd = table.update().dialect_options(mysql_limit=10)
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- ORM API Features for Querying¶
- ORM Loader Options¶
- ORM Execution Options¶
  - Populate Existing¶
  - Autoflush¶
  - Fetching Large Result Sets with Yield Per¶

Home | Download this Documentation

Home | Download this Documentation

This page is part of the ORM Querying Guide.

Previous: Relationship Loading Techniques | Next: Legacy Query API

Loader options are objects which, when passed to the Select.options() method of a Select object or similar SQL construct, affect the loading of both column and relationship-oriented attributes. The majority of loader options descend from the Load hierarchy. For a complete overview of using loader options, see the linked sections below.

Column Loading Options - details mapper and loading options that affect how column and SQL-expression mapped attributes are loaded

Relationship Loading Techniques - details relationship and loading options that affect how relationship() mapped attributes are loaded

ORM-level execution options are keyword options that may be associated with a statement execution using either the Session.execute.execution_options parameter, which is a dictionary argument accepted by Session methods such as Session.execute() and Session.scalars(), or by associating them directly with the statement to be invoked itself using the Executable.execution_options() method, which accepts them as arbitrary keyword arguments.

ORM-level options are distinct from the Core level execution options documented at Connection.execution_options(). It’s important to note that the ORM options discussed below are not compatible with Core level methods Connection.execution_options() or Engine.execution_options(); the options are ignored at this level, even if the Engine or Connection is associated with the Session in use.

Within this section, the Executable.execution_options() method style will be illustrated for examples.

The populate_existing execution option ensures that, for all rows loaded, the corresponding instances in the Session will be fully refreshed – erasing any existing data within the objects (including pending changes) and replacing with the data loaded from the result.

Example use looks like:

Normally, ORM objects are only loaded once, and if they are matched up to the primary key in a subsequent result row, the row is not applied to the object. This is both to preserve pending, unflushed changes on the object as well as to avoid the overhead and complexity of refreshing data which is already there. The Session assumes a default working model of a highly isolated transaction, and to the degree that data is expected to change within the transaction outside of the local changes being made, those use cases would be handled using explicit steps such as this method.

Using populate_existing, any set of objects that matches a query can be refreshed, and it also allows control over relationship loader options. E.g. to refresh an instance while also refreshing a related set of objects:

Another use case for populate_existing is in support of various attribute loading features that can change how an attribute is loaded on a per-query basis. Options for which this apply include:

The with_expression() option

The PropComparator.and_() method that can modify what a loader strategy loads

The contains_eager() option

The with_loader_criteria() option

The load_only() option to select what attributes to refresh

The populate_existing execution option is equvialent to the Query.populate_existing() method in 1.x style ORM queries.

I’m re-loading data with my Session but it isn’t seeing changes that I committed elsewhere - in Frequently Asked Questions

Refreshing / Expiring - in the ORM Session documentation

This option, when passed as False, will cause the Session to not invoke the “autoflush” step. It is equivalent to using the Session.no_autoflush context manager to disable autoflush:

This option will also work on ORM-enabled Update and Delete queries.

The autoflush execution option is equvialent to the Query.autoflush() method in 1.x style ORM queries.

The yield_per execution option is an integer value which will cause the Result to buffer only a limited number of rows and/or ORM objects at a time, before making data available to the client.

Normally, the ORM will fetch all rows immediately, constructing ORM objects for each and assembling those objects into a single buffer, before passing this buffer to the Result object as a source of rows to be returned. The rationale for this behavior is to allow correct behavior for features such as joined eager loading, uniquifying of results, and the general case of result handling logic that relies upon the identity map maintaining a consistent state for every object in a result set as it is fetched.

The purpose of the yield_per option is to change this behavior so that the ORM result set is optimized for iteration through very large result sets (e.g. > 10K rows), where the user has determined that the above patterns don’t apply. When yield_per is used, the ORM will instead batch ORM results into sub-collections and yield rows from each sub-collection individually as the Result object is iterated, so that the Python interpreter doesn’t need to declare very large areas of memory which is both time consuming and leads to excessive memory use. The option affects both the way the database cursor is used as well as how the ORM constructs rows and objects to be passed to the Result.

From the above, it follows that the Result must be consumed in an iterable fashion, that is, using iteration such as for row in result or using partial row methods such as Result.fetchmany() or Result.partitions(). Calling Result.all() will defeat the purpose of using yield_per.

Using yield_per is equivalent to making use of both the Connection.execution_options.stream_results execution option, which selects for server side cursors to be used by the backend if supported, and the Result.yield_per() method on the returned Result object, which establishes a fixed size of rows to be fetched as well as a corresponding limit to how many ORM objects will be constructed at once.

yield_per is now available as a Core execution option as well, described in detail at Using Server Side Cursors (a.k.a. stream results). This section details the use of yield_per as an execution option with an ORM Session. The option behaves as similarly as possible in both contexts.

When used with the ORM, yield_per must be established either via the Executable.execution_options() method on the given statement or by passing it to the Session.execute.execution_options parameter of Session.execute() or other similar Session method such as Session.scalars(). Typical use for fetching ORM objects is illustrated below:

The above code is equivalent to the example below, which uses Connection.execution_options.stream_results and Connection.execution_options.max_row_buffer Core-level execution options in conjunction with the Result.yield_per() method of Result:

yield_per is also commonly used in combination with the Result.partitions() method, which will iterate rows in grouped partitions. The size of each partition defaults to the integer value passed to yield_per, as in the below example:

The yield_per execution option is not compatible with “subquery” eager loading loading or “joined” eager loading when using collections. It is potentially compatible with “select in” eager loading , provided the database driver supports multiple, independent cursors.

Additionally, the yield_per execution option is not compatible with the Result.unique() method; as this method relies upon storing a complete set of identities for all rows, it would necessarily defeat the purpose of using yield_per which is to handle an arbitrarily large number of rows.

Changed in version 1.4.6: An exception is raised when ORM rows are fetched from a Result object that makes use of the Result.unique() filter, at the same time as the yield_per execution option is used.

When using the legacy Query object with 1.x style ORM use, the Query.yield_per() method will have the same result as that of the yield_per execution option.

Using Server Side Cursors (a.k.a. stream results)

This option is an advanced-use feature mostly intended to be used with the Horizontal Sharding extension. For typical cases of loading objects with identical primary keys from different “shards” or partitions, consider using individual Session objects per shard first.

The “identity token” is an arbitrary value that can be associated within the identity key of newly loaded objects. This element exists first and foremost to support extensions which perform per-row “sharding”, where objects may be loaded from any number of replicas of a particular database table that nonetheless have overlapping primary key values. The primary consumer of “identity token” is the Horizontal Sharding extension, which supplies a general framework for persisting objects among multiple “shards” of a particular database table.

The identity_token execution option may be used on a per-query basis to directly affect this token. Using it directly, one can populate a Session with multiple instances of an object that have the same primary key and source table, but different “identities”.

One such example is to populate a Session with objects that come from same-named tables in different schemas, using the Translation of Schema Names feature which can affect the choice of schema within the scope of queries. Given a mapping as:

The default “schema” name for the class above is None, meaning, no schema qualification will be written into SQL statements. However, if we make use of Connection.execution_options.schema_translate_map, mapping None to an alternate schema, we can place instances of MyTable into two different schemas:

The above two blocks create a Session object linked to a different schema translate map each time, and an instance of MyTable is persisted into both test_schema.my_table as well as test_schema_2.my_table.

The Session objects above are independent. If we wanted to persist both objects in one transaction, we would need to use the Horizontal Sharding extension to do this.

However, we can illustrate querying for these objects in one session as follows:

Both obj1 and obj2 are distinct from each other. However, they both refer to primary key id 1 for the MyTable class, yet are distinct. This is how the identity_token comes into play, which we can see in the inspection of each object, where we look at InstanceState.key to view the two distinct identity tokens:

The above logic takes place automatically when using the Horizontal Sharding extension.

Added in version 2.0.0rc1: - added the identity_token ORM level execution option.

Horizontal Sharding - in the ORM Examples section. See the script separate_schema_translates.py for a demonstration of the above use case using the full sharding API.

The select() construct, as well as the insert(), update() and delete() constructs (for the latter DML constructs, as of SQLAlchemy 1.4.33), all support the ability to inspect the entities in which these statements are created against, as well as the columns and datatypes that would be returned in a result set.

For a Select object, this information is available from the Select.column_descriptions attribute. This attribute operates in the same way as the legacy Query.column_descriptions attribute. The format returned is a list of dictionaries:

When Select.column_descriptions is used with non-ORM objects such as plain Table or Column objects, the entries will contain basic information about individual columns returned in all cases:

Changed in version 1.4.33: The Select.column_descriptions attribute now returns a value when used against a Select that is not ORM-enabled. Previously, this would raise NotImplementedError.

For insert(), update() and delete() constructs, there are two separate attributes. One is UpdateBase.entity_description which returns information about the primary ORM entity and database table which the DML construct would be affecting:

The UpdateBase.entity_description includes an entry "table" which is actually the table to be inserted, updated or deleted by the statement, which is not always the same as the SQL “selectable” to which the class may be mapped. For example, in a joined-table inheritance scenario, "table" will refer to the local table for the given entity.

The other is UpdateBase.returning_column_descriptions which delivers information about the columns present in the RETURNING collection in a manner roughly similar to that of Select.column_descriptions:

Added in version 1.4.33: Added the UpdateBase.entity_description and UpdateBase.returning_column_descriptions attributes.

aliased(element[, alias, name, flat, ...])

Produce an alias of the given element, usually an AliasedClass instance.

Represents an “aliased” form of a mapped class for usage with Query.

Provide an inspection interface for an AliasedClass object.

A grouping of SQL expressions that are returned by a Query under one namespace.

join(left, right[, onclause, isouter, ...])

Produce an inner join between left and right clauses.

outerjoin(left, right[, onclause, full])

Produce a left outer join between left and right clauses.

with_loader_criteria(entity_or_base, where_criteria[, loader_only, include_aliases, ...])

Add additional WHERE criteria to the load for all occurrences of a particular entity.

with_parent(instance, prop[, from_entity])

Create filtering criterion that relates this query’s primary entity to the given related instance, using established relationship() configuration.

Produce an alias of the given element, usually an AliasedClass instance.

The aliased() function is used to create an ad-hoc mapping of a mapped class to a new selectable. By default, a selectable is generated from the normally mapped selectable (typically a Table ) using the FromClause.alias() method. However, aliased() can also be used to link the class to a new select() statement. Also, the with_polymorphic() function is a variant of aliased() that is intended to specify a so-called “polymorphic selectable”, that corresponds to the union of several joined-inheritance subclasses at once.

For convenience, the aliased() function also accepts plain FromClause constructs, such as a Table or select() construct. In those cases, the FromClause.alias() method is called on the object and the new Alias object returned. The returned Alias is not ORM-mapped in this case.

ORM Entity Aliases - in the SQLAlchemy Unified Tutorial

Selecting ORM Aliases - in the ORM Querying Guide

element¶ – element to be aliased. Is normally a mapped class, but for convenience can also be a FromClause element.

alias¶ – Optional selectable unit to map the element to. This is usually used to link the object to a subquery, and should be an aliased select construct as one would produce from the Query.subquery() method or the Select.subquery() or Select.alias() methods of the select() construct.

name¶ – optional string name to use for the alias, if not specified by the alias parameter. The name, among other things, forms the attribute name that will be accessible via tuples returned by a Query object. Not supported when creating aliases of Join objects.

Boolean, will be passed through to the FromClause.alias() call so that aliases of Join objects will alias the individual tables inside the join, rather than creating a subquery. This is generally supported by all modern databases with regards to right-nested joins and generally produces more efficient queries.

When aliased.flat is combined with aliased.name, the resulting joins will alias individual tables using a naming scheme similar to <prefix>_<tablename>. This naming scheme is for visibility / debugging purposes only and the specific scheme is subject to change without notice.

Added in version 2.0.32: added support for combining aliased.name with aliased.flat. Previously, this would raise NotImplementedError.

if True, more liberal “matching” will be used when mapping the mapped columns of the ORM entity to those of the given selectable - a name-based match will be performed if the given selectable doesn’t otherwise have a column that corresponds to one on the entity. The use case for this is when associating an entity with some derived selectable such as one that uses aggregate functions:

Above, functions on aggregated_unit_price which refer to .price will return the func.sum(UnitPrice.price).label('price') column, as it is matched on the name “price”. Ordinarily, the “price” function wouldn’t have any “column correspondence” to the actual UnitPrice.price column as it is not a proxy of the original.

inherits from sqlalchemy.inspection.Inspectable, sqlalchemy.orm.ORMColumnsClauseRole

Represents an “aliased” form of a mapped class for usage with Query.

The ORM equivalent of a alias() construct, this object mimics the mapped class using a __getattr__ scheme and maintains a reference to a real Alias object.

A primary purpose of AliasedClass is to serve as an alternate within a SQL statement generated by the ORM, such that an existing mapped entity can be used in multiple contexts. A simple example:

AliasedClass is also capable of mapping an existing mapped class to an entirely new selectable, provided this selectable is column- compatible with the existing mapped selectable, and it can also be configured in a mapping as the target of a relationship(). See the links below for examples.

The AliasedClass object is constructed typically using the aliased() function. It also is produced with additional configuration when using the with_polymorphic() function.

The resulting object is an instance of AliasedClass. This object implements an attribute scheme which produces the same attribute and method interface as the original mapped class, allowing AliasedClass to be compatible with any attribute technique which works on the original class, including hybrid attributes (see Hybrid Attributes).

The AliasedClass can be inspected for its underlying Mapper, aliased selectable, and other information using inspect():

The resulting inspection object is an instance of AliasedInsp.

Relationship to Aliased Class

Row-Limited Relationships with Window Functions

inherits from sqlalchemy.orm.ORMEntityColumnsClauseRole, sqlalchemy.orm.ORMFromClauseRole, sqlalchemy.sql.cache_key.HasCacheKey, sqlalchemy.orm.base.InspectionAttr, sqlalchemy.util.langhelpers.MemoizedSlots, sqlalchemy.inspection.Inspectable, typing.Generic

Provide an inspection interface for an AliasedClass object.

The AliasedInsp object is returned given an AliasedClass using the inspect() function:

Attributes on AliasedInsp include:

entity - the AliasedClass represented.

mapper - the Mapper mapping the underlying class.

selectable - the Alias construct which ultimately represents an aliased Table or Select construct.

name - the name of the alias. Also is used as the attribute name when returned in a result tuple from Query.

with_polymorphic_mappers - collection of Mapper objects indicating all those mappers expressed in the select construct for the AliasedClass.

polymorphic_on - an alternate column or SQL expression which will be used as the “discriminator” for a polymorphic load.

Runtime Inspection API

inherits from sqlalchemy.orm.ORMColumnsClauseRole, sqlalchemy.sql.annotation.SupportsCloneAnnotations, sqlalchemy.sql.cache_key.MemoizedHasCacheKey, sqlalchemy.inspection.Inspectable, sqlalchemy.orm.base.InspectionAttr

A grouping of SQL expressions that are returned by a Query under one namespace.

The Bundle essentially allows nesting of the tuple-based results returned by a column-oriented Query object. It also is extensible via simple subclassing, where the primary capability to override is that of how the set of expressions should be returned, allowing post-processing as well as custom return types, without involving ORM identity-mapped classes.

Grouping Selected Attributes with Bundles

Construct a new Bundle.

An alias for Bundle.columns.

A namespace of SQL expressions referred to by this Bundle.

create_row_processor()

Produce the “row processing” function for this Bundle.

True if this object is an instance of AliasedClass.

True if this object is an instance of Bundle.

True if this object is an instance of ClauseElement.

True if this object is an instance of Mapper.

Provide a copy of this Bundle passing a new label.

If True, queries for a single Bundle will be returned as a single entity, rather than an element within a keyed tuple.

Construct a new Bundle.

name¶ – name of the bundle.

*exprs¶ – columns or SQL expressions comprising the bundle.

single_entity=False¶ – if True, rows for this Bundle can be returned as a “single entity” outside of any enclosing tuple in the same manner as a mapped entity.

An alias for Bundle.columns.

A namespace of SQL expressions referred to by this Bundle.

Nesting of bundles is also supported:

Produce the “row processing” function for this Bundle.

May be overridden by subclasses to provide custom behaviors when results are fetched. The method is passed the statement object and a set of “row processor” functions at query execution time; these processor functions when given a result row will return the individual attribute value, which can then be adapted into any kind of return data structure.

The example below illustrates replacing the usual Row return structure with a straight Python dictionary:

A result from the above Bundle will return dictionary values:

True if this object is an instance of AliasedClass.

True if this object is an instance of Bundle.

True if this object is an instance of ClauseElement.

True if this object is an instance of Mapper.

Provide a copy of this Bundle passing a new label.

If True, queries for a single Bundle will be returned as a single entity, rather than an element within a keyed tuple.

Add additional WHERE criteria to the load for all occurrences of a particular entity.

Added in version 1.4.

The with_loader_criteria() option is intended to add limiting criteria to a particular kind of entity in a query, globally, meaning it will apply to the entity as it appears in the SELECT query as well as within any subqueries, join conditions, and relationship loads, including both eager and lazy loaders, without the need for it to be specified in any particular part of the query. The rendering logic uses the same system used by single table inheritance to ensure a certain discriminator is applied to a table.

E.g., using 2.0-style queries, we can limit the way the User.addresses collection is loaded, regardless of the kind of loading used:

Above, the “selectinload” for User.addresses will apply the given filtering criteria to the WHERE clause.

Another example, where the filtering will be applied to the ON clause of the join, in this example using 1.x style queries:

The primary purpose of with_loader_criteria() is to use it in the SessionEvents.do_orm_execute() event handler to ensure that all occurrences of a particular entity are filtered in a certain way, such as filtering for access control roles. It also can be used to apply criteria to relationship loads. In the example below, we can apply a certain set of rules to all queries emitted by a particular Session:

In the above example, the SessionEvents.do_orm_execute() event will intercept all queries emitted using the Session. For those queries which are SELECT statements and are not attribute or relationship loads a custom with_loader_criteria() option is added to the query. The with_loader_criteria() option will be used in the given statement and will also be automatically propagated to all relationship loads that descend from this query.

The criteria argument given is a lambda that accepts a cls argument. The given class will expand to include all mapped subclass and need not itself be a mapped class.

When using with_loader_criteria() option in conjunction with the contains_eager() loader option, it’s important to note that with_loader_criteria() only affects the part of the query that determines what SQL is rendered in terms of the WHERE and FROM clauses. The contains_eager() option does not affect the rendering of the SELECT statement outside of the columns clause, so does not have any interaction with the with_loader_criteria() option. However, the way things “work” is that contains_eager() is meant to be used with a query that is already selecting from the additional entities in some way, where with_loader_criteria() can apply it’s additional criteria.

In the example below, assuming a mapping relationship as A -> A.bs -> B, the given with_loader_criteria() option will affect the way in which the JOIN is rendered:

Above, the given with_loader_criteria() option will affect the ON clause of the JOIN that is specified by .join(A.bs), so is applied as expected. The contains_eager() option has the effect that columns from B are added to the columns clause:

The use of the contains_eager() option within the above statement has no effect on the behavior of the with_loader_criteria() option. If the contains_eager() option were omitted, the SQL would be the same as regards the FROM and WHERE clauses, where with_loader_criteria() continues to add its criteria to the ON clause of the JOIN. The addition of contains_eager() only affects the columns clause, in that additional columns against b are added which are then consumed by the ORM to produce B instances.

The use of a lambda inside of the call to with_loader_criteria() is only invoked once per unique class. Custom functions should not be invoked within this lambda. See Using Lambdas to add significant speed gains to statement production for an overview of the “lambda SQL” feature, which is for advanced use only.

entity_or_base¶ – a mapped class, or a class that is a super class of a particular set of mapped classes, to which the rule will apply.

a Core SQL expression that applies limiting criteria. This may also be a “lambda:” or Python function that accepts a target class as an argument, when the given class is a base with many different mapped subclasses.

To support pickling, use a module-level Python function to produce the SQL expression instead of a lambda or a fixed SQL expression, which tend to not be picklable.

include_aliases¶ – if True, apply the rule to aliased() constructs as well.

propagate_to_loaders¶ –

defaults to True, apply to relationship loaders such as lazy loaders. This indicates that the option object itself including SQL expression is carried along with each loaded instance. Set to False to prevent the object from being assigned to individual instances.

ORM Query Events - includes examples of using with_loader_criteria().

Adding global WHERE / ON criteria - basic example on how to combine with_loader_criteria() with the SessionEvents.do_orm_execute() event.

track_closure_variables¶ –

when False, closure variables inside of a lambda expression will not be used as part of any cache key. This allows more complex expressions to be used inside of a lambda expression but requires that the lambda ensures it returns the identical SQL every time given a particular class.

Added in version 1.4.0b2.

Produce an inner join between left and right clauses.

join() is an extension to the core join interface provided by join(), where the left and right selectable may be not only core selectable objects such as Table, but also mapped classes or AliasedClass instances. The “on” clause can be a SQL expression or an ORM mapped attribute referencing a configured relationship().

join() is not commonly needed in modern usage, as its functionality is encapsulated within that of the Select.join() and Query.join() methods. which feature a significant amount of automation beyond join() by itself. Explicit use of join() with ORM-enabled SELECT statements involves use of the Select.select_from() method, as in:

In modern SQLAlchemy the above join can be written more succinctly as:

using join() directly may not work properly with modern ORM options such as with_loader_criteria(). It is strongly recommended to use the idiomatic join patterns provided by methods such as Select.join() and Select.join_from() when creating ORM joins.

Joins - in the ORM Querying Guide for background on idiomatic ORM join patterns

Produce a left outer join between left and right clauses.

This is the “outer join” version of the join() function, featuring the same behavior except that an OUTER JOIN is generated. See that function’s documentation for other usage details.

Create filtering criterion that relates this query’s primary entity to the given related instance, using established relationship() configuration.

The SQL rendered is the same as that rendered when a lazy loader would fire off from the given parent on that attribute, meaning that the appropriate state is taken from the parent object in Python without the need to render joins to the parent table in the rendered statement.

The given property may also make use of PropComparator.of_type() to indicate the left side of the criteria:

The above use is equivalent to using the from_entity() argument:

instance¶ – An instance which has some relationship().

property¶ – Class-bound attribute, which indicates what relationship from the instance should be used to reconcile the parent/child relationship.

Entity in which to consider as the left side. This defaults to the “zero” entity of the Query itself.

Added in version 1.2.

Next Query Guide Section: Legacy Query API

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (sql):
```sql
>>> stmt = select(User).execution_options(populate_existing=True)
>>> result = session.execute(stmt)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
...
```

Example 2 (markdown):
```markdown
stmt = (
    select(User)
    .where(User.name.in_(names))
    .execution_options(populate_existing=True)
    .options(selectinload(User.addresses))
)
# will refresh all matching User objects as well as the related
# Address objects
users = session.execute(stmt).scalars().all()
```

Example 3 (sql):
```sql
>>> stmt = select(User).execution_options(autoflush=False)
>>> session.execute(stmt)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
...
```

Example 4 (sql):
```sql
>>> stmt = select(User).execution_options(yield_per=10)
>>> for user_obj in session.scalars(stmt):
...     print(user_obj)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
[...] ()
User(id=1, name='spongebob', fullname='Spongebob Squarepants')
User(id=2, name='sandy', fullname='Sandy Cheeks')
...
>>> # ... rows continue ...
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- ORM Querying Guide¶

Home | Download this Documentation

Home | Download this Documentation

This section provides an overview of emitting queries with the SQLAlchemy ORM using 2.0 style usage.

Readers of this section should be familiar with the SQLAlchemy overview at SQLAlchemy Unified Tutorial, and in particular most of the content here expands upon the content at Using SELECT Statements.

For users of SQLAlchemy 1.x

In the SQLAlchemy 2.x series, SQL SELECT statements for the ORM are constructed using the same select() construct as is used in Core, which is then invoked in terms of a Session using the Session.execute() method (as are the update() and delete() constructs now used for the ORM-Enabled INSERT, UPDATE, and DELETE statements feature). However, the legacy Query object, which performs these same steps as more of an “all-in-one” object, continues to remain available as a thin facade over this new system, to support applications that were built on the 1.x series without the need for wholesale replacement of all queries. For reference on this object, see the section Legacy Query API.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

---
