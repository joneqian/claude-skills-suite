# Sqlalchemy - Types

**Pages:** 2

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/core/custom_types.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Core
    - Project Versions
- Custom Types¶
- Overriding Type Compilation¶
- Augmenting Existing Types¶
- TypeDecorator Recipes¶
  - Coercing Encoded Strings to Unicode¶
  - Rounding Numerics¶

Home | Download this Documentation

Home | Download this Documentation

A variety of methods exist to redefine the behavior of existing types as well as to provide new ones.

A frequent need is to force the “string” version of a type, that is the one rendered in a CREATE TABLE statement or other SQL function like CAST, to be changed. For example, an application may want to force the rendering of BINARY for all platforms except for one, in which it wants BLOB to be rendered. Usage of an existing generic type, in this case LargeBinary, is preferred for most use cases. But to control types more accurately, a compilation directive that is per-dialect can be associated with any type:

The above code allows the usage of BINARY, which will produce the string BINARY against all backends except SQLite, in which case it will produce BLOB.

See the section Changing Compilation of Types, a subsection of Custom SQL Constructs and Compilation Extension, for additional examples.

The TypeDecorator allows the creation of custom types which add bind-parameter and result-processing behavior to an existing type object. It is used when additional in-Python marshalling of data to and/or from the database is required.

The bind- and result-processing of TypeDecorator is in addition to the processing already performed by the hosted type, which is customized by SQLAlchemy on a per-DBAPI basis to perform processing specific to that DBAPI. While it is possible to replace this handling for a given type through direct subclassing, it is never needed in practice and SQLAlchemy no longer supports this as a public use case.

The TypeDecorator can be used to provide a consistent means of converting some type of value as it is passed into and out of the database. When using the ORM, a similar technique exists for converting user data from arbitrary formats which is to use the validates() decorator. This technique may be more appropriate when data coming into an ORM model needs to be normalized in some way that is specific to the business case and isn’t as generic as a datatype.

Allows the creation of types which add additional functionality to an existing type.

inherits from sqlalchemy.sql.expression.SchemaEventTarget, sqlalchemy.types.ExternalType, sqlalchemy.types.TypeEngine

Allows the creation of types which add additional functionality to an existing type.

This method is preferred to direct subclassing of SQLAlchemy’s built-in types as it ensures that all required functionality of the underlying type is kept in place.

The class-level impl attribute is required, and can reference any TypeEngine class. Alternatively, the load_dialect_impl() method can be used to provide different type classes based on the dialect given; in this case, the impl variable can reference TypeEngine as a placeholder.

The TypeDecorator.cache_ok class-level flag indicates if this custom TypeDecorator is safe to be used as part of a cache key. This flag defaults to None which will initially generate a warning when the SQL compiler attempts to generate a cache key for a statement that uses this type. If the TypeDecorator is not guaranteed to produce the same bind/result behavior and SQL generation every time, this flag should be set to False; otherwise if the class produces the same behavior each time, it may be set to True. See TypeDecorator.cache_ok for further notes on how this works.

Types that receive a Python type that isn’t similar to the ultimate type used may want to define the TypeDecorator.coerce_compared_value() method. This is used to give the expression system a hint when coercing Python objects into bind parameters within expressions. Consider this expression:

Above, if “somecol” is an Integer variant, it makes sense that we’re doing date arithmetic, where above is usually interpreted by databases as adding a number of days to the given date. The expression system does the right thing by not attempting to coerce the “date()” value into an integer-oriented bind parameter.

However, in the case of TypeDecorator, we are usually changing an incoming Python type to something new - TypeDecorator by default will “coerce” the non-typed side to be the same type as itself. Such as below, we define an “epoch” type that stores a date value as an integer:

Our expression of somecol + date with the above type will coerce the “date” on the right side to also be treated as MyEpochType.

This behavior can be overridden via the TypeDecorator.coerce_compared_value() method, which returns a type that should be used for the value of the expression. Below we set it such that an integer value will be treated as an Integer, and any other value is assumed to be a date and will be treated as a MyEpochType:

Note that the behavior of coerce_compared_value is not inherited by default from that of the base type. If the TypeDecorator is augmenting a type that requires special logic for certain types of operators, this method must be overridden. A key example is when decorating the JSON and JSONB types; the default rules of TypeEngine.coerce_compared_value() should be used in order to deal with operators like index operations:

Without the above step, index operations such as mycol['foo'] will cause the index value 'foo' to be JSON encoded.

Similarly, when working with the ARRAY datatype, the type coercion for index operations (e.g. mycol[5]) is also handled by TypeDecorator.coerce_compared_value(), where again a simple override is sufficient unless special rules are needed for particular operators:

Indicate if statements using this ExternalType are “safe to cache”.

Operate on an argument.

Reverse operate on an argument.

Construct a TypeDecorator.

Given a bind value (i.e. a BindParameter instance), return a SQL expression which will typically wrap the given parameter.

Provide a bound value processing function for the given Dialect.

