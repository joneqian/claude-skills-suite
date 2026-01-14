# Sqlalchemy - Relationships

**Pages:** 7

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Basic Relationship Patterns¶
- Declarative vs. Imperative Forms¶
- One To Many¶
  - Using Sets, Lists, or other Collection Types for One To Many¶
  - Configuring Delete Behavior for One to Many¶
- Many To One¶

Home | Download this Documentation

Home | Download this Documentation

A quick walkthrough of the basic relational patterns, which in this section are illustrated using Declarative style mappings based on the use of the Mapped annotation type.

The setup for each of the following sections is as follows:

As SQLAlchemy has evolved, different ORM configurational styles have emerged. For examples in this section and others that use annotated Declarative mappings with Mapped, the corresponding non-annotated form should use the desired class, or string class name, as the first argument passed to relationship(). The example below illustrates the form used in this document, which is a fully Declarative example using PEP 484 annotations, where the relationship() construct is also deriving the target class and collection type from the Mapped annotation, which is the most modern form of SQLAlchemy Declarative mapping:

In contrast, using a Declarative mapping without annotations is the more “classic” form of mapping, where relationship() requires all parameters passed to it directly, as in the example below:

Finally, using Imperative Mapping, which is SQLAlchemy’s original mapping form before Declarative was made (which nonetheless remains preferred by a vocal minority of users), the above configuration looks like:

Additionally, the default collection style for non-annotated mappings is list. To use a set or other collection without annotations, indicate it using the relationship.collection_class parameter:

Detail on collection configuration for relationship() is at Customizing Collection Access.

Additional differences between annotated and non-annotated / imperative styles will be noted as needed.

A one to many relationship places a foreign key on the child table referencing the parent. relationship() is then specified on the parent, as referencing a collection of items represented by the child:

To establish a bidirectional relationship in one-to-many, where the “reverse” side is a many to one, specify an additional relationship() and connect the two using the relationship.back_populates parameter, using the attribute name of each relationship() as the value for relationship.back_populates on the other:

Child will get a parent attribute with many-to-one semantics.

Using annotated Declarative mappings, the type of collection used for the relationship() is derived from the collection type passed to the Mapped container type. The example from the previous section may be written to use a set rather than a list for the Parent.children collection using Mapped[Set["Child"]]:

When using non-annotated forms including imperative mappings, the Python class to use as a collection may be passed using the relationship.collection_class parameter.

Customizing Collection Access - contains further detail on collection configuration including some techniques to map relationship() to dictionaries.

It is often the case that all Child objects should be deleted when their owning Parent is deleted. To configure this behavior, the delete cascade option described at delete is used. An additional option is that a Child object can itself be deleted when it is deassociated from its parent. This behavior is described at delete-orphan.

Using foreign key ON DELETE cascade with ORM relationships

Many to one places a foreign key in the parent table referencing the child. relationship() is declared on the parent, where a new scalar-holding attribute will be created:

The above example shows a many-to-one relationship that assumes non-nullable behavior; the next section, Nullable Many-to-One, illustrates a nullable version.

Bidirectional behavior is achieved by adding a second relationship() and applying the relationship.back_populates parameter in both directions, using the attribute name of each relationship() as the value for relationship.back_populates on the other:

In the preceding example, the Parent.child relationship is not typed as allowing None; this follows from the Parent.child_id column itself not being nullable, as it is typed with Mapped[int]. If we wanted Parent.child to be a nullable many-to-one, we can set both Parent.child_id and Parent.child to be Optional[] (or its equivalent), in which case the configuration would look like:

Above, the column for Parent.child_id will be created in DDL to allow NULL values. When using mapped_column() with explicit typing declarations, the specification of child_id: Mapped[Optional[int]] is equivalent to setting Column.nullable to True on the Column, whereas child_id: Mapped[int] is equivalent to setting it to False. See mapped_column() derives the datatype and nullability from the Mapped annotation for background on this behavior.

If using Python 3.10 or greater, PEP 604 syntax is more convenient to indicate optional types using | None, which when combined with PEP 563 postponed annotation evaluation so that string-quoted types aren’t required, would look like:

One To One is essentially a One To Many relationship from a foreign key perspective, but indicates that there will only be one row at any time that refers to a particular parent row.

When using annotated mappings with Mapped, the “one-to-one” convention is achieved by applying a non-collection type to the Mapped annotation on both sides of the relationship, which will imply to the ORM that a collection should not be used on either side, as in the example below:

Above, when we load a Parent object, the Parent.child attribute will refer to a single Child object rather than a collection. If we replace the value of Parent.child with a new Child object, the ORM’s unit of work process will replace the previous Child row with the new one, setting the previous child.parent_id column to NULL by default unless there are specific cascade behaviors set up.

As mentioned previously, the ORM considers the “one-to-one” pattern as a convention, where it makes the assumption that when it loads the Parent.child attribute on a Parent object, it will get only one row back. If more than one row is returned, the ORM will emit a warning.

However, the Child.parent side of the above relationship remains as a “many-to-one” relationship. By itself, it will not detect assignment of more than one Child, unless the relationship.single_parent parameter is set, which may be useful:

Outside of setting this parameter, the “one-to-many” side (which here is one-to-one by convention) will also not reliably detect if more than one Child is associated with a single Parent, such as in the case where the multiple Child objects are pending and not database-persistent.

Whether or not relationship.single_parent is used, it is recommended that the database schema include a unique constraint to indicate that the Child.parent_id column should be unique, to ensure at the database level that only one Child row may refer to a particular Parent row at a time (see Declarative Table Configuration for background on the __table_args__ tuple syntax):

Added in version 2.0: The relationship() construct can derive the effective value of the relationship.uselist parameter from a given Mapped annotation.

When using relationship() without the benefit of Mapped annotations, the one-to-one pattern can be enabled using the relationship.uselist parameter set to False on what would normally be the “many” side, illustrated in a non-annotated Declarative configuration below:

Many to Many adds an association table between two classes. The association table is nearly always given as a Core Table object or other Core selectable such as a Join object, and is indicated by the relationship.secondary argument to relationship(). Usually, the Table uses the MetaData object associated with the declarative base class, so that the ForeignKey directives can locate the remote tables with which to link:

The “association table” above has foreign key constraints established that refer to the two entity tables on either side of the relationship. The data type of each of association.left_id and association.right_id is normally inferred from that of the referenced table and may be omitted. It is also recommended, though not in any way required by SQLAlchemy, that the columns which refer to the two entity tables are established within either a unique constraint or more commonly as the primary key constraint; this ensures that duplicate rows won’t be persisted within the table regardless of issues on the application side:

For a bidirectional relationship, both sides of the relationship contain a collection. Specify using relationship.back_populates, and for each relationship() specify the common association table:

The relationship.secondary parameter of relationship() also accepts two different “late evaluated” forms, including string table name as well as lambda callable. See the section Using a late-evaluated form for the “secondary” argument of many-to-many for background and examples.

Configuration of collections for a Many to Many relationship is identical to that of One To Many, as described at Using Sets, Lists, or other Collection Types for One To Many. For an annotated mapping using Mapped, the collection can be indicated by the type of collection used within the Mapped generic class, such as set:

When using non-annotated forms including imperative mappings, as is the case with one-to-many, the Python class to use as a collection may be passed using the relationship.collection_class parameter.

Customizing Collection Access - contains further detail on collection configuration including some techniques to map relationship() to dictionaries.

A behavior which is unique to the relationship.secondary argument to relationship() is that the Table which is specified here is automatically subject to INSERT and DELETE statements, as objects are added or removed from the collection. There is no need to delete from this table manually. The act of removing a record from the collection will have the effect of the row being deleted on flush:

A question which often arises is how the row in the “secondary” table can be deleted when the child object is handed directly to Session.delete():

There are several possibilities here:

If there is a relationship() from Parent to Child, but there is not a reverse-relationship that links a particular Child to each Parent, SQLAlchemy will not have any awareness that when deleting this particular Child object, it needs to maintain the “secondary” table that links it to the Parent. No delete of the “secondary” table will occur.

If there is a relationship that links a particular Child to each Parent, suppose it’s called Child.parents, SQLAlchemy by default will load in the Child.parents collection to locate all Parent objects, and remove each row from the “secondary” table which establishes this link. Note that this relationship does not need to be bidirectional; SQLAlchemy is strictly looking at every relationship() associated with the Child object being deleted.

A higher performing option here is to use ON DELETE CASCADE directives with the foreign keys used by the database. Assuming the database supports this feature, the database itself can be made to automatically delete rows in the “secondary” table as referencing rows in “child” are deleted. SQLAlchemy can be instructed to forego actively loading in the Child.parents collection in this case using the relationship.passive_deletes directive on relationship(); see Using foreign key ON DELETE cascade with ORM relationships for more details on this.

Note again, these behaviors are only relevant to the relationship.secondary option used with relationship(). If dealing with association tables that are mapped explicitly and are not present in the relationship.secondary option of a relevant relationship(), cascade rules can be used instead to automatically delete entities in reaction to a related entity being deleted - see Cascades for information on this feature.

Using delete cascade with many-to-many relationships

Using foreign key ON DELETE with many-to-many relationships

The association object pattern is a variant on many-to-many: it’s used when an association table contains additional columns beyond those which are foreign keys to the parent and child (or left and right) tables, columns which are most ideally mapped to their own ORM mapped class. This mapped class is mapped against the Table that would otherwise be noted as relationship.secondary when using the many-to-many pattern.

In the association object pattern, the relationship.secondary parameter is not used; instead, a class is mapped directly to the association table. Two individual relationship() constructs then link first the parent side to the mapped association class via one to many, and then the mapped association class to the child side via many-to-one, to form a uni-directional association object relationship from parent, to association, to child. For a bi-directional relationship, four relationship() constructs are used to link the mapped association class to both parent and child in both directions.

The example below illustrates a new class Association which maps to the Table named association; this table now includes an additional column called extra_data, which is a string value that is stored along with each association between Parent and Child. By mapping the table to an explicit class, rudimental access from Parent to Child makes explicit use of Association:

To illustrate the bi-directional version, we add two more relationship() constructs, linked to the existing ones using relationship.back_populates:

Working with the association pattern in its direct form requires that child objects are associated with an association instance before being appended to the parent; similarly, access from parent to child goes through the association object:

To enhance the association object pattern such that direct access to the Association object is optional, SQLAlchemy provides the Association Proxy extension. This extension allows the configuration of attributes which will access two “hops” with a single access, one “hop” to the associated object, and a second to a target attribute.

Association Proxy - allows direct “many to many” style access between parent and child for a three-class association object mapping.

Avoid mixing the association object pattern with the many-to-many pattern directly, as this produces conditions where data may be read and written in an inconsistent fashion without special steps; the association proxy is typically used to provide more succinct access. For more detailed background on the caveats introduced by this combination, see the next section Combining Association Object with Many-to-Many Access Patterns.

As mentioned in the previous section, the association object pattern does not automatically integrate with usage of the many-to-many pattern against the same tables/columns at the same time. From this it follows that read operations may return conflicting data and write operations may also attempt to flush conflicting changes, causing either integrity errors or unexpected inserts or deletes.

To illustrate, the example below configures a bidirectional many-to-many relationship between Parent and Child via Parent.children and Child.parents. At the same time, an association object relationship is also configured, between Parent.child_associations -> Association.child and Child.parent_associations -> Association.parent:

When using this ORM model to make changes, changes made to Parent.children will not be coordinated with changes made to Parent.child_associations or Child.parent_associations in Python; while all of these relationships will continue to function normally by themselves, changes on one will not show up in another until the Session is expired, which normally occurs automatically after Session.commit().

Additionally, if conflicting changes are made, such as adding a new Association object while also appending the same related Child to Parent.children, this will raise integrity errors when the unit of work flush process proceeds, as in the example below:

Appending Child to Parent.children directly also implies the creation of rows in the association table without indicating any value for the association.extra_data column, which will receive NULL for its value.

It’s fine to use a mapping like the above if you know what you’re doing; there may be good reason to use many-to-many relationships in the case where use of the “association object” pattern is infrequent, which is that it’s easier to load relationships along a single many-to-many relationship, which can also optimize slightly better how the “secondary” table is used in SQL statements, compared to how two separate relationships to an explicit association class is used. It’s at least a good idea to apply the relationship.viewonly parameter to the “secondary” relationship to avoid the issue of conflicting changes occurring, as well as preventing NULL being written to the additional association columns, as below:

The above mapping will not write any changes to Parent.children or Child.parents to the database, preventing conflicting writes. However, reads of Parent.children or Child.parents will not necessarily match the data that’s read from Parent.child_associations or Child.parent_associations, if changes are being made to these collections within the same transaction or Session as where the viewonly collections are being read. If use of the association object relationships is infrequent and is carefully organized against code that accesses the many-to-many collections to avoid stale reads (in extreme cases, making direct use of Session.expire() to cause collections to be refreshed within the current transaction), the pattern may be feasible.

A popular alternative to the above pattern is one where the direct many-to-many Parent.children and Child.parents relationships are replaced with an extension that will transparently proxy through the Association class, while keeping everything consistent from the ORM’s point of view. This extension is known as the Association Proxy.

Association Proxy - allows direct “many to many” style access between parent and child for a three-class association object mapping.

Most of the examples in the preceding sections illustrate mappings where the various relationship() constructs refer to their target classes using a string name, rather than the class itself, such as when using Mapped, a forward reference is generated that exists at runtime only as a string:

Similarly, when using non-annotated forms such as non-annotated Declarative or Imperative mappings, a string name is also supported directly by the relationship() construct:

These string names are resolved into classes in the mapper resolution stage, which is an internal process that occurs typically after all mappings have been defined and is normally triggered by the first usage of the mappings themselves. The registry object is the container where these names are stored and resolved to the mapped classes to which they refer.

In addition to the main class argument for relationship(), other arguments which depend upon the columns present on an as-yet undefined class may also be specified either as Python functions, or more commonly as strings. For most of these arguments except that of the main argument, string inputs are evaluated as Python expressions using Python’s built-in eval() function, as they are intended to receive complete SQL expressions.

As the Python eval() function is used to interpret the late-evaluated string arguments passed to relationship() mapper configuration construct, these arguments should not be repurposed such that they would receive untrusted user input; eval() is not secure against untrusted user input.

The full namespace available within this evaluation includes all classes mapped for this declarative base, as well as the contents of the sqlalchemy package, including expression functions like desc() and sqlalchemy.sql.functions.func:

For the case where more than one module contains a class of the same name, string class names can also be specified as module-qualified paths within any of these string expressions:

In an example like the above, the string passed to Mapped can be disambiguated from a specific class argument by passing the class location string directly to the first positional parameter (relationship.argument) as well. Below illustrates a typing-only import for Child, combined with a runtime specifier for the target class that will search for the correct name within the registry:

The qualified path can be any partial path that removes ambiguity between the names. For example, to disambiguate between myapp.model1.Child and myapp.model2.Child, we can specify model1.Child or model2.Child:

The relationship() construct also accepts Python functions or lambdas as input for these arguments. A Python functional approach might look like the following:

The full list of parameters which accept Python functions/lambdas or strings that will be passed to eval() are:

relationship.order_by

relationship.primaryjoin

relationship.secondaryjoin

relationship.secondary

relationship.remote_side

relationship.foreign_keys

relationship._user_defined_foreign_keys

As stated previously, the above parameters to relationship() are evaluated as Python code expressions using eval(). DO NOT PASS UNTRUSTED INPUT TO THESE ARGUMENTS.

It should also be noted that in a similar way as described at Appending additional columns to an existing Declarative mapped class, any MapperProperty construct can be added to a declarative base mapping at any time (noting that annotated forms are not supported in this context). If we wanted to implement this relationship() after the Address class were available, we could also apply it afterwards:

As is the case for ORM mapped columns, there’s no capability for the Mapped annotation type to take part in this operation; therefore, the related class must be specified directly within the relationship() construct, either as the class itself, the string name of the class, or a callable function that returns a reference to the target class.

As is the case for ORM mapped columns, assignment of mapped properties to an already mapped class will only function correctly if the “declarative base” class is used, meaning the user-defined subclass of DeclarativeBase or the dynamically generated class returned by declarative_base() or registry.generate_base(). This “base” class includes a Python metaclass which implements a special __setattr__() method that intercepts these operations.

