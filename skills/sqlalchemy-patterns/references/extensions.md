# Sqlalchemy - Extensions

**Pages:** 5

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Mutation Tracking¶
- Establishing Mutability on Scalar Column Values¶
  - Supporting Pickling¶
  - Receiving Events¶
- Establishing Mutability on Composites¶
  - Coercing Mutable Composites¶

Home | Download this Documentation

Home | Download this Documentation

Provide support for tracking of in-place changes to scalar values, which are propagated into ORM change events on owning parent objects.

A typical example of a “mutable” structure is a Python dictionary. Following the example introduced in SQL Datatype Objects, we begin with a custom type that marshals Python dictionaries into JSON strings before being persisted:

The usage of json is only for the purposes of example. The sqlalchemy.ext.mutable extension can be used with any type whose target Python type may be mutable, including PickleType, ARRAY, etc.

When using the sqlalchemy.ext.mutable extension, the value itself tracks all parents which reference it. Below, we illustrate a simple version of the MutableDict dictionary object, which applies the Mutable mixin to a plain Python dictionary:

The above dictionary class takes the approach of subclassing the Python built-in dict to produce a dict subclass which routes all mutation events through __setitem__. There are variants on this approach, such as subclassing UserDict.UserDict or collections.MutableMapping; the part that’s important to this example is that the Mutable.changed() method is called whenever an in-place change to the datastructure takes place.

We also redefine the Mutable.coerce() method which will be used to convert any values that are not instances of MutableDict, such as the plain dictionaries returned by the json module, into the appropriate type. Defining this method is optional; we could just as well created our JSONEncodedDict such that it always returns an instance of MutableDict, and additionally ensured that all calling code uses MutableDict explicitly. When Mutable.coerce() is not overridden, any values applied to a parent object which are not instances of the mutable type will raise a ValueError.

Our new MutableDict type offers a class method Mutable.as_mutable() which we can use within column metadata to associate with types. This method grabs the given type object or class and associates a listener that will detect all future mappings of this type, applying event listening instrumentation to the mapped attribute. Such as, with classical table metadata:

Above, Mutable.as_mutable() returns an instance of JSONEncodedDict (if the type object was not an instance already), which will intercept any attributes which are mapped against this type. Below we establish a simple mapping against the my_data table:

The MyDataClass.data member will now be notified of in place changes to its value.

Any in-place changes to the MyDataClass.data member will flag the attribute as “dirty” on the parent object:

The MutableDict can be associated with all future instances of JSONEncodedDict in one step, using Mutable.associate_with(). This is similar to Mutable.as_mutable() except it will intercept all occurrences of MutableDict in all mappings unconditionally, without the need to declare it individually:

The key to the sqlalchemy.ext.mutable extension relies upon the placement of a weakref.WeakKeyDictionary upon the value object, which stores a mapping of parent mapped objects keyed to the attribute name under which they are associated with this value. WeakKeyDictionary objects are not picklable, due to the fact that they contain weakrefs and function callbacks. In our case, this is a good thing, since if this dictionary were picklable, it could lead to an excessively large pickle size for our value objects that are pickled by themselves outside of the context of the parent. The developer responsibility here is only to provide a __getstate__ method that excludes the MutableBase._parents() collection from the pickle stream:

With our dictionary example, we need to return the contents of the dict itself (and also restore them on __setstate__):

In the case that our mutable value object is pickled as it is attached to one or more parent objects that are also part of the pickle, the Mutable mixin will re-establish the Mutable._parents collection on each value object as the owning parents themselves are unpickled.

The AttributeEvents.modified() event handler may be used to receive an event when a mutable scalar emits a change event. This event handler is called when the flag_modified() function is called from within the mutable extension:

Composites are a special ORM feature which allow a single scalar attribute to be assigned an object value which represents information “composed” from one or more columns from the underlying mapped table. The usual example is that of a geometric “point”, and is introduced in Composite Column Types.

As is the case with Mutable, the user-defined composite class subclasses MutableComposite as a mixin, and detects and delivers change events to its parents via the MutableComposite.changed() method. In the case of a composite class, the detection is usually via the usage of the special Python method __setattr__(). In the example below, we expand upon the Point class introduced in Composite Column Types to include MutableComposite in its bases and to route attribute set events via __setattr__ to the MutableComposite.changed() method:

The MutableComposite class makes use of class mapping events to automatically establish listeners for any usage of composite() that specifies our Point type. Below, when Point is mapped to the Vertex class, listeners are established which will route change events from Point objects to each of the Vertex.start and Vertex.end attributes:

Any in-place changes to the Vertex.start or Vertex.end members will flag the attribute as “dirty” on the parent object:

The MutableBase.coerce() method is also supported on composite types. In the case of MutableComposite, the MutableBase.coerce() method is only called for attribute set operations, not load operations. Overriding the MutableBase.coerce() method is essentially equivalent to using a validates() validation routine for all attributes which make use of the custom composite type:

As is the case with Mutable, the MutableComposite helper class uses a weakref.WeakKeyDictionary available via the MutableBase._parents() attribute which isn’t picklable. If we need to pickle instances of Point or its owning class Vertex, we at least need to define a __getstate__ that doesn’t include the _parents dictionary. Below we define both a __getstate__ and a __setstate__ that package up the minimal form of our Point class:

As with Mutable, the MutableComposite augments the pickling process of the parent’s object-relational state so that the MutableBase._parents() collection is restored to all Point objects.

Mixin that defines transparent propagation of change events to a parent object.

Common base class to Mutable and MutableComposite.

Mixin that defines transparent propagation of change events on a SQLAlchemy “composite” object to its owning parent or parents.

A dictionary type that implements Mutable.

A list type that implements Mutable.

A set type that implements Mutable.

Common base class to Mutable and MutableComposite.

Dictionary of parent object’s InstanceState->attribute name on the parent.

Given a value, coerce it into the target type.

Dictionary of parent object’s InstanceState->attribute name on the parent.

This attribute is a so-called “memoized” property. It initializes itself with a new weakref.WeakKeyDictionary the first time it is accessed, returning the same object upon subsequent access.

Changed in version 1.4: the InstanceState is now used as the key in the weak dictionary rather than the instance itself.

Given a value, coerce it into the target type.

Can be overridden by custom subclasses to coerce incoming data into a particular type.

By default, raises ValueError.

This method is called in different scenarios depending on if the parent class is of type Mutable or of type MutableComposite. In the case of the former, it is called for both attribute-set operations as well as during ORM loading operations. For the latter, it is only called during attribute-set operations; the mechanics of the composite() construct handle coercion during load operations.

key¶ – string name of the ORM-mapped attribute being set.

value¶ – the incoming value.

the method should return the coerced value, or raise ValueError if the coercion cannot be completed.

inherits from sqlalchemy.ext.mutable.MutableBase

Mixin that defines transparent propagation of change events to a parent object.

See the example in Establishing Mutability on Scalar Column Values for usage information.

Given a descriptor attribute, return a set() of the attribute keys which indicate a change in the state of this attribute.

_listen_on_attribute()

Establish this type as a mutation listener for the given mapped descriptor.

Dictionary of parent object’s InstanceState->attribute name on the parent.

Associate a SQL type with this mutable Python type.

Associate this wrapper with all future mapped columns of the given type.

associate_with_attribute()

Establish this type as a mutation listener for the given mapped descriptor.

Subclasses should call this method whenever change events occur.

Given a value, coerce it into the target type.

inherited from the sqlalchemy.ext.mutable.MutableBase._get_listen_keys method of MutableBase

Given a descriptor attribute, return a set() of the attribute keys which indicate a change in the state of this attribute.

This is normally just set([attribute.key]), but can be overridden to provide for additional keys. E.g. a MutableComposite augments this set with the attribute keys associated with the columns that comprise the composite value.

This collection is consulted in the case of intercepting the InstanceEvents.refresh() and InstanceEvents.refresh_flush() events, which pass along a list of attribute names that have been refreshed; the list is compared against this set to determine if action needs to be taken.

inherited from the sqlalchemy.ext.mutable.MutableBase._listen_on_attribute method of MutableBase

Establish this type as a mutation listener for the given mapped descriptor.

inherited from the sqlalchemy.ext.mutable.MutableBase._parents attribute of MutableBase

Dictionary of parent object’s InstanceState->attribute name on the parent.

This attribute is a so-called “memoized” property. It initializes itself with a new weakref.WeakKeyDictionary the first time it is accessed, returning the same object upon subsequent access.

Changed in version 1.4: the InstanceState is now used as the key in the weak dictionary rather than the instance itself.

Associate a SQL type with this mutable Python type.

This establishes listeners that will detect ORM mappings against the given type, adding mutation event trackers to those mappings.

The type is returned, unconditionally as an instance, so that as_mutable() can be used inline:

Note that the returned type is always an instance, even if a class is given, and that only columns which are declared specifically with that type instance receive additional instrumentation.

To associate a particular mutable type with all occurrences of a particular type, use the Mutable.associate_with() classmethod of the particular Mutable subclass to establish a global association.

The listeners established by this method are global to all mappers, and are not garbage collected. Only use as_mutable() for types that are permanent to an application, not with ad-hoc types else this will cause unbounded growth in memory usage.

Associate this wrapper with all future mapped columns of the given type.

This is a convenience method that calls associate_with_attribute automatically.

The listeners established by this method are global to all mappers, and are not garbage collected. Only use associate_with() for types that are permanent to an application, not with ad-hoc types else this will cause unbounded growth in memory usage.

Establish this type as a mutation listener for the given mapped descriptor.

Subclasses should call this method whenever change events occur.

inherited from the MutableBase.coerce() method of MutableBase

Given a value, coerce it into the target type.

Can be overridden by custom subclasses to coerce incoming data into a particular type.

By default, raises ValueError.

This method is called in different scenarios depending on if the parent class is of type Mutable or of type MutableComposite. In the case of the former, it is called for both attribute-set operations as well as during ORM loading operations. For the latter, it is only called during attribute-set operations; the mechanics of the composite() construct handle coercion during load operations.

key¶ – string name of the ORM-mapped attribute being set.

value¶ – the incoming value.

the method should return the coerced value, or raise ValueError if the coercion cannot be completed.

inherits from sqlalchemy.ext.mutable.MutableBase

Mixin that defines transparent propagation of change events on a SQLAlchemy “composite” object to its owning parent or parents.

See the example in Establishing Mutability on Composites for usage information.

Subclasses should call this method whenever change events occur.

Subclasses should call this method whenever change events occur.

inherits from sqlalchemy.ext.mutable.Mutable, builtins.dict, typing.Generic

A dictionary type that implements Mutable.

The MutableDict object implements a dictionary that will emit change events to the underlying mapping when the contents of the dictionary are altered, including when values are added or removed.

Note that MutableDict does not apply mutable tracking to the values themselves inside the dictionary. Therefore it is not a sufficient solution for the use case of tracking deep changes to a recursive dictionary structure, such as a JSON structure. To support this use case, build a subclass of MutableDict that provides appropriate coercion to the values placed in the dictionary so that they too are “mutable”, and emit events up to their parent structure.

Remove all items from the dict.

Convert plain dictionary to instance of this class.

If the key is not found, return the default if given; otherwise, raise a KeyError.

Remove and return a (key, value) pair as a 2-tuple.

Insert key with a value of default if key is not in the dictionary.

If E is present and has a .keys() method, then does: for k in E.keys(): D[k] = E[k] If E is present and lacks a .keys() method, then does: for k, v in E: D[k] = v In either case, this is followed by: for k in F: D[k] = F[k]

Remove all items from the dict.

Convert plain dictionary to instance of this class.

If the key is not found, return the default if given; otherwise, raise a KeyError.

Remove and return a (key, value) pair as a 2-tuple.

Pairs are returned in LIFO (last-in, first-out) order. Raises KeyError if the dict is empty.

Insert key with a value of default if key is not in the dictionary.

Return the value for key if key is in the dictionary, else default.

If E is present and has a .keys() method, then does: for k in E.keys(): D[k] = E[k] If E is present and lacks a .keys() method, then does: for k, v in E: D[k] = v In either case, this is followed by: for k in F: D[k] = F[k]

