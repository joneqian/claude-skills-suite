# Sqlalchemy - Events

**Pages:** 4

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/core/event.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Core
    - Project Versions
- Events¶
- Event Registration¶
- Named Argument Styles¶
- Targets¶
- Modifiers¶
- Events and Multiprocessing¶

Home | Download this Documentation

Home | Download this Documentation

SQLAlchemy includes an event API which publishes a wide variety of hooks into the internals of both SQLAlchemy Core and ORM.

Subscribing to an event occurs through a single API point, the listen() function, or alternatively the listens_for() decorator. These functions accept a target, a string identifier which identifies the event to be intercepted, and a user-defined listening function. Additional positional and keyword arguments to these two functions may be supported by specific types of events, which may specify alternate interfaces for the given event function, or provide instructions regarding secondary event targets based on the given target.

The name of an event and the argument signature of a corresponding listener function is derived from a class bound specification method, which exists bound to a marker class that’s described in the documentation. For example, the documentation for PoolEvents.connect() indicates that the event name is "connect" and that a user-defined listener function should receive two positional arguments:

To listen with the listens_for() decorator looks like:

There are some varieties of argument styles which can be accepted by listener functions. Taking the example of PoolEvents.connect(), this function is documented as receiving dbapi_connection and connection_record arguments. We can opt to receive these arguments by name, by establishing a listener function that accepts **keyword arguments, by passing named=True to either listen() or listens_for():

When using named argument passing, the names listed in the function argument specification will be used as keys in the dictionary.

Named style passes all arguments by name regardless of the function signature, so specific arguments may be listed as well, in any order, as long as the names match up:

Above, the presence of **kw tells listens_for() that arguments should be passed to the function by name, rather than positionally.

The listen() function is very flexible regarding targets. It generally accepts classes, instances of those classes, and related classes or objects from which the appropriate target can be derived. For example, the above mentioned "connect" event accepts Engine classes and objects as well as Pool classes and objects:

Some listeners allow modifiers to be passed to listen(). These modifiers sometimes provide alternate calling signatures for listeners. Such as with ORM events, some event listeners can have a return value which modifies the subsequent handling. By default, no listener ever requires a return value, but by passing retval=True this value can be supported:

SQLAlchemy’s event hooks are implemented with Python functions and objects, so events propagate via Python function calls. Python multiprocessing follows the same way we think about OS multiprocessing, such as a parent process forking a child process, thus we can describe the SQLAlchemy event system’s behavior using the same model.

Event hooks registered in a parent process will be present in new child processes that are forked from that parent after the hooks have been registered, since the child process starts with a copy of all existing Python structures from the parent when spawned. Child processes that already exist before the hooks are registered will not receive those new event hooks, as changes made to Python structures in a parent process do not propagate to child processes.

For the events themselves, these are Python function calls, which do not have any ability to propagate between processes. SQLAlchemy’s event system does not implement any inter-process communication. It is possible to implement event hooks that use Python inter-process messaging within them, however this would need to be implemented by the user.

Both SQLAlchemy Core and SQLAlchemy ORM feature a wide variety of event hooks:

Core Events - these are described in Core Events and include event hooks specific to connection pool lifecycle, SQL statement execution, transaction lifecycle, and schema creation and teardown.

ORM Events - these are described in ORM Events, and include event hooks specific to class and attribute instrumentation, object initialization hooks, attribute on-change hooks, session state, flush, and commit hooks, mapper initialization, object/result population, and per-instance persistence hooks.

contains(target, identifier, fn)

Return True if the given target/ident/fn is set up to listen.

listen(target, identifier, fn, *args, **kw)

Register a listener function for the given target.

listens_for(target, identifier, *args, **kw)

Decorate a function as a listener for the given target + identifier.

remove(target, identifier, fn)

Remove an event listener.

Register a listener function for the given target.

The listen() function is part of the primary interface for the SQLAlchemy event system, documented at Events.

insert¶ (bool) – The default behavior for event handlers is to append the decorated user defined function to an internal list of registered event listeners upon discovery. If a user registers a function with insert=True, SQLAlchemy will insert (prepend) the function to the internal list upon discovery. This feature is not typically used or recommended by the SQLAlchemy maintainers, but is provided to ensure certain user defined functions can run before others, such as when Changing the sql_mode in MySQL.

named¶ (bool) – When using named argument passing, the names listed in the function argument specification will be used as keys in the dictionary. See Named Argument Styles.

once¶ (bool) – Private/Internal API usage. Deprecated. This parameter would provide that an event function would run only once per given target. It does not however imply automatic de-registration of the listener function; associating an arbitrarily high number of listeners without explicitly removing them will cause memory to grow unbounded even if once=True is specified.

propagate¶ (bool) – The propagate kwarg is available when working with ORM instrumentation and mapping events. See MapperEvents and MapperEvents.before_mapper_configured() for examples.

This flag applies only to specific event listeners, each of which includes documentation explaining when it should be used. By default, no listener ever requires a return value. However, some listeners do support special behaviors for return values, and include in their documentation that the retval=True flag is necessary for a return value to be processed.

Event listener suites that make use of listen.retval include ConnectionEvents and AttributeEvents.

The listen() function cannot be called at the same time that the target event is being run. This has implications for thread safety, and also means an event cannot be added from inside the listener function for itself. The list of events to be run are present inside of a mutable collection that can’t be changed during iteration.

Event registration and removal is not intended to be a “high velocity” operation; it is a configurational operation. For systems that need to quickly associate and deassociate with events at high scale, use a mutable structure that is handled from inside of a single listener.

Decorate a function as a listener for the given target + identifier.

The listens_for() decorator is part of the primary interface for the SQLAlchemy event system, documented at Events.

This function generally shares the same kwargs as listen().

A given function can also be invoked for only the first invocation of the event using the once argument:

The once argument does not imply automatic de-registration of the listener function after it has been invoked a first time; a listener entry will remain associated with the target object. Associating an arbitrarily high number of listeners without explicitly removing them will cause memory to grow unbounded even if once=True is specified.

listen() - general description of event listening

Remove an event listener.

The arguments here should match exactly those which were sent to listen(); all the event registration which proceeded as a result of this call will be reverted by calling remove() with the same arguments.

Above, the listener function associated with SomeMappedClass was also propagated to subclasses of SomeMappedClass; the remove() function will revert all of these operations.

The remove() function cannot be called at the same time that the target event is being run. This has implications for thread safety, and also means an event cannot be removed from inside the listener function for itself. The list of events to be run are present inside of a mutable collection that can’t be changed during iteration.

Event registration and removal is not intended to be a “high velocity” operation; it is a configurational operation. For systems that need to quickly associate and deassociate with events at high scale, use a mutable structure that is handled from inside of a single listener.

Return True if the given target/ident/fn is set up to listen.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from sqlalchemy.event import listen
from sqlalchemy.pool import Pool


def my_on_connect(dbapi_con, connection_record):
    print("New DBAPI connection:", dbapi_con)


listen(Pool, "connect", my_on_connect)
```

Example 2 (python):
```python
from sqlalchemy.event import listens_for
from sqlalchemy.pool import Pool


@listens_for(Pool, "connect")
def my_on_connect(dbapi_con, connection_record):
    print("New DBAPI connection:", dbapi_con)
```

Example 3 (python):
```python
from sqlalchemy.event import listens_for
from sqlalchemy.pool import Pool


@listens_for(Pool, "connect", named=True)
def my_on_connect(**kw):
    print("New DBAPI connection:", kw["dbapi_connection"])
```

Example 4 (python):
```python
from sqlalchemy.event import listens_for
from sqlalchemy.pool import Pool


@listens_for(Pool, "connect", named=True)
def my_on_connect(dbapi_connection, **kw):
    print("New DBAPI connection:", dbapi_connection)
    print("Connection record:", kw["connection_record"])
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/core/inspection.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy Core
    - Project Versions
- Runtime Inspection API¶
- Available Inspection Targets¶

Home | Download this Documentation

Home | Download this Documentation

The inspection module provides the inspect() function, which delivers runtime information about a wide variety of SQLAlchemy objects, both within the Core as well as the ORM.

The inspect() function is the entry point to SQLAlchemy’s public API for viewing the configuration and construction of in-memory objects. Depending on the type of object passed to inspect(), the return value will either be a related object which provides a known interface, or in many cases it will return the object itself.

The rationale for inspect() is twofold. One is that it replaces the need to be aware of a large variety of “information getting” functions in SQLAlchemy, such as Inspector.from_engine() (deprecated in 1.4), instance_state(), class_mapper(), and others. The other is that the return value of inspect() is guaranteed to obey a documented API, thus allowing third party tools which build on top of SQLAlchemy configurations to be constructed in a forwards-compatible way.

inspect(subject[, raiseerr])

Produce an inspection object for the given target.

Produce an inspection object for the given target.

The returned value in some cases may be the same object as the one given, such as if a Mapper object is passed. In other cases, it will be an instance of the registered inspection type for the given object, such as if an Engine is passed, an Inspector object is returned.

subject¶ – the subject to be inspected.

raiseerr¶ – When True, if the given subject does not correspond to a known SQLAlchemy inspected type, sqlalchemy.exc.NoInspectionAvailable is raised. If False, None is returned.

Below is a listing of many of the most common inspection targets.

Connectable (i.e. Engine, Connection) - returns an Inspector object.

ClauseElement - all SQL expression components, including Table, Column, serve as their own inspection objects, meaning any of these objects passed to inspect() return themselves.

object - an object given will be checked by the ORM for a mapping - if so, an InstanceState is returned representing the mapped state of the object. The InstanceState also provides access to per attribute state via the AttributeState interface as well as the per-flush “history” of any attribute via the History object.

Inspection of Mapped Instances

type (i.e. a class) - a class given will be checked by the ORM for a mapping - if so, a Mapper for that class is returned.

Inspection of Mapper objects

mapped attribute - passing a mapped attribute to inspect(), such as inspect(MyClass.some_attribute), returns a QueryableAttribute object, which is the descriptor associated with a mapped class. This descriptor refers to a MapperProperty, which is usually an instance of ColumnProperty or RelationshipProperty, via its QueryableAttribute.property attribute.

AliasedClass - returns an AliasedInsp object.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/internals.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- ORM Internals¶

Home | Download this Documentation

Home | Download this Documentation

Key ORM constructs, not otherwise covered in other sections, are listed here.

A token propagated throughout the course of a chain of attribute events.

Provide an inspection interface corresponding to a particular attribute on a particular mapped object.

Keeps track of the options sent to relationship.cascade

Tracks state information at the class level.

Describes an object attribute that corresponds to a table column or other column expression.

Declarative-compatible front-end for the CompositeProperty class.

Defines a “composite” mapped attribute, representing a collection of columns as one attribute.

A base class applied to all ORM objects and attributes that are related to things that can be returned by the inspect() function.

InspectionAttrExtensionType

Symbols indicating the type of extension that a InspectionAttr is part of.

Adds the .info attribute to InspectionAttr.

Tracks state information at the instance level.

InstrumentedAttribute

Base class for descriptor objects that intercept attribute events on behalf of a MapperProperty object. The actual MapperProperty is accessible via the QueryableAttribute.property attribute.

Represent an ORM mapped attribute on a mapped class.

Maps a single Column on a class.

Declarative front-end for the ColumnProperty class.

Represent a particular class attribute mapped by Mapper.

merge_frozen_result(session, statement, frozen_result[, load])

Merge a FrozenResult back into a Session, returning a new Result object with persistent objects.

merge_result(query, iterator[, load])

Merge a result into the given Query object’s Session.

Defines SQL operations for ORM mapped attributes.

Base class for descriptor objects that intercept attribute events on behalf of a MapperProperty object. The actual MapperProperty is accessible via the QueryableAttribute.property attribute.

Describes an object property that holds a single item or list of items that correspond to a related database table.

RelationshipDirection

enumeration which indicates the ‘direction’ of a RelationshipProperty.

Describes an object property that holds a single item or list of items that correspond to a related database table.

A type that may be used to indicate any ORM-level attribute or object that acts in place of one, in the context of SQL expression construction.

Declarative front-end for the SynonymProperty class.

Denote an attribute name as a synonym to a mapped property, in that the attribute will mirror the value and expression behavior of another attribute.

Provide an inspection interface corresponding to a particular attribute on a particular mapped object.

The AttributeState object is accessed via the InstanceState.attrs collection of a particular InstanceState:

Return the current pre-flush change history for this attribute, via the History interface.

Return the current pre-flush change history for this attribute, via the History interface.

This method will not emit loader callables if the value of the attribute is unloaded.

The attribute history system tracks changes on a per flush basis. Each time the Session is flushed, the history of each attribute is reset to empty. The Session by default autoflushes each time a Query is invoked. For options on how to control this, see Flushing.

AttributeState.load_history() - retrieve history using loader callables if the value is not locally present.

get_history() - underlying function

Return the current pre-flush change history for this attribute, via the History interface.

This method will emit loader callables if the value of the attribute is unloaded.

The attribute history system tracks changes on a per flush basis. Each time the Session is flushed, the history of each attribute is reset to empty. The Session by default autoflushes each time a Query is invoked. For options on how to control this, see Flushing.

AttributeState.history

get_history() - underlying function

The current value of this attribute as loaded from the database.

If the value has not been loaded, or is otherwise not present in the object’s dictionary, returns NO_VALUE.

Return the value of this attribute.

This operation is equivalent to accessing the object’s attribute directly or via getattr(), and will fire off any pending loader callables if needed.

inherits from builtins.frozenset, typing.Generic

Keeps track of the options sent to relationship.cascade

inherits from sqlalchemy.util.langhelpers.HasMemoized, builtins.dict, typing.Generic, sqlalchemy.event.registry.EventTarget

Tracks state information at the class level.

expired_attribute_loader

previously known as deferred_scalar_loader

Mark this instance as the manager for its class.

Return a (instance) -> InstanceState callable.

remove all instrumentation established by this ClassManager.

Deprecated since version 1.4: The ClassManager.deferred_scalar_loader attribute is now named expired_attribute_loader

previously known as deferred_scalar_loader

Mark this instance as the manager for its class.

Return a (instance) -> InstanceState callable.

“state getter” callables should raise either KeyError or AttributeError if no InstanceState could be found for the instance.

remove all instrumentation established by this ClassManager.

inherits from sqlalchemy.orm._MapsColumns, sqlalchemy.orm.StrategizedProperty, sqlalchemy.orm._IntrospectsAnnotations, sqlalchemy.log.Identified

