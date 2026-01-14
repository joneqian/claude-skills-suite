# Sqlalchemy - Orm Mapping

**Pages:** 6

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Composing Mapped Hierarchies with Mixins¶
- Augmenting the Base¶
- Mixing in Columns¶
- Mixing in Relationships¶
- Mixing in column_property() and other MapperProperty classes¶
- Using Mixins and Base Classes with Mapped Inheritance Patterns¶

Home | Download this Documentation

Home | Download this Documentation

A common need when mapping classes using the Declarative style is to share common functionality, such as particular columns, table or mapper options, naming schemes, or other mapped properties, across many classes. When using declarative mappings, this idiom is supported via the use of mixin classes, as well as via augmenting the declarative base class itself.

In addition to mixin classes, common column options may also be shared among many classes using PEP 593 Annotated types; see Mapping Multiple Type Configurations to Python Types and Mapping Whole Column Declarations to Python Types for background on these SQLAlchemy 2.0 features.

An example of some commonly mixed-in idioms is below:

The above example illustrates a class MyModel which includes two mixins CommonMixin and HasLogRecord in its bases, as well as a supplementary class LogRecord which also includes CommonMixin, demonstrating a variety of constructs that are supported on mixins and base classes, including:

columns declared using mapped_column(), Mapped or Column are copied from mixins or base classes onto the target class to be mapped; above this is illustrated via the column attributes CommonMixin.id and HasLogRecord.log_record_id.

Declarative directives such as __table_args__ and __mapper_args__ can be assigned to a mixin or base class, where they will take effect automatically for any classes which inherit from the mixin or base. The above example illustrates this using the __table_args__ and __mapper_args__ attributes.

All Declarative directives, including all of __tablename__, __table__, __table_args__ and __mapper_args__, may be implemented using user-defined class methods, which are decorated with the declared_attr decorator (specifically the declared_attr.directive sub-member, more on that in a moment). Above, this is illustrated using a def __tablename__(cls) classmethod that generates a Table name dynamically; when applied to the MyModel class, the table name will be generated as "mymodel", and when applied to the LogRecord class, the table name will be generated as "logrecord".

Other ORM properties such as relationship() can be generated on the target class to be mapped using user-defined class methods also decorated with the declared_attr decorator. Above, this is illustrated by generating a many-to-one relationship() to a mapped object called LogRecord.

The features above may all be demonstrated using a select() example:

The examples of declared_attr will attempt to illustrate the correct PEP 484 annotations for each method example. The use of annotations with declared_attr functions are completely optional, and are not consumed by Declarative; however, these annotations are required in order to pass Mypy --strict type checking.

Additionally, the declared_attr.directive sub-member illustrated above is optional as well, and is only significant for PEP 484 typing tools, as it adjusts for the expected return type when creating methods to override Declarative directives such as __tablename__, __mapper_args__ and __table_args__.

Added in version 2.0: As part of PEP 484 typing support for the SQLAlchemy ORM, added the declared_attr.directive to declared_attr to distinguish between Mapped attributes and Declarative configurational attributes

There’s no fixed convention for the order of mixins and base classes. Normal Python method resolution rules apply, and the above example would work just as well with:

This works because Base here doesn’t define any of the variables that CommonMixin or HasLogRecord defines, i.e. __tablename__, __table_args__, id, etc. If the Base did define an attribute of the same name, the class placed first in the inherits list would determine which attribute is used on the newly defined class.

While the above example is using Annotated Declarative Table form based on the Mapped annotation class, mixin classes also work perfectly well with non-annotated and legacy Declarative forms, such as when using Column directly instead of mapped_column().

Changed in version 2.0: For users coming from the 1.4 series of SQLAlchemy who may have been using the mypy plugin, the declarative_mixin() class decorator is no longer needed to mark declarative mixins, assuming the mypy plugin is no longer in use.

In addition to using a pure mixin, most of the techniques in this section can also be applied to the base class directly, for patterns that should apply to all classes derived from a particular base. The example below illustrates some of the previous section’s example in terms of the Base class:

Where above, MyModel as well as LogRecord, in deriving from Base, will both have their table name derived from their class name, a primary key column named id, as well as the above table and mapper arguments defined by Base.__table_args__ and Base.__mapper_args__.

When using legacy declarative_base() or registry.generate_base(), the declarative_base.cls parameter may be used as follows to generate an equivalent effect, as illustrated in the non-annotated example below:

Columns can be indicated in mixins assuming the Declarative table style of configuration is in use (as opposed to imperative table configuration), so that columns declared on the mixin can then be copied to be part of the Table that the Declarative process generates. All three of the mapped_column(), Mapped, and Column constructs may be declared inline in a declarative mixin:

Where above, all declarative classes that include TimestampMixin in their class bases will automatically include a column created_at that applies a timestamp to all row insertions, as well as an updated_at column, which does not include a default for the purposes of the example (if it did, we would use the Column.onupdate parameter which is accepted by mapped_column()). These column constructs are always copied from the originating mixin or base class, so that the same mixin/base class may be applied to any number of target classes which will each have their own column constructs.

All Declarative column forms are supported by mixins, including:

Annotated attributes - with or without mapped_column() present:

mapped_column - with or without Mapped present:

Column - legacy Declarative form:

In each of the above forms, Declarative handles the column-based attributes on the mixin class by creating a copy of the construct, which is then applied to the target class.

Changed in version 2.0: The declarative API can now accommodate Column objects as well as mapped_column() constructs of any form when using mixins without the need to use declared_attr(). Previous limitations which prevented columns with ForeignKey elements from being used directly in mixins have been removed.

Relationships created by relationship() are provided with declarative mixin classes exclusively using the declared_attr approach, eliminating any ambiguity which could arise when copying a relationship and its possibly column-bound contents. Below is an example which combines a foreign key column and a relationship so that two classes Foo and Bar can both be configured to reference a common target class via many-to-one:

With the above mapping, each of Foo and Bar contain a relationship to Target accessed along the .target attribute:

Special arguments such as relationship.primaryjoin may also be used within mixed-in classmethods, which often need to refer to the class that’s being mapped. For schemes that need to refer to locally mapped columns, in ordinary cases these columns are made available by Declarative as attributes on the mapped class which is passed as the cls argument to the decorated classmethod. Using this feature, we could for example rewrite the RefTargetMixin.target method using an explicit primaryjoin which refers to pending mapped columns on both Target and cls:

Like relationship(), other MapperProperty subclasses such as column_property() also need to have class-local copies generated when used by mixins, so are also declared within functions that are decorated by declared_attr. Within the function, other ordinary mapped columns that were declared with mapped_column(), Mapped, or Column will be made available from the cls argument so that they may be used to compose new attributes, as in the example below which adds two columns together:

Above, we may make use of Something.x_plus_y in a statement where it produces the full expression:

The declared_attr decorator causes the decorated callable to behave exactly as a classmethod. However, typing tools like Pylance may not be able to recognize this, which can sometimes cause it to complain about access to the cls variable inside the body of the function. To resolve this issue when it occurs, the @classmethod decorator may be combined directly with declared_attr as:

Added in version 2.0: - declared_attr can accommodate a function decorated with @classmethod to help with PEP 484 integration where needed.

When dealing with mapper inheritance patterns as documented at Mapping Class Inheritance Hierarchies, some additional capabilities are present when using declared_attr either with mixin classes, or when augmenting both mapped and un-mapped superclasses in a class hierarchy.

When defining functions decorated by declared_attr on mixins or base classes to be interpreted by subclasses in a mapped inheritance hierarchy, there is an important distinction made between functions that generate the special names used by Declarative such as __tablename__, __mapper_args__ vs. those that may generate ordinary mapped attributes such as mapped_column() and relationship(). Functions that define Declarative directives are invoked for each subclass in a hierarchy, whereas functions that generate mapped attributes are invoked only for the first mapped superclass in a hierarchy.

The rationale for this difference in behavior is based on the fact that mapped properties are already inheritable by classes, such as a particular column on a superclass’ mapped table should not be duplicated to that of a subclass as well, whereas elements that are specific to a particular class or its mapped table are not inheritable, such as the name of the table that is locally mapped.

The difference in behavior between these two use cases is demonstrated in the following two sections.

A common recipe with mixins is to create a def __tablename__(cls) function that generates a name for the mapped Table dynamically.

This recipe can be used to generate table names for an inheriting mapper hierarchy as in the example below which creates a mixin that gives every class a simple table name based on class name. The recipe is illustrated below where a table name is generated for the Person mapped class and the Engineer subclass of Person, but not for the Manager subclass of Person:

In the above example, both the Person base class as well as the Engineer class, being subclasses of the Tablename mixin class which generates new table names, will have a generated __tablename__ attribute, which to Declarative indicates that each class should have its own Table generated to which it will be mapped. For the Engineer subclass, the style of inheritance applied is joined table inheritance, as it will be mapped to a table engineer that joins to the base person table. Any other subclasses that inherit from Person will also have this style of inheritance applied by default (and within this particular example, would need to each specify a primary key column; more on that in the next section).

By contrast, the Manager subclass of Person overrides the __tablename__ classmethod to return None. This indicates to Declarative that this class should not have a Table generated, and will instead make use exclusively of the base Table to which Person is mapped. For the Manager subclass, the style of inheritance applied is single table inheritance.

The example above illustrates that Declarative directives like __tablename__ are necessarily applied to each subclass individually, as each mapped class needs to state which Table it will be mapped towards, or if it will map itself to the inheriting superclass’ Table.

If we instead wanted to reverse the default table scheme illustrated above, so that single table inheritance were the default and joined table inheritance could be defined only when a __tablename__ directive were supplied to override it, we can make use of Declarative helpers within the top-most __tablename__() method, in this case a helper called has_inherited_table(). This function will return True if a superclass is already mapped to a Table. We may use this helper within the base-most __tablename__() classmethod so that we may conditionally return None for the table name, if a table is already present, thus indicating single-table inheritance for inheriting subclasses by default:

In contrast to how __tablename__ and other special names are handled when used with declared_attr, when we mix in columns and properties (e.g. relationships, column properties, etc.), the function is invoked for the base class only in the hierarchy, unless the declared_attr directive is used in combination with the declared_attr.cascading sub-directive. Below, only the Person class will receive a column called id; the mapping will fail on Engineer, which is not given a primary key:

It is usually the case in joined-table inheritance that we want distinctly named columns on each subclass. However in this case, we may want to have an id column on every table, and have them refer to each other via foreign key. We can achieve this as a mixin by using the declared_attr.cascading modifier, which indicates that the function should be invoked for each class in the hierarchy, in almost (see warning below) the same way as it does for __tablename__:

The declared_attr.cascading feature currently does not allow for a subclass to override the attribute with a different function or value. This is a current limitation in the mechanics of how @declared_attr is resolved, and a warning is emitted if this condition is detected. This limitation only applies to ORM mapped columns, relationships, and other MapperProperty styles of attribute. It does not apply to Declarative directives such as __tablename__, __mapper_args__, etc., which resolve in a different way internally than that of declared_attr.cascading.

In the case of __table_args__ or __mapper_args__ specified with declarative mixins, you may want to combine some parameters from several mixins with those you wish to define on the class itself. The declared_attr decorator can be used here to create user-defined collation routines that pull from multiple collections:

Using named constraints such as Index, UniqueConstraint, CheckConstraint, where each object is to be unique to a specific table descending from a mixin, requires that an individual instance of each object is created per actual mapped class.

As a simple example, to define a named, potentially multicolumn Index that applies to all tables derived from a mixin, use the “inline” form of Index and establish it as part of __table_args__, using declared_attr to establish __table_args__() as a class method that will be invoked for each subclass:

The above example would generate two tables "table_a" and "table_b", with indexes "test_idx_table_a" and "test_idx_table_b"

Typically, in modern SQLAlchemy we would use a naming convention, as documented at Configuring Constraint Naming Conventions. While naming conventions take place automatically using the MetaData.naming_convention as new Constraint objects are created, as this convention is applied at object construction time based on the parent Table for a particular Constraint, a distinct Constraint object needs to be created for each inheriting subclass with its own Table, again using declared_attr with __table_args__(), below illustrated using an abstract mapped base:

The above mapping will generate DDL that includes table-specific names for all constraints, including primary key, CHECK constraint, unique constraint:

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class CommonMixin:
    """define a series of common elements that may be applied to mapped
    classes using this class as a mixin class."""

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    __table_args__ = {"mysql_engine": "InnoDB"}
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)


class HasLogRecord:
    """mark classes that have a many-to-one relationship to the
    ``LogRecord`` class."""

    log_record_id: Mapped[int] = mapped_column(ForeignKey("logrecord.id"))

    @declared_attr
    def log_record(self) -> Mapped["LogRecord"]:
        return relationship("LogRecord")


class LogRecord(CommonMixin, Base):
    log_info: Mapped[str]


class MyModel(CommonMixin, HasLogRecord, Base):
    name: Mapped[str]
```

Example 2 (sql):
```sql
>>> from sqlalchemy import select
>>> print(select(MyModel).join(MyModel.log_record))
SELECT mymodel.name, mymodel.id, mymodel.log_record_id
FROM mymodel JOIN logrecord ON logrecord.id = mymodel.log_record_id
```

Example 3 (php):
```php
class MyModel(Base, HasLogRecord, CommonMixin):
    name: Mapped[str] = mapped_column()
```

Example 4 (python):
```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    """define a series of common elements that may be applied to mapped
    classes using this class as a base class."""

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    __table_args__ = {"mysql_engine": "InnoDB"}
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)


class HasLogRecord:
    """mark classes that have a many-to-one relationship to the
    ``LogRecord`` class."""

    log_record_id: Mapped[int] = mapped_column(ForeignKey("logrecord.id"))

    @declared_attr
    def log_record(self) -> Mapped["LogRecord"]:
        return relationship("LogRecord")


class LogRecord(Base):
    log_info: Mapped[str]


class MyModel(HasLogRecord, Base):
    name: Mapped[str]
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Writing SELECT statements for Inheritance Mappings¶
- SELECTing from the base class vs. specific sub-classes¶
- Using selectin_polymorphic()¶
  - Applying selectin_polymorphic() to an existing eager load¶
  - Applying loader options to the subclasses loaded by selectin_polymorphic¶
    - Applying loader options when selectin_polymorphic is itself a sub-option¶

Home | Download this Documentation

Home | Download this Documentation

This page is part of the ORM Querying Guide.

Previous: Writing SELECT statements for ORM Mapped Classes | Next: ORM-Enabled INSERT, UPDATE, and DELETE statements

This section makes use of ORM mappings configured using the ORM Inheritance feature, described at Mapping Class Inheritance Hierarchies. The emphasis will be on Joined Table Inheritance as this is the most intricate ORM querying case.

View the ORM setup for this page.

A SELECT statement constructed against a class in a joined inheritance hierarchy will query against the table to which the class is mapped, as well as any super-tables present, using JOIN to link them together. The query would then return objects that are of that requested type as well as any sub-types of the requested type, using the discriminator value in each row to determine the correct type. The query below is established against the Manager subclass of Employee, which then returns a result that will contain only objects of type Manager:

When the SELECT statement is against the base class in the hierarchy, the default behavior is that only that class’ table will be included in the rendered SQL and JOIN will not be used. As in all cases, the discriminator column is used to distinguish between different requested sub-types, which then results in objects of any possible sub-type being returned. The objects returned will have attributes corresponding to the base table populated, and attributes corresponding to sub-tables will start in an un-loaded state, loading automatically when accessed. The loading of sub-attributes is configurable to be more “eager” in a variety of ways, discussed later in this section.

The example below creates a query against the Employee superclass. This indicates that objects of any type, including Manager, Engineer, and Employee, may be within the result set:

Above, the additional tables for Manager and Engineer were not included in the SELECT, which means that the returned objects will not yet contain data represented from those tables, in this example the .manager_name attribute of the Manager class as well as the .engineer_info attribute of the Engineer class. These attributes start out in the expired state, and will automatically populate themselves when first accessed using lazy loading:

This lazy load behavior is not desirable if a large number of objects have been loaded, in the case that the consuming application will need to be accessing subclass-specific attributes, as this would be an example of the N plus one problem that emits additional SQL per row. This additional SQL can impact performance and also be incompatible with approaches such as using asyncio. Additionally, in our query for Employee objects, since the query is against the base table only, we did not have a way to add SQL criteria involving subclass-specific attributes in terms of Manager or Engineer. The next two sections detail two constructs that provide solutions to these two issues in different ways, the selectin_polymorphic() loader option and the with_polymorphic() entity construct.

To address the issue of performance when accessing attributes on subclasses, the selectin_polymorphic() loader strategy may be used to eagerly load these additional attributes up front across many objects at once. This loader option works in a similar fashion as the selectinload() relationship loader strategy to emit an additional SELECT statement against each sub-table for objects loaded in the hierarchy, using IN to query for additional rows based on primary key.

selectin_polymorphic() accepts as its arguments the base entity that is being queried, followed by a sequence of subclasses of that entity for which their specific attributes should be loaded for incoming rows:

The selectin_polymorphic() construct is then used as a loader option, passing it to the Select.options() method of Select. The example illustrates the use of selectin_polymorphic() to eagerly load columns local to both the Manager and Engineer subclasses:

The above example illustrates two additional SELECT statements being emitted in order to eagerly fetch additional attributes such as Engineer.engineer_info as well as Manager.manager_name. We can now access these sub-attributes on the objects that were loaded without any additional SQL statements being emitted:

The selectin_polymorphic() loader option does not yet optimize for the fact that the base employee table does not need to be included in the second two “eager load” queries; hence in the example above we see a JOIN from employee to manager and engineer, even though columns from employee are already loaded. This is in contrast to the selectinload() relationship strategy which is more sophisticated in this regard and can factor out the JOIN when not needed.

In addition to selectin_polymorphic() being specified as an option for a top-level entity loaded by a statement, we may also indicate selectin_polymorphic() on the target of an existing load. As our setup mapping includes a parent Company entity with a Company.employees relationship() referring to Employee entities, we may illustrate a SELECT against the Company entity that eagerly loads all Employee objects as well as all attributes on their subtypes as follows, by applying Load.selectin_polymorphic() as a chained loader option; in this form, the first argument is implicit from the previous loader option (in this case selectinload()), so we only indicate the additional target subclasses we wish to load:

Eager Loading of Polymorphic Subtypes - illustrates the equivalent example as above using with_polymorphic() instead

The SELECT statements emitted by selectin_polymorphic() are themselves ORM statements, so we may also add other loader options (such as those documented at Relationship Loading Techniques) that refer to specific subclasses. These options should be applied as siblings to a selectin_polymorphic() option, that is, comma separated within select.options().

For example, if we considered that the Manager mapper had a one to many relationship to an entity called Paperwork, we could combine the use of selectin_polymorphic() and selectinload() to eagerly load this collection on all Manager objects, where the sub-attributes of Manager objects were also themselves eagerly loaded:

Added in version 2.0.21.

The previous section illustrated selectin_polymorphic() and selectinload() used as sibling options, both used within a single call to select.options(). If the target entity is one that is already being loaded from a parent relationship, as in the example at Applying selectin_polymorphic() to an existing eager load, we can apply this “sibling” pattern using the Load.options() method that applies sub-options to a parent, as illustrated at Specifying Sub-Options with Load.options(). Below we combine the two examples to load Company.employees, also loading the attributes for the Manager and Engineer classes, as well as eagerly loading the `Manager.paperwork` attribute:

The behavior of selectin_polymorphic() may be configured on specific mappers so that it takes place by default, by using the Mapper.polymorphic_load parameter, using the value "selectin" on a per-subclass basis. The example below illustrates the use of this parameter within Engineer and Manager subclasses:

With the above mapping, SELECT statements against the Employee class will automatically assume the use of selectin_polymorphic(Employee, [Engineer, Manager]) as a loader option when the statement is emitted.

In contrast to selectin_polymorphic() which affects only the loading of objects, the with_polymorphic() construct affects how the SQL query for a polymorphic structure is rendered, most commonly as a series of LEFT OUTER JOINs to each of the included sub-tables. This join structure is known as the polymorphic selectable. By providing for a view of several sub-tables at once, with_polymorphic() offers a means of writing a SELECT statement across several inherited classes at once with the ability to add filtering criteria based on individual sub-tables.

with_polymorphic() is essentially a special form of the aliased() construct. It accepts as its arguments a similar form to that of selectin_polymorphic(), which is the base entity that is being queried, followed by a sequence of subclasses of that entity for which their specific attributes should be loaded for incoming rows:

In order to indicate that all subclasses should be part of the entity, with_polymorphic() will also accept the string "*", which may be passed in place of the sequence of classes to indicate all classes (note this is not yet supported by selectin_polymorphic()):

The example below illustrates the same operation as illustrated in the previous section, to load all columns for Manager and Engineer at once:

As is the case with selectin_polymorphic(), attributes on subclasses are already loaded:

As the default selectable produced by with_polymorphic() uses LEFT OUTER JOIN, from a database point of view the query is not as well optimized as the approach that selectin_polymorphic() takes, with simple SELECT statements using only JOINs emitted on a per-table basis.

The with_polymorphic() construct makes available the attributes on the included subclass mappers, by including namespaces that allow references to subclasses. The employee_poly construct created in the previous section includes attributes named .Engineer and .Manager which provide the namespace for Engineer and Manager in terms of the polymorphic SELECT. In the example below, we can use the or_() construct to create criteria against both classes at once:

The with_polymorphic() construct, as a special case of aliased(), also provides the basic feature that aliased() does, which is that of “aliasing” of the polymorphic selectable itself. Specifically this means two or more with_polymorphic() entities, referring to the same class hierarchy, can be used at once in a single statement.

To use this feature with a joined inheritance mapping, we typically want to pass two parameters, with_polymorphic.aliased as well as with_polymorphic.flat. The with_polymorphic.aliased parameter indicates that the polymorphic selectable should be referenced by an alias name that is unique to this construct. The with_polymorphic.flat parameter is specific to the default LEFT OUTER JOIN polymorphic selectable and indicates that a more optimized form of aliasing should be used in the statement.

To illustrate this feature, the example below emits a SELECT for two separate polymorphic entities, Employee joined with Engineer, and Employee joined with Manager. Since these two polymorphic entities will both be including the base employee table in their polymorphic selectable, aliasing must be applied in order to differentiate this table in its two different contexts. The two polymorphic entities are treated like two individual tables, and as such typically need to be joined with each other in some way, as illustrated below where the entities are joined on the company_id column along with some additional limiting criteria against the Employee / Manager entity:

In the above example, the behavior of with_polymorphic.flat is that the polymorphic selectables remain as a LEFT OUTER JOIN of their individual tables, which themselves are given anonymous alias names. There is also a right-nested JOIN produced.

When omitting the with_polymorphic.flat parameter, the usual behavior is that each polymorphic selectable is enclosed within a subquery, producing a more verbose form:

The above form historically has been more portable to backends that didn’t necessarily have support for right-nested JOINs, and it additionally may be appropriate when the “polymorphic selectable” used by with_polymorphic() is not a simple LEFT OUTER JOIN of tables, as is the case when using mappings such as concrete table inheritance mappings as well as when using alternative polymorphic selectables in general.

As is the case with selectin_polymorphic(), the with_polymorphic() construct also supports a mapper-configured version which may be configured in two different ways, either on the base class using the mapper.with_polymorphic parameter, or in a more modern form using the Mapper.polymorphic_load parameter on a per-subclass basis, passing the value "inline".

For joined inheritance mappings, prefer explicit use of with_polymorphic() within queries, or for implicit eager subclass loading use Mapper.polymorphic_load with "selectin", instead of using the mapper-level mapper.with_polymorphic parameter described in this section. This parameter invokes complex heuristics intended to rewrite the FROM clauses within SELECT statements that can interfere with construction of more complex statements, particularly those with nested subqueries that refer to the same mapped entity.

For example, we may state our Employee mapping using Mapper.polymorphic_load as "inline" as below:

With the above mapping, SELECT statements against the Employee class will automatically assume the use of with_polymorphic(Employee, [Engineer, Manager]) as the primary entity when the statement is emitted:

When using mapper-level “with polymorphic”, queries can also refer to the subclass entities directly, where they implicitly represent the joined tables in the polymorphic query. Above, we can freely refer to Manager and Engineer directly against the default Employee entity:

However, if we needed to refer to the Employee entity or its sub entities in separate, aliased contexts, we would again make direct use of with_polymorphic() to define these aliased entities as illustrated in Using aliasing with with_polymorphic.

For more centralized control over the polymorphic selectable, the more legacy form of mapper-level polymorphic control may be used which is the Mapper.with_polymorphic parameter, configured on the base class. This parameter accepts arguments that are comparable to the with_polymorphic() construct, however common use with a joined inheritance mapping is the plain asterisk, indicating all sub-tables should be LEFT OUTER JOINED, as in:

Overall, the LEFT OUTER JOIN format used by with_polymorphic() and by options such as Mapper.with_polymorphic may be cumbersome from a SQL and database optimizer point of view; for general loading of subclass attributes in joined inheritance mappings, the selectin_polymorphic() approach, or its mapper level equivalent of setting Mapper.polymorphic_load to "selectin" should likely be preferred, making use of with_polymorphic() on a per-query basis only as needed.

As a with_polymorphic() entity is a special case of aliased(), in order to treat a polymorphic entity as the target of a join, specifically when using a relationship() construct as the ON clause, we use the same technique for regular aliases as detailed at Using Relationship to join between aliased targets, most succinctly using PropComparator.of_type(). In the example below we illustrate a join from the parent Company entity along the one-to-many relationship Company.employees, which is configured in the setup to link to Employee objects, using a with_polymorphic() entity as the target:

More directly, PropComparator.of_type() is also used with inheritance mappings of any kind to limit a join along a relationship() to a particular sub-type of the relationship()’s target. The above query could be written strictly in terms of Engineer targets as follows:

It can be observed above that joining to the Engineer target directly, rather than the “polymorphic selectable” of with_polymorphic(Employee, [Engineer]) has the useful characteristic of using an inner JOIN rather than a LEFT OUTER JOIN, which is generally more performant from a SQL optimizer point of view.

The use of PropComparator.of_type() illustrated with the Select.join() method in the previous section may also be applied equivalently to relationship loader options, such as selectinload() and joinedload().

As a basic example, if we wished to load Company objects, and additionally eagerly load all elements of Company.employees using the with_polymorphic() construct against the full hierarchy, we may write:

The above query may be compared directly to the selectin_polymorphic() version illustrated in the previous section Applying selectin_polymorphic() to an existing eager load.

Applying selectin_polymorphic() to an existing eager load - illustrates the equivalent example as above using selectin_polymorphic() instead

Single Table Inheritance Setup

This section discusses single table inheritance, described at Single Table Inheritance, which uses a single table to represent multiple classes in a hierarchy.

View the ORM setup for this section.

In contrast to joined inheritance mappings, the construction of SELECT statements for single inheritance mappings tends to be simpler since for an all-single-inheritance hierarchy, there’s only one table.

Regardless of whether or not the inheritance hierarchy is all single-inheritance or has a mixture of joined and single inheritance, SELECT statements for single inheritance differentiate queries against the base class vs. a subclass by limiting the SELECT statement with additional WHERE criteria.

As an example, a query for the single-inheritance example mapping of Employee will load objects of type Manager, Engineer and Employee using a simple SELECT of the table:

When a load is emitted for a specific subclass, additional criteria is added to the SELECT that limits the rows, such as below where a SELECT against the Engineer entity is performed:

The default behavior of single inheritance mappings regarding how attributes on subclasses are SELECTed is similar to that of joined inheritance, in that subclass-specific attributes still emit a second SELECT by default. In the example below, a single Employee of type Manager is loaded, however since the requested class is Employee, the Manager.manager_name attribute is not present by default, and an additional SELECT is emitted when it’s accessed:

To alter this behavior, the same general concepts used to eagerly load these additional attributes used in joined inheritance loading apply to single inheritance as well, including use of the selectin_polymorphic() option as well as the with_polymorphic() option, the latter of which simply includes the additional columns and from a SQL perspective is more efficient for single-inheritance mappers:

Since the overhead of loading single-inheritance subclass mappings is usually minimal, it’s therefore recommended that single inheritance mappings include the Mapper.polymorphic_load parameter with a setting of "inline" for those subclasses where loading of their specific subclass attributes is expected to be common. An example illustrating the setup, modified to include this option, is below:

With the above mapping, the Manager and Engineer classes will have their columns included in SELECT statements against the Employee entity automatically:

selectin_polymorphic(base_cls, classes)

Indicate an eager load should take place for all attributes specific to a subclass.

with_polymorphic(base, classes[, selectable, flat, ...])

Produce an AliasedClass construct which specifies columns for descendant mappers of the given base.

Produce an AliasedClass construct which specifies columns for descendant mappers of the given base.

Using this method will ensure that each descendant mapper’s tables are included in the FROM clause, and will allow filter() criterion to be used against those tables. The resulting instances will also have those columns already loaded so that no “post fetch” of those columns will be required.

Using with_polymorphic() - full discussion of with_polymorphic().

base¶ – Base class to be aliased.

classes¶ – a single class or mapper, or list of class/mappers, which inherit from the base class. Alternatively, it may also be the string '*', in which case all descending mapped classes will be added to the FROM clause.

aliased¶ – when True, the selectable will be aliased. For a JOIN, this means the JOIN will be SELECTed from inside of a subquery unless the with_polymorphic.flat flag is set to True, which is recommended for simpler use cases.

flat¶ – Boolean, will be passed through to the FromClause.alias() call so that aliases of Join objects will alias the individual tables inside the join, rather than creating a subquery. This is generally supported by all modern databases with regards to right-nested joins and generally produces more efficient queries. Setting this flag is recommended as long as the resulting SQL is functional.

a table or subquery that will be used in place of the generated FROM clause. This argument is required if any of the desired classes use concrete table inheritance, since SQLAlchemy currently cannot generate UNIONs among tables automatically. If used, the selectable argument must represent the full set of tables and columns mapped by every mapped class. Otherwise, the unaccounted mapped columns will result in their table being appended directly to the FROM clause which will usually lead to incorrect results.

When left at its default value of False, the polymorphic selectable assigned to the base mapper is used for selecting rows. However, it may also be passed as None, which will bypass the configured polymorphic selectable and instead construct an ad-hoc selectable for the target classes given; for joined table inheritance this will be a join that includes all target mappers and their subclasses.

polymorphic_on¶ – a column to be used as the “discriminator” column for the given selectable. If not given, the polymorphic_on attribute of the base classes’ mapper will be used, if any. This is useful for mappings that don’t have polymorphic loading behavior by default.

innerjoin¶ – if True, an INNER JOIN will be used. This should only be specified if querying for one specific subtype only

Passes through the aliased.adapt_on_names parameter to the aliased object. This may be useful in situations where the given selectable is not directly related to the existing mapped selectable.

Added in version 1.4.33.

Name given to the generated AliasedClass.

Added in version 2.0.31.

Indicate an eager load should take place for all attributes specific to a subclass.

This uses an additional SELECT with IN against all matched primary key values, and is the per-query analogue to the "selectin" setting on the mapper.polymorphic_load parameter.

Added in version 1.2.

Using selectin_polymorphic()

Next Query Guide Section: ORM-Enabled INSERT, UPDATE, and DELETE statements

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (sql):
```sql
>>> from sqlalchemy import select
>>> stmt = select(Manager).order_by(Manager.id)
>>> managers = session.scalars(stmt).all()
BEGIN (implicit)
SELECT manager.id, employee.id AS id_1, employee.name, employee.type, employee.company_id, manager.manager_name
FROM employee JOIN manager ON employee.id = manager.id ORDER BY manager.id
[...] ()
>>> print(managers)
[Manager('Mr. Krabs')]
```

Example 2 (sql):
```sql
>>> from sqlalchemy import select
>>> stmt = select(Employee).order_by(Employee.id)
>>> objects = session.scalars(stmt).all()
BEGIN (implicit)
SELECT employee.id, employee.name, employee.type, employee.company_id
FROM employee ORDER BY employee.id
[...] ()
>>> print(objects)
[Manager('Mr. Krabs'), Engineer('SpongeBob'), Engineer('Squidward')]
```

Example 3 (sql):
```sql
>>> mr_krabs = objects[0]
>>> print(mr_krabs.manager_name)
SELECT manager.manager_name AS manager_manager_name
FROM manager
WHERE ? = manager.id
[...] (1,)
Eugene H. Krabs
```

