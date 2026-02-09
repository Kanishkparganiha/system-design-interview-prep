"""
Kafka Partitioning Simulation
==============================
This script simulates how Kafka assigns messages to partitions.

Key concepts demonstrated:
1. Hash-based partitioning (key → partition)
2. Round-robin partitioning (no key)
3. Custom partitioners
4. Partition ordering guarantees

Run: python 02_partitioning.py
"""

import hashlib
from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class ProducerRecord:
    """Represents a message to be sent to Kafka"""
    topic: str
    key: Optional[str]
    value: Any
    partition: Optional[int] = None  # Can be explicitly set


class Partitioner:
    """Base partitioner class"""

    def partition(self, key: Optional[str], num_partitions: int) -> int:
        raise NotImplementedError


class DefaultPartitioner(Partitioner):
    """
    Simulates Kafka's default partitioner:
    - If key is provided: hash(key) % num_partitions
    - If no key: round-robin across partitions
    """

    def __init__(self):
        self.round_robin_counter = 0

    def partition(self, key: Optional[str], num_partitions: int) -> int:
        if key is not None:
            # Hash-based partitioning
            # Using murmur2 hash in real Kafka, we'll use MD5 for simplicity
            key_bytes = key.encode('utf-8')
            hash_value = int(hashlib.md5(key_bytes).hexdigest(), 16)
            return hash_value % num_partitions
        else:
            # Round-robin for null keys
            partition = self.round_robin_counter % num_partitions
            self.round_robin_counter += 1
            return partition


class StickyPartitioner(Partitioner):
    """
    Simulates Kafka's sticky partitioner (default since Kafka 2.4):
    - Batches messages to the same partition until batch is full
    - Reduces latency by filling batches faster
    """

    def __init__(self, batch_size: int = 3):
        self.batch_size = batch_size
        self.current_partition = 0
        self.current_batch_count = 0

    def partition(self, key: Optional[str], num_partitions: int) -> int:
        if key is not None:
            # Keys always use hash-based partitioning
            key_bytes = key.encode('utf-8')
            hash_value = int(hashlib.md5(key_bytes).hexdigest(), 16)
            return hash_value % num_partitions

        # Sticky behavior for null keys
        partition = self.current_partition
        self.current_batch_count += 1

        if self.current_batch_count >= self.batch_size:
            # Move to next partition
            self.current_partition = (self.current_partition + 1) % num_partitions
            self.current_batch_count = 0

        return partition


class Topic:
    """Simulates a Kafka topic with multiple partitions"""

    def __init__(self, name: str, num_partitions: int):
        self.name = name
        self.num_partitions = num_partitions
        self.partitions: Dict[int, List[Dict]] = {
            i: [] for i in range(num_partitions)
        }

    def append(self, partition: int, record: Dict):
        """Append a record to a partition"""
        self.partitions[partition].append(record)

    def get_partition(self, partition: int) -> List[Dict]:
        """Get all records in a partition"""
        return self.partitions[partition]

    def stats(self) -> Dict:
        """Get distribution statistics"""
        return {
            f"partition-{i}": len(records)
            for i, records in self.partitions.items()
        }


class Producer:
    """Simulates a Kafka producer"""

    def __init__(self, partitioner: Optional[Partitioner] = None):
        self.partitioner = partitioner or DefaultPartitioner()
        self.topics: Dict[str, Topic] = {}

    def register_topic(self, topic: Topic):
        """Register a topic with this producer"""
        self.topics[topic.name] = topic

    def send(self, record: ProducerRecord) -> int:
        """
        Send a record to the topic.
        Returns the partition the record was sent to.
        """
        topic = self.topics.get(record.topic)
        if not topic:
            raise ValueError(f"Unknown topic: {record.topic}")

        # Determine partition
        if record.partition is not None:
            # Explicitly specified partition
            partition = record.partition
        else:
            # Use partitioner
            partition = self.partitioner.partition(
                record.key,
                topic.num_partitions
            )

        # Append to partition
        topic.append(partition, {
            "key": record.key,
            "value": record.value,
            "partition": partition
        })

        return partition


def demo_hash_partitioning():
    """Demonstrate hash-based partitioning"""

    print("=" * 60)
    print("HASH-BASED PARTITIONING")
    print("=" * 60)
    print()
    print("Same key ALWAYS goes to same partition!")
    print()

    topic = Topic("user-events", num_partitions=4)
    producer = Producer(DefaultPartitioner())
    producer.register_topic(topic)

    # Send events for different users
    events = [
        ("user-alice", "login"),
        ("user-bob", "purchase"),
        ("user-alice", "view_product"),
        ("user-charlie", "login"),
        ("user-bob", "logout"),
        ("user-alice", "logout"),
        ("user-charlie", "purchase"),
        ("user-bob", "login"),
    ]

    print("Sending events:")
    print("-" * 40)
    user_partitions = {}

    for key, event in events:
        record = ProducerRecord(topic="user-events", key=key, value=event)
        partition = producer.send(record)

        if key not in user_partitions:
            user_partitions[key] = partition

        print(f"  key={key:15} event={event:15} → partition {partition}")

    print()
    print("Observation:")
    print("-" * 40)
    for user, partition in user_partitions.items():
        print(f"  {user} always goes to partition {partition}")

    print()
    print("Why this matters:")
    print("  • All events for a user are in the same partition")
    print("  • Events are ORDERED within a partition")
    print("  • Perfect for maintaining per-user event ordering!")
    print()

    return topic


