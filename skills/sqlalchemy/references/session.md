# Sqlalchemy - Session

**Pages:** 7

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/cascades.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Cascades¶
- save-update¶
  - Behavior of save-update cascade with bi-directional relationships¶
- delete¶
  - Using delete cascade with many-to-many relationships¶
  - Using foreign key ON DELETE cascade with ORM relationships¶

Home | Download this Documentation

Home | Download this Documentation

Mappers support the concept of configurable cascade behavior on relationship() constructs. This refers to how operations performed on a “parent” object relative to a particular Session should be propagated to items referred to by that relationship (e.g. “child” objects), and is affected by the relationship.cascade option.

The default behavior of cascade is limited to cascades of the so-called save-update and merge settings. The typical “alternative” setting for cascade is to add the delete and delete-orphan options; these settings are appropriate for related objects which only exist as long as they are attached to their parent, and are otherwise deleted.

Cascade behavior is configured using the relationship.cascade option on relationship():

To set cascades on a backref, the same flag can be used with the backref() function, which ultimately feeds its arguments back into relationship():

The Origins of Cascade

SQLAlchemy’s notion of cascading behavior on relationships, as well as the options to configure them, are primarily derived from the similar feature in the Hibernate ORM; Hibernate refers to “cascade” in a few places such as in Example: Parent/Child. If cascades are confusing, we’ll refer to their conclusion, stating “The sections we have just covered can be a bit confusing. However, in practice, it all works out nicely.”

The default value of relationship.cascade is save-update, merge. The typical alternative setting for this parameter is either all or more commonly all, delete-orphan. The all symbol is a synonym for save-update, merge, refresh-expire, expunge, delete, and using it in conjunction with delete-orphan indicates that the child object should follow along with its parent in all cases, and be deleted once it is no longer associated with that parent.

The all cascade option implies the refresh-expire cascade setting which may not be desirable when using the Asynchronous I/O (asyncio) extension, as it will expire related objects more aggressively than is typically appropriate in an explicit IO context. See the notes at Preventing Implicit IO when Using AsyncSession for further background.

The list of available values which can be specified for the relationship.cascade parameter are described in the following subsections.

save-update cascade indicates that when an object is placed into a Session via Session.add(), all the objects associated with it via this relationship() should also be added to that same Session. Suppose we have an object user1 with two related objects address1, address2:

If we add user1 to a Session, it will also add address1, address2 implicitly:

save-update cascade also affects attribute operations for objects that are already present in a Session. If we add a third object, address3 to the user1.addresses collection, it becomes part of the state of that Session:

A save-update cascade can exhibit surprising behavior when removing an item from a collection or de-associating an object from a scalar attribute. In some cases, the orphaned objects may still be pulled into the ex-parent’s Session; this is so that the flush process may handle that related object appropriately. This case usually only arises if an object is removed from one Session and added to another:

The save-update cascade is on by default, and is typically taken for granted; it simplifies code by allowing a single call to Session.add() to register an entire structure of objects within that Session at once. While it can be disabled, there is usually not a need to do so.

The save-update cascade takes place uni-directionally in the context of a bi-directional relationship, i.e. when using the relationship.back_populates or relationship.backref parameters to create two separate relationship() objects which refer to each other.

An object that’s not associated with a Session, when assigned to an attribute or collection on a parent object that is associated with a Session, will be automatically added to that same Session. However, the same operation in reverse will not have this effect; an object that’s not associated with a Session, upon which a child object that is associated with a Session is assigned, will not result in an automatic addition of that parent object to the Session. The overall subject of this behavior is known as “cascade backrefs”, and represents a change in behavior that was standardized as of SQLAlchemy 2.0.

To illustrate, given a mapping of Order objects which relate bi-directionally to a series of Item objects via relationships Order.items and Item.order:

If an Order is already associated with a Session, and an Item object is then created and appended to the Order.items collection of that Order, the Item will be automatically cascaded into that same Session:

Above, the bidirectional nature of Order.items and Item.order means that appending to Order.items also assigns to Item.order. At the same time, the save-update cascade allowed for the Item object to be added to the same Session which the parent Order was already associated.

However, if the operation above is performed in the reverse direction, where Item.order is assigned rather than appending directly to Order.item, the cascade operation into the Session will not take place automatically, even though the object assignments Order.items and Item.order will be in the same state as in the previous example:

In the above case, after the Item object is created and all the desired state is set upon it, it should then be added to the Session explicitly:

In older versions of SQLAlchemy, the save-update cascade would occur bidirectionally in all cases. It was then made optional using an option known as cascade_backrefs. Finally, in SQLAlchemy 1.4 the old behavior was deprecated and the cascade_backrefs option was removed in SQLAlchemy 2.0. The rationale is that users generally do not find it intuitive that assigning to an attribute on an object, illustrated above as the assignment of i1.order = o1, would alter the persistence state of that object i1 such that it’s now pending within a Session, and there would frequently be subsequent issues where autoflush would prematurely flush the object and cause errors, in those cases where the given object was still being constructed and wasn’t in a ready state to be flushed. The option to select between uni-directional and bi-directional behaviors was also removed, as this option created two slightly different ways of working, adding to the overall learning curve of the ORM as well as to the documentation and user support burden.

cascade_backrefs behavior deprecated for removal in 2.0 - background on the change in behavior for “cascade backrefs”

The delete cascade indicates that when a “parent” object is marked for deletion, its related “child” objects should also be marked for deletion. If for example we have a relationship User.addresses with delete cascade configured:

If using the above mapping, we have a User object and two related Address objects:

If we mark user1 for deletion, after the flush operation proceeds, address1 and address2 will also be deleted:

Alternatively, if our User.addresses relationship does not have delete cascade, SQLAlchemy’s default behavior is to instead de-associate address1 and address2 from user1 by setting their foreign key reference to NULL. Using a mapping as follows:

Upon deletion of a parent User object, the rows in address are not deleted, but are instead de-associated:

delete cascade on one-to-many relationships is often combined with delete-orphan cascade, which will emit a DELETE for the related row if the “child” object is deassociated from the parent. The combination of delete and delete-orphan cascade covers both situations where SQLAlchemy has to decide between setting a foreign key column to NULL versus deleting the row entirely.

The feature by default works completely independently of database-configured FOREIGN KEY constraints that may themselves configure CASCADE behavior. In order to integrate more efficiently with this configuration, additional directives described at Using foreign key ON DELETE cascade with ORM relationships should be used.

Note that the ORM’s “delete” and “delete-orphan” behavior applies only to the use of the Session.delete() method to mark individual ORM instances for deletion within the unit of work process. It does not apply to “bulk” deletes, which would be emitted using the delete() construct as illustrated at ORM UPDATE and DELETE with Custom WHERE Criteria. See Important Notes and Caveats for ORM-Enabled Update and Delete for additional background.

Using foreign key ON DELETE cascade with ORM relationships

Using delete cascade with many-to-many relationships

The cascade="all, delete" option works equally well with a many-to-many relationship, one that uses relationship.secondary to indicate an association table. When a parent object is deleted, and therefore de-associated with its related objects, the unit of work process will normally delete rows from the association table, but leave the related objects intact. When combined with cascade="all, delete", additional DELETE statements will take place for the child rows themselves.

The following example adapts that of Many To Many to illustrate the cascade="all, delete" setting on one side of the association:

Above, when a Parent object is marked for deletion using Session.delete(), the flush process will as usual delete the associated rows from the association table, however per cascade rules it will also delete all related Child rows.

If the above cascade="all, delete" setting were configured on both relationships, then the cascade action would continue cascading through all Parent and Child objects, loading each children and parents collection encountered and deleting everything that’s connected. It is typically not desirable for “delete” cascade to be configured bidirectionally.

Deleting Rows from the Many to Many Table

Using foreign key ON DELETE with many-to-many relationships

The behavior of SQLAlchemy’s “delete” cascade overlaps with the ON DELETE feature of a database FOREIGN KEY constraint. SQLAlchemy allows configuration of these schema-level DDL behaviors using the ForeignKey and ForeignKeyConstraint constructs; usage of these objects in conjunction with Table metadata is described at ON UPDATE and ON DELETE.

In order to use ON DELETE foreign key cascades in conjunction with relationship(), it’s important to note first and foremost that the relationship.cascade setting must still be configured to match the desired “delete” or “set null” behavior (using delete cascade or leaving it omitted), so that whether the ORM or the database level constraints will handle the task of actually modifying the data in the database, the ORM will still be able to appropriately track the state of locally present objects that may be affected.

There is then an additional option on relationship() which indicates the degree to which the ORM should try to run DELETE/UPDATE operations on related rows itself, vs. how much it should rely upon expecting the database-side FOREIGN KEY constraint cascade to handle the task; this is the relationship.passive_deletes parameter and it accepts options False (the default), True and "all".

The most typical example is that where child rows are to be deleted when parent rows are deleted, and that ON DELETE CASCADE is configured on the relevant FOREIGN KEY constraint as well:

The behavior of the above configuration when a parent row is deleted is as follows:

The application calls session.delete(my_parent), where my_parent is an instance of Parent.

When the Session next flushes changes to the database, all of the currently loaded items within the my_parent.children collection are deleted by the ORM, meaning a DELETE statement is emitted for each record.

If the my_parent.children collection is unloaded, then no DELETE statements are emitted. If the relationship.passive_deletes flag were not set on this relationship(), then a SELECT statement for unloaded Child objects would have been emitted.

A DELETE statement is then emitted for the my_parent row itself.

The database-level ON DELETE CASCADE setting ensures that all rows in child which refer to the affected row in parent are also deleted.

The Parent instance referred to by my_parent, as well as all instances of Child that were related to this object and were loaded (i.e. step 2 above took place), are de-associated from the Session.

To use “ON DELETE CASCADE”, the underlying database engine must support FOREIGN KEY constraints and they must be enforcing:

When using MySQL, an appropriate storage engine must be selected. See CREATE TABLE arguments including Storage Engines for details.

When using SQLite, foreign key support must be enabled explicitly. See Foreign Key Support for details.

Notes on Passive Deletes

It is important to note the differences between the ORM and the relational database’s notion of “cascade” as well as how they integrate:

A database level ON DELETE cascade is configured effectively on the many-to-one side of the relationship; that is, we configure it relative to the FOREIGN KEY constraint that is the “many” side of a relationship. At the ORM level, this direction is reversed. SQLAlchemy handles the deletion of “child” objects relative to a “parent” from the “parent” side, which means that delete and delete-orphan cascade are configured on the one-to-many side.

Database level foreign keys with no ON DELETE setting are often used to prevent a parent row from being removed, as it would necessarily leave an unhandled related row present. If this behavior is desired in a one-to-many relationship, SQLAlchemy’s default behavior of setting a foreign key to NULL can be caught in one of two ways:

The easiest and most common is just to set the foreign-key-holding column to NOT NULL at the database schema level. An attempt by SQLAlchemy to set the column to NULL will fail with a simple NOT NULL constraint exception.

The other, more special case way is to set the relationship.passive_deletes flag to the string "all". This has the effect of entirely disabling SQLAlchemy’s behavior of setting the foreign key column to NULL, and a DELETE will be emitted for the parent row without any affect on the child row, even if the child row is present in memory. This may be desirable in the case when database-level foreign key triggers, either special ON DELETE settings or otherwise, need to be activated in all cases when a parent row is deleted.

Database level ON DELETE cascade is generally much more efficient than relying upon the “cascade” delete feature of SQLAlchemy. The database can chain a series of cascade operations across many relationships at once; e.g. if row A is deleted, all the related rows in table B can be deleted, and all the C rows related to each of those B rows, and on and on, all within the scope of a single DELETE statement. SQLAlchemy on the other hand, in order to support the cascading delete operation fully, has to individually load each related collection in order to target all rows that then may have further related collections. That is, SQLAlchemy isn’t sophisticated enough to emit a DELETE for all those related rows at once within this context.

SQLAlchemy doesn’t need to be this sophisticated, as we instead provide smooth integration with the database’s own ON DELETE functionality, by using the relationship.passive_deletes option in conjunction with properly configured foreign key constraints. Under this behavior, SQLAlchemy only emits DELETE for those rows that are already locally present in the Session; for any collections that are unloaded, it leaves them to the database to handle, rather than emitting a SELECT for them. The section Using foreign key ON DELETE cascade with ORM relationships provides an example of this use.

While database-level ON DELETE functionality works only on the “many” side of a relationship, SQLAlchemy’s “delete” cascade has limited ability to operate in the reverse direction as well, meaning it can be configured on the “many” side to delete an object on the “one” side when the reference on the “many” side is deleted. However this can easily result in constraint violations if there are other objects referring to this “one” side from the “many”, so it typically is only useful when a relationship is in fact a “one to one”. The relationship.single_parent flag should be used to establish an in-Python assertion for this case.

As described at Using delete cascade with many-to-many relationships, “delete” cascade works for many-to-many relationships as well. To make use of ON DELETE CASCADE foreign keys in conjunction with many to many, FOREIGN KEY directives are configured on the association table. These directives can handle the task of automatically deleting from the association table, but cannot accommodate the automatic deletion of the related objects themselves.

In this case, the relationship.passive_deletes directive can save us some additional SELECT statements during a delete operation but there are still some collections that the ORM will continue to load, in order to locate affected child objects and handle them correctly.

Hypothetical optimizations to this could include a single DELETE statement against all parent-associated rows of the association table at once, then use RETURNING to locate affected related child rows, however this is not currently part of the ORM unit of work implementation.

In this configuration, we configure ON DELETE CASCADE on both foreign key constraints of the association table. We configure cascade="all, delete" on the parent->child side of the relationship, and we can then configure passive_deletes=True on the other side of the bidirectional relationship as illustrated below:

Using the above configuration, the deletion of a Parent object proceeds as follows:

A Parent object is marked for deletion using Session.delete().

When the flush occurs, if the Parent.children collection is not loaded, the ORM will first emit a SELECT statement in order to load the Child objects that correspond to Parent.children.

It will then then emit DELETE statements for the rows in association which correspond to that parent row.

for each Child object affected by this immediate deletion, because passive_deletes=True is configured, the unit of work will not need to try to emit SELECT statements for each Child.parents collection as it is assumed the corresponding rows in association will be deleted.

DELETE statements are then emitted for each Child object that was loaded from Parent.children.

delete-orphan cascade adds behavior to the delete cascade, such that a child object will be marked for deletion when it is de-associated from the parent, not just when the parent is marked for deletion. This is a common feature when dealing with a related object that is “owned” by its parent, with a NOT NULL foreign key, so that removal of the item from the parent collection results in its deletion.

delete-orphan cascade implies that each child object can only have one parent at a time, and in the vast majority of cases is configured only on a one-to-many relationship. For the much less common case of setting it on a many-to-one or many-to-many relationship, the “many” side can be forced to allow only a single object at a time by configuring the relationship.single_parent argument, which establishes Python-side validation that ensures the object is associated with only one parent at a time, however this greatly limits the functionality of the “many” relationship and is usually not what’s desired.

For relationship <relationship>, delete-orphan cascade is normally configured only on the “one” side of a one-to-many relationship, and not on the “many” side of a many-to-one or many-to-many relationship. - background on a common error scenario involving delete-orphan cascade.

merge cascade indicates that the Session.merge() operation should be propagated from a parent that’s the subject of the Session.merge() call down to referred objects. This cascade is also on by default.

refresh-expire is an uncommon option, indicating that the Session.expire() operation should be propagated from a parent down to referred objects. When using Session.refresh(), the referred objects are expired only, but not actually refreshed.

expunge cascade indicates that when the parent object is removed from the Session using Session.expunge(), the operation should be propagated down to referred objects.

The ORM in general never modifies the contents of a collection or scalar relationship during the flush process. This means, if your class has a relationship() that refers to a collection of objects, or a reference to a single object such as many-to-one, the contents of this attribute will not be modified when the flush process occurs. Instead, it is expected that the Session would eventually be expired, either through the expire-on-commit behavior of Session.commit() or through explicit use of Session.expire(). At that point, any referenced object or collection associated with that Session will be cleared and will re-load itself upon next access.

A common confusion that arises regarding this behavior involves the use of the Session.delete() method. When Session.delete() is invoked upon an object and the Session is flushed, the row is deleted from the database. Rows that refer to the target row via foreign key, assuming they are tracked using a relationship() between the two mapped object types, will also see their foreign key attributes UPDATED to null, or if delete cascade is set up, the related rows will be deleted as well. However, even though rows related to the deleted object might be themselves modified as well, no changes occur to relationship-bound collections or object references on the objects involved in the operation within the scope of the flush itself. This means if the object was a member of a related collection, it will still be present on the Python side until that collection is expired. Similarly, if the object were referenced via many-to-one or one-to-one from another object, that reference will remain present on that object until the object is expired as well.

Below, we illustrate that after an Address object is marked for deletion, it’s still present in the collection associated with the parent User, even after a flush:

When the above session is committed, all attributes are expired. The next access of user.addresses will re-load the collection, revealing the desired state:

There is a recipe for intercepting Session.delete() and invoking this expiration automatically; see ExpireRelationshipOnFKChange for this. However, the usual practice of deleting items within collections is to forego the usage of Session.delete() directly, and instead use cascade behavior to automatically invoke the deletion as a result of removing the object from the parent collection. The delete-orphan cascade accomplishes this, as illustrated in the example below:

Where above, upon removing the Address object from the User.addresses collection, the delete-orphan cascade has the effect of marking the Address object for deletion in the same way as passing it to Session.delete().

The delete-orphan cascade can also be applied to a many-to-one or one-to-one relationship, so that when an object is de-associated from its parent, it is also automatically marked for deletion. Using delete-orphan cascade on a many-to-one or one-to-one requires an additional flag relationship.single_parent which invokes an assertion that this related object is not to shared with any other parent simultaneously:

Above, if a hypothetical Preference object is removed from a User, it will be deleted on flush:

Cascades for detail on cascades.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (typescript):
```typescript
class Order(Base):
    __tablename__ = "order"

    items = relationship("Item", cascade="all, delete-orphan")
    customer = relationship("User", cascade="save-update")
```