inherits from sqlalchemy.ext.mutable.Mutable, builtins.list, typing.Generic

A list type that implements Mutable.

The MutableList object implements a list that will emit change events to the underlying mapping when the contents of the list are altered, including when values are added or removed.

Note that MutableList does not apply mutable tracking to the values themselves inside the list. Therefore it is not a sufficient solution for the use case of tracking deep changes to a recursive mutable structure, such as a JSON structure. To support this use case, build a subclass of MutableList that provides appropriate coercion to the values placed in the dictionary so that they too are “mutable”, and emit events up to their parent structure.

Append object to the end of the list.

Remove all items from list.

Convert plain list to instance of this class.

Extend list by appending elements from the iterable.

Insert object before index.

Remove and return item at index (default last).

Remove first occurrence of value.

Sort the list in ascending order and return None.

Append object to the end of the list.

Remove all items from list.

Convert plain list to instance of this class.

Extend list by appending elements from the iterable.

Insert object before index.

Remove and return item at index (default last).

Raises IndexError if list is empty or index is out of range.

Remove first occurrence of value.

Raises ValueError if the value is not present.

Sort the list in ascending order and return None.

The sort is in-place (i.e. the list itself is modified) and stable (i.e. the order of two equal elements is maintained).

If a key function is given, apply it once to each list item and sort them, ascending or descending, according to their function values.

The reverse flag can be set to sort in descending order.

inherits from sqlalchemy.ext.mutable.Mutable, builtins.set, typing.Generic

A set type that implements Mutable.

The MutableSet object implements a set that will emit change events to the underlying mapping when the contents of the set are altered, including when values are added or removed.

Note that MutableSet does not apply mutable tracking to the values themselves inside the set. Therefore it is not a sufficient solution for the use case of tracking deep changes to a recursive mutable structure. To support this use case, build a subclass of MutableSet that provides appropriate coercion to the values placed in the dictionary so that they too are “mutable”, and emit events up to their parent structure.

Add an element to a set.

Remove all elements from this set.

Convert plain set to instance of this class.

Update the set, removing elements found in others.

Remove an element from a set if it is a member.

intersection_update()

Update the set, keeping only elements found in it and all others.

Remove and return an arbitrary set element.

Remove an element from a set; it must be a member.

symmetric_difference_update()

Update the set, keeping only elements found in either set, but not in both.

Update the set, adding elements from all others.

Add an element to a set.

This has no effect if the element is already present.

Remove all elements from this set.

Convert plain set to instance of this class.

Update the set, removing elements found in others.

Remove an element from a set if it is a member.

Unlike set.remove(), the discard() method does not raise an exception when an element is missing from the set.

Update the set, keeping only elements found in it and all others.

Remove and return an arbitrary set element.

Raises KeyError if the set is empty.

Remove an element from a set; it must be a member.

If the element is not a member, raise a KeyError.

Update the set, keeping only elements found in either set, but not in both.

Update the set, adding elements from all others.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from sqlalchemy.types import TypeDecorator, VARCHAR
import json


class JSONEncodedDict(TypeDecorator):
    "Represents an immutable structure as a json-encoded string."

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value
```

Example 2 (python):
```python
from sqlalchemy.ext.mutable import Mutable


class MutableDict(Mutable, dict):
    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutableDict."

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."

        dict.__delitem__(self, key)
        self.changed()
```

Example 3 (python):
```python
from sqlalchemy import Table, Column, Integer

my_data = Table(
    "my_data",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("data", MutableDict.as_mutable(JSONEncodedDict)),
)
```

Example 4 (typescript):
```typescript
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class MyDataClass(Base):
    __tablename__ = "my_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[dict[str, str]] = mapped_column(
        MutableDict.as_mutable(JSONEncodedDict)
    )
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/extensions/baked.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Baked Queries¶
- Synopsis¶
- Performance¶
- Rationale¶
- Special Query Techniques¶
  - Using IN expressions¶

Home | Download this Documentation

Home | Download this Documentation

baked provides an alternative creational pattern for Query objects, which allows for caching of the object’s construction and string-compilation steps. This means that for a particular Query building scenario that is used more than once, all of the Python function invocation involved in building the query from its initial construction up through generating a SQL string will only occur once, rather than for each time that query is built up and executed.

The rationale for this system is to greatly reduce Python interpreter overhead for everything that occurs before the SQL is emitted. The caching of the “baked” system does not in any way reduce SQL calls or cache the return results from the database. A technique that demonstrates the caching of the SQL calls and result sets themselves is available in Dogpile Caching.

Deprecated since version 1.4: SQLAlchemy 1.4 and 2.0 feature an all-new direct query caching system that removes the need for the BakedQuery system. Caching is now transparently active for all Core and ORM queries with no action taken by the user, using the system described at SQL Compilation Caching.

The sqlalchemy.ext.baked extension is not for beginners. Using it correctly requires a good high level understanding of how SQLAlchemy, the database driver, and the backend database interact with each other. This extension presents a very specific kind of optimization that is not ordinarily needed. As noted above, it does not cache queries, only the string formulation of the SQL itself.

Usage of the baked system starts by producing a so-called “bakery”, which represents storage for a particular series of query objects:

The above “bakery” will store cached data in an LRU cache that defaults to 200 elements, noting that an ORM query will typically contain one entry for the ORM query as invoked, as well as one entry per database dialect for the SQL string.

The bakery allows us to build up a Query object by specifying its construction as a series of Python callables, which are typically lambdas. For succinct usage, it overrides the += operator so that a typical query build-up looks like the following:

Following are some observations about the above code:

The baked_query object is an instance of BakedQuery. This object is essentially the “builder” for a real orm Query object, but it is not itself the actual Query object.

The actual Query object is not built at all, until the very end of the function when Result.all() is called.

The steps that are added to the baked_query object are all expressed as Python functions, typically lambdas. The first lambda given to the bakery() function receives a Session as its argument. The remaining lambdas each receive a Query as their argument.

In the above code, even though our application may call upon search_for_user() many times, and even though within each invocation we build up an entirely new BakedQuery object, all of the lambdas are only called once. Each lambda is never called a second time for as long as this query is cached in the bakery.

The caching is achieved by storing references to the lambda objects themselves in order to formulate a cache key; that is, the fact that the Python interpreter assigns an in-Python identity to these functions is what determines how to identify the query on successive runs. For those invocations of search_for_user() where the email parameter is specified, the callable lambda q: q.filter(User.email == bindparam('email')) will be part of the cache key that’s retrieved; when email is None, this callable is not part of the cache key.

Because the lambdas are all called only once, it is essential that no variables which may change across calls are referenced within the lambdas; instead, assuming these are values to be bound into the SQL string, we use bindparam() to construct named parameters, where we apply their actual values later using Result.params().

The baked query probably looks a little odd, a little bit awkward and a little bit verbose. However, the savings in Python performance for a query which is invoked lots of times in an application are very dramatic. The example suite short_selects demonstrated in Performance illustrates a comparison of queries which each return only one row, such as the following regular query:

compared to the equivalent “baked” query:

The difference in Python function call count for an iteration of 10000 calls to each block are:

In terms of number of seconds on a powerful laptop, this comes out as:

Note that this test very intentionally features queries that only return one row. For queries that return many rows, the performance advantage of the baked query will have less and less of an impact, proportional to the time spent fetching rows. It is critical to keep in mind that the baked query feature only applies to building the query itself, not the fetching of results. Using the baked feature is by no means a guarantee to a much faster application; it is only a potentially useful feature for those applications that have been measured as being impacted by this particular form of overhead.

Measure twice, cut once

For background on how to profile a SQLAlchemy application, please see the section Performance. It is essential that performance measurement techniques are used when attempting to improve the performance of an application.

The “lambda” approach above is a superset of what would be a more traditional “parameterized” approach. Suppose we wished to build a simple system where we build a Query just once, then store it in a dictionary for reuse. This is possible right now by just building up the query, and removing its Session by calling my_cached_query = query.with_session(None):

The above approach gets us a very minimal performance benefit. By reusing a Query, we save on the Python work within the session.query(Model) constructor as well as calling upon filter(Model.id == bindparam('id')), which will skip for us the building up of the Core expression as well as sending it to Query.filter(). However, the approach still regenerates the full Select object every time when Query.all() is called and additionally this brand new Select is sent off to the string compilation step every time, which for a simple case like the above is probably about 70% of the overhead.

To reduce the additional overhead, we need some more specialized logic, some way to memoize the construction of the select object and the construction of the SQL. There is an example of this on the wiki in the section BakedQuery, a precursor to this feature, however in that system, we aren’t caching the construction of the query. In order to remove all the overhead, we need to cache both the construction of the query as well as the SQL compilation. Let’s assume we adapted the recipe in this way and made ourselves a method .bake() that pre-compiles the SQL for the query, producing a new object that can be invoked with minimal overhead. Our example becomes:

Above, we’ve fixed the performance situation, but we still have this string cache key to deal with.

We can use the “bakery” approach to re-frame the above in a way that looks less unusual than the “building up lambdas” approach, and more like a simple improvement upon the simple “reuse a query” approach:

Above, we use the “baked” system in a manner that is very similar to the simplistic “cache a query” system. However, it uses two fewer lines of code, does not need to manufacture a cache key of “my_key”, and also includes the same feature as our custom “bake” function that caches 100% of the Python invocation work from the constructor of the query, to the filter call, to the production of the Select object, to the string compilation step.

From the above, if we ask ourselves, “what if lookup needs to make conditional decisions as to the structure of the query?”, this is where hopefully it becomes apparent why “baked” is the way it is. Instead of a parameterized query building off from exactly one function (which is how we thought baked might work originally), we can build it from any number of functions. Consider our naive example, if we needed to have an additional clause in our query on a conditional basis:

Our “simple” parameterized system must now be tasked with generating cache keys which take into account whether or not the “include_frobnizzle” flag was passed, as the presence of this flag means that the generated SQL would be entirely different. It should be apparent that as the complexity of query building goes up, the task of caching these queries becomes burdensome very quickly. We can convert the above example into a direct use of “bakery” as follows:

Above, we again cache not just the query object but all the work it needs to do in order to generate SQL. We also no longer need to deal with making sure we generate a cache key that accurately takes into account all of the structural modifications we’ve made; this is now handled automatically and without the chance of mistakes.

This code sample is a few lines shorter than the naive example, removes the need to deal with cache keys, and has the vast performance benefits of the full so-called “baked” feature. But still a little verbose! Hence we take methods like BakedQuery.add_criteria() and BakedQuery.with_criteria() and shorten them into operators, and encourage (though certainly not require!) using simple lambdas, only as a means to reduce verbosity:

Where above, the approach is simpler to implement and much more similar in code flow to what a non-cached querying function would look like, hence making code easier to port.

The above description is essentially a summary of the design process used to arrive at the current “baked” approach. Starting from the “normal” approaches, the additional issues of cache key construction and management, removal of all redundant Python execution, and queries built up with conditionals needed to be addressed, leading to the final approach.

This section will describe some techniques for specific query situations.

The ColumnOperators.in_() method in SQLAlchemy historically renders a variable set of bound parameters based on the list of items that’s passed to the method. This doesn’t work for baked queries as the length of that list can change on different calls. To solve this problem, the bindparam.expanding parameter supports a late-rendered IN expression that is safe to be cached inside of baked query. The actual list of elements is rendered at statement execution time, rather than at statement compilation time:

ColumnOperators.in_()

When using Query objects, it is often needed that one Query object is used to generate a subquery within another. In the case where the Query is currently in baked form, an interim method may be used to retrieve the Query object, using the BakedQuery.to_query() method. This method is passed the Session or Query that is the argument to the lambda callable used to generate a particular step of the baked query:

Added in version 1.3.

As of SQLAlchemy 1.3.11, the use of the QueryEvents.before_compile() event against a particular Query will disallow the baked query system from caching the query, if the event hook returns a new Query object that is different from the one passed in. This is so that the QueryEvents.before_compile() hook may be invoked against a particular Query every time it is used, to accommodate for hooks that alter the query differently each time. To allow a QueryEvents.before_compile() to alter a sqlalchemy.orm.Query() object, but still to allow the result to be cached, the event can be registered passing the bake_ok=True flag:

The above strategy is appropriate for an event that will modify a given Query in exactly the same way every time, not dependent on specific parameters or external state that changes.

Added in version 1.3.11: - added the “bake_ok” flag to the QueryEvents.before_compile() event and disallowed caching via the “baked” extension from occurring for event handlers that return a new Query object if this flag is not set.

The flag Session.enable_baked_queries may be set to False, causing all baked queries to not use the cache when used against that Session:

Like all session flags, it is also accepted by factory objects like sessionmaker and methods like sessionmaker.configure().

The immediate rationale for this flag is so that an application which is seeing issues potentially due to cache key conflicts from user-defined baked queries or other baked query issues can turn the behavior off, in order to identify or eliminate baked queries as the cause of an issue.

Added in version 1.2.

Changed in version 1.4: As of SQLAlchemy 1.4, the “baked query” system is no longer part of the relationship loading system. The native caching system is used instead.

A builder object for Query objects.

Construct a new bakery.

Callable which returns a BakedQuery.

Construct a new bakery.

an instance of Bakery

A builder object for Query objects.

Add a criteria function to this BakedQuery.

Construct a new bakery.

Return a Result object for this BakedQuery.

Cancel any query caching that will occur on this BakedQuery object.

Return the Query object for use as a subquery.

Add a criteria function to a BakedQuery cloned from this one.

Add a criteria function to this BakedQuery.

This is equivalent to using the += operator to modify a BakedQuery in-place.

Construct a new bakery.

an instance of Bakery

Return a Result object for this BakedQuery.

This is equivalent to calling the BakedQuery as a Python callable, e.g. result = my_baked_query(session).

Cancel any query caching that will occur on this BakedQuery object.

The BakedQuery can continue to be used normally, however additional creational functions will not be cached; they will be called on every invocation.

This is to support the case where a particular step in constructing a baked query disqualifies the query from being cacheable, such as a variant that relies upon some uncacheable value.

full¶ – if False, only functions added to this BakedQuery object subsequent to the spoil step will be non-cached; the state of the BakedQuery up until this point will be pulled from the cache. If True, then the entire Query object is built from scratch each time, with all creational functions being called on each invocation.

Return the Query object for use as a subquery.

This method should be used within the lambda callable being used to generate a step of an enclosing BakedQuery. The parameter should normally be the Query object that is passed to the lambda:

In the case where the subquery is used in the first callable against a Session, the Session is also accepted:

a Query object or a class Session object, that is assumed to be within the context of an enclosing BakedQuery callable.

Added in version 1.3.

Add a criteria function to a BakedQuery cloned from this one.

This is equivalent to using the + operator to produce a new BakedQuery with modifications.

Callable which returns a BakedQuery.

This object is returned by the class method BakedQuery.bakery(). It exists as an object so that the “cache” can be easily inspected.

Added in version 1.2.

Invokes a BakedQuery against a Session.

The Result object is where the actual Query object gets created, or retrieved from the cache, against a target Session, and is then invoked for results.

Equivalent to Query.all().

Equivalent to Query.count().

Note this uses a subquery to ensure an accurate count regardless of the structure of the original statement.

Return the first row.

Equivalent to Query.first().

Retrieve an object based on identity.

Equivalent to Query.get().

Return exactly one result or raise an exception.

Equivalent to Query.one().

Return one or zero results, or raise an exception for multiple rows.

Equivalent to Query.one_or_none().

Specify parameters to be replaced into the string SQL statement.

Return the first element of the first result or None if no rows present. If multiple rows are returned, raises MultipleResultsFound.

Equivalent to Query.scalar().

Add a criteria function that will be applied post-cache.

This adds a function that will be run against the Query object after it is retrieved from the cache. This currently includes only the Query.params() and Query.execution_options() methods.

Result.with_post_criteria() functions are applied to the Query object after the query’s SQL statement object has been retrieved from the cache. Only Query.params() and Query.execution_options() methods should be used.

Added in version 1.2.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (sql):
```sql
from sqlalchemy.ext import baked

bakery = baked.bakery()
```

Example 2 (python):
```python
from sqlalchemy import bindparam


def search_for_user(session, username, email=None):
    baked_query = bakery(lambda session: session.query(User))
    baked_query += lambda q: q.filter(User.name == bindparam("username"))

    baked_query += lambda q: q.order_by(User.id)

    if email:
        baked_query += lambda q: q.filter(User.email == bindparam("email"))

    result = baked_query(session).params(username=username, email=email).all()

    return result
```

Example 3 (bash):
```bash
session = Session(bind=engine)
for id_ in random.sample(ids, n):
    session.query(Customer).filter(Customer.id == id_).one()
```

