# Nestjs - Microservices

**Pages:** 7

---

## 

**URL:** https://docs.nestjs.com/microservices/nats

**Contents:**
  - NATS
    - Installation#
    - Overview#
    - Options#
    - Client#
    - Request-response#
    - Event-based#
    - Queue groups#
    - Context#
    - Wildcards#

NATS is a simple, secure and high performance open source messaging system for cloud native applications, IoT messaging, and microservices architectures. The NATS server is written in the Go programming language, but client libraries to interact with the server are available for dozens of major programming languages. NATS supports both At Most Once and At Least Once delivery. It can run anywhere, from large servers and cloud instances, through edge gateways and even Internet of Things devices.

To start building NATS-based microservices, first install the required package:

To use the NATS transporter, pass the following options object to the createMicroservice() method:

The options object is specific to the chosen transporter. The NATS transporter exposes the properties described here as well as the following properties:

Like other microservice transporters, you have several options for creating a NATS ClientProxy instance.

One method for creating an instance is to use the ClientsModule. To create a client instance with the ClientsModule, import it and use the register() method to pass an options object with the same properties shown above in the createMicroservice() method, as well as a name property to be used as the injection token. Read more about ClientsModulehere.

Other options to create a client (either ClientProxyFactory or @Client()) can be used as well. You can read about them here.

For the request-response message style (read more), the NATS transporter does not use the NATS built-in Request-Reply mechanism. Instead, a "request" is published on a given subject using the publish() method with a unique reply subject name, and responders listen on that subject and send responses to the reply subject. Reply subjects are directed back to the requestor dynamically, regardless of location of either party.

For the event-based message style (read more), the NATS transporter uses NATS built-in Publish-Subscribe mechanism. A publisher sends a message on a subject and any active subscriber listening on that subject receives the message. Subscribers can also register interest in wildcard subjects that work a bit like a regular expression. This one-to-many pattern is sometimes called fan-out.

NATS provides a built-in load balancing feature called distributed queues. To create a queue subscription, use the queue property as follows:

In more complex scenarios, you may need to access additional information about the incoming request. When using the NATS transporter, you can access the NatsContext object.

A subscription may be to an explicit subject, or it may include wildcards.

To configure message options, you can use the NatsRecordBuilder class (note: this is doable for event-based flows as well). For example, to add x-version header, use the setHeaders method, as follows:

And you can read these headers on the server-side as well, by accessing the NatsContext, as follows:

In some cases you might want to configure headers for multiple requests, you can pass these as options to the ClientProxyFactory:

To get real-time updates on the connection and the state of the underlying driver instance, you can subscribe to the status stream. This stream provides status updates specific to the chosen driver. For the NATS driver, the status stream emits connected, disconnected, and reconnecting events.

Similarly, you can subscribe to the server's status stream to receive notifications about the server's status.

In some cases, you might want to listen to internal events emitted by the microservice. For example, you could listen for the error event to trigger additional operations when an error occurs. To do this, use the on() method, as shown below:

Similarly, you can listen to the server's internal events:

For more advanced use cases, you may need to access the underlying driver instance. This can be useful for scenarios like manually closing the connection or using driver-specific methods. However, keep in mind that for most cases, you shouldn't need to access the driver directly.

To do so, you can use the unwrap() method, which returns the underlying driver instance. The generic type parameter should specify the type of driver instance you expect.

Similarly, you can access the server's underlying driver instance:

**Examples:**

Example 1 (bash):
```bash
$ npm i --save nats
```

Example 2 (typescript):
```typescript
const app = await NestFactory.createMicroservice<MicroserviceOptions>(AppModule, {
  transport: Transport.NATS,
  options: {
    servers: ['nats://localhost:4222'],
  },
});
```

Example 3 (typescript):
```typescript
const app = await NestFactory.createMicroservice(AppModule, {
  transport: Transport.NATS,
  options: {
    servers: ['nats://localhost:4222'],
  },
});
```

Example 4 (typescript):
```typescript
@Module({
  imports: [
    ClientsModule.register([
      {
        name: 'MATH_SERVICE',
        transport: Transport.NATS,
        options: {
          servers: ['nats://localhost:4222'],
        }
      },
    ]),
  ]
  ...
})
```

---

## 

**URL:** https://docs.nestjs.com/microservices/redis

**Contents:**
  - Redis
    - Installation#
    - Overview#
    - Options#
    - Client#
    - Context#
    - Wildcards#
    - Instance status updates#
    - Listening to Redis events#
    - Underlying driver access#

The Redis transporter implements the publish/subscribe messaging paradigm and leverages the Pub/Sub feature of Redis. Published messages are categorized in channels, without knowing what subscribers (if any) will eventually receive the message. Each microservice can subscribe to any number of channels. In addition, more than one channel can be subscribed to at a time. Messages exchanged through channels are fire-and-forget, which means that if a message is published and there are no subscribers interested in it, the message is removed and cannot be recovered. Thus, you don't have a guarantee that either messages or events will be handled by at least one service. A single message can be subscribed to (and received) by multiple subscribers.