Runtime assignment of class-mapped attributes to a mapped class will not work if the class is mapped using decorators like registry.mapped() or imperative functions like registry.map_imperatively().

Many-to-many relationships make use of the relationship.secondary parameter, which ordinarily indicates a reference to a typically non-mapped Table object or other Core selectable object. Late evaluation using a lambda callable is typical.

For the example given at Many To Many, if we assumed that the association_table Table object would be defined at a point later on in the module than the mapped class itself, we may write the relationship() using a lambda as:

As a shortcut for table names that are also valid Python identifiers, the relationship.secondary parameter may also be passed as a string, where resolution works by evaluation of the string as a Python expression, with simple identifier names linked to same-named Table objects that are present in the same MetaData collection referenced by the current registry.

In the example below, the expression "association_table" is evaluated as a variable named “association_table” that is resolved against the table names within the MetaData collection:

When passed as a string, the name passed to relationship.secondary must be a valid Python identifier starting with a letter and containing only alphanumeric characters or underscores. Other characters such as dashes etc. will be interpreted as Python operators which will not resolve to the name given. Please consider using lambda expressions rather than strings for improved clarity.

When passed as a string, relationship.secondary argument is interpreted using Python’s eval() function, even though it’s typically the name of a table. DO NOT PASS UNTRUSTED INPUT TO THIS STRING.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from __future__ import annotations
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass
```

Example 2 (typescript):
```typescript
class Parent(Base):
    __tablename__ = "parent_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["Child"]] = relationship(back_populates="parent")


class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))
    parent: Mapped["Parent"] = relationship(back_populates="children")
```

Example 3 (typescript):
```typescript
class Parent(Base):
    __tablename__ = "parent_table"

    id = mapped_column(Integer, primary_key=True)
    children = relationship("Child", back_populates="parent")


class Child(Base):
    __tablename__ = "child_table"

    id = mapped_column(Integer, primary_key=True)
    parent_id = mapped_column(ForeignKey("parent_table.id"))
    parent = relationship("Parent", back_populates="children")
```

Example 4 (json):
```json
registry.map_imperatively(
    Parent,
    parent_table,
    properties={"children": relationship("Child", back_populates="parent")},
)

registry.map_imperatively(
    Child,
    child_table,
    properties={"parent": relationship("Parent", back_populates="children")},
)
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/collection_api.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Collection Customization and API Details¶
- Customizing Collection Access¶
  - Dictionary Collections¶
    - Dealing with Key Mutations and back-populating for Dictionary collections¶
- Custom Collection Implementations¶
  - Annotating Custom Collections via Decorators¶

Home | Download this Documentation

Home | Download this Documentation

The relationship() function defines a linkage between two classes. When the linkage defines a one-to-many or many-to-many relationship, it’s represented as a Python collection when objects are loaded and manipulated. This section presents additional information about collection configuration and techniques.

Mapping a one-to-many or many-to-many relationship results in a collection of values accessible through an attribute on the parent instance. The two common collection types for these are list and set, which in Declarative mappings that use Mapped is established by using the collection type within the Mapped container, as demonstrated in the Parent.children collection below where list is used:

Or for a set, illustrated in the same Parent.children collection:

If using Python 3.7 or 3.8, annotations for collections need to use typing.List or typing.Set, e.g. Mapped[List["Child"]] or Mapped[Set["Child"]]; the list and set Python built-ins don’t yet support generic annotation in these Python versions, such as:

When using mappings without the Mapped annotation, such as when using imperative mappings or untyped Python code, as well as in a few special cases, the collection class for a relationship() can always be specified directly using the relationship.collection_class parameter:

In the absence of relationship.collection_class or Mapped, the default collection type is list.

Beyond list and set builtins, there is also support for two varieties of dictionary, described below at Dictionary Collections. There is also support for any arbitrary mutable sequence type can be set up as the target collection, with some additional configuration steps; this is described in the section Custom Collection Implementations.

A little extra detail is needed when using a dictionary as a collection. This because objects are always loaded from the database as lists, and a key-generation strategy must be available to populate the dictionary correctly. The attribute_keyed_dict() function is by far the most common way to achieve a simple dictionary collection. It produces a dictionary class that will apply a particular attribute of the mapped class as a key. Below we map an Item class containing a dictionary of Note items keyed to the Note.keyword attribute. When using attribute_keyed_dict(), the Mapped annotation may be typed using the KeyFuncDict or just plain dict as illustrated in the following example. However, the relationship.collection_class parameter is required in this case so that the attribute_keyed_dict() may be appropriately parametrized:

Item.notes is then a dictionary:

attribute_keyed_dict() will ensure that the .keyword attribute of each Note complies with the key in the dictionary. Such as, when assigning to Item.notes, the dictionary key we supply must match that of the actual Note object:

The attribute which attribute_keyed_dict() uses as a key does not need to be mapped at all! Using a regular Python @property allows virtually any detail or combination of details about the object to be used as the key, as below when we establish it as a tuple of Note.keyword and the first ten letters of the Note.text field:

Above we added a Note.item relationship, with a bi-directional relationship.back_populates configuration. Assigning to this reverse relationship, the Note is added to the Item.notes dictionary and the key is generated for us automatically:

Other built-in dictionary types include column_keyed_dict(), which is almost like attribute_keyed_dict() except given the Column object directly:

as well as mapped_collection() which is passed any callable function. Note that it’s usually easier to use attribute_keyed_dict() along with a @property as mentioned earlier:

Dictionary mappings are often combined with the “Association Proxy” extension to produce streamlined dictionary views. See Proxying to Dictionary Based Collections and Composite Association Proxies for examples.

When using attribute_keyed_dict(), the “key” for the dictionary is taken from an attribute on the target object. Changes to this key are not tracked. This means that the key must be assigned towards when it is first used, and if the key changes, the collection will not be mutated. A typical example where this might be an issue is when relying upon backrefs to populate an attribute mapped collection. Given the following:

Above, if we create a B() that refers to a specific A(), the back populates will then add the B() to the A.bs collection, however if the value of B.data is not set yet, the key will be None:

Setting b1.data after the fact does not update the collection:

This can also be seen if one attempts to set up B() in the constructor. The order of arguments changes the result:

If backrefs are being used in this way, ensure that attributes are populated in the correct order using an __init__ method.

An event handler such as the following may also be used to track changes in the collection as well:

You can use your own types for collections as well. In simple cases, inheriting from list or set, adding custom behavior, is all that’s needed. In other cases, special decorators are needed to tell SQLAlchemy more detail about how the collection operates.

Do I need a custom collection implementation?

In most cases not at all! The most common use cases for a “custom” collection is one that validates or marshals incoming values into a new form, such as a string that becomes a class instance, or one which goes a step beyond and represents the data internally in some fashion, presenting a “view” of that data on the outside of a different form.

For the first use case, the validates() decorator is by far the simplest way to intercept incoming values in all cases for the purposes of validation and simple marshaling. See Simple Validators for an example of this.

For the second use case, the Association Proxy extension is a well-tested, widely used system that provides a read/write “view” of a collection in terms of some attribute present on the target object. As the target attribute can be a @property that returns virtually anything, a wide array of “alternative” views of a collection can be constructed with just a few functions. This approach leaves the underlying mapped collection unaffected and avoids the need to carefully tailor collection behavior on a method-by-method basis.

Customized collections are useful when the collection needs to have special behaviors upon access or mutation operations that can’t otherwise be modeled externally to the collection. They can of course be combined with the above two approaches.

Collections in SQLAlchemy are transparently instrumented. Instrumentation means that normal operations on the collection are tracked and result in changes being written to the database at flush time. Additionally, collection operations can fire events which indicate some secondary operation must take place. Examples of a secondary operation include saving the child item in the parent’s Session (i.e. the save-update cascade), as well as synchronizing the state of a bi-directional relationship (i.e. a backref()).

The collections package understands the basic interface of lists, sets and dicts and will automatically apply instrumentation to those built-in types and their subclasses. Object-derived types that implement a basic collection interface are detected and instrumented via duck-typing:

append, remove, and extend are known members of list, and will be instrumented automatically. __iter__ is not a mutator method and won’t be instrumented, and foo won’t be either.

Duck-typing (i.e. guesswork) isn’t rock-solid, of course, so you can be explicit about the interface you are implementing by providing an __emulates__ class attribute:

This class looks similar to a Python list (i.e. “list-like”) as it has an append method, but the __emulates__ attribute forces it to be treated as a set. remove is known to be part of the set interface and will be instrumented.

But this class won’t work quite yet: a little glue is needed to adapt it for use by SQLAlchemy. The ORM needs to know which methods to use to append, remove and iterate over members of the collection. When using a type like list or set, the appropriate methods are well-known and used automatically when present. However the class above, which only roughly resembles a set, does not provide the expected add method, so we must indicate to the ORM the method that will instead take the place of the add method, in this case using a decorator @collection.appender; this is illustrated in the next section.

Decorators can be used to tag the individual methods the ORM needs to manage collections. Use them when your class doesn’t quite meet the regular interface for its container type, or when you otherwise would like to use a different method to get the job done.

And that’s all that’s needed to complete the example. SQLAlchemy will add instances via the append method. remove and __iter__ are the default methods for sets and will be used for removing and iteration. Default methods can be changed as well:

There is no requirement to be “list-like” or “set-like” at all. Collection classes can be any shape, so long as they have the append, remove and iterate interface marked for SQLAlchemy’s use. Append and remove methods will be called with a mapped entity as the single argument, and iterator methods are called with no arguments and must return an iterator.

The KeyFuncDict class can be used as a base class for your custom types or as a mix-in to quickly add dict collection support to other classes. It uses a keying function to delegate to __setitem__ and __delitem__:

When subclassing KeyFuncDict, user-defined versions of __setitem__() or __delitem__() should be decorated with collection.internally_instrumented(), if they call down to those same methods on KeyFuncDict. This because the methods on KeyFuncDict are already instrumented - calling them from within an already instrumented call can cause events to be fired off repeatedly, or inappropriately, leading to internal state corruption in rare cases:

The ORM understands the dict interface just like lists and sets, and will automatically instrument all “dict-like” methods if you choose to subclass dict or provide dict-like collection behavior in a duck-typed class. You must decorate appender and remover methods, however- there are no compatible methods in the basic dictionary interface for SQLAlchemy to use by default. Iteration will go through values() unless otherwise decorated.

Many custom types and existing library classes can be used as a entity collection type as-is without further ado. However, it is important to note that the instrumentation process will modify the type, adding decorators around methods automatically.

The decorations are lightweight and no-op outside of relationships, but they do add unneeded overhead when triggered elsewhere. When using a library class as a collection, it can be good practice to use the “trivial subclass” trick to restrict the decorations to just your usage in relationships. For example:

The ORM uses this approach for built-ins, quietly substituting a trivial subclass when a list, set or dict is used directly.

attribute_keyed_dict(attr_name, *, [ignore_unpopulated_attribute])

A dictionary-based collection type with attribute-based keying.

attribute_mapped_collection

A dictionary-based collection type with attribute-based keying.

column_keyed_dict(mapping_spec, *, [ignore_unpopulated_attribute])

A dictionary-based collection type with column-based keying.

column_mapped_collection

A dictionary-based collection type with column-based keying.

keyfunc_mapping(keyfunc, *, [ignore_unpopulated_attribute])

A dictionary-based collection type with arbitrary keying.

Base for ORM mapped dictionary classes.

A dictionary-based collection type with arbitrary keying.

Base for ORM mapped dictionary classes.

A dictionary-based collection type with attribute-based keying.

Changed in version 2.0: Renamed attribute_mapped_collection to attribute_keyed_dict().

Returns a KeyFuncDict factory which will produce new dictionary keys based on the value of a particular named attribute on ORM mapped instances to be added to the dictionary.

the value of the target attribute must be assigned with its value at the time that the object is being added to the dictionary collection. Additionally, changes to the key attribute are not tracked, which means the key in the dictionary is not automatically synchronized with the key value on the target object itself. See Dealing with Key Mutations and back-populating for Dictionary collections for further details.

Dictionary Collections - background on use

attr_name¶ – string name of an ORM-mapped attribute on the mapped class, the value of which on a particular instance is to be used as the key for a new dictionary entry for that instance.

ignore_unpopulated_attribute¶ –

if True, and the target attribute on an object is not populated at all, the operation will be silently skipped. By default, an error is raised.

Added in version 2.0: an error is raised by default if the attribute being used for the dictionary key is determined that it was never populated with any value. The attribute_keyed_dict.ignore_unpopulated_attribute parameter may be set which will instead indicate that this condition should be ignored, and the append operation silently skipped. This is in contrast to the behavior of the 1.x series which would erroneously populate the value in the dictionary with an arbitrary key value of None.

A dictionary-based collection type with column-based keying.

Changed in version 2.0: Renamed column_mapped_collection to column_keyed_dict.

Returns a KeyFuncDict factory which will produce new dictionary keys based on the value of a particular Column-mapped attribute on ORM mapped instances to be added to the dictionary.

the value of the target attribute must be assigned with its value at the time that the object is being added to the dictionary collection. Additionally, changes to the key attribute are not tracked, which means the key in the dictionary is not automatically synchronized with the key value on the target object itself. See Dealing with Key Mutations and back-populating for Dictionary collections for further details.

Dictionary Collections - background on use

mapping_spec¶ – a Column object that is expected to be mapped by the target mapper to a particular attribute on the mapped class, the value of which on a particular instance is to be used as the key for a new dictionary entry for that instance.

ignore_unpopulated_attribute¶ –

if True, and the mapped attribute indicated by the given Column target attribute on an object is not populated at all, the operation will be silently skipped. By default, an error is raised.

Added in version 2.0: an error is raised by default if the attribute being used for the dictionary key is determined that it was never populated with any value. The column_keyed_dict.ignore_unpopulated_attribute parameter may be set which will instead indicate that this condition should be ignored, and the append operation silently skipped. This is in contrast to the behavior of the 1.x series which would erroneously populate the value in the dictionary with an arbitrary key value of None.

A dictionary-based collection type with arbitrary keying.

Changed in version 2.0: Renamed mapped_collection to keyfunc_mapping().

Returns a KeyFuncDict factory with a keying function generated from keyfunc, a callable that takes an entity and returns a key value.

the given keyfunc is called only once at the time that the target object is being added to the collection. Changes to the effective value returned by the function are not tracked.

Dictionary Collections - background on use

keyfunc¶ – a callable that will be passed the ORM-mapped instance which should then generate a new key to use in the dictionary. If the value returned is LoaderCallableStatus.NO_VALUE, an error is raised.

ignore_unpopulated_attribute¶ –

if True, and the callable returns LoaderCallableStatus.NO_VALUE for a particular instance, the operation will be silently skipped. By default, an error is raised.

Added in version 2.0: an error is raised by default if the callable being used for the dictionary key returns LoaderCallableStatus.NO_VALUE, which in an ORM attribute context indicates an attribute that was never populated with any value. The mapped_collection.ignore_unpopulated_attribute parameter may be set which will instead indicate that this condition should be ignored, and the append operation silently skipped. This is in contrast to the behavior of the 1.x series which would erroneously populate the value in the dictionary with an arbitrary key value of None.

A dictionary-based collection type with attribute-based keying.

Changed in version 2.0: Renamed attribute_mapped_collection to attribute_keyed_dict().

Returns a KeyFuncDict factory which will produce new dictionary keys based on the value of a particular named attribute on ORM mapped instances to be added to the dictionary.

the value of the target attribute must be assigned with its value at the time that the object is being added to the dictionary collection. Additionally, changes to the key attribute are not tracked, which means the key in the dictionary is not automatically synchronized with the key value on the target object itself. See Dealing with Key Mutations and back-populating for Dictionary collections for further details.

Dictionary Collections - background on use

attr_name – string name of an ORM-mapped attribute on the mapped class, the value of which on a particular instance is to be used as the key for a new dictionary entry for that instance.

ignore_unpopulated_attribute –

if True, and the target attribute on an object is not populated at all, the operation will be silently skipped. By default, an error is raised.

Added in version 2.0: an error is raised by default if the attribute being used for the dictionary key is determined that it was never populated with any value. The attribute_keyed_dict.ignore_unpopulated_attribute parameter may be set which will instead indicate that this condition should be ignored, and the append operation silently skipped. This is in contrast to the behavior of the 1.x series which would erroneously populate the value in the dictionary with an arbitrary key value of None.