Describes an object attribute that corresponds to a table column or other column expression.

Public constructor is the column_property() function.

Operate on an argument.

Reverse operate on an argument.

Perform class-specific initialization at early declarative scanning time.

Perform subclass-specific initialization post-mapper-creation steps.

Hook called by the Mapper to the property to initiate instrumentation of the class attribute managed by this MapperProperty.

Merge the attribute represented by this MapperProperty from source to destination object.

inherits from sqlalchemy.util.langhelpers.MemoizedSlots, sqlalchemy.orm.PropComparator

Produce boolean, comparison, and other operators for ColumnProperty attributes.

See the documentation for PropComparator for a brief overview.

Redefining and Creating New Operators

TypeEngine.comparator_factory

attribute, adjusted for any aliasing in progress.

Added in version 1.3.17.

Mapping a Class against Multiple Tables - usage example

Operate on an argument.

This is the lowest level of operation, raises NotImplementedError by default.

Overriding this on a subclass can allow common behavior to be applied to all operations. For example, overriding ColumnOperators to apply func.lower() to the left and right side:

op¶ – Operator callable.

*other¶ – the ‘other’ side of the operation. Will be a single scalar for most operations.

**kwargs¶ – modifiers. These may be passed by special operators such as ColumnOperators.contains().

Reverse operate on an argument.

Usage is the same as operate().

A list of Column objects that should be declaratively added to the new Table object.

Perform class-specific initialization at early declarative scanning time.

Added in version 2.0.

Perform subclass-specific initialization post-mapper-creation steps.

This is a template method called by the MapperProperty object’s init() method.

Return the primary column or expression for this ColumnProperty.

Composing from Column Properties at Mapping Time

Hook called by the Mapper to the property to initiate instrumentation of the class attribute managed by this MapperProperty.

The MapperProperty here will typically call out to the attributes module to set up an InstrumentedAttribute.

This step is the first of two steps to set up an InstrumentedAttribute, and is called early in the mapper setup process.

The second step is typically the init_class_attribute step, called from StrategizedProperty via the post_instrument_class() hook. This step assigns additional state to the InstrumentedAttribute (specifically the “impl”) which has been determined after the MapperProperty has determined what kind of persistence management it needs to do (e.g. scalar, object, collection, etc).

return a MapperProperty to be assigned to the declarative mapping

Merge the attribute represented by this MapperProperty from source to destination object.

inherits from sqlalchemy.orm.descriptor_props.CompositeProperty, sqlalchemy.orm.base._DeclarativeMapped

Declarative-compatible front-end for the CompositeProperty class.

Public constructor is the composite() function.

Changed in version 2.0: Added Composite as a Declarative compatible subclass of CompositeProperty.

Composite Column Types

inherits from sqlalchemy.orm._MapsColumns, sqlalchemy.orm._IntrospectsAnnotations, sqlalchemy.orm.descriptor_props.DescriptorProperty

Defines a “composite” mapped attribute, representing a collection of columns as one attribute.

CompositeProperty is constructed using the composite() function.

Composite Column Types

create_row_processor()

Produce the “row processing” function for this Bundle.

Perform class-specific initialization at early declarative scanning time.

Initialization which occurs after the Composite has been associated with its parent mapper.

Provided for userland code that uses attributes.get_history().

Hook called by the Mapper to the property to initiate instrumentation of the class attribute managed by this MapperProperty.

inherits from sqlalchemy.orm.PropComparator

Produce boolean, comparison, and other operators for Composite attributes.

See the example in Redefining Comparison Operations for Composites for an overview of usage , as well as the documentation for PropComparator.

Redefining and Creating New Operators

TypeEngine.comparator_factory

inherits from sqlalchemy.orm.Bundle

Produce the “row processing” function for this Bundle.

May be overridden by subclasses to provide custom behaviors when results are fetched. The method is passed the statement object and a set of “row processor” functions at query execution time; these processor functions when given a result row will return the individual attribute value, which can then be adapted into any kind of return data structure.

The example below illustrates replacing the usual Row return structure with a straight Python dictionary:

A result from the above Bundle will return dictionary values:

A list of Column objects that should be declaratively added to the new Table object.

Perform class-specific initialization at early declarative scanning time.

Added in version 2.0.

Initialization which occurs after the Composite has been associated with its parent mapper.

Provided for userland code that uses attributes.get_history().

Hook called by the Mapper to the property to initiate instrumentation of the class attribute managed by this MapperProperty.

The MapperProperty here will typically call out to the attributes module to set up an InstrumentedAttribute.

This step is the first of two steps to set up an InstrumentedAttribute, and is called early in the mapper setup process.

The second step is typically the init_class_attribute step, called from StrategizedProperty via the post_instrument_class() hook. This step assigns additional state to the InstrumentedAttribute (specifically the “impl”) which has been determined after the MapperProperty has determined what kind of persistence management it needs to do (e.g. scalar, object, collection, etc).

return a MapperProperty to be assigned to the declarative mapping

A token propagated throughout the course of a chain of attribute events.

Serves as an indicator of the source of the event and also provides a means of controlling propagation across a chain of attribute operations.

The Event object is sent as the initiator argument when dealing with events such as AttributeEvents.append(), AttributeEvents.set(), and AttributeEvents.remove().

The Event object is currently interpreted by the backref event handlers, and is used to control the propagation of operations across two mutually-dependent attributes.

Changed in version 2.0: Changed the name from AttributeEvent to AttributeEventToken.

The AttributeImpl which is the current event initiator.

The symbol OP_APPEND, OP_REMOVE, OP_REPLACE, or OP_BULK_REPLACE, indicating the source operation.

return True if any InstanceStates present have been marked as ‘modified’.

return True if any InstanceStates present have been marked as ‘modified’.

A base class applied to all ORM objects and attributes that are related to things that can be returned by the inspect() function.

The attributes defined here allow the usage of simple boolean checks to test basic facts about the object returned.

While the boolean checks here are basically the same as using the Python isinstance() function, the flags here can be used without the need to import all of these classes, and also such that the SQLAlchemy class system can change while leaving the flags here intact for forwards-compatibility.

The extension type, if any. Defaults to NotExtension.NOT_EXTENSION

True if this object is an instance of AliasedClass.

True if this object is a Python descriptor.

True if this object is an instance of Bundle.

True if this object is an instance of ClauseElement.

True if this object is an instance of InstanceState.

True if this object is an instance of Mapper.

True if this object is an instance of MapperProperty.

Return True if this object is an instance of Selectable.

The extension type, if any. Defaults to NotExtension.NOT_EXTENSION

AssociationProxyExtensionType

True if this object is an instance of AliasedClass.

True if this object is a Python descriptor.

This can refer to one of many types. Usually a QueryableAttribute which handles attributes events on behalf of a MapperProperty. But can also be an extension type such as AssociationProxy or hybrid_property. The InspectionAttr.extension_type will refer to a constant identifying the specific subtype.

Mapper.all_orm_descriptors

True if this object is an instance of Bundle.

True if this object is an instance of ClauseElement.

True if this object is an instance of InstanceState.

True if this object is an instance of Mapper.

True if this object is an instance of MapperProperty.

Return True if this object is an instance of Selectable.

inherits from sqlalchemy.orm.base.InspectionAttr

Adds the .info attribute to InspectionAttr.

The rationale for InspectionAttr vs. InspectionAttrInfo is that the former is compatible as a mixin for classes that specify __slots__; this is essentially an implementation artifact.

Info dictionary associated with the object, allowing user-defined data to be associated with this InspectionAttr.

Info dictionary associated with the object, allowing user-defined data to be associated with this InspectionAttr.

The dictionary is generated when first accessed. Alternatively, it can be specified as a constructor argument to the column_property(), relationship(), or composite() functions.

QueryableAttribute.info

inherits from sqlalchemy.orm.base.InspectionAttrInfo, typing.Generic

Tracks state information at the instance level.

The InstanceState is a key object used by the SQLAlchemy ORM in order to track the state of an object; it is created the moment an object is instantiated, typically as a result of instrumentation which SQLAlchemy applies to the __init__() method of the class.

InstanceState is also a semi-public object, available for runtime inspection as to the state of a mapped instance, including information such as its current status within a particular Session and details about data on individual attributes. The public API in order to acquire a InstanceState object is to use the inspect() system:

Inspection of Mapped Instances

Return a namespace representing each attribute on the mapped object, including its current value and history.

A namespace where a per-state loader callable can be associated.

When True the object is expired.

The set of keys which are ‘expired’ to be loaded by the manager’s deferred scalar loader, assuming no pending changes.

True if this object is an instance of InstanceState.

Return the Mapper used for this mapped object.

When True the object was modified.

unmodified_intersection()

Return self.unmodified.intersection(keys).

Return the owning AsyncSession for this instance, or None if none available.

This attribute is only non-None when the sqlalchemy.ext.asyncio API is in use for this ORM object. The returned AsyncSession object will be a proxy for the Session object that would be returned from the InstanceState.session attribute for this InstanceState.

Added in version 1.4.18.

Asynchronous I/O (asyncio)

Return a namespace representing each attribute on the mapped object, including its current value and history.

The returned object is an instance of AttributeState. This object allows inspection of the current data within an attribute as well as attribute history since the last flush.

A namespace where a per-state loader callable can be associated.

In SQLAlchemy 1.0, this is only used for lazy loaders / deferred loaders that were set up via query option.

Previously, callables was used also to indicate expired attributes by storing a link to the InstanceState itself in this dictionary. This role is now handled by the expired_attributes set.

Return True if the object is deleted.

An object that is in the deleted state is guaranteed to not be within the Session.identity_map of its parent Session; however if the session’s transaction is rolled back, the object will be restored to the persistent state and the identity map.

The InstanceState.deleted attribute refers to a specific state of the object that occurs between the “persistent” and “detached” states; once the object is detached, the InstanceState.deleted attribute no longer returns True; in order to detect that a state was deleted, regardless of whether or not the object is associated with a Session, use the InstanceState.was_deleted accessor.

Quickie Intro to Object States

Return True if the object is detached.

Quickie Intro to Object States

Return the instance dict used by the object.

Under normal circumstances, this is always synonymous with the __dict__ attribute of the mapped object, unless an alternative instrumentation system has been configured.

In the case that the actual object has been garbage collected, this accessor returns a blank dictionary.

When True the object is expired.

Refreshing / Expiring

The set of keys which are ‘expired’ to be loaded by the manager’s deferred scalar loader, assuming no pending changes.

See also the unmodified collection which is intersected against this set when a refresh operation occurs.

Return True if this object has an identity key.

This should always have the same value as the expression state.persistent or state.detached.

Return the mapped identity of the mapped object. This is the primary key identity as persisted by the ORM which can always be passed directly to Query.get().

Returns None if the object has no primary key identity.

An object which is transient or pending does not have a mapped identity until it is flushed, even if its attributes include primary key values.

Return the identity key for the mapped object.

This is the key used to locate the object within the Session.identity_map mapping. It contains the identity as returned by identity within it.

True if this object is an instance of InstanceState.

Return the Mapper used for this mapped object.

When True the object was modified.

Return the mapped object represented by this InstanceState.

Returns None if the object has been garbage collected

Return True if the object is pending.

Quickie Intro to Object States

Return True if the object is persistent.

An object that is in the persistent state is guaranteed to be within the Session.identity_map of its parent Session.

Quickie Intro to Object States

Return the owning Session for this instance, or None if none available.

Note that the result here can in some cases be different from that of obj in session; an object that’s been deleted will report as not in session, however if the transaction is still in progress, this attribute will still refer to that session. Only when the transaction is completed does the object become fully detached under normal circumstances.

InstanceState.async_session

Return True if the object is transient.

Quickie Intro to Object States

Return the set of keys which do not have a loaded value.

This includes expired attributes and any other attribute that was never populated or modified.

Synonymous with InstanceState.unloaded.

Deprecated since version 2.0: The InstanceState.unloaded_expirable attribute is deprecated. Please use InstanceState.unloaded.

This attribute was added as an implementation-specific detail at some point and should be considered to be private.

Return the set of keys which have no uncommitted changes

Return self.unmodified.intersection(keys).

Return True if this object is or was previously in the “deleted” state and has not been reverted to persistent.

This flag returns True once the object was deleted in flush. When the object is expunged from the session either explicitly or via transaction commit and enters the “detached” state, this flag will continue to report True.

InstanceState.deleted - refers to the “deleted” state

was_deleted() - standalone function

Quickie Intro to Object States

inherits from sqlalchemy.orm.QueryableAttribute

Base class for descriptor objects that intercept attribute events on behalf of a MapperProperty object. The actual MapperProperty is accessible via the QueryableAttribute.property attribute.

InstrumentedAttribute

Mapper.all_orm_descriptors

inherits from enum.Enum

Symbol used internally to indicate an attribute had no callable.

Symbol returned by a loader callable to indicate the retrieved value, or values, were assigned to their attributes on the target object.

Synonymous with NO_VALUE

Symbol which may be placed as the ‘previous’ value of an attribute, indicating no value was loaded for an attribute when it was modified, and flags indicated we were not to load it.

PASSIVE_CLASS_MISMATCH

Symbol indicating that an object is locally present for a given primary key identity but it is not of the requested class. The return value is therefore None and no SQL should be emitted.

Symbol returned by a loader callable or other attribute/history retrieval operation when a value could not be determined, based on loader callable flags.

Symbol used internally to indicate an attribute had no callable.

Symbol returned by a loader callable to indicate the retrieved value, or values, were assigned to their attributes on the target object.

Synonymous with NO_VALUE

Changed in version 1.4: NEVER_SET was merged with NO_VALUE

Symbol which may be placed as the ‘previous’ value of an attribute, indicating no value was loaded for an attribute when it was modified, and flags indicated we were not to load it.

Symbol indicating that an object is locally present for a given primary key identity but it is not of the requested class. The return value is therefore None and no SQL should be emitted.

Symbol returned by a loader callable or other attribute/history retrieval operation when a value could not be determined, based on loader callable flags.

inherits from sqlalchemy.orm.base.SQLORMExpression, sqlalchemy.orm.base.ORMDescriptor, sqlalchemy.orm.base._MappedAnnotationBase, sqlalchemy.sql.roles.DDLConstraintColumnRole

Represent an ORM mapped attribute on a mapped class.

