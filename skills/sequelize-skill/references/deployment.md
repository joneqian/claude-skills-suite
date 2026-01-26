# Sequelize - Deployment

**Pages:** 1

---

## Using sequelize in AWS Lambda

**URL:** https://sequelize.org/docs/v6/other-topics/aws-lambda/

**Contents:**
- Using sequelize in AWS Lambda
- TL;DR​
  - Using AWS RDS Proxy​
- The Node.js event loop​
- AWS Lambda function handler types in Node.js​
- AWS Lambda execution environments (i.e. containers)​
- Sequelize connection pooling in AWS Lambda​
  - Detailed race condition example​

AWS Lambda is a serverless computing service that allows customers to run code without having to worry about the underlying servers. Using sequelize in AWS Lambda can be tricky if certain concepts are not properly understood and an appropriate configuration is not used. This guide seeks to clarify some of these concepts so users of the library can properly configure sequelize for AWS Lambda and troubleshoot issues.

If you just want to learn how to properly configure sequelize connection pooling for AWS Lambda, all you need to know is that sequelize connection pooling does not get along well with AWS Lambda's Node.js runtime and it ends up causing more problems than it solves. Therefore, the most appropriate configuration is to use pooling within the same invocation and avoid pooling across invocations (i.e. close all connections at the end):

If your are using AWS RDS and you are using Aurora or a supported database engine, then connect to your database using AWS RDS Proxy. This will make sure that opening/closing connections on each invocation is not an expensive operation for your underlying database server.

If you want to understand why you must use sequelize this way in AWS Lambda, continue reading the rest of this document:

The Node.js event loop is:

what allows Node.js to perform non-blocking I/O operations — despite the fact that JavaScript is single-threaded —

While the event loop implementation is in C++, here's a simplified JavaScript pseudo-implementation that illustrates how Node.js would execute a script named index.js:

AWS Lambda handlers come in two flavors in Node.js:

Non-async handlers (i.e. callback):

Async handlers (i.e. use async/await or Promises):

While at first glance it seems like async VS non-async handlers are simply a code styling choice, there is a fundamental difference between the two:

This fundamental difference is very important to understand in order to rationalize how sequelize may be affected by it. Here are a few examples to illustrate the difference:

AWS Lambda function handlers are invoked by built-in or custom runtimes which run in execution environments (i.e. containers) that may or may not be re-used across invocations. Containers can only process one request at a time. Concurrent invocations of a Lambda function means that a container instance will be created for each concurrent request.

In practice, this means that Lambda functions should be designed to be stateless but developers can use state for caching purposes:

When a Lambda function doesn't wait for the event loop to be empty and a container is re-used, the event loop will be "paused" until the next invocation occurs. For example:

sequelize uses connection pooling for optimizing usage of database connections. The connection pool used by sequelize is implemented using setTimeout() callbacks (which are processed by the Node.js event loop).

Given the fact that AWS Lambda containers process one request at a time, one would be tempted to configure sequelize as follows:

This configuration prevents Lambda containers from overwhelming the database server with an excessive number of connections (since each container takes at most 1 connection). It also makes sure that the container's connection is not garbage collected when idle so the connection does not need to be re-established when the Lambda container is re-used. Unfortunately, this configuration presents a set of issues:

You can attempt to mitigate issue #2 by using { min: 1, max: 2 }. However, this will still suffer from issues #1 and #3 whilst introducing additional ones:

Using { min: 2, max: 2 } mitigates additional issue #1. However, the configuration still suffers from all the other issues (original #1, #3, and additional #2).

In order to make sense of the example, you'll need a bit more context of how certain parts of Lambda and sequelize are implemented.

The built-in AWS Lambda runtime for nodejs.12x is implemented in Node.js. You can access the entire source code of the runtime by reading the contents of /var/runtime/ inside a Node.js Lambda function. The relevant subset of the code is as follows:

The runtime schedules an iteration at the end of the initialization code:

All SQL queries invoked by a Lambda handler using sequelize are ultimately executed using Sequelize.prototype.query(). This method is responsible for obtaining a connection from the pool, executing the query, and releasing the connection back to the pool when the query completes. The following snippet shows a simplification of the method's logic for queries without transactions:

The field this.connectionManager is an instance of a dialect-specific ConnectionManager class. All dialect-specific managers inherit from an abstract ConnectionManager class which initializes the connection pool and configures it to invoke the dialect-specific class' connect() method everytime a new connection needs to be created. The following snippet shows a simplification of the mysql dialect connect() method:

mysql/connection-manager.js

The field this.lib refers to mysql2 and the function createConnection() creates a connection by creating an instance of a Connection class. The relevant subset of this class is as follows:

Based on the previous code, the following sequence of events shows how a connection pooling race condition with { min: 1, max: 1 } can result with in a ETIMEDOUT error:

**Examples:**

Example 1 (javascript):
```javascript
const { Sequelize } = require("sequelize");let sequelize = null;async function loadSequelize() {  const sequelize = new Sequelize(/* (...) */, {    // (...)    pool: {      /*       * Lambda functions process one request at a time but your code may issue multiple queries       * concurrently. Be wary that `sequelize` has methods that issue 2 queries concurrently       * (e.g. `Model.findAndCountAll()`). Using a value higher than 1 allows concurrent queries to       * be executed in parallel rather than serialized. Careful with executing too many queries in       * parallel per Lambda function execution since that can bring down your database with an       * excessive number of connections.       *       * Ideally you want to choose a `max` number where this holds true:       * max * EXPECTED_MAX_CONCURRENT_LAMBDA_INVOCATIONS < MAX_ALLOWED_DATABASE_CONNECTIONS * 0.8       */      max: 2,      /*       * Set this value to 0 so connection pool eviction logic eventually cleans up all connections       * in the event of a Lambda function timeout.       */      min: 0,      /*       * Set this value to 0 so connections are eligible for cleanup immediately after they're       * returned to the pool.       */      idle: 0,      // Choose a small enough value that fails fast if a connection takes too long to be established.      acquire: 3000,      /*       * Ensures the connection pool attempts to be cleaned up automatically on the next Lambda       * function invocation, if the previous invocation timed out.       */      evict: CURRENT_LAMBDA_FUNCTION_TIMEOUT    }  });  // or `sequelize.sync()`  await sequelize.authenticate();  return sequelize;}module.exports.handler = async function (event, callback) {  // re-use the sequelize instance across invocations to improve performance  if (!sequelize) {    sequelize = await loadSequelize();  } else {    // restart connection pool to ensure connections are not re-used across invocations    sequelize.connectionManager.initPools();    // restore `getConnection()` if it has been overwritten by `close()`    if (sequelize.connectionManager.hasOwnProperty("getConnection")) {      delete sequelize.connectionManager.getConnection;    }  }  try {    return await doSomethingWithSequelize(sequelize);  } finally {    // close any opened connections during the invocation    // this will wait for any in-progress queries to finish before closing the connections    await sequelize.connectionManager.close();  }};
```