A dictionary-based collection type with column-based keying.

Changed in version 2.0: Renamed column_mapped_collection to column_keyed_dict.

Returns a KeyFuncDict factory which will produce new dictionary keys based on the value of a particular Column-mapped attribute on ORM mapped instances to be added to the dictionary.

the value of the target attribute must be assigned with its value at the time that the object is being added to the dictionary collection. Additionally, changes to the key attribute are not tracked, which means the key in the dictionary is not automatically synchronized with the key value on the target object itself. See Dealing with Key Mutations and back-populating for Dictionary collections for further details.

Dictionary Collections - background on use

mapping_spec – a Column object that is expected to be mapped by the target mapper to a particular attribute on the mapped class, the value of which on a particular instance is to be used as the key for a new dictionary entry for that instance.

ignore_unpopulated_attribute –

if True, and the mapped attribute indicated by the given Column target attribute on an object is not populated at all, the operation will be silently skipped. By default, an error is raised.

Added in version 2.0: an error is raised by default if the attribute being used for the dictionary key is determined that it was never populated with any value. The column_keyed_dict.ignore_unpopulated_attribute parameter may be set which will instead indicate that this condition should be ignored, and the append operation silently skipped. This is in contrast to the behavior of the 1.x series which would erroneously populate the value in the dictionary with an arbitrary key value of None.

A dictionary-based collection type with arbitrary keying.

Changed in version 2.0: Renamed mapped_collection to keyfunc_mapping().

Returns a KeyFuncDict factory with a keying function generated from keyfunc, a callable that takes an entity and returns a key value.

the given keyfunc is called only once at the time that the target object is being added to the collection. Changes to the effective value returned by the function are not tracked.

Dictionary Collections - background on use

keyfunc – a callable that will be passed the ORM-mapped instance which should then generate a new key to use in the dictionary. If the value returned is LoaderCallableStatus.NO_VALUE, an error is raised.

ignore_unpopulated_attribute –

if True, and the callable returns LoaderCallableStatus.NO_VALUE for a particular instance, the operation will be silently skipped. By default, an error is raised.

Added in version 2.0: an error is raised by default if the callable being used for the dictionary key returns LoaderCallableStatus.NO_VALUE, which in an ORM attribute context indicates an attribute that was never populated with any value. The mapped_collection.ignore_unpopulated_attribute parameter may be set which will instead indicate that this condition should be ignored, and the append operation silently skipped. This is in contrast to the behavior of the 1.x series which would erroneously populate the value in the dictionary with an arbitrary key value of None.

inherits from builtins.dict, typing.Generic

Base for ORM mapped dictionary classes.

Extends the dict type with additional methods needed by SQLAlchemy ORM collection classes. Use of KeyFuncDict is most directly by using the attribute_keyed_dict() or column_keyed_dict() class factories. KeyFuncDict may also serve as the base for user-defined custom dictionary classes.

Changed in version 2.0: Renamed MappedCollection to KeyFuncDict.

attribute_keyed_dict()

Dictionary Collections

Custom Collection Implementations

Create a new collection with keying provided by keyfunc.

Remove all items from the dict.

If the key is not found, return the default if given; otherwise, raise a KeyError.

Remove and return a (key, value) pair as a 2-tuple.

Remove an item by value, consulting the keyfunc for the key.

Add an item by value, consulting the keyfunc for the key.

Insert key with a value of default if key is not in the dictionary.

If E is present and has a .keys() method, then does: for k in E.keys(): D[k] = E[k] If E is present and lacks a .keys() method, then does: for k, v in E: D[k] = v In either case, this is followed by: for k in F: D[k] = F[k]

Create a new collection with keying provided by keyfunc.

keyfunc may be any callable that takes an object and returns an object for use as a dictionary key.

The keyfunc will be called every time the ORM needs to add a member by value-only (such as when loading instances from the database) or remove a member. The usual cautions about dictionary keying apply- keyfunc(object) should return the same output for the life of the collection. Keying based on mutable properties can result in unreachable instances “lost” in the collection.

Remove all items from the dict.

If the key is not found, return the default if given; otherwise, raise a KeyError.

Remove and return a (key, value) pair as a 2-tuple.

Pairs are returned in LIFO (last-in, first-out) order. Raises KeyError if the dict is empty.

Remove an item by value, consulting the keyfunc for the key.

Add an item by value, consulting the keyfunc for the key.

Insert key with a value of default if key is not in the dictionary.

Return the value for key if key is in the dictionary, else default.

If E is present and has a .keys() method, then does: for k in E.keys(): D[k] = E[k] If E is present and lacks a .keys() method, then does: for k, v in E: D[k] = v In either case, this is followed by: for k in F: D[k] = F[k]

Base for ORM mapped dictionary classes.

Extends the dict type with additional methods needed by SQLAlchemy ORM collection classes. Use of KeyFuncDict is most directly by using the attribute_keyed_dict() or column_keyed_dict() class factories. KeyFuncDict may also serve as the base for user-defined custom dictionary classes.

Changed in version 2.0: Renamed MappedCollection to KeyFuncDict.

attribute_keyed_dict()

Dictionary Collections

Custom Collection Implementations

bulk_replace(values, existing_adapter, new_adapter[, initiator])

Load a new collection, firing events based on prior like membership.

Decorators for entity collection classes.

Return a callable object that fetches the given attribute(s) from its operand. After f = attrgetter(‘name’), the call f(r) returns r.name. After g = attrgetter(‘name’, ‘date’), the call g(r) returns (r.name, r.date). After h = attrgetter(‘name.first’, ‘name.last’), the call h(r) returns (r.name.first, r.name.last).

Bridges between the ORM and arbitrary Python collections.

An instrumented version of the built-in dict.

An instrumented version of the built-in list.

An instrumented version of the built-in set.

prepare_instrumentation(factory)

Prepare a callable for future use as a collection class factory.

Load a new collection, firing events based on prior like membership.

Appends instances in values onto the new_adapter. Events will be fired for any instance not present in the existing_adapter. Any instances in existing_adapter not present in values will have remove events fired upon them.

values¶ – An iterable of collection member instances

existing_adapter¶ – A CollectionAdapter of instances to be replaced

new_adapter¶ – An empty CollectionAdapter to load with values

Decorators for entity collection classes.

The decorators fall into two groups: annotations and interception recipes.

The annotating decorators (appender, remover, iterator, converter, internally_instrumented) indicate the method’s purpose and take no arguments. They are not written with parens:

The recipe decorators all require parens, even those that take no arguments:

Mark the method as adding an entity to the collection.

Tag the method as the collection appender.

Tag the method as the collection converter.

internally_instrumented()

Tag the method as instrumented.

Tag the method as the collection remover.

Tag the method as the collection remover.

Mark the method as removing an entity in the collection.

Mark the method as removing an entity in the collection.

Mark the method as replacing an entity in the collection.

Mark the method as adding an entity to the collection.

Adds “add to collection” handling to the method. The decorator argument indicates which method argument holds the SQLAlchemy-relevant value. Arguments can be specified positionally (i.e. integer) or by name:

Tag the method as the collection appender.

The appender method is called with one positional argument: the value to append. The method will be automatically decorated with ‘adds(1)’ if not already decorated:

If the value to append is not allowed in the collection, you may raise an exception. Something to remember is that the appender will be called for each object mapped by a database query. If the database contains rows that violate your collection semantics, you will need to get creative to fix the problem, as access via the collection will not work.

If the appender method is internally instrumented, you must also receive the keyword argument ‘_sa_initiator’ and ensure its promulgation to collection events.

Tag the method as the collection converter.

Deprecated since version 1.3: The collection.converter() handler is deprecated and will be removed in a future release. Please refer to the bulk_replace listener interface in conjunction with the listen() function.

This optional method will be called when a collection is being replaced entirely, as in:

The converter method will receive the object being assigned and should return an iterable of values suitable for use by the appender method. A converter must not assign values or mutate the collection, its sole job is to adapt the value the user provides into an iterable of values for the ORM’s use.

The default converter implementation will use duck-typing to do the conversion. A dict-like collection will be convert into an iterable of dictionary values, and other types will simply be iterated:

If the duck-typing of the object does not match the type of this collection, a TypeError is raised.

Supply an implementation of this method if you want to expand the range of possible types that can be assigned in bulk or perform validation on the values about to be assigned.

Tag the method as instrumented.

This tag will prevent any decoration from being applied to the method. Use this if you are orchestrating your own calls to collection_adapter() in one of the basic SQLAlchemy interface methods, or to prevent an automatic ABC method decoration from wrapping your implementation:

Tag the method as the collection remover.

The iterator method is called with no arguments. It is expected to return an iterator over all collection members:

Tag the method as the collection remover.

The remover method is called with one positional argument: the value to remove. The method will be automatically decorated with removes_return() if not already decorated:

If the value to remove is not present in the collection, you may raise an exception or return None to ignore the error.

If the remove method is internally instrumented, you must also receive the keyword argument ‘_sa_initiator’ and ensure its promulgation to collection events.

Mark the method as removing an entity in the collection.

Adds “remove from collection” handling to the method. The decorator argument indicates which method argument holds the SQLAlchemy-relevant value to be removed. Arguments can be specified positionally (i.e. integer) or by name:

For methods where the value to remove is not known at call-time, use collection.removes_return.

Mark the method as removing an entity in the collection.

Adds “remove from collection” handling to the method. The return value of the method, if any, is considered the value to remove. The method arguments are not inspected:

For methods where the value to remove is known at call-time, use collection.remove.

Mark the method as replacing an entity in the collection.

Adds “add to collection” and “remove from collection” handling to the method. The decorator argument indicates which method argument holds the SQLAlchemy-relevant value to be added, and return value, if any will be considered the value to remove.

Arguments can be specified positionally (i.e. integer) or by name:

Return a callable object that fetches the given attribute(s) from its operand. After f = attrgetter(‘name’), the call f(r) returns r.name. After g = attrgetter(‘name’, ‘date’), the call g(r) returns (r.name, r.date). After h = attrgetter(‘name.first’, ‘name.last’), the call h(r) returns (r.name.first, r.name.last).

Bridges between the ORM and arbitrary Python collections.

Proxies base-level collection operations (append, remove, iterate) to the underlying Python collection, and emits add/remove events for entities entering or leaving the collection.

The ORM uses CollectionAdapter exclusively for interaction with entity collections.

inherits from builtins.dict, typing.Generic

An instrumented version of the built-in dict.

inherits from builtins.list, typing.Generic

An instrumented version of the built-in list.

inherits from builtins.set, typing.Generic

An instrumented version of the built-in set.

Prepare a callable for future use as a collection class factory.

Given a collection class factory (either a type or no-arg callable), return another factory that will produce compatible instances when called.

This function is responsible for converting collection_class=list into the run-time behavior of collection_class=InstrumentedList.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from sqlalchemy import ForeignKey

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Parent(Base):
    __tablename__ = "parent"

    parent_id: Mapped[int] = mapped_column(primary_key=True)

    # use a list
    children: Mapped[List["Child"]] = relationship()


class Child(Base):
    __tablename__ = "child"

    child_id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent.id"))
```

Example 2 (python):
```python
from typing import Set
from sqlalchemy import ForeignKey

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Parent(Base):
    __tablename__ = "parent"

    parent_id: Mapped[int] = mapped_column(primary_key=True)

    # use a set
    children: Mapped[Set["Child"]] = relationship()


class Child(Base):
    __tablename__ = "child"

    child_id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent.id"))
```

Example 3 (python):
```python
from typing import List


class Parent(Base):
    __tablename__ = "parent"

    parent_id: Mapped[int] = mapped_column(primary_key=True)

    # use a List, Python 3.8 and earlier
    children: Mapped[List["Child"]] = relationship()
```

Example 4 (typescript):
```typescript
# non-annotated mapping


class Parent(Base):
    __tablename__ = "parent"

    parent_id = mapped_column(Integer, primary_key=True)

    children = relationship("Child", collection_class=set)


class Child(Base):
    __tablename__ = "child"

    child_id = mapped_column(Integer, primary_key=True)
    parent_id = mapped_column(ForeignKey("parent.id"))
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/relationships.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Relationship Configuration¶

Home | Download this Documentation

Home | Download this Documentation

This section describes the relationship() function and in depth discussion of its usage. For an introduction to relationships, start with Working with ORM Related Objects in the SQLAlchemy Unified Tutorial.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/join_conditions.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Configuring how Relationship Joins¶
- Handling Multiple Join Paths¶
- Specifying Alternate Join Conditions¶
- Creating Custom Foreign Conditions¶
- Using custom operators in join conditions¶
- Custom operators based on SQL functions¶

Home | Download this Documentation

Home | Download this Documentation

relationship() will normally create a join between two tables by examining the foreign key relationship between the two tables to determine which columns should be compared. There are a variety of situations where this behavior needs to be customized.

One of the most common situations to deal with is when there are more than one foreign key path between two tables.

Consider a Customer class that contains two foreign keys to an Address class:

The above mapping, when we attempt to use it, will produce the error:

The above message is pretty long. There are many potential messages that relationship() can return, which have been carefully tailored to detect a variety of common configurational issues; most will suggest the additional configuration that’s needed to resolve the ambiguity or other missing information.

In this case, the message wants us to qualify each relationship() by instructing for each one which foreign key column should be considered, and the appropriate form is as follows:

Above, we specify the foreign_keys argument, which is a Column or list of Column objects which indicate those columns to be considered “foreign”, or in other words, the columns that contain a value referring to a parent table. Loading the Customer.billing_address relationship from a Customer object will use the value present in billing_address_id in order to identify the row in Address to be loaded; similarly, shipping_address_id is used for the shipping_address relationship. The linkage of the two columns also plays a role during persistence; the newly generated primary key of a just-inserted Address object will be copied into the appropriate foreign key column of an associated Customer object during a flush.

When specifying foreign_keys with Declarative, we can also use string names to specify, however it is important that if using a list, the list is part of the string:

In this specific example, the list is not necessary in any case as there’s only one Column we need:

When passed as a Python-evaluable string, the relationship.foreign_keys argument is interpreted using Python’s eval() function. DO NOT PASS UNTRUSTED INPUT TO THIS STRING. See Evaluation of relationship arguments for details on declarative evaluation of relationship() arguments.

The default behavior of relationship() when constructing a join is that it equates the value of primary key columns on one side to that of foreign-key-referring columns on the other. We can change this criterion to be anything we’d like using the relationship.primaryjoin argument, as well as the relationship.secondaryjoin argument in the case when a “secondary” table is used.

In the example below, using the User class as well as an Address class which stores a street address, we create a relationship boston_addresses which will only load those Address objects which specify a city of “Boston”:

Within this string SQL expression, we made use of the and_() conjunction construct to establish two distinct predicates for the join condition - joining both the User.id and Address.user_id columns to each other, as well as limiting rows in Address to just city='Boston'. When using Declarative, rudimentary SQL functions like and_() are automatically available in the evaluated namespace of a string relationship() argument.

When passed as a Python-evaluable string, the relationship.primaryjoin argument is interpreted using Python’s eval() function. DO NOT PASS UNTRUSTED INPUT TO THIS STRING. See Evaluation of relationship arguments for details on declarative evaluation of relationship() arguments.

The custom criteria we use in a relationship.primaryjoin is generally only significant when SQLAlchemy is rendering SQL in order to load or represent this relationship. That is, it’s used in the SQL statement that’s emitted in order to perform a per-attribute lazy load, or when a join is constructed at query time, such as via Select.join(), or via the eager “joined” or “subquery” styles of loading. When in-memory objects are being manipulated, we can place any Address object we’d like into the boston_addresses collection, regardless of what the value of the .city attribute is. The objects will remain present in the collection until the attribute is expired and re-loaded from the database where the criterion is applied. When a flush occurs, the objects inside of boston_addresses will be flushed unconditionally, assigning value of the primary key user.id column onto the foreign-key-holding address.user_id column for each row. The city criteria has no effect here, as the flush process only cares about synchronizing primary key values into referencing foreign key values.

Another element of the primary join condition is how those columns considered “foreign” are determined. Usually, some subset of Column objects will specify ForeignKey, or otherwise be part of a ForeignKeyConstraint that’s relevant to the join condition. relationship() looks to this foreign key status as it decides how it should load and persist data for this relationship. However, the relationship.primaryjoin argument can be used to create a join condition that doesn’t involve any “schema” level foreign keys. We can combine relationship.primaryjoin along with relationship.foreign_keys and relationship.remote_side explicitly in order to establish such a join.