To start building Redis-based microservices, first install the required package:

To use the Redis transporter, pass the following options object to the createMicroservice() method:

The options property is specific to the chosen transporter. The Redis transporter exposes the properties described below.

All the properties supported by the official ioredis client are also supported by this transporter.

Like other microservice transporters, you have several options for creating a Redis ClientProxy instance.

One method for creating an instance is to use the ClientsModule. To create a client instance with the ClientsModule, import it and use the register() method to pass an options object with the same properties shown above in the createMicroservice() method, as well as a name property to be used as the injection token. Read more about ClientsModulehere.

Other options to create a client (either ClientProxyFactory or @Client()) can be used as well. You can read about them here.

In more complex scenarios, you may need to access additional information about the incoming request. When using the Redis transporter, you can access the RedisContext object.

To enable wildcards support, set the wildcards option to true. This instructs the transporter to use psubscribe and pmessage under the hood.

Make sure to pass the wildcards option when creating a client instance as well.

With this option enabled, you can use wildcards in your message and event patterns. For example, to subscribe to all channels starting with notifications, you can use the following pattern:

To get real-time updates on the connection and the state of the underlying driver instance, you can subscribe to the status stream. This stream provides status updates specific to the chosen driver. For the Redis driver, the status stream emits connected, disconnected, and reconnecting events.

Similarly, you can subscribe to the server's status stream to receive notifications about the server's status.

In some cases, you might want to listen to internal events emitted by the microservice. For example, you could listen for the error event to trigger additional operations when an error occurs. To do this, use the on() method, as shown below:

Similarly, you can listen to the server's internal events:

For more advanced use cases, you may need to access the underlying driver instance. This can be useful for scenarios like manually closing the connection or using driver-specific methods. However, keep in mind that for most cases, you shouldn't need to access the driver directly.

To do so, you can use the unwrap() method, which returns the underlying driver instance. The generic type parameter should specify the type of driver instance you expect.

Similarly, you can access the server's underlying driver instance:

Note that, in contrary to other transporters, the Redis transporter returns a tuple of two ioredis instances: the first one is used for publishing messages, and the second one is used for subscribing to messages.

**Examples:**

Example 1 (bash):
```bash
$ npm i --save ioredis
```

Example 2 (typescript):
```typescript
const app = await NestFactory.createMicroservice<MicroserviceOptions>(AppModule, {
  transport: Transport.REDIS,
  options: {
    host: 'localhost',
    port: 6379,
  },
});
```

Example 3 (typescript):
```typescript
const app = await NestFactory.createMicroservice(AppModule, {
  transport: Transport.REDIS,
  options: {
    host: 'localhost',
    port: 6379,
  },
});
```

Example 4 (typescript):
```typescript
@Module({
  imports: [
    ClientsModule.register([
      {
        name: 'MATH_SERVICE',
        transport: Transport.REDIS,
        options: {
          host: 'localhost',
          port: 6379,
        }
      },
    ]),
  ]
  ...
})
```

---

## 

**URL:** https://docs.nestjs.com/microservices/kafka

**Contents:**
  - Kafka
    - Installation#
    - Overview#
    - Options#
    - Client#
    - Message pattern#
    - Message response subscription#
    - Incoming#
    - Outgoing#
    - Event-based#

Kafka is an open source, distributed streaming platform which has three key capabilities:

The Kafka project aims to provide a unified, high-throughput, low-latency platform for handling real-time data feeds. It integrates very well with Apache Storm and Spark for real-time streaming data analysis.

To start building Kafka-based microservices, first install the required package:

Like other Nest microservice transport layer implementations, you select the Kafka transporter mechanism using the transport property of the options object passed to the createMicroservice() method, along with an optional options property, as shown below:

The options property is specific to the chosen transporter. The Kafka transporter exposes the properties described below.

There is a small difference in Kafka compared to other microservice transporters. Instead of the ClientProxy class, we use the ClientKafkaProxy class.

Like other microservice transporters, you have several options for creating a ClientKafkaProxy instance.

One method for creating an instance is to use the ClientsModule. To create a client instance with the ClientsModule, import it and use the register() method to pass an options object with the same properties shown above in the createMicroservice() method, as well as a name property to be used as the injection token. Read more about ClientsModulehere.

Other options to create a client (either ClientProxyFactory or @Client()) can be used as well. You can read about them here.

Use the @Client() decorator as follows:

The Kafka microservice message pattern utilizes two topics for the request and reply channels. The ClientKafkaProxy.send() method sends messages with a return address by associating a correlation id, reply topic, and reply partition with the request message. This requires the ClientKafkaProxy instance to be subscribed to the reply topic and assigned to at least one partition before sending a message.

Subsequently, you need to have at least one reply topic partition for every Nest application running. For example, if you are running 4 Nest applications but the reply topic only has 3 partitions, then 1 of the Nest applications will error out when trying to send a message.

