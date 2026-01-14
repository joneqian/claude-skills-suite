# Sqlalchemy - Sql

**Pages:** 4

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/core/compiler.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Core
    - Project Versions
- Custom SQL Constructs and Compilation Extension¶
- Synopsis¶
- Dialect-specific compilation rules¶
- Compiling sub-elements of a custom expression construct¶
  - Cross Compiling between SQL and DDL compilers¶
- Changing the default compilation of existing constructs¶

Home | Download this Documentation

Home | Download this Documentation

Provides an API for creation of custom ClauseElements and compilers.

Usage involves the creation of one or more ClauseElement subclasses and one or more callables defining its compilation:

Above, MyColumn extends ColumnClause, the base expression element for named column objects. The compiles decorator registers itself with the MyColumn class so that it is invoked when the object is compiled to a string:

Compilers can also be made dialect-specific. The appropriate compiler will be invoked for the dialect in use:

The second visit_alter_table will be invoked when any postgresql dialect is used.

The compiler argument is the Compiled object in use. This object can be inspected for any information about the in-progress compilation, including compiler.dialect, compiler.statement etc. The SQLCompiler and DDLCompiler both include a process() method which can be used for compilation of embedded attributes:

Produces (formatted for readability):

The above InsertFromSelect construct is only an example, this actual functionality is already available using the Insert.from_select() method.

SQL and DDL constructs are each compiled using different base compilers - SQLCompiler and DDLCompiler. A common need is to access the compilation rules of SQL expressions from within a DDL expression. The DDLCompiler includes an accessor sql_compiler for this reason, such as below where we generate a CHECK constraint that embeds a SQL expression:

Above, we add an additional flag to the process step as called by SQLCompiler.process(), which is the literal_binds flag. This indicates that any SQL expression which refers to a BindParameter object or other “literal” object such as those which refer to strings or integers should be rendered in-place, rather than being referred to as a bound parameter; when emitting DDL, bound parameters are typically not supported.

The compiler extension applies just as well to the existing constructs. When overriding the compilation of a built in SQL construct, the @compiles decorator is invoked upon the appropriate class (be sure to use the class, i.e. Insert or Select, instead of the creation function such as insert() or select()).

Within the new compilation function, to get at the “original” compilation routine, use the appropriate visit_XXX method - this because compiler.process() will call upon the overriding routine and cause an endless loop. Such as, to add “prefix” to all insert statements:

The above compiler will prefix all INSERT statements with “some prefix” when compiled.

compiler works for types, too, such as below where we implement the MS-SQL specific ‘max’ keyword for String/VARCHAR:

A big part of using the compiler extension is subclassing SQLAlchemy expression constructs. To make this easier, the expression and schema packages feature a set of “bases” intended for common tasks. A synopsis is as follows:

ClauseElement - This is the root expression class. Any SQL expression can be derived from this base, and is probably the best choice for longer constructs such as specialized INSERT statements.

ColumnElement - The root of all “column-like” elements. Anything that you’d place in the “columns” clause of a SELECT statement (as well as order by and group by) can derive from this - the object will automatically have Python “comparison” behavior.

ColumnElement classes want to have a type member which is expression’s return type. This can be established at the instance level in the constructor, or at the class level if its generally constant:

FunctionElement - This is a hybrid of a ColumnElement and a “from clause” like object, and represents a SQL function or stored procedure type of call. Since most databases support statements along the line of “SELECT FROM <some function>” FunctionElement adds in the ability to be used in the FROM clause of a select() construct:

ExecutableDDLElement - The root of all DDL expressions, like CREATE TABLE, ALTER TABLE, etc. Compilation of ExecutableDDLElement subclasses is issued by a DDLCompiler instead of a SQLCompiler. ExecutableDDLElement can also be used as an event hook in conjunction with event hooks like DDLEvents.before_create() and DDLEvents.after_create(), allowing the construct to be invoked automatically during CREATE TABLE and DROP TABLE sequences.

Customizing DDL - contains examples of associating DDL objects (which are themselves ExecutableDDLElement instances) with DDLEvents event hooks.

Executable - This is a mixin which should be used with any expression class that represents a “standalone” SQL statement that can be passed directly to an execute() method. It is already implicit within DDLElement and FunctionElement.

Most of the above constructs also respond to SQL statement caching. A subclassed construct will want to define the caching behavior for the object, which usually means setting the flag inherit_cache to the value of False or True. See the next section Enabling Caching Support for Custom Constructs for background.

SQLAlchemy as of version 1.4 includes a SQL compilation caching facility which will allow equivalent SQL constructs to cache their stringified form, along with other structural information used to fetch results from the statement.

For reasons discussed at Object will not produce a cache key, Performance Implications, the implementation of this caching system takes a conservative approach towards including custom SQL constructs and/or subclasses within the caching system. This includes that any user-defined SQL constructs, including all the examples for this extension, will not participate in caching by default unless they positively assert that they are able to do so. The HasCacheKey.inherit_cache attribute when set to True at the class level of a specific subclass will indicate that instances of this class may be safely cached, using the cache key generation scheme of the immediate superclass. This applies for example to the “synopsis” example indicated previously:

Above, the MyColumn class does not include any new state that affects its SQL compilation; the cache key of MyColumn instances will make use of that of the ColumnClause superclass, meaning it will take into account the class of the object (MyColumn), the string name and datatype of the object:

For objects that are likely to be used liberally as components within many larger statements, such as Column subclasses and custom SQL datatypes, it’s important that caching be enabled as much as possible, as this may otherwise negatively affect performance.

An example of an object that does contain state which affects its SQL compilation is the one illustrated at Compiling sub-elements of a custom expression construct; this is an “INSERT FROM SELECT” construct that combines together a Table as well as a Select construct, each of which independently affect the SQL string generation of the construct. For this class, the example illustrates that it simply does not participate in caching:

While it is also possible that the above InsertFromSelect could be made to produce a cache key that is composed of that of the Table and Select components together, the API for this is not at the moment fully public. However, for an “INSERT FROM SELECT” construct, which is only used by itself for specific operations, caching is not as critical as in the previous example.

For objects that are used in relative isolation and are generally standalone, such as custom DML constructs like an “INSERT FROM SELECT”, caching is generally less critical as the lack of caching for such a construct will have only localized implications for that specific operation.

A function that works like “CURRENT_TIMESTAMP” except applies the appropriate conversions so that the time is in UTC time. Timestamps are best stored in relational databases as UTC, without time zones. UTC so that your database doesn’t think time has gone backwards in the hour when daylight savings ends, without timezones because timezones are like character encodings - they’re best applied only at the endpoints of an application (i.e. convert to UTC upon user input, re-apply desired timezone upon display).

For PostgreSQL and Microsoft SQL Server:

The “GREATEST” function is given any number of arguments and returns the one that is of the highest value - its equivalent to Python’s max function. A SQL standard version versus a CASE based version which only accommodates two arguments:

Render a “false” constant expression, rendering as “0” on platforms that don’t have a “false” constant:

compiles(class_, *specs)

Register a function as a compiler for a given ClauseElement type.

Remove all custom compilers associated with a given ClauseElement type.

Register a function as a compiler for a given ClauseElement type.

Remove all custom compilers associated with a given ClauseElement type.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import ColumnClause


class MyColumn(ColumnClause):
    inherit_cache = True


@compiles(MyColumn)
def compile_mycolumn(element, compiler, **kw):
    return "[%s]" % element.name
```

Example 2 (sql):
```sql
from sqlalchemy import select

s = select(MyColumn("x"), MyColumn("y"))
print(str(s))
```

Example 3 (sql):
```sql
SELECT [x], [y]
```

Example 4 (python):
```python
from sqlalchemy.schema import DDLElement


class AlterColumn(DDLElement):
    inherit_cache = False

    def __init__(self, column, cmd):
        self.column = column
        self.cmd = cmd


@compiles(AlterColumn)
def visit_alter_column(element, compiler, **kw):
    return "ALTER COLUMN %s ..." % element.column.name


@compiles(AlterColumn, "postgresql")
def visit_alter_column(element, compiler, **kw):
    return "ALTER TABLE %s ALTER COLUMN %s ..." % (
        element.table.name,
        element.column.name,
    )
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/core/functions.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Core
    - Project Versions
- SQL and Generic Functions¶
- Function API¶
- Selected “Known” Functions¶

Home | Download this Documentation

Home | Download this Documentation

SQL functions are invoked by using the func namespace. See the tutorial at Working with SQL Functions for background on how to use the func object to render SQL functions in statements.

Working with SQL Functions - in the SQLAlchemy Unified Tutorial

The base API for SQL functions, which provides for the func namespace as well as classes that may be used for extensibility.

Define a function in “ansi” format, which doesn’t render parenthesis.

Describe a named SQL function.

Base for SQL function-oriented constructs.

Define a ‘generic’ function.

register_function(identifier, fn[, package])

Associate a callable with a particular func. name.

inherits from sqlalchemy.sql.functions.GenericFunction

Define a function in “ansi” format, which doesn’t render parenthesis.

inherits from sqlalchemy.sql.functions.FunctionElement

Describe a named SQL function.

The Function object is typically generated from the func generation object.

*clauses¶ – list of column expressions that form the arguments of the SQL function call.

type_¶ – optional TypeEngine datatype object that will be used as the return value of the column expression generated by this function call.

a string which indicates package prefix names to be prepended to the function name when the SQL is generated. The func generator creates these when it is called using dotted format, e.g.:

Working with SQL Functions - in the SQLAlchemy Unified Tutorial

func - namespace which produces registered or ad-hoc Function instances.

GenericFunction - allows creation of registered function types.

Construct a Function.

Construct a Function.

The func construct is normally used to construct new Function instances.

inherits from sqlalchemy.sql.expression.Executable, sqlalchemy.sql.expression.ColumnElement, sqlalchemy.sql.expression.FromClause, sqlalchemy.sql.expression.Generative

Base for SQL function-oriented constructs.

This is a generic type, meaning that type checkers and IDEs can be instructed on the types to expect in a Result for this function. See GenericFunction for an example of how this is done.

Working with SQL Functions - in the SQLAlchemy Unified Tutorial

Function - named SQL function.

func - namespace which produces registered or ad-hoc Function instances.

GenericFunction - allows creation of registered function types.

Construct a FunctionElement.

Produce a Alias construct against this FunctionElement.

Interpret this expression as a boolean comparison between two values.

synonym for FunctionElement.columns.

Return the underlying ClauseList which contains the arguments for this FunctionElement.

Return this FunctionElement as a column expression that selects from itself as a FROM clause.

The set of columns exported by this FunctionElement.

Produce a FILTER clause against this function.

Produce an OVER clause against this function.

scalar_table_valued()

Return a column expression that’s against this FunctionElement as a scalar table-valued expression.

Produce a select() construct against this FunctionElement.

Apply a ‘grouping’ to this ClauseElement.

Return a TableValuedAlias representation of this FunctionElement with table-valued expressions added.

Produce a WITHIN GROUP (ORDER BY expr) clause against this function.

For types that define their return type as based on the criteria within a WITHIN GROUP (ORDER BY) expression, called by the WithinGroup construct.

Construct a FunctionElement.

*clauses¶ – list of column expressions that form the arguments of the SQL function call.

**kwargs¶ – additional kwargs are typically consumed by subclasses.

Produce a Alias construct against this FunctionElement.

The FunctionElement.alias() method is part of the mechanism by which “table valued” SQL functions are created. However, most use cases are covered by higher level methods on FunctionElement including FunctionElement.table_valued(), and FunctionElement.column_valued().

This construct wraps the function in a named alias which is suitable for the FROM clause, in the style accepted for example by PostgreSQL. A column expression is also provided using the special .column attribute, which may be used to refer to the output of the function as a scalar value in the columns or where clause, for a backend such as PostgreSQL.

For a full table-valued expression, use the FunctionElement.table_valued() method first to establish named columns.

The FunctionElement.column_valued() method provides a shortcut for the above pattern:

Added in version 1.4.0b2: Added the .column accessor

name¶ – alias name, will be rendered as AS <name> in the FROM clause

when True, the table valued function may be used in the FROM clause without any explicit JOIN to other tables in the SQL query, and no “cartesian product” warning will be generated. May be useful for SQL functions such as func.json_each().

Added in version 1.4.33.

Table-Valued Functions - in the SQLAlchemy Unified Tutorial

FunctionElement.table_valued()

FunctionElement.scalar_table_valued()

FunctionElement.column_valued()

Interpret this expression as a boolean comparison between two values.

This method is used for an ORM use case described at Custom operators based on SQL functions.

A hypothetical SQL function “is_equal()” which compares to values for equality would be written in the Core expression language as:

If “is_equal()” above is comparing “a” and “b” for equality, the FunctionElement.as_comparison() method would be invoked as:

Where above, the integer value “1” refers to the first argument of the “is_equal()” function and the integer value “2” refers to the second.

This would create a BinaryExpression that is equivalent to:

However, at the SQL level it would still render as “is_equal(‘a’, ‘b’)”.

The ORM, when it loads a related object or collection, needs to be able to manipulate the “left” and “right” sides of the ON clause of a JOIN expression. The purpose of this method is to provide a SQL function construct that can also supply this information to the ORM, when used with the relationship.primaryjoin parameter. The return value is a containment object called FunctionAsBinary.

An ORM example is as follows:

Above, the “Venue” class can load descendant “Venue” objects by determining if the name of the parent Venue is contained within the start of the hypothetical descendant value’s name, e.g. “parent1” would match up to “parent1/child1”, but not to “parent2/child1”.

Possible use cases include the “materialized path” example given above, as well as making use of special SQL functions such as geometric functions to create join conditions.

left_index¶ – the integer 1-based index of the function argument that serves as the “left” side of the expression.

right_index¶ – the integer 1-based index of the function argument that serves as the “right” side of the expression.

Added in version 1.3.

Custom operators based on SQL functions - example use within the ORM

synonym for FunctionElement.columns.

Return the underlying ClauseList which contains the arguments for this FunctionElement.

Return this FunctionElement as a column expression that selects from itself as a FROM clause.

This is shorthand for:

name¶ – optional name to assign to the alias name that’s generated. If omitted, a unique anonymizing name is used.

when True, the “table” portion of the column valued function may be a member of the FROM clause without any explicit JOIN to other tables in the SQL query, and no “cartesian product” warning will be generated. May be useful for SQL functions such as func.json_array_elements().

Added in version 1.4.46.

Column Valued Functions - Table Valued Function as a Scalar Column - in the SQLAlchemy Unified Tutorial

Column Valued Functions - in the PostgreSQL documentation

FunctionElement.table_valued()

The set of columns exported by this FunctionElement.

This is a placeholder collection that allows the function to be placed in the FROM clause of a statement:

The above form is a legacy feature that is now superseded by the fully capable FunctionElement.table_valued() method; see that method for details.

FunctionElement.table_valued() - generates table-valued SQL function expressions.

overrides FromClause.entity_namespace as functions are generally column expressions and not FromClauses.

A ColumnCollection that represents the “exported” columns of this Selectable.

The “exported” columns for a FromClause object are synonymous with the FromClause.columns collection.

Added in version 1.4.

Selectable.exported_columns

SelectBase.exported_columns

Produce a FILTER clause against this function.

Used against aggregate and window functions, for database backends that support the “FILTER” clause.

Special Modifiers WITHIN GROUP, FILTER - in the SQLAlchemy Unified Tutorial

Produce an OVER clause against this function.

Used against aggregate or so-called “window” functions, for database backends that support window functions.

See over() for a full description.

Using Window Functions - in the SQLAlchemy Unified Tutorial

Return a column expression that’s against this FunctionElement as a scalar table-valued expression.

The returned expression is similar to that returned by a single column accessed off of a FunctionElement.table_valued() construct, except no FROM clause is generated; the function is rendered in the similar way as a scalar subquery.

Added in version 1.4.0b2.

FunctionElement.table_valued()

FunctionElement.alias()

FunctionElement.column_valued()

Produce a select() construct against this FunctionElement.

This is shorthand for:

Apply a ‘grouping’ to this ClauseElement.

This method is overridden by subclasses to return a “grouping” construct, i.e. parenthesis. In particular it’s used by “binary” expressions to provide a grouping around themselves when placed into a larger expression, as well as by select() constructs when placed into the FROM clause of another select(). (Note that subqueries should be normally created using the Select.alias() method, as many platforms require nested SELECT statements to be named).

As expressions are composed together, the application of self_group() is automatic - end-user code should never need to use this method directly. Note that SQLAlchemy’s clause constructs take operator precedence into account - so parenthesis might not be needed, for example, in an expression like x OR (y AND z) - AND takes precedence over OR.

The base self_group() method of ClauseElement just returns self.

Return a TableValuedAlias representation of this FunctionElement with table-valued expressions added.

A WITH ORDINALITY expression may be generated by passing the keyword argument “with_ordinality”:

*expr¶ – A series of string column names that will be added to the .c collection of the resulting TableValuedAlias construct as columns. column() objects with or without datatypes may also be used.

name¶ – optional name to assign to the alias name that’s generated. If omitted, a unique anonymizing name is used.

with_ordinality¶ – string name that when present results in the WITH ORDINALITY clause being added to the alias, and the given string name will be added as a column to the .c collection of the resulting TableValuedAlias.

when True, the table valued function may be used in the FROM clause without any explicit JOIN to other tables in the SQL query, and no “cartesian product” warning will be generated. May be useful for SQL functions such as func.json_each().

Added in version 1.4.33.

Added in version 1.4.0b2.

Table-Valued Functions - in the SQLAlchemy Unified Tutorial

Table-Valued Functions - in the PostgreSQL documentation

FunctionElement.scalar_table_valued() - variant of FunctionElement.table_valued() which delivers the complete table valued expression as a scalar column expression

FunctionElement.column_valued()

TableValuedAlias.render_derived() - renders the alias using a derived column clause, e.g. AS name(col1, col2, ...)

Produce a WITHIN GROUP (ORDER BY expr) clause against this function.

Used against so-called “ordered set aggregate” and “hypothetical set aggregate” functions, including percentile_cont, rank, dense_rank, etc.

See within_group() for a full description.

Special Modifiers WITHIN GROUP, FILTER - in the SQLAlchemy Unified Tutorial

For types that define their return type as based on the criteria within a WITHIN GROUP (ORDER BY) expression, called by the WithinGroup construct.

Returns None by default, in which case the function’s normal .type is used.

inherits from sqlalchemy.sql.functions.Function

Define a ‘generic’ function.

A generic function is a pre-established Function class that is instantiated automatically when called by name from the func attribute. Note that calling any name from func has the effect that a new Function instance is created automatically, given that name. The primary use case for defining a GenericFunction class is so that a function of a particular name may be given a fixed return type. It can also include custom argument parsing schemes as well as additional methods.

Subclasses of GenericFunction are automatically registered under the name of the class. For example, a user-defined function as_utc() would be available immediately:

User-defined generic functions can be organized into packages by specifying the “package” attribute when defining GenericFunction. Third party libraries containing many functions may want to use this in order to avoid name conflicts with other systems. For example, if our as_utc() function were part of a package “time”:

The above function would be available from func using the package name time:

A final option is to allow the function to be accessed from one name in func but to render as a different name. The identifier attribute will override the name used to access the function as loaded from func, but will retain the usage of name as the rendered name:

The above function will render as follows:

The name will be rendered as is, however without quoting unless the name contains special characters that require quoting. To force quoting on or off for the name, use the quoted_name construct:

The above function will render as:

Type parameters for this class as a generic type can be passed and should match the type seen in a Result. For example:

The above indicates that the following expression returns a datetime object:

Added in version 1.3.13: The quoted_name construct is now recognized for quoting when used with the “name” attribute of the object, so that quoting can be forced on or off for the function name.

Associate a callable with a particular func. name.

This is normally called by GenericFunction, but is also available by itself so that a non-Function construct can be associated with the func accessor (i.e. CAST, EXTRACT).

These are GenericFunction implementations for a selected set of common SQL functions that set up the expected return type for each function automatically. The are invoked in the same way as any other member of the func namespace:

Note that any name not known to func generates the function name as is - there is no restriction on what SQL functions can be called, known or unknown to SQLAlchemy, built-in or user defined. The section here only describes those functions where SQLAlchemy already knows what argument and return types are in use.

Implement a generic string aggregation function.

Support for the ARRAY_AGG function.

The CHAR_LENGTH() SQL function.

The SQL CONCAT() function, which concatenates strings.

The ANSI COUNT aggregate function. With no arguments, emits COUNT *.

Implement the CUBE grouping operation.

Implement the cume_dist hypothetical-set aggregate function.

The CURRENT_DATE() SQL function.

The CURRENT_TIME() SQL function.

The CURRENT_TIMESTAMP() SQL function.

The CURRENT_USER() SQL function.

Implement the dense_rank hypothetical-set aggregate function.

Implement the GROUPING SETS grouping operation.

The localtime() SQL function.

The localtimestamp() SQL function.

The SQL MAX() aggregate function.

The SQL MIN() aggregate function.

Implement the mode ordered-set aggregate function.

Represent the ‘next value’, given a Sequence as its single argument.

The SQL now() datetime function.

Implement the percent_rank hypothetical-set aggregate function.

Implement the percentile_cont ordered-set aggregate function.

Implement the percentile_disc ordered-set aggregate function.

The RANDOM() SQL function.

Implement the rank hypothetical-set aggregate function.

Implement the ROLLUP grouping operation.

The SESSION_USER() SQL function.

The SQL SUM() aggregate function.

The SYSDATE() SQL function.

The USER() SQL function.

inherits from sqlalchemy.sql.functions.GenericFunction

Implement a generic string aggregation function.

This function will concatenate non-null values into a string and separate the values by a delimiter.

This function is compiled on a per-backend basis, into functions such as group_concat(), string_agg(), or LISTAGG().

e.g. Example usage with delimiter ‘.’:

The return type of this function is String.

inherits from sqlalchemy.sql.functions.ReturnTypeFromArgs

Support for the ARRAY_AGG function.

The func.array_agg(expr) construct returns an expression of type ARRAY.

array_agg() - PostgreSQL-specific version that returns ARRAY, which has PG-specific operators added.

inherits from sqlalchemy.sql.functions.GenericFunction

The CHAR_LENGTH() SQL function.

inherits from sqlalchemy.sql.functions.ReturnTypeFromOptionalArgs

inherits from sqlalchemy.sql.functions.GenericFunction

The SQL CONCAT() function, which concatenates strings.

String concatenation in SQLAlchemy is more commonly available using the Python + operator with string datatypes, which will render a backend-specific concatenation operator, such as :

inherits from sqlalchemy.sql.functions.GenericFunction

The ANSI COUNT aggregate function. With no arguments, emits COUNT *.

Executing stmt would emit:

inherits from sqlalchemy.sql.functions.GenericFunction

Implement the CUBE grouping operation.

This function is used as part of the GROUP BY of a statement, e.g. Select.group_by():

Added in version 1.2.

inherits from sqlalchemy.sql.functions.GenericFunction

Implement the cume_dist hypothetical-set aggregate function.

This function must be used with the FunctionElement.within_group() modifier to supply a sort expression to operate upon.

The return type of this function is Numeric.

inherits from sqlalchemy.sql.functions.AnsiFunction

The CURRENT_DATE() SQL function.

inherits from sqlalchemy.sql.functions.AnsiFunction

The CURRENT_TIME() SQL function.

inherits from sqlalchemy.sql.functions.AnsiFunction

The CURRENT_TIMESTAMP() SQL function.

inherits from sqlalchemy.sql.functions.AnsiFunction

The CURRENT_USER() SQL function.

inherits from sqlalchemy.sql.functions.GenericFunction

Implement the dense_rank hypothetical-set aggregate function.

This function must be used with the FunctionElement.within_group() modifier to supply a sort expression to operate upon.

The return type of this function is Integer.

inherits from sqlalchemy.sql.functions.GenericFunction

Implement the GROUPING SETS grouping operation.

This function is used as part of the GROUP BY of a statement, e.g. Select.group_by():

In order to group by multiple sets, use the tuple_() construct:

Added in version 1.2.

inherits from sqlalchemy.sql.functions.AnsiFunction

The localtime() SQL function.

inherits from sqlalchemy.sql.functions.AnsiFunction

The localtimestamp() SQL function.

inherits from sqlalchemy.sql.functions.ReturnTypeFromArgs

The SQL MAX() aggregate function.

inherits from sqlalchemy.sql.functions.ReturnTypeFromArgs

The SQL MIN() aggregate function.

inherits from sqlalchemy.sql.functions.OrderedSetAgg

Implement the mode ordered-set aggregate function.

This function must be used with the FunctionElement.within_group() modifier to supply a sort expression to operate upon.

The return type of this function is the same as the sort expression.

inherits from sqlalchemy.sql.functions.GenericFunction

Represent the ‘next value’, given a Sequence as its single argument.

Compiles into the appropriate function on each backend, or will raise NotImplementedError if used on a backend that does not provide support for sequences.

inherits from sqlalchemy.sql.functions.GenericFunction

The SQL now() datetime function.

SQLAlchemy dialects will usually render this particular function in a backend-specific way, such as rendering it as CURRENT_TIMESTAMP.

inherits from sqlalchemy.sql.functions.GenericFunction

Implement the percent_rank hypothetical-set aggregate function.

This function must be used with the FunctionElement.within_group() modifier to supply a sort expression to operate upon.

The return type of this function is Numeric.

inherits from sqlalchemy.sql.functions.OrderedSetAgg

Implement the percentile_cont ordered-set aggregate function.

This function must be used with the FunctionElement.within_group() modifier to supply a sort expression to operate upon.

The return type of this function is the same as the sort expression, or if the arguments are an array, an ARRAY of the sort expression’s type.

inherits from sqlalchemy.sql.functions.OrderedSetAgg

Implement the percentile_disc ordered-set aggregate function.

This function must be used with the FunctionElement.within_group() modifier to supply a sort expression to operate upon.

The return type of this function is the same as the sort expression, or if the arguments are an array, an ARRAY of the sort expression’s type.

inherits from sqlalchemy.sql.functions.GenericFunction

The RANDOM() SQL function.

inherits from sqlalchemy.sql.functions.GenericFunction

Implement the rank hypothetical-set aggregate function.

This function must be used with the FunctionElement.within_group() modifier to supply a sort expression to operate upon.

The return type of this function is Integer.

inherits from sqlalchemy.sql.functions.GenericFunction

Implement the ROLLUP grouping operation.

This function is used as part of the GROUP BY of a statement, e.g. Select.group_by():

Added in version 1.2.

inherits from sqlalchemy.sql.functions.AnsiFunction

The SESSION_USER() SQL function.

inherits from sqlalchemy.sql.functions.ReturnTypeFromArgs

The SQL SUM() aggregate function.

inherits from sqlalchemy.sql.functions.AnsiFunction

The SYSDATE() SQL function.

inherits from sqlalchemy.sql.functions.AnsiFunction

The USER() SQL function.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (unknown):
```unknown
func.mypackage.some_function(col1, col2)
```

Example 2 (sql):
```sql
>>> from sqlalchemy import func, select, column
>>> data_view = func.unnest([1, 2, 3]).alias("data_view")
>>> print(select(data_view.column))
SELECT data_view
FROM unnest(:unnest_1) AS data_view
```

Example 3 (sql):
```sql
>>> data_view = func.unnest([1, 2, 3]).column_valued("data_view")
>>> print(select(data_view))
SELECT data_view
FROM unnest(:unnest_1) AS data_view
```