Example 2 (javascript):
```javascript
// see: https://nodejs.org/en/docs/guides/event-loop-timers-and-nexttick/// see: https://www.youtube.com/watch?v=P9csgxBgaZ8// see: https://www.youtube.com/watch?v=PNa9OMajw9wconst process = require('process');/* * counter of pending events * * reference counter is increased for every: * * 1. scheduled timer: `setTimeout()`, `setInterval()`, etc. * 2. scheduled immediate: `setImmediate()`. * 3. syscall of non-blocking IO: `require('net').Server.listen()`, etc. * 4. scheduled task to the thread pool: `require('fs').WriteStream.write()`, etc. * * reference counter is decreased for every: * * 1. elapsed timer * 2. executed immediate * 3. completed non-blocking IO * 4. completed thread pool task * * references can be explicitly decreased by invoking `.unref()` on some * objects like: `require('net').Socket.unref()` */let refs = 0;/* * a heap of timers, sorted by next ocurrence * * whenever `setTimeout()` or `setInterval()` is invoked, a timer gets added here */const timersHeap = /* (...) */;/* * a FIFO queue of immediates * * whenever `setImmediate()` is invoked, it gets added here */const immediates = /* (...) */;/* * a FIFO queue of next tick callbacks * * whenever `require('process').nextTick()` is invoked, the callback gets added here */const nextTickCallbacks = [];/* * a heap of Promise-related callbacks, sorted by promise constructors callbacks first, * and then resolved/rejected callbacks * * whenever a new Promise instance is created via `new Promise` or a promise resolves/rejects * the appropriate callback (if any) gets added here */const promiseCallbacksHeap = /* ... */;function execTicksAndPromises() {  while (nextTickCallbacks.length || promiseCallbacksHeap.size()) {    // execute all callbacks scheduled with `process.nextTick()`    while (nextTickCallbacks.length) {      const callback = nextTickCallbacks.shift();      callback();    }    // execute all promise-related callbacks    while (promiseCallbacksHeap.size()) {      const callback = promiseCallbacksHeap.pop();      callback();    }  }}try {  // execute index.js  require('./index');  execTicksAndPromises();  do {    // timers phase: executes all elapsed timers    getElapsedTimerCallbacks(timersHeap).forEach(callback => {      callback();      execTicksAndPromises();    });    // pending callbacks phase: executes some system operations (like `TCP errors`) that are not    //                          executed in the poll phase    getPendingCallbacks().forEach(callback => {      callback();      execTicksAndPromises();    })    // poll phase: gets completed non-blocking I/O events or thread pool tasks and invokes the    //             corresponding callbacks; if there are none and there's no pending immediates,    //             it blocks waiting for events/completed tasks for a maximum of `maxWait`    const maxWait = computeWhenNextTimerElapses(timersHeap);    pollForEventsFromKernelOrThreadPool(maxWait, immediates).forEach(callback => {      callback();      execTicksAndPromises();    });    // check phase: execute available immediates; if an immediate callback invokes `setImmediate()`    //              it will be invoked on the next event loop iteration    getImmediateCallbacks(immediates).forEach(callback => {      callback();      execTicksAndPromises();    });    // close callbacks phase: execute special `.on('close')` callbacks    getCloseCallbacks().forEach(callback => {      callback();      execTicksAndPromises();    });    if (refs === 0) {      // listeners of this event may execute code that increments `refs`      process.emit('beforeExit');    }  } while (refs > 0);} catch (err) {  if (!process.listenerCount('uncaughtException')) {    // default behavior: print stack and exit with status code 1    console.error(err.stack);    process.exit(1);  } else {    // there are listeners: emit the event and exit using `process.exitCode || 0`    process.emit('uncaughtException');    process.exit();  }}
```

Example 3 (r):
```r
module.exports.handler = function (event, context, callback) {  try {    doSomething();    callback(null, 'Hello World!'); // Lambda returns "Hello World!"  } catch (err) {    // try/catch is not required, uncaught exceptions invoke `callback(err)` implicitly    callback(err); // Lambda fails with `err`  }};
```

Example 4 (javascript):
```javascript
// async/awaitmodule.exports.handler = async function (event, context) {  try {    await doSomethingAsync();    return 'Hello World!'; // equivalent of: callback(null, "Hello World!");  } catch (err) {    // try/cath is not required, async functions always return a Promise    throw err; // equivalent of: callback(err);  }};// Promisemodule.exports.handler = function (event, context) {  /*   * must return a `Promise` to be considered an async handler   *   * an uncaught exception that prevents a `Promise` to be returned   * by the handler will "downgrade" the handler to non-async   */  return Promise.resolve()    .then(() => doSomethingAsync())    .then(() => 'Hello World!');};
```

---