When new ClientKafkaProxy instances are launched they join the consumer group and subscribe to their respective topics. This process triggers a rebalance of topic partitions assigned to consumers of the consumer group.

Normally, topic partitions are assigned using the round robin partitioner, which assigns topic partitions to a collection of consumers sorted by consumer names which are randomly set on application launch. However, when a new consumer joins the consumer group, the new consumer can be positioned anywhere within the collection of consumers. This creates a condition where pre-existing consumers can be assigned different partitions when the pre-existing consumer is positioned after the new consumer. As a result, the consumers that are assigned different partitions will lose response messages of requests sent before the rebalance.

To prevent the ClientKafkaProxy consumers from losing response messages, a Nest-specific built-in custom partitioner is utilized. This custom partitioner assigns partitions to a collection of consumers sorted by high-resolution timestamps (process.hrtime()) that are set on application launch.

The ClientKafkaProxy class provides the subscribeToResponseOf() method. The subscribeToResponseOf() method takes a request's topic name as an argument and adds the derived reply topic name to a collection of reply topics. This method is required when implementing the message pattern.

If the ClientKafkaProxy instance is created asynchronously, the subscribeToResponseOf() method must be called before calling the connect() method.

Nest receives incoming Kafka messages as an object with key, value, and headers properties that have values of type Buffer. Nest then parses these values by transforming the buffers into strings. If the string is "object like", Nest attempts to parse the string as JSON. The value is then passed to its associated handler.

Nest sends outgoing Kafka messages after a serialization process when publishing events or sending messages. This occurs on arguments passed to the ClientKafkaProxyemit() and send() methods or on values returned from a @MessagePattern method. This serialization "stringifies" objects that are not strings or buffers by using JSON.stringify() or the toString() prototype method.

Outgoing messages can also be keyed by passing an object with the key and value properties. Keying messages is important for meeting the co-partitioning requirement.

Additionally, messages passed in this format can also contain custom headers set in the headers hash property. Header hash property values must be either of type string or type Buffer.

While the request-response method is ideal for exchanging messages between services, it is less suitable when your message style is event-based (which in turn is ideal for Kafka) - when you just want to publish events without waiting for a response. In that case, you do not want the overhead required by request-response for maintaining two topics.

Check out these two sections to learn more about this: Overview: Event-based and Overview: Publishing events.

In more complex scenarios, you may need to access additional information about the incoming request. When using the Kafka transporter, you can access the KafkaContext object.

To access the original Kafka IncomingMessage object, use the getMessage() method of the KafkaContext object, as follows:

Where the IncomingMessage fulfills the following interface:

If your handler involves a slow processing time for each received message you should consider using the heartbeat callback. To retrieve the heartbeat function, use the getHeartbeat() method of the KafkaContext, as follows:

The Kafka microservice components append a description of their respective role onto the client.clientId and consumer.groupId options to prevent collisions between Nest microservice client and server components. By default the ClientKafkaProxy components append -client and the ServerKafka components append -server to both of these options. Note how the provided values below are transformed in that way (as shown in the comments).

Since the Kafka microservice message pattern utilizes two topics for the request and reply channels, a reply pattern should be derived from the request topic. By default, the name of the reply topic is the composite of the request topic name with .reply appended.

Similar to other transporters, all unhandled exceptions are automatically wrapped into an RpcException and converted to a "user-friendly" format. However, there are edge-cases when you might want to bypass this mechanism and let exceptions be consumed by the kafkajs driver instead. Throwing an exception when processing a message instructs kafkajs to retry it (redeliver it) which means that even though the message (or event) handler was triggered, the offset won't be committed to Kafka.

For this, you can use a dedicated class called KafkaRetriableException, as follows:

Along with the default error handling mechanisms, you can create a custom Exception Filter for Kafka events to manage retry logic. For instance, the example below demonstrates how to skip a problematic event after a configurable number of retries:

This filter offers a way to retry processing a Kafka event up to a configurable number of times. Once the maximum retries are reached, it triggers a custom skipHandler (if provided) and commits the offset, effectively skipping the problematic event. This allows subsequent events to be processed without interruption.

You can integrate this filter by adding it to your event handlers:

Committing offsets is essential when working with Kafka. Per default, messages will be automatically committed after a specific time. For more information visit KafkaJS docs. KafkaContext offers a way to access the active consumer for manually committing offsets. The consumer is the KafkaJS consumer and works as the native KafkaJS implementation.

To disable auto-committing of messages set autoCommit: false in the run configuration, as follows:

To get real-time updates on the connection and the state of the underlying driver instance, you can subscribe to the status stream. This stream provides status updates specific to the chosen driver. For the Kafka driver, the status stream emits connected, disconnected, rebalancing, crashed, and stopped events.

Similarly, you can subscribe to the server's status stream to receive notifications about the server's status.

For more advanced use cases, you may need to access the underlying producer and consumer instances. This can be useful for scenarios like manually closing the connection or using driver-specific methods. However, keep in mind that for most cases, you shouldn't need to access the driver directly.