Example 2 (typescript):
```typescript
class Item(Base):
    __tablename__ = "item"

    order = relationship(
        "Order", backref=backref("items", cascade="all, delete-orphan")
    )
```

Example 3 (unknown):
```unknown
>>> user1 = User()
>>> address1, address2 = Address(), Address()
>>> user1.addresses = [address1, address2]
```

Example 4 (unknown):
```unknown
>>> sess = Session()
>>> sess.add(user1)
>>> address1 in sess
True
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/session_basics.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Session Basics¶
- What does the Session do ?¶
- Basics of Using a Session¶
  - Opening and Closing a Session¶
  - Framing out a begin / commit / rollback block¶
  - Using a sessionmaker¶

Home | Download this Documentation

Home | Download this Documentation

In the most general sense, the Session establishes all conversations with the database and represents a “holding zone” for all the objects which you’ve loaded or associated with it during its lifespan. It provides the interface where SELECT and other queries are made that will return and modify ORM-mapped objects. The ORM objects themselves are maintained inside the Session, inside a structure called the identity map - a data structure that maintains unique copies of each object, where “unique” means “only one object with a particular primary key”.

The Session in its most common pattern of use begins in a mostly stateless form. Once queries are issued or other objects are persisted with it, it requests a connection resource from an Engine that is associated with the Session, and then establishes a transaction on that connection. This transaction remains in effect until the Session is instructed to commit or roll back the transaction. When the transaction ends, the connection resource associated with the Engine is released to the connection pool managed by the engine. A new transaction then starts with a new connection checkout.

The ORM objects maintained by a Session are instrumented such that whenever an attribute or a collection is modified in the Python program, a change event is generated which is recorded by the Session. Whenever the database is about to be queried, or when the transaction is about to be committed, the Session first flushes all pending changes stored in memory to the database. This is known as the unit of work pattern.

When using a Session, it’s useful to consider the ORM mapped objects that it maintains as proxy objects to database rows, which are local to the transaction being held by the Session. In order to maintain the state on the objects as matching what’s actually in the database, there are a variety of events that will cause objects to re-access the database in order to keep synchronized. It is possible to “detach” objects from a Session, and to continue using them, though this practice has its caveats. It’s intended that usually, you’d re-associate detached objects with another Session when you want to work with them again, so that they can resume their normal task of representing database state.

The most basic Session use patterns are presented here.

The Session may be constructed on its own or by using the sessionmaker class. It typically is passed a single Engine as a source of connectivity up front. A typical use may look like:

Above, the Session is instantiated with an Engine associated with a particular database URL. It is then used in a Python context manager (i.e. with: statement) so that it is automatically closed at the end of the block; this is equivalent to calling the Session.close() method.

The call to Session.commit() is optional, and is only needed if the work we’ve done with the Session includes new data to be persisted to the database. If we were only issuing SELECT calls and did not need to write any changes, then the call to Session.commit() would be unnecessary.

Note that after Session.commit() is called, either explicitly or when using a context manager, all objects associated with the Session are expired, meaning their contents are erased to be re-loaded within the next transaction. If these objects are instead detached, they will be non-functional until re-associated with a new Session, unless the Session.expire_on_commit parameter is used to disable this behavior. See the section Committing for more detail.

We may also enclose the Session.commit() call and the overall “framing” of the transaction within a context manager for those cases where we will be committing data to the database. By “framing” we mean that if all operations succeed, the Session.commit() method will be called, but if any exceptions are raised, the Session.rollback() method will be called so that the transaction is rolled back immediately, before propagating the exception outward. In Python this is most fundamentally expressed using a try: / except: / else: block such as:

The long-form sequence of operations illustrated above can be achieved more succinctly by making use of the SessionTransaction object returned by the Session.begin() method, which provides a context manager interface for the same sequence of operations:

More succinctly, the two contexts may be combined:

The purpose of sessionmaker is to provide a factory for Session objects with a fixed configuration. As it is typical that an application will have an Engine object in module scope, the sessionmaker can provide a factory for Session objects that are constructed against this engine:

The sessionmaker is analogous to the Engine as a module-level factory for function-level sessions / connections. As such it also has its own sessionmaker.begin() method, analogous to Engine.begin(), which returns a Session object and also maintains a begin/commit/rollback block:

Where above, the Session will both have its transaction committed as well as that the Session will be closed, when the above with: block ends.

When you write your application, the sessionmaker factory should be scoped the same as the Engine object created by create_engine(), which is typically at module-level or global scope. As these objects are both factories, they can be used by any number of functions and threads simultaneously.

The primary means of querying is to make use of the select() construct to create a Select object, which is then executed to return a result using methods such as Session.execute() and Session.scalars(). Results are then returned in terms of Result objects, including sub-variants such as ScalarResult.

A complete guide to SQLAlchemy ORM querying can be found at ORM Querying Guide. Some brief examples follow:

Changed in version 2.0: “2.0” style querying is now standard. See 2.0 Migration - ORM Usage for migration notes from the 1.x series.

Session.add() is used to place instances in the session. For transient (i.e. brand new) instances, this will have the effect of an INSERT taking place for those instances upon the next flush. For instances which are persistent (i.e. were loaded by this session), they are already present and do not need to be added. Instances which are detached (i.e. have been removed from a session) may be re-associated with a session using this method:

To add a list of items to the session at once, use Session.add_all():

The Session.add() operation cascades along the save-update cascade. For more details see the section Cascades.

The Session.delete() method places an instance into the Session’s list of objects to be marked as deleted:

Session.delete() marks an object for deletion, which will result in a DELETE statement emitted for each primary key affected. Before the pending deletes are flushed, objects marked by “delete” are present in the Session.deleted collection. After the DELETE, they are expunged from the Session, which becomes permanent after the transaction is committed.

There are various important behaviors related to the Session.delete() operation, particularly in how relationships to other objects and collections are handled. There’s more information on how this works in the section Cascades, but in general the rules are:

Rows that correspond to mapped objects that are related to a deleted object via the relationship() directive are not deleted by default. If those objects have a foreign key constraint back to the row being deleted, those columns are set to NULL. This will cause a constraint violation if the columns are non-nullable.

To change the “SET NULL” into a DELETE of a related object’s row, use the delete cascade on the relationship().

Rows that are in tables linked as “many-to-many” tables, via the relationship.secondary parameter, are deleted in all cases when the object they refer to is deleted.

When related objects include a foreign key constraint back to the object being deleted, and the related collections to which they belong are not currently loaded into memory, the unit of work will emit a SELECT to fetch all related rows, so that their primary key values can be used to emit either UPDATE or DELETE statements on those related rows. In this way, the ORM without further instruction will perform the function of ON DELETE CASCADE, even if this is configured on Core ForeignKeyConstraint objects.

The relationship.passive_deletes parameter can be used to tune this behavior and rely upon “ON DELETE CASCADE” more naturally; when set to True, this SELECT operation will no longer take place, however rows that are locally present will still be subject to explicit SET NULL or DELETE. Setting relationship.passive_deletes to the string "all" will disable all related object update/delete.

When the DELETE occurs for an object marked for deletion, the object is not automatically removed from collections or object references that refer to it. When the Session is expired, these collections may be loaded again so that the object is no longer present. However, it is preferable that instead of using Session.delete() for these objects, the object should instead be removed from its collection and then delete-orphan should be used so that it is deleted as a secondary effect of that collection removal. See the section Notes on Delete - Deleting Objects Referenced from Collections and Scalar Relationships for an example of this.

delete - describes “delete cascade”, which marks related objects for deletion when a lead object is deleted.

delete-orphan - describes “delete orphan cascade”, which marks related objects for deletion when they are de-associated from their lead object.

Notes on Delete - Deleting Objects Referenced from Collections and Scalar Relationships - important background on Session.delete() as involves relationships being refreshed in memory.

When the Session is used with its default configuration, the flush step is nearly always done transparently. Specifically, the flush occurs before any individual SQL statement is issued as a result of a Query or a 2.0-style Session.execute() call, as well as within the Session.commit() call before the transaction is committed. It also occurs before a SAVEPOINT is issued when Session.begin_nested() is used.

A Session flush can be forced at any time by calling the Session.flush() method:

The flush which occurs automatically within the scope of certain methods is known as autoflush. Autoflush is defined as a configurable, automatic flush call which occurs at the beginning of methods including:

Session.execute() and other SQL-executing methods, when used against ORM-enabled SQL constructs, such as select() objects that refer to ORM entities and/or ORM-mapped attributes

When a Query is invoked to send SQL to the database

Within the Session.merge() method before querying the database

When objects are refreshed

When ORM lazy load operations occur against unloaded object attributes.

There are also points at which flushes occur unconditionally; these points are within key transactional boundaries which include:

Within the process of the Session.commit() method

When Session.begin_nested() is called

When the Session.prepare() 2PC method is used.

The autoflush behavior, as applied to the previous list of items, can be disabled by constructing a Session or sessionmaker passing the Session.autoflush parameter as False:

Additionally, autoflush can be temporarily disabled within the flow of using a Session using the Session.no_autoflush context manager:

To reiterate: The flush process always occurs when transactional methods such as Session.commit() and Session.begin_nested() are called, regardless of any “autoflush” settings, when the Session has remaining pending changes to process.

As the Session only invokes SQL to the database within the context of a DBAPI transaction, all “flush” operations themselves only occur within a database transaction (subject to the isolation level of the database transaction), provided that the DBAPI is not in driver level autocommit mode. This means that assuming the database connection is providing for atomicity within its transactional settings, if any individual DML statement inside the flush fails, the entire operation will be rolled back.

When a failure occurs within a flush, in order to continue using that same Session, an explicit call to Session.rollback() is required after a flush fails, even though the underlying transaction will have been rolled back already (even if the database driver is technically in driver-level autocommit mode). This is so that the overall nesting pattern of so-called “subtransactions” is consistently maintained. The FAQ section “This Session’s transaction has been rolled back due to a previous exception during flush.” (or similar) contains a more detailed description of this behavior.

“This Session’s transaction has been rolled back due to a previous exception during flush.” (or similar) - further background on why Session.rollback() must be called when a flush fails.

As the Session makes use of an identity map which refers to current in-memory objects by primary key, the Session.get() method is provided as a means of locating objects by primary key, first looking within the current identity map and then querying the database for non present values. Such as, to locate a User entity with primary key identity (5, ):

The Session.get() also includes calling forms for composite primary key values, which may be passed as tuples or dictionaries, as well as additional parameters which allow for specific loader and execution options. See Session.get() for the complete parameter list.

An important consideration that will often come up when using the Session is that of dealing with the state that is present on objects that have been loaded from the database, in terms of keeping them synchronized with the current state of the transaction. The SQLAlchemy ORM is based around the concept of an identity map such that when an object is “loaded” from a SQL query, there will be a unique Python object instance maintained corresponding to a particular database identity. This means if we emit two separate queries, each for the same row, and get a mapped object back, the two queries will have returned the same Python object:

Following from this, when the ORM gets rows back from a query, it will skip the population of attributes for an object that’s already loaded. The design assumption here is to assume a transaction that’s perfectly isolated, and then to the degree that the transaction isn’t isolated, the application can take steps on an as-needed basis to refresh objects from the database transaction. The FAQ entry at I’m re-loading data with my Session but it isn’t seeing changes that I committed elsewhere discusses this concept in more detail.

When an ORM mapped object is loaded into memory, there are three general ways to refresh its contents with new data from the current transaction:

the expire() method - the Session.expire() method will erase the contents of selected or all attributes of an object, such that they will be loaded from the database when they are next accessed, e.g. using a lazy loading pattern:

the refresh() method - closely related is the Session.refresh() method, which does everything the Session.expire() method does but also emits one or more SQL queries immediately to actually refresh the contents of the object:

the populate_existing() method or execution option - This is now an execution option documented at Populate Existing; in legacy form it’s found on the Query object as the Query.populate_existing() method. This operation in either form indicates that objects being returned from a query should be unconditionally re-populated from their contents in the database:

Further discussion on the refresh / expire concept can be found at Refreshing / Expiring.

Refreshing / Expiring

I’m re-loading data with my Session but it isn’t seeing changes that I committed elsewhere

SQLAlchemy 2.0 includes enhanced capabilities for emitting several varieties of ORM-enabled INSERT, UPDATE and DELETE statements. See the document at ORM-Enabled INSERT, UPDATE, and DELETE statements for documentation.

ORM-Enabled INSERT, UPDATE, and DELETE statements

ORM UPDATE and DELETE with Custom WHERE Criteria

The Session object features a behavior known as autobegin. This indicates that the Session will internally consider itself to be in a “transactional” state as soon as any work is performed with the Session, either involving modifications to the internal state of the Session with regards to object state changes, or with operations that require database connectivity.

When the Session is first constructed, there’s no transactional state present. The transactional state is begun automatically, when a method such as Session.add() or Session.execute() is invoked, or similarly if a Query is executed to return results (which ultimately uses Session.execute()), or if an attribute is modified on a persistent object.

The transactional state can be checked by accessing the Session.in_transaction() method, which returns True or False indicating if the “autobegin” step has proceeded. While not normally needed, the Session.get_transaction() method will return the actual SessionTransaction object that represents this transactional state.

The transactional state of the Session may also be started explicitly, by invoking the Session.begin() method. When this method is called, the Session is placed into the “transactional” state unconditionally. Session.begin() may be used as a context manager as described at Framing out a begin / commit / rollback block.

The “autobegin” behavior may be disabled using the Session.autobegin parameter set to False. By using this parameter, a Session will require that the Session.begin() method is called explicitly. Upon construction, as well as after any of the Session.rollback(), Session.commit(), or Session.close() methods are called, the Session won’t implicitly begin any new transactions and will raise an error if an attempt to use the Session is made without first calling Session.begin():

Added in version 2.0: Added Session.autobegin, allowing “autobegin” behavior to be disabled

Session.commit() is used to commit the current transaction. At its core this indicates that it emits COMMIT on all current database connections that have a transaction in progress; from a DBAPI perspective this means the connection.commit() DBAPI method is invoked on each DBAPI connection.

When there is no transaction in place for the Session, indicating that no operations were invoked on this Session since the previous call to Session.commit(), the method will begin and commit an internal-only “logical” transaction, that does not normally affect the database unless pending flush changes were detected, but will still invoke event handlers and object expiration rules.

The Session.commit() operation unconditionally issues Session.flush() before emitting COMMIT on relevant database connections. If no pending changes are detected, then no SQL is emitted to the database. This behavior is not configurable and is not affected by the Session.autoflush parameter.

Subsequent to that, assuming the Session is bound to an Engine, Session.commit() will then COMMIT the actual database transaction that is in place, if one was started. After the commit, the Connection object associated with that transaction is closed, causing its underlying DBAPI connection to be released back to the connection pool associated with the Engine to which the Session is bound.

For a Session that’s bound to multiple engines (e.g. as described at Partitioning Strategies), the same COMMIT steps will proceed for each Engine / Connection that is in play within the “logical” transaction being committed. These database transactions are uncoordinated with each other unless two-phase features are enabled.

Other connection-interaction patterns are available as well, by binding the Session to a Connection directly; in this case, it’s assumed that an externally-managed transaction is present, and a real COMMIT will not be emitted automatically in this case; see the section Joining a Session into an External Transaction (such as for test suites) for background on this pattern.

Finally, all objects within the Session are expired as the transaction is closed out. This is so that when the instances are next accessed, either through attribute access or by them being present in the result of a SELECT, they receive the most recent state. This behavior may be controlled by the Session.expire_on_commit flag, which may be set to False when this behavior is undesirable.

Session.rollback() rolls back the current transaction, if any. When there is no transaction in place, the method passes silently.

With a default configured session, the post-rollback state of the session, subsequent to a transaction having been begun either via autobegin or by calling the Session.begin() method explicitly, is as follows:

Database transactions are rolled back. For a Session bound to a single Engine, this means ROLLBACK is emitted for at most a single Connection that’s currently in use. For Session objects bound to multiple Engine objects, ROLLBACK is emitted for all Connection objects that were checked out.

Database connections are released. This follows the same connection-related behavior noted in Committing, where Connection objects obtained from Engine objects are closed, causing the DBAPI connections to be released to the connection pool within the Engine. New connections are checked out from the Engine if and when a new transaction begins.

For a Session that’s bound directly to a Connection as described at Joining a Session into an External Transaction (such as for test suites), rollback behavior on this Connection would follow the behavior specified by the Session.join_transaction_mode parameter, which could involve rolling back savepoints or emitting a real ROLLBACK.

Objects which were initially in the pending state when they were added to the Session within the lifespan of the transaction are expunged, corresponding to their INSERT statement being rolled back. The state of their attributes remains unchanged.

Objects which were marked as deleted within the lifespan of the transaction are promoted back to the persistent state, corresponding to their DELETE statement being rolled back. Note that if those objects were first pending within the transaction, that operation takes precedence instead.

All objects not expunged are fully expired - this is regardless of the Session.expire_on_commit setting.

With that state understood, the Session may safely continue usage after a rollback occurs.

Changed in version 1.4: The Session object now features deferred “begin” behavior, as described in autobegin. If no transaction is begun, methods like Session.commit() and Session.rollback() have no effect. This behavior would not have been observed prior to 1.4 as under non-autocommit mode, a transaction would always be implicitly present.

When a Session.flush() fails, typically for reasons like primary key, foreign key, or “not nullable” constraint violations, a ROLLBACK is issued automatically (it’s currently not possible for a flush to continue after a partial failure). However, the Session goes into a state known as “inactive” at this point, and the calling application must always call the Session.rollback() method explicitly so that the Session can go back into a usable state (it can also be simply closed and discarded). See the FAQ entry at “This Session’s transaction has been rolled back due to a previous exception during flush.” (or similar) for further discussion.

The Session.close() method issues a Session.expunge_all() which removes all ORM-mapped objects from the session, and releases any transactional/connection resources from the Engine object(s) to which it is bound. When connections are returned to the connection pool, transactional state is rolled back as well.

By default, when the Session is closed, it is essentially in the original state as when it was first constructed, and may be used again. In this sense, the Session.close() method is more like a “reset” back to the clean state and not as much like a “database close” method. In this mode of operation the method Session.reset() is an alias to Session.close() and behaves in the same way.

The default behavior of Session.close() can be changed by setting the parameter Session.close_resets_only to False, indicating that the Session cannot be reused after the method Session.close() has been called. In this mode of operation the Session.reset() method will allow multiple “reset” of the session, behaving like Session.close() when Session.close_resets_only is set to True.

Added in version 2.0.22.

It’s recommended that the scope of a Session be limited by a call to Session.close() at the end, especially if the Session.commit() or Session.rollback() methods are not used. The Session may be used as a context manager to ensure that Session.close() is called:

Changed in version 1.4: The Session object features deferred “begin” behavior, as described in autobegin. no longer immediately begins a new transaction after the Session.close() method is called.

By this point, many users already have questions about sessions. This section presents a mini-FAQ (note that we have also a real FAQ) of the most basic issues one is presented with when using a Session.

Just one time, somewhere in your application’s global scope. It should be looked upon as part of your application’s configuration. If your application has three .py files in a package, you could, for example, place the sessionmaker line in your __init__.py file; from that point on your other modules say “from mypackage import Session”. That way, everyone else just uses Session(), and the configuration of that session is controlled by that central point.

If your application starts up, does imports, but does not know what database it’s going to be connecting to, you can bind the Session at the “class” level to the engine later on, using sessionmaker.configure().

In the examples in this section, we will frequently show the sessionmaker being created right above the line where we actually invoke Session. But that’s just for example’s sake! In reality, the sessionmaker would be somewhere at the module level. The calls to instantiate Session would then be placed at the point in the application where database conversations begin.

As a general rule, keep the lifecycle of the session separate and external from functions and objects that access and/or manipulate database data. This will greatly help with achieving a predictable and consistent transactional scope.

Make sure you have a clear notion of where transactions begin and end, and keep transactions short, meaning, they end at the series of a sequence of operations, instead of being held open indefinitely.

A Session is typically constructed at the beginning of a logical operation where database access is potentially anticipated.

The Session, whenever it is used to talk to the database, begins a database transaction as soon as it starts communicating. This transaction remains in progress until the Session is rolled back, committed, or closed. The Session will begin a new transaction if it is used again, subsequent to the previous transaction ending; from this it follows that the Session is capable of having a lifespan across many transactions, though only one at a time. We refer to these two concepts as transaction scope and session scope.

It’s usually not very hard to determine the best points at which to begin and end the scope of a Session, though the wide variety of application architectures possible can introduce challenging situations.

Some sample scenarios include:

Web applications. In this case, it’s best to make use of the SQLAlchemy integrations provided by the web framework in use. Or otherwise, the basic pattern is create a Session at the start of a web request, call the Session.commit() method at the end of web requests that do POST, PUT, or DELETE, and then close the session at the end of web request. It’s also usually a good idea to set Session.expire_on_commit to False so that subsequent access to objects that came from a Session within the view layer do not need to emit new SQL queries to refresh the objects, if the transaction has been committed already.

A background daemon which spawns off child forks would want to create a Session local to each child process, work with that Session through the life of the “job” that the fork is handling, then tear it down when the job is completed.

For a command-line script, the application would create a single, global Session that is established when the program begins to do its work, and commits it right as the program is completing its task.

For a GUI interface-driven application, the scope of the Session may best be within the scope of a user-generated event, such as a button push. Or, the scope may correspond to explicit user interaction, such as the user “opening” a series of records, then “saving” them.

As a general rule, the application should manage the lifecycle of the session externally to functions that deal with specific data. This is a fundamental separation of concerns which keeps data-specific operations agnostic of the context in which they access and manipulate that data.

Keep the lifecycle of the session (and usually the transaction) separate and external. The example below illustrates how this might look, and additionally makes use of a Python context manager (i.e. the with: keyword) in order to manage the scope of the Session and its transaction automatically:

Changed in version 1.4: The Session may be used as a context manager without the use of external helper functions.

Yeee…no. It’s somewhat used as a cache, in that it implements the identity map pattern, and stores objects keyed to their primary key. However, it doesn’t do any kind of query caching. This means, if you say session.scalars(select(Foo).filter_by(name='bar')), even if Foo(name='bar') is right there, in the identity map, the session has no idea about that. It has to issue SQL to the database, get the rows back, and then when it sees the primary key in the row, then it can look in the local identity map and see that the object is already there. It’s only when you say query.get({some primary key}) that the Session doesn’t have to issue a query.

Additionally, the Session stores object instances using a weak reference by default. This also defeats the purpose of using the Session as a cache.

The Session is not designed to be a global object from which everyone consults as a “registry” of objects. That’s more the job of a second level cache. SQLAlchemy provides a pattern for implementing second level caching using dogpile.cache, via the Dogpile Caching example.

Use the Session.object_session() classmethod available on Session:

The newer Runtime Inspection API system can also be used:

The Session is a mutable, stateful object that represents a single database transaction. An instance of Session therefore cannot be shared among concurrent threads or asyncio tasks without careful synchronization. The Session is intended to be used in a non-concurrent fashion, that is, a particular instance of Session should be used in only one thread or task at a time.

When using the AsyncSession object from SQLAlchemy’s asyncio extension, this object is only a thin proxy on top of a Session, and the same rules apply; it is an unsynchronized, mutable, stateful object, so it is not safe to use a single instance of AsyncSession in multiple asyncio tasks at once.

An instance of Session or AsyncSession represents a single logical database transaction, referencing only a single Connection at a time for a particular Engine or AsyncEngine to which the object is bound (note that these objects both support being bound to multiple engines at once, however in this case there will still be only one connection per engine in play within the scope of a transaction).

A database connection within a transaction is also a stateful object that is intended to be operated upon in a non-concurrent, sequential fashion. Commands are issued on the connection in a sequence, which are handled by the database server in the exact order in which they are emitted. As the Session emits commands upon this connection and receives results, the Session itself is transitioning through internal state changes that align with the state of commands and data present on this connection; states which include if a transaction were begun, committed, or rolled back, what SAVEPOINTs if any are in play, as well as fine-grained synchronization of the state of individual database rows with local ORM-mapped objects.

When designing database applications for concurrency, the appropriate model is that each concurrent task / thread works with its own database transaction. This is why when discussing the issue of database concurrency, the standard terminology used is multiple, concurrent transactions. Within traditional RDMS there is no analogue for a single database transaction that is receiving and processing multiple commands concurrently.

The concurrency model for SQLAlchemy’s Session and AsyncSession is therefore Session per thread, AsyncSession per task. An application that uses multiple threads, or multiple tasks in asyncio such as when using an API like asyncio.gather() would want to ensure that each thread has its own Session, each asyncio task has its own AsyncSession.

The best way to ensure this use is by using the standard context manager pattern locally within the top level Python function that is inside the thread or task, which will ensure the lifespan of the Session or AsyncSession is maintained within a local scope.

For applications that benefit from having a “global” Session where it’s not an option to pass the Session object to specific functions and methods which require it, the scoped_session approach can provide for a “thread local” Session object; see the section Contextual/Thread-local Sessions for background. Within the asyncio context, the async_scoped_session object is the asyncio analogue for scoped_session, however is more challenging to configure as it requires a custom “context” function.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# an Engine, which the Session will use for connection
# resources
engine = create_engine("postgresql+psycopg2://scott:tiger@localhost/")

# create session and add objects
with Session(engine) as session:
    session.add(some_object)
    session.add(some_other_object)
    session.commit()
```