Example 4 (typescript):
```typescript
bakery = baked.bakery()
s = Session(bind=engine)
for id_ in random.sample(ids, n):
    q = bakery(lambda s: s.query(Customer))
    q += lambda q: q.filter(Customer.id == bindparam("id"))
    q(s).params(id=id_).one()
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Association Proxy¶
- Simplifying Scalar Collections¶
  - Creation of New Values¶
- Simplifying Association Objects¶
- Proxying to Dictionary Based Collections¶
- Composite Association Proxies¶

Home | Download this Documentation

Home | Download this Documentation

associationproxy is used to create a read/write view of a target attribute across a relationship. It essentially conceals the usage of a “middle” attribute between two endpoints, and can be used to cherry-pick fields from both a collection of related objects or scalar relationship. or to reduce the verbosity of using the association object pattern. Applied creatively, the association proxy allows the construction of sophisticated collections and dictionary views of virtually any geometry, persisted to the database using standard, transparently configured relational patterns.

Consider a many-to-many mapping between two classes, User and Keyword. Each User can have any number of Keyword objects, and vice-versa (the many-to-many pattern is described at Many To Many). The example below illustrates this pattern in the same way, with the exception of an extra attribute added to the User class called User.keywords:

In the above example, association_proxy() is applied to the User class to produce a “view” of the kw relationship, which exposes the string value of .keyword associated with each Keyword object. It also creates new Keyword objects transparently when strings are added to the collection:

To understand the mechanics of this, first review the behavior of User and Keyword without using the .keywords association proxy. Normally, reading and manipulating the collection of “keyword” strings associated with User requires traversal from each collection element to the .keyword attribute, which can be awkward. The example below illustrates the identical series of operations applied without using the association proxy:

The AssociationProxy object produced by the association_proxy() function is an instance of a Python descriptor, and is not considered to be “mapped” by the Mapper in any way. Therefore, it’s always indicated inline within the class definition of the mapped class, regardless of whether Declarative or Imperative mappings are used.

The proxy functions by operating upon the underlying mapped attribute or collection in response to operations, and changes made via the proxy are immediately apparent in the mapped attribute, as well as vice versa. The underlying attribute remains fully accessible.

When first accessed, the association proxy performs introspection operations on the target collection so that its behavior corresponds correctly. Details such as if the locally proxied attribute is a collection (as is typical) or a scalar reference, as well as if the collection acts like a set, list, or dictionary is taken into account, so that the proxy should act just like the underlying collection or attribute does.

When a list append() event (or set add(), dictionary __setitem__(), or scalar assignment event) is intercepted by the association proxy, it instantiates a new instance of the “intermediary” object using its constructor, passing as a single argument the given value. In our example above, an operation like:

Is translated by the association proxy into the operation:

The example works here because we have designed the constructor for Keyword to accept a single positional argument, keyword. For those cases where a single-argument constructor isn’t feasible, the association proxy’s creational behavior can be customized using the association_proxy.creator argument, which references a callable (i.e. Python function) that will produce a new object instance given the singular argument. Below we illustrate this using a lambda as is typical:

The creator function accepts a single argument in the case of a list- or set- based collection, or a scalar attribute. In the case of a dictionary-based collection, it accepts two arguments, “key” and “value”. An example of this is below in Proxying to Dictionary Based Collections.

The “association object” pattern is an extended form of a many-to-many relationship, and is described at Association Object. Association proxies are useful for keeping “association objects” out of the way during regular use.

Suppose our user_keyword table above had additional columns which we’d like to map explicitly, but in most cases we don’t require direct access to these attributes. Below, we illustrate a new mapping which introduces the UserKeywordAssociation class, which is mapped to the user_keyword table illustrated earlier. This class adds an additional column special_key, a value which we occasionally want to access, but not in the usual case. We create an association proxy on the User class called keywords, which will bridge the gap from the user_keyword_associations collection of User to the .keyword attribute present on each UserKeywordAssociation:

With the above configuration, we can operate upon the .keywords collection of each User object, each of which exposes a collection of Keyword objects that are obtained from the underlying UserKeywordAssociation elements:

This example is in contrast to the example illustrated previously at Simplifying Scalar Collections, where the association proxy exposed a collection of strings, rather than a collection of composed objects. In this case, each .keywords.append() operation is equivalent to:

The UserKeywordAssociation object has two attributes that are both populated within the scope of the append() operation of the association proxy; .keyword, which refers to the Keyword object, and .user, which refers to the User object. The .keyword attribute is populated first, as the association proxy generates a new UserKeywordAssociation object in response to the .append() operation, assigning the given Keyword instance to the .keyword attribute. Then, as the UserKeywordAssociation object is appended to the User.user_keyword_associations collection, the UserKeywordAssociation.user attribute, configured as back_populates for User.user_keyword_associations, is initialized upon the given UserKeywordAssociation instance to refer to the parent User receiving the append operation. The special_key argument above is left at its default value of None.

For those cases where we do want special_key to have a value, we create the UserKeywordAssociation object explicitly. Below we assign all three attributes, wherein the assignment of .user during construction, has the effect of appending the new UserKeywordAssociation to the User.user_keyword_associations collection (via the relationship):

The association proxy returns to us a collection of Keyword objects represented by all these operations:

The association proxy can proxy to dictionary based collections as well. SQLAlchemy mappings usually use the attribute_keyed_dict() collection type to create dictionary collections, as well as the extended techniques described in Custom Dictionary-Based Collections.

The association proxy adjusts its behavior when it detects the usage of a dictionary-based collection. When new values are added to the dictionary, the association proxy instantiates the intermediary object by passing two arguments to the creation function instead of one, the key and the value. As always, this creation function defaults to the constructor of the intermediary class, and can be customized using the creator argument.

Below, we modify our UserKeywordAssociation example such that the User.user_keyword_associations collection will now be mapped using a dictionary, where the UserKeywordAssociation.special_key argument will be used as the key for the dictionary. We also apply a creator argument to the User.keywords proxy so that these values are assigned appropriately when new elements are added to the dictionary:

We illustrate the .keywords collection as a dictionary, mapping the UserKeywordAssociation.special_key value to Keyword objects:

Given our previous examples of proxying from relationship to scalar attribute, proxying across an association object, and proxying dictionaries, we can combine all three techniques together to give User a keywords dictionary that deals strictly with the string value of special_key mapped to the string keyword. Both the UserKeywordAssociation and Keyword classes are entirely concealed. This is achieved by building an association proxy on User that refers to an association proxy present on UserKeywordAssociation:

User.keywords is now a dictionary of string to string, where UserKeywordAssociation and Keyword objects are created and removed for us transparently using the association proxy. In the example below, we illustrate usage of the assignment operator, also appropriately handled by the association proxy, to apply a dictionary value to the collection at once:

One caveat with our example above is that because Keyword objects are created for each dictionary set operation, the example fails to maintain uniqueness for the Keyword objects on their string name, which is a typical requirement for a tagging scenario such as this one. For this use case the recipe UniqueObject, or a comparable creational strategy, is recommended, which will apply a “lookup first, then create” strategy to the constructor of the Keyword class, so that an already existing Keyword is returned if the given name is already present.

The AssociationProxy features simple SQL construction capabilities which work at the class level in a similar way as other ORM-mapped attributes, and provide rudimentary filtering support primarily based on the SQL EXISTS keyword.

The primary purpose of the association proxy extension is to allow for improved persistence and object-access patterns with mapped object instances that are already loaded. The class-bound querying feature is of limited use and will not replace the need to refer to the underlying attributes when constructing SQL queries with JOINs, eager loading options, etc.

For this section, assume a class with both an association proxy that refers to a column, as well as an association proxy that refers to a related object, as in the example mapping below:

The SQL generated takes the form of a correlated subquery against the EXISTS SQL operator so that it can be used in a WHERE clause without the need for additional modifications to the enclosing query. If the immediate target of an association proxy is a mapped column expression, standard column operators can be used which will be embedded in the subquery. For example a straight equality operator:

For association proxies where the immediate target is a related object or collection, or another association proxy or attribute on the related object, relationship-oriented operators can be used instead, such as PropComparator.has() and PropComparator.any(). The User.keywords attribute is in fact two association proxies linked together, so when using this proxy for generating SQL phrases, we get two levels of EXISTS subqueries:

This is not the most efficient form of SQL, so while association proxies can be convenient for generating WHERE criteria quickly, SQL results should be inspected and “unrolled” into explicit JOIN criteria for best use, especially when chaining association proxies together.

Changed in version 1.3: Association proxy features distinct querying modes based on the type of target. See AssociationProxy now provides standard column operators for a column-oriented target.

Added in version 1.3.

An assignment to A.b will generate an AB object:

The A.b association is scalar, and includes use of the parameter AssociationProxy.cascade_scalar_deletes. When this parameter is enabled, setting A.b to None will remove A.ab as well:

When AssociationProxy.cascade_scalar_deletes is not set, the association object a.ab above would remain in place.

Note that this is not the behavior for collection-based association proxies; in that case, the intermediary association object is always removed when members of the proxied collection are removed. Whether or not the row is deleted depends on the relationship cascade setting.

The example below illustrates the use of the association proxy on the many side of of a one-to-many relationship, accessing attributes of a scalar object:

A summary of the steps of my_snack can be printed using:

association_proxy(target_collection, attr, *, [creator, getset_factory, proxy_factory, proxy_bulk_set, info, cascade_scalar_deletes, create_on_none_assignment, init, repr, default, default_factory, compare, kw_only, hash, dataclass_metadata])

Return a Python property implementing a view of a target attribute which references an attribute on members of the target.

A descriptor that presents a read/write view of an object attribute.

AssociationProxyExtensionType

AssociationProxyInstance

A per-class object that serves class- and object-specific results.

ColumnAssociationProxyInstance

an AssociationProxyInstance that has a database column as a target.

ObjectAssociationProxyInstance

an AssociationProxyInstance that has an object as a target.

Return a Python property implementing a view of a target attribute which references an attribute on members of the target.

The returned value is an instance of AssociationProxy.

Implements a Python property representing a relationship as a collection of simpler values, or a scalar value. The proxied property will mimic the collection type of the target (list, dict or set), or, in the case of a one to one relationship, a simple scalar value.

target_collection¶ – Name of the attribute that is the immediate target. This attribute is typically mapped by relationship() to link to a target collection, but can also be a many-to-one or non-scalar relationship.

attr¶ – Attribute on the associated instance or instances that are available on instances of the target object.

Defines custom behavior when new items are added to the proxied collection.

By default, adding new items to the collection will trigger a construction of an instance of the target object, passing the given item as a positional argument to the target constructor. For cases where this isn’t sufficient, association_proxy.creator can supply a callable that will construct the object in the appropriate way, given the item that was passed.

For list- and set- oriented collections, a single argument is passed to the callable. For dictionary oriented collections, two arguments are passed, corresponding to the key and value.

The association_proxy.creator callable is also invoked for scalar (i.e. many-to-one, one-to-one) relationships. If the current value of the target relationship attribute is None, the callable is used to construct a new object. If an object value already exists, the given attribute value is populated onto that object.

Creation of New Values

cascade_scalar_deletes¶ –

when True, indicates that setting the proxied value to None, or deleting it via del, should also remove the source object. Only applies to scalar attributes. Normally, removing the proxied target will not remove the proxy source, as this object may have other state that is still to be kept.

Added in version 1.3.

Cascading Scalar Deletes - complete usage example

create_on_none_assignment¶ –

when True, indicates that setting the proxied value to None should create the source object if it does not exist, using the creator. Only applies to scalar attributes. This is mutually exclusive vs. the association_proxy.cascade_scalar_deletes.

Added in version 2.0.18.

Specific to Declarative Dataclass Mapping, specifies if the mapped attribute should be part of the __init__() method as generated by the dataclass process.

Added in version 2.0.0b4.

Specific to Declarative Dataclass Mapping, specifies if the attribute established by this AssociationProxy should be part of the __repr__() method as generated by the dataclass process.

Added in version 2.0.0b4.

Specific to Declarative Dataclass Mapping, specifies a default-value generation function that will take place as part of the __init__() method as generated by the dataclass process.

Added in version 2.0.0b4.

Specific to Declarative Dataclass Mapping, indicates if this field should be included in comparison operations when generating the __eq__() and __ne__() methods for the mapped class.

Added in version 2.0.0b4.

Specific to Declarative Dataclass Mapping, indicates if this field should be marked as keyword-only when generating the __init__() method as generated by the dataclass process.

Added in version 2.0.0b4.

Specific to Declarative Dataclass Mapping, controls if this field is included when generating the __hash__() method for the mapped class.

Added in version 2.0.36.

dataclass_metadata¶ –

Specific to Declarative Dataclass Mapping, supplies metadata to be attached to the generated dataclass field.

Added in version 2.0.42.

info¶ – optional, will be assigned to AssociationProxy.info if present.

The following additional parameters involve injection of custom behaviors within the AssociationProxy object and are for advanced use only:

Optional. Proxied attribute access is automatically handled by routines that get and set values based on the attr argument for this proxy.

If you would like to customize this behavior, you may supply a getset_factory callable that produces a tuple of getter and setter functions. The factory is called with two arguments, the abstract type of the underlying collection and this proxy instance.

proxy_factory¶ – Optional. The type of collection to emulate is determined by sniffing the target collection. If your collection type can’t be determined by duck typing or you’d like to use a different collection implementation, you may supply a factory function to produce those collections. Only applicable to non-scalar relationships.

proxy_bulk_set¶ – Optional, use with proxy_factory.

inherits from sqlalchemy.orm.base.InspectionAttrInfo, sqlalchemy.orm.base.ORMDescriptor, sqlalchemy.orm._DCAttributeOptions, sqlalchemy.ext.associationproxy._AssociationProxyProtocol

A descriptor that presents a read/write view of an object attribute.

Construct a new AssociationProxy.

cascade_scalar_deletes

create_on_none_assignment

The extension type, if any. Defaults to NotExtension.NOT_EXTENSION

Return the internal state local to a specific mapped class.

Info dictionary associated with the object, allowing user-defined data to be associated with this InspectionAttr.

True if this object is an instance of AliasedClass.

True if this object is a Python descriptor.

True if this object is an instance of Bundle.

True if this object is an instance of ClauseElement.

True if this object is an instance of InstanceState.

True if this object is an instance of Mapper.

True if this object is an instance of MapperProperty.

Return True if this object is an instance of Selectable.

Construct a new AssociationProxy.

The AssociationProxy object is typically constructed using the association_proxy() constructor function. See the description of association_proxy() for a description of all parameters.

The extension type, if any. Defaults to NotExtension.NOT_EXTENSION

AssociationProxyExtensionType

Return the internal state local to a specific mapped class.

E.g., given a class User:

If we access this AssociationProxy from Mapper.all_orm_descriptors, and we want to view the target class for this proxy as mapped by User:

This returns an instance of AssociationProxyInstance that is specific to the User class. The AssociationProxy object remains agnostic of its parent class.

class_¶ – the class that we are returning state for.

obj¶ – optional, an instance of the class that is required if the attribute refers to a polymorphic target, e.g. where we have to look at the type of the actual destination object to get the complete path.

Added in version 1.3: - AssociationProxy no longer stores any state specific to a particular parent class; the state is now stored in per-class AssociationProxyInstance objects.

inherited from the InspectionAttrInfo.info attribute of InspectionAttrInfo

Info dictionary associated with the object, allowing user-defined data to be associated with this InspectionAttr.

The dictionary is generated when first accessed. Alternatively, it can be specified as a constructor argument to the column_property(), relationship(), or composite() functions.

QueryableAttribute.info

inherited from the InspectionAttr.is_aliased_class attribute of InspectionAttr

True if this object is an instance of AliasedClass.

True if this object is a Python descriptor.

This can refer to one of many types. Usually a QueryableAttribute which handles attributes events on behalf of a MapperProperty. But can also be an extension type such as AssociationProxy or hybrid_property. The InspectionAttr.extension_type will refer to a constant identifying the specific subtype.

Mapper.all_orm_descriptors

inherited from the InspectionAttr.is_bundle attribute of InspectionAttr

True if this object is an instance of Bundle.

inherited from the InspectionAttr.is_clause_element attribute of InspectionAttr

True if this object is an instance of ClauseElement.

inherited from the InspectionAttr.is_instance attribute of InspectionAttr

True if this object is an instance of InstanceState.

inherited from the InspectionAttr.is_mapper attribute of InspectionAttr

True if this object is an instance of Mapper.

inherited from the InspectionAttr.is_property attribute of InspectionAttr

True if this object is an instance of MapperProperty.

inherited from the InspectionAttr.is_selectable attribute of InspectionAttr

Return True if this object is an instance of Selectable.

inherits from sqlalchemy.orm.base.SQLORMOperations

A per-class object that serves class- and object-specific results.

This is used by AssociationProxy when it is invoked in terms of a specific class or instance of a class, i.e. when it is used as a regular Python descriptor.

When referring to the AssociationProxy as a normal Python descriptor, the AssociationProxyInstance is the object that actually serves the information. Under normal circumstances, its presence is transparent:

In the special case that the AssociationProxy object is being accessed directly, in order to get an explicit handle to the AssociationProxyInstance, use the AssociationProxy.for_class() method:

Added in version 1.3.

Implement the == operator.

Implement the <= operator.

Implement the < operator.

Implement the != operator.

Produce an all_() clause against the parent object.

Produce a proxied ‘any’ expression using EXISTS.

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

Produce a proxied ‘has’ expression using EXISTS.

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

Return True if this AssociationProxyInstance proxies a scalar relationship on the local side.

Implement the startswith operator.

The intermediary class handled by this AssociationProxyInstance.

Hack, allows datetime objects to be compared on the LHS.

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

Produce a proxied ‘any’ expression using EXISTS.

This expression will be a composed product using the Comparator.any() and/or Comparator.has() operators of the underlying proxied attributes.

inherited from the ColumnOperators.any_() method of ColumnOperators

Produce an any_() clause against the parent object.

See the documentation for any_() for examples.

be sure to not confuse the newer ColumnOperators.any_() method with the legacy version of this method, the Comparator.any() method that’s specific to ARRAY, which uses a different calling style.

inherited from the ColumnOperators.asc() method of ColumnOperators

Produce a asc() clause against the parent object.

Return a tuple of (local_attr, remote_attr).

This attribute was originally intended to facilitate using the Query.join() method to join across the two relationships at once, however this makes use of a deprecated calling style.

To use select.join() or Query.join() with an association proxy, the current method is to make use of the AssociationProxyInstance.local_attr and AssociationProxyInstance.remote_attr attributes separately:

A future release may seek to provide a more succinct join pattern for association proxy attributes.

AssociationProxyInstance.local_attr

AssociationProxyInstance.remote_attr

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

inherited from the ColumnOperators.collate() method of ColumnOperators

Produce a collate() clause against the parent object, given the collation string.

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

Produce a proxied ‘has’ expression using EXISTS.

This expression will be a composed product using the Comparator.any() and/or Comparator.has() operators of the underlying proxied attributes.

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

inherited from the ColumnOperators.like() method of ColumnOperators

Implement the like operator.

In a column context, produces the expression:

other¶ – expression to be compared

optional escape character, renders the ESCAPE keyword, e.g.:

ColumnOperators.ilike()

The ‘local’ class attribute referenced by this AssociationProxyInstance.

AssociationProxyInstance.attr

AssociationProxyInstance.remote_attr

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

inherited from the Operators.operate() method of Operators

Operate on an argument.

This is the lowest level of operation, raises NotImplementedError by default.

Overriding this on a subclass can allow common behavior to be applied to all operations. For example, overriding ColumnOperators to apply func.lower() to the left and right side:

op¶ – Operator callable.

*other¶ – the ‘other’ side of the operation. Will be a single scalar for most operations.

**kwargs¶ – modifiers. These may be passed by special operators such as ColumnOperators.contains().

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

The ‘remote’ class attribute referenced by this AssociationProxyInstance.

AssociationProxyInstance.attr

AssociationProxyInstance.local_attr

inherited from the Operators.reverse_operate() method of Operators

Reverse operate on an argument.

Usage is the same as operate().

Return True if this AssociationProxyInstance proxies a scalar relationship on the local side.

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

The intermediary class handled by this AssociationProxyInstance.

Intercepted append/set/assignment events will result in the generation of new instances of this class.

inherited from the ColumnOperators.timetuple attribute of ColumnOperators

Hack, allows datetime objects to be compared on the LHS.

inherits from sqlalchemy.ext.associationproxy.AssociationProxyInstance

an AssociationProxyInstance that has an object as a target.

Implement the <= operator.

Implement the < operator.

Produce an all_() clause against the parent object.

Produce a proxied ‘any’ expression using EXISTS.

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

Produce a proxied ‘contains’ expression using EXISTS.

Produce a desc() clause against the parent object.

Produce a distinct() clause against the parent object.

Implement the ‘endswith’ operator.

Produce a proxied ‘has’ expression using EXISTS.

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

Return True if this AssociationProxyInstance proxies a scalar relationship on the local side.

Implement the startswith operator.

The intermediary class handled by this AssociationProxyInstance.

Hack, allows datetime objects to be compared on the LHS.

inherited from the sqlalchemy.sql.expression.ColumnOperators.__le__ method of ColumnOperators

Implement the <= operator.

In a column context, produces the clause a <= b.

inherited from the sqlalchemy.sql.expression.ColumnOperators.__lt__ method of ColumnOperators

Implement the < operator.

In a column context, produces the clause a < b.

inherited from the ColumnOperators.all_() method of ColumnOperators

Produce an all_() clause against the parent object.

See the documentation for all_() for examples.

be sure to not confuse the newer ColumnOperators.all_() method with the legacy version of this method, the Comparator.all() method that’s specific to ARRAY, which uses a different calling style.

inherited from the AssociationProxyInstance.any() method of AssociationProxyInstance

Produce a proxied ‘any’ expression using EXISTS.

This expression will be a composed product using the Comparator.any() and/or Comparator.has() operators of the underlying proxied attributes.

inherited from the ColumnOperators.any_() method of ColumnOperators

Produce an any_() clause against the parent object.

See the documentation for any_() for examples.

be sure to not confuse the newer ColumnOperators.any_() method with the legacy version of this method, the Comparator.any() method that’s specific to ARRAY, which uses a different calling style.

inherited from the ColumnOperators.asc() method of ColumnOperators

Produce a asc() clause against the parent object.

Return a tuple of (local_attr, remote_attr).

This attribute was originally intended to facilitate using the Query.join() method to join across the two relationships at once, however this makes use of a deprecated calling style.

To use select.join() or Query.join() with an association proxy, the current method is to make use of the AssociationProxyInstance.local_attr and AssociationProxyInstance.remote_attr attributes separately:

A future release may seek to provide a more succinct join pattern for association proxy attributes.

AssociationProxyInstance.local_attr

AssociationProxyInstance.remote_attr

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

inherited from the ColumnOperators.collate() method of ColumnOperators

Produce a collate() clause against the parent object, given the collation string.

inherited from the ColumnOperators.concat() method of ColumnOperators

Implement the ‘concat’ operator.

In a column context, produces the clause a || b, or uses the concat() operator on MySQL.

Produce a proxied ‘contains’ expression using EXISTS.

This expression will be a composed product using the Comparator.any(), Comparator.has(), and/or Comparator.contains() operators of the underlying proxied attributes.

inherited from the ColumnOperators.desc() method of ColumnOperators

Produce a desc() clause against the parent object.

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

inherited from the AssociationProxyInstance.has() method of AssociationProxyInstance

Produce a proxied ‘has’ expression using EXISTS.

This expression will be a composed product using the Comparator.any() and/or Comparator.has() operators of the underlying proxied attributes.

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

inherited from the ColumnOperators.like() method of ColumnOperators

Implement the like operator.

In a column context, produces the expression:

other¶ – expression to be compared

optional escape character, renders the ESCAPE keyword, e.g.:

ColumnOperators.ilike()

The ‘local’ class attribute referenced by this AssociationProxyInstance.

AssociationProxyInstance.attr

AssociationProxyInstance.remote_attr

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

inherited from the Operators.operate() method of Operators

Operate on an argument.

This is the lowest level of operation, raises NotImplementedError by default.

Overriding this on a subclass can allow common behavior to be applied to all operations. For example, overriding ColumnOperators to apply func.lower() to the left and right side:

op¶ – Operator callable.

*other¶ – the ‘other’ side of the operation. Will be a single scalar for most operations.

**kwargs¶ – modifiers. These may be passed by special operators such as ColumnOperators.contains().

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

The ‘remote’ class attribute referenced by this AssociationProxyInstance.

AssociationProxyInstance.attr

AssociationProxyInstance.local_attr

inherited from the Operators.reverse_operate() method of Operators

Reverse operate on an argument.

Usage is the same as operate().

inherited from the AssociationProxyInstance.scalar attribute of AssociationProxyInstance

Return True if this AssociationProxyInstance proxies a scalar relationship on the local side.

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

The intermediary class handled by this AssociationProxyInstance.

Intercepted append/set/assignment events will result in the generation of new instances of this class.

inherited from the ColumnOperators.timetuple attribute of ColumnOperators

Hack, allows datetime objects to be compared on the LHS.

inherits from sqlalchemy.ext.associationproxy.AssociationProxyInstance

an AssociationProxyInstance that has a database column as a target.

Implement the <= operator.

Implement the < operator.

Implement the != operator.

Produce an all_() clause against the parent object.

Produce a proxied ‘any’ expression using EXISTS.

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

Produce a proxied ‘has’ expression using EXISTS.

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

Return True if this AssociationProxyInstance proxies a scalar relationship on the local side.

Implement the startswith operator.

The intermediary class handled by this AssociationProxyInstance.

Hack, allows datetime objects to be compared on the LHS.

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

inherited from the AssociationProxyInstance.any() method of AssociationProxyInstance

Produce a proxied ‘any’ expression using EXISTS.

This expression will be a composed product using the Comparator.any() and/or Comparator.has() operators of the underlying proxied attributes.

inherited from the ColumnOperators.any_() method of ColumnOperators

Produce an any_() clause against the parent object.

See the documentation for any_() for examples.

be sure to not confuse the newer ColumnOperators.any_() method with the legacy version of this method, the Comparator.any() method that’s specific to ARRAY, which uses a different calling style.

inherited from the ColumnOperators.asc() method of ColumnOperators

Produce a asc() clause against the parent object.

Return a tuple of (local_attr, remote_attr).

This attribute was originally intended to facilitate using the Query.join() method to join across the two relationships at once, however this makes use of a deprecated calling style.

To use select.join() or Query.join() with an association proxy, the current method is to make use of the AssociationProxyInstance.local_attr and AssociationProxyInstance.remote_attr attributes separately:

A future release may seek to provide a more succinct join pattern for association proxy attributes.

AssociationProxyInstance.local_attr

AssociationProxyInstance.remote_attr

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

inherited from the ColumnOperators.collate() method of ColumnOperators

Produce a collate() clause against the parent object, given the collation string.

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

inherited from the AssociationProxyInstance.has() method of AssociationProxyInstance

Produce a proxied ‘has’ expression using EXISTS.

This expression will be a composed product using the Comparator.any() and/or Comparator.has() operators of the underlying proxied attributes.

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

inherited from the ColumnOperators.like() method of ColumnOperators

Implement the like operator.

In a column context, produces the expression:

other¶ – expression to be compared

optional escape character, renders the ESCAPE keyword, e.g.:

ColumnOperators.ilike()

The ‘local’ class attribute referenced by this AssociationProxyInstance.

AssociationProxyInstance.attr

AssociationProxyInstance.remote_attr

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

The ‘remote’ class attribute referenced by this AssociationProxyInstance.

AssociationProxyInstance.attr

AssociationProxyInstance.local_attr

inherited from the Operators.reverse_operate() method of Operators

Reverse operate on an argument.

Usage is the same as operate().

inherited from the AssociationProxyInstance.scalar attribute of AssociationProxyInstance

Return True if this AssociationProxyInstance proxies a scalar relationship on the local side.

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

The intermediary class handled by this AssociationProxyInstance.

Intercepted append/set/assignment events will result in the generation of new instances of this class.

inherited from the ColumnOperators.timetuple attribute of ColumnOperators

Hack, allows datetime objects to be compared on the LHS.

inherits from sqlalchemy.orm.base.InspectionAttrExtensionType

Symbol indicating an InspectionAttr that’s of type AssociationProxy.

Symbol indicating an InspectionAttr that’s of type AssociationProxy.

Is assigned to the InspectionAttr.extension_type attribute.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from __future__ import annotations

from typing import Final
from typing import List

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    kw: Mapped[List[Keyword]] = relationship(secondary=lambda: user_keyword_table)

    def __init__(self, name: str):
        self.name = name

    # proxy the 'keyword' attribute from the 'kw' relationship
    keywords: AssociationProxy[List[str]] = association_proxy("kw", "keyword")


class Keyword(Base):
    __tablename__ = "keyword"
    id: Mapped[int] = mapped_column(primary_key=True)
    keyword: Mapped[str] = mapped_column(String(64))

    def __init__(self, keyword: str):
        self.keyword = keyword


user_keyword_table: Final[Table] = Table(
    "user_keyword",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("keyword_id", Integer, ForeignKey("keyword.id"), primary_key=True),
)
```