coerce_compared_value()

Suggest a type for a ‘coerced’ Python value in an expression.

Specify those Python types which should be coerced at the expression level to “IS <constant>” when compared using == (and same for IS NOT in conjunction with !=).

Given a SELECT column expression, return a wrapping SQL expression.

Given two values, compare them for equality.

Produce a copy of this TypeDecorator instance.

Return the DBAPI type object represented by this TypeDecorator.

Provide a literal processing function for the given Dialect.

Return a TypeEngine object corresponding to a dialect.

Receive a bound parameter value to be converted.

process_literal_param()

Receive a literal parameter value to be rendered inline within a statement.

process_result_value()

Receive a result-row column value to be converted.

Provide a result value processing function for the given Dialect.

Return a dialect-specific TypeEngine instance for this TypeDecorator.

inherited from the ExternalType.cache_ok attribute of ExternalType

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

inherits from sqlalchemy.types.Comparator

A Comparator that is specific to TypeDecorator.

User-defined TypeDecorator classes should not typically need to modify this.

Operate on an argument.

This is the lowest level of operation, raises NotImplementedError by default.

Overriding this on a subclass can allow common behavior to be applied to all operations. For example, overriding ColumnOperators to apply func.lower() to the left and right side:

op¶ – Operator callable.

*other¶ – the ‘other’ side of the operation. Will be a single scalar for most operations.

**kwargs¶ – modifiers. These may be passed by special operators such as ColumnOperators.contains().

Reverse operate on an argument.

Usage is the same as operate().

Construct a TypeDecorator.

Arguments sent here are passed to the constructor of the class assigned to the impl class level attribute, assuming the impl is a callable, and the resulting object is assigned to the self.impl instance attribute (thus overriding the class attribute of the same name).

If the class level impl is not a callable (the unusual case), it will be assigned to the same instance attribute ‘as-is’, ignoring those arguments passed to the constructor.

Subclasses can override this to customize the generation of self.impl entirely.

Given a bind value (i.e. a BindParameter instance), return a SQL expression which will typically wrap the given parameter.

This method is called during the SQL compilation phase of a statement, when rendering a SQL string. It is not necessarily called against specific values, and should not be confused with the TypeDecorator.process_bind_param() method, which is the more typical method that processes the actual value passed to a particular parameter at statement execution time.

Subclasses of TypeDecorator can override this method to provide custom bind expression behavior for the type. This implementation will replace that of the underlying implementation type.

Provide a bound value processing function for the given Dialect.

This is the method that fulfills the TypeEngine contract for bound value conversion which normally occurs via the TypeEngine.bind_processor() method.

User-defined subclasses of TypeDecorator should not implement this method, and should instead implement TypeDecorator.process_bind_param() so that the “inner” processing provided by the implementing type is maintained.

dialect¶ – Dialect instance in use.

Suggest a type for a ‘coerced’ Python value in an expression.

By default, returns self. This method is called by the expression system when an object using this type is on the left or right side of an expression against a plain Python object which does not yet have a SQLAlchemy type assigned:

Where above, if somecolumn uses this type, this method will be called with the value operator.add and 35. The return value is whatever SQLAlchemy type should be used for 35 for this particular operation.

Specify those Python types which should be coerced at the expression level to “IS <constant>” when compared using == (and same for IS NOT in conjunction with !=).

For most SQLAlchemy types, this includes NoneType, as well as bool.

TypeDecorator modifies this list to only include NoneType, as typedecorator implementations that deal with boolean types are common.

Custom TypeDecorator classes can override this attribute to return an empty tuple, in which case no values will be coerced to constants.

Given a SELECT column expression, return a wrapping SQL expression.

This method is called during the SQL compilation phase of a statement, when rendering a SQL string. It is not called against specific values, and should not be confused with the TypeDecorator.process_result_value() method, which is the more typical method that processes the actual value returned in a result row subsequent to statement execution time.

Subclasses of TypeDecorator can override this method to provide custom column expression behavior for the type. This implementation will replace that of the underlying implementation type.

See the description of TypeEngine.column_expression() for a complete description of the method’s use.

Base class for custom comparison operations defined at the type level. See TypeEngine.comparator_factory.

Given two values, compare them for equality.

By default this calls upon TypeEngine.compare_values() of the underlying “impl”, which in turn usually uses the Python equals operator ==.

This function is used by the ORM to compare an original-loaded value with an intercepted “changed” value, to determine if a net change has occurred.

Produce a copy of this TypeDecorator instance.

This is a shallow copy and is provided to fulfill part of the TypeEngine contract. It usually does not need to be overridden unless the user-defined TypeDecorator has local state that should be deep-copied.

Return the DBAPI type object represented by this TypeDecorator.

By default this calls upon TypeEngine.get_dbapi_type() of the underlying “impl”.

Provide a literal processing function for the given Dialect.

This is the method that fulfills the TypeEngine contract for literal value conversion which normally occurs via the TypeEngine.literal_processor() method.