Example 4 (sql):
```sql
>>> from sqlalchemy.orm import selectin_polymorphic
>>> loader_opt = selectin_polymorphic(Employee, [Manager, Engineer])
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/scalar_mapping.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Mapping SQL Expressions¶

Home | Download this Documentation

Home | Download this Documentation

This page has been merged into the ORM Mapped Class Configuration index.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Table Configuration with Declarative¶
- Declarative Table with mapped_column()¶
  - ORM Annotated Declarative - Automated Mapping with Type Annotations¶
  - Dataclass features in mapped_column()¶
  - Accessing Table and Metadata¶
  - Declarative Table Configuration¶

Home | Download this Documentation

Home | Download this Documentation

As introduced at Declarative Mapping, the Declarative style includes the ability to generate a mapped Table object at the same time, or to accommodate a Table or other FromClause object directly.

The following examples assume a declarative base class as:

All of the examples that follow illustrate a class inheriting from the above Base. The decorator style introduced at Declarative Mapping using a Decorator (no declarative base) is fully supported with all the following examples as well, as are legacy forms of Declarative Base including base classes generated by declarative_base().

When using Declarative, the body of the class to be mapped in most cases includes an attribute __tablename__ that indicates the string name of a Table that should be generated along with the mapping. The mapped_column() construct, which features additional ORM-specific configuration capabilities not present in the plain Column class, is then used within the class body to indicate columns in the table. The example below illustrates the most basic use of this construct within a Declarative mapping:

Above, mapped_column() constructs are placed inline within the class definition as class level attributes. At the point at which the class is declared, the Declarative mapping process will generate a new Table object against the MetaData collection associated with the Declarative Base; each instance of mapped_column() will then be used to generate a Column object during this process, which will become part of the Table.columns collection of this Table object.

In the above example, Declarative will build a Table construct that is equivalent to the following:

When the User class above is mapped, this Table object can be accessed directly via the __table__ attribute; this is described further at Accessing Table and Metadata.

mapped_column() supersedes the use of Column()

Users of 1.x SQLAlchemy will note the use of the mapped_column() construct, which is new as of the SQLAlchemy 2.0 series. This ORM-specific construct is intended first and foremost to be a drop-in replacement for the use of Column within Declarative mappings only, adding new ORM-specific convenience features such as the ability to establish mapped_column.deferred within the construct, and most importantly to indicate to typing tools such as Mypy and Pylance an accurate representation of how the attribute will behave at runtime at both the class level as well as the instance level. As will be seen in the following sections, it’s also at the forefront of a new annotation-driven configuration style introduced in SQLAlchemy 2.0.

Users of legacy code should be aware that the Column form will always work in Declarative in the same way it always has. The different forms of attribute mapping may also be mixed within a single mapping on an attribute by attribute basis, so migration to the new form can be at any pace. See the section ORM Declarative Models for a step by step guide to migrating a Declarative model to the new form.

The mapped_column() construct accepts all arguments that are accepted by the Column construct, as well as additional ORM-specific arguments. The mapped_column.__name positional parameter, indicating the name of the database column, is typically omitted, as the Declarative process will make use of the attribute name given to the construct and assign this as the name of the column (in the above example, this refers to the names id, name, fullname, nickname). Assigning an alternate mapped_column.__name is valid as well, where the resulting Column will use the given name in SQL and DDL statements, while the User mapped class will continue to allow access to the attribute using the attribute name given, independent of the name given to the column itself (more on this at Naming Declarative Mapped Columns Explicitly).

The mapped_column() construct is only valid within a Declarative class mapping. When constructing a Table object using Core as well as when using imperative table configuration, the Column construct is still required in order to indicate the presence of a database column.

Mapping Table Columns - contains additional notes on affecting how Mapper interprets incoming Column objects.

The mapped_column() construct in modern Python is normally augmented by the use of PEP 484 Python type annotations, where it is capable of deriving its column-configuration information from type annotations associated with the attribute as declared in the Declarative mapped class. These type annotations, if used, must be present within a special SQLAlchemy type called Mapped, which is a generic type that indicates a specific Python type within it.

Using this technique, the example in the previous section can be written more succinctly as below:

The example above demonstrates that if a class attribute is type-hinted with Mapped but doesn’t have an explicit mapped_column() assigned to it, SQLAlchemy will automatically create one. Furthermore, details like the column’s datatype and whether it can be null (nullability) are inferred from the Mapped annotation. However, you can always explicitly provide these arguments to mapped_column() to override these automatically-derived settings.

For complete details on using the ORM Annotated Declarative system, see ORM Annotated Declarative - Complete Guide later in this chapter.

ORM Annotated Declarative - Complete Guide - complete reference for ORM Annotated Declarative

The mapped_column() construct integrates with SQLAlchemy’s “native dataclasses” feature, discussed at Declarative Dataclass Mapping. See that section for current background on additional directives supported by mapped_column().

A declaratively mapped class will always include an attribute called __table__; when the above configuration using __tablename__ is complete, the declarative process makes the Table available via the __table__ attribute:

The above table is ultimately the same one that corresponds to the Mapper.local_table attribute, which we can see through the runtime inspection system:

The MetaData collection associated with both the declarative registry as well as the base class is frequently necessary in order to run DDL operations such as CREATE, as well as in use with migration tools such as Alembic. This object is available via the .metadata attribute of registry as well as the declarative base class. Below, for a small script we may wish to emit a CREATE for all tables against a SQLite database:

When using Declarative Table configuration with the __tablename__ declarative class attribute, additional arguments to be supplied to the Table constructor should be provided using the __table_args__ declarative class attribute.

This attribute accommodates both positional as well as keyword arguments that are normally sent to the Table constructor. The attribute can be specified in one of two forms. One is as a dictionary:

The other, a tuple, where each argument is positional (usually constraints):

Keyword arguments can be specified with the above form by specifying the last argument as a dictionary:

A class may also specify the __table_args__ declarative attribute, as well as the __tablename__ attribute, in a dynamic style using the declared_attr() method decorator. See Composing Mapped Hierarchies with Mixins for background.

The schema name for a Table as documented at Specifying the Schema Name is applied to an individual Table using the Table.schema argument. When using Declarative tables, this option is passed like any other to the __table_args__ dictionary:

The schema name can also be applied to all Table objects globally by using the MetaData.schema parameter documented at Specifying a Default Schema Name with MetaData. The MetaData object may be constructed separately and associated with a DeclarativeBase subclass by assigning to the metadata attribute directly:

Specifying the Schema Name - in the Describing Databases with MetaData documentation.

The mapped_column() construct accepts additional ORM-specific arguments that affect how the generated Column is mapped, affecting its load and persistence-time behavior. Options that are commonly used include:

deferred column loading - The mapped_column.deferred boolean establishes the Column using deferred column loading by default. In the example below, the User.bio column will not be loaded by default, but only when accessed:

Limiting which Columns Load with Column Deferral - full description of deferred column loading

active history - The mapped_column.active_history ensures that upon change of value for the attribute, the previous value will have been loaded and made part of the AttributeState.history collection when inspecting the history of the attribute. This may incur additional SQL statements:

See the docstring for mapped_column() for a list of supported parameters.

Applying Load, Persistence and Mapping Options for Imperative Table Columns - describes using column_property() and deferred() for use with Imperative Table configuration

All of the examples thus far feature the mapped_column() construct linked to an ORM mapped attribute, where the Python attribute name given to the mapped_column() is also that of the column as we see in CREATE TABLE statements as well as queries. The name for a column as expressed in SQL may be indicated by passing the string positional argument mapped_column.__name as the first positional argument. In the example below, the User class is mapped with alternate names given to the columns themselves:

Where above User.id resolves to a column named user_id and User.name resolves to a column named user_name. We may write a select() statement using our Python attribute names and will see the SQL names generated:

Alternate Attribute Names for Mapping Table Columns - applies to Imperative Table

A declarative table configuration allows the addition of new Column objects to an existing mapping after the Table metadata has already been generated.

For a declarative class that is declared using a declarative base class, the underlying metaclass DeclarativeMeta includes a __setattr__() method that will intercept additional mapped_column() or Core Column objects and add them to both the Table using Table.append_column() as well as to the existing Mapper using Mapper.add_property():

All arguments are supported including an alternate name, such as MyClass.some_new_column = mapped_column("some_name", String). However, the SQL type must be passed to the mapped_column() or Column object explicitly, as in the above examples where the String type is passed. There’s no capability for the Mapped annotation type to take part in the operation.

Additional Column objects may also be added to a mapping in the specific circumstance of using single table inheritance, where additional columns are present on mapped subclasses that have no Table of their own. This is illustrated in the section Single Table Inheritance.

Adding Relationships to Mapped Classes After Declaration - similar examples for relationship()

Assignment of mapped properties to an already mapped class will only function correctly if the “declarative base” class is used, meaning the user-defined subclass of DeclarativeBase or the dynamically generated class returned by declarative_base() or registry.generate_base(). This “base” class includes a Python metaclass which implements a special __setattr__() method that intercepts these operations.

Runtime assignment of class-mapped attributes to a mapped class will not work if the class is mapped using decorators like registry.mapped() or imperative functions like registry.map_imperatively().

The mapped_column() construct is capable of deriving its column-configuration information from PEP 484 type annotations associated with the attribute as declared in the Declarative mapped class. These type annotations, if used, must be present within a special SQLAlchemy type called Mapped, which is a generic type that then indicates a specific Python type within it.

Using this technique, the User example from previous sections may be written as below:

Above, when Declarative processes each class attribute, each mapped_column() will derive additional arguments from the corresponding Mapped type annotation on the left side, if present. Additionally, Declarative will generate an empty mapped_column() directive implicitly, whenever a Mapped type annotation is encountered that does not have a value assigned to the attribute (this form is inspired by the similar style used in Python dataclasses); this mapped_column() construct proceeds to derive its configuration from the Mapped annotation present.

The two qualities that mapped_column() derives from the Mapped annotation are:

datatype - the Python type given inside Mapped, as contained within the typing.Optional construct if present, is associated with a TypeEngine subclass such as Integer, String, DateTime, or Uuid, to name a few common types.

The datatype is determined based on a dictionary of Python type to SQLAlchemy datatype. This dictionary is completely customizable, as detailed in the next section Customizing the Type Map. The default type map is implemented as in the code example below:

If the mapped_column() construct indicates an explicit type as passed to the mapped_column.__type argument, then the given Python type is disregarded.

nullability - The mapped_column() construct will indicate its Column as NULL or NOT NULL first and foremost by the presence of the mapped_column.nullable parameter, passed either as True or False. Additionally , if the mapped_column.primary_key parameter is present and set to True, that will also imply that the column should be NOT NULL.

In the absence of both of these parameters, the presence of typing.Optional[] (or its equivalent) within the Mapped type annotation will be used to determine nullability, where typing.Optional[] means NULL, and the absence of typing.Optional[] means NOT NULL. If there is no Mapped[] annotation present at all, and there is no mapped_column.nullable or mapped_column.primary_key parameter, then SQLAlchemy’s usual default for Column of NULL is used.

In the example below, the id and data columns will be NOT NULL, and the additional_info column will be NULL:

It is also perfectly valid to have a mapped_column() whose nullability is different from what would be implied by the annotation. For example, an ORM mapped attribute may be annotated as allowing None within Python code that works with the object as it is first being created and populated, however the value will ultimately be written to a database column that is NOT NULL. The mapped_column.nullable parameter, when present, will always take precedence:

Similarly, a non-None attribute that’s written to a database column that for whatever reason needs to be NULL at the schema level, mapped_column.nullable may be set to True:

The mapping of Python types to SQLAlchemy TypeEngine types described in the previous section defaults to a hardcoded dictionary present in the sqlalchemy.sql.sqltypes module. However, the registry object that coordinates the Declarative mapping process will first consult a local, user defined dictionary of types which may be passed as the registry.type_annotation_map parameter when constructing the registry, which may be associated with the DeclarativeBase superclass when first used.

As an example, if we wish to make use of the BIGINT datatype for int, the TIMESTAMP datatype with timezone=True for datetime.datetime, and then for str types we’d like to see NVARCHAR when Microsoft SQL Server is used and VARCHAR(255) when MySQL is used, the registry and Declarative base could be configured as:

Below illustrates the CREATE TABLE statement generated for the above mapping, first on the Microsoft SQL Server backend, illustrating the NVARCHAR datatype:

On MySQL, we get a VARCHAR column with an explicit length (required by MySQL):

Then on the PostgreSQL backend, illustrating TIMESTAMP WITH TIME ZONE:

By making use of methods such as TypeEngine.with_variant(), we’re able to build up a type map that’s customized to what we need for different backends, while still being able to use succinct annotation-only mapped_column() configurations. There are two more levels of Python-type configurability available beyond this, described in the next two sections.

Changed in version 2.0.37: The features described in this section have been repaired and enhanced to work consistently. Prior to this change, union types were supported in type_annotation_map, however the feature exhibited inconsistent behaviors between union syntaxes as well as in how None was handled. Please ensure SQLAlchemy is up to date before attempting to use the features described in this section.

SQLAlchemy supports mapping union types inside the type_annotation_map to allow mapping database types that can support multiple Python types, such as JSON or JSONB:

The above example maps the union of list[int] and list[str] to the Postgresql JSONB datatype, while naming a union of float, str, bool will match to the JSON datatype. An equivalent union, stated in the Mapped construct, will match into the corresponding entry in the type map.

The matching of a union type is based on the contents of the union regardless of how the individual types are named, and additionally excluding the use of the None type. That is, json_scalar will also match to str | bool | float | None. It will not match to a union that is a subset or superset of this union; that is, str | bool would not match, nor would str | bool | float | int. The individual contents of the union excluding None must be an exact match.

The None value is never significant as far as matching from type_annotation_map to Mapped, however is significant as an indicator for nullability of the Column. When None is present in the union either as it is placed in the Mapped construct. When present in Mapped, it indicates the Column would be nullable, in the absence of more specific indicators. This logic works in the same way as indicating an Optional type as described at mapped_column() derives the datatype and nullability from the Mapped annotation.

The CREATE TABLE statement for the above mapping will look as below:

While union types use a “loose” matching approach that matches on any equivalent set of subtypes, Python typing also features a way to create “type aliases” that are treated as distinct types that are non-equivalent to another type that includes the same composition. Integration of these types with type_annotation_map is described in the next section, Support for Type Alias Types (defined by PEP 695) and NewType.

In contrast to the typing lookup described in Union types inside the Type Map, Python typing also includes two ways to create a composed type in a more formal way, using typing.NewType as well as the type keyword introduced in PEP 695. These types behave differently from ordinary type aliases (i.e. assigning a type to a variable name), and this difference is honored in how SQLAlchemy resolves these types from the type map.

Changed in version 2.0.44: Support for resolving pep-695 types without a corresponding entry in registry.type_annotation_map has been expanded, reversing part of the restrictions introduced in 2.0.37. Please ensure SQLAlchemy is up to date before attempting to use the features described in this section.

Changed in version 2.0.37: The behaviors described in this section for typing.NewType as well as PEP 695 type were formalized to disallow these types from being implicitly resolvable without entries in registry.type_annotation_map, with deprecation warnings emitted when these patterns were detected. As of 2.0.44, a pep-695 type is implicitly resolvable as long as the type it resolves to is present in the type map.

The typing module allows the creation of “new types” using typing.NewType:

The NewType construct creates types that are analogous to creating a subclass of the referenced type.

Additionally, PEP 695 introduced in Python 3.12 provides a new type keyword for creating type aliases with greater separation of concerns from plain aliases, as well as succinct support for generics without requiring explicit use of TypeVar or Generic elements. Types created by the type keyword are represented at runtime by typing.TypeAliasType:

Both NewType and pep-695 type constructs may be used as arguments within Mapped annotations, where they will be resolved to Python types using the following rules:

When a TypeAliasType or NewType object is present in the registry.type_annotation_map, it will resolve directly:

A TypeAliasType that refers directly to another type present in the type map will resolve against that type:

A TypeAliasType that refers to another pep-695 TypeAliasType not present in the type map will not resolve (emits a deprecation warning in 2.0), as this would involve a recursive lookup:

A NewType that is not in the type map will not resolve (emits a deprecation warning in 2.0). Since NewType is analogous to creating an entirely new type with different semantics than the type it extends, these must be explicitly matched in the type map:

For all of the above examples, any type that is combined with Optional[] or | None will consider this to indicate the column is nullable, if no other directive for nullability is present.

Mapping Whole Column Declarations to Generic Python Types

As individual Python types may be associated with TypeEngine configurations of any variety by using the registry.type_annotation_map parameter, an additional capability is the ability to associate a single Python type with different variants of a SQL type based on additional type qualifiers. One typical example of this is mapping the Python str datatype to VARCHAR SQL types of different lengths. Another is mapping different varieties of decimal.Decimal to differently sized NUMERIC columns.

Python’s typing system provides a great way to add additional metadata to a Python type which is by using the PEP 593 Annotated generic type, which allows additional information to be bundled along with a Python type. The mapped_column() construct will correctly interpret an Annotated object by identity when resolving it in the registry.type_annotation_map, as in the example below where we declare two variants of String and Numeric:

The Python type passed to the Annotated container, in the above example the str and Decimal types, is important only for the benefit of typing tools; as far as the mapped_column() construct is concerned, it will only need perform a lookup of each type object in the registry.type_annotation_map dictionary without actually looking inside of the Annotated object, at least in this particular context. Similarly, the arguments passed to Annotated beyond the underlying Python type itself are also not important, it’s only that at least one argument must be present for the Annotated construct to be valid. We can then use these augmented types directly in our mapping where they will be matched to the more specific type constructions, as in the following example:

a CREATE TABLE for the above mapping will illustrate the different variants of VARCHAR and NUMERIC we’ve configured, and looks like:

While variety in linking Annotated types to different SQL types grants us a wide degree of flexibility, the next section illustrates a second way in which Annotated may be used with Declarative that is even more open ended.

The previous section illustrated using PEP 593 Annotated type instances as keys within the registry.type_annotation_map dictionary. In this form, the mapped_column() construct does not actually look inside the Annotated object itself, it’s instead used only as a dictionary key. However, Declarative also has the ability to extract an entire pre-established mapped_column() construct from an Annotated object directly. Using this form, we can define not only different varieties of SQL datatypes linked to Python types without using the registry.type_annotation_map dictionary, we can also set up any number of arguments such as nullability, column defaults, and constraints in a reusable fashion.

A set of ORM models will usually have some kind of primary key style that is common to all mapped classes. There also may be common column configurations such as timestamps with defaults and other fields of pre-established sizes and configurations. We can compose these configurations into mapped_column() instances that we then bundle directly into instances of Annotated, which are then reused in any number of class declarations. Declarative will unpack an Annotated object when provided in this manner, skipping over any other directives that don’t apply to SQLAlchemy and searching only for SQLAlchemy ORM constructs.

The example below illustrates a variety of pre-configured field types used in this way, where we define intpk that represents an Integer primary key column, timestamp that represents a DateTime type which will use CURRENT_TIMESTAMP as a DDL level column default, and required_name which is a String of length 30 that’s NOT NULL:

The above Annotated objects can then be used directly within Mapped, where the pre-configured mapped_column() constructs will be extracted and copied to a new instance that will be specific to each attribute:

CREATE TABLE for our above mapping looks like:

When using Annotated types in this way, the configuration of the type may also be affected on a per-attribute basis. For the types in the above example that feature explicit use of mapped_column.nullable, we can apply the Optional[] generic modifier to any of our types so that the field is optional or not at the Python level, which will be independent of the NULL / NOT NULL setting that takes place in the database:

The mapped_column() construct is also reconciled with an explicitly passed mapped_column() construct, whose arguments will take precedence over those of the Annotated construct. Below we add a ForeignKey constraint to our integer primary key and also use an alternate server default for the created_at column:

The CREATE TABLE statement illustrates these per-attribute settings, adding a FOREIGN KEY constraint as well as substituting UTC_TIMESTAMP for CURRENT_TIMESTAMP:

The feature of mapped_column() just described, where a fully constructed set of column arguments may be indicated using PEP 593 Annotated objects that contain a “template” mapped_column() object to be copied into the attribute, is currently not implemented for other ORM constructs such as relationship() and composite(). While this functionality is in theory possible, for the moment attempting to use Annotated to indicate further arguments for relationship() and similar will raise a NotImplementedError exception at runtime, but may be implemented in future releases.

Using the Annotated approach from the previous section, we may also create a generic version that will apply particular mapped_column() elements across many different Python/SQL types in one step. Below illustrates a plain alias against a generic form of Annotated that will apply the primary_key=True option to any column to which it’s applied:

The above type can now apply primary_key=True to any Python type:

For a more shorthand approach, we may opt to use the PEP 695 type keyword (Python 3.12 or above) which allows us to skip having to define a TypeVar variable:

Added in version 2.0.44: Generic PEP 695 types may be used with PEP 593 Annotated elements to create generic types that automatically deliver mapped_column() arguments.

Added in version 2.0.0b4: - Added Enum support

Added in version 2.0.1: - Added Literal support

User-defined Python types which derive from the Python built-in enum.Enum as well as the typing.Literal class are automatically linked to the SQLAlchemy Enum datatype when used in an ORM declarative mapping. The example below uses a custom enum.Enum within the Mapped[] constructor:

In the above example, the mapped attribute SomeClass.status will be linked to a Column with the datatype of Enum(Status). We can see this for example in the CREATE TABLE output for the PostgreSQL database:

In a similar way, typing.Literal may be used instead, using a typing.Literal that consists of all strings:

The entries used in registry.type_annotation_map link the base enum.Enum Python type as well as the typing.Literal type to the SQLAlchemy Enum SQL type, using a special form which indicates to the Enum datatype that it should automatically configure itself against an arbitrary enumerated type. This configuration, which is implicit by default, would be indicated explicitly as:

The resolution logic within Declarative is able to resolve subclasses of enum.Enum as well as instances of typing.Literal to match the enum.Enum or typing.Literal entry in the registry.type_annotation_map dictionary. The Enum SQL type then knows how to produce a configured version of itself with the appropriate settings, including default string length. If a typing.Literal that does not consist of only string values is passed, an informative error is raised.

typing.TypeAliasType can also be used to create enums, by assigning them to a typing.Literal of strings:

Since this is a typing.TypeAliasType, it represents a unique type object, so it must be placed in the type_annotation_map for it to be looked up successfully, keyed to the Enum type as follows:

Since SQLAlchemy supports mapping different typing.TypeAliasType objects that are otherwise structurally equivalent individually, these must be present in type_annotation_map to avoid ambiguity.

The Enum.native_enum parameter refers to if the Enum datatype should create a so-called “native” enum, which on MySQL/MariaDB is the ENUM datatype and on PostgreSQL is a new TYPE object created by CREATE TYPE, or a “non-native” enum, which means that VARCHAR will be used to create the datatype. For backends other than MySQL/MariaDB or PostgreSQL, VARCHAR is used in all cases (third party dialects may have their own behaviors).

Because PostgreSQL’s CREATE TYPE requires that there’s an explicit name for the type to be created, special fallback logic exists when working with implicitly generated Enum without specifying an explicit Enum datatype within a mapping:

If the Enum is linked to an enum.Enum object, the Enum.native_enum parameter defaults to True and the name of the enum will be taken from the name of the enum.Enum datatype. The PostgreSQL backend will assume CREATE TYPE with this name.

If the Enum is linked to a typing.Literal object, the Enum.native_enum parameter defaults to False; no name is generated and VARCHAR is assumed.

To use typing.Literal with a PostgreSQL CREATE TYPE type, an explicit Enum must be used, either within the type map:

Or alternatively within mapped_column():

In order to modify the fixed configuration of the Enum datatype that’s generated implicitly, specify new entries in the registry.type_annotation_map, indicating additional arguments. For example, to use “non native enumerations” unconditionally, the Enum.native_enum parameter may be set to False for all types:

Changed in version 2.0.1: Implemented support for overriding parameters such as Enum.native_enum within the Enum datatype when establishing the registry.type_annotation_map. Previously, this functionality was not working.

To use a specific configuration for a specific enum.Enum subtype, such as setting the string length to 50 when using the example Status datatype:

By default Enum that are automatically generated are not associated with the MetaData instance used by the Base, so if the metadata defines a schema it will not be automatically associated with the enum. To automatically associate the enum with the schema in the metadata or table they belong to the Enum.inherit_schema can be set:

The above examples feature the use of an Enum that is automatically configuring itself to the arguments / attributes present on an enum.Enum or typing.Literal type object. For use cases where specific kinds of enum.Enum or typing.Literal should be linked to other types, these specific types may be placed in the type map also. In the example below, an entry for Literal[] that contains non-string types is linked to the JSON datatype:

In the above configuration, the my_literal datatype will resolve to a JSON instance. Other Literal variants will continue to resolve to Enum datatypes.

Declarative mappings may also be provided with a pre-existing Table object, or otherwise a Table or other arbitrary FromClause construct (such as a Join or Subquery) that is constructed separately.

This is referred to as a “hybrid declarative” mapping, as the class is mapped using the declarative style for everything involving the mapper configuration, however the mapped Table object is produced separately and passed to the declarative process directly:

Above, a Table object is constructed using the approach described at Describing Databases with MetaData. It can then be applied directly to a class that is declaratively mapped. The __tablename__ and __table_args__ declarative class attributes are not used in this form. The above configuration is often more readable as an inline definition:

A natural effect of the above style is that the __table__ attribute is itself defined within the class definition block. As such it may be immediately referenced within subsequent attributes, such as the example below which illustrates referring to the type column in a polymorphic mapper configuration:

The “imperative table” form is also used when a non-Table construct, such as a Join or Subquery object, is to be mapped. An example below:

For background on mapping to non-Table constructs see the sections Mapping a Class against Multiple Tables and Mapping a Class against Arbitrary Subqueries.

The “imperative table” form is of particular use when the class itself is using an alternative form of attribute declaration, such as Python dataclasses. See the section Applying ORM Mappings to an existing dataclass (legacy dataclass use) for detail.

Describing Databases with MetaData

Applying ORM Mappings to an existing dataclass (legacy dataclass use)

The section Naming Declarative Mapped Columns Explicitly illustrated how to use mapped_column() to provide a specific name for the generated Column object separate from the attribute name under which it is mapped.

When using Imperative Table configuration, we already have Column objects present. To map these to alternate names we may assign the Column to the desired attributes directly:

The User mapping above will refer to the "user_id" and "user_name" columns via the User.id and User.name attributes, in the same way as demonstrated at Naming Declarative Mapped Columns Explicitly.

One caveat to the above mapping is that the direct inline link to Column will not be typed correctly when using PEP 484 typing tools. A strategy to resolve this is to apply the Column objects within the column_property() function; while the Mapper already generates this property object for its internal use automatically, by naming it in the class declaration, typing tools will be able to match the attribute to the Mapped annotation:

Naming Declarative Mapped Columns Explicitly - applies to Declarative Table

The section Setting Load and Persistence Options for Declarative Mapped Columns reviewed how to set load and persistence options when using the mapped_column() construct with Declarative Table configuration. When using Imperative Table configuration, we already have existing Column objects that are mapped. In order to map these Column objects along with additional parameters that are specific to the ORM mapping, we may use the column_property() and deferred() constructs in order to associate additional parameters with the column. Options include:

deferred column loading - The deferred() function is shorthand for invoking column_property() with the column_property.deferred parameter set to True; this construct establishes the Column using deferred column loading by default. In the example below, the User.bio column will not be loaded by default, but only when accessed:

Limiting which Columns Load with Column Deferral - full description of deferred column loading

active history - The column_property.active_history ensures that upon change of value for the attribute, the previous value will have been loaded and made part of the AttributeState.history collection when inspecting the history of the attribute. This may incur additional SQL statements:

The column_property() construct is also important for cases where classes are mapped to alternative FROM clauses such as joins and selects. More background on these cases is at:

Mapping a Class against Multiple Tables

SQL Expressions as Mapped Attributes

For Declarative Table configuration with mapped_column(), most options are available directly; see the section Setting Load and Persistence Options for Declarative Mapped Columns for examples.

There are several patterns available which provide for producing mapped classes against a series of Table objects that were introspected from the database, using the reflection process described at Reflecting Database Objects.

A simple way to map a class to a table reflected from the database is to use a declarative hybrid mapping, passing the Table.autoload_with parameter to the constructor for Table:

A variant on the above pattern that scales for many tables is to use the MetaData.reflect() method to reflect a full set of Table objects at once, then refer to them from the MetaData:

One caveat to the approach of using __table__ is that the mapped classes cannot be declared until the tables have been reflected, which requires the database connectivity source to be present while the application classes are being declared; it’s typical that classes are declared as the modules of an application are being imported, but database connectivity isn’t available until the application starts running code so that it can consume configuration information and create an engine. There are currently two approaches to working around this, described in the next two sections.

To accommodate the use case of declaring mapped classes where reflection of table metadata can occur afterwards, a simple extension called the DeferredReflection mixin is available, which alters the declarative mapping process to be delayed until a special class-level DeferredReflection.prepare() method is called, which will perform the reflection process against a target database, and will integrate the results with the declarative table mapping process, that is, classes which use the __tablename__ attribute:

Above, we create a mixin class Reflected that will serve as a base for classes in our declarative hierarchy that should become mapped when the Reflected.prepare method is called. The above mapping is not complete until we do so, given an Engine:

The purpose of the Reflected class is to define the scope at which classes should be reflectively mapped. The plugin will search among the subclass tree of the target against which .prepare() is called and reflect all tables which are named by declared classes; tables in the target database that are not part of mappings and are not related to the target tables via foreign key constraint will not be reflected.

A more automated solution to mapping against an existing database where table reflection is to be used is to use the Automap extension. This extension will generate entire mapped classes from a database schema, including relationships between classes based on observed foreign key constraints. While it includes hooks for customization, such as hooks that allow custom class naming and relationship naming schemes, automap is oriented towards an expedient zero-configuration style of working. If an application wishes to have a fully explicit model that makes use of table reflection, the DeferredReflection class may be preferable for its less automated approach.

When using any of the previous reflection techniques, we have the option to change the naming scheme by which columns are mapped. The Column object includes a parameter Column.key which is a string name that determines under what name this Column will be present in the Table.c collection, independently of the SQL name of the column. This key is also used by Mapper as the attribute name under which the Column will be mapped, if not supplied through other means such as that illustrated at Alternate Attribute Names for Mapping Table Columns.

When working with table reflection, we can intercept the parameters that will be used for Column as they are received using the DDLEvents.column_reflect() event and apply whatever changes we need, including the .key attribute but also things like datatypes.

The event hook is most easily associated with the MetaData object that’s in use as illustrated below:

With the above event, the reflection of Column objects will be intercepted with our event that adds a new “.key” element, such as in a mapping as below:

The approach also works with both the DeferredReflection base class as well as with the Automap extension. For automap specifically, see the section Intercepting Column Definitions for background.

Mapping Declaratively with Reflected Tables

DDLEvents.column_reflect()

Intercepting Column Definitions - in the Automap documentation

The Mapper construct in order to successfully map a table always requires that at least one column be identified as the “primary key” for that selectable. This is so that when an ORM object is loaded or persisted, it can be placed in the identity map with an appropriate identity key.

In those cases where a reflected table to be mapped does not include a primary key constraint, as well as in the general case for mapping against arbitrary selectables where primary key columns might not be present, the Mapper.primary_key parameter is provided so that any set of columns may be configured as the “primary key” for the table, as far as ORM mapping is concerned.

Given the following example of an Imperative Table mapping against an existing Table object where the table does not have any declared primary key (as may occur in reflection scenarios), we may map such a table as in the following example:

Above, the group_users table is an association table of some kind with string columns user_id and group_id, but no primary key is set up; instead, there is only a UniqueConstraint establishing that the two columns represent a unique key. The Mapper does not automatically inspect unique constraints for primary keys; instead, we make use of the Mapper.primary_key parameter, passing a collection of [group_users.c.user_id, group_users.c.group_id], indicating that these two columns should be used in order to construct the identity key for instances of the GroupUsers class.

Sometimes table reflection may provide a Table with many columns that are not important for our needs and may be safely ignored. For such a table that has lots of columns that don’t need to be referenced in the application, the Mapper.include_properties or Mapper.exclude_properties parameters can indicate a subset of columns to be mapped, where other columns from the target Table will not be considered by the ORM in any way. Example:

In the above example, the User class will map to the user_table table, only including the user_id and user_name columns - the rest are not referenced.

will map the Address class to the address_table table, including all columns present except street, city, state, and zip.

As indicated in the two examples, columns may be referenced either by string name or by referring to the Column object directly. Referring to the object directly may be useful for explicitness as well as to resolve ambiguities when mapping to multi-table constructs that might have repeated names:

When columns are not included in a mapping, these columns will not be referenced in any SELECT statements emitted when executing select() or legacy Query objects, nor will there be any mapped attribute on the mapped class which represents the column; assigning an attribute of that name will have no effect beyond that of a normal Python attribute assignment.

However, it is important to note that schema level column defaults WILL still be in effect for those Column objects that include them, even though they may be excluded from the ORM mapping.

“Schema level column defaults” refers to the defaults described at Column INSERT/UPDATE Defaults including those configured by the Column.default, Column.onupdate, Column.server_default and Column.server_onupdate parameters. These constructs continue to have normal effects because in the case of Column.default and Column.onupdate, the Column object is still present on the underlying Table, thus allowing the default functions to take place when the ORM emits an INSERT or UPDATE, and in the case of Column.server_default and Column.server_onupdate, the relational database itself emits these defaults as a server side behavior.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (php):
```php
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
```

Example 2 (python):
```python
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50), nullable=False)
    fullname = mapped_column(String)
    nickname = mapped_column(String(30))
