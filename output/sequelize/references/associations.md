# Sequelize - Associations

**Pages:** 5

---

## Advanced M:N Associations

**URL:** https://sequelize.org/docs/v6/advanced-association-concepts/advanced-many-to-many/

**Contents:**
- Advanced M:N Associations
- Through tables versus normal tables and the "Super Many-to-Many association"​
  - Models recap (with minor rename)​
  - Using One-to-Many relationships instead​
  - The best of both worlds: the Super Many-to-Many relationship​
- Aliases and custom key names​
- Self-references​
- Specifying attributes from the through table​
- Many-to-many-to-many relationships and beyond​

Make sure you have read the associations guide before reading this guide.

Let's start with an example of a Many-to-Many relationship between User and Profile.

The simplest way to define the Many-to-Many relationship is:

By passing a string to through above, we are asking Sequelize to automatically generate a model named User_Profiles as the through table (also known as junction table), with only two columns: userId and profileId. A composite unique key will be established on these two columns.

We can also define ourselves a model to be used as the through table.

The above has the exact same effect. Note that we didn't define any attributes on the User_Profile model. The fact that we passed it into a belongsToMany call tells sequelize to create the two attributes userId and profileId automatically, just like other associations also cause Sequelize to automatically add a column to one of the involved models.

However, defining the model by ourselves has several advantages. We can, for example, define more columns on our through table:

With this, we can now track an extra information at the through table, namely the selfGranted boolean. For example, when calling the user.addProfile() we can pass values for the extra columns using the through option.

You can create all relationship in single create call too.

You probably noticed that the User_Profiles table does not have an id field. As mentioned above, it has a composite unique key instead. The name of this composite unique key is chosen automatically by Sequelize but can be customized with the uniqueKey option:

Another possibility, if desired, is to force the through table to have a primary key just like other standard tables. To do this, simply define the primary key in the model:

The above will still create two columns userId and profileId, of course, but instead of setting up a composite unique key on them, the model will use its id column as primary key. Everything else will still work just fine.

Now we will compare the usage of the last Many-to-Many setup shown above with the usual One-to-Many relationships, so that in the end we conclude with the concept of a "Super Many-to-Many relationship".

To make things easier to follow, let's rename our User_Profile model to grant. Note that everything works in the same way as before. Our models are:

We established a Many-to-Many relationship between User and Profile using the Grant model as the through table:

This automatically added the columns userId and profileId to the Grant model.

Note: As shown above, we have chosen to force the grant model to have a single primary key (called id, as usual). This is necessary for the Super Many-to-Many relationship that will be defined soon.

Instead of setting up the Many-to-Many relationship defined above, what if we did the following instead?

The result is essentially the same! This is because User.hasMany(Grant) and Profile.hasMany(Grant) will automatically add the userId and profileId columns to Grant, respectively.

This shows that one Many-to-Many relationship isn't very different from two One-to-Many relationships. The tables in the database look the same.

The only difference is when you try to perform an eager load with Sequelize.

We can simply combine both approaches shown above!

This way, we can do all kinds of eager loading:

We can even perform all kinds of deeply nested includes:

Similarly to the other relationships, aliases can be defined for Many-to-Many relationships.

Before proceeding, please recall the aliasing example for belongsTo on the associations guide. Note that, in that case, defining an association impacts both the way includes are done (i.e. passing the association name) and the name Sequelize chooses for the foreign key (in that example, leaderId was created on the Ship model).

Defining an alias for a belongsToMany association also impacts the way includes are performed:

However, defining an alias here has nothing to do with the foreign key names. The names of both foreign keys created in the through table are still constructed by Sequelize based on the name of the models being associated. This can readily be seen by inspecting the generated SQL for the through table in the example above:

We can see that the foreign keys are productId and categoryId. To change these names, Sequelize accepts the options foreignKey and otherKey respectively (i.e., the foreignKey defines the key for the source model in the through relation, and otherKey defines it for the target model):

As shown above, when you define a Many-to-Many relationship with two belongsToMany calls (which is the standard way), you should provide the foreignKey and otherKey options appropriately in both calls. If you pass these options in only one of the calls, the Sequelize behavior will be unreliable.

Sequelize supports self-referential Many-to-Many relationships, intuitively:

By default, when eager loading a many-to-many relationship, Sequelize will return data in the following structure (based on the first example in this guide):

Notice that the outer object is an User, which has a field called profiles, which is a Profile array, such that each Profile comes with an extra field called grant which is a Grant instance. This is the default structure created by Sequelize when eager loading from a Many-to-Many relationship.

However, if you want only some of the attributes of the through table, you can provide an array with the attributes you want in the attributes option. For example, if you only want the selfGranted attribute from the through table:

If you don't want the nested grant field at all, use attributes: []:

If you are using mixins (such as user.getProfiles()) instead of finder methods (such as User.findAll()), you have to use the joinTableAttributes option instead:

Consider you are trying to model a game championship. There are players and teams. Teams play games. However, players can change teams in the middle of the championship (but not in the middle of a game). So, given one specific game, there are certain teams participating in that game, and each of these teams has a set of players (for that game).

So we start by defining the three relevant models:

Now, the question is: how to associate them?

The above observations show that we need a Many-to-Many relationship between Game and Team. Let's use the Super Many-to-Many relationship as explained earlier in this guide:

The part about players is trickier. We note that the set of players that form a team depends not only on the team (obviously), but also on which game is being considered. Therefore, we don't want a Many-to-Many relationship between Player and Team. We also don't want a Many-to-Many relationship between Player and Game. Instead of associating a Player to any of those models, what we need is an association between a Player and something like a "team-game pair constraint", since it is the pair (team plus game) that defines which players belong there. So what we are looking for turns out to be precisely the junction model, GameTeam, itself! And, we note that, since a given game-team pair specifies many players, and on the other hand that the same player can participate of many game-team pairs, we need a Many-to-Many relationship between Player and GameTeam!

To provide the greatest flexibility, let's use the Super Many-to-Many relationship construction here again:

The above associations achieve precisely what we want. Here is a full runnable example of this:

So this is how we can achieve a many-to-many-to-many relationship between three models in Sequelize, by taking advantage of the Super Many-to-Many relationship technique!

This idea can be applied recursively for even more complex, many-to-many-to-...-to-many relationships (although at some point queries might become slow).

**Examples:**

Example 1 (css):
```css
const User = sequelize.define(  'user',  {    username: DataTypes.STRING,    points: DataTypes.INTEGER,  },  { timestamps: false },);const Profile = sequelize.define(  'profile',  {    name: DataTypes.STRING,  },  { timestamps: false },);
```

Example 2 (css):
```css
User.belongsToMany(Profile, { through: 'User_Profiles' });Profile.belongsToMany(User, { through: 'User_Profiles' });
```

Example 3 (css):
```css
const User_Profile = sequelize.define('User_Profile', {}, { timestamps: false });User.belongsToMany(Profile, { through: User_Profile });Profile.belongsToMany(User, { through: User_Profile });
```

Example 4 (css):
```css
const User_Profile = sequelize.define(  'User_Profile',  {    selfGranted: DataTypes.BOOLEAN,  },  { timestamps: false },);User.belongsToMany(Profile, { through: User_Profile });Profile.belongsToMany(User, { through: User_Profile });
```

---

## Creating with Associations

**URL:** https://sequelize.org/docs/v6/advanced-association-concepts/creating-with-associations/

**Contents:**
- Creating with Associations
- BelongsTo / HasMany / HasOne association​
- BelongsTo association with an alias​
- HasMany / BelongsToMany association​

An instance can be created with nested association in one step, provided all elements are new.

In contrast, performing updates and deletions involving nested objects is currently not possible. For that, you will have to perform each separate action explicitly.

Consider the following models:

A new Product, User, and one or more Address can be created in one step in the following way:

Observe the usage of the include option in the Product.create call. That is necessary for Sequelize to understand what you are trying to create along with the association.

Note: here, our user model is called user, with a lowercase u - This means that the property in the object should also be user. If the name given to sequelize.define was User, the key in the object should also be User. Likewise for addresses, except it's pluralized being a hasMany association.

The previous example can be extended to support an association alias.

Let's introduce the ability to associate a product with many tags. Setting up the models could look like:

Now we can create a product with multiple tags in the following way:

And, we can modify this example to support an alias as well:

**Examples:**

Example 1 (gdscript):
```gdscript
class Product extends Model {}Product.init(  {    title: Sequelize.STRING,  },  { sequelize, modelName: 'product' },);class User extends Model {}User.init(  {    firstName: Sequelize.STRING,    lastName: Sequelize.STRING,  },  { sequelize, modelName: 'user' },);class Address extends Model {}Address.init(  {    type: DataTypes.STRING,    line1: Sequelize.STRING,    line2: Sequelize.STRING,    city: Sequelize.STRING,    state: Sequelize.STRING,    zip: Sequelize.STRING,  },  { sequelize, modelName: 'address' },);// We save the return values of the association setup calls to use them laterProduct.User = Product.belongsTo(User);User.Addresses = User.hasMany(Address);// Also works for `hasOne`
```

Example 2 (css):
```css
return Product.create(  {    title: 'Chair',    user: {      firstName: 'Mick',      lastName: 'Broadstone',      addresses: [        {          type: 'home',          line1: '100 Main St.',          city: 'Austin',          state: 'TX',          zip: '78704',        },      ],    },  },  {    include: [      {        association: Product.User,        include: [User.Addresses],      },    ],  },);
```

Example 3 (css):
```css
const Creator = Product.belongsTo(User, { as: 'creator' });return Product.create(  {    title: 'Chair',    creator: {      firstName: 'Matt',      lastName: 'Hansen',    },  },  {    include: [Creator],  },);
```

