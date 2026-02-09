# Kafka Simulations: Learn by Building

> Understand Kafka internals by implementing them from scratch in Python — no Kafka installation required!

---

## Why Simulations?

The best way to understand a distributed system is to **build it yourself**. These Python scripts simulate Kafka's core mechanisms, helping you:

- **Visualize** how Kafka works internally
- **Experiment** without setting up infrastructure
- **Prepare** for system design interviews
- **Debug** mental models of distributed systems

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         WHAT YOU'LL BUILD                                 │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│   01_commit_log.py      →  The append-only log (Kafka's core)            │
│   02_partitioning.py    →  How messages route to partitions              │
│   03_consumer_groups.py →  Consumer coordination & rebalancing           │
│   04_replication.py     →  Fault tolerance via leader-follower           │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

```bash
# No dependencies needed! Just Python 3.7+
cd simulations

# Run each simulation
python 01_commit_log.py
python 02_partitioning.py
python 03_consumer_groups.py
python 04_replication.py
```

---

## Simulation 1: The Commit Log

**File:** `01_commit_log.py`

### What is the Commit Log?

The commit log is Kafka's foundational data structure — an **append-only, ordered sequence of messages**. Every partition in Kafka is essentially a commit log.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          COMMIT LOG                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   Offset:   0      1      2      3      4      5      6                 │
│           ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐             │
│           │Msg1│ │Msg2│ │Msg3│ │Msg4│ │Msg5│ │Msg6│ │    │ ──▶ Append  │
│           └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘             │
│                                                                          │
│   Properties:                                                            │
│   ✓ Append-only (O(1) writes)                                           │
│   ✓ Immutable (messages never modified)                                  │
│   ✓ Ordered (by offset)                                                  │
│   ✓ Persistent (survives restarts)                                       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### What This Simulation Covers

| Concept | Description | Why It Matters |
|---------|-------------|----------------|
| **Append-only writes** | New messages only added at the end | O(1) write performance |
| **Offset tracking** | Each message gets a unique sequential ID | Consumers track position |
| **Segment files** | Log split into files by size/time | Efficient cleanup & indexing |
| **Immutability** | Messages are never modified | Safe replication, multiple readers |

### Key Classes

```python
class Message:
    """A single message with offset, timestamp, key, value"""
    offset: int
    timestamp: float
    key: Optional[str]
    value: Any

class Segment:
    """A portion of the log (like a .log file in Kafka)"""
    base_offset: int
    messages: List[Message]
    is_active: bool  # Only one segment is active for writes

class CommitLog:
    """The complete log for one partition"""
    segments: List[Segment]
    current_offset: int

    def append(key, value) -> int:  # Returns offset
    def read(offset) -> Message
    def read_from(start_offset, count) -> List[Message]
```

### Run It

```bash
$ python 01_commit_log.py

📝 PRODUCING MESSAGES
  Written: offset=0, key=user-1, order_id=A001
  Written: offset=1, key=user-2, order_id=A002
  ...

📁 Created new segment starting at offset 5

📖 READING INDIVIDUAL MESSAGES
  Offset 0: key=user-1, value={...}
  Offset 3: key=user-3, value={...}

🚚 CONSUMER READING (starting from offset 3)
  Consumed: offset=3, key=user-3
  Consumed: offset=4, key=user-2
  ...
```

### Interview Insights

> **Q: Why is Kafka so fast for writes?**
>
> A: Append-only writes are O(1). No random seeks, no index updates. Just append to the end of a file. This is why Kafka can handle millions of messages per second.

---

## Simulation 2: Partitioning

**File:** `02_partitioning.py`

### How Does Partitioning Work?

Partitioning is how Kafka achieves parallelism and ordering guarantees.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         PARTITIONING                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   Producer sends message with key="user-123"                             │
│                     │                                                    │
│                     ▼                                                    │
│              ┌─────────────┐                                             │
│              │   hash(key) │                                             │
│              │   % 3 = 1   │  ← Deterministic!                          │
│              └─────────────┘                                             │
│                     │                                                    │
│         ┌──────────┬┴─────────┐                                          │
│         ▼          ▼          ▼                                          │
│     Partition 0  Partition 1  Partition 2                                │
│                      ▲                                                   │
│                      │                                                   │
│            user-123 always goes here!                                    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### What This Simulation Covers

| Concept | Description | Why It Matters |
|---------|-------------|----------------|
| **Hash partitioning** | Same key → same partition | Ordering guarantee per key |
| **Round-robin** | No key → even distribution | Load balancing |
| **Sticky partitioning** | Batch to same partition | Better batching efficiency |
| **Custom partitioners** | Your logic decides | Priority queues, geo-routing |

### Key Classes

```python
class DefaultPartitioner:
    """Kafka's default partitioning logic"""

    def partition(key, num_partitions) -> int:
        if key is not None:
            return hash(key) % num_partitions  # Deterministic
        else:
            return self.round_robin_counter++ % num_partitions

class StickyPartitioner:
    """Kafka 2.4+ default for null keys"""

    def partition(key, num_partitions) -> int:
        if key is not None:
            return hash(key) % num_partitions
        # Stick to current partition until batch is full
        if self.batch_count >= self.batch_size:
            self.current_partition = (self.current_partition + 1) % num_partitions
            self.batch_count = 0
        return self.current_partition
```

