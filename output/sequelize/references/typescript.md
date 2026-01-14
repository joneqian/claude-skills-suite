# Sequelize - Typescript

**Pages:** 1

---

## TypeScript

**URL:** https://sequelize.org/docs/v6/other-topics/typescript/

**Contents:**
- TypeScript
- Installation​
- Usage​
  - The case of Model.init​
  - Usage without strict types for attributes​
- Usage of Sequelize#define​
- Utility Types​
  - Requesting a Model Class​
  - Getting a Model's attributes​

We're working hard on making Sequelize a breeze to use in TypeScript. Some parts are still a work in progress. We recommend using sequelize-typescript to bridge the gap until our improvements are ready to be released.

Sequelize provides its own TypeScript definitions.

Please note that only TypeScript >= 4.1 is supported. Our TypeScript support does not follow SemVer. We will support TypeScript releases for at least one year, after which they may be dropped in a SemVer MINOR release.

As Sequelize heavily relies on runtime property assignments, TypeScript won't be very useful out of the box. A decent amount of manual type declarations are needed to make models workable.

In order to avoid clashes with different Node versions, the typings for Node are not included. You must install @types/node manually.

Important: You must use declare on your class properties typings to ensure TypeScript does not emit those class properties. See Caveat with Public Class Fields

Sequelize Models accept two generic types to define what the model's Attributes & Creation Attributes are like:

This solution is verbose. Sequelize >=6.14.0 provides new utility types that will drastically reduce the amount of boilerplate necessary: InferAttributes, and InferCreationAttributes. They will extract Attribute typings directly from the Model:

Important things to know about InferAttributes & InferCreationAttributes work: They will select all declared properties of the class except:

InferCreationAttributes works the same way as InferAttributes with one exception:Properties typed using the CreationOptional type will be marked as optional. Note that attributes that accept null, or undefined do not need to use CreationOptional:

You only need to use CreationOptional & NonAttribute on class instance fields or getters.

Example of a minimal TypeScript project with strict type-checking for attributes:

Model.init requires an attribute configuration for each attribute declared in typings.

Some attributes don't actually need to be passed to Model.init, this is how you can make this static method aware of them:

Methods used to define associations (Model.belongsTo, Model.hasMany, etc…) already handle the configuration of the necessary foreign keys attributes. It is not necessary to configure these foreign keys using Model.init. Use the ForeignKey<> branded type to make Model.init aware of the fact that it isn't necessary to configure the foreign key:

Timestamp attributes managed by Sequelize (by default, createdAt, updatedAt, and deletedAt) don't need to be configured using Model.init, unfortunately Model.init has no way of knowing this. We recommend you use the minimum necessary configuration to silence this error:

The typings for Sequelize v5 allowed you to define models without specifying types for the attributes. This is still possible for backwards compatibility and for cases where you feel strict typing for attributes isn't worth it.

In Sequelize versions before v5, the default way of defining a model involved using Sequelize#define. It's still possible to define models with that, and you can also add typings to these models using interfaces.

ModelStatic is designed to be used to type a Model class.

Here is an example of a utility method that requests a Model Class, and returns the list of primary keys defined in that class:

If you need to access the list of attributes of a given model, Attributes<Model> and CreationAttributes<Model> are what you need to use.

They will return the Attributes (and Creation Attributes) of the Model passed as a parameter.

Don't confuse them with InferAttributes and InferCreationAttributes. These two utility types should only ever be used in the definition of a Model to automatically create the list of attributes from the model's public class fields. They only work with class-based model definitions (When using Model.init).