This class represents the complete descriptor interface for any class attribute that will have been instrumented by the ORM Mapper class. Provides appropriate information to type checkers such as pylance and mypy so that ORM-mapped attributes are correctly typed.

The most prominent use of Mapped is in the Declarative Mapping form of Mapper configuration, where used explicitly it drives the configuration of ORM attributes such as mapped_class() and relationship().

Using a Declarative Base Class

Declarative Table with mapped_column()

The Mapped class represents attributes that are handled directly by the Mapper class. It does not include other Python descriptor classes that are provided as extensions, including Hybrid Attributes and the Association Proxy. While these systems still make use of ORM-specific superclasses and structures, they are not instrumented by the Mapper and instead provide their own functionality when they are accessed on a class.

Added in version 1.4.

inherits from sqlalchemy.orm._IntrospectsAnnotations, sqlalchemy.orm._MapsColumns, sqlalchemy.orm.base._DeclarativeMapped

Maps a single Column on a class.

MappedColumn is a specialization of the ColumnProperty class and is oriented towards declarative configuration.

To construct MappedColumn objects, use the mapped_column() constructor function.

Added in version 2.0.

inherits from sqlalchemy.sql.cache_key.HasCacheKey, sqlalchemy.orm._DCAttributeOptions, sqlalchemy.orm.base._MappedAttribute, sqlalchemy.orm.base.InspectionAttrInfo, sqlalchemy.util.langhelpers.MemoizedSlots

Represent a particular class attribute mapped by Mapper.

The most common occurrences of MapperProperty are the mapped Column, which is represented in a mapping as an instance of ColumnProperty, and a reference to another class produced by relationship(), represented in the mapping as an instance of Relationship.

Iterate through instances related to the given instance for a particular ‘cascade’, starting with this MapperProperty.

The PropComparator instance that implements SQL expression construction on behalf of this mapped attribute.

create_row_processor()

Produce row processing functions and append to the given set of populators lists.

Perform subclass-specific initialization post-mapper-creation steps.

optional documentation string

Info dictionary associated with the object, allowing user-defined data to be associated with this InspectionAttr.

Called after all mappers are created to assemble relationships between mappers and perform other post-mapper-creation initialization steps.

Hook called by the Mapper to the property to initiate instrumentation of the class attribute managed by this MapperProperty.

Part of the InspectionAttr interface; states this object is a mapper property.

name of class attribute

Merge the attribute represented by this MapperProperty from source to destination object.

the Mapper managing this property.

post_instrument_class()

Perform instrumentation adjustments that need to occur after init() has completed.

Set the parent mapper that references this MapperProperty.

Called by Query for the purposes of constructing a SQL statement.

Iterate through instances related to the given instance for a particular ‘cascade’, starting with this MapperProperty.

Return an iterator3-tuples (instance, mapper, state).

Note that the ‘cascade’ collection on this MapperProperty is checked first for the given type before cascade_iterator is called.

This method typically only applies to Relationship.

Return the class-bound descriptor corresponding to this MapperProperty.

This is basically a getattr() call:

I.e. if this MapperProperty were named addresses, and the class to which it is mapped is User, this sequence is possible:

The PropComparator instance that implements SQL expression construction on behalf of this mapped attribute.

Produce row processing functions and append to the given set of populators lists.

Perform subclass-specific initialization post-mapper-creation steps.

This is a template method called by the MapperProperty object’s init() method.

optional documentation string

Info dictionary associated with the object, allowing user-defined data to be associated with this InspectionAttr.

The dictionary is generated when first accessed. Alternatively, it can be specified as a constructor argument to the column_property(), relationship(), or composite() functions.

QueryableAttribute.info

Called after all mappers are created to assemble relationships between mappers and perform other post-mapper-creation initialization steps.

Hook called by the Mapper to the property to initiate instrumentation of the class attribute managed by this MapperProperty.

The MapperProperty here will typically call out to the attributes module to set up an InstrumentedAttribute.

This step is the first of two steps to set up an InstrumentedAttribute, and is called early in the mapper setup process.

The second step is typically the init_class_attribute step, called from StrategizedProperty via the post_instrument_class() hook. This step assigns additional state to the InstrumentedAttribute (specifically the “impl”) which has been determined after the MapperProperty has determined what kind of persistence management it needs to do (e.g. scalar, object, collection, etc).

Part of the InspectionAttr interface; states this object is a mapper property.

name of class attribute

Merge the attribute represented by this MapperProperty from source to destination object.

the Mapper managing this property.

Perform instrumentation adjustments that need to occur after init() has completed.

The given Mapper is the Mapper invoking the operation, which may not be the same Mapper as self.parent in an inheritance scenario; however, Mapper will always at least be a sub-mapper of self.parent.

This method is typically used by StrategizedProperty, which delegates it to LoaderStrategy.init_class_attribute() to perform final setup on the class-bound InstrumentedAttribute.

Set the parent mapper that references this MapperProperty.

This method is overridden by some subclasses to perform extra setup when the mapper is first known.

Called by Query for the purposes of constructing a SQL statement.

Each MapperProperty associated with the target mapper processes the statement referenced by the query context, adding columns and/or criterion as appropriate.

inherits from sqlalchemy.orm.properties.ColumnProperty, sqlalchemy.orm.base._DeclarativeMapped

Declarative front-end for the ColumnProperty class.

Public constructor is the column_property() function.

Changed in version 2.0: Added MappedSQLExpression as a Declarative compatible subclass for ColumnProperty.

inherits from enum.Enum

Symbols indicating the type of extension that a InspectionAttr is part of.

inherits from sqlalchemy.orm.base.InspectionAttrExtensionType

Symbol indicating an InspectionAttr that’s not part of sqlalchemy.ext.

Symbol indicating an InspectionAttr that’s not part of sqlalchemy.ext.

Is assigned to the InspectionAttr.extension_type attribute.

Merge a result into the given Query object’s Session.

Deprecated since version 2.0: The merge_result() function is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. The function as well as the method on Query is superseded by the merge_frozen_result() function. (Background on SQLAlchemy 2.0 at: SQLAlchemy 2.0 - Major Migration Guide)

See Query.merge_result() for top-level documentation on this function.

Merge a FrozenResult back into a Session, returning a new Result object with persistent objects.

See the section Re-Executing Statements for an example.

Re-Executing Statements

inherits from sqlalchemy.orm.base.SQLORMOperations, typing.Generic, sqlalchemy.sql.expression.ColumnOperators

Defines SQL operations for ORM mapped attributes.

SQLAlchemy allows for operators to be redefined at both the Core and ORM level. PropComparator is the base class of operator redefinition for ORM-level operations, including those of ColumnProperty, Relationship, and Composite.

User-defined subclasses of PropComparator may be created. The built-in Python comparison and math operator methods, such as ColumnOperators.__eq__(), ColumnOperators.__lt__(), and ColumnOperators.__add__(), can be overridden to provide new operator behavior. The custom PropComparator is passed to the MapperProperty instance via the comparator_factory argument. In each case, the appropriate subclass of PropComparator should be used:

Note that for column-level operator redefinition, it’s usually simpler to define the operators at the Core level, using the TypeEngine.comparator_factory attribute. See Redefining and Creating New Operators for more detail.

Redefining and Creating New Operators

TypeEngine.comparator_factory

Implement the == operator.

Implement the <= operator.

Implement the < operator.

Implement the != operator.

Return a copy of this PropComparator which will use the given AliasedInsp to produce corresponding expressions.

Produce a callable that adapts column expressions to suit an aliased version of this comparator.

Produce an all_() clause against the parent object.

Add additional criteria to the ON clause that’s represented by this relationship attribute.

Return a SQL expression representing true if this element references a member which meets the given criterion.

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

Return a SQL expression representing true if this element references a member which meets the given criterion.

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

Redefine this object in terms of a polymorphic subclass, with_polymorphic() construct, or aliased() construct.

Produce a generic operator function.

Operate on an argument.

Return the MapperProperty associated with this PropComparator.

Implements a database-specific ‘regexp match’ operator.

Implements a database-specific ‘regexp replace’ operator.

Reverse operate on an argument.

Implement the startswith operator.

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

Return a copy of this PropComparator which will use the given AliasedInsp to produce corresponding expressions.

Produce a callable that adapts column expressions to suit an aliased version of this comparator.

inherited from the ColumnOperators.all_() method of ColumnOperators

Produce an all_() clause against the parent object.

See the documentation for all_() for examples.

be sure to not confuse the newer ColumnOperators.all_() method with the legacy version of this method, the Comparator.all() method that’s specific to ARRAY, which uses a different calling style.

Add additional criteria to the ON clause that’s represented by this relationship attribute.

Added in version 1.4.

Combining Relationship with Custom ON Criteria

Adding Criteria to loader options

with_loader_criteria()

Return a SQL expression representing true if this element references a member which meets the given criterion.

The usual implementation of any() is Comparator.any().

criterion¶ – an optional ClauseElement formulated against the member class’ table or attributes.

**kwargs¶ – key/value pairs corresponding to member class attribute names which will be compared via equality to the corresponding values.

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

Return a SQL expression representing true if this element references a member which meets the given criterion.

The usual implementation of has() is Comparator.has().

criterion¶ – an optional ClauseElement formulated against the member class’ table or attributes.

**kwargs¶ – key/value pairs corresponding to member class attribute names which will be compared via equality to the corresponding values.

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

Redefine this object in terms of a polymorphic subclass, with_polymorphic() construct, or aliased() construct.

Returns a new PropComparator from which further criterion can be evaluated.

class_¶ – a class or mapper indicating that criterion will be against this specific subclass.

Using Relationship to join between aliased targets - in the ORM Querying Guide

Joining to specific sub-types or with_polymorphic() entities

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

Return the MapperProperty associated with this PropComparator.

Return values here will commonly be instances of ColumnProperty or Relationship.

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

inherited from the Operators.reverse_operate() method of Operators

Reverse operate on an argument.

Usage is the same as operate().

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

inherits from sqlalchemy.orm.RelationshipProperty, sqlalchemy.orm.base._DeclarativeMapped

Describes an object property that holds a single item or list of items that correspond to a related database table.

Public constructor is the relationship() function.

Relationship Configuration

Changed in version 2.0: Added Relationship as a Declarative compatible subclass for RelationshipProperty.

inherits from enum.Enum

enumeration which indicates the ‘direction’ of a RelationshipProperty.

RelationshipDirection is accessible from the Relationship.direction attribute of RelationshipProperty.

Indicates the many-to-many direction for a relationship().

Indicates the many-to-one direction for a relationship().

Indicates the one-to-many direction for a relationship().

Indicates the many-to-many direction for a relationship().

This symbol is typically used by the internals but may be exposed within certain API features.

Indicates the many-to-one direction for a relationship().

This symbol is typically used by the internals but may be exposed within certain API features.

Indicates the one-to-many direction for a relationship().

This symbol is typically used by the internals but may be exposed within certain API features.

inherits from sqlalchemy.orm._IntrospectsAnnotations, sqlalchemy.orm.StrategizedProperty, sqlalchemy.log.Identified

Describes an object property that holds a single item or list of items that correspond to a related database table.

Public constructor is the relationship() function.

Relationship Configuration

Implement the == operator.

Construction of Comparator is internal to the ORM’s attribute mechanics.

Implement the != operator.

Return a copy of this PropComparator which will use the given AliasedInsp to produce corresponding expressions.

Produce an expression that tests a collection against particular criterion, using EXISTS.

Return a simple expression that tests a collection for containment of a particular item.

The target entity referred to by this Comparator.

Produce an expression that tests a scalar reference against particular criterion, using EXISTS.

Produce an IN clause - this is not implemented for relationship()-based attributes at this time.

The target Mapper referred to by this Comparator.

Redefine this object in terms of a polymorphic subclass.

Iterate through instances related to the given instance for a particular ‘cascade’, starting with this MapperProperty.

Perform class-specific initialization at early declarative scanning time.

Perform subclass-specific initialization post-mapper-creation steps.

Return the target mapped entity, which is an inspect() of the class or aliased class that is referenced by this RelationshipProperty.

Hook called by the Mapper to the property to initiate instrumentation of the class attribute managed by this MapperProperty.

Return the targeted Mapper for this RelationshipProperty.

Merge the attribute represented by this MapperProperty from source to destination object.

inherits from sqlalchemy.util.langhelpers.MemoizedSlots, sqlalchemy.orm.PropComparator

Produce boolean, comparison, and other operators for RelationshipProperty attributes.

See the documentation for PropComparator for a brief overview of ORM level operator definition.

Redefining and Creating New Operators

TypeEngine.comparator_factory

Implement the == operator.

In a many-to-one context, such as:

this will typically produce a clause such as:

Where <some id> is the primary key of the given object.

The == operator provides partial functionality for non- many-to-one comparisons:

Comparisons against collections are not supported. Use Comparator.contains().

Compared to a scalar one-to-many, will produce a clause that compares the target columns in the parent to the given target.

Compared to a scalar many-to-many, an alias of the association table will be rendered as well, forming a natural join that is part of the main body of the query. This will not work for queries that go beyond simple AND conjunctions of comparisons, such as those which use OR. Use explicit joins, outerjoins, or Comparator.has() for more comprehensive non-many-to-one scalar membership tests.

Comparisons against None given in a one-to-many or many-to-many context produce a NOT EXISTS clause.

Construction of Comparator is internal to the ORM’s attribute mechanics.

Implement the != operator.

In a many-to-one context, such as:

This will typically produce a clause such as:

Where <some id> is the primary key of the given object.

The != operator provides partial functionality for non- many-to-one comparisons:

Comparisons against collections are not supported. Use Comparator.contains() in conjunction with not_().

Compared to a scalar one-to-many, will produce a clause that compares the target columns in the parent to the given target.

Compared to a scalar many-to-many, an alias of the association table will be rendered as well, forming a natural join that is part of the main body of the query. This will not work for queries that go beyond simple AND conjunctions of comparisons, such as those which use OR. Use explicit joins, outerjoins, or Comparator.has() in conjunction with not_() for more comprehensive non-many-to-one scalar membership tests.

Comparisons against None given in a one-to-many or many-to-many context produce an EXISTS clause.

Return a copy of this PropComparator which will use the given AliasedInsp to produce corresponding expressions.

See PropComparator.and_() for an example.

Added in version 1.4.

Produce an expression that tests a collection against particular criterion, using EXISTS.

Will produce a query like:

Because Comparator.any() uses a correlated subquery, its performance is not nearly as good when compared against large target tables as that of using a join.