### Run It

```bash
$ python 02_partitioning.py

HASH-BASED PARTITIONING
  key=user-alice    event=login           → partition 2
  key=user-bob      event=purchase        → partition 0
  key=user-alice    event=view_product    → partition 2  ← Same!
  key=user-alice    event=logout          → partition 2  ← Same!

Observation:
  user-alice always goes to partition 2
  user-bob always goes to partition 0
```

### Interview Insights

> **Q: How do you guarantee ordering in Kafka?**
>
> A: Ordering is guaranteed ONLY within a partition. Use the same key for messages that need ordering. All events for `user-123` will be in the same partition, in order.

---

## Simulation 3: Consumer Groups

**File:** `03_consumer_groups.py`

### How Do Consumer Groups Work?

Consumer groups enable parallel consumption while ensuring each message is processed exactly once per group.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       CONSUMER GROUPS                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   Topic: orders (4 partitions)                                           │
│   ┌────┐ ┌────┐ ┌────┐ ┌────┐                                           │
│   │ P0 │ │ P1 │ │ P2 │ │ P3 │                                           │
│   └──┬─┘ └──┬─┘ └──┬─┘ └──┬─┘                                           │
│      │      │      │      │                                              │
│      │      │      │      │                                              │
│   ┌──┴──────┴──────┴──────┴──────────────────────────────────────┐      │
│   │           Consumer Group: "order-service"                     │      │
│   ├───────────────────────────────────────────────────────────────┤      │
│   │                                                               │      │
│   │   Consumer-1 ◄── P0, P1                                       │      │
│   │   Consumer-2 ◄── P2, P3                                       │      │
│   │                                                               │      │
│   │   Rule: Each partition → exactly ONE consumer                 │      │
│   │                                                               │      │
│   └───────────────────────────────────────────────────────────────┘      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### What This Simulation Covers

| Concept | Description | Why It Matters |
|---------|-------------|----------------|
| **Partition assignment** | Which consumer gets which partition | Parallelism control |
| **Rebalancing** | Redistribution when consumers join/leave | Fault tolerance |
| **Consumer groups** | Independent consumption of same topic | Multiple use cases |
| **Offset tracking** | Each group tracks its own position | Independent progress |

### Rebalancing Visualized

```
Initial: 3 consumers, 6 partitions
─────────────────────────────────────
Consumer-1: [P0, P1]
Consumer-2: [P2, P3]
Consumer-3: [P4, P5]

Consumer-2 crashes! 💥 Rebalancing...
─────────────────────────────────────
Consumer-1: [P0, P1, P2]
Consumer-3: [P3, P4, P5]

Consumer-4 joins! 🆕 Rebalancing...
─────────────────────────────────────
Consumer-1: [P0, P1]
Consumer-3: [P2, P3]
Consumer-4: [P4, P5]
```

### Key Classes

```python
class ConsumerGroup:
    """Simulates Kafka's consumer group coordination"""

    def __init__(group_id, strategy):
        self.consumers = {}
        self.subscribed_topics = {}

    def add_consumer(consumer_id) -> Consumer:
        # Add and trigger rebalance
        self._rebalance()

    def remove_consumer(consumer_id):
        # Remove and trigger rebalance
        self._rebalance()

    def _rebalance():
        # Redistribute partitions among consumers
        if strategy == ROUND_ROBIN:
            # Distribute evenly
        elif strategy == RANGE:
            # Assign contiguous ranges
```

### Run It

```bash
$ python 03_consumer_groups.py

BASIC CONSUMER GROUP
  ➕ Consumer 'consumer-1' joining group

  🔄 REBALANCING GROUP
    consumer-1: Partitions [0, 1, 2, 3, 4, 5]

  ➕ Consumer 'consumer-2' joining group

  🔄 REBALANCING GROUP
    consumer-1: Partitions [0, 2, 4]
    consumer-2: Partitions [1, 3, 5]

  ➕ Consumer 'consumer-3' joining group

  🔄 REBALANCING GROUP
    consumer-1: Partitions [0, 3]
    consumer-2: Partitions [1, 4]
    consumer-3: Partitions [2, 5]
```

### Interview Insights

> **Q: What's the maximum parallelism for a topic?**
>
> A: The number of partitions. If you have 10 partitions and 15 consumers, 5 consumers will be idle. This is why partition count is a critical design decision.

---

## Simulation 4: Replication

**File:** `04_replication.py`

### How Does Replication Work?