```

Example 3 (markdown):
```markdown
# equivalent Table object produced
user_table = Table(
    "user",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("fullname", String()),
    Column("nickname", String(30)),
)
```

Example 4 (python):
```python
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    fullname: Mapped[str | None]
    nickname: Mapped[str | None] = mapped_column(String(30))
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/declarative_config.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Mapper Configuration with Declarative¶
- Defining Mapped Properties with Declarative¶
- Mapper Configuration Options with Declarative¶
  - Constructing mapper arguments dynamically¶
- Other Declarative Mapping Directives¶
  - __declare_last__()¶

Home | Download this Documentation

Home | Download this Documentation

The section Mapped Class Essential Components discusses the general configurational elements of a Mapper construct, which is the structure that defines how a particular user defined class is mapped to a database table or other SQL construct. The following sections describe specific details about how the declarative system goes about constructing the Mapper.

The examples given at Table Configuration with Declarative illustrate mappings against table-bound columns, using the mapped_column() construct. There are several other varieties of ORM mapped constructs that may be configured besides table-bound columns, the most common being the relationship() construct. Other kinds of properties include SQL expressions that are defined using the column_property() construct and multiple-column mappings using the composite() construct.

While an imperative mapping makes use of the properties dictionary to establish all the mapped class attributes, in the declarative mapping, these properties are all specified inline with the class definition, which in the case of a declarative table mapping are inline with the Column objects that will be used to generate a Table object.