To do so, you can use producer and consumer getters exposed by the ClientKafkaProxy instance.

**Examples:**

Example 1 (bash):
```bash
$ npm i --save kafkajs
```

Example 2 (typescript):
```typescript
const app = await NestFactory.createMicroservice<MicroserviceOptions>(AppModule, {
  transport: Transport.KAFKA,
  options: {
    client: {
      brokers: ['localhost:9092'],
    }
  }
});
```

Example 3 (typescript):
```typescript
const app = await NestFactory.createMicroservice(AppModule, {
  transport: Transport.KAFKA,
  options: {
    client: {
      brokers: ['localhost:9092'],
    }
  }
});
```

Example 4 (typescript):
```typescript
@Module({
  imports: [
    ClientsModule.register([
      {
        name: 'HERO_SERVICE',
        transport: Transport.KAFKA,
        options: {
          client: {
            clientId: 'hero',
            brokers: ['localhost:9092'],
          },
          consumer: {
            groupId: 'hero-consumer'
          }
        }
      },
    ]),
  ]
  ...
})
```

---

## 

**URL:** https://docs.nestjs.com/microservices/grpc

**Contents:**
  - gRPC
    - Installation#
    - Overview#
    - Options#
    - Sample gRPC service#
    - Client#
    - Example#
    - gRPC Reflection#
    - gRPC Streaming#
- Official enterprise support

gRPC is a modern, open source, high performance RPC framework that can run in any environment. It can efficiently connect services in and across data centers with pluggable support for load balancing, tracing, health checking and authentication.

Like many RPC systems, gRPC is based on the concept of defining a service in terms of functions (methods) that can be called remotely. For each method, you define the parameters and return types. Services, parameters, and return types are defined in .proto files using Google's open source language-neutral protocol buffers mechanism.

With the gRPC transporter, Nest uses .proto files to dynamically bind clients and servers to make it easy to implement remote procedure calls, automatically serializing and deserializing structured data.

To start building gRPC-based microservices, first install the required packages:

Like other Nest microservices transport layer implementations, you select the gRPC transporter mechanism using the transport property of the options object passed to the createMicroservice() method. In the following example, we'll set up a hero service. The options property provides metadata about that service; its properties are described below.

In the nest-cli.json file, we add the assets property that allows us to distribute non-TypeScript files, and watchAssets - to turn on watching all non-TypeScript assets. In our case, we want .proto files to be automatically copied to the dist folder.

The gRPC transporter options object exposes the properties described below.

Let's define our sample gRPC service called HeroesService. In the above options object, theprotoPath property sets a path to the .proto definitions file hero.proto. The hero.proto file is structured using protocol buffers. Here's what it looks like:

Our HeroesService exposes a FindOne() method. This method expects an input argument of type HeroById and returns a Hero message (protocol buffers use message elements to define both parameter types and return types).

Next, we need to implement the service. To define a handler that fulfills this definition, we use the @GrpcMethod() decorator in a controller, as shown below. This decorator provides the metadata needed to declare a method as a gRPC service method.

The decorator shown above takes two arguments. The first is the service name (e.g., 'HeroesService'), corresponding to the HeroesService service definition in hero.proto. The second (the string 'FindOne') corresponds to the FindOne() rpc method defined within HeroesService in the hero.proto file.

The findOne() handler method takes three arguments, the data passed from the caller, metadata that stores gRPC request metadata and call to obtain the GrpcCall object properties such as sendMetadata for send metadata to client.

Both @GrpcMethod() decorator arguments are optional. If called without the second argument (e.g., 'FindOne'), Nest will automatically associate the .proto file rpc method with the handler based on converting the handler name to upper camel case (e.g., the findOne handler is associated with the FindOne rpc call definition). This is shown below.

You can also omit the first @GrpcMethod() argument. In this case, Nest automatically associates the handler with the service definition from the proto definitions file based on the class name where the handler is defined. For example, in the following code, class HeroesService associates its handler methods with the HeroesService service definition in the hero.proto file based on the matching of the name 'HeroesService'.

Nest applications can act as gRPC clients, consuming services defined in .proto files. You access remote services through a ClientGrpc object. You can obtain a ClientGrpc object in several ways.

The preferred technique is to import the ClientsModule. Use the register() method to bind a package of services defined in a .proto file to an injection token, and to configure the service. The name property is the injection token. For gRPC services, use transport: Transport.GRPC. The options property is an object with the same properties described above.

Once registered, we can inject the configured ClientGrpc object with @Inject(). Then we use the ClientGrpc object's getService() method to retrieve the service instance, as shown below.

Notice that there is a small difference compared to the technique used in other microservice transport methods. Instead of the ClientProxy class, we use the ClientGrpc class, which provides the getService() method. The getService() generic method takes a service name as an argument and returns its instance (if available).

Alternatively, you can use the @Client() decorator to instantiate a ClientGrpc object, as follows:

Finally, for more complex scenarios, we can inject a dynamically configured client using the ClientProxyFactory class as described here.

In either case, we end up with a reference to our HeroesService proxy object, which exposes the same set of methods that are defined inside the .proto file. Now, when we access this proxy object (i.e., heroesService), the gRPC system automatically serializes requests, forwards them to the remote system, returns a response, and deserializes the response. Because gRPC shields us from these network communication details, heroesService looks and acts like a local provider.

Note, all service methods are lower camel cased (in order to follow the natural convention of the language). So, for example, while our .proto file HeroesService definition contains the FindOne() function, the heroesService instance will provide the findOne() method.

A message handler is also able to return an Observable, in which case the result values will be emitted until the stream is completed.

To send gRPC metadata (along with the request), you can pass a second argument, as follows:

Please note that this would require updating the HeroesService interface that we've defined a few steps earlier.

A working example is available here.

The gRPC Server Reflection Specification is a standard which allows gRPC clients to request details about the API that the server exposes, akin to exposing an OpenAPI document for a REST API. This can make working with developer debugging tools such as grpc-ui or postman significantly easier.

To add gRPC reflection support to your server, first install the required implementation package:

Then it can be hooked into the gRPC server using the onLoadPackageDefinition hook in your gRPC server options, as follows:

Now your server will respond to messages requesting API details using the reflection specification.

gRPC on its own supports long-term live connections, conventionally known as streams. Streams are useful for cases such as Chatting, Observations or Chunk-data transfers. Find more details in the official documentation here.

Nest supports GRPC stream handlers in two possible ways:

Official enterprise support Providing technical guidance Performing in-depth code reviews Mentoring team members Advising best practices Explore more

Let's define a new sample gRPC service called HelloService. The hello.proto file is structured using protocol buffers. Here's what it looks like:

Based on this .proto file, let's define the HelloService interface:

The @GrpcStreamMethod() decorator provides the function parameter as an RxJS Observable. Thus, we can receive and process multiple messages.

According to the service definition (in the .proto file), the BidiHello method should stream requests to the service. To send multiple asynchronous messages to the stream from a client, we leverage an RxJS ReplaySubject class.

In the example above, we wrote two messages to the stream (next() calls) and notified the service that we've completed sending the data (complete() call).

When the method return value is defined as stream, the @GrpcStreamCall() decorator provides the function parameter as grpc.ServerDuplexStream, which supports standard methods like .on('data', callback), .write(message) or .cancel(). Full documentation on available methods can be found here.

Alternatively, when the method return value is not a stream, the @GrpcStreamCall() decorator provides two function parameters, respectively grpc.ServerReadableStream (read more here) and callback.

Let's start with implementing the BidiHello which should support a full-duplex interaction.

In the example above, we used the write() method to write objects to the response stream. The callback passed into the .on() method as a second parameter will be called every time our service receives a new chunk of data.

Let's implement the LotsOfGreetings method.

Here we used the callback function to send the response once processing of the requestStream has been completed.

When running a gRPC application in an orchestrator such a Kubernetes, you may need to know if it is running and in a healthy state. The gRPC Health Check specification is a standard that allow gRPC clients to expose their health status to allow the orchestrator to act accordingly.

To add gRPC health check support, first install the grpc-node package:

Then it can be hooked into the gRPC service using the onLoadPackageDefinition hook in your gRPC server options, as follows. Note that the protoPath needs to have both the health check and the hero package.

Metadata is information about a particular RPC call in the form of a list of key-value pairs, where the keys are strings and the values are typically strings but can be binary data. Metadata is opaque to gRPC itself - it lets the client provide information associated with the call to the server and vice versa. Metadata may include authentication tokens, request identifiers and tags for monitoring purposes, and data information such as the number of records in a data set.

To read the metadata in @GrpcMethod() handler, use the second argument (metadata), which is of type Metadata (imported from the grpc package).

To send back metadata from the handler, use the ServerUnaryCall#sendMetadata() method (third handler argument).

Likewise, to read the metadata in handlers annotated with the @GrpcStreamMethod() handler (subject strategy), use the second argument (metadata), which is of type Metadata (imported from the grpc package).

To send back metadata from the handler, use the ServerDuplexStream#sendMetadata() method (third handler argument).

To read metadata from within the call stream handlers (handlers annotated with @GrpcStreamCall() decorator), listen to the metadata event on the requestStream reference, as follows:

**Examples:**

Example 1 (bash):
```bash
$ npm i --save @grpc/grpc-js @grpc/proto-loader
```

Example 2 (typescript):
```typescript
const app = await NestFactory.createMicroservice<MicroserviceOptions>(AppModule, {
  transport: Transport.GRPC,
  options: {
    package: 'hero',
    protoPath: join(__dirname, 'hero/hero.proto'),
  },
});
```