Example 4 (gdscript):
```gdscript
class Tag extends Model {}Tag.init(  {    name: Sequelize.STRING,  },  { sequelize, modelName: 'tag' },);Product.hasMany(Tag);// Also works for `belongsToMany`.
```

---

## Polymorphic Associations

**URL:** https://sequelize.org/docs/v6/advanced-association-concepts/polymorphic-associations/

**Contents:**
- Polymorphic Associations
- Concept​
- Configuring a One-to-Many polymorphic association​
  - Polymorphic lazy loading​
  - Polymorphic eager loading​
  - Caution - possibly invalid eager/lazy loading!​
- Configuring a Many-to-Many polymorphic association​
  - Applying scopes on the target model​

Note: the usage of polymorphic associations in Sequelize, as outlined in this guide, should be done with caution. Don't just copy-paste code from here, otherwise you might easily make mistakes and introduce bugs in your code. Make sure you understand what is going on.

A polymorphic association consists on two (or more) associations happening with the same foreign key.

For example, consider the models Image, Video and Comment. The first two represent something that a user might post. We want to allow comments to be placed in both of them. This way, we immediately think of establishing the following associations:

A One-to-Many association between Image and Comment:

A One-to-Many association between Video and Comment:

However, the above would cause Sequelize to create two foreign keys on the Comment table: ImageId and VideoId. This is not ideal because this structure makes it look like a comment can be attached at the same time to one image and one video, which isn't true. Instead, what we really want here is precisely a polymorphic association, in which a Comment points to a single Commentable, an abstract polymorphic entity that represents one of Image or Video.

Before proceeding to how to configure such an association, let's see how using it looks like:

To setup the polymorphic association for the example above (which is an example of One-to-Many polymorphic association), we have the following steps:

Since the commentableId column references several tables (two in this case), we cannot add a REFERENCES constraint to it. This is why the constraints: false option was used.

Note that, in the code above:

These scopes are automatically applied when using the association functions (as explained in the Association Scopes guide). Some examples are below, with their generated SQL statements:

Here we can see that `comment`.`commentableType` = 'image' was automatically added to the WHERE clause of the generated SQL. This is exactly the behavior we want.

image.createComment({ title: 'Awesome!' }):

image.addComment(comment):

The getCommentable instance method on Comment provides an abstraction for lazy loading the associated commentable - working whether the comment belongs to an Image or a Video.

It works by simply converting the commentableType string into a call to the correct mixin (either getImage or getVideo).

Note that the getCommentable implementation above:

Now, we want to perform a polymorphic eager loading of the associated commentables for one (or more) comments. We want to achieve something similar to the following idea:

The solution is to tell Sequelize to include both Images and Videos, so that our afterFind hook defined above will do the work, automatically adding the commentable field to the instance object, providing the abstraction we want.

Consider a comment Foo whose commentableId is 2 and commentableType is image. Consider also that Image A and Video X both happen to have an id equal to 2. Conceptually, it is clear that Video X is not associated to Foo, because even though its id is 2, the commentableType of Foo is image, not video. However, this distinction is made by Sequelize only at the level of the abstractions performed by getCommentable and the hook we created above.

This means that if you call Comment.findAll({ include: Video }) in the situation above, Video X will be eager loaded into Foo. Thankfully, our afterFind hook will delete it automatically, to help prevent bugs, but regardless it is important that you understand what is going on.

The best way to prevent this kind of mistake is to avoid using the concrete accessors and mixins directly at all costs (such as .image, .getVideo(), .setImage(), etc), always preferring the abstractions we created, such as .getCommentable() and .commentable. If you really need to access eager-loaded .image and .video for some reason, make sure you wrap that in a type check such as comment.commentableType === 'image'.

In the above example, we had the models Image and Video being abstractly called commentables, with one commentable having many comments. However, one given comment would belong to a single commentable - this is why the whole situation is a One-to-Many polymorphic association.

Now, to consider a Many-to-Many polymorphic association, instead of considering comments, we will consider tags. For convenience, instead of calling Image and Video as commentables, we will now call them taggables. One taggable may have several tags, and at the same time one tag can be placed in several taggables.

The setup for this goes as follows:

The constraints: false option disables references constraints, as the taggableId column references several tables, we cannot add a REFERENCES constraint to it.

These scopes are automatically applied when using the association functions. Some examples are below, with their generated SQL statements:

Here we can see that `tag_taggable`.`taggableType` = 'image' was automatically added to the WHERE clause of the generated SQL. This is exactly the behavior we want.

Note that the above implementation of getTaggables() allows you to pass an options object to getCommentable(options), just like any other standard Sequelize method. This is useful to specify where-conditions or includes, for example.

In the example above, the scope options (such as scope: { taggableType: 'image' }) were applied to the through model, not the target model, since it was used under the through option.

We can also apply an association scope on the target model. We can even do both at the same time.

To illustrate this, consider an extension of the above example between tags and taggables, where each tag has a status. This way, to get all pending tags of an image, we could establish another belongsToMany relationship between Image and Tag, this time applying a scope on the through model and another scope on the target model:

This way, when calling image.getPendingTags(), the following SQL query will be generated:

We can see that both scopes were applied automatically:

**Examples:**

Example 1 (unknown):
```unknown
Image.hasMany(Comment);Comment.belongsTo(Image);
```

Example 2 (unknown):
```unknown
Video.hasMany(Comment);Comment.belongsTo(Video);
```

Example 3 (javascript):
```javascript
const image = await Image.create({ url: 'https://placekitten.com/408/287' });const comment = await image.createComment({ content: 'Awesome!' });console.log(comment.commentableId === image.id); // true// We can also retrieve which type of commentable a comment is associated to.// The following prints the model name of the associated commentable instance.console.log(comment.commentableType); // "Image"// We can use a polymorphic method to retrieve the associated commentable, without// having to worry whether it's an Image or a Video.const associatedCommentable = await comment.getCommentable();// In this example, `associatedCommentable` is the same thing as `image`:const isDeepEqual = require('deep-equal');console.log(isDeepEqual(image, commentable)); // true
```

Example 4 (javascript):
```javascript
// Helper functionconst uppercaseFirst = str => `${str[0].toUpperCase()}${str.substr(1)}`;class Image extends Model {}Image.init(  {    title: DataTypes.STRING,    url: DataTypes.STRING,  },  { sequelize, modelName: 'image' },);class Video extends Model {}Video.init(  {    title: DataTypes.STRING,    text: DataTypes.STRING,  },  { sequelize, modelName: 'video' },);class Comment extends Model {  getCommentable(options) {    if (!this.commentableType) return Promise.resolve(null);    const mixinMethodName = `get${uppercaseFirst(this.commentableType)}`;    return this[mixinMethodName](options);  }}Comment.init(  {    title: DataTypes.STRING,    commentableId: DataTypes.INTEGER,    commentableType: DataTypes.STRING,  },  { sequelize, modelName: 'comment' },);Image.hasMany(Comment, {  foreignKey: 'commentableId',  constraints: false,  scope: {    commentableType: 'image',  },});Comment.belongsTo(Image, { foreignKey: 'commentableId', constraints: false });Video.hasMany(Comment, {  foreignKey: 'commentableId',  constraints: false,  scope: {    commentableType: 'video',  },});Comment.belongsTo(Video, { foreignKey: 'commentableId', constraints: false });Comment.addHook('afterFind', findResult => {  if (!Array.isArray(findResult)) findResult = [findResult];  for (const instance of findResult) {    if (instance.commentableType === 'image' && instance.image !== undefined) {      instance.commentable = instance.image;    } else if (instance.commentableType === 'video' && instance.video !== undefined) {      instance.commentable = instance.video;    }    // To prevent mistakes:    delete instance.image;    delete instance.dataValues.image;    delete instance.video;    delete instance.dataValues.video;  }});
```

---

## Associations

**URL:** https://sequelize.org/docs/v6/core-concepts/assocs/

**Contents:**
- Associations
- Defining the Sequelize associations​
- Creating the standard relationships​
- One-To-One relationships​
  - Philosophy​
  - Goal​
  - Implementation​
  - Options​
    - onDelete and onUpdate​
    - Customizing the foreign key​

Sequelize supports the standard associations: One-To-One, One-To-Many and Many-To-Many.

To do this, Sequelize provides four types of associations that should be combined to create them:

The guide will start explaining how to define these four types of associations, and then will follow up to explain how to combine those to define the three standard association types (One-To-One, One-To-Many and Many-To-Many).

The four association types are defined in a very similar way. Let's say we have two models, A and B. Telling Sequelize that you want an association between the two needs just a function call:

They all accept an options object as a second parameter (optional for the first three, mandatory for belongsToMany containing at least the through property):

The order in which the association is defined is relevant. In other words, the order matters, for the four cases. In all examples above, A is called the source model and B is called the target model. This terminology is important.

The A.hasOne(B) association means that a One-To-One relationship exists between A and B, with the foreign key being defined in the target model (B).

The A.belongsTo(B) association means that a One-To-One relationship exists between A and B, with the foreign key being defined in the source model (A).

The A.hasMany(B) association means that a One-To-Many relationship exists between A and B, with the foreign key being defined in the target model (B).

These three calls will cause Sequelize to automatically add foreign keys to the appropriate models (unless they are already present).

The A.belongsToMany(B, { through: 'C' }) association means that a Many-To-Many relationship exists between A and B, using table C as junction table, which will have the foreign keys (aId and bId, for example). Sequelize will automatically create this model C (unless it already exists) and define the appropriate foreign keys on it.

Note: In the examples above for belongsToMany, a string ('C') was passed to the through option. In this case, Sequelize automatically generates a model with this name. However, you can also pass a model directly, if you have already defined it.

These are the main ideas involved in each type of association. However, these relationships are often used in pairs, in order to enable better usage with Sequelize. This will be seen later on.

As mentioned, usually the Sequelize associations are defined in pairs. In summary:

This will all be seen in detail next. The advantages of using these pairs instead of one single association will be discussed in the end of this chapter.

Before digging into the aspects of using Sequelize, it is useful to take a step back to consider what happens with a One-To-One relationship.

Let's say we have two models, Foo and Bar. We want to establish a One-To-One relationship between Foo and Bar. We know that in a relational database, this will be done by establishing a foreign key in one of the tables. So in this case, a very relevant question is: in which table do we want this foreign key to be? In other words, do we want Foo to have a barId column, or should Bar have a fooId column instead?

In principle, both options are a valid way to establish a One-To-One relationship between Foo and Bar. However, when we say something like "there is a One-To-One relationship between Foo and Bar", it is unclear whether or not the relationship is mandatory or optional. In other words, can a Foo exist without a Bar? Can a Bar exist without a Foo? The answers to these questions help figuring out where we want the foreign key column to be.

For the rest of this example, let's assume that we have two models, Foo and Bar. We want to setup a One-To-One relationship between them such that Bar gets a fooId column.

The main setup to achieve the goal is as follows:

Since no option was passed, Sequelize will infer what to do from the names of the models. In this case, Sequelize knows that a fooId column must be added to Bar.

This way, calling Bar.sync() after the above will yield the following SQL (on PostgreSQL, for example):

Various options can be passed as a second parameter of the association call.

For example, to configure the ON DELETE and ON UPDATE behaviors, you can do:

The possible choices are RESTRICT, CASCADE, NO ACTION, SET DEFAULT and SET NULL.

The defaults for the One-To-One associations is SET NULL for ON DELETE and CASCADE for ON UPDATE.

Both the hasOne and belongsTo calls shown above will infer that the foreign key to be created should be called fooId. To use a different name, such as myFooId:

As shown above, the foreignKey option accepts a string or an object. When receiving an object, this object will be used as the definition for the column just like it would do in a standard sequelize.define call. Therefore, specifying options such as type, allowNull, defaultValue, etc, just work.

For example, to use UUID as the foreign key data type instead of the default (INTEGER), you can simply do:

By default, the association is considered optional. In other words, in our example, the fooId is allowed to be null, meaning that one Bar can exist without a Foo. Changing this is just a matter of specifying allowNull: false in the foreign key options:

One-To-Many associations are connecting one source with multiple targets, while all these targets are connected only with this single source.

This means that, unlike the One-To-One association, in which we had to choose where the foreign key would be placed, there is only one option in One-To-Many associations. For example, if one Foo has many Bars (and this way each Bar belongs to one Foo), then the only sensible implementation is to have a fooId column in the Bar table. The opposite is impossible, since one Foo has many Bars.

In this example, we have the models Team and Player. We want to tell Sequelize that there is a One-To-Many relationship between them, meaning that one Team has many Players, while each Player belongs to a single Team.

The main way to do this is as follows:

Again, as mentioned, the main way to do it used a pair of Sequelize associations (hasMany and belongsTo).

For example, in PostgreSQL, the above setup will yield the following SQL upon sync():

The options to be applied in this case are the same from the One-To-One case. For example, to change the name of the foreign key and make sure that the relationship is mandatory, we can do:

Like One-To-One relationships, ON DELETE defaults to SET NULL and ON UPDATE defaults to CASCADE.

Many-To-Many associations connect one source with multiple targets, while all these targets can in turn be connected to other sources beyond the first.

This cannot be represented by adding one foreign key to one of the tables, like the other relationships did. Instead, the concept of a Junction Model is used. This will be an extra model (and extra table in the database) which will have two foreign key columns and will keep track of the associations. The junction table is also sometimes called join table or through table.

For this example, we will consider the models Movie and Actor. One actor may have participated in many movies, and one movie had many actors involved with its production. The junction table that will keep track of the associations will be called ActorMovies, which will contain the foreign keys movieId and actorId.

The main way to do this in Sequelize is as follows:

Since a string was given in the through option of the belongsToMany call, Sequelize will automatically create the ActorMovies model which will act as the junction model. For example, in PostgreSQL:

Instead of a string, passing a model directly is also supported, and in that case the given model will be used as the junction model (and no model will be created automatically). For example:

The above yields the following SQL in PostgreSQL, which is equivalent to the one shown above:

Unlike One-To-One and One-To-Many relationships, the defaults for both ON UPDATE and ON DELETE are CASCADE for Many-To-Many relationships.

Belongs-To-Many creates a unique key on through model. This unique key name can be overridden using uniqueKey option. To prevent creating this unique key, use the unique: false option.

With the basics of defining associations covered, we can look at queries involving associations. The most common queries on this matter are the read queries (i.e. SELECTs). Later on, other types of queries will be shown.

In order to study this, we will consider an example in which we have Ships and Captains, and a one-to-one relationship between them. We will allow null on foreign keys (the default), meaning that a Ship can exist without a Captain and vice-versa.

