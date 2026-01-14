# Sequelize - Other

**Pages:** 2

---

## Sequelize v6

**URL:** https://sequelize.org/docs/v6/

**Contents:**
- Sequelize v6
- Quick example​
- Supporting the project​

Sequelize is a promise-based Node.js ORM tool for Postgres, MySQL, MariaDB, SQLite, Microsoft SQL Server, Oracle Database, Amazon Redshift and Snowflake’s Data Cloud. It features solid transaction support, relations, eager and lazy loading, read replication and more.

Sequelize follows Semantic Versioning and supports Node v10 and above.

You are currently looking at the Tutorials and Guides for Sequelize. You might also be interested in the API Reference.

To learn more about how to use Sequelize, read the tutorials available in the left menu. Begin with Getting Started.

Do you like Sequelize and would like to give back to the engineering team behind it?

We have recently created an OpenCollective based money pool which is shared amongst all core maintainers based on their contributions. All support is wholeheartedly welcome. ❤️

**Examples:**

Example 1 (javascript):
```javascript
const { Sequelize, Model, DataTypes } = require('sequelize');const sequelize = new Sequelize('sqlite::memory:');class User extends Model {}User.init(  {    username: DataTypes.STRING,    birthday: DataTypes.DATE,  },  { sequelize, modelName: 'user' },);(async () => {  await sequelize.sync();  const jane = await User.create({    username: 'janedoe',    birthday: new Date(1980, 6, 20),  });  console.log(jane.toJSON());})();
```

---

## Resources

**URL:** https://sequelize.org/docs/v6/other-topics/resources/

**Contents:**
- Resources
- Addons & Plugins​
  - ACL​
  - Auto Code Generation & Scaffolding​
  - Autoloader​
  - Bcrypt​
  - Browser​
  - Caching​
  - Filters​
  - Fixtures / mock data​

---