Example 4 (unknown):
```unknown
expr = func.is_equal("a", "b")
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/core/operators.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Core
    - Project Versions
- Operator Reference¶
- Comparison Operators¶
- IN Comparisons¶
  - IN against a list of values¶
  - Empty IN Expressions¶
  - NOT IN¶

Home | Download this Documentation

Home | Download this Documentation

This section details usage of the operators that are available to construct SQL expressions.

These methods are presented in terms of the Operators and ColumnOperators base classes. The methods are then available on descendants of these classes, including:

ColumnElement objects more generally, which are the root of all Core SQL Expression language column-level expressions

InstrumentedAttribute objects, which are ORM level mapped attributes.

The operators are first introduced in the tutorial sections, including:

SQLAlchemy Unified Tutorial - unified tutorial in 2.0 style

Object Relational Tutorial - ORM tutorial in 1.x style

SQL Expression Language Tutorial - Core tutorial in 1.x style

Basic comparisons which apply to many datatypes, including numerics, strings, dates, and many others:

ColumnOperators.__eq__() (Python “==” operator):

ColumnOperators.__ne__() (Python “!=” operator):

ColumnOperators.__gt__() (Python “>” operator):

ColumnOperators.__lt__() (Python “<” operator):

ColumnOperators.__ge__() (Python “>=” operator):

ColumnOperators.__le__() (Python “<=” operator):

ColumnOperators.between():

The SQL IN operator is a subject all its own in SQLAlchemy. As the IN operator is usually used against a list of fixed values, SQLAlchemy’s feature of bound parameter coercion makes use of a special form of SQL compilation that renders an interim SQL string for compilation that’s formed into the final list of bound parameters in a second step. In other words, “it just works”.

IN is available most typically by passing a list of values to the ColumnOperators.in_() method:

The special bound form __[POSTCOMPILE is rendered into individual parameters at execution time, illustrated below:

SQLAlchemy produces a mathematically valid result for an empty IN expression by rendering a backend-specific subquery that returns no rows. Again in other words, “it just works”:

The “empty set” subquery above generalizes correctly and is also rendered in terms of the IN operator which remains in place.

“NOT IN” is available via the ColumnOperators.not_in() operator:

This is typically more easily available by negating with the ~ operator:

Comparison of tuples to tuples is common with IN, as among other use cases accommodates for the case when matching rows to a set of potential composite primary key values. The tuple_() construct provides the basic building block for tuple comparisons. The Tuple.in_() operator then receives a list of tuples:

To illustrate the parameters rendered:

Finally, the ColumnOperators.in_() and ColumnOperators.not_in() operators work with subqueries. The form provides that a Select construct is passed in directly, without any explicit conversion to a named subquery:

Tuples work as expected:

These operators involve testing for special SQL values such as NULL, boolean constants such as true or false which some databases support:

ColumnOperators.is_():

This operator will provide exactly the SQL for “x IS y”, most often seen as “<expr> IS NULL”. The NULL constant is most easily acquired using regular Python None:

SQL NULL is also explicitly available, if needed, using the null() construct:

The ColumnOperators.is_() operator is automatically invoked when using the ColumnOperators.__eq__() overloaded operator, i.e. ==, in conjunction with the None or null() value. In this way, there’s typically not a need to use ColumnOperators.is_() explicitly, particularly when used with a dynamic value:

Note that the Python is operator is not overloaded. Even though Python provides hooks to overload operators such as == and !=, it does not provide any way to redefine is.

ColumnOperators.is_not():

Similar to ColumnOperators.is_(), produces “IS NOT”:

Is similarly equivalent to != None:

ColumnOperators.is_distinct_from():

Produces SQL IS DISTINCT FROM:

ColumnOperators.isnot_distinct_from():

Produces SQL IS NOT DISTINCT FROM:

ColumnOperators.like():

ColumnOperators.ilike():

Case insensitive LIKE makes use of the SQL lower() function on a generic backend. On the PostgreSQL backend it will use ILIKE:

ColumnOperators.notlike():

ColumnOperators.notilike():

String containment operators are basically built as a combination of LIKE and the string concatenation operator, which is || on most backends or sometimes a function like concat():

ColumnOperators.startswith():

ColumnOperators.endswith():

ColumnOperators.contains():

Matching operators are always backend-specific and may provide different behaviors and results on different databases:

ColumnOperators.match():

This is a dialect-specific operator that makes use of the MATCH feature of the underlying database, if available:

ColumnOperators.regexp_match():

This operator is dialect specific. We can illustrate it in terms of for example the PostgreSQL dialect:

ColumnOperators.concat():

String concatenation:

This operator is available via ColumnOperators.__add__(), that is, the Python + operator, when working with a column expression that derives from String:

The operator will produce the appropriate database-specific construct, such as on MySQL it’s historically been the concat() SQL function:

ColumnOperators.regexp_replace():

Complementary to ColumnOperators.regexp() this produces REGEXP REPLACE equivalent for the backends which support it:

ColumnOperators.collate():

Produces the COLLATE SQL operator which provides for specific collations at expression time:

To use COLLATE against a literal value, use the literal() construct:

ColumnOperators.__add__(), ColumnOperators.__radd__() (Python “+” operator):

Note that when the datatype of the expression is String or similar, the ColumnOperators.__add__() operator instead produces string concatenation.

ColumnOperators.__sub__(), ColumnOperators.__rsub__() (Python “-” operator):

ColumnOperators.__mul__(), ColumnOperators.__rmul__() (Python “*” operator):

ColumnOperators.__truediv__(), ColumnOperators.__rtruediv__() (Python “/” operator). This is the Python truediv operator, which will ensure integer true division occurs:

Changed in version 2.0: The Python / operator now ensures integer true division takes place

ColumnOperators.__floordiv__(), ColumnOperators.__rfloordiv__() (Python “//” operator). This is the Python floordiv operator, which will ensure floor division occurs. For the default backend as well as backends such as PostgreSQL, the SQL / operator normally behaves this way for integer values:

For backends that don’t use floor division by default, or when used with numeric values, the FLOOR() function is used to ensure floor division:

Added in version 2.0: Support for FLOOR division

ColumnOperators.__mod__(), ColumnOperators.__rmod__() (Python “%” operator):

Bitwise operator functions provide uniform access to bitwise operators across different backends, which are expected to operate on compatible values such as integers and bit-strings (e.g. PostgreSQL BIT and similar). Note that these are not general boolean operators.

Added in version 2.0.2: Added dedicated operators for bitwise operations.

ColumnOperators.bitwise_not(), bitwise_not(). Available as a column-level method, producing a bitwise NOT clause against a parent object:

This operator is also available as a column-expression-level method, applying bitwise NOT to an individual column expression:

ColumnOperators.bitwise_and() produces bitwise AND:

ColumnOperators.bitwise_or() produces bitwise OR:

ColumnOperators.bitwise_xor() produces bitwise XOR:

For PostgreSQL dialects, “#” is used to represent bitwise XOR; this emits automatically when using one of these backends:

ColumnOperators.bitwise_rshift(), ColumnOperators.bitwise_lshift() produce bitwise shift operators:

The most common conjunction, “AND”, is automatically applied if we make repeated use of the Select.where() method, as well as similar methods such as Update.where() and Delete.where():

Select.where(), Update.where() and Delete.where() also accept multiple expressions with the same effect:

The “AND” conjunction, as well as its partner “OR”, are both available directly using the and_() and or_() functions:

A negation is available using the not_() function. This will typically invert the operator in a boolean expression:

It also may apply a keyword such as NOT when appropriate:

The above conjunction functions and_(), or_(), not_() are also available as overloaded Python operators:

The Python &, | and ~ operators take high precedence in the language; as a result, parenthesis must usually be applied for operands that themselves contain expressions, as indicated in the examples below.

Operators.__and__() (Python “&” operator):

The Python binary & operator is overloaded to behave the same as and_() (note parenthesis around the two operands):

Operators.__or__() (Python “|” operator):

The Python binary | operator is overloaded to behave the same as or_() (note parenthesis around the two operands):

Operators.__invert__() (Python “~” operator):

The Python binary ~ operator is overloaded to behave the same as not_(), either inverting the existing operator, or applying the NOT keyword to the expression as a whole:

Parenthesization of expressions is rendered based on operator precedence, not the placement of parentheses in Python code, since there is no means of detecting parentheses from interpreted Python expressions. So an expression like:

won’t include parentheses, because the AND operator takes natural precedence over OR:

Whereas this one, where OR would otherwise not be evaluated before the AND, does:

The same behavior takes effect for math operators. In the parenthesized Python expression below, the multiplication operator naturally takes precedence over the addition operator, therefore the SQL will not include parentheses:

Whereas this one, where the addition operator would not otherwise occur before the multiplication operator, does get parentheses:

More background on this is in the FAQ at Why are the parentheses rules like this?.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (unknown):
```unknown
>>> print(column("x") == 5)
x = :x_1
```

Example 2 (unknown):
```unknown
>>> print(column("x") != 5)
x != :x_1
```

Example 3 (unknown):
```unknown
>>> print(column("x") > 5)
x > :x_1
```

Example 4 (unknown):
```unknown
>>> print(column("x") < 5)
x < :x_1
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/core/sqlelement.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Core
    - Project Versions
- Column Elements and Expressions¶
- Column Element Foundational Constructors¶
- Column Element Modifier Constructors¶
- Column Element Class Documentation¶
- Column Element Typing Utilities¶

Home | Download this Documentation

Home | Download this Documentation

The expression API consists of a series of classes each of which represents a specific lexical element within a SQL string. Composed together into a larger structure, they form a statement construct that may be compiled into a string representation that can be passed to a database. The classes are organized into a hierarchy that begins at the basemost ClauseElement class. Key subclasses include ColumnElement, which represents the role of any column-based expression in a SQL statement, such as in the columns clause, WHERE clause, and ORDER BY clause, and FromClause, which represents the role of a token that is placed in the FROM clause of a SELECT statement.

Standalone functions imported from the sqlalchemy namespace which are used when building up SQLAlchemy Expression Language constructs.

Produce a conjunction of expressions joined by AND.

bindparam(key[, value, type_, unique, ...])

Produce a “bound expression”.

Produce a unary bitwise NOT clause, typically via the ~ operator.

case(*whens, [value, else_])

Produce a CASE expression.

cast(expression, type_)

Produce a CAST expression.

column(text[, type_, is_literal, _selectable])

Produce a ColumnClause object.

Represent a ‘custom’ operator.

Produce an column-expression-level unary DISTINCT clause.

Return a Extract construct.

Return a False_ construct.

Generate SQL function expressions.

lambda_stmt(lmb[, enable_tracking, track_closure_variables, track_on, ...])

Produce a SQL statement that is cached as a lambda.

literal(value[, type_, literal_execute])

Return a literal clause, bound to a bind parameter.

literal_column(text[, type_])

Produce a ColumnClause object that has the column.is_literal flag set to True.

Return a negation of the given clause, i.e. NOT(clause).

Return a constant Null construct.

Produce a conjunction of expressions joined by OR.

outparam(key[, type_])

Create an ‘OUT’ parameter for usage in functions (stored procedures), for databases which support them.

Represent a SQL identifier combined with quoting preferences.

Construct a new TextClause clause, representing a textual SQL string directly.

Return a constant True_ construct.

try_cast(expression, type_)

Produce a TRY_CAST expression for backends which support it; this is a CAST which returns NULL for un-castable conversions.

tuple_(*clauses, [types])

type_coerce(expression, type_)

Associate a SQL expression with a particular type, without rendering CAST.

Produce a conjunction of expressions joined by AND.

The and_() conjunction is also available using the Python & operator (though note that compound expressions need to be parenthesized in order to function with Python operator precedence behavior):

The and_() operation is also implicit in some cases; the Select.where() method for example can be invoked multiple times against a statement, which will have the effect of each clause being combined using and_():

The and_() construct must be given at least one positional argument in order to be valid; a and_() construct with no arguments is ambiguous. To produce an “empty” or dynamically generated and_() expression, from a given list of expressions, a “default” element of true() (or just True) should be specified:

The above expression will compile to SQL as the expression true or 1 = 1, depending on backend, if no other expressions are present. If expressions are present, then the true() value is ignored as it does not affect the outcome of an AND expression that has other elements.

Deprecated since version 1.4: The and_() element now requires that at least one argument is passed; creating the and_() construct with no arguments is deprecated, and will emit a deprecation warning while continuing to produce a blank SQL string.

Produce a “bound expression”.

The return value is an instance of BindParameter; this is a ColumnElement subclass which represents a so-called “placeholder” value in a SQL expression, the value of which is supplied at the point at which the statement in executed against a database connection.

In SQLAlchemy, the bindparam() construct has the ability to carry along the actual value that will be ultimately used at expression time. In this way, it serves not just as a “placeholder” for eventual population, but also as a means of representing so-called “unsafe” values which should not be rendered directly in a SQL statement, but rather should be passed along to the DBAPI as values which need to be correctly escaped and potentially handled for type-safety.

When using bindparam() explicitly, the use case is typically one of traditional deferment of parameters; the bindparam() construct accepts a name which can then be referred to at execution time:

The above statement, when rendered, will produce SQL similar to:

In order to populate the value of :username above, the value would typically be applied at execution time to a method like Connection.execute():

Explicit use of bindparam() is also common when producing UPDATE or DELETE statements that are to be invoked multiple times, where the WHERE criterion of the statement is to change on each invocation, such as:

SQLAlchemy’s Core expression system makes wide use of bindparam() in an implicit sense. It is typical that Python literal values passed to virtually all SQL expression functions are coerced into fixed bindparam() constructs. For example, given a comparison operation such as:

The above expression will produce a BinaryExpression construct, where the left side is the Column object representing the name column, and the right side is a BindParameter representing the literal value:

The expression above will render SQL such as:

Where the :name_1 parameter name is an anonymous name. The actual string Wendy is not in the rendered string, but is carried along where it is later used within statement execution. If we invoke a statement like the following:

We would see SQL logging output as:

Above, we see that Wendy is passed as a parameter to the database, while the placeholder :name_1 is rendered in the appropriate form for the target database, in this case the PostgreSQL database.

Similarly, bindparam() is invoked automatically when working with CRUD statements as far as the “VALUES” portion is concerned. The insert() construct produces an INSERT expression which will, at statement execution time, generate bound placeholders based on the arguments passed, as in:

The above will produce SQL output as:

The Insert construct, at compilation/execution time, rendered a single bindparam() mirroring the column name name as a result of the single name parameter we passed to the Connection.execute() method.

the key (e.g. the name) for this bind param. Will be used in the generated SQL statement for dialects that use named parameters. This value may be modified when part of a compilation operation, if other BindParameter objects exist with the same key, or if its length is too long and truncation is required.

If omitted, an “anonymous” name is generated for the bound parameter; when given a value to bind, the end result is equivalent to calling upon the literal() function with a value to bind, particularly if the bindparam.unique parameter is also provided.

value¶ – Initial value for this bind param. Will be used at statement execution time as the value for this parameter passed to the DBAPI, if no other value is indicated to the statement execution method for this particular parameter name. Defaults to None.

callable_¶ – A callable function that takes the place of “value”. The function will be called at statement execution time to determine the ultimate value. Used for scenarios where the actual bind value cannot be determined at the point at which the clause construct is created, but embedded bind values are still desirable.

A TypeEngine class or instance representing an optional datatype for this bindparam(). If not passed, a type may be determined automatically for the bind, based on the given value; for example, trivial Python types such as str, int, bool may result in the String, Integer or Boolean types being automatically selected.

The type of a bindparam() is significant especially in that the type will apply pre-processing to the value before it is passed to the database. For example, a bindparam() which refers to a datetime value, and is specified as holding the DateTime type, may apply conversion needed to the value (such as stringification on SQLite) before passing the value to the database.

unique¶ – if True, the key name of this BindParameter will be modified if another BindParameter of the same name already has been located within the containing expression. This flag is used generally by the internals when producing so-called “anonymous” bound expressions, it isn’t generally applicable to explicitly-named bindparam() constructs.

required¶ – If True, a value is required at execution time. If not passed, it defaults to True if neither bindparam.value or bindparam.callable were passed. If either of these parameters are present, then bindparam.required defaults to False.

quote¶ – True if this parameter name requires quoting and is not currently known as a SQLAlchemy reserved word; this currently only applies to the Oracle Database backends, where bound names must sometimes be quoted.