The concepts of Eager Loading and Lazy Loading are fundamental to understand how fetching associations work in Sequelize. Lazy Loading refers to the technique of fetching the associated data only when you really want it; Eager Loading, on the other hand, refers to the technique of fetching everything at once, since the beginning, with a larger query.

Observe that in the example above, we made two queries, only fetching the associated ship when we wanted to use it. This can be especially useful if we may or may not need the ship, perhaps we want to fetch it conditionally, only in a few cases; this way we can save time and memory by only fetching it when necessary.

Note: the getShip() instance method used above is one of the methods Sequelize automatically adds to Captain instances. There are others. You will learn more about them later in this guide.

As shown above, Eager Loading is performed in Sequelize by using the include option. Observe that here only one query was performed to the database (which brings the associated data along with the instance).

This was just a quick introduction to Eager Loading in Sequelize. There is a lot more to it, which you can learn at the dedicated guide on Eager Loading.

The above showed the basics on queries for fetching data involving associations. For creating, updating and deleting, you can either:

Use the standard model queries directly:

Or use the special methods/mixins available for associated models, which are explained later on this page.

Note: The save() instance method is not aware of associations. In other words, if you change a value from a child object that was eager loaded along a parent object, calling save() on the parent will completely ignore the change that happened on the child.

In all the above examples, Sequelize automatically defined the foreign key names. For example, in the Ship and Captain example, Sequelize automatically defined a captainId field on the Ship model. However, it is easy to specify a custom foreign key.

Let's consider the models Ship and Captain in a simplified form, just to focus on the current topic, as shown below (less fields):

There are three ways to specify a different name for the foreign key:

By using simply Ship.belongsTo(Captain), sequelize will generate the foreign key name automatically:

The foreign key name can be provided directly with an option in the association definition, as follows:

Defining an Alias is more powerful than simply specifying a custom name for the foreign key. This is better understood with an example:

Aliases are especially useful when you need to define two different associations between the same models. For example, if we have the models Mail and Person, we may want to associate them twice, to represent the sender and receiver of the Mail. In this case we must use an alias for each association, since otherwise a call like mail.getPerson() would be ambiguous. With the sender and receiver aliases, we would have the two methods available and working: mail.getSender() and mail.getReceiver(), both of them returning a Promise<Person>.

When defining an alias for a hasOne or belongsTo association, you should use the singular form of a word (such as leader, in the example above). On the other hand, when defining an alias for hasMany and belongsToMany, you should use the plural form. Defining aliases for Many-to-Many relationships (with belongsToMany) is covered in the Advanced Many-to-Many Associations guide.

We can define and alias and also directly define the foreign key:

When an association is defined between two models, the instances of those models gain special methods to interact with their associated counterparts.

For example, if we have two models, Foo and Bar, and they are associated, their instances will have the following methods/mixins available, depending on the association type:

The same ones from Foo.hasOne(Bar):

The getter method accepts options just like the usual finder methods (such as findAll):

The same ones from Foo.hasMany(Bar):

For belongsToMany relationships, by default getBars() will return all fields from the join table. Note that any include options will apply to the target Bar object, so trying to set options for the join table as you would when eager loading with find methods is not possible. To choose what attributes of the join table to include, getBars() supports a joinTableAttributes option that can be used similarly to setting through.attributes in an include. As an example, given Foo belongsToMany Bar, the following will both output results without join table fields:

As shown in the examples above, the names Sequelize gives to these special methods are formed by a prefix (e.g. get, add, set) concatenated with the model name (with the first letter in uppercase). When necessary, the plural is used, such as in fooInstance.setBars(). Again, irregular plurals are also handled automatically by Sequelize. For example, Person becomes People and Hypothesis becomes Hypotheses.

If an alias was defined, it will be used instead of the model name to form the method names. For example:

As mentioned earlier and shown in most examples above, usually associations in Sequelize are defined in pairs:

When a Sequelize association is defined between two models, only the source model knows about it. So, for example, when using Foo.hasOne(Bar) (so Foo is the source model and Bar is the target model), only Foo knows about the existence of this association. This is why in this case, as shown above, Foo instances gain the methods getBar(), setBar() and createBar(), while on the other hand Bar instances get nothing.

Similarly, for Foo.hasOne(Bar), since Foo knows about the relationship, we can perform eager loading as in Foo.findOne({ include: Bar }), but we can't do Bar.findOne({ include: Foo }).

Therefore, to bring full power to Sequelize usage, we usually setup the relationship in pairs, so that both models get to know about it.

Practical demonstration:

If we do not define the pair of associations, calling for example just Foo.hasOne(Bar):

If we define the pair as recommended, i.e., both Foo.hasOne(Bar) and Bar.belongsTo(Foo):

In Sequelize, it is possible to define multiple associations between the same models. You just have to define different aliases for them:

In all the examples above, the associations were defined by referencing the primary keys of the involved models (in our case, their IDs). However, Sequelize allows you to define an association that uses another field, instead of the primary key field, to establish the association.