User-defined subclasses of TypeDecorator should not implement this method, and should instead implement TypeDecorator.process_literal_param() so that the “inner” processing provided by the implementing type is maintained.

Return a TypeEngine object corresponding to a dialect.

This is an end-user override hook that can be used to provide differing types depending on the given dialect. It is used by the TypeDecorator implementation of type_engine() to help determine what type should ultimately be returned for a given TypeDecorator.

By default returns self.impl.

Receive a bound parameter value to be converted.

Custom subclasses of TypeDecorator should override this method to provide custom behaviors for incoming data values. This method is called at statement execution time and is passed the literal Python data value which is to be associated with a bound parameter in the statement.

The operation could be anything desired to perform custom behavior, such as transforming or serializing data. This could also be used as a hook for validating logic.

value¶ – Data to operate upon, of any type expected by this method in the subclass. Can be None.

dialect¶ – the Dialect in use.

Augmenting Existing Types

TypeDecorator.process_result_value()

Receive a literal parameter value to be rendered inline within a statement.

This method is called during the SQL compilation phase of a statement, when rendering a SQL string. Unlike other SQL compilation methods, it is passed a specific Python value to be rendered as a string. However it should not be confused with the TypeDecorator.process_bind_param() method, which is the more typical method that processes the actual value passed to a particular parameter at statement execution time.

Custom subclasses of TypeDecorator should override this method to provide custom behaviors for incoming data values that are in the special case of being rendered as literals.

The returned string will be rendered into the output string.

Receive a result-row column value to be converted.

Custom subclasses of TypeDecorator should override this method to provide custom behaviors for data values being received in result rows coming from the database. This method is called at result fetching time and is passed the literal Python data value that’s extracted from a database result row.

The operation could be anything desired to perform custom behavior, such as transforming or deserializing data.

value¶ – Data to operate upon, of any type expected by this method in the subclass. Can be None.

dialect¶ – the Dialect in use.

Augmenting Existing Types

TypeDecorator.process_bind_param()

Provide a result value processing function for the given Dialect.

This is the method that fulfills the TypeEngine contract for bound value conversion which normally occurs via the TypeEngine.result_processor() method.

User-defined subclasses of TypeDecorator should not implement this method, and should instead implement TypeDecorator.process_result_value() so that the “inner” processing provided by the implementing type is maintained.

dialect¶ – Dialect instance in use.

coltype¶ – A SQLAlchemy data type

The type of the None singleton.

Return a dialect-specific TypeEngine instance for this TypeDecorator.

In most cases this returns a dialect-adapted form of the TypeEngine type represented by self.impl. Makes usage of dialect_impl(). Behavior can be customized here by overriding load_dialect_impl().

A few key TypeDecorator recipes follow.

A common source of confusion regarding the Unicode type is that it is intended to deal only with Python unicode objects on the Python side, meaning values passed to it as bind parameters must be of the form u'some string' if using Python 2 and not 3. The encoding/decoding functions it performs are only to suit what the DBAPI in use requires, and are primarily a private implementation detail.

The use case of a type that can safely receive Python bytestrings, that is strings that contain non-ASCII characters and are not u'' objects in Python 2, can be achieved using a TypeDecorator which coerces as needed:

Some database connectors like those of SQL Server choke if a Decimal is passed with too many decimal places. Here’s a recipe that rounds them down:

Timestamps in databases should always be stored in a timezone-agnostic way. For most databases, this means ensuring a timestamp is first in the UTC timezone before it is stored, then storing it as timezone-naive (that is, without any timezone associated with it; UTC is assumed to be the “implicit” timezone). Alternatively, database-specific types like PostgreSQLs “TIMESTAMP WITH TIMEZONE” are often preferred for their richer functionality; however, storing as plain UTC will work on all databases and drivers. When a timezone-intelligent database type is not an option or is not preferred, the TypeDecorator can be used to create a datatype that convert timezone aware timestamps into timezone naive and back again. Below, Python’s built-in datetime.timezone.utc timezone is used to normalize and denormalize:

Since version 2.0 the built-in Uuid type that behaves similarly should be preferred. This example is presented just as an example of a type decorator that receives and returns python objects.

Receives and returns Python uuid() objects. Uses the PG UUID type when using PostgreSQL, UNIQUEIDENTIFIER when using MSSQL, CHAR(32) on other backends, storing them in stringified format. The GUIDHyphens version stores the value with hyphens instead of just the hex string, using a CHAR(36) type:

When declaring ORM mappings using Annotated Declarative Table mappings, the custom GUID type defined above may be associated with the Python uuid.UUID datatype by adding it to the type annotation map, which is typically defined on the DeclarativeBase class:

With the above configuration, ORM mapped classes which extend from Base may refer to Python uuid.UUID in annotations which will make use of GUID automatically:

Customizing the Type Map

This type uses simplejson to marshal Python data structures to/from JSON. Can be modified to use Python’s builtin json encoder:

The ORM by default will not detect “mutability” on such a type as above - meaning, in-place changes to values will not be detected and will not be flushed. Without further steps, you instead would need to replace the existing value with a new one on each parent object to detect changes:

The above limitation may be fine, as many applications may not require that the values are ever mutated once created. For those which do have this requirement, support for mutability is best applied using the sqlalchemy.ext.mutable extension. For a dictionary-oriented JSON structure, we can apply this as:

The default behavior of TypeDecorator is to coerce the “right hand side” of any expression into the same type. For a type like JSON, this means that any operator used must make sense in terms of JSON. For some cases, users may wish for the type to behave like JSON in some circumstances, and as plain text in others. One example is if one wanted to handle the LIKE operator for the JSON type. LIKE makes no sense against a JSON structure, but it does make sense against the underlying textual representation. To get at this with a type like JSONEncodedDict, we need to coerce the column to a textual form using cast() or type_coerce() before attempting to use this operator:

TypeDecorator provides a built-in system for working up type translations like these based on operators. If we wanted to frequently use the LIKE operator with our JSON object interpreted as a string, we can build it into the type by overriding the TypeDecorator.coerce_compared_value() method:

Above is just one approach to handling an operator like “LIKE”. Other applications may wish to raise NotImplementedError for operators that have no meaning with a JSON object such as “LIKE”, rather than automatically coercing to text.

As seen in the section Augmenting Existing Types, SQLAlchemy allows Python functions to be invoked both when parameters are sent to a statement, as well as when result rows are loaded from the database, to apply transformations to the values as they are sent to or from the database. It is also possible to define SQL-level transformations as well. The rationale here is when only the relational database contains a particular series of functions that are necessary to coerce incoming and outgoing data between an application and persistence format. Examples include using database-defined encryption/decryption functions, as well as stored procedures that handle geographic data.

Any TypeEngine, UserDefinedType or TypeDecorator subclass can include implementations of TypeEngine.bind_expression() and/or TypeEngine.column_expression(), which when defined to return a non-None value should return a ColumnElement expression to be injected into the SQL statement, either surrounding bound parameters or a column expression.

As SQL-level result processing features are intended to assist with coercing data from a SELECT statement into result rows in Python, the TypeEngine.column_expression() conversion method is applied only to the outermost columns clause in a SELECT; it does not apply to columns rendered inside of subqueries, as these column expressions are not directly delivered to a result. The expression should not be applied to both, as this would lead to double-conversion of columns, and the “outermost” level rather than the “innermost” level is used so that conversion routines don’t interfere with the internal expressions used by the statement, and so that only data that’s outgoing to a result row is actually subject to conversion, which is consistent with the result row processing functionality provided by TypeDecorator.process_result_value().

For example, to build a Geometry type which will apply the PostGIS function ST_GeomFromText to all outgoing values and the function ST_AsText to all incoming data, we can create our own subclass of UserDefinedType which provides these methods in conjunction with func:

We can apply the Geometry type into Table metadata and use it in a select() construct:

The resulting SQL embeds both functions as appropriate. ST_AsText is applied to the columns clause so that the return value is run through the function before passing into a result set, and ST_GeomFromText is run on the bound parameter so that the passed-in value is converted:

The TypeEngine.column_expression() method interacts with the mechanics of the compiler such that the SQL expression does not interfere with the labeling of the wrapped expression. Such as, if we rendered a select() against a label() of our expression, the string label is moved to the outside of the wrapped expression:

Another example is we decorate BYTEA to provide a PGPString, which will make use of the PostgreSQL pgcrypto extension to encrypt/decrypt values transparently:

The pgp_sym_encrypt and pgp_sym_decrypt functions are applied to the INSERT and SELECT statements:

SQLAlchemy Core defines a fixed set of expression operators available to all column expressions. Some of these operations have the effect of overloading Python’s built-in operators; examples of such operators include ColumnOperators.__eq__() (table.c.somecolumn == 'foo'), ColumnOperators.__invert__() (~table.c.flag), and ColumnOperators.__add__() (table.c.x + table.c.y). Other operators are exposed as explicit methods on column expressions, such as ColumnOperators.in_() (table.c.value.in_(['x', 'y'])) and ColumnOperators.like() (table.c.value.like('%ed%')).

When the need arises for a SQL operator that isn’t directly supported by the already supplied methods above, the most expedient way to produce this operator is to use the Operators.op() method on any SQL expression object; this method is given a string representing the SQL operator to render, and the return value is a Python callable that accepts any arbitrary right-hand side expression:

When making use of custom SQL types, there is also a means of implementing custom operators as above that are automatically present upon any column expression that makes use of that column type, without the need to directly call Operators.op() each time the operator is to be used.

To achieve this, a SQL expression construct consults the TypeEngine object associated with the construct in order to determine the behavior of the built-in operators as well as to look for new methods that may have been invoked. TypeEngine defines a “comparison” object implemented by the Comparator class to provide the base behavior for SQL operators, and many specific types provide their own sub-implementations of this class. User-defined Comparator implementations can be built directly into a simple subclass of a particular type in order to override or define new operations. Below, we create a Integer subclass which overrides the ColumnOperators.__add__() operator, which in turn uses Operators.op() to produce the custom SQL itself:

The above configuration creates a new class MyInt, which establishes the TypeEngine.comparator_factory attribute as referring to a new class, subclassing the Comparator class associated with the Integer type.

The implementation for ColumnOperators.__add__() is consulted by an owning SQL expression, by instantiating the Comparator with itself as the expr attribute. This attribute may be used when the implementation needs to refer to the originating ColumnElement object directly:

New methods added to a Comparator are exposed on an owning SQL expression object using a dynamic lookup scheme, which exposes methods added to Comparator onto the owning ColumnElement expression construct. For example, to add a log() function to integers:

Using the above type:

When using Operators.op() for comparison operations that return a boolean result, the Operators.op.is_comparison flag should be set to True:

Unary operations are also possible. For example, to add an implementation of the PostgreSQL factorial operator, we combine the UnaryExpression construct along with a custom_op to produce the factorial expression:

Using the above type:

TypeEngine.comparator_factory

The UserDefinedType class is provided as a simple base class for defining entirely new database types. Use this to represent native database types not known by SQLAlchemy. If only Python translation behavior is needed, use TypeDecorator instead.

Base for user defined types.

inherits from sqlalchemy.types.ExternalType, sqlalchemy.types.TypeEngineMixin, sqlalchemy.types.TypeEngine, sqlalchemy.util.langhelpers.EnsureKWArg

Base for user defined types.

This should be the base of new types. Note that for most cases, TypeDecorator is probably more appropriate:

Once the type is made, it’s immediately usable:

The get_col_spec() method will in most cases receive a keyword argument type_expression which refers to the owning expression of the type as being compiled, such as a Column or cast() construct. This keyword is only sent if the method accepts keyword arguments (e.g. **kw) in its argument signature; introspection is used to check for this in order to support legacy forms of this function.

The UserDefinedType.cache_ok class-level flag indicates if this custom UserDefinedType is safe to be used as part of a cache key. This flag defaults to None which will initially generate a warning when the SQL compiler attempts to generate a cache key for a statement that uses this type. If the UserDefinedType is not guaranteed to produce the same bind/result behavior and SQL generation every time, this flag should be set to False; otherwise if the class produces the same behavior each time, it may be set to True. See UserDefinedType.cache_ok for further notes on how this works.

Added in version 1.4.28: Generalized the ExternalType.cache_ok flag so that it is available for both TypeDecorator as well as UserDefinedType.

Indicate if statements using this ExternalType are “safe to cache”.

coerce_compared_value()

Suggest a type for a ‘coerced’ Python value in an expression.

a regular expression that indicates method names for which the method should accept **kw arguments.

inherited from the ExternalType.cache_ok attribute of ExternalType

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

Default behavior for UserDefinedType is the same as that of TypeDecorator; by default it returns self, assuming the compared value should be coerced into the same type as this one. See TypeDecorator.coerce_compared_value() for more detail.

a regular expression that indicates method names for which the method should accept **kw arguments.

The class will scan for methods matching the name template and decorate them if necessary to ensure **kw parameters are accepted.

It is important to note that database types which are modified to have additional in-Python behaviors, including types based on TypeDecorator as well as other user-defined subclasses of datatypes, do not have any representation within a database schema. When using database the introspection features described at Reflecting Database Objects, SQLAlchemy makes use of a fixed mapping which links the datatype information reported by a database server to a SQLAlchemy datatype object. For example, if we look inside of a PostgreSQL schema at the definition for a particular database column, we might receive back the string "VARCHAR". SQLAlchemy’s PostgreSQL dialect has a hardcoded mapping which links the string name "VARCHAR" to the SQLAlchemy VARCHAR class, and that’s how when we emit a statement like Table('my_table', m, autoload_with=engine), the Column object within it would have an instance of VARCHAR present inside of it.

The implication of this is that if a Table object makes use of type objects that don’t correspond directly to the database-native type name, if we create a new Table object against a new MetaData collection for this database table elsewhere using reflection, it will not have this datatype. For example:

Above, we made use of PickleType, which is a TypeDecorator that works on top of the LargeBinary datatype, which on SQLite corresponds to the database type BLOB. In the CREATE TABLE, we see that the BLOB datatype is used. The SQLite database knows nothing about the PickleType we’ve used.

If we look at the datatype of my_table.c.data.type, as this is a Python object that was created by us directly, it is PickleType:

However, if we create another instance of Table using reflection, the use of PickleType is not represented in the SQLite database we’ve created; we instead get back BLOB:

Typically, when an application defines explicit Table metadata with custom types, there is no need to use table reflection because the necessary Table metadata is already present. However, for the case where an application, or a combination of them, need to make use of both explicit Table metadata which includes custom, Python-level datatypes, as well as Table objects which set up their Column objects as reflected from the database, which nevertheless still need to exhibit the additional Python behaviors of the custom datatypes, additional steps must be taken to allow this.