Working with the example mapping of User and Address, we may illustrate a declarative table mapping that includes not just mapped_column() objects but also relationships and SQL expressions:

The above declarative table mapping features two tables, each with a relationship() referring to the other, as well as a simple SQL expression mapped by column_property(), and an additional mapped_column() that indicates loading should be on a “deferred” basis as defined by the mapped_column.deferred keyword. More documentation on these particular concepts may be found at Basic Relationship Patterns, Using column_property, and Limiting which Columns Load with Column Deferral.

Properties may be specified with a declarative mapping as above using “hybrid table” style as well; the Column objects that are directly part of a table move into the Table definition but everything else, including composed SQL expressions, would still be inline with the class definition. Constructs that need to refer to a Column directly would reference it in terms of the Table object. To illustrate the above mapping using hybrid table style:

Things to note above:

The address Table contains a column called address_statistics, however we re-map this column under the same attribute name to be under the control of a deferred() construct.

With both declararative table and hybrid table mappings, when we define a ForeignKey construct, we always name the target table using the table name, and not the mapped class name.

When we define relationship() constructs, as these constructs create a linkage between two mapped classes where one necessarily is defined before the other, we can refer to the remote class using its string name. This functionality also extends into the area of other arguments specified on the relationship() such as the “primary join” and “order by” arguments. See the section Late-Evaluation of Relationship Arguments for details on this.

With all mapping forms, the mapping of the class is configured through parameters that become part of the Mapper object. The function which ultimately receives these arguments is the Mapper function, and are delivered to it from one of the front-facing mapping functions defined on the registry object.

For the declarative form of mapping, mapper arguments are specified using the __mapper_args__ declarative class variable, which is a dictionary that is passed as keyword arguments to the Mapper function. Some examples:

Map Specific Primary Key Columns

The example below illustrates Declarative-level settings for the Mapper.primary_key parameter, which establishes particular columns as part of what the ORM should consider to be a primary key for the class, independently of schema-level primary key constraints:

Mapping to an Explicit Set of Primary Key Columns - further background on ORM mapping of explicit columns as primary key columns

The example below illustrates Declarative-level settings for the Mapper.version_id_col and Mapper.version_id_generator parameters, which configure an ORM-maintained version counter that is updated and checked within the unit of work flush process:

Configuring a Version Counter - background on the ORM version counter feature

Single Table Inheritance

The example below illustrates Declarative-level settings for the Mapper.polymorphic_on and Mapper.polymorphic_identity parameters, which are used when configuring a single-table inheritance mapping:

Single Table Inheritance - background on the ORM single table inheritance mapping feature.

The __mapper_args__ dictionary may be generated from a class-bound descriptor method rather than from a fixed dictionary by making use of the declared_attr() construct. This is useful to create arguments for mappers that are programmatically derived from the table configuration or other aspects of the mapped class. A dynamic __mapper_args__ attribute will typically be useful when using a Declarative Mixin or abstract base class.

For example, to omit from the mapping any columns that have a special Column.info value, a mixin can use a __mapper_args__ method that scans for these columns from the cls.__table__ attribute and passes them to the Mapper.exclude_properties collection:

Above, the ExcludeColsWFlag mixin provides a per-class __mapper_args__ hook that will scan for Column objects that include the key/value 'exclude': True passed to the Column.info parameter, and then add their string “key” name to the Mapper.exclude_properties collection which will prevent the resulting Mapper from considering these columns for any SQL operations.

Composing Mapped Hierarchies with Mixins

The __declare_last__() hook allows definition of a class level function that is automatically called by the MapperEvents.after_configured() event, which occurs after mappings are assumed to be completed and the ‘configure’ step has finished:

Like __declare_last__(), but is called at the beginning of mapper configuration via the MapperEvents.before_configured() event:

The MetaData collection normally used to assign a new Table is the registry.metadata attribute associated with the registry object in use. When using a declarative base class such as that produced by the DeclarativeBase superclass, as well as legacy functions such as declarative_base() and registry.generate_base(), this MetaData is also normally present as an attribute named .metadata that’s directly on the base class, and thus also on the mapped class via inheritance. Declarative uses this attribute, when present, in order to determine the target MetaData collection, or if not present, uses the MetaData associated directly with the registry.