This other field must have a unique constraint on it (otherwise, it wouldn't make sense).

First, recall that the A.belongsTo(B) association places the foreign key in the source model (i.e., in A).

Let's again use the example of Ships and Captains. Additionally, we will assume that Captain names are unique:

This way, instead of keeping the captainId on our Ships, we could keep a captainName instead and use it as our association tracker. In other words, instead of referencing the id from the target model (Captain), our relationship will reference another column on the target model: the name column. To specify this, we have to define a target key. We will also have to specify a name for the foreign key itself:

Now we can do things like:

The exact same idea can be applied to the hasOne and hasMany associations, but instead of providing a targetKey, we provide a sourceKey when defining the association. This is because unlike belongsTo, the hasOne and hasMany associations keep the foreign key on the target model:

The same idea can also be applied to belongsToMany relationships. However, unlike the other situations, in which we have only one foreign key involved, the belongsToMany relationship involves two foreign keys which are kept on an extra table (the junction table).

Consider the following setup:

There are four cases to consider:

Don't forget that the field referenced in the association must have a unique constraint placed on it. Otherwise, an error will be thrown (and sometimes with a mysterious error message - such as SequelizeDatabaseError: SQLITE_ERROR: foreign key mismatch - "ships" referencing "captains" for SQLite).

The trick to deciding between sourceKey and targetKey is just to remember where each relationship places its foreign key. As mentioned in the beginning of this guide:

A.belongsTo(B) keeps the foreign key in the source model (A), therefore the referenced key is in the target model, hence the usage of targetKey.

A.hasOne(B) and A.hasMany(B) keep the foreign key in the target model (B), therefore the referenced key is in the source model, hence the usage of sourceKey.

A.belongsToMany(B) involves an extra table (the junction table), therefore both sourceKey and targetKey are usable, with sourceKey corresponding to some field in A (the source) and targetKey corresponding to some field in B (the target).

**Examples:**

Example 1 (css):
```css
const A = sequelize.define('A' /* ... */);const B = sequelize.define('B' /* ... */);A.hasOne(B); // A HasOne BA.belongsTo(B); // A BelongsTo BA.hasMany(B); // A HasMany BA.belongsToMany(B, { through: 'C' }); // A BelongsToMany B through the junction table C
```

Example 2 (css):
```css
A.hasOne(B, {  /* options */});A.belongsTo(B, {  /* options */});A.hasMany(B, {  /* options */});A.belongsToMany(B, { through: 'C' /* options */ });
```

Example 3 (unknown):
```unknown
Foo.hasOne(Bar);Bar.belongsTo(Foo);
```

Example 4 (sql):
```sql
CREATE TABLE IF NOT EXISTS "foos" (  /* ... */);CREATE TABLE IF NOT EXISTS "bars" (  /* ... */  "fooId" INTEGER REFERENCES "foos" ("id") ON DELETE SET NULL ON UPDATE CASCADE  /* ... */);
```

---

## Eager Loading

**URL:** https://sequelize.org/docs/v6/advanced-association-concepts/eager-loading/

**Contents:**
- Eager Loading
- Basic example​
  - Fetching a single associated element​
  - Fetching all associated elements​
  - Fetching an Aliased association​
  - Required eager loading​
  - Eager loading filtered at the associated model level​
    - Referring to other columns​
  - Complex where clauses at the top-level​
  - Fetching with RIGHT OUTER JOIN (MySQL, MariaDB, PostgreSQL and MSSQL only)​

As briefly mentioned in the associations guide, eager Loading is the act of querying data of several models at once (one 'main' model and one or more associated models). At the SQL level, this is a query with one or more joins.

When this is done, the associated models will be added by Sequelize in appropriately named, automatically created field(s) in the returned objects.

In Sequelize, eager loading is mainly done by using the include option on a model finder query (such as findOne, findAll, etc).

Let's assume the following setup:

OK. So, first of all, let's load all tasks with their associated user:

Here, tasks[0].user instanceof User is true. This shows that when Sequelize fetches associated models, they are added to the output object as model instances.

Above, the associated model was added to a new field called user in the fetched task. The name of this field was automatically chosen by Sequelize based on the name of the associated model, where its pluralized form is used when applicable (i.e., when the association is hasMany or belongsToMany). In other words, since Task.belongsTo(User), a task is associated to one user, therefore the logical choice is the singular form (which Sequelize follows automatically).

Now, instead of loading the user that is associated to a given task, we will do the opposite - we will find all tasks associated to a given user.

The method call is essentially the same. The only difference is that now the extra field created in the query result uses the pluralized form (tasks in this case), and its value is an array of task instances (instead of a single instance, as above).

Notice that the accessor (the tasks property in the resulting instance) is pluralized since the association is one-to-many.

If an association is aliased (using the as option), you must specify this alias when including the model. Instead of passing the model directly to the include option, you should instead provide an object with two options: model and as.

Notice how the user's Tools are aliased as Instruments above. In order to get that right you have to specify the model you want to load, as well as the alias:

You can also include by alias name by specifying a string that matches the association alias:

When eager loading, we can force the query to return only records which have an associated model, effectively converting the query from the default OUTER JOIN to an INNER JOIN. This is done with the required: true option, as follows:

This option also works on nested includes.

When eager loading, we can also filter the associated model using the where option, as in the following example:

Note that the SQL query generated above will only fetch users that have at least one tool that matches the condition (of not being small, in this case). This is the case because, when the where option is used inside an include, Sequelize automatically sets the required option to true. This means that, instead of an OUTER JOIN, an INNER JOIN is done, returning only the parent models with at least one matching children.

Note also that the where option used was converted into a condition for the ON clause of the INNER JOIN. In order to obtain a top-level WHERE clause, instead of an ON clause, something different must be done. This will be shown next.

If you want to apply a WHERE clause in an included model referring to a value from an associated model, you can simply use the Sequelize.col function, as show in the example below:

To obtain top-level WHERE clauses that involve nested columns, Sequelize provides a way to reference nested columns: the '$nested.column$' syntax.

It can be used, for example, to move the where conditions from an included model from the ON condition to a top-level WHERE clause.

The $nested.column$ syntax also works for columns that are nested several levels deep, such as $some.super.deeply.nested.column$. Therefore, you can use this to make complex filters on deeply nested columns.

For a better understanding of all differences between the inner where option (used inside an include), with and without the required option, and a top-level where using the $nested.column$ syntax, below we have four examples for you:

Generated SQLs, in order:

By default, associations are loaded using a LEFT OUTER JOIN - that is to say it only includes records from the parent table. You can change this behavior to a RIGHT OUTER JOIN by passing the right option, if the dialect you are using supports it.

Currently, SQLite does not support right joins.

Note: right is only respected if required is false.

The include option can receive an array in order to fetch multiple associated models at once:

When you perform eager loading on a model with a Belongs-to-Many relationship, Sequelize will fetch the junction table data as well, by default. For example:

Note that every bar instance eager loaded into the "Bars" property has an extra property called Foo_Bar which is the relevant Sequelize instance of the junction model. By default, Sequelize fetches all attributes from the junction table in order to build this extra property.

However, you can specify which attributes you want fetched. This is done with the attributes option applied inside the through option of the include. For example:

If you don't want anything from the junction table, you can explicitly provide an empty array to the attributes option inside the through option of the include option, and in this case nothing will be fetched and the extra property will not even be created:

Whenever including a model from a Many-to-Many relationship, you can also apply a filter on the junction table. This is done with the where option applied inside the through option of the include. For example:

Generated SQL (using SQLite):

To include all associated models, you can use the all and nested options:

In case you want to eager load soft deleted records you can do that by setting include.paranoid to false:

When you want to apply ORDER clauses to eager loaded models, you must use the top-level order option with augmented arrays, starting with the specification of the nested model you want to sort.

This is better understood with examples.

In the case of many-to-many relationships, you are also able to sort by attributes in the through table. For example, assuming we have a Many-to-Many relationship between Division and Department whose junction model is DepartmentDivision, you can do:

In all the above examples, you have noticed that the order option is used at the top-level. The only situation in which order also works inside the include option is when separate: true is used. In that case, the usage is as follows:

Take a look at the guide on sub-queries for an example of how to use a sub-query to assist a more complex ordering.

You can use nested eager loading to load all related models of a related model:

This will produce an outer join. However, a where clause on a related model will create an inner join and return only the instances that have matching sub-models. To return all parent instances, you should add required: false.

The query above will return all users, and all their instruments, but only those teachers associated with Woodstock Music School.

The findAndCountAll utility function supports includes. Only the includes that are marked as required will be considered in count. For example, if you want to find and count all users who have a profile:

Because the include for Profile has required set it will result in an inner join, and only the users who have a profile will be counted. If we remove required from the include, both users with and without profiles will be counted. Adding a where clause to the include automatically makes it required:

The query above will only count users who have an active profile, because required is implicitly set to true when you add a where clause to the include.

**Examples:**

Example 1 (css):
```css
const User = sequelize.define('user', { name: DataTypes.STRING }, { timestamps: false });const Task = sequelize.define('task', { name: DataTypes.STRING }, { timestamps: false });const Tool = sequelize.define(  'tool',  {    name: DataTypes.STRING,    size: DataTypes.STRING,  },  { timestamps: false },);User.hasMany(Task);Task.belongsTo(User);User.hasMany(Tool, { as: 'Instruments' });
```

Example 2 (javascript):
```javascript
const tasks = await Task.findAll({ include: User });console.log(JSON.stringify(tasks, null, 2));
```

Example 3 (json):
```json
[  {    "name": "A Task",    "id": 1,    "userId": 1,    "user": {      "name": "John Doe",      "id": 1    }  }]
```

Example 4 (javascript):
```javascript
const users = await User.findAll({ include: Task });console.log(JSON.stringify(users, null, 2));
```

---