Comparator.any() is particularly useful for testing for empty collections:

Comparator.any() is only valid for collections, i.e. a relationship() that has uselist=True. For scalar references, use Comparator.has().

Return a simple expression that tests a collection for containment of a particular item.

Comparator.contains() is only valid for a collection, i.e. a relationship() that implements one-to-many or many-to-many with uselist=True.

When used in a simple one-to-many context, an expression like:

Produces a clause like:

Where <some id> is the value of the foreign key attribute on other which refers to the primary key of its parent object. From this it follows that Comparator.contains() is very useful when used with simple one-to-many operations.

For many-to-many operations, the behavior of Comparator.contains() has more caveats. The association table will be rendered in the statement, producing an “implicit” join, that is, includes multiple tables in the FROM clause which are equated in the WHERE clause:

Produces a query like:

Where <some id> would be the primary key of other. From the above, it is clear that Comparator.contains() will not work with many-to-many collections when used in queries that move beyond simple AND conjunctions, such as multiple Comparator.contains() expressions joined by OR. In such cases subqueries or explicit “outer joins” will need to be used instead. See Comparator.any() for a less-performant alternative using EXISTS, or refer to Query.outerjoin() as well as Joins for more details on constructing outer joins.

kwargs may be ignored by this operator but are required for API conformance.

The target entity referred to by this Comparator.

This is either a Mapper or AliasedInsp object.

This is the “target” or “remote” side of the relationship().

Produce an expression that tests a scalar reference against particular criterion, using EXISTS.

Will produce a query like:

Because Comparator.has() uses a correlated subquery, its performance is not nearly as good when compared against large target tables as that of using a join.

Comparator.has() is only valid for scalar references, i.e. a relationship() that has uselist=False. For collection references, use Comparator.any().

Produce an IN clause - this is not implemented for relationship()-based attributes at this time.

The target Mapper referred to by this Comparator.

This is the “target” or “remote” side of the relationship().

Redefine this object in terms of a polymorphic subclass.

See PropComparator.of_type() for an example.

Return the current cascade setting for this RelationshipProperty.

Iterate through instances related to the given instance for a particular ‘cascade’, starting with this MapperProperty.

Return an iterator3-tuples (instance, mapper, state).

Note that the ‘cascade’ collection on this MapperProperty is checked first for the given type before cascade_iterator is called.

This method typically only applies to Relationship.

Perform class-specific initialization at early declarative scanning time.

Added in version 2.0.

Perform subclass-specific initialization post-mapper-creation steps.

This is a template method called by the MapperProperty object’s init() method.

Return the target mapped entity, which is an inspect() of the class or aliased class that is referenced by this RelationshipProperty.

Hook called by the Mapper to the property to initiate instrumentation of the class attribute managed by this MapperProperty.

The MapperProperty here will typically call out to the attributes module to set up an InstrumentedAttribute.

This step is the first of two steps to set up an InstrumentedAttribute, and is called early in the mapper setup process.

The second step is typically the init_class_attribute step, called from StrategizedProperty via the post_instrument_class() hook. This step assigns additional state to the InstrumentedAttribute (specifically the “impl”) which has been determined after the MapperProperty has determined what kind of persistence management it needs to do (e.g. scalar, object, collection, etc).

Return the targeted Mapper for this RelationshipProperty.

Merge the attribute represented by this MapperProperty from source to destination object.

inherits from sqlalchemy.orm.base.SQLORMOperations, sqlalchemy.sql.expression.SQLColumnExpression, sqlalchemy.util.langhelpers.TypingOnly

A type that may be used to indicate any ORM-level attribute or object that acts in place of one, in the context of SQL expression construction.

SQLORMExpression extends from the Core SQLColumnExpression to add additional SQL methods that are ORM specific, such as PropComparator.of_type(), and is part of the bases for InstrumentedAttribute. It may be used in PEP 484 typing to indicate arguments or return values that should behave as ORM-level attribute expressions.

Added in version 2.0.0b4.

inherits from sqlalchemy.orm.descriptor_props.SynonymProperty, sqlalchemy.orm.base._DeclarativeMapped

Declarative front-end for the SynonymProperty class.

Public constructor is the synonym() function.

Changed in version 2.0: Added Synonym as a Declarative compatible subclass for SynonymProperty

Synonyms - Overview of synonyms

inherits from sqlalchemy.orm.descriptor_props.DescriptorProperty

Denote an attribute name as a synonym to a mapped property, in that the attribute will mirror the value and expression behavior of another attribute.

Synonym is constructed using the synonym() function.

Synonyms - Overview of synonyms

optional documentation string

Info dictionary associated with the object, allowing user-defined data to be associated with this InspectionAttr.

name of class attribute

the Mapper managing this property.

Set the parent mapper that references this MapperProperty.

inherited from the DescriptorProperty.doc attribute of DescriptorProperty

optional documentation string

inherited from the MapperProperty.info attribute of MapperProperty

Info dictionary associated with the object, allowing user-defined data to be associated with this InspectionAttr.

The dictionary is generated when first accessed. Alternatively, it can be specified as a constructor argument to the column_property(), relationship(), or composite() functions.

QueryableAttribute.info

inherited from the MapperProperty.key attribute of MapperProperty

name of class attribute

inherited from the MapperProperty.parent attribute of MapperProperty

the Mapper managing this property.

Set the parent mapper that references this MapperProperty.

This method is overridden by some subclasses to perform extra setup when the mapper is first known.

Returns True when the argument is true, False otherwise. The builtins True and False are the only two instances of the class bool. The class bool is a subclass of the class int, and cannot be subclassed.

inherits from sqlalchemy.sql.expression.Options

inherits from sqlalchemy.orm.base._DeclarativeMapped, sqlalchemy.orm.base.SQLORMExpression, sqlalchemy.orm.base.InspectionAttr, sqlalchemy.orm.PropComparator, sqlalchemy.sql.roles.JoinTargetRole, sqlalchemy.sql.roles.OnClauseRole, sqlalchemy.sql.expression.Immutable, sqlalchemy.sql.cache_key.SlotsMemoizedHasCacheKey, sqlalchemy.util.langhelpers.MemoizedSlots, sqlalchemy.event.registry.EventTarget

Base class for descriptor objects that intercept attribute events on behalf of a MapperProperty object. The actual MapperProperty is accessible via the QueryableAttribute.property attribute.

InstrumentedAttribute

Mapper.all_orm_descriptors

Return a copy of this PropComparator which will use the given AliasedInsp to produce corresponding expressions.

Add additional criteria to the ON clause that’s represented by this relationship attribute.

The SQL expression object represented by this QueryableAttribute.

True if this object is a Python descriptor.

Redefine this object in terms of a polymorphic subclass, with_polymorphic() construct, or aliased() construct.

Operate on an argument.

Return an inspection instance representing the parent.

Reverse operate on an argument.

Return a copy of this PropComparator which will use the given AliasedInsp to produce corresponding expressions.

Add additional criteria to the ON clause that’s represented by this relationship attribute.

Added in version 1.4.

Combining Relationship with Custom ON Criteria

Adding Criteria to loader options

with_loader_criteria()

The SQL expression object represented by this QueryableAttribute.

This will typically be an instance of a ColumnElement subclass representing a column expression.

Return the ‘info’ dictionary for the underlying SQL element.

The behavior here is as follows:

If the attribute is a column-mapped property, i.e. ColumnProperty, which is mapped directly to a schema-level Column object, this attribute will return the SchemaItem.info dictionary associated with the core-level Column object.

If the attribute is a ColumnProperty but is mapped to any other kind of SQL expression other than a Column, the attribute will refer to the MapperProperty.info dictionary associated directly with the ColumnProperty, assuming the SQL expression itself does not have its own .info attribute (which should be the case, unless a user-defined SQL construct has defined one).

If the attribute refers to any other kind of MapperProperty, including Relationship, the attribute will refer to the MapperProperty.info dictionary associated with that MapperProperty.

To access the MapperProperty.info dictionary of the MapperProperty unconditionally, including for a ColumnProperty that’s associated directly with a Column, the attribute can be referred to using QueryableAttribute.property attribute, as MyClass.someattribute.property.info.

True if this object is a Python descriptor.

This can refer to one of many types. Usually a QueryableAttribute which handles attributes events on behalf of a MapperProperty. But can also be an extension type such as AssociationProxy or hybrid_property. The InspectionAttr.extension_type will refer to a constant identifying the specific subtype.

Mapper.all_orm_descriptors

Redefine this object in terms of a polymorphic subclass, with_polymorphic() construct, or aliased() construct.

Returns a new PropComparator from which further criterion can be evaluated.

class_¶ – a class or mapper indicating that criterion will be against this specific subclass.

Using Relationship to join between aliased targets - in the ORM Querying Guide

Joining to specific sub-types or with_polymorphic() entities

Operate on an argument.

This is the lowest level of operation, raises NotImplementedError by default.

Overriding this on a subclass can allow common behavior to be applied to all operations. For example, overriding ColumnOperators to apply func.lower() to the left and right side:

op¶ – Operator callable.

*other¶ – the ‘other’ side of the operation. Will be a single scalar for most operations.

**kwargs¶ – modifiers. These may be passed by special operators such as ColumnOperators.contains().

Return an inspection instance representing the parent.

This will be either an instance of Mapper or AliasedInsp, depending upon the nature of the parent entity which this attribute is associated with.

Reverse operate on an argument.

Usage is the same as operate().

filter_states_for_dep()

Filter the given list of InstanceStates to those relevant to the given DependencyProcessor.

finalize_flush_changes()

Mark processed objects as clean / deleted after a successful flush().

get_attribute_history()

Facade to attributes.get_state_history(), including caching of results.

Return True if the given state is marked as deleted within this uowtransaction.

remove_state_actions()

Remove pending actions for a state from the uowtransaction.

was_already_deleted()

Return True if the given state is expired and was deleted previously.

Filter the given list of InstanceStates to those relevant to the given DependencyProcessor.

Mark processed objects as clean / deleted after a successful flush().

This method is called within the flush() method after the execute() method has succeeded and the transaction has been committed.

Facade to attributes.get_state_history(), including caching of results.

Return True if the given state is marked as deleted within this uowtransaction.

Remove pending actions for a state from the uowtransaction.

Return True if the given state is expired and was deleted previously.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from sqlalchemy import inspect

insp = inspect(some_mapped_object)
attr_state = insp.attrs.some_attribute
```

Example 2 (python):
```python
class MyComparator(ColumnOperators):
    def operate(self, op, other, **kwargs):
        return op(func.lower(self), func.lower(other), **kwargs)
```

Example 3 (php):
```php
class File(Base):
    # ...

    name = Column(String(64))
    extension = Column(String(8))
    filename = column_property(name + "." + extension)
    path = column_property("C:/" + filename.expression)
```

Example 4 (python):
```python
from sqlalchemy.orm import Bundle


class DictBundle(Bundle):
    def create_row_processor(self, query, procs, labels):
        "Override create_row_processor to return values as dictionaries"

        def proc(row):
            return dict(zip(labels, (proc(row) for proc in procs)))

        return proc
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/events.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- ORM Events¶
- Session Events¶
- Mapper Events¶
- Instance Events¶
- Attribute Events¶
- Query Events¶

Home | Download this Documentation

Home | Download this Documentation

The ORM includes a wide variety of hooks available for subscription.

For an introduction to the most commonly used ORM events, see the section Tracking queries, object and Session Changes with Events. The event system in general is discussed at Events. Non-ORM events such as those regarding connections and low-level statement execution are described in Core Events.

The most basic event hooks are available at the level of the ORM Session object. The types of things that are intercepted here include:

Persistence Operations - the ORM flush process that sends changes to the database can be extended using events that fire off at different parts of the flush, to augment or modify the data being sent to the database or to allow other things to happen when persistence occurs. Read more about persistence events at Persistence Events.

Object lifecycle events - hooks when objects are added, persisted, deleted from sessions. Read more about these at Object Lifecycle Events.

Execution Events - Part of the 2.0 style execution model, all SELECT statements against ORM entities emitted, as well as bulk UPDATE and DELETE statements outside of the flush process, are intercepted from the Session.execute() method using the SessionEvents.do_orm_execute() method. Read more about this event at Execute Events.

Be sure to read the Tracking queries, object and Session Changes with Events chapter for context on these events.

Define events specific to Session lifecycle.

inherits from sqlalchemy.event.Events

Define events specific to Session lifecycle.

The listen() function will accept Session objects as well as the return result of sessionmaker() and scoped_session().

Additionally, it accepts the Session class which will apply listeners to all Session instances globally.

When True, the “target” argument passed to applicable event listener functions that work on individual objects will be the instance’s InstanceState management object, rather than the mapped instance itself.

Added in version 1.3.14.

restore_load_context=False¶ –

Applies to the SessionEvents.loaded_as_persistent() event. Restores the loader context of the object when the event hook is complete, so that ongoing eager load operations continue to target the object appropriately. A warning is emitted if the object is moved to a new loader context from within this event if this flag is not set.

Added in version 1.3.14.

Execute after an instance is attached to a session.

Execute after a transaction is begun on a connection.

Event for after the legacy Query.delete() method has been called.

Event for after the legacy Query.update() method has been called.

Execute after a commit has occurred.

Execute after flush has completed, but before commit has been called.

after_flush_postexec()

Execute after flush has completed, and after the post-exec state occurs.

Execute after a real DBAPI rollback has occurred.

after_soft_rollback()

Execute after any rollback has occurred, including “soft” rollbacks that don’t actually emit at the DBAPI level.

after_transaction_create()

Execute when a new SessionTransaction is created.

after_transaction_end()

Execute when the span of a SessionTransaction ends.

Execute before an instance is attached to a session.

Execute before commit is called.

Execute before flush process has started.

deleted_to_detached()

Intercept the “deleted to detached” transition for a specific object.

deleted_to_persistent()

Intercept the “deleted to persistent” transition for a specific object.

detached_to_persistent()

Intercept the “detached to persistent” transition for a specific object.

reference back to the _Dispatch class.

Intercept statement executions that occur on behalf of an ORM Session object.

loaded_as_persistent()

Intercept the “loaded as persistent” transition for a specific object.

pending_to_persistent()

Intercept the “pending to persistent”” transition for a specific object.

pending_to_transient()

Intercept the “pending to transient” transition for a specific object.

persistent_to_deleted()

Intercept the “persistent to deleted” transition for a specific object.