Example 2 (markdown):
```markdown
# verbose version of what a context manager will do
with Session(engine) as session:
    session.begin()
    try:
        session.add(some_object)
        session.add(some_other_object)
    except:
        session.rollback()
        raise
    else:
        session.commit()
```

Example 3 (markdown):
```markdown
# create session and add objects
with Session(engine) as session:
    with session.begin():
        session.add(some_object)
        session.add(some_other_object)
    # inner context calls session.commit(), if there were no exceptions
# outer context calls session.close()
```

Example 4 (markdown):
```markdown
# create session and add objects
with Session(engine) as session, session.begin():
    session.add(some_object)
    session.add(some_other_object)
# inner context calls session.commit(), if there were no exceptions
# outer context calls session.close()
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/session.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Using the Session¶

Home | Download this Documentation

Home | Download this Documentation

The declarative base and ORM mapping functions described at ORM Mapped Class Configuration are the primary configurational interface for the ORM. Once mappings are configured, the primary usage interface for persistence operations is the Session.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/session_api.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Session API¶
- Session and sessionmaker()¶
- Session Utilities¶
- Attribute and State Management Utilities¶

Home | Download this Documentation

Home | Download this Documentation

Represents a call to the Session.execute() method, as passed to the SessionEvents.do_orm_execute() event hook.

Manages persistence operations for ORM-mapped objects.

A configurable Session factory.

A Session-level transaction.

SessionTransactionOrigin

indicates the origin of a SessionTransaction.

inherits from sqlalchemy.orm.session._SessionClassMethods, typing.Generic

A configurable Session factory.

The sessionmaker factory generates new Session objects when called, creating them given the configurational arguments established here.

Context manager use is optional; otherwise, the returned Session object may be closed explicitly via the Session.close() method. Using a try:/finally: block is optional, however will ensure that the close takes place even if there are database errors:

sessionmaker acts as a factory for Session objects in the same way as an Engine acts as a factory for Connection objects. In this way it also includes a sessionmaker.begin() method, that provides a context manager which both begins and commits a transaction, as well as closes out the Session when complete, rolling back the transaction if any errors occur:

Added in version 1.4.

When calling upon sessionmaker to construct a Session, keyword arguments may also be passed to the method; these arguments will override that of the globally configured parameters. Below we use a sessionmaker bound to a certain Engine to produce a Session that is instead bound to a specific Connection procured from that engine:

The class also includes a method sessionmaker.configure(), which can be used to specify additional keyword arguments to the factory, which will take effect for subsequent Session objects generated. This is usually used to associate one or more Engine objects with an existing sessionmaker factory before it is first used:

Opening and Closing a Session - introductory text on creating sessions using sessionmaker.

Produce a new Session object using the configuration established in this sessionmaker.

Construct a new sessionmaker.

Produce a context manager that both provides a new Session as well as a transaction that commits.

Close all sessions in memory.

(Re)configure the arguments for this sessionmaker.

Return an identity key.

Return the Session to which an object belongs.

Produce a new Session object using the configuration established in this sessionmaker.

In Python, the __call__ method is invoked on an object when it is “called” in the same way as a function:

Construct a new sessionmaker.

All arguments here except for class_ correspond to arguments accepted by Session directly. See the Session.__init__() docstring for more details on parameters.

bind¶ – a Engine or other Connectable with which newly created Session objects will be associated.

class_¶ – class to use in order to create new Session objects. Defaults to Session.

The autoflush setting to use with newly created Session objects.

Flushing - additional background on autoflush

expire_on_commit=True¶ – the Session.expire_on_commit setting to use with newly created Session objects.

info¶ – optional dictionary of information that will be available via Session.info. Note this dictionary is updated, not replaced, when the info parameter is specified to the specific Session construction operation.

**kw¶ – all other keyword arguments are passed to the constructor of newly created Session objects.

Produce a context manager that both provides a new Session as well as a transaction that commits.

Added in version 1.4.

inherited from the sqlalchemy.orm.session._SessionClassMethods.close_all method of sqlalchemy.orm.session._SessionClassMethods

Close all sessions in memory.

Deprecated since version 1.3: The Session.close_all() method is deprecated and will be removed in a future release. Please refer to close_all_sessions().

(Re)configure the arguments for this sessionmaker.

inherited from the sqlalchemy.orm.session._SessionClassMethods.identity_key method of sqlalchemy.orm.session._SessionClassMethods

Return an identity key.

This is an alias of identity_key().

inherited from the sqlalchemy.orm.session._SessionClassMethods.object_session method of sqlalchemy.orm.session._SessionClassMethods

Return the Session to which an object belongs.

This is an alias of object_session().

inherits from sqlalchemy.util.langhelpers.MemoizedSlots

Represents a call to the Session.execute() method, as passed to the SessionEvents.do_orm_execute() event hook.

Added in version 1.4.

Execute Events - top level documentation on how to use SessionEvents.do_orm_execute()

Construct a new ORMExecuteState.

The dictionary passed as the Session.execute.bind_arguments dictionary.

The complete dictionary of current execution options.

Execute the statement represented by this ORMExecuteState, without re-invoking events that have already proceeded.

local_execution_options

Dictionary view of the execution options passed to the Session.execute() method.

Dictionary of parameters that was passed to Session.execute().

The SQL statement being invoked.

update_execution_options()

Update the local execution options with new values.

Construct a new ORMExecuteState.

this object is constructed internally.

Return a sequence of all Mapper objects that are involved at the top level of this statement.

By “top level” we mean those Mapper objects that would be represented in the result set rows for a select() query, or for a update() or delete() query, the mapper that is the main subject of the UPDATE or DELETE.

Added in version 1.4.0b2.

ORMExecuteState.bind_mapper

The dictionary passed as the Session.execute.bind_arguments dictionary.

This dictionary may be used by extensions to Session to pass arguments that will assist in determining amongst a set of database connections which one should be used to invoke this statement.

Return the Mapper that is the primary “bind” mapper.

For an ORMExecuteState object invoking an ORM statement, that is, the ORMExecuteState.is_orm_statement attribute is True, this attribute will return the Mapper that is considered to be the “primary” mapper of the statement. The term “bind mapper” refers to the fact that a Session object may be “bound” to multiple Engine objects keyed to mapped classes, and the “bind mapper” determines which of those Engine objects would be selected.

For a statement that is invoked against a single mapped class, ORMExecuteState.bind_mapper is intended to be a reliable way of getting this mapper.

Added in version 1.4.0b2.

ORMExecuteState.all_mappers

The complete dictionary of current execution options.

This is a merge of the statement level options with the locally passed execution options.

ORMExecuteState.local_execution_options

Executable.execution_options()

ORM Execution Options

Execute the statement represented by this ORMExecuteState, without re-invoking events that have already proceeded.

This method essentially performs a re-entrant execution of the current statement for which the SessionEvents.do_orm_execute() event is being currently invoked. The use case for this is for event handlers that want to override how the ultimate Result object is returned, such as for schemes that retrieve results from an offline cache or which concatenate results from multiple executions.

When the Result object is returned by the actual handler function within SessionEvents.do_orm_execute() and is propagated to the calling Session.execute() method, the remainder of the Session.execute() method is preempted and the Result object is returned to the caller of Session.execute() immediately.

statement¶ – optional statement to be invoked, in place of the statement currently represented by ORMExecuteState.statement.

optional dictionary of parameters or list of parameters which will be merged into the existing ORMExecuteState.parameters of this ORMExecuteState.

Changed in version 2.0: a list of parameter dictionaries is accepted for executemany executions.

execution_options¶ – optional dictionary of execution options will be merged into the existing ORMExecuteState.execution_options of this ORMExecuteState.

bind_arguments¶ – optional dictionary of bind_arguments which will be merged amongst the current ORMExecuteState.bind_arguments of this ORMExecuteState.

a Result object with ORM-level results.

Re-Executing Statements - background and examples on the appropriate usage of ORMExecuteState.invoke_statement().

Return True if the operation is refreshing column-oriented attributes on an existing ORM object.

This occurs during operations such as Session.refresh(), as well as when an attribute deferred by defer() is being loaded, or an attribute that was expired either directly by Session.expire() or via a commit operation is being loaded.

Handlers will very likely not want to add any options to queries when such an operation is occurring as the query should be a straight primary key fetch which should not have any additional WHERE criteria, and loader options travelling with the instance will have already been added to the query.

Added in version 1.4.0b2.

ORMExecuteState.is_relationship_load

return True if this is a DELETE operation.

Changed in version 2.0.30: - the attribute is also True for a Select.from_statement() construct that is itself against a Delete construct, such as select(Entity).from_statement(delete(..))

return True if the parameters are a multi-element list of dictionaries with more than one dictionary.

Added in version 2.0.

return True if this operation is a Select.from_statement() operation.

This is independent from ORMExecuteState.is_select, as a select().from_statement() construct can be used with INSERT/UPDATE/DELETE RETURNING types of statements as well. ORMExecuteState.is_select will only be set if the Select.from_statement() is itself against a Select construct.

Added in version 2.0.30.

return True if this is an INSERT operation.

Changed in version 2.0.30: - the attribute is also True for a Select.from_statement() construct that is itself against a Insert construct, such as select(Entity).from_statement(insert(..))

return True if the operation is an ORM statement.

This indicates that the select(), insert(), update(), or delete() being invoked contains ORM entities as subjects. For a statement that does not have ORM entities and instead refers only to Table metadata, it is invoked as a Core SQL statement and no ORM-level automation takes place.

Return True if this load is loading objects on behalf of a relationship.

This means, the loader in effect is either a LazyLoader, SelectInLoader, SubqueryLoader, or similar, and the entire SELECT statement being emitted is on behalf of a relationship load.

Handlers will very likely not want to add any options to queries when such an operation is occurring, as loader options are already capable of being propagated to relationship loaders and should be already present.

ORMExecuteState.is_column_load

return True if this is a SELECT operation.

Changed in version 2.0.30: - the attribute is also True for a Select.from_statement() construct that is itself against a Select construct, such as select(Entity).from_statement(select(..))

return True if this is an UPDATE operation.

Changed in version 2.0.30: - the attribute is also True for a Select.from_statement() construct that is itself against a Update construct, such as select(Entity).from_statement(update(..))

An InstanceState that is using this statement execution for a lazy load operation.

The primary rationale for this attribute is to support the horizontal sharding extension, where it is available within specific query execution time hooks created by this extension. To that end, the attribute is only intended to be meaningful at query execution time, and importantly not any time prior to that, including query compilation time.

Return the load_options that will be used for this execution.

Return the PathRegistry for the current load path.

This object represents the “path” in a query along relationships when a particular object or collection is being loaded.

Dictionary view of the execution options passed to the Session.execute() method.

This does not include options that may be associated with the statement being invoked.

ORMExecuteState.execution_options

Dictionary of parameters that was passed to Session.execute().

The SQL statement being invoked.

For an ORM selection as would be retrieved from Query, this is an instance of select that was generated from the ORM query.

Return the update_delete_options that will be used for this execution.

Update the local execution options with new values.

The sequence of UserDefinedOptions that have been associated with the statement being invoked.

inherits from sqlalchemy.orm.session._SessionClassMethods, sqlalchemy.event.registry.EventTarget

Manages persistence operations for ORM-mapped objects.

The Session is not safe for use in concurrent threads.. See Is the Session thread-safe? Is AsyncSession safe to share in concurrent tasks? for background.

The Session’s usage paradigm is described at Using the Session.

Construct a new Session.

Place an object into this Session.

Add the given collection of instances to this Session.

Begin a transaction, or nested transaction, on this Session, if one is not already begun.

Begin a “nested” transaction on this Session, e.g. SAVEPOINT.

Associate a Mapper or arbitrary Python class with a “bind”, e.g. an Engine or Connection.

Associate a Table with a “bind”, e.g. an Engine or Connection.

bulk_insert_mappings()

Perform a bulk insert of the given list of mapping dictionaries.

Perform a bulk save of the given list of objects.

bulk_update_mappings()

Perform a bulk update of the given list of mapping dictionaries.

Close out the transactional resources and ORM objects used by this Session.

Close all sessions in memory.

Flush pending changes and commit the current transaction.

Return a Connection object corresponding to this Session object’s transactional state.

Mark an instance as deleted.

enable_relationship_loading()

Associate an object with this Session for related object loading.

Execute a SQL expression construct.

Expire the attributes on an instance.

Expires all persistent instances within this Session.

Remove the instance from this Session.

Remove all object instances from this Session.

Flush all the object changes to the database.

Return an instance based on the given primary key identifier, or None if not found.

Return a “bind” to which this Session is bound.

get_nested_transaction()

Return the current nested transaction in progress, if any.

Return exactly one instance based on the given primary key identifier, or raise an exception if not found.

Return the current root transaction in progress, if any.

Return an identity key.

A mapping of object identities to objects themselves.

in_nested_transaction()

Return True if this Session has begun a nested transaction, e.g. SAVEPOINT.

Return True if this Session has begun a transaction.

A user-modifiable dictionary.

Close this Session, using connection invalidation.

Return True if the given instance has locally modified attributes.

Copy the state of a given instance into a corresponding instance within this Session.

Return a context manager that disables autoflush.

Return the Session to which an object belongs.

Prepare the current transaction in progress for two phase commit.

Return a new Query object corresponding to this Session.

Expire and refresh attributes on the given instance.

Close out the transactional resources and ORM objects used by this Session, resetting the session to its initial state.

Rollback the current transaction in progress.

Execute a statement and return a scalar result.

Execute a statement and return the results as scalars.

Construct a new Session.

See also the sessionmaker function which is used to generate a Session-producing callable with a given set of arguments.

When True, all query operations will issue a Session.flush() call to this Session before proceeding. This is a convenience feature so that Session.flush() need not be called repeatedly in order for database queries to retrieve results.

Flushing - additional background on autoflush

Automatically start transactions (i.e. equivalent to invoking Session.begin()) when database access is requested by an operation. Defaults to True. Set to False to prevent a Session from implicitly beginning transactions after construction, as well as after any of the Session.rollback(), Session.commit(), or Session.close() methods are called.

Added in version 2.0.

Disabling Autobegin to Prevent Implicit Transactions

bind¶ – An optional Engine or Connection to which this Session should be bound. When specified, all SQL operations performed by this session will execute via this connectable.

A dictionary which may specify any number of Engine or Connection objects as the source of connectivity for SQL operations on a per-entity basis. The keys of the dictionary consist of any series of mapped classes, arbitrary Python classes that are bases for mapped classes, Table objects and Mapper objects. The values of the dictionary are then instances of Engine or less commonly Connection objects. Operations which proceed relative to a particular mapped class will consult this dictionary for the closest matching entity in order to determine which Engine should be used for a particular SQL operation. The complete heuristics for resolution are described at Session.get_bind(). Usage looks like:

Partitioning Strategies (e.g. multiple database backends per Session)

Session.bind_mapper()

class_¶ – Specify an alternate class other than sqlalchemy.orm.session.Session which should be used by the returned class. This is the only argument that is local to the sessionmaker function, and is not sent directly to the constructor for Session.

enable_baked_queries¶ –

legacy; defaults to True. A parameter consumed by the sqlalchemy.ext.baked extension to determine if “baked queries” should be cached, as is the normal operation of this extension. When set to False, caching as used by this particular extension is disabled.

Changed in version 1.4: The sqlalchemy.ext.baked extension is legacy and is not used by any of SQLAlchemy’s internals. This flag therefore only affects applications that are making explicit use of this extension within their own code.

Defaults to True. When True, all instances will be fully expired after each commit(), so that all attribute/object access subsequent to a completed transaction will load from the most recent database state.

Deprecated; this flag is always True.

SQLAlchemy 2.0 - Major Migration Guide

info¶ – optional dictionary of arbitrary data to be associated with this Session. Is available via the Session.info attribute. Note the dictionary is copied at construction time so that modifications to the per- Session dictionary will be local to that Session.

query_cls¶ – Class which should be used to create new Query objects, as returned by the Session.query() method. Defaults to Query.

twophase¶ – When True, all transactions will be started as a “two phase” transaction, i.e. using the “two phase” semantics of the database in use along with an XID. During a commit(), after flush() has been issued for all attached databases, the TwoPhaseTransaction.prepare() method on each database’s TwoPhaseTransaction will be called. This allows each database to roll back the entire transaction, before each transaction is committed.

autocommit¶ – the “autocommit” keyword is present for backwards compatibility but must remain at its default value of False.

join_transaction_mode¶ –

Describes the transactional behavior to take when a given bind is a Connection that has already begun a transaction outside the scope of this Session; in other words the Connection.in_transaction() method returns True.

The following behaviors only take effect when the Session actually makes use of the connection given; that is, a method such as Session.execute(), Session.connection(), etc. are actually invoked:

"conditional_savepoint" - this is the default. if the given Connection is begun within a transaction but does not have a SAVEPOINT, then "rollback_only" is used. If the Connection is additionally within a SAVEPOINT, in other words Connection.in_nested_transaction() method returns True, then "create_savepoint" is used.

"conditional_savepoint" behavior attempts to make use of savepoints in order to keep the state of the existing transaction unchanged, but only if there is already a savepoint in progress; otherwise, it is not assumed that the backend in use has adequate support for SAVEPOINT, as availability of this feature varies. "conditional_savepoint" also seeks to establish approximate backwards compatibility with previous Session behavior, for applications that are not setting a specific mode. It is recommended that one of the explicit settings be used.

"create_savepoint" - the Session will use Connection.begin_nested() in all cases to create its own transaction. This transaction by its nature rides “on top” of any existing transaction that’s opened on the given Connection; if the underlying database and the driver in use has full, non-broken support for SAVEPOINT, the external transaction will remain unaffected throughout the lifespan of the Session.

The "create_savepoint" mode is the most useful for integrating a Session into a test suite where an externally initiated transaction should remain unaffected; however, it relies on proper SAVEPOINT support from the underlying driver and database.

When using SQLite, the SQLite driver included through Python 3.11 does not handle SAVEPOINTs correctly in all cases without workarounds. See the sections Serializable isolation / Savepoints / Transactional DDL and Serializable isolation / Savepoints / Transactional DDL (asyncio version) for details on current workarounds.

"control_fully" - the Session will take control of the given transaction as its own; Session.commit() will call .commit() on the transaction, Session.rollback() will call .rollback() on the transaction, Session.close() will call .rollback on the transaction.

This mode of use is equivalent to how SQLAlchemy 1.4 would handle a Connection given with an existing SAVEPOINT (i.e. Connection.begin_nested()); the Session would take full control of the existing SAVEPOINT.

"rollback_only" - the Session will take control of the given transaction for .rollback() calls only; .commit() calls will not be propagated to the given transaction. .close() calls will have no effect on the given transaction.

This mode of use is equivalent to how SQLAlchemy 1.4 would handle a Connection given with an existing regular database transaction (i.e. Connection.begin()); the Session would propagate Session.rollback() calls to the underlying transaction, but not Session.commit() or Session.close() calls.

Added in version 2.0.0rc1.

Defaults to True. Determines if the session should reset itself after calling .close() or should pass in a no longer usable state, disabling reuse.

Added in version 2.0.22: added flag close_resets_only. A future SQLAlchemy version may change the default value of this flag to False.

Closing - Detail on the semantics of Session.close() and Session.reset().

Place an object into this Session.

Objects that are in the transient state when passed to the Session.add() method will move to the pending state, until the next flush, at which point they will move to the persistent state.

Objects that are in the detached state when passed to the Session.add() method will move to the persistent state directly.

If the transaction used by the Session is rolled back, objects which were transient when they were passed to Session.add() will be moved back to the transient state, and will no longer be present within this Session.

Adding New or Existing Items - at Basics of Using a Session

Add the given collection of instances to this Session.

See the documentation for Session.add() for a general behavioral description.

Adding New or Existing Items - at Basics of Using a Session

Begin a transaction, or nested transaction, on this Session, if one is not already begun.

The Session object features autobegin behavior, so that normally it is not necessary to call the Session.begin() method explicitly. However, it may be used in order to control the scope of when the transactional state is begun.

When used to begin the outermost transaction, an error is raised if this Session is already inside of a transaction.

nested¶ – if True, begins a SAVEPOINT transaction and is equivalent to calling Session.begin_nested(). For documentation on SAVEPOINT transactions, please see Using SAVEPOINT.

the SessionTransaction object. Note that SessionTransaction acts as a Python context manager, allowing Session.begin() to be used in a “with” block. See Explicit Begin for an example.

Managing Transactions

Session.begin_nested()

Begin a “nested” transaction on this Session, e.g. SAVEPOINT.

The target database(s) and associated drivers must support SQL SAVEPOINT for this method to function correctly.

For documentation on SAVEPOINT transactions, please see Using SAVEPOINT.

the SessionTransaction object. Note that SessionTransaction acts as a context manager, allowing Session.begin_nested() to be used in a “with” block. See Using SAVEPOINT for a usage example.

Serializable isolation / Savepoints / Transactional DDL - special workarounds required with the SQLite driver in order for SAVEPOINT to work correctly. For asyncio use cases, see the section Serializable isolation / Savepoints / Transactional DDL (asyncio version).

Associate a Mapper or arbitrary Python class with a “bind”, e.g. an Engine or Connection.

The given entity is added to a lookup used by the Session.get_bind() method.

mapper¶ – a Mapper object, or an instance of a mapped class, or any Python class that is the base of a set of mapped classes.

bind¶ – an Engine or Connection object.

Partitioning Strategies (e.g. multiple database backends per Session)

Associate a Table with a “bind”, e.g. an Engine or Connection.

The given Table is added to a lookup used by the Session.get_bind() method.

table¶ – a Table object, which is typically the target of an ORM mapping, or is present within a selectable that is mapped.

bind¶ – an Engine or Connection object.

Partitioning Strategies (e.g. multiple database backends per Session)

Session.bind_mapper()

Perform a bulk insert of the given list of mapping dictionaries.

This method is a legacy feature as of the 2.0 series of SQLAlchemy. For modern bulk INSERT and UPDATE, see the sections ORM Bulk INSERT Statements and ORM Bulk UPDATE by Primary Key. The 2.0 API shares implementation details with this method and adds new features as well.

mapper¶ – a mapped class, or the actual Mapper object, representing the single kind of object represented within the mapping list.

mappings¶ – a sequence of dictionaries, each one containing the state of the mapped row to be inserted, in terms of the attribute names on the mapped class. If the mapping refers to multiple tables, such as a joined-inheritance mapping, each dictionary must contain all keys to be populated into all tables.

when True, the INSERT process will be altered to ensure that newly generated primary key values will be fetched. The rationale for this parameter is typically to enable Joined Table Inheritance mappings to be bulk inserted.

for backends that don’t support RETURNING, the Session.bulk_insert_mappings.return_defaults parameter can significantly decrease performance as INSERT statements can no longer be batched. See “Insert Many Values” Behavior for INSERT statements for background on which backends are affected.

When True, a value of None will result in a NULL value being included in the INSERT statement, rather than the column being omitted from the INSERT. This allows all the rows being INSERTed to have the identical set of columns which allows the full set of rows to be batched to the DBAPI. Normally, each column-set that contains a different combination of NULL values than the previous row must omit a different series of columns from the rendered INSERT statement, which means it must be emitted as a separate statement. By passing this flag, the full set of rows are guaranteed to be batchable into one batch; the cost however is that server-side defaults which are invoked by an omitted column will be skipped, so care must be taken to ensure that these are not necessary.

When this flag is set, server side default SQL values will not be invoked for those columns that are inserted as NULL; the NULL value will be sent explicitly. Care must be taken to ensure that no server-side default functions need to be invoked for the operation as a whole.

ORM-Enabled INSERT, UPDATE, and DELETE statements

Session.bulk_save_objects()

Session.bulk_update_mappings()

Perform a bulk save of the given list of objects.

This method is a legacy feature as of the 2.0 series of SQLAlchemy. For modern bulk INSERT and UPDATE, see the sections ORM Bulk INSERT Statements and ORM Bulk UPDATE by Primary Key.

For general INSERT and UPDATE of existing ORM mapped objects, prefer standard unit of work data management patterns, introduced in the SQLAlchemy Unified Tutorial at Data Manipulation with the ORM. SQLAlchemy 2.0 now uses “Insert Many Values” Behavior for INSERT statements with modern dialects which solves previous issues of bulk INSERT slowness.

a sequence of mapped object instances. The mapped objects are persisted as is, and are not associated with the Session afterwards.

For each object, whether the object is sent as an INSERT or an UPDATE is dependent on the same rules used by the Session in traditional operation; if the object has the InstanceState.key attribute set, then the object is assumed to be “detached” and will result in an UPDATE. Otherwise, an INSERT is used.

In the case of an UPDATE, statements are grouped based on which attributes have changed, and are thus to be the subject of each SET clause. If update_changed_only is False, then all attributes present within each object are applied to the UPDATE statement, which may help in allowing the statements to be grouped together into a larger executemany(), and will also reduce the overhead of checking history on attributes.

return_defaults¶ – when True, rows that are missing values which generate defaults, namely integer primary key defaults and sequences, will be inserted one at a time, so that the primary key value is available. In particular this will allow joined-inheritance and other multi-table mappings to insert correctly without the need to provide primary key values ahead of time; however, Session.bulk_save_objects.return_defaults greatly reduces the performance gains of the method overall. It is strongly advised to please use the standard Session.add_all() approach.

update_changed_only¶ – when True, UPDATE statements are rendered based on those attributes in each state that have logged changes. When False, all attributes present are rendered into the SET clause with the exception of primary key attributes.

preserve_order¶ – when True, the order of inserts and updates matches exactly the order in which the objects are given. When False, common types of objects are grouped into inserts and updates, to allow for more batching opportunities.

ORM-Enabled INSERT, UPDATE, and DELETE statements

Session.bulk_insert_mappings()

Session.bulk_update_mappings()

Perform a bulk update of the given list of mapping dictionaries.

This method is a legacy feature as of the 2.0 series of SQLAlchemy. For modern bulk INSERT and UPDATE, see the sections ORM Bulk INSERT Statements and ORM Bulk UPDATE by Primary Key. The 2.0 API shares implementation details with this method and adds new features as well.

mapper¶ – a mapped class, or the actual Mapper object, representing the single kind of object represented within the mapping list.

mappings¶ – a sequence of dictionaries, each one containing the state of the mapped row to be updated, in terms of the attribute names on the mapped class. If the mapping refers to multiple tables, such as a joined-inheritance mapping, each dictionary may contain keys corresponding to all tables. All those keys which are present and are not part of the primary key are applied to the SET clause of the UPDATE statement; the primary key values, which are required, are applied to the WHERE clause.

ORM-Enabled INSERT, UPDATE, and DELETE statements

Session.bulk_insert_mappings()

Session.bulk_save_objects()

Close out the transactional resources and ORM objects used by this Session.

This expunges all ORM objects associated with this Session, ends any transaction in progress and releases any Connection objects which this Session itself has checked out from associated Engine objects. The operation then leaves the Session in a state which it may be used again.

In the default running mode the Session.close() method does not prevent the Session from being used again. The Session itself does not actually have a distinct “closed” state; it merely means the Session will release all database connections and ORM objects.

Setting the parameter Session.close_resets_only to False will instead make the close final, meaning that any further action on the session will be forbidden.

Changed in version 1.4: The Session.close() method does not immediately create a new SessionTransaction object; instead, the new SessionTransaction is created only if the Session is used again for a database operation.

Closing - detail on the semantics of Session.close() and Session.reset().

Session.reset() - a similar method that behaves like close() with the parameter Session.close_resets_only set to True.

inherited from the sqlalchemy.orm.session._SessionClassMethods.close_all method of sqlalchemy.orm.session._SessionClassMethods

Close all sessions in memory.

Deprecated since version 1.3: The Session.close_all() method is deprecated and will be removed in a future release. Please refer to close_all_sessions().

Flush pending changes and commit the current transaction.

When the COMMIT operation is complete, all objects are fully expired, erasing their internal contents, which will be automatically re-loaded when the objects are next accessed. In the interim, these objects are in an expired state and will not function if they are detached from the Session. Additionally, this re-load operation is not supported when using asyncio-oriented APIs. The Session.expire_on_commit parameter may be used to disable this behavior.

When there is no transaction in place for the Session, indicating that no operations were invoked on this Session since the previous call to Session.commit(), the method will begin and commit an internal-only “logical” transaction, that does not normally affect the database unless pending flush changes were detected, but will still invoke event handlers and object expiration rules.

The outermost database transaction is committed unconditionally, automatically releasing any SAVEPOINTs in effect.

Managing Transactions

Preventing Implicit IO when Using AsyncSession

Return a Connection object corresponding to this Session object’s transactional state.

Either the Connection corresponding to the current transaction is returned, or if no transaction is in progress, a new one is begun and the Connection returned (note that no transactional state is established with the DBAPI until the first SQL statement is emitted).

Ambiguity in multi-bind or unbound Session objects can be resolved through any of the optional keyword arguments. This ultimately makes usage of the get_bind() method for resolution.

bind_arguments¶ – dictionary of bind arguments. May include “mapper”, “bind”, “clause”, other custom arguments that are passed to Session.get_bind().

a dictionary of execution options that will be passed to Connection.execution_options(), when the connection is first procured only. If the connection is already present within the Session, a warning is emitted and the arguments are ignored.

Setting Transaction Isolation Levels / DBAPI AUTOCOMMIT

Mark an instance as deleted.

The object is assumed to be either persistent or detached when passed; after the method is called, the object will remain in the persistent state until the next flush proceeds. During this time, the object will also be a member of the Session.deleted collection.

When the next flush proceeds, the object will move to the deleted state, indicating a DELETE statement was emitted for its row within the current transaction. When the transaction is successfully committed, the deleted object is moved to the detached state and is no longer present within this Session.

Deleting - at Basics of Using a Session

The set of all instances marked as ‘deleted’ within this Session

The set of all persistent instances considered dirty.

Instances are considered dirty when they were modified but not deleted.

Note that this ‘dirty’ calculation is ‘optimistic’; most attribute-setting or collection modification operations will mark an instance as ‘dirty’ and place it in this set, even if there is no net change to the attribute’s value. At flush time, the value of each attribute is compared to its previously saved value, and if there’s no net change, no SQL operation will occur (this is a more expensive operation so it’s only done at flush time).

To check if an instance has actionable net changes to its attributes, use the Session.is_modified() method.

Associate an object with this Session for related object loading.

enable_relationship_loading() exists to serve special use cases and is not recommended for general use.

Accesses of attributes mapped with relationship() will attempt to load a value from the database using this Session as the source of connectivity. The values will be loaded based on foreign key and primary key values present on this object - if not present, then those relationships will be unavailable.

The object will be attached to this session, but will not participate in any persistence operations; its state for almost all purposes will remain either “transient” or “detached”, except for the case of relationship loading.

Also note that backrefs will often not work as expected. Altering a relationship-bound attribute on the target object may not fire off a backref event, if the effective value is what was already loaded from a foreign-key-holding value.

The Session.enable_relationship_loading() method is similar to the load_on_pending flag on relationship(). Unlike that flag, Session.enable_relationship_loading() allows an object to remain transient while still being able to load related items.

To make a transient object associated with a Session via Session.enable_relationship_loading() pending, add it to the Session using Session.add() normally. If the object instead represents an existing identity in the database, it should be merged using Session.merge().

Session.enable_relationship_loading() does not improve behavior when the ORM is used normally - object references should be constructed at the object level, not at the foreign key level, so that they are present in an ordinary way before flush() proceeds. This method is not intended for general use.

relationship.load_on_pending - this flag allows per-relationship loading of many-to-ones on items that are pending.

make_transient_to_detached() - allows for an object to be added to a Session without SQL emitted, which then will unexpire attributes on access.

Execute a SQL expression construct.

Returns a Result object representing results of the statement execution.

The API contract of Session.execute() is similar to that of Connection.execute(), the 2.0 style version of Connection.

Changed in version 1.4: the Session.execute() method is now the primary point of ORM statement execution when using 2.0 style ORM usage.

statement¶ – An executable statement (i.e. an Executable expression such as select()).

params¶ – Optional dictionary, or list of dictionaries, containing bound parameter values. If a single dictionary, single-row execution occurs; if a list of dictionaries, an “executemany” will be invoked. The keys in each dictionary must correspond to parameter names present in the statement.

optional dictionary of execution options, which will be associated with the statement execution. This dictionary can provide a subset of the options that are accepted by Connection.execution_options(), and may also provide additional options understood only in an ORM context.

ORM Execution Options - ORM-specific execution options

bind_arguments¶ – dictionary of additional arguments to determine the bind. May include “mapper”, “bind”, or other custom arguments. Contents of this dictionary are passed to the Session.get_bind() method.

Expire the attributes on an instance.

Marks the attributes of an instance as out of date. When an expired attribute is next accessed, a query will be issued to the Session object’s current transactional context in order to load all expired attributes for the given instance. Note that a highly isolated transaction will return the same values as were previously read in that same transaction, regardless of changes in database state outside of that transaction.

To expire all objects in the Session simultaneously, use Session.expire_all().

The Session object’s default behavior is to expire all state whenever the Session.rollback() or Session.commit() methods are called, so that new state can be loaded for the new transaction. For this reason, calling Session.expire() only makes sense for the specific case that a non-ORM SQL statement was emitted in the current transaction.

instance¶ – The instance to be refreshed.

attribute_names¶ – optional list of string attribute names indicating a subset of attributes to be expired.

Refreshing / Expiring - introductory material

Query.populate_existing()

Expires all persistent instances within this Session.

When any attributes on a persistent instance is next accessed, a query will be issued using the Session object’s current transactional context in order to load all expired attributes for the given instance. Note that a highly isolated transaction will return the same values as were previously read in that same transaction, regardless of changes in database state outside of that transaction.

To expire individual objects and individual attributes on those objects, use Session.expire().

The Session object’s default behavior is to expire all state whenever the Session.rollback() or Session.commit() methods are called, so that new state can be loaded for the new transaction. For this reason, calling Session.expire_all() is not usually needed, assuming the transaction is isolated.

Refreshing / Expiring - introductory material

Query.populate_existing()

Remove the instance from this Session.

This will free all internal references to the instance. Cascading will be applied according to the expunge cascade rule.

Remove all object instances from this Session.

This is equivalent to calling expunge(obj) on all objects in this Session.

Flush all the object changes to the database.

Writes out all pending object creations, deletions and modifications to the database as INSERTs, DELETEs, UPDATEs, etc. Operations are automatically ordered by the Session’s unit of work dependency solver.

Database operations will be issued in the current transactional context and do not affect the state of the transaction, unless an error occurs, in which case the entire transaction is rolled back. You may flush() as often as you like within a transaction to move changes from Python to the database’s transaction buffer.

Optional; restricts the flush operation to operate only on elements that are in the given collection.

This feature is for an extremely narrow set of use cases where particular objects may need to be operated upon before the full flush() occurs. It is not intended for general use.

Return an instance based on the given primary key identifier, or None if not found.

Added in version 1.4: Added Session.get(), which is moved from the now legacy Query.get() method.

Session.get() is special in that it provides direct access to the identity map of the Session. If the given primary key identifier is present in the local identity map, the object is returned directly from this collection and no SQL is emitted, unless the object has been marked fully expired. If not present, a SELECT is performed in order to locate the object.

Session.get() also will perform a check if the object is present in the identity map and marked as expired - a SELECT is emitted to refresh the object as well as to ensure that the row is still present. If not, ObjectDeletedError is raised.

entity¶ – a mapped class or Mapper indicating the type of entity to be loaded.

A scalar, tuple, or dictionary representing the primary key. For a composite (e.g. multiple column) primary key, a tuple or dictionary should be passed.

For a single-column primary key, the scalar calling form is typically the most expedient. If the primary key of a row is the value “5”, the call looks like:

The tuple form contains primary key values typically in the order in which they correspond to the mapped Table object’s primary key columns, or if the Mapper.primary_key configuration parameter were used, in the order used for that parameter. For example, if the primary key of a row is represented by the integer digits “5, 10” the call would look like:

The dictionary form should include as keys the mapped attribute names corresponding to each element of the primary key. If the mapped class has the attributes id, version_id as the attributes which store the object’s primary key value, the call would look like:

options¶ – optional sequence of loader options which will be applied to the query, if one is emitted.

populate_existing¶ – causes the method to unconditionally emit a SQL query and refresh the object with the newly loaded data, regardless of whether or not the object is already present.

with_for_update¶ – optional boolean True indicating FOR UPDATE should be used, or may be a dictionary containing flags to indicate a more specific set of FOR UPDATE flags for the SELECT; flags should match the parameters of Query.with_for_update(). Supersedes the Session.refresh.lockmode parameter.

optional dictionary of execution options, which will be associated with the query execution if one is emitted. This dictionary can provide a subset of the options that are accepted by Connection.execution_options(), and may also provide additional options understood only in an ORM context.

Added in version 1.4.29.

ORM Execution Options - ORM-specific execution options

dictionary of additional arguments to determine the bind. May include “mapper”, “bind”, or other custom arguments. Contents of this dictionary are passed to the Session.get_bind() method.

The object instance, or None.

Return a “bind” to which this Session is bound.

The “bind” is usually an instance of Engine, except in the case where the Session has been explicitly bound directly to a Connection.

For a multiply-bound or unbound Session, the mapper or clause arguments are used to determine the appropriate bind to return.

Note that the “mapper” argument is usually present when Session.get_bind() is called via an ORM operation such as a Session.query(), each individual INSERT/UPDATE/DELETE operation within a Session.flush(), call, etc.

The order of resolution is:

if mapper given and Session.binds is present, locate a bind based first on the mapper in use, then on the mapped class in use, then on any base classes that are present in the __mro__ of the mapped class, from more specific superclasses to more general.

if clause given and Session.binds is present, locate a bind based on Table objects found in the given clause present in Session.binds.

if Session.binds is present, return that.

if clause given, attempt to return a bind linked to the MetaData ultimately associated with the clause.

if mapper given, attempt to return a bind linked to the MetaData ultimately associated with the Table or other selectable to which the mapper is mapped.

No bind can be found, UnboundExecutionError is raised.

Note that the Session.get_bind() method can be overridden on a user-defined subclass of Session to provide any kind of bind resolution scheme. See the example at Custom Vertical Partitioning.

mapper¶ – Optional mapped class or corresponding Mapper instance. The bind can be derived from a Mapper first by consulting the “binds” map associated with this Session, and secondly by consulting the MetaData associated with the Table to which the Mapper is mapped for a bind.

clause¶ – A ClauseElement (i.e. select(), text(), etc.). If the mapper argument is not present or could not produce a bind, the given expression construct will be searched for a bound element, typically a Table associated with bound MetaData.

Partitioning Strategies (e.g. multiple database backends per Session)

Session.bind_mapper()

Return the current nested transaction in progress, if any.

Added in version 1.4.

Return exactly one instance based on the given primary key identifier, or raise an exception if not found.

Raises NoResultFound if the query selects no rows.

For a detailed documentation of the arguments see the method Session.get().

Added in version 2.0.22.

returns None if no row was found with the provided primary key

Return the current root transaction in progress, if any.

Added in version 1.4.

inherited from the sqlalchemy.orm.session._SessionClassMethods.identity_key method of sqlalchemy.orm.session._SessionClassMethods

Return an identity key.

This is an alias of identity_key().

A mapping of object identities to objects themselves.

Iterating through Session.identity_map.values() provides access to the full set of persistent objects (i.e., those that have row identity) currently in the session.

identity_key() - helper function to produce the keys used in this dictionary.

Return True if this Session has begun a nested transaction, e.g. SAVEPOINT.

Added in version 1.4.

Return True if this Session has begun a transaction.

Added in version 1.4.

A user-modifiable dictionary.

The initial value of this dictionary can be populated using the info argument to the Session constructor or sessionmaker constructor or factory methods. The dictionary here is always local to this Session and can be modified independently of all other Session objects.

Close this Session, using connection invalidation.

This is a variant of Session.close() that will additionally ensure that the Connection.invalidate() method will be called on each Connection object that is currently in use for a transaction (typically there is only one connection unless the Session is used with multiple engines).

This can be called when the database is known to be in a state where the connections are no longer safe to be used.

Below illustrates a scenario when using gevent, which can produce Timeout exceptions that may mean the underlying connection should be discarded:

The method additionally does everything that Session.close() does, including that all ORM objects are expunged.

True if this Session not in “partial rollback” state.

Changed in version 1.4: The Session no longer begins a new transaction immediately, so this attribute will be False when the Session is first instantiated.

“partial rollback” state typically indicates that the flush process of the Session has failed, and that the Session.rollback() method must be emitted in order to fully roll back the transaction.

If this Session is not in a transaction at all, the Session will autobegin when it is first used, so in this case Session.is_active will return True.

Otherwise, if this Session is within a transaction, and that transaction has not been rolled back internally, the Session.is_active will also return True.

“This Session’s transaction has been rolled back due to a previous exception during flush.” (or similar)

Session.in_transaction()

Return True if the given instance has locally modified attributes.

This method retrieves the history for each instrumented attribute on the instance and performs a comparison of the current value to its previously flushed or committed value, if any.

It is in effect a more expensive and accurate version of checking for the given instance in the Session.dirty collection; a full test for each attribute’s net “dirty” status is performed.

A few caveats to this method apply:

Instances present in the Session.dirty collection may report False when tested with this method. This is because the object may have received change events via attribute mutation, thus placing it in Session.dirty, but ultimately the state is the same as that loaded from the database, resulting in no net change here.

Scalar attributes may not have recorded the previously set value when a new value was applied, if the attribute was not loaded, or was expired, at the time the new value was received - in these cases, the attribute is assumed to have a change, even if there is ultimately no net change against its database value. SQLAlchemy in most cases does not need the “old” value when a set event occurs, so it skips the expense of a SQL call if the old value isn’t present, based on the assumption that an UPDATE of the scalar value is usually needed, and in those few cases where it isn’t, is less expensive on average than issuing a defensive SELECT.

The “old” value is fetched unconditionally upon set only if the attribute container has the active_history flag set to True. This flag is set typically for primary key attributes and scalar object references that are not a simple many-to-one. To set this flag for any arbitrary mapped column, use the active_history argument with column_property().

instance¶ – mapped instance to be tested for pending changes.

include_collections¶ – Indicates if multivalued collections should be included in the operation. Setting this to False is a way to detect only local-column based properties (i.e. scalar columns or many-to-one foreign keys) that would result in an UPDATE for this instance upon flush.

Copy the state of a given instance into a corresponding instance within this Session.

Session.merge() examines the primary key attributes of the source instance, and attempts to reconcile it with an instance of the same primary key in the session. If not found locally, it attempts to load the object from the database based on primary key, and if none can be located, creates a new instance. The state of each attribute on the source instance is then copied to the target instance. The resulting target instance is then returned by the method; the original source instance is left unmodified, and un-associated with the Session if not already.

This operation cascades to associated instances if the association is mapped with cascade="merge".

See Merging for a detailed discussion of merging.

instance¶ – Instance to be merged.

Boolean, when False, merge() switches into a “high performance” mode which causes it to forego emitting history events as well as all database access. This flag is used for cases such as transferring graphs of objects into a Session from a second level cache, or to transfer just-loaded objects into the Session owned by a worker thread or process without re-querying the database.

The load=False use case adds the caveat that the given object has to be in a “clean” state, that is, has no pending changes to be flushed - even if the incoming object is detached from any Session. This is so that when the merge operation populates local attributes and cascades to related objects and collections, the values can be “stamped” onto the target object as is, without generating any history or attribute events, and without the need to reconcile the incoming data with any existing related objects or collections that might not be loaded. The resulting objects from load=False are always produced as “clean”, so it is only appropriate that the given objects should be “clean” as well, else this suggests a mis-use of the method.

optional sequence of loader options which will be applied to the Session.get() method when the merge operation loads the existing version of the object from the database.

Added in version 1.4.24.

make_transient_to_detached() - provides for an alternative means of “merging” a single object into the Session

The set of all instances marked as ‘new’ within this Session.

Return a context manager that disables autoflush.

Operations that proceed within the with: block will not be subject to flushes occurring upon query access. This is useful when initializing a series of objects which involve existing database queries, where the uncompleted object should not yet be flushed.

inherited from the sqlalchemy.orm.session._SessionClassMethods.object_session method of sqlalchemy.orm.session._SessionClassMethods

Return the Session to which an object belongs.

This is an alias of object_session().

Prepare the current transaction in progress for two phase commit.

If no transaction is in progress, this method raises an InvalidRequestError.

Only root transactions of two phase sessions can be prepared. If the current transaction is not such, an InvalidRequestError is raised.

Return a new Query object corresponding to this Session.

Note that the Query object is legacy as of SQLAlchemy 2.0; the select() construct is now used to construct ORM queries.

SQLAlchemy Unified Tutorial

Legacy Query API - legacy API doc

Expire and refresh attributes on the given instance.

The selected attributes will first be expired as they would when using Session.expire(); then a SELECT statement will be issued to the database to refresh column-oriented attributes with the current value available in the current transaction.

relationship() oriented attributes will also be immediately loaded if they were already eagerly loaded on the object, using the same eager loading strategy that they were loaded with originally.

Added in version 1.4: - the Session.refresh() method can also refresh eagerly loaded attributes.

relationship() oriented attributes that would normally load using the select (or “lazy”) loader strategy will also load if they are named explicitly in the attribute_names collection, emitting a SELECT statement for the attribute using the immediate loader strategy. If lazy-loaded relationships are not named in Session.refresh.attribute_names, then they remain as “lazy loaded” attributes and are not implicitly refreshed.

Changed in version 2.0.4: The Session.refresh() method will now refresh lazy-loaded relationship() oriented attributes for those which are named explicitly in the Session.refresh.attribute_names collection.

While the Session.refresh() method is capable of refreshing both column and relationship oriented attributes, its primary focus is on refreshing of local column-oriented attributes on a single instance. For more open ended “refresh” functionality, including the ability to refresh the attributes on many objects at once while having explicit control over relationship loader strategies, use the populate existing feature instead.

Note that a highly isolated transaction will return the same values as were previously read in that same transaction, regardless of changes in database state outside of that transaction. Refreshing attributes usually only makes sense at the start of a transaction where database rows have not yet been accessed.

attribute_names¶ – optional. An iterable collection of string attribute names indicating a subset of attributes to be refreshed.

with_for_update¶ – optional boolean True indicating FOR UPDATE should be used, or may be a dictionary containing flags to indicate a more specific set of FOR UPDATE flags for the SELECT; flags should match the parameters of Query.with_for_update(). Supersedes the Session.refresh.lockmode parameter.

Refreshing / Expiring - introductory material

Populate Existing - allows any ORM query to refresh objects as they would be loaded normally.

Close out the transactional resources and ORM objects used by this Session, resetting the session to its initial state.

This method provides for same “reset-only” behavior that the Session.close() method has provided historically, where the state of the Session is reset as though the object were brand new, and ready to be used again. This method may then be useful for Session objects which set Session.close_resets_only to False, so that “reset only” behavior is still available.

Added in version 2.0.22.

Closing - detail on the semantics of Session.close() and Session.reset().

Session.close() - a similar method will additionally prevent reuse of the Session when the parameter Session.close_resets_only is set to False.

Rollback the current transaction in progress.

If no transaction is in progress, this method is a pass-through.

The method always rolls back the topmost database transaction, discarding any nested transactions that may be in progress.

Managing Transactions

Execute a statement and return a scalar result.

Usage and parameters are the same as that of Session.execute(); the return result is a scalar Python value.

Execute a statement and return the results as scalars.

Usage and parameters are the same as that of Session.execute(); the return result is a ScalarResult filtering object which will return single elements rather than Row objects.

a ScalarResult object

Added in version 1.4.24: Added Session.scalars()

Added in version 1.4.26: Added scoped_session.scalars()

Selecting ORM Entities - contrasts the behavior of Session.execute() to Session.scalars()

inherits from sqlalchemy.orm.state_changes._StateChange, sqlalchemy.engine.util.TransactionalContext

A Session-level transaction.

SessionTransaction is produced from the Session.begin() and Session.begin_nested() methods. It’s largely an internal object that in modern use provides a context manager for session transactions.

Documentation on interacting with SessionTransaction is at: Managing Transactions.

Changed in version 1.4: The scoping and API methods to work with the SessionTransaction object directly have been simplified.

Managing Transactions

Session.begin_nested()

Session.in_transaction()

Session.in_nested_transaction()

Session.get_transaction()

Session.get_nested_transaction()

Indicates if this is a nested, or SAVEPOINT, transaction.

Origin of this SessionTransaction.

Indicates if this is a nested, or SAVEPOINT, transaction.

When SessionTransaction.nested is True, it is expected that SessionTransaction.parent will be present as well, linking to the enclosing SessionTransaction.

SessionTransaction.origin

Origin of this SessionTransaction.

Refers to a SessionTransactionOrigin instance which is an enumeration indicating the source event that led to constructing this SessionTransaction.

Added in version 2.0.

The parent SessionTransaction of this SessionTransaction.

If this attribute is None, indicates this SessionTransaction is at the top of the stack, and corresponds to a real “COMMIT”/”ROLLBACK” block. If non-None, then this is either a “subtransaction” (an internal marker object used by the flush process) or a “nested” / SAVEPOINT transaction. If the SessionTransaction.nested attribute is True, then this is a SAVEPOINT, and if False, indicates this a subtransaction.

inherits from enum.Enum

indicates the origin of a SessionTransaction.

This enumeration is present on the SessionTransaction.origin attribute of any SessionTransaction object.

Added in version 2.0.

transaction were started by autobegin

transaction were started by calling Session.begin()

transaction were started by Session.begin_nested()

transaction is an internal “subtransaction”

transaction were started by autobegin

transaction were started by calling Session.begin()

transaction were started by Session.begin_nested()

transaction is an internal “subtransaction”

Close all sessions in memory.

make_transient(instance)

Alter the state of the given instance so that it is transient.

make_transient_to_detached(instance)

Make the given transient instance detached.

object_session(instance)

Return the Session to which the given instance belongs.

Return True if the given object was deleted within a session flush.

Close all sessions in memory.

This function consults a global registry of all Session objects and calls Session.close() on them, which resets them to a clean state.

This function is not for general use but may be useful for test suites within the teardown scheme.

Added in version 1.3.

Alter the state of the given instance so that it is transient.

make_transient() is a special-case function for advanced use cases only.

The given mapped instance is assumed to be in the persistent or detached state. The function will remove its association with any Session as well as its InstanceState.identity. The effect is that the object will behave as though it were newly constructed, except retaining any attribute / collection values that were loaded at the time of the call. The InstanceState.deleted flag is also reset if this object had been deleted as a result of using Session.delete().

make_transient() does not “unexpire” or otherwise eagerly load ORM-mapped attributes that are not currently loaded at the time the function is called. This includes attributes which:

were expired via Session.expire()

were expired as the natural effect of committing a session transaction, e.g. Session.commit()

are normally lazy loaded but are not currently loaded

are “deferred” (see Limiting which Columns Load with Column Deferral) and are not yet loaded

were not present in the query which loaded this object, such as that which is common in joined table inheritance and other scenarios.

After make_transient() is called, unloaded attributes such as those above will normally resolve to the value None when accessed, or an empty collection for a collection-oriented attribute. As the object is transient and un-associated with any database identity, it will no longer retrieve these values.

make_transient_to_detached()

Make the given transient instance detached.

make_transient_to_detached() is a special-case function for advanced use cases only.

All attribute history on the given instance will be reset as though the instance were freshly loaded from a query. Missing attributes will be marked as expired. The primary key attributes of the object, which are required, will be made into the “key” of the instance.

The object can then be added to a session, or merged possibly with the load=False flag, at which point it will look as if it were loaded that way, without emitting SQL.

This is a special use case function that differs from a normal call to Session.merge() in that a given persistent state can be manufactured without any SQL calls.

Session.enable_relationship_loading()

Return the Session to which the given instance belongs.

This is essentially the same as the InstanceState.session accessor. See that attribute for details.

Return True if the given object was deleted within a session flush.

This is regardless of whether or not the object is persistent or detached.

InstanceState.was_deleted

These functions are provided by the SQLAlchemy attribute instrumentation API to provide a detailed interface for dealing with instances, attribute values, and history. Some of them are useful when constructing event listener functions, such as those described in ORM Events.

del_attribute(instance, key)

Delete the value of an attribute, firing history events.

Mark an instance as ‘dirty’ without any specific attribute mentioned.

flag_modified(instance, key)

Mark an attribute on an instance as ‘modified’.

get_attribute(instance, key)

Get the value of an attribute, firing any callables required.

get_history(obj, key[, passive])

Return a History record for the given object and attribute key.

A 3-tuple of added, unchanged and deleted values, representing the changes which have occurred on an instrumented attribute.

init_collection(obj, key)

Initialize a collection attribute and return the collection adapter.

Return the InstanceState for a given mapped object.

is_instrumented(instance, key)

Return True if the given attribute on the given instance is instrumented by the attributes package.

object_state(instance)

Given an object, return the InstanceState associated with the object.

set_attribute(instance, key, value[, initiator])

Set the value of an attribute, firing history events.

set_committed_value(instance, key, value)

Set the value of an attribute with no history events.

Given an object, return the InstanceState associated with the object.

Raises sqlalchemy.orm.exc.UnmappedInstanceError if no mapping is configured.

Equivalent functionality is available via the inspect() function as:

Using the inspection system will raise sqlalchemy.exc.NoInspectionAvailable if the instance is not part of a mapping.

Delete the value of an attribute, firing history events.

This function may be used regardless of instrumentation applied directly to the class, i.e. no descriptors are required. Custom attribute management schemes will need to make usage of this method to establish attribute state as understood by SQLAlchemy.

Get the value of an attribute, firing any callables required.

This function may be used regardless of instrumentation applied directly to the class, i.e. no descriptors are required. Custom attribute management schemes will need to make usage of this method to make usage of attribute state as understood by SQLAlchemy.

Return a History record for the given object and attribute key.

This is the pre-flush history for a given attribute, which is reset each time the Session flushes changes to the current database transaction.

Prefer to use the AttributeState.history and AttributeState.load_history() accessors to retrieve the History for instance attributes.

obj¶ – an object whose class is instrumented by the attributes package.

key¶ – string attribute name.

passive¶ – indicates loading behavior for the attribute if the value is not already present. This is a bitflag attribute, which defaults to the symbol PASSIVE_OFF indicating all necessary SQL should be emitted.

AttributeState.history

AttributeState.load_history() - retrieve history using loader callables if the value is not locally present.

Initialize a collection attribute and return the collection adapter.

This function is used to provide direct access to collection internals for a previously unloaded attribute. e.g.:

For an easier way to do the above, see set_committed_value().

obj¶ – a mapped object

key¶ – string attribute name where the collection is located.

Mark an attribute on an instance as ‘modified’.

This sets the ‘modified’ flag on the instance and establishes an unconditional change event for the given attribute. The attribute must have a value present, else an InvalidRequestError is raised.

To mark an object “dirty” without referring to any specific attribute so that it is considered within a flush, use the flag_dirty() call.

Mark an instance as ‘dirty’ without any specific attribute mentioned.

This is a special operation that will allow the object to travel through the flush process for interception by events such as SessionEvents.before_flush(). Note that no SQL will be emitted in the flush process for an object that has no changes, even if marked dirty via this method. However, a SessionEvents.before_flush() handler will be able to see the object in the Session.dirty collection and may establish changes on it, which will then be included in the SQL emitted.

Added in version 1.2.

Return the InstanceState for a given mapped object.

This function is the internal version of object_state(). The object_state() and/or the inspect() function is preferred here as they each emit an informative exception if the given object is not mapped.

Return True if the given attribute on the given instance is instrumented by the attributes package.

This function may be used regardless of instrumentation applied directly to the class, i.e. no descriptors are required.

Set the value of an attribute, firing history events.

This function may be used regardless of instrumentation applied directly to the class, i.e. no descriptors are required. Custom attribute management schemes will need to make usage of this method to establish attribute state as understood by SQLAlchemy.

instance¶ – the object that will be modified

key¶ – string name of the attribute

value¶ – value to assign

an instance of Event that would have been propagated from a previous event listener. This argument is used when the set_attribute() function is being used within an existing event listening function where an Event object is being supplied; the object may be used to track the origin of the chain of events.

Added in version 1.2.3.

Set the value of an attribute with no history events.

Cancels any previous history present. The value should be a scalar value for scalar-holding attributes, or an iterable for any collection-holding attribute.

This is the same underlying method used when a lazy loader fires off and loads additional data from the database. In particular, this method can be used by application code which has loaded additional attributes or collections through separate queries, which can then be attached to an instance as though it were part of its original loaded state.

inherits from builtins.tuple

A 3-tuple of added, unchanged and deleted values, representing the changes which have occurred on an instrumented attribute.

The easiest way to get a History object for a particular attribute on an object is to use the inspect() function:

Each tuple member is an iterable sequence:

added - the collection of items added to the attribute (the first tuple element).

unchanged - the collection of items that have not changed on the attribute (the second tuple element).

deleted - the collection of items that have been removed from the attribute (the third tuple element).

Alias for field number 0

Alias for field number 2

Return True if this History has no changes and no existing, unchanged state.

Return True if this History has changes.

Return a collection of unchanged + deleted.

Return a collection of added + unchanged.

Return a collection of added + unchanged + deleted.

Alias for field number 1

Alias for field number 0

Alias for field number 2

Return True if this History has no changes and no existing, unchanged state.

Return True if this History has changes.

Return a collection of unchanged + deleted.

Return a collection of added + unchanged.

Return a collection of added + unchanged + deleted.

Alias for field number 1

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# an Engine, which the Session will use for connection
# resources
engine = create_engine("postgresql+psycopg2://scott:tiger@localhost/")

Session = sessionmaker(engine)

with Session() as session:
    session.add(some_object)
    session.add(some_other_object)
    session.commit()
```

