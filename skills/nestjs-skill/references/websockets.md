# Nestjs - Websockets

**Pages:** 2

---

## 

**URL:** https://docs.nestjs.com/websockets/adapter

**Contents:**
  - Adapters
    - Extend socket.io#
    - Ws library#
    - Advanced (custom adapter)#
    - Example#

The WebSockets module is platform-agnostic, hence, you can bring your own library (or even a native implementation) by making use of WebSocketAdapter interface. This interface forces to implement few methods described in the following table:

The socket.io package is wrapped in an IoAdapter class. What if you would like to enhance the basic functionality of the adapter? For instance, your technical requirements require a capability to broadcast events across multiple load-balanced instances of your web service. For this, you can extend IoAdapter and override a single method which responsibility is to instantiate new socket.io servers. But first of all, let's install the required package.

Once the package is installed, we can create a RedisIoAdapter class.

Afterward, simply switch to your newly created Redis adapter.

Another available adapter is a WsAdapter which in turn acts like a proxy between the framework and integrate blazing fast and thoroughly tested ws library. This adapter is fully compatible with native browser WebSockets and is far faster than socket.io package. Unluckily, it has significantly fewer functionalities available out-of-the-box. In some cases, you don't necessarily need them though.

In order to use ws, we firstly have to install the required package:

Once the package is installed, we can switch an adapter:

The wsAdapter is designed to handle messages in the { event: string, data: any } format. If you need to receive and process messages in a different format, you'll need to configure a message parser to convert them into this required format.

Alternatively, you can configure the message parser after the adapter is created by using the setMessageParser method.

For demonstration purposes, we are going to integrate the ws library manually. As mentioned, the adapter for this library is already created and is exposed from the @nestjs/platform-ws package as a WsAdapter class. Here is how the simplified implementation could potentially look like:

Then, we can set up a custom adapter using useWebSocketAdapter() method:

A working example that uses WsAdapter is available here.

**Examples:**

Example 1 (bash):
```bash
$ npm i --save redis socket.io @socket.io/redis-adapter
```

Example 2 (typescript):
```typescript
import { IoAdapter } from '@nestjs/platform-socket.io';
import { ServerOptions } from 'socket.io';
import { createAdapter } from '@socket.io/redis-adapter';
import { createClient } from 'redis';

export class RedisIoAdapter extends IoAdapter {
  private adapterConstructor: ReturnType<typeof createAdapter>;

  async connectToRedis(): Promise<void> {
    const pubClient = createClient({ url: `redis://localhost:6379` });
    const subClient = pubClient.duplicate();

    await Promise.all([pubClient.connect(), subClient.connect()]);

    this.adapterConstructor = createAdapter(pubClient, subClient);
  }

  createIOServer(port: number, options?: ServerOptions): any {
    const server = super.createIOServer(port, options);
    server.adapter(this.adapterConstructor);
    return server;
  }
}
```

Example 3 (typescript):
```typescript
const app = await NestFactory.create(AppModule);
const redisIoAdapter = new RedisIoAdapter(app);
await redisIoAdapter.connectToRedis();

app.useWebSocketAdapter(redisIoAdapter);
```

Example 4 (bash):
```bash
$ npm i --save @nestjs/platform-ws
```

---

## 

**URL:** https://docs.nestjs.com/faq/http-adapter

**Contents:**
  - HTTP adapter
    - Outside application context strategy#
    - As injectable#
    - Listening event#

Occasionally, you may want to access the underlying HTTP server, either within the Nest application context or from the outside.

Every native (platform-specific) HTTP server/library (e.g., Express and Fastify) instance is wrapped in an adapter. The adapter is registered as a globally available provider that can be retrieved from the application context, as well as injected into other providers.

To get a reference to the HttpAdapter from outside of the application context, call the getHttpAdapter() method.

To get a reference to the HttpAdapterHost from within the application context, inject it using the same technique as any other existing provider (e.g., using constructor injection).

The HttpAdapterHost is not an actual HttpAdapter. To get the actual HttpAdapter instance, simply access the httpAdapter property.

The httpAdapter is the actual instance of the HTTP adapter used by the underlying framework. It is an instance of either ExpressAdapter or FastifyAdapter (both classes extend AbstractHttpAdapter).

The adapter object exposes several useful methods to interact with the HTTP server. However, if you want to access the library instance (e.g., the Express instance) directly, call the getInstance() method.

To execute an action when the server begins listening for incoming requests, you can subscribe to the listen$ stream, as demonstrated below:

Additionally, the HttpAdapterHost provides a listening boolean property that indicates whether the server is currently active and listening:

**Examples:**

Example 1 (typescript):
```typescript
const app = await NestFactory.create(AppModule);
const httpAdapter = app.getHttpAdapter();
```

Example 2 (typescript):
```typescript
export class CatsService {
  constructor(private adapterHost: HttpAdapterHost) {}
}
```

Example 3 (typescript):
```typescript
@Dependencies(HttpAdapterHost)
export class CatsService {
  constructor(adapterHost) {
    this.adapterHost = adapterHost;
  }
}
```

Example 4 (typescript):
```typescript
const adapterHost = app.get(HttpAdapterHost);
const httpAdapter = adapterHost.httpAdapter;
```

---