Below, a class HostEntry joins to itself, equating the string content column to the ip_address column, which is a PostgreSQL type called INET. We need to use cast() in order to cast one side of the join to the type of the other:

The above relationship will produce a join like:

An alternative syntax to the above is to use the foreign() and remote() annotations, inline within the relationship.primaryjoin expression. This syntax represents the annotations that relationship() normally applies by itself to the join condition given the relationship.foreign_keys and relationship.remote_side arguments. These functions may be more succinct when an explicit join condition is present, and additionally serve to mark exactly the column that is “foreign” or “remote” independent of whether that column is stated multiple times or within complex SQL expressions:

Another use case for relationships is the use of custom operators, such as PostgreSQL’s “is contained within” << operator when joining with types such as INET and CIDR. For custom boolean operators we use the Operators.bool_op() function:

A comparison like the above may be used directly with relationship.primaryjoin when constructing a relationship():

Above, a query such as:

A variant to the use case for Operators.op.is_comparison is when we aren’t using an operator, but a SQL function. The typical example of this use case is the PostgreSQL PostGIS functions however any SQL function on any database that resolves to a binary condition may apply. To suit this use case, the FunctionElement.as_comparison() method can modify any SQL function, such as those invoked from the func namespace, to indicate to the ORM that the function produces a comparison of two expressions. The below example illustrates this with the Geoalchemy2 library:

Above, the FunctionElement.as_comparison() indicates that the func.ST_Contains() SQL function is comparing the Polygon.geom and Point.geom expressions. The foreign() annotation additionally notes which column takes on the “foreign key” role in this particular relationship.

Added in version 1.3: Added FunctionElement.as_comparison().

A rare scenario can arise when composite foreign keys are used, such that a single column may be the subject of more than one column referred to via foreign key constraint.

Consider an (admittedly complex) mapping such as the Magazine object, referred to both by the Writer object and the Article object using a composite primary key scheme that includes magazine_id for both; then to make Article refer to Writer as well, Article.magazine_id is involved in two separate relationships; Article.magazine and Article.writer:

When the above mapping is configured, we will see this warning emitted:

What this refers to originates from the fact that Article.magazine_id is the subject of two different foreign key constraints; it refers to Magazine.id directly as a source column, but also refers to Writer.magazine_id as a source column in the context of the composite key to Writer.

When objects are added to an ORM Session using Session.add(), the ORM flush process takes on the task of reconciling object references that correspond to relationship() configurations and delivering this state to the database using INSERT/UPDATE/DELETE statements. In this specific example, if we associate an Article with a particular Magazine, but then associate the Article with a Writer that’s associated with a different Magazine, this flush process will overwrite Article.magazine_id non-deterministically, silently changing which magazine to which we refer; it may also attempt to place NULL into this column if we de-associate a Writer from an Article. The warning lets us know that this scenario may occur during ORM flush sequences.

To solve this, we need to break out the behavior of Article to include all three of the following features:

Article first and foremost writes to Article.magazine_id based on data persisted in the Article.magazine relationship only, that is a value copied from Magazine.id.

Article can write to Article.writer_id on behalf of data persisted in the Article.writer relationship, but only the Writer.id column; the Writer.magazine_id column should not be written into Article.magazine_id as it ultimately is sourced from Magazine.id.

Article takes Article.magazine_id into account when loading Article.writer, even though it doesn’t write to it on behalf of this relationship.

To get just #1 and #2, we could specify only Article.writer_id as the “foreign keys” for Article.writer:

However, this has the effect of Article.writer not taking Article.magazine_id into account when querying against Writer:

Therefore, to get at all of #1, #2, and #3, we express the join condition as well as which columns to be written by combining relationship.primaryjoin fully, along with either the relationship.foreign_keys argument, or more succinctly by annotating with foreign():

this section details an experimental feature.

Using custom expressions means we can produce unorthodox join conditions that don’t obey the usual primary/foreign key model. One such example is the materialized path pattern, where we compare strings for overlapping path tokens in order to produce a tree structure.

Through careful use of foreign() and remote(), we can build a relationship that effectively produces a rudimentary materialized path system. Essentially, when foreign() and remote() are on the same side of the comparison expression, the relationship is considered to be “one to many”; when they are on different sides, the relationship is considered to be “many to one”. For the comparison we’ll use here, we’ll be dealing with collections so we keep things configured as “one to many”:

Above, if given an Element object with a path attribute of "/foo/bar2", we seek for a load of Element.descendants to look like:

This section documents a two-table variant of the “adjacency list” pattern, which is documented at Adjacency List Relationships. Be sure to review the self-referential querying patterns in subsections Self-Referential Query Strategies and Configuring Self-Referential Eager Loading which apply equally well to the mapping pattern discussed here.

Many to many relationships can be customized by one or both of relationship.primaryjoin and relationship.secondaryjoin - the latter is significant for a relationship that specifies a many-to-many reference using the relationship.secondary argument. A common situation which involves the usage of relationship.primaryjoin and relationship.secondaryjoin is when establishing a many-to-many relationship from a class to itself, as shown below:

Where above, SQLAlchemy can’t know automatically which columns should connect to which for the right_nodes and left_nodes relationships. The relationship.primaryjoin and relationship.secondaryjoin arguments establish how we’d like to join to the association table. In the Declarative form above, as we are declaring these conditions within the Python block that corresponds to the Node class, the id variable is available directly as the Column object we wish to join with.

Alternatively, we can define the relationship.primaryjoin and relationship.secondaryjoin arguments using strings, which is suitable in the case that our configuration does not have either the Node.id column object available yet or the node_to_node table perhaps isn’t yet available. When referring to a plain Table object in a declarative string, we use the string name of the table as it is present in the MetaData:

When passed as a Python-evaluable string, the relationship.primaryjoin and relationship.secondaryjoin arguments are interpreted using Python’s eval() function. DO NOT PASS UNTRUSTED INPUT TO THESE STRINGS. See Evaluation of relationship arguments for details on declarative evaluation of relationship() arguments.

A classical mapping situation here is similar, where node_to_node can be joined to node.c.id:

Note that in both examples, the relationship.backref keyword specifies a left_nodes backref - when relationship() creates the second relationship in the reverse direction, it’s smart enough to reverse the relationship.primaryjoin and relationship.secondaryjoin arguments.

Adjacency List Relationships - single table version

Self-Referential Query Strategies - tips on querying with self-referential mappings

Configuring Self-Referential Eager Loading - tips on eager loading with self- referential mapping

This section features far edge cases that are somewhat supported by SQLAlchemy, however it is recommended to solve problems like these in simpler ways whenever possible, by using reasonable relational layouts and / or in-Python attributes.

Sometimes, when one seeks to build a relationship() between two tables there is a need for more than just two or three tables to be involved in order to join them. This is an area of relationship() where one seeks to push the boundaries of what’s possible, and often the ultimate solution to many of these exotic use cases needs to be hammered out on the SQLAlchemy mailing list.

In more recent versions of SQLAlchemy, the relationship.secondary parameter can be used in some of these cases in order to provide a composite target consisting of multiple tables. Below is an example of such a join condition (requires version 0.9.2 at least to function as is):

In the above example, we provide all three of relationship.secondary, relationship.primaryjoin, and relationship.secondaryjoin, in the declarative style referring to the named tables a, b, c, d directly. A query from A to D looks like:

In the above example, we take advantage of being able to stuff multiple tables into a “secondary” container, so that we can join across many tables while still keeping things “simple” for relationship(), in that there’s just “one” table on both the “left” and the “right” side; the complexity is kept within the middle.

A relationship like the above is typically marked as viewonly=True, using relationship.viewonly, and should be considered as read-only. While there are sometimes ways to make relationships like the above writable, this is generally complicated and error prone.

Notes on using the viewonly relationship parameter

In the previous section, we illustrated a technique where we used relationship.secondary in order to place additional tables within a join condition. There is one complex join case where even this technique is not sufficient; when we seek to join from A to B, making use of any number of C, D, etc. in between, however there are also join conditions between A and B directly. In this case, the join from A to B may be difficult to express with just a complex relationship.primaryjoin condition, as the intermediary tables may need special handling, and it is also not expressible with a relationship.secondary object, since the A->secondary->B pattern does not support any references between A and B directly. When this extremely advanced case arises, we can resort to creating a second mapping as a target for the relationship. This is where we use AliasedClass in order to make a mapping to a class that includes all the additional tables we need for this join. In order to produce this mapper as an “alternative” mapping for our class, we use the aliased() function to produce the new construct, then use relationship() against the object as though it were a plain mapped class.

Below illustrates a relationship() with a simple join from A to B, however the primaryjoin condition is augmented with two additional entities C and D, which also must have rows that line up with the rows in both A and B simultaneously:

With the above mapping, a simple join looks like:

The creation of the aliased() construct against a mapped class forces the configure_mappers() step to proceed, which will resolve all current classes and their relationships. This may be problematic if unrelated mapped classes needed by the current mappings have not yet been declared, or if the configuration of the relationship itself needs access to as-yet undeclared classes. Additionally, SQLAlchemy’s Declarative pattern works with Python typing most effectively when relationships are declared up front.

To organize the construction of the relationship to work with these issues, a configure level event hook like MapperEvents.before_mapper_configured() may be used, which will invoke the configuration code only when all mappings are ready for configuration:

Above, the function _configure_ab_relationship() will be invoked only when a fully configured version of A is requested, at which point the classes B, D and C would be available.

For an approach that integrates with inline typing, a similar technique can be used to effectively generate a “singleton” creation pattern for the aliased class where it is late-initialized as a global variable, which can then be used in the relationship inline:

In the previous example, the A.b relationship refers to the B_viacd entity as the target, and not the B class directly. To add additional criteria involving the A.b relationship, it’s typically necessary to reference the B_viacd directly rather than using B, especially in a case where the target entity of A.b is to be transformed into an alias or a subquery. Below illustrates the same relationship using a subquery, rather than a join:

A query using the above A.b relationship will render a subquery:

If we want to add additional criteria based on the A.b join, we must do so in terms of B_viacd_subquery rather than B directly:

Another interesting use case for relationships to AliasedClass objects are situations where the relationship needs to join to a specialized SELECT of any form. One scenario is when the use of a window function is desired, such as to limit how many rows should be returned for a relationship. The example below illustrates a non-primary mapper relationship that will load the first ten items for each collection:

We can use the above partitioned_bs relationship with most of the loader strategies, such as selectinload():

Where above, the “selectinload” query looks like:

Above, for each matching primary key in “a”, we will get the first ten “bs” as ordered by “b.id”. By partitioning on “a_id” we ensure that each “row number” is local to the parent “a_id”.

Such a mapping would ordinarily also include a “plain” relationship from “A” to “B”, for persistence operations as well as when the full set of “B” objects per “A” is desired.

Very ambitious custom join conditions may fail to be directly persistable, and in some cases may not even load correctly. To remove the persistence part of the equation, use the flag relationship.viewonly on the relationship(), which establishes it as a read-only attribute (data written to the collection will be ignored on flush()). However, in extreme cases, consider using a regular Python property in conjunction with Query as follows:

In other cases, the descriptor can be built to make use of existing in-Python data. See the section on Using Descriptors and Hybrids for more general discussion of special Python attributes.

Using Descriptors and Hybrids

The relationship.viewonly parameter when applied to a relationship() construct indicates that this relationship() will not take part in any ORM unit of work operations, and additionally that the attribute does not expect to participate within in-Python mutations of its represented collection. This means that while the viewonly relationship may refer to a mutable Python collection like a list or set, making changes to that list or set as present on a mapped instance will have no effect on the ORM flush process.

To explore this scenario consider this mapping:

The following sections will note different aspects of this configuration.

The above mapping targets the User.current_week_tasks viewonly relationship as the backref target of the Task.user attribute. This is not currently flagged by SQLAlchemy’s ORM configuration process, however is a configuration error. Changing the .user attribute on a Task will not affect the .current_week_tasks attribute:

There is another parameter called relationship.sync_backrefs which can be turned on here to allow .current_week_tasks to be mutated in this case, however this is not considered to be a best practice with a viewonly relationship, which instead should not be relied upon for in-Python mutations.

In this mapping, backrefs can be configured between User.all_tasks and Task.user, as these are both not viewonly and will synchronize normally.

Beyond the issue of backref mutations being disabled for viewonly relationships, plain changes to the User.all_tasks collection in Python are also not reflected in the User.current_week_tasks collection until changes have been flushed to the database.

Overall, for a use case where a custom collection should respond immediately to in-Python mutations, the viewonly relationship is generally not appropriate. A better approach is to use the Hybrid Attributes feature of SQLAlchemy, or for instance-only cases to use a Python @property, where a user-defined collection that is generated in terms of the current Python instance can be implemented. To change our example to work this way, we repair the relationship.back_populates parameter on Task.user to reference User.all_tasks, and then illustrate a simple @property that will deliver results in terms of the immediate User.all_tasks collection:

Using an in-Python collection calculated on the fly each time, we are guaranteed to have the correct answer at all times, without the need to use a database at all:

Continuing with the original viewonly attribute, if we do in fact make changes to the User.all_tasks collection on a persistent object, the viewonly collection can only show the net result of this change after two things occur. The first is that the change to User.all_tasks is flushed, so that the new data is available in the database, at least within the scope of the local transaction. The second is that the User.current_week_tasks attribute is expired and reloaded via a new SQL query to the database.

To support this requirement, the simplest flow to use is one where the viewonly relationship is consumed only in operations that are primarily read only to start with. Such as below, if we retrieve a User fresh from the database, the collection will be current:

When we make modifications to u1.all_tasks, if we want to see these changes reflected in the u1.current_week_tasks viewonly relationship, these changes need to be flushed and the u1.current_week_tasks attribute needs to be expired, so that it will lazy load on next access. The simplest approach to this is to use Session.commit(), keeping the Session.expire_on_commit parameter set at its default of True:

Above, the call to Session.commit() flushed the changes to u1.all_tasks to the database, then expired all objects, so that when we accessed u1.current_week_tasks, a :term:` lazy load` occurred which fetched the contents for this attribute freshly from the database.

To intercept operations without actually committing the transaction, the attribute needs to be explicitly expired first. A simplistic way to do this is to just call it directly. In the example below, Session.flush() sends pending changes to the database, then Session.expire() is used to expire the u1.current_week_tasks collection so that it re-fetches on next access:

We can in fact skip the call to Session.flush(), assuming a Session that keeps Session.autoflush at its default value of True, as the expired current_week_tasks attribute will trigger autoflush when accessed after expiration:

Continuing with the above approach to something more elaborate, we can apply the expiration programmatically when the related User.all_tasks collection changes, using event hooks. This an advanced technique, where simpler architectures like @property or sticking to read-only use cases should be examined first. In our simple example, this would be configured as:

With the above hooks, mutation operations are intercepted and result in the User.current_week_tasks collection to be expired automatically:

The AttributeEvents event hooks used above are also triggered by backref mutations, so with the above hooks a change to Task.user is also intercepted:

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customer"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)

    billing_address_id = mapped_column(Integer, ForeignKey("address.id"))
    shipping_address_id = mapped_column(Integer, ForeignKey("address.id"))

    billing_address = relationship("Address")
    shipping_address = relationship("Address")


class Address(Base):
    __tablename__ = "address"
    id = mapped_column(Integer, primary_key=True)
    street = mapped_column(String)
    city = mapped_column(String)
    state = mapped_column(String)
    zip = mapped_column(String)
```

Example 2 (sql):
```sql
sqlalchemy.exc.AmbiguousForeignKeysError: Could not determine join
condition between parent/child tables on relationship
Customer.billing_address - there are multiple foreign key
paths linking the tables.  Specify the 'foreign_keys' argument,
providing a list of those columns which should be
counted as containing a foreign key reference to the parent table.
```

Example 3 (typescript):
```typescript
class Customer(Base):
    __tablename__ = "customer"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)

    billing_address_id = mapped_column(Integer, ForeignKey("address.id"))
    shipping_address_id = mapped_column(Integer, ForeignKey("address.id"))

    billing_address = relationship("Address", foreign_keys=[billing_address_id])
    shipping_address = relationship("Address", foreign_keys=[shipping_address_id])