Example 2 (json):
```json
>>> user = User("jek")
>>> user.keywords.append("cheese-inspector")
>>> user.keywords.append("snack-ninja")
>>> print(user.keywords)
['cheese-inspector', 'snack-ninja']
```

Example 3 (julia):
```julia
>>> # identical operations without using the association proxy
>>> user = User("jek")
>>> user.kw.append(Keyword("cheese-inspector"))
>>> user.kw.append(Keyword("snack-ninja"))
>>> print([keyword.keyword for keyword in user.kw])
['cheese-inspector', 'snack-ninja']
```

Example 4 (unknown):
```unknown
user.keywords.append("cheese-inspector")
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Hybrid Attributes¶
- Defining Expression Behavior Distinct from Attribute Behavior¶
- Using inplace to create pep-484 compliant hybrid properties¶
- Defining Setters¶
- Allowing Bulk ORM Update¶
- Working with Relationships¶

Home | Download this Documentation

Home | Download this Documentation

Define attributes on ORM-mapped classes that have “hybrid” behavior.

“hybrid” means the attribute has distinct behaviors defined at the class level and at the instance level.

The hybrid extension provides a special form of method decorator and has minimal dependencies on the rest of SQLAlchemy. Its basic theory of operation can work with any descriptor-based expression system.

Consider a mapping Interval, representing integer start and end values. We can define higher level functions on mapped classes that produce SQL expressions at the class level, and Python expression evaluation at the instance level. Below, each function decorated with hybrid_method or hybrid_property may receive self as an instance of the class, or may receive the class directly, depending on context:

Above, the length property returns the difference between the end and start attributes. With an instance of Interval, this subtraction occurs in Python, using normal Python descriptor mechanics:

When dealing with the Interval class itself, the hybrid_property descriptor evaluates the function body given the Interval class as the argument, which when evaluated with SQLAlchemy expression mechanics returns a new SQL expression:

Filtering methods such as Select.filter_by() are supported with hybrid attributes as well:

The Interval class example also illustrates two methods, contains() and intersects(), decorated with hybrid_method. This decorator applies the same idea to methods that hybrid_property applies to attributes. The methods return boolean values, and take advantage of the Python | and & bitwise operators to produce equivalent instance-level and SQL expression-level boolean behavior:

In the previous section, our usage of the & and | bitwise operators within the Interval.contains and Interval.intersects methods was fortunate, considering our functions operated on two boolean values to return a new one. In many cases, the construction of an in-Python function and a SQLAlchemy SQL expression have enough differences that two separate Python expressions should be defined. The hybrid decorator defines a modifier hybrid_property.expression() for this purpose. As an example we’ll define the radius of the interval, which requires the usage of the absolute value function:

In the above example, the hybrid_property first assigned to the name Interval.radius is amended by a subsequent method called Interval._radius_expression, using the decorator @radius.inplace.expression, which chains together two modifiers hybrid_property.inplace and hybrid_property.expression. The use of hybrid_property.inplace indicates that the hybrid_property.expression() modifier should mutate the existing hybrid object at Interval.radius in place, without creating a new object. Notes on this modifier and its rationale are discussed in the next section Using inplace to create pep-484 compliant hybrid properties. The use of @classmethod is optional, and is strictly to give typing tools a hint that cls in this case is expected to be the Interval class, and not an instance of Interval.

hybrid_property.inplace as well as the use of @classmethod for proper typing support are available as of SQLAlchemy 2.0.4, and will not work in earlier versions.

With Interval.radius now including an expression element, the SQL function ABS() is returned when accessing Interval.radius at the class level:

In the previous section, a hybrid_property decorator is illustrated which includes two separate method-level functions being decorated, both to produce a single object attribute referenced as Interval.radius. There are actually several different modifiers we can use for hybrid_property including hybrid_property.expression(), hybrid_property.setter() and hybrid_property.update_expression().

SQLAlchemy’s hybrid_property decorator intends that adding on these methods may be done in the identical manner as Python’s built-in @property decorator, where idiomatic use is to continue to redefine the attribute repeatedly, using the same attribute name each time, as in the example below that illustrates the use of hybrid_property.setter() and hybrid_property.expression() for the Interval.radius descriptor:

Above, there are three Interval.radius methods, but as each are decorated, first by the hybrid_property decorator and then by the @radius name itself, the end effect is that Interval.radius is a single attribute with three different functions contained within it. This style of use is taken from Python’s documented use of @property. It is important to note that the way both @property as well as hybrid_property work, a copy of the descriptor is made each time. That is, each call to @radius.expression, @radius.setter etc. make a new object entirely. This allows the attribute to be re-defined in subclasses without issue (see Reusing Hybrid Properties across Subclasses later in this section for how this is used).

However, the above approach is not compatible with typing tools such as mypy and pyright. Python’s own @property decorator does not have this limitation only because these tools hardcode the behavior of @property, meaning this syntax is not available to SQLAlchemy under PEP 484 compliance.

In order to produce a reasonable syntax while remaining typing compliant, the hybrid_property.inplace decorator allows the same decorator to be reused with different method names, while still producing a single decorator under one name:

Using hybrid_property.inplace further qualifies the use of the decorator that a new copy should not be made, thereby maintaining the Interval.radius name while allowing additional methods Interval._radius_setter and Interval._radius_expression to be differently named.

Added in version 2.0.4: Added hybrid_property.inplace to allow less verbose construction of composite hybrid_property objects while not having to use repeated method names. Additionally allowed the use of @classmethod within hybrid_property.expression, hybrid_property.update_expression, and hybrid_property.comparator to allow typing tools to identify cls as a class and not an instance in the method signature.

The hybrid_property.setter() modifier allows the construction of a custom setter method, that can modify values on the object:

The length(self, value) method is now called upon set:

A hybrid can define a custom “UPDATE” handler for when using ORM-enabled updates, allowing the hybrid to be used in the SET clause of the update.

Normally, when using a hybrid with update(), the SQL expression is used as the column that’s the target of the SET. If our Interval class had a hybrid start_point that linked to Interval.start, this could be substituted directly:

However, when using a composite hybrid like Interval.length, this hybrid represents more than one column. We can set up a handler that will accommodate a value passed in the VALUES expression which can affect this, using the hybrid_property.update_expression() decorator. A handler that works similarly to our setter would be:

Above, if we use Interval.length in an UPDATE expression, we get a hybrid SET expression:

This SET expression is accommodated by the ORM automatically.

ORM-Enabled INSERT, UPDATE, and DELETE statements - includes background on ORM-enabled UPDATE statements

There’s no essential difference when creating hybrids that work with related objects as opposed to column-based data. The need for distinct expressions tends to be greater. The two variants we’ll illustrate are the “join-dependent” hybrid, and the “correlated subquery” hybrid.

Consider the following declarative mapping which relates a User to a SavingsAccount:

The above hybrid property balance works with the first SavingsAccount entry in the list of accounts for this user. The in-Python getter/setter methods can treat accounts as a Python list available on self.

The User.balance getter in the above example accesses the self.accounts collection, which will normally be loaded via the selectinload() loader strategy configured on the User.balance relationship(). The default loader strategy when not otherwise stated on relationship() is lazyload(), which emits SQL on demand. When using asyncio, on-demand loaders such as lazyload() are not supported, so care should be taken to ensure the self.accounts collection is accessible to this hybrid accessor when using asyncio.

At the expression level, it’s expected that the User class will be used in an appropriate context such that an appropriate join to SavingsAccount will be present:

Note however, that while the instance level accessors need to worry about whether self.accounts is even present, this issue expresses itself differently at the SQL expression level, where we basically would use an outer join:

We can, of course, forego being dependent on the enclosing query’s usage of joins in favor of the correlated subquery, which can portably be packed into a single column expression. A correlated subquery is more portable, but often performs more poorly at the SQL level. Using the same technique illustrated at Using column_property, we can adjust our SavingsAccount example to aggregate the balances for all accounts, and use a correlated subquery for the column expression:

The above recipe will give us the balance column which renders a correlated SELECT:

The hybrid property also includes a helper that allows construction of custom comparators. A comparator object allows one to customize the behavior of each SQLAlchemy expression operator individually. They are useful when creating custom types that have some highly idiosyncratic behavior on the SQL side.

The hybrid_property.comparator() decorator introduced in this section replaces the use of the hybrid_property.expression() decorator. They cannot be used together.

The example class below allows case-insensitive comparisons on the attribute named word_insensitive:

Above, SQL expressions against word_insensitive will apply the LOWER() SQL function to both sides:

The CaseInsensitiveComparator above implements part of the ColumnOperators interface. A “coercion” operation like lowercasing can be applied to all comparison operations (i.e. eq, lt, gt, etc.) using Operators.operate():

A hybrid can be referred to from a superclass, to allow modifying methods like hybrid_property.getter(), hybrid_property.setter() to be used to redefine those methods on a subclass. This is similar to how the standard Python @property object works:

Above, the FirstNameLastName class refers to the hybrid from FirstNameOnly.name to repurpose its getter and setter for the subclass.

When overriding hybrid_property.expression() and hybrid_property.comparator() alone as the first reference to the superclass, these names conflict with the same-named accessors on the class- level QueryableAttribute object returned at the class level. To override these methods when referring directly to the parent class descriptor, add the special qualifier hybrid_property.overrides, which will de- reference the instrumented attribute back to the hybrid object:

Note in our previous example, if we were to compare the word_insensitive attribute of a SearchWord instance to a plain Python string, the plain Python string would not be coerced to lower case - the CaseInsensitiveComparator we built, being returned by @word_insensitive.comparator, only applies to the SQL side.

A more comprehensive form of the custom comparator is to construct a Hybrid Value Object. This technique applies the target value or expression to a value object which is then returned by the accessor in all cases. The value object allows control of all operations upon the value as well as how compared values are treated, both on the SQL expression side as well as the Python value side. Replacing the previous CaseInsensitiveComparator class with a new CaseInsensitiveWord class:

Above, the CaseInsensitiveWord object represents self.word, which may be a SQL function, or may be a Python native. By overriding operate() and __clause_element__() to work in terms of self.word, all comparison operations will work against the “converted” form of word, whether it be SQL side or Python side. Our SearchWord class can now deliver the CaseInsensitiveWord object unconditionally from a single hybrid call:

The word_insensitive attribute now has case-insensitive comparison behavior universally, including SQL expression vs. Python expression (note the Python value is converted to lower case on the Python side here):

SQL expression versus SQL expression:

Python only expression:

The Hybrid Value pattern is very useful for any kind of value that may have multiple representations, such as timestamps, time deltas, units of measurement, currencies and encrypted passwords.

Hybrids and Value Agnostic Types - on the techspot.zzzeek.org blog

Value Agnostic Types, Part II - on the techspot.zzzeek.org blog

A helper class that allows easy construction of custom PropComparator classes for usage with hybrids.

A decorator which allows definition of a Python object method with both instance-level and class-level behavior.

A decorator which allows definition of a Python descriptor with both instance-level and class-level behavior.

inherits from sqlalchemy.orm.base.InspectionAttrInfo, typing.Generic

A decorator which allows definition of a Python object method with both instance-level and class-level behavior.

Create a new hybrid_method.

Provide a modifying decorator that defines a SQL-expression producing method.

The extension type, if any. Defaults to NotExtension.NOT_EXTENSION

True if this object is a Python descriptor.

Create a new hybrid_method.

Usage is typically via decorator:

Provide a modifying decorator that defines a SQL-expression producing method.

The extension type, if any. Defaults to NotExtension.NOT_EXTENSION

AssociationProxyExtensionType

Return the inplace mutator for this hybrid_method.

The hybrid_method class already performs “in place” mutation when the hybrid_method.expression() decorator is called, so this attribute returns Self.

Added in version 2.0.4.

Using inplace to create pep-484 compliant hybrid properties

True if this object is a Python descriptor.

This can refer to one of many types. Usually a QueryableAttribute which handles attributes events on behalf of a MapperProperty. But can also be an extension type such as AssociationProxy or hybrid_property. The InspectionAttr.extension_type will refer to a constant identifying the specific subtype.

Mapper.all_orm_descriptors

inherits from sqlalchemy.orm.base.InspectionAttrInfo, sqlalchemy.orm.base.ORMDescriptor

A decorator which allows definition of a Python descriptor with both instance-level and class-level behavior.

Create a new hybrid_property.

Provide a modifying decorator that defines a custom comparator producing method.

Provide a modifying decorator that defines a deletion method.

Provide a modifying decorator that defines a SQL-expression producing method.

The extension type, if any. Defaults to NotExtension.NOT_EXTENSION

Provide a modifying decorator that defines a getter method.

True if this object is a Python descriptor.

Provide a modifying decorator that defines a setter method.

Provide a modifying decorator that defines an UPDATE tuple producing method.

Create a new hybrid_property.

Usage is typically via decorator:

Provide a modifying decorator that defines a custom comparator producing method.

The return value of the decorated method should be an instance of Comparator.

The hybrid_property.comparator() decorator replaces the use of the hybrid_property.expression() decorator. They cannot be used together.

When a hybrid is invoked at the class level, the Comparator object given here is wrapped inside of a specialized QueryableAttribute, which is the same kind of object used by the ORM to represent other mapped attributes. The reason for this is so that other class-level attributes such as docstrings and a reference to the hybrid itself may be maintained within the structure that’s returned, without any modifications to the original comparator object passed in.

When referring to a hybrid property from an owning class (e.g. SomeClass.some_hybrid), an instance of QueryableAttribute is returned, representing the expression or comparator object as this hybrid object. However, that object itself has accessors called expression and comparator; so when attempting to override these decorators on a subclass, it may be necessary to qualify it using the hybrid_property.overrides modifier first. See that modifier for details.

Provide a modifying decorator that defines a deletion method.

Provide a modifying decorator that defines a SQL-expression producing method.

When a hybrid is invoked at the class level, the SQL expression given here is wrapped inside of a specialized QueryableAttribute, which is the same kind of object used by the ORM to represent other mapped attributes. The reason for this is so that other class-level attributes such as docstrings and a reference to the hybrid itself may be maintained within the structure that’s returned, without any modifications to the original SQL expression passed in.

When referring to a hybrid property from an owning class (e.g. SomeClass.some_hybrid), an instance of QueryableAttribute is returned, representing the expression or comparator object as well as this hybrid object. However, that object itself has accessors called expression and comparator; so when attempting to override these decorators on a subclass, it may be necessary to qualify it using the hybrid_property.overrides modifier first. See that modifier for details.

Defining Expression Behavior Distinct from Attribute Behavior

The extension type, if any. Defaults to NotExtension.NOT_EXTENSION

AssociationProxyExtensionType

Provide a modifying decorator that defines a getter method.

Added in version 1.2.

Return the inplace mutator for this hybrid_property.

This is to allow in-place mutation of the hybrid, allowing the first hybrid method of a certain name to be reused in order to add more methods without having to name those methods the same, e.g.:

Added in version 2.0.4.

Using inplace to create pep-484 compliant hybrid properties

True if this object is a Python descriptor.

This can refer to one of many types. Usually a QueryableAttribute which handles attributes events on behalf of a MapperProperty. But can also be an extension type such as AssociationProxy or hybrid_property. The InspectionAttr.extension_type will refer to a constant identifying the specific subtype.

Mapper.all_orm_descriptors

Prefix for a method that is overriding an existing attribute.

The hybrid_property.overrides accessor just returns this hybrid object, which when called at the class level from a parent class, will de-reference the “instrumented attribute” normally returned at this level, and allow modifying decorators like hybrid_property.expression() and hybrid_property.comparator() to be used without conflicting with the same-named attributes normally present on the QueryableAttribute:

Added in version 1.2.

Reusing Hybrid Properties across Subclasses

Provide a modifying decorator that defines a setter method.

Provide a modifying decorator that defines an UPDATE tuple producing method.

The method accepts a single value, which is the value to be rendered into the SET clause of an UPDATE statement. The method should then process this value into individual column expressions that fit into the ultimate SET clause, and return them as a sequence of 2-tuples. Each tuple contains a column expression as the key and a value to be rendered.

Added in version 1.2.

inherits from sqlalchemy.orm.PropComparator

A helper class that allows easy construction of custom PropComparator classes for usage with hybrids.

inherits from sqlalchemy.orm.base.InspectionAttrExtensionType

Symbol indicating an InspectionAttr that’s of type hybrid_method.

Symbol indicating an InspectionAttr that’s of type hybrid_method.

Is assigned to the InspectionAttr.extension_type attribute.

Mapper.all_orm_attributes

of type hybrid_method.

Is assigned to the InspectionAttr.extension_type attribute.

Mapper.all_orm_attributes

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from __future__ import annotations

from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Interval(Base):
    __tablename__ = "interval"

    id: Mapped[int] = mapped_column(primary_key=True)
    start: Mapped[int]
    end: Mapped[int]

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    @hybrid_property
    def length(self) -> int:
        return self.end - self.start

    @hybrid_method
    def contains(self, point: int) -> bool:
        return (self.start <= point) & (point <= self.end)

    @hybrid_method
    def intersects(self, other: Interval) -> bool:
        return self.contains(other.start) | self.contains(other.end)
```

