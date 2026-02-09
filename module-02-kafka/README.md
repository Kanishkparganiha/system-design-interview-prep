# Module 02: Apache Kafka Deep Dive

> Understanding distributed event streaming through concepts, simulations, and real-world implementations.

---

## Video Resource

📺 **Recommended Video:** [Apache Kafka Explained](https://youtu.be/DU8o-OTeoCc?si=dlKHJkV5AG5Kp-Mt)

Watch this video for a visual walkthrough of Kafka concepts before diving into the material below.

---

## Table of Contents

1. [What is Kafka?](#what-is-kafka)
2. [Real-World Analogy](#real-world-analogy)
3. [Core Concepts](#core-concepts)
4. [Architecture Deep Dive](#architecture-deep-dive)
5. [How Kafka Works Internally](#how-kafka-works-internally)
6. [Python Simulations](#python-simulations)
7. [Using Real Kafka with Python](#using-real-kafka-with-python)
8. [Use Case: Real-Time Order Processing](#use-case-real-time-order-processing)
9. [Interview Questions](#interview-questions)

---

## What is Kafka?

**Apache Kafka** is a distributed event streaming platform capable of handling trillions of events per day. Think of it as a **super-powered, distributed commit log** that:

- **Stores** streams of records durably and reliably
- **Processes** streams of records as they occur
- **Publishes & Subscribes** to streams of records (like a messaging system)

### Why Kafka?

| Problem | Traditional Solution | Kafka Solution |
|---------|---------------------|----------------|
| High throughput messaging | Message queues (slow) | Millions of messages/sec |
| Data loss on failure | Hope for the best | Replicated, durable logs |
| Real-time + Batch processing | Separate systems | Single platform |
| Decoupling services | Point-to-point connections | Centralized event bus |

---

## Real-World Analogy

### The Newspaper Distribution Center

Imagine Kafka as a **massive newspaper distribution center**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    NEWSPAPER DISTRIBUTION CENTER                 │
│                         (Kafka Cluster)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   LOADING DOCKS (Topics)                                         │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│   │   Sports    │  │   Weather   │  │   Finance   │             │
│   │   Section   │  │   Section   │  │   Section   │             │
│   └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                  │
│   PRINTING PRESSES (Producers)                                   │
│   📰 → Continuously print newspapers and send to loading docks   │
│                                                                  │
│   STORAGE RACKS (Partitions)                                     │
│   📦 Each section has multiple racks, papers stored in order     │
│                                                                  │
│   DELIVERY TRUCKS (Consumers)                                    │
│   🚚 Pick up papers from racks, remember where they left off     │
│                                                                  │
│   BACKUP COPIES (Replication)                                    │
│   📋 Each paper copied to multiple locations for safety          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Mapping to Kafka:**

| Newspaper Center | Kafka Concept |
|------------------|---------------|
| Distribution Center | Kafka Cluster |
| Section (Sports, Weather) | Topic |
| Storage Rack | Partition |
| Paper's position on rack | Offset |
| Printing Press | Producer |
| Delivery Truck | Consumer |
| Fleet of trucks for one section | Consumer Group |
| Backup copies | Replication Factor |

---

## Core Concepts

### 1. Topics

A **topic** is a category or feed name to which records are published.

```
Topic: "user-signups"
┌────────────────────────────────────────────────────────────────┐
│  Message 1 │ Message 2 │ Message 3 │ Message 4 │ Message 5 │...│
└────────────────────────────────────────────────────────────────┘
              ───────────────────────────────────────────▶
                              Time / Offset
```

### 2. Partitions

Topics are split into **partitions** for parallelism and scalability.

```
Topic: "orders" (3 partitions)

Partition 0: │ msg0 │ msg3 │ msg6 │ msg9  │ ...
Partition 1: │ msg1 │ msg4 │ msg7 │ msg10 │ ...
Partition 2: │ msg2 │ msg5 │ msg8 │ msg11 │ ...

Each partition:
- Is an ordered, immutable sequence
- Has its own offset counter
- Can be on different brokers
- Enables parallel processing
```

### 3. Offsets

An **offset** is a unique identifier for each message within a partition.

```
Partition 0:
┌─────┬─────┬─────┬─────┬─────┬─────┐
│  0  │  1  │  2  │  3  │  4  │  5  │  ← Offsets
├─────┼─────┼─────┼─────┼─────┼─────┤
│ Msg │ Msg │ Msg │ Msg │ Msg │ Msg │  ← Messages
└─────┴─────┴─────┴─────┴─────┴─────┘
                          ▲
                    Consumer is here
                    (committed offset: 4)
```

### 4. Producers

**Producers** publish data to topics.

```python
# Conceptually:
producer.send(
    topic="orders",
    key="user-123",      # Determines partition
    value={"item": "laptop", "price": 999}
)
```

### 5. Consumers & Consumer Groups

**Consumers** read data from topics. **Consumer Groups** enable parallel processing.

```
Topic "orders" (3 partitions)
           │
           ▼
┌─────────────────────────────────────┐
│      Consumer Group: "order-service" │
├─────────────────────────────────────┤
│                                      │
│   Consumer 1 ◄── Partition 0         │
│   Consumer 2 ◄── Partition 1         │
│   Consumer 3 ◄── Partition 2         │
│                                      │
└─────────────────────────────────────┘

Rule: Each partition → exactly ONE consumer in a group
      (But one consumer can handle multiple partitions)
```

### 6. Brokers

A **broker** is a Kafka server that stores data and serves clients.

```
Kafka Cluster (3 Brokers)
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Broker 1   │  │  Broker 2   │  │  Broker 3   │
│             │  │             │  │             │
│ Topic A     │  │ Topic A     │  │ Topic A     │
│ Partition 0 │  │ Partition 1 │  │ Partition 2 │
│ (Leader)    │  │ (Leader)    │  │ (Leader)    │
│             │  │             │  │             │
│ Topic A     │  │ Topic A     │  │ Topic A     │
│ Partition 1 │  │ Partition 2 │  │ Partition 0 │
│ (Replica)   │  │ (Replica)   │  │ (Replica)   │
└─────────────┘  └─────────────┘  └─────────────┘
```

### 7. Replication

**Replication** ensures fault tolerance. Each partition has:
- **1 Leader**: Handles all reads/writes
- **N-1 Followers**: Replicate data from leader

```
Partition 0 (Replication Factor: 3)

Broker 1 (Leader)     Broker 2 (Follower)   Broker 3 (Follower)
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│ msg0,msg1,msg2  │──▶│ msg0,msg1,msg2  │   │ msg0,msg1,msg2  │
│                 │──▶│                 │   │                 │
└─────────────────┘   └─────────────────┘   └─────────────────┘
        │                     ▲                     ▲
        └─────────────────────┴─────────────────────┘
                    Replication
```

---

## Architecture Deep Dive

### Complete Kafka Architecture

```
                              KAFKA CLUSTER
┌──────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│    ┌─────────────────────────────────────────────────────────────┐       │
│    │                     ZOOKEEPER / KRAFT                        │       │
│    │    • Cluster metadata    • Leader election                   │       │
│    │    • Topic configuration • Consumer group coordination       │       │
│    └─────────────────────────────────────────────────────────────┘       │
│                                    │                                      │
│         ┌──────────────────────────┼──────────────────────────┐          │
│         ▼                          ▼                          ▼          │
│    ┌─────────┐               ┌─────────┐               ┌─────────┐       │
│    │ Broker 1│               │ Broker 2│               │ Broker 3│       │
│    │         │◄─────────────▶│         │◄─────────────▶│         │       │
│    │ P0(L)   │  Replication  │ P1(L)   │  Replication  │ P2(L)   │       │
│    │ P1(F)   │               │ P2(F)   │               │ P0(F)   │       │
│    └────┬────┘               └────┬────┘               └────┬────┘       │
│         │                         │                         │            │
└─────────┼─────────────────────────┼─────────────────────────┼────────────┘
          │                         │                         │
          ▼                         ▼                         ▼
    ┌──────────┐             ┌──────────┐             ┌──────────┐
    │ Producer │             │ Producer │             │ Producer │
    │    A     │             │    B     │             │    C     │
    └──────────┘             └──────────┘             └──────────┘

          │                         │                         │
          ▼                         ▼                         ▼
    ┌──────────┐             ┌──────────┐             ┌──────────┐
    │ Consumer │             │ Consumer │             │ Consumer │
    │ Group 1  │             │ Group 1  │             │ Group 2  │
    └──────────┘             └──────────┘             └──────────┘

(L) = Leader    (F) = Follower    P = Partition
```

### Message Flow

```
Producer sends message
         │
         ▼
┌────────────────────┐
│ 1. Serialize data  │
│ 2. Determine        │
│    partition        │──▶ Key hash % num_partitions
│ 3. Batch messages   │     OR round-robin if no key
└────────────────────┘
         │
         ▼
┌────────────────────┐
│ 4. Send to Leader  │
│    Broker          │
└────────────────────┘
         │
         ▼
┌────────────────────┐
│ 5. Write to commit │
│    log (disk)      │
│ 6. Replicate to    │
│    followers       │
└────────────────────┘
         │
         ▼
┌────────────────────┐
│ 7. Acknowledge     │
│    producer        │──▶ acks=0 (fire & forget)
│                    │    acks=1 (leader only)
└────────────────────┘    acks=all (all replicas)
```

---

## How Kafka Works Internally

### The Commit Log

Kafka's secret sauce is the **append-only commit log**:

```
Partition = Append-only log file on disk

┌───────────────────────────────────────────────────────────────────┐
│                         COMMIT LOG                                 │
├───────────────────────────────────────────────────────────────────┤
│                                                                    │
│   Offset: 0        1        2        3        4        5          │
│         ┌────┐  ┌────┐  ┌────┐  ┌────┐  ┌────┐  ┌────┐           │
│         │Msg │  │Msg │  │Msg │  │Msg │  │Msg │  │Msg │  ────▶    │
│         │ A  │  │ B  │  │ C  │  │ D  │  │ E  │  │ F  │  (append) │
│         └────┘  └────┘  └────┘  └────┘  └────┘  └────┘           │
│                                                                    │
│   • Messages are NEVER modified (immutable)                        │
│   • Messages are NEVER deleted (until retention expires)           │
│   • New messages ONLY added at the end                             │
│   • This makes writes O(1) - blazing fast!                         │
│                                                                    │
└───────────────────────────────────────────────────────────────────┘
```

### Segment Files

Partitions are split into **segment files**:

```
Partition 0 Directory:
├── 00000000000000000000.log    ← Segment 1 (offsets 0-999)
├── 00000000000000000000.index  ← Index for segment 1
├── 00000000000000001000.log    ← Segment 2 (offsets 1000-1999)
├── 00000000000000001000.index  ← Index for segment 2
└── 00000000000000002000.log    ← Active segment (currently writing)

Why segments?
• Easier to delete old data (delete whole file)
• Efficient indexing
• Parallel I/O operations
```

### Index Structure

```
.index file (sparse index):
┌─────────────────────────────┐
│ Offset  │ Position in .log  │
├─────────────────────────────┤
│   0     │      0            │
│   100   │    8234           │
│   200   │   16502           │
│   300   │   24891           │
└─────────────────────────────┘

To find offset 150:
1. Binary search index → find 100 (position 8234)
2. Sequential scan from 8234 until offset 150
```

### Consumer Offset Management

```
__consumer_offsets (internal topic)
┌────────────────────────────────────────────────────────┐
│  Group ID    │  Topic     │  Partition  │  Offset      │
├────────────────────────────────────────────────────────┤
│  order-svc   │  orders    │      0      │    1542      │
│  order-svc   │  orders    │      1      │    1238      │
│  order-svc   │  orders    │      2      │    1891      │
│  analytics   │  orders    │      0      │    1200      │
└────────────────────────────────────────────────────────┘

Each consumer group tracks its own position independently!
```

---

## Python Simulations

These scripts simulate Kafka's core concepts WITHOUT needing a real Kafka cluster. **Learn by building Kafka's internals from scratch!**

📖 **[Read the full Simulations Guide →](./simulations/README.md)**

### What You'll Build

| Script | Concept | What You Learn |
|--------|---------|----------------|
| `01_commit_log.py` | Append-only log | Why Kafka writes are O(1) |
| `02_partitioning.py` | Hash partitioning | How ordering is guaranteed |
| `03_consumer_groups.py` | Group coordination | Rebalancing & parallelism |
| `04_replication.py` | Leader-follower | Fault tolerance & ISR |

### Quick Start

```bash
# No Kafka needed! Just Python 3.7+
cd simulations
python 01_commit_log.py
python 02_partitioning.py
python 03_consumer_groups.py
python 04_replication.py
```

### Directory Structure

```
module-02-kafka/
├── README.md
├── simulations/
│   ├── README.md               ← 📖 Detailed simulation guide
│   ├── 01_commit_log.py        ← Simulate append-only log
│   ├── 02_partitioning.py      ← Simulate partition assignment
│   ├── 03_consumer_groups.py   ← Simulate consumer group coordination
│   └── 04_replication.py       ← Simulate leader-follower replication
├── real_kafka/
│   ├── docker-compose.yml      ← Spin up local Kafka
│   ├── producer_example.py     ← Real Kafka producer
│   └── consumer_example.py     ← Real Kafka consumer
└── use_case/
    ├── README.md               ← Order processing architecture
    ├── order_producer.py       ← Order processing example
    ├── order_consumer.py
    ├── inventory_consumer.py
    └── analytics_consumer.py
```

---

## Using Real Kafka with Python

### Installation

```bash
# Install kafka-python library
pip install kafka-python

# Or use confluent-kafka (higher performance)
pip install confluent-kafka
```

### Quick Start with Docker

```yaml
# docker-compose.yml
version: '3'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:latest
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```

```bash
# Start Kafka
docker-compose up -d
```

### Basic Producer

```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8') if k else None
)

# Send a message
producer.send(
    topic='orders',
    key='user-123',
    value={'item': 'laptop', 'price': 999, 'quantity': 1}
)

# Ensure all messages are sent
producer.flush()
```

### Basic Consumer

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'orders',
    bootstrap_servers=['localhost:9092'],
    group_id='order-processor',
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    print(f"Received: {message.value}")
    print(f"  Topic: {message.topic}")
    print(f"  Partition: {message.partition}")
    print(f"  Offset: {message.offset}")
```

See the `real_kafka/` folder for complete examples.

---

## Use Case: Real-Time Order Processing

### Architecture

```
                           KAFKA CLUSTER
┌──────────────────────────────────────────────────────────────────┐
│                                                                   │
│                        Topic: "orders"                            │
│              ┌────────────────────────────────┐                   │
│              │  P0  │  P1  │  P2  │  P3      │                   │
│              └────────────────────────────────┘                   │
│                              │                                    │
└──────────────────────────────┼────────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌───────────────┐    ┌─────────────────┐    ┌────────────────┐
│ Order Service │    │ Inventory Svc   │    │ Analytics Svc  │
│ (Consumer     │    │ (Consumer       │    │ (Consumer      │
│  Group A)     │    │  Group B)       │    │  Group C)      │
│               │    │                 │    │                │
│ • Validate    │    │ • Update stock  │    │ • Calculate    │
│ • Process     │    │ • Alert if low  │    │   metrics      │
│ • Confirm     │    │                 │    │ • Dashboard    │
└───────────────┘    └─────────────────┘    └────────────────┘
```

### Benefits

1. **Decoupling**: Services don't know about each other
2. **Scalability**: Add more consumers as load increases
3. **Fault Tolerance**: If analytics dies, orders still process
4. **Replay**: Reprocess events if needed (rewind offset)

See the `use_case/` folder for complete implementation.

---

## Interview Questions

### Conceptual Questions

**Q: How does Kafka achieve high throughput?**
```
1. Sequential I/O (append-only log)
2. Zero-copy data transfer
3. Batching messages
4. Compression
5. Partition-based parallelism
```

**Q: What happens when a broker fails?**
```
1. ZooKeeper/KRaft detects failure
2. Followers of partitions led by failed broker compete
3. In-Sync Replica (ISR) with latest data becomes new leader
4. Producers/Consumers automatically switch to new leader
5. When broker recovers, it rejoins as follower and catches up
```

**Q: How do you guarantee message ordering?**
```
• Messages within a SINGLE partition are strictly ordered
• Use the same key for related messages (same key → same partition)
• For global ordering: use single partition (sacrifices parallelism)
```

**Q: Explain at-least-once vs exactly-once delivery**
```
At-least-once:
• Consumer commits offset AFTER processing
• If crash before commit → message reprocessed
• Safe but may have duplicates

At-most-once:
• Consumer commits offset BEFORE processing
• If crash after commit → message lost
• No duplicates but may lose messages

Exactly-once:
• Kafka 0.11+ supports idempotent producers
• Transactional producers for atomic writes
• Requires consumer-side deduplication typically
```

### Design Questions

**Q: Design a real-time analytics pipeline**
```
┌─────────┐    ┌───────┐    ┌─────────────┐    ┌──────────┐
│ Web App │───▶│ Kafka │───▶│ Spark/Flink │───▶│ Dashboard│
│ Events  │    │       │    │ Streaming   │    │          │
└─────────┘    └───────┘    └─────────────┘    └──────────┘
                   │
                   ▼
              ┌─────────┐
              │ S3/HDFS │
              │ (batch) │
              └─────────┘
```

**Q: How would you handle message processing failures?**
```
1. Dead Letter Queue (DLQ)
   - Failed messages → separate topic
   - Retry later or manual intervention

2. Retry Topic
   - topic.retry.1 (wait 1 min)
   - topic.retry.2 (wait 5 min)
   - topic.retry.3 (wait 15 min)
   - After all retries → DLQ

3. Transactional Processing
   - Only commit offset if processing succeeds
   - But handle duplicates (idempotency)
```

---

## Summary

| Concept | Key Point |
|---------|-----------|
| **Topic** | Category of messages |
| **Partition** | Unit of parallelism, ordered log |
| **Offset** | Position in partition |
| **Producer** | Writes to topics |
| **Consumer** | Reads from topics |
| **Consumer Group** | Parallel consumers sharing work |
| **Broker** | Kafka server |
| **Replication** | Copies for fault tolerance |
| **Leader/Follower** | Only leader serves requests |

---

## Next Steps

1. **Run the simulations** in `simulations/` folder
2. **Set up local Kafka** with Docker
3. **Build the order processing** use case
4. **Experiment** with different configurations

---

*Kafka is the backbone of modern event-driven architectures. Master it, and you'll understand how companies like LinkedIn, Uber, and Netflix handle billions of events daily.*
