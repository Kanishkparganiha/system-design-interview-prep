# API Learning Module: A Complete Guide to Modern APIs

> From beginner to intermediate — understanding APIs through real-world analogies and practical examples.

---

## Table of Contents

1. [What is an API?](#what-is-an-api)
2. [REST API](#1-rest-api)
3. [SOAP API](#2-soap-api)
4. [gRPC API](#3-grpc-api)
5. [GraphQL API](#4-graphql-api)
6. [Webhooks](#5-webhooks)
7. [WebSockets](#6-websockets)
8. [WebRTC](#7-webrtc)
9. [Comparison Matrix](#comparison-matrix)
10. [Decision Guide](#decision-guide)

---

## What is an API?

**API** stands for **Application Programming Interface**. Think of it as a **waiter in a restaurant**:

- You (the client) sit at a table with a menu
- The kitchen (the server) prepares food
- The waiter (the API) takes your order to the kitchen and brings back your food

You don't need to know *how* the kitchen works — you just need to know how to communicate with the waiter.

---

## 1. REST API

### What is it?

**REST** (Representational State Transfer) is an architectural style for designing networked applications. It uses standard HTTP methods to perform operations on resources.

### Real-World Analogy: The Library System

Imagine a library where:
- Each book has a unique catalog number (URL/endpoint)
- You can **GET** a book (read it)
- You can **POST** a new book (donate one)
- You can **PUT** a book back with updates (replace it)
- You can **DELETE** a book (remove it from catalog)

```
Library System          →    REST API
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Catalog number          →    URL endpoint
Librarian actions       →    HTTP methods
Book                    →    Resource
Library card            →    API key/token
```

### How It Works

```
┌──────────────┐         HTTP Request          ┌──────────────┐
│              │  ─────────────────────────▶   │              │
│    Client    │    GET /api/users/123         │    Server    │
│              │  ◀─────────────────────────   │              │
└──────────────┘      JSON Response            └──────────────┘
                  { "name": "John", ... }
```

### Practical Example

```javascript
// Fetching a user from a REST API
fetch('https://api.example.com/users/123', {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer your-token',
        'Content-Type': 'application/json'
    }
})
.then(response => response.json())
.then(data => console.log(data));
```

### Common HTTP Methods

| Method | Purpose | Example |
|--------|---------|---------|
| GET | Retrieve data | Get user profile |
| POST | Create new data | Create new account |
| PUT | Update/replace data | Update entire profile |
| PATCH | Partial update | Update just the email |
| DELETE | Remove data | Delete account |

### Strengths

- **Simple and intuitive** — uses familiar HTTP concepts
- **Stateless** — each request contains all needed information
- **Cacheable** — responses can be cached for performance
- **Scalable** — easy to scale horizontally
- **Wide adoption** — massive community and tooling support

### Limitations

- **Over-fetching** — might receive more data than needed
- **Under-fetching** — might need multiple requests for related data
- **No real-time** — requires polling for updates
- **Versioning challenges** — API changes can break clients

### When to Use REST

✅ Building public APIs for third-party developers
✅ CRUD operations on resources
✅ When simplicity and caching are priorities
✅ Mobile and web applications

### Real-World Examples

- **Twitter API** — fetching tweets, posting updates
- **GitHub API** — managing repositories, issues
- **Stripe API** — processing payments

---

## 2. SOAP API

### What is it?

**SOAP** (Simple Object Access Protocol) is a protocol for exchanging structured information using XML. It's more rigid and formal than REST.

### Real-World Analogy: Certified Mail

Think of SOAP like sending **certified mail with legal documents**:
- Everything must be in a specific envelope format (XML envelope)
- The letter has a strict structure (header, body)
- You get a receipt confirming delivery (built-in error handling)
- It's slower but guaranteed and traceable

```
Certified Mail          →    SOAP API
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Envelope                →    SOAP Envelope
Letter format           →    XML Schema (WSDL)
Certified receipt       →    WS-Security
Post office rules       →    SOAP standards
```

### How It Works

```
┌──────────────┐      SOAP Envelope (XML)      ┌──────────────┐
│              │  ─────────────────────────▶   │              │
│    Client    │   <?xml version="1.0"?>       │    Server    │
│              │   <soap:Envelope>...</soap>   │              │
│              │  ◀─────────────────────────   │              │
└──────────────┘      SOAP Response (XML)      └──────────────┘
```

### SOAP Message Structure

```xml
<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">

    <!-- Optional header for metadata, security, etc. -->
    <soap:Header>
        <auth:Credentials xmlns:auth="http://example.com/auth">
            <auth:Username>user123</auth:Username>
            <auth:Token>abc-xyz-token</auth:Token>
        </auth:Credentials>
    </soap:Header>

    <!-- Required body with actual request -->
    <soap:Body>
        <m:GetUserDetails xmlns:m="http://example.com/users">
            <m:UserId>123</m:UserId>
        </m:GetUserDetails>
    </soap:Body>

</soap:Envelope>
```

### Practical Example (Python)

```python
from zeep import Client

# WSDL defines the service contract
wsdl = 'http://example.com/service?wsdl'
client = Client(wsdl)

# Call a SOAP method
result = client.service.GetUserDetails(UserId=123)
print(result)
```

### Key Components

| Component | Purpose |
|-----------|---------|
| **WSDL** | Describes the service (Web Services Description Language) |
| **SOAP Envelope** | Wraps the entire message |
| **Header** | Contains metadata, security tokens |
| **Body** | Contains the actual request/response |
| **Fault** | Standardized error reporting |

### Strengths

- **Strong typing** — strict contract via WSDL
- **Built-in security** — WS-Security standard
- **ACID compliance** — supports transactions
- **Reliable messaging** — guaranteed delivery
- **Language/platform neutral** — works across any system

### Limitations

- **Verbose** — XML messages are large
- **Complex** — steep learning curve
- **Slower** — more overhead than REST
- **Overkill** — too heavy for simple use cases

### When to Use SOAP

✅ Enterprise integrations (banking, insurance)
✅ When you need guaranteed message delivery
✅ Financial transactions requiring ACID compliance
✅ Legacy system integration
✅ When formal contracts (WSDL) are required

### Real-World Examples

- **Payment gateways** — PayPal's legacy API
- **Banking systems** — inter-bank transfers
- **Healthcare** — HL7 messaging for medical records
- **Government services** — tax filing systems

---

## 3. gRPC API

### What is it?

**gRPC** (Google Remote Procedure Call) is a high-performance framework that uses HTTP/2 and Protocol Buffers for efficient communication between services.

### Real-World Analogy: Walkie-Talkies with Code Words

Imagine military walkie-talkies:
- They use **code words** instead of full sentences (Protocol Buffers = compact binary)
- Communication is **two-way and instant** (bidirectional streaming)
- Multiple conversations can happen **simultaneously** (HTTP/2 multiplexing)
- Everyone uses the same **codebook** (`.proto` files define the contract)

```
Walkie-Talkies          →    gRPC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Code words              →    Protocol Buffers
Codebook                →    .proto files
Two-way radio           →    Bidirectional streaming
Multiple channels       →    HTTP/2 multiplexing
```

### How It Works

```
┌──────────────┐     Binary (Protobuf) / HTTP/2     ┌──────────────┐
│              │  ════════════════════════════════▶ │              │
│   Client     │        Multiplexed Streams         │   Server     │
│   (Stub)     │  ◀════════════════════════════════ │   (Service)  │
└──────────────┘                                    └──────────────┘
        │                                                   │
        └───────── Generated from .proto file ──────────────┘
```

### Protocol Buffer Definition

```protobuf
// user.proto - The contract between client and server

syntax = "proto3";

package user;

// Define the service
service UserService {
    // Unary RPC - single request, single response
    rpc GetUser (GetUserRequest) returns (User);

    // Server streaming - single request, stream of responses
    rpc ListUsers (ListUsersRequest) returns (stream User);

    // Client streaming - stream of requests, single response
    rpc UploadUsers (stream User) returns (UploadResponse);

    // Bidirectional streaming - streams both ways
    rpc Chat (stream Message) returns (stream Message);
}

// Define messages
message GetUserRequest {
    int32 user_id = 1;
}

message User {
    int32 id = 1;
    string name = 2;
    string email = 3;
}
```

### Practical Example (Python)

```python
import grpc
import user_pb2
import user_pb2_grpc

# Create a channel and stub
channel = grpc.insecure_channel('localhost:50051')
stub = user_pb2_grpc.UserServiceStub(channel)

# Make a unary call
request = user_pb2.GetUserRequest(user_id=123)
response = stub.GetUser(request)
print(f"User: {response.name}, Email: {response.email}")

# Server streaming example
for user in stub.ListUsers(user_pb2.ListUsersRequest()):
    print(f"Received user: {user.name}")
```

### Four Communication Patterns

```
1. UNARY (Request-Response)
   Client ──── Request ────▶ Server
   Client ◀─── Response ──── Server

2. SERVER STREAMING
   Client ──── Request ────▶ Server
   Client ◀─── Response 1 ── Server
   Client ◀─── Response 2 ── Server
   Client ◀─── Response N ── Server

3. CLIENT STREAMING
   Client ──── Request 1 ──▶ Server
   Client ──── Request 2 ──▶ Server
   Client ──── Request N ──▶ Server
   Client ◀─── Response ──── Server

4. BIDIRECTIONAL STREAMING
   Client ════ Requests ════▶ Server
   Client ◀═══ Responses ════ Server
   (Both directions simultaneously)
```

### Strengths

- **Blazing fast** — binary serialization, HTTP/2
- **Strongly typed** — compile-time type checking
- **Streaming support** — all four patterns
- **Code generation** — auto-generate client/server code
- **Language agnostic** — supports 10+ languages

### Limitations

- **Not browser-friendly** — requires gRPC-Web for browsers
- **Debugging harder** — binary format isn't human-readable
- **Learning curve** — need to learn Protocol Buffers
- **Limited tooling** — fewer tools than REST

### When to Use gRPC

✅ Microservices communication
✅ Real-time applications requiring streaming
✅ Low-latency, high-throughput systems
✅ Polyglot environments (multiple languages)
✅ Mobile apps needing efficient data transfer

### Real-World Examples

- **Netflix** — inter-service communication
- **Google** — internal services
- **Kubernetes** — container orchestration
- **Cisco** — network management

---

## 4. GraphQL API

### What is it?

**GraphQL** is a query language for APIs that lets clients request exactly the data they need — no more, no less.

### Real-World Analogy: Custom Pizza Order

Imagine ordering a pizza:

- **REST** = Fixed menu: "I'll have Pizza #7" (you get whatever toppings #7 has)
- **GraphQL** = Build your own: "I want thin crust, pepperoni, mushrooms, extra cheese"

You specify exactly what you want, and you get exactly that.

```
Pizza Ordering          →    GraphQL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Custom order            →    Query
Available toppings      →    Schema
Order slip              →    Query document
Kitchen validation      →    Type system
```

### How It Works

```
┌──────────────┐       GraphQL Query           ┌──────────────┐
│              │  ─────────────────────────▶   │              │
│    Client    │    query { user(id: 123)      │    Server    │
│              │      { name, email } }        │   (GraphQL)  │
│              │  ◀─────────────────────────   │              │
└──────────────┘     Exact data requested      └──────────────┘
                  { "user": { "name": "John",
                              "email": "..." }}
```

### Schema Definition

```graphql
# Define types (the shape of your data)
type User {
    id: ID!
    name: String!
    email: String!
    posts: [Post!]!
    friends: [User!]!
}

type Post {
    id: ID!
    title: String!
    content: String!
    author: User!
    comments: [Comment!]!
}

type Comment {
    id: ID!
    text: String!
    author: User!
}

# Define entry points
type Query {
    user(id: ID!): User
    users: [User!]!
    post(id: ID!): Post
}

type Mutation {
    createUser(name: String!, email: String!): User!
    updateUser(id: ID!, name: String): User!
    deleteUser(id: ID!): Boolean!
}

type Subscription {
    newPost: Post!
    userOnline(userId: ID!): User!
}
```

### Query Examples

```graphql
# Basic query - get exactly what you need
query {
    user(id: "123") {
        name
        email
    }
}

# Nested query - fetch related data in one request
query {
    user(id: "123") {
        name
        posts {
            title
            comments {
                text
                author {
                    name
                }
            }
        }
    }
}

# Mutation - modify data
mutation {
    createUser(name: "Jane", email: "jane@example.com") {
        id
        name
    }
}

# Subscription - real-time updates
subscription {
    newPost {
        title
        author {
            name
        }
    }
}
```

### Practical Example (JavaScript)

```javascript
// Using fetch
const query = `
    query GetUser($id: ID!) {
        user(id: $id) {
            name
            email
            posts {
                title
            }
        }
    }
`;

fetch('https://api.example.com/graphql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        query,
        variables: { id: '123' }
    })
})
.then(res => res.json())
.then(data => console.log(data));

// Using Apollo Client
import { useQuery, gql } from '@apollo/client';

const GET_USER = gql`
    query GetUser($id: ID!) {
        user(id: $id) {
            name
            email
        }
    }
`;

function UserProfile({ userId }) {
    const { loading, error, data } = useQuery(GET_USER, {
        variables: { id: userId }
    });

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error!</p>;

    return <h1>{data.user.name}</h1>;
}
```

### REST vs GraphQL Comparison

```
Scenario: Get a user's name and their latest 3 posts

REST (Multiple requests):
────────────────────────
GET /users/123                    → Full user object
GET /users/123/posts?limit=3      → Full post objects
= 2 requests, lots of extra data

GraphQL (Single request):
─────────────────────────
query {
    user(id: "123") {
        name
        posts(limit: 3) {
            title
        }
    }
}
= 1 request, exact data needed
```

### Strengths

- **No over-fetching** — get exactly what you ask for
- **No under-fetching** — get all related data in one request
- **Strongly typed** — schema provides clear contract
- **Introspection** — API is self-documenting
- **Real-time ready** — subscriptions built-in
- **Evolving APIs** — add fields without versioning

### Limitations

- **Complexity** — more complex than REST for simple APIs
- **Caching challenges** — harder to cache than REST
- **N+1 problem** — can cause database performance issues
- **Learning curve** — new concepts to learn
- **File uploads** — not straightforward

### When to Use GraphQL

✅ Complex applications with many related entities
✅ Mobile apps needing bandwidth efficiency
✅ Rapid frontend development
✅ When different clients need different data shapes
✅ Real-time features with subscriptions

### Real-World Examples

- **GitHub API v4** — querying repositories, issues
- **Shopify** — e-commerce platform
- **Facebook** — where GraphQL was created
- **Airbnb** — listing and booking data

---

## 5. Webhooks

### What is it?

**Webhooks** are automated messages sent from apps when something happens. They're HTTP callbacks that notify your application of events in real-time.

### Real-World Analogy: Doorbell Notifications

Think of webhooks like a **smart doorbell**:

- **Polling (without webhooks)**: You check the front door every 5 minutes to see if someone's there
- **Webhooks**: The doorbell rings (notifies you) only when someone arrives

```
Smart Doorbell          →    Webhooks
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Someone at door         →    Event occurs
Doorbell rings          →    HTTP POST sent
Your phone notification →    Your server receives
You see who's there     →    Process the data
```

### How It Works

```
Traditional Polling:
┌──────────────┐                         ┌──────────────┐
│              │ ── "Any updates?" ────▶ │              │
│    Client    │ ◀─── "No" ───────────── │    Server    │
│              │ ── "Any updates?" ────▶ │              │
│              │ ◀─── "No" ───────────── │              │
│              │ ── "Any updates?" ────▶ │              │
│              │ ◀─── "Yes! Here's data" │              │
└──────────────┘                         └──────────────┘
(Wasteful - many unnecessary requests)

Webhooks:
┌──────────────┐                         ┌──────────────┐
│              │                         │              │
│  Your Server │                         │   Provider   │
│  (listening) │                         │   (Stripe)   │
│              │                         │              │
│              │ ◀── Event: payment ──── │   EVENT!     │
│              │ ── "200 OK" ──────────▶ │              │
└──────────────┘                         └──────────────┘
(Efficient - only notified when needed)
```

### Webhook Request Example

```http
POST /webhooks/stripe HTTP/1.1
Host: yourapp.com
Content-Type: application/json
Stripe-Signature: t=1234567890,v1=abc123...

{
    "id": "evt_1234",
    "type": "payment_intent.succeeded",
    "data": {
        "object": {
            "id": "pi_1234",
            "amount": 2000,
            "currency": "usd",
            "customer": "cus_1234"
        }
    }
}
```

### Practical Example (Node.js/Express)

```javascript
const express = require('express');
const crypto = require('crypto');
const app = express();

// Webhook endpoint
app.post('/webhooks/stripe', express.raw({type: 'application/json'}), (req, res) => {
    const signature = req.headers['stripe-signature'];
    const payload = req.body;

    // 1. Verify the webhook signature (CRITICAL for security!)
    const expectedSignature = crypto
        .createHmac('sha256', process.env.WEBHOOK_SECRET)
        .update(payload)
        .digest('hex');

    if (signature !== expectedSignature) {
        return res.status(401).send('Invalid signature');
    }

    // 2. Parse and handle the event
    const event = JSON.parse(payload);

    switch (event.type) {
        case 'payment_intent.succeeded':
            handlePaymentSuccess(event.data.object);
            break;
        case 'customer.subscription.deleted':
            handleSubscriptionCancelled(event.data.object);
            break;
        default:
            console.log(`Unhandled event type: ${event.type}`);
    }

    // 3. Respond quickly (within 5 seconds typically)
    res.status(200).json({ received: true });
});

function handlePaymentSuccess(paymentIntent) {
    console.log(`Payment succeeded: ${paymentIntent.id}`);
    // Update database, send confirmation email, etc.
}
```

### Setting Up Webhooks

```
Step 1: Create an endpoint on your server
        POST https://yourapp.com/webhooks/provider

Step 2: Register the URL with the provider
        (In their dashboard or via API)

Step 3: Provider sends events to your endpoint
        You receive HTTP POST requests

Step 4: Verify signature & process event
        Always verify before trusting the data!

Step 5: Respond with 200 OK
        Within timeout period (usually 5-30 seconds)
```

### Security Best Practices

```javascript
// 1. ALWAYS verify signatures
function verifyWebhookSignature(payload, signature, secret) {
    const computed = crypto
        .createHmac('sha256', secret)
        .update(payload)
        .digest('hex');
    return crypto.timingSafeEqual(
        Buffer.from(signature),
        Buffer.from(computed)
    );
}

// 2. Use HTTPS endpoints only

// 3. Implement idempotency (handle duplicate events)
const processedEvents = new Set();

function handleEvent(event) {
    if (processedEvents.has(event.id)) {
        return; // Already processed
    }
    processedEvents.add(event.id);
    // Process event...
}

// 4. Respond quickly, process asynchronously
app.post('/webhook', (req, res) => {
    res.status(200).send('OK'); // Respond immediately
    processEventAsync(req.body); // Process in background
});
```

### Strengths

- **Real-time** — instant notifications when events occur
- **Efficient** — no wasted polling requests
- **Decoupled** — services don't need to know about each other
- **Simple** — just HTTP POST requests
- **Event-driven** — enables reactive architectures

### Limitations

- **Delivery uncertainty** — what if your server is down?
- **Order not guaranteed** — events may arrive out of order
- **Security concerns** — need to verify signatures
- **Debugging difficulty** — hard to replay events
- **Firewall issues** — your server needs to be publicly accessible

### When to Use Webhooks

✅ Payment notifications (Stripe, PayPal)
✅ CI/CD pipelines (GitHub, GitLab)
✅ Chat integrations (Slack, Discord)
✅ E-commerce events (orders, shipments)
✅ Any event-driven notification system

### Real-World Examples

- **Stripe** — payment success/failure notifications
- **GitHub** — push, PR, issue events
- **Twilio** — SMS received, call completed
- **Shopify** — order created, inventory updated

---

## 6. WebSockets

### What is it?

**WebSockets** provide full-duplex, bidirectional communication over a single, persistent TCP connection. Unlike HTTP's request-response model, WebSockets allow both client and server to send messages at any time.

### Real-World Analogy: Phone Call vs Text Messages

- **HTTP (REST)** = Sending individual text messages. Each message is separate; you send, wait for reply, then send again.
- **WebSockets** = Phone call. Once connected, both parties can talk simultaneously, interrupt each other, or stay silent — the line stays open.

```
Phone Call              →    WebSockets
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Dial number             →    HTTP upgrade request
Call connected          →    WebSocket handshake
Talk anytime            →    Send messages anytime
Hang up                 →    Close connection
```

### How It Works

```
Initial Handshake (HTTP Upgrade):
┌──────────────┐                              ┌──────────────┐
│              │ ── GET /chat HTTP/1.1 ─────▶ │              │
│              │    Upgrade: websocket        │              │
│    Client    │    Connection: Upgrade       │    Server    │
│              │                              │              │
│              │ ◀─ HTTP/1.1 101 Switching ── │              │
│              │    Upgrade: websocket        │              │
└──────────────┘                              └──────────────┘

After Handshake (Full-Duplex):
┌──────────────┐      Persistent Connection   ┌──────────────┐
│              │ ════════════════════════════ │              │
│    Client    │ ◀──── Server can push ────── │    Server    │
│              │ ────── Client can send ────▶ │              │
│              │         (anytime!)           │              │
└──────────────┘                              └──────────────┘
```

### HTTP vs WebSocket Comparison

```
HTTP (Request-Response):
─────────────────────────
Client ── Request 1 ──▶ Server
Client ◀── Response 1 ── Server
[Connection closed]

Client ── Request 2 ──▶ Server
Client ◀── Response 2 ── Server
[Connection closed]

WebSocket (Persistent):
───────────────────────
Client ── Handshake ──▶ Server
Client ◀── Accepted ─── Server
[Connection stays open]

Client ── Message ────▶ Server
Server ── Message ────▶ Client
Client ── Message ────▶ Server
Server ── Message ────▶ Client
Server ── Message ────▶ Client
...
[Until explicitly closed]
```

### Practical Example (Client - JavaScript)

```javascript
// Create WebSocket connection
const socket = new WebSocket('wss://example.com/chat');

// Connection opened
socket.addEventListener('open', (event) => {
    console.log('Connected to server!');
    socket.send(JSON.stringify({
        type: 'join',
        room: 'general',
        user: 'Alice'
    }));
});

// Listen for messages
socket.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);

    switch (data.type) {
        case 'chat':
            displayMessage(data.user, data.message);
            break;
        case 'user_joined':
            showNotification(`${data.user} joined the chat`);
            break;
        case 'typing':
            showTypingIndicator(data.user);
            break;
    }
});

// Send a message
function sendMessage(text) {
    socket.send(JSON.stringify({
        type: 'chat',
        message: text
    }));
}

// Handle errors
socket.addEventListener('error', (event) => {
    console.error('WebSocket error:', event);
});

// Connection closed
socket.addEventListener('close', (event) => {
    console.log('Disconnected:', event.code, event.reason);
    // Implement reconnection logic
});
```

### Practical Example (Server - Node.js)

```javascript
const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 8080 });

// Track all connected clients
const clients = new Map();

wss.on('connection', (ws) => {
    console.log('New client connected');

    ws.on('message', (data) => {
        const message = JSON.parse(data);

        switch (message.type) {
            case 'join':
                // Store client info
                clients.set(ws, { user: message.user, room: message.room });
                // Notify others
                broadcast(message.room, {
                    type: 'user_joined',
                    user: message.user
                }, ws);
                break;

            case 'chat':
                const clientInfo = clients.get(ws);
                // Broadcast to room
                broadcast(clientInfo.room, {
                    type: 'chat',
                    user: clientInfo.user,
                    message: message.message
                });
                break;
        }
    });

    ws.on('close', () => {
        const clientInfo = clients.get(ws);
        if (clientInfo) {
            broadcast(clientInfo.room, {
                type: 'user_left',
                user: clientInfo.user
            });
            clients.delete(ws);
        }
    });
});

function broadcast(room, message, exclude = null) {
    clients.forEach((info, client) => {
        if (info.room === room && client !== exclude) {
            if (client.readyState === WebSocket.OPEN) {
                client.send(JSON.stringify(message));
            }
        }
    });
}
```

### WebSocket Message Types

```javascript
// Text messages (most common)
socket.send('Hello, World!');

// JSON messages
socket.send(JSON.stringify({ type: 'ping' }));

// Binary data (Blob or ArrayBuffer)
socket.send(new Blob(['binary data']));

// Control frames (automatic)
// - Ping/Pong: Keep connection alive
// - Close: Gracefully close connection
```

### Strengths

- **True real-time** — instant bidirectional communication
- **Low latency** — no HTTP overhead after handshake
- **Efficient** — single connection for all messages
- **Full-duplex** — both sides can send simultaneously
- **Wide support** — all modern browsers and platforms

### Limitations

- **Stateful** — harder to scale horizontally
- **Connection management** — need to handle reconnection
- **Firewall/proxy issues** — some networks block WebSockets
- **No built-in features** — need to implement pub/sub, rooms, etc.
- **Resource intensive** — each connection uses server resources

### When to Use WebSockets

✅ Real-time chat applications
✅ Live notifications and feeds
✅ Collaborative editing (Google Docs-style)
✅ Online gaming
✅ Live sports scores / stock tickers
✅ IoT device communication

### Real-World Examples

- **Slack** — real-time messaging
- **Trello** — live board updates
- **Figma** — multiplayer design collaboration
- **Robinhood** — live stock prices

---

## 7. WebRTC

### What is it?

**WebRTC** (Web Real-Time Communication) enables peer-to-peer audio, video, and data transfer directly between browsers without requiring a server to relay the media.

### Real-World Analogy: Direct Phone Line vs Switchboard

Traditional video calls (like old phone systems):
- You → Central Switchboard → Friend
- All audio/video goes through the middle

WebRTC (like a direct private line):
- You ←→ Friend (directly connected)
- After initial setup, data flows peer-to-peer

```
Traditional                    WebRTC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  You ──▶ Server ──▶ Friend     You ◀════════▶ Friend
         (relay)                     (direct)

All data through server        Server only helps connect
Higher latency                 Lower latency
Server bandwidth used          Minimal server load
```

### How It Works

```
Step 1: SIGNALING (via your server - WebSocket, HTTP, etc.)
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│              │       │   Signaling  │       │              │
│    Peer A    │──────▶│    Server    │◀──────│    Peer B    │
│              │       │              │       │              │
└──────────────┘       └──────────────┘       └──────────────┘
        Exchange SDP offers/answers and ICE candidates

Step 2: NAT TRAVERSAL (STUN/TURN servers help find public IPs)
┌──────────────┐       ┌──────────────┐
│              │       │    STUN      │
│    Peer A    │──────▶│    Server    │  "What's my public IP?"
│              │◀──────│              │  "You're 203.0.113.5:12345"
└──────────────┘       └──────────────┘

Step 3: DIRECT CONNECTION (peer-to-peer media flow)
┌──────────────┐                              ┌──────────────┐
│              │ ════════════════════════════ │              │
│    Peer A    │     Audio/Video/Data         │    Peer B    │
│              │    (encrypted, direct)       │              │
└──────────────┘                              └──────────────┘
```

### WebRTC Components

```
┌─────────────────────────────────────────────────────────────┐
│                         WebRTC                               │
├─────────────────┬─────────────────┬─────────────────────────┤
│   getUserMedia  │  RTCPeerConnect │    RTCDataChannel       │
│                 │      ion        │                         │
│   Access camera │  Establish P2P  │   Send arbitrary data   │
│   & microphone  │   connection    │   (files, game state)   │
├─────────────────┴─────────────────┴─────────────────────────┤
│                    ICE Framework                             │
│        (STUN servers find public IPs)                       │
│        (TURN servers relay when direct fails)               │
├─────────────────────────────────────────────────────────────┤
│                Security (SRTP, DTLS)                         │
│          All media encrypted by default                      │
└─────────────────────────────────────────────────────────────┘
```

### Practical Example (Simple Video Call)

```javascript
// Configuration with STUN/TURN servers
const configuration = {
    iceServers: [
        { urls: 'stun:stun.l.google.com:19302' },  // Free Google STUN
        {
            urls: 'turn:your-turn-server.com',
            username: 'user',
            credential: 'pass'
        }
    ]
};

// Create peer connection
const peerConnection = new RTCPeerConnection(configuration);

// Get local media
async function startCall() {
    // 1. Get camera and microphone
    const localStream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true
    });

    // Show local video
    document.getElementById('localVideo').srcObject = localStream;

    // 2. Add tracks to peer connection
    localStream.getTracks().forEach(track => {
        peerConnection.addTrack(track, localStream);
    });

    // 3. Create offer (caller side)
    const offer = await peerConnection.createOffer();
    await peerConnection.setLocalDescription(offer);

    // 4. Send offer to peer via signaling server
    signalingServer.send({
        type: 'offer',
        sdp: offer.sdp
    });
}

// Handle incoming tracks (remote video)
peerConnection.ontrack = (event) => {
    document.getElementById('remoteVideo').srcObject = event.streams[0];
};

// Handle ICE candidates
peerConnection.onicecandidate = (event) => {
    if (event.candidate) {
        signalingServer.send({
            type: 'ice-candidate',
            candidate: event.candidate
        });
    }
};

// Receive answer from peer (caller side)
async function handleAnswer(answer) {
    await peerConnection.setRemoteDescription(
        new RTCSessionDescription(answer)
    );
}

// Receive offer from peer (callee side)
async function handleOffer(offer) {
    await peerConnection.setRemoteDescription(
        new RTCSessionDescription(offer)
    );

    const answer = await peerConnection.createAnswer();
    await peerConnection.setLocalDescription(answer);

    signalingServer.send({
        type: 'answer',
        sdp: answer.sdp
    });
}

// Add received ICE candidate
async function handleIceCandidate(candidate) {
    await peerConnection.addIceCandidate(
        new RTCIceCandidate(candidate)
    );
}
```

### Data Channels (File Transfer, Gaming)

```javascript
// Create data channel (on caller side)
const dataChannel = peerConnection.createDataChannel('files', {
    ordered: true  // Guarantee order (like TCP)
});

dataChannel.onopen = () => {
    console.log('Data channel open!');
    // Send a file
    dataChannel.send(fileData);
};

dataChannel.onmessage = (event) => {
    console.log('Received:', event.data);
};

// Handle data channel (on callee side)
peerConnection.ondatachannel = (event) => {
    const channel = event.channel;
    channel.onmessage = (e) => {
        console.log('Received:', e.data);
    };
};
```

### Signaling Flow

```
Caller (A)                 Server              Callee (B)
    │                        │                     │
    │── Create Offer ──────▶ │                     │
    │   (SDP)                │ ──── Forward ─────▶ │
    │                        │                     │
    │                        │ ◀─── Answer ─────── │
    │ ◀─── Forward ──────────│     (SDP)           │
    │                        │                     │
    │── ICE Candidate ─────▶ │ ──── Forward ─────▶ │
    │                        │                     │
    │ ◀─── Forward ──────────│ ◀── ICE Candidate ─ │
    │                        │                     │
    ├════════════════════════════════════════════════
    │       Direct P2P Connection Established      │
    ├════════════════════════════════════════════════
```

### Strengths

- **Peer-to-peer** — lower latency, less server load
- **Built-in encryption** — all media encrypted (DTLS/SRTP)
- **No plugins** — works natively in browsers
- **High quality** — adaptive bitrate, echo cancellation
- **Versatile** — audio, video, AND arbitrary data

### Limitations

- **Complex setup** — signaling, STUN/TURN needed
- **NAT traversal** — sometimes needs TURN relay (adds latency/cost)
- **Scaling challenges** — many-to-many calls need SFU/MCU servers
- **Codec compatibility** — not all browsers support all codecs
- **Debugging difficult** — many moving parts

### When to Use WebRTC

✅ Video/audio calling (1:1 or small groups)
✅ Screen sharing applications
✅ P2P file sharing
✅ Real-time gaming
✅ Live streaming to limited audience
✅ IoT camera feeds

### Real-World Examples

- **Google Meet** — video conferencing
- **Discord** — voice and video chat
- **Zoom** (partially) — web client
- **Facebook Messenger** — video calls
- **Peer-to-peer file sharing** — ShareDrop

---

## Comparison Matrix

| Feature | REST | SOAP | gRPC | GraphQL | Webhooks | WebSockets | WebRTC |
|---------|------|------|------|---------|----------|------------|--------|
| **Communication** | Request-Response | Request-Response | Streaming + Unary | Request-Response | Event Push | Bidirectional | P2P |
| **Data Format** | JSON/XML | XML | Protobuf (binary) | JSON | JSON | Any | Binary |
| **Transport** | HTTP/1.1 | HTTP/SMTP | HTTP/2 | HTTP | HTTP | TCP | UDP/TCP |
| **Real-time** | ❌ (polling) | ❌ | ✅ (streaming) | ⚠️ (subscriptions) | ✅ | ✅ | ✅ |
| **Browser Support** | ✅ Native | ⚠️ Limited | ⚠️ gRPC-Web | ✅ | ✅ | ✅ | ✅ |
| **Complexity** | Low | High | Medium | Medium | Low | Medium | High |
| **Best For** | CRUD APIs | Enterprise | Microservices | Flexible queries | Events | Chat/Live | Video/Audio |

---

## Decision Guide

```
                    What are you building?
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
      Video/Audio?    Real-time?       Standard API?
          │                │                │
          ▼                │                ▼
       WebRTC              │         Query flexibility
                           │             needed?
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
      Bidirectional?   Event-based?     Yes: GraphQL
          │                │            No: REST
          ▼                ▼
     WebSockets        Webhooks

For internal microservices with high performance needs → gRPC
For enterprise with strict contracts → SOAP
```

### Quick Reference

| Scenario | Recommended API |
|----------|-----------------|
| Public REST API for third parties | **REST** |
| Banking/financial transactions | **SOAP** |
| Microservices (internal) | **gRPC** |
| Complex frontend data needs | **GraphQL** |
| Payment/event notifications | **Webhooks** |
| Chat, live updates | **WebSockets** |
| Video calling, P2P file sharing | **WebRTC** |

---

## Next Steps

1. **Practice**: Build a simple project with each API type
2. **Combine**: Most real apps use multiple (REST + WebSockets + Webhooks)
3. **Explore**: Look at real-world implementations (GitHub, Stripe, Discord APIs)

---

*Happy learning! Remember: there's no "best" API type — only the best fit for your specific use case.*