Example 2 (unknown):
```unknown
>>> i1 = Interval(5, 10)
>>> i1.length
5
```

Example 3 (sql):
```sql
>>> from sqlalchemy import select
>>> print(select(Interval.length))
SELECT interval."end" - interval.start AS length
FROM interval
>>> print(select(Interval).filter(Interval.length > 10))
SELECT interval.id, interval.start, interval."end"
FROM interval
WHERE interval."end" - interval.start > :param_1
```

Example 4 (sql):
```sql
>>> print(select(Interval).filter_by(length=5))
SELECT interval.id, interval.start, interval."end"
FROM interval
WHERE interval."end" - interval.start = :param_1
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Automap¶
- Basic Use¶
- Generating Mappings from an Existing MetaData¶
- Generating Mappings from Multiple Schemas¶
  - Automapping same-named tables across multiple schemas¶
- Specifying Classes Explicitly¶

Home | Download this Documentation

Home | Download this Documentation

Define an extension to the sqlalchemy.ext.declarative system which automatically generates mapped classes and relationships from a database schema, typically though not necessarily one which is reflected.

It is hoped that the AutomapBase system provides a quick and modernized solution to the problem that the very famous SQLSoup also tries to solve, that of generating a quick and rudimentary object model from an existing database on the fly. By addressing the issue strictly at the mapper configuration level, and integrating fully with existing Declarative class techniques, AutomapBase seeks to provide a well-integrated approach to the issue of expediently auto-generating ad-hoc mappings.

The Automap extension is geared towards a “zero declaration” approach, where a complete ORM model including classes and pre-named relationships can be generated on the fly from a database schema. For applications that still want to use explicit class declarations including explicit relationship definitions in conjunction with reflection of tables, the DeferredReflection class, described at Using DeferredReflection, is a better choice.

The simplest usage is to reflect an existing database into a new model. We create a new AutomapBase class in a similar manner as to how we create a declarative base class, using automap_base(). We then call AutomapBase.prepare() on the resulting base class, asking it to reflect the schema and produce mappings:

Above, calling AutomapBase.prepare() while passing along the AutomapBase.prepare.reflect parameter indicates that the MetaData.reflect() method will be called on this declarative base classes’ MetaData collection; then, each viable Table within the MetaData will get a new mapped class generated automatically. The ForeignKeyConstraint objects which link the various tables together will be used to produce new, bidirectional relationship() objects between classes. The classes and relationships follow along a default naming scheme that we can customize. At this point, our basic mapping consisting of related User and Address classes is ready to use in the traditional way.

By viable, we mean that for a table to be mapped, it must specify a primary key. Additionally, if the table is detected as being a pure association table between two other tables, it will not be directly mapped and will instead be configured as a many-to-many table between the mappings for the two referring tables.

We can pass a pre-declared MetaData object to automap_base(). This object can be constructed in any way, including programmatically, from a serialized file, or from itself being reflected using MetaData.reflect(). Below we illustrate a combination of reflection and explicit table declaration:

The AutomapBase.prepare() method when used with reflection may reflect tables from one schema at a time at most, using the AutomapBase.prepare.schema parameter to indicate the name of a schema to be reflected from. In order to populate the AutomapBase with tables from multiple schemas, AutomapBase.prepare() may be invoked multiple times, each time passing a different name to the AutomapBase.prepare.schema parameter. The AutomapBase.prepare() method keeps an internal list of Table objects that have already been mapped, and will add new mappings only for those Table objects that are new since the last time AutomapBase.prepare() was run:

Added in version 2.0: The AutomapBase.prepare() method may be called any number of times; only newly added tables will be mapped on each run. Previously in version 1.4 and earlier, multiple calls would cause errors as it would attempt to re-map an already mapped class. The previous workaround approach of invoking MetaData.reflect() directly remains available as well.

For the common case where multiple schemas may have same-named tables and therefore would generate same-named classes, conflicts can be resolved either through use of the AutomapBase.prepare.classname_for_table hook to apply different classnames on a per-schema basis, or by using the AutomapBase.prepare.modulename_for_table hook, which allows disambiguation of same-named classes by changing their effective __module__ attribute. In the example below, this hook is used to create a __module__ attribute for all classes that is of the form mymodule.<schemaname>, where the schema name default is used if no schema is present:

The same named-classes are organized into a hierarchical collection available at AutomapBase.by_module. This collection is traversed using the dot-separated name of a particular package/module down into the desired class name.

When using the AutomapBase.prepare.modulename_for_table hook to return a new __module__ that is not None, the class is not placed into the AutomapBase.classes collection; only classes that were not given an explicit modulename are placed here, as the collection cannot represent same-named classes individually.

In the example above, if the database contained a table named accounts in all three of the default schema, the test_schema schema, and the test_schema_2 schema, three separate classes will be available as:

The default module namespace generated for all AutomapBase classes is sqlalchemy.ext.automap. If no AutomapBase.prepare.modulename_for_table hook is used, the contents of AutomapBase.by_module will be entirely within the sqlalchemy.ext.automap namespace (e.g. MyBase.by_module.sqlalchemy.ext.automap.<classname>), which would contain the same series of classes as what would be seen in AutomapBase.classes. Therefore it’s generally only necessary to use AutomapBase.by_module when explicit __module__ conventions are present.

If explicit classes are expected to be prominent in an application, consider using DeferredReflection instead.

The automap extension allows classes to be defined explicitly, in a way similar to that of the DeferredReflection class. Classes that extend from AutomapBase act like regular declarative classes, but are not immediately mapped after their construction, and are instead mapped when we call AutomapBase.prepare(). The AutomapBase.prepare() method will make use of the classes we’ve established based on the table name we use. If our schema contains tables user and address, we can define one or both of the classes to be used:

Above, one of the more intricate details is that we illustrated overriding one of the relationship() objects that automap would have created. To do this, we needed to make sure the names match up with what automap would normally generate, in that the relationship name would be User.address_collection and the name of the class referred to, from automap’s perspective, is called address, even though we are referring to it as Address within our usage of this class.

automap is tasked with producing mapped classes and relationship names based on a schema, which means it has decision points in how these names are determined. These three decision points are provided using functions which can be passed to the AutomapBase.prepare() method, and are known as classname_for_table(), name_for_scalar_relationship(), and name_for_collection_relationship(). Any or all of these functions are provided as in the example below, where we use a “camel case” scheme for class names and a “pluralizer” for collection names using the Inflect package:

From the above mapping, we would now have classes User and Address, where the collection from User to Address is called User.addresses:

The vast majority of what automap accomplishes is the generation of relationship() structures based on foreign keys. The mechanism by which this works for many-to-one and one-to-many relationships is as follows:

A given Table, known to be mapped to a particular class, is examined for ForeignKeyConstraint objects.

From each ForeignKeyConstraint, the remote Table object present is matched up to the class to which it is to be mapped, if any, else it is skipped.

As the ForeignKeyConstraint we are examining corresponds to a reference from the immediate mapped class, the relationship will be set up as a many-to-one referring to the referred class; a corresponding one-to-many backref will be created on the referred class referring to this class.

If any of the columns that are part of the ForeignKeyConstraint are not nullable (e.g. nullable=False), a relationship.cascade keyword argument of all, delete-orphan will be added to the keyword arguments to be passed to the relationship or backref. If the ForeignKeyConstraint reports that ForeignKeyConstraint.ondelete is set to CASCADE for a not null or SET NULL for a nullable set of columns, the option relationship.passive_deletes flag is set to True in the set of relationship keyword arguments. Note that not all backends support reflection of ON DELETE.

The names of the relationships are determined using the AutomapBase.prepare.name_for_scalar_relationship and AutomapBase.prepare.name_for_collection_relationship callable functions. It is important to note that the default relationship naming derives the name from the the actual class name. If you’ve given a particular class an explicit name by declaring it, or specified an alternate class naming scheme, that’s the name from which the relationship name will be derived.

The classes are inspected for an existing mapped property matching these names. If one is detected on one side, but none on the other side, AutomapBase attempts to create a relationship on the missing side, then uses the relationship.back_populates parameter in order to point the new relationship to the other side.

In the usual case where no relationship is on either side, AutomapBase.prepare() produces a relationship() on the “many-to-one” side and matches it to the other using the relationship.backref parameter.

Production of the relationship() and optionally the backref() is handed off to the AutomapBase.prepare.generate_relationship function, which can be supplied by the end-user in order to augment the arguments passed to relationship() or backref() or to make use of custom implementations of these functions.

The AutomapBase.prepare.generate_relationship hook can be used to add parameters to relationships. For most cases, we can make use of the existing generate_relationship() function to return the object, after augmenting the given keyword dictionary with our own arguments.

Below is an illustration of how to send relationship.cascade and relationship.passive_deletes options along to all one-to-many relationships:

automap will generate many-to-many relationships, e.g. those which contain a secondary argument. The process for producing these is as follows:

A given Table is examined for ForeignKeyConstraint objects, before any mapped class has been assigned to it.

If the table contains two and exactly two ForeignKeyConstraint objects, and all columns within this table are members of these two ForeignKeyConstraint objects, the table is assumed to be a “secondary” table, and will not be mapped directly.

The two (or one, for self-referential) external tables to which the Table refers to are matched to the classes to which they will be mapped, if any.

If mapped classes for both sides are located, a many-to-many bi-directional relationship() / backref() pair is created between the two classes.

The override logic for many-to-many works the same as that of one-to-many/ many-to-one; the generate_relationship() function is called upon to generate the structures and existing attributes will be maintained.

automap will not generate any relationships between two classes that are in an inheritance relationship. That is, with two classes given as follows:

The foreign key from Engineer to Employee is used not for a relationship, but to establish joined inheritance between the two classes.

Note that this means automap will not generate any relationships for foreign keys that link from a subclass to a superclass. If a mapping has actual relationships from subclass to superclass as well, those need to be explicit. Below, as we have two separate foreign keys from Engineer to Employee, we need to set up both the relationship we want as well as the inherit_condition, as these are not things SQLAlchemy can guess:

In the case of naming conflicts during mapping, override any of classname_for_table(), name_for_scalar_relationship(), and name_for_collection_relationship() as needed. For example, if automap is attempting to name a many-to-one relationship the same as an existing column, an alternate convention can be conditionally selected. Given a schema:

The above schema will first automap the table_a table as a class named table_a; it will then automap a relationship onto the class for table_b with the same name as this related class, e.g. table_a. This relationship name conflicts with the mapping column table_b.table_a, and will emit an error on mapping.

We can resolve this conflict by using an underscore as follows:

Alternatively, we can change the name on the column side. The columns that are mapped can be modified using the technique described at Naming Declarative Mapped Columns Explicitly, by assigning the column explicitly to a new name:

As noted previously, automap has no dependency on reflection, and can make use of any collection of Table objects within a MetaData collection. From this, it follows that automap can also be used generate missing relationships given an otherwise complete model that fully defines table metadata:

Above, given mostly complete User and Address mappings, the ForeignKey which we defined on Address.user_id allowed a bidirectional relationship pair Address.user and User.address_collection to be generated on the mapped classes.

Note that when subclassing AutomapBase, the AutomapBase.prepare() method is required; if not called, the classes we’ve declared are in an un-mapped state.

The MetaData and Table objects support an event hook DDLEvents.column_reflect() that may be used to intercept the information reflected about a database column before the Column object is constructed. For example if we wanted to map columns using a naming convention such as "attr_<columnname>", the event could be applied as:

Added in version 1.4.0b2: the DDLEvents.column_reflect() event may be applied to a MetaData object.

DDLEvents.column_reflect()

Automating Column Naming Schemes from Reflected Tables - in the ORM mapping documentation

automap_base([declarative_base], **kw)

Produce a declarative automap base.

Base class for an “automap” schema.

classname_for_table(base, tablename, table)

Return the class name that should be used, given the name of a table.

generate_relationship(base, direction, return_fn, attrname, ..., **kw)

Generate a relationship() or backref() on behalf of two mapped classes.

name_for_collection_relationship(base, local_cls, referred_cls, constraint)

Return the attribute name that should be used to refer from one class to another, for a collection reference.

name_for_scalar_relationship(base, local_cls, referred_cls, constraint)

Return the attribute name that should be used to refer from one class to another, for a scalar object reference.

Produce a declarative automap base.

This function produces a new base class that is a product of the AutomapBase class as well a declarative base produced by declarative_base().

All parameters other than declarative_base are keyword arguments that are passed directly to the declarative_base() function.

declarative_base¶ – an existing class produced by declarative_base(). When this is passed, the function no longer invokes declarative_base() itself, and all other keyword arguments are ignored.

**kw¶ – keyword arguments are passed along to declarative_base().

Base class for an “automap” schema.

The AutomapBase class can be compared to the “declarative base” class that is produced by the declarative_base() function. In practice, the AutomapBase class is always used as a mixin along with an actual declarative base.

A new subclassable AutomapBase is typically instantiated using the automap_base() function.

An instance of Properties containing a hierarchal structure of dot-separated module names linked to classes.

An instance of Properties containing classes.

Refers to the MetaData collection that will be used for new Table objects.

Extract mapped classes and relationships from the MetaData and perform mappings.

An instance of Properties containing a hierarchal structure of dot-separated module names linked to classes.

This collection is an alternative to the AutomapBase.classes collection that is useful when making use of the AutomapBase.prepare.modulename_for_table parameter, which will apply distinct __module__ attributes to generated classes.

The default __module__ an automap-generated class is sqlalchemy.ext.automap; to access this namespace using AutomapBase.by_module looks like:

If a class had a __module__ of mymodule.account, accessing this namespace looks like:

Added in version 2.0.

Generating Mappings from Multiple Schemas

An instance of Properties containing classes.

This object behaves much like the .c collection on a table. Classes are present under the name they were given, e.g.:

For class names that overlap with a method name of Properties, such as items(), the getitem form is also supported:

Refers to the MetaData collection that will be used for new Table objects.

Accessing Table and Metadata

Extract mapped classes and relationships from the MetaData and perform mappings.

For full documentation and examples see Basic Use.

autoload_with¶ – an Engine or Connection with which to perform schema reflection; when specified, the MetaData.reflect() method will be invoked within the scope of this method.

engine¶ – legacy; use AutomapBase.autoload_with. Used to indicate the Engine or Connection with which to reflect tables with, if AutomapBase.reflect is True.

reflect¶ – legacy; use AutomapBase.autoload_with. Indicates that MetaData.reflect() should be invoked.

classname_for_table¶ – callable function which will be used to produce new class names, given a table name. Defaults to classname_for_table().

modulename_for_table¶ –

callable function which will be used to produce the effective __module__ for an internally generated class, to allow for multiple classes of the same name in a single automap base which would be in different “modules”.

Defaults to None, which will indicate that __module__ will not be set explicitly; the Python runtime will use the value sqlalchemy.ext.automap for these classes.

When assigning __module__ to generated classes, they can be accessed based on dot-separated module names using the AutomapBase.by_module collection. Classes that have an explicit __module_ assigned using this hook do not get placed into the AutomapBase.classes collection, only into AutomapBase.by_module.

Added in version 2.0.

Generating Mappings from Multiple Schemas

name_for_scalar_relationship¶ – callable function which will be used to produce relationship names for scalar relationships. Defaults to name_for_scalar_relationship().

name_for_collection_relationship¶ – callable function which will be used to produce relationship names for collection-oriented relationships. Defaults to name_for_collection_relationship().

generate_relationship¶ – callable function which will be used to actually generate relationship() and backref() constructs. Defaults to generate_relationship().

collection_class¶ – the Python collection class that will be used when a new relationship() object is created that represents a collection. Defaults to list.

Schema name to reflect when reflecting tables using the AutomapBase.prepare.autoload_with parameter. The name is passed to the MetaData.reflect.schema parameter of MetaData.reflect(). When omitted, the default schema in use by the database connection is used.

The AutomapBase.prepare.schema parameter supports reflection of a single schema at a time. In order to include tables from many schemas, use multiple calls to AutomapBase.prepare().

For an overview of multiple-schema automap including the use of additional naming conventions to resolve table name conflicts, see the section Generating Mappings from Multiple Schemas.

Added in version 2.0: AutomapBase.prepare() supports being directly invoked any number of times, keeping track of tables that have already been processed to avoid processing them a second time.

reflection_options¶ –

When present, this dictionary of options will be passed to MetaData.reflect() to supply general reflection-specific options like only and/or dialect-specific options like oracle_resolve_synonyms.

Added in version 1.4.

Return the class name that should be used, given the name of a table.

The default implementation is:

Alternate implementations can be specified using the AutomapBase.prepare.classname_for_table parameter.

base¶ – the AutomapBase class doing the prepare.

tablename¶ – string name of the Table.

table¶ – the Table object itself.

In Python 2, the string used for the class name must be a non-Unicode object, e.g. a str() object. The .name attribute of Table is typically a Python unicode subclass, so the str() function should be applied to this name, after accounting for any non-ASCII characters.

Return the attribute name that should be used to refer from one class to another, for a scalar object reference.

The default implementation is:

Alternate implementations can be specified using the AutomapBase.prepare.name_for_scalar_relationship parameter.

base¶ – the AutomapBase class doing the prepare.

local_cls¶ – the class to be mapped on the local side.

referred_cls¶ – the class to be mapped on the referring side.

constraint¶ – the ForeignKeyConstraint that is being inspected to produce this relationship.

Return the attribute name that should be used to refer from one class to another, for a collection reference.

The default implementation is:

Alternate implementations can be specified using the AutomapBase.prepare.name_for_collection_relationship parameter.

base¶ – the AutomapBase class doing the prepare.

local_cls¶ – the class to be mapped on the local side.

referred_cls¶ – the class to be mapped on the referring side.

constraint¶ – the ForeignKeyConstraint that is being inspected to produce this relationship.

Generate a relationship() or backref() on behalf of two mapped classes.

An alternate implementation of this function can be specified using the AutomapBase.prepare.generate_relationship parameter.

The default implementation of this function is as follows:

base¶ – the AutomapBase class doing the prepare.

direction¶ – indicate the “direction” of the relationship; this will be one of ONETOMANY, MANYTOONE, MANYTOMANY.

return_fn¶ – the function that is used by default to create the relationship. This will be either relationship() or backref(). The backref() function’s result will be used to produce a new relationship() in a second step, so it is critical that user-defined implementations correctly differentiate between the two functions, if a custom relationship function is being used.

attrname¶ – the attribute name to which this relationship is being assigned. If the value of generate_relationship.return_fn is the backref() function, then this name is the name that is being assigned to the backref.

local_cls¶ – the “local” class to which this relationship or backref will be locally present.

referred_cls¶ – the “referred” class to which the relationship or backref refers to.

**kw¶ – all additional keyword arguments are passed along to the function.

a relationship() or backref() construct, as dictated by the generate_relationship.return_fn parameter.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

Base = automap_base()

# engine, suppose it has two tables 'user' and 'address' set up
engine = create_engine("sqlite:///mydatabase.db")

# reflect the tables
Base.prepare(autoload_with=engine)

# mapped classes are now created with names by default
# matching that of the table name.
User = Base.classes.user
Address = Base.classes.address

session = Session(engine)

# rudimentary relationships are produced
session.add(Address(email_address="foo@bar.com", user=User(name="foo")))
session.commit()

# collection-based relationships are by default named
# "<classname>_collection"
u1 = session.query(User).first()
print(u1.address_collection)
```