Example 3 (typescript):
```typescript
const app = await NestFactory.createMicroservice(AppModule, {
  transport: Transport.GRPC,
  options: {
    package: 'hero',
    protoPath: join(__dirname, 'hero/hero.proto'),
  },
});
```

Example 4 (json):
```json
{
  "compilerOptions": {
    "assets": ["**/*.proto"],
    "watchAssets": true
  }
}
```

---

## 

**URL:** https://docs.nestjs.com/microservices/custom-transport

**Contents:**
  - Custom transporters
    - Creating a strategy#
    - Client proxy#
    - Message serialization#

Nest provides a variety of transporters out-of-the-box, as well as an API allowing developers to build new custom transport strategies. Transporters enable you to connect components over a network using a pluggable communications layer and a very simple application-level message protocol (read full article).

With a custom transporter, you can integrate any messaging system/protocol (including Google Cloud Pub/Sub, Amazon Kinesis, and others) or extend the existing one, adding extra features on top (for example, QoS for MQTT).

First, let's define a class representing our custom transporter.

In our example above, we declared the GoogleCloudPubSubServer class and provided listen() and close() methods enforced by the CustomTransportStrategy interface. Also, our class extends the Server class imported from the @nestjs/microservices package that provides a few useful methods, for example, methods used by Nest runtime to register message handlers. Alternatively, in case you want to extend the capabilities of an existing transport strategy, you could extend the corresponding server class, for example, ServerRedis. Conventionally, we added the "Server" suffix to our class as it will be responsible for subscribing to messages/events (and responding to them, if necessary).

With this in place, we can now use our custom strategy instead of using a built-in transporter, as follows:

Basically, instead of passing the normal transporter options object with transport and options properties, we pass a single property, strategy, whose value is an instance of our custom transporter class.

Back to our GoogleCloudPubSubServer class, in a real-world application, we would be establishing a connection to our message broker/external service and registering subscribers/listening to specific channels in listen() method (and then removing subscriptions & closing the connection in the close() teardown method), but since this requires a good understanding of how Nest microservices communicate with each other, we recommend reading this article series. In this chapter instead, we'll focus on the capabilities the Server class provides and how you can leverage them to build custom strategies.

For example, let's say that somewhere in our application, the following message handler is defined:

This message handler will be automatically registered by Nest runtime. With Server class, you can see what message patterns have been registered and also, access and execute the actual methods that were assigned to them. To test this out, let's add a simple console.log inside listen() method before callback function is called:

After your application restarts, you'll see the following log in your terminal:

As you can see, the messageHandlers property is a Map collection of all message (and event) handlers, in which patterns are being used as keys. Now, you can use a key (for example, "echo") to receive a reference to the message handler:

Once we execute the echoHandler passing an arbitrary string as an argument ("Hello world!" here), we should see it in the console:

Which means that our method handler was properly executed.

When using a CustomTransportStrategy with Interceptors the handlers are wrapped into RxJS streams. This means that you need to subscribe to them in order to execute the streams underlying logic (e.g. continue into the controller logic after an interceptor has been executed).

An example of this can be seen below:

As we mentioned in the first section, you don't necessarily need to use the @nestjs/microservices package to create microservices, but if you decide to do so and you need to integrate a custom strategy, you will need to provide a "client" class too.

To communicate with an external service/emit & publish messages (or events) you can either use a library-specific SDK package, or implement a custom client class that extends the ClientProxy, as follows:

As you can see, ClientProxy class requires us to provide several methods for establishing & closing the connection and publishing messages (publish) and events (dispatchEvent). Note, if you don't need a request-response communication style support, you can leave the publish() method empty. Likewise, if you don't need to support event-based communication, skip the dispatchEvent() method.

To observe what and when those methods are executed, let's add multiple console.log calls, as follows:

With this in place, let's create an instance of GoogleCloudPubSubClient class and run the send() method (which you might have seen in earlier chapters), subscribing to the returned observable stream.

Now, you should see the following output in your terminal:

To test if our "teardown" method (which our publish() method returns) is properly executed, let's apply a timeout operator to our stream, setting it to 2 seconds to make sure it throws earlier then our setTimeout calls the callback function.

With timeout operator applied, your terminal output should look as follows:

To dispatch an event (instead of sending a message), use the emit() method:

And that's what you should see in the console:

If you need to add some custom logic around the serialization of responses on the client side, you can use a custom class that extends the ClientProxy class or one of its child classes. For modifying successful requests you can override the serializeResponse method, and for modifying any errors that go through this client you can override the serializeError method. To make use of this custom class, you can pass the class itself to the ClientsModule.register() method using the customClass property. Below is an example of a custom ClientProxy that serializes each error into an RpcException.

and then use it in the ClientsModule like so:

**Examples:**