isoutparam¶ – if True, the parameter should be treated like a stored procedure “OUT” parameter. This applies to backends such as Oracle Database which support OUT parameters.

if True, this parameter will be treated as an “expanding” parameter at execution time; the parameter value is expected to be a sequence, rather than a scalar value, and the string SQL statement will be transformed on a per-execution basis to accommodate the sequence with a variable number of parameter slots passed to the DBAPI. This is to allow statement caching to be used in conjunction with an IN clause.

ColumnOperators.in_()

Using IN expressions - with baked queries

The “expanding” feature does not support “executemany”- style parameter sets.

Added in version 1.2.

Changed in version 1.3: the “expanding” bound parameter feature now supports empty lists.

if True, the bound parameter will be rendered in the compile phase with a special “POSTCOMPILE” token, and the SQLAlchemy compiler will render the final value of the parameter into the SQL statement at statement execution time, omitting the value from the parameter dictionary / list passed to DBAPI cursor.execute(). This produces a similar effect as that of using the literal_binds, compilation flag, however takes place as the statement is sent to the DBAPI cursor.execute() method, rather than when the statement is compiled. The primary use of this capability is for rendering LIMIT / OFFSET clauses for database drivers that can’t accommodate for bound parameters in these contexts, while allowing SQL constructs to be cacheable at the compilation level.

Added in version 1.4: Added “post compile” bound parameters

New “post compile” bound parameters used for LIMIT/OFFSET in Oracle, SQL Server.

Sending Parameters - in the SQLAlchemy Unified Tutorial

Produce a unary bitwise NOT clause, typically via the ~ operator.

Not to be confused with boolean negation not_().

Added in version 2.0.2.

Produce a CASE expression.

The CASE construct in SQL is a conditional object that acts somewhat analogously to an “if/then” construct in other languages. It returns an instance of Case.

case() in its usual form is passed a series of “when” constructs, that is, a list of conditions and results as tuples:

The above statement will produce SQL resembling:

When simple equality expressions of several values against a single parent column are needed, case() also has a “shorthand” format used via the case.value parameter, which is passed a column expression to be compared. In this form, the case.whens parameter is passed as a dictionary containing expressions to be compared against keyed to result expressions. The statement below is equivalent to the preceding statement:

The values which are accepted as result values in case.whens as well as with case.else_ are coerced from Python literals into bindparam() constructs. SQL expressions, e.g. ColumnElement constructs, are accepted as well. To coerce a literal string expression into a constant expression rendered inline, use the literal_column() construct, as in:

The above will render the given constants without using bound parameters for the result values (but still for the comparison values), as in:

The criteria to be compared against, case.whens accepts two different forms, based on whether or not case.value is used.

Changed in version 1.4: the case() function now accepts the series of WHEN conditions positionally

In the first form, it accepts multiple 2-tuples passed as positional arguments; each 2-tuple consists of (<sql expression>, <value>), where the SQL expression is a boolean expression and “value” is a resulting value, e.g.:

In the second form, it accepts a Python dictionary of comparison values mapped to a resulting value; this form requires case.value to be present, and values will be compared using the == operator, e.g.:

value¶ – An optional SQL expression which will be used as a fixed “comparison point” for candidate values within a dictionary passed to case.whens.

else_¶ – An optional SQL expression which will be the evaluated result of the CASE construct if all expressions within case.whens evaluate to false. When omitted, most databases will produce a result of NULL if none of the “when” expressions evaluate to true.

Produce a CAST expression.

cast() returns an instance of Cast.

The above statement will produce SQL resembling:

The cast() function performs two distinct functions when used. The first is that it renders the CAST expression within the resulting SQL string. The second is that it associates the given type (e.g. TypeEngine class or instance) with the column expression on the Python side, which means the expression will take on the expression operator behavior associated with that type, as well as the bound-value handling and result-row-handling behavior of the type.

An alternative to cast() is the type_coerce() function. This function performs the second task of associating an expression with a specific type, but does not render the CAST expression in SQL.

expression¶ – A SQL expression, such as a ColumnElement expression or a Python string which will be coerced into a bound literal value.

type_¶ – A TypeEngine class or instance indicating the type to which the CAST should apply.

Data Casts and Type Coercion

try_cast() - an alternative to CAST that results in NULLs when the cast fails, instead of raising an error. Only supported by some dialects.

type_coerce() - an alternative to CAST that coerces the type on the Python side only, which is often sufficient to generate the correct SQL and data coercion.

Produce a ColumnClause object.

The ColumnClause is a lightweight analogue to the Column class. The column() function can be invoked with just a name alone, as in:

The above statement would produce SQL like:

Once constructed, column() may be used like any other SQL expression element such as within select() constructs:

The text handled by column() is assumed to be handled like the name of a database column; if the string contains mixed case, special characters, or matches a known reserved word on the target backend, the column expression will render using the quoting behavior determined by the backend. To produce a textual SQL expression that is rendered exactly without any quoting, use literal_column() instead, or pass True as the value of column.is_literal. Additionally, full SQL statements are best handled using the text() construct.

column() can be used in a table-like fashion by combining it with the table() function (which is the lightweight analogue to Table ) to produce a working table construct with minimal boilerplate:

A column() / table() construct like that illustrated above can be created in an ad-hoc fashion and is not associated with any MetaData, DDL, or events, unlike its Table counterpart.

text¶ – the text of the element.

type¶ – TypeEngine object which can associate this ColumnClause with a type.

is_literal¶ – if True, the ColumnClause is assumed to be an exact expression that will be delivered to the output with no quoting rules applied regardless of case sensitive settings. the literal_column() function essentially invokes column() while passing is_literal=True.

Selecting with Textual Column Expressions

inherits from sqlalchemy.sql.expression.OperatorType, typing.Generic

Represent a ‘custom’ operator.

custom_op is normally instantiated when the Operators.op() or Operators.bool_op() methods are used to create a custom operator callable. The class can also be used directly when programmatically constructing expressions. E.g. to represent the “factorial” operation:

Produce an column-expression-level unary DISTINCT clause.

This applies the DISTINCT keyword to an individual column expression (e.g. not the whole statement), and renders specifically in that column position; this is used for containment within an aggregate function, as in:

The above would produce an statement resembling:

The distinct() function does not apply DISTINCT to the full SELECT statement, instead applying a DISTINCT modifier to individual column expressions. For general SELECT DISTINCT support, use the Select.distinct() method on Select.

The distinct() function is also available as a column-level method, e.g. ColumnElement.distinct(), as in:

The distinct() operator is different from the Select.distinct() method of Select, which produces a SELECT statement with DISTINCT applied to the result set as a whole, e.g. a SELECT DISTINCT expression. See that method for further information.

ColumnElement.distinct()

Return a Extract construct.

This is typically available as extract() as well as func.extract from the func namespace.

The field to extract.

This field is used as a literal SQL string. DO NOT PASS UNTRUSTED INPUT TO THIS STRING.

expr¶ – A column or Python scalar expression serving as the right side of the EXTRACT expression.

In the above example, the statement is used to select ids from the database where the YEAR component matches a specific value.

Similarly, one can also select an extracted component:

The implementation of EXTRACT may vary across database backends. Users are reminded to consult their database documentation.

Return a False_ construct.

A backend which does not support true/false constants will render as an expression against 1 or 0:

The true() and false() constants also feature “short circuit” operation within an and_() or or_() conjunction:

Generate SQL function expressions.

func is a special object instance which generates SQL functions based on name-based attributes, e.g.:

The returned object is an instance of Function, and is a column-oriented SQL element like any other, and is used in that way:

Any name can be given to func. If the function name is unknown to SQLAlchemy, it will be rendered exactly as is. For common SQL functions which SQLAlchemy is aware of, the name may be interpreted as a generic function which will be compiled appropriately to the target database:

To call functions which are present in dot-separated packages, specify them in the same manner:

SQLAlchemy can be made aware of the return type of functions to enable type-specific lexical and result-based behavior. For example, to ensure that a string-based function returns a Unicode value and is similarly treated as a string in expressions, specify Unicode as the type:

The object returned by a func call is usually an instance of Function. This object meets the “column” interface, including comparison and labeling functions. The object can also be passed the Connectable.execute() method of a Connection or Engine, where it will be wrapped inside of a SELECT statement first:

In a few exception cases, the func accessor will redirect a name to a built-in expression such as cast() or extract(), as these names have well-known meaning but are not exactly the same as “functions” from a SQLAlchemy perspective.

Functions which are interpreted as “generic” functions know how to calculate their return type automatically. For a listing of known generic functions, see SQL and Generic Functions.

The func construct has only limited support for calling standalone “stored procedures”, especially those with special parameterization concerns.

See the section Calling Stored Procedures and User Defined Functions for details on how to use the DBAPI-level callproc() method for fully traditional stored procedures.

Working with SQL Functions - in the SQLAlchemy Unified Tutorial

Produce a SQL statement that is cached as a lambda.

The Python code object within the lambda is scanned for both Python literals that will become bound parameters as well as closure variables that refer to Core or ORM constructs that may vary. The lambda itself will be invoked only once per particular set of constructs detected.

The object returned is an instance of StatementLambdaElement.

Added in version 1.4.

lmb¶ – a Python function, typically a lambda, which takes no arguments and returns a SQL expression construct

enable_tracking¶ – when False, all scanning of the given lambda for changes in closure variables or bound parameters is disabled. Use for a lambda that produces the identical results in all cases with no parameterization.

track_closure_variables¶ – when False, changes in closure variables within the lambda will not be scanned. Use for a lambda where the state of its closure variables will never change the SQL structure returned by the lambda.

track_bound_values¶ – when False, bound parameter tracking will be disabled for the given lambda. Use for a lambda that either does not produce any bound values, or where the initial bound values never change.

global_track_bound_values¶ – when False, bound parameter tracking will be disabled for the entire statement including additional links added via the StatementLambdaElement.add_criteria() method.

lambda_cache¶ – a dictionary or other mapping-like object where information about the lambda’s Python code as well as the tracked closure variables in the lambda itself will be stored. Defaults to a global LRU cache. This cache is independent of the “compiled_cache” used by the Connection object.

Using Lambdas to add significant speed gains to statement production

Return a literal clause, bound to a bind parameter.

Literal clauses are created automatically when non- ClauseElement objects (such as strings, ints, dates, etc.) are used in a comparison operation with a ColumnElement subclass, such as a Column object. Use this function to force the generation of a literal clause, which will be created as a BindParameter with a bound value.

value¶ – the value to be bound. Can be any Python object supported by the underlying DB-API, or is translatable via the given type argument.

type_¶ – an optional TypeEngine which will provide bind-parameter translation for this literal.

optional bool, when True, the SQL engine will attempt to render the bound value directly in the SQL statement at execution time rather than providing as a parameter value.

Added in version 2.0.

Produce a ColumnClause object that has the column.is_literal flag set to True.

literal_column() is similar to column(), except that it is more often used as a “standalone” column expression that renders exactly as stated; while column() stores a string name that will be assumed to be part of a table and may be quoted as such, literal_column() can be that, or any other arbitrary column-oriented expression.

text¶ – the text of the expression; can be any SQL expression. Quoting rules will not be applied. To specify a column-name expression which should be subject to quoting rules, use the column() function.

type_¶ – an optional TypeEngine object which will provide result-set translation and additional expression semantics for this column. If left as None the type will be NullType.

Selecting with Textual Column Expressions

Return a negation of the given clause, i.e. NOT(clause).

The ~ operator is also overloaded on all ColumnElement subclasses to produce the same result.

Return a constant Null construct.

Produce a conjunction of expressions joined by OR.

The or_() conjunction is also available using the Python | operator (though note that compound expressions need to be parenthesized in order to function with Python operator precedence behavior):

The or_() construct must be given at least one positional argument in order to be valid; a or_() construct with no arguments is ambiguous. To produce an “empty” or dynamically generated or_() expression, from a given list of expressions, a “default” element of false() (or just False) should be specified:

The above expression will compile to SQL as the expression false or 0 = 1, depending on backend, if no other expressions are present. If expressions are present, then the false() value is ignored as it does not affect the outcome of an OR expression which has other elements.

Deprecated since version 1.4: The or_() element now requires that at least one argument is passed; creating the or_() construct with no arguments is deprecated, and will emit a deprecation warning while continuing to produce a blank SQL string.

Create an ‘OUT’ parameter for usage in functions (stored procedures), for databases which support them.

The outparam can be used like a regular function parameter. The “output” value will be available from the CursorResult object via its out_parameters attribute, which returns a dictionary containing the values.

Construct a new TextClause clause, representing a textual SQL string directly.

The advantages text() provides over a plain string are backend-neutral support for bind parameters, per-statement execution options, as well as bind parameter and result-column typing behavior, allowing SQLAlchemy type constructs to play a role when executing a statement that is specified literally. The construct can also be provided with a .c collection of column elements, allowing it to be embedded in other SQL expression constructs as a subquery.

Bind parameters are specified by name, using the format :name. E.g.:

For SQL statements where a colon is required verbatim, as within an inline string, use a backslash to escape:

The TextClause construct includes methods which can provide information about the bound parameters as well as the column values which would be returned from the textual statement, assuming it’s an executable SELECT type of statement. The TextClause.bindparams() method is used to provide bound parameter detail, and TextClause.columns() method allows specification of return columns including names and types:

The text() construct is used in cases when a literal string SQL fragment is specified as part of a larger query, such as for the WHERE clause of a SELECT statement:

text() is also used for the construction of a full, standalone statement using plain text. As such, SQLAlchemy refers to it as an Executable object and may be used like any other statement passed to an .execute() method.

text¶ – the text of the SQL statement to be created. Use :<param> to specify bind parameters; they will be compiled to their engine-specific format.

Selecting with Textual Column Expressions

Return a constant True_ construct.

A backend which does not support true/false constants will render as an expression against 1 or 0:

The true() and false() constants also feature “short circuit” operation within an and_() or or_() conjunction:

Produce a TRY_CAST expression for backends which support it; this is a CAST which returns NULL for un-castable conversions.

In SQLAlchemy, this construct is supported only by the SQL Server dialect, and will raise a CompileError if used on other included backends. However, third party backends may also support this construct.

As try_cast() originates from the SQL Server dialect, it’s importable both from sqlalchemy. as well as from sqlalchemy.dialects.mssql.

try_cast() returns an instance of TryCast and generally behaves similarly to the Cast construct; at the SQL level, the difference between CAST and TRY_CAST is that TRY_CAST returns NULL for an un-castable expression, such as attempting to cast a string "hi" to an integer value.

The above would render on Microsoft SQL Server as:

Added in version 2.0.14: try_cast() has been generalized from the SQL Server dialect into a general use construct that may be supported by additional dialects.

Main usage is to produce a composite IN construct using ColumnOperators.in_()