Example 2 (python):
```python
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey
from sqlalchemy.ext.automap import automap_base

engine = create_engine("sqlite:///mydatabase.db")

# produce our own MetaData object
metadata = MetaData()

# we can reflect it ourselves from a database, using options
# such as 'only' to limit what tables we look at...
metadata.reflect(engine, only=["user", "address"])

# ... or just define our own Table objects with it (or combine both)
Table(
    "user_order",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user.id")),
)

# we can then produce a set of mappings from this MetaData.
Base = automap_base(metadata=metadata)

# calling prepare() just sets up mapped classes and relationships.
Base.prepare()

# mapped classes are ready
User = Base.classes.user
Address = Base.classes.address
Order = Base.classes.user_order
```

Example 3 (python):
```python
e = create_engine("postgresql://scott:tiger@localhost/test")

Base.metadata.create_all(e)

Base = automap_base()

Base.prepare(e)
Base.prepare(e, schema="test_schema")
Base.prepare(e, schema="test_schema_2")
```

Example 4 (python):
```python
e = create_engine("postgresql://scott:tiger@localhost/test")

Base.metadata.create_all(e)


def module_name_for_table(cls, tablename, table):
    if table.schema is not None:
        return f"mymodule.{table.schema}"
    else:
        return f"mymodule.default"


Base = automap_base()

Base.prepare(e, modulename_for_table=module_name_for_table)
Base.prepare(
    e, schema="test_schema", modulename_for_table=module_name_for_table
)
Base.prepare(
    e, schema="test_schema_2", modulename_for_table=module_name_for_table
)
```

---