Example 2 (yaml):
```yaml
session = Session()
try:
    session.add(some_object)
    session.add(some_other_object)
    session.commit()
finally:
    session.close()
```

Example 3 (markdown):
```markdown
Session = sessionmaker(engine)

with Session.begin() as session:
    session.add(some_object)
    session.add(some_other_object)
# commits transaction, closes session
```

Example 4 (markdown):
```markdown
Session = sessionmaker(engine)

# bind an individual session to a connection

with engine.connect() as connection:
    with Session(bind=connection) as session:
        ...  # work with session
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/faq/sessions.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - Frequently Asked Questions
    - Project Versions
- Sessions / Queries¶
- I’m re-loading data with my Session but it isn’t seeing changes that I committed elsewhere¶
- “This Session’s transaction has been rolled back due to a previous exception during flush.” (or similar)¶
  - But why does flush() insist on issuing a ROLLBACK?¶
  - But why isn’t the one automatic call to ROLLBACK enough? Why must I ROLLBACK again?¶
- How do I make a Query that always adds a certain filter to every query?¶

Home | Download this Documentation

Home | Download this Documentation

I’m re-loading data with my Session but it isn’t seeing changes that I committed elsewhere

“This Session’s transaction has been rolled back due to a previous exception during flush.” (or similar)

But why does flush() insist on issuing a ROLLBACK?

But why isn’t the one automatic call to ROLLBACK enough? Why must I ROLLBACK again?

How do I make a Query that always adds a certain filter to every query?

My Query does not return the same number of objects as query.count() tells me - why?

I’ve created a mapping against an Outer Join, and while the query returns rows, no objects are returned. Why not?

I’m using joinedload() or lazy=False to create a JOIN/OUTER JOIN and SQLAlchemy is not constructing the correct query when I try to add a WHERE, ORDER BY, LIMIT, etc. (which relies upon the (OUTER) JOIN)

Query has no __len__(), why not?

How Do I use Textual SQL with ORM Queries?

I’m calling Session.delete(myobject) and it isn’t removed from the parent collection!

why isn’t my __init__() called when I load objects?

how do I use ON DELETE CASCADE with SA’s ORM?

I set the “foo_id” attribute on my instance to “7”, but the “foo” attribute is still None - shouldn’t it have loaded Foo with id #7?

How do I walk all objects that are related to a given object?

Is there a way to automagically have only unique keywords (or other kinds of objects) without doing a query for the keyword and getting a reference to the row containing that keyword?

Why does post_update emit UPDATE in addition to the first UPDATE?

The main issue regarding this behavior is that the session acts as though the transaction is in the serializable isolation state, even if it’s not (and it usually is not). In practical terms, this means that the session does not alter any data that it’s already read within the scope of a transaction.

If the term “isolation level” is unfamiliar, then you first need to read this link:

In short, serializable isolation level generally means that once you SELECT a series of rows in a transaction, you will get the identical data back each time you re-emit that SELECT. If you are in the next-lower isolation level, “repeatable read”, you’ll see newly added rows (and no longer see deleted rows), but for rows that you’ve already loaded, you won’t see any change. Only if you are in a lower isolation level, e.g. “read committed”, does it become possible to see a row of data change its value.

For information on controlling the isolation level when using the SQLAlchemy ORM, see Setting Transaction Isolation Levels / DBAPI AUTOCOMMIT.

To simplify things dramatically, the Session itself works in terms of a completely isolated transaction, and doesn’t overwrite any mapped attributes it’s already read unless you tell it to. The use case of trying to re-read data you’ve already loaded in an ongoing transaction is an uncommon use case that in many cases has no effect, so this is considered to be the exception, not the norm; to work within this exception, several methods are provided to allow specific data to be reloaded within the context of an ongoing transaction.

To understand what we mean by “the transaction” when we talk about the Session, your Session is intended to only work within a transaction. An overview of this is at Managing Transactions.

Once we’ve figured out what our isolation level is, and we think that our isolation level is set at a low enough level so that if we re-SELECT a row, we should see new data in our Session, how do we see it?

Three ways, from most common to least:

We simply end our transaction and start a new one on next access with our Session by calling Session.commit() (note that if the Session is in the lesser-used “autocommit” mode, there would be a call to Session.begin() as well). The vast majority of applications and use cases do not have any issues with not being able to “see” data in other transactions because they stick to this pattern, which is at the core of the best practice of short lived transactions. See When do I construct a Session, when do I commit it, and when do I close it? for some thoughts on this.

We tell our Session to re-read rows that it has already read, either when we next query for them using Session.expire_all() or Session.expire(), or immediately on an object using refresh. See Refreshing / Expiring for detail on this.

We can run whole queries while setting them to definitely overwrite already-loaded objects as they read rows by using “populate existing”. This is an execution option described at Populate Existing.

But remember, the ORM cannot see changes in rows if our isolation level is repeatable read or higher, unless we start a new transaction.

This is an error that occurs when a Session.flush() raises an exception, rolls back the transaction, but further commands upon the Session are called without an explicit call to Session.rollback() or Session.close().

It usually corresponds to an application that catches an exception upon Session.flush() or Session.commit() and does not properly handle the exception. For example:

The usage of the Session should fit within a structure similar to this:

Many things can cause a failure within the try/except besides flushes. Applications should ensure some system of “framing” is applied to ORM-oriented processes so that connection and transaction resources have a definitive boundary, and so that transactions can be explicitly rolled back if any failure conditions occur.

This does not mean there should be try/except blocks throughout an application, which would not be a scalable architecture. Instead, a typical approach is that when ORM-oriented methods and functions are first called, the process that’s calling the functions from the very top would be within a block that commits transactions at the successful completion of a series of operations, as well as rolls transactions back if operations fail for any reason, including failed flushes. There are also approaches using function decorators or context managers to achieve similar results. The kind of approach taken depends very much on the kind of application being written.

For a detailed discussion on how to organize usage of the Session, please see When do I construct a Session, when do I commit it, and when do I close it?.

It would be great if Session.flush() could partially complete and then not roll back, however this is beyond its current capabilities since its internal bookkeeping would have to be modified such that it can be halted at any time and be exactly consistent with what’s been flushed to the database. While this is theoretically possible, the usefulness of the enhancement is greatly decreased by the fact that many database operations require a ROLLBACK in any case. Postgres in particular has operations which, once failed, the transaction is not allowed to continue:

What SQLAlchemy offers that solves both issues is support of SAVEPOINT, via Session.begin_nested(). Using Session.begin_nested(), you can frame an operation that may potentially fail within a transaction, and then “roll back” to the point before its failure while maintaining the enclosing transaction.

The rollback that’s caused by the flush() is not the end of the complete transaction block; while it ends the database transaction in play, from the Session point of view there is still a transaction that is now in an inactive state.

Given a block such as:

Above, when a Session is first created, assuming “autocommit mode” isn’t used, a logical transaction is established within the Session. This transaction is “logical” in that it does not actually use any database resources until a SQL statement is invoked, at which point a connection-level and DBAPI-level transaction is started. However, whether or not database-level transactions are part of its state, the logical transaction will stay in place until it is ended using Session.commit(), Session.rollback(), or Session.close().

When the flush() above fails, the code is still within the transaction framed by the try/commit/except/rollback block. If flush() were to fully roll back the logical transaction, it would mean that when we then reach the except: block the Session would be in a clean state, ready to emit new SQL on an all new transaction, and the call to Session.rollback() would be out of sequence. In particular, the Session would have begun a new transaction by this point, which the Session.rollback() would be acting upon erroneously. Rather than allowing SQL operations to proceed on a new transaction in this place where normal usage dictates a rollback is about to take place, the Session instead refuses to continue until the explicit rollback actually occurs.

In other words, it is expected that the calling code will always call Session.commit(), Session.rollback(), or Session.close() to correspond to the current transaction block. flush() keeps the Session within this transaction block so that the behavior of the above code is predictable and consistent.

See the recipe at FilteredQuery.

The Query object, when asked to return a list of ORM-mapped objects, will deduplicate the objects based on primary key. That is, if we for example use the User mapping described at Using ORM Declarative Forms to Define Table Metadata, and we had a SQL query like the following:

Above, the sample data used in the tutorial has two rows in the addresses table for the users row with the name 'jack', primary key value 5. If we ask the above query for a Query.count(), we will get the answer 2:

However, if we run Query.all() or iterate over the query, we get back one element:

This is because when the Query object returns full entities, they are deduplicated. This does not occur if we instead request individual columns back:

There are two main reasons the Query will deduplicate:

To allow joined eager loading to work correctly - Joined Eager Loading works by querying rows using joins against related tables, where it then routes rows from those joins into collections upon the lead objects. In order to do this, it has to fetch rows where the lead object primary key is repeated for each sub-entry. This pattern can then continue into further sub-collections such that a multiple of rows may be processed for a single lead object, such as User(id=5). The dedpulication allows us to receive objects in the way they were queried, e.g. all the User() objects whose name is 'jack' which for us is one object, with the User.addresses collection eagerly loaded as was indicated either by lazy='joined' on the relationship() or via the joinedload() option. For consistency, the deduplication is still applied whether or not the joinedload is established, as the key philosophy behind eager loading is that these options never affect the result.

To eliminate confusion regarding the identity map - this is admittedly the less critical reason. As the Session makes use of an identity map, even though our SQL result set has two rows with primary key 5, there is only one User(id=5) object inside the Session which must be maintained uniquely on its identity, that is, its primary key / class combination. It doesn’t actually make much sense, if one is querying for User() objects, to get the same object multiple times in the list. An ordered set would potentially be a better representation of what Query seeks to return when it returns full objects.

The issue of Query deduplication remains problematic, mostly for the single reason that the Query.count() method is inconsistent, and the current status is that joined eager loading has in recent releases been superseded first by the “subquery eager loading” strategy and more recently the “select IN eager loading” strategy, both of which are generally more appropriate for collection eager loading. As this evolution continues, SQLAlchemy may alter this behavior on Query, which may also involve new APIs in order to more directly control this behavior, and may also alter the behavior of joined eager loading in order to create a more consistent usage pattern.

Rows returned by an outer join may contain NULL for part of the primary key, as the primary key is the composite of both tables. The Query object ignores incoming rows that don’t have an acceptable primary key. Based on the setting of the allow_partial_pks flag on Mapper, a primary key is accepted if the value has at least one non-NULL value, or alternatively if the value has no NULL values. See allow_partial_pks at Mapper.

The joins generated by joined eager loading are only used to fully load related collections, and are designed to have no impact on the primary results of the query. Since they are anonymously aliased, they cannot be referenced directly.

For detail on this behavior, see The Zen of Joined Eager Loading.

The Python __len__() magic method applied to an object allows the len() builtin to be used to determine the length of the collection. It’s intuitive that a SQL query object would link __len__() to the Query.count() method, which emits a SELECT COUNT. The reason this is not possible is because evaluating the query as a list would incur two SQL calls instead of one:

Getting ORM Results from Textual Statements - Ad-hoc textual blocks with Query

Using SQL Expressions with Sessions - Using Session with textual SQL directly.

See Notes on Delete - Deleting Objects Referenced from Collections and Scalar Relationships for a description of this behavior.

See Maintaining Non-Mapped State Across Loads for a description of this behavior.

SQLAlchemy will always issue UPDATE or DELETE statements for dependent rows which are currently loaded in the Session. For rows which are not loaded, it will by default issue SELECT statements to load those rows and update/delete those as well; in other words it assumes there is no ON DELETE CASCADE configured. To configure SQLAlchemy to cooperate with ON DELETE CASCADE, see Using foreign key ON DELETE cascade with ORM relationships.

The ORM is not constructed in such a way as to support immediate population of relationships driven from foreign key attribute changes - instead, it is designed to work the other way around - foreign key attributes are handled by the ORM behind the scenes, the end user sets up object relationships naturally. Therefore, the recommended way to set o.foo is to do just that - set it!:

Manipulation of foreign key attributes is of course entirely legal. However, setting a foreign-key attribute to a new value currently does not trigger an “expire” event of the relationship() in which it’s involved. This means that for the following sequence:

o.foo is loaded with its effective database value of None when it is first accessed. Setting o.foo_id = 7 will have the value of “7” as a pending change, but no flush has occurred - so o.foo is still None:

For o.foo to load based on the foreign key mutation is usually achieved naturally after the commit, which both flushes the new foreign key value and expires all state:

A more minimal operation is to expire the attribute individually - this can be performed for any persistent object using Session.expire():

Note that if the object is not persistent but present in the Session, it’s known as pending. This means the row for the object has not been INSERTed into the database yet. For such an object, setting foo_id does not have meaning until the row is inserted; otherwise there is no row yet:

Attribute loading for non-persistent objects

One variant on the “pending” behavior above is if we use the flag load_on_pending on relationship(). When this flag is set, the lazy loader will emit for new_obj.foo before the INSERT proceeds; another variant of this is to use the Session.enable_relationship_loading() method, which can “attach” an object to a Session in such a way that many-to-one relationships load as according to foreign key attributes regardless of the object being in any particular state. Both techniques are not recommended for general use; they were added to suit specific programming scenarios encountered by users which involve the repurposing of the ORM’s usual object states.

The recipe ExpireRelationshipOnFKChange features an example using SQLAlchemy events in order to coordinate the setting of foreign key attributes with many-to-one relationships.

An object that has other objects related to it will correspond to the relationship() constructs set up between mappers. This code fragment will iterate all the objects, correcting for cycles as well:

The function can be demonstrated as follows:

When people read the many-to-many example in the docs, they get hit with the fact that if you create the same Keyword twice, it gets put in the DB twice. Which is somewhat inconvenient.

This UniqueObject recipe was created to address this issue.

The post_update feature, documented at Rows that point to themselves / Mutually Dependent Rows, involves that an UPDATE statement is emitted in response to changes to a particular relationship-bound foreign key, in addition to the INSERT/UPDATE/DELETE that would normally be emitted for the target row. While the primary purpose of this UPDATE statement is that it pairs up with an INSERT or DELETE of that row, so that it can post-set or pre-unset a foreign key reference in order to break a cycle with a mutually dependent foreign key, it currently is also bundled as a second UPDATE that emits when the target row itself is subject to an UPDATE. In this case, the UPDATE emitted by post_update is usually unnecessary and will often appear wasteful.

However, some research into trying to remove this “UPDATE / UPDATE” behavior reveals that major changes to the unit of work process would need to occur not just throughout the post_update implementation, but also in areas that aren’t related to post_update for this to work, in that the order of operations would need to be reversed on the non-post_update side in some cases, which in turn can impact other cases, such as correctly handling an UPDATE of a referenced primary key value (see #1063 for a proof of concept).

The answer is that “post_update” is used to break a cycle between two mutually dependent foreign keys, and to have this cycle breaking be limited to just INSERT/DELETE of the target table implies that the ordering of UPDATE statements elsewhere would need to be liberalized, leading to breakage in other edge cases.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(create_engine("sqlite://"))


class Foo(Base):
    __tablename__ = "foo"
    id = Column(Integer, primary_key=True)


Base.metadata.create_all()

session = sessionmaker()()

# constraint violation
session.add_all([Foo(id=1), Foo(id=1)])

try:
    session.commit()
except:
    # ignore error
    pass

# continue using session without rolling back
session.commit()
```