Attributes<Model> and CreationAttributes<Model> will return the list of attributes of any model, no matter how they were created (be it Model.init or Sequelize#define).

Here is an example of a utility function that requests a Model Class, and the name of an attribute ; and returns the corresponding attribute metadata.

**Examples:**

Example 1 (typescript):
```typescript
import { Model, Optional } from 'sequelize';// We don't recommend doing this. Read on for the new way of declaring Model typings.type UserAttributes = {  id: number;  name: string;  // other attributes...};// we're telling the Model that 'id' is optional// when creating an instance of the model (such as using Model.create()).type UserCreationAttributes = Optional<UserAttributes, 'id'>;class User extends Model<UserAttributes, UserCreationAttributes> {  declare id: number;  declare name: string;  // other attributes...}
```

Example 2 (typescript):
```typescript
import { Model, InferAttributes, InferCreationAttributes, CreationOptional } from 'sequelize';// order of InferAttributes & InferCreationAttributes is important.class User extends Model<InferAttributes<User>, InferCreationAttributes<User>> {  // 'CreationOptional' is a special type that marks the field as optional  // when creating an instance of the model (such as using Model.create()).  declare id: CreationOptional<number>;  declare name: string;  // other attributes...}
```

Example 3 (typescript):
```typescript
class User extends Model<InferAttributes<User>, InferCreationAttributes<User>> {  declare firstName: string;  // there is no need to use CreationOptional on lastName because nullable attributes  // are always optional in User.create()  declare lastName: string | null;}// ...await User.create({  firstName: 'Zoé',  // last name omitted, but this is still valid!});
```

Example 4 (typescript):
```typescript
/** * Keep this file in sync with the code in the "Usage" section * in /docs/manual/other-topics/typescript.md * * Don't include this comment in the md file. */import {  Association, DataTypes, HasManyAddAssociationMixin, HasManyCountAssociationsMixin,  HasManyCreateAssociationMixin, HasManyGetAssociationsMixin, HasManyHasAssociationMixin,  HasManySetAssociationsMixin, HasManyAddAssociationsMixin, HasManyHasAssociationsMixin,  HasManyRemoveAssociationMixin, HasManyRemoveAssociationsMixin, Model, ModelDefined, Optional,  Sequelize, InferAttributes, InferCreationAttributes, CreationOptional, NonAttribute, ForeignKey,} from 'sequelize';const sequelize = new Sequelize('mysql://root:asd123@localhost:3306/mydb');// 'projects' is excluded as it's not an attribute, it's an association.class User extends Model<InferAttributes<User, { omit: 'projects' }>, InferCreationAttributes<User, { omit: 'projects' }>> {  // id can be undefined during creation when using `autoIncrement`  declare id: CreationOptional<number>;  declare name: string;  declare preferredName: string | null; // for nullable fields  // timestamps!  // createdAt can be undefined during creation  declare createdAt: CreationOptional<Date>;  // updatedAt can be undefined during creation  declare updatedAt: CreationOptional<Date>;  // Since TS cannot determine model association at compile time  // we have to declare them here purely virtually  // these will not exist until `Model.init` was called.  declare getProjects: HasManyGetAssociationsMixin<Project>; // Note the null assertions!  declare addProject: HasManyAddAssociationMixin<Project, number>;  declare addProjects: HasManyAddAssociationsMixin<Project, number>;  declare setProjects: HasManySetAssociationsMixin<Project, number>;  declare removeProject: HasManyRemoveAssociationMixin<Project, number>;  declare removeProjects: HasManyRemoveAssociationsMixin<Project, number>;  declare hasProject: HasManyHasAssociationMixin<Project, number>;  declare hasProjects: HasManyHasAssociationsMixin<Project, number>;  declare countProjects: HasManyCountAssociationsMixin;  declare createProject: HasManyCreateAssociationMixin<Project, 'ownerId'>;  // You can also pre-declare possible inclusions, these will only be populated if you  // actively include a relation.  declare projects?: NonAttribute<Project[]>; // Note this is optional since it's only populated when explicitly requested in code  // getters that are not attributes should be tagged using NonAttribute  // to remove them from the model's Attribute Typings.  get fullName(): NonAttribute<string> {    return this.name;  }  declare static associations: {    projects: Association<User, Project>;  };}class Project extends Model<  InferAttributes<Project>,  InferCreationAttributes<Project>> {  // id can be undefined during creation when using `autoIncrement`  declare id: CreationOptional<number>;  // foreign keys are automatically added by associations methods (like Project.belongsTo)  // by branding them using the `ForeignKey` type, `Project.init` will know it does not need to  // display an error if ownerId is missing.  declare ownerId: ForeignKey<User['id']>;  declare name: string;  // `owner` is an eagerly-loaded association.  // We tag it as `NonAttribute`  declare owner?: NonAttribute<User>;  // createdAt can be undefined during creation  declare createdAt: CreationOptional<Date>;  // updatedAt can be undefined during creation  declare updatedAt: CreationOptional<Date>;}class Address extends Model<  InferAttributes<Address>,  InferCreationAttributes<Address>> {  declare userId: ForeignKey<User['id']>;  declare address: string;  // createdAt can be undefined during creation  declare createdAt: CreationOptional<Date>;  // updatedAt can be undefined during creation  declare updatedAt: CreationOptional<Date>;}Project.init(  {    id: {      type: DataTypes.INTEGER.UNSIGNED,      autoIncrement: true,      primaryKey: true    },    name: {      type: new DataTypes.STRING(128),      allowNull: false    },    createdAt: DataTypes.DATE,    updatedAt: DataTypes.DATE,  },  {    sequelize,    tableName: 'projects'  });User.init(  {    id: {      type: DataTypes.INTEGER.UNSIGNED,      autoIncrement: true,      primaryKey: true    },    name: {      type: new DataTypes.STRING(128),      allowNull: false    },    preferredName: {      type: new DataTypes.STRING(128),      allowNull: true    },    createdAt: DataTypes.DATE,    updatedAt: DataTypes.DATE,  },  {    tableName: 'users',    sequelize // passing the `sequelize` instance is required  });Address.init(  {    address: {      type: new DataTypes.STRING(128),      allowNull: false    },    createdAt: DataTypes.DATE,    updatedAt: DataTypes.DATE,  },  {    tableName: 'address',    sequelize // passing the `sequelize` instance is required  });// You can also define modules in a functional wayinterface NoteAttributes {  id: number;  title: string;  content: string;}// You can also set multiple attributes optional at oncetype NoteCreationAttributes = Optional<NoteAttributes, 'id' | 'title'>;// And with a functional approach defining a module looks like thisconst Note: ModelDefined<  NoteAttributes,  NoteCreationAttributes> = sequelize.define(  'Note',  {    id: {      type: DataTypes.INTEGER.UNSIGNED,      autoIncrement: true,      primaryKey: true    },    title: {      type: new DataTypes.STRING(64),      defaultValue: 'Unnamed Note'    },    content: {      type: new DataTypes.STRING(4096),      allowNull: false    }  },  {    tableName: 'notes'  });// Here we associate which actually populates out pre-declared `association` static and other methods.User.hasMany(Project, {  sourceKey: 'id',  foreignKey: 'ownerId',  as: 'projects' // this determines the name in `associations`!});Address.belongsTo(User, { targetKey: 'id' });User.hasOne(Address, { sourceKey: 'id' });async function doStuffWithUser() {  const newUser = await User.create({    name: 'Johnny',    preferredName: 'John',  });  console.log(newUser.id, newUser.name, newUser.preferredName);  const project = await newUser.createProject({    name: 'first!'  });  const ourUser = await User.findByPk(1, {    include: [User.associations.projects],    rejectOnEmpty: true // Specifying true here removes `null` from the return type!  });  // Note the `!` null assertion since TS can't know if we included  // the model or not  console.log(ourUser.projects![0].name);}(async () => {  await sequelize.sync();  await doStuffWithUser();})();
```

---