Example 1 (typescript):
```typescript
import { CustomTransportStrategy, Server } from '@nestjs/microservices';

class GoogleCloudPubSubServer
  extends Server
  implements CustomTransportStrategy
{
  /**
   * Triggered when you run "app.listen()".
   */
  listen(callback: () => void) {
    callback();
  }

  /**
   * Triggered on application shutdown.
   */
  close() {}

  /**
   * You can ignore this method if you don't want transporter users
   * to be able to register event listeners. Most custom implementations
   * will not need this.
   */
  on(event: string, callback: Function) {
    throw new Error('Method not implemented.');
  }

  /**
   * You can ignore this method if you don't want transporter users
   * to be able to retrieve the underlying native server. Most custom implementations
   * will not need this.
   */
  unwrap<T = never>(): T {
    throw new Error('Method not implemented.');
  }
}
```

Example 2 (typescript):
```typescript
const app = await NestFactory.createMicroservice<MicroserviceOptions>(
  AppModule,
  {
    strategy: new GoogleCloudPubSubServer(),
  },
);
```

Example 3 (typescript):
```typescript
@MessagePattern('echo')
echo(@Payload() data: object) {
  return data;
}
```

Example 4 (typescript):
```typescript
listen(callback: () => void) {
  console.log(this.messageHandlers);
  callback();
}
```

---

## 

**URL:** https://docs.nestjs.com/microservices/rabbitmq

**Contents:**
  - RabbitMQ
    - Installation#
    - Overview#
    - Options#
    - Client#
    - Context#
    - Message acknowledgement#
    - Record builders#
    - Instance status updates#
    - Listening to RabbitMQ events#

RabbitMQ is an open-source and lightweight message broker which supports multiple messaging protocols. It can be deployed in distributed and federated configurations to meet high-scale, high-availability requirements. In addition, it's the most widely deployed message broker, used worldwide at small startups and large enterprises.

To start building RabbitMQ-based microservices, first install the required packages:

To use the RabbitMQ transporter, pass the following options object to the createMicroservice() method:

The options property is specific to the chosen transporter. The RabbitMQ transporter exposes the properties described below.

Like other microservice transporters, you have several options for creating a RabbitMQ ClientProxy instance.

One method for creating an instance is to use the ClientsModule. To create a client instance with the ClientsModule, import it and use the register() method to pass an options object with the same properties shown above in the createMicroservice() method, as well as a name property to be used as the injection token. Read more about ClientsModulehere.

Other options to create a client (either ClientProxyFactory or @Client()) can be used as well. You can read about them here.

In more complex scenarios, you may need to access additional information about the incoming request. When using the RabbitMQ transporter, you can access the RmqContext object.

To access the original RabbitMQ message (with the properties, fields, and content), use the getMessage() method of the RmqContext object, as follows:

To retrieve a reference to the RabbitMQ channel, use the getChannelRef method of the RmqContext object, as follows:

To make sure a message is never lost, RabbitMQ supports message acknowledgements. An acknowledgement is sent back by the consumer to tell RabbitMQ that a particular message has been received, processed and that RabbitMQ is free to delete it. If a consumer dies (its channel is closed, connection is closed, or TCP connection is lost) without sending an ack, RabbitMQ will understand that a message wasn't processed fully and will re-queue it.

To enable manual acknowledgment mode, set the noAck property to false:

When manual consumer acknowledgements are turned on, we must send a proper acknowledgement from the worker to signal that we are done with a task.

To configure message options, you can use the RmqRecordBuilder class (note: this is doable for event-based flows as well). For example, to set headers and priority properties, use the setOptions method, as follows:

And you can read these values on the server-side as well, by accessing the RmqContext, as follows:

To get real-time updates on the connection and the state of the underlying driver instance, you can subscribe to the status stream. This stream provides status updates specific to the chosen driver. For the RMQ driver, the status stream emits connected and disconnected events.

Similarly, you can subscribe to the server's status stream to receive notifications about the server's status.

In some cases, you might want to listen to internal events emitted by the microservice. For example, you could listen for the error event to trigger additional operations when an error occurs. To do this, use the on() method, as shown below:

Similarly, you can listen to the server's internal events:

For more advanced use cases, you may need to access the underlying driver instance. This can be useful for scenarios like manually closing the connection or using driver-specific methods. However, keep in mind that for most cases, you shouldn't need to access the driver directly.

To do so, you can use the unwrap() method, which returns the underlying driver instance. The generic type parameter should specify the type of driver instance you expect.

Similarly, you can access the server's underlying driver instance:

RabbitMQ supports the use of wildcards in routing keys to allow for flexible message routing. The # wildcard matches zero or more words, while the * wildcard matches exactly one word.

For example, the routing key cats.# matches cats, cats.meow, and cats.meow.purr. The routing key cats.* matches cats.meow but not cats.meow.purr.

To enable wildcard support in your RabbitMQ microservice, set the wildcards configuration option to true in the options object:

With this configuration, you can use wildcards in your routing keys when subscribing to events/messages. For example, to listen for messages with the routing key cats.#, you can use the following code:

To send a message with a specific routing key, you can use the send() method of the ClientProxy instance:

**Examples:**

Example 1 (bash):
```bash
$ npm i --save amqplib amqp-connection-manager
```