Changed in version 1.3.6: Added support for SQLite IN tuples.

The composite IN construct is not supported by all backends, and is currently known to work on PostgreSQL, MySQL, and SQLite. Unsupported backends will raise a subclass of DBAPIError when such an expression is invoked.

Associate a SQL expression with a particular type, without rendering CAST.

The above construct will produce a TypeCoerce object, which does not modify the rendering in any way on the SQL side, with the possible exception of a generated label if used in a columns clause context:

When result rows are fetched, the StringDateTime type processor will be applied to result rows on behalf of the date_string column.

the type_coerce() construct does not render any SQL syntax of its own, including that it does not imply parenthesization. Please use TypeCoerce.self_group() if explicit parenthesization is required.

In order to provide a named label for the expression, use ColumnElement.label():

A type that features bound-value handling will also have that behavior take effect when literal values or bindparam() constructs are passed to type_coerce() as targets. For example, if a type implements the TypeEngine.bind_expression() method or TypeEngine.bind_processor() method or equivalent, these functions will take effect at statement compilation/execution time when a literal value is passed, as in:

When using type_coerce() with composed expressions, note that parenthesis are not applied. If type_coerce() is being used in an operator context where the parenthesis normally present from CAST are necessary, use the TypeCoerce.self_group() method:

expression¶ – A SQL expression, such as a ColumnElement expression or a Python string which will be coerced into a bound literal value.

type_¶ – A TypeEngine class or instance indicating the type to which the expression is coerced.

Data Casts and Type Coercion

inherits from sqlalchemy.util.langhelpers.MemoizedSlots, builtins.str

Represent a SQL identifier combined with quoting preferences.

quoted_name is a Python unicode/str subclass which represents a particular identifier name along with a quote flag. This quote flag, when set to True or False, overrides automatic quoting behavior for this identifier in order to either unconditionally quote or to not quote the name. If left at its default of None, quoting behavior is applied to the identifier on a per-backend basis based on an examination of the token itself.

A quoted_name object with quote=True is also prevented from being modified in the case of a so-called “name normalize” option. Certain database backends, such as Oracle Database, Firebird, and DB2 “normalize” case-insensitive names as uppercase. The SQLAlchemy dialects for these backends convert from SQLAlchemy’s lower-case-means-insensitive convention to the upper-case-means-insensitive conventions of those backends. The quote=True flag here will prevent this conversion from occurring to support an identifier that’s quoted as all lower case against such a backend.

The quoted_name object is normally created automatically when specifying the name for key schema constructs such as Table, Column, and others. The class can also be passed explicitly as the name to any function that receives a name which can be quoted. Such as to use the Engine.has_table() method with an unconditionally quoted name:

The above logic will run the “has table” logic against the Oracle Database backend, passing the name exactly as "some_table" without converting to upper case.

Changed in version 1.2: The quoted_name construct is now importable from sqlalchemy.sql, in addition to the previous location of sqlalchemy.sql.elements.

whether the string should be unconditionally quoted

whether the string should be unconditionally quoted

Functions listed here are more commonly available as methods from any ColumnElement construct, for example, the label() function is usually invoked via the ColumnElement.label() method.

Produce an ALL expression.

Produce an ANY expression.

Produce an ascending ORDER BY clause element.

between(expr, lower_bound, upper_bound[, symmetric])

Produce a BETWEEN predicate clause.

collate(expression, collation)

Return the clause expression COLLATE collation.

Produce a descending ORDER BY clause element.

funcfilter(func, *criterion)

Produce a FunctionFilter object against a function.

label(name, element[, type_])

Return a Label object for the given ColumnElement.

Produce the NULLS FIRST modifier for an ORDER BY expression.

Produce the NULLS LAST modifier for an ORDER BY expression.

Synonym for the nulls_first() function.

Legacy synonym for the nulls_last() function.

over(element[, partition_by, order_by, range_, ...])

Produce an Over object against a function.

within_group(element, *order_by)

Produce a WithinGroup object against a function.

Produce an ALL expression.

For dialects such as that of PostgreSQL, this operator applies to usage of the ARRAY datatype, for that of MySQL, it may apply to a subquery. e.g.:

Comparison to NULL may work using None:

The any_() / all_() operators also feature a special “operand flipping” behavior such that if any_() / all_() are used on the left side of a comparison using a standalone operator such as ==, !=, etc. (not including operator methods such as ColumnOperators.is_()) the rendered expression is flipped:

Or with None, which note will not perform the usual step of rendering “IS” as is normally the case for NULL:

Changed in version 1.4.26: repaired the use of any_() / all_() comparing to NULL on the right side to be flipped to the left.

The column-level ColumnElement.all_() method (not to be confused with ARRAY level Comparator.all()) is shorthand for all_(col):

ColumnOperators.all_()

Produce an ANY expression.

For dialects such as that of PostgreSQL, this operator applies to usage of the ARRAY datatype, for that of MySQL, it may apply to a subquery. e.g.:

Comparison to NULL may work using None or null():

The any_() / all_() operators also feature a special “operand flipping” behavior such that if any_() / all_() are used on the left side of a comparison using a standalone operator such as ==, !=, etc. (not including operator methods such as ColumnOperators.is_()) the rendered expression is flipped:

Or with None, which note will not perform the usual step of rendering “IS” as is normally the case for NULL:

Changed in version 1.4.26: repaired the use of any_() / all_() comparing to NULL on the right side to be flipped to the left.

The column-level ColumnElement.any_() method (not to be confused with ARRAY level Comparator.any()) is shorthand for any_(col):

ColumnOperators.any_()

Produce an ascending ORDER BY clause element.

The asc() function is a standalone version of the ColumnElement.asc() method available on all SQL expressions, e.g.:

column¶ – A ColumnElement (e.g. scalar SQL expression) with which to apply the asc() operation.

Produce a BETWEEN predicate clause.

Would produce SQL resembling:

The between() function is a standalone version of the ColumnElement.between() method available on all SQL expressions, as in:

All arguments passed to between(), including the left side column expression, are coerced from Python scalar values if a the value is not a ColumnElement subclass. For example, three fixed values can be compared as in:

expr¶ – a column expression, typically a ColumnElement instance or alternatively a Python scalar expression to be coerced into a column expression, serving as the left side of the BETWEEN expression.

lower_bound¶ – a column or Python scalar expression serving as the lower bound of the right side of the BETWEEN expression.

upper_bound¶ – a column or Python scalar expression serving as the upper bound of the right side of the BETWEEN expression.

symmetric¶ – if True, will render “ BETWEEN SYMMETRIC “. Note that not all databases support this syntax.

ColumnElement.between()

Return the clause expression COLLATE collation.

The collation expression is also quoted if it is a case sensitive identifier, e.g. contains uppercase characters.

Changed in version 1.2: quoting is automatically applied to COLLATE expressions if they are case sensitive.

Produce a descending ORDER BY clause element.

The desc() function is a standalone version of the ColumnElement.desc() method available on all SQL expressions, e.g.:

column¶ – A ColumnElement (e.g. scalar SQL expression) with which to apply the desc() operation.

Produce a FunctionFilter object against a function.

Used against aggregate and window functions, for database backends that support the “FILTER” clause.

Would produce “COUNT(1) FILTER (WHERE myclass.name = ‘some name’)”.

This function is also available from the func construct itself via the FunctionElement.filter() method.

Special Modifiers WITHIN GROUP, FILTER - in the SQLAlchemy Unified Tutorial

FunctionElement.filter()

Return a Label object for the given ColumnElement.

A label changes the name of an element in the columns clause of a SELECT statement, typically via the AS SQL keyword.

This functionality is more conveniently available via the ColumnElement.label() method on ColumnElement.

obj¶ – a ColumnElement.

Produce the NULLS FIRST modifier for an ORDER BY expression.

nulls_first() is intended to modify the expression produced by asc() or desc(), and indicates how NULL values should be handled when they are encountered during ordering:

The SQL expression from the above would resemble:

Like asc() and desc(), nulls_first() is typically invoked from the column expression itself using ColumnElement.nulls_first(), rather than as its standalone function version, as in:

Changed in version 1.4: nulls_first() is renamed from nullsfirst() in previous releases. The previous name remains available for backwards compatibility.

Synonym for the nulls_first() function.

Changed in version 2.0.5: restored missing legacy symbol nullsfirst().

Produce the NULLS LAST modifier for an ORDER BY expression.

nulls_last() is intended to modify the expression produced by asc() or desc(), and indicates how NULL values should be handled when they are encountered during ordering:

The SQL expression from the above would resemble:

Like asc() and desc(), nulls_last() is typically invoked from the column expression itself using ColumnElement.nulls_last(), rather than as its standalone function version, as in:

Changed in version 1.4: nulls_last() is renamed from nullslast() in previous releases. The previous name remains available for backwards compatibility.

Legacy synonym for the nulls_last() function.

Changed in version 2.0.5: restored missing legacy symbol nullslast().

Produce an Over object against a function.

Used against aggregate or so-called “window” functions, for database backends that support window functions.

over() is usually called using the FunctionElement.over() method, e.g.:

Ranges are also possible using the over.range_, over.rows, and over.groups parameters. These mutually-exclusive parameters each accept a 2-tuple, which contains a combination of integers and None:

The above would produce:

A value of None indicates “unbounded”, a value of zero indicates “current row”, and negative / positive integers indicate “preceding” and “following”:

RANGE BETWEEN 5 PRECEDING AND 10 FOLLOWING:

ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW:

RANGE BETWEEN 2 PRECEDING AND UNBOUNDED FOLLOWING:

RANGE BETWEEN 1 FOLLOWING AND 3 FOLLOWING:

GROUPS BETWEEN 1 FOLLOWING AND 3 FOLLOWING:

element¶ – a FunctionElement, WithinGroup, or other compatible construct.

partition_by¶ – a column element or string, or a list of such, that will be used as the PARTITION BY clause of the OVER construct.

order_by¶ – a column element or string, or a list of such, that will be used as the ORDER BY clause of the OVER construct.

range_¶ – optional range clause for the window. This is a tuple value which can contain integer values or None, and will render a RANGE BETWEEN PRECEDING / FOLLOWING clause.

rows¶ – optional rows clause for the window. This is a tuple value which can contain integer values or None, and will render a ROWS BETWEEN PRECEDING / FOLLOWING clause.

optional groups clause for the window. This is a tuple value which can contain integer values or None, and will render a GROUPS BETWEEN PRECEDING / FOLLOWING clause.

Added in version 2.0.40.

This function is also available from the func construct itself via the FunctionElement.over() method.

Using Window Functions - in the SQLAlchemy Unified Tutorial

Produce a WithinGroup object against a function.

Used against so-called “ordered set aggregate” and “hypothetical set aggregate” functions, including percentile_cont, rank, dense_rank, etc.

within_group() is usually called using the FunctionElement.within_group() method, e.g.:

The above statement would produce SQL similar to SELECT department.id, percentile_cont(0.5) WITHIN GROUP (ORDER BY department.salary DESC).

element¶ – a FunctionElement construct, typically generated by func.

*order_by¶ – one or more column elements that will be used as the ORDER BY clause of the WITHIN GROUP construct.

Special Modifiers WITHIN GROUP, FILTER - in the SQLAlchemy Unified Tutorial

The classes here are generated using the constructors listed at Column Element Foundational Constructors and Column Element Modifier Constructors.

Represent an expression that is LEFT <operator> RIGHT.

Represent a “bound expression”.

Represent a CASE expression.

Represent a CAST expression.

Describe a list of clauses, separated by an operator.

Represents a column expression from any textual string.

Collection of ColumnElement instances, typically for FromClause objects.

Represent a column-oriented SQL expression suitable for usage in the “columns” clause, WHERE clause etc. of a statement.

ColumnExpressionArgument

General purpose “column expression” argument.

Defines boolean, comparison, and other operators for ColumnElement expressions.

Represent a SQL EXTRACT clause, extract(field FROM expr).

Represent the false keyword, or equivalent, in a SQL statement.

Represent a function FILTER clause.

Represents a column label (AS).

Represent the NULL keyword in a SQL statement.

Base of comparison and logical operators.

Represent an OVER clause.

A type that may be used to indicate any SQL column element or object that acts in place of one.

Represent a literal SQL text fragment.

Represent the true keyword, or equivalent, in a SQL statement.

Represent a TRY_CAST expression.

Represent a SQL tuple.

Represent a Python-side type-coercion wrapper.

Define a ‘unary’ expression.

Represent a WITHIN GROUP (ORDER BY) clause.

WrapsColumnExpression

Mixin that defines a ColumnElement as a wrapper with special labeling behavior for an expression that already has a name.

inherits from sqlalchemy.sql.expression.OperatorExpression

Represent an expression that is LEFT <operator> RIGHT.

A BinaryExpression is generated automatically whenever two column expressions are used in a Python binary expression:

inherits from sqlalchemy.sql.roles.InElementRole, sqlalchemy.sql.expression.KeyedColumnElement

Represent a “bound expression”.

BindParameter is invoked explicitly using the bindparam() function, as in:

Detailed discussion of how BindParameter is used is at bindparam().

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

render_literal_execute()

Produce a copy of this bound parameter that will enable the BindParameter.literal_execute flag.

Return the value of this bound parameter, taking into account if the callable parameter was set.

The callable value will be evaluated and returned if present, else value.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

Produce a copy of this bound parameter that will enable the BindParameter.literal_execute flag.

The BindParameter.literal_execute flag will have the effect of the parameter rendered in the compiled SQL string using [POSTCOMPILE] form, which is a special form that is converted to be a rendering of the literal value of the parameter at SQL execution time. The rationale is to support caching of SQL statement strings that can embed per-statement literal values, such as LIMIT and OFFSET parameters, in the final SQL string that is passed to the DBAPI. Dialects in particular may want to use this method within custom compilation schemes.

Added in version 1.4.5.

Caching for Third Party Dialects

inherits from sqlalchemy.sql.expression.ColumnElement

Represent a CASE expression.

Case is produced using the case() factory function, as in:

Details on Case usage is at case().

inherits from sqlalchemy.sql.expression.WrapsColumnExpression

Represent a CAST expression.

Cast is produced using the cast() factory function, as in:

Details on Cast usage is at cast().

Data Casts and Type Coercion

type_coerce() - an alternative to CAST that coerces the type on the Python side only, which is often sufficient to generate the correct SQL and data coercion.

inherits from sqlalchemy.sql.roles.InElementRole, sqlalchemy.sql.roles.OrderByRole, sqlalchemy.sql.roles.ColumnsClauseRole, sqlalchemy.sql.roles.DMLColumnRole, sqlalchemy.sql.expression.DQLDMLClauseElement

Describe a list of clauses, separated by an operator.

By default, is comma-separated, such as a column listing.