Example 2 (jsx):
```jsx
try:
    # <use session>
    session.commit()
except:
    session.rollback()
    raise
finally:
    session.close()  # optional, depends on use case
```

Example 3 (sql):
```sql
test=> create table foo(id integer primary key);
NOTICE:  CREATE TABLE / PRIMARY KEY will create implicit index "foo_pkey" for table "foo"
CREATE TABLE
test=> begin;
BEGIN
test=> insert into foo values(1);
INSERT 0 1
test=> commit;
COMMIT
test=> begin;
BEGIN
test=> insert into foo values(1);
ERROR:  duplicate key value violates unique constraint "foo_pkey"
test=> insert into foo values(2);
ERROR:  current transaction is aborted, commands ignored until end of transaction block
```

Example 4 (yaml):
```yaml
sess = Session()  # begins a logical transaction
try:
    sess.flush()

    sess.commit()
except:
    sess.rollback()
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/session_state_management.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- State Management¶
- Quickie Intro to Object States¶
  - Getting the Current State of an Object¶
- Session Attributes¶
- Session Referencing Behavior¶
- Merging¶

Home | Download this Documentation

Home | Download this Documentation

It’s helpful to know the states which an instance can have within a session:

Transient - an instance that’s not in a session, and is not saved to the database; i.e. it has no database identity. The only relationship such an object has to the ORM is that its class has a Mapper associated with it.

Pending - when you Session.add() a transient instance, it becomes pending. It still wasn’t actually flushed to the database yet, but it will be when the next flush occurs.

Persistent - An instance which is present in the session and has a record in the database. You get persistent instances by either flushing so that the pending instances become persistent, or by querying the database for existing instances (or moving persistent instances from other sessions into your local session).

Deleted - An instance which has been deleted within a flush, but the transaction has not yet completed. Objects in this state are essentially in the opposite of “pending” state; when the session’s transaction is committed, the object will move to the detached state. Alternatively, when the session’s transaction is rolled back, a deleted object moves back to the persistent state.

Detached - an instance which corresponds, or previously corresponded, to a record in the database, but is not currently in any session. The detached object will contain a database identity marker, however because it is not associated with a session, it is unknown whether or not this database identity actually exists in a target database. Detached objects are safe to use normally, except that they have no ability to load unloaded attributes or attributes that were previously marked as “expired”.

For a deeper dive into all possible state transitions, see the section Object Lifecycle Events which describes each transition as well as how to programmatically track each one.

The actual state of any mapped object can be viewed at any time using the inspect() function on a mapped instance; this function will return the corresponding InstanceState object which manages the internal ORM state for the object. InstanceState provides, among other accessors, boolean attributes indicating the persistence state of the object, including:

InstanceState.transient

InstanceState.pending

InstanceState.persistent

InstanceState.deleted

InstanceState.detached

Inspection of Mapped Instances - further examples of InstanceState

The Session itself acts somewhat like a set-like collection. All items present may be accessed using the iterator interface:

And presence may be tested for using regular “contains” semantics:

The session is also keeping track of all newly created (i.e. pending) objects, all objects which have had changes since they were last loaded or saved (i.e. “dirty”), and everything that’s been marked as deleted:

(Documentation: Session.new, Session.dirty, Session.deleted, Session.identity_map).

Objects within the session are weakly referenced. This means that when they are dereferenced in the outside application, they fall out of scope from within the Session as well and are subject to garbage collection by the Python interpreter. The exceptions to this include objects which are pending, objects which are marked as deleted, or persistent objects which have pending changes on them. After a full flush, these collections are all empty, and all objects are again weakly referenced.

To cause objects in the Session to remain strongly referenced, usually a simple approach is all that’s needed. Examples of externally managed strong-referencing behavior include loading objects into a local dictionary keyed to their primary key, or into lists or sets for the span of time that they need to remain referenced. These collections can be associated with a Session, if desired, by placing them into the Session.info dictionary.

An event based approach is also feasible. A simple recipe that provides “strong referencing” behavior for all objects as they remain within the persistent state is as follows:

Above, we intercept the SessionEvents.pending_to_persistent(), SessionEvents.detached_to_persistent(), SessionEvents.deleted_to_persistent() and SessionEvents.loaded_as_persistent() event hooks in order to intercept objects as they enter the persistent transition, and the SessionEvents.persistent_to_detached() and SessionEvents.persistent_to_deleted() hooks to intercept objects as they leave the persistent state.

The above function may be called for any Session in order to provide strong-referencing behavior on a per-Session basis:

It may also be called for any sessionmaker:

Session.merge() transfers state from an outside object into a new or already existing instance within a session. It also reconciles the incoming data against the state of the database, producing a history stream which will be applied towards the next flush, or alternatively can be made to produce a simple “transfer” of state without producing change history or accessing the database. Usage is as follows:

When given an instance, it follows these steps:

It examines the primary key of the instance. If it’s present, it attempts to locate that instance in the local identity map. If the load=True flag is left at its default, it also checks the database for this primary key if not located locally.

If the given instance has no primary key, or if no instance can be found with the primary key given, a new instance is created.

The state of the given instance is then copied onto the located/newly created instance. For attribute values which are present on the source instance, the value is transferred to the target instance. For attribute values that aren’t present on the source instance, the corresponding attribute on the target instance is expired from memory, which discards any locally present value from the target instance for that attribute, but no direct modification is made to the database-persisted value for that attribute.

If the load=True flag is left at its default, this copy process emits events and will load the target object’s unloaded collections for each attribute present on the source object, so that the incoming state can be reconciled against what’s present in the database. If load is passed as False, the incoming data is “stamped” directly without producing any history.

The operation is cascaded to related objects and collections, as indicated by the merge cascade (see Cascades).

The new instance is returned.

With Session.merge(), the given “source” instance is not modified nor is it associated with the target Session, and remains available to be merged with any number of other Session objects. Session.merge() is useful for taking the state of any kind of object structure without regard for its origins or current session associations and copying its state into a new session. Here’s some examples:

An application which reads an object structure from a file and wishes to save it to the database might parse the file, build up the structure, and then use Session.merge() to save it to the database, ensuring that the data within the file is used to formulate the primary key of each element of the structure. Later, when the file has changed, the same process can be re-run, producing a slightly different object structure, which can then be merged in again, and the Session will automatically update the database to reflect those changes, loading each object from the database by primary key and then updating its state with the new state given.

An application is storing objects in an in-memory cache, shared by many Session objects simultaneously. Session.merge() is used each time an object is retrieved from the cache to create a local copy of it in each Session which requests it. The cached object remains detached; only its state is moved into copies of itself that are local to individual Session objects.

In the caching use case, it’s common to use the load=False flag to remove the overhead of reconciling the object’s state with the database. There’s also a “bulk” version of Session.merge() called Query.merge_result() that was designed to work with cache-extended Query objects - see the section Dogpile Caching.

An application wants to transfer the state of a series of objects into a Session maintained by a worker thread or other concurrent system. Session.merge() makes a copy of each object to be placed into this new Session. At the end of the operation, the parent thread/process maintains the objects it started with, and the thread/worker can proceed with local copies of those objects.

In the “transfer between threads/processes” use case, the application may want to use the load=False flag as well to avoid overhead and redundant SQL queries as the data is transferred.

Session.merge() is an extremely useful method for many purposes. However, it deals with the intricate border between objects that are transient/detached and those that are persistent, as well as the automated transference of state. The wide variety of scenarios that can present themselves here often require a more careful approach to the state of objects. Common problems with merge usually involve some unexpected state regarding the object being passed to Session.merge().

Lets use the canonical example of the User and Address objects:

Assume a User object with one Address, already persistent:

We now create a1, an object outside the session, which we’d like to merge on top of the existing Address:

A surprise would occur if we said this:

Why is that ? We weren’t careful with our cascades. The assignment of a1.user to a persistent object cascaded to the backref of User.addresses and made our a1 object pending, as though we had added it. Now we have two Address objects in the session:

Above, our a1 is already pending in the session. The subsequent Session.merge() operation essentially does nothing. Cascade can be configured via the relationship.cascade option on relationship(), although in this case it would mean removing the save-update cascade from the User.addresses relationship - and usually, that behavior is extremely convenient. The solution here would usually be to not assign a1.user to an object already persistent in the target session.

The cascade_backrefs=False option of relationship() will also prevent the Address from being added to the session via the a1.user = u1 assignment.

Further detail on cascade operation is at Cascades.

Another example of unexpected state:

Above, the assignment of user takes precedence over the foreign key assignment of user_id, with the end result that None is applied to user_id, causing a failure.

Most Session.merge() issues can be examined by first checking - is the object prematurely in the session ?

Or is there state on the object that we don’t want ? Examining __dict__ is a quick way to check:

Expunge removes an object from the Session, sending persistent instances to the detached state, and pending instances to the transient state:

To remove all items, call Session.expunge_all() (this method was formerly known as clear()).

Expiring means that the database-persisted data held inside a series of object attributes is erased, in such a way that when those attributes are next accessed, a SQL query is emitted which will refresh that data from the database.

When we talk about expiration of data we are usually talking about an object that is in the persistent state. For example, if we load an object as follows:

The above User object is persistent, and has a series of attributes present; if we were to look inside its __dict__, we’d see that state loaded:

where id and name refer to those columns in the database. _sa_instance_state is a non-database-persisted value used by SQLAlchemy internally (it refers to the InstanceState for the instance. While not directly relevant to this section, if we want to get at it, we should use the inspect() function to access it).

At this point, the state in our User object matches that of the loaded database row. But upon expiring the object using a method such as Session.expire(), we see that the state is removed:

We see that while the internal “state” still hangs around, the values which correspond to the id and name columns are gone. If we were to access one of these columns and are watching SQL, we’d see this:

Above, upon accessing the expired attribute user.name, the ORM initiated a lazy load to retrieve the most recent state from the database, by emitting a SELECT for the user row to which this user refers. Afterwards, the __dict__ is again populated:

While we are peeking inside of __dict__ in order to see a bit of what SQLAlchemy does with object attributes, we should not modify the contents of __dict__ directly, at least as far as those attributes which the SQLAlchemy ORM is maintaining (other attributes outside of SQLA’s realm are fine). This is because SQLAlchemy uses descriptors in order to track the changes we make to an object, and when we modify __dict__ directly, the ORM won’t be able to track that we changed something.

Another key behavior of both Session.expire() and Session.refresh() is that all un-flushed changes on an object are discarded. That is, if we were to modify an attribute on our User:

but then we call Session.expire() without first calling Session.flush(), our pending value of 'user2' is discarded:

The Session.expire() method can be used to mark as “expired” all ORM-mapped attributes for an instance:

it can also be passed a list of string attribute names, referring to specific attributes to be marked as expired:

The Session.expire_all() method allows us to essentially call Session.expire() on all objects contained within the Session at once:

The Session.refresh() method has a similar interface, but instead of expiring, it emits an immediate SELECT for the object’s row immediately:

Session.refresh() also accepts a list of string attribute names, but unlike Session.expire(), expects at least one name to be that of a column-mapped attribute:

An alternative method of refreshing which is often more flexible is to use the Populate Existing feature of the ORM, available for 2.0 style queries with select() as well as from the Query.populate_existing() method of Query within 1.x style queries. Using this execution option, all of the ORM objects returned in the result set of the statement will be refreshed with data from the database:

See Populate Existing for further detail.

The SELECT statement that’s emitted when an object marked with Session.expire() or loaded with Session.refresh() varies based on several factors, including:

The load of expired attributes is triggered from column-mapped attributes only. While any kind of attribute can be marked as expired, including a relationship() - mapped attribute, accessing an expired relationship() attribute will emit a load only for that attribute, using standard relationship-oriented lazy loading. Column-oriented attributes, even if expired, will not load as part of this operation, and instead will load when any column-oriented attribute is accessed.

relationship()- mapped attributes will not load in response to expired column-based attributes being accessed.

Regarding relationships, Session.refresh() is more restrictive than Session.expire() with regards to attributes that aren’t column-mapped. Calling Session.refresh() and passing a list of names that only includes relationship-mapped attributes will actually raise an error. In any case, non-eager-loading relationship() attributes will not be included in any refresh operation.

relationship() attributes configured as “eager loading” via the relationship.lazy parameter will load in the case of Session.refresh(), if either no attribute names are specified, or if their names are included in the list of attributes to be refreshed.

Attributes that are configured as deferred() will not normally load, during either the expired-attribute load or during a refresh. An unloaded attribute that’s deferred() instead loads on its own when directly accessed, or if part of a “group” of deferred attributes where an unloaded attribute in that group is accessed.

For expired attributes that are loaded on access, a joined-inheritance table mapping will emit a SELECT that typically only includes those tables for which unloaded attributes are present. The action here is sophisticated enough to load only the parent or child table, for example, if the subset of columns that were originally expired encompass only one or the other of those tables.

When Session.refresh() is used on a joined-inheritance table mapping, the SELECT emitted will resemble that of when Session.query() is used on the target object’s class. This is typically all those tables that are set up as part of the mapping.

The Session uses the expiration feature automatically whenever the transaction referred to by the session ends. Meaning, whenever Session.commit() or Session.rollback() is called, all objects within the Session are expired, using a feature equivalent to that of the Session.expire_all() method. The rationale is that the end of a transaction is a demarcating point at which there is no more context available in order to know what the current state of the database is, as any number of other transactions may be affecting it. Only when a new transaction starts can we again have access to the current state of the database, at which point any number of changes may have occurred.

Transaction Isolation

Of course, most databases are capable of handling multiple transactions at once, even involving the same rows of data. When a relational database handles multiple transactions involving the same tables or rows, this is when the isolation aspect of the database comes into play. The isolation behavior of different databases varies considerably and even on a single database can be configured to behave in different ways (via the so-called isolation level setting). In that sense, the Session can’t fully predict when the same SELECT statement, emitted a second time, will definitely return the data we already have, or will return new data. So as a best guess, it assumes that within the scope of a transaction, unless it is known that a SQL expression has been emitted to modify a particular row, there’s no need to refresh a row unless explicitly told to do so.

The Session.expire() and Session.refresh() methods are used in those cases when one wants to force an object to re-load its data from the database, in those cases when it is known that the current state of data is possibly stale. Reasons for this might include:

some SQL has been emitted within the transaction outside of the scope of the ORM’s object handling, such as if a Table.update() construct were emitted using the Session.execute() method;

if the application is attempting to acquire data that is known to have been modified in a concurrent transaction, and it is also known that the isolation rules in effect allow this data to be visible.

The second bullet has the important caveat that “it is also known that the isolation rules in effect allow this data to be visible.” This means that it cannot be assumed that an UPDATE that happened on another database connection will yet be visible here locally; in many cases, it will not. This is why if one wishes to use Session.expire() or Session.refresh() in order to view data between ongoing transactions, an understanding of the isolation behavior in effect is essential.

Populate Existing - allows any ORM query to refresh objects as they would be loaded normally, refreshing all matching objects in the identity map against the results of a SELECT statement.

isolation - glossary explanation of isolation which includes links to Wikipedia.

The SQLAlchemy Session In-Depth - a video + slides with an in-depth discussion of the object lifecycle including the role of data expiration.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (python):
```python
>>> from sqlalchemy import inspect
>>> insp = inspect(my_object)
>>> insp.persistent
True
```

Example 2 (python):
```python
for obj in session:
    print(obj)