The most straightforward is to override specific columns as described at Overriding Reflected Columns. In this technique, we simply use reflection in combination with explicit Column objects for those columns for which we want to use a custom or decorated datatype:

The my_reflected_table object above is reflected, and will load the definition of the “id” column from the SQLite database. But for the “data” column, we’ve overridden the reflected object with an explicit Column definition that includes our desired in-Python datatype, the PickleType. The reflection process will leave this Column object intact:

A more elaborate way to convert from database-native type objects to custom datatypes is to use the DDLEvents.column_reflect() event handler. If for example we knew that we wanted all BLOB datatypes to in fact be PickleType, we could set up a rule across the board:

When the above code is invoked before any table reflection occurs (note also it should be invoked only once in the application, as it is a global rule), upon reflecting any Table that includes a column with a BLOB datatype, the resulting datatype will be stored in the Column object as PickleType.

In practice, the above event-based approach would likely have additional rules in order to affect only those columns where the datatype is important, such as a lookup table of table names and possibly column names, or other heuristics in order to accurately determine which columns should be established with an in Python datatype.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import BINARY


@compiles(BINARY, "sqlite")
def compile_binary_sqlite(type_, compiler, **kw):
    return "BLOB"
```

Example 2 (python):
```python
import sqlalchemy.types as types


class MyType(types.TypeDecorator):
    """Prefixes Unicode values with "PREFIX:" on the way in and
    strips it off on the way out.
    """

    impl = types.Unicode

    cache_ok = True

    def process_bind_param(self, value, dialect):
        return "PREFIX:" + value

    def process_result_value(self, value, dialect):
        return value[7:]

    def copy(self, **kw):
        return MyType(self.impl.length)
```

Example 3 (unknown):
```unknown
mytable.c.somecol + datetime.date(2009, 5, 15)
```

Example 4 (python):
```python
class MyEpochType(types.TypeDecorator):
    impl = types.Integer

    cache_ok = True

    epoch = datetime.date(1970, 1, 1)

    def process_bind_param(self, value, dialect):
        return (value - self.epoch).days

    def process_result_value(self, value, dialect):
        return self.epoch + timedelta(days=value)
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/core/type_api.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Core
    - Project Versions
- Base Type API¶

Home | Download this Documentation

Home | Download this Documentation

A mixin that marks a type as supporting ‘concatenation’, typically strings.

mixin that defines attributes and behaviors specific to third-party datatypes.

A mixin that marks a type as supporting indexing operations, such as array or JSON structures.

The ultimate base class for all SQL datatypes.

deprecated. symbol is present for backwards-compatibility with workaround recipes, however this actual type should not be used.

inherits from sqlalchemy.sql.visitors.Visitable, typing.Generic

The ultimate base class for all SQL datatypes.

Common subclasses of TypeEngine include String, Integer, and Boolean.

For an overview of the SQLAlchemy typing system, see SQL Datatype Objects.

Operate on an argument.

Reverse operate on an argument.

Produce an “adapted” form of this type, given an “impl” class to work with.

Return an instance of the generic type corresponding to this type using heuristic rule. The method may be overridden if this heuristic rule is not sufficient.

Given a bind value (i.e. a BindParameter instance), return a SQL expression in its place.

Return a conversion function for processing bind values.

coerce_compared_value()

Suggest a type for a ‘coerced’ Python value in an expression.

Given a SELECT column expression, return a wrapping SQL expression.

Compare two values for equality.

Produce a string-compiled form of this TypeEngine.

Return a dialect-specific implementation for this TypeEngine.

Return a copy of this type which has the should_evaluate_none flag set to True.

Return the corresponding type object from the underlying DB-API, if any.

Flag, if False, means values from this type aren’t hashable.

Return a conversion function for processing literal values that are to be rendered directly without using binds.

Render bind casts for BindTyping.RENDER_CASTS mode.

render casts when rendering a value as an inline literal, e.g. with TypeEngine.literal_processor().

Return a conversion function for processing result row values.

If True, the Python constant None is considered to be handled explicitly by this type.

A sorting function that can be passed as the key to sorted.

Produce a copy of this type object that will utilize the given type when applied to the dialect of the given name.

inherits from sqlalchemy.sql.expression.ColumnOperators, typing.Generic

Base class for custom comparison operations defined at the type level. See TypeEngine.comparator_factory.

Operate on an argument.

This is the lowest level of operation, raises NotImplementedError by default.

Overriding this on a subclass can allow common behavior to be applied to all operations. For example, overriding ColumnOperators to apply func.lower() to the left and right side:

op¶ – Operator callable.

*other¶ – the ‘other’ side of the operation. Will be a single scalar for most operations.

**kwargs¶ – modifiers. These may be passed by special operators such as ColumnOperators.contains().

Reverse operate on an argument.