Apply a ‘grouping’ to this ClauseElement.

Apply a ‘grouping’ to this ClauseElement.

This method is overridden by subclasses to return a “grouping” construct, i.e. parenthesis. In particular it’s used by “binary” expressions to provide a grouping around themselves when placed into a larger expression, as well as by select() constructs when placed into the FROM clause of another select(). (Note that subqueries should be normally created using the Select.alias() method, as many platforms require nested SELECT statements to be named).

As expressions are composed together, the application of self_group() is automatic - end-user code should never need to use this method directly. Note that SQLAlchemy’s clause constructs take operator precedence into account - so parenthesis might not be needed, for example, in an expression like x OR (y AND z) - AND takes precedence over OR.

The base self_group() method of ClauseElement just returns self.

inherits from sqlalchemy.sql.roles.DDLReferredColumnRole, sqlalchemy.sql.roles.LabeledColumnExprRole, sqlalchemy.sql.roles.StrAsPlainColumnRole, sqlalchemy.sql.expression.Immutable, sqlalchemy.sql.expression.NamedColumn

Represents a column expression from any textual string.

The ColumnClause, a lightweight analogue to the Column class, is typically invoked using the column() function, as in:

The above statement would produce SQL like:

ColumnClause is the immediate superclass of the schema-specific Column object. While the Column class has all the same capabilities as ColumnClause, the ColumnClause class is usable by itself in those cases where behavioral requirements are limited to simple SQL expression generation. The object has none of the associations with schema-level metadata or with execution-time behavior that Column does, so in that sense is a “lightweight” version of Column.

Full details on ColumnClause usage is at column().

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

This is used for visit traversal.

**kw may contain flags that change the collection that is returned, for example to return a subset of items in order to cut down on larger traversals, or to return child items from a different context (such as schema-level collections instead of clause-level).

inherits from typing.Generic

Collection of ColumnElement instances, typically for FromClause objects.

The ColumnCollection object is most commonly available as the Table.c or Table.columns collection on the Table object, introduced at Accessing Tables and Columns.

The ColumnCollection has both mapping- and sequence- like behaviors. A ColumnCollection usually stores Column objects, which are then accessible both via mapping style access as well as attribute access style.

To access Column objects using ordinary attribute-style access, specify the name like any other object attribute, such as below a column named employee_name is accessed:

To access columns that have names with special characters or spaces, index-style access is used, such as below which illustrates a column named employee ' payment is accessed:

As the ColumnCollection object provides a Python dictionary interface, common dictionary method names like ColumnCollection.keys(), ColumnCollection.values(), and ColumnCollection.items() are available, which means that database columns that are keyed under these names also need to use indexed access:

The name for which a Column would be present is normally that of the Column.key parameter. In some contexts, such as a Select object that uses a label style set using the Select.set_label_style() method, a column of a certain key may instead be represented under a particular label name such as tablename_columnname:

ColumnCollection also indexes the columns in order and allows them to be accessible by their integer position:

Added in version 1.4: ColumnCollection allows integer-based index access to the collection.

Iterating the collection yields the column expressions in order:

The base ColumnCollection object can store duplicates, which can mean either two columns with the same key, in which case the column returned by key access is arbitrary:

Or it can also mean the same column multiple times. These cases are supported as ColumnCollection is used to represent the columns in a SELECT statement which may include duplicates.

A special subclass DedupeColumnCollection exists which instead maintains SQLAlchemy’s older behavior of not allowing duplicates; this collection is used for schema level objects like Table and PrimaryKeyConstraint where this deduping is helpful. The DedupeColumnCollection class also has additional mutation methods as the schema constructs have more use cases that require removal and replacement of columns.

Changed in version 1.4: ColumnCollection now stores duplicate column keys as well as the same column in multiple positions. The DedupeColumnCollection class is added to maintain the former behavior in those cases where deduplication as well as additional replace/remove operations are needed.

Add a column to this ColumnCollection.

Return a “read only” form of this ColumnCollection.

Dictionary clear() is not implemented for ColumnCollection.

Compare this ColumnCollection to another based on the names of the keys

Checks if a column object exists in this collection

corresponding_column()

Given a ColumnElement, return the exported ColumnElement object from this ColumnCollection which corresponds to that original ColumnElement via a common ancestor column.

Get a ColumnClause or Column object based on a string key name from this ColumnCollection.

Return a sequence of (key, column) tuples for all columns in this collection each consisting of a string key name and a ColumnClause or Column object.

Return a sequence of string key names for all columns in this collection.

Dictionary update() is not implemented for ColumnCollection.

Return a sequence of ColumnClause or Column objects for all columns in this collection.

Add a column to this ColumnCollection.

This method is not normally used by user-facing code, as the ColumnCollection is usually part of an existing object such as a Table. To add a Column to an existing Table object, use the Table.append_column() method.

Return a “read only” form of this ColumnCollection.

Dictionary clear() is not implemented for ColumnCollection.

Compare this ColumnCollection to another based on the names of the keys

Checks if a column object exists in this collection

Given a ColumnElement, return the exported ColumnElement object from this ColumnCollection which corresponds to that original ColumnElement via a common ancestor column.

column¶ – the target ColumnElement to be matched.

require_embedded¶ – only return corresponding columns for the given ColumnElement, if the given ColumnElement is actually present within a sub-element of this Selectable. Normally the column will match if it merely shares a common ancestor with one of the exported columns of this Selectable.

Selectable.corresponding_column() - invokes this method against the collection returned by Selectable.exported_columns.

Changed in version 1.4: the implementation for corresponding_column was moved onto the ColumnCollection itself.

Get a ColumnClause or Column object based on a string key name from this ColumnCollection.

Return a sequence of (key, column) tuples for all columns in this collection each consisting of a string key name and a ColumnClause or Column object.

Return a sequence of string key names for all columns in this collection.

Dictionary update() is not implemented for ColumnCollection.

Return a sequence of ColumnClause or Column objects for all columns in this collection.

inherits from sqlalchemy.sql.roles.ColumnArgumentOrKeyRole, sqlalchemy.sql.roles.StatementOptionRole, sqlalchemy.sql.roles.WhereHavingRole, sqlalchemy.sql.roles.BinaryElementRole, sqlalchemy.sql.roles.OrderByRole, sqlalchemy.sql.roles.ColumnsClauseRole, sqlalchemy.sql.roles.LimitOffsetRole, sqlalchemy.sql.roles.DMLColumnRole, sqlalchemy.sql.roles.DDLConstraintColumnRole, sqlalchemy.sql.roles.DDLExpressionRole, sqlalchemy.sql.expression.SQLColumnExpression, sqlalchemy.sql.expression.DQLDMLClauseElement

Represent a column-oriented SQL expression suitable for usage in the “columns” clause, WHERE clause etc. of a statement.

While the most familiar kind of ColumnElement is the Column object, ColumnElement serves as the basis for any unit that may be present in a SQL expression, including the expressions themselves, SQL functions, bound parameters, literal expressions, keywords such as NULL, etc. ColumnElement is the ultimate base class for all such elements.

A wide variety of SQLAlchemy Core functions work at the SQL expression level, and are intended to accept instances of ColumnElement as arguments. These functions will typically document that they accept a “SQL expression” as an argument. What this means in terms of SQLAlchemy usually refers to an input which is either already in the form of a ColumnElement object, or a value which can be coerced into one. The coercion rules followed by most, but not all, SQLAlchemy Core functions with regards to SQL expressions are as follows:

a literal Python value, such as a string, integer or floating point value, boolean, datetime, Decimal object, or virtually any other Python object, will be coerced into a “literal bound value”. This generally means that a bindparam() will be produced featuring the given value embedded into the construct; the resulting BindParameter object is an instance of ColumnElement. The Python value will ultimately be sent to the DBAPI at execution time as a parameterized argument to the execute() or executemany() methods, after SQLAlchemy type-specific converters (e.g. those provided by any associated TypeEngine objects) are applied to the value.

any special object value, typically ORM-level constructs, which feature an accessor called __clause_element__(). The Core expression system looks for this method when an object of otherwise unknown type is passed to a function that is looking to coerce the argument into a ColumnElement and sometimes a SelectBase expression. It is used within the ORM to convert from ORM-specific objects like mapped classes and mapped attributes into Core expression objects.

The Python None value is typically interpreted as NULL, which in SQLAlchemy Core produces an instance of null().

A ColumnElement provides the ability to generate new ColumnElement objects using Python expressions. This means that Python operators such as ==, != and < are overloaded to mimic SQL operations, and allow the instantiation of further ColumnElement instances which are composed from other, more fundamental ColumnElement objects. For example, two ColumnClause objects can be added together with the addition operator + to produce a BinaryExpression. Both ColumnClause and BinaryExpression are subclasses of ColumnElement:

Implement the == operator.

Implement the <= operator.

Implement the < operator.

Implement the != operator.

Produce an all_() clause against the parent object.

Produce an any_() clause against the parent object.

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

Produce a distinct() clause against the parent object.

Implement the ‘endswith’ operator.

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

Implement the icontains operator, e.g. case insensitive version of ColumnOperators.contains().

Implement the iendswith operator, e.g. case insensitive version of ColumnOperators.endswith().

Implement the ilike operator, e.g. case insensitive LIKE.

Implement the in operator.

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

Implements a database-specific ‘regexp match’ operator.

Implements a database-specific ‘regexp replace’ operator.

Reverse operate on an argument.

Apply a ‘grouping’ to this ClauseElement.

Return True if the given ColumnElement has a common ancestor to this ColumnElement.

Implement the startswith operator.

Hack, allows datetime objects to be compared on the LHS.

Return a copy with bindparam() elements replaced.

inherited from the sqlalchemy.sql.expression.ColumnOperators.__eq__ method of ColumnOperators

Implement the == operator.

In a column context, produces the clause a = b. If the target is None, produces a IS NULL.

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

inherited from the ColumnOperators.desc() method of ColumnOperators

Produce a desc() clause against the parent object.

inherited from the ClauseElement.description attribute of ClauseElement

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

inherited from the ClauseElement.entity_namespace attribute of ClauseElement

Return a column expression.

Part of the inspection interface; returns self.

inherited from the HasTraverseInternals.get_children() method of HasTraverseInternals

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

inherited from the HasCacheKey.inherit_cache attribute of HasCacheKey

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

The ‘key’ that in some circumstances refers to this object in a Python namespace.

This typically refers to the “key” of the column as present in the .c collection of a selectable, e.g. sometable.c["somekey"] would return a Column with a .key of “somekey”.

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

Operate on an argument.

This is the lowest level of operation, raises NotImplementedError by default.

Overriding this on a subclass can allow common behavior to be applied to all operations. For example, overriding ColumnOperators to apply func.lower() to the left and right side:

op¶ – Operator callable.

*other¶ – the ‘other’ side of the operation. Will be a single scalar for most operations.

**kwargs¶ – modifiers. These may be passed by special operators such as ColumnOperators.contains().

inherited from the ClauseElement.params() method of ClauseElement

Return a copy with bindparam() elements replaced.

Returns a copy of this ClauseElement with bindparam() elements replaced with values taken from the given dictionary:

set of all columns we are proxying

as of 2.0 this is explicitly deannotated columns. previously it was effectively deannotated columns but wasn’t enforced. annotated columns should basically not go into sets if at all possible because their hashing behavior is very non-performant.

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

Reverse operate on an argument.

Usage is the same as operate().

Apply a ‘grouping’ to this ClauseElement.

This method is overridden by subclasses to return a “grouping” construct, i.e. parenthesis. In particular it’s used by “binary” expressions to provide a grouping around themselves when placed into a larger expression, as well as by select() constructs when placed into the FROM clause of another select(). (Note that subqueries should be normally created using the Select.alias() method, as many platforms require nested SELECT statements to be named).

As expressions are composed together, the application of self_group() is automatic - end-user code should never need to use this method directly. Note that SQLAlchemy’s clause constructs take operator precedence into account - so parenthesis might not be needed, for example, in an expression like x OR (y AND z) - AND takes precedence over OR.

The base self_group() method of ClauseElement just returns self.

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

inherited from the ClauseElement.unique_params() method of ClauseElement

Return a copy with bindparam() elements replaced.

Same functionality as ClauseElement.params(), except adds unique=True to affected bind parameters so that multiple statements can be used.

General purpose “column expression” argument.

Added in version 2.0.13.

This type is used for “column” kinds of expressions that typically represent a single SQL column expression, including ColumnElement, as well as ORM-mapped attributes that will have a __clause_element__() method.

inherits from sqlalchemy.sql.expression.Operators

Defines boolean, comparison, and other operators for ColumnElement expressions.

By default, all methods call down to operate() or reverse_operate(), passing in the appropriate operator function from the Python builtin operator module or a SQLAlchemy-specific operator function from sqlalchemy.expression.operators. For example the __eq__ function:

Where operators.eq is essentially:

The core column expression unit ColumnElement overrides Operators.operate() and others to return further ColumnElement constructs, so that the == operation above is replaced by a clause construct.

Redefining and Creating New Operators

TypeEngine.comparator_factory

Implement the + operator.

Implement the & operator.

Implement the == operator.

Implement the // operator.

Implement the >= operator.

Implement the [] operator.

Implement the > operator.

Implement the ~ operator.

Implement the <= operator.

implement the << operator.

Implement the < operator.

Implement the % operator.

Implement the * operator.

Implement the != operator.

Implement the - operator.

Implement the | operator.

Implement the + operator in reverse.

Implement the // operator in reverse.

Implement the % operator in reverse.

Implement the * operator in reverse.

implement the >> operator.

Implement the - operator in reverse.

Implement the / operator in reverse.

Operate on an argument.

Implement the - operator.

Implement the / operator.

Produce an all_() clause against the parent object.

Produce an any_() clause against the parent object.

Produce a asc() clause against the parent object.

Produce a between() clause against the parent object, given the lower and upper range.

Produce a bitwise AND operation, typically via the & operator.

Produce a bitwise LSHIFT operation, typically via the << operator.

Produce a bitwise NOT operation, typically via the ~ operator.

Produce a bitwise OR operation, typically via the | operator.

Produce a bitwise RSHIFT operation, typically via the >> operator.

Produce a bitwise XOR operation, typically via the ^ operator, or # for PostgreSQL.

Return a custom boolean operator.

Produce a collate() clause against the parent object, given the collation string.

Implement the ‘concat’ operator.

Implement the ‘contains’ operator.

Produce a desc() clause against the parent object.

Produce a distinct() clause against the parent object.

Implement the ‘endswith’ operator.

Implement the icontains operator, e.g. case insensitive version of ColumnOperators.contains().

Implement the iendswith operator, e.g. case insensitive version of ColumnOperators.endswith().