Example 2 (typescript):
```typescript
const app = await NestFactory.createMicroservice<MicroserviceOptions>(AppModule, {
  transport: Transport.RMQ,
  options: {
    urls: ['amqp://localhost:5672'],
    queue: 'cats_queue',
    queueOptions: {
      durable: false
    },
  },
});
```

Example 3 (typescript):
```typescript
const app = await NestFactory.createMicroservice(AppModule, {
  transport: Transport.RMQ,
  options: {
    urls: ['amqp://localhost:5672'],
    queue: 'cats_queue',
    queueOptions: {
      durable: false
    },
  },
});
```

Example 4 (typescript):
```typescript
@Module({
  imports: [
    ClientsModule.register([
      {
        name: 'MATH_SERVICE',
        transport: Transport.RMQ,
        options: {
          urls: ['amqp://localhost:5672'],
          queue: 'cats_queue',
          queueOptions: {
            durable: false
          },
        },
      },
    ]),
  ]
  ...
})
```

---

## 

**URL:** https://docs.nestjs.com/microservices/mqtt

**Contents:**
  - MQTT
    - Installation#
    - Overview#
    - Options#
    - Client#
    - Context#
    - Wildcards#
    - Quality of Service (QoS)#
    - Record builders#
    - Instance status updates#

MQTT (Message Queuing Telemetry Transport) is an open source, lightweight messaging protocol, optimized for low latency. This protocol provides a scalable and cost-efficient way to connect devices using a publish/subscribe model. A communication system built on MQTT consists of the publishing server, a broker and one or more clients. It is designed for constrained devices and low-bandwidth, high-latency or unreliable networks.

To start building MQTT-based microservices, first install the required package:

To use the MQTT transporter, pass the following options object to the createMicroservice() method:

The options object is specific to the chosen transporter. The MQTT transporter exposes the properties described here.

Like other microservice transporters, you have several options for creating a MQTT ClientProxy instance.

One method for creating an instance is to use use the ClientsModule. To create a client instance with the ClientsModule, import it and use the register() method to pass an options object with the same properties shown above in the createMicroservice() method, as well as a name property to be used as the injection token. Read more about ClientsModulehere.

Other options to create a client (either ClientProxyFactory or @Client()) can be used as well. You can read about them here.

In more complex scenarios, you may need to access additional information about the incoming request. When using the MQTT transporter, you can access the MqttContext object.

To access the original mqtt packet, use the getPacket() method of the MqttContext object, as follows:

A subscription may be to an explicit topic, or it may include wildcards. Two wildcards are available, + and #. + is a single-level wildcard, while # is a multi-level wildcard which covers many topic levels.

Any subscription created with @MessagePattern or @EventPattern decorators will subscribe with QoS 0. If a higher QoS is required, it can be set globally using the subscribeOptions block when establishing the connection as follows:

If a topic specific QoS is required, consider creating a Custom transporter.

To configure message options (adjust the QoS level, set the Retain or DUP flags, or add additional properties to the payload), you can use the MqttRecordBuilder class. For example, to set QoS to 2 use the setQoS method, as follows:

And you can read these options on the server-side as well, by accessing the MqttContext.

In some cases you might want to configure user properties for multiple requests, you can pass these options to the ClientProxyFactory.

To get real-time updates on the connection and the state of the underlying driver instance, you can subscribe to the status stream. This stream provides status updates specific to the chosen driver. For the MQTT driver, the status stream emits connected, disconnected, reconnecting, and closed events.

Similarly, you can subscribe to the server's status stream to receive notifications about the server's status.

In some cases, you might want to listen to internal events emitted by the microservice. For example, you could listen for the error event to trigger additional operations when an error occurs. To do this, use the on() method, as shown below:

Similarly, you can listen to the server's internal events:

For more advanced use cases, you may need to access the underlying driver instance. This can be useful for scenarios like manually closing the connection or using driver-specific methods. However, keep in mind that for most cases, you shouldn't need to access the driver directly.

To do so, you can use the unwrap() method, which returns the underlying driver instance. The generic type parameter should specify the type of driver instance you expect.

Similarly, you can access the server's underlying driver instance:

**Examples:**

Example 1 (bash):
```bash
$ npm i --save mqtt
```

Example 2 (typescript):
```typescript
const app = await NestFactory.createMicroservice<MicroserviceOptions>(AppModule, {
  transport: Transport.MQTT,
  options: {
    url: 'mqtt://localhost:1883',
  },
});
```

Example 3 (typescript):
```typescript
const app = await NestFactory.createMicroservice(AppModule, {
  transport: Transport.MQTT,
  options: {
    url: 'mqtt://localhost:1883',
  },
});
```

Example 4 (typescript):
```typescript
@Module({
  imports: [
    ClientsModule.register([
      {
        name: 'MATH_SERVICE',
        transport: Transport.MQTT,
        options: {
          url: 'mqtt://localhost:1883',
        }
      },
    ]),
  ]
  ...
})
```

---