Usage is the same as operate().

Produce an “adapted” form of this type, given an “impl” class to work with.

This method is used internally to associate generic types with “implementation” types that are specific to a particular dialect.

Return an instance of the generic type corresponding to this type using heuristic rule. The method may be overridden if this heuristic rule is not sufficient.

Added in version 1.4.0b2.

Reflecting with Database-Agnostic Types - describes the use of TypeEngine.as_generic() in conjunction with the DDLEvents.column_reflect() event, which is its intended use.

Given a bind value (i.e. a BindParameter instance), return a SQL expression in its place.

This is typically a SQL function that wraps the existing bound parameter within the statement. It is used for special data types that require literals being wrapped in some special database function in order to coerce an application-level value into a database-specific format. It is the SQL analogue of the TypeEngine.bind_processor() method.

This method is called during the SQL compilation phase of a statement, when rendering a SQL string. It is not called against specific values.

Note that this method, when implemented, should always return the exact same structure, without any conditional logic, as it may be used in an executemany() call against an arbitrary number of bound parameter sets.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.bind_expression() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.bind_expression(), implement a TypeDecorator class and provide an implementation of TypeDecorator.bind_expression().

Augmenting Existing Types

Applying SQL-level Bind/Result Processing

Return a conversion function for processing bind values.

Returns a callable which will receive a bind parameter value as the sole positional argument and will return a value to send to the DB-API.

If processing is not necessary, the method should return None.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.bind_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.bind_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_bind_param().

Augmenting Existing Types

dialect¶ – Dialect instance in use.

Suggest a type for a ‘coerced’ Python value in an expression.

Given an operator and value, gives the type a chance to return a type which the value should be coerced into.

The default behavior here is conservative; if the right-hand side is already coerced into a SQL type based on its Python type, it is usually left alone.

End-user functionality extension here should generally be via TypeDecorator, which provides more liberal behavior in that it defaults to coercing the other side of the expression into this type, thus applying special Python conversions above and beyond those needed by the DBAPI to both ides. It also provides the public method TypeDecorator.coerce_compared_value() which is intended for end-user customization of this behavior.

Given a SELECT column expression, return a wrapping SQL expression.

This is typically a SQL function that wraps a column expression as rendered in the columns clause of a SELECT statement. It is used for special data types that require columns to be wrapped in some special database function in order to coerce the value before being sent back to the application. It is the SQL analogue of the TypeEngine.result_processor() method.

The column_expression() method is applied only to the outermost columns clause of a SELECT statement, that is, the columns that are to be delivered directly into the returned result rows. It does not apply to the columns clause inside of subqueries. This necessarily avoids double conversions against the column and only runs the conversion when ready to be returned to the client.

This method is called during the SQL compilation phase of a statement, when rendering a SQL string. It is not called against specific values.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.column_expression() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.column_expression(), implement a TypeDecorator class and provide an implementation of TypeDecorator.column_expression().

Augmenting Existing Types

Applying SQL-level Bind/Result Processing

Compare two values for equality.

Produce a string-compiled form of this TypeEngine.

When called with no arguments, uses a “default” dialect to produce a string result.

dialect¶ – a Dialect instance.

Return a dialect-specific implementation for this TypeEngine.

Return a copy of this type which has the should_evaluate_none flag set to True.

The ORM uses this flag to indicate that a positive value of None is passed to the column in an INSERT statement, rather than omitting the column from the INSERT statement which has the effect of firing off column-level defaults. It also allows for types which have special behavior associated with the Python None value to indicate that the value doesn’t necessarily translate into SQL NULL; a prime example of this is a JSON type which may wish to persist the JSON value 'null'.

In all cases, the actual NULL SQL value can be always be persisted in any column by using the null SQL construct in an INSERT statement or associated with an ORM-mapped attribute.

The “evaluates none” flag does not apply to a value of None passed to Column.default or Column.server_default; in these cases, None still means “no default”.

Forcing NULL on a column with a default - in the ORM documentation

JSON.none_as_null - PostgreSQL JSON interaction with this flag.

TypeEngine.should_evaluate_none - class-level flag

Return the corresponding type object from the underlying DB-API, if any.

This can be useful for calling setinputsizes(), for example.

Flag, if False, means values from this type aren’t hashable.

Used by the ORM when uniquing result lists.

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

Render bind casts for BindTyping.RENDER_CASTS mode.

If True, this type (usually a dialect level impl type) signals to the compiler that a cast should be rendered around a bound parameter for this type.

Added in version 2.0.

render casts when rendering a value as an inline literal, e.g. with TypeEngine.literal_processor().

Added in version 2.0.

Return a conversion function for processing result row values.

Returns a callable which will receive a result row column value as the sole positional argument and will return a value to return to the user.

If processing is not necessary, the method should return None.

This method is only called relative to a dialect specific type object, which is often private to a dialect in use and is not the same type object as the public facing one, which means it’s not feasible to subclass a TypeEngine class in order to provide an alternate TypeEngine.result_processor() method, unless subclassing the UserDefinedType class explicitly.