persistent_to_detached()

Intercept the “persistent to detached” transition for a specific object.

persistent_to_transient()

Intercept the “persistent to transient” transition for a specific object.

transient_to_pending()

Intercept the “transient to pending” transition for a specific object.

Execute after an instance is attached to a session.

Example argument forms:

This is called after an add, delete or merge.

As of 0.8, this event fires off after the item has been fully associated with the session, which is different than previous releases. For event handlers that require the object not yet be part of session state (such as handlers which may autoflush while the target object is not yet complete) consider the new before_attach() event.

SessionEvents.before_attach()

Object Lifecycle Events

Execute after a transaction is begun on a connection.

Example argument forms:

This event is called within the process of the Session modifying its own internal state. To invoke SQL operations within this hook, use the Connection provided to the event; do not run SQL operations using the Session directly.

session¶ – The target Session.

transaction¶ – The SessionTransaction.

connection¶ – The Connection object which will be used for SQL statements.

SessionEvents.before_commit()

SessionEvents.after_commit()

SessionEvents.after_transaction_create()

SessionEvents.after_transaction_end()

Event for after the legacy Query.delete() method has been called.

Example argument forms:

Changed in version 0.9: The SessionEvents.after_bulk_delete() event now accepts the arguments SessionEvents.after_bulk_delete.delete_context. Support for listener functions which accept the previous argument signature(s) listed above as “deprecated” will be removed in a future release.

The SessionEvents.after_bulk_delete() method is a legacy event hook as of SQLAlchemy 2.0. The event does not participate in 2.0 style invocations using delete() documented at ORM UPDATE and DELETE with Custom WHERE Criteria. For 2.0 style use, the SessionEvents.do_orm_execute() hook will intercept these calls.

a “delete context” object which contains details about the update, including these attributes:

session - the Session involved

query -the Query object that this update operation was called upon.

result the CursorResult returned as a result of the bulk DELETE operation.

Changed in version 1.4: the update_context no longer has a QueryContext object associated with it.

QueryEvents.before_compile_delete()

SessionEvents.after_bulk_update()

Event for after the legacy Query.update() method has been called.

Example argument forms:

Changed in version 0.9: The SessionEvents.after_bulk_update() event now accepts the arguments SessionEvents.after_bulk_update.update_context. Support for listener functions which accept the previous argument signature(s) listed above as “deprecated” will be removed in a future release.

The SessionEvents.after_bulk_update() method is a legacy event hook as of SQLAlchemy 2.0. The event does not participate in 2.0 style invocations using update() documented at ORM UPDATE and DELETE with Custom WHERE Criteria. For 2.0 style use, the SessionEvents.do_orm_execute() hook will intercept these calls.

an “update context” object which contains details about the update, including these attributes:

session - the Session involved

query -the Query object that this update operation was called upon.

values The “values” dictionary that was passed to Query.update().

result the CursorResult returned as a result of the bulk UPDATE operation.

Changed in version 1.4: the update_context no longer has a QueryContext object associated with it.

QueryEvents.before_compile_update()

SessionEvents.after_bulk_delete()

Execute after a commit has occurred.

Example argument forms:

The SessionEvents.after_commit() hook is not per-flush, that is, the Session can emit SQL to the database many times within the scope of a transaction. For interception of these events, use the SessionEvents.before_flush(), SessionEvents.after_flush(), or SessionEvents.after_flush_postexec() events.

The Session is not in an active transaction when the SessionEvents.after_commit() event is invoked, and therefore can not emit SQL. To emit SQL corresponding to every transaction, use the SessionEvents.before_commit() event.

session¶ – The target Session.

SessionEvents.before_commit()

SessionEvents.after_begin()

SessionEvents.after_transaction_create()

SessionEvents.after_transaction_end()

Execute after flush has completed, but before commit has been called.

Example argument forms:

Note that the session’s state is still in pre-flush, i.e. ‘new’, ‘dirty’, and ‘deleted’ lists still show pre-flush state as well as the history settings on instance attributes.

This event runs after the Session has emitted SQL to modify the database, but before it has altered its internal state to reflect those changes, including that newly inserted objects are placed into the identity map. ORM operations emitted within this event such as loads of related items may produce new identity map entries that will immediately be replaced, sometimes causing confusing results. SQLAlchemy will emit a warning for this condition as of version 1.3.9.

session¶ – The target Session.

flush_context¶ – Internal UOWTransaction object which handles the details of the flush.

SessionEvents.before_flush()

SessionEvents.after_flush_postexec()

Execute after flush has completed, and after the post-exec state occurs.

Example argument forms:

This will be when the ‘new’, ‘dirty’, and ‘deleted’ lists are in their final state. An actual commit() may or may not have occurred, depending on whether or not the flush started its own transaction or participated in a larger transaction.

session¶ – The target Session.

flush_context¶ – Internal UOWTransaction object which handles the details of the flush.

SessionEvents.before_flush()

SessionEvents.after_flush()

Execute after a real DBAPI rollback has occurred.

Example argument forms:

Note that this event only fires when the actual rollback against the database occurs - it does not fire each time the Session.rollback() method is called, if the underlying DBAPI transaction has already been rolled back. In many cases, the Session will not be in an “active” state during this event, as the current transaction is not valid. To acquire a Session which is active after the outermost rollback has proceeded, use the SessionEvents.after_soft_rollback() event, checking the Session.is_active flag.

session¶ – The target Session.

Execute after any rollback has occurred, including “soft” rollbacks that don’t actually emit at the DBAPI level.

Example argument forms:

This corresponds to both nested and outer rollbacks, i.e. the innermost rollback that calls the DBAPI’s rollback() method, as well as the enclosing rollback calls that only pop themselves from the transaction stack.

The given Session can be used to invoke SQL and Session.query() operations after an outermost rollback by first checking the Session.is_active flag:

session¶ – The target Session.

previous_transaction¶ – The SessionTransaction transactional marker object which was just closed. The current SessionTransaction for the given Session is available via the Session.transaction attribute.

Execute when a new SessionTransaction is created.

Example argument forms:

This event differs from SessionEvents.after_begin() in that it occurs for each SessionTransaction overall, as opposed to when transactions are begun on individual database connections. It is also invoked for nested transactions and subtransactions, and is always matched by a corresponding SessionEvents.after_transaction_end() event (assuming normal operation of the Session).

session¶ – the target Session.

the target SessionTransaction.

To detect if this is the outermost SessionTransaction, as opposed to a “subtransaction” or a SAVEPOINT, test that the SessionTransaction.parent attribute is None:

To detect if the SessionTransaction is a SAVEPOINT, use the SessionTransaction.nested attribute:

SessionEvents.after_transaction_end()

Execute when the span of a SessionTransaction ends.

Example argument forms:

This event differs from SessionEvents.after_commit() in that it corresponds to all SessionTransaction objects in use, including those for nested transactions and subtransactions, and is always matched by a corresponding SessionEvents.after_transaction_create() event.

session¶ – the target Session.

the target SessionTransaction.

To detect if this is the outermost SessionTransaction, as opposed to a “subtransaction” or a SAVEPOINT, test that the SessionTransaction.parent attribute is None:

To detect if the SessionTransaction is a SAVEPOINT, use the SessionTransaction.nested attribute:

SessionEvents.after_transaction_create()

Execute before an instance is attached to a session.

Example argument forms:

This is called before an add, delete or merge causes the object to be part of the session.

SessionEvents.after_attach()

Object Lifecycle Events

Execute before commit is called.

Example argument forms:

The SessionEvents.before_commit() hook is not per-flush, that is, the Session can emit SQL to the database many times within the scope of a transaction. For interception of these events, use the SessionEvents.before_flush(), SessionEvents.after_flush(), or SessionEvents.after_flush_postexec() events.

session¶ – The target Session.

SessionEvents.after_commit()

SessionEvents.after_begin()

SessionEvents.after_transaction_create()

SessionEvents.after_transaction_end()

Execute before flush process has started.

Example argument forms:

session¶ – The target Session.

flush_context¶ – Internal UOWTransaction object which handles the details of the flush.

instances¶ – Usually None, this is the collection of objects which can be passed to the Session.flush() method (note this usage is deprecated).

SessionEvents.after_flush()

SessionEvents.after_flush_postexec()

Intercept the “deleted to detached” transition for a specific object.

Example argument forms:

This event is invoked when a deleted object is evicted from the session. The typical case when this occurs is when the transaction for a Session in which the object was deleted is committed; the object moves from the deleted state to the detached state.

It is also invoked for objects that were deleted in a flush when the Session.expunge_all() or Session.close() events are called, as well as if the object is individually expunged from its deleted state via Session.expunge().

Object Lifecycle Events

Intercept the “deleted to persistent” transition for a specific object.

Example argument forms:

This transition occurs only when an object that’s been deleted successfully in a flush is restored due to a call to Session.rollback(). The event is not called under any other circumstances.

Object Lifecycle Events

Intercept the “detached to persistent” transition for a specific object.

Example argument forms:

This event is a specialization of the SessionEvents.after_attach() event which is only invoked for this specific transition. It is invoked typically during the Session.add() call, as well as during the Session.delete() call if the object was not previously associated with the Session (note that an object marked as “deleted” remains in the “persistent” state until the flush proceeds).

If the object becomes persistent as part of a call to Session.delete(), the object is not yet marked as deleted when this event is called. To detect deleted objects, check the deleted flag sent to the SessionEvents.persistent_to_detached() to event after the flush proceeds, or check the Session.deleted collection within the SessionEvents.before_flush() event if deleted objects need to be intercepted before the flush.

session¶ – target Session

instance¶ – the ORM-mapped instance being operated upon.

Object Lifecycle Events

reference back to the _Dispatch class.

Bidirectional against _Dispatch._events

Intercept statement executions that occur on behalf of an ORM Session object.

Example argument forms:

This event is invoked for all top-level SQL statements invoked from the Session.execute() method, as well as related methods such as Session.scalars() and Session.scalar(). As of SQLAlchemy 1.4, all ORM queries that run through the Session.execute() method as well as related methods Session.scalars(), Session.scalar() etc. will participate in this event. This event hook does not apply to the queries that are emitted internally within the ORM flush process, i.e. the process described at Flushing.

The SessionEvents.do_orm_execute() event hook is triggered for ORM statement executions only, meaning those invoked via the Session.execute() and similar methods on the Session object. It does not trigger for statements that are invoked by SQLAlchemy Core only, i.e. statements invoked directly using Connection.execute() or otherwise originating from an Engine object without any Session involved. To intercept all SQL executions regardless of whether the Core or ORM APIs are in use, see the event hooks at ConnectionEvents, such as ConnectionEvents.before_execute() and ConnectionEvents.before_cursor_execute().

Also, this event hook does not apply to queries that are emitted internally within the ORM flush process, i.e. the process described at Flushing; to intercept steps within the flush process, see the event hooks described at Persistence Events as well as Mapper-level Flush Events.

This event is a do_ event, meaning it has the capability to replace the operation that the Session.execute() method normally performs. The intended use for this includes sharding and result-caching schemes which may seek to invoke the same statement across multiple database connections, returning a result that is merged from each of them, or which don’t invoke the statement at all, instead returning data from a cache.

The hook intends to replace the use of the Query._execute_and_instances method that could be subclassed prior to SQLAlchemy 1.4.

orm_execute_state¶ – an instance of ORMExecuteState which contains all information about the current execution, as well as helper functions used to derive other commonly required information. See that object for details.

Execute Events - top level documentation on how to use SessionEvents.do_orm_execute()

ORMExecuteState - the object passed to the SessionEvents.do_orm_execute() event which contains all information about the statement to be invoked. It also provides an interface to extend the current statement, options, and parameters as well as an option that allows programmatic invocation of the statement at any point.

ORM Query Events - includes examples of using SessionEvents.do_orm_execute()

Dogpile Caching - an example of how to integrate Dogpile caching with the ORM Session making use of the SessionEvents.do_orm_execute() event hook.

Horizontal Sharding - the Horizontal Sharding example / extension relies upon the SessionEvents.do_orm_execute() event hook to invoke a SQL statement on multiple backends and return a merged result.

Added in version 1.4.

Intercept the “loaded as persistent” transition for a specific object.

Example argument forms:

This event is invoked within the ORM loading process, and is invoked very similarly to the InstanceEvents.load() event. However, the event here is linkable to a Session class or instance, rather than to a mapper or class hierarchy, and integrates with the other session lifecycle events smoothly. The object is guaranteed to be present in the session’s identity map when this event is called.

This event is invoked within the loader process before eager loaders may have been completed, and the object’s state may not be complete. Additionally, invoking row-level refresh operations on the object will place the object into a new loader context, interfering with the existing load context. See the note on InstanceEvents.load() for background on making use of the SessionEvents.restore_load_context parameter, which works in the same manner as that of InstanceEvents.restore_load_context, in order to resolve this scenario.

session¶ – target Session

instance¶ – the ORM-mapped instance being operated upon.

Object Lifecycle Events

Intercept the “pending to persistent”” transition for a specific object.

Example argument forms:

This event is invoked within the flush process, and is similar to scanning the Session.new collection within the SessionEvents.after_flush() event. However, in this case the object has already been moved to the persistent state when the event is called.

session¶ – target Session

instance¶ – the ORM-mapped instance being operated upon.

Object Lifecycle Events

Intercept the “pending to transient” transition for a specific object.

Example argument forms:

This less common transition occurs when an pending object that has not been flushed is evicted from the session; this can occur when the Session.rollback() method rolls back the transaction, or when the Session.expunge() method is used.

session¶ – target Session

instance¶ – the ORM-mapped instance being operated upon.

Object Lifecycle Events

Intercept the “persistent to deleted” transition for a specific object.

Example argument forms:

This event is invoked when a persistent object’s identity is deleted from the database within a flush, however the object still remains associated with the Session until the transaction completes.

If the transaction is rolled back, the object moves again to the persistent state, and the SessionEvents.deleted_to_persistent() event is called. If the transaction is committed, the object becomes detached, which will emit the SessionEvents.deleted_to_detached() event.

Note that while the Session.delete() method is the primary public interface to mark an object as deleted, many objects get deleted due to cascade rules, which are not always determined until flush time. Therefore, there’s no way to catch every object that will be deleted until the flush has proceeded. the SessionEvents.persistent_to_deleted() event is therefore invoked at the end of a flush.

Object Lifecycle Events

Intercept the “persistent to detached” transition for a specific object.