```

Example 4 (unknown):
```unknown
billing_address = relationship("Address", foreign_keys="[Customer.billing_address_id]")
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/relationship_api.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Relationships API¶

Home | Download this Documentation

Home | Download this Documentation

backref(name, **kwargs)

When using the relationship.backref parameter, provides specific parameters to be used when the new relationship() is generated.

dynamic_loader([argument], **kw)

Construct a dynamically-loading mapper property.

Annotate a portion of a primaryjoin expression with a ‘foreign’ annotation.

relationship([argument, secondary], *, [uselist, collection_class, primaryjoin, secondaryjoin, back_populates, order_by, backref, overlaps, post_update, cascade, viewonly, init, repr, default, default_factory, compare, kw_only, hash, lazy, passive_deletes, passive_updates, active_history, enable_typechecks, foreign_keys, remote_side, join_depth, comparator_factory, single_parent, innerjoin, distinct_target_key, load_on_pending, query_class, info, omit_join, sync_backref, dataclass_metadata], **kw)

Provide a relationship between two mapped classes.

Annotate a portion of a primaryjoin expression with a ‘remote’ annotation.

Provide a relationship between two mapped classes.

This corresponds to a parent-child or associative table relationship. The constructed class is an instance of Relationship.

Working with ORM Related Objects - tutorial introduction to relationship() in the SQLAlchemy Unified Tutorial

Relationship Configuration - narrative documentation

This parameter refers to the class that is to be related. It accepts several forms, including a direct reference to the target class itself, the Mapper instance for the target class, a Python callable / lambda that will return a reference to the class or Mapper when called, and finally a string name for the class, which will be resolved from the registry in use in order to locate the class, e.g.:

The relationship.argument may also be omitted from the relationship() construct entirely, and instead placed inside a Mapped annotation on the left side, which should include a Python collection type if the relationship is expected to be a collection, such as:

Or for a many-to-one or one-to-one relationship:

Defining Mapped Properties with Declarative - further detail on relationship configuration when using Declarative.

For a many-to-many relationship, specifies the intermediary table, and is typically an instance of Table. In less common circumstances, the argument may also be specified as an Alias construct, or even a Join construct.

relationship.secondary may also be passed as a callable function which is evaluated at mapper initialization time. When using Declarative, it may also be a string argument noting the name of a Table that is present in the MetaData collection associated with the parent-mapped Table.

When passed as a Python-evaluable string, the argument is interpreted using Python’s eval() function. DO NOT PASS UNTRUSTED INPUT TO THIS STRING. See Evaluation of relationship arguments for details on declarative evaluation of relationship() arguments.

The relationship.secondary keyword argument is typically applied in the case where the intermediary Table is not otherwise expressed in any direct class mapping. If the “secondary” table is also explicitly mapped elsewhere (e.g. as in Association Object), one should consider applying the relationship.viewonly flag so that this relationship() is not used for persistence operations which may conflict with those of the association object pattern.

Many To Many - Reference example of “many to many”.

Self-Referential Many-to-Many Relationship - Specifics on using many-to-many in a self-referential case.

Configuring Many-to-Many Relationships - Additional options when using Declarative.

Association Object - an alternative to relationship.secondary when composing association table relationships, allowing additional attributes to be specified on the association table.

Composite “Secondary” Joins - a lesser-used pattern which in some cases can enable complex relationship() SQL conditions to be used.

active_history=False¶ – When True, indicates that the “previous” value for a many-to-one reference should be loaded when replaced, if not already loaded. Normally, history tracking logic for simple many-to-ones only needs to be aware of the “new” value in order to perform a flush. This flag is available for applications that make use of get_history() which also need to know the “previous” value of the attribute.

A reference to a string relationship name, or a backref() construct, which will be used to automatically generate a new relationship() on the related class, which then refers to this one using a bi-directional relationship.back_populates configuration.

In modern Python, explicit use of relationship() with relationship.back_populates should be preferred, as it is more robust in terms of mapper configuration as well as more conceptually straightforward. It also integrates with new PEP 484 typing features introduced in SQLAlchemy 2.0 which is not possible with dynamically generated attributes.

Using the legacy ‘backref’ relationship parameter - notes on using relationship.backref

Working with ORM Related Objects - in the SQLAlchemy Unified Tutorial, presents an overview of bi-directional relationship configuration and behaviors using relationship.back_populates

backref() - allows control over relationship() configuration when using relationship.backref.

Indicates the name of a relationship() on the related class that will be synchronized with this one. It is usually expected that the relationship() on the related class also refer to this one. This allows objects on both sides of each relationship() to synchronize in-Python state changes and also provides directives to the unit of work flush process how changes along these relationships should be persisted.

Working with ORM Related Objects - in the SQLAlchemy Unified Tutorial, presents an overview of bi-directional relationship configuration and behaviors.

Basic Relationship Patterns - includes many examples of relationship.back_populates.

relationship.backref - legacy form which allows more succinct configuration, but does not support explicit typing

A string name or comma-delimited set of names of other relationships on either this mapper, a descendant mapper, or a target mapper with which this relationship may write to the same foreign keys upon persistence. The only effect this has is to eliminate the warning that this relationship will conflict with another upon persistence. This is used for such relationships that are truly capable of conflicting with each other on write, but the application will ensure that no such conflicts occur.

Added in version 1.4.

relationship X will copy column Q to column P, which conflicts with relationship(s): ‘Y’ - usage example

A comma-separated list of cascade rules which determines how Session operations should be “cascaded” from parent to child. This defaults to False, which means the default cascade should be used - this default cascade is "save-update, merge".

The available cascades are save-update, merge, expunge, delete, delete-orphan, and refresh-expire. An additional option, all indicates shorthand for "save-update, merge, refresh-expire, expunge, delete", and is often used as in "all, delete-orphan" to indicate that related objects should follow along with the parent object in all cases, and be deleted when de-associated.

Cascades - Full detail on each of the available cascade options.

cascade_backrefs=False¶ –

Legacy; this flag is always False.

Changed in version 2.0: “cascade_backrefs” functionality has been removed.

A class or callable that returns a new list-holding object. will be used in place of a plain list for storing elements.

Customizing Collection Access - Introductory documentation and examples.

comparator_factory¶ –

A class which extends Comparator which provides custom SQL clause generation for comparison operations.

PropComparator - some detail on redefining comparators at this level.

Operator Customization - Brief intro to this feature.

distinct_target_key=None¶ –

Indicate if a “subquery” eager load should apply the DISTINCT keyword to the innermost SELECT statement. When left as None, the DISTINCT keyword will be applied in those cases when the target columns do not comprise the full primary key of the target table. When set to True, the DISTINCT keyword is applied to the innermost SELECT unconditionally.

It may be desirable to set this flag to False when the DISTINCT is reducing performance of the innermost subquery beyond that of what duplicate innermost rows may be causing.

Relationship Loading Techniques - includes an introduction to subquery eager loading.

doc¶ – Docstring which will be applied to the resulting descriptor.

A list of columns which are to be used as “foreign key” columns, or columns which refer to the value in a remote column, within the context of this relationship() object’s relationship.primaryjoin condition. That is, if the relationship.primaryjoin condition of this relationship() is a.id == b.a_id, and the values in b.a_id are required to be present in a.id, then the “foreign key” column of this relationship() is b.a_id.

In normal cases, the relationship.foreign_keys parameter is not required. relationship() will automatically determine which columns in the relationship.primaryjoin condition are to be considered “foreign key” columns based on those Column objects that specify ForeignKey, or are otherwise listed as referencing columns in a ForeignKeyConstraint construct. relationship.foreign_keys is only needed when:

There is more than one way to construct a join from the local table to the remote table, as there are multiple foreign key references present. Setting foreign_keys will limit the relationship() to consider just those columns specified here as “foreign”.

The Table being mapped does not actually have ForeignKey or ForeignKeyConstraint constructs present, often because the table was reflected from a database that does not support foreign key reflection (MySQL MyISAM).

The relationship.primaryjoin argument is used to construct a non-standard join condition, which makes use of columns or expressions that do not normally refer to their “parent” column, such as a join condition expressed by a complex comparison using a SQL function.

The relationship() construct will raise informative error messages that suggest the use of the relationship.foreign_keys parameter when presented with an ambiguous condition. In typical cases, if relationship() doesn’t raise any exceptions, the relationship.foreign_keys parameter is usually not needed.

relationship.foreign_keys may also be passed as a callable function which is evaluated at mapper initialization time, and may be passed as a Python-evaluable string when using Declarative.

When passed as a Python-evaluable string, the argument is interpreted using Python’s eval() function. DO NOT PASS UNTRUSTED INPUT TO THIS STRING. See Evaluation of relationship arguments for details on declarative evaluation of relationship() arguments.

Handling Multiple Join Paths

Creating Custom Foreign Conditions

foreign() - allows direct annotation of the “foreign” columns within a relationship.primaryjoin condition.

info¶ – Optional data dictionary which will be populated into the MapperProperty.info attribute of this object.

When True, joined eager loads will use an inner join to join against related tables instead of an outer join. The purpose of this option is generally one of performance, as inner joins generally perform better than outer joins.

This flag can be set to True when the relationship references an object via many-to-one using local foreign keys that are not nullable, or when the reference is one-to-one or a collection that is guaranteed to have one or at least one entry.

The option supports the same “nested” and “unnested” options as that of joinedload.innerjoin. See that flag for details on nested / unnested behaviors.

joinedload.innerjoin - the option as specified by loader option, including detail on nesting behavior.

What Kind of Loading to Use ? - Discussion of some details of various loader options.

When non-None, an integer value indicating how many levels deep “eager” loaders should join on a self-referring or cyclical relationship. The number counts how many times the same Mapper shall be present in the loading condition along a particular join branch. When left at its default of None, eager loaders will stop chaining when they encounter a the same target mapper which is already higher up in the chain. This option applies both to joined- and subquery- eager loaders.

Configuring Self-Referential Eager Loading - Introductory documentation and examples.

specifies How the related items should be loaded. Default value is select. Values include:

select - items should be loaded lazily when the property is first accessed, using a separate SELECT statement, or identity map fetch for simple many-to-one references.

immediate - items should be loaded as the parents are loaded, using a separate SELECT statement, or identity map fetch for simple many-to-one references.

joined - items should be loaded “eagerly” in the same query as that of the parent, using a JOIN or LEFT OUTER JOIN. Whether the join is “outer” or not is determined by the relationship.innerjoin parameter.

subquery - items should be loaded “eagerly” as the parents are loaded, using one additional SQL statement, which issues a JOIN to a subquery of the original statement, for each collection requested.

selectin - items should be loaded “eagerly” as the parents are loaded, using one or more additional SQL statements, which issues a JOIN to the immediate parent object, specifying primary key identifiers using an IN clause.

noload - no loading should occur at any time. The related collection will remain empty. The noload strategy is not recommended for general use. For a general use “never load” approach, see Write Only Relationships

raise - lazy loading is disallowed; accessing the attribute, if its value were not already loaded via eager loading, will raise an InvalidRequestError. This strategy can be used when objects are to be detached from their attached Session after they are loaded.

raise_on_sql - lazy loading that emits SQL is disallowed; accessing the attribute, if its value were not already loaded via eager loading, will raise an InvalidRequestError, if the lazy load needs to emit SQL. If the lazy load can pull the related value from the identity map or determine that it should be None, the value is loaded. This strategy can be used when objects will remain associated with the attached Session, however additional SELECT statements should be blocked.

write_only - the attribute will be configured with a special “virtual collection” that may receive WriteOnlyCollection.add() and WriteOnlyCollection.remove() commands to add or remove individual objects, but will not under any circumstances load or iterate the full set of objects from the database directly. Instead, methods such as WriteOnlyCollection.select(), WriteOnlyCollection.insert(), WriteOnlyCollection.update() and WriteOnlyCollection.delete() are provided which generate SQL constructs that may be used to load and modify rows in bulk. Used for large collections that are never appropriate to load at once into memory.

The write_only loader style is configured automatically when the WriteOnlyMapped annotation is provided on the left hand side within a Declarative mapping. See the section Write Only Relationships for examples.

Added in version 2.0.

Write Only Relationships - in the ORM Querying Guide

dynamic - the attribute will return a pre-configured Query object for all read operations, onto which further filtering operations can be applied before iterating the results.

The dynamic loader style is configured automatically when the DynamicMapped annotation is provided on the left hand side within a Declarative mapping. See the section Dynamic Relationship Loaders for examples.

The “dynamic” lazy loader strategy is the legacy form of what is now the “write_only” strategy described in the section Write Only Relationships.

Dynamic Relationship Loaders - in the ORM Querying Guide

Write Only Relationships - more generally useful approach for large collections that should not fully load into memory

True - a synonym for ‘select’

False - a synonym for ‘joined’

None - a synonym for ‘noload’

Relationship Loading Techniques - Full documentation on relationship loader configuration in the ORM Querying Guide.

load_on_pending=False¶ –

Indicates loading behavior for transient or pending parent objects.

When set to True, causes the lazy-loader to issue a query for a parent object that is not persistent, meaning it has never been flushed. This may take effect for a pending object when autoflush is disabled, or for a transient object that has been “attached” to a Session but is not part of its pending collection.

The relationship.load_on_pending flag does not improve behavior when the ORM is used normally - object references should be constructed at the object level, not at the foreign key level, so that they are present in an ordinary way before a flush proceeds. This flag is not not intended for general use.

Session.enable_relationship_loading() - this method establishes “load on pending” behavior for the whole object, and also allows loading on objects that remain transient or detached.

Indicates the ordering that should be applied when loading these items. relationship.order_by is expected to refer to one of the Column objects to which the target class is mapped, or the attribute itself bound to the target class which refers to the column.

relationship.order_by may also be passed as a callable function which is evaluated at mapper initialization time, and may be passed as a Python-evaluable string when using Declarative.

When passed as a Python-evaluable string, the argument is interpreted using Python’s eval() function. DO NOT PASS UNTRUSTED INPUT TO THIS STRING. See Evaluation of relationship arguments for details on declarative evaluation of relationship() arguments.

passive_deletes=False¶ –

Indicates loading behavior during delete operations.

A value of True indicates that unloaded child items should not be loaded during a delete operation on the parent. Normally, when a parent item is deleted, all child items are loaded so that they can either be marked as deleted, or have their foreign key to the parent set to NULL. Marking this flag as True usually implies an ON DELETE <CASCADE|SET NULL> rule is in place which will handle updating/deleting child rows on the database side.

Additionally, setting the flag to the string value ‘all’ will disable the “nulling out” of the child foreign keys, when the parent object is deleted and there is no delete or delete-orphan cascade enabled. This is typically used when a triggering or error raise scenario is in place on the database side. Note that the foreign key attributes on in-session child objects will not be changed after a flush occurs so this is a very special use-case setting. Additionally, the “nulling out” will still occur if the child object is de-associated with the parent.

Using foreign key ON DELETE cascade with ORM relationships - Introductory documentation and examples.

passive_updates=True¶ –

Indicates the persistence behavior to take when a referenced primary key value changes in place, indicating that the referencing foreign key columns will also need their value changed.

When True, it is assumed that ON UPDATE CASCADE is configured on the foreign key in the database, and that the database will handle propagation of an UPDATE from a source column to dependent rows. When False, the SQLAlchemy relationship() construct will attempt to emit its own UPDATE statements to modify related targets. However note that SQLAlchemy cannot emit an UPDATE for more than one level of cascade. Also, setting this flag to False is not compatible in the case where the database is in fact enforcing referential integrity, unless those constraints are explicitly “deferred”, if the target backend supports it.

It is highly advised that an application which is employing mutable primary keys keeps passive_updates set to True, and instead uses the referential integrity features of the database itself in order to handle the change efficiently and fully.

Mutable Primary Keys / Update Cascades - Introductory documentation and examples.

mapper.passive_updates - a similar flag which takes effect for joined-table inheritance mappings.

This indicates that the relationship should be handled by a second UPDATE statement after an INSERT or before a DELETE. This flag is used to handle saving bi-directional dependencies between two individual rows (i.e. each row references the other), where it would otherwise be impossible to INSERT or DELETE both rows fully since one row exists before the other. Use this flag when a particular mapping arrangement will incur two rows that are dependent on each other, such as a table that has a one-to-many relationship to a set of child rows, and also has a column that references a single child row within that list (i.e. both tables contain a foreign key to each other). If a flush operation returns an error that a “cyclical dependency” was detected, this is a cue that you might want to use relationship.post_update to “break” the cycle.