Replication provides fault tolerance. Each partition exists on multiple brokers.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          REPLICATION                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   Partition 0 (Replication Factor = 3)                                   │
│                                                                          │
│   Broker 1              Broker 2              Broker 3                   │
│   ┌─────────────┐       ┌─────────────┐       ┌─────────────┐           │
│   │   LEADER    │       │  FOLLOWER   │       │  FOLLOWER   │           │
│   │             │──────▶│             │       │             │           │
│   │  [0,1,2,3]  │       │  [0,1,2,3]  │◀──────│  [0,1,2,3]  │           │
│   │             │──────────────────────────────▶            │           │
│   └─────────────┘       └─────────────┘       └─────────────┘           │
│         │                                                                │
│         │◀── All reads/writes go through leader                         │
│         │                                                                │
│   Producer/Consumer                                                      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### What This Simulation Covers

| Concept | Description | Why It Matters |
|---------|-------------|----------------|
| **Leader/Follower** | One leader handles all I/O | Consistency guarantee |
| **ISR (In-Sync Replicas)** | Followers caught up with leader | Candidates for leader election |
| **Acks settings** | How many replicas must confirm | Durability vs latency trade-off |
| **Leader election** | Choosing new leader on failure | Automatic failover |

### Acknowledgment Modes

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       PRODUCER ACK MODES                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   acks=0 (Fire and Forget)                                              │
│   ─────────────────────────                                              │
│   Producer ──▶ Leader     Follower     Follower                          │
│      ✓ Done immediately                                                  │
│   ⚡ Fastest, but may lose messages                                      │
│                                                                          │
│   acks=1 (Leader Only)                                                   │
│   ────────────────────                                                   │
│   Producer ──▶ Leader ──▶ Follower     Follower                          │
│      ◀── ACK    ✓          (async)       (async)                         │
│   🔄 Balanced, but may lose if leader fails before replication           │
│                                                                          │
│   acks=all (All ISR)                                                     │
│   ──────────────────                                                     │
│   Producer ──▶ Leader ──▶ Follower ──▶ Follower                          │
│      ◀───── ACK ──────      ✓            ✓                               │
│   🔒 Safest, all ISR must confirm                                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Classes

```python
class Replica:
    """A replica of a partition on a broker"""
    broker_id: int
    is_leader: bool
    is_alive: bool
    log_end_offset: int  # How far this replica has replicated

class Partition:
    """Partition with replication"""
    replicas: Dict[broker_id, Replica]
    isr: Set[broker_id]  # In-Sync Replicas
    leader_broker: int

    def produce(key, value, acks) -> Result:
        if acks == 0:  # Fire and forget
            leader.append(message)
            return success
        elif acks == 1:  # Leader only
            leader.append(message)
            return success if leader.is_alive else failure
        elif acks == -1:  # All ISR
            leader.append(message)
            replicate_to_all_isr()
            return success if all_isr_acked else failure

    def fail_broker(broker_id):
        replica.is_alive = False
        isr.remove(broker_id)
        if broker_id == leader_broker:
            _elect_new_leader()  # Choose from ISR
```

### Run It

```bash
$ python 04_replication.py

KAFKA REPLICATION BASICS
  Partition 0:
    Leader: Broker-1
    ISR: [1, 2, 3]
    Replicas:
      Broker-1(LEADER, UP, LEO=3)
      Broker-2(follower, UP, LEO=3)
      Broker-3(follower, UP, LEO=3)

💥 BROKER-1 (Leader) CRASHES!

  🔄 LEADER ELECTION for orders-0
  ✅ Broker-2 elected as new leader

After failure:
  Partition 0:
    Leader: Broker-2
    ISR: [2, 3]
```

### Interview Insights

> **Q: How does Kafka handle broker failures?**
>
> A: When a leader fails, one of the In-Sync Replicas (ISR) is elected as the new leader. Producers and consumers automatically discover the new leader. No manual intervention required.

---

## Learning Path

```
Recommended Order:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   01_commit_log.py          Understanding the foundation
         │
         ▼
   02_partitioning.py        How data is distributed
         │
         ▼
   03_consumer_groups.py     How data is consumed
         │
         ▼
   04_replication.py         How data survives failures
         │
         ▼
   ../real_kafka/            Use the real thing!
         │
         ▼
   ../use_case/              Build a complete system!
```

---

## Key Takeaways

| Simulation | Core Concept | Interview Sound Bite |
|------------|--------------|---------------------|
| Commit Log | Append-only, immutable | "Kafka is fast because writes are O(1) appends" |
| Partitioning | Hash key → partition | "Same key = same partition = ordered" |
| Consumer Groups | Partition:Consumer = 1:1 | "Max parallelism = partition count" |
| Replication | Leader handles I/O, followers replicate | "ISR = candidates for leader election" |

---

## Video Resource

For a visual explanation of Kafka concepts, watch this excellent video:

📺 **[Apache Kafka Explained](https://youtu.be/DU8o-OTeoCc?si=dlKHJkV5AG5Kp-Mt)**

---

## Next Steps

After running these simulations:

1. **Set up real Kafka**: `cd ../real_kafka && docker-compose up -d`
2. **Run producer/consumer examples**: `python producer_example.py`
3. **Build the order processing system**: `cd ../use_case`

---

*Understanding the internals makes you a better Kafka user. Now go build something!*