Implement the ilike operator, e.g. case insensitive LIKE.

Implement the in operator.

Implement the IS operator.

Implement the IS DISTINCT FROM operator.

Implement the IS NOT operator.

is_not_distinct_from()

Implement the IS NOT DISTINCT FROM operator.

Implement the IS NOT operator.

isnot_distinct_from()

Implement the IS NOT DISTINCT FROM operator.

Implement the istartswith operator, e.g. case insensitive version of ColumnOperators.startswith().

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

Implements a database-specific ‘regexp match’ operator.

Implements a database-specific ‘regexp replace’ operator.

Reverse operate on an argument.

Implement the startswith operator.

Hack, allows datetime objects to be compared on the LHS.

Implement the + operator.

In a column context, produces the clause a + b if the parent object has non-string affinity. If the parent object has a string affinity, produces the concatenation operator, a || b - see ColumnOperators.concat().

inherited from the sqlalchemy.sql.expression.Operators.__and__ method of Operators

Implement the & operator.

When used with SQL expressions, results in an AND operation, equivalent to and_(), that is:

Care should be taken when using & regarding operator precedence; the & operator has the highest precedence. The operands should be enclosed in parenthesis if they contain further sub expressions:

Implement the == operator.

In a column context, produces the clause a = b. If the target is None, produces a IS NULL.

Implement the // operator.

In a column context, produces the clause a / b, which is the same as “truediv”, but considers the result type to be integer.

Added in version 2.0.

Implement the >= operator.

In a column context, produces the clause a >= b.

Implement the [] operator.

This can be used by some database-specific types such as PostgreSQL ARRAY and HSTORE.

Implement the > operator.

In a column context, produces the clause a > b.

inherited from the sqlalchemy.sql.expression.Operators.__invert__ method of Operators

Implement the ~ operator.

When used with SQL expressions, results in a NOT operation, equivalent to not_(), that is:

Implement the <= operator.

In a column context, produces the clause a <= b.

implement the << operator.

Not used by SQLAlchemy core, this is provided for custom operator systems which want to use << as an extension point.

Implement the < operator.

In a column context, produces the clause a < b.

Implement the % operator.

In a column context, produces the clause a % b.

Implement the * operator.

In a column context, produces the clause a * b.

Implement the != operator.

In a column context, produces the clause a != b. If the target is None, produces a IS NOT NULL.

Implement the - operator.

In a column context, produces the clause -a.

inherited from the sqlalchemy.sql.expression.Operators.__or__ method of Operators

Implement the | operator.

When used with SQL expressions, results in an OR operation, equivalent to or_(), that is:

Care should be taken when using | regarding operator precedence; the | operator has the highest precedence. The operands should be enclosed in parenthesis if they contain further sub expressions:

Implement the + operator in reverse.

See ColumnOperators.__add__().

Implement the // operator in reverse.

See ColumnOperators.__floordiv__().

Implement the % operator in reverse.

See ColumnOperators.__mod__().

Implement the * operator in reverse.

See ColumnOperators.__mul__().

implement the >> operator.

Not used by SQLAlchemy core, this is provided for custom operator systems which want to use >> as an extension point.

Implement the - operator in reverse.

See ColumnOperators.__sub__().

Implement the / operator in reverse.

See ColumnOperators.__truediv__().

inherited from the sqlalchemy.sql.expression.Operators.__sa_operate__ method of Operators

Operate on an argument.

This is the lowest level of operation, raises NotImplementedError by default.

Overriding this on a subclass can allow common behavior to be applied to all operations. For example, overriding ColumnOperators to apply func.lower() to the left and right side:

op¶ – Operator callable.

*other¶ – the ‘other’ side of the operation. Will be a single scalar for most operations.

**kwargs¶ – modifiers. These may be passed by special operators such as ColumnOperators.contains().

Implement the - operator.

In a column context, produces the clause a - b.

Implement the / operator.

In a column context, produces the clause a / b, and considers the result type to be numeric.

Changed in version 2.0: The truediv operator against two integers is now considered to return a numeric value. Behavior on specific backends may vary.

Produce an all_() clause against the parent object.

See the documentation for all_() for examples.

be sure to not confuse the newer ColumnOperators.all_() method with the legacy version of this method, the Comparator.all() method that’s specific to ARRAY, which uses a different calling style.

Produce an any_() clause against the parent object.

See the documentation for any_() for examples.

be sure to not confuse the newer ColumnOperators.any_() method with the legacy version of this method, the Comparator.any() method that’s specific to ARRAY, which uses a different calling style.

Produce a asc() clause against the parent object.

Produce a between() clause against the parent object, given the lower and upper range.

Produce a bitwise AND operation, typically via the & operator.

Added in version 2.0.2.

Produce a bitwise LSHIFT operation, typically via the << operator.

Added in version 2.0.2.

Produce a bitwise NOT operation, typically via the ~ operator.

Added in version 2.0.2.

Produce a bitwise OR operation, typically via the | operator.

Added in version 2.0.2.

Produce a bitwise RSHIFT operation, typically via the >> operator.

Added in version 2.0.2.

Produce a bitwise XOR operation, typically via the ^ operator, or # for PostgreSQL.

Added in version 2.0.2.

inherited from the Operators.bool_op() method of Operators

Return a custom boolean operator.

This method is shorthand for calling Operators.op() and passing the Operators.op.is_comparison flag with True. A key advantage to using Operators.bool_op() is that when using column constructs, the “boolean” nature of the returned expression will be present for PEP 484 purposes.

Produce a collate() clause against the parent object, given the collation string.

Implement the ‘concat’ operator.

In a column context, produces the clause a || b, or uses the concat() operator on MySQL.

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

Produce a desc() clause against the parent object.

Produce a distinct() clause against the parent object.

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

Implement the ilike operator, e.g. case insensitive LIKE.

In a column context, produces an expression either of the form:

Or on backends that support the ILIKE operator:

other¶ – expression to be compared

optional escape character, renders the ESCAPE keyword, e.g.:

ColumnOperators.like()

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

Implement the IS operator.

Normally, IS is generated automatically when comparing to a value of None, which resolves to NULL. However, explicit usage of IS may be desirable if comparing to boolean values on certain platforms.

ColumnOperators.is_not()

Implement the IS DISTINCT FROM operator.

Renders “a IS DISTINCT FROM b” on most platforms; on some such as SQLite may render “a IS NOT b”.

Implement the IS NOT operator.

Normally, IS NOT is generated automatically when comparing to a value of None, which resolves to NULL. However, explicit usage of IS NOT may be desirable if comparing to boolean values on certain platforms.

Changed in version 1.4: The is_not() operator is renamed from isnot() in previous releases. The previous name remains available for backwards compatibility.

ColumnOperators.is_()

Implement the IS NOT DISTINCT FROM operator.

Renders “a IS NOT DISTINCT FROM b” on most platforms; on some such as SQLite may render “a IS b”.

Changed in version 1.4: The is_not_distinct_from() operator is renamed from isnot_distinct_from() in previous releases. The previous name remains available for backwards compatibility.

Implement the IS NOT operator.

Normally, IS NOT is generated automatically when comparing to a value of None, which resolves to NULL. However, explicit usage of IS NOT may be desirable if comparing to boolean values on certain platforms.

Changed in version 1.4: The is_not() operator is renamed from isnot() in previous releases. The previous name remains available for backwards compatibility.

ColumnOperators.is_()

Implement the IS NOT DISTINCT FROM operator.

Renders “a IS NOT DISTINCT FROM b” on most platforms; on some such as SQLite may render “a IS b”.

Changed in version 1.4: The is_not_distinct_from() operator is renamed from isnot_distinct_from() in previous releases. The previous name remains available for backwards compatibility.

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

Implement the like operator.

In a column context, produces the expression:

other¶ – expression to be compared

optional escape character, renders the ESCAPE keyword, e.g.:

ColumnOperators.ilike()

Implements a database-specific ‘match’ operator.

ColumnOperators.match() attempts to resolve to a MATCH-like function or operator provided by the backend. Examples include:

PostgreSQL - renders x @@ plainto_tsquery(y)

Changed in version 2.0: plainto_tsquery() is used instead of to_tsquery() for PostgreSQL now; for compatibility with other forms, see Full Text Search.

MySQL - renders MATCH (x) AGAINST (y IN BOOLEAN MODE)

match - MySQL specific construct with additional features.

Oracle Database - renders CONTAINS(x, y)

other backends may provide special implementations.

Backends without any special implementation will emit the operator as “MATCH”. This is compatible with SQLite, for example.

implement the NOT ILIKE operator.

This is equivalent to using negation with ColumnOperators.ilike(), i.e. ~x.ilike(y).

Changed in version 1.4: The not_ilike() operator is renamed from notilike() in previous releases. The previous name remains available for backwards compatibility.

ColumnOperators.ilike()

implement the NOT IN operator.

This is equivalent to using negation with ColumnOperators.in_(), i.e. ~x.in_(y).

In the case that other is an empty sequence, the compiler produces an “empty not in” expression. This defaults to the expression “1 = 1” to produce true in all cases. The create_engine.empty_in_strategy may be used to alter this behavior.

Changed in version 1.4: The not_in() operator is renamed from notin_() in previous releases. The previous name remains available for backwards compatibility.

Changed in version 1.2: The ColumnOperators.in_() and ColumnOperators.not_in() operators now produce a “static” expression for an empty IN sequence by default.

ColumnOperators.in_()

implement the NOT LIKE operator.

This is equivalent to using negation with ColumnOperators.like(), i.e. ~x.like(y).

Changed in version 1.4: The not_like() operator is renamed from notlike() in previous releases. The previous name remains available for backwards compatibility.

ColumnOperators.like()

implement the NOT ILIKE operator.

This is equivalent to using negation with ColumnOperators.ilike(), i.e. ~x.ilike(y).

Changed in version 1.4: The not_ilike() operator is renamed from notilike() in previous releases. The previous name remains available for backwards compatibility.

ColumnOperators.ilike()

implement the NOT IN operator.

This is equivalent to using negation with ColumnOperators.in_(), i.e. ~x.in_(y).

In the case that other is an empty sequence, the compiler produces an “empty not in” expression. This defaults to the expression “1 = 1” to produce true in all cases. The create_engine.empty_in_strategy may be used to alter this behavior.

Changed in version 1.4: The not_in() operator is renamed from notin_() in previous releases. The previous name remains available for backwards compatibility.

Changed in version 1.2: The ColumnOperators.in_() and ColumnOperators.not_in() operators now produce a “static” expression for an empty IN sequence by default.

ColumnOperators.in_()

implement the NOT LIKE operator.

This is equivalent to using negation with ColumnOperators.like(), i.e. ~x.like(y).

Changed in version 1.4: The not_like() operator is renamed from notlike() in previous releases. The previous name remains available for backwards compatibility.

ColumnOperators.like()

Produce a nulls_first() clause against the parent object.

Changed in version 1.4: The nulls_first() operator is renamed from nullsfirst() in previous releases. The previous name remains available for backwards compatibility.

Produce a nulls_last() clause against the parent object.

Changed in version 1.4: The nulls_last() operator is renamed from nullslast() in previous releases. The previous name remains available for backwards compatibility.

Produce a nulls_first() clause against the parent object.

Changed in version 1.4: The nulls_first() operator is renamed from nullsfirst() in previous releases. The previous name remains available for backwards compatibility.

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

inherited from the Operators.operate() method of Operators

Operate on an argument.

This is the lowest level of operation, raises NotImplementedError by default.

Overriding this on a subclass can allow common behavior to be applied to all operations. For example, overriding ColumnOperators to apply func.lower() to the left and right side:

op¶ – Operator callable.

*other¶ – the ‘other’ side of the operation. Will be a single scalar for most operations.

**kwargs¶ – modifiers. These may be passed by special operators such as ColumnOperators.contains().

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

Implements a database-specific ‘regexp replace’ operator.

ColumnOperators.regexp_replace() attempts to resolve to a REGEXP_REPLACE-like function provided by the backend, that usually emit the function REGEXP_REPLACE(). However, the specific regular expression syntax and flags available are not backend agnostic.

Regular expression replacement support is currently implemented for Oracle Database, PostgreSQL, MySQL 8 or greater and MariaDB. Support among third-party dialects may vary.

pattern¶ – The regular expression pattern string or column clause.

pattern¶ – The replacement string or column clause.

flags¶ – Any regular expression string flags to apply, passed as plain Python string only. These flags are backend specific. Some backends, like PostgreSQL and MariaDB, may alternatively specify the flags as part of the pattern.

Added in version 1.4.

Changed in version 1.4.48,: 2.0.18 Note that due to an implementation error, the “flags” parameter previously accepted SQL expression objects such as column expressions in addition to plain Python strings. This implementation did not work correctly with caching and was removed; strings only should be passed for the “flags” parameter, as these flags are rendered as literal inline values within SQL expressions.

ColumnOperators.regexp_match()

inherited from the Operators.reverse_operate() method of Operators

Reverse operate on an argument.

Usage is the same as operate().

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

Hack, allows datetime objects to be compared on the LHS.

inherits from sqlalchemy.sql.expression.ColumnElement

Represent a SQL EXTRACT clause, extract(field FROM expr).

inherits from sqlalchemy.sql.expression.SingletonConstant, sqlalchemy.sql.roles.ConstExprRole, sqlalchemy.sql.expression.ColumnElement

Represent the false keyword, or equivalent, in a SQL statement.

False_ is accessed as a constant via the false() function.

inherits from sqlalchemy.sql.expression.Generative, sqlalchemy.sql.expression.ColumnElement

Represent a function FILTER clause.

This is a special operator against aggregate and window functions, which controls which rows are passed to it. It’s supported only by certain database backends.

Invocation of FunctionFilter is via FunctionElement.filter():

FunctionElement.filter()

Produce an additional FILTER against the function.

Produce an OVER clause against this filtered function.

Apply a ‘grouping’ to this ClauseElement.

Produce a WITHIN GROUP (ORDER BY expr) clause against this function.

Produce an additional FILTER against the function.

This method adds additional criteria to the initial criteria set up by FunctionElement.filter().

Multiple criteria are joined together at SQL render time via AND.

Produce an OVER clause against this filtered function.

Used against aggregate or so-called “window” functions, for database backends that support window functions.

See over() for a full description.

Apply a ‘grouping’ to this ClauseElement.

This method is overridden by subclasses to return a “grouping” construct, i.e. parenthesis. In particular it’s used by “binary” expressions to provide a grouping around themselves when placed into a larger expression, as well as by select() constructs when placed into the FROM clause of another select(). (Note that subqueries should be normally created using the Select.alias() method, as many platforms require nested SELECT statements to be named).