Rows that point to themselves / Mutually Dependent Rows - Introductory documentation and examples.

A SQL expression that will be used as the primary join of the child object against the parent object, or in a many-to-many relationship the join of the parent object to the association table. By default, this value is computed based on the foreign key relationships of the parent and child tables (or association table).

relationship.primaryjoin may also be passed as a callable function which is evaluated at mapper initialization time, and may be passed as a Python-evaluable string when using Declarative.

When passed as a Python-evaluable string, the argument is interpreted using Python’s eval() function. DO NOT PASS UNTRUSTED INPUT TO THIS STRING. See Evaluation of relationship arguments for details on declarative evaluation of relationship() arguments.

Specifying Alternate Join Conditions

Used for self-referential relationships, indicates the column or list of columns that form the “remote side” of the relationship.

relationship.remote_side may also be passed as a callable function which is evaluated at mapper initialization time, and may be passed as a Python-evaluable string when using Declarative.

When passed as a Python-evaluable string, the argument is interpreted using Python’s eval() function. DO NOT PASS UNTRUSTED INPUT TO THIS STRING. See Evaluation of relationship arguments for details on declarative evaluation of relationship() arguments.

Adjacency List Relationships - in-depth explanation of how relationship.remote_side is used to configure self-referential relationships.

remote() - an annotation function that accomplishes the same purpose as relationship.remote_side, typically when a custom relationship.primaryjoin condition is used.

A Query subclass that will be used internally by the AppenderQuery returned by a “dynamic” relationship, that is, a relationship that specifies lazy="dynamic" or was otherwise constructed using the dynamic_loader() function.

Dynamic Relationship Loaders - Introduction to “dynamic” relationship loaders.

A SQL expression that will be used as the join of an association table to the child object. By default, this value is computed based on the foreign key relationships of the association and child tables.

relationship.secondaryjoin may also be passed as a callable function which is evaluated at mapper initialization time, and may be passed as a Python-evaluable string when using Declarative.

When passed as a Python-evaluable string, the argument is interpreted using Python’s eval() function. DO NOT PASS UNTRUSTED INPUT TO THIS STRING. See Evaluation of relationship arguments for details on declarative evaluation of relationship() arguments.

Specifying Alternate Join Conditions

When True, installs a validator which will prevent objects from being associated with more than one parent at a time. This is used for many-to-one or many-to-many relationships that should be treated either as one-to-one or one-to-many. Its usage is optional, except for relationship() constructs which are many-to-one or many-to-many and also specify the delete-orphan cascade option. The relationship() construct itself will raise an error instructing when this option is required.

Cascades - includes detail on when the relationship.single_parent flag may be appropriate.

A boolean that indicates if this property should be loaded as a list or a scalar. In most cases, this value is determined automatically by relationship() at mapper configuration time. When using explicit Mapped annotations, relationship.uselist may be derived from the whether or not the annotation within Mapped contains a collection class. Otherwise, relationship.uselist may be derived from the type and direction of the relationship - one to many forms a list, many to one forms a scalar, many to many is a list. If a scalar is desired where normally a list would be present, such as a bi-directional one-to-one relationship, use an appropriate Mapped annotation or set relationship.uselist to False.

The relationship.uselist flag is also available on an existing relationship() construct as a read-only attribute, which can be used to determine if this relationship() deals with collections or scalar attributes:

One To One - Introduction to the “one to one” relationship pattern, which is typically when an alternate setting for relationship.uselist is involved.

When set to True, the relationship is used only for loading objects, and not for any persistence operation. A relationship() which specifies relationship.viewonly can work with a wider range of SQL operations within the relationship.primaryjoin condition, including operations that feature the use of a variety of comparison operators as well as SQL functions such as cast(). The relationship.viewonly flag is also of general use when defining any kind of relationship() that doesn’t represent the full set of related objects, to prevent modifications of the collection from resulting in persistence operations.

Notes on using the viewonly relationship parameter - more details on best practices when using relationship.viewonly.

A boolean that enables the events used to synchronize the in-Python attributes when this relationship is target of either relationship.backref or relationship.back_populates.

Defaults to None, which indicates that an automatic value should be selected based on the value of the relationship.viewonly flag. When left at its default, changes in state will be back-populated only if neither sides of a relationship is viewonly.

Added in version 1.3.17.

Changed in version 1.4: - A relationship that specifies relationship.viewonly automatically implies that relationship.sync_backref is False.

relationship.viewonly

Allows manual control over the “selectin” automatic join optimization. Set to False to disable the “omit join” feature added in SQLAlchemy 1.3; or leave as None to leave automatic optimization in place.

This flag may only be set to False. It is not necessary to set it to True as the “omit_join” optimization is automatically detected; if it is not detected, then the optimization is not supported.

Changed in version 1.3.11: setting omit_join to True will now emit a warning as this was not the intended use of this flag.

Added in version 1.3.

init¶ – Specific to Declarative Dataclass Mapping, specifies if the mapped attribute should be part of the __init__() method as generated by the dataclass process.

repr¶ – Specific to Declarative Dataclass Mapping, specifies if the mapped attribute should be part of the __repr__() method as generated by the dataclass process.

default_factory¶ – Specific to Declarative Dataclass Mapping, specifies a default-value generation function that will take place as part of the __init__() method as generated by the dataclass process.

Specific to Declarative Dataclass Mapping, indicates if this field should be included in comparison operations when generating the __eq__() and __ne__() methods for the mapped class.

Added in version 2.0.0b4.

kw_only¶ – Specific to Declarative Dataclass Mapping, indicates if this field should be marked as keyword-only when generating the __init__().

Specific to Declarative Dataclass Mapping, controls if this field is included when generating the __hash__() method for the mapped class.

Added in version 2.0.36.

dataclass_metadata¶ –

Specific to Declarative Dataclass Mapping, supplies metadata to be attached to the generated dataclass field.

Added in version 2.0.42.

When using the relationship.backref parameter, provides specific parameters to be used when the new relationship() is generated.

The relationship.backref parameter is generally considered to be legacy; for modern applications, using explicit relationship() constructs linked together using the relationship.back_populates parameter should be preferred.

Using the legacy ‘backref’ relationship parameter - background on backrefs

Construct a dynamically-loading mapper property.

This is essentially the same as using the lazy='dynamic' argument with relationship():

See the section Dynamic Relationship Loaders for more details on dynamic loading.

Annotate a portion of a primaryjoin expression with a ‘foreign’ annotation.

See the section Creating Custom Foreign Conditions for a description of use.

Creating Custom Foreign Conditions

Annotate a portion of a primaryjoin expression with a ‘remote’ annotation.

See the section Creating Custom Foreign Conditions for a description of use.

Creating Custom Foreign Conditions

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (php):
```php
class SomeClass(Base):
    # ...

    related = relationship("RelatedClass")
```

Example 2 (php):
```php
class SomeClass(Base):
    # ...

    related_items: Mapped[List["RelatedItem"]] = relationship()
```

Example 3 (php):
```php
class SomeClass(Base):
    # ...

    related_item: Mapped["RelatedItem"] = relationship()
```

Example 4 (unknown):
```unknown
>>> User.addresses.property.uselist
True
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/self_referential.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Adjacency List Relationships¶
- Composite Adjacency Lists¶
- Self-Referential Query Strategies¶
- Configuring Self-Referential Eager Loading¶

Home | Download this Documentation

Home | Download this Documentation

The adjacency list pattern is a common relational pattern whereby a table contains a foreign key reference to itself, in other words is a self referential relationship. This is the most common way to represent hierarchical data in flat tables. Other methods include nested sets, sometimes called “modified preorder”, as well as materialized path. Despite the appeal that modified preorder has when evaluated for its fluency within SQL queries, the adjacency list model is probably the most appropriate pattern for the large majority of hierarchical storage needs, for reasons of concurrency, reduced complexity, and that modified preorder has little advantage over an application which can fully load subtrees into the application space.

This section details the single-table version of a self-referential relationship. For a self-referential relationship that uses a second table as an association table, see the section Self-Referential Many-to-Many Relationship.

In this example, we’ll work with a single mapped class called Node, representing a tree structure:

With this structure, a graph such as the following:

Would be represented with data such as:

The relationship() configuration here works in the same way as a “normal” one-to-many relationship, with the exception that the “direction”, i.e. whether the relationship is one-to-many or many-to-one, is assumed by default to be one-to-many. To establish the relationship as many-to-one, an extra directive is added known as relationship.remote_side, which is a Column or collection of Column objects that indicate those which should be considered to be “remote”:

Where above, the id column is applied as the relationship.remote_side of the parent relationship(), thus establishing parent_id as the “local” side, and the relationship then behaves as a many-to-one.

As always, both directions can be combined into a bidirectional relationship using two relationship() constructs linked by relationship.back_populates:

Adjacency List - working example, updated for SQLAlchemy 2.0

A sub-category of the adjacency list relationship is the rare case where a particular column is present on both the “local” and “remote” side of the join condition. An example is the Folder class below; using a composite primary key, the account_id column refers to itself, to indicate sub folders which are within the same account as that of the parent; while folder_id refers to a specific folder within that account:

Above, we pass account_id into the relationship.remote_side list. relationship() recognizes that the account_id column here is on both sides, and aligns the “remote” column along with the folder_id column, which it recognizes as uniquely present on the “remote” side.

Querying of self-referential structures works like any other query:

However extra care is needed when attempting to join along the foreign key from one level of the tree to the next. In SQL, a join from a table to itself requires that at least one side of the expression be “aliased” so that it can be unambiguously referred to.

Recall from Selecting ORM Aliases in the ORM tutorial that the aliased() construct is normally used to provide an “alias” of an ORM entity. Joining from Node to itself using this technique looks like:

Eager loading of relationships occurs using joins or outerjoins from parent to child table during a normal query operation, such that the parent and its immediate child collection or reference can be populated from a single SQL statement, or a second statement for all immediate child collections. SQLAlchemy’s joined and subquery eager loading use aliased tables in all cases when joining to related items, so are compatible with self-referential joining. However, to use eager loading with a self-referential relationship, SQLAlchemy needs to be told how many levels deep it should join and/or query; otherwise the eager load will not take place at all. This depth setting is configured via relationships.join_depth:

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (typescript):
```typescript
class Node(Base):
    __tablename__ = "node"
    id = mapped_column(Integer, primary_key=True)
    parent_id = mapped_column(Integer, ForeignKey("node.id"))
    data = mapped_column(String(50))
    children = relationship("Node")
```

Example 2 (php):
```php
root --+---> child1
       +---> child2 --+--> subchild1
       |              +--> subchild2
       +---> child3
```

Example 3 (yaml):
```yaml
id       parent_id     data
---      -------       ----
1        NULL          root
2        1             child1
3        1             child2
4        3             subchild1
5        3             subchild2
6        1             child3
```

Example 4 (typescript):
```typescript
class Node(Base):
    __tablename__ = "node"
    id = mapped_column(Integer, primary_key=True)
    parent_id = mapped_column(Integer, ForeignKey("node.id"))
    data = mapped_column(String(50))
    parent = relationship("Node", remote_side=[id])
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Relationship Loading Techniques¶
- Summary of Relationship Loading Styles¶
- Configuring Loader Strategies at Mapping Time¶
- Relationship Loading with Loader Options¶
  - Adding Criteria to loader options¶
  - Specifying Sub-Options with Load.options()¶

Home | Download this Documentation

Home | Download this Documentation

This page is part of the ORM Querying Guide.

Previous: Column Loading Options | Next: ORM API Features for Querying

This section presents an in-depth view of how to load related objects. Readers should be familiar with Relationship Configuration and basic use.

Most examples here assume the “User/Address” mapping setup similar to the one illustrated at setup for selects.

A big part of SQLAlchemy is providing a wide range of control over how related objects get loaded when querying. By “related objects” we refer to collections or scalar associations configured on a mapper using relationship(). This behavior can be configured at mapper construction time using the relationship.lazy parameter to the relationship() function, as well as by using ORM loader options with the Select construct.

The loading of relationships falls into three categories; lazy loading, eager loading, and no loading. Lazy loading refers to objects that are returned from a query without the related objects loaded at first. When the given collection or reference is first accessed on a particular object, an additional SELECT statement is emitted such that the requested collection is loaded.

Eager loading refers to objects returned from a query with the related collection or scalar reference already loaded up front. The ORM achieves this either by augmenting the SELECT statement it would normally emit with a JOIN to load in related rows simultaneously, or by emitting additional SELECT statements after the primary one to load collections or scalar references at once.

“No” loading refers to the disabling of loading on a given relationship, either that the attribute is empty and is just never loaded, or that it raises an error when it is accessed, in order to guard against unwanted lazy loads.

The primary forms of relationship loading are:

lazy loading - available via lazy='select' or the lazyload() option, this is the form of loading that emits a SELECT statement at attribute access time to lazily load a related reference on a single object at a time. Lazy loading is the default loading style for all relationship() constructs that don’t otherwise indicate the relationship.lazy option. Lazy loading is detailed at Lazy Loading.

select IN loading - available via lazy='selectin' or the selectinload() option, this form of loading emits a second (or more) SELECT statement which assembles the primary key identifiers of the parent objects into an IN clause, so that all members of related collections / scalar references are loaded at once by primary key. Select IN loading is detailed at Select IN loading.

joined loading - available via lazy='joined' or the joinedload() option, this form of loading applies a JOIN to the given SELECT statement so that related rows are loaded in the same result set. Joined eager loading is detailed at Joined Eager Loading.

raise loading - available via lazy='raise', lazy='raise_on_sql', or the raiseload() option, this form of loading is triggered at the same time a lazy load would normally occur, except it raises an ORM exception in order to guard against the application making unwanted lazy loads. An introduction to raise loading is at Preventing unwanted lazy loads using raiseload.

subquery loading - available via lazy='subquery' or the subqueryload() option, this form of loading emits a second SELECT statement which re-states the original query embedded inside of a subquery, then JOINs that subquery to the related table to be loaded to load all members of related collections / scalar references at once. Subquery eager loading is detailed at Subquery Eager Loading.

write only loading - available via lazy='write_only', or by annotating the left side of the Relationship object using the WriteOnlyMapped annotation. This collection-only loader style produces an alternative attribute instrumentation that never implicitly loads records from the database, instead only allowing WriteOnlyCollection.add(), WriteOnlyCollection.add_all() and WriteOnlyCollection.remove() methods. Querying the collection is performed by invoking a SELECT statement which is constructed using the WriteOnlyCollection.select() method. Write only loading is discussed at Write Only Relationships.

dynamic loading - available via lazy='dynamic', or by annotating the left side of the Relationship object using the DynamicMapped annotation. This is a legacy collection-only loader style which produces a Query object when the collection is accessed, allowing custom SQL to be emitted against the collection’s contents. However, dynamic loaders will implicitly iterate the underlying collection in various circumstances which makes them less useful for managing truly large collections. Dynamic loaders are superseded by “write only” collections, which will prevent the underlying collection from being implicitly loaded under any circumstances. Dynamic loaders are discussed at Dynamic Relationship Loaders.

The loader strategy for a particular relationship can be configured at mapping time to take place in all cases where an object of the mapped type is loaded, in the absence of any query-level options that modify it. This is configured using the relationship.lazy parameter to relationship(); common values for this parameter include select, selectin and joined.

The example below illustrates the relationship example at One To Many, configuring the Parent.children relationship to use Select IN loading when a SELECT statement for Parent objects is emitted:

Above, whenever a collection of Parent objects are loaded, each Parent will also have its children collection populated, using the "selectin" loader strategy that emits a second query.

The default value of the relationship.lazy argument is "select", which indicates Lazy Loading.

The other, and possibly more common way to configure loading strategies is to set them up on a per-query basis against specific attributes using the Select.options() method. Very detailed control over relationship loading is available using loader options; the most common are joinedload(), selectinload() and lazyload(). The option accepts a class-bound attribute referring to the specific class/attribute that should be targeted:

The loader options can also be “chained” using method chaining to specify how loading should occur further levels deep:

Chained loader options can be applied against a “lazy” loaded collection. This means that when a collection or association is lazily loaded upon access, the specified option will then take effect:

Above, the query will return Parent objects without the children collections loaded. When the children collection on a particular Parent object is first accessed, it will lazy load the related objects, but additionally apply eager loading to the subelements collection on each member of children.

The relationship attributes used to indicate loader options include the ability to add additional filtering criteria to the ON clause of the join that’s created, or to the WHERE criteria involved, depending on the loader strategy. This can be achieved using the PropComparator.and_() method which will pass through an option such that loaded results are limited to the given filter criteria:

When using limiting criteria, if a particular collection is already loaded it won’t be refreshed; to ensure the new criteria takes place, apply the Populate Existing execution option:

In order to add filtering criteria to all occurrences of an entity throughout a query, regardless of loader strategy or where it occurs in the loading process, see the with_loader_criteria() function.

Added in version 1.4.

Using method chaining, the loader style of each link in the path is explicitly stated. To navigate along a path without changing the existing loader style of a particular attribute, the defaultload() method/function may be used:

A similar approach can be used to specify multiple sub-options at once, using the Load.options() method:

Using load_only() on related objects and collections - illustrates examples of combining relationship and column-oriented loader options.

The loader options applied to an object’s lazy-loaded collections are “sticky” to specific object instances, meaning they will persist upon collections loaded by that specific object for as long as it exists in memory. For example, given the previous example:

if the children collection on a particular Parent object loaded by the above query is expired (such as when a Session object’s transaction is committed or rolled back, or Session.expire_all() is used), when the Parent.children collection is next accessed in order to re-load it, the Child.subelements collection will again be loaded using subquery eager loading. This stays the case even if the above Parent object is accessed from a subsequent query that specifies a different set of options. To change the options on an existing object without expunging it and re-loading, they must be set explicitly in conjunction using the Populate Existing execution option:

If the objects loaded above are fully cleared from the Session, such as due to garbage collection or that Session.expunge_all() were used, the “sticky” options will also be gone and the newly created objects will make use of new options if loaded again.

A future SQLAlchemy release may add more alternatives to manipulating the loader options on already-loaded objects.

By default, all inter-object relationships are lazy loading. The scalar or collection attribute associated with a relationship() contains a trigger which fires the first time the attribute is accessed. This trigger typically issues a SQL call at the point of access in order to load the related object or objects:

The one case where SQL is not emitted is for a simple many-to-one relationship, when the related object can be identified by its primary key alone and that object is already present in the current Session. For this reason, while lazy loading can be expensive for related collections, in the case that one is loading lots of objects with simple many-to-ones against a relatively small set of possible target objects, lazy loading may be able to refer to these objects locally without emitting as many SELECT statements as there are parent objects.

This default behavior of “load upon attribute access” is known as “lazy” or “select” loading - the name “select” because a “SELECT” statement is typically emitted when the attribute is first accessed.

Lazy loading can be enabled for a given attribute that is normally configured in some other way using the lazyload() loader option:

The lazyload() strategy produces an effect that is one of the most common issues referred to in object relational mapping; the N plus one problem, which states that for any N objects loaded, accessing their lazy-loaded attributes means there will be N+1 SELECT statements emitted. In SQLAlchemy, the usual mitigation for the N+1 problem is to make use of its very capable eager load system. However, eager loading requires that the attributes which are to be loaded be specified with the Select up front. The problem of code that may access other attributes that were not eagerly loaded, where lazy loading is not desired, may be addressed using the raiseload() strategy; this loader strategy replaces the behavior of lazy loading with an informative error being raised:

Above, a User object loaded from the above query will not have the .addresses collection loaded; if some code later on attempts to access this attribute, an ORM exception is raised.

raiseload() may be used with a so-called “wildcard” specifier to indicate that all relationships should use this strategy. For example, to set up only one attribute as eager loading, and all the rest as raise:

The above wildcard will apply to all relationships not just on Order besides items, but all those on the Item objects as well. To set up raiseload() for only the Order objects, specify a full path with Load:

Conversely, to set up the raise for just the Item objects:

The raiseload() option applies only to relationship attributes. For column-oriented attributes, the defer() option supports the defer.raiseload option which works in the same way.

The “raiseload” strategies do not apply within the unit of work flush process. That means if the Session.flush() process needs to load a collection in order to finish its work, it will do so while bypassing any raiseload() directives.

Wildcard Loading Strategies

Using raiseload to prevent deferred column loads

Joined eager loading is the oldest style of eager loading included with the SQLAlchemy ORM. It works by connecting a JOIN (by default a LEFT OUTER join) to the SELECT statement emitted, and populates the target scalar/collection from the same result set as that of the parent.

At the mapping level, this looks like:

Joined eager loading is usually applied as an option to a query, rather than as a default loading option on the mapping, in particular when used for collections rather than many-to-one-references. This is achieved using the joinedload() loader option:

When including joinedload() in reference to a one-to-many or many-to-many collection, the Result.unique() method must be applied to the returned result, which will uniquify the incoming rows by primary key that otherwise are multiplied out by the join. The ORM will raise an error if this is not present.

This is not automatic in modern SQLAlchemy, as it changes the behavior of the result set to return fewer ORM objects than the statement would normally return in terms of number of rows. Therefore SQLAlchemy keeps the use of Result.unique() explicit, so there’s no ambiguity that the returned objects are being uniqified on primary key.

The JOIN emitted by default is a LEFT OUTER JOIN, to allow for a lead object that does not refer to a related row. For an attribute that is guaranteed to have an element, such as a many-to-one reference to a related object where the referencing foreign key is NOT NULL, the query can be made more efficient by using an inner join; this is available at the mapping level via the relationship.innerjoin flag:

At the query option level, via the joinedload.innerjoin flag:

The JOIN will right-nest itself when applied in a chain that includes an OUTER JOIN:

If using database row locking techniques when emitting the SELECT, meaning the Select.with_for_update() method is being used to emit SELECT..FOR UPDATE, the joined table may be locked as well, depending on the behavior of the backend in use. It’s not recommended to use joined eager loading at the same time as SELECT..FOR UPDATE for this reason.

Since joined eager loading seems to have many resemblances to the use of Select.join(), it often produces confusion as to when and how it should be used. It is critical to understand the distinction that while Select.join() is used to alter the results of a query, joinedload() goes through great lengths to not alter the results of the query, and instead hide the effects of the rendered join to only allow for related objects to be present.

The philosophy behind loader strategies is that any set of loading schemes can be applied to a particular query, and the results don’t change - only the number of SQL statements required to fully load related objects and collections changes. A particular query might start out using all lazy loads. After using it in context, it might be revealed that particular attributes or collections are always accessed, and that it would be more efficient to change the loader strategy for these. The strategy can be changed with no other modifications to the query, the results will remain identical, but fewer SQL statements would be emitted. In theory (and pretty much in practice), nothing you can do to the Select would make it load a different set of primary or related objects based on a change in loader strategy.

How joinedload() in particular achieves this result of not impacting entity rows returned in any way is that it creates an anonymous alias of the joins it adds to your query, so that they can’t be referenced by other parts of the query. For example, the query below uses joinedload() to create a LEFT OUTER JOIN from users to addresses, however the ORDER BY added against Address.email_address is not valid - the Address entity is not named in the query:

Above, ORDER BY addresses.email_address is not valid since addresses is not in the FROM list. The correct way to load the User records and order by email address is to use Select.join():

The statement above is of course not the same as the previous one, in that the columns from addresses are not included in the result at all. We can add joinedload() back in, so that there are two joins - one is that which we are ordering on, the other is used anonymously to load the contents of the User.addresses collection:

What we see above is that our usage of Select.join() is to supply JOIN clauses we’d like to use in subsequent query criterion, whereas our usage of joinedload() only concerns itself with the loading of the User.addresses collection, for each User in the result. In this case, the two joins most probably appear redundant - which they are. If we wanted to use just one JOIN for collection loading as well as ordering, we use the contains_eager() option, described in Routing Explicit Joins/Statements into Eagerly Loaded Collections below. But to see why joinedload() does what it does, consider if we were filtering on a particular Address:

Above, we can see that the two JOINs have very different roles. One will match exactly one row, that of the join of User and Address where Address.email_address=='someaddress@foo.com'. The other LEFT OUTER JOIN will match all Address rows related to User, and is only used to populate the User.addresses collection, for those User objects that are returned.

By changing the usage of joinedload() to another style of loading, we can change how the collection is loaded completely independently of SQL used to retrieve the actual User rows we want. Below we change joinedload() into selectinload():

When using joined eager loading, if the query contains a modifier that impacts the rows returned externally to the joins, such as when using DISTINCT, LIMIT, OFFSET or equivalent, the completed statement is first wrapped inside a subquery, and the joins used specifically for joined eager loading are applied to the subquery. SQLAlchemy’s joined eager loading goes the extra mile, and then ten miles further, to absolutely ensure that it does not affect the end result of the query, only the way collections and related objects are loaded, no matter what the format of the query is.

Routing Explicit Joins/Statements into Eagerly Loaded Collections - using contains_eager()

In most cases, selectin loading is the most simple and efficient way to eagerly load collections of objects. The only scenario in which selectin eager loading is not feasible is when the model is using composite primary keys, and the backend database does not support tuples with IN, which currently includes SQL Server.

“Select IN” eager loading is provided using the "selectin" argument to relationship.lazy or by using the selectinload() loader option. This style of loading emits a SELECT that refers to the primary key values of the parent object, or in the case of a many-to-one relationship to the those of the child objects, inside of an IN clause, in order to load related associations:

Above, the second SELECT refers to addresses.user_id IN (5, 7), where the “5” and “7” are the primary key values for the previous two User objects loaded; after a batch of objects are completely loaded, their primary key values are injected into the IN clause for the second SELECT. Because the relationship between User and Address has a simple primary join condition and provides that the primary key values for User can be derived from Address.user_id, the statement has no joins or subqueries at all.

For simple many-to-one loads, a JOIN is also not needed as the foreign key value from the parent object is used:

by “simple” we mean that the relationship.primaryjoin condition expresses an equality comparison between the primary key of the “one” side and a straight foreign key of the “many” side, without any additional criteria.

Select IN loading also supports many-to-many relationships, where it currently will JOIN across all three tables to match rows from one side to the other.

Things to know about this kind of loading include:

The strategy emits a SELECT for up to 500 parent primary key values at a time, as the primary keys are rendered into a large IN expression in the SQL statement. Some databases like Oracle Database have a hard limit on how large an IN expression can be, and overall the size of the SQL string shouldn’t be arbitrarily large.

As “selectin” loading relies upon IN, for a mapping with composite primary keys, it must use the “tuple” form of IN, which looks like WHERE (table.column_a, table.column_b) IN ((?, ?), (?, ?), (?, ?)). This syntax is not currently supported on SQL Server and for SQLite requires at least version 3.15. There is no special logic in SQLAlchemy to check ahead of time which platforms support this syntax or not; if run against a non-supporting platform, the database will return an error immediately. An advantage to SQLAlchemy just running the SQL out for it to fail is that if a particular database does start supporting this syntax, it will work without any changes to SQLAlchemy (as was the case with SQLite).

The subqueryload() eager loader is mostly legacy at this point, superseded by the selectinload() strategy which is of much simpler design, more flexible with features such as Yield Per, and emits more efficient SQL statements in most cases. As subqueryload() relies upon re-interpreting the original SELECT statement, it may fail to work efficiently when given very complex source queries.

subqueryload() may continue to be useful for the specific case of an eager loaded collection for objects that use composite primary keys, on the Microsoft SQL Server backend that continues to not have support for the “tuple IN” syntax.

Subquery loading is similar in operation to selectin eager loading, however the SELECT statement which is emitted is derived from the original statement, and has a more complex query structure as that of selectin eager loading.

Subquery eager loading is provided using the "subquery" argument to relationship.lazy or by using the subqueryload() loader option.

The operation of subquery eager loading is to emit a second SELECT statement for each relationship to be loaded, across all result objects at once. This SELECT statement refers to the original SELECT statement, wrapped inside of a subquery, so that we retrieve the same list of primary keys for the primary object being returned, then link that to the sum of all the collection members to load them at once:

Things to know about this kind of loading include:

The SELECT statement emitted by the “subquery” loader strategy, unlike that of “selectin”, requires a subquery, and will inherit whatever performance limitations are present in the original query. The subquery itself may also incur performance penalties based on the specifics of the database in use.

“subquery” loading imposes some special ordering requirements in order to work correctly. A query which makes use of subqueryload() in conjunction with a limiting modifier such as Select.limit(), or Select.offset() should always include Select.order_by() against unique column(s) such as the primary key, so that the additional queries emitted by subqueryload() include the same ordering as used by the parent query. Without it, there is a chance that the inner query could return the wrong rows:

Why is ORDER BY recommended with LIMIT (especially with subqueryload())? - detailed example

“subquery” loading also incurs additional performance / complexity issues when used on a many-levels-deep eager load, as subqueries will be nested repeatedly.

“subquery” loading is not compatible with the “batched” loading supplied by Yield Per, both for collection and scalar relationships.

For the above reasons, the “selectin” strategy should be preferred over “subquery”.

Which type of loading to use typically comes down to optimizing the tradeoff between number of SQL executions, complexity of SQL emitted, and amount of data fetched.

One to Many / Many to Many Collection - The selectinload() is generally the best loading strategy to use. It emits an additional SELECT that uses as few tables as possible, leaving the original statement unaffected, and is most flexible for any kind of originating query. Its only major limitation is when using a table with composite primary keys on a backend that does not support “tuple IN”, which currently includes SQL Server and very old SQLite versions; all other included backends support it.

Many to One - The joinedload() strategy is the most general purpose strategy. In special cases, the immediateload() strategy may also be useful, if there are a very small number of potential related values, as this strategy will fetch the object from the local Session without emitting any SQL if the related object is already present.

Specification of polymorphic options on a per-eager-load basis is supported. See the section Eager Loading of Polymorphic Subtypes for examples of the PropComparator.of_type() method in conjunction with the with_polymorphic() function.

Each of joinedload(), subqueryload(), lazyload(), selectinload(), and raiseload() can be used to set the default style of relationship() loading for a particular query, affecting all relationship() -mapped attributes not otherwise specified in the statement. This feature is available by passing the string '*' as the argument to any of these options:

Above, the lazyload('*') option will supersede the lazy setting of all relationship() constructs in use for that query, with the exception of those that use lazy='write_only' or lazy='dynamic'.

If some relationships specify lazy='joined' or lazy='selectin', for example, using lazyload('*') will unilaterally cause all those relationships to use 'select' loading, e.g. emit a SELECT statement when each attribute is accessed.

The option does not supersede loader options stated in the query, such as joinedload(), selectinload(), etc. The query below will still use joined loading for the widget relationship:

While the instruction for joinedload() above will take place regardless of whether it appears before or after the lazyload() option, if multiple options that each included "*" were passed, the last one will take effect.

A variant of the wildcard loader strategy is the ability to set the strategy on a per-entity basis. For example, if querying for User and Address, we can instruct all relationships on Address to use lazy loading, while leaving the loader strategies for User unaffected, by first applying the Load object, then specifying the * as a chained option:

Above, all relationships on Address will be set to a lazy load.

The behavior of joinedload() is such that joins are created automatically, using anonymous aliases as targets, the results of which are routed into collections and scalar references on loaded objects. It is often the case that a query already includes the necessary joins which represent a particular collection or scalar reference, and the joins added by the joinedload feature are redundant - yet you’d still like the collections/references to be populated.

For this SQLAlchemy supplies the contains_eager() option. This option is used in the same manner as the joinedload() option except it is assumed that the Select object will explicitly include the appropriate joins, typically using methods like Select.join(). Below, we specify a join between User and Address and additionally establish this as the basis for eager loading of User.addresses:

If the “eager” portion of the statement is “aliased”, the path should be specified using PropComparator.of_type(), which allows the specific aliased() construct to be passed:

The path given as the argument to contains_eager() needs to be a full path from the starting entity. For example if we were loading Users->orders->Order->items->Item, the option would be used as:

When we use contains_eager(), we are constructing ourselves the SQL that will be used to populate collections. From this, it naturally follows that we can opt to modify what values the collection is intended to store, by writing our SQL to load a subset of elements for collections or scalar attributes.

SQLAlchemy now has a much simpler way to do this, by allowing WHERE criteria to be added directly to loader options such as joinedload() and selectinload() using PropComparator.and_(). See the section Adding Criteria to loader options for examples.