```

Example 3 (python):
```python
if obj in session:
    print("Object is present")
```

Example 4 (markdown):
```markdown
# pending objects recently added to the Session
session.new

# persistent objects which currently have changes detected
# (this collection is now created on the fly each time the property is called)
session.dirty

# persistent objects that have been marked as deleted via session.delete(obj)
session.deleted

# dictionary of all persistent objects, keyed on their
# identity key
session.identity_map
```

---

## SQLAlchemy 2.0 Documentation

**URL:** https://docs.sqlalchemy.org/en/20/orm/session_transaction.html

**Contents:**
- SQLAlchemy 2.0 Documentation
  - SQLAlchemy 2.0 Documentation
  - SQLAlchemy ORM
    - Project Versions
- Transactions and Connection Management¶
- Managing Transactions¶
  - Using SAVEPOINT¶
  - Session-level vs. Engine level transaction control¶
    - Commit as you go¶
    - Begin Once¶

Home | Download this Documentation

Home | Download this Documentation

Changed in version 1.4: Session transaction management has been revised to be clearer and easier to use. In particular, it now features “autobegin” operation, which means the point at which a transaction begins may be controlled, without using the legacy “autocommit” mode.

The Session tracks the state of a single “virtual” transaction at a time, using an object called SessionTransaction. This object then makes use of the underlying Engine or engines to which the Session object is bound in order to start real connection-level transactions using the Connection object as needed.

This “virtual” transaction is created automatically when needed, or can alternatively be started using the Session.begin() method. To as great a degree as possible, Python context manager use is supported both at the level of creating Session objects as well as to maintain the scope of the SessionTransaction.

Below, assume we start with a Session:

We can now run operations within a demarcated transaction using a context manager:

At the end of the above context, assuming no exceptions were raised, any pending objects will be flushed to the database and the database transaction will be committed. If an exception was raised within the above block, then the transaction would be rolled back. In both cases, the above Session subsequent to exiting the block is ready to be used in subsequent transactions.

The Session.begin() method is optional, and the Session may also be used in a commit-as-you-go approach, where it will begin transactions automatically as needed; these only need be committed or rolled back:

The Session itself features a Session.close() method. If the Session is begun within a transaction that has not yet been committed or rolled back, this method will cancel (i.e. rollback) that transaction, and also expunge all objects contained within the Session object’s state. If the Session is being used in such a way that a call to Session.commit() or Session.rollback() is not guaranteed (e.g. not within a context manager or similar), the close method may be used to ensure all resources are released:

Finally, the session construction / close process can itself be run via context manager. This is the best way to ensure that the scope of a Session object’s use is scoped within a fixed block. Illustrated via the Session constructor first:

Similarly, the sessionmaker can be used in the same way:

sessionmaker itself includes a sessionmaker.begin() method to allow both operations to take place at once:

SAVEPOINT transactions, if supported by the underlying engine, may be delineated using the Session.begin_nested() method:

Each time Session.begin_nested() is called, a new “BEGIN SAVEPOINT” command is emitted to the database within the scope of the current database transaction (starting one if not already in progress), and an object of type SessionTransaction is returned, which represents a handle to this SAVEPOINT. When the .commit() method on this object is called, “RELEASE SAVEPOINT” is emitted to the database, and if instead the .rollback() method is called, “ROLLBACK TO SAVEPOINT” is emitted. The enclosing database transaction remains in progress.

Session.begin_nested() is typically used as a context manager where specific per-instance errors may be caught, in conjunction with a rollback emitted for that portion of the transaction’s state, without rolling back the whole transaction, as in the example below:

When the context manager yielded by Session.begin_nested() completes, it “commits” the savepoint, which includes the usual behavior of flushing all pending state. When an error is raised, the savepoint is rolled back and the state of the Session local to the objects that were changed is expired.

This pattern is ideal for situations such as using PostgreSQL and catching IntegrityError to detect duplicate rows; PostgreSQL normally aborts the entire transaction when such an error is raised, however when using SAVEPOINT, the outer transaction is maintained. In the example below a list of data is persisted into the database, with the occasional “duplicate primary key” record skipped, without rolling back the entire operation:

When Session.begin_nested() is called, the Session first flushes all currently pending state to the database; this occurs unconditionally, regardless of the value of the Session.autoflush parameter which normally may be used to disable automatic flush. The rationale for this behavior is so that when a rollback on this nested transaction occurs, the Session may expire any in-memory state that was created within the scope of the SAVEPOINT, while ensuring that when those expired objects are refreshed, the state of the object graph prior to the beginning of the SAVEPOINT will be available to re-load from the database.

In modern versions of SQLAlchemy, when a SAVEPOINT initiated by Session.begin_nested() is rolled back, in-memory object state that was modified since the SAVEPOINT was created is expired, however other object state that was not altered since the SAVEPOINT began is maintained. This is so that subsequent operations can continue to make use of the otherwise unaffected data without the need for refreshing it from the database.

Connection.begin_nested() - Core SAVEPOINT API

The Connection in Core and _session.Session in ORM feature equivalent transactional semantics, both at the level of the sessionmaker vs. the Engine, as well as the Session vs. the Connection. The following sections detail these scenarios based on the following scheme:

Both Session and Connection feature Connection.commit() and Connection.rollback() methods. Using SQLAlchemy 2.0-style operation, these methods affect the outermost transaction in all cases. For the Session, it is assumed that Session.autobegin is left at its default value of True.

Both sessionmaker and Engine feature a Engine.begin() method that will both procure a new object with which to execute SQL statements (the Session and Connection, respectively) and then return a context manager that will maintain a begin/commit/rollback context for that object.

When using a SAVEPOINT via the Session.begin_nested() or Connection.begin_nested() methods, the transaction object returned must be used to commit or rollback the SAVEPOINT. Calling the Session.commit() or Connection.commit() methods will always commit the outermost transaction; this is a SQLAlchemy 2.0 specific behavior that is reversed from the 1.x series.

The Session features “autobegin” behavior, meaning that as soon as operations begin to take place, it ensures a SessionTransaction is present to track ongoing operations. This transaction is completed when Session.commit() is called.

It is often desirable, particularly in framework integrations, to control the point at which the “begin” operation occurs. To suit this, the Session uses an “autobegin” strategy, such that the Session.begin() method may be called directly for a Session that has not already had a transaction begun:

The above pattern is more idiomatically invoked using a context manager:

The Session.begin() method and the session’s “autobegin” process use the same sequence of steps to begin the transaction. This includes that the SessionEvents.after_transaction_create() event is invoked when it occurs; this hook is used by frameworks in order to integrate their own transactional processes with that of the ORM Session.

For backends which support two-phase operation (currently MySQL and PostgreSQL), the session can be instructed to use two-phase commit semantics. This will coordinate the committing of transactions across databases so that the transaction is either committed or rolled back in all databases. You can also Session.prepare() the session for interacting with transactions not managed by SQLAlchemy. To use two phase transactions set the flag twophase=True on the session:

Most DBAPIs support the concept of configurable transaction isolation levels. These are traditionally the four levels “READ UNCOMMITTED”, “READ COMMITTED”, “REPEATABLE READ” and “SERIALIZABLE”. These are usually applied to a DBAPI connection before it begins a new transaction, noting that most DBAPIs will begin this transaction implicitly when SQL statements are first emitted.

DBAPIs that support isolation levels also usually support the concept of true “autocommit”, which means that the DBAPI connection itself will be placed into a non-transactional autocommit mode. This usually means that the typical DBAPI behavior of emitting “BEGIN” to the database automatically no longer occurs, but it may also include other directives. When using this mode, the DBAPI does not use a transaction under any circumstances. SQLAlchemy methods like .begin(), .commit() and .rollback() pass silently.

SQLAlchemy’s dialects support settable isolation modes on a per-Engine or per-Connection basis, using flags at both the create_engine() level as well as at the Connection.execution_options() level.

When using the ORM Session, it acts as a facade for engines and connections, but does not expose transaction isolation directly. So in order to affect transaction isolation level, we need to act upon the Engine or Connection as appropriate.

Setting Transaction Isolation Levels including DBAPI Autocommit - be sure to review how isolation levels work at the level of the SQLAlchemy Connection object as well.

To set up a Session or sessionmaker with a specific isolation level globally, the first technique is that an Engine can be constructed against a specific isolation level in all cases, which is then used as the source of connectivity for a Session and/or sessionmaker:

Another option, useful if there are to be two engines with different isolation levels at once, is to use the Engine.execution_options() method, which will produce a shallow copy of the original Engine which shares the same connection pool as the parent engine. This is often preferable when operations will be separated into “transactional” and “autocommit” operations:

Above, both “eng” and "autocommit_engine" share the same dialect and connection pool. However the “AUTOCOMMIT” mode will be set upon connections when they are acquired from the autocommit_engine. The two sessionmaker objects “transactional_session” and “autocommit_session" then inherit these characteristics when they work with database connections.

The “autocommit_session” continues to have transactional semantics, including that Session.commit() and Session.rollback() still consider themselves to be “committing” and “rolling back” objects, however the transaction will be silently absent. For this reason, it is typical, though not strictly required, that a Session with AUTOCOMMIT isolation be used in a read-only fashion, that is:

When we make a new Session, either using the constructor directly or when we call upon the callable produced by a sessionmaker, we can pass the bind argument directly, overriding the pre-existing bind. We can for example create our Session from a default sessionmaker and pass an engine set for autocommit:

For the case where the Session or sessionmaker is configured with multiple “binds”, we can either re-specify the binds argument fully, or if we want to only replace specific binds, we can use the Session.bind_mapper() or Session.bind_table() methods:

A key caveat regarding isolation level is that the setting cannot be safely modified on a Connection where a transaction has already started. Databases cannot change the isolation level of a transaction in progress, and some DBAPIs and SQLAlchemy dialects have inconsistent behaviors in this area.

Therefore it is preferable to use a Session that is up front bound to an engine with the desired isolation level. However, the isolation level on a per-connection basis can be affected by using the Session.connection() method at the start of a transaction:

Above, we first produce a Session using either the constructor or a sessionmaker. Then we explicitly set up the start of a database-level transaction by calling upon Session.connection(), which provides for execution options that will be passed to the connection before the database-level transaction is begun. The transaction proceeds with this selected isolation level. When the transaction completes, the isolation level is reset on the connection to its default before the connection is returned to the connection pool.

The Session.begin() method may also be used to begin the Session level transaction; calling upon Session.connection() subsequent to that call may be used to set up the per-connection-transaction isolation level:

See the section Transaction Events for an overview of the available event hooks for session transaction state changes.

If a Connection is being used which is already in a transactional state (i.e. has a Transaction established), a Session can be made to participate within that transaction by just binding the Session to that Connection. The usual rationale for this is a test suite that allows ORM code to work freely with a Session, including the ability to call Session.commit(), where afterwards the entire database interaction is rolled back.

Changed in version 2.0: The “join into an external transaction” recipe is newly improved again in 2.0; event handlers to “reset” the nested transaction are no longer required.

The recipe works by establishing a Connection within a transaction and optionally a SAVEPOINT, then passing it to a Session as the “bind”; the Session.join_transaction_mode parameter is passed with the setting "create_savepoint", which indicates that new SAVEPOINTs should be created in order to implement BEGIN/COMMIT/ROLLBACK for the Session, which will leave the external transaction in the same state in which it was passed.

When the test tears down, the external transaction is rolled back so that any data changes throughout the test are reverted:

The above recipe is part of SQLAlchemy’s own CI to ensure that it remains working as expected.

flambé! the dragon and The Alchemist image designs created and generously donated by Rotem Yaari.

**Examples:**

Example 1 (sql):
```sql
from sqlalchemy.orm import Session

session = Session(engine)
```

Example 2 (markdown):
```markdown
with session.begin():
    session.add(some_object())
    session.add(some_other_object())
# commits transaction at the end, or rolls back if there
# was an exception raised
```

Example 3 (sql):
```sql
session = Session(engine)

session.add(some_object())
session.add(some_other_object())

session.commit()  # commits

# will automatically begin again
result = session.execute(text("< some select statement >"))
session.add_all([more_objects, ...])
session.commit()  # commits

session.add(still_another_object)
session.flush()  # flush still_another_object
session.rollback()  # rolls back still_another_object
```

Example 4 (markdown):
```markdown
# expunges all objects, releases all transactions unconditionally
# (with rollback), releases all database connections back to their
# engines
session.close()
```

---