Example argument forms:

This event is invoked when a persistent object is evicted from the session. There are many conditions that cause this to happen, including:

using a method such as Session.expunge() or Session.close()

Calling the Session.rollback() method, when the object was part of an INSERT statement for that session’s transaction

session¶ – target Session

instance¶ – the ORM-mapped instance being operated upon.

deleted¶ – boolean. If True, indicates this object moved to the detached state because it was marked as deleted and flushed.

Object Lifecycle Events

Intercept the “persistent to transient” transition for a specific object.

Example argument forms:

This less common transition occurs when an pending object that has has been flushed is evicted from the session; this can occur when the Session.rollback() method rolls back the transaction.

session¶ – target Session

instance¶ – the ORM-mapped instance being operated upon.

Object Lifecycle Events

Intercept the “transient to pending” transition for a specific object.

Example argument forms:

This event is a specialization of the SessionEvents.after_attach() event which is only invoked for this specific transition. It is invoked typically during the Session.add() call.

session¶ – target Session

instance¶ – the ORM-mapped instance being operated upon.

Object Lifecycle Events

Mapper event hooks encompass things that happen as related to individual or multiple Mapper objects, which are the central configurational object that maps a user-defined class to a Table object. Types of things which occur at the Mapper level include:

Per-object persistence operations - the most popular mapper hooks are the unit-of-work hooks such as MapperEvents.before_insert(), MapperEvents.after_update(), etc. These events are contrasted to the more coarse grained session-level events such as SessionEvents.before_flush() in that they occur within the flush process on a per-object basis; while finer grained activity on an object is more straightforward, availability of Session features is limited.

Mapper configuration events - the other major class of mapper hooks are those which occur as a class is mapped, as a mapper is finalized, and when sets of mappers are configured to refer to each other. These events include MapperEvents.instrument_class(), MapperEvents.before_mapper_configured() and MapperEvents.mapper_configured() at the individual Mapper level, and MapperEvents.before_configured() and MapperEvents.after_configured() at the level of collections of Mapper objects.

Define events specific to mappings.

inherits from sqlalchemy.event.Events

Define events specific to mappings.

Available targets include:

unmapped superclasses of mapped or to-be-mapped classes (using the propagate=True flag)

the Mapper class itself indicates listening for all mappers.

Mapper events provide hooks into critical sections of the mapper, including those related to object instrumentation, object loading, and object persistence. In particular, the persistence methods MapperEvents.before_insert(), and MapperEvents.before_update() are popular places to augment the state being persisted - however, these methods operate with several significant restrictions. The user is encouraged to evaluate the SessionEvents.before_flush() and SessionEvents.after_flush() methods as more flexible and user-friendly hooks in which to apply additional database state during a flush.

When using MapperEvents, several modifiers are available to the listen() function.

propagate=False¶ – When True, the event listener should be applied to all inheriting mappers and/or the mappers of inheriting classes, as well as any mapper which is the target of this listener.

raw=False¶ – When True, the “target” argument passed to applicable event listener functions will be the instance’s InstanceState management object, rather than the mapped instance itself.

when True, the user-defined event function must have a return value, the purpose of which is either to control subsequent event propagation, or to otherwise alter the operation in progress by the mapper. Possible return values are:

sqlalchemy.orm.interfaces.EXT_CONTINUE - continue event processing normally.

sqlalchemy.orm.interfaces.EXT_STOP - cancel all subsequent event handlers in the chain.

other values - the return value specified by specific listeners.

Called after a series of mappers have been configured.

Receive an object instance after a DELETE statement has been emitted corresponding to that instance.

Receive an object instance after an INSERT statement is emitted corresponding to that instance.

after_mapper_constructed()

Receive a class and mapper when the Mapper has been fully constructed.

Receive an object instance after an UPDATE statement is emitted corresponding to that instance.

Called before a series of mappers have been configured.

Receive an object instance before a DELETE statement is emitted corresponding to that instance.

Receive an object instance before an INSERT statement is emitted corresponding to that instance.

before_mapper_configured()

Called right before a specific mapper is to be configured.

Receive an object instance before an UPDATE statement is emitted corresponding to that instance.

reference back to the _Dispatch class.

Receive a class when the mapper is first constructed, before instrumentation is applied to the mapped class.

Called when a specific mapper has completed its own configuration within the scope of the configure_mappers() call.

Called after a series of mappers have been configured.

The MapperEvents.after_configured() event is invoked each time the configure_mappers() function is invoked, after the function has completed its work. configure_mappers() is typically invoked automatically as mappings are first used, as well as each time new mappers have been made available and new mapper use is detected.

Similar events to this one include MapperEvents.before_configured(), which is invoked before a series of mappers are configured, as well as MapperEvents.before_mapper_configured() and MapperEvents.mapper_configured(), which are both invoked on a per-mapper basis.

This event can only be applied to the Mapper class, and not to individual mappings or mapped classes:

Typically, this event is called once per application, but in practice may be called more than once, any time new mappers are to be affected by a configure_mappers() call. If new mappings are constructed after existing ones have already been used, this event will likely be called again.

MapperEvents.before_mapper_configured()

MapperEvents.mapper_configured()

MapperEvents.before_configured()

Receive an object instance after a DELETE statement has been emitted corresponding to that instance.

Example argument forms:

this event only applies to the session flush operation and does not apply to the ORM DML operations described at ORM-Enabled INSERT, UPDATE, and DELETE statements. To intercept ORM DML events, use SessionEvents.do_orm_execute().

This event is used to emit additional SQL statements on the given connection as well as to perform application specific bookkeeping related to a deletion event.

The event is often called for a batch of objects of the same class after their DELETE statements have been emitted at once in a previous step.

Mapper-level flush events only allow very limited operations, on attributes local to the row being operated upon only, as well as allowing any SQL to be emitted on the given Connection. Please read fully the notes at Mapper-level Flush Events for guidelines on using these methods; generally, the SessionEvents.before_flush() method should be preferred for general on-flush changes.

mapper¶ – the Mapper which is the target of this event.

connection¶ – the Connection being used to emit DELETE statements for this instance. This provides a handle into the current transaction on the target database specific to this instance.

target¶ – the mapped instance being deleted. If the event is configured with raw=True, this will instead be the InstanceState state-management object associated with the instance.

No return value is supported by this event.

Receive an object instance after an INSERT statement is emitted corresponding to that instance.

Example argument forms:

this event only applies to the session flush operation and does not apply to the ORM DML operations described at ORM-Enabled INSERT, UPDATE, and DELETE statements. To intercept ORM DML events, use SessionEvents.do_orm_execute().

This event is used to modify in-Python-only state on the instance after an INSERT occurs, as well as to emit additional SQL statements on the given connection.

The event is often called for a batch of objects of the same class after their INSERT statements have been emitted at once in a previous step. In the extremely rare case that this is not desirable, the Mapper object can be configured with batch=False, which will cause batches of instances to be broken up into individual (and more poorly performing) event->persist->event steps.

Mapper-level flush events only allow very limited operations, on attributes local to the row being operated upon only, as well as allowing any SQL to be emitted on the given Connection. Please read fully the notes at Mapper-level Flush Events for guidelines on using these methods; generally, the SessionEvents.before_flush() method should be preferred for general on-flush changes.

mapper¶ – the Mapper which is the target of this event.

connection¶ – the Connection being used to emit INSERT statements for this instance. This provides a handle into the current transaction on the target database specific to this instance.

target¶ – the mapped instance being persisted. If the event is configured with raw=True, this will instead be the InstanceState state-management object associated with the instance.

No return value is supported by this event.

Receive a class and mapper when the Mapper has been fully constructed.

Example argument forms:

This event is called after the initial constructor for Mapper completes. This occurs after the MapperEvents.instrument_class() event and after the Mapper has done an initial pass of its arguments to generate its collection of MapperProperty objects, which are accessible via the Mapper.get_property() method and the Mapper.iterate_properties attribute.

This event differs from the MapperEvents.before_mapper_configured() event in that it is invoked within the constructor for Mapper, rather than within the registry.configure() process. Currently, this event is the only one which is appropriate for handlers that wish to create additional mapped classes in response to the construction of this Mapper, which will be part of the same configure step when registry.configure() next runs.

Added in version 2.0.2.

Versioning Objects - an example which illustrates the use of the MapperEvents.before_mapper_configured() event to create new mappers to record change-audit histories on objects.

Receive an object instance after an UPDATE statement is emitted corresponding to that instance.

Example argument forms:

this event only applies to the session flush operation and does not apply to the ORM DML operations described at ORM-Enabled INSERT, UPDATE, and DELETE statements. To intercept ORM DML events, use SessionEvents.do_orm_execute().

This event is used to modify in-Python-only state on the instance after an UPDATE occurs, as well as to emit additional SQL statements on the given connection.

This method is called for all instances that are marked as “dirty”, even those which have no net changes to their column-based attributes, and for which no UPDATE statement has proceeded. An object is marked as dirty when any of its column-based attributes have a “set attribute” operation called or when any of its collections are modified. If, at update time, no column-based attributes have any net changes, no UPDATE statement will be issued. This means that an instance being sent to MapperEvents.after_update() is not a guarantee that an UPDATE statement has been issued.

To detect if the column-based attributes on the object have net changes, and therefore resulted in an UPDATE statement, use object_session(instance).is_modified(instance, include_collections=False).

The event is often called for a batch of objects of the same class after their UPDATE statements have been emitted at once in a previous step. In the extremely rare case that this is not desirable, the Mapper can be configured with batch=False, which will cause batches of instances to be broken up into individual (and more poorly performing) event->persist->event steps.

Mapper-level flush events only allow very limited operations, on attributes local to the row being operated upon only, as well as allowing any SQL to be emitted on the given Connection. Please read fully the notes at Mapper-level Flush Events for guidelines on using these methods; generally, the SessionEvents.before_flush() method should be preferred for general on-flush changes.

mapper¶ – the Mapper which is the target of this event.

connection¶ – the Connection being used to emit UPDATE statements for this instance. This provides a handle into the current transaction on the target database specific to this instance.

target¶ – the mapped instance being persisted. If the event is configured with raw=True, this will instead be the InstanceState state-management object associated with the instance.

No return value is supported by this event.

Called before a series of mappers have been configured.

The MapperEvents.before_configured() event is invoked each time the configure_mappers() function is invoked, before the function has done any of its work. configure_mappers() is typically invoked automatically as mappings are first used, as well as each time new mappers have been made available and new mapper use is detected.

Similar events to this one include MapperEvents.after_configured(), which is invoked after a series of mappers has been configured, as well as MapperEvents.before_mapper_configured() and MapperEvents.mapper_configured(), which are both invoked on a per-mapper basis.

This event can only be applied to the Mapper class, and not to individual mappings or mapped classes:

Typically, this event is called once per application, but in practice may be called more than once, any time new mappers are to be affected by a configure_mappers() call. If new mappings are constructed after existing ones have already been used, this event will likely be called again.

MapperEvents.before_mapper_configured()

MapperEvents.mapper_configured()

MapperEvents.after_configured()

Receive an object instance before a DELETE statement is emitted corresponding to that instance.

Example argument forms:

this event only applies to the session flush operation and does not apply to the ORM DML operations described at ORM-Enabled INSERT, UPDATE, and DELETE statements. To intercept ORM DML events, use SessionEvents.do_orm_execute().

This event is used to emit additional SQL statements on the given connection as well as to perform application specific bookkeeping related to a deletion event.

The event is often called for a batch of objects of the same class before their DELETE statements are emitted at once in a later step.

Mapper-level flush events only allow very limited operations, on attributes local to the row being operated upon only, as well as allowing any SQL to be emitted on the given Connection. Please read fully the notes at Mapper-level Flush Events for guidelines on using these methods; generally, the SessionEvents.before_flush() method should be preferred for general on-flush changes.

mapper¶ – the Mapper which is the target of this event.

connection¶ – the Connection being used to emit DELETE statements for this instance. This provides a handle into the current transaction on the target database specific to this instance.

target¶ – the mapped instance being deleted. If the event is configured with raw=True, this will instead be the InstanceState state-management object associated with the instance.

No return value is supported by this event.

Receive an object instance before an INSERT statement is emitted corresponding to that instance.

Example argument forms:

this event only applies to the session flush operation and does not apply to the ORM DML operations described at ORM-Enabled INSERT, UPDATE, and DELETE statements. To intercept ORM DML events, use SessionEvents.do_orm_execute().

This event is used to modify local, non-object related attributes on the instance before an INSERT occurs, as well as to emit additional SQL statements on the given connection.

The event is often called for a batch of objects of the same class before their INSERT statements are emitted at once in a later step. In the extremely rare case that this is not desirable, the Mapper object can be configured with batch=False, which will cause batches of instances to be broken up into individual (and more poorly performing) event->persist->event steps.

Mapper-level flush events only allow very limited operations, on attributes local to the row being operated upon only, as well as allowing any SQL to be emitted on the given Connection. Please read fully the notes at Mapper-level Flush Events for guidelines on using these methods; generally, the SessionEvents.before_flush() method should be preferred for general on-flush changes.

mapper¶ – the Mapper which is the target of this event.

connection¶ – the Connection being used to emit INSERT statements for this instance. This provides a handle into the current transaction on the target database specific to this instance.

target¶ – the mapped instance being persisted. If the event is configured with raw=True, this will instead be the InstanceState state-management object associated with the instance.

No return value is supported by this event.

Called right before a specific mapper is to be configured.

The MapperEvents.before_mapper_configured() event is invoked for each mapper that is encountered when the configure_mappers() function proceeds through the current list of not-yet-configured mappers. It is similar to the MapperEvents.mapper_configured() event, except that it’s invoked right before the configuration occurs, rather than afterwards.

The MapperEvents.before_mapper_configured() event includes the special capability where it can force the configure step for a specific mapper to be skipped; to use this feature, establish the event using the retval=True parameter and return the interfaces.EXT_SKIP symbol to indicate the mapper should be left unconfigured:

MapperEvents.before_configured()

MapperEvents.after_configured()

MapperEvents.mapper_configured()

Receive an object instance before an UPDATE statement is emitted corresponding to that instance.

Example argument forms:

this event only applies to the session flush operation and does not apply to the ORM DML operations described at ORM-Enabled INSERT, UPDATE, and DELETE statements. To intercept ORM DML events, use SessionEvents.do_orm_execute().