This attribute may also be assigned towards in order to affect the MetaData collection to be used on a per-mapped-hierarchy basis for a single base and/or registry. This takes effect whether a declarative base class is used or if the registry.mapped() decorator is used directly, thus allowing patterns such as the metadata-per-abstract base example in the next section, __abstract__. A similar pattern can be illustrated using registry.mapped() as follows:

__abstract__ causes declarative to skip the production of a table or mapper for the class entirely. A class can be added within a hierarchy in the same way as mixin (see Mixin and Custom Base Classes), allowing subclasses to extend just from the special class:

One possible use of __abstract__ is to use a distinct MetaData for different bases:

Above, classes which inherit from DefaultBase will use one MetaData as the registry of tables, and those which inherit from OtherBase will use a different one. The tables themselves can then be created perhaps within distinct databases:

Building Deeper Hierarchies with polymorphic_abstract - an alternative form of “abstract” mapped class that is appropriate for inheritance hierarchies.

Allows the callable / class used to generate a Table to be customized. This is a very open-ended hook that can allow special customizations to a Table that one generates here:

The above mixin would cause all Table objects generated to include the prefix "my_", followed by the name normally specified using the __tablename__ attribute.

__table_cls__ also supports the case of returning None, which causes the class to be considered as single-table inheritance vs. its subclass. This may be useful in some customization schemes to determine that single-table inheritance should take place based on the arguments for the table itself, such as, define as single-inheritance if there is no primary key present:

The above Employee class would be mapped as single-table inheritance against Person; the employee_name column would be added as a member of the Person table.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from typing import List
from typing import Optional

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import column_property
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    fullname: Mapped[str] = column_property(firstname + " " + lastname)

    addresses: Mapped[List["Address"]] = relationship(back_populates="user")


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    email_address: Mapped[str]
    address_statistics: Mapped[Optional[str]] = mapped_column(Text, deferred=True)

    user: Mapped["User"] = relationship(back_populates="addresses")
```

Example 2 (python):
```python
# mapping attributes using declarative with imperative table
# i.e. __table__

from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import column_property
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import deferred
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __table__ = Table(
        "user",
        Base.metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String),
        Column("firstname", String(50)),
        Column("lastname", String(50)),
    )

    fullname = column_property(__table__.c.firstname + " " + __table__.c.lastname)

    addresses = relationship("Address", back_populates="user")


class Address(Base):
    __table__ = Table(
        "address",
        Base.metadata,
        Column("id", Integer, primary_key=True),
        Column("user_id", ForeignKey("user.id")),
        Column("email_address", String),
        Column("address_statistics", Text),
    )

    address_statistics = deferred(__table__.c.address_statistics)

    user = relationship("User", back_populates="addresses")
```

Example 3 (json):
```json
class GroupUsers(Base):
    __tablename__ = "group_users"

    user_id = mapped_column(String(40))
    group_id = mapped_column(String(40))

    __mapper_args__ = {"primary_key": [user_id, group_id]}
```

Example 4 (python):
```python
from datetime import datetime


class Widget(Base):
    __tablename__ = "widgets"

    id = mapped_column(Integer, primary_key=True)
    timestamp = mapped_column(DateTime, nullable=False)

    __mapper_args__ = {
        "version_id_col": timestamp,
        "version_id_generator": lambda v: datetime.now(),
    }
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/inheritance.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Mapping Class Inheritance Hierarchies¶
- Joined Table Inheritance¶
  - Relationships with Joined Inheritance¶
  - Loading Joined Inheritance Mappings¶
- Single Table Inheritance¶
  - Resolving Column Conflicts with use_existing_column¶

Home | Download this Documentation

Home | Download this Documentation

SQLAlchemy supports three forms of inheritance:

single table inheritance – several types of classes are represented by a single table;

concrete table inheritance – each type of class is represented by independent tables;

joined table inheritance – the class hierarchy is broken up among dependent tables. Each class represented by its own table that only includes those attributes local to that class.

The most common forms of inheritance are single and joined table, while concrete inheritance presents more configurational challenges.

When mappers are configured in an inheritance relationship, SQLAlchemy has the ability to load elements polymorphically, meaning that a single query can return objects of multiple types.

Writing SELECT statements for Inheritance Mappings - in the ORM Querying Guide

Inheritance Mapping Recipes - complete examples of joined, single and concrete inheritance

In joined table inheritance, each class along a hierarchy of classes is represented by a distinct table. Querying for a particular subclass in the hierarchy will render as a SQL JOIN along all tables in its inheritance path. If the queried class is the base class, the base table is queried instead, with options to include other tables at the same time or to allow attributes specific to sub-tables to load later.

In all cases, the ultimate class to instantiate for a given row is determined by a discriminator column or SQL expression, defined on the base class, which will yield a scalar value that is associated with a particular subclass.

The base class in a joined inheritance hierarchy is configured with additional arguments that will indicate to the polymorphic discriminator column, and optionally a polymorphic identifier for the base class itself:

In the above example, the discriminator is the type column, whichever is configured using the Mapper.polymorphic_on parameter. This parameter accepts a column-oriented expression, specified either as a string name of the mapped attribute to use or as a column expression object such as Column or mapped_column() construct.

The discriminator column will store a value which indicates the type of object represented within the row. The column may be of any datatype, though string and integer are the most common. The actual data value to be applied to this column for a particular row in the database is specified using the Mapper.polymorphic_identity parameter, described below.

While a polymorphic discriminator expression is not strictly necessary, it is required if polymorphic loading is desired. Establishing a column on the base table is the easiest way to achieve this, however very sophisticated inheritance mappings may make use of SQL expressions, such as a CASE expression, as the polymorphic discriminator.

Currently, only one discriminator column or SQL expression may be configured for the entire inheritance hierarchy, typically on the base- most class in the hierarchy. “Cascading” polymorphic discriminator expressions are not yet supported.

We next define Engineer and Manager subclasses of Employee. Each contains columns that represent the attributes unique to the subclass they represent. Each table also must contain a primary key column (or columns), as well as a foreign key reference to the parent table:

In the above example, each mapping specifies the Mapper.polymorphic_identity parameter within its mapper arguments. This value populates the column designated by the Mapper.polymorphic_on parameter established on the base mapper. The Mapper.polymorphic_identity parameter should be unique to each mapped class across the whole hierarchy, and there should only be one “identity” per mapped class; as noted above, “cascading” identities where some subclasses introduce a second identity are not supported.

The ORM uses the value set up by Mapper.polymorphic_identity in order to determine which class a row belongs towards when loading rows polymorphically. In the example above, every row which represents an Employee will have the value 'employee' in its type column; similarly, every Engineer will get the value 'engineer', and each Manager will get the value 'manager'. Regardless of whether the inheritance mapping uses distinct joined tables for subclasses as in joined table inheritance, or all one table as in single table inheritance, this value is expected to be persisted and available to the ORM when querying. The Mapper.polymorphic_identity parameter also applies to concrete table inheritance, but is not actually persisted; see the later section at Concrete Table Inheritance for details.

In a polymorphic setup, it is most common that the foreign key constraint is established on the same column or columns as the primary key itself, however this is not required; a column distinct from the primary key may also be made to refer to the parent via foreign key. The way that a JOIN is constructed from the base table to subclasses is also directly customizable, however this is rarely necessary.

Joined inheritance primary keys

One natural effect of the joined table inheritance configuration is that the identity of any mapped object can be determined entirely from rows in the base table alone. This has obvious advantages, so SQLAlchemy always considers the primary key columns of a joined inheritance class to be those of the base table only. In other words, the id columns of both the engineer and manager tables are not used to locate Engineer or Manager objects - only the value in employee.id is considered. engineer.id and manager.id are still of course critical to the proper operation of the pattern overall as they are used to locate the joined row, once the parent row has been determined within a statement.

With the joined inheritance mapping complete, querying against Employee will return a combination of Employee, Engineer and Manager objects. Newly saved Engineer, Manager, and Employee objects will automatically populate the employee.type column with the correct “discriminator” value in this case "engineer", "manager", or "employee", as appropriate.

Relationships are fully supported with joined table inheritance. The relationship involving a joined-inheritance class should target the class in the hierarchy that also corresponds to the foreign key constraint; below, as the employee table has a foreign key constraint back to the company table, the relationships are set up between Company and Employee:

If the foreign key constraint is on a table corresponding to a subclass, the relationship should target that subclass instead. In the example below, there is a foreign key constraint from manager to company, so the relationships are established between the Manager and Company classes:

Above, the Manager class will have a Manager.company attribute; Company will have a Company.managers attribute that always loads against a join of the employee and manager tables together.

See the section Writing SELECT statements for Inheritance Mappings for background on inheritance loading techniques, including configuration of tables to be queried both at mapper configuration time as well as query time.

Single table inheritance represents all attributes of all subclasses within a single table. A particular subclass that has attributes unique to that class will persist them within columns in the table that are otherwise NULL if the row refers to a different kind of object.

Querying for a particular subclass in the hierarchy will render as a SELECT against the base table, which will include a WHERE clause that limits rows to those with a particular value or values present in the discriminator column or expression.

Single table inheritance has the advantage of simplicity compared to joined table inheritance; queries are much more efficient as only one table needs to be involved in order to load objects of every represented class.

Single-table inheritance configuration looks much like joined-table inheritance, except only the base class specifies __tablename__. A discriminator column is also required on the base table so that classes can be differentiated from each other.

Even though subclasses share the base table for all of their attributes, when using Declarative, mapped_column objects may still be specified on subclasses, indicating that the column is to be mapped only to that subclass; the mapped_column will be applied to the same base Table object:

Note that the mappers for the derived classes Manager and Engineer omit the __tablename__, indicating they do not have a mapped table of their own. Additionally, a mapped_column() directive with nullable=True is included; as the Python types declared for these classes do not include Optional[], the column would normally be mapped as NOT NULL, which would not be appropriate as this column only expects to be populated for those rows that correspond to that particular subclass.

Note in the previous section that the manager_name and engineer_info columns are “moved up” to be applied to Employee.__table__, as a result of their declaration on a subclass that has no table of its own. A tricky case comes up when two subclasses want to specify the same column, as below:

Above, the start_date column declared on both Engineer and Manager will result in an error:

The above scenario presents an ambiguity to the Declarative mapping system that may be resolved by using the mapped_column.use_existing_column parameter on mapped_column(), which instructs mapped_column() to look on the inheriting superclass present and use the column that’s already mapped, if already present, else to map a new column:

Above, when Manager is mapped, the start_date column is already present on the Employee class, having been provided by the Engineer mapping already. The mapped_column.use_existing_column parameter indicates to mapped_column() that it should look for the requested Column on the mapped Table for Employee first, and if present, maintain that existing mapping. If not present, mapped_column() will map the column normally, adding it as one of the columns in the Table referenced by the Employee superclass.

Added in version 2.0.0b4: - Added mapped_column.use_existing_column, which provides a 2.0-compatible means of mapping a column on an inheriting subclass conditionally. The previous approach which combines declared_attr with a lookup on the parent .__table__ continues to function as well, but lacks PEP 484 typing support.

A similar concept can be used with mixin classes (see Composing Mapped Hierarchies with Mixins) to define a particular series of columns and/or other mapped attributes from a reusable mixin class:

Relationships are fully supported with single table inheritance. Configuration is done in the same manner as that of joined inheritance; a foreign key attribute should be on the same class that’s the “foreign” side of the relationship:

Also, like the case of joined inheritance, we can create relationships that involve a specific subclass. When queried, the SELECT statement will include a WHERE clause that limits the class selection to that subclass or subclasses:

Above, the Manager class will have a Manager.company attribute; Company will have a Company.managers attribute that always loads against the employee with an additional WHERE clause that limits rows to those with type = 'manager'.

Added in version 2.0.