To provide alternate behavior for TypeEngine.result_processor(), implement a TypeDecorator class and provide an implementation of TypeDecorator.process_result_value().

Augmenting Existing Types

dialect¶ – Dialect instance in use.

coltype¶ – DBAPI coltype argument received in cursor.description.

If True, the Python constant None is considered to be handled explicitly by this type.

The ORM uses this flag to indicate that a positive value of None is passed to the column in an INSERT statement, rather than omitting the column from the INSERT statement which has the effect of firing off column-level defaults. It also allows types which have special behavior for Python None, such as a JSON type, to indicate that they’d like to handle the None value explicitly.

To set this flag on an existing type, use the TypeEngine.evaluates_none() method.

TypeEngine.evaluates_none()

A sorting function that can be passed as the key to sorted.

The default value of None indicates that the values stored by this type are self-sorting.

Added in version 1.3.8.

Produce a copy of this type object that will utilize the given type when applied to the dialect of the given name.

The variant mapping indicates that when this type is interpreted by a specific dialect, it will instead be transmuted into the given type, rather than using the primary type.

Changed in version 2.0: the TypeEngine.with_variant() method now works with a TypeEngine object “in place”, returning a copy of the original type rather than returning a wrapping object; the Variant class is no longer used.

type_¶ – a TypeEngine that will be selected as a variant from the originating type, when a dialect of the given name is in use.

one or more base names of the dialect which uses this type. (i.e. 'postgresql', 'mysql', etc.)

Changed in version 2.0: multiple dialect names can be specified for one variant.

Using “UPPERCASE” and Backend-specific types for multiple backends - illustrates the use of TypeEngine.with_variant().

inherits from sqlalchemy.types.TypeEngineMixin

A mixin that marks a type as supporting ‘concatenation’, typically strings.

inherits from sqlalchemy.types.Comparator

inherits from sqlalchemy.types.TypeEngineMixin

A mixin that marks a type as supporting indexing operations, such as array or JSON structures.

inherits from sqlalchemy.types.Comparator

inherits from sqlalchemy.types.TypeEngine

NullType is used as a default type for those cases where a type cannot be determined, including:

During table reflection, when the type of a column is not recognized by the Dialect

When constructing SQL expressions using plain Python objects of unknown types (e.g. somecolumn == my_special_object)

When a new Column is created, and the given type is passed as None or is not passed at all.

The NullType can be used within SQL expression invocation without issue, it just has no behavior either at the expression construction level or at the bind-parameter/result processing level. NullType will result in a CompileError if the compiler is asked to render the type itself, such as if it is used in a cast() operation or within a schema creation operation such as that invoked by MetaData.create_all() or the CreateTable construct.

inherits from sqlalchemy.types.TypeEngineMixin

mixin that defines attributes and behaviors specific to third-party datatypes.

“Third party” refers to datatypes that are defined outside the scope of SQLAlchemy within either end-user application code or within external extensions to SQLAlchemy.

Subclasses currently include TypeDecorator and UserDefinedType.

Added in version 1.4.28.

Indicate if statements using this ExternalType are “safe to cache”.

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

inherits from sqlalchemy.types.TypeDecorator

deprecated. symbol is present for backwards-compatibility with workaround recipes, however this actual type should not be used.

Produce a copy of this type object that will utilize the given type when applied to the dialect of the given name.

inherited from the TypeEngine.with_variant() method of TypeEngine

Produce a copy of this type object that will utilize the given type when applied to the dialect of the given name.

The variant mapping indicates that when this type is interpreted by a specific dialect, it will instead be transmuted into the given type, rather than using the primary type.

Changed in version 2.0: the TypeEngine.with_variant() method now works with a TypeEngine object “in place”, returning a copy of the original type rather than returning a wrapping object; the Variant class is no longer used.

type_¶ – a TypeEngine that will be selected as a variant from the originating type, when a dialect of the given name is in use.

one or more base names of the dialect which uses this type. (i.e. 'postgresql', 'mysql', etc.)

Changed in version 2.0: multiple dialect names can be specified for one variant.

Using “UPPERCASE” and Backend-specific types for multiple backends - illustrates the use of TypeEngine.with_variant().

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
class MyComparator(ColumnOperators):
    def operate(self, op, other, **kwargs):
        return op(func.lower(self), func.lower(other), **kwargs)
```

Example 2 (sql):
```sql
>>> from sqlalchemy.dialects.mysql import INTEGER
>>> INTEGER(display_width=4).as_generic()
Integer()
```

Example 3 (sql):
```sql
>>> from sqlalchemy.dialects.mysql import NVARCHAR
>>> NVARCHAR(length=100).as_generic()
Unicode(length=100)
```

Example 4 (unknown):
```unknown
Table(
    "some_table",
    metadata,
    Column(
        String(50).evaluates_none(),
        nullable=True,
        server_default="no value",
    ),
)
```

---