The techniques described here still apply if the related collection is to be queried using SQL criteria or modifiers more complex than a simple WHERE clause.

As an example, we can load a User object and eagerly load only particular addresses into its .addresses collection by filtering the joined data, routing it using contains_eager(), also using Populate Existing to ensure any already-loaded collections are overwritten:

The above query will load only User objects which contain at least Address object that contains the substring 'aol.com' in its email field; the User.addresses collection will contain only these Address entries, and not any other Address entries that are in fact associated with the collection.

In all cases, the SQLAlchemy ORM does not overwrite already loaded attributes and collections unless told to do so. As there is an identity map in use, it is often the case that an ORM query is returning objects that were in fact already present and loaded in memory. Therefore, when using contains_eager() to populate a collection in an alternate way, it is usually a good idea to use Populate Existing as illustrated above so that an already-loaded collection is refreshed with the new data. The populate_existing option will reset all attributes that were already present, including pending changes, so make sure all data is flushed before using it. Using the Session with its default behavior of autoflush is sufficient.

The customized collection we load using contains_eager() is not “sticky”; that is, the next time this collection is loaded, it will be loaded with its usual default contents. The collection is subject to being reloaded if the object is expired, which occurs whenever the Session.commit(), Session.rollback() methods are used assuming default session settings, or the Session.expire_all() or Session.expire() methods are used.

Adding Criteria to loader options - modern API allowing WHERE criteria directly within any relationship loader option

contains_eager(*keys, **kw)

Indicate that the given attribute should be eagerly loaded from columns stated manually in the query.

Indicate an attribute should load using its predefined loader style.

immediateload(*keys, [recursion_depth])

Indicate that the given attribute should be loaded using an immediate load with a per-attribute SELECT statement.

joinedload(*keys, **kw)

Indicate that the given attribute should be loaded using joined eager loading.

Indicate that the given attribute should be loaded using “lazy” loading.

Represents loader options which modify the state of a ORM-enabled Select or a legacy Query in order to affect how various mapped attributes are loaded.

Indicate that the given relationship attribute should remain unloaded.

raiseload(*keys, **kw)

Indicate that the given attribute should raise an error if accessed.

selectinload(*keys, [recursion_depth])

Indicate that the given attribute should be loaded using SELECT IN eager loading.

Indicate that the given attribute should be loaded using subquery eager loading.

Indicate that the given attribute should be eagerly loaded from columns stated manually in the query.

This function is part of the Load interface and supports both method-chained and standalone operation.

The option is used in conjunction with an explicit join that loads the desired rows, i.e.:

The above query would join from the Order entity to its related User entity, and the returned Order objects would have the Order.user attribute pre-populated.

It may also be used for customizing the entries in an eagerly loaded collection; queries will normally want to use the Populate Existing execution option assuming the primary collection of parent objects may already have been loaded:

See the section Routing Explicit Joins/Statements into Eagerly Loaded Collections for complete usage details.

Relationship Loading Techniques

Routing Explicit Joins/Statements into Eagerly Loaded Collections

Indicate an attribute should load using its predefined loader style.

The behavior of this loading option is to not change the current loading style of the attribute, meaning that the previously configured one is used or, if no previous style was selected, the default loading will be used.

This method is used to link to other loader options further into a chain of attributes without altering the loader style of the links along the chain. For example, to set joined eager loading for an element of an element:

defaultload() is also useful for setting column-level options on a related class, namely that of defer() and undefer():

Specifying Sub-Options with Load.options()

Indicate that the given attribute should be loaded using an immediate load with a per-attribute SELECT statement.

The load is achieved using the “lazyloader” strategy and does not fire off any additional eager loaders.

The immediateload() option is superseded in general by the selectinload() option, which performs the same task more efficiently by emitting a SELECT for all loaded objects.

This function is part of the Load interface and supports both method-chained and standalone operation.

optional int; when set to a positive integer in conjunction with a self-referential relationship, indicates “selectin” loading will continue that many levels deep automatically until no items are found.

The immediateload.recursion_depth option currently supports only self-referential relationships. There is not yet an option to automatically traverse recursive structures with more than one relationship involved.

This parameter is new and experimental and should be treated as “alpha” status

Added in version 2.0: added immediateload.recursion_depth

Relationship Loading Techniques

Indicate that the given attribute should be loaded using joined eager loading.

This function is part of the Load interface and supports both method-chained and standalone operation.

if True, indicates that the joined eager load should use an inner join instead of the default of left outer join:

In order to chain multiple eager joins together where some may be OUTER and others INNER, right-nested joins are used to link them:

The above query, linking A.bs via “outer” join and B.cs via “inner” join would render the joins as “a LEFT OUTER JOIN (b JOIN c)”. When using older versions of SQLite (< 3.7.16), this form of JOIN is translated to use full subqueries as this syntax is otherwise not directly supported.

The innerjoin flag can also be stated with the term "unnested". This indicates that an INNER JOIN should be used, unless the join is linked to a LEFT OUTER JOIN to the left, in which case it will render as LEFT OUTER JOIN. For example, supposing A.bs is an outerjoin:

The above join will render as “a LEFT OUTER JOIN b LEFT OUTER JOIN c”, rather than as “a LEFT OUTER JOIN (b JOIN c)”.

The “unnested” flag does not affect the JOIN rendered from a many-to-many association table, e.g. a table configured as relationship.secondary, to the target table; for correctness of results, these joins are always INNER and are therefore right-nested if linked to an OUTER join.

The joins produced by joinedload() are anonymously aliased. The criteria by which the join proceeds cannot be modified, nor can the ORM-enabled Select or legacy Query refer to these joins in any way, including ordering. See The Zen of Joined Eager Loading for further detail.

To produce a specific SQL JOIN which is explicitly available, use Select.join() and Query.join(). To combine explicit JOINs with eager loading of collections, use contains_eager(); see Routing Explicit Joins/Statements into Eagerly Loaded Collections.

Relationship Loading Techniques

Indicate that the given attribute should be loaded using “lazy” loading.

This function is part of the Load interface and supports both method-chained and standalone operation.

Relationship Loading Techniques

inherits from sqlalchemy.orm.strategy_options._AbstractLoad

Represents loader options which modify the state of a ORM-enabled Select or a legacy Query in order to affect how various mapped attributes are loaded.

The Load object is in most cases used implicitly behind the scenes when one makes use of a query option like joinedload(), defer(), or similar. It typically is not instantiated directly except for in some very specific cases.

Per-Entity Wildcard Loading Strategies - illustrates an example where direct use of Load may be useful

Produce a new Load object with the contains_eager() option applied.

Produce a new Load object with the defaultload() option applied.

Produce a new Load object with the defer() option applied.

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

Produce a new Load object with the immediateload() option applied.

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

Produce a new Load object with the joinedload() option applied.

Produce a new Load object with the lazyload() option applied.

Produce a new Load object with the load_only() option applied.

Produce a new Load object with the noload() option applied.

Apply a series of options as sub-options to this Load object.

process_compile_state()

Apply a modification to a given ORMCompileState.

process_compile_state_replaced_entities()

Apply a modification to a given ORMCompileState, given entities that were replaced by with_only_columns() or with_entities().

if True, indicate this option should be carried along to “secondary” SELECT statements that occur for relationship lazy loaders as well as attribute load / refresh operations.

Produce a new Load object with the raiseload() option applied.

selectin_polymorphic()

Produce a new Load object with the selectin_polymorphic() option applied.

Produce a new Load object with the selectinload() option applied.

Produce a new Load object with the subqueryload() option applied.

Produce a new Load object with the undefer() option applied.

Produce a new Load object with the undefer_group() option applied.

Produce a new Load object with the with_expression() option applied.

inherited from the sqlalchemy.orm.strategy_options._AbstractLoad.contains_eager method of sqlalchemy.orm.strategy_options._AbstractLoad

Produce a new Load object with the contains_eager() option applied.

See contains_eager() for usage examples.

inherited from the sqlalchemy.orm.strategy_options._AbstractLoad.defaultload method of sqlalchemy.orm.strategy_options._AbstractLoad

Produce a new Load object with the defaultload() option applied.

See defaultload() for usage examples.

inherited from the sqlalchemy.orm.strategy_options._AbstractLoad.defer method of sqlalchemy.orm.strategy_options._AbstractLoad

Produce a new Load object with the defer() option applied.

See defer() for usage examples.

inherited from the HasTraverseInternals.get_children() method of HasTraverseInternals

Return immediate child HasTraverseInternals elements of this HasTraverseInternals.

This is used for visit traversal.

**kw may contain flags that change the collection that is returned, for example to return a subset of items in order to cut down on larger traversals, or to return child items from a different context (such as schema-level collections instead of clause-level).

inherited from the sqlalchemy.orm.strategy_options._AbstractLoad.immediateload method of sqlalchemy.orm.strategy_options._AbstractLoad

Produce a new Load object with the immediateload() option applied.

See immediateload() for usage examples.

inherited from the HasCacheKey.inherit_cache attribute of HasCacheKey

Indicate if this HasCacheKey instance should make use of the cache key generation scheme used by its immediate superclass.

The attribute defaults to None, which indicates that a construct has not yet taken into account whether or not its appropriate for it to participate in caching; this is functionally equivalent to setting the value to False, except that a warning is also emitted.

This flag can be set to True on a particular class, if the SQL that corresponds to the object does not change based on attributes which are local to this class, and not its superclass.

Enabling Caching Support for Custom Constructs - General guideslines for setting the HasCacheKey.inherit_cache attribute for third-party or user defined SQL constructs.

inherited from the sqlalchemy.orm.strategy_options._AbstractLoad.joinedload method of sqlalchemy.orm.strategy_options._AbstractLoad

Produce a new Load object with the joinedload() option applied.

See joinedload() for usage examples.

inherited from the sqlalchemy.orm.strategy_options._AbstractLoad.lazyload method of sqlalchemy.orm.strategy_options._AbstractLoad

Produce a new Load object with the lazyload() option applied.

See lazyload() for usage examples.

inherited from the sqlalchemy.orm.strategy_options._AbstractLoad.load_only method of sqlalchemy.orm.strategy_options._AbstractLoad

Produce a new Load object with the load_only() option applied.

See load_only() for usage examples.

inherited from the sqlalchemy.orm.strategy_options._AbstractLoad.noload method of sqlalchemy.orm.strategy_options._AbstractLoad

Produce a new Load object with the noload() option applied.

See noload() for usage examples.

Apply a series of options as sub-options to this Load object.

*opts¶ – A series of loader option objects (ultimately Load objects) which should be applied to the path specified by this Load object.

Added in version 1.3.6.

Specifying Sub-Options with Load.options()

inherited from the sqlalchemy.orm.strategy_options._AbstractLoad.process_compile_state method of sqlalchemy.orm.strategy_options._AbstractLoad

Apply a modification to a given ORMCompileState.

This method is part of the implementation of a particular CompileStateOption and is only invoked internally when an ORM query is compiled.

inherited from the sqlalchemy.orm.strategy_options._AbstractLoad.process_compile_state_replaced_entities method of sqlalchemy.orm.strategy_options._AbstractLoad

Apply a modification to a given ORMCompileState, given entities that were replaced by with_only_columns() or with_entities().

This method is part of the implementation of a particular CompileStateOption and is only invoked internally when an ORM query is compiled.

Added in version 1.4.19.

inherited from the sqlalchemy.orm.strategy_options._AbstractLoad.propagate_to_loaders attribute of sqlalchemy.orm.strategy_options._AbstractLoad

if True, indicate this option should be carried along to “secondary” SELECT statements that occur for relationship lazy loaders as well as attribute load / refresh operations.

inherited from the sqlalchemy.orm.strategy_options._AbstractLoad.raiseload method of sqlalchemy.orm.strategy_options._AbstractLoad

Produce a new Load object with the raiseload() option applied.

See raiseload() for usage examples.

inherited from the sqlalchemy.orm.strategy_options._AbstractLoad.selectin_polymorphic method of sqlalchemy.orm.strategy_options._AbstractLoad

Produce a new Load object with the selectin_polymorphic() option applied.

See selectin_polymorphic() for usage examples.

inherited from the sqlalchemy.orm.strategy_options._AbstractLoad.selectinload method of sqlalchemy.orm.strategy_options._AbstractLoad

Produce a new Load object with the selectinload() option applied.

See selectinload() for usage examples.

inherited from the sqlalchemy.orm.strategy_options._AbstractLoad.subqueryload method of sqlalchemy.orm.strategy_options._AbstractLoad

Produce a new Load object with the subqueryload() option applied.

See subqueryload() for usage examples.

inherited from the sqlalchemy.orm.strategy_options._AbstractLoad.undefer method of sqlalchemy.orm.strategy_options._AbstractLoad

Produce a new Load object with the undefer() option applied.

See undefer() for usage examples.

inherited from the sqlalchemy.orm.strategy_options._AbstractLoad.undefer_group method of sqlalchemy.orm.strategy_options._AbstractLoad

Produce a new Load object with the undefer_group() option applied.

See undefer_group() for usage examples.

inherited from the sqlalchemy.orm.strategy_options._AbstractLoad.with_expression method of sqlalchemy.orm.strategy_options._AbstractLoad

Produce a new Load object with the with_expression() option applied.

See with_expression() for usage examples.

Indicate that the given relationship attribute should remain unloaded.

The relationship attribute will return None when accessed without producing any loading effect.

This function is part of the Load interface and supports both method-chained and standalone operation.

noload() applies to relationship() attributes only.

The noload() option is legacy. As it forces collections to be empty, which invariably leads to non-intuitive and difficult to predict results. There are no legitimate uses for this option in modern SQLAlchemy.

Relationship Loading Techniques

Indicate that the given attribute should raise an error if accessed.

A relationship attribute configured with raiseload() will raise an InvalidRequestError upon access. The typical way this is useful is when an application is attempting to ensure that all relationship attributes that are accessed in a particular context would have been already loaded via eager loading. Instead of having to read through SQL logs to ensure lazy loads aren’t occurring, this strategy will cause them to raise immediately.

raiseload() applies to relationship() attributes only. In order to apply raise-on-SQL behavior to a column-based attribute, use the defer.raiseload parameter on the defer() loader option.

sql_only¶ – if True, raise only if the lazy load would emit SQL, but not if it is only checking the identity map, or determining that the related value should just be None due to missing keys. When False, the strategy will raise for all varieties of relationship loading.

This function is part of the Load interface and supports both method-chained and standalone operation.

Relationship Loading Techniques

Preventing unwanted lazy loads using raiseload

Using raiseload to prevent deferred column loads

Indicate that the given attribute should be loaded using SELECT IN eager loading.

This function is part of the Load interface and supports both method-chained and standalone operation.

optional int; when set to a positive integer in conjunction with a self-referential relationship, indicates “selectin” loading will continue that many levels deep automatically until no items are found.

The selectinload.recursion_depth option currently supports only self-referential relationships. There is not yet an option to automatically traverse recursive structures with more than one relationship involved.

Additionally, the selectinload.recursion_depth parameter is new and experimental and should be treated as “alpha” status for the 2.0 series.

Added in version 2.0: added selectinload.recursion_depth

Relationship Loading Techniques

Indicate that the given attribute should be loaded using subquery eager loading.

This function is part of the Load interface and supports both method-chained and standalone operation.

Relationship Loading Techniques

Subquery Eager Loading

Next Query Guide Section: ORM API Features for Querying

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Parent(Base):
    __tablename__ = "parent"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["Child"]] = relationship(lazy="selectin")


class Child(Base):
    __tablename__ = "child"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent.id"))
```

Example 2 (sql):
```sql
from sqlalchemy import select
from sqlalchemy.orm import lazyload

# set children to load lazily
stmt = select(Parent).options(lazyload(Parent.children))

from sqlalchemy.orm import joinedload

# set children to load eagerly with a join
stmt = select(Parent).options(joinedload(Parent.children))
```

Example 3 (sql):
```sql
from sqlalchemy import select
from sqlalchemy.orm import joinedload

stmt = select(Parent).options(
    joinedload(Parent.children).subqueryload(Child.subelements)
)
```

Example 4 (sql):
```sql
from sqlalchemy import select
from sqlalchemy.orm import lazyload

stmt = select(Parent).options(lazyload(Parent.children).subqueryload(Child.subelements))
```

---