When building any kind of inheritance hierarchy, a mapped class may include the Mapper.polymorphic_abstract parameter set to True, which indicates that the class should be mapped normally, however would not expect to be instantiated directly and would not include a Mapper.polymorphic_identity. Subclasses may then be declared as subclasses of this mapped class, which themselves can include a Mapper.polymorphic_identity and therefore be used normally. This allows a series of subclasses to be referenced at once by a common base class which is considered to be “abstract” within the hierarchy, both in queries as well as in relationship() declarations. This use differs from the use of the __abstract__ attribute with Declarative, which leaves the target class entirely unmapped and thus not usable as a mapped class by itself. Mapper.polymorphic_abstract may be applied to any class or classes at any level in the hierarchy, including on multiple levels at once.

As an example, suppose Manager and Principal were both to be classified against a superclass Executive, and Engineer and Sysadmin were classified against a superclass Technologist. Neither Executive or Technologist is ever instantiated, therefore have no Mapper.polymorphic_identity. These classes can be configured using Mapper.polymorphic_abstract as follows:

In the above example, the new classes Technologist and Executive are ordinary mapped classes, and also indicate new columns to be added to the superclass called executive_background and competencies. However, they both lack a setting for Mapper.polymorphic_identity; this is because it’s not expected that Technologist or Executive would ever be instantiated directly; we’d always have one of Manager, Principal, Engineer or SysAdmin. We can however query for Principal and Technologist roles, as well as have them be targets of relationship(). The example below demonstrates a SELECT statement for Technologist objects:

The Technologist and Executive abstract mapped classes may also be made the targets of relationship() mappings, like any other mapped class. We can extend the above example to include Company, with separate collections Company.technologists and Company.principals:

Using the above mapping we can use joins and relationship loading techniques across Company.technologists and Company.executives individually:

__abstract__ - Declarative parameter which allows a Declarative class to be completely un-mapped within a hierarchy, while still extending from a mapped superclass.

The loading techniques for single-table inheritance are mostly identical to those used for joined-table inheritance, and a high degree of abstraction is provided between these two mapping types such that it is easy to switch between them as well as to intermix them in a single hierarchy (just omit __tablename__ from whichever subclasses are to be single-inheriting). See the sections Writing SELECT statements for Inheritance Mappings and SELECT Statements for Single Inheritance Mappings for documentation on inheritance loading techniques, including configuration of classes to be queried both at mapper configuration time as well as query time.

Concrete inheritance maps each subclass to its own distinct table, each of which contains all columns necessary to produce an instance of that class. A concrete inheritance configuration by default queries non-polymorphically; a query for a particular class will only query that class’ table and only return instances of that class. Polymorphic loading of concrete classes is enabled by configuring within the mapper a special SELECT that typically is produced as a UNION of all the tables.

Concrete table inheritance is much more complicated than joined or single table inheritance, and is much more limited in functionality especially pertaining to using it with relationships, eager loading, and polymorphic loading. When used polymorphically it produces very large queries with UNIONS that won’t perform as well as simple joins. It is strongly advised that if flexibility in relationship loading and polymorphic loading is required, that joined or single table inheritance be used if at all possible. If polymorphic loading isn’t required, then plain non-inheriting mappings can be used if each class refers to its own table completely.

Whereas joined and single table inheritance are fluent in “polymorphic” loading, it is a more awkward affair in concrete inheritance. For this reason, concrete inheritance is more appropriate when polymorphic loading is not required. Establishing relationships that involve concrete inheritance classes is also more awkward.

To establish a class as using concrete inheritance, add the Mapper.concrete parameter within the __mapper_args__. This indicates to Declarative as well as the mapping that the superclass table should not be considered as part of the mapping:

Two critical points should be noted:

We must define all columns explicitly on each subclass, even those of the same name. A column such as Employee.name here is not copied out to the tables mapped by Manager or Engineer for us.

while the Engineer and Manager classes are mapped in an inheritance relationship with Employee, they still do not include polymorphic loading. Meaning, if we query for Employee objects, the manager and engineer tables are not queried at all.

Polymorphic loading with concrete inheritance requires that a specialized SELECT is configured against each base class that should have polymorphic loading. This SELECT needs to be capable of accessing all the mapped tables individually, and is typically a UNION statement that is constructed using a SQLAlchemy helper polymorphic_union().

As discussed in Writing SELECT statements for Inheritance Mappings, mapper inheritance configurations of any type can be configured to load from a special selectable by default using the Mapper.with_polymorphic argument. Current public API requires that this argument is set on a Mapper when it is first constructed.

However, in the case of Declarative, both the mapper and the Table that is mapped are created at once, the moment the mapped class is defined. This means that the Mapper.with_polymorphic argument cannot be provided yet, since the Table objects that correspond to the subclasses haven’t yet been defined.

There are a few strategies available to resolve this cycle, however Declarative provides helper classes ConcreteBase and AbstractConcreteBase which handle this issue behind the scenes.

Using ConcreteBase, we can set up our concrete mapping in almost the same way as we do other forms of inheritance mappings:

Above, Declarative sets up the polymorphic selectable for the Employee class at mapper “initialization” time; this is the late-configuration step for mappers that resolves other dependent mappers. The ConcreteBase helper uses the polymorphic_union() function to create a UNION of all concrete-mapped tables after all the other classes are set up, and then configures this statement with the already existing base-class mapper.

Upon select, the polymorphic union produces a query like this:

The above UNION query needs to manufacture “NULL” columns for each subtable in order to accommodate for those columns that aren’t members of that particular subclass.

The concrete mappings illustrated thus far show both the subclasses as well as the base class mapped to individual tables. In the concrete inheritance use case, it is common that the base class is not represented within the database, only the subclasses. In other words, the base class is “abstract”.

Normally, when one would like to map two different subclasses to individual tables, and leave the base class unmapped, this can be achieved very easily. When using Declarative, just declare the base class with the __abstract__ indicator:

Above, we are not actually making use of SQLAlchemy’s inheritance mapping facilities; we can load and persist instances of Manager and Engineer normally. The situation changes however when we need to query polymorphically, that is, we’d like to emit select(Employee) and get back a collection of Manager and Engineer instances. This brings us back into the domain of concrete inheritance, and we must build a special mapper against Employee in order to achieve this.

To modify our concrete inheritance example to illustrate an “abstract” base that is capable of polymorphic loading, we will have only an engineer and a manager table and no employee table, however the Employee mapper will be mapped directly to the “polymorphic union”, rather than specifying it locally to the Mapper.with_polymorphic parameter.

To help with this, Declarative offers a variant of the ConcreteBase class called AbstractConcreteBase which achieves this automatically:

Above, the registry.configure() method is invoked, which will trigger the Employee class to be actually mapped; before the configuration step, the class has no mapping as the sub-tables which it will query from have not yet been defined. This process is more complex than that of ConcreteBase, in that the entire mapping of the base class must be delayed until all the subclasses have been declared. With a mapping like the above, only instances of Manager and Engineer may be persisted; querying against the Employee class will always produce Manager and Engineer objects.

Using the above mapping, queries can be produced in terms of the Employee class and any attributes that are locally declared upon it, such as the Employee.name:

The AbstractConcreteBase.strict_attrs parameter indicates that the Employee class should directly map only those attributes which are local to the Employee class, in this case the Employee.name attribute. Other attributes such as Manager.manager_data and Engineer.engineer_info are present only on their corresponding subclass. When AbstractConcreteBase.strict_attrs is not set, then all subclass attributes such as Manager.manager_data and Engineer.engineer_info get mapped onto the base Employee class. This is a legacy mode of use which may be more convenient for querying but has the effect that all subclasses share the full set of attributes for the whole hierarchy; in the above example, not using AbstractConcreteBase.strict_attrs would have the effect of generating non-useful Engineer.manager_name and Manager.engineer_info attributes.

Added in version 2.0: Added AbstractConcreteBase.strict_attrs parameter to AbstractConcreteBase which produces a cleaner mapping; the default is False to allow legacy mappings to continue working as they did in 1.x versions.

The Declarative configurations illustrated with ConcreteBase and AbstractConcreteBase are equivalent to two other forms of configuration that make use of polymorphic_union() explicitly. These configurational forms make use of the Table object explicitly so that the “polymorphic union” can be created first, then applied to the mappings. These are illustrated here to clarify the role of the polymorphic_union() function in terms of mapping.

A semi-classical mapping for example makes use of Declarative, but establishes the Table objects separately:

Next, the UNION is produced using polymorphic_union():

With the above Table objects, the mappings can be produced using “semi-classical” style, where we use Declarative in conjunction with the __table__ argument; our polymorphic union above is passed via __mapper_args__ to the Mapper.with_polymorphic parameter:

Alternatively, the same Table objects can be used in fully “classical” style, without using Declarative at all. A constructor similar to that supplied by Declarative is illustrated:

The “abstract” example can also be mapped using “semi-classical” or “classical” style. The difference is that instead of applying the “polymorphic union” to the Mapper.with_polymorphic parameter, we apply it directly as the mapped selectable on our basemost mapper. The semi-classical mapping is illustrated below:

Above, we use polymorphic_union() in the same manner as before, except that we omit the employee table.

Imperative Mapping - background information on imperative, or “classical” mappings

In a concrete inheritance scenario, mapping relationships is challenging since the distinct classes do not share a table. If the relationships only involve specific classes, such as a relationship between Company in our previous examples and Manager, special steps aren’t needed as these are just two related tables.

However, if Company is to have a one-to-many relationship to Employee, indicating that the collection may include both Engineer and Manager objects, that implies that Employee must have polymorphic loading capabilities and also that each table to be related must have a foreign key back to the company table. An example of such a configuration is as follows:

The next complexity with concrete inheritance and relationships involves when we’d like one or all of Employee, Manager and Engineer to themselves refer back to Company. For this case, SQLAlchemy has special behavior in that a relationship() placed on Employee which links to Company does not work against the Manager and Engineer classes, when exercised at the instance level. Instead, a distinct relationship() must be applied to each class. In order to achieve bi-directional behavior in terms of three separate relationships which serve as the opposite of Company.employees, the relationship.back_populates parameter is used between each of the relationships:

The above limitation is related to the current implementation, including that concrete inheriting classes do not share any of the attributes of the superclass and therefore need distinct relationships to be set up.

The options for loading with concrete inheritance are limited; generally, if polymorphic loading is configured on the mapper using one of the declarative concrete mixins, it can’t be modified at query time in current SQLAlchemy versions. Normally, the with_polymorphic() function would be able to override the style of loading used by concrete, however due to current limitations this is not yet supported.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Employee(Base):
    __tablename__ = "employee"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    type: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": "employee",
        "polymorphic_on": "type",
    }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r})"
```

Example 2 (json):
```json
class Engineer(Employee):
    __tablename__ = "engineer"
    id: Mapped[int] = mapped_column(ForeignKey("employee.id"), primary_key=True)
    engineer_name: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": "engineer",
    }


class Manager(Employee):
    __tablename__ = "manager"
    id: Mapped[int] = mapped_column(ForeignKey("employee.id"), primary_key=True)
    manager_name: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": "manager",
    }
```

Example 3 (python):
```python
from __future__ import annotations

from sqlalchemy.orm import relationship


class Company(Base):
    __tablename__ = "company"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    employees: Mapped[List[Employee]] = relationship(back_populates="company")


class Employee(Base):
    __tablename__ = "employee"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    type: Mapped[str]
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    company: Mapped[Company] = relationship(back_populates="employees")

    __mapper_args__ = {
        "polymorphic_identity": "employee",
        "polymorphic_on": "type",
    }


class Manager(Employee): ...


class Engineer(Employee): ...
```

Example 4 (json):
```json
class Company(Base):
    __tablename__ = "company"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    managers: Mapped[List[Manager]] = relationship(back_populates="company")


class Employee(Base):
    __tablename__ = "employee"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    type: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": "employee",
        "polymorphic_on": "type",
    }


class Manager(Employee):
    __tablename__ = "manager"
    id: Mapped[int] = mapped_column(ForeignKey("employee.id"), primary_key=True)
    manager_name: Mapped[str]

    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    company: Mapped[Company] = relationship(back_populates="managers")

    __mapper_args__ = {
        "polymorphic_identity": "manager",
    }


class Engineer(Employee): ...
```

---