As expressions are composed together, the application of self_group() is automatic - end-user code should never need to use this method directly. Note that SQLAlchemy’s clause constructs take operator precedence into account - so parenthesis might not be needed, for example, in an expression like x OR (y AND z) - AND takes precedence over OR.

The base self_group() method of ClauseElement just returns self.

Produce a WITHIN GROUP (ORDER BY expr) clause against this function.

inherits from sqlalchemy.sql.roles.LabeledColumnExprRole, sqlalchemy.sql.expression.NamedColumn

Represents a column label (AS).

Represent a label, as typically applied to any column-level element using the AS sql keyword.

Apply a ‘grouping’ to this ClauseElement.

Build an immutable unordered collection of unique elements.

Returns True when the argument is true, False otherwise. The builtins True and False are the only two instances of the class bool. The class bool is a subclass of the class int, and cannot be subclassed.

Apply a ‘grouping’ to this ClauseElement.

This method is overridden by subclasses to return a “grouping” construct, i.e. parenthesis. In particular it’s used by “binary” expressions to provide a grouping around themselves when placed into a larger expression, as well as by select() constructs when placed into the FROM clause of another select(). (Note that subqueries should be normally created using the Select.alias() method, as many platforms require nested SELECT statements to be named).

As expressions are composed together, the application of self_group() is automatic - end-user code should never need to use this method directly. Note that SQLAlchemy’s clause constructs take operator precedence into account - so parenthesis might not be needed, for example, in an expression like x OR (y AND z) - AND takes precedence over OR.

The base self_group() method of ClauseElement just returns self.

inherits from sqlalchemy.sql.expression.SingletonConstant, sqlalchemy.sql.roles.ConstExprRole, sqlalchemy.sql.expression.ColumnElement

Represent the NULL keyword in a SQL statement.

Null is accessed as a constant via the null() function.

Base of comparison and logical operators.

Implements base methods Operators.operate() and Operators.reverse_operate(), as well as Operators.__and__(), Operators.__or__(), Operators.__invert__().

Usually is used via its most common subclass ColumnOperators.

Implement the & operator.

Implement the ~ operator.

Implement the | operator.

Operate on an argument.

Return a custom boolean operator.

Produce a generic operator function.

Operate on an argument.

Reverse operate on an argument.

Implement the & operator.

When used with SQL expressions, results in an AND operation, equivalent to and_(), that is:

Care should be taken when using & regarding operator precedence; the & operator has the highest precedence. The operands should be enclosed in parenthesis if they contain further sub expressions:

Implement the ~ operator.

When used with SQL expressions, results in a NOT operation, equivalent to not_(), that is:

Implement the | operator.

When used with SQL expressions, results in an OR operation, equivalent to or_(), that is:

Care should be taken when using | regarding operator precedence; the | operator has the highest precedence. The operands should be enclosed in parenthesis if they contain further sub expressions:

Operate on an argument.

This is the lowest level of operation, raises NotImplementedError by default.

Overriding this on a subclass can allow common behavior to be applied to all operations. For example, overriding ColumnOperators to apply func.lower() to the left and right side:

op¶ – Operator callable.

*other¶ – the ‘other’ side of the operation. Will be a single scalar for most operations.

**kwargs¶ – modifiers. These may be passed by special operators such as ColumnOperators.contains().

Return a custom boolean operator.

This method is shorthand for calling Operators.op() and passing the Operators.op.is_comparison flag with True. A key advantage to using Operators.bool_op() is that when using column constructs, the “boolean” nature of the returned expression will be present for PEP 484 purposes.

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

Operate on an argument.

This is the lowest level of operation, raises NotImplementedError by default.

Overriding this on a subclass can allow common behavior to be applied to all operations. For example, overriding ColumnOperators to apply func.lower() to the left and right side:

op¶ – Operator callable.

*other¶ – the ‘other’ side of the operation. Will be a single scalar for most operations.

**kwargs¶ – modifiers. These may be passed by special operators such as ColumnOperators.contains().

Reverse operate on an argument.

Usage is the same as operate().

inherits from sqlalchemy.sql.expression.ColumnElement

Represent an OVER clause.

This is a special operator against a so-called “window” function, as well as any aggregate function, which produces results relative to the result set itself. Most modern SQL backends now support window functions.

The underlying expression object to which this Over object refers.

The underlying expression object to which this Over object refers.

inherits from sqlalchemy.sql.expression.SQLCoreOperations, sqlalchemy.sql.roles.ExpressionElementRole, sqlalchemy.util.langhelpers.TypingOnly

A type that may be used to indicate any SQL column element or object that acts in place of one.

SQLColumnExpression is a base of ColumnElement, as well as within the bases of ORM elements such as InstrumentedAttribute, and may be used in PEP 484 typing to indicate arguments or return values that should behave as column expressions.

Added in version 2.0.0b4.

inherits from sqlalchemy.sql.roles.DDLConstraintColumnRole, sqlalchemy.sql.roles.DDLExpressionRole, sqlalchemy.sql.roles.StatementOptionRole, sqlalchemy.sql.roles.WhereHavingRole, sqlalchemy.sql.roles.OrderByRole, sqlalchemy.sql.roles.FromClauseRole, sqlalchemy.sql.roles.SelectStatementRole, sqlalchemy.sql.roles.InElementRole, sqlalchemy.sql.expression.Generative, sqlalchemy.sql.expression.Executable, sqlalchemy.sql.expression.DQLDMLClauseElement, sqlalchemy.sql.roles.BinaryElementRole, sqlalchemy.inspection.Inspectable

Represent a literal SQL text fragment.

The TextClause construct is produced using the text() function; see that function for full documentation.

Establish the values and/or types of bound parameters within this TextClause construct.

Turn this TextClause object into a TextualSelect object that serves the same role as a SELECT statement.

Apply a ‘grouping’ to this ClauseElement.

Establish the values and/or types of bound parameters within this TextClause construct.

Given a text construct such as:

the TextClause.bindparams() method can be used to establish the initial value of :name and :timestamp, using simple keyword arguments:

Where above, new BindParameter objects will be generated with the names name and timestamp, and values of jack and datetime.datetime(2012, 10, 8, 15, 12, 5), respectively. The types will be inferred from the values given, in this case String and DateTime.

When specific typing behavior is needed, the positional *binds argument can be used in which to specify bindparam() constructs directly. These constructs must include at least the key argument, then an optional value and type:

Above, we specified the type of DateTime for the timestamp bind, and the type of String for the name bind. In the case of name we also set the default value of "jack".

Additional bound parameters can be supplied at statement execution time, e.g.:

The TextClause.bindparams() method can be called repeatedly, where it will reuse existing BindParameter objects to add new information. For example, we can call TextClause.bindparams() first with typing information, and a second time with value information, and it will be combined:

The TextClause.bindparams() method also supports the concept of unique bound parameters. These are parameters that are “uniquified” on name at statement compilation time, so that multiple text() constructs may be combined together without the names conflicting. To use this feature, specify the BindParameter.unique flag on each bindparam() object:

The above statement will render as:

Added in version 1.3.11: Added support for the BindParameter.unique flag to work with text() constructs.

Turn this TextClause object into a TextualSelect object that serves the same role as a SELECT statement.

The TextualSelect is part of the SelectBase hierarchy and can be embedded into another statement by using the TextualSelect.subquery() method to produce a Subquery object, which can then be SELECTed from.

This function essentially bridges the gap between an entirely textual SELECT statement and the SQL expression language concept of a “selectable”:

Above, we pass a series of column() elements to the TextClause.columns() method positionally. These column() elements now become first class elements upon the TextualSelect.selected_columns column collection, which then become part of the Subquery.c collection after TextualSelect.subquery() is invoked.

The column expressions we pass to TextClause.columns() may also be typed; when we do so, these TypeEngine objects become the effective return type of the column, so that SQLAlchemy’s result-set-processing systems may be used on the return values. This is often needed for types such as date or boolean types, as well as for unicode processing on some dialect configurations:

As a shortcut to the above syntax, keyword arguments referring to types alone may be used, if only type conversion is needed:

The positional form of TextClause.columns() also provides the unique feature of positional column targeting, which is particularly useful when using the ORM with complex textual queries. If we specify the columns from our model to TextClause.columns(), the result set will match to those columns positionally, meaning the name or origin of the column in the textual SQL doesn’t matter:

The TextClause.columns() method provides a direct route to calling FromClause.subquery() as well as SelectBase.cte() against a textual SELECT statement:

*cols¶ – A series of ColumnElement objects, typically Column objects from a Table or ORM level column-mapped attributes, representing a set of columns that this textual string will SELECT from.

**types¶ – A mapping of string names to TypeEngine type objects indicating the datatypes to use for names that are SELECTed from the textual string. Prefer to use the *cols argument as it also indicates positional ordering.

Apply a ‘grouping’ to this ClauseElement.

This method is overridden by subclasses to return a “grouping” construct, i.e. parenthesis. In particular it’s used by “binary” expressions to provide a grouping around themselves when placed into a larger expression, as well as by select() constructs when placed into the FROM clause of another select(). (Note that subqueries should be normally created using the Select.alias() method, as many platforms require nested SELECT statements to be named).

As expressions are composed together, the application of self_group() is automatic - end-user code should never need to use this method directly. Note that SQLAlchemy’s clause constructs take operator precedence into account - so parenthesis might not be needed, for example, in an expression like x OR (y AND z) - AND takes precedence over OR.

The base self_group() method of ClauseElement just returns self.

inherits from sqlalchemy.sql.expression.Cast

Represent a TRY_CAST expression.

Details on TryCast usage is at try_cast().

Data Casts and Type Coercion

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

inherits from sqlalchemy.sql.expression.ClauseList, sqlalchemy.sql.expression.ColumnElement

Represent a SQL tuple.

Apply a ‘grouping’ to this ClauseElement.

Apply a ‘grouping’ to this ClauseElement.

This method is overridden by subclasses to return a “grouping” construct, i.e. parenthesis. In particular it’s used by “binary” expressions to provide a grouping around themselves when placed into a larger expression, as well as by select() constructs when placed into the FROM clause of another select(). (Note that subqueries should be normally created using the Select.alias() method, as many platforms require nested SELECT statements to be named).

As expressions are composed together, the application of self_group() is automatic - end-user code should never need to use this method directly. Note that SQLAlchemy’s clause constructs take operator precedence into account - so parenthesis might not be needed, for example, in an expression like x OR (y AND z) - AND takes precedence over OR.

The base self_group() method of ClauseElement just returns self.

inherits from sqlalchemy.sql.expression.ColumnElement

Represent a WITHIN GROUP (ORDER BY) clause.

This is a special operator against so-called “ordered set aggregate” and “hypothetical set aggregate” functions, including percentile_cont(), rank(), dense_rank(), etc.

It’s supported only by certain database backends, such as PostgreSQL, Oracle Database and MS SQL Server.

The WithinGroup construct extracts its type from the method FunctionElement.within_group_type(). If this returns None, the function’s .type is used.

Produce a FILTER clause against this function.

Produce an OVER clause against this WithinGroup construct.

Produce a FILTER clause against this function.

Produce an OVER clause against this WithinGroup construct.

This function has the same signature as that of FunctionElement.over().

inherits from sqlalchemy.sql.expression.ColumnElement

Mixin that defines a ColumnElement as a wrapper with special labeling behavior for an expression that already has a name.

Added in version 1.4.

Improved column labeling for simple column expressions using CAST or similar

inherits from sqlalchemy.sql.expression.SingletonConstant, sqlalchemy.sql.roles.ConstExprRole, sqlalchemy.sql.expression.ColumnElement

Represent the true keyword, or equivalent, in a SQL statement.

True_ is accessed as a constant via the true() function.

inherits from sqlalchemy.sql.expression.WrapsColumnExpression

Represent a Python-side type-coercion wrapper.

TypeCoerce supplies the type_coerce() function; see that function for usage details.

Apply a ‘grouping’ to this ClauseElement.

Apply a ‘grouping’ to this ClauseElement.

This method is overridden by subclasses to return a “grouping” construct, i.e. parenthesis. In particular it’s used by “binary” expressions to provide a grouping around themselves when placed into a larger expression, as well as by select() constructs when placed into the FROM clause of another select(). (Note that subqueries should be normally created using the Select.alias() method, as many platforms require nested SELECT statements to be named).

As expressions are composed together, the application of self_group() is automatic - end-user code should never need to use this method directly. Note that SQLAlchemy’s clause constructs take operator precedence into account - so parenthesis might not be needed, for example, in an expression like x OR (y AND z) - AND takes precedence over OR.

The base self_group() method of ClauseElement just returns self.

inherits from sqlalchemy.sql.expression.ColumnElement

Define a ‘unary’ expression.

A unary expression has a single column expression and an operator. The operator can be placed on the left (where it is called the ‘operator’) or right (where it is called the ‘modifier’) of the column expression.

UnaryExpression is the basis for several unary operators including those used by desc(), asc(), distinct(), nulls_first() and nulls_last().

Apply a ‘grouping’ to this ClauseElement.

Apply a ‘grouping’ to this ClauseElement.

This method is overridden by subclasses to return a “grouping” construct, i.e. parenthesis. In particular it’s used by “binary” expressions to provide a grouping around themselves when placed into a larger expression, as well as by select() constructs when placed into the FROM clause of another select(). (Note that subqueries should be normally created using the Select.alias() method, as many platforms require nested SELECT statements to be named).

As expressions are composed together, the application of self_group() is automatic - end-user code should never need to use this method directly. Note that SQLAlchemy’s clause constructs take operator precedence into account - so parenthesis might not be needed, for example, in an expression like x OR (y AND z) - AND takes precedence over OR.

The base self_group() method of ClauseElement just returns self.

Standalone utility functions imported from the sqlalchemy namespace to improve support by type checkers.

Types a column or ORM class as not nullable.

Types a column or ORM class as nullable.

Types a column or ORM class as not nullable.

This can be used in select and other contexts to express that the value of a column cannot be null, for example due to a where condition on a nullable column:

At runtime this method returns the input unchanged.

Added in version 2.0.20.

Types a column or ORM class as nullable.

This can be used in select and other contexts to express that the value of a column can be null, for example due to an outer join:

At runtime this method returns the input unchanged.

Added in version 2.0.20.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from sqlalchemy import and_

stmt = select(users_table).where(
    and_(users_table.c.name == "wendy", users_table.c.enrolled == True)
)
```

Example 2 (csharp):
```csharp
stmt = select(users_table).where(
    (users_table.c.name == "wendy") & (users_table.c.enrolled == True)
)
```

Example 3 (csharp):
```csharp
stmt = (
    select(users_table)
    .where(users_table.c.name == "wendy")
    .where(users_table.c.enrolled == True)
)
```

Example 4 (python):
```python
from sqlalchemy import true

criteria = and_(true(), *expressions)
```

---