This event is used to modify local, non-object related attributes on the instance before an UPDATE occurs, as well as to emit additional SQL statements on the given connection.

This method is called for all instances that are marked as “dirty”, even those which have no net changes to their column-based attributes. An object is marked as dirty when any of its column-based attributes have a “set attribute” operation called or when any of its collections are modified. If, at update time, no column-based attributes have any net changes, no UPDATE statement will be issued. This means that an instance being sent to MapperEvents.before_update() is not a guarantee that an UPDATE statement will be issued, although you can affect the outcome here by modifying attributes so that a net change in value does exist.

To detect if the column-based attributes on the object have net changes, and will therefore generate an UPDATE statement, use object_session(instance).is_modified(instance, include_collections=False).

The event is often called for a batch of objects of the same class before their UPDATE statements are emitted at once in a later step. In the extremely rare case that this is not desirable, the Mapper can be configured with batch=False, which will cause batches of instances to be broken up into individual (and more poorly performing) event->persist->event steps.

Mapper-level flush events only allow very limited operations, on attributes local to the row being operated upon only, as well as allowing any SQL to be emitted on the given Connection. Please read fully the notes at Mapper-level Flush Events for guidelines on using these methods; generally, the SessionEvents.before_flush() method should be preferred for general on-flush changes.

mapper¶ – the Mapper which is the target of this event.

connection¶ – the Connection being used to emit UPDATE statements for this instance. This provides a handle into the current transaction on the target database specific to this instance.

target¶ – the mapped instance being persisted. If the event is configured with raw=True, this will instead be the InstanceState state-management object associated with the instance.

No return value is supported by this event.

reference back to the _Dispatch class.

Bidirectional against _Dispatch._events

Receive a class when the mapper is first constructed, before instrumentation is applied to the mapped class.

Example argument forms:

This event is the earliest phase of mapper construction. Most attributes of the mapper are not yet initialized. To receive an event within initial mapper construction where basic state is available such as the Mapper.attrs collection, the MapperEvents.after_mapper_constructed() event may be a better choice.

This listener can either be applied to the Mapper class overall, or to any un-mapped class which serves as a base for classes that will be mapped (using the propagate=True flag):

mapper¶ – the Mapper which is the target of this event.

class_¶ – the mapped class.

MapperEvents.after_mapper_constructed()

Called when a specific mapper has completed its own configuration within the scope of the configure_mappers() call.

Example argument forms:

The MapperEvents.mapper_configured() event is invoked for each mapper that is encountered when the configure_mappers() function proceeds through the current list of not-yet-configured mappers. configure_mappers() is typically invoked automatically as mappings are first used, as well as each time new mappers have been made available and new mapper use is detected.

When the event is called, the mapper should be in its final state, but not including backrefs that may be invoked from other mappers; they might still be pending within the configuration operation. Bidirectional relationships that are instead configured via the relationship.back_populates argument will be fully available, since this style of relationship does not rely upon other possibly-not-configured mappers to know that they exist.

For an event that is guaranteed to have all mappers ready to go including backrefs that are defined only on other mappings, use the MapperEvents.after_configured() event; this event invokes only after all known mappings have been fully configured.

The MapperEvents.mapper_configured() event, unlike the MapperEvents.before_configured() or MapperEvents.after_configured() events, is called for each mapper/class individually, and the mapper is passed to the event itself. It also is called exactly once for a particular mapper. The event is therefore useful for configurational steps that benefit from being invoked just once on a specific mapper basis, which don’t require that “backref” configurations are necessarily ready yet.

mapper¶ – the Mapper which is the target of this event.

class_¶ – the mapped class.

MapperEvents.before_configured()

MapperEvents.after_configured()

MapperEvents.before_mapper_configured()

Instance events are focused on the construction of ORM mapped instances, including when they are instantiated as transient objects, when they are loaded from the database and become persistent objects, as well as when database refresh or expiration operations occur on the object.

Define events specific to object lifecycle.

inherits from sqlalchemy.event.Events

Define events specific to object lifecycle.

Available targets include:

unmapped superclasses of mapped or to-be-mapped classes (using the propagate=True flag)

the Mapper class itself indicates listening for all mappers.

Instance events are closely related to mapper events, but are more specific to the instance and its instrumentation, rather than its system of persistence.

When using InstanceEvents, several modifiers are available to the listen() function.

propagate=False¶ – When True, the event listener should be applied to all inheriting classes as well as the class which is the target of this listener.

raw=False¶ – When True, the “target” argument passed to applicable event listener functions will be the instance’s InstanceState management object, rather than the mapped instance itself.

restore_load_context=False¶ –

Applies to the InstanceEvents.load() and InstanceEvents.refresh() events. Restores the loader context of the object when the event hook is complete, so that ongoing eager load operations continue to target the object appropriately. A warning is emitted if the object is moved to a new loader context from within one of these events if this flag is not set.

Added in version 1.3.14.

reference back to the _Dispatch class.

Receive an object instance after its attributes or some subset have been expired.

Called when the first instance of a particular mapping is called.

Receive an instance when its constructor is called.

Receive an instance when its constructor has been called, and raised an exception.

Receive an object instance after it has been created via __new__, and after initial attribute population has occurred.

Receive an object instance when its associated state is being pickled.

Receive an object instance after one or more attributes have been refreshed from a query.

Receive an object instance after one or more attributes that contain a column-level default or onupdate handler have been refreshed during persistence of the object’s state.

Receive an object instance after its associated state has been unpickled.

reference back to the _Dispatch class.

Bidirectional against _Dispatch._events

Receive an object instance after its attributes or some subset have been expired.

Example argument forms:

‘keys’ is a list of attribute names. If None, the entire state was expired.

target¶ – the mapped instance. If the event is configured with raw=True, this will instead be the InstanceState state-management object associated with the instance.

attrs¶ – sequence of attribute names which were expired, or None if all attributes were expired.

Called when the first instance of a particular mapping is called.

Example argument forms:

This event is called when the __init__ method of a class is called the first time for that particular class. The event invokes before __init__ actually proceeds as well as before the InstanceEvents.init() event is invoked.

Receive an instance when its constructor is called.

Example argument forms:

This method is only called during a userland construction of an object, in conjunction with the object’s constructor, e.g. its __init__ method. It is not called when an object is loaded from the database; see the InstanceEvents.load() event in order to intercept a database load.

The event is called before the actual __init__ constructor of the object is called. The kwargs dictionary may be modified in-place in order to affect what is passed to __init__.

target¶ – the mapped instance. If the event is configured with raw=True, this will instead be the InstanceState state-management object associated with the instance.

args¶ – positional arguments passed to the __init__ method. This is passed as a tuple and is currently immutable.

kwargs¶ – keyword arguments passed to the __init__ method. This structure can be altered in place.

InstanceEvents.init_failure()

InstanceEvents.load()

Receive an instance when its constructor has been called, and raised an exception.

Example argument forms:

This method is only called during a userland construction of an object, in conjunction with the object’s constructor, e.g. its __init__ method. It is not called when an object is loaded from the database.

The event is invoked after an exception raised by the __init__ method is caught. After the event is invoked, the original exception is re-raised outwards, so that the construction of the object still raises an exception. The actual exception and stack trace raised should be present in sys.exc_info().

target¶ – the mapped instance. If the event is configured with raw=True, this will instead be the InstanceState state-management object associated with the instance.

args¶ – positional arguments that were passed to the __init__ method.

kwargs¶ – keyword arguments that were passed to the __init__ method.

InstanceEvents.init()

InstanceEvents.load()

Receive an object instance after it has been created via __new__, and after initial attribute population has occurred.

Example argument forms:

This typically occurs when the instance is created based on incoming result rows, and is only called once for that instance’s lifetime.

During a result-row load, this event is invoked when the first row received for this instance is processed. When using eager loading with collection-oriented attributes, the additional rows that are to be loaded / processed in order to load subsequent collection items have not occurred yet. This has the effect both that collections will not be fully loaded, as well as that if an operation occurs within this event handler that emits another database load operation for the object, the “loading context” for the object can change and interfere with the existing eager loaders still in progress.

Examples of what can cause the “loading context” to change within the event handler include, but are not necessarily limited to:

accessing deferred attributes that weren’t part of the row, will trigger an “undefer” operation and refresh the object

accessing attributes on a joined-inheritance subclass that weren’t part of the row, will trigger a refresh operation.

As of SQLAlchemy 1.3.14, a warning is emitted when this occurs. The InstanceEvents.restore_load_context option may be used on the event to prevent this warning; this will ensure that the existing loading context is maintained for the object after the event is called:

Changed in version 1.3.14: Added InstanceEvents.restore_load_context and SessionEvents.restore_load_context flags which apply to “on load” events, which will ensure that the loading context for an object is restored when the event hook is complete; a warning is emitted if the load context of the object changes without this flag being set.

The InstanceEvents.load() event is also available in a class-method decorator format called reconstructor().

target¶ – the mapped instance. If the event is configured with raw=True, this will instead be the InstanceState state-management object associated with the instance.

context¶ – the QueryContext corresponding to the current Query in progress. This argument may be None if the load does not correspond to a Query, such as during Session.merge().

Maintaining Non-Mapped State Across Loads

InstanceEvents.init()

InstanceEvents.refresh()

SessionEvents.loaded_as_persistent()

Receive an object instance when its associated state is being pickled.

Example argument forms:

target¶ – the mapped instance. If the event is configured with raw=True, this will instead be the InstanceState state-management object associated with the instance.

state_dict¶ – the dictionary returned by __getstate__, containing the state to be pickled.

Receive an object instance after one or more attributes have been refreshed from a query.

Example argument forms:

Contrast this to the InstanceEvents.load() method, which is invoked when the object is first loaded from a query.

This event is invoked within the loader process before eager loaders may have been completed, and the object’s state may not be complete. Additionally, invoking row-level refresh operations on the object will place the object into a new loader context, interfering with the existing load context. See the note on InstanceEvents.load() for background on making use of the InstanceEvents.restore_load_context parameter, in order to resolve this scenario.

target¶ – the mapped instance. If the event is configured with raw=True, this will instead be the InstanceState state-management object associated with the instance.

context¶ – the QueryContext corresponding to the current Query in progress.

attrs¶ – sequence of attribute names which were populated, or None if all column-mapped, non-deferred attributes were populated.

Maintaining Non-Mapped State Across Loads

InstanceEvents.load()

Receive an object instance after one or more attributes that contain a column-level default or onupdate handler have been refreshed during persistence of the object’s state.

Example argument forms:

This event is the same as InstanceEvents.refresh() except it is invoked within the unit of work flush process, and includes only non-primary-key columns that have column level default or onupdate handlers, including Python callables as well as server side defaults and triggers which may be fetched via the RETURNING clause.

While the InstanceEvents.refresh_flush() event is triggered for an object that was INSERTed as well as for an object that was UPDATEd, the event is geared primarily towards the UPDATE process; it is mostly an internal artifact that INSERT actions can also trigger this event, and note that primary key columns for an INSERTed row are explicitly omitted from this event. In order to intercept the newly INSERTed state of an object, the SessionEvents.pending_to_persistent() and MapperEvents.after_insert() are better choices.

target¶ – the mapped instance. If the event is configured with raw=True, this will instead be the InstanceState state-management object associated with the instance.

flush_context¶ – Internal UOWTransaction object which handles the details of the flush.

attrs¶ – sequence of attribute names which were populated.

Maintaining Non-Mapped State Across Loads

Fetching Server-Generated Defaults

Column INSERT/UPDATE Defaults

Receive an object instance after its associated state has been unpickled.

Example argument forms:

target¶ – the mapped instance. If the event is configured with raw=True, this will instead be the InstanceState state-management object associated with the instance.

state_dict¶ – the dictionary sent to __setstate__, containing the state dictionary which was pickled.

Attribute events are triggered as things occur on individual attributes of ORM mapped objects. These events form the basis for things like custom validation functions as well as backref handlers.

Changing Attribute Behavior

Define events for object attributes.

inherits from sqlalchemy.event.Events

Define events for object attributes.

These are typically defined on the class-bound descriptor for the target class.

For example, to register a listener that will receive the AttributeEvents.append() event:

Listeners have the option to return a possibly modified version of the value, when the AttributeEvents.retval flag is passed to listen() or listens_for(), such as below, illustrated using the AttributeEvents.set() event:

A validation function like the above can also raise an exception such as ValueError to halt the operation.

The AttributeEvents.propagate flag is also important when applying listeners to mapped classes that also have mapped subclasses, as when using mapper inheritance patterns:

The full list of modifiers available to the listen() and listens_for() functions are below.

active_history=False¶ – When True, indicates that the “set” event would like to receive the “old” value being replaced unconditionally, even if this requires firing off database loads. Note that active_history can also be set directly via column_property() and relationship().

propagate=False¶ – When True, the listener function will be established not just for the class attribute given, but for attributes of the same name on all current subclasses of that class, as well as all future subclasses of that class, using an additional listener that listens for instrumentation events.

raw=False¶ – When True, the “target” argument to the event will be the InstanceState management object, rather than the mapped instance itself.

retval=False¶ – when True, the user-defined event listening must return the “value” argument from the function. This gives the listening function the opportunity to change the value that is ultimately used for a “set” or “append” event.

Receive a collection append event.

Receive a collection append event where the collection was not actually mutated.

Receive a collection ‘bulk replace’ event.

reference back to the _Dispatch class.

Receive a ‘collection dispose’ event.

Receive a ‘collection init’ event.

Receive a scalar “init” event.

Receive a ‘modified’ event.

Receive a collection remove event.

Receive a scalar set event.

Receive a collection append event.

Example argument forms:

The append event is invoked for each element as it is appended to the collection. This occurs for single-item appends as well as for a “bulk replace” operation.

target¶ – the object instance receiving the event. If the listener is registered with raw=True, this will be the InstanceState object.

value¶ – the value being appended. If this listener is registered with retval=True, the listener function must return this value, or a new value which replaces it.

initiator¶ – An instance of Event representing the initiation of the event. May be modified from its original value by backref handlers in order to control chained event propagation, as well as be inspected for information about the source of the event.

When the event is established using the AttributeEvents.include_key parameter set to True, this will be the key used in the operation, such as collection[some_key_or_index] = value. The parameter is not passed to the event at all if the the AttributeEvents.include_key was not used to set up the event; this is to allow backwards compatibility with existing event handlers that don’t include the key parameter.

Added in version 2.0.

if the event was registered with retval=True, the given value, or a new effective value, should be returned.