def demo_roundrobin_partitioning():
    """Demonstrate round-robin partitioning (null keys)"""

    print("=" * 60)
    print("ROUND-ROBIN PARTITIONING (null keys)")
    print("=" * 60)
    print()
    print("When key is None, messages are distributed evenly.")
    print()

    topic = Topic("metrics", num_partitions=3)
    producer = Producer(DefaultPartitioner())
    producer.register_topic(topic)

    # Send metrics without keys
    print("Sending 9 messages without keys:")
    print("-" * 40)

    for i in range(9):
        record = ProducerRecord(topic="metrics", key=None, value=f"metric-{i}")
        partition = producer.send(record)
        print(f"  message={record.value} → partition {partition}")

    print()
    print("Distribution:", topic.stats())
    print()
    print("Result: Even distribution across partitions!")
    print()

    return topic


def demo_sticky_partitioning():
    """Demonstrate sticky partitioning"""

    print("=" * 60)
    print("STICKY PARTITIONING (Kafka 2.4+)")
    print("=" * 60)
    print()
    print("Messages without keys stick to one partition until batch is full.")
    print("This improves batching efficiency and reduces latency.")
    print()

    topic = Topic("logs", num_partitions=3)
    producer = Producer(StickyPartitioner(batch_size=3))
    producer.register_topic(topic)

    print("Sending 9 messages (batch_size=3):")
    print("-" * 40)

    for i in range(9):
        record = ProducerRecord(topic="logs", key=None, value=f"log-{i}")
        partition = producer.send(record)
        print(f"  message={record.value} → partition {partition}")

        if (i + 1) % 3 == 0:
            print("  --- batch full, switching partition ---")

    print()
    print("Distribution:", topic.stats())
    print()


def demo_partition_ordering():
    """Demonstrate ordering guarantees within partitions"""

    print("=" * 60)
    print("PARTITION ORDERING GUARANTEES")
    print("=" * 60)
    print()

    topic = Topic("orders", num_partitions=2)
    producer = Producer(DefaultPartitioner())
    producer.register_topic(topic)

    # Send order lifecycle events
    order_events = [
        ("order-123", {"event": "created", "seq": 1}),
        ("order-456", {"event": "created", "seq": 1}),
        ("order-123", {"event": "paid", "seq": 2}),
        ("order-123", {"event": "shipped", "seq": 3}),
        ("order-456", {"event": "paid", "seq": 2}),
        ("order-123", {"event": "delivered", "seq": 4}),
        ("order-456", {"event": "shipped", "seq": 3}),
    ]

    print("Sending order lifecycle events:")
    print("-" * 40)

    for key, value in order_events:
        record = ProducerRecord(topic="orders", key=key, value=value)
        partition = producer.send(record)
        print(f"  {key} → {value['event']:12} (seq={value['seq']}) → P{partition}")

    print()
    print("Partition contents:")
    print("-" * 40)

    for partition_id in range(topic.num_partitions):
        records = topic.get_partition(partition_id)
        print(f"\nPartition {partition_id}:")
        for r in records:
            print(f"  {r['key']} → {r['value']['event']} (seq={r['value']['seq']})")

    print()
    print("GUARANTEE: Within each partition, events are in the order they were sent!")
    print("           order-123: created → paid → shipped → delivered")
    print()


def demo_explicit_partition():
    """Demonstrate explicit partition assignment"""

    print("=" * 60)
    print("EXPLICIT PARTITION ASSIGNMENT")
    print("=" * 60)
    print()
    print("You can explicitly specify which partition to use.")
    print()

    topic = Topic("priority-queue", num_partitions=3)
    producer = Producer(DefaultPartitioner())
    producer.register_topic(topic)

    # Partition 0 = High priority
    # Partition 1 = Medium priority
    # Partition 2 = Low priority

    tasks = [
        (0, "CRITICAL: Server down!"),
        (2, "Low: Update docs"),
        (1, "Medium: Fix typo"),
        (0, "CRITICAL: Data loss!"),
        (2, "Low: Refactor code"),
        (1, "Medium: Add feature"),
    ]

    print("Sending tasks with explicit partitions:")
    print("-" * 40)

    for partition, task in tasks:
        record = ProducerRecord(
            topic="priority-queue",
            key=None,
            value=task,
            partition=partition
        )
        producer.send(record)
        priority = ["HIGH", "MEDIUM", "LOW"][partition]
        print(f"  [{priority:6}] {task}")

    print()
    print("Partition contents:")
    print("-" * 40)
    priorities = ["HIGH", "MEDIUM", "LOW"]
    for partition_id in range(3):
        print(f"\nPartition {partition_id} ({priorities[partition_id]} priority):")
        for r in topic.get_partition(partition_id):
            print(f"  • {r['value']}")


def main():
    demo_hash_partitioning()
    print("\n" + "=" * 60 + "\n")

    demo_roundrobin_partitioning()
    print("\n" + "=" * 60 + "\n")

    demo_sticky_partitioning()
    print("\n" + "=" * 60 + "\n")

    demo_partition_ordering()
    print("\n" + "=" * 60 + "\n")

    demo_explicit_partition()

    print("\n" + "=" * 60)
    print("KEY TAKEAWAYS")
    print("=" * 60)
    print("""
    1. Same key → Same partition (guaranteed)
    2. Ordering guaranteed WITHIN a partition only
    3. No key → Round-robin or sticky distribution
    4. More partitions = More parallelism
    5. Can explicitly assign partitions for special cases
    """)


if __name__ == "__main__":
    main()