AttributeEvents - background on listener options such as propagation to subclasses.

AttributeEvents.bulk_replace()

Receive a collection append event where the collection was not actually mutated.

Example argument forms:

This event differs from AttributeEvents.append() in that it is fired off for de-duplicating collections such as sets and dictionaries, when the object already exists in the target collection. The event does not have a return value and the identity of the given object cannot be changed.

The event is used for cascading objects into a Session when the collection has already been mutated via a backref event.

target¶ – the object instance receiving the event. If the listener is registered with raw=True, this will be the InstanceState object.

value¶ – the value that would be appended if the object did not already exist in the collection.

initiator¶ – An instance of Event representing the initiation of the event. May be modified from its original value by backref handlers in order to control chained event propagation, as well as be inspected for information about the source of the event.

When the event is established using the AttributeEvents.include_key parameter set to True, this will be the key used in the operation, such as collection[some_key_or_index] = value. The parameter is not passed to the event at all if the the AttributeEvents.include_key was not used to set up the event; this is to allow backwards compatibility with existing event handlers that don’t include the key parameter.

Added in version 2.0.

No return value is defined for this event.

Added in version 1.4.15.

Receive a collection ‘bulk replace’ event.

Example argument forms:

This event is invoked for a sequence of values as they are incoming to a bulk collection set operation, which can be modified in place before the values are treated as ORM objects. This is an “early hook” that runs before the bulk replace routine attempts to reconcile which objects are already present in the collection and which are being removed by the net replace operation.

It is typical that this method be combined with use of the AttributeEvents.append() event. When using both of these events, note that a bulk replace operation will invoke the AttributeEvents.append() event for all new items, even after AttributeEvents.bulk_replace() has been invoked for the collection as a whole. In order to determine if an AttributeEvents.append() event is part of a bulk replace, use the symbol attributes.OP_BULK_REPLACE to test the incoming initiator:

Added in version 1.2.

target¶ – the object instance receiving the event. If the listener is registered with raw=True, this will be the InstanceState object.

value¶ – a sequence (e.g. a list) of the values being set. The handler can modify this list in place.

initiator¶ – An instance of Event representing the initiation of the event.

When the event is established using the AttributeEvents.include_key parameter set to True, this will be the sequence of keys used in the operation, typically only for a dictionary update. The parameter is not passed to the event at all if the the AttributeEvents.include_key was not used to set up the event; this is to allow backwards compatibility with existing event handlers that don’t include the key parameter.

Added in version 2.0.

AttributeEvents - background on listener options such as propagation to subclasses.

reference back to the _Dispatch class.

Bidirectional against _Dispatch._events

Receive a ‘collection dispose’ event.

Example argument forms:

This event is triggered for a collection-based attribute when a collection is replaced, that is:

The old collection received will contain its previous contents.

Changed in version 1.2: The collection passed to AttributeEvents.dispose_collection() will now have its contents before the dispose intact; previously, the collection would be empty.

AttributeEvents - background on listener options such as propagation to subclasses.

Receive a ‘collection init’ event.

Example argument forms:

This event is triggered for a collection-based attribute, when the initial “empty collection” is first generated for a blank attribute, as well as for when the collection is replaced with a new one, such as via a set event.

E.g., given that User.addresses is a relationship-based collection, the event is triggered here:

and also during replace operations:

target¶ – the object instance receiving the event. If the listener is registered with raw=True, this will be the InstanceState object.

collection¶ – the new collection. This will always be generated from what was specified as relationship.collection_class, and will always be empty.

collection_adapter¶ – the CollectionAdapter that will mediate internal access to the collection.

AttributeEvents - background on listener options such as propagation to subclasses.

AttributeEvents.init_scalar() - “scalar” version of this event.

Receive a scalar “init” event.

Example argument forms:

This event is invoked when an uninitialized, unpersisted scalar attribute is accessed, e.g. read:

The ORM’s default behavior when this occurs for an un-initialized attribute is to return the value None; note this differs from Python’s usual behavior of raising AttributeError. The event here can be used to customize what value is actually returned, with the assumption that the event listener would be mirroring a default generator that is configured on the Core Column object as well.

Since a default generator on a Column might also produce a changing value such as a timestamp, the AttributeEvents.init_scalar() event handler can also be used to set the newly returned value, so that a Core-level default generation function effectively fires off only once, but at the moment the attribute is accessed on the non-persisted object. Normally, no change to the object’s state is made when an uninitialized attribute is accessed (much older SQLAlchemy versions did in fact change the object’s state).

If a default generator on a column returned a particular constant, a handler might be used as follows:

Above, we initialize the attribute MyClass.some_attribute to the value of SOME_CONSTANT. The above code includes the following features:

By setting the value SOME_CONSTANT in the given dict_, we indicate that this value is to be persisted to the database. This supersedes the use of SOME_CONSTANT in the default generator for the Column. The active_column_defaults.py example given at Attribute Instrumentation illustrates using the same approach for a changing default, e.g. a timestamp generator. In this particular example, it is not strictly necessary to do this since SOME_CONSTANT would be part of the INSERT statement in either case.

By establishing the retval=True flag, the value we return from the function will be returned by the attribute getter. Without this flag, the event is assumed to be a passive observer and the return value of our function is ignored.

The propagate=True flag is significant if the mapped class includes inheriting subclasses, which would also make use of this event listener. Without this flag, an inheriting subclass will not use our event handler.

In the above example, the attribute set event AttributeEvents.set() as well as the related validation feature provided by validates is not invoked when we apply our value to the given dict_. To have these events to invoke in response to our newly generated value, apply the value to the given object as a normal attribute set operation:

When multiple listeners are set up, the generation of the value is “chained” from one listener to the next by passing the value returned by the previous listener that specifies retval=True as the value argument of the next listener.

target¶ – the object instance receiving the event. If the listener is registered with raw=True, this will be the InstanceState object.

value¶ – the value that is to be returned before this event listener were invoked. This value begins as the value None, however will be the return value of the previous event handler function if multiple listeners are present.

dict_¶ – the attribute dictionary of this mapped object. This is normally the __dict__ of the object, but in all cases represents the destination that the attribute system uses to get at the actual value of this attribute. Placing the value in this dictionary has the effect that the value will be used in the INSERT statement generated by the unit of work.

AttributeEvents.init_collection() - collection version of this event

AttributeEvents - background on listener options such as propagation to subclasses.

Attribute Instrumentation - see the active_column_defaults.py example.

Receive a ‘modified’ event.

Example argument forms:

This event is triggered when the flag_modified() function is used to trigger a modify event on an attribute without any specific value being set.

Added in version 1.2.

target¶ – the object instance receiving the event. If the listener is registered with raw=True, this will be the InstanceState object.

initiator¶ – An instance of Event representing the initiation of the event.

AttributeEvents - background on listener options such as propagation to subclasses.

Receive a collection remove event.

Example argument forms:

target¶ – the object instance receiving the event. If the listener is registered with raw=True, this will be the InstanceState object.

value¶ – the value being removed.

initiator¶ – An instance of Event representing the initiation of the event. May be modified from its original value by backref handlers in order to control chained event propagation.

When the event is established using the AttributeEvents.include_key parameter set to True, this will be the key used in the operation, such as del collection[some_key_or_index]. The parameter is not passed to the event at all if the the AttributeEvents.include_key was not used to set up the event; this is to allow backwards compatibility with existing event handlers that don’t include the key parameter.

Added in version 2.0.

No return value is defined for this event.

AttributeEvents - background on listener options such as propagation to subclasses.

Receive a scalar set event.

Example argument forms:

target¶ – the object instance receiving the event. If the listener is registered with raw=True, this will be the InstanceState object.

value¶ – the value being set. If this listener is registered with retval=True, the listener function must return this value, or a new value which replaces it.

oldvalue¶ – the previous value being replaced. This may also be the symbol NEVER_SET or NO_VALUE. If the listener is registered with active_history=True, the previous value of the attribute will be loaded from the database if the existing value is currently unloaded or expired.

initiator¶ – An instance of Event representing the initiation of the event. May be modified from its original value by backref handlers in order to control chained event propagation.

if the event was registered with retval=True, the given value, or a new effective value, should be returned.

AttributeEvents - background on listener options such as propagation to subclasses.

Represent events within the construction of a Query object.

inherits from sqlalchemy.event.Events

Represent events within the construction of a Query object.

The QueryEvents event methods are legacy as of SQLAlchemy 2.0, and only apply to direct use of the Query object. They are not used for 2.0 style statements. For events to intercept and modify 2.0 style ORM use, use the SessionEvents.do_orm_execute() hook.

The QueryEvents hooks are now superseded by the SessionEvents.do_orm_execute() event hook.

Receive the Query object before it is composed into a core Select object.

before_compile_delete()

Allow modifications to the Query object within Query.delete().

before_compile_update()

Allow modifications to the Query object within Query.update().

reference back to the _Dispatch class.

Receive the Query object before it is composed into a core Select object.

Example argument forms:

Deprecated since version 1.4: The QueryEvents.before_compile() event is superseded by the much more capable SessionEvents.do_orm_execute() hook. In version 1.4, the QueryEvents.before_compile() event is no longer used for ORM-level attribute loads, such as loads of deferred or expired attributes as well as relationship loaders. See the new examples in ORM Query Events which illustrate new ways of intercepting and modifying ORM queries for the most common purpose of adding arbitrary filter criteria.

This event is intended to allow changes to the query given:

The event should normally be listened with the retval=True parameter set, so that the modified query may be returned.

The QueryEvents.before_compile() event by default will disallow “baked” queries from caching a query, if the event hook returns a new Query object. This affects both direct use of the baked query extension as well as its operation within lazy loaders and eager loaders for relationships. In order to re-establish the query being cached, apply the event adding the bake_ok flag:

When bake_ok is set to True, the event hook will only be invoked once, and not called for subsequent invocations of a particular query that is being cached.

Added in version 1.3.11: - added the “bake_ok” flag to the QueryEvents.before_compile() event and disallowed caching via the “baked” extension from occurring for event handlers that return a new Query object if this flag is not set.

QueryEvents.before_compile_update()

QueryEvents.before_compile_delete()

Using the before_compile event

Allow modifications to the Query object within Query.delete().

Example argument forms:

Deprecated since version 1.4: The QueryEvents.before_compile_delete() event is superseded by the much more capable SessionEvents.do_orm_execute() hook.

Like the QueryEvents.before_compile() event, this event should be configured with retval=True, and the modified Query object returned, as in

query¶ – a Query instance; this is also the .query attribute of the given “delete context” object.

delete_context¶ – a “delete context” object which is the same kind of object as described in QueryEvents.after_bulk_delete.delete_context.

Added in version 1.2.17.

QueryEvents.before_compile()

QueryEvents.before_compile_update()

Allow modifications to the Query object within Query.update().

Example argument forms:

Deprecated since version 1.4: The QueryEvents.before_compile_update() event is superseded by the much more capable SessionEvents.do_orm_execute() hook.

Like the QueryEvents.before_compile() event, if the event is to be used to alter the Query object, it should be configured with retval=True, and the modified Query object returned, as in

The .values dictionary of the “update context” object can also be modified in place as illustrated above.

query¶ – a Query instance; this is also the .query attribute of the given “update context” object.

update_context¶ – an “update context” object which is the same kind of object as described in QueryEvents.after_bulk_update.update_context. The object has a .values attribute in an UPDATE context which is the dictionary of parameters passed to Query.update(). This dictionary can be modified to alter the VALUES clause of the resulting UPDATE statement.

Added in version 1.2.17.

QueryEvents.before_compile()

QueryEvents.before_compile_delete()

reference back to the _Dispatch class.

Bidirectional against _Dispatch._events

Defines SQLAlchemy’s system of class instrumentation.

This module is usually not directly visible to user applications, but defines a large part of the ORM’s interactivity.

instrumentation.py deals with registration of end-user classes for state tracking. It interacts closely with state.py and attributes.py which establish per-instance and per-class-attribute instrumentation, respectively.

The class instrumentation system can be customized on a per-class or global basis using the sqlalchemy.ext.instrumentation module, which provides the means to build and specify alternate instrumentation forms.

InstrumentationEvents

Events related to class instrumentation events.

inherits from sqlalchemy.event.Events

Events related to class instrumentation events.

The listeners here support being established against any new style class, that is any object that is a subclass of ‘type’. Events will then be fired off for events against that class. If the “propagate=True” flag is passed to event.listen(), the event will fire off for subclasses of that class as well.

The Python type builtin is also accepted as a target, which when used has the effect of events being emitted for all classes.

Note the “propagate” flag here is defaulted to True, unlike the other class level events where it defaults to False. This means that new subclasses will also be the subject of these events, when a listener is established on a superclass.

attribute_instrument()

Called when an attribute is instrumented.

Called after the given class is instrumented.

Called before the given class is uninstrumented.

reference back to the _Dispatch class.

Called when an attribute is instrumented.

Example argument forms:

Called after the given class is instrumented.

Example argument forms:

To get at the ClassManager, use manager_of_class().

Called before the given class is uninstrumented.

Example argument forms:

To get at the ClassManager, use manager_of_class().

reference back to the _Dispatch class.

Bidirectional against _Dispatch._events

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker


def my_before_commit(session):
    print("before commit!")


Session = sessionmaker()

event.listen(Session, "before_commit", my_before_commit)
```

Example 2 (python):
```python
from sqlalchemy import event


@event.listens_for(SomeSessionClassOrObject, 'after_attach')
def receive_after_attach(session, instance):
    "listen for the 'after_attach' event"

    # ... (event handling logic) ...
```

Example 3 (python):
```python
from sqlalchemy import event


@event.listens_for(SomeSessionClassOrObject, 'after_begin')
def receive_after_begin(session, transaction, connection):
    "listen for the 'after_begin' event"

    # ... (event handling logic) ...
```

Example 4 (python):
```python
from sqlalchemy import event


@event.listens_for(SomeSessionClassOrObject, 'after_bulk_delete')
def receive_after_bulk_delete(delete_context):
    "listen for the 'after_bulk_delete' event"

    # ... (event handling logic) ...

# DEPRECATED calling style (pre-0.9, will be removed in a future release)
@event.listens_for(SomeSessionClassOrObject, 'after_bulk_delete')
def receive_after_bulk_delete(session, query, query_context, result):
    "listen for the 'after_bulk_delete' event"

    # ... (event handling logic) ...
```

---
